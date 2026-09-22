#!/usr/bin/env python3
"""Offline contract checks for the repository validation matrix."""

import fnmatch
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "tests" / "validation-matrix.json"
SOURCE_ROOTS = ("playbook.yml", "roles", "playbooks", "nvidia", "proxmox-util")
IGNORED_PARTS = {".git", ".ansible", ".venv", ".nb-pm", "node_modules", "__pycache__"}


def source_files() -> set[str]:
    paths: set[str] = set()
    root_playbook = ROOT / "playbook.yml"
    if root_playbook.is_file():
        paths.add(root_playbook.name)
    for root_name in SOURCE_ROOTS[1:]:
        root = ROOT / root_name
        if not root.is_dir():
            continue
        for path in root.rglob("*.y*ml"):
            if path.is_file() and not IGNORED_PARTS.intersection(path.relative_to(ROOT).parts):
                paths.add(path.relative_to(ROOT).as_posix())
    return paths


class ValidationMatrixTests(unittest.TestCase):
    def test_matrix_covers_every_first_party_yaml_source(self) -> None:
        matrix = json.loads(MATRIX.read_text())
        entries = matrix["entries"]
        matched_by_path = {path: 0 for path in source_files()}

        for entry in entries:
            self.assertIn(entry["evidence"], {"offline", "discovery", "molecule", "blocked", "dependency-review"})
            self.assertIn(entry["tier"], {"read-only", "routine-idempotent", "guarded-mutation", "metadata"})
            if entry["evidence"] == "blocked":
                self.assertTrue(entry.get("reason"))
            matched = {path for path in source_files() if fnmatch.fnmatch(path, entry["pattern"])}
            self.assertTrue(matched, entry["pattern"])
            for path in matched:
                matched_by_path[path] += 1

        self.assertEqual(set(matched_by_path), set(source_files()))
        self.assertTrue(all(count == 1 for count in matched_by_path.values()), matched_by_path)

    def test_development_requirements_are_pinned(self) -> None:
        requirements = (ROOT / "requirements-dev.txt").read_text().splitlines()
        for requirement in ("ansible-core", "ansible-lint", "molecule"):
            self.assertTrue(any(line.startswith(f"{requirement}==") for line in requirements))


if __name__ == "__main__":
    unittest.main()
