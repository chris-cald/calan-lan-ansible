---
id: wi-vgpu-talos-compatibility-spike
title: Prove Talos vGPU compatibility before platform rollout
status: planned
subtype: spike
priority: high
---

# Talos vGPU compatibility spike

## Goal

Prove or reject the exact Proxmox NVIDIA vGPU Manager, Talos kernel, and
NVIDIA guest-driver combination required to share the two physical GPUs among
AI and video workloads.

## Constraints

- Proxmox host changes remain guarded, operator-run Ansible work.
- Talos nodes stay immutable: no SSH or package installation inside guests.
- Do not place inventory, topology, credentials, license material, private
  keys, or controller state in Git.
- Do not test against production workloads or the only shared GPU capacity
  without an approved maintenance window and rollback plan.

## Acceptance criteria

- [ ] Record the exact GPU model, supported vGPU profile, Proxmox release,
  NVIDIA vGPU Manager branch, Talos release/kernel, and guest-driver branch.
- [ ] Confirm NVIDIA licensing and distribution terms permit the required
  custom Talos system-extension build.
- [ ] Build a reproducible, version-pinned guest-driver extension compatible
  with the selected Talos kernel and host vGPU Manager.
- [ ] In a disposable VM, prove the mediated device is visible after Talos
  boot and the extension loads without SSH or package installation.
- [ ] Through Flux, deploy the NVIDIA runtime/device plugin and verify a
  constrained test workload receives the expected GPU resource.
- [ ] Document upgrade order, rollback limit, and compatibility checks for
  host manager, Talos, guest extension, and Flux workload changes.

## Non-goals

- Changing a production Proxmox host, Talos node, or workload.
- Selecting GPU profile sizes or service scheduling policy.
- Replacing guarded host Ansible with image builds.

## Dependencies

- Talos foundation branch and the approved Proxmox/OpenTofu lifecycle model.
- A separately approved protected test environment and NVIDIA licensing.
