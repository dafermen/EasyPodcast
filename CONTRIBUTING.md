# Contributing

Read AGENTS.md, README.md, docs/DEVELOPMENT.md and docs/ARCHITECTURE.md. A good first walkthrough is docs/JUNIOR_GUIDE.md; docs/CODE_REFERENCE.md lists the source symbols and state.

Keep changes focused and preserve the local-only security boundary. Use English for source identifiers/comments/documentation and support both UI languages. Do not translate user content or rename protocol keys for localization. Keep dependency locks, licenses and third-party notices. Never add .env, media, model caches, tokens or rendered videos to Git.

Before submitting, run backend pytest/Ruff, frontend tests/format/build and relevant transcription tests. A render change needs a synthetic real MP4 check. Update implementation status with observed checks, not assumptions. Regenerate the code reference when symbols change. Explain the problem, final behavior, tests and limitations in the pull request. No paid calls, deployment or user-media publication in automated checks.
