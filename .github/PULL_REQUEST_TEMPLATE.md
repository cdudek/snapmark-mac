<!--
Decision4 writing rules:
- Source: Habitat Thinking Decision4 v1.0.1, pinned at 4429f821780655f253a954b2659bf38e7b9d5517.
- Read boundary-map.yaml; use the highest decision class, at or above its floor. Unmapped or unsure: higher class and log a map gap.
- Select exactly one bold class with its one colour circle: 🟢 Undo, 🟡 Repair, 🟠 Migrate, 🔴 Answer.
- Explain who has to put it right and what it takes. Do not invent recovery steps, backups or preserved work.
- Repair and above need Recovery steps as a standalone bold line and a top-level numbered list. Undo may omit them.
- Responsible for recovery is a role; at Answer it must be a named person or @handle.
- Classification change is None unless changed; record from -> to, who raised/lowered it and why. Never lower silently.
- Keep Decision record at Repair (Chose / Over / Because / Commits us to), Migrate (Options: at least two real options, or one Forced with its Constraint), Answer (labelled Evidence and Challenges; no recommendation). Omit it at Undo.
- At Answer label every evidence item observed / inferred / asked / unknown. A person with standing writes the decision.
- Unattended runs close only Undo; above Undo hand back and stop unless the owner has explicitly authorized the work.
- Preserve repo-specific human checklists and use H2 headings throughout.
-->
## What

<one or two sentences: what changes for the user or the system>

Fixes <LINEAR-ID>

## Which requirements this satisfies

> One row per requirement from `changes/<id>/facts.md`, or from the issue when there is no change
> folder. A requirement with no proof is not done, and a proof with no requirement is scope creep.

| Requirement | Proof                          |
| ----------- | ------------------------------ |
| F1          | `<test file> › <test name>`    |
| F2          | manual: <who checked, and how> |

## Verification

- [ ] `<verify command>` exits 0
- [ ] Every `F`/`N` above has a proof in the table
- [ ] No `[NEEDS CLARIFICATION]` marker is left in the change folder or the issue

## Out of scope

- <what this PR deliberately does not do>

## How hard is it to undo this PR after merging?

**🟡 Repair** — <who has to put it right and what it takes, concrete>

**Recovery steps**

1. <first step>
2. <next step>

- **Responsible for recovery:** <role; at Answer a named person>
- **Classification change:** None

## Decision record

- **Chose:** <what was decided>
- **Over:** <viable alternative>
- **Because:** <reason>
- **Commits us to:** <what this ties the team to>

<details>
<summary>Recovery levels</summary>

Undo — a revert puts it right
Repair — real work, contained to this team
Migrate — coordinated change involving other people
Answer — someone outside the team with standing to ask is affected, and nothing unmakes it

</details>
