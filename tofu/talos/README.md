# Talos Flux substitutions

This OpenTofu root has one responsibility: read the reserved MetalLB
prefix from NetBox and make it available to Flux as a ConfigMap.

Provide `proxmox_endpoint`, `proxmox_api_token`, `netbox_url`,
`netbox_api_token`, `metallb_netbox_tag`, and `kubeconfig_path` from protected
Semaphore/OpenTofu inputs. The NetBox token must be read-only; the Proxmox
token must use the least privileges required by the VM module. TLS verification
is required unless the caller explicitly sets `proxmox_insecure`. Do not commit
a `.tfvars` file, kubeconfig, address, or credential.

Run `tofu init -lockfile=readonly`, `tofu validate`, and `tofu plan` only
after the Talos cluster and Flux namespace exist. Applying changes
NetBox is intentionally impossible from this root; the sole managed object is
the in-cluster substitution ConfigMap.
