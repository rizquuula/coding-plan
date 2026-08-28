# How to read a Model Studio doc page

Every page under `https://www.alibabacloud.com/help/en/model-studio/` serves a
markdown twin. Append `.md` to the path.

    https://www.alibabacloud.com/help/en/model-studio/model-pricing
    https://www.alibabacloud.com/help/en/model-studio/model-pricing.md

The twin returns `Content-Type: text/markdown` and the whole page. This is the
only reliable way to read the large pages. The same twin works on the China site
under `https://help.aliyun.com/zh/model-studio/`.

## What works and what does not

Measured on 2026-08-28.

| Page | `WebFetch` | HTML size | Twin size |
|---|---|---|---|
| `model-pricing` | Truncates | 1.28 MB | 376 KB |
| `rate-limit` | Reaches the Qwen sections | 236 KB | 190 KB |
| `text-generation-model` | Not tested | — | 31 KB |
| `coding-plan` | Not tested | — | 9.5 KB |
| `token-plan-overview` | Not tested | — | 7.8 KB |
| `context-cache` | Works | 89 KB | 60 KB |

## Trap: `WebFetch` truncates `model-pricing` and reports success

`model-pricing` runs to about 1,670 lines in its twin. On 2026-08-28 `WebFetch`
stopped at the section `Text generation - third-party models`, near line 552. It
answered a question about a later section with `NOT PRESENT`.

So `WebFetch` reads the Qwen sections at the top of that page and nothing after
them. It gave the right rate for `qwen-max` and the right rates for the coder
models. It cannot reach image, video, speech, embedding, reranking, or industry
model prices.

Use the twin for every value on that page. A short answer from `WebFetch` is not
evidence that the page holds nothing more.

## Trap: the twin keeps every table as raw HTML on one line

The twin is markdown for headings and paragraphs. It is **not** markdown for
tables. Each table is one `<table>` element on a single physical line.

One table in `model-pricing` is over 40 KB on one line. So `grep` on the twin
returns a 40 KB blob, and `head` cuts a table in half.

Run the shipped script instead. It flattens each table into pipe-delimited rows.

## Run the shipped script

```bash
python3 <skill-dir>/scripts/read_tables.py <page> <pattern>
```

`<page>` is a slug on the international site, or a full URL for any other site.
`<pattern>` is a case-insensitive regular expression. Python 3 standard library
only. There is nothing to install.

```bash
# The rate for one exact model ID.
python3 scripts/read_tables.py model-pricing '^qwen-max'

# A model across every region on the rate-limit page.
python3 scripts/read_tables.py rate-limit '^qwen3-coder-plus$'

# A whole small page.
python3 scripts/read_tables.py coding-plan '.'

# The China site, by full URL.
python3 scripts/read_tables.py \
  https://help.aliyun.com/zh/model-studio/coding-plan '价格'
```

Each printed row starts with the line number of its table. Two tables that share
a line number are the same table.

## Find the region heading above a table

A price means nothing without its region. The region is an `####` heading above
the table, so it never appears in a row. Print the headings with `--context` and
match the line numbers.

```bash
python3 scripts/read_tables.py model-pricing '^####' --context
```

On 2026-08-28 that printed `26: #### Singapore` and `34: #### China (Beijing)`.
The `qwen-max` row sat at line 32, so it belongs to Singapore.

## The manual recipe, if the script breaks

```bash
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'

# 1. Confirm the twin answers and check for a redirect.
curl -sA "$UA" -o /dev/null \
  -w '%{http_code} %{size_download} %{content_type} %{redirect_url}\n' \
  https://www.alibabacloud.com/help/en/model-studio/model-pricing.md

# 2. Save it, then list the headings.
curl -sA "$UA" -o pricing.md \
  https://www.alibabacloud.com/help/en/model-studio/model-pricing.md
grep -n '^#' pricing.md
```

Send the desktop browser `User-Agent`. The script sends it too.

## When the script returns nothing

Work through these in order.

1. Read the error line. It prints the URL the script built. Confirm the slug.
2. Run step 1 of the manual recipe. A 301 means the slug moved. Follow it.
3. Check the `Content-Type`. `text/html` means the twin does not exist for that
   path, and you fetched a page instead.
4. Widen the pattern to `.` and look at what the page does hold. The model may
   have moved to another page.
5. Only after all four, conclude the page shape changed. Then repair the script
   and record what changed in this file.
