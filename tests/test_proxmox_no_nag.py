#!/usr/bin/env python3
"""Offline contract for the guarded Proxmox no-nag role."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text()


def test_role_is_default_disabled_and_explicitly_guarded() -> None:
    defaults = read("roles/proxmox_no_nag/defaults/main.yml")
    guard = read("roles/proxmox_no_nag/tasks/guard.yml")
    assert "proxmox_no_nag_apply: false" in defaults
    assert "proxmox_no_nag_confirmation" in guard
    assert "apply-proxmox-no-nag" in guard


def test_role_uses_local_pinned_source_and_hook_without_remote_execution() -> None:
    tasks = read("roles/proxmox_no_nag/tasks/main.yml")
    source = read("roles/proxmox_no_nag/templates/proxmox-no-subscription.sources.j2")
    hook = read("roles/proxmox_no_nag/files/proxmox-remove-nag")
    assert "pve-no-subscription" in source
    assert "Suites: {{ proxmox_no_nag_debian_suite }}" in source
    assert "proxmox_no_nag_debian_suite: trixie" in read("roles/proxmox_no_nag/defaults/main.yml")
    assert "Signed-By: {{ proxmox_no_nag_keyring }}" in source
    assert "proxmox-archive-keyring.gpg" in read("roles/proxmox_no_nag/defaults/main.yml")
    assert "ansible.builtin.stat" in tasks
    assert "NoMoreNagging" in tasks
    assert "DPkg::Post-Invoke" in tasks
    assert "NoMoreNagging" in hook
    assert "curl" not in tasks
    assert "ansible.builtin.git" not in tasks


def test_playbook_requires_a_caller_owned_inventory() -> None:
    playbook = read("playbooks/proxmox-no-nag.yml")
    assert "proxmox_no_nag_inventory" in playbook
    assert "ansible_inventory_sources" in playbook
    assert "proxmox_no_nag" in playbook


if __name__ == "__main__":
    test_role_is_default_disabled_and_explicitly_guarded()
    test_role_uses_local_pinned_source_and_hook_without_remote_execution()
    test_playbook_requires_a_caller_owned_inventory()
    print("Proxmox no-nag role contract checks passed")
