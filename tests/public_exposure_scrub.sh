#!/usr/bin/env sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$root"

for path in \
  proxmox-util/hosts.ini \
  playbooks/podman/inventory \
  playbooks/podman-semaphore/inventory \
  playbooks/awx/awx-github.pub
do
  if git ls-files --error-unmatch "$path" >/dev/null 2>&1; then
    echo "tracked private artifact: $path" >&2
    exit 1
  fi
  if ! git check-ignore -q "$path"; then
    echo "private artifact is not ignored: $path" >&2
    exit 1
  fi
done

if git grep -nE '\b(10\.[0-9]{1,3}\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[0-1])\.)' -- ':!tests/public_exposure_scrub.sh' >/dev/null; then
  echo "tracked private-network address" >&2
  exit 1
fi
