# Projects, recovery and brand templates

## What is saved

A valid upload creates a local project automatically. Its SQLite record stores the title, timestamps, last checkpoint status, Design, subtitle cues/estimated word timing, approvals and media fingerprints. Controlled UUID folders store input audio, normalized/source-aspect background, optional logo, SRT and completed MP4 artifacts. No job token, thread event, subprocess, provider key or arbitrary user path is serialized.

The durable library defaults to `~/.easypodcast/library`, configurable with LIBRARY_ROOT. It is separate from TEMP_ROOT. Temporary editing/render sessions still expire and are cleaned up. Closing one removes its workspace, not the durable project. The current UI deliberately does not delete/prune saved projects automatically.

## Recovery workflow

Open Project library, find the cover/title and choose Continue project. An idle live workspace may be reused; after restart the server reconstructs a new workspace and token. A browser reload can reconnect to an existing running job and show progress/cancellation. A backend restart interrupts its child processes; an interrupted encoder, image generation or transcription never silently restarts. Review or explicitly retry as appropriate. Duplicate gives independent files/settings and a new project ID.

At the temporary workspace limit, opening another project may close the oldest idle safely archived workspace. Running operations and active downloads are protected. A missing/expired workspace can be reopened from its saved library entry. This is one local user's editor, not simultaneous collaborative editing; explicit saves/checkpoints from different sessions can supersede one another.

## Autosave and explicit saves

Design edits are sent as recovery drafts after a 900 ms pause. The status confirms acknowledgement. The request includes the last saved Design as a base version, so an old in-flight draft is ignored if a newer explicit design was saved. Switching projects first flushes the current draft. Page close attempts a keepalive flush but cannot guarantee delivery after a crash/network/disk failure. Wait for Recovery draft saved before relying on it.

Autosave does not approve backgrounds/previews or start rendering. Save design still commits validated render settings. Recovering a different draft invalidates old previews. SRT text/timing corrections use the explicit save button; they are not covered by appearance draft autosave.

## Templates

Save a clean design as a brand template, then apply it to another episode. Settings, output format, background/source image and logo are reused. Audio, captions, title, description, encoding quality/preset and explicit trim permission remain those of the current episode. Applying branding clears image/preview approvals; review a new preview. A template is more than a settings JSON: it also stores media locally. JSON import/export remains portable settings-only.

## Reliability and privacy

Metadata uses SQLite transactions; changed media is copied with bounded memory and per-file atomic replacement. Unchanged audio is not recopied for each draft. This is not an atomic filesystem-wide backup across sudden power loss. Missing required inputs or disk/access failures produce a visible archive error; retain the session/originals until resolved. Durable data needs space in addition to temporary rendering data.

The browser obtains a same-origin HttpOnly library capability with POST /api/library/session. The private capability file stays in the library and no secret appears in URLs/localStorage. Library list/open/duplicate/drafts/templates/covers require this session; job APIs keep their header-token checks. Never expose this single-user local service publicly.

## Backup and moving computers

Stop EasyPodcast after saving/completing work, then back up the entire LIBRARY_ROOT together, including SQLite, project/template folders, marker and private capability file. Keep that backup private. To move between Windows/macOS, install fresh application dependencies, restore the library into a dedicated directory, point LIBRARY_ROOT there and start one backend instance. Do not copy live temporary workspaces, .venv or node_modules. Cross-OS library transfer is documented but still needs native Mac validation. A local library does not synchronize itself or protect against storage failure.
