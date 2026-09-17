# ssh_safe_reader

Installs or removes one persistent, non-privileged SSH public key for an existing target login user. It is disabled by default, does not select hosts, grant sudo, alter groups, or harden service data.

## Use

Target hosts at execution time; do not put a target default in the role:

```sh
ANSIBLE_ROLES_PATH="$PWD/roles" ansible-playbook -i inventory playbooks/ssh-safe-reader.yml \
  -e ssh_safe_reader_targets=home \
  -e ssh_safe_reader_enabled=true
```

By default, the role uses the current Ansible connection user and controller path
`~/.ssh/id_ed25519_safe_reader`. Set `ssh_safe_reader_login_user` or
`ssh_safe_reader_key_path` to override either.

The private key and `.pub` must already exist. To create an encrypted keypair locally,
explicitly set both `ssh_safe_reader_create_key=true` and a nonempty
`ssh_safe_reader_key_passphrase`; the passphrase is never logged. The role fails closed
when the key material is missing or incomplete.

Set `ssh_safe_reader_state=absent` to remove the exact deployed public key. Retain its
public key locally until removal succeeds.

The temporary per-operation OpenSSH-CA certificate workflow is intentionally not part of
this role yet.
