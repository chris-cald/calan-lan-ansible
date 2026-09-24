#!/usr/bin/env python3
"""Offline contract for the QEMU guest-agent package policy."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class QemuGuestAgentPolicyTests(unittest.TestCase):
    def test_guest_agent_install_does_not_upgrade_to_latest(self) -> None:
        task = (ROOT / "proxmox-util" / "qemu.yaml").read_text()
        self.assertIn("name: qemu-guest-agent", task)
        self.assertIn("state: present", task)
        self.assertNotIn("state: latest", task)


if __name__ == "__main__":
    unittest.main()
