// Screenshoty všech jazyků ve 390 / 768 / 1440 px do screenshots/ (složka je v .gitignore).
import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import { mkdirSync } from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const out = path.join(root, 'screenshots');
mkdirSync(out, { recursive: true });
const pages = { cs: 'index.html', pl: 'pl/index.html', de: 'de/index.html' };
const widths = [390, 768, 1440];

const browser = await chromium.launch();
for (const [lang, file] of Object.entries(pages)) {
  for (const w of widths) {
    const page = await browser.newPage({ viewport: { width: w, height: 900 } });
    await page.goto(pathToFileURL(path.join(root, file)).href);
    await page.addStyleTag({ content: '.reveal{opacity:1!important;transform:none!important;transition:none!important}' });
    // projít stránku, aby se načetly lazy fotky
    await page.evaluate(async () => {
      for (let y = 0; y < document.body.scrollHeight; y += 400) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
      window.scrollTo(0, 0);
    });
    await page.waitForFunction(() => [...document.querySelectorAll('main img')].every(i => i.complete && i.naturalWidth > 0));
    await page.waitForTimeout(600);
    await page.screenshot({ path: path.join(out, `${lang}-${w}.png`), fullPage: true });
    await page.close();
  }
}
await browser.close();
console.log('Hotovo:', out);
