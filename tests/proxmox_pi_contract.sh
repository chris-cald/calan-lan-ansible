#!/bin/sh
set -eu

role=roles/proxmox_pi
for file in "$role/defaults/main.yml" "$role/tasks/main.yml" "$role/README.md" playbooks/proxmox-pi.yml; do
  test -f "$file" || { echo "missing $file" >&2; exit 1; }
done

grep -Fqx 'proxmox_pi_apply: false' "$role/defaults/main.yml"
grep -Fq 'proxmox_pi_confirm: ""' "$role/defaults/main.yml"
grep -Fq 'proxmox_pi_unsupported_hardware_acknowledgement: ""' "$role/defaults/main.yml"
grep -Fq 'include_role:' "$role/tasks/main.yml"
grep -Fq 'name: proxmox_ve' "$role/tasks/main.yml"
grep -Fq 'proxmox_ve_supported_architectures: [aarch64, arm64]' "$role/tasks/main.yml"
grep -Fq "FingerlessGloves, ‘Installing Proxmox on Raspberry Pi’" "$role/README.md"
grep -Fq 'proxmox_pi' playbooks/proxmox-pi.yml
