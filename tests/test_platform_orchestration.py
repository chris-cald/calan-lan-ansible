#!/usr/bin/env python3
"""Offline contract for the staged Proxmox-to-Talos orchestration boundary."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text()


def test_single_playbook_has_separate_entrypoint_and_handoff_plays() -> None:
    playbook = read("playbooks/platform-orchestration.yml")
    for name in (
        "Validate platform orchestration inputs",
        "Bootstrap SSH-ready Raspberry Pi Proxmox nodes",
        "Bootstrap SSH-ready x64 Proxmox nodes",
        "Bootstrap SSH-ready supported ARM Proxmox nodes",
        "Validate or configure existing Proxmox nodes",
        "Declare future BMC or Pixie provisioning handoff",
        "Configure optional NVIDIA vGPU hosts",
        "Configure optional mediated devices after reboot",
        "Record the handoff to OpenTofu Talos provisioning",
    ):
        assert name in playbook
    assert "proxmox_pi" in playbook
    assert "proxmox_x64" in playbook
    assert "proxmox_arm64" in playbook
    assert "proxmox_existing" in playbook
    assert "proxmox_bmc_pixie" in playbook
    assert "talos_handoff" in playbook
    assert "proxmox_vgpu_host" in playbook
    assert "proxmox_vgpu_unlock" in playbook
    assert "proxmox_vgpu_mdev" in playbook
    assert "platform_orchestration_mode == 'apply'" in playbook
    assert "serial: 1" in playbook


def test_orchestration_is_default_discovery_with_fail_closed_rollback() -> None:
    defaults = read("roles/platform_orchestration/defaults/main.yml")
    tasks = read("roles/platform_orchestration/tasks/main.yml")
    assert "platform_orchestration_mode: discover" in defaults
    assert "apply-platform-orchestration" in defaults
    assert "platform_orchestration_checkpoint_path" in tasks
    assert "automatic rollback" in tasks.lower()
    assert "set_stats" in tasks


def test_pi_mixed_architecture_cluster_requires_a_separate_override() -> None:
    defaults = read("roles/proxmox_pi/defaults/main.yml")
    tasks = read("roles/proxmox_pi/tasks/main.yml")
    assert "proxmox_pi_mixed_architecture_cluster_acknowledgement" in defaults
    assert "accept-mixed-architecture-proxmox-cluster" in defaults
    assert "proxmox_pi_mixed_architecture_cluster_acknowledgement" in tasks


def test_talos_is_handed_to_opentofu_without_ansible_vm_lifecycle() -> None:
    tasks = read("roles/talos_handoff/tasks/main.yml")
    assert "ansible.builtin.copy" in tasks
    assert "tofu apply" not in tasks
    assert "talos_handoff_path" in tasks


if __name__ == "__main__":
    test_single_playbook_has_separate_entrypoint_and_handoff_plays()
    test_orchestration_is_default_discovery_with_fail_closed_rollback()
    test_pi_mixed_architecture_cluster_requires_a_separate_override()
    test_talos_is_handed_to_opentofu_without_ansible_vm_lifecycle()
    print("Platform orchestration contract checks passed")
