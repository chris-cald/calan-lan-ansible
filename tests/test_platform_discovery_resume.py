#!/usr/bin/env python3
"""Offline contract for protected discovery, resume state, and pipeline handoff."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text()


def test_discovery_needs_only_inventory_and_writes_no_target_state() -> None:
    defaults = read("roles/platform_orchestration/defaults/main.yml")
    discovery = read("roles/platform_discovery/tasks/main.yml")
    assert "platform_orchestration_requested_roles: []" in defaults
    assert "platform_orchestration_state_directory" in defaults
    assert "check_mode: false" in discovery
    assert "argv: [pveversion]" in discovery
    assert "argv: [lspci, -nn]" in discovery
    assert "ansible.builtin.set_fact" in discovery
    assert "Require selected roles to be supported by their target" in discovery


def test_handoff_persists_discovery_and_prints_next_owner_commands() -> None:
    tasks = read("roles/platform_handoff/tasks/main.yml")
    assert "ansible.builtin.copy" in tasks
    assert "to_nice_json" in tasks
    assert "tofu -chdir=" in tasks
    assert "flux reconcile kustomization" in tasks
    assert "platform_orchestration_checkpoint_path" in tasks


def test_orchestrator_discovers_before_selected_role_apply() -> None:
    playbook = read("playbooks/platform-orchestration.yml")
    assert "Discover platform role eligibility" in playbook
    assert "platform_discovery" in playbook
    assert "'proxmox_pi' in platform_orchestration_requested_roles" in playbook
    assert "'proxmox_vgpu_host' in platform_orchestration_requested_roles" in playbook
    assert "'talos_handoff' in platform_orchestration_requested_roles" in playbook


if __name__ == "__main__":
    test_discovery_needs_only_inventory_and_writes_no_target_state()
    test_handoff_persists_discovery_and_prints_next_owner_commands()
    test_orchestrator_discovers_before_selected_role_apply()
    print("Platform discovery and resume contract checks passed")
