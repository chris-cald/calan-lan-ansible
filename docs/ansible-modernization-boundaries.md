# Ansible modernization boundaries

This document refines plan items 004 and 005 against the reconciled source
tree and the validation matrix. It is a change-control boundary, not approval
to alter automation behavior.

## Audit baseline

`ansible-lint --offline -p` currently exits non-zero with 139 findings:

| Boundary | Findings | Status |
| --- | ---: | --- |
| Root `playbook.yml` | 1 | Blocked by the absent `roles/microk8s` role. |
| `roles/sudo/**` | 53 | Privilege-boundary remediation requires a reviewed behavioral baseline. |
| Legacy `playbooks/**` | 81 | Split into controller and virtualization slices below. |
| `nvidia/**` | 4 | Driver and bootloader changes require dedicated review. |

The count is an audit baseline, not an allowed lint baseline. Item 006 may
only enforce lint after the approved slices reach a clean result.

## Item 004 — root entrypoint and sudo role

### 004-A: root MicroK8s entrypoint

`playbook.yml` names a missing local `microk8s` role. Do not restore, replace,
or remove that reference as lint remediation. The choice changes cluster
lifecycle and needs a dedicated migration decision covering the intended
replacement, operator inputs, rollback limit, and validation evidence.

**Boundary:** syntax or documentation work that does not change the entrypoint
is allowed. Any role restoration, Talos replacement, or retirement is blocked
pending approval.

### 004-B: sudo privilege role

`roles/sudo/**` is the only current local role. Its tasks manage users, groups,
and sudo access.

**Boundary:** documentation, test harnesses, and task-local changes proven not
to change privilege behavior may proceed. Changes to defaults, task order,
users, groups, sudoers content, handlers, or idempotence semantics require
approval with an offline before/after contract test.

## Item 005 — standalone playbooks

### 005-A: controller services

`playbooks/awx/**`, `playbooks/podman/**`, and
`playbooks/podman-semaphore/**` change controller or service state.

**Boundary:** preserve protected inputs and do not convert shell/API behavior
without a proposed payload, changed-state, and rollback analysis. Discovery
and static analysis are safe; live convergence is not CI evidence.

### 005-B: Proxmox and cloud-init

`playbooks/proxmox-cloudinit/**`, `playbooks/proxmox-maint/**`, and
`proxmox-util/**` affect VMs, cloud-init, packages, and caller-owned
inventories.

**Boundary:** do not alter VM, host, package, inventory, or teardown behavior
without an explicit approval and a caller-protected check/discovery plan.

### 005-C: NVIDIA host and guest automation

`nvidia/**` changes drivers, vGPU state, bootloader configuration, and host or
guest state.

**Boundary:** only static/read-only analysis may proceed. Every command/module
replacement, task reordering, or changed-state adjustment requires explicit
approval and hardware-safe validation.

## Approval record required for a behavior change

Before implementing a blocked change, record:

1. exact files/tasks and the intended before/after behavior;
2. safety tier, blast radius, and rollback limit;
3. caller-owned inputs or protected artifacts required for validation; and
4. focused offline plus check/discovery evidence.

No inventory, topology, credential, private key, or controller state belongs
in this document or the checkout.
