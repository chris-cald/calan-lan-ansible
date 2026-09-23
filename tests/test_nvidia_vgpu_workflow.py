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
        driver = (ROOT / "nvidia" / "tasks" / "nvidia_vgpu_manager.yml").read_text()
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

    def test_bespoke_guest_patch_is_explicit_and_hash_verified(self) -> None:
        playbook = (ROOT / "nvidia" / "guest-playbook.yml").read_text()
        patch = (ROOT / "nvidia" / "tasks" / "nvidia_guest_nvenc_patch.yml").read_text()
        self.assertIn("nvidia_guest_apply: false", playbook)
        self.assertIn("nvidia_guest_nvenc_patch_apply: false", playbook)
        self.assertNotIn("vars_prompt", playbook)
        for variable in ("nvidia_guest_nvenc_patch_path", "nvidia_guest_nvenc_patch_sha256"):
            self.assertIn(variable, patch)
        self.assertNotIn("ansible.builtin.git", patch)


if __name__ == "__main__":
    unittest.main()
