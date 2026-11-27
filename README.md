# FIRST DNS Abuse SIG

This repo holds the source content and publishing tooling for the [FIRST](https://www.first.org/) **DNS Abuse Special Interest Group (SIG)** website and its primary publication, the **DNS Abuse Techniques Matrix**.

> **Looking for the SIG itself?** The official homepage is <https://www.first.org/global/sigs/dns> - the authoritative source for the SIG's mission, goals, meeting schedule, chairs, and how to join. It is generated from the contents of this repository, so the two should always agree; if they ever drift, the homepage wins. This README covers what lives here and how to build it.

## Repository layout

| Path | Contents |
| --- | --- |
| [`index.md`](index.md) | Site landing page. |
| [`policies.md`](policies.md) | Code of Conduct and information-sharing policies. |
| [`dns-abuse-examples.md`](dns-abuse-examples.md) | Real-world examples of DNS abuse techniques. |
| [`stakeholder-advice/`](stakeholder-advice/) | Per-technique advice documents (one Markdown file per abuse technique) plus an index. |
| [`matrix/`](matrix/) | Canonical Markdown and CSV content, assets, DOCX layout template and PDF build pipeline. See [`matrix/README.md`](matrix/README.md). |
| [`DNS-Abuse-Techniques-Matrix_v1.3.pdf`](DNS-Abuse-Techniques-Matrix_v1.3.pdf) | Current released Matrix snapshot. |
| [`DNS-Abuse-Techniques-Matrix_v1-latest.pdf`](DNS-Abuse-Techniques-Matrix_v1-latest.pdf) | Rolling working copy. Actions proposes updates through draft PRs. |
| [`DNS-Abuse-Techniques-Matrix_v1.1.pdf`](DNS-Abuse-Techniques-Matrix_v1.1.pdf) / [`*-ja.pdf`](DNS-Abuse-Techniques-Matrix_v1.1-ja.pdf) | Prior version and Japanese translation of v1.1. |
| [`Makefile`](Makefile) | Build targets for the Matrix pipeline. |
| [`AGENTS.md`](AGENTS.md) | Instructions for automated/agentic edits to the Matrix pipeline. |
| [`CHANGES.md`](CHANGES.md) | Reverse-chronological log of notable SIG and document changes. |
| [`CONTRIBUTORS.md`](CONTRIBUTORS.md) | List of contributors. |

The Markdown pages carry an HTML-comment front matter block (`title:`) and are rendered into the FIRST-hosted site.

## The DNS Abuse Techniques Matrix

The Matrix maps, for each DNS abuse technique, whether a given stakeholder is positioned to **detect**, **mitigate**, or **prevent** it. It is intended for incident responders: during an incident, look up the relevant technique under the appropriate action to see which stakeholders you might contact for help.

It is also used beyond this repo. An HTML version is maintained by JPCERT/CC at <https://firstdotorg.github.io/dns-abuse-sig/>, and it has been incorporated into the [MISP Galaxy](https://github.com/MISP/misp-galaxy#first-dns-abuse-techniques-matrix) and the [OASIS STIX Event Type Vocabulary](https://github.com/oasis-open/cti-stix-common-objects/blob/main/extension-definition-specifications/incident-ef7/Incident%20Extension%20Suite.adoc#44-event-type-vocabulary).

### Data model

The canonical report content is in Markdown under `matrix/content/`. Normalized CSV under `matrix/data/` holds repeated definitions and matrix data, so diffs surface individual changes rather than reflowed wide tables. The DOCX in `matrix/templates/` provides layout only. `matrix/report.json` owns title, subtitle, language, history heading, history column labels and the website URL used in report and footer links. The five assets in `matrix/assets/` provide yes/no markers, landscape headers, a cover header and a regular portrait header:

- `actions.csv` - the three incident-response actions (detect, mitigate, prevent).
- `techniques.csv` - abuse techniques and their descriptions.
- `stakeholders.csv` - stakeholder columns and definitions.
- `matrix.csv` - one row per (action, technique, stakeholder) with a `yes`/`no` `capability` and an optional `note`.
- `version_history.csv` - publication history.

Markdown references shared definitions with `{{technique:id}}`, `{{stakeholder:id}}` and `{{action:id|displayLabel}}` includes. Rows are validated against `matrix/schemas/matrix.schema.json`. Narrative extras, including Law Enforcement and the hosting aside, remain in Markdown.

## Building the Matrix PDF

The v1.3 PDF is the design reference. The current source revision fits the original 22-page layout and includes later approved definition edits, so its text is not identical to the older export. The build fills a temporary report DOCX from Markdown, CSV and assets, then exports it with LibreOffice. The filled report DOCX is a build output, never canonical source. Legitimate content growth can change the page count; the CI check has no fixed 22-page limit and expects portrait narrative pages, landscape matrix pages and portrait closing pages. PDF proposals still need independent review.

`make pdf` builds from Markdown and CSV using the DOCX layout template. `make pdf-check` checks source paragraph, URL and colored capability-symbol coverage in the PDF, then reviews page regions, text bounds and footers. It does not compare the filled DOCX body with template body text. `make pdf-test` checks Markdown and CSV source sensitivity and deterministic output. The generator is checked on Linux CI. Every proposal requires layout review before publication. The historical Pandoc/Typst target creates a separate draft. See [`matrix/README.md`](matrix/README.md) for setup and review requirements.

The workflow builds and checks pull requests without write permissions. A successful default-branch build may open a separate draft PR for the latest PDF and its provenance JSON. It does not push to the default branch or merge. All repository changes, including generated PDFs, require pull requests. Merges happen on GitHub.

## Contributing

Contributions are welcome. Record notable changes in `CHANGES.md` (reverse chronological) and add contributors to `CONTRIBUTORS.md`. For how to join the SIG and the applicable policies, see the homepage above and `policies.md`.
