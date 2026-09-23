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
    "guest_driver_artifact_path",
    "guest_driver_artifact_sha256",
    "nvenc_patch_enabled",
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
    if not all(char in "0123456789abcdefABCDEF" for char in values["guest_driver_artifact_sha256"]) or len(values["guest_driver_artifact_sha256"]) != 64:
        print("guest_driver_artifact_sha256 must be a SHA-256 digest", file=sys.stderr)
        return 1
    if values["nvenc_patch_enabled"].lower() not in {"true", "false"}:
        print("nvenc_patch_enabled must be true or false", file=sys.stderr)
        return 1
    if values["nvenc_patch_enabled"].lower() == "true":
        patch_fields = {"nvenc_patch_source", "nvenc_patch_revision", "nvenc_patch_sha256"}
        missing_patch_fields = sorted(key for key in patch_fields if not values.get(key))
        if missing_patch_fields:
            print(f"missing NVENC patch fields: {', '.join(missing_patch_fields)}", file=sys.stderr)
            return 1
        if len(values["nvenc_patch_sha256"]) != 64 or not all(char in "0123456789abcdefABCDEF" for char in values["nvenc_patch_sha256"]):
            print("nvenc_patch_sha256 must be a SHA-256 digest", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
