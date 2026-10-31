---
id: 2026-10-25-adr-capture-bar-and-settings-window
title: 'Capture bar on ⌃⇧5, Settings as a window, Keyboard Shortcuts in its own file'
type: adr
status: accepted
created: 2026-10-25
supersedes: []
superseded_by: []
amended_by: [2026-10-26-adr-recording-key-frames]
amends: [2026-10-25-adr-keys-follow-macos]
tags: [ux, keys, menu, capture, settings]
---

# Capture bar on ⌃⇧5, Settings as a window, Keyboard Shortcuts in its own file

Accepted on 2026-10-25 with the plan of `changes/2026-10-25-finish-app` (milestone 2). The full spec is that change's `spec/capture-and-settings.md`. Decisions 3, 6 and 11 were amended on 2026-10-26 by the plan of `changes/2026-10-26-picked-designs`, whose spec is that change's `spec/`.

## Context

⌃⇧5 popped the Capture Options items as a menu at the menu bar icon, and the menu bar menu held them again as a submenu. The owner asked for it "more like this, with a menu on the screen", with macOS's own capture bar as the picture (A5), for "proper settings and everything" (A6), and for "the proper UI that we were promised" in the Keyboard Shortcuts window (A7).

## Decision

1. **⌃⇧5 opens the capture bar.** It replaces the popup menu, as macOS's ⇧⌘5 opens its bar. No new key; ⌃⇧4, ⌃⇧3 and ⌃⇧N do exactly what they did. This amends "Keys follow macOS" (its line "⌃⇧5 shows the capture options as a menu").
2. **The menu bar menu's Capture Options row opens the bar.** It becomes "Capture Options…" with ⌃⇧5 beside it, without a submenu. Choose New Area, Capture Window, Capture Scrolling and One-Shot live in the bar.
3. **Buttons choose what to capture; a Session | One-Shot segmented control chooses where it goes; Options choose how** (amended 2026-10-26, A6, A10). The segmented control sits in the bar's top row with the session pop-up, and replaces Options ▸ Save to, so a window or scrolling capture can be one-shot too. The Capture button reads "Capture One-Shot" while One-Shot is chosen, and is the bar's one blue button, with its ↩ keycap (A2, A3).
4. **Options apply only to captures from the bar.** ⌃⇧4 and ⌃⇧3 keep working as before, so a one-shot left on never steals a session capture.
5. **Timer and Show Mouse Pointer work for areas only.** `screencapture -C` draws the pointer only in non-interactive captures, and a timer needs the area first. Snapmark's own picker gives `-R`, so Choose New Area and Capture Last Area support both; Capture Window and Capture Scrolling grey them.
6. **Full Screen and Record join the bar; still no Clipboard target** (amended 2026-10-26, A6, Q8). The modes, in order and on keys 1–6: New Area, Window, Full Screen, Last Area, Scrolling, Record, matching the global digits. Full Screen takes every display, as ⌃⇧3. Record is decided in "Recording with key frames" (2026-10-26-adr-recording-key-frames).
7. **Settings is a window with General, Capture and Shortcuts tabs.** Every Settings submenu item moves in; the menu keeps one row, "Settings…" (⌘,).
8. **Keyboard Shortcuts stays its own window, in its own file `src/shortcuts.html`**, reached by ⌘/ from any Snapmark window and from Settings ▸ Shortcuts. It is a reference sheet kept open beside the editor, wide and two-column like the round-1 mock.
9. **Snapmark sets its own app menu**, the smallest one that gives ⌘, and ⌘/: About, Settings… ⌘,, Keyboard Shortcuts ⌘/, Services, Hide, Hide Others, Show All, Quit. File, Edit, View and Window stay Electron's stock roles.
10. **No beautify option in the bar.** The one-shot editor already remembers its last Beautify settings.
11. **The bar names each mode under its icon, with its key, and 1–6 pick a mode** (amended 2026-10-26, Q3, Q8). The drawn label above the bar (`tip.html`) goes: names and keys are on the bar itself (guide WIN-2). The bar becomes the key window while staying a non-activating panel, so its keys reach the bar and never the app behind (guide CAP-13). While it is open, Esc closes it from every app, even after a click elsewhere (A1, guide CAP-12, EX-7). A number only chooses, as a click does.

The bar is a non-activating panel at the bottom centre of the display with the pointer, over every Space and full-screen app, with the system's popover material. It closes, then waits for `closed` plus 200 ms, before any capture runs, so it is never in the screenshot. While it is open, or while its Timer counts, ⌃⇧1–⌃⇧4 and ⌃⇧N do nothing: one capture at a time.

## Rejected

- **A fifth button for One-Shot**, area only, as the old menu item: a window or scrolling one-shot would be impossible.
- **The bar's options for ⌃⇧4 and ⌃⇧3**, as macOS's ⇧⌘4 follows ⇧⌘5's: a one-shot or a timer left on would change the everyday keys without a sign.
- **Folding Keyboard Shortcuts into the Settings window**: the guidelines want it one key away (⌘/), and Settings is narrow and fixed.
- **Taking ⇧⌘5 itself**: as in "Keys follow macOS", it works only after the owner turns macOS's own key off.

## Consequences

- The menu bar menu loses two submenus and keeps its row count.
- A global Esc is held only while the bar is open or a countdown runs (amended 2026-10-26).
- The editor and session window show Snapmark's own menu in the Mac menu bar, with Settings… ⌘, and Keyboard Shortcuts ⌘/.

## Milestones

- fixes: changes/2026-10-25-finish-app (milestone 2)
- fixes: changes/2026-10-26-interaction-guide-polish (the bar's label and keys 1–4)
- fixes: changes/2026-10-26-picked-designs (milestone 1: decisions 3, 6 and 11; milestone 3: Record)

| Date       | Decision                                            | Answer (quoted)                                                          | By whom      |
| ---------- | --------------------------------------------------- | ------------------------------------------------------------------------ | ------------ |
| 2026-10-25 | Capture bar on ⌃⇧5, as macOS's own (A5)             | "Can we have it more like this, with a menu on the screen?"              | the owner    |
| 2026-10-25 | Settings as a window (A6)                           | "...so we can have proper settings and everything."                      | the owner    |
| 2026-10-25 | Keyboard Shortcuts as the round-1 design (A7)       | "I want the proper UI that we were promised"                             | the owner    |
| 2026-10-25 | The plan of changes/2026-10-25-finish-app           | approved                                                                 | Calvin Dudek |
| 2026-10-26 | One-Shot as a tab, not a menu (decision 3, A6)      | "I think overall there should be a tab though for one shot vs. session." | the owner    |
| 2026-10-26 | Blue Capture with its ↩ keycap (A3)                 | "Blue Capture + ↩ keycap"                                                | the owner    |
| 2026-10-26 | Bar digits match the global digits (decision 6, Q8) | "Yes, match (Recommended)"                                               | the owner    |
| 2026-10-26 | Retire the drawn label (decision 11, Q3)            | default, at the plan gate                                                | orchestrator |
| 2026-10-26 | The plan of changes/2026-10-26-picked-designs       | approved                                                                 | Calvin Dudek |
