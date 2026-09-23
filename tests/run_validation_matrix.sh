#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$root"

python3 tests/test_validation_matrix.py
python3 tests/test_platform_transition.py
python3 tests/test_vgpu_compatibility_manifest.py
python3 tests/test_nvidia_vgpu_workflow.py
python3 tests/test_proxmox_vgpu_roles.py
python3 tests/test_platform_orchestration.py
python3 tests/test_platform_discovery_resume.py
sh tests/proxmox_platform_roles_contract.sh
sh tests/proxmox_pi_contract.sh
python3 tests/test_proxmox_vgpu_unlock_podman.py
python3 tests/test_proxmox_no_nag.py
python3 tests/test_safe_sudo.py
python3 tests/test_vgpu_e2e_stack.py
sh tests/public_exposure_scrub.sh
sh tests/proxmox_util_inventory_gate.sh
ANSIBLE_ROLES_PATH="$PWD/roles" ansible-playbook -i 'localhost,' --syntax-check roles/sudo/tests/test.yml

if [ -f playbook.yml ] && [ -d roles/microk8s ]; then
  ANSIBLE_ROLES_PATH="$PWD/roles" ansible-playbook --syntax-check playbook.yml
elif [ -f playbook.yml ]; then
  echo 'SKIP: playbook.yml requires the absent roles/microk8s role.'
else
  echo 'SKIP: legacy MicroK8s playbook retired; Talos lifecycle is owned by OpenTofu and Flux.'
fi

if [ "${RUN_MOLECULE:-0}" = 1 ]; then
  molecule test
else
  echo 'SKIP: set RUN_MOLECULE=1 in a disposable Docker-capable runner to execute future Molecule scenarios.'
fi
