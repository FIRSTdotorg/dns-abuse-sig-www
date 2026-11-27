# Repository Instructions

These instructions apply to all contributors and tools.

## Changes and merges

- Submit repository changes through a GitHub pull request, including generated PDF updates.
- Merge pull requests on GitHub. Do not merge branches locally or push directly to the default branch.
- Use concise wording and normal ASCII hyphens in prose and pull request text.

## Matrix PDF source and build

- Canonical report content is `matrix/content/*.md`, with normalized data in `matrix/data/*.csv`. `matrix/report.json`, `matrix/assets/` and the DOCX layout template `matrix/templates/DNS-Abuse-Techniques-Matrix.docx` are also build inputs. There is no canonical `matrix/source/` directory. Repeated definitions belong in the CSV files and Markdown references use `{{technique:id}}`, `{{stakeholder:id}}` and `{{action:id|displayLabel}}` includes. Keep narrative extras such as Law Enforcement and the hosting aside in Markdown. The five mapped assets are `capability-yes.png`, `capability-no.png`, `header.png` for landscape pages, `header-large.png` for the cover, and `header-portrait.png` for regular portrait pages.
- `report.json` owns the report title, subtitle, language, history heading and three history column labels. Its `website` field is the single source for the website URL in the report and its footer links.
- Build the PDF with `make pdf`. The build fills a temporary report DOCX from Markdown, CSV and assets, using `matrix/scripts/fill_docx_template.py`, then exports it with LibreOffice through `build_docx_pdf.py`. The filled report DOCX is a build output, never canonical source. The source template must not be changed by the build.
- Keep the original v1.3 design as the goal, including page orientation, matrices, symbols, colours, links, headers, footers and fonts. The current source revision fits the 22-page design and includes approved definition edits, so its text is not identical to the older export. Legitimate content growth may change the page count; the check has no fixed 22-page limit. It requires portrait narrative pages, landscape matrix pages and portrait closing pages.
- Run `make pdf-check` after building. Set `DOCX_TEMPLATE` or `REPORT_PDF` on the make command to select other inputs. QA checks Markdown/CSV-derived expected paragraphs, URLs and the count of colored capability symbols in the PDF. It also checks page regions, text bounds and footer rules and creates comparison previews under `build/matrix/review/`. It does not compare the filled DOCX body with the layout template body; the DOCX supplies layout only. Review every preview and obtain an independent review before publication.
- Run `make pdf-test` after source or generator changes. Tests verify that Markdown and CSV input edits affect the PDF and that builds are deterministic.
- The generator runs in Linux CI. A successful check prepares a proposal, not publication approval. Review every proposal independently, even when it matches the original page count.
- The workflow builds and checks pull requests without write permissions, then uploads the PDF and review previews. A successful default-branch build may prepare a separate draft pull request containing only the latest PDF and `matrix/pdf-build.json`. It must not push to the default branch or merge automatically. Bot branches are immutable and keyed by the source commit.
- The repository setting to allow GitHub Actions to create pull requests may need to be enabled by an administrator. Do not bypass this setting or push generated files directly.
- `DNS-Abuse-Techniques-Matrix_v1-latest.pdf` is the rolling working copy. Numbered PDFs are immutable release snapshots; create a new snapshot only when a release is requested. Keep historical draft PDFs under separate filenames. Do not begin a v2 redesign without a separate request.
- For a local human setup, use Python 3 with a virtual environment and `matrix/requirements-pdf.txt`, then install LibreOffice and Poppler. The Markdown parser is a Python dependency. GitHub Actions uses an isolated dependency environment on its runner.
- The `make import` target is for inspection only and writes imported files under `build/matrix/imported/`; never overwrite canonical content or data with an import.
- The historical `make draft-pdf` target uses Pandoc and Typst for a separate draft. It is not the canonical PDF build path.

## Reference data

- Keep the CSV files under `matrix/data/` normalized. `matrix.csv` has one row per action, technique and stakeholder combination, with capability values of `yes` or `no`; keep full action definitions in `actions.csv`.
- Run `make validate` before building after changing Markdown or CSV source data.
- Do not hand-edit `matrix/generated/` or `build/` files.
