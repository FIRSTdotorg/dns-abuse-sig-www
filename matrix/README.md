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

## Build the PDF

Install Python 3, Pandoc and Typst. On macOS with Homebrew:

```bash
brew install python pandoc typst
```

From the repository root, run:

```bash
make pdf
```

This validates the data, generates tables and assembles the report before writing `build/matrix/DNS-Abuse-Techniques-Matrix.pdf`. Check the PDF for missing sections, tables and layout problems. `make validate`, `make tables` and `make assemble` can also be run separately. The PDF template uses Arial when available, and Liberation Sans as a fallback. Install one of these fonts for a consistent layout.

`make import DOCX_SOURCE="../DNS Abuse Techniques Matrix.docx"` is only for a deliberate re-import from a Google Docs DOCX export. It requires `python-docx` and overwrites source content and data. Do not run it for a normal rebuild.

## Working copy and releases

GitHub Actions rebuilds and commits `DNS-Abuse-Techniques-Matrix-latest.pdf` when PDF inputs change on the default branch. The workflow also supports a manual run. It needs permission to write repository contents, and branch rules must allow the workflow to push. If a run fails, inspect the Actions log and rerun it after resolving the problem.

The latest PDF is a working copy, not a numbered release. Create a versioned PDF only when a release is requested: update the version history and other release details, build and review the PDF, then copy the reviewed build to a new versioned filename. Update publication links and `CHANGES.md` as appropriate. Do not replace existing versioned snapshots during routine builds.

## Editing Rules

Edit source files in `content/`, `data/`, `assets/`, and `templates/`.

Do not edit `generated/` or `build/` files directly.

The matrix data is intentionally normalized so diffs show individual capability changes instead of reflowed wide tables.

