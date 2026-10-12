// Renders HTML/SVG jobs to PNG with the pre-installed Chromium.
// Usage: node tools/render.js jobs.json   (jobs: [{html, width, height, out}])
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch({
    executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  });
  const page = await browser.newPage({ deviceScaleFactor: 1 });
  for (const job of jobs) {
    await page.setViewportSize({ width: job.width, height: job.height });
    await page.setContent(job.html, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: job.out, omitBackground: !!job.transparent, clip: { x: 0, y: 0, width: job.width, height: job.height } });
  }
  await browser.close();
})();
