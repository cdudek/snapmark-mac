---
id: 2026-10-26-adr-recording-key-frames
title: 'Recording with key frames: Record in the capture bar, a filmstrip for the agent and a GIF for people, 30 s at most'
type: adr
status: accepted
created: 2026-10-26
supersedes: []
superseded_by: []
amended_by: []
amends: [2026-10-25-adr-capture-bar-and-settings-window, 2026-10-25-adr-keys-follow-macos]
tags: [ux, capture, recording, keys, session, ai-handoff]
---

# Recording with key frames

Accepted on 2026-10-26 with the plan of `changes/2026-10-26-picked-designs` (milestone 3). The full spec is that change's `spec/`: the states in `interaction.md`, the screens and words in `screens.md`.

## Context

Snapmark took only still screenshots. Some bugs show only while something moves. The owner asked: "it would be nice if we could capture GIFs for animations", with "the frames per second for the GIF with a maximum of 15, down to 5, 4, or 2" and "a nice little countdown" (A6). In the review of the recording designs he chose "Filmstrip + GIF" and a "30 s cap" (A8), and asked for "keyframes only, I gues we can strip away images based on the identical hash or something? also when playing it keeps the timing?" (A11). An agent reads a few labelled frames well and an animated GIF badly; a person reads the GIF at once.

## Decision

1. **Record is the capture bar's sixth mode, on key 6.** It has no global key of its own. Options ▸ Frame Rate offers 15, 10, 5, 4 and 2 fps, 10 by default, remembered, and greyed unless Record is chosen.
2. **Record starts on the last area.** Capture opens the picker showing it: ↩ keeps it, a drag replaces it, Esc cancels. With no area, the plain picker opens (Q11).
3. **A 3-2-1 countdown comes first**, in an overlay on the area and as digits beside the menu bar icon, or from the Timer's value when that is longer. Esc, ⌃⇧5 or a click on the icon cancels it.
4. **A recording lasts 30 s at most** (A8). A small panel outside the area shows ⓧ, a red dot, the clock ("0:07 of 0:30 · 10 fps") and a blue Done. The clock turns amber at 25 s; at 30 s the recording ends as on Done.
5. **Keys while recording:** no plain key is taken, so the recorded app keeps ↩, Esc and every other key (Q9). Done is the Done button, ⌃⇧5 or a click on the menu bar icon. Cancel is ⓧ, and the recording goes to Discarded for 7 days. ⌃⇧1–⌃⇧4 and ⌃⇧N do nothing until it ends.
6. **Key frames:** the first frame, every changed frame and the settled last one, at most 24 (Q5). Identical frames go by hash; then a pixel difference on a downscaled copy decides, and above 24 the threshold rises until 24 remain. A frame with a mark is always a key frame, on top of the 24. "Finding key frames…" shows past 400 ms; after 15 s Snapmark opens the editor with evenly spaced frames.
7. **The editor marks the key frames.** They show as a grid, each labelled with its time in seconds. A mark belongs to the frame where it starts and is clipped to it. ⇧⌘F switches between key frames and all frames (Q12).
8. **The session gets two files per recording:** `img/NNN.png`, a filmstrip of the key and marked frames by time, each labelled, for the agent; and `img/NNN.gif` for people. The GIF has no marks, merges identical frames in a row into one with their delays summed, and plays at the real speed (A11).
9. **Edit Again works from the raw frames**, their times and the marks, kept in `.edit/NNN/frames/` and `.edit/NNN.json`. They expire with the entry's Discarded copy.
10. **One-Shot copies the marked filmstrip PNG**, "Copy Filmstrip"; the GIF is under Copy or Save (Q10).
11. **Frames come from `desktopCapturer` in a hidden page**, drawn to a canvas at the chosen rate and written to temp files at once. The GIF is written by macOS's ImageIO through JXA, as OCR uses Vision. No new dependency.

## Rejected

- **Repeated `screencapture -R`:** it cannot reach 10–15 fps.
- **The GIF alone:** an agent reads a 256-colour animation badly, and 30 s at 15 fps is 450 frames.
- **Every frame in the filmstrip:** near-identical frames bury the moment that matters (A11).
- **Plain ↩ and Esc to stop and cancel:** the recorded app would lose them while it is being shown (Q9).
- **No cap, or a longer one:** frame data grows fast; 30 s covers an animation or a short flow (A8).
- **Decoding the GIF for Edit Again:** it has 256 colours and merged frames.

## Consequences

- The bar has six modes; the guide's CAP-3 lists them, and REC-1 and REC-2 hold the key-frame and mark rules.
- Session folders grow: a 30 s recording keeps its raw frames in `.edit/`. If one is over 100 MB, non-key frames are stored as JPEG (plan risk, milestone 3).
- `session.md`, the session window and the PDF and ZIP exports list a recording as one entry with its filmstrip and GIF.

## Milestones

- fixes: changes/2026-10-26-picked-designs (milestone 3)

| Date       | Decision                                           | Answer (quoted)                                                                                                                    | By whom      |
| ---------- | -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| 2026-10-26 | Record GIFs, with a countdown and 15 to 2 fps (A6) | "it would be nice if we could capture GIFs for animations"                                                                         | the owner    |
| 2026-10-26 | Filmstrip plus GIF, 30 s cap (A8)                  | "Filmstrip + GIF (Recommended)"; "30 s cap (Recommended)"                                                                          | the owner    |
| 2026-10-26 | Key frames only, real timing (A11)                 | "keyframes only, I gues we can strip away images based on the identical hash or something? also when playing it keeps the timing?" | the owner    |
| 2026-10-26 | No plain key while recording (Q9)                  | "No, Done/⌃⇧5/menu icon (Recommended)"                                                                                             | the owner    |
| 2026-10-26 | One-Shot copies the marked filmstrip (Q10)         | "Marked filmstrip PNG (Recommended)"                                                                                               | the owner    |
| 2026-10-26 | The plan of changes/2026-10-26-picked-designs      | approved                                                                                                                           | Calvin Dudek |
