import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require('d:/TRILONG-tools/website-projects/trilong-atlas/node_modules/@playwright/test');
import path from 'path';

async function testFull() {
  const browser = await chromium.launch({ headless: true });
  const url = 'https://daotao.banhmimahai.vn/kynangsale/?nocache=' + Date.now();
  console.log('Testing URL:', url);
  
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto(url, { waitUntil: 'networkidle' });
  
  const artifactDir = 'C:/Users/admin/.gemini/antigravity/brain/da3eb171-3234-4d6a-bec4-5ead1d549214';
  
  // 1. Gate Screenshot
  await page.screenshot({ path: path.join(artifactDir, 'screenshot_live_master200_gate.png'), fullPage: false });
  console.log('Saved Gate screenshot');
  
  // Fill Gate Form
  await page.fill("input[placeholder='Nhập họ và tên học viên']", 'Trần Minh Long');
  await page.fill("input[placeholder='Nhập số điện thoại (10 chữ số)']", '0901234567');
  
  // 2. Click Study Mode
  await page.click('text=Chế độ Luyện tập');
  await page.waitForTimeout(1200);
  await page.screenshot({ path: path.join(artifactDir, 'screenshot_live_master200_study.png'), fullPage: false });
  console.log('Saved Study screenshot');

  // Click Option on first question to verify interaction & quote/explanation
  const firstOption = await page.$('.space-y-3 button, .space-y-2\\.5 button, .grid button');
  if (firstOption) {
    await firstOption.click();
    await page.waitForTimeout(800);
    await page.screenshot({ path: path.join(artifactDir, 'screenshot_live_master200_question.png'), fullPage: false });
    console.log('Saved Question screenshot');
  }

  // 3. Click Header "Thi chính thức" tab
  await page.click("header button:has-text('Thi chính thức')");
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(artifactDir, 'screenshot_live_master200_test.png'), fullPage: false });
  console.log('Saved Test Mode screenshot');
  
  await browser.close();
  console.log('All visual screenshots captured successfully!');
}

testFull().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
