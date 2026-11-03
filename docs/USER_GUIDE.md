# User guide

## Preferences

Use **Interface language** to choose English or Spanish. New browser profiles default to English. **Interface theme** offers Studio (default) and Classic. Preferences are stored in this browser and change immediately without clearing the episode. Explicit saved preferences take priority over defaults. Audio language is a separate transcription setting. Your title and subtitle content are never translated automatically.

## 1. Files

Check Media engine ready. Upload MP3, WAV or M4A audio. Select an existing UTF-8 SRT or Generate from audio (local). The backend inspects the actual contents. Optionally upload PNG/JPEG background and a transparent PNG logo. Select Create episode.

For generation, choose the language spoken in the audio and Tiny or Base. First use downloads a model from Hugging Face. Wait for transcription, download/review its SRT and approve subtitles before designing. Editing generated SRT removes word timestamps, so word highlighting becomes unavailable. Standard subtitles still work.

## 2. Design

Choose Configure manually or Import a JSON design. Import accepts settings exported by EasyPodcast, not another program's transcript JSON. Audio, SRT, background and logo are separate files. Review imported settings before continuing.

Set the title, visual description and atmosphere; these are content, not interface preferences. Typography and logo contains title/subtitle fonts and sizes, title bold, horizontal/vertical title offsets and six logo placements. Negative offsets move left/up; positive offsets move right/down. Zero restores the original title position.

Adjust visualizer, colors and subtitle layout. If subtitles extend beyond the audio, explicitly permit trimming. Warnings about dense text or overlap deserve preview review. Select Save design; the confirmation points to the green Approve background and continue button. Unsaved changes block continuation.

The local background requires no provider. AI image generation is optional and explicit, may cost money, and receives only visual context. Review generated images before approval. To keep the same hosts in later episodes, reuse the downloaded PNG; the same prompt does not guarantee identical characters.

## 3. Preview

Enter the starting second: 0 tests the beginning; 60 tests from one minute. The clip lasts up to 20 seconds or the remaining audio. Watch it and inspect sound, timing, line wrapping, title, logo and current-word highlighting. The MP4 is the final reference; the browser canvas is approximate. Adjust design if necessary, otherwise approve the preview.

## 4. Export

Render the complete episode with the approved settings. Progress follows processed audio time. Download the MP4, background and design JSON. Downloads stream to the browser. The video is 1920 × 1080, 30 fps, H.264/AAC. No lip movement or automatic publishing is provided.

## Projects, templates and recovery

Your validated uploads create a saved local project automatically. The Project library above the editor shows covers, names, dates, status and recovery drafts. Continue project reopens it after a reload or restart. Duplicate creates an independent copy. Close episode removes the temporary workspace; the saved project remains in the library. Projects are stored on this computer, not synchronized to another OS automatically.

Design changes save a recovery draft after a short pause. Wait for Recovery draft saved before closing; a page-close flush is best effort. Save design still commits the actual render settings. A recovered changed draft invalidates earlier previews so you must review a new one. Save failures are shown: keep the session open and check disk/access rather than assuming recovery succeeded. Subtitle text/timing edits require Save SRT corrections.

Save current design as template stores fonts, colors, positions, output format, background and logo. Apply template keeps this episode's title/description and subtitles, replaces branding and requires a new preview. Save pending design changes before applying a template.

On the canvas, drag the title/logo or focus them and use arrow keys (Shift for larger steps). Corner handles resize title/logo; the sliders remain available. Alignment guides appear while dragging. Choose landscape 16:9, portrait 9:16 or square 1:1 and inspect each independently. Backgrounds fit without cropping; a landscape image may have padding in portrait output. A true vertical background keeps its source aspect.

Review or edit subtitles opens audio playback plus cue blocks and editable start/end seconds and text. Listen jumps to a phrase. Save corrections, then approve subtitles again. The raw SRT editor remains available. Changing timing/text removes estimated word highlighting.

Before Preview and Export, Pre-export checks reports text overflow, invalid title placement and likely logo collisions. Fix blockers; warnings still need visual review. It cannot identify faces or judge aesthetics. Download the SRT from Export alongside MP4/background/JSON.

Keep originals and back up LIBRARY_ROOT. Persistence does not protect against a deleted library, disk failure, loss of an unacknowledged draft or an operation interrupted before its output was validated. Completed snapshots are recoverable; running encoders/transcription must be explicitly retried. No project deletion or automatic archive pruning is provided in this block; use backups/storage management deliberately.
