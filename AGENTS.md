# Repository Instructions

These instructions apply to all contributors and tools.

## Changes and merges

- Submit repository changes through a GitHub pull request, including generated PDF updates.
- Merge pull requests on GitHub. Do not merge branches locally or push directly to the default branch.
- Use concise wording and normal ASCII hyphens in prose and pull request text.

## Matrix PDF source and build

- The canonical PDF authoring source is `matrix/source/DNS-Abuse-Techniques-Matrix.docx`. Its baseline SHA-256 is `81250da695c618c5db868b49760dc15c6a14e3ebedae1e97c8de7b243a7bc968`.
- Build the PDF from that DOCX with `make pdf`. Do not author the PDF from Markdown or CSV. Those files are reference data and import derivations.
- `build_docx_pdf.py` applies temporary, render-only OOXML corrections to a work copy for LibreOffice. It must not change the canonical DOCX. Reuse fonts embedded in the source.
- Preserve the v1.3 design and pagination. Change source text only when requested. Preserve page orientation, matrices, symbols, colours, links, headers, footers and fonts.
- Run `make pdf-check` after building. It checks the 22-page count, page dimensions and orientation, body text for the unchanged baseline, text bounds and URL targets. It creates side-by-side and difference previews for all pages under `build/matrix/review/`.
- Review every preview and obtain an independent review before publication. The comparison is not a pixel-identity test. LibreOffice can produce small font and line-position differences, observed up to about 15 pt. This is not an approved visual tolerance and does not remove the independent-review gate.
- Run `make pdf-test` to check that source edits affect the output, builds are deterministic and the canonical DOCX remains unchanged.
- The generator runs in Linux CI. A successful check prepares a proposal, not publication approval. The initial migrated PDF still requires user layout approval because it is not pixel-identical to the Google Docs export. Do not waive the original fidelity requirement without that approval.
- The workflow builds and checks pull requests without write permissions, then uploads the PDF and review previews. A successful default-branch build may prepare a separate draft pull request containing the latest PDF and `matrix/pdf-build.json`. It must not push to the default branch or merge automatically. Bot branches are immutable and keyed by the source commit.
- The repository setting to allow GitHub Actions to create pull requests may need to be enabled by an administrator. Do not bypass this setting or push generated files directly.
- `DNS-Abuse-Techniques-Matrix_v1-latest.pdf` is the rolling working copy. Numbered PDFs are immutable release snapshots; create a new snapshot only when a release is requested. Do not begin a v2 redesign without a separate request.
- For a local human setup, use Python 3 with a virtual environment and `matrix/requirements-pdf.txt`, then install LibreOffice and Poppler. Automated contributors with a bundled document runtime should use it. GitHub Actions uses an isolated dependency environment on its runner.
- The historical `make draft-pdf` target uses Pandoc and Typst for the structured reference data. It is not the PDF authoring path.

## Reference data

- Keep `matrix/data/matrix.csv` normalized: one row per action, technique and stakeholder combination, with capability values of `yes` or `no`.
- Run `make validate` after changing reference data.
- Do not hand-edit `matrix/generated/` or `build/` files.
