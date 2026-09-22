#!/usr/bin/env python3
"""Offline checks for caller-owned Talos vGPU compatibility manifests."""

import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tests" / "validate_vgpu_compatibility_manifest.py"


class VgpuCompatibilityManifestTests(unittest.TestCase):
    def test_accepts_a_complete_compatible_manifest(self) -> None:
        manifest = """gpu_model: test-gpu
vgpu_profile: test-profile
proxmox_version: test
host_vgpu_manager_branch: 550
talos_version: test
talos_kernel: test
guest_driver_branch: 550
license_reviewed: true
compatibility_reference: https://example.invalid/matrix
extension_source: protected local build recipe
"""
        with tempfile.NamedTemporaryFile("w", suffix=".yml") as file:
            file.write(manifest)
            file.flush()
            result = subprocess.run(["python3", VALIDATOR, file.name], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_mismatched_driver_branches(self) -> None:
        manifest = "host_vgpu_manager_branch: 550\nguest_driver_branch: 535\n"
        with tempfile.NamedTemporaryFile("w", suffix=".yml") as file:
            file.write(manifest)
            file.flush()
            result = subprocess.run(["python3", VALIDATOR, file.name], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
