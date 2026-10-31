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

Run it before reporting any task complete, and paste the tail. If a test fails, fix the
code, not the test. The Stop hook runs it for you when source files are dirty.

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
