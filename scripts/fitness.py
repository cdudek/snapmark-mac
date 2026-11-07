#!/usr/bin/env python3
"""Fitness functions that read architecture.yaml (STR-3, CI-23).

  python3 scripts/fitness.py arch   [--base REF] [--root DIR]   boundaries, cycles, score
  python3 scripts/fitness.py perf                               bundle budgets (run `npm run build` first)
  python3 scripts/fitness.py all                                every dimension, writes fitness-report.json

Needs PyYAML. `arch` parses imports and <script src> tags, so it needs no build and no node_modules.
"""

import argparse
import fnmatch
import gzip
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCH_BASELINE = ".fitness/arch-baseline.json"
SCORE_FLOOR = 90
IMPORT = re.compile(r"""(?:\bfrom\s*|\bimport\s*\(?\s*|\brequire\s*\(\s*)['"]([^'"]+)['"]""")
SCRIPT_SRC = re.compile(r"""<script[^>]*\ssrc=["']([^"']+)["']""")
RESOLVE = ["", ".ts", ".d.ts", ".html", ".css", "/index.ts"]


def load_arch():
    import yaml

    return yaml.safe_load((ROOT / "architecture.yaml").read_text())


def specs_of(file, text):
    return SCRIPT_SRC.findall(text) if file.endswith(".html") else IMPORT.findall(text)


def package_of(spec):
    parts = spec.removeprefix("node:").split("/")
    return "/".join(parts[:2]) if spec.startswith("@") else parts[0]


def analyse(tree, arch):
    """Return (violations, cross_module_edges, violating_edges, module_graph) for the files under tree."""
    mods = {m["name"]: m for m in [*arch["modules"], *arch["shared"]]}
    owner = {}
    for m in mods.values():
        for p in m["paths"]:
            owner[p] = m["name"]
    scan = Path(tree) / arch["scan"]
    files = sorted(p.relative_to(tree).as_posix() for p in scan.rglob("*") if p.suffix in (".ts", ".html") and p.is_file())
    violations, edges, bad, graph = [], set(), set(), {n: set() for n in mods}
    for f in files:
        if f not in owner:
            violations.append(f"unowned: {f} belongs to no module in architecture.yaml")
            continue
        me = mods[owner[f]]
        for spec in specs_of(f, (Path(tree) / f).read_text()):
            if spec.startswith(".") or (f.endswith(".html") and "://" not in spec):
                # <script src="x.js"> points at the compiled file; the source is x.ts
                base = _norm((Path(f).parent / re.sub(r"\.js$", "", spec)).as_posix())
                if "node_modules/" in base:
                    spec = base.split("node_modules/")[-1]  # a package loaded by a <script> tag
                else:
                    target = next((base + e for e in RESOLVE if (Path(tree) / (base + e)).is_file()), None)
                    if target is None or target not in owner:
                        violations.append(f"unresolved: {f} imports {spec}")
                        continue
                    other = mods[owner[target]]
                    if other["name"] == me["name"]:
                        continue
                    edges.add((f, target))
                    graph[me["name"]].add(other["name"])
                    if other["name"] not in me.get("may_depend_on", []):
                        violations.append(f"undeclared: {me['name']} -> {other['name']} ({f} imports {spec})")
                        bad.add((f, target))
                    elif other.get("door") != target:
                        violations.append(f"door: {f} imports {target}, but {other['name']}'s door is {other['door']}")
                        bad.add((f, target))
                    continue
            allowed = me.get("external")
            pkg = package_of(spec)
            if allowed is not None and not any(pkg == a or pkg.startswith(a + "/") for a in allowed):
                violations.append(f"external: {me['name']} uses {pkg} ({f}), allowed {allowed}")
    return sorted(set(violations)), len(edges), len(bad), graph


def _norm(p):
    out = []
    for part in p.split("/"):
        if part == "..":
            out.pop()
        elif part != ".":
            out.append(part)
    return "/".join(out)


def cycles(graph):
    found, state = [], {}

    def visit(n, stack):
        state[n] = 1
        for m in sorted(graph[n]):
            if state.get(m) == 1:
                found.append(" -> ".join([*stack[stack.index(m) :], n, m]) if m in stack else f"{n} -> {m}")
            elif m not in state:
                visit(m, [*stack, n])
        state[n] = 2

    for n in sorted(graph):
        if n not in state:
            visit(n, [])
    return found


def score(edges, bad):
    return round(100 * (1 - bad / edges), 2) if edges else 100.0


def arch(base, root):
    spec = load_arch()
    violations, edges, bad, graph = analyse(root or ROOT, spec)
    loops = cycles(graph)
    allowed = set(json.loads((ROOT / ARCH_BASELINE).read_text())["violations"]) if (ROOT / ARCH_BASELINE).exists() else set()
    new = [v for v in violations if v not in allowed]
    now = score(edges, bad)
    floor = SCORE_FLOOR
    if base:
        ref = subprocess.run(["git", "merge-base", base, "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip() or base
        tree = tempfile.mkdtemp()
        subprocess.run(["git", "worktree", "add", "--detach", "-f", tree, ref], cwd=ROOT, check=True, capture_output=True)
        try:
            floor = max(floor, score(*analyse(tree, spec)[1:3]))
        finally:
            subprocess.run(["git", "worktree", "remove", "--force", tree], cwd=ROOT, check=True, capture_output=True)
    rows = [
        {"id": "arch.boundaries", "value": len(new), "threshold": 0, "baseline": len(allowed), "pass": not new},
        {"id": "arch.cycles", "value": len(loops), "threshold": 0, "baseline": 0, "pass": not loops},
        {"id": "arch.score", "value": now, "threshold": floor, "baseline": 100.0, "pass": now >= floor},
    ]
    for line in [*new, *(f"cycle: {c}" for c in loops)]:
        print(f"  {line}")
    return rows


def perf():
    budgets = next(f for f in load_arch()["fitness"] if f["id"] == "perf.bundle")["budgets"]
    rows = []
    for b in budgets:
        files = [p for p in ROOT.glob(b["files"]) if p.is_file()]
        size = sum(len(gzip.compress(p.read_bytes(), 9)) for p in files)
        if not files:
            sys.exit(f"perf: {b['files']} matches nothing; run `npm run build` first")
        rows.append({"id": f"perf.bundle[{b['name']}]", "value": size, "threshold": b["max_gzip"], "baseline": b["max_gzip"], "pass": size <= b["max_gzip"]})
    print("perf.web: not applicable (the product has no web pages)")
    return rows


def slop():
    p = subprocess.run([sys.executable, str(ROOT / "scripts/slop.py"), "--base", "origin/main", "--report", "slop-report.json"], cwd=ROOT, capture_output=True, text=True)
    return json.loads((ROOT / "slop-report.json").read_text())["rows"] if (ROOT / "slop-report.json").exists() else [{"id": "slop", "value": p.returncode, "threshold": 0, "baseline": 0, "pass": False}]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dimension", choices=["arch", "perf", "all"])
    ap.add_argument("--base")
    ap.add_argument("--root")
    ap.add_argument("--report", default="fitness-report.json")
    a = ap.parse_args()
    rows = []
    if a.dimension in ("arch", "all"):
        rows += arch(a.base or ("origin/main" if a.dimension == "all" else None), a.root)
    if a.dimension in ("perf", "all"):
        rows += perf()
    if a.dimension == "all":
        rows += slop()
        print("decision4: runs in CI against the PR body, not locally")
    for r in rows:
        print(f"{'ok  ' if r['pass'] else 'FAIL'} {r['id']}: {r['value']} (limit {r['threshold']})")
    (ROOT / a.report).write_text(json.dumps({"rows": rows, "pass": all(r["pass"] for r in rows)}, indent=2) + "\n")
    sys.exit(0 if all(r["pass"] for r in rows) else 1)


if __name__ == "__main__":
    main()
