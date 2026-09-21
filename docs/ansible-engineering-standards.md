# Ansible engineering standards

This is the canonical engineering contract for repository-owned Ansible under
`roles/`, top-level `playbooks/`, `nvidia/`, `proxmox-util/`, and root
entrypoints. Upstream submodules and generated/controller-local directories
retain their own rules.

## Operating stance

Act as a conservative Ansible platform engineer: use the smallest idempotent
change that preserves an operator's control. Prefer explicit inputs, bounded
commands, and offline evidence over clever YAML or inferred topology.

## Safety tiers

Classify a workflow before changing it. The current classification is recorded
in the [modernization risk report](ansible-modernization-risk-report.md).

| Tier | Purpose | Required controls |
| --- | --- | --- |
| Read-only | Validation, discovery, collection, or verification. | Must not introduce target mutation without explicit approval. |
| Routine idempotent | Normal convergence without credentials, destructive lifecycle, or an external-service API contract. | Idempotent modules, caller-selected targets, validated inputs, and focused offline evidence. |
| Guarded mutation | Service, security, certificate, network, host, VM, driver, or external API changes. | Default-disabled apply path, explicit apply variable, typed confirmation when appropriate, private prompts and `no_log`, input validation, and documented rollback limits. |

Do not reclassify a workflow to a weaker tier merely to remove a guard. A
read-only, bootstrap, check, or discovery workflow remains non-mutating.

## Role and playbook boundaries

- Roles are reusable constraints. Put generic, default-disabled inputs in
  `defaults/`; callers provide topology, identities, and protected artifact
  paths.
- Playbooks compose roles and select the safety boundary. They do not embed
  secrets, fixed inventories, endpoint addresses, or controller state.
- Document each role or guarded workflow's inputs, intended mutations,
  validation, checkpoints, and rollback limit in its nearest README or
  operational contract.
- Do not claim rollback when required state was not recorded.

## Implementation rules

- Use `ansible.builtin.*` FQCNs in new or changed local tasks.
- Prefer idempotent modules. Supply meaningful `changed_when` and
  `failed_when` when a command cannot report them correctly.
- Prefer `ansible.builtin.command` with `argv:`. A shell task is exceptional:
  validate input at the trust boundary, bound the command, and document why a
  module or `command` cannot express it.
- Validate caller-controlled data with `ansible.builtin.assert` before it is
  used in paths, commands, API calls, or topology selection.
- Keep inventories, credentials, Vault passwords, API tokens, private keys,
  certificate keys, and controller state outside the checkout. Protect secret
  handling with `no_log: true`.
- Keep changes narrow. Do not reformat unrelated YAML or edit generated and
  upstream content.

## Evidence and behavior changes

Use red-green-refactor for behavior changes: first add the smallest failing
offline test, then make it pass, then run the focused and relevant broader
checks. Documentation-only changes validate links.

Every first-party unit must have one of these evidence classes:

1. **Offline contract or extraction test** for role inputs, defaults, guards,
   and rendered content.
2. **Molecule converge and idempotence** when a role is safely
   containerizable.
3. **Documented syntax, check, or discovery evidence** when live or hardware
   behavior cannot safely run in CI.

Never use a homelab target, apply path, rollback path, protected inventory, or
credential as CI evidence. A changed default, handler order, target set,
privilege boundary, API interaction, VM lifecycle, driver behavior, or network
behavior is a behavior change. For guarded mutation, obtain explicit approval
before implementation and record the blast radius and validation in the risk
report or nearest workflow contract.

## Exceptions

A deviation is allowed only at the exact task that needs it. Use the narrowest
supported lint waiver (for example, a task-local `# noqa`) and document in the
nearest README or contract:

- the rule and exact task waived;
- why the compliant alternative is unsuitable;
- the residual risk and validation; and
- the condition for removing the waiver.

A waiver does not permit a secret, inferred operator input, unbounded shell
interpolation, or a weaker safety tier.

## Review checklist

- [ ] The safety tier is unchanged or explicitly approved.
- [ ] Inputs are validated; secrets and topology are outside the checkout.
- [ ] The implementation is idempotent and uses FQCN modules and bounded
      commands.
- [ ] The required documentation and evidence class are updated.
- [ ] A behavior-changing guarded workflow has recorded approval, blast radius,
      and validation.
