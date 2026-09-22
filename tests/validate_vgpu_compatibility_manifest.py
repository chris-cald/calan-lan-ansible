#!/usr/bin/env python3
"""Validate a flat, caller-owned Talos vGPU compatibility manifest."""

import sys
from pathlib import Path

REQUIRED = {
    "gpu_model",
    "vgpu_profile",
    "proxmox_version",
    "host_vgpu_manager_branch",
    "talos_version",
    "talos_kernel",
    "guest_driver_branch",
    "license_reviewed",
    "compatibility_reference",
    "extension_source",
}


def load(path: Path) -> dict[str, str]:
    values = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"unsupported manifest line: {line}")
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"\'')
    return values


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_vgpu_compatibility_manifest.py /absolute/path/manifest.yml", file=sys.stderr)
        return 2
    values = load(Path(sys.argv[1]))
    missing = sorted(key for key in REQUIRED if not values.get(key))
    if missing:
        print(f"missing required fields: {', '.join(missing)}", file=sys.stderr)
        return 1
    if values["license_reviewed"].lower() != "true":
        print("license_reviewed must be true", file=sys.stderr)
        return 1
    if values["host_vgpu_manager_branch"] != values["guest_driver_branch"]:
        print("host and guest vGPU driver branches must match", file=sys.stderr)
        return 1
    if not values["compatibility_reference"].startswith("https://"):
        print("compatibility_reference must be an HTTPS source", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
