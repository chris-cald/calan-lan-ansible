#!/usr/bin/env python3
"""Offline contract for the pinned, non-privileged vGPU unlock image flow."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIN = "f432ffc8b7ed245df8858e9b38000d3b8f0352f4"
ARCHIVE_SHA256 = "07f2f6d847867b7994b465d245176aee2bb649dcbb92badf65372be0cc22aaaf"


def read(path: str) -> str:
    return (ROOT / path).read_text()


def test_role_builds_a_pinned_local_image_and_extracts_without_running_it() -> None:
    defaults = read("roles/proxmox_vgpu_unlock/defaults/main.yml")
    guard = read("roles/proxmox_vgpu_unlock/tasks/guard.yml")
    tasks = read("roles/proxmox_vgpu_unlock/tasks/main.yml")
    containerfile = read("roles/proxmox_vgpu_unlock/templates/Containerfile.j2")

    assert "proxmox_vgpu_unlock_apply: false" in defaults
    assert PIN in defaults
    assert ARCHIVE_SHA256 in defaults
    assert "proxmox_vgpu_unlock_platform: linux/amd64" in defaults
    assert "proxmox_vgpu_unlock_confirmation" in guard
    assert "apply-proxmox-vgpu-unlock" in defaults
    assert "delegate_to: localhost" in tasks
    assert "Build pinned local vGPU unlock Podman image" in tasks
    assert "Save local vGPU unlock Podman image archive" in tasks
    assert "Load local vGPU unlock Podman image on Proxmox host" in tasks
    assert "Extract vGPU unlock payload without running a container" in tasks
    assert "--privileged" not in tasks
    assert "podman, run" not in tasks
    assert "FROM scratch" in containerfile
    assert "vgpu_unlock_hooks.c" in containerfile
    assert "kern.ld" in containerfile


def test_role_applies_reviewed_dkms_and_service_changes_then_requires_reboot() -> None:
    tasks = read("roles/proxmox_vgpu_unlock/tasks/main.yml")
    handlers = read("roles/proxmox_vgpu_unlock/handlers/main.yml")

    assert "Create NVIDIA vGPU service override directories" in tasks
    assert "Configure NVIDIA vGPU service wrappers" in tasks
    assert "os-interface.c" in tasks
    assert "nvidia.Kbuild" in tasks
    assert "dkms, remove" in tasks
    assert "dkms, install" in tasks
    assert "Reboot Proxmox vGPU unlock host" in handlers


def test_provisioning_playbook_composes_the_unlock_role() -> None:
    playbook = read("playbooks/proxmox-vgpu.yml")
    assert "proxmox_vgpu_host" in playbook
    assert "proxmox_vgpu_unlock" in playbook
    assert "proxmox_vgpu_mdev" in playbook


if __name__ == "__main__":
    test_role_builds_a_pinned_local_image_and_extracts_without_running_it()
    test_role_applies_reviewed_dkms_and_service_changes_then_requires_reboot()
    test_provisioning_playbook_composes_the_unlock_role()
    print("Proxmox vGPU unlock Podman contract checks passed")
