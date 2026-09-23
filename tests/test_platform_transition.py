#!/usr/bin/env python3
"""Offline contract for the approved platform ownership transition."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PlatformTransitionTests(unittest.TestCase):
    def test_talos_replaces_the_legacy_microk8s_entrypoint(self) -> None:
        self.assertFalse((ROOT / "playbook.yml").exists())
        self.assertTrue((ROOT / "tofu" / "talos" / "versions.tf").is_file())
        self.assertTrue((ROOT / "kubernetes" / "clusters" / "talos" / "infrastructure.yaml").is_file())

    def test_retired_controller_automation_is_removed(self) -> None:
        for path in ("playbooks/awx", "playbooks/podman", "playbooks/podman-semaphore"):
            self.assertFalse((ROOT / path).exists(), path)

    def test_sudo_role_maps_prefixed_compatibility_inputs(self) -> None:
        compatibility = (ROOT / "roles" / "sudo" / "tasks" / "compatibility.yml").read_text()
        for alias, target in (
            ("sudo_privileged_user", "privileged_user"),
            ("sudo_privileged_group", "privilege_group"),
            ("sudo_password_required", "password_required"),
            ("sudo_preserve_user", "preserve_user"),
        ):
            self.assertIn(f"{target}: \"{{{{ {alias} }}}}\"", compatibility)


if __name__ == "__main__":
    unittest.main()
