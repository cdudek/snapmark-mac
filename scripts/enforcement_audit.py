#!/usr/bin/env python3
"""Enforcement audit (CI-30, CI-31): does every rule that claims a check actually run it?

  python3 scripts/enforcement_audit.py [--spec F] [--workflow F] [--root DIR] [--offline] [--summary F] [--issue]

Reads the `enforcement` row of every fitness id in architecture.yaml and reports four states per row:
  installed   every tool in `tools` resolves (a node_modules/ path must exist, anything else must be on PATH)
  configured  every file in `config` exists
  executed    `job` exists in the workflow and, for a required row, is `check` itself or feeds the `check` summary job
  passed      the job's last run on the default branch succeeded (gh api); `unknown` without gh or a token
Plus once: does the branch ruleset require `check` (`unknown` without access).
A gap is a required row with a "no" in any state, or a ruleset that does not require `check`. Exit 1 on a gap.
--issue opens or updates one issue with the gaps and closes it when there are none (the monthly workflow).
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ISSUE_TITLE = "Enforcement audit: gaps"


def gh(*args):
    p = subprocess.run(["gh", *args], capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else None


def last_jobs(repo, workflow):
    """{job name: conclusion} of the last completed run of the workflow on the default branch, or None."""
    runs = gh("api", f"repos/{repo}/actions/workflows/{Path(workflow).name}/runs?branch=main&status=completed&per_page=1")
    if not runs or not json.loads(runs)["workflow_runs"]:
        return None
    run_id = json.loads(runs)["workflow_runs"][0]["id"]
    jobs = gh("api", f"repos/{repo}/actions/runs/{run_id}/jobs?per_page=100")
    return {j["name"]: j["conclusion"] for j in json.loads(jobs)["jobs"]} if jobs else None


def ruleset_requires(repo, context):
    out = gh("api", f"repos/{repo}/rules/branches/main")
    if out is None:
        return "unknown"
    contexts = [c["context"] for r in json.loads(out) if r["type"] == "required_status_checks" for c in r["parameters"]["required_status_checks"]]
    return "yes" if context in contexts else "no"


def yes_no(ok):
    return "yes" if ok else "no"


def audit(spec, workflow, root, offline):
    jobs = workflow["jobs"]
    summary = jobs.get("check", {}).get("needs", [])
    repo = os.environ.get("GITHUB_REPOSITORY") or (gh("repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner") or "").strip()
    last = None if offline or not repo else last_jobs(repo, "ci.yml")
    rows = []
    for f in spec["fitness"]:
        e = f.get("enforcement")
        if not e:
            continue
        job = e.get("job")
        name = jobs.get(job, {}).get("name", job) if job else None
        row = {
            "id": f["id"],
            "required": bool(e.get("required", True)),
            "installed": yes_no(all((root / t).exists() if t.startswith("node_modules/") else shutil.which(t) for t in e.get("tools", []))),
            "configured": yes_no(all((root / c).exists() for c in e.get("config", []))),
            "executed": yes_no(job in jobs and (job == "check" or job in summary or not e.get("required", True))),
            "passed": "unknown" if last is None or name not in last else yes_no(last[name] in ("success", "skipped")),
        }
        rows.append(row)
    ruleset = "unknown" if offline or not repo else ruleset_requires(repo, "check")
    return rows, ruleset


def gaps_of(rows, ruleset):
    out = [f"{r['id']}: {k} = no" for r in rows if r["required"] for k in ("installed", "configured", "executed", "passed") if r[k] == "no"]
    return out + (["the branch ruleset does not require the `check` summary job"] if ruleset == "no" else [])


def report(rows, ruleset, gaps):
    lines = ["### Enforcement audit", "", "| row | required | installed | configured | executed | passed |", "|---|---|---|---|---|---|"]
    lines += [f"| {r['id']} | {yes_no(r['required'])} | {r['installed']} | {r['configured']} | {r['executed']} | {r['passed']} |" for r in rows]
    lines += ["", f"Ruleset requires `check`: {ruleset}", "", *(f"- gap: {g}" for g in gaps)] if gaps else ["", f"Ruleset requires `check`: {ruleset}", "", "No gaps."]
    return "\n".join(lines)


def sync_issue(gaps, body):
    found = json.loads(gh("issue", "list", "--state", "open", "--search", f'"{ISSUE_TITLE}" in:title', "--json", "number,title") or "[]")
    number = next((i["number"] for i in found if i["title"] == ISSUE_TITLE), None)
    if gaps and number:
        gh("issue", "edit", str(number), "--body", body)
    elif gaps:
        gh("issue", "create", "--title", ISSUE_TITLE, "--body", body)
    elif number:
        gh("issue", "close", str(number), "--comment", "The monthly audit found no gaps.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec")
    ap.add_argument("--workflow")
    ap.add_argument("--root")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--summary")
    ap.add_argument("--issue", action="store_true")
    a = ap.parse_args()
    root = Path(a.root).resolve() if a.root else ROOT
    spec = yaml.safe_load(Path(a.spec or root / "architecture.yaml").read_text())
    workflow = yaml.safe_load(Path(a.workflow or root / ".github/workflows/ci.yml").read_text())
    rows, ruleset = audit(spec, workflow, root, a.offline)
    gaps = gaps_of(rows, ruleset)
    text = report(rows, ruleset, gaps)
    print(text)
    if a.summary:
        Path(a.summary).write_text(text + "\n")
    if a.issue:
        sync_issue(gaps, text)
    sys.exit(1 if gaps else 0)


if __name__ == "__main__":
    main()
