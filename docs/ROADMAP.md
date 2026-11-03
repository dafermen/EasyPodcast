# Roadmap

| Phase | Scope | Acceptance |
| --- | --- | --- |
| 0 Foundation | Repository, environment, docs, backend/frontend, dependency locks | Health, capabilities and real build |
| 1 First video | Audio/SRT/image validation, ASS, CLI, FFmpeg | Decodable synthetic MP4 verified by FFprobe |
| 2 Browser workflow | Streaming uploads, tokens, queue, polling, cancellation, downloads, TTL | Browser walkthrough |
| 3 Design | Waveform/bars, title/fonts/position/logo, subtitle layout and preview offsets | Layout controls and real short render |
| 4 Optional AI | Provider abstraction, explicit generation/approval and safe errors | Fake contract tests; paid verification only if requested/configured |
| 5 Reliability | Managed cleanup, CI, testing, docs, benchmark | Evidence and explicit limits |

Implemented additions: local transcription and word highlighting; typography and title positioning; six additional font families; explicit manual/import design entry; grouped save/green-continue actions; 24-hour retention; Classic/Studio themes; English/Spanish interface and English developer documentation.

Remaining validation: native macOS, long human recordings and Whisper Base quality, 60–120 minute workloads, interrupted operating-system shutdown, download disconnects under load, assistive-technology review and a configured paid image generation if explicitly requested. Local snapshot persistence is now implemented separately from workspace TTL; cloud sync and automatic process continuation remain outside scope. Improve dense subtitle editing and continue breaking App into focused components as needed. Do not claim these tasks complete from synthetic tests alone.

## Completed studio expansion · 2026-11-03

Local project library/history/duplicate and recovery; debounced versioned appearance drafts; brand templates with background/logo; direct title/logo positioning and resizing with guides; audio-assisted subtitle timing/text editor; measured preflight; landscape/portrait/square rendering; SRT export link. Remaining checks include long-form library storage/backup workflows, native macOS and accessibility review. No automatic paid requests or publishing were added.
