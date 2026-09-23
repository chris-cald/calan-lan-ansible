# `proxmox_pi`

Experimental Raspberry Pi wrapper around [`proxmox_ve`](../proxmox_ve/README.md).

## Attribution and support boundary

Adapted from **FingerlessGloves, ‘Installing Proxmox on Raspberry Pi’**
(published 5 August 2026),
<https://fingerlessgloves.me/2026/08/05/installing-proxmox-on-raspberry-pi/>.
The guide builds on Proxmox's [Debian 13 Trixie installation guide](https://pve.proxmox.com/wiki/Install_Proxmox_VE_on_Debian_13_Trixie).
This role is not affiliated with, endorsed by, or a replacement for either
source.

[Proxmox VE system requirements](https://pve.proxmox.com/wiki/System_Requirements)
exclude device-tree-only Raspberry Pi systems. This wrapper therefore requires
`proxmox_pi_unsupported_hardware_acknowledgement:
accept-unsupported-raspberry-pi-pve` before it will delegate any mutation to
the common role.

## Inputs

```yaml
proxmox_pi_apply: true
proxmox_pi_confirm: provision-proxmox-pi
proxmox_pi_unsupported_hardware_acknowledgement: accept-unsupported-raspberry-pi-pve
proxmox_pi_node_address: 192.0.2.10
proxmox_pi_node_hostname: pve-pi-01
proxmox_pi_cluster_mode: single # or create, join
```

All topology is caller-supplied. Set `proxmox_pi_manage_network: true` with the
interface, prefix, and gateway to stage `vmbr0` for a separately planned,
console-tested activation. `create` needs `proxmox_pi_cluster_name`; `join`
needs the existing node IP, SHA-256 API certificate fingerprint, protected
password, and the explicit `/etc/pve` data-loss acknowledgement.

Validate with:

```sh
./tests/proxmox_pi_contract.sh
ANSIBLE_ROLES_PATH=roles ansible-playbook --syntax-check playbooks/proxmox-pi.yml
```
