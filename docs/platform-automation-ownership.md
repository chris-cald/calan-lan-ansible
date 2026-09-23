# Platform automation ownership

## Decisions

| Concern | Owner | Boundary |
| --- | --- | --- |
| Kubernetes node lifecycle | Talos | Immutable node OS; no SSH or package management in nodes. |
| Kubernetes desired state | Flux | Reconciles repository manifests and workloads. |
| Proxmox VM and image lifecycle | OpenTofu | Declarative lifecycle only; state stays outside Git. |
| Proxmox host maintenance | Ansible | Protected operator controller, dedicated SSH account, narrowly scoped sudo. |
| NVIDIA vGPU host configuration | Ansible | Guarded host packages, IOMMU, vGPU Manager, mediated devices, reboots, and validation. |
| NVIDIA vGPU Talos guest | Talos custom system extension | Blocked by the doc-vader compatibility spike before production rollout. |
| GPU workload scheduling | Flux | Deploys runtime/device-plugin resources after guest compatibility is proven. |
| Legacy AWX and Semaphore | Retired | Remove runnable automation; retain only Git history. |
| Secrets | OpenBao/Vault | Dedicated Proxmox VM, external to Git and Talos bootstrap. |
| Vault recovery | Shamir shares | Separate protected locations; no share in Git or the same VM. |

## Bootstrap order

1. OpenTofu provisions the dedicated OpenBao/Vault VM.
2. Guarded Ansible configures OpenBao/Vault from the protected controller.
3. OpenBao/Vault supplies scoped credentials to the protected controller.
4. OpenTofu provisions Talos VM lifecycle resources and renders NetBox-derived
   MetalLB data.
5. Talos boots immutable nodes; Flux reconciles cluster workloads.
6. The vGPU compatibility spike must pass before GPU-sharing services enter
   the Talos rollout.

## Non-negotiable constraints

- No secrets, topology, inventory, private keys, or state in Git.
- CI validates source only; it never applies, rolls back, or contacts a target.
- Host changes retain explicit apply/confirmation controls and caller-owned
  protected inputs.
- Talos vGPU guest support is not presumed: it requires a version-pinned,
  license-compliant extension compatible with the selected Proxmox vGPU
  Manager.
