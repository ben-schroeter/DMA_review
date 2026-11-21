// Render every site/infographics/*.svg to <name>_1200.png, <name>_2400.png and <name>_thumb.webp (560px).
// Run from research/digital_rulebook: node site/render_infographics.js   (thumbnails are converted with Pillow afterwards)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const FONTS = 'https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&display=block';
(async () => {
  const dir = path.resolve('site/infographics');
  const svgs = fs.readdirSync(dir).filter(f => f.endsWith('.svg'));
  const b = await chromium.launch();
  for (const scale of [1, 2]) {
    const p = await b.newPage({ viewport: { width: 1200, height: 1200 }, deviceScaleFactor: scale });
    for (const f of svgs) {
      const svg = fs.readFileSync(path.join(dir, f), 'utf8');
      // load the site's fonts (DM Sans, Source Serif 4) and wait for them, so text is not drawn in a fallback face
      await p.setContent(`<html><head><link rel="stylesheet" href="${FONTS}"></head><body style="margin:0;background:#FAF9F5">${svg.replace('width="100%"', 'width="1200" height="1200"')}</body></html>`, { waitUntil: 'networkidle' });
      await p.evaluate(async () => { await document.fonts.load('400 20px "DM Sans"'); await document.fonts.load('700 20px "DM Sans"'); await document.fonts.load('700 20px "Source Serif 4"'); await document.fonts.ready; });
      if (!(await p.evaluate(() => document.fonts.check('700 20px "DM Sans"')))) throw new Error('DM Sans did not load');
      await p.waitForTimeout(150);
      await p.screenshot({ path: path.join(dir, f.replace('.svg', scale === 1 ? '_1200.png' : '_2400.png')), clip: { x: 0, y: 0, width: 1200, height: 1200 } });
    }
    await p.close();
  }
  await b.close();
  console.log('rendered', svgs.length);
})();
