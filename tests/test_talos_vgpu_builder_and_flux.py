#!/usr/bin/env python3
"""Offline contract for the protected Talos vGPU builder and Flux fixture gate."""

from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text()


def test_builder_requires_pinned_forks_and_records_immutable_outputs() -> None:
    builder = read("talos/vgpu-extension/build.py")
    guide = read("talos/vgpu-extension/README.md")
    for field in (
        "talos_source_url",
        "talos_source_revision",
        "extensions_source_url",
        "extensions_source_revision",
        "builder_workspace",
        "build_result_path",
        "extension_output_path",
    ):
        assert field in builder
    assert "vgpu-kernel" in builder
    assert "vgpu-extension" in builder
    assert "vgpu-imager" in builder
    assert "NVENC_PATCH_SHA256" in builder
    assert "@sha256:" in builder
    assert "protected forks" in guide


def test_builder_dry_run_validates_the_protected_build_contract() -> None:
    manifest = """gpu_model: test-gpu
vgpu_profile: test-profile
proxmox_version: test
host_vgpu_manager_branch: 550
talos_version: test
talos_kernel: test
guest_driver_branch: 550
license_reviewed: true
compatibility_reference: https://example.invalid/matrix
extension_source: protected fork
guest_driver_artifact_path: /protected/NVIDIA-Linux-grid.run
guest_driver_artifact_sha256: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
nvenc_patch_enabled: false
talos_source_url: https://example.invalid/talos.git
talos_source_revision: 0123456789abcdef0123456789abcdef01234567
extensions_source_url: https://example.invalid/extensions.git
extensions_source_revision: 89abcdef0123456789abcdef0123456789abcdef
builder_workspace: /protected/workspace
builder_registry: registry.example.invalid/calan
build_result_path: /protected/result.json
extension_output_path: /protected/output.json
"""
    with tempfile.NamedTemporaryFile("w", suffix=".yml") as file:
        file.write(manifest)
        file.flush()
        result = subprocess.run(
            ["python3", ROOT / "talos/vgpu-extension/build.py", "--dry-run", file.name],
            capture_output=True,
            text=True,
        )
    assert result.returncode == 0, result.stderr
    assert "vgpu-kernel" in result.stdout
    assert "vgpu-extension" in result.stdout
    assert "vgpu-imager" in result.stdout


def test_flux_gpu_fixture_has_a_suspended_opt_in_kustomization() -> None:
    fixture = read("kubernetes/clusters/talos/tests/vgpu-flux.yaml")
    infra = read("kubernetes/clusters/talos/infrastructure.yaml")
    assert "kind: Kustomization" in fixture
    assert "name: vgpu-test" in fixture
    assert "path: ./kubernetes/clusters/talos/tests/vgpu" in fixture
    assert "suspend: true" in fixture
    assert "vgpu-test" not in infra


if __name__ == "__main__":
    test_builder_requires_pinned_forks_and_records_immutable_outputs()
    test_builder_dry_run_validates_the_protected_build_contract()
    test_flux_gpu_fixture_has_a_suspended_opt_in_kustomization()
    print("Talos vGPU builder and Flux gate contract checks passed")
