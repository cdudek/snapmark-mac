# Provenance

- Source: https://github.com/dmmulroy/anti-slop (MIT), skill `install-anti-slop`, plugin `oxlint-plugin-anti-slop` 0.1.2
- Source commit: 13909c9e07590f5a85d93c62712259fe14a883f7
- Installed with the skill's `scripts/install.mjs` into this folder; the generic plugin only (`index.ts`), the Effect group in `effect/` is copied but not enabled (this app does not use Effect, CQ-14)
- Registered in `/.oxlintrc.json`, run by `scripts/slop.py` in the `slop` CI job
- Deviations from upstream: none
- Update through the skill ("update anti-slop while preserving local customizations"), and record any rule change as an ADR
