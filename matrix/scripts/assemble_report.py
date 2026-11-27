#!/usr/bin/env python3
"""Assemble the generated Pandoc Markdown input for the PDF build."""

from __future__ import annotations

import argparse
import json
import re
from fill_docx_template import expand, read_csv
from build_tables import build_matrix_table, build_version_history
from pathlib import Path


CONTENT_ORDER = [
    "01-introduction.md",
    "02-terms.md",
    "03-examples-of-techniques.md",
    "04-advice-for-incident-responders.md",
    "05-abuse-matrices.md",
    "06-acknowledgements.md",
]


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def assemble(matrix_dir: Path, out_path: Path) -> None:
    metadata = json.loads((matrix_dir / "report.json").read_text(encoding="utf-8"))
    lines = ["---"]
    for key in ("title", "subtitle", "website", "language"):
        if key in metadata:
            lines.append(f"{key}: {yaml_quote(metadata[key])}")
    lines.extend(["---", ""])

    data = {}
    for kind, filename, identifier in [('action','actions.csv','action'),('technique','techniques.csv','technique_id'),('stakeholder','stakeholders.csv','stakeholder_id')]:
        data[kind] = {row[identifier]:row for row in read_csv(matrix_dir/'data'/filename)}
    rows = {(r['action'],r['technique_id'],r['stakeholder_id']):r for r in read_csv(matrix_dir/'data/matrix.csv')}
    seen = set()
    def table(match):
        action=match[1]
        stakeholders=list(data['stakeholder'].values())
        return '\n\n'.join(build_matrix_table(action,data['action'][action]['label'],list(data['technique'].values()),stakeholders[n:n+4],rows) for n in range(0,len(stakeholders),4))
    content_dir = matrix_dir / "content"
    for relative in CONTENT_ORDER:
        path = (content_dir / relative).resolve()
        if not path.exists():
            raise ValueError(f"Missing source chapter: {path}")
        text=expand(path.read_text(encoding="utf-8"),data,seen)
        lines.append(re.sub(r"\{\{matrix:(detect|mitigate|prevent)\}\}",table,text).strip())
        lines.append("")

    history=build_version_history(read_csv(matrix_dir/'data/version_history.csv'))
    history=history.replace('## Version History','## '+metadata['history_heading']).replace('| Version | Date | Comment |','| '+' | '.join(metadata['history_columns'])+' |')
    lines.append(history)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("matrix_dir", type=Path, nargs="?", default=Path("matrix"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    assemble(args.matrix_dir, args.out)
    print(args.out)


if __name__ == "__main__":
    main()
