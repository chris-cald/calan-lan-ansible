variable "proxmox_endpoint" {
  description = "Proxmox API endpoint, supplied by the caller."
  type        = string
  sensitive   = true
}

variable "proxmox_api_token" {
  description = "Least-privilege Proxmox API token, supplied by the caller."
  type        = string
  sensitive   = true
}

variable "proxmox_insecure" {
  description = "Permit an unverified Proxmox TLS certificate."
  type        = bool
  default     = false
}

variable "netbox_url" {
  description = "NetBox API base URL, supplied by the caller."
  type        = string
  sensitive   = true
}

variable "netbox_api_token" {
  description = "Read-only NetBox API token, supplied by the caller."
  type        = string
  sensitive   = true
}

variable "metallb_netbox_tag" {
  description = "NetBox tag slug applied to exactly one reserved MetalLB prefix."
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9]+(?:-[a-z0-9]+)*$", var.metallb_netbox_tag))
    error_message = "metallb_netbox_tag must be a NetBox tag slug."
  }
}

variable "kubeconfig_path" {
  description = "Path to the Talos-generated kubeconfig, supplied by the caller."
  type        = string
  sensitive   = true
}
