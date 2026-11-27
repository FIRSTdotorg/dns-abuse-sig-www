# Repository Instructions

## DNS Abuse Matrix Publishing

- Treat `matrix/content/`, `matrix/data/`, `matrix/assets/`, `matrix/templates/`, and `matrix/report.json` as the source of truth for the DNS Abuse Techniques Matrix.
- Do not hand-edit files under `matrix/generated/` or `build/`; regenerate them with `make tables` or `make assemble`.
- Do not hand-edit generated PDFs. Change the Markdown, CSV, JSON, assets, or template, then rebuild.
- After changing matrix source data, run `make validate`.
- After changing prose, data, assets, or templates, run `make assemble`; run `make pdf` when Pandoc and Typst are available.
- Keep `matrix/data/matrix.csv` normalized: one row per action, technique, and stakeholder combination.
- Keep capability values in `matrix/data/matrix.csv` to `yes` or `no`.
- Prefer small, reviewable edits to source files over regenerated wholesale output.
- Use concise wording in project prose and PR text. Use normal ASCII hyphens instead of en or em dashes.
- The `DNS-Abuse-Techniques-Matrix_v1-latest.pdf` file is an automatically updated working copy. GitHub Actions rebuilds it after source changes reach the default branch.
- Numbered PDFs are release snapshots. Create a new snapshot only when a release is requested. Do not replace existing snapshots.
