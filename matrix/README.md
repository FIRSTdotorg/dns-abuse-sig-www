# DNS Abuse Techniques Matrix PDF

## Canonical sources

Markdown files in [`content/`](content/) and CSV files in [`data/`](data/) are the canonical report sources. [`report.json`](report.json) supplies title, subtitle, language, history heading, history column labels and the website URL used in report and footer links. The five mapped assets are `capability-yes.png`, `capability-no.png`, `header.png` for landscape pages, `header-large.png` for the cover and `header-portrait.png` for regular portrait pages. [`templates/DNS-Abuse-Techniques-Matrix.docx`](templates/DNS-Abuse-Techniques-Matrix.docx) supplies layout only. There is no canonical `source/` directory.

Shared terms and action definitions belong in the CSV files. Markdown uses `{{technique:id}}`, `{{stakeholder:id}}` and `{{action:id|displayLabel}}` includes for repeated definitions. Keep narrative extras such as Law Enforcement and the hosting aside in Markdown. `report.json` and every asset used by the report are build inputs.

The original v1.3 PDF is a design reference. The current source revision fits the original 22-page layout and includes later approved definition edits, so its text is not identical to the older export. Preserve the intended design, including portrait text pages, landscape matrices, fonts, symbols, colours, links, headers and footers. Legitimate content growth can change the page count; CI has no fixed 22-page limit and checks for portrait narrative pages, landscape matrix pages and portrait closing pages. Every PDF proposal still requires independent review.

## Build and review

Use Python 3, LibreOffice and Poppler. The Python requirements include the Markdown parser. For a local human setup:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r matrix/requirements-pdf.txt
brew install --cask libreoffice
brew install poppler
```

Automated contributors with a bundled document runtime should use it. GitHub Actions installs the dependencies into an isolated environment on its runner.

From the repository root, run:

```sh
make pdf
make pdf-check
make pdf-test
```

`make pdf` uses `matrix/scripts/fill_docx_template.py` to combine the Markdown, CSV and assets into a temporary report DOCX based on the layout template. `matrix/scripts/build_docx_pdf.py` exports that report DOCX with LibreOffice to `build/matrix/DNS-Abuse-Techniques-Matrix.pdf`. The filled DOCX is a build output and never canonical source. The build records provenance alongside the output. The template must remain unchanged.

`make pdf-check` checks the template and PDF selected by `DOCX_TEMPLATE` and `REPORT_PDF` (their defaults are shown in the Makefile). It checks Markdown/CSV-derived expected paragraphs, URLs and colored capability-symbol counts in the PDF. It also checks page regions, page dimensions, text bounds and footer rules, then renders comparison previews under `build/matrix/review/`. It does not compare the filled DOCX body with the template body; the DOCX supplies layout only. Review every preview and obtain an independent review before publication. Comparisons are for review and do not prove pixel identity.

`make pdf-test` verifies that Markdown and CSV edits affect the PDF and repeated builds are deterministic. Run it after source or generator changes. `make import` writes imported material to `build/matrix/imported/` for inspection; it must not overwrite canonical files.

## Workflow and publication status

The Markdown/CSV generator is checked on Linux CI. Successful builds propose PDF updates through draft pull requests. Passing checks are not publication approval. Review every page independently. The current source revision fits the old pagination, but future content can grow the page count while retaining the three page regions.

The GitHub Actions workflow builds and checks pull requests with read-only permissions, then uploads the PDF and review previews. A manual workflow run is limited to the default branch. A successful default-branch run may prepare a separate draft pull request with only the latest PDF and `matrix/pdf-build.json`. The bot branch is immutable and keyed by source commit. The workflow does not push to the default branch or merge its pull request. Repository administrators may need to enable the GitHub Actions setting that allows workflows to create pull requests.

All repository changes, including generated PDF updates, go through pull requests. Merge on GitHub. Do not merge locally or push directly to the default branch. Numbered PDFs are immutable release snapshots; create a new snapshot only when a release is requested. Do not begin a v2 redesign without a separate request.

## Validation and historical draft

The normalized CSV under `data/` records individual capability values and full action definitions. Run `make validate` after changing Markdown or CSV sources. Do not hand-edit files under `generated/` or `build/`.

`make draft-pdf` is a historical Pandoc/Typst path for a separate draft. It is not the canonical PDF build path.

The render copy replaces the template's frozen closing-page number with a live PAGE field. PDF checks verify every page number and total, so content growth does not retain the original footer numbering error. The template and v1.3 release PDF stay unchanged.
