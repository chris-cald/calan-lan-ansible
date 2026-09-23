#!/bin/sh
set -eu

for role in proxmox_ve proxmox_pi proxmox_x64 proxmox_arm64; do
  for file in "roles/$role/defaults/main.yml" "roles/$role/tasks/main.yml" "roles/$role/README.md"; do
    test -f "$file" || { echo "missing $file" >&2; exit 1; }
  done
done

for playbook in playbooks/proxmox-pi.yml playbooks/proxmox-x64.yml playbooks/proxmox-arm64.yml; do
  test -f "$playbook" || { echo "missing $playbook" >&2; exit 1; }
done

grep -Fq 'include_role:' roles/proxmox_pi/tasks/main.yml
grep -Fq 'name: proxmox_ve' roles/proxmox_pi/tasks/main.yml
grep -Fq 'include_role:' roles/proxmox_x64/tasks/main.yml
grep -Fq 'name: proxmox_ve' roles/proxmox_x64/tasks/main.yml
grep -Fq 'include_role:' roles/proxmox_arm64/tasks/main.yml
grep -Fq 'name: proxmox_ve' roles/proxmox_arm64/tasks/main.yml
grep -Fq "FingerlessGloves, ‘Installing Proxmox on Raspberry Pi’" roles/proxmox_pi/README.md
grep -Fq 'nvidia-grace-hopper' roles/proxmox_arm64/defaults/main.yml
grep -Fq 'nvidia-vera' roles/proxmox_arm64/defaults/main.yml
grep -Fq 'proxmox_ve_apply: false' roles/proxmox_ve/defaults/main.yml
grep -Fq "'pvecm', 'create'" roles/proxmox_ve/tasks/main.yml
grep -Fq 'pvecm add' roles/proxmox_ve/tasks/main.yml
grep -Fq 'no_log: true' roles/proxmox_ve/tasks/main.yml
grep -Fq '/sys/firmware/efi' roles/proxmox_arm64/tasks/main.yml
grep -Fq '/sys/firmware/acpi' roles/proxmox_arm64/tasks/main.yml
