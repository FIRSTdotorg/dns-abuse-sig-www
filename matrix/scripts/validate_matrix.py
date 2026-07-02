#!/usr/bin/env python3
"""Validate the normalized DNS Abuse Techniques Matrix data."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


EXPECTED_ACTIONS = {"detect", "mitigate", "prevent"}
EXPECTED_CAPABILITIES = {"yes", "no"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate(matrix_dir: Path) -> list[str]:
    data_dir = matrix_dir / "data"
    errors: list[str] = []

    actions = read_csv(data_dir / "actions.csv")
    stakeholders = read_csv(data_dir / "stakeholders.csv")
    techniques = read_csv(data_dir / "techniques.csv")
    matrix = read_csv(data_dir / "matrix.csv")
    versions = read_csv(data_dir / "version_history.csv")

    action_ids = {row["action"] for row in actions}
    stakeholder_ids = {row["stakeholder_id"] for row in stakeholders}
    technique_ids = {row["technique_id"] for row in techniques}

    if action_ids != EXPECTED_ACTIONS:
        fail(errors, f"actions.csv must contain {sorted(EXPECTED_ACTIONS)}, found {sorted(action_ids)}")

    for label, ids in (("stakeholder", stakeholder_ids), ("technique", technique_ids)):
        if len(ids) == 0:
            fail(errors, f"{label} list is empty")

    expected_count = len(action_ids) * len(stakeholder_ids) * len(technique_ids)
    if len(matrix) != expected_count:
        fail(errors, f"matrix.csv has {len(matrix)} rows; expected {expected_count}")

    seen: set[tuple[str, str, str]] = set()
    for index, row in enumerate(matrix, start=2):
        action = row.get("action", "")
        technique_id = row.get("technique_id", "")
        stakeholder_id = row.get("stakeholder_id", "")
        capability = row.get("capability", "")
        key = (action, technique_id, stakeholder_id)

        if action not in action_ids:
            fail(errors, f"matrix.csv:{index}: unknown action {action!r}")
        if technique_id not in technique_ids:
            fail(errors, f"matrix.csv:{index}: unknown technique_id {technique_id!r}")
        if stakeholder_id not in stakeholder_ids:
            fail(errors, f"matrix.csv:{index}: unknown stakeholder_id {stakeholder_id!r}")
        if capability not in EXPECTED_CAPABILITIES:
            fail(errors, f"matrix.csv:{index}: capability must be yes/no, found {capability!r}")
        if key in seen:
            fail(errors, f"matrix.csv:{index}: duplicate row for {key}")
        seen.add(key)

    for filename, rows, id_column in (
        ("actions.csv", actions, "action"),
        ("stakeholders.csv", stakeholders, "stakeholder_id"),
        ("techniques.csv", techniques, "technique_id"),
    ):
        seen_ids: set[str] = set()
        for index, row in enumerate(rows, start=2):
            item_id = row.get(id_column, "")
            if not item_id:
                fail(errors, f"{filename}:{index}: missing {id_column}")
            if item_id in seen_ids:
                fail(errors, f"{filename}:{index}: duplicate {id_column} {item_id!r}")
            seen_ids.add(item_id)
            if not row.get("label", ""):
                fail(errors, f"{filename}:{index}: missing label")

    if not versions:
        fail(errors, "version_history.csv is empty")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("matrix_dir", type=Path, nargs="?", default=Path("matrix"))
    args = parser.parse_args()

    errors = validate(args.matrix_dir)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("matrix data OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

