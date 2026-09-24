# Talos vGPU compatibility spike

The vGPU spike is a production gate. Keep the protected manifest outside Git;
it records the exact host, Talos, guest-driver, and optional NVENC inputs.

## Protected extension-build input

Create a flat YAML manifest outside the checkout:

```yaml
# Placeholders only. Never commit artifact paths, GPU details, or credentials.
gpu_model: PLACEHOLDER
vgpu_profile: PLACEHOLDER
proxmox_version: PLACEHOLDER
host_vgpu_manager_branch: PLACEHOLDER
talos_version: PLACEHOLDER
talos_kernel: PLACEHOLDER
guest_driver_branch: PLACEHOLDER
license_reviewed: true
compatibility_reference: https://vendor.example/compatibility-matrix
extension_source: protected Talos/extensions forks
guest_driver_artifact_path: /protected/NVIDIA-Linux-grid.run
guest_driver_artifact_sha256: SHA256_OF_GUEST_DRIVER
nvenc_patch_enabled: false
talos_source_url: https://git.example.invalid/platform/talos.git
talos_source_revision: 40_HEX_GIT_COMMIT
extensions_source_url: https://git.example.invalid/platform/extensions.git
extensions_source_revision: 40_HEX_GIT_COMMIT
builder_workspace: /protected/talos-vgpu-builder
builder_registry: registry.example.invalid/calan
build_result_path: /protected/talos-vgpu-builder/result.json
extension_output_path: /protected/talos-vgpu-extension.json
# Required only when nvenc_patch_enabled is true:
# nvenc_patch_source: https://example.invalid/source
# nvenc_patch_revision: immutable-reviewed-revision
# nvenc_patch_sha256: SHA256_OF_PATCH_ARTIFACT
```

Validate it without contacting a host:

```sh
python3 tests/validate_vgpu_compatibility_manifest.py \
  /absolute/path/vgpu-compatibility.yml
```

A passing manifest is an input gate, not a deployment. Build the signed kernel,
GRID/vGPU extension, and installer on the protected builder with:

```sh
python3 talos/vgpu-extension/build.py /absolute/path/vgpu-compatibility.yml
```

The protected forks must implement the bounded `vgpu-kernel`, `vgpu-extension`,
and `vgpu-imager` make targets documented in
[`talos/vgpu-extension/README.md`](../talos/vgpu-extension/README.md). It still
requires a disposable mediated-device VM proof and Flux device-plugin/workload
validation. See
[self-supported vGPU architecture](self-supported-vgpu-architecture.md) for the ownership and
instrumentation model.
