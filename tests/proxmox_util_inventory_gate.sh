#!/usr/bin/env sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$root"

playbook=proxmox-util/playbook.yml
test -f "$playbook"
grep -q 'ansible.builtin.assert:' "$playbook"
grep -q 'proxmox_util_inventory' "$playbook"
ansible-playbook --syntax-check -i 'localhost,' "$playbook" \
  -e proxmox_util_inventory=/tmp/proxmox-hosts.ini >/dev/null
