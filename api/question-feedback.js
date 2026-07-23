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

  // Exact matching for Vercel preview or production host, no loose includes
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
  const NOTION_FEEDBACK_DATA_SOURCE_ID = process.env.NOTION_FEEDBACK_DATA_SOURCE_ID;

  if (!NOTION_TOKEN || !NOTION_FEEDBACK_DATA_SOURCE_ID) {
    return res.status(503).json({ ok: false, error: 'Feedback endpoint setup missing.' });
  }


  const body = req.body || {};
  const rawFeedbackText = String(body.feedbackText || '').trim();
  if (rawFeedbackText.length > 1000) {
    return res.status(400).json({ ok: false, error: 'Góp ý không được vượt quá 1000 ký tự.' });
  }
  const feedbackText = rawFeedbackText;
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
    parent: { database_id: NOTION_FEEDBACK_DATA_SOURCE_ID },
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

function parseRetryAfterMs(headerVal) {
  if (!headerVal) return null;
  const parsedInt = parseInt(headerVal, 10);
  if (!isNaN(parsedInt) && parsedInt >= 0) {
    return parsedInt * 1000;
  }
  const parsedDate = Date.parse(headerVal);
  if (!isNaN(parsedDate)) {
    const diff = parsedDate - Date.now();
    return diff > 0 ? diff : 1000;
  }
  return null;
}

async function fetchWithRetry(url, options = {}, maxRetries = 10, timeoutMs = 12000) {
  let attempt = 0;
  let lastError = null;

  while (attempt <= maxRetries) {
    attempt++;
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);

    try {
      const fetchFn = global.customFetch || fetch;
      const res = await fetchFn(url, { ...options, signal: controller.signal });
      clearTimeout(timer);

      if (res.ok) {
        return res;
      }

      const isRetryable = res.status === 429 || res.status === 409 || (res.status >= 500 && res.status <= 599);
      if (!isRetryable || attempt > maxRetries) {
        return res;
      }

      let delayMs = 200 * Math.pow(2, attempt - 1) + Math.floor(Math.random() * 100);
      const retryAfterHeader = (res.headers && typeof res.headers.get === 'function') ? res.headers.get('retry-after') : null;
      const parsedDelay = parseRetryAfterMs(retryAfterHeader);
      if (parsedDelay !== null) {
        delayMs = Math.min(parsedDelay + Math.floor(Math.random() * 300), 10000);
      }

      await new Promise(resolve => setTimeout(resolve, delayMs));
    } catch (err) {
      clearTimeout(timer);
      lastError = err;

      if (attempt > maxRetries) {
        throw err;
      }

      const delayMs = 250 * Math.pow(2, attempt - 1) + Math.floor(Math.random() * 100);
      await new Promise(resolve => setTimeout(resolve, delayMs));
    }
  }

  if (lastError) throw lastError;
  throw new Error('Request failed after retries.');
}

  try {
    const response = await fetchWithRetry('https://api.notion.com/v1/pages', {
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
