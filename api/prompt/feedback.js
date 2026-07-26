const NOTION_VERSION = '2022-06-28';

module.exports = async function handler(req, res) {
  const host = req.headers.host || '';
  const originHeader = req.headers.origin || req.headers.referer || '';
  let originHost = '';
  
  if (originHeader) {
    try {
      originHost = new URL(originHeader).host;
    } catch (e) {
      return res.status(403).json({ ok: false, error: 'Invalid Origin.' });
    }
  }

  const isVercelApp = host === 'edu-banhmimahai-web.vercel.app' || (host.startsWith('edu-banhmimahai-web-') && host.endsWith('.vercel.app'));
  const isApprovedHost = isVercelApp || host === 'daotao.banhmimahai.vn' || host.startsWith('localhost:') || host.startsWith('127.0.0.1:');

  if (!isApprovedHost || (originHost && originHost !== host)) {
    return res.status(403).json({ ok: false, error: 'Forbidden.' });
  }

  if (req.method === 'OPTIONS') {
    res.setHeader('Access-Control-Allow-Origin', originHeader || '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    return res.status(204).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ ok: false, error: 'Method Not Allowed' });
  }

  const NOTION_TOKEN = process.env.NOTION_TOKEN;
  const NOTION_FEEDBACK_DATA_SOURCE_ID = process.env.NOTION_PROMPT_FEEDBACK_DATA_SOURCE_ID || process.env.NOTION_FEEDBACK_DATA_SOURCE_ID || '34115a1d78e94d8caec3fab256711f85';

  if (!NOTION_TOKEN) {
    return res.status(503).json({ ok: false, error: 'Feedback endpoint setup missing.' });
  }

  const body = req.body || {};
  const promptId = String(body.promptId || '').trim().slice(0, 40);
  const promptTitle = String(body.promptTitle || '').trim().slice(0, 300);
  const category = ['Hệ thống', 'Lõi', 'Tình huống'].includes(body.category) ? body.category : 'Tình huống';
  const feedback = String(body.feedback || '').trim().slice(0, 1500);
  const source = String(body.source || '').trim().slice(0, 1000);

  if (!promptId || !promptTitle || feedback.length < 5) {
    return res.status(400).json({ ok: false, error: 'Thiếu mã prompt, tên prompt hoặc nội dung góp ý.' });
  }

  const notionPayload = {
    parent: { database_id: NOTION_FEEDBACK_DATA_SOURCE_ID },
    properties: {
      'Tiêu đề': { title: [{ type: 'text', text: { content: `Góp ý ${promptId} · ${promptTitle}`.slice(0, 1900) } }] },
      'Prompt ID': { rich_text: [{ type: 'text', text: { content: promptId } }] },
      'Tên Prompt': { rich_text: [{ type: 'text', text: { content: promptTitle } }] },
      'Nhóm': { select: { name: category } },
      'Nội dung góp ý': { rich_text: [{ type: 'text', text: { content: feedback } }] },
      'Người góp ý': { rich_text: [{ type: 'text', text: { content: 'Đồng nghiệp VSF' } }] },
      'Trạng thái': { status: { name: 'Mới' } },
      ...(source.startsWith('http') ? { 'Nguồn': { url: source } } : {})
    }
  };

  try {
    const response = await fetch('https://api.notion.com/v1/pages', {
      method: 'POST',
      headers: {
        authorization: `Bearer ${NOTION_TOKEN}`,
        'content-type': 'application/json',
        'notion-version': NOTION_VERSION
      },
      body: JSON.stringify(notionPayload)
    });

    if (!response.ok) {
      const detail = await response.text();
      console.error('Notion prompt feedback error', response.status, detail.slice(0, 500));
      return res.status(502).json({ ok: false, error: 'Không thể lưu góp ý vào Notion.' });
    }

    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Fetch error:', err);
    return res.status(500).json({ ok: false, error: 'Internal Server Error' });
  }
};
