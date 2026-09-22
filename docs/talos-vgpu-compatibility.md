# Talos vGPU compatibility spike

The vGPU spike is a production gate: Proxmox host Ansible and Flux GPU
workloads must not change until a caller-owned compatibility manifest passes.

## Protected input

Create a flat YAML manifest outside the checkout with these fields:

```yaml
# Store this file outside Git. Values below are placeholders only.
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
```

Validate it without contacting a host:

```sh
python3 tests/validate_vgpu_compatibility_manifest.py \
  /absolute/path/vgpu-compatibility.yml
```

The validator requires an explicit license review, an HTTPS compatibility
reference, and matching host/guest vGPU driver branches. Passing it is only the
input gate. The work item still requires a disposable VM proof, a pinned Talos
extension build, Flux device-plugin verification, and a documented rollback
limit before production rollout.
