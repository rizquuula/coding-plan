#!/usr/bin/env node
// Print the GLM Coding Plan prices for every billing term.
//
// The page at https://z.ai/subscribe renders its prices client-side and shows
// one billing term at a time. WebFetch and `chrome --headless --dump-dom` both
// return no price. Playwright driving the system Chrome works.
//
// Setup:
//   npm i playwright-core
// Run:
//   node read-subscribe.js
//
// Override the browser with CHROME_PATH when Chrome is not at the default path.

// Node resolves modules from this file's directory, not the working directory.
// Look in the working directory too, so `npm i playwright-core` anywhere works.
module.paths.push(require('path').join(process.cwd(), 'node_modules'));

let chromium;
try {
  ({ chromium } = require('playwright-core'));
} catch {
  console.error('playwright-core is missing. Install it, then run this script again:');
  console.error('  npm i playwright-core');
  process.exit(1);
}

const URL = 'https://z.ai/subscribe';
const CHROME = process.env.CHROME_PATH || '/usr/bin/google-chrome';
const TERMS = ['Monthly', 'Quarterly', 'Yearly'];

// The price block sits between these two markers in the body text.
const START = 'Code with GLM Coding Plan';
const END = 'Invite friends';

function priceBlock(text) {
  const from = text.indexOf(START);
  if (from === -1) return null;
  const to = text.indexOf(END, from);
  return text.slice(from, to === -1 ? from + 2000 : to).trim();
}

async function main() {
  const browser = await chromium.launch({
    executablePath: CHROME,
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });

  try {
    const page = await browser.newPage({ viewport: { width: 1400, height: 1400 } });
    await page.goto(URL, { waitUntil: 'networkidle', timeout: 90000 });
    // networkidle alone is too early. The prices arrive after it.
    await page.waitForTimeout(5000);

    for (const term of TERMS) {
      try {
        await page.getByText(term, { exact: true }).first().click({ timeout: 8000 });
        await page.waitForTimeout(2500);
      } catch (error) {
        console.log(`\n### ${term}: could not click the toggle`);
        console.log(error.message.split('\n')[0]);
        continue;
      }

      const block = priceBlock(await page.evaluate(() => document.body.innerText));
      console.log(`\n### ${term}\n`);
      console.log(block || 'the price block did not render; the page markers may have changed');
    }

    console.log('\n---');
    console.log('Each figure is a rate PER MONTH, not the price of the term.');
    console.log('Multiply by 3 for a quarter and by 12 for a year before you write `amount`.');
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error('failed:', error.message);
  process.exit(1);
});
