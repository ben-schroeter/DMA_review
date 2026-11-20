// Render every site/infographics/*.svg to <name>_1200.png, <name>_2400.png and <name>_thumb.webp (560px).
// Run from research/digital_rulebook: node site/render_infographics.js   (thumbnails are converted with Pillow afterwards)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = path.resolve('site/infographics');
  const svgs = fs.readdirSync(dir).filter(f => f.endsWith('.svg'));
  const b = await chromium.launch();
  for (const scale of [1, 2]) {
    const p = await b.newPage({ viewport: { width: 1200, height: 1200 }, deviceScaleFactor: scale });
    for (const f of svgs) {
      const svg = fs.readFileSync(path.join(dir, f), 'utf8');
      await p.setContent(`<html><body style="margin:0;background:#FAF9F5">${svg.replace('width="100%"', 'width="1200" height="1200"')}</body></html>`);
      await p.waitForTimeout(150);
      await p.screenshot({ path: path.join(dir, f.replace('.svg', scale === 1 ? '_1200.png' : '_2400.png')), clip: { x: 0, y: 0, width: 1200, height: 1200 } });
    }
    await p.close();
  }
  await b.close();
  console.log('rendered', svgs.length);
})();
