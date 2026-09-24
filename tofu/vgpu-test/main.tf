provider "proxmox" {
  endpoint  = var.proxmox_endpoint
  api_token = var.proxmox_api_token
  insecure  = var.proxmox_insecure
}

resource "proxmox_virtual_environment_vm" "vgpu_test" {
  count = var.vgpu_test_apply ? 1 : 0

  name      = var.vgpu_test_vm_name
  node_name = var.vgpu_test_node_name
  vm_id     = var.vgpu_test_vm_id
  started   = true
  tags      = ["test", "vgpu"]

  clone {
    vm_id = var.vgpu_test_template_vm_id
    full  = true
  }

  hostpci {
    device = var.vgpu_parent_pci_device
    id     = "hostpci0"
    mdev   = var.vgpu_mdev_uuid
    pcie   = true
  }
}
