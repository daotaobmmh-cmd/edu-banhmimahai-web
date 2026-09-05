const NOTION_VERSION = '2022-06-28';
const fs = require('fs');
const path = require('path');

let canonicalAnswerKey = null;

function getCanonicalAnswerKey() {
  if (canonicalAnswerKey) return canonicalAnswerKey;
  try {
    let filePath = path.join(process.cwd(), 'kynangsale', 'questions.js');
    if (!fs.existsSync(filePath)) {
      filePath = path.join(__dirname, '..', 'kynangsale', 'questions.js');
    }
    const code = fs.readFileSync(filePath, 'utf8');
    const win = {};
    const fn = new Function('window', code);
    fn(win);
    const map = new Map();
    const questions = win.KYNANGSALE_QUESTIONS || win.HOINHAP_QUESTIONS || [];
    if (!Array.isArray(questions) || questions.length !== 200) {
      console.error('Canonical dataset length mismatch. Expected 200, got:', questions.length);
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
    if (map.size !== 200) {
      console.error('Canonical map size mismatch. Expected 200 unique IDs, got:', map.size);
      return null;
    }
    canonicalAnswerKey = map;
    return map;
  } catch (err) {
    console.error('Failed to load canonical answer key:', err.message);
    return null;
  }
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

  const body = req.body || {};
  const attemptId = String(body.attemptId || '').trim();
  const learnerName = String(body.learnerName || '').trim();
  const learnerEmail = String(body.learnerEmail || body.email || body.phoneNumber || '').trim();
  const phoneNumber = learnerEmail;
  const testAnswers = body.testAnswers;
  const rawQuestions = body.testQuestions;
  const rawStartedAt = body.startedAt;
  const rawSubmittedAt = body.submittedAt;
  const rawDurationSeconds = body.durationSeconds;

  // Strict Payload Validation
  const attemptIdRegex = /^[a-zA-Z0-9_-]{16,100}$/;
  if (!attemptId || !attemptIdRegex.test(attemptId)) {
    return res.status(400).json({ ok: false, error: 'Mã lượt thi không hợp lệ.' });
  }

  if (!learnerName || learnerName.length > 100) {
    return res.status(400).json({ ok: false, error: 'Họ tên không được để trống và không vượt quá 100 ký tự.' });
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const phoneRegex = /^(03|05|07|08|09)\d{8}$/;
  if (!learnerEmail || (!emailRegex.test(learnerEmail) && !phoneRegex.test(learnerEmail))) {
    return res.status(400).json({ ok: false, error: 'Địa chỉ Gmail / Email không hợp lệ.' });
  }

  if (!Array.isArray(rawQuestions) || rawQuestions.length !== 60) {
    return res.status(400).json({ ok: false, error: 'Danh sách câu hỏi phải chứa đúng 60 câu.' });
  }

  const questionIdList = [];
  for (const item of rawQuestions) {
    const qId = (typeof item === 'object' && item !== null ? String(item.id || '') : String(item)).trim();
    if (!qId) {
      return res.status(400).json({ ok: false, error: 'ID câu hỏi không được để trống.' });
    }
    questionIdList.push(qId);
  }

  if (new Set(questionIdList).size !== 60) {
    return res.status(400).json({ ok: false, error: 'Bài thi chứa câu hỏi bị trùng lặp.' });
  }

  if (typeof testAnswers !== 'object' || testAnswers === null || Array.isArray(testAnswers)) {
    return res.status(400).json({ ok: false, error: 'Bộ câu trả lời phải là một object.' });
  }

  // Validate canonical answer key
  const answerKeyMap = getCanonicalAnswerKey();
  if (!answerKeyMap || answerKeyMap.size !== 200) {
    return res.status(500).json({ ok: false, error: 'Không thể tải bộ đáp án chuẩn 200 câu.' });
  }

  // Verify all questions exist in canonical set
  for (const qId of questionIdList) {
    if (!answerKeyMap.has(qId)) {
      return res.status(400).json({ ok: false, error: `Câu hỏi ID '${qId}' không tồn tại trong bộ đáp án chuẩn.` });
    }
  }

  if (typeof rawStartedAt !== 'string' || !rawStartedAt.trim() || isNaN(Date.parse(rawStartedAt.trim()))) {
    return res.status(400).json({ ok: false, error: 'Trường startedAt không hợp lệ.' });
  }
  if (typeof rawSubmittedAt !== 'string' || !rawSubmittedAt.trim() || isNaN(Date.parse(rawSubmittedAt.trim()))) {
    return res.status(400).json({ ok: false, error: 'Trường submittedAt không hợp lệ.' });
  }

  const startedAt = rawStartedAt.trim();
  const submittedAt = rawSubmittedAt.trim();

  const startMs = Date.parse(startedAt);
  const subMs = Date.parse(submittedAt);

  const durationSeconds = (typeof rawDurationSeconds === 'number' && rawDurationSeconds >= 0 && rawDurationSeconds <= 2700)
    ? rawDurationSeconds
    : Math.min(2700, Math.max(1, Math.round((subMs - startMs) / 1000)));

  const durationMinutes = Math.round((durationSeconds / 60) * 100) / 100;

  // Calculate score immediately on server
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

  const threshold = 48; // Ngưỡng 48/60 (80%)
  const passed = score >= threshold;
  const resultPayload = {
    attemptId,
    score,
    total: 60,
    threshold,
    passed,
    wrong,
    unanswered,
    startedAt,
    submittedAt,
    durationSeconds,
    durationMinutes
  };

  if (!global.kynangsaleQuizResultCache) global.kynangsaleQuizResultCache = new Map();
  global.kynangsaleQuizResultCache.set(attemptId, resultPayload);

  // Background Notion Async Sync
  const NOTION_TOKEN = process.env.NOTION_TOKEN;
  const NOTION_QUIZ_RESULT_DATA_SOURCE_ID = process.env.NOTION_QUIZ_RESULT_DATA_SOURCE_ID;

  if (NOTION_TOKEN && NOTION_QUIZ_RESULT_DATA_SOURCE_ID) {
    (async () => {
      try {
        const DATASET_VERSION = 'kynangsale-v1.0';
        const displayName = `${learnerName} (${phoneNumber})`;
        const derivedPageUrl = `${originUrl.origin}/kynangsale/`;

        const notionPayload = {
          parent: { database_id: NOTION_QUIZ_RESULT_DATA_SOURCE_ID },
          properties: {
            'Result ID': { title: [{ type: 'text', text: { content: attemptId } }] },
            'Họ tên': { rich_text: [{ type: 'text', text: { content: displayName } }] },
            'Điểm': { number: score },
            'Tổng số câu': { number: 60 },
            'Ngưỡng đạt': { number: threshold },
            'Kết quả': { status: { name: passed ? 'Đạt' : 'Chưa đạt' } },
            'Thời gian bắt đầu': { date: { start: startedAt } },
            'Thời gian nộp': { date: { start: submittedAt } },
            'Thời lượng (giây)': { number: durationSeconds },
            'Thời lượng (phút)': { number: durationMinutes },
            'URL': { url: derivedPageUrl },
            'Chế độ': { select: { name: 'Thi chính thức' } },
            'Dataset version': { rich_text: [{ type: 'text', text: { content: DATASET_VERSION } }] },
            'Số câu sai': { number: wrong },
            'Số câu chưa trả lời': { number: unanswered }
          }
        };

        const fetchFn = global.customFetch || fetch;
        await fetchFn('https://api.notion.com/v1/pages', {
          method: 'POST',
          headers: {
            authorization: `Bearer ${NOTION_TOKEN}`,
            'content-type': 'application/json',
            'notion-version': NOTION_VERSION
          },
          body: JSON.stringify(notionPayload)
        });
      } catch (err) {
        console.error('Async Notion sync background notice:', err.message);
      }
    })().catch(() => {});
  }

  // Instant 200 OK Response to client!
  return res.status(200).json({ ok: true, ...resultPayload });
};
