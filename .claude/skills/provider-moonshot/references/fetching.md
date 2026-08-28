# How to read the Kimi membership pricing page

`https://www.kimi.com/membership/pricing` holds the only published membership
prices. It is a Vue single-page app. It renders every tier client-side.

The prices are **not** in the page and **not** in the JavaScript bundle. The page
calls one RPC at runtime. That RPC is public. So you never need a browser. Call
the RPC and read the numbers out of the JSON.

## What works and what does not

| Tool | Result |
|---|---|
| `WebFetch` on the page | 200 and the page title only. No tier, no price. |
| `curl` on the raw HTML | 200 and about 15 KB of SPA shell. No tier, no price. |
| `curl` on the JS bundle | 200 and about 1.6 MB. Names the RPC. Holds no price. |
| `curl` POST on the RPC | Works. Every tier, every term. |

The first three all return success codes. None of them returns a price. Do not
read a 200 as evidence that you have the data.

## Run the shipped script

`scripts/read_plans.py` prints every tier under every billing term.

```bash
python3 <skill-dir>/scripts/read_plans.py         # the live tier names
python3 <skill-dir>/scripts/read_plans.py --all   # all three domains
python3 <skill-dir>/scripts/read_plans.py --json  # the raw response
```

Python 3 standard library only. There is nothing to install. The endpoint needs
no API key, no cookie, and no login.

## The manual recipe, if the script breaks

```bash
curl -s -X POST \
  'https://www.kimi.com/apiv2/kimi.gateway.order.v1.GoodsService/ListGoods' \
  -H 'Content-Type: application/json' \
  -H 'x-msh-platform: web' \
  -d '{"domains":[],"pageSize":0,"pageToken":"","paymentChannel":"PAYMENT_CHANNEL_UNSPECIFIED"}'
```

`www.kimi.ai` serves the same endpoint and returns the same body.

Three parts of that URL matter:

1. The path prefix is `/apiv2`. A POST to `/api` returns 404 with
   `Cannot POST /kimi.gateway.order.v1.GoodsService/ListGoods`. A POST to the
   bare host 302s to the home page.
2. The service name is `kimi.gateway.order.v1.GoodsService`. It is a Connect RPC
   service, so the method is the last path segment.
3. The body is Connect JSON. An empty `domains` list returns the live tiers.

## The object shape

Each tier and term is one `goods` entry. A real sample, unmodified:

```json
{
  "id": "b2c3d4e5-f6a7-8901-bcde-f23456789024",
  "title": "Allegretto",
  "durationDays": 30,
  "useRegion": "REGION_OVERSEA",
  "membershipLevel": "LEVEL_INTERMEDIATE",
  "amounts": [{"currency": "USD", "priceInCents": "37200"}],
  "billingCycle": {"duration": 1, "timeUnit": "TIME_UNIT_YEAR"},
  "type": "GOODS_TYPE_SUBSCRIPTION",
  "domain": "DOMAIN_NEXUS",
  "stock": {}
}
```

## Trap: `durationDays` lies on a yearly record

The sample above is the **yearly** Allegretto and it still says
`durationDays: 30`. Read `billingCycle`. It carries `duration` and `timeUnit`,
and it is correct on every record. Never derive a term from `durationDays`.

## Trap: `priceInCents` is cents, and it is the term total

`priceInCents` is a string of cents for the whole term. Divide by 100 once. Do
not multiply by the term.

Allegretto yearly returns `37200`. That is 372 USD for one year, which the page
prints as 31 USD per month. `AGENTS.md` defines `amount` as the term total, so
write `372`. An agent that multiplies writes 4464 where 372 is right.

`scripts/read_plans.py` already divides by 100. Copy what it prints.

## Trap: `membershipLevel` does not sort by price

The enum reads `LEVEL_FREE`, `LEVEL_BASIC`, `LEVEL_INTERMEDIATE`,
`LEVEL_ADVANCED`, `LEVEL_STANDARD`. `LEVEL_STANDARD` is the **top** tier, above
`LEVEL_ADVANCED`. The name suggests a middle tier and it is not. Sort by price,
not by the enum name.

## Trap: three domains, three tier namings

`domains: []` returns `DOMAIN_NEXUS`. Ask for another domain and you get another
set of names. See `pricing.md` for the table and for which one to take.

## When the script returns nothing

Work through these in order:

1. Confirm the host still answers: `curl -sI https://www.kimi.com/`.
2. Repeat the manual `curl` above and read the body, not the status code.
3. Read the SPA bundle list out of the page HTML:
   `curl -s https://www.kimi.com/membership/pricing | grep -o 'src="[^"]*\.js"'`.
4. Fetch the main bundle and grep for `GoodsService` and for `listGoods`. The
   service or the method name may have changed.
5. Grep the bundle for `assets/membership` and fetch that chunk. It names the
   request fields the page sends.
6. Only after all five, conclude the RPC changed. Then repair
   `scripts/read_plans.py` and record what changed in this file.

Bundle file names carry a content hash and change on every deploy. Read the
bundle list out of the HTML each time. Never hard-code a bundle name.
