#!/usr/bin/env python3
"""Negative fixtures for every gate (TEST-19): bad-* must fail it, good-* must pass it.

  python3 scripts/gates_test.py [gate ...]

tests/fixtures/gates/<gate>/<case>/ holds one case. A bad case may carry `expect`, a text its output must contain,
so it fails for the reason it is named after. Needs what the gates need: PyYAML, lizard, node 22 and `npm ci`.
  slop         head/ [base/] baseline.json   scripts/slop.py --root head [--base-root base]
  arch         spec.yaml + src/      scripts/fitness.py arch --root case
  perf         spec.yaml + bundle/    scripts/fitness.py perf --root case
  enforcement  spec.yaml + ci.yml    scripts/enforcement_audit.py --offline
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests/fixtures/gates"
PY = sys.executable


def command(gate, case, tmp):
    report = str(Path(tmp) / "report.json")
    if gate == "slop":
        cmd = [PY, "scripts/slop.py", "--root", str(case / "head"), "--baseline", str(case / "baseline.json"), "--report", report]
        if (case / "base").exists():
            cmd += ["--base-root", str(case / "base")]
    elif gate in ("arch", "perf"):
        cmd = [PY, "scripts/fitness.py", gate, "--root", str(case), "--spec", str(case / "spec.yaml"), "--report", report]
    elif gate == "enforcement":
        cmd = [PY, "scripts/enforcement_audit.py", "--root", str(case), "--spec", str(case / "spec.yaml"), "--workflow", str(case / "ci.yml"), "--offline"]
    else:
        sys.exit(f"gates-test: no runner for the fixture folder {gate}")
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def main():
    present = {p.name for p in FIXTURES.iterdir() if p.is_dir()}
    if {"slop", "arch", "perf", "enforcement"} - present:
        sys.exit(f"gates-test: no fixtures for {sorted({'slop', 'arch', 'perf', 'enforcement'} - present)}")
    gates = sys.argv[1:] or sorted(present)
    failures = 0
    for gate in gates:
        cases = sorted(p for p in (FIXTURES / gate).iterdir() if p.is_dir())
        kinds = {c.name.split("-")[0] for c in cases}
        if kinds != {"bad", "good"}:
            print(f"FAIL {gate}: needs at least one bad-* and one good-* case, has {sorted(kinds)}")
            failures += 1
        for case in cases:
            with tempfile.TemporaryDirectory() as tmp:
                p = command(gate, case, tmp)
            out = p.stdout + p.stderr
            bad = case.name.startswith("bad-")
            want = (case / "expect").read_text().strip() if (case / "expect").exists() else ""
            if bad and p.returncode == 0:
                verdict = "gate passed a bad case"
            elif not bad and p.returncode != 0:
                verdict = f"gate failed a good case\n{out[-1500:]}"
            elif bad and want not in out:
                verdict = f"failed, but not for the expected reason ({want!r})\n{out[-1500:]}"
            else:
                verdict = ""
            print(f"{'FAIL' if verdict else 'ok  '} {gate}/{case.name}" + (f": {verdict}" if verdict else ""))
            failures += bool(verdict)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
