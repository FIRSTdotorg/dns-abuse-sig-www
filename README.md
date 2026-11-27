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
| [`matrix/`](matrix/) | Canonical DOCX source, reference data and PDF build pipeline. See [`matrix/README.md`](matrix/README.md). |
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

The PDF's canonical authoring source is `matrix/source/DNS-Abuse-Techniques-Matrix.docx`. Normalized CSV under `matrix/data/` is structured reference data, so diffs surface individual capability changes rather than reflowed wide tables:

- `actions.csv` - the three incident-response actions (detect, mitigate, prevent).
- `techniques.csv` - abuse techniques and their descriptions.
- `stakeholders.csv` - stakeholder columns and definitions.
- `matrix.csv` - one row per (action, technique, stakeholder) with a `yes`/`no` `capability` and an optional `note`.
- `version_history.csv` - publication history.

Rows are validated against `matrix/schemas/matrix.schema.json`.

## Building the Matrix PDF

The v1.3 PDF is the design and pagination reference. Future v1 updates must preserve that design, with text changing only where requested. The canonical DOCX is the input to the replacement PDF build.

`make pdf` builds from the DOCX with LibreOffice. `make pdf-check` creates side-by-side and difference previews for all 22 pages and checks page layout, text and links. `make pdf-test` checks source sensitivity, deterministic output and source integrity. The generator is checked on Linux CI. Generated PDF proposals still require independent layout review; the initial migrated PDF also requires user approval of remaining renderer differences. The historical Pandoc/Typst target is a draft for reference data, not the PDF authoring path. See [`matrix/README.md`](matrix/README.md) for setup and review requirements.

The workflow builds and checks pull requests without write permissions. A successful default-branch build may open a separate draft PR for the latest PDF and its provenance JSON. It does not push to the default branch or merge. All repository changes, including generated PDFs, require pull requests. Merges happen on GitHub.

## Contributing

Contributions are welcome. Record notable changes in `CHANGES.md` (reverse chronological) and add contributors to `CONTRIBUTORS.md`. For how to join the SIG and the applicable policies, see the homepage above and `policies.md`.
