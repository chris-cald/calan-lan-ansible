# Talos OpenTofu handoff

Records that guarded Proxmox work completed and hands Talos VM lifecycle to a
caller-owned OpenTofu root. It never plans, applies, rolls back, or otherwise
owns OpenTofu state, Talos nodes, or Flux reconciliation.
