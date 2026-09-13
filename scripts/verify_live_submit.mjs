import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require('d:/TRILONG-tools/website-projects/trilong-atlas/node_modules/@playwright/test');
import path from 'path';

async function testSubmitLive() {
  const browser = await chromium.launch({ headless: true });
  const url = 'https://daotao.banhmimahai.vn/kynangsale/?nocache=' + Date.now();
  console.log('Navigating to:', url);
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  
  page.on('dialog', async d => {
    console.log('Browser Dialog popup:', d.message());
    await d.accept();
  });
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('response', res => {
    if (res.url().includes('api/')) {
      console.log('API RESPONSE:', res.url(), res.status());
    }
  });

  await page.goto(url, { waitUntil: 'networkidle' });
  
  // Fill gate form
  await page.fill("input[placeholder*='Nguyễn Văn A']", 'Trần Minh Long');
  await page.fill("input[placeholder*='name@gmail.com']", 'nguyenlong5238@gmail.com');
  
  // Start test mode
  await page.click('.bento-card:has-text("Thi chính thức")');
  await page.waitForTimeout(1000);

  // Trigger submitTest with auto=true to bypass confirm dialog
  console.log('Calling submitTest(true)...');
  await page.evaluate(() => {
    Alpine.$data(document.querySelector('[x-data]')).submitTest(true);
  });
  
  // Wait for submission API response
  console.log('Waiting for API and UI transition...');
  await page.waitForTimeout(4000);

  const finalInfo = await page.evaluate(() => {
    const d = Alpine.$data(document.querySelector('[x-data]'));
    return {
      currentView: d.currentView,
      resultSaved: d.resultSaved,
      resultSendingStatus: d.resultSendingStatus,
      resultErrorMessage: d.resultErrorMessage,
      hasErrorOnPage: document.body.innerText.includes('Không thể kết nối đến máy chủ')
    };
  });
  console.log('Final Info:', JSON.stringify(finalInfo, null, 2));

  const artifactDir = 'C:/Users/admin/.gemini/antigravity/brain/da3eb171-3234-4d6a-bec4-5ead1d549214';
  const ssPath = path.join(artifactDir, 'screenshot_live_final_success.png');
  await page.screenshot({ path: ssPath, fullPage: false });
  console.log('Saved screenshot to:', ssPath);

  await browser.close();
}

testSubmitLive().catch(err => {
  console.error(err);
  process.exit(1);
});
