const NOTION_VERSION = '2022-06-28';
const fs = require('fs');
const path = require('path');

const APPROVED_UNITS = [
  "Bộ phận Phát triển Khách hàng hiện hữu",
  "Phòng Marketing",
  "Bộ phận Phát triển nhượng quyền",
  "Phòng Kinh doanh",
  "Nhà máy MHF",
  "Phòng Kho vận",
  "Phòng Hành chính - Nhân sự",
  "Phòng Tài chính - Kế toán",
  "Ban Quản lý Quy trình",
  "VSF University"
];

let canonicalAnswerKey = null;

function getCanonicalAnswerKey() {
  if (canonicalAnswerKey) return canonicalAnswerKey;
  try {
    let filePath = path.join(process.cwd(), 'hoinhap', 'questions.js');
    if (!fs.existsSync(filePath)) {
      filePath = path.join(__dirname, '..', 'hoinhap', 'questions.js');
    }
    const code = fs.readFileSync(filePath, 'utf8');
    const win = {};
    const fn = new Function('window', code);
    fn(win);
    const map = new Map();
    const questions = win.HOINHAP_QUESTIONS || [];
    if (!Array.isArray(questions) || questions.length !== 171) {
      console.error('Canonical dataset length mismatch. Expected 171, got:', questions.length);
      return null;
    }
    for (const q of questions) {
      if (!q || !q.id || (typeof q.id !== 'string' && typeof q.id !== 'number')) {
        return null;
      }
      const qId = String(q.id).trim();
      const ans = String(q.correctAnswer || '').trim().toLowerCase();
      if (!['a', 'b', 'c', 'd'].includes(ans)) {
        return null;
      }
      map.set(qId, ans);
    }
    if (map.size !== 171) {
      console.error('Canonical map size mismatch. Expected 171 unique IDs, got:', map.size);
      return null;
    }
    canonicalAnswerKey = map;
    return map;
  } catch (err) {
    console.error('Failed to load canonical answer key:', err.message);
    return null;
  }
}

function getThresholdForUnit(unit) {
  if (unit === 'Nhà máy MHF' || unit === 'Phòng Kho vận') {
    return 20;
  }
  return 25;
}

module.exports = async function handler(req, res) {
  const host = req.headers.host || '';
  const originHeader = req.headers.origin || req.headers.referer || '';
  let originUrl = null;
  
  if (originHeader) {
    try {
      originUrl = new URL(originHeader);
    } catch (e) {
      return res.status(403).json({ ok: false, error: 'Invalid Origin format.' });
    }
  }

  const isVercelApp = host === 'edu-banhmimahai-web.vercel.app' || (host.startsWith('edu-banhmimahai-web-') && host.endsWith('.vercel.app'));
  const isApprovedHost = isVercelApp || host === 'daotao.banhmimahai.vn' || host.startsWith('localhost:') || host.startsWith('127.0.0.1:');

  if (!isApprovedHost || !originUrl || originUrl.host !== host) {
    return res.status(403).json({ ok: false, error: 'Forbidden. Origin mismatch or unauthorized host.' });
  }

  if (req.method === 'OPTIONS') {
    res.setHeader('Access-Control-Allow-Origin', originUrl.origin);
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    return res.status(204).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ ok: false, error: 'Method Not Allowed' });
  }

  const NOTION_TOKEN = process.env.NOTION_TOKEN;
  const NOTION_QUIZ_RESULT_DATA_SOURCE_ID = process.env.NOTION_QUIZ_RESULT_DATA_SOURCE_ID;

  if (!NOTION_TOKEN || !NOTION_QUIZ_RESULT_DATA_SOURCE_ID) {
    return res.status(503).json({ ok: false, error: 'Quiz result endpoint setup missing.' });
  }

  const body = req.body || {};
  const attemptId = String(body.attemptId || '').trim();
  const learnerName = String(body.learnerName || '').trim();
  const unit = String(body.unit || '').trim();
  const testAnswers = body.testAnswers;
  const rawQuestions = body.testQuestions;

  // Strict Payload Validation
  const attemptIdRegex = /^[a-zA-Z0-9_-]{16,100}$/;
  if (!attemptId || !attemptIdRegex.test(attemptId)) {
    return res.status(400).json({ ok: false, error: 'Mã lượt thi không hợp lệ (cần từ 16 đến 100 ký tự hợp lệ).' });
  }

  if (!learnerName || learnerName.length > 100) {
    return res.status(400).json({ ok: false, error: 'Họ tên không được để trống và không vượt quá 100 ký tự.' });
  }

  if (!APPROVED_UNITS.includes(unit)) {
    return res.status(400).json({ ok: false, error: 'Đơn vị không hợp lệ.' });
  }

  if (!Array.isArray(rawQuestions) || rawQuestions.length !== 30) {
    return res.status(400).json({ ok: false, error: 'Danh sách câu hỏi phải chứa đúng 30 câu.' });
  }

  const questionIdList = [];
  for (const item of rawQuestions) {
    const qId = (typeof item === 'object' && item !== null ? String(item.id || '') : String(item)).trim();
    if (!qId) {
      return res.status(400).json({ ok: false, error: 'ID câu hỏi không được để trống.' });
    }
    questionIdList.push(qId);
  }

  if (new Set(questionIdList).size !== 30) {
    return res.status(400).json({ ok: false, error: 'Bài thi chứa câu hỏi bị trùng lặp.' });
  }

  if (typeof testAnswers !== 'object' || testAnswers === null || Array.isArray(testAnswers)) {
    return res.status(400).json({ ok: false, error: 'Bộ câu trả lời phải là một object.' });
  }

  // FIX 3: Reject extra keys in testAnswers that are not in the selected 30 question IDs
  const allowedKeySet = new Set(questionIdList);
  for (const key of Object.keys(testAnswers)) {
    if (!allowedKeySet.has(key)) {
      return res.status(400).json({ ok: false, error: `Key '${key}' trong testAnswers không thuộc danh sách 30 câu hỏi.` });
    }
  }

  // FIX 3: Strict answer validation for each of the 30 questions
  for (const qId of questionIdList) {
    const val = testAnswers[qId];
    if (val === undefined || val === null) {
      continue; // Normalized unanswered
    }
    if (typeof val === 'string' && val.trim() === '') {
      return res.status(400).json({ ok: false, error: `Đáp án rỗng cho câu hỏi ${qId} không hợp lệ.` });
    }
    const ansStr = String(val).trim().toLowerCase();
    if (!['a', 'b', 'c', 'd'].includes(ansStr)) {
      return res.status(400).json({ ok: false, error: `Đáp án '${val}' cho câu hỏi ${qId} không hợp lệ.` });
    }
  }

  // Validate canonical answer key
  const answerKeyMap = getCanonicalAnswerKey();
  if (!answerKeyMap || answerKeyMap.size !== 171) {
    return res.status(500).json({ ok: false, error: 'Không thể tải bộ đáp án chuẩn (yêu cầu đúng 171 câu).' });
  }

  // Verify all submitted question IDs exist in canonical set
  for (const qId of questionIdList) {
    if (!answerKeyMap.has(qId)) {
      return res.status(400).json({ ok: false, error: `Câu hỏi ID '${qId}' không tồn tại trong bộ đáp án chuẩn.` });
    }
  }

  // L1 In-Memory Cache Check
  if (!global.quizResultCache) global.quizResultCache = new Map();
  if (!global.quizResultInFlight) global.quizResultInFlight = new Map();

  // FIX 2: Spread cached BEFORE setting duplicate: true so cached.duplicate: false cannot overwrite it
  const cached = global.quizResultCache.get(attemptId);
  if (cached) {
    return res.status(200).json({ ok: true, ...cached, duplicate: true });
  }

  // FIX 1: L1 Same-Instance In-Flight Single-Flight Promise Deduplication
  const inFlightPromise = global.quizResultInFlight.get(attemptId);
  if (inFlightPromise) {
    try {
      const result = await inFlightPromise;
      return res.status(200).json({ ok: true, ...result, duplicate: true });
    } catch (err) {
      return res.status(502).json({ ok: false, error: err.message || 'Lỗi xử lý lượt thi đồng thời.' });
    }
  }

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

  // Single-Flight Executor Promise
  const executeResultProcess = (async () => {
    // 1. Notion Data Source Preflight Query (Fail-Closed)
    let checkRes;
    try {
      checkRes = await fetchWithRetry(`https://api.notion.com/v1/databases/${NOTION_QUIZ_RESULT_DATA_SOURCE_ID}/query`, {
        method: 'POST',
        headers: {
          authorization: `Bearer ${NOTION_TOKEN}`,
          'content-type': 'application/json',
          'notion-version': NOTION_VERSION
        },
        body: JSON.stringify({
          filter: {
            property: 'Result ID',
            title: { equals: attemptId }
          }
        })
      });
    } catch (err) {
      throw new Error('Không thể kết nối đến Notion để kiểm tra mã bài thi.');
    }

    if (!checkRes.ok) {
      throw new Error(`Kiểm tra dữ liệu bài thi thất bại (Mã lỗi HTTP ${checkRes.status}).`);
    }

    let existingData;
    try {
      existingData = await checkRes.json();
    } catch (err) {
      throw new Error('Dữ liệu phản hồi từ dịch vụ lưu trữ không thể xử lý.');
    }

    if (existingData && Array.isArray(existingData.results) && existingData.results.length > 0) {
      const pageProps = existingData.results[0].properties || {};
      const score = typeof pageProps['Điểm']?.number === 'number' ? pageProps['Điểm'].number : 0;
      const threshold = typeof pageProps['Ngưỡng đạt']?.number === 'number' ? pageProps['Ngưỡng đạt'].number : getThresholdForUnit(unit);
      const statusName = pageProps['Kết quả']?.status?.name || (score >= threshold ? 'Đạt' : 'Chưa đạt');
      const passed = statusName === 'Đạt';
      const wrong = typeof pageProps['Số câu sai']?.number === 'number' ? pageProps['Số câu sai'].number : 0;
      const unanswered = typeof pageProps['Số câu chưa trả lời']?.number === 'number' ? pageProps['Số câu chưa trả lời'].number : 0;

      const storedResult = { attemptId, duplicate: true, score, total: 30, threshold, passed, wrong, unanswered };
      global.quizResultCache.set(attemptId, storedResult);
      return storedResult;
    }

    // 2. Server Recomputation of Score & Metadata
    let score = 0;
    let wrong = 0;
    let unanswered = 0;

    for (const qId of questionIdList) {
      const canonicalAns = answerKeyMap.get(qId);
      const rawUserAns = testAnswers[qId];
      const userAns = (rawUserAns !== undefined && rawUserAns !== null && rawUserAns !== '')
        ? String(rawUserAns).trim().toLowerCase()
        : null;

      if (!userAns || !['a', 'b', 'c', 'd'].includes(userAns)) {
        unanswered++;
      } else if (userAns === canonicalAns) {
        score++;
      } else {
        wrong++;
      }
    }

    const threshold = getThresholdForUnit(unit);
    const passed = score >= threshold;
    const DATASET_VERSION = 'ad1e93032815c8f99986166f5d8ed04d27ef1c9fbd033d26dbecfdb46e0e6394';
    const serverSubmittedAt = new Date().toISOString();
    const derivedPageUrl = `${originUrl.origin}/hoinhap/`;

    const notionPayload = {
      parent: { database_id: NOTION_QUIZ_RESULT_DATA_SOURCE_ID },
      properties: {
        'Result ID': { title: [{ type: 'text', text: { content: attemptId } }] },
        'Họ tên': { rich_text: [{ type: 'text', text: { content: learnerName } }] },
        'Đơn vị': { select: { name: unit } },
        'Điểm': { number: score },
        'Tổng số câu': { number: 30 },
        'Ngưỡng đạt': { number: threshold },
        'Kết quả': { status: { name: passed ? 'Đạt' : 'Chưa đạt' } },
        'Thời gian nộp': { date: { start: serverSubmittedAt } },
        'URL': { url: derivedPageUrl },
        'Chế độ': { select: { name: 'Thi chính thức' } },
        'Dataset version': { rich_text: [{ type: 'text', text: { content: DATASET_VERSION } }] },
        'Số câu sai': { number: wrong },
        'Số câu chưa trả lời': { number: unanswered }
      }
    };

    // 3. Create Page on Notion with Preflight Re-check on Retry
    let createRes;
    let createAttempt = 0;
    const maxCreateRetries = 10;

    while (createAttempt <= maxCreateRetries) {
      createAttempt++;
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 12000);
      let pageError = null;

      try {
        const fetchFn = global.customFetch || fetch;
        createRes = await fetchFn('https://api.notion.com/v1/pages', {
          method: 'POST',
          headers: {
            authorization: `Bearer ${NOTION_TOKEN}`,
            'content-type': 'application/json',
            'notion-version': NOTION_VERSION
          },
          body: JSON.stringify(notionPayload),
          signal: controller.signal
        });
        clearTimeout(timer);

        if (createRes.ok) {
          break;
        }

        const isRetryable = createRes.status === 429 || createRes.status === 409 || (createRes.status >= 500 && createRes.status <= 599);
        if (!isRetryable || createAttempt > maxCreateRetries) {
          break;
        }

        const retryAfterHeader = (createRes.headers && typeof createRes.headers.get === 'function') ? createRes.headers.get('retry-after') : null;
        const parsedDelay = parseRetryAfterMs(retryAfterHeader);
        let delayMs = (parsedDelay !== null) ? Math.min(parsedDelay + Math.floor(Math.random() * 300), 10000) : (250 * Math.pow(2, createAttempt - 1) + Math.floor(Math.random() * 100));
        await new Promise(resolve => setTimeout(resolve, delayMs));

      } catch (err) {
        clearTimeout(timer);
        pageError = err;
      }

      // Recheck Notion DB before repeating POST /v1/pages
      try {
        const fetchFn = global.customFetch || fetch;
        const recheckRes = await fetchFn(`https://api.notion.com/v1/databases/${NOTION_QUIZ_RESULT_DATA_SOURCE_ID}/query`, {
          method: 'POST',
          headers: {
            authorization: `Bearer ${NOTION_TOKEN}`,
            'content-type': 'application/json',
            'notion-version': NOTION_VERSION
          },
          body: JSON.stringify({
            filter: { property: 'Result ID', title: { equals: attemptId } }
          })
        });
        if (recheckRes.ok) {
          const recheckData = await recheckRes.json();
          if (recheckData && Array.isArray(recheckData.results) && recheckData.results.length > 0) {
            const pageProps = recheckData.results[0].properties || {};
            const score = typeof pageProps['Điểm']?.number === 'number' ? pageProps['Điểm'].number : 0;
            const threshold = typeof pageProps['Ngưỡng đạt']?.number === 'number' ? pageProps['Ngưỡng đạt'].number : getThresholdForUnit(unit);
            const statusName = pageProps['Kết quả']?.status?.name || (score >= threshold ? 'Đạt' : 'Chưa đạt');
            const passed = statusName === 'Đạt';
            const wrong = typeof pageProps['Số câu sai']?.number === 'number' ? pageProps['Số câu sai'].number : 0;
            const unanswered = typeof pageProps['Số câu chưa trả lời']?.number === 'number' ? pageProps['Số câu chưa trả lời'].number : 0;

            const storedResult = { attemptId, duplicate: true, score, total: 30, threshold, passed, wrong, unanswered };
            global.quizResultCache.set(attemptId, storedResult);
            return storedResult;
          }
        }
      } catch (e) {}

      if (pageError && createAttempt > maxCreateRetries) {
        throw pageError;
      }
    }

    if (!createRes.ok) {
      console.error('Notion page create failed with status:', createRes.status);
      throw new Error(`Không thể ghi kết quả thi vào hệ thống (Mã lỗi HTTP ${createRes.status}).`);
    }

    const newResultData = { attemptId, duplicate: false, score, total: 30, threshold, passed, wrong, unanswered };
    global.quizResultCache.set(attemptId, newResultData);
    return newResultData;
  })();

  global.quizResultInFlight.set(attemptId, executeResultProcess);

  try {
    const resultData = await executeResultProcess;
    return res.status(200).json({ ok: true, ...resultData });
  } catch (err) {
    return res.status(502).json({ ok: false, error: err.message || 'Lỗi lưu kết quả thi.' });
  } finally {
    global.quizResultInFlight.delete(attemptId);
  }
};
