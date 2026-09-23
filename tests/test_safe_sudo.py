#!/usr/bin/env python3
"""Offline contract for the safe-sudo dispatcher role."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text()


def test_dispatcher_is_default_disabled_and_sudoers_only_runs_it() -> None:
    defaults = read("roles/safe_sudo/defaults/main.yml")
    policy = read("roles/safe_sudo/templates/safe-sudo.sudoers.j2")
    assert "safe_sudo_enabled: false" in defaults
    assert "NOPASSWD: SAFE_SUDO" in policy
    assert "safe_sudo_dispatcher_path" in policy


def test_pvesh_get_is_a_narrow_dispatcher_capability() -> None:
    dispatcher = read("roles/safe_sudo/files/safe-sudo")
    assert "pvesh-get)" in dispatcher
    assert 'exec "$PVESH" get "$endpoint"' in dispatcher
    assert 'pvesh endpoint is not whitelisted' in dispatcher
    assert "/cluster/resources" in dispatcher


def test_deployment_playbook_requires_a_typed_confirmation() -> None:
    playbook = read("playbooks/safe-sudo.yml")
    assert "safe_sudo_apply: false" in playbook
    assert "apply-safe-sudo" in playbook


if __name__ == "__main__":
    test_dispatcher_is_default_disabled_and_sudoers_only_runs_it()
    test_pvesh_get_is_a_narrow_dispatcher_capability()
    test_deployment_playbook_requires_a_typed_confirmation()
    print("safe-sudo contract checks passed")
