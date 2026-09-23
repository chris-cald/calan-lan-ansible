# Talos vGPU custom-kernel builder

A GRID/vGPU driver is an out-of-tree Talos kernel module. Talos accepts it only
when it is signed by the same custom kernel build. This protected builder
therefore consumes pinned Talos and Sidero extensions **protected forks** that
implement these make targets:

- `vgpu-kernel` — build and push the custom signed kernel;
- `vgpu-extension` — build and push the signed GRID/vGPU system extension; and
- `vgpu-imager` — build and push the installer/image using that kernel and
  extension.

Each target receives `REGISTRY`, `PUSH=true`, `PLATFORM=linux/amd64`,
`VGPU_DRIVER_PATH`, `VGPU_DRIVER_SHA256`, and `BUILD_RESULT_PATH`. The final
target must write JSON at `BUILD_RESULT_PATH` containing immutable
`kernel_image`, `extension_image`, and `installer_image` OCI references using
`@sha256:` digests.

The flat protected manifest retains `guest_driver_artifact_sha256` and
`nvenc_patch_enabled`, validated by
`tests/validate_vgpu_compatibility_manifest.py`, and adds:

```yaml
talos_source_url: https://git.example.invalid/platform/talos.git
talos_source_revision: 40_HEX_GIT_COMMIT
extensions_source_url: https://git.example.invalid/platform/extensions.git
extensions_source_revision: 40_HEX_GIT_COMMIT
builder_workspace: /protected/talos-vgpu-builder
builder_registry: registry.example.invalid/calan
build_result_path: /protected/talos-vgpu-builder/result.json
extension_output_path: /protected/talos-vgpu-extension.json
```

Build only on the protected builder:

```sh
python3 talos/vgpu-extension/build.py /absolute/path/vgpu-compatibility.yml
```

Use `--dry-run` to print the bounded Git and make commands. The builder checks
the guest-driver SHA-256, checks out both exact commits, requires immutable
output references, verifies them through the builder's Podman registry auth,
and records the result outside Git. When NVENC is enabled, it downloads the
HTTPS patch, verifies its declared SHA-256, and passes its path, digest, and
revision to the protected fork. It never builds on a Talos node.
