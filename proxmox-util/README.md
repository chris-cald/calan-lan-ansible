# Proxmox utilities

No inventory is included in this repository. Supply a caller-owned protected
inventory outside the checkout when running these playbooks:

```sh
ansible-playbook \
  -i /absolute/path/to/protected-hosts.ini \
  -e proxmox_util_inventory=/absolute/path/to/protected-hosts.ini \
  proxmox-util/playbook.yml
```

The standalone entrypoint rejects an omitted, repository-local, or different
inventory path before importing any utility tasks. It ensures the QEMU guest
agent is installed from the distribution's configured repository but never
upgrades it to the latest available version; use the separate guarded Proxmox
maintenance workflow for package upgrades.

Do not add topology, credentials, or controller state to this directory.
