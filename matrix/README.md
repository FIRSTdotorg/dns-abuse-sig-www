# DNS Abuse Techniques Matrix PDF

## Required layout

The original `DNS-Abuse-Techniques-Matrix_v1.3.pdf` is the layout reference for the v1 series. It has 22 pages, with portrait text pages and landscape matrices. Preserve its design and pagination. Change text only where requested. Preserve fonts, full-width matrices, capability symbols, colours, links, headers and footers.

The latest PDF is restored to that exact original as a baseline. Its SHA-256 is `1a4d37aacf7903e761dd6df89cae957cb02f7ecf2cb582137fccdb1af683ee77`.

## Editable build status

The current Pandoc/Typst build does not match v1.3 and must not publish the working copy. Automatic PDF publication is paused while a faithful editable build is prepared. Copying the original PDF restores the baseline, but does not complete the editable rebuild.

The Markdown, CSV, assets, metadata and template remain in the repository. `make validate` checks matrix data. `make pdf` still runs the existing draft build and writes `build/matrix/DNS-Abuse-Techniques-Matrix.pdf`; this is experimental output and must not replace the reviewed latest PDF.

The original DOCX is also available locally. The authoring format for the replacement build must preserve the v1.3 design. Do not discard source content or assume that a new renderer matches the original.

## Review and publication

Render every page and compare it with the original before publication. Check requested content changes, pagination, text extraction and link targets. Obtain an independent review. Do not publish a substitute design or begin a v2 redesign without a separate request.

All repository changes, including generated PDF updates, require a GitHub pull request. Merge on GitHub. Do not merge locally or push directly to the default branch. When automated PDF publication resumes, it must open or update a pull request and must not push to the default branch or merge its own changes.

Numbered PDFs remain immutable snapshots. Create a new numbered file only when a release is requested.
