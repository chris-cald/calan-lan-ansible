#!/usr/bin/env python3
"""Offline contract checks for the Talos/MetalLB foundation."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text()


def test_proxmox_lifecycle_dependencies_are_pinned() -> None:
    versions = read("tofu/talos/versions.tf")
    assert 'source  = "bpg/proxmox"' in versions
    assert 'source  = "siderolabs/talos"' in versions
    assert 'version = "0.114.0"' in versions


def test_netbox_is_the_only_pool_source() -> None:
    netbox = read("tofu/talos/netbox.tf")
    variables = read("tofu/talos/variables.tf")
    assert 'data "netbox_prefix" "metallb"' in netbox
    assert "tag = var.metallb_netbox_tag" in netbox
    assert 'METALLB_POOL_CIDR = data.netbox_prefix.metallb.prefix' in netbox
    assert 'variable "netbox_url"' in variables
    assert 'variable "netbox_api_token"' in variables
    assert "sensitive   = true" in variables


def test_metallb_uses_flux_substitution_and_l2() -> None:
    pool = read("kubernetes/clusters/talos/infrastructure/metallb/config/address-pool.yaml")
    advertisement = read("kubernetes/clusters/talos/infrastructure/metallb/config/l2-advertisement.yaml")
    config = read("kubernetes/clusters/talos/infrastructure.yaml")
    assert "kind: IPAddressPool" in pool
    assert "- ${METALLB_POOL_CIDR}" in pool
    assert "kind: L2Advertisement" in advertisement
    assert "dependsOn:" in config
    assert "metallb-release" in config
    assert "metallb-config" in config
    assert "substituteFrom:" in config
    assert "metallb-address-pool" in config


def test_topology_and_state_are_not_committed() -> None:
    tracked = "\n".join(path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if path.is_file())
    assert "terraform.tfstate" not in tracked
    assert "*.tfvars" in read(".gitignore")


if __name__ == "__main__":
    test_proxmox_lifecycle_dependencies_are_pinned()
    test_netbox_is_the_only_pool_source()
    test_metallb_uses_flux_substitution_and_l2()
    test_topology_and_state_are_not_committed()
    print("Talos foundation contract checks passed")
