#!/usr/bin/env python3
"""Assemble the generated Pandoc Markdown input for the PDF build."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


CONTENT_ORDER = [
    "01-introduction.md",
    "02-terms.md",
    "03-examples-of-techniques.md",
    "04-advice-for-incident-responders.md",
    "05-abuse-matrices.md",
    "../generated/matrix-tables.md",
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

    content_dir = matrix_dir / "content"
    for relative in CONTENT_ORDER:
        path = (content_dir / relative).resolve()
        if not path.exists():
            continue
        lines.append(path.read_text(encoding="utf-8").strip())
        lines.append("")

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
