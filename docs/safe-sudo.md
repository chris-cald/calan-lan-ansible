# Safe passwordless operations

`roles/safe_sudo` gives an explicitly named operator group passwordless access
to one root-owned dispatcher. Sudoers grants no direct access to `pvesh`, a
shell, or `NOPASSWD:ALL`.

The role is disabled by default. `playbooks/safe-sudo.yml` requires both
`safe_sudo_apply=true` and `safe_sudo_confirmation=apply-safe-sudo` before it
changes a target. Supply its target and users only from a protected inventory.

For Proxmox discovery, use the dispatcher rather than direct sudo:

```bash
sudo -n /usr/local/sbin/safe-sudo pvesh-get /nodes
sudo -n /usr/local/sbin/safe-sudo pvesh-get /nodes/pve-836-01/status
```

Only the documented read-only endpoints are accepted. Add a new capability as
a reviewed dispatcher subcommand; do not broaden the sudoers command alias.
