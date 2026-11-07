#!/usr/bin/env python3
"""The `slop` gate (CQ-16, CQ-18..21): anti-slop lint rules plus complexity and clone metrics.

  python3 scripts/slop.py [--base REF] [--update] [--report FILE] [--summary FILE]

Needs on PATH: node (22+), lizard (pip install lizard==1.25.1), npx (jscpd). Run from anywhere.
Measures the TypeScript under SCOPE, then fails when:
  1. an anti-slop rule has more hits in a file than .fitness/slop-baseline.json allows (0 new hits),
  2. a function above complexity 10 is not in the baseline, or is more complex than its baseline entry (CQ-19),
  3. erosion, complex-function count, max complexity, clone ratio or hit density is above REF's (CQ-18, CQ-20),
  4. the baseline holds anything the merge base's baseline did not (it may only shrink, CQ-21).
REF is the merge base on a PR and the previous commit on a push. Without --base only 1 and 2 run.
--update rewrites the baseline from today's measurement; commit it only when it shrank.
"""

import argparse
import csv
import json
import math
import os
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCOPE = ["snapmark-app/src", "snapmark-app/test"]
BASELINE = ".fitness/slop-baseline.json"
CC_LIMIT = 10
# Lower is better for every metric; a PR may not raise any of them (CQ-18..20).
METRICS = ["erosion", "complex_functions", "max_complexity", "clone_ratio", "hits_per_kloc"]
SLOP_RULES = ("anti-slop(", "oxc(no-accumulating-spread)")
OXLINT = ROOT / "node_modules/.bin/oxlint"
JSCPD = "jscpd@5.4.2"


def run(cmd, cwd, ok=(0,)):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if p.returncode not in ok:
        sys.exit(f"slop: {' '.join(map(str, cmd))} exited {p.returncode}\n{p.stderr[-2000:]}")
    return p.stdout


def lizard(root):
    """Per function: (file, name, complexity, nloc)."""
    out = run(["lizard", "-l", "typescript", "--csv", *SCOPE], root)
    return [(r[6], r[7], int(r[1]), int(r[0])) for r in csv.reader(out.splitlines()) if len(r) >= 10]


def clone_ratio(root):
    with tempfile.TemporaryDirectory() as out:
        run(["npx", "--yes", JSCPD, "--reporters", "json", "--output", out, "--format", "typescript", "--silent", *SCOPE], root)
        return json.loads((Path(out) / "jscpd-report.json").read_text())["statistics"]["total"]["percentage"] / 100


def slop_hits(root):
    """{"file|rule": count} of error-level anti-slop hits. Runs HEAD's config on the tree at root."""
    cmd = [str(OXLINT), "-c", str(ROOT / ".oxlintrc.json"), "-f", "json", *SCOPE]
    out = run(cmd, root, ok=(0, 1))
    return dict(Counter(f"{d['filename']}|{d['code']}" for d in json.loads(out)["diagnostics"] if d["severity"] == "error" and d["code"].startswith(SLOP_RULES)))


def hotspots(funcs):
    """{"file::name#n": complexity} for functions above the limit; #n keeps same-named ones apart."""
    seen, out = Counter(), {}
    for file, name, cc, _ in sorted(funcs, key=lambda f: -f[2]):
        if cc > CC_LIMIT:
            seen[(file, name)] += 1
            out[f"{file}::{name}#{seen[(file, name)]}"] = cc
    return out


def measure(root):
    funcs, hits = lizard(root), slop_hits(root)
    mass = [cc * math.sqrt(n) for _, _, cc, n in funcs]
    heavy = [m for m, f in zip(mass, funcs, strict=True) if f[2] > CC_LIMIT]
    nloc = sum(f[3] for f in funcs)
    m = {
        "erosion": sum(heavy) / sum(mass) if mass else 0.0,
        "complex_functions": len(heavy),
        "max_complexity": max((f[2] for f in funcs), default=0),
        "clone_ratio": clone_ratio(root),
        "hits_per_kloc": sum(hits.values()) / nloc * 1000 if nloc else 0.0,
    }
    return {k: round(v, 4) for k, v in m.items()}, hits, hotspots(funcs)


def base_tree(ref):
    d = tempfile.mkdtemp()
    run(["git", "worktree", "add", "--detach", "-f", d, ref], ROOT)
    return d


def baseline_at(ref):
    p = subprocess.run(["git", "show", f"{ref}:{BASELINE}"], cwd=ROOT, capture_output=True, text=True)
    return json.loads(p.stdout) if p.returncode == 0 else None


def grew(new, old):
    return {k: v for k, v in new.items() if v > old.get(k, 0)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base")
    ap.add_argument("--update", action="store_true")
    ap.add_argument("--report", default="slop-report.json")
    ap.add_argument("--summary")
    a = ap.parse_args()

    metrics, hits, spots = measure(ROOT)
    path = ROOT / BASELINE
    if a.update:
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps({"metrics": metrics, "hits": dict(sorted(hits.items())), "hotspots": dict(sorted(spots.items()))}, indent=2) + "\n")
        print(f"slop: wrote {BASELINE}")
        return
    if not path.exists():
        sys.exit(f"slop: {BASELINE} is missing; run with --update once")
    base = json.loads(path.read_text())
    errors = []

    for k, v in grew(hits, base["hits"]).items():
        errors.append(f"new anti-slop hits (limit {base['hits'].get(k, 0)}, found {v}): {k}")
    for k, v in grew(spots, base["hotspots"]).items():
        errors.append(f"function above complexity {CC_LIMIT} not in the baseline or more complex than it (limit {base['hotspots'].get(k, CC_LIMIT)}, found {v}): {k}")

    rows = [{"id": f"slop.{k}", "value": v, "threshold": base["metrics"][k], "baseline": base["metrics"][k], "pass": v <= base["metrics"][k]} for k, v in metrics.items()]
    if a.base:
        ref = subprocess.run(["git", "merge-base", a.base, "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip() or a.base
        old_baseline = baseline_at(ref)
        if old_baseline:
            for part in ("hits", "hotspots"):
                for k in grew(base[part], old_baseline[part]):
                    errors.append(f"the baseline may only shrink, but {part} grew: {k}")
        tree = base_tree(ref)
        try:
            ref_metrics = measure(tree)[0]
        finally:
            run(["git", "worktree", "remove", "--force", tree], ROOT)
        for r in rows:
            k = r["id"].removeprefix("slop.")
            r["threshold"] = ref_metrics[k]
            r["pass"] = r["value"] <= ref_metrics[k]
    for r in rows:
        if not r["pass"]:
            errors.append(f"{r['id']} {r['value']} is above {r['threshold']}")
    shrinkable = len(grew(base["hits"], hits)) + len(grew(base["hotspots"], spots))

    (ROOT / a.report).write_text(json.dumps({"dimension": "quality.slop", "rows": rows, "pass": not errors}, indent=2) + "\n")
    lines = ["### Slop metrics", "", "| metric | now | limit | |", "|---|---|---|---|"]
    lines += [f"| {r['id']} | {r['value']} | {r['threshold']} | {'ok' if r['pass'] else 'FAIL'} |" for r in rows]
    lines += ["", f"Baseline can shrink by {shrinkable} entries (`npm run slop -- --update`)." if shrinkable else "Baseline is tight."]
    lines += ["", *[f"- {e}" for e in errors]]
    print("\n".join(lines))
    if a.summary:
        Path(a.summary).write_text("\n".join(lines) + "\n")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    os.chdir(ROOT)
    main()
