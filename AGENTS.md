# Repository instructions for coding agents

## Scope and ownership

- Treat [`README.md`](README.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), and
  [`docs/README.md`](docs/README.md) as the repository entrypoints.
- Local source is rooted in `roles/`, top-level `playbooks/`, `nvidia/`,
  `proxmox-util/`, and the root `playbook.yml`. `playbooks/k3s-ansible/` and
  `playbooks/netbox-proxmox/` are upstream submodules: read and follow their
  own instructions before editing them.
- Do not inspect, edit, or document `.ansible/`, `.venv/`, `.nb-pm/`,
  `node_modules/`, `__pycache__/`, or `.DS_Store` as source. They are local or
  generated artifacts.

## Security and operational invariants

- Never add inventories, endpoint addresses, credentials, Vault passwords,
  API tokens, private keys, certificate keys, or controller state to the
  checkout. Use a caller-supplied protected file outside the repository.
- Preserve default-disabled behavior, explicit apply variables, typed
  confirmations, private prompts, `no_log` handling, input validation, and
  fail-closed rollback checks in guarded workflows.
- Do not turn a read-only/bootstrap/check workflow into a mutation workflow,
  infer missing operator inputs, or claim a rollback exists when state is not
  recorded.
- Keep generic roles free of service-specific topology and identities. Put
  reusable constraints in role defaults; pass environment data from a caller.

## Implementation conventions

- For behavior changes, use the red-green-refactor loop: add the smallest
  failing offline test, make it pass, then run the focused and relevant broader
  checks. Documentation-only changes are exempt; validate links instead.
- Prefer `ansible.builtin.*` FQCNs, idempotent modules, and `command: argv:`.
  Avoid shell interpolation; if a shell task is necessary, validate all input
  at the trust boundary and keep it bounded.
- Keep edits narrow. Do not reformat unrelated YAML or modify ignored/generated
  artifacts.
- Update the nearest role documentation and the relevant `docs/` contract when
  changing inputs, mutations, checkpoints, rollback behavior, or validation.

## Validation

Use the commands in [`CONTRIBUTING.md`](CONTRIBUTING.md). Start with
`tests/extraction.yml` or `tests/service_security_manifest.yml` for local
service roles. Use `--check` or the documented discovery mode before any
workflow that could contact a target; never invoke live apply/rollback merely
to test a code change.

## Tech Stack

- **Automation:** Ansible roles and playbooks in YAML.
- **Managed platforms:** MicroK8s, Podman/Compose, Proxmox, NVIDIA/vGPU, and guarded NetBox/service-security workflows.
- **Repository:** GitHub target; `main` default branch; conventional commits.
See [HERO.md](./HERO.md) for the full configuration managed by `hero-skills:init-hero`.

## Best Practices

- **Safety:** Use risk-appropriate guards; never commit credentials, topology, private keys, or controller state.
- **Quality:** Root pre-commit, lint, and CI configuration are planned but not yet present; use the documented offline checks.
- **Tests:** Prefer focused offline role/workflow tests, then relevant broader checks; never live-apply to validate a change.
See [HERO.md](./HERO.md) for details managed by `hero-skills:init-hero`.

## Coding Conventions

- **Modules:** Prefer `ansible.builtin.*` and idempotent modules.
- **Commands:** Prefer bounded `command: argv:`; validate any necessary shell input at the trust boundary.
- **Roles:** Keep defaults generic; callers supply topology, identities, and protected artifact paths.
- **Documentation:** Update the nearest role README and contract documentation when behavior changes.
See [HERO.md](./HERO.md) for full coding conventions.
