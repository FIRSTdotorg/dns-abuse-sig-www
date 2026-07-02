# DNS Abuse Techniques Matrix Publishing Pipeline

This directory is the new source of truth for the PDF publication.

## Source Files

- `content/` contains the narrative Markdown.
- `data/actions.csv` defines the three incident-response actions.
- `data/techniques.csv` defines abuse techniques and their descriptions.
- `data/stakeholders.csv` defines stakeholder columns.
- `data/matrix.csv` contains one normalized row per action, technique, and stakeholder.
- `data/version_history.csv` contains the publication history table.
- `assets/` contains logos and small symbols extracted from the source DOCX.
- `templates/dns-abuse-report.typ` controls PDF page layout, headers, footers, fonts, and table defaults.

## Commands

From the repository root:

```bash
make import DOCX_SOURCE="../DNS Abuse Techniques Matrix.docx"
make validate
make assemble
make pdf
```

`make import` re-extracts Markdown, CSV, and assets from the Google Docs DOCX export.

`make validate` checks the normalized data model.

`make assemble` writes `build/matrix/report.md`, the generated Pandoc input.

`make pdf` requires `pandoc` and `typst` on PATH and writes `build/matrix/DNS-Abuse-Techniques-Matrix.pdf`.

On macOS, the expected local toolchain is:

```bash
brew install pandoc typst
```

## Editing Rules

Edit source files in `content/`, `data/`, `assets/`, and `templates/`.

Do not edit `generated/` or `build/` files directly.

The matrix data is intentionally normalized so diffs show individual capability changes instead of reflowed wide tables.

