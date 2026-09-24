#!/usr/bin/env python3
"""Offline contract for restricted passwordless sudo."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_role_supports_caller_supplied_passwordless_commands() -> None:
    defaults = (ROOT / "roles/sudo/defaults/main.yml").read_text()
    task = (ROOT / "roles/sudo/tasks/passwordless_privilege.yml").read_text()
    spec = (ROOT / "roles/sudo/meta/argument_specs.yml").read_text()

    assert "passwordless_commands: []" in defaults
    assert "passwordless_commands | join(', ')" in task
    assert "else 'ALL'" in task
    assert "passwordless_commands:" in spec


def test_role_documentation_keeps_proxmox_commands_at_the_caller() -> None:
    readme = (ROOT / "roles/sudo/README.md").read_text()
    assert "/usr/bin/pvesh get *" in readme
    assert "caller" in readme.lower()


if __name__ == "__main__":
    test_role_supports_caller_supplied_passwordless_commands()
    test_role_documentation_keeps_proxmox_commands_at_the_caller()
    print("sudo passwordless allowlist contract checks passed")
