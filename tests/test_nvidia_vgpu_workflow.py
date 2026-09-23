#!/usr/bin/env python3
"""Offline contract for the self-supported vGPU host workflow."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class NvidiaVgpuWorkflowTests(unittest.TestCase):
    def test_host_mutation_is_default_disabled_and_confirmed(self) -> None:
        playbook = (ROOT / "nvidia" / "host-playbook.yml").read_text()
        self.assertIn("nvidia_vgpu_apply: false", playbook)
        self.assertIn("nvidia_vgpu_reboot: false", playbook)
        self.assertIn("tasks/nvidia_vgpu_guard.yml", playbook)

    def test_guard_requires_artifacts_and_typed_confirmation(self) -> None:
        guard = (ROOT / "nvidia" / "tasks" / "nvidia_vgpu_guard.yml").read_text()
        for variable in (
            "nvidia_vgpu_confirmation",
            "nvidia_vgpu_driver_path",
            "nvidia_vgpu_driver_sha256",
            "nvidia_vgpu_unlock_path",
            "nvidia_vgpu_unlock_sha256",
        ):
            self.assertIn(variable, guard)

    def test_unlock_uses_caller_supplied_pinned_artifacts(self) -> None:
        enable = (ROOT / "nvidia" / "tasks" / "nvidia_enable_vgpu.yml").read_text()
        driver = (ROOT / "nvidia" / "tasks" / "nvidia_driver.yml").read_text()
        self.assertNotIn("ansible.builtin.git", enable)
        self.assertNotIn("cargo build", enable)
        self.assertNotIn("version: master", enable)
        for variable in ("nvidia_vgpu_driver_path", "nvidia_vgpu_driver_sha256"):
            self.assertIn(variable, driver)
        for variable in ("nvidia_vgpu_unlock_path", "nvidia_vgpu_unlock_sha256"):
            self.assertIn(variable, enable)

    def test_discovery_does_not_use_shell_pipelines(self) -> None:
        facts = (ROOT / "nvidia" / "tasks" / "gather_nvidia_facts.yml").read_text()
        self.assertNotIn("ansible.builtin.shell", facts)

    def test_guest_entrypoint_does_not_apply_the_nvenc_unlock_patch(self) -> None:
        playbook = (ROOT / "nvidia" / "guest-playbook.yml").read_text()
        self.assertNotIn("nvidia_enc_unlock_patch.yml", playbook)


if __name__ == "__main__":
    unittest.main()
