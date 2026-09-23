# Talos vGPU extension build contract

The extension build runs on a protected builder, never on a Talos node. Start
with the protected manifest and validate it before collecting artifacts:

```sh
python3 tests/validate_vgpu_compatibility_manifest.py \
  /absolute/path/vgpu-compatibility.yml
```

The builder must verify `guest_driver_artifact_sha256` before constructing the
image. When `nvenc_patch_enabled` is true, it must also fetch the reviewed
`nvenc_patch_revision`, verify `nvenc_patch_sha256`, apply it during the build,
and record the final extension image digest outside Git.

The resulting extension must use the exact `guest_driver_branch` in the
manifest. Attach it only to the disposable VM created by `tofu/vgpu-test`.
Collect the extension digest, guest driver version, and `nvidia-smi` result as
protected evidence before allowing the Flux smoke workload.
