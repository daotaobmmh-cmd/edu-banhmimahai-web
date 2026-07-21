const NOTION_VERSION = '2025-09-03';

module.exports = async function handler(req, res) {
  if (req.method === 'OPTIONS') {
    res.setHeader('Allow', 'POST, OPTIONS');
    return res.status(204).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ ok: false, error: 'Method Not Allowed' });
  }

  const NOTION_TOKEN = process.env.NOTION_TOKEN;
  const NOTION_FEEDBACK_DATA_SOURCE_ID = process.env.NOTION_FEEDBACK_DATA_SOURCE_ID;

  console.log('DEBUG ENV:', { 
    token_len: NOTION_TOKEN ? NOTION_TOKEN.length : 0, 
    id_len: NOTION_FEEDBACK_DATA_SOURCE_ID ? NOTION_FEEDBACK_DATA_SOURCE_ID.length : 0 
  });

  if (!NOTION_TOKEN || !NOTION_FEEDBACK_DATA_SOURCE_ID) {
    return res.status(503).json({ ok: false, error: 'Feedback endpoint setup missing.' });
  }

  const body = req.body || {};
  const feedbackText = String(body.feedbackText || '').trim().slice(0, 1000);
  const learnerName = String(body.learnerName || '').trim().slice(0, 100);
  const stableId = String(body.stableId || '').trim();
  const displayNumber = String(body.displayNumber || '').trim();
  const sectionNo = String(body.sectionNo || '').trim();
  const sectionName = String(body.sectionName || '').trim().slice(0, 100);
  const questionText = String(body.questionText || '').trim().slice(0, 500);
  const selectedAnswer = String(body.selectedAnswer || '').trim();
  const correctAnswer = String(body.correctAnswer || '').trim();
  const mode = String(body.mode || '').trim();
  const pageUrl = String(body.pageUrl || '').trim().slice(0, 500);
  const submittedAt = String(body.submittedAt || new Date().toISOString()).trim();

  if (!feedbackText || !learnerName || !stableId || !questionText) {
    return res.status(400).json({ ok: false, error: 'Thiếu thông tin bắt buộc.' });
  }

  const notionPayload = {
    parent: { type: 'database_id', database_id: NOTION_FEEDBACK_DATA_SOURCE_ID },
    properties: {
      'Góp ý': { title: [{ type: 'text', text: { content: feedbackText } }] },
      'Trạng thái': { status: { name: 'Mới' } },
      'Người học': { rich_text: [{ type: 'text', text: { content: learnerName } }] },
      'Stable ID': { rich_text: [{ type: 'text', text: { content: stableId } }] },
      'Số câu': { number: Number(displayNumber) || 0 },
      'Phần số': { number: Number(sectionNo) || 0 },
      'Tên phần': { rich_text: [{ type: 'text', text: { content: sectionName } }] },
      'Câu hỏi snapshot': { rich_text: [{ type: 'text', text: { content: questionText } }] },
      'Đáp án đã chọn': { rich_text: [{ type: 'text', text: { content: selectedAnswer } }] },
      'Đáp án đúng': { rich_text: [{ type: 'text', text: { content: correctAnswer } }] },
      'Chế độ': { select: { name: mode === 'test' ? 'Thi' : 'Luyện tập' } },
      'URL': { url: pageUrl.startsWith('http') ? pageUrl : null },
      'Thời gian gửi': { date: { start: submittedAt } }
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
      console.error('Notion feedback error', response.status, detail.slice(0, 500));
      return res.status(502).json({ ok: false, error: 'Không thể lưu góp ý vào Notion.' });
    }

    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Fetch error:', err);
    return res.status(500).json({ ok: false, error: 'Internal Server Error' });
  }
};
