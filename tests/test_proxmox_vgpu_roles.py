#!/usr/bin/env python3
"""Offline contract for guarded vanilla-Proxmox vGPU roles."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text()


def test_host_role_is_default_disabled_and_requires_verified_artifacts() -> None:
    defaults = read("roles/proxmox_vgpu_host/defaults/main.yml")
    guard = read("roles/proxmox_vgpu_host/tasks/guard.yml")
    tasks = read("roles/proxmox_vgpu_host/tasks/main.yml")
    assert "proxmox_vgpu_host_apply: false" in defaults
    assert "proxmox_vgpu_host_confirmation" in guard
    assert "proxmox_vgpu_host_manager_sha256" in guard
    assert "proxmox_vgpu_host_unlock_sha256" in guard
    assert "ansible.builtin.apt" in tasks
    assert "ansible.builtin.stat" in tasks
    assert "ansible.builtin.git" not in tasks
    assert "cargo build" not in tasks


def test_mdev_role_is_separate_and_idempotent() -> None:
    defaults = read("roles/proxmox_vgpu_mdev/defaults/main.yml")
    guard = read("roles/proxmox_vgpu_mdev/tasks/guard.yml")
    tasks = read("roles/proxmox_vgpu_mdev/tasks/main.yml")
    assert "proxmox_vgpu_mdev_apply: false" in defaults
    assert "proxmox_vgpu_mdev_parent" in guard
    assert "proxmox_vgpu_mdev_type" in guard
    assert "proxmox_vgpu_mdev_uuid" in guard
    assert "- define" in tasks
    assert "start, --uuid" in tasks


def test_playbook_requires_a_protected_inventory_and_typed_confirmation() -> None:
    playbook = read("playbooks/proxmox-vgpu.yml")
    assert "proxmox_vgpu_inventory" in playbook
    assert "ansible_inventory_sources" in playbook
    assert "proxmox_vgpu_host" in playbook
    assert "proxmox_vgpu_mdev" in playbook


if __name__ == "__main__":
    test_host_role_is_default_disabled_and_requires_verified_artifacts()
    test_mdev_role_is_separate_and_idempotent()
    test_playbook_requires_a_protected_inventory_and_typed_confirmation()
    print("Proxmox vGPU role contract checks passed")
