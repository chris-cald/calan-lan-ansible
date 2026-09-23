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
extension_source: protected local build recipe
guest_driver_artifact_path: /protected/NVIDIA-Linux-grid.run
guest_driver_artifact_sha256: SHA256_OF_GUEST_DRIVER
nvenc_patch_enabled: false
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

A passing manifest is an input gate, not a deployment. It still requires a
reproducible Talos extension build, a disposable mediated-device VM proof, and
Flux device-plugin/workload validation. See
[Talos vGPU architecture](talos-vgpu-architecture.md) for the ownership and
instrumentation model.
