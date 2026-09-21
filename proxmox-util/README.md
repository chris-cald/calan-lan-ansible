# Proxmox utilities

No inventory is included in this repository. Supply a caller-owned protected
inventory outside the checkout when running these playbooks:

```sh
ansible-playbook -i /absolute/path/to/protected-hosts.ini playbook.yml
```

Do not add topology, credentials, or controller state to this directory.
