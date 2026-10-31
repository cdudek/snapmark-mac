---
id: 2026-10-25-adr-keys-follow-macos
title: 'Keys follow macOS: ⌃⇧ plus the screenshot digits, Preview and Finder keys in the windows'
type: adr
status: accepted
created: 2026-10-25
supersedes: []
superseded_by: []
amended_by: [2026-10-25-adr-capture-bar-and-settings-window, 2026-10-26-adr-recording-key-frames]
tags: [ux, keys]
---

# Keys follow macOS

Amended on 2026-10-26 by the plan of `changes/2026-10-26-picked-designs`: the global keys below are the owner's list (A4), with One-Shot on ⌃⇧2. Keys while recording are in "Recording with key frames".

## Context

Snapmark captured with ⌃⇧1 and repeated the last area with ⌃⇧3. macOS uses ⇧⌘3 for the whole screen, ⇧⌘4 for an area and ⇧⌘5 for the screenshot options. The owner asked for "the shortcut mechanics close to what the default mac short cuts are" (2026-10-25). The interaction guidelines listed this as option (c) under Keyboard and focus.

## Decision

- Global keys keep macOS's digits and use ⌃⇧ for ⇧⌘, which macOS keeps for itself (amended 2026-10-26, A4):
  - ⌃⇧1 Capture New Area…: the area picker sets a new area and captures it (Q11).
  - ⌃⇧2 Capture One-Shot…: macOS's own overlay; drag an area, or Space for a window, and the editor opens in One-Shot (Q1).
  - ⌃⇧3 Capture Full Screen: every display at once, one screenshot and one editor each, as macOS's ⇧⌘3 (Q7).
  - ⌃⇧4 Capture Last Area: captures the area at once. With no area yet, or after a New Session, the picker comes first (Q2).
  - ⌃⇧5 opens the capture bar ("Capture bar on ⌃⇧5"). While a capture runs, it means Done or Cancel.
  - ⌃⇧N New Session, unchanged. It forgets the area.
- While a capture runs, ⌃⇧1–⌃⇧4 and ⌃⇧N do nothing: one capture at a time.
- The editor uses Preview's keys: ⌘S saves into the session (in one-shot mode it is Save As…), ⌘C copies the image when no text has the cursor, the arrow keys nudge the selected marks by 1 point (⇧ by 10), and ⌘A selects every mark.
- The session window uses Finder's keys: ↩ renames the session, ⌘⌫ moves the open screenshot to Discarded, ⌘O opens it in the editor again.
- Esc still closes the editor one step past Select; Discarded brings the screenshot back (owner, 2026-10-25).

## Rejected

- Taking ⇧⌘3, ⇧⌘4 and ⇧⌘5 themselves: it works only after the owner turns macOS's own keys off in System Settings. A later setting can offer it.
- ⌃ for "to the clipboard", as macOS does: Snapmark's chords would need four keys.
- Keeping ⌃⇧1 as a second capture key: two keys for one action. Since 2026-10-26 ⌃⇧1 sets a new area instead, as macOS's digits run 3, 4, 5 and the owner asked for 1 (A4).
- Leaving ⌃⇧4 on a fresh picker every time (2026-10-25): the owner asked ⌃⇧4 to repeat the area once one is set (A4).

## Consequences

- The owner re-learns one key, ⌃⇧1 to ⌃⇧4, once. Since 2026-10-26, ⌃⇧4 repeats the area and ⌃⇧3 takes the whole screen, as on macOS.
- ⌘A makes a multi-selection possible for the first time. It can be moved and removed as one step, but not resized or rotated.

## Milestones

- fixes: changes/2026-10-25-mac-shortcuts
- fixes: changes/2026-10-26-picked-designs (milestone 1, the keys as A4 lists them)

| Date       | Decision                                                     | Answer (quoted)                                                                                                                                                                                                      | By whom      |
| ---------- | ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| 2026-10-25 | Keys follow macOS, as proposed in chat on 2026-10-25         | "ok go"                                                                                                                                                                                                              | the owner    |
| 2026-10-26 | ⌃⇧1 New Area, ⌃⇧3 Full Screen, ⌃⇧4 Last Area, ⌃⇧5 as is (A4) | "Ctrl + Shift + 1 => Set new Area / Ctrl + Shift + 3 => full screen capture / Ctrl + Shift + 4 => if no area set / new session, set area first, if area set just capture selected area. / Ctrl + Shift + 5 => as is" | the owner    |
| 2026-10-26 | ⌃⇧2 Capture One-Shot… with macOS's overlay (Q1)              | "Drag an area, then One-Shot (Recommended)"                                                                                                                                                                          | the owner    |
| 2026-10-26 | ⌃⇧3 takes every display (Q7)                                 | "⌃⇧3 should just capture the full screen, like the mac."                                                                                                                                                             | the owner    |
| 2026-10-26 | The plan of changes/2026-10-26-picked-designs                | approved                                                                                                                                                                                                             | Calvin Dudek |
