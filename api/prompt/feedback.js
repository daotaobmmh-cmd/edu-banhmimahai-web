const NOTION_VERSION = '2022-06-28';

function isAllowedOrigin(originStr, reqHost) {
  if (!originStr) return false;
  let parsed;
  try {
    parsed = new URL(originStr);
  } catch (e) {
    return false;
  }

  const hostname = parsed.hostname;
  const protocol = parsed.protocol;

  // Localhost allowed for dev/test
  if ((hostname === 'localhost' || hostname === '127.0.0.1') && (protocol === 'http:' || protocol === 'https:')) {
    return true;
  }

  if (protocol !== 'https:') return false;

  // Approved domain list
  const isCustomDomain = hostname === 'daotao.banhmimahai.vn';
  const isVercelPrimary = hostname === 'edu-banhmimahai-web.vercel.app';
  const isVercelPreview = (hostname.startsWith('edu-banhmimahai-web-') || hostname.startsWith('edu-banhmimahai-')) && hostname.endsWith('.vercel.app');

  if (!isCustomDomain && !isVercelPrimary && !isVercelPreview) {
    return false;
  }

  // Host match rule for production
  if (reqHost && hostname !== 'localhost' && hostname !== '127.0.0.1') {
    if (parsed.host !== reqHost) {
      return false;
    }
  }

  return true;
}

function isValidHttpsSourceUrl(urlStr) {
  if (!urlStr) return null;
  try {
    const parsed = new URL(urlStr);
    if (parsed.protocol !== 'https:') return null;
    const hn = parsed.hostname;
    const isCustomDomain = hn === 'daotao.banhmimahai.vn';
    const isVercelPrimary = hn === 'edu-banhmimahai-web.vercel.app';
    const isVercelPreview = (hn.startsWith('edu-banhmimahai-web-') || hn.startsWith('edu-banhmimahai-')) && hn.endsWith('.vercel.app');
    if (isCustomDomain || isVercelPrimary || isVercelPreview) {
      return parsed.href;
    }
  } catch (e) {}
  return null;
}

function parseRetryAfterMs(headerVal) {
  if (!headerVal) return null;
  const parsedInt = parseInt(headerVal, 10);
  if (!isNaN(parsedInt) && parsedInt >= 0) return parsedInt * 1000;
  const parsedDate = Date.parse(headerVal);
  if (!isNaN(parsedDate)) {
    const diff = parsedDate - Date.now();
    return diff > 0 ? diff : 1000;
  }
  return null;
}

async function fetchWithRetry(url, options = {}, maxRetries = 3, timeoutMs = 10000) {
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

      if (res.ok) return res;

      const isRetryable = res.status === 429 || res.status === 409 || (res.status >= 500 && res.status <= 599);
      if (!isRetryable || attempt > maxRetries) return res;

      let delayMs = 200 * Math.pow(2, attempt - 1) + Math.floor(Math.random() * 100);
      const retryAfterHeader = (res.headers && typeof res.headers.get === 'function') ? res.headers.get('retry-after') : null;
      const parsedDelay = parseRetryAfterMs(retryAfterHeader);
      if (parsedDelay !== null) {
        delayMs = Math.min(parsedDelay + Math.floor(Math.random() * 300), 5000);
      }

      await new Promise(resolve => setTimeout(resolve, delayMs));
    } catch (err) {
      clearTimeout(timer);
      lastError = err;
      if (attempt > maxRetries) throw err;
      const delayMs = 250 * Math.pow(2, attempt - 1) + Math.floor(Math.random() * 100);
      await new Promise(resolve => setTimeout(resolve, delayMs));
    }
  }

  if (lastError) throw lastError;
  throw new Error('Request failed after retries.');
}

module.exports = async function handler(req, res) {
  const host = req.headers.host || '';
  const originHeader = req.headers.origin || '';
  const refererHeader = req.headers.referer || '';

  let effectiveOrigin = originHeader;
  if (!effectiveOrigin && refererHeader) {
    try {
      effectiveOrigin = new URL(refererHeader).origin;
    } catch (e) {}
  }

  const isLocalhost = host.startsWith('localhost:') || host.startsWith('127.0.0.1:');

  // Production requirement: Must have valid Origin or Referer
  if (!isLocalhost && !originHeader && !refererHeader) {
    return res.status(403).json({ ok: false, error: 'Forbidden.' });
  }

  const validOrigin = isAllowedOrigin(effectiveOrigin, isLocalhost ? '' : host);

  // OPTIONS CORS preflight check
  if (req.method === 'OPTIONS') {
    if (!validOrigin) {
      return res.status(403).json({ ok: false, error: 'Forbidden.' });
    }
    res.setHeader('Access-Control-Allow-Origin', effectiveOrigin);
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    return res.status(204).end();
  }

  // Method check: POST only
  if (req.method !== 'POST') {
    return res.status(405).json({ ok: false, error: 'Method Not Allowed' });
  }

  // Origin check for POST
  if (!validOrigin) {
    return res.status(403).json({ ok: false, error: 'Forbidden.' });
  }

  // Content-Type check
  const contentType = (req.headers['content-type'] || '').toLowerCase();
  if (!contentType.startsWith('application/json')) {
    return res.status(415).json({ ok: false, error: 'Unsupported Media Type.' });
  }

  // Payload size limit check (10KB limit)
  const body = req.body || {};
  const rawBodyStr = JSON.stringify(body);
  if (rawBodyStr.length > 10000) {
    return res.status(413).json({ ok: false, error: 'Payload Too Large.' });
  }

  // Honeypot check
  const hpWebsite = String(body.website || '').trim();
  const hpCompany = String(body.company || '').trim();
  if (hpWebsite || hpCompany) {
    // Drop silently (honeypot triggered)
    return res.status(200).json({ ok: true });
  }

  // Environment variables check (ENV ONLY, NO FALLBACKS, NO HARDCODED IDS)
  const NOTION_TOKEN = process.env.NOTION_TOKEN;
  const NOTION_PROMPT_FEEDBACK_DATA_SOURCE_ID = process.env.NOTION_PROMPT_FEEDBACK_DATA_SOURCE_ID;

  if (!NOTION_TOKEN || !NOTION_PROMPT_FEEDBACK_DATA_SOURCE_ID) {
    return res.status(503).json({ ok: false, error: 'Feedback endpoint setup missing.' });
  }

  // Strict Field Validations
  const promptId = String(body.promptId || '').trim();
  const promptTitle = String(body.promptTitle || '').trim().slice(0, 300);
  const category = String(body.category || '').trim();
  const feedback = String(body.feedback || '').trim();
  const rawSource = String(body.source || '').trim();

  // Pattern check for promptId (alphanumeric, hyphen, underscore up to 40 chars)
  if (!promptId || !/^[a-zA-Z0-9_-]{1,40}$/.test(promptId)) {
    return res.status(400).json({ ok: false, error: 'Mã prompt không hợp lệ.' });
  }

  if (!promptTitle) {
    return res.status(400).json({ ok: false, error: 'Thiếu tên prompt.' });
  }

  // Category must match exact allowlist (no silent conversion)
  const allowedCategories = ['Hệ thống', 'Lõi', 'Tình huống'];
  if (!allowedCategories.includes(category)) {
    return res.status(400).json({ ok: false, error: 'Nhóm prompt không hợp lệ.' });
  }

  // Feedback min 5, max 1500 chars
  if (!feedback || feedback.length < 5 || feedback.length > 1500) {
    return res.status(400).json({ ok: false, error: 'Nội dung góp ý không hợp lệ (tối thiểu 5, tối đa 1500 ký tự).' });
  }

  const validSourceUrl = isValidHttpsSourceUrl(rawSource);

  const notionPayload = {
    parent: { database_id: NOTION_PROMPT_FEEDBACK_DATA_SOURCE_ID },
    properties: {
      'Tiêu đề': { title: [{ type: 'text', text: { content: `Góp ý ${promptId} · ${promptTitle}`.slice(0, 1900) } }] },
      'Prompt ID': { rich_text: [{ type: 'text', text: { content: promptId } }] },
      'Tên Prompt': { rich_text: [{ type: 'text', text: { content: promptTitle } }] },
      'Nhóm': { select: { name: category } },
      'Nội dung góp ý': { rich_text: [{ type: 'text', text: { content: feedback } }] },
      'Người góp ý': { rich_text: [{ type: 'text', text: { content: 'Đồng nghiệp Nhà Má Hải' } }] },
      'Trạng thái': { status: { name: 'Mới' } },
      ...(validSourceUrl ? { 'Nguồn': { url: validSourceUrl } } : {})
    }
  };

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
      console.error('Notion prompt feedback error HTTP:', response.status);
      return res.status(502).json({ ok: false, error: 'Không thể lưu góp ý vào Notion.' });
    }

    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Prompt feedback fetch error:', err.message);
    return res.status(500).json({ ok: false, error: 'Internal Server Error' });
  }
};
