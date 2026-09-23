#!/usr/bin/env python3
"""Offline contract for the opt-in vGPU end-to-end test stack."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text()


def test_opentofu_vm_is_explicitly_gated_and_uses_an_mdev() -> None:
    vm = read("tofu/vgpu-test/main.tf")
    checks = read("tofu/vgpu-test/checks.tf")
    assert 'resource "proxmox_virtual_environment_vm" "vgpu_test"' in vm
    assert "hostpci" in vm
    assert "mdev" in vm and "var.vgpu_mdev_uuid" in vm
    assert "var.vgpu_test_apply" in vm
    assert "vgpu_test_confirmation" in checks


def test_flux_gpu_smoke_stack_is_isolated_from_default_infrastructure() -> None:
    infra = read("kubernetes/clusters/talos/infrastructure.yaml")
    test_kustomization = read("kubernetes/clusters/talos/tests/vgpu/kustomization.yaml")
    smoke = read("kubernetes/clusters/talos/tests/vgpu/gpu-smoke.yaml")
    assert "tests/vgpu" not in infra
    assert "nvidia-device-plugin.yaml" in test_kustomization
    assert "nvidia.com/gpu" in smoke
    assert "vgpu.calan.lan/test" in smoke


def test_talos_extension_recipe_is_manifest_driven() -> None:
    recipe = read("talos/vgpu-extension/README.md")
    assert "validate_vgpu_compatibility_manifest.py" in recipe
    assert "guest_driver_artifact_sha256" in recipe
    assert "nvenc_patch_enabled" in recipe
    assert "SSH" not in recipe


if __name__ == "__main__":
    test_opentofu_vm_is_explicitly_gated_and_uses_an_mdev()
    test_flux_gpu_smoke_stack_is_isolated_from_default_infrastructure()
    test_talos_extension_recipe_is_manifest_driven()
    print("vGPU end-to-end stack contract checks passed")
