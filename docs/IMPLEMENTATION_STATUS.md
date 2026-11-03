# Implementation status

## Durable studio tools · 0.5.0 · 2026-11-03

Implemented durable SQLite projects/history/covers, reopen/duplicate, versioned appearance drafts, brand templates with media, direct title/logo dragging and resizing with guides, audio-assisted subtitle cue editing, preflight and 16:9/9:16/1:1 output. SRT is downloadable from Export. Completed project snapshots survive restart; active operations are not restarted automatically. Current browser sessions can reconnect to a still-running job after a page reload.

Browser review with synthetic speech and generated illustration/logo confirmed library reopen after a real backend restart, recovery of portrait format/title offset/logo placement, named template creation, audio seek/playback (4.435-second source), subtitle text/timing correction and approval, preflight, real vertical preview, and complete export. Windows verification: 110 backend tests, 27 frontend tests and 2 Node tests passed; Ruff, frontend formatting and TypeScript/Vite build passed. Local documentation links and all backend class/function docstrings were audited. The final service reports version 0.5.0. A completed portrait MP4 and its edited SRT were reopened successfully after another real restart; the interface resumed at Export. Screenshot: docs/screenshots/studio-050-export.png. Native macOS, large-library endurance and sudden power-loss corruption remain unverified.


## Bilingual UI and English documentation · 2026-11-03

Implemented English/Spanish interface selection with persistent browser preference, English initial locale, Studio initial theme and preservation of explicit existing preferences. User-authored titles, descriptions, subtitles and the spoken audio language stay independent. Backend default episode title/atmosphere now start in English. Backend message strings remain legacy API text and are localized in browser display.

Documentation is maintained in English, with installation, API, architecture, configuration, design, localization, privacy, transcription, testing and student learning guides. Backend classes/functions include docstrings; named frontend units include JSDoc. CODE_REFERENCE.md is generated from source and inventories functions/classes/parameters/assigned variables by scope. License text and exact code/catalog excerpts are preserved.

Verification in Windows: 97 backend tests, 22 frontend tests and 2 Node tests passed. Ruff, frontend format and TypeScript/Vite build passed. All backend functions/classes have docstrings; local documentation links were checked. Browser review covered English/Spanish Files, Design, Preview and Export; an unsaved custom title survived switching both ways, settings saved, a real synthetic preview rendered, phase/expiry labels localized and the preference survived reload. Screenshot: docs/screenshots/bilingual-studio.png. The authorized backend restart completed and health responded successfully. Native macOS, paid provider integration and long human speech recognition remain unverified.

## Previously observed evidence

- Windows backend baseline: 97 tests passed; frontend theme baseline: 18 tests passed; TypeScript/Vite build passed.
- Thirteen font families with Regular/Bold files. The six latest families were rendered in both weights and pixel differences were checked.
- Title offsets were tested in real renders, including JSON compatibility and layout bounds.
- Local Tiny Whisper recognized 11 words of 4.435-second synthetic English speech; audio-only → SRT → approval → highlighted MP4 was verified. Uploaded/edited SRT uses ordinary subtitles.
- Browser walkthroughs covered manual/import design entry, grouped Save/Continue feedback, typography, word highlighting and both themes. Screenshots are retained in docs/screenshots; older screenshots intentionally show earlier Spanish UI.
- Health/capabilities confirmed local service operation, 24-hour completed retention, 15-minute failure retention, 4-hour active deadline and survives_restart=false.
- Synthetic 30-minute Windows render: 720.20 seconds wall time, 391.15 MiB peak RSS, 196.48 MiB peak managed disk; raw benchmark in docs/benchmarks/windows-30m.json.
- Earlier Linux CI runs were observed successful, including https://github.com/dafermen/EasyPodcast/actions/runs/41642426978. This is historical evidence, not an assertion about the current commit.

## Operational limitations

Live editing jobs are in memory and interrupted by restart. The durable local library now reconstructs saved projects, while a browser reload can reconnect through its library cookie. A 404/410 does not imply a size limit and an old cached preview does not recover the audio. MIT covers original code; font licenses remain separate. No Internet exposure, lip synchronization, diarization, automatic transcript translation, or publishing is implemented. Do not infer native macOS verification or long-form human audio accuracy from synthetic Windows/Linux tests.
