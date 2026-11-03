# Privacy, files and session lifetime

EasyPodcast is intended for a single local user on loopback. Audio, SRT, rendered video and local transcription remain on the machine. Hugging Face supplies model files on first use; optional image generation sends only visual context after an explicit action. Provider keys remain backend-only.

A job has a random ID and secret token. API calls authenticate with X-Job-Token. Browser media navigation uses a job-specific HttpOnly/SameSite cookie scoped to artifacts. Cookies expire with the existing job deadline; polling does not extend the deadline. Browser preference storage contains no media or tokens. A separate HttpOnly library cookie authorizes local project access; its private owner key never enters JavaScript.

The managed temporary root is exclusive, marker-protected and file-locked. Each job has a UUID child folder with internal filenames. Original upload names are not used as filesystem paths. Startup and scheduled cleanup remove only managed children; symlinks are not followed. Deletion is deferred while a worker or download reader uses files. Models use a separate persistent cache and are not removed with episode cleanup.

Default retention is 24 hours after creation or a completed operation, 15 minutes after failure/cancellation, and 4 hours maximum active operation time. These are configurable workspace limits. A separate SQLite library retains validated projects and completed artifacts beyond workspace expiry. Restart interrupts active work and reload loses the workspace token, but Project library can reopen archived inputs/settings with a valid session. Cached previews alone still do not prove the live workspace exists.

Keep originals, download outputs and export design JSON. JSON recovers settings only. Never commit user media, model caches, .env, tokens or render outputs. MIT covers original code; third-party media/fonts keep their own rights. Do not expose this local service on a LAN or the Internet without a separate authentication/TLS design.

LIBRARY_ROOT defaults to ~/.easypodcast/library. It contains project audio/images/SRT/video, template images, metadata and the private library capability. Treat the whole directory as private local data and include it in your own backups. Archives are not automatically deleted. Checkpoints copy changed media, so temporary plus durable files need more disk space than a single export. The app deletes only its temporary workspaces and incomplete staging copies, never user originals or durable projects automatically.

Autosaved appearance drafts are separate from approved render settings and contain no job token. Only acknowledged saves are reliable; page-close/network/disk failure may prevent the last edit from reaching storage. SRT edits are explicit saves. A local library is not multi-user access control, cloud sync or a crash-proof transactional filesystem backup.
