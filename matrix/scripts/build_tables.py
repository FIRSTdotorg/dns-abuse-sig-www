#!/usr/bin/env python3
"""Build generated Markdown tables from normalized matrix CSV files."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ACTION_ORDER = ["detect", "mitigate", "prevent"]
STAKEHOLDER_CHUNK_SIZE = 4


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def escape_cell(value: str) -> str:
    value = value.replace("|", "\\|")
    value = value.replace("\n", "<br>")
    return value.strip()


def cell_text(capability: str, note: str) -> str:
    marker = "yes" if capability == "yes" else "no"
    note = note.strip()
    if note:
        return f"{marker}; {escape_cell(note)}"
    return marker


def build_matrix_table(
    action: str,
    action_label: str,
    techniques: list[dict[str, str]],
    stakeholders: list[dict[str, str]],
    rows_by_key: dict[tuple[str, str, str], dict[str, str]],
) -> str:
    first = stakeholders[0]["label"]
    last = stakeholders[-1]["label"]
    lines = [f"### {action_label}: {first} to {last}", ""]
    headers = [f"{action_label}: Technique"] + [escape_cell(row["label"]) for row in stakeholders]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

    for technique in techniques:
        cells = [escape_cell(technique["label"])]
        for stakeholder in stakeholders:
            row = rows_by_key[(action, technique["technique_id"], stakeholder["stakeholder_id"])]
            cells.append(cell_text(row["capability"], row["note"]))
        lines.append("| " + " | ".join(cells) + " |")

    return "\n".join(lines)


def build_definition_table(title: str, first_column: str, rows: list[dict[str, str]], id_key: str) -> str:
    lines = [f"## {title}", ""]
    lines.append(f"| {first_column} | Description |")
    lines.append("| --- | --- |")
    for row in rows:
        lines.append(
            "| "
            + escape_cell(row["label"])
            + " | "
            + escape_cell(row.get("description", ""))
            + " |"
        )
    return "\n".join(lines)


def build_version_history(rows: list[dict[str, str]]) -> str:
    lines = ["## Version History", ""]
    lines.append("| Version | Date | Comment |")
    lines.append("| --- | --- | --- |")
    for row in rows:
        lines.append(
            "| "
            + escape_cell(row["version"])
            + " | "
            + escape_cell(row["date"])
            + " | "
            + escape_cell(row["comment"])
            + " |"
        )
    return "\n".join(lines)


def build(matrix_dir: Path) -> Path:
    data_dir = matrix_dir / "data"
    actions = read_csv(data_dir / "actions.csv")
    techniques = read_csv(data_dir / "techniques.csv")
    stakeholders = read_csv(data_dir / "stakeholders.csv")
    matrix = read_csv(data_dir / "matrix.csv")
    versions = read_csv(data_dir / "version_history.csv")

    action_labels = {row["action"]: row["label"] for row in actions}
    rows_by_key = {
        (row["action"], row["technique_id"], row["stakeholder_id"]): row
        for row in matrix
    }

    parts = ["The following tables are generated from `data/matrix.csv`."]

    for action in ACTION_ORDER:
        for offset in range(0, len(stakeholders), STAKEHOLDER_CHUNK_SIZE):
            stakeholder_chunk = stakeholders[offset : offset + STAKEHOLDER_CHUNK_SIZE]
            parts.append(
                build_matrix_table(
                    action,
                    action_labels[action],
                    techniques,
                    stakeholder_chunk,
                    rows_by_key,
                )
            )

    parts.append(build_version_history(versions))

    generated_dir = matrix_dir / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)
    path = generated_dir / "matrix-tables.md"
    path.write_text("\n\n".join(parts).strip() + "\n", encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("matrix_dir", type=Path, nargs="?", default=Path("matrix"))
    args = parser.parse_args()

    path = build(args.matrix_dir)
    print(path)


if __name__ == "__main__":
    main()
