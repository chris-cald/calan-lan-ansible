#!/usr/bin/env python3
"""Build a custom Talos vGPU kernel, extension, and installer from pinned forks."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "tests" / "validate_vgpu_compatibility_manifest.py"
REVISION = re.compile(r"^[0-9a-fA-F]{40}$")
DIGEST_REF = re.compile(r"^.+@sha256:[0-9a-fA-F]{64}$")
REGISTRY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/:@-]*$")
BUILD_REQUIRED = {
    "talos_source_url",
    "talos_source_revision",
    "extensions_source_url",
    "extensions_source_revision",
    "builder_workspace",
    "builder_registry",
    "build_result_path",
    "extension_output_path",
}
OUTPUT_REQUIRED = {"kernel_image", "extension_image", "installer_image"}


def load(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            if ":" not in line:
                raise ValueError(f"unsupported manifest line: {line}")
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip().strip("\"'")
    return values


def run(argv: list[str], dry_run: bool = False) -> None:
    print("+", shlex.join(argv))
    if not dry_run:
        subprocess.run(argv, check=True)


def verify_sha256(path: Path, expected: str) -> None:
    with path.open("rb") as artifact:
        actual = hashlib.file_digest(artifact, "sha256").hexdigest()
    if actual.lower() != expected.lower():
        raise ValueError(f"SHA-256 mismatch for {path}")


def checkout(workspace: Path, name: str, url: str, revision: str, dry_run: bool) -> Path:
    target = workspace / name
    if not dry_run and target.exists() and not (target / ".git").is_dir():
        raise ValueError(f"{target} exists but is not a Git checkout")
    if not target.exists():
        run(["git", "clone", "--no-checkout", url, str(target)], dry_run)
    run(["git", "-C", str(target), "fetch", "--depth", "1", "origin", revision], dry_run)
    run(["git", "-C", str(target), "checkout", "--detach", revision], dry_run)
    if not dry_run:
        head = subprocess.check_output(["git", "-C", str(target), "rev-parse", "HEAD"], text=True).strip()
        if head != revision:
            raise ValueError(f"{name} revision mismatch: expected {revision}, found {head}")
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()

    subprocess.run([sys.executable, str(VALIDATOR), str(args.manifest)], check=True)
    values = load(args.manifest)
    missing = sorted(field for field in BUILD_REQUIRED if not values.get(field))
    if missing:
        raise ValueError(f"missing builder fields: {', '.join(missing)}")
    for field in ("talos_source_revision", "extensions_source_revision"):
        if not REVISION.fullmatch(values[field]):
            raise ValueError(f"{field} must be a full Git revision")
    for field in ("talos_source_url", "extensions_source_url"):
        if not values[field].startswith("https://"):
            raise ValueError(f"{field} must use HTTPS")

    workspace = Path(values["builder_workspace"])
    result_path = Path(values["build_result_path"])
    output_path = Path(values["extension_output_path"])
    driver_path = Path(values["guest_driver_artifact_path"])
    protected_paths = (workspace, result_path, output_path, driver_path)
    if not all(path.is_absolute() for path in protected_paths):
        raise ValueError("builder workspace, result, output, and driver paths must be absolute")
    if any(path.resolve().is_relative_to(ROOT) for path in protected_paths):
        raise ValueError("protected builder paths must be outside this checkout")
    if not REGISTRY.fullmatch(values["builder_registry"]):
        raise ValueError("builder_registry contains unsupported characters")
    if not args.dry_run:
        workspace.mkdir(mode=0o700, parents=True, exist_ok=True)
        if not driver_path.is_file():
            raise ValueError(f"guest driver artifact is absent: {driver_path}")
        verify_sha256(driver_path, values["guest_driver_artifact_sha256"])

    nvenc_patch_path: Path | None = None
    if values["nvenc_patch_enabled"].lower() == "true":
        patch_source = values["nvenc_patch_source"]
        if not patch_source.startswith("https://"):
            raise ValueError("nvenc_patch_source must use HTTPS")
        nvenc_patch_path = workspace / "nvenc.patch"
        run(
            [
                "curl",
                "--fail",
                "--location",
                "--proto",
                "=https",
                "--output",
                str(nvenc_patch_path),
                patch_source,
            ],
            args.dry_run,
        )
        if not args.dry_run:
            verify_sha256(nvenc_patch_path, values["nvenc_patch_sha256"])

    talos = checkout(workspace, "talos", values["talos_source_url"], values["talos_source_revision"], args.dry_run)
    extensions = checkout(workspace, "extensions", values["extensions_source_url"], values["extensions_source_revision"], args.dry_run)
    common = [
        f"REGISTRY={values['builder_registry']}",
        "PUSH=true",
        "PLATFORM=linux/amd64",
        f"VGPU_DRIVER_PATH={driver_path}",
        f"VGPU_DRIVER_SHA256={values['guest_driver_artifact_sha256']}",
        f"BUILD_RESULT_PATH={result_path}",
    ]
    if nvenc_patch_path:
        common.extend(
            [
                f"NVENC_PATCH_PATH={nvenc_patch_path}",
                f"NVENC_PATCH_SHA256={values['nvenc_patch_sha256']}",
                f"NVENC_PATCH_REVISION={values['nvenc_patch_revision']}",
            ]
        )
    # The protected forks must implement these targets and write BUILD_RESULT_PATH.
    run(["make", "-C", str(talos), "vgpu-kernel", *common], args.dry_run)
    run(["make", "-C", str(extensions), "vgpu-extension", *common], args.dry_run)
    run(["make", "-C", str(talos), "vgpu-imager", *common], args.dry_run)
    if args.dry_run:
        return 0

    result = json.loads(result_path.read_text())
    missing = sorted(OUTPUT_REQUIRED - result.keys())
    if missing:
        raise ValueError(f"build result is missing: {', '.join(missing)}")
    for field in OUTPUT_REQUIRED:
        if not DIGEST_REF.fullmatch(result[field]):
            raise ValueError(f"{field} must be an immutable OCI digest reference")
        run(["podman", "manifest", "inspect", result[field]])

    output_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    output_path.write_text(json.dumps({"manifest": values, "outputs": result}, indent=2) + "\n")
    output_path.chmod(0o600)
    print(f"wrote immutable Talos vGPU build record: {output_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, subprocess.CalledProcessError, ValueError, json.JSONDecodeError) as error:
        print(f"builder failed: {error}", file=sys.stderr)
        raise SystemExit(1)
