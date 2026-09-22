provider "proxmox" {
  endpoint  = var.proxmox_endpoint
  api_token = var.proxmox_api_token
  insecure  = var.proxmox_insecure
}

# Talos is managed by the siderolabs provider when the VM module is added.
provider "talos" {}
