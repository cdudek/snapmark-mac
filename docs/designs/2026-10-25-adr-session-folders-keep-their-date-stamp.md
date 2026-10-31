---
id: 2026-10-25-adr-session-folders-keep-their-date-stamp
title: 'Session folders keep their date stamp; screens show a readable name'
type: adr
status: accepted
created: 2026-10-25
supersedes: []
superseded_by: []
amended_by: []
tags: [ux, sessions, menu]
---

# Session folders keep their date stamp; screens show a readable name

Accepted on 2026-10-25 with the plan of `changes/2026-10-25-session-names`.

## Context

A session is a folder under the sessions folder. Snapmark names a new one after its start, `2026-10-24 23.38`. Screens showed that name three ways: "24 Oct 23.38" in the menu, the raw folder name in the session window and editor, and a rename replaced the whole folder name, so the date was gone. The owner asked for a year-first date that reads well, and for a rename to keep the date (2026-10-25).

## Decision

1. **The folder name stays the one source.** No metadata file, no rename of existing folders.
2. **A new session's folder is `2026-10-24 23.38`**, as today.
3. **Rename keeps the stamp:** renaming it to "Ledgerly Q4 review" gives the folder `2026-10-24 23.38 Ledgerly Q4 review`. Sorting folders by name still sorts by date.
4. **Rename never changes the stamp.** The stamp is `YYYY-MM-DD HH.MM` with its same-minute suffix ` (2)` when there is one, so `2026-10-24 23.38 (2)` renamed becomes `2026-10-24 23.38 (2) Ledgerly Q4 review`. Typed text that starts with a date is part of the name. An empty name on a stamped session gives the date-only session back.
5. **Screens show the display name:** `2026-10-24, 23:38` for an unnamed session, `2026-10-24 · Ledgerly Q4 review` for a named one, `2026-10-24, 23:38 (2)` for a same-minute twin.
6. **A folder with no stamp** (renamed before this change) shows its folder name, with no date. A folder date is not used: syncing through iCloud Drive or Google Drive resets it, and a wrong date is worse than none.
7. **File names keep the folder name:** Save As…, PDF and ZIP. `session.md`'s first line is the display name (F19). macOS shows a colon in a file name as "/", so "23:38" never goes into one. The PDF's rendered first heading shows the display name.

## Rejected

- **Name in a sidecar file, folder untouched:** Finder, the copied path and the AI prompt would show only the stamp, and a second file can drift from the folder.
- **Folder date (birthtime) for stamp-less folders:** wrong after a sync.
- **Bulk-renaming old folders to add a stamp:** touches the owner's real sessions without a request.
- **Colon in folder names:** Finder shows it as "/".

## Consequences

- `sessions.shortName()` becomes the display rule for every screen; every caller changes at once.
- Two sessions of one day given the same name read the same in the menu ("2026-10-24 · Ledgerly Q4 review"); their folders differ by time. Accepted: rare, and the owner chose the names.
- The glossary proposal's "28 Sep 14:32" row and the guideline proposal's "twenty recent sessions plus Other Session…" are stale; the next `omr-ux:guidelines` round takes this ADR.

| Date       | Decision                                                                                                | Answer (quoted)                                                      | By whom   |
| ---------- | ------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | --------- |
| 2026-10-25 | Date format "2026-10-24, 23:38"                                                                         | intent.md, Decisions at confirmation 1                               | the owner |
| 2026-10-25 | Renaming keeps the timestamp                                                                            | "Write down that renaming a session would still keep the timestamp." | the owner |
| 2026-10-25 | Folder form `<stamp> <name>`, stamp-less folders show no date, `session.md` heading is the display name | plan approved at the gate of changes/2026-10-25-session-names        | the owner |
