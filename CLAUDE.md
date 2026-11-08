# kingfish

## How work moves: the SDLC

This repo runs Anthropic's AI-native SDLC through the kit skill `omr-dev:run-sdlc`,
configured by `sdlc.json`. Every unit of work is a **change**: a folder
`changes/<YYYY-MM-DD>-<KEY>-<slug>/` (no `<KEY>` when there is no Linear issue) with `intent.md` (optional when the ticket states it),
`facts.md` (testable outcomes) and `plan.md` (files · order of work · risks · **Done**),
one PR, and a Linear issue when there is one. The plan is gated in plannotator before any code; the build
runs with **`/goal`** against the plan's Done section; every PR auto-merges on green; Claude reviews every PR
against [`REVIEW.md`](REVIEW.md); when the PR is green the folder moves to
`changes/archive/` under the same name. A design that outlives one PR is a
file in `docs/designs/`, edited in the change's PR; issue = change = PR, project = design. Handovers live in
the change folder, never in `.claude/plans/`. Start with `/omr-dev:run-sdlc <title>`;
the reference is **[docs/sdlc.md](docs/sdlc.md)**.

## Verifying your work

    npm run format && npm run lint && npm run typecheck && npm test

Run it before reporting any task complete, and paste the tail. `npm run slop` (anti-slop rules, complexity and clone metrics against `origin/main`; needs `lizard` on PATH) is its own CI job; hotspots live in `.fitness/slop-baseline.json` and may only shrink. `architecture.yaml` is the module and dependency policy: `npm run arch` checks the imports against it, `npm run perf` checks the bundle budgets, `npm run fitness` runs every dimension and writes `fitness-report.json`. `npm run gates-test` runs the negative fixtures in `tests/fixtures/gates` (every gate has `bad-*` cases that must fail and `good-*` cases that must pass; add one when you add a gate), and `npm run enforcement:audit` reports whether each rule's check is installed, configured, wired into `check` and green; a new fitness row in `architecture.yaml` needs an `enforcement` entry. If a test fails, fix the
code, not the test. The Stop hook runs it for you when source files are dirty.

## Decision4 handoff contract (v1)

Source: [Decision4 v1.0.1](https://github.com/Habitat-Thinking/decision4/blob/v1.0.1/DECISION4.md), Habitat Thinking, CC BY 4.0.

For every decision you make, ask: "If this turns out to be wrong,
what does it take to put right?" Take the class from the boundary map.
Classes run from lowest to highest: Undo, Repair, Migrate, Answer.

- Undo (a revert): hand back the result.
- Repair (real work, contained to this team): hand back the result and a
  choice story: Chose / Over / Because / Commits us to.
- Migrate (coordinated change involving other people): hand back at least
  two real options, or one stated as forced with the constraint that forces it.
- Answer (an explanation to someone outside the team with standing to ask,
  because the wrong outcome has reached them and nothing unmakes it): hand back
  evidence labelled observed, inferred, asked or unknown, and your challenges.
  Do not recommend.

Rules:

- Propose a class at or above the map's floor, never below it.
- Unmapped or unsure: take the higher class and log a map gap.
- A change takes the class of its highest decision.
- Escalate freely and say who it pulls in. Never lower a class silently.
- Unattended runs close only Undo. Above Undo, hand back and stop.

Here:

- The boundary map is `boundary-map.yaml` at the repo root.
- The PR description carries the Decision4 fields (`Decision-Class`, `Put-right`, `Answerer`, `Class-Change`); the template has them and the `decision4` check reads them.
- Autonomous runs (a /goal build, scheduled jobs, bots) close only work at or below the class approved at the plan gate (default ceiling Undo) and hand back anything higher.
- The answerer for Migrate and Answer is the owner unless the map names another.

<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:ca08a54f -->

## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

## Session Completion

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd dolt push
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**

- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds

<!-- END BEADS INTEGRATION -->

## Local CI and releases

Before every push, run `npm run format:check`, `npm run lint`, `npm run typecheck`, `npm test`, `npm run slop`, `npm run arch`, `npm run perf`, `npm run gates-test` and `npm run smoke` locally. Remote CI confirms a locally green change. Never push to find out which test fails.

Read the exact failing job or test, reproduce it locally, and rerun that test plus the directly affected suite until green. For an E2E change, iterate on the changed spec and its neighbours. Then run the full local gate once, batch the fixes into one push, and do not retry the whole pipeline for one failure.

To release a reviewed commit on main, choose its version and run `git tag vX.Y.Z && git push --tags`. The release workflow reads the version from the tag; ordinary main pushes never start it. Alternatively, use **Actions → Release → Run workflow** on main: Conventional Commits since the last release select the next version (fix/perf = patch, feat = minor, breaking = major). A manual run with no pending release stops before macOS starts. Both paths retain signing, notarization, update-bucket upload and GitHub release publishing.
