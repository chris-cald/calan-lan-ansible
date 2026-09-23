# sudo role

Creates a user with the platform's privileged group and optionally writes a
validated passwordless sudoers entry.

## Inputs

- `privileged_user` — required user name.
- `privileged_group` — optional privileged group; defaults from platform vars.
- `password_required` — defaults to `true`.
- `passwordless_commands` — optional caller-owned command list used only when
  `password_required: false`. An empty list preserves legacy `NOPASSWD:ALL`.

Keep service-specific privilege policy in the caller. For read-only Proxmox API
queries, a protected caller can use:

```yaml
password_required: false
passwordless_commands:
  - /usr/bin/pvesh get *
```

This permits `pvesh get` only; it does not permit `create`, `set`, or `delete`.
The sudoers file is validated with `visudo` before it is written.
