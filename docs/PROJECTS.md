# Projects, recovery and brand templates

## What is saved

A valid upload creates a local project automatically. Its SQLite record stores the title, timestamps, last checkpoint status, Design, subtitle cues/estimated word timing, approvals and media fingerprints. Controlled UUID folders store input audio, normalized/source-aspect background, optional logo, SRT and completed MP4 artifacts. No job token, thread event, subprocess, provider key or arbitrary user path is serialized.

The durable library defaults to `~/.easypodcast/library`, configurable with LIBRARY_ROOT. It is separate from TEMP_ROOT. Temporary editing/render sessions still expire and are cleaned up. Closing one removes its workspace, not the durable project. The UI supports explicit recoverable Trash and typed permanent deletion; it never prunes saved projects automatically.

## Recovery workflow

Open Project library, find the cover/title and choose Continue project. An idle live workspace may be reused; after restart the server reconstructs a new workspace and token. A browser reload can reconnect to an existing running job and show progress/cancellation. A backend restart interrupts its child processes; an interrupted encoder, image generation or transcription never silently restarts. Review or explicitly retry as appropriate. Duplicate gives independent files/settings and a new project ID.

At the temporary workspace limit, opening another project may close the oldest idle safely archived workspace. Running operations and active downloads are protected. A missing/expired workspace can be reopened from its saved library entry. This is one local user's editor, not simultaneous collaborative editing; explicit saves/checkpoints from different sessions can supersede one another.

## Autosave and explicit saves

Design edits are sent as recovery drafts after a 900 ms pause. The status confirms acknowledgement. The request includes the last saved Design as a base version, so an old in-flight draft is ignored if a newer explicit design was saved. Switching projects first flushes the current draft. Page close attempts a keepalive flush but cannot guarantee delivery after a crash/network/disk failure. Wait for Recovery draft saved before relying on it.

Autosave does not approve backgrounds/previews or start rendering. Save design still commits validated render settings. Recovering a different draft invalidates old previews. Subtitle text/timing edits now also autosave as raw recovery text, including incomplete or temporarily invalid SRT. The saved SRT digest plus an edit generation reject stale requests. Explicit Save corrections validates SRT, drops obsolete word timestamps and invalidates renders; approval remains separate. Pending subtitle recovery blocks rendering until saved or discarded. Recovery opens the raw editor so unfinished text remains editable. Discard requires confirmation.

## Templates

Save a clean design as a brand template, then apply it to another episode. Settings, output format, background/source image and logo are reused. Audio, captions, title, description, encoding quality/preset and explicit trim permission remain those of the current episode. Applying branding clears image/preview approvals; review a new preview. A template is more than a settings JSON: it also stores media locally. JSON import/export remains portable settings-only.

## Reliability and privacy

Metadata uses SQLite transactions; changed media is copied with bounded memory and per-file atomic replacement. Unchanged audio is not recopied for each draft. This is not an atomic filesystem-wide backup across sudden power loss. Missing required inputs or disk/access failures produce a visible archive error; retain the session/originals until resolved. Durable data needs space in addition to temporary rendering data.

The browser obtains a same-origin HttpOnly library capability with POST /api/library/session. The private capability file stays in the library and no secret appears in URLs/localStorage. Library list/open/duplicate/drafts/templates/covers require this session; job APIs keep their header-token checks. Never expose this single-user local service publicly.

## Backup and moving computers

Open **Project library → Manage, transfer and back up**. **Export project ZIP** packages one saved episode with audio, images, logo, SRT, estimated word timing, saved appearance, recovery drafts and completed outputs. **Prepare library backup** packages all projects, brand templates and Trash. Download the prepared ZIP within 30 minutes; downloads are single-use and streamed from disk. A failed/interrupted download can be prepared again. Packages contain private media; keep them private. They exclude the machine-local owner key, SQLite file, provider secrets and temporary job tokens.

On the other computer, install EasyPodcast and its native dependencies. Choose **Import project or library ZIP**, review the verified contents, then **Import as new copies**. Validation alone does not install anything. Confirmation assigns fresh IDs, never overwrites existing projects and preserves Trash placement. Cancel removes staged files. No automatic rendering or transcription occurs. Settings-only design JSON is still a separate option and does not include media. The ZIP protocol uses fixed ASCII filenames and UUID paths; native macOS execution remains unverified.

Exports freeze archived media versions under the library lock, then build a disk-backed ZIP64 file. Imports stream uploads, check expanded/file/manifest budgets, reject unsafe paths/duplicates/links/unexpected entries, verify SHA-256 and inspect actual audio/images/video. Validated copies install transactionally; a failed install rolls back only its new records/directories. SHA-256 detects damage, not authorship. Completed saved checkpoints are included; active operations may finish after the frozen backup and should be backed up again afterward. ZIPs are not incremental backups or cloud synchronization.

## Administration and storage

Search project titles and sort by recent update, name or size. Management also searches templates. Rename changes a library label independently from the title burned into the video. Move to Trash requires confirmation and closes idle workspaces after checkpointing; running operations and downloads block it. Restore keeps the identity, media and drafts. Permanent deletion is available only in Trash and requires typing the exact displayed confirmation name. It cannot be undone. Storage reports active project/template bytes, Trash bytes, database bytes and free disk. Moving to Trash does not free disk space. Figures exclude temporary workspaces, model caches and browser downloads.

For a complete forensic filesystem copy, stop the service and copy the entire private LIBRARY_ROOT consistently. Prefer portable UI packages when moving individual episodes or merging libraries. Do not copy .venv, node_modules or live temporary workspaces between operating systems.
