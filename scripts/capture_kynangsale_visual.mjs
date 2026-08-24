import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require('d:/TRILONG-tools/website-projects/trilong-atlas/node_modules/@playwright/test');
import http from 'http';
import fs from 'fs';
import path from 'path';

const PORT = 3333;
const ROOT_DIR = process.cwd();

// Simple static server
const mimeTypes = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.ico': 'image/x-icon',
  '.svg': 'image/svg+xml'
};

const server = http.createServer((req, res) => {
  const parsedUrl = new URL(req.url, `http://localhost:${PORT}`);
  let pathname = parsedUrl.pathname;
  if (pathname.endsWith('/')) {
    pathname += 'index.html';
  }
  
  const filePath = path.join(ROOT_DIR, pathname);
  const ext = path.extname(filePath).toLowerCase();
  
  fs.readFile(filePath, (err, content) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('Not Found');
    } else {
      res.writeHead(200, { 'Content-Type': mimeTypes[ext] || 'application/octet-stream' });
      res.end(content);
    }
  });
});

async function run() {
  await new Promise(resolve => server.listen(PORT, resolve));
  console.log(`Local static server listening on http://localhost:${PORT}`);

  const artifactDir = 'C:/Users/admin/.gemini/antigravity/brain/da3eb171-3234-4d6a-bec4-5ead1d549214';
  if (!fs.existsSync(artifactDir)) {
    fs.mkdirSync(artifactDir, { recursive: true });
  }

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 }
  });
  const page = await context.newPage();

  console.log('Navigating to local kynangsale...');
  await page.goto(`http://localhost:${PORT}/kynangsale/?v=nocache_${Date.now()}`, { waitUntil: 'networkidle' });

  // 1. Screenshot Gate Screen
  const gatePath = path.join(artifactDir, 'screenshot_gate.png');
  await page.screenshot({ path: gatePath, fullPage: false });
  console.log('Saved Gate screenshot:', gatePath);

  // 2. Fill Info & Go to Study Mode
  await page.fill("input[placeholder='Nhập họ và tên học viên']", 'Trần Minh Long');
  await page.fill("input[placeholder='Nhập số điện thoại (10 chữ số)']", '0909123456');
  
  // Click Luyện tập
  await page.click("text=Chế độ Luyện tập");
  await page.waitForTimeout(600);

  // Take screenshot of Study Mode showing 8 sections sidebar
  const studyPath = path.join(artifactDir, 'screenshot_study_8sections.png');
  await page.screenshot({ path: studyPath, fullPage: false });
  console.log('Saved Study 8 Sections screenshot:', studyPath);

  // Scroll sidebar to see bottom sections 5-8
  const sidebar = await page.$('aside');
  if (sidebar) {
    await sidebar.evaluate(el => el.scrollTop = 400);
    await page.waitForTimeout(400);
    const studyScrolledPath = path.join(artifactDir, 'screenshot_study_sections_scrolled.png');
    await page.screenshot({ path: studyScrolledPath, fullPage: false });
    console.log('Saved Study Scrolled screenshot:', studyScrolledPath);
  }

  // 3. Switch to Test Mode
  await page.click("nav button:has-text('Thi chính thức')");
  await page.waitForTimeout(600);
  const testPath = path.join(artifactDir, 'screenshot_test_mode.png');
  await page.screenshot({ path: testPath, fullPage: false });
  console.log('Saved Test Mode screenshot:', testPath);

  await browser.close();
  server.close();
  console.log('Visual capture complete!');
}

run().catch(err => {
  console.error('Error during visual capture:', err);
  server.close();
  process.exit(1);
});
