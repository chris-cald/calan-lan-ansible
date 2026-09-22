# Ansible modernization risk report

## Decision gate

This report was re-baselined against the reconciled `main` source tree on
2026-09-22. It classifies current repository-owned YAML only; upstream
submodules and local/generated directories are excluded.

The classification describes execution risk, not permission to run a workflow.
No operational behavior change is approved by this report. A change to a
protected input, topology, privilege boundary, apply gate, external API,
driver, VM, or rollback contract requires explicit approval before it is made.

## Scope and coverage

The source manifest is enforced by
[`tests/test_validation_matrix.py`](../tests/test_validation_matrix.py) using
[`tests/validation-matrix.json`](../tests/validation-matrix.json). Every
repository-owned YAML source has exactly one evidence class:

| Boundary | Tier | Evidence |
| --- | --- | --- |
| Root `playbook.yml` | Routine idempotent | Blocked: its `microk8s` role is absent after reconciliation. |
| `roles/sudo/**` | Routine idempotent | Offline syntax check of `roles/sudo/tests/test.yml`. |
| `playbooks/awx/**`, `playbooks/podman/**`, `playbooks/podman-semaphore/**`, `playbooks/proxmox-cloudinit/**`, and `playbooks/proxmox-maint/*.yml` | Guarded mutation | Discovery/check-only evidence; no target is used in CI. |
| `playbooks/proxmox-maint/requirements.yaml` | Metadata | Dependency review. |
| `nvidia/tasks/**`, `nvidia/handlers/**`, and NVIDIA entrypoint playbooks | Guarded mutation | Discovery/check-only evidence; no target is used in CI. |
| `nvidia/requirements.yml` | Metadata | Dependency review. |
| `proxmox-util/*.yaml` and `proxmox-util/playbook.yml` | Guarded mutation | Discovery/check-only evidence; caller-owned inventory only. |

## Matrix execution

Install the pinned developer tools:

```sh
python3 -m pip install -r requirements-dev.txt
```

Run the safe default matrix:

```sh
sh tests/run_validation_matrix.sh
```

It runs static matrix coverage, public-exposure scrub, caller-inventory gating,
and the `sudo` role syntax check. It intentionally reports—not hides—the
blocked root playbook until the missing role is restored or replaced.

Molecule and live/target checks are excluded from the default matrix. Run
Molecule only after a pinned disposable Docker scenario exists, and run guarded
workflows only through their documented discovery or `--check` paths with
caller-supplied protected inputs.

## Known behavior risks and approval status

| Source boundary | Behavior at risk | Approval |
| --- | --- | --- |
| Root `playbook.yml` | Restoring or replacing `microk8s` changes cluster lifecycle and plugin behavior. | Required. |
| `roles/sudo/**` | Changes can expand remote privilege or alter user/group and sudo policy. | Required. |
| Legacy AWX, Podman, Proxmox, and cloud-init playbooks | Changes can affect host, VM, service, or credential lifecycle. | Required. |
| NVIDIA sources | Changes can affect driver, vGPU, bootloader, or host state. | Required. |
| `proxmox-util/**` | Changes can affect VM lifecycle or caller inventory selection. | Required. |

## Audit limitations

This is static evidence only. It does not assert runtime idempotence or
connectivity, and it does not use a homelab target, inventory, credential,
private key, or controller state.
