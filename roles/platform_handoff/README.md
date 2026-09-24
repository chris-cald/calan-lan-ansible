# Platform handoff

Persists discovery results outside the checkout and, after a selected Talos
handoff, prints OpenTofu and Flux commands for the next owner. It does not run
OpenTofu or Flux and never stores credentials, topology, or state in Git.
