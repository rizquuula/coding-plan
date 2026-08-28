# How to read the Z.ai subscribe page

`https://z.ai/subscribe` holds the only published Individual plan prices. It is a
Next.js app. It renders the prices client-side and shows one billing term at a
time.

The prices are **compiled into the page's own JavaScript bundle**. The page does
not fetch them at runtime. So you never need a browser. Fetch the bundle and read
the numbers out of it.

## What works and what does not

| Tool | Result |
|---|---|
| `WebFetch` | Navigation and page header only. No price. |
| `curl` on the raw HTML | 200 and about 165 KB. No tier name, no price. |
| `google-chrome --headless --dump-dom` | 0 bytes. |
| `curl` or Python on the JS chunks | Works. Every tier, every term. |

The first three all return success codes. None of them returns a price. Do not
read a 200 as evidence that you have the data.

## Run the shipped script

`scripts/read_subscribe.py` prints every tier under every billing term.

```bash
python3 <skill-dir>/scripts/read_subscribe.py
```

Python 3 standard library only. There is nothing to install.

The script fetches the page, reads the chunk list out of the HTML, fetches each
chunk, and stops at the first chunk that matches. It sends a desktop browser
`User-Agent`, which the site needs.

## The manual recipe, if the script breaks

Chunk file names carry a content hash. They change on every Z.ai deploy. Read the
chunk list out of the HTML each time. Never hard-code a chunk name.

```bash
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'

# 1. List every chunk the page loads.
curl -sA "$UA" https://z.ai/subscribe \
  | grep -o '/_next/static/chunks/[^"]*\.js' | sort -u

# 2. Grep one chunk for the product list.
curl -sA "$UA" https://z.ai/_next/static/chunks/8519-2879b762fffa3bcb.js \
  | grep -o 'productId:"product-[0-9a-f]*"[^}]*'
```

On 2026-08-28 the product list sat in `/_next/static/chunks/8519-2879b762fffa3bcb.js`.
Treat that name as an example, not a constant.

## The object shape

Each product is one JS object literal. A real sample, unmodified:

```
{productId:"product-9194ae",name:"Pro",description:"For professional workloads",tag:"50% off 1st Quarter",tagSuffix:" per Quarter",tagMoney:"20%",money:192,oldMoney:240,icon:"/images/my-collection.svg",...n,...u,isShow:!1,type:"pro",value:"Quarterly",simpleValue:"quarter",level:2,version:"V3",showLineThrough:!0,monthStep:3,stepUnit:"month"}
```

This regex extracts all of them:

```python
re.compile(r'\{productId:"(product-[0-9a-f]+)",name:"(Lite|Pro|Max)".*?money:([0-9.]+),oldMoney:([0-9.]+).*?value:"(Monthly|Quarterly|Yearly)".*?version:"(V\d)"')
```

## Trap: the chunk holds three generations at once

The bundle ships V1, V2, and V3 side by side. V1 and V2 are dead legacy pricing.
Only the highest `version` string is the plan Z.ai sells today. A naive
extraction returns nine wrong prices next to the nine right ones.

Read on 2026-08-28. `money` per term:

| version | tier | Monthly | Quarterly | Yearly |
|---|---|---|---|---|
| V1 | Lite | 3 | 9 | 36 |
| V1 | Pro | 15 | 45 | 180 |
| V1 | Max | 30 | 90 | 360 |
| V2 | Lite | 16.2 | 43.2 | 151.2 |
| V2 | Pro | 64.8 | 172.8 | 604.8 |
| V2 | Max | 144 | 384 | 1344 |
| V3 | Lite | 18 | 43.2 | 151.2 |
| V3 | Pro | 80 | 192 | 672 |
| V3 | Max | 168 | 403.2 | 1411.2 |

Take the V3 block. It matches `data/plans.yaml` exactly.

## Trap: `money` is the term total. Do not multiply it

`money` is already the price charged for the whole term. V3 Lite Quarterly
`money: 43.2` is the price of one quarter, not a rate per month. `oldMoney` is
the undiscounted list price, so 54 for Lite Quarterly, which is 18 times 3.

`AGENTS.md` defines `amount` as the term total. So copy `money` into `amount`
with no arithmetic.

The **rendered page** prints a rate per month, such as `$14.4/month` under the
quarterly toggle. The bundle does not. You read the bundle, so you do not
multiply. An agent that multiplies writes 129.6 where 43.2 is right.

## Team prices

The page has an `Individual` tab and a `Team` tab. The Team prices come from a
public JSON API, no auth needed:

```bash
curl -s https://api.z.ai/api/biz/overseas/team/subscribe/product/public_pricing
```

On 2026-08-28 it returned PRO at 88 per month and 1056 per year, MAX at 188 per
month and 2256 per year.

**Those are Team seat prices.** They belong in the two Team rows in
`data/plans.yaml` and nowhere else. Never copy a Team figure into an Individual
row, or an Individual figure into a Team row.

The endpoint also returns four entries that are `purchasable: false`. Filter
them out first. The trap and the full table sit in `pricing.md`.

The bundle maps the API tier strings to display names. `LEVEL_RIGHTS` holds
`pro:{productName:"Standard Seat"...}` and `max:{productName:"Premium Seat"...}`.
`PLAN_ITEMS` maps each tier and period to the same `productId` values the API
returns, which is what ties the two together.

The base URL for every `/biz/...` path is `https://api.z.ai/api`. It appears in
the page bundle as `baseURL:"https://api.z.ai/api"`.

## When the script returns nothing

Work through these in order:

1. Confirm the page still answers: `curl -sI https://z.ai/subscribe`.
2. Confirm the HTML still lists chunks. Run step 1 of the manual recipe.
3. Grep a few chunks for `productId:"product-`. The product list may have moved
   to another chunk.
4. Grep for `name:"Pro"` alone. The field order in the object may have changed,
   which breaks the regex.
5. Only after all four, conclude the bundle shape changed. Then repair the regex
   in `scripts/read_subscribe.py` and record what changed in this file.
