# safe_sudo role

Installs a root-owned `/usr/local/sbin/safe-sudo` dispatcher and a sudoers rule
that allows a dedicated operator group to run only that dispatcher without a
password. It does not grant `NOPASSWD:ALL`.

The role is disabled by default. Use the guarded playbook with protected
inventory data:

```bash
ansible-playbook -i /protected/inventory.yml playbooks/safe-sudo.yml \
  -e safe_sudo_targets=proxmox \
  -e safe_sudo_users='["operator"]' \
  -e safe_sudo_apply=true \
  -e safe_sudo_confirmation=apply-safe-sudo \
  --check --diff
```

Apply only after reviewing the check output. The imported dispatcher retains
its explicit operational subcommands. Its Proxmox capability is deliberately
narrow: `safe-sudo pvesh-get` accepts exactly one of `/version`, `/nodes`,
`/storage`, `/cluster/status`, `/cluster/resources`, or
`/nodes/<name>/status` and executes `pvesh get` only.

The generic `sudo` role remains unchanged; use it for its existing behavior,
not as a substitute for this dispatcher.
