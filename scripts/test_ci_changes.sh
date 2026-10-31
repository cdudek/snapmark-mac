#!/usr/bin/env bash
# Usage: sh scripts/test_ci_changes.sh   (needs bash and jq)
# Runs the `changes` step of .github/workflows/ci.yml (the lines between its changes-script markers) against fake
# changed-file lists and this repo's own sdlc.json ciPaths, with a stub `gh`. One line per case; exits 1 if a case differs.
set -eu
root=$(cd "$(dirname "$0")/.." && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

sed -n '/# >>> changes-script/,/# <<< changes-script/p' "$root/.github/workflows/ci.yml" | sed 's/^          //' > "$tmp/changes.sh"
[ -s "$tmp/changes.sh" ] || { echo "FAIL: no changes-script markers in ci.yml"; exit 1; }
cp "$root/sdlc.json" "$tmp/sdlc.json"
mkdir "$tmp/bin"
printf '#!/bin/sh\ncat "$FAKE_FILES"\n' > "$tmp/bin/gh"
chmod +x "$tmp/bin/gh"

fail=0
# case NAME BASE HEAD EXPECTED("lint unit e2e-matrix-kind") FILES...   kind: none | shards
run_case() {
  local name=$1 base=$2 head=$3 want=$4; shift 4
  printf '%s\n' "$@" > "$tmp/files"
  : > "$tmp/out"
  local pr=7
  [ "$base" = push ] && pr=""
  (cd "$tmp" && PATH="$tmp/bin:$PATH" FAKE_FILES="$tmp/files" GITHUB_OUTPUT="$tmp/out" GITHUB_STEP_SUMMARY=/dev/null \
    PR="$pr" BASE="$base" HEAD="$head" DEFAULT=main SHARDS=1 bash "$tmp/changes.sh") || { echo "FAIL  $name: script exited non-zero"; fail=1; return; }
  local m kind got
  m=$(sed -n 's/^matrix=//p' "$tmp/out")
  case "$m" in '[]') kind=none ;; *) kind=smoke ;; esac
  got="$(sed -n 's/^lint=//p' "$tmp/out") $(sed -n 's/^unit=//p' "$tmp/out") $kind"
  if [ "$got" = "$want" ]; then echo "ok    $name: $got"; else echo "FAIL  $name: got [$got] want [$want]"; fail=1; fi
}

M=milestone/x # a feature PR into a milestone branch: not a full run
run_case "readme and docs"          $M f/a "false false none" README.md docs/ux/owner-words.md docs/designs/INDEX.md changes/2026-x/plan.md CLAUDE.md
run_case "screenshots"              $M f/a "false false none" docs/ux/shot.png changes/2026-x/shot.png snapmark-app/README.md
run_case "design exploration code"  $M f/a "false false none" design-explorations/2026-x/index.html design-explorations/2026-x/app.js
run_case "unlisted non-code file"   $M f/a "false false none" notes.csv .github/dependabot.yml .claude/plans/a.json
run_case "app source"               $M f/a "true true none"   snapmark-app/src/editor.html
run_case "unit test"                $M f/a "true true none"   snapmark-app/test/sessions.test.ts
run_case "bundled asset"            $M f/a "false true none"  snapmark-app/assets/trayTemplate.png
run_case "packaging entitlements"   $M f/a "false false none" snapmark-app/build/entitlements.mac.plist
run_case "package.json"             $M f/a "true true none"   snapmark-app/package.json
run_case "tsconfig"                 $M f/a "true true none"   snapmark-app/tsconfig.json
run_case "prettier config"          $M f/a "true false none"  .prettierrc.json
run_case "sdlc script"              $M f/a "true true none"   scripts/verify_gate.py
run_case "claude hook"              $M f/a "false true none"  .claude/hooks/gate-bash.sh
run_case "workflow"                 $M f/a "true true none"   .github/workflows/ci.yml
run_case "sdlc.json"                $M f/a "true true none"   sdlc.json
run_case "lockfile"                 $M f/a "true true none"   package-lock.json
# the safety net
run_case "docs only, into main"     main f/a "false false none"  README.md changes/2026-x/plan.md docs/ux/shot.png
run_case "docs only, milestone head" main milestone/x "false false none" README.md
run_case "app source, into main"    main f/a "true true smoke"   snapmark-app/src/main.ts
run_case "asset only, into main"    main f/a "true true smoke"   snapmark-app/assets/tray.svg
run_case "app source plus docs"     main f/a "true true smoke"   README.md snapmark-app/src/main.ts
run_case "push to main"             push "" "true true smoke"    README.md
exit "$fail"
