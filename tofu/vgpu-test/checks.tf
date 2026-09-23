check "explicit_vgpu_test_approval" {
  assert {
    condition = !var.vgpu_test_apply || (
      var.vgpu_test_confirmation == "apply-disposable-vgpu-test" &&
      var.proxmox_endpoint != "" &&
      var.proxmox_api_token != "" &&
      var.vgpu_test_node_name != "" &&
      var.vgpu_test_template_vm_id > 0 &&
      var.vgpu_test_vm_id > 0 &&
      var.vgpu_mdev_uuid != "" &&
      var.vgpu_parent_pci_device != ""
    )
    error_message = "Applying the disposable vGPU VM requires all protected inputs and the typed confirmation."
  }
}
