variable "proxmox_endpoint" {
  type      = string
  sensitive = true
  default   = ""
}

variable "proxmox_api_token" {
  type      = string
  sensitive = true
  default   = ""
}

variable "proxmox_insecure" {
  type    = bool
  default = false
}

variable "vgpu_test_apply" {
  type    = bool
  default = false
}

variable "vgpu_test_confirmation" {
  type      = string
  sensitive = true
  default   = ""
}

variable "vgpu_test_node_name" {
  type    = string
  default = ""
}

variable "vgpu_test_template_vm_id" {
  type    = number
  default = 0
}

variable "vgpu_test_vm_id" {
  type    = number
  default = 0
}

variable "vgpu_test_vm_name" {
  type    = string
  default = "vgpu-talos-test"
}

variable "vgpu_mdev_uuid" {
  description = "Caller-created mediated-device UUID."
  type        = string
  default     = ""
}

variable "vgpu_parent_pci_device" {
  description = "Caller-supplied PCI device identifier for the mdev parent."
  type        = string
  default     = ""
}
