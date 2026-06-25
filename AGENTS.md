# Codex Instructions

## DNS Abuse Matrix Publishing

- Treat `matrix/content/`, `matrix/data/`, `matrix/assets/`, and `matrix/templates/` as the source of truth for the DNS Abuse Techniques Matrix.
- Do not hand-edit files under `matrix/generated/` or `build/`; regenerate them with `make tables` or `make assemble`.
- Do not hand-edit generated PDFs. Change the Markdown, CSV, JSON, assets, or template, then rebuild.
- After changing matrix source data, run `make validate`.
- After changing prose, data, assets, or templates, run `make assemble`; run `make pdf` when Pandoc and Typst are available.
- Keep `matrix/data/matrix.csv` normalized: one row per action, technique, and stakeholder combination.
- Keep capability values in `matrix/data/matrix.csv` to `yes` or `no`.
- Prefer small, reviewable edits to source files over regenerated wholesale output.

