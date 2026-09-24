# Disposable vGPU VM test root

This root is disabled by default. It creates one cloned test VM and attaches a
caller-created mediated device only when all protected inputs are supplied and
`vgpu_test_confirmation=apply-disposable-vgpu-test`.

Keep endpoint, token, node, template, VM ID, PCI identifier, mdev UUID, state,
and plans outside Git. Run from the protected controller:

```sh
tofu init -backend=false
tofu validate
tofu plan -var-file=/absolute/path/vgpu-test.tfvars
```

Apply only after the guarded Ansible host workflow exposes the selected mdev
profile and a disposable VM snapshot/cleanup owner is recorded.
