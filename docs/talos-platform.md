# Talos platform foundation

## Decision

Run a single Talos control-plane VM on Proxmox. OpenTofu owns VM and
Talos lifecycle; Flux owns in-cluster manifests; NetBox is the address-pool
authority. The cluster may expand to three control-plane VMs without changing
its GitOps layout.

Talos was chosen over MicroK8s because its immutable API-managed operating
model matches the declared lifecycle. K3s remains the fallback if Kubernetes
nodes later need to be general Linux hosts. Rancher/RKE2 and Portainer are not
part of the initial platform: they add management-plane overhead without
improving this single-node cluster.

## Initial operating model

- Storage: local-path volumes and Proxmox backups.
- Service exposure: MetalLB Layer 2 on a NetBox-reserved LAN prefix.
- Delivery: Flux reconciles `kubernetes/clusters/talos/` from this repository.
- Node diagnostics: Talos API and `talosctl`, not SSH or package management.

`tofu/talos/netbox.tf` reads the prefix selected by
`metallb_netbox_tag` and writes it to the `flux-system/metallb-address-pool`
ConfigMap. Flux substitutes that value into MetalLB's `IPAddressPool`; the
CIDR and credentials never enter Git.

## Apply order

1. Create exactly one NetBox prefix tagged for MetalLB and issue a read-only
   API token.
2. Provision the Talos VM through the `bpg/proxmox` and `siderolabs/talos`
   providers, using a standard Talos Image Factory installer ISO, UEFI/q35,
   VirtIO SCSI, VirtIO networking, and disabled ballooning. This foundation
   intentionally does not infer VM names, addresses, disk, CPU, memory, or
   cluster endpoint.
3. Bootstrap Flux against `kubernetes/clusters/talos/` with a protected Git
   credential. Flux creates its own generated bootstrap manifests at that
   time.
4. Apply `tofu/talos/` with caller-supplied protected variables. It creates
   only the Flux substitution ConfigMap.
5. Verify `metallb-release` and `metallb-config` report Ready, then create a
   disposable `LoadBalancer` Service and confirm its allocated address is in
   the NetBox-reserved prefix.

No Talos, Flux, NetBox, Proxmox, or Kubernetes command may be applied as part
of repository validation. The legacy MicroK8s root playbook remains untouched
until a separately approved migration and rollback plan exists.
