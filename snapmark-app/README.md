<p align="center"><img src="assets/app-icon.svg" width="128" alt="Snapmark icon"></p>

<h1 align="center">Snapmark</h1>

<p align="center">Screenshot, mark it up, and collect it in one Markdown file you can hand to an AI.</p>

---

## What it is for

When you review a UI with an AI agent (Claude Code, Cursor, Codex), you spend a lot of words describing _where_ something is: "the second button in the header, the one next to…". A picture with a numbered reference says it faster and more precisely.

Snapmark is a macOS menu bar app for exactly that loop:

1. Press `⌃⇧4`, drag over the part of the screen you mean.
2. Mark it: a box, an arrow, a cross for "remove this", a freehand pen, references ① ② with a note each.
3. Press `⌘↵`. The annotated image and your notes are appended to the current session's `session.md`.
4. Point your agent at the session folder: _"Work through `~/Documents/Snapmark/2026-09-25 14.02/session.md`"_.

### Why it is token-efficient

- **Crops, not full screens.** You capture only the region that matters. Models shrink large images (Claude to about 1.15 megapixels), so on a full-screen capture small UI text becomes unreadable; on a crop it stays sharp, and the model does not spend attention on the rest of the screen.
- **Saved at the size the model uses.** Retina captures are 2× pixels. Snapmark stores every image within 1568 px on the long edge and about 1.15 megapixels, the limits above which Claude resizes anyway. Nothing is lost for the model, and uploads and sessions stay small.
- **Numbers instead of descriptions.** Note 2 refers to marker ② on the image. The model does not have to guess which element you mean, and you do not have to describe it.
- **One plain Markdown file per session.** No app, no account, no export step. Any agent that reads files can read it, and it diffs cleanly in git.

A session looks like this:

```markdown
# 2026-09-25 14.02

## 001 · 14:03

![Screenshot 1](img/001.png)

Checkout page on mobile width.

1. Button label is cut off, should wrap
2. Remove this promo banner entirely
```

## Install

1. Download the DMG for your Mac from the update bucket, `https://storage.googleapis.com/snapmark-updates/mac/Snapmark-<version>-<arch>.dmg`: `arm64` for Apple Silicon (M1 and later), `x64` for Intel. The newest `<version>` is in [latest-mac.yml](https://storage.googleapis.com/snapmark-updates/mac/latest-mac.yml).
2. Open it and drag **Snapmark** onto **Applications**.
3. First launch: the app is not yet signed with an Apple Developer ID, so macOS blocks it. Open **System Settings → Privacy & Security** and click **Open Anyway** under the Snapmark message.
4. On the first capture macOS asks for **Screen Recording** permission. Grant it, then quit Snapmark from the menu bar and start it again. Without it, captures show only the wallpaper.

Snapmark lives in the menu bar as the corner-and-dot icon. It shows a Dock icon only while an editor is open.

## Use

| Shortcut | Anywhere                                                                                  |
| -------- | ----------------------------------------------------------------------------------------- |
| `⌃⇧1`    | Capture New Area: drag an area, capture it, and keep it for `⌃⇧4`                         |
| `⌃⇧2`    | Capture One-Shot: macOS's own capture overlay, into a one-shot editor, not into a session |
| `⌃⇧3`    | Capture Full Screen: every display at once, one screenshot each                           |
| `⌃⇧4`    | Capture Last Area: the kept area at once (the first time, drag the area)                  |
| `⌃⇧5`    | Open the capture bar                                                                      |
| `⌃⇧N`    | Start a new session (it also forgets the area)                                            |

The digits are macOS's own: `⇧⌘1` to `⇧⌘5` with `⌃` in place of `⌘`, which macOS keeps for itself.

In the editor, press a key to pick a tool. Press the same key again to cycle its tools; the top bar shows which one is active.

The toolbar shows one icon per key: the tool that is on, with its key underneath. The colour swatch beside the tools sets the colour of the next marks: ten presets, or **Custom…** for the macOS colour panel (Remove marks are always coral red, highlights yellow). The right side shows where the screenshot goes: **Session** | **One-Shot** (⇧⌘O), then the session pop-up "<session> (<n>)" (⇧⌘P), which moves this screenshot to a recent session, **Older Sessions…** or **New Session**. Dots under a key mean it holds more than one tool (the filled dot is the one that is on): press the key again for the next, and the icon changes with it. Hover an icon for its name.

| Key             | Tools                                                                                           |
| --------------- | ----------------------------------------------------------------------------------------------- |
| `C`             | Select: move, resize or delete (`⌫`) any mark                                                   |
| `1`             | Reference (a numbered diamond): click, then type its note in the panel → Card: a speech bubble  |
| `2`             | Box → Ellipse                                                                                   |
| `3`             | Arrow                                                                                           |
| `4`             | Pen (freehand)                                                                                  |
| `5`             | Cross → Remove area (hatched), always coral red                                                 |
| `6`             | Highlighter → Spotlight (dims the rest)                                                         |
| `7`             | Cut & move: drag around an element, then drag it where it should go → Redact (pixelates)        |
| `Esc`           | Step back: out of the text, then deselect, then back to Select, then close                      |
| `←` `↑` `→` `↓` | Nudge the selected marks 1 point; with `⇧`, 10 points                                           |
| `⌘A`            | Select every mark except redactions, to move or delete them together                            |
| `⌘1`–`⌘7`       | Pick a tool, also while typing a note or card (there the plain digit types)                     |
| `⌘Z`            | Undo: in a note, its typing first, then the marks (a reference placed by mistake goes at once)  |
| `⇧⌘Z`           | Redo                                                                                            |
| `⌘S` / `⌘↵`     | Add to Session; in Edit Again, Save Changes (in One-Shot, `⌘S` is Save As… and `⌘↵` Copy Image) |
| `⇧⌘O`           | Switch between Session and One-Shot, in the same window: the marks, notes and undo stay         |
| `⇧⌘P`           | Open the session pop-up, to move this screenshot to another session                             |
| `⇧⌘C`           | Copy Image: the marked-up image to the clipboard, without adding it to the session              |
| `⇧⌘S`           | Save As…: the marked-up image as a PNG wherever you pick, without adding it to the session      |
| `⌘W`            | Discard the screenshot (kept 7 days: **Reopen Last Discarded** in the menu)                     |
| `⌘C`            | Copy Image, when no text has the cursor; in One-Shot it also closes the editor                  |

The side panel starts with a one-line comment field. References appear there once you add the first one, and every field grows with its text. The comment and reference notes take Markdown as you type, like Notion: `# ` makes a heading, `- ` a list, `**bold**` bold; `session.md` keeps it as Markdown. **Keyboard Shortcuts** (⌘/ in any Snapmark window, or **Show All Shortcuts** in the Settings window) lists all of this in the app, other keys on the left and the editor tools on the right; Esc closes it. While an editor is open, Snapmark shows its icon in the Dock.

**Cards** are yellow speech bubbles: click to place one and start typing. To point at something, press on it and release where the card should sit; the bubble's tail turns toward it and a line follows the card wherever you move it. **Cut & move** leaves a dashed outline where the element is now and draws an arrow to where you dropped it. Cards and moves are also written into `session.md`, so an agent reads them as text.

**Auto-redact.** When a screenshot opens in the editor, Snapmark reads its text and pixelates email addresses, API keys and tokens (`sk-…`, `ghp_…`, `github_pat_…`, `xoxb-…`, `AKIA…`, JWTs, other long random strings), private key headers, card numbers and IBANs, with the same Redact marks you draw yourself. The side panel says _Redacted 2 sensitive items · ⌘Z to undo_; one ⌘Z takes them all back, and a single mark can be selected and deleted. Add to Session, Copy Image and Save As… wait for it, so none of it leaves your Mac. The text it reads is used only to find these; it is never written to `session.md`. Edit Again does not redact a screenshot a second time. Text recognition runs on your Mac; nothing is uploaded.

**Copy Image** (⇧⌘C) and **Save As…** (⇧⌘S), beside Undo and Redo, take the marked-up image out without adding it to the session: to the clipboard, or to a PNG wherever you pick (the name follows the entry it would become, for example `Ledgerly Q4 review 013.png`). It is the exact image **Add to Session** saves, within the AI's size limits. Outside a note, plain ⌘C copies the image too. Inside a note, ⌘C copies the text and ⇧⌘C still copies the image. **Add to Session** stays the main action.

Click the menu bar icon for the menu. It is built fresh each time it opens, and every item has an icon:

- **Adding screenshots to** shows the current session and how many screenshots it holds.
- **Capture Last Area** (⌃⇧4) captures the same part of the screen each time, for example the page in your browser. The first time, or after a New Session, the screen dims and you drag the area; after that every press captures it at once and opens the editor. Snapmark remembers the area after a restart, and asks again if the display it was on is gone. A shortcut another app already owns shows as "(shortcut unavailable)".
- **Capture New Area…** (⌃⇧1) lets you drag a new area, captures it, and keeps it for ⌃⇧4.
- **Capture Full Screen** (⌃⇧3) captures every display at once, one screenshot each, like macOS's ⇧⌘3.
- **Capture One-Shot…** (⌃⇧2) opens macOS's own capture overlay (Space picks a window); the capture opens in a one-shot editor and is not added to a session.
- **Capture Options…** (⌃⇧5) opens the capture bar at the bottom of the screen with the pointer, like macOS's ⇧⌘5, over any app and full-screen apps too. It is one row, left to right: Close (Esc), the modes **New Area** (1), **Window** (2), **Full Screen** (3), **Last Area** (4) and **Scrolling** (5), the destination, **Options** (⌥O) and the blue **Capture**. The destination reads **To** and the current session's name, or **One-Shot**; it opens a pop-up (⇧⌘P) with One-Shot first, then the sessions and New Session, and ⇧⌘O switches between One-Shot and the last session. Capture follows the mode (**Start Scrolling** for Scrolling) and reads **Capture One-Shot** while One-Shot is chosen. Rest the pointer on a control, or Tab to it, and the bar shows its name and key. Click a mode, press its digit, or press ← and →, to choose it; ↩ or ⌘↩ captures, and the bar is gone before the capture starts. Esc closes it, also from another app while the bar is open. **Options** opens a menu: **Timer** None, 3, 5 or 10 Seconds, and **Show Mouse Pointer**; both work for areas and the full screen. The bar opens on what you used last. Its options apply only to captures from the bar: the global keys stay as they are.
  - With a **Timer**, a countdown shows over the area (or in the middle of the display for Full Screen), and the seconds count beside the menu bar icon. It is never in the screenshot. Esc, ⌃⇧5 or a click on the menu bar icon cancels it: nothing is captured.
  - **Capture Window** captures one window: the pointer becomes a camera, click the window, and it opens in the editor cropped to the window's edges, without the shadow macOS draws around it. Esc cancels.
  - **Capture Scrolling** takes a page taller than the screen in one screenshot. The screen dims and you drag over the part that scrolls, for example a browser's page. Then scroll it down at your own pace: a small bar under the area counts the frames and the height so far. Press **Done** (↩) to open the stitched screenshot in the editor, or **Cancel** (Esc). The editor fits a tall screenshot to the window's width and scrolls. Snapmark stitches by matching each new view against the last one, keeps a sticky header and footer once, and stops at 20,000 px. Like every screenshot it is saved within the AI's size limits (1568 px on the long edge), so a page much taller than two screens arrives narrow and hard for the model to read. Scroll down only and not too fast: if a step goes further than the area's height, the bar says so, and scrolling back up a little picks up again. Content that moves by itself (animations, video, carousels), lazy-loaded images that appear late, and sideways scrolling come out wrong. There is no direct shortcut, on purpose: it is not the everyday capture.
  - **One-Shot** (the bar's **Session** | **One-Shot**, or ⌃⇧2) is the second mode, for an image that goes to people rather than an AI, for example into slides. Capture as usual, with any mode; the editor opens with the same tools, but the side panel shows **Beautify** instead of the comment and References: **Padding**, **Rounded corners** and **Shadow** sliders, a **Background** (the logo's gradient, pink, violet, teal, amber, graphite, a soft light gradient, white, **None** for transparent, or a custom colour, with a hex field beside **Custom**), and a **Ratio** for the whole image (Auto, 4:3, 3:2, 16:9, 1:1; the screenshot stays centred and the padding grows to fill). The canvas shows the result as you change it. **Copy Image** (⌘C, or ⇧⌘C) is the main button, and **Save As…** (⌘S or ⇧⌘S) suggests `Snapmark 2026-10-25 14.03.12.png`; both give the beautified image at full Retina resolution, not the AI size. There is no Add to Session, and nothing is written to a session. **Copy Image** also closes the editor; the capture stays in Discarded for 7 days as "Copied One-Shot". Closing it (Discard, ⌘W, Esc) keeps it in Discarded like any screenshot, and it reopens in one-shot mode. The editor's **Session** | **One-Shot** (⇧⌘O) switches live, in the same window, with the marks and undo kept; when the screenshot has notes, One-Shot says "Notes stay with Session. They are not copied." Snapmark remembers the last settings for the next one-shot.
- **Open Current Session** opens the session in Snapmark's own window, at 90 % of the screen the first time and then at the size you last gave it. Its header shows the session's name and how many screenshots it has; click the name (or the pencil), or press ↩, to rename it in place: ↩ saves, Esc cancels, and a name that is taken says so under the field. **Document** shows `session.md` with its screenshots inline, and you edit it in place, like Notion. **Screenshots** is a grid of every screenshot with its heading and note count; hover one for **Edit Again**, which reopens it in the editor with its marks and text (**Save Changes** replaces it in place), and **…** ▸ **Remove from Session**. Click a thumbnail to see it large: ← and → flip through them, Esc or **‹ All Screenshots** goes back to the grid. There, ⌘O is **Edit Again** and ⌘⌫ is **Remove from Session**; ⌘Z puts the last removed screenshot back. **Discarded** (shown when there is something) lists this session's screenshots closed without saving or removed in the last 7 days, each with **Reopen**. **Open in Markdown App** opens `session.md` in your default app.
- **Copy Prompt for AI** puts a ready instruction on the clipboard: the path to `session.md` plus what the marks mean. Paste it into Claude Code or any agent.
- **Session** ▸ everything else about sessions, under the current one's name:
  - **New Session** (⌃⇧N) starts a new session; while the current one is still empty, it keeps using that one.
  - **Switch Session** ▸ lists the 10 most recently used sessions, the current one always among them; click one to make it current. **Older Sessions…** (shown when there are more) opens the sessions folder to pick any other.
  - **Rename Session…**, **Export Session** ▸ PDF or ZIP (see below; shown once the session has a screenshot), **Show Session in Finder**, and **Copy Session File Path**, which puts the full path to `session.md` on the clipboard.
- **Discarded Screenshots** ▸ **Reopen Last Discarded** and **Reopen Discarded…** appears when something was thrown away in the last 7 days. That covers an editor closed without saving (Discard, ⌘W, Esc, the close button) and a screenshot removed from a session. A closed editor reopens with its marks; a removed screenshot goes back into its session. The menu covers every session; the session window's **Discarded** tab shows one session's. They live in `.discarded/` in the sessions folder and are deleted after 7 days, and follow a session when it is renamed.
- **Settings…** (⌘,, also from the Snapmark menu while a Snapmark window is in front) opens the Settings window, titled after the tab shown. **General**: Open Snapmark at login (it says so while macOS waits for your approval, with a button to Login Items), the sessions folder with **Change…**, **Clear Sessions Older Than 60 Days…** (asks first, moves them to the Trash; never the current session or one that is open), and the version with **Check for Updates…**. **Capture**: the capture bar's Save to, Timer and Show mouse pointer. **Shortcuts**: Pick tools with single keys (on by default; off, plain letters and digits pick no tool and only `⌘1`–`⌘7` do), the six global keys (a key another app owns says "Taken by another app"), and **Show All Shortcuts**. **Quit Snapmark** asks first if an editor still has marks or text that are not in a session.

Copies confirm with a notification. A session moved or deleted in Finder is reported instead of silently doing nothing.

**Export → ZIP** packs `session.md` and `img/` into `<session>.zip`, for agents and developers. **Export → PDF** renders the session into `<session>.pdf`, for people who just want to read it, without the _Text in the screenshot_ blocks that older entries still carry. Both land in the session folder, and Finder opens with the file selected. Sessions are stored in `~/Documents/Snapmark/`. **Settings… ▸ General ▸ Change…** moves new sessions elsewhere; pick a folder inside iCloud Drive or Google Drive and your sessions sync and can be shared from there. The `SNAPMARK_ROOT` environment variable overrides the choice (used by the tests).

## Develop

Requires Node 22 and macOS.

```sh
npm install
npm start            # build and run from source
npm run format       # prettier
npm run lint         # eslint
npm run typecheck    # tsc --noEmit
npm test             # session and Markdown logic
npm run smoke        # drives the real editor window: draws every tool, saves, checks pixels and Markdown
npm run smoke:background  # the same, failing if Snapmark ever takes the front from your other apps (macOS)
npm run dist         # build DMG + ZIP into release/ (ad-hoc signed)
npm run tokens       # rebuild src/tokens.css from design-system-starter (see below)
```

| Path                  | What                                                     |
| --------------------- | -------------------------------------------------------- |
| `src/main.ts`         | Menu bar, global shortcuts, capture, auto-update, IPC    |
| `src/menu.ts`         | The menu bar menu as data, tested without Electron       |
| `src/editor.ts/.html` | Annotation editor window                                 |
| `src/viewer.ts/.html` | Session window: `session.md` editable, screenshots       |
| `src/area.ts/.html`   | Area picker for Capture Last Area and Capture Scrolling  |
| `src/scroll.ts/.html` | Capture Scrolling's Done and Cancel bar                  |
| `src/stitch.ts`       | Stitches the scrolled frames, tested without Electron    |
| `src/beautify.ts`     | One-shot mode's Beautify layout, tested without Electron |
| `src/sessions.ts`     | Session folders and `session.md` writing                 |
| `src/ocr.ts`          | Text recognition (Vision through JXA), for auto-redact   |
| `src/redact.ts`       | Auto-redact's patterns, tested without Electron          |
| `src/tokens.css`      | Colours, sizes and shapes, generated; never edit by hand |
| `design/`             | `product.json` (Snapmark's values) and the tokens' lock  |
| `assets/`             | App icon, menu bar template icon                         |
| `build/`              | Packaging resources (icon, entitlements)                 |

Every window reads its colours, sizes and shapes from `src/tokens.css`: [design-system-starter](https://github.com/cdudek/design-system-starter) at the commit in `design/tokens.lock.json`, with Snapmark's accent from `design/product.json`. To take a newer system, bump `COMMIT` in `scripts/sync-tokens.mjs` and run `npm run tokens` from the repo root; `test/style.test.ts` fails when `tokens.css` and the lock disagree.

CI (`.github/workflows/ci.yml`) runs format check, lint, typecheck, unit test and the smoke test on every pull request.

## Release

Releases are manual: run **Actions › Release › Run workflow** on `main`; a merge only shows the pending version in the run summary. Versions follow [semver](https://semver.org) and are chosen by [semantic-release](https://semantic-release.gitbook.io) from all commit messages on `main` since the last release. Every pull request is squash-merged with its title as the commit, and CI rejects titles that are not [Conventional Commits](https://www.conventionalcommits.org):

| PR title starts with                              | Release              |
| ------------------------------------------------- | -------------------- |
| `fix:` or `perf:`                                 | patch: 0.4.0 → 0.4.1 |
| `feat:`                                           | minor: 0.4.1 → 0.5.0 |
| `feat!:`, `fix!:`, or a `BREAKING CHANGE:` footer | major: → 1.0.0       |
| `docs:`, `chore:`, `ci:`, `test:`, `refactor:`    | no release           |

A major version is the owner's decision. CI fails a PR that would make one (`!` in the title, or `BREAKING CHANGE` in the description) unless it carries the `major` label, which only people with write access to the repo can add.

The version lives in the release tag; `package.json` is not bumped in git.

`.github/workflows/release.yml` builds `arm64` and `x64` DMGs and ZIPs on macOS, signs and notarizes them, uploads them to the public bucket `gs://snapmark-updates/mac/` (keeping the newest 10 versions), and publishes the GitHub release and its `vX.Y.Z` tag with generated notes, at the version semantic-release chose for that commit. It does this only when started by hand on `main`. The upload logs in to GCP with Workload Identity Federation, so no key is stored.

The app checks the bucket's `latest-mac.yml` on start, then once a day, and from **Check for Updates…** in the Settings window, downloads in the background, and installs on quit (`electron-updater`). Two conditions must hold for it to work:

1. **The app must be signed with a Developer ID.** macOS refuses to apply updates to ad-hoc signed apps. Add these repository secrets and the release workflow signs and notarizes automatically: `MAC_CERT_P12_BASE64`, `MAC_CERT_PASSWORD`, `APPLE_ID`, `APPLE_APP_SPECIFIC_PASSWORD`, `APPLE_TEAM_ID`.
2. **The app must be able to read the update files.** The repository is private, so they come from the public bucket, not from GitHub releases (`build.publish` in `package.json`).
