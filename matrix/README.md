# DNS Abuse Techniques Matrix PDF

## Canonical source

The PDF is built from [`source/DNS-Abuse-Techniques-Matrix.docx`](source/DNS-Abuse-Techniques-Matrix.docx). Its baseline SHA-256 is `81250da695c618c5db868b49760dc15c6a14e3ebedae1e97c8de7b243a7bc968`. The Markdown and CSV files in this directory are reference data and import derivations. They are not the PDF authoring source.

The original v1.3 PDF is the layout reference. Preserve its 22-page design and pagination, including portrait text pages, landscape matrices, fonts, symbols, colours, links, headers and footers. Change text only when requested. The rolling `DNS-Abuse-Techniques-Matrix_v1-latest.pdf` and the v1.3 reference PDF currently have the same SHA-256: `1a4d37aacf7903e761dd6df89cae957cb02f7ecf2cb582137fccdb1af683ee77`.

## Build and review

Use Python 3, LibreOffice and Poppler. For a local human setup:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r matrix/requirements-pdf.txt
brew install --cask libreoffice
brew install poppler
```

Automated contributors should use the Python/runtime bundled in their environment instead of installing local dependencies.

From the repository root, run:

```sh
make pdf
make pdf-check
make pdf-test
```

`make pdf` uses `matrix/scripts/build_docx_pdf.py` to convert the original DOCX to `build/matrix/DNS-Abuse-Techniques-Matrix.pdf`. It makes temporary, render-only OOXML corrections in a work copy for LibreOffice and reuses the DOCX's embedded fonts. It records build provenance alongside the output. The canonical DOCX must remain unchanged.

`make pdf-check` compares the generated PDF with the v1.3 reference. It checks the 22-page count, page dimensions and orientation, body text when the source is unchanged, text bounds and URL targets. It renders all 22 pages to side-by-side and difference previews under `build/matrix/review/`. Review every preview. The comparison is not a pixel-identity test: LibreOffice can produce small font and line-position differences, observed up to about 15 pt. This observation is not an approved visual tolerance. An independent review remains required before publication.

`make pdf-test` verifies that DOCX edits affect the PDF, repeated builds are deterministic, and the canonical DOCX stays unchanged. Run it after source or generator changes.

## Workflow and publication status

The DOCX-based generator is under verification. Do not treat generated output or a bot pull request as approved for publication until Linux CI quality checks pass and the maintainer confirms that publication can be enabled.

The GitHub Actions workflow builds and checks pull requests with read-only permissions, then uploads the PDF and review previews. A manual workflow run is limited to the default branch. A successful default-branch run may prepare a separate pull request with only the latest PDF and `matrix/pdf-build.json`. The bot branch is immutable and keyed by source commit. The workflow does not push to the default branch or merge its pull request. Repository administrators may need to enable the GitHub Actions setting that allows workflows to create pull requests.

All repository changes, including generated PDF updates, go through pull requests. Merge on GitHub. Do not merge locally or push directly to the default branch. Numbered PDFs are immutable release snapshots; create a new snapshot only when a release is requested. Do not begin a v2 redesign without a separate request.

## Reference data and historical draft

The normalized CSV under `data/` records individual capability values. Run `make validate` after changing reference data. Do not hand-edit files under `generated/` or `build/`.

`make draft-pdf` is a historical Pandoc/Typst path for the structured reference data. It is not the PDF authoring source and must not replace the DOCX-based build.
