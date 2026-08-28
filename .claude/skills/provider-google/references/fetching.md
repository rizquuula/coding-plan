# How to read the Google plan pages

The Gemini API docs on `ai.google.dev` need no trick. `WebFetch` reads them. This
file covers the two consumer plan pages, which both localize the price.

## The trap: the price follows your IP address

`https://gemini.google/subscriptions/` returns a 200 and a full plan table. It
prints the price in the currency of the country it detects from your IP. From
this machine it returns Indonesian rupiah:

    Rp 75.000 IDR/bulan          <- Google AI Plus
    Rp 309.000 IDR/bulan         <- Google AI Pro
    Rp 1.579.000 IDR / bulan     <- Google AI Ultra, 5x
    Rp 3.399.000 IDR / bulan     <- Google AI Ultra, 20x

`data/plans.yaml` carries USD, so those figures are wrong for this repository.
Do not convert them. Read the USD page.

## The fix: the `/us/` path

`https://gemini.google/us/subscriptions/` returns the United States page in USD.

```bash
curl -sL https://gemini.google/us/subscriptions/ -o us.html
```

`WebFetch` reads the same URL and returns the plan cards in full. Use `WebFetch`
first.

The `/us/` path is not linked from the site navigation. It appears when you
follow the redirect chain:

```bash
curl -sL -o /dev/null -w '%{url_effective}\n' 'https://gemini.google/subscriptions/?hl=en'
# -> https://gemini.google/us/subscriptions/?hl=en
```

Confirm the page shows `United States` before you copy a figure. That string sits
above the first plan card.

## What does not work

| Attempt | Result |
|---|---|
| `https://gemini.google/subscriptions/?hl=en` | 301. Follow it to reach `/us/`. |
| `https://gemini.google/subscriptions/?gl=us&hl=en` | 301. Same redirect. |
| `https://gemini.google/intl/en_us/subscriptions/` | 302 back to the IDR page. |
| `https://gemini.google/intl/en/subscriptions/` | 302 back to the IDR page. |

A locale query parameter does not change the currency on this site. Only the
`/us/` path does.

## `one.google.com` holds no price at all

`https://one.google.com/about/google-ai-plans/` is worse. It never prints a
price, in any currency, to any fetch tool. The price is a custom element with an
empty body:

```html
<div class="planCardPrice_mKmrs priceText_iIhJ7 ...">
  <g1-localized-price variant="PRICE_GEN_AI_PRO_MONTHLY" country="ID"></g1-localized-price>/bln
</div>
```

The browser fills that element after load. `curl` and `WebFetch` both see an
empty tag next to a bare `/bln`. A summarizer reads that as "price not
displayed".

`country="ID"` is baked into the served HTML from your IP address. These all
return the same markup:

    https://one.google.com/about/google-ai-plans/
    https://one.google.com/about/google-ai-plans/?hl=en
    https://one.google.com/about/google-ai-plans/?hl=en&gl=us
    https://one.google.com/about/google-ai-plans/?gl=US&hl=en-US

`https://one.google.com/us/about/google-ai-plans/` returns 404. This site has no
`/us/` path. Treat `one.google.com` as a dead end for every price.

## Trap: a regex tag-strip eats the `200k` threshold

Some models on the API pricing page charge two input rates, split at 200k tokens.
The page writes the threshold with a raw, unescaped `<`:

```html
<td>$2.00, prompts <= 200k tokens<br>$4.00, prompts > 200k tokens</td>
```

A tag-strip such as `re.sub(r'<[^>]+>', '', html)` treats `<= 200k tokens<` as a
tag and deletes it. The text collapses to `$2.00, prompts $4.00, prompts > 200k
tokens`, which reads as one price followed by another.

Use `WebFetch` on this page. It handles the markup correctly. When you must use
`curl`, read the raw `<td>` and do not strip tags first.

## Confirm a `.md` twin by byte count, not by status code

`ai.google.dev` returns 200 for any `.md` suffix and serves the HTML page. Both
URLs below returned 105,895 bytes on 2026-08-28:

```bash
curl -sL -o /dev/null -w '%{size_download}\n' https://ai.google.dev/gemini-api/docs/rate-limits
curl -sL -o /dev/null -w '%{size_download}\n' https://ai.google.dev/gemini-api/docs/rate-limits.md
```

Equal byte counts mean there is no twin. `https://ai.google.dev/llms.txt` returns
404, so there is no docs index either.

## When the plan price is missing

Work through these in order:

1. Confirm the page still answers: `curl -sI https://gemini.google/us/subscriptions/`.
2. Grep the HTML for `price-amount`. The price sits in that class.
3. Grep for `United States`. A missing string means the `/us/` path moved.
4. Follow `https://gemini.google/subscriptions/?hl=en` and read the final URL.
   The country path may have changed.
5. Only after all four, fall back to the blog post, and record in `notes` that
   the figure is rounded. See `pricing.md`.
