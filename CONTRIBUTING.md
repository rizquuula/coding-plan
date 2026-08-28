# Contributing

Thanks for helping keep the tracker accurate. Contributions are mostly data
updates: a new plan, a changed price, a fresh rate limit. This guide covers the
essentials; `AGENTS.md` holds the full schemas and rules.

## Ground rules

1. Edit only the files under `data/`. The build script derives everything else.
2. Never edit `site/`. The build deletes and rewrites that directory.
3. Never invent a value. Copy every price, quota, and parameter count from a
   page the provider owns, and link that page in the row's `links` list.
4. Do not cite blogs, comparison sites, or aggregators. Provider pages only.
5. Read the page yourself before you write a value. A search summary is not a
   source.
6. Set `last_verified` to the date you read the page (`YYYY-MM-DD`).

## Workflow

1. Fork and clone the repository.
2. Install the dependencies and confirm the data validates:

   ```bash
   pip install -r requirements.txt
   python build.py --check
   ```

3. Edit the relevant file under `data/`:

   | File | Contents |
   |---|---|
   | `data/plans.yaml` | Subscription plans |
   | `data/api_pricing.yaml` | Per-model API rates |
   | `data/rate_limits.yaml` | Published API rate limits |
   | `data/models.yaml` | Model specifications |

4. Follow the schema in `AGENTS.md` for the file you touch. Key points:
   - One record per plan tier — do not merge tiers.
   - Use the same provider spelling in all four files.
   - `prices` amounts are the full term total, not the monthly equivalent.
   - Write rate-limit numbers as plain integers (`5000000`, not `5M`).
5. Run `python build.py --check` again and fix every error it prints.
6. Preview locally if you changed templates or assets:

   ```bash
   python build.py
   python -m http.server -d site 8000
   ```

7. Open a pull request. In the description, list which rows changed and link
   the provider pages you read.

## When a plan disappears

Do not delete the record. Set `status: discontinued`, set `discontinued_on`,
and say so in `notes`.

## Adding a new provider

Add rows to the data files, add a sourcing skill under
`.claude/skills/provider-<name>/`, and extend the provider table in
`AGENTS.md`. See an existing skill such as `provider-anthropic` for the shape.

## Commit messages

Use Conventional Commits: `fix(data): update the Cursor Ultra price`,
`feat(data): add the DeepSeek Harness plan`.

## License

By contributing, you agree that your contributions are licensed under the
[MIT License](LICENSE).
