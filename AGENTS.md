# Repository Instructions

These instructions apply to all contributors and tools.

## Changes and merges

- Submit every repository change through a GitHub pull request, including generated PDF updates.
- Merge pull requests on GitHub. Do not merge branches locally or push directly to the default branch.
- Use concise wording and normal ASCII hyphens in prose and pull request text.

## PDF publication

- Use the original `DNS-Abuse-Techniques-Matrix_v1.3.pdf` as the layout reference for the v1 series.
- Preserve its design and pagination for future edits. Change text only where requested. Preserve portrait and landscape page sizes, fonts, full-width matrices, capability symbols, colours, links, headers and footers.
- The latest PDF is restored to the exact v1.3 file as the baseline. A faithful editable rebuild is still required. Do not treat copying the PDF as completion of that rebuild.
- Do not publish the current Pandoc/Typst output. Its layout does not reproduce v1.3. Keep the editable Markdown and CSV sources. Automatic PDF publication is paused until the replacement build meets the layout requirement.
- Render and compare every page against the reference before publication. For requested content edits, verify that visual changes are confined to the intended areas, text is extractable and links still work.
- Obtain an independent review before publishing a changed PDF. Do not substitute a new design for the original.
- `DNS-Abuse-Techniques-Matrix_v1-latest.pdf` is the rolling working copy. Its updates also require a pull request.
- Numbered PDFs are immutable release snapshots. Create a new snapshot only when a release is requested.
- Do not begin a v2 redesign without a separate request.

## Reference data

- Keep `matrix/data/matrix.csv` normalized: one row per action, technique and stakeholder combination, with capability values of `yes` or `no`.
- Run `make validate` after changing reference data.
- Do not hand-edit `matrix/generated/` or `build/` files.
