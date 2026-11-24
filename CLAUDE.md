# kingfish

## How work moves: the SDLC

sdlc-run is retired. Work runs through cfactory: start with `/calvin-factory:cfactory`.
Claude reviews every PR against [`REVIEW.md`](REVIEW.md). The existing `changes/` folders and
`sdlc.json` stay because scripts read them; [docs/sdlc.md](docs/sdlc.md) is history.

## Verifying your work

    npm run format && npm run lint && npm run typecheck && npm test

Run it before reporting any task complete, and paste the tail. `npm run slop` (anti-slop rules, complexity and clone metrics against `origin/main`; needs `lizard` on PATH) is its own CI job; hotspots live in `.fitness/slop-baseline.json` and may only shrink. `architecture.yaml` is the module and dependency policy: `npm run arch` checks the imports against it, `npm run perf` checks the bundle budgets, `npm run fitness` runs every dimension and writes `fitness-report.json`. `npm run gates-test` runs the negative fixtures in `tests/fixtures/gates` (every gate has `bad-*` cases that must fail and `good-*` cases that must pass; add one when you add a gate), and `npm run enforcement:audit` reports whether each rule's check is installed, configured, wired into `check` and green; a new fitness row in `architecture.yaml` needs an `enforcement` entry. If a test fails, fix the
code, not the test. Git hooks run the cheap part for you (see "Git hooks" in `AGENTS.md`).

## Decision4

@AGENTS.md

The handoff contract lives in `AGENTS.md`; use `boundary-map.yaml` and the readable PR template.

## Tracking

`bd` (beads) is available, not mandatory.

## Checks and releases

Fast checks run in the git hooks (pre-commit, pre-push; see "Git hooks" in `AGENTS.md`). The full suite (`npm test`), `npm run slop`, `npm run arch`, `npm run perf`, `npm run gates-test` and `npm run smoke` run in CI only. Remote CI runs once per ready (non-draft) PR, never on push, and Decision4 is an optional PR-body section with no CI check. Read the failing job, reproduce that one test locally, fix it, and batch the fixes into one push; do not rerun the whole pipeline for one failure.

To release a reviewed commit on main, choose its version and run `git tag vX.Y.Z && git push --tags`. The release workflow reads the version from the tag; ordinary main pushes never start it. Alternatively, use **Actions → Release → Run workflow** on main: Conventional Commits since the last release select the next version (fix/perf = patch, feat = minor, breaking = major). A manual run with no pending release stops before macOS starts. Both paths retain signing, notarization, update-bucket upload and GitHub release publishing.

## Node tooling

Use `nvm use` before local checks. `.nvmrc` is the Node 24 tooling version source;
CI reads it with `node-version-file` and `engines.node` constrains the same major.
Electron bundles its own Node runtime.
