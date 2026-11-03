# Changelog

## 2026-11-03 · Localization and developer documentation

- English and Spanish interface with English initial language and persistent preference.
- Studio becomes the initial theme; explicit Classic preferences are retained.
- English backend default episode context; UI language does not translate user media/content.
- English documentation reorganized for users and software-development students, including configuration, localization and generated source-symbol reference.
- Backend docstrings and frontend JSDoc explain responsibilities and state invariants.

## 2026-11-03 · Themes and design improvements

- Added Classic and midnight-blue Studio interface themes with browser preference storage.
- Added Baloo 2, Outfit, Balsamiq Sans, Lexend, Atkinson Hyperlegible and Comic Neue in Regular/Bold weights. Comic Neue is a libre Comic Sans-style alternative; Microsoft font files are not distributed.
- Added horizontal/vertical title offsets, immediate composition preview, JSON persistence and safe layout checks.
- Moved manual/import choice to the start of Design. Grouped save confirmation and green explicit background approval.

## 0.4.1 · 2026-11-03

- Extended completed retention from one hour to 24 hours; failures remain 15 minutes and active deadline four hours.
- Exposed retention capabilities, aligned media-cookie expiry and added unavailable-job recovery guidance/retained settings download.
- Confirmed that polling does not extend retention and restarts do not preserve episodes.

## 0.4.0 · 2026-11-03

- Added title bold and Nunito, Fredoka, Rounded and Poppins families with real local weights and license notices.
- Original application licensed MIT by its owner; third-party licenses retained.

## 0.3.0 · 2026-11-03

- Added independent title/subtitle fonts and sizes, six logo placements and margin controls across composition and render.

## 0.2.0 · 2026-11-02

- Added local Tiny/Base Whisper SRT generation, review/edit/download/approval and retry.
- Added optional configurable current-word highlighting with estimated timestamps.
- Bounded processing windows, cancellation, progress and intermediate cleanup.

## 0.1.0 · 2026-11-02

- Established local React/FastAPI workflow, native FFmpeg pipeline, validation, queue, preview approval, streaming downloads and managed cleanup.
- Added synthetic multimedia tests, CI, setup/diagnostic utilities and a measured 30-minute Windows render benchmark.
