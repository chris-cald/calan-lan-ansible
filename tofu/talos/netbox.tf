provider "netbox" {
  server_url = var.netbox_url
  api_token  = var.netbox_api_token
}

provider "kubernetes" {
  config_path = var.kubeconfig_path
}

# ponytail: one reserved prefix is enough until HA requires a different allocation model.
data "netbox_prefix" "metallb" {
  tag = var.metallb_netbox_tag
}

resource "kubernetes_config_map_v1" "flux_substitutions" {
  metadata {
    name      = "metallb-address-pool"
    namespace = "flux-system"
  }

  data = {
    METALLB_POOL_CIDR = data.netbox_prefix.metallb.prefix
  }
}
