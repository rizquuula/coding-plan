# How to read the Z.ai subscribe page

`https://z.ai/subscribe` holds the only published plan prices. It renders them
client-side, after load, and shows one billing term at a time.

## What works and what does not

| Tool | Result |
|---|---|
| `WebFetch` | Navigation and page header only. No price. |
| `curl` on the raw HTML | 200 and about 165 KB. No tier name, no price. |
| `google-chrome --headless --dump-dom` | 0 bytes. |
| Playwright driving the system Chrome | Works. Full price table. |

The first three all return success codes. None of them returns a price. Do not
read a 200 as evidence that you have the data.

## Run the shipped script

`scripts/read-subscribe.js` prints every tier under every billing term.

```bash
cd /tmp/scratch            # any directory you can write to
npm i playwright-core
node <skill-dir>/scripts/read-subscribe.js
```

Install `playwright-core`, not `playwright`. It skips the browser download and
reuses the Chrome already on the machine. Set `CHROME_PATH` when Chrome is not
at `/usr/bin/google-chrome`.

The script pushes the working directory onto `module.paths`, so the install does
not have to sit beside the script.

## The recipe, if you write your own

```js
const { chromium } = require('playwright-core');

const browser = await chromium.launch({
  executablePath: '/usr/bin/google-chrome',
  args: ['--no-sandbox', '--disable-dev-shm-usage'],
});
const page = await browser.newPage({ viewport: { width: 1400, height: 1400 } });
await page.goto('https://z.ai/subscribe', { waitUntil: 'networkidle', timeout: 90000 });
await page.waitForTimeout(5000);
console.log(await page.evaluate(() => document.body.innerText));
```

Four things this page needs you to know:

1. `waitUntil: 'networkidle'` is too early on its own. Wait about 5 more seconds.
2. Read `document.body.innerText`, not the HTML. The prices sit in styled spans
   that are painful to parse and trivial to read as text.
3. Click each billing term and re-read the page:

   ```js
   await page.getByText('Quarterly', { exact: true }).first().click();
   await page.waitForTimeout(2500);
   ```

   The terms are `Monthly`, `Quarterly`, and `Yearly`.
4. `--no-sandbox` is required in this container. Without it Chrome exits.

## The price block markers

The tier rows sit between two stable strings in the body text:

- starts at `Code with GLM Coding Plan`
- ends at `Invite friends`

Slice between them to drop the hero copy, the IDE testimonials, and the footer.
When the slice comes back empty, the page copy changed. Print the whole body and
find the new markers rather than guessing.

## The Team tab

The page has an `Individual` tab and a `Team` tab. On 2026-08-28,
`getByText('Team', { exact: true }).first().click()` timed out after 8 seconds.
Nobody has read the Team prices from this page.

This repository tracks the list price for one seat, so `Individual` is the tab
you want. `https://docs.z.ai/devpack/teamplan` publishes the Team seat quotas
but no Team price.

If you need Team prices, expect to find a different selector first. Do not
assume the tab is broken.

## When the script returns nothing

Work through these in order:

1. Confirm Chrome runs at all: `google-chrome --version`.
2. Drop the term loop and print the whole `innerText`. Confirm the page loaded.
3. Raise the wait from 5 seconds. A slow network delays the price fetch.
4. Check the markers above against the printed text.
5. Only after all four, conclude the page changed shape.
