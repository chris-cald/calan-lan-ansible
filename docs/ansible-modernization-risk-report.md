# Ansible modernization risk report

**Audit date:** 2026-09-19
**Scope:** repository-owned Ansible only; static inspection, no target contact or mutation.

## Decision gate

This report is the approval gate for modernization. Mechanical documentation,
formatting, lint configuration, and test-harness changes may proceed when they
do not change behavior. Any row marked **approval required** needs explicit
operator approval before its operational behavior, inputs, topology,
credentials, rollback contract, or external API effects change.

The classification describes execution risk, not permission to run a workflow.
All existing apply gates, confirmations, protected inputs, and discovery/check
requirements remain in force.

## Scope and coverage

The audit accounts for 72 first-party operational units:

| Area | Units | Coverage |
| --- | ---: | --- |
| `roles/` | 20 | A role and all of its `defaults/`, `tasks/`, `handlers/`, `vars/`, and templates are one unit. |
| Top-level `playbooks/` | 20 | Every top-level YAML entrypoint; upstream submodules are excluded. |
| Legacy nested `playbooks/` | 12 | First-party AWX, Podman, Proxmox cloud-init, and Proxmox maintenance YAML listed below. |
| Root | 1 | `playbook.yml`. |
| `nvidia/` | 17 | All Ansible YAML except `requirements.yml`; task, handler, and test YAML are included. |
| `proxmox-util/` | 2 | `main.yaml` and `qemu.yaml`. |

Excluded: `playbooks/k3s-ansible/` and `playbooks/netbox-proxmox/` (upstream
submodules), plus `.ansible/`, `.venv/`, `.nb-pm/`, `node_modules/`, caches,
and other generated or controller-local artifacts.

## Safety tiers

| Tier | Definition | Modernization rule |
| --- | --- | --- |
| Read-only | Validates, discovers, collects, or verifies without intended target mutation. | Preserve read-only behavior; any new mutation requires approval. |
| Routine idempotent | Normal convergence with no credentials, destructive lifecycle, or external service API contract. | Preserve idempotency and document any changed default, handler order, or target set. |
| Guarded mutation | Changes service, security, certificate, network, host, VM, driver, or external API state. | Preserve explicit gates and rollback limits. Approval is required for behavior changes. |

### Role inventory

| Tier | Roles | Test evidence | Approval |
| --- | --- | --- | --- |
| Read-only | `certificate_expiry_check`, `npm_proxy_location_baseline`, `service_security_manifest` | Existing extraction and service-manifest checks where applicable; add focused offline contract checks for uncovered roles. | Only if mutation is introduced. |
| Routine idempotent | `microk8s`, `sudo` | Root syntax check plus focused role tests; add Molecule only when containerization is safe. | Required for changed defaults, plugin selection, privilege, or handler behavior. |
| Guarded mutation | `authentik_npm_forward_auth_config`, `authentik_oauth_resource_server`, `authentik_proxy_forward_auth`, `certificate_expiry_schedule`, `healthchecks_check`, `mtls_caddy_sidecar`, `netbox_mcp_gateway`, `netbox_podman_compose`, `npm_mtls_mount_verify`, `npm_proxy_host`, `npm_proxy_location`, `podman_compose_runtime`, `restricted_ssh_deployer`, `service_security_rotation`, `user_present_receiver_bootstrap` | Existing offline contracts, then focused offline checks or documented discovery/check-only validation. | Required for every operational behavior change. |

### Playbook inventory

| Tier | Entrypoints | Test evidence | Approval |
| --- | --- | --- | --- |
| Read-only | `bootstrap-netbox-mcp.yml`, `collect-npm-proxy-location-baseline.yml`, `service-security-validate.yml` | Offline validation or documented read-only discovery. | Only if mutation is introduced. |
| Guarded mutation | `deploy-netbox-mcp-oidc-mtls.yml`, `deploy-netbox-mcp-target-mtls.yml`, `install-netbox-mcp.yml`, `install-netbox.yml`, `provision-authentik-oauth-resource-server.yml`, `provision-npm-proxy-location.yml`, `provision-service-authentik.yml`, `provision-service-healthchecks.yml`, `provision-service-mtls.yml`, `provision-service-npm.yml`, `rollback-authentik-oauth-resource-server.yml`, `rollback-netbox-mcp-caddy.yml`, `rollback-netbox-mcp-gateway.yml`, `rollback-npm-proxy-location.yml`, `rotate-service-mtls-client.yml`, `service-security-orchestration.yml`, `verify-npm-mtls-mounts.yml` | Existing offline role/manifest checks; preserve documented discovery or `--check` flows. | Required for every operational behavior change. |
| Guarded mutation | `playbooks/awx/main.yml`, `playbooks/awx/fixed_projects.yml`, `playbooks/awx/remove.yml`, `playbooks/podman/main.yml`, `playbooks/podman-semaphore/main.yml`, `playbooks/proxmox-cloudinit/main.yml`, `playbooks/proxmox-cloudinit/teardown.yml`, `playbooks/proxmox-cloudinit/test.yml`, `playbooks/proxmox-cloudinit/test2.yml`, `playbooks/proxmox-maint/playbook.yml`, `playbooks/proxmox-maint/apt.yml`, `playbooks/proxmox-maint/apt_handlers.yml` | Syntax/offline checks only when caller-protected inputs are available; preserve documented discovery or `--check` flows. Never use a homelab target as CI evidence. | Required for every operational behavior change. |

### Root and standalone inventory

| Tier | Units | Test evidence | Approval |
| --- | --- | --- | --- |
| Routine idempotent | Root `playbook.yml` | `ansible-playbook --syntax-check playbook.yml`; add focused evidence for changed MicroK8s behavior. | Required for changed hosts, plugins, users, or task order. |
| Guarded mutation | `nvidia/guest-playbook.yml`, `host-playbook.yml`, `hosts-test.yml`, `playbook.yml`, `test-playbook.yml`, task and handler YAML under `nvidia/`; `proxmox-util/main.yaml`, `proxmox-util/qemu.yaml` | Syntax/offline checks only unless a safe disposable target is established; never use a homelab target as CI evidence. | Required for every driver, vGPU, bootloader, VM, cloud-init, or host-state change. |

`nvidia/requirements.yml` is dependency metadata, not an operational Ansible
unit; it still requires dependency-review evidence when changed.

### Standalone source manifest

The role and playbook tables name every role and entrypoint. The legacy
nested playbooks are explicitly covered here; the remaining standalone YAML is
covered by this manifest:

- Legacy nested playbooks: `playbooks/awx/main.yml`,
  `playbooks/awx/fixed_projects.yml`, `playbooks/awx/remove.yml`,
  `playbooks/podman/main.yml`, `playbooks/podman-semaphore/main.yml`,
  `playbooks/proxmox-cloudinit/main.yml`,
  `playbooks/proxmox-cloudinit/teardown.yml`, `playbooks/proxmox-cloudinit/test.yml`,
  `playbooks/proxmox-cloudinit/test2.yml`, `playbooks/proxmox-maint/playbook.yml`,
  `playbooks/proxmox-maint/apt.yml`, and `playbooks/proxmox-maint/apt_handlers.yml`.
- Root: `playbook.yml`.
- NVIDIA: `guest-playbook.yml`, `host-playbook.yml`, `hosts-test.yml`,
  `playbook.yml`, `test-playbook.yml`, `handlers/nvidia_driver_handlers.yml`,
  `handlers/nvidia_vgpu_patch_handlers.yml`, `handlers/test.yml`,
  `tasks/ensure_build_prereqs.yml`, `tasks/gather_bootloader_facts.yml`,
  `tasks/gather_nvidia_facts.yml`, `tasks/iommu.yml`,
  `tasks/nvidia_apply_vgpu_patch.yml`, `tasks/nvidia_driver.yml`,
  `tasks/nvidia_enable_vgpu.yml`, `tasks/nvidia_enc_unlock_patch.yml`, and
  `tasks/test.yml` (all relative to `nvidia/`).
- Proxmox utilities: `proxmox-util/main.yaml` and `proxmox-util/qemu.yaml`.

## Existing evidence and gaps

| Evidence | Current status | Gap to close |
| --- | --- | --- |
| Topology scrub | `tests/topology_scrub.sh` rejects committed topology and host-derived inventory. | Run in the future shared matrix. |
| Root syntax | `ansible-playbook --syntax-check playbook.yml`. | Extend syntax coverage to every safe standalone entrypoint, including legacy nested playbooks that do not require caller-protected inputs. |
| Local role contracts | `tests/extraction.yml` and `tests/service_security_manifest.yml`. | Map each role to an explicit offline, Molecule, or discovery/check-only evidence class. |
| Guarded workflow documentation | `docs/` documents NetBox and service-security contracts. | Add equivalent contract coverage for NVIDIA, Proxmox utilities, MicroK8s, and legacy playbooks. |
| Root lint, hooks, CI, pinned test dependencies | Not configured. | Items 002, 003, and 006 establish them after the clean baseline is proven. |

## Known behavior risks and approval status

| Source boundary | Behavior at risk | Blast radius | Status |
| --- | --- | --- | --- |
| All roles | Moving values between defaults, vars, playbooks, or caller inputs changes Ansible precedence and the public role contract. | Every caller of the role. | Approval required when values, names, or precedence change. |
| All roles and playbooks | Replacing commands with modules, changing `changed_when`, or reordering handlers changes convergence and restart behavior. | Managed host or service. | Approval required when behavior can differ. |
| Read-only units | Adding a state-changing task converts a validation/discovery contract into a mutation workflow. | Target host, controller, or external service. | Approval required. |
| Guarded service-security and NetBox units | Altering apply gates, confirmations, prompts, `no_log`, certificate material, API payloads, snapshots, or rollback checks affects credentials, traffic, and recoverability. | Authentication, mTLS, proxy routing, NetBox, and all selected services. | Approval required. |
| `restricted_ssh_deployer`, `sudo`, and receiver bootstrap | Changes can expand remote privilege, SSH access, forced-command behavior, or allowed deployment actions. | Target security boundary. | Approval required. |
| `npm_proxy_*`, `mtls_caddy_sidecar`, and gateway units | Changes can alter public routing, mTLS enforcement, headers, and streamed traffic. | Public service availability and client authentication. | Approval required. |
| `netbox_podman_compose` and `podman_compose_runtime` | Image, revision, lifecycle, volume, or Compose changes can replace service state or affect rollback. | NetBox or Podman-managed services. | Approval required. |
| `certificate_expiry_schedule` | Wrapper, command, cron, inventory, extra-vars, or callback changes alter scheduled caller-defined execution or external notification. | Scheduled certificate checks and notification endpoint. | Approval required. |
| `healthchecks_check` and `npm_mtls_mount_verify` | API writes or local private runtime/attestation writes alter external monitoring state or controller evidence. | Healthchecks project, NPM verification evidence, and private controller state. | Approval required. |
| `microk8s` and root playbook | Plugin, user membership, host group, or task-order changes affect cluster availability and authorization. | MicroK8s nodes and workloads. | Approval required. |
| `nvidia/` | Driver, vGPU, IOMMU, bootloader, or patch changes can prevent host boot or change GPU allocation. | NVIDIA hosts, guests, and workloads. | Approval required. |
| `proxmox-util/` and legacy AWX, Podman, and Proxmox playbooks | Package, Kubernetes/AWX, container, VM, cloud-init, guest-agent, or host changes can alter workload or guest lifecycle and access. | MicroK8s nodes, Podman hosts, Proxmox guests, and Proxmox hosts. | Approval required. |
| Test modernization | Molecule or discovery scenarios can contact or mutate a real target if inventory, credentials, or apply paths leak into CI. | CI runner and connected infrastructure. | Approval required before introducing any live target. |

No operational behavior change is approved by this report. The approved next
step is to establish the policy and tier definitions in item 002, then build
the reproducible test matrix in item 003. Items 004 and 005 must cite this
report and obtain explicit approval for each high-risk change before applying
it.

## Audit method and limitations

The audit statically enumerated first-party YAML and inspected repository
contracts and safety signals (`assert`, `no_log`, prompts, apply variables, and
bounded command use). Static inspection cannot prove runtime idempotency,
external API schemas, rollback effectiveness, or target state. Those claims
require the tiered evidence specified above; no live apply or rollback was run.
