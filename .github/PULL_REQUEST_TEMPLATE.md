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

## Decision4

If this turns out to be wrong, what does it take to put right? Take the class from `boundary-map.yaml`; a change takes the class of its highest decision. When unsure, take the higher class. Fill the fields below; delete the lines and blocks that do not apply to your class. The `decision4` check reads them.

Decision-Class: <Undo | Repair | Migrate | Answer>
Put-right: <Repair and above: what it takes to put this right>
Answerer: <Migrate and Answer: who answers for it>
Class-Change: <only if lowered: `<from> -> <to>; lowered by <who>; <why>`>

**Choice story (Repair)**

- Chose:
- Over:
- Because:
- Commits us to:

**Options (Migrate)**

- Option 1:
- Option 2:
- Or one option stated as forced, with the constraint that forces it:

**Evidence and challenges (Answer)**

- Observed / inferred / asked / unknown:
- Challenges:
- No recommendation.
