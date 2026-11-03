# Privacy, files and session lifetime

EasyPodcast is intended for a single local user on loopback. Audio, SRT, rendered video and local transcription remain on the machine. Hugging Face supplies model files on first use; optional image generation sends only visual context after an explicit action. Provider keys remain backend-only.

A job has a random ID and secret token. API calls authenticate with X-Job-Token. Browser media navigation uses a job-specific HttpOnly/SameSite cookie scoped to artifacts. Cookies expire with the existing job deadline; polling does not extend the deadline. Browser language/theme storage contains no media or tokens.

The managed temporary root is exclusive, marker-protected and file-locked. Each job has a UUID child folder with internal filenames. Original upload names are not used as filesystem paths. Startup and scheduled cleanup remove only managed children; symlinks are not followed. Deletion is deferred while a worker or download reader uses files. Models use a separate persistent cache and are not removed with episode cleanup.

Default retention is 24 hours after creation or a completed operation, 15 minutes after failure/cancellation, and 4 hours maximum active operation time. These are configurable. There is no database, history or restart recovery: restarting destroys jobs; reloading the page loses the token held in React memory. Cached previews do not prove the server still retains the original audio.

Keep originals, download outputs and export design JSON. JSON recovers settings only. Never commit user media, model caches, .env, tokens or render outputs. MIT covers original code; third-party media/fonts keep their own rights. Do not expose this local service on a LAN or the Internet without a separate authentication/TLS design.
