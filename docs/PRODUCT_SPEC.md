# Product specification

## Purpose

Provide a local, OS-independent browser workflow for creating podcast videos from audio and subtitles. Primary output: 1920 × 1080, 30 fps MP4, H.264 video with AAC audio, a static background, optional title/logo, audio-reactive waveform/frequency bars and styled subtitles.

## Required workflow

Files → optional subtitle review → Design → Preview → Export. Accept existing SRT or local Whisper generation. Design starts with manual/import choice; preserve explicit approval of subtitles, background and preview. Saving settings invalidates stale render artifacts. A preview lasts up to 20 seconds at a user-selected offset.

UI supports English/Spanish with English default and Studio/Classic with Studio default. Explicit browser preferences persist. These preferences never change episode content or exported JSON. Font families, sizes, title position and logo placement belong to the episode design.

## Constraints and acceptance

One backend process, one media worker, bounded queue/upload/storage limits and supervised cancellation. Stream uploads/downloads. Reject malformed media, unsafe fields and invalid layout. Expose honest phase/progress information, actionable validation and retention deadlines. Keep secrets/backend paths out of UI responses.

Defaults: 1 GiB audio, 5 MiB SRT, 20 MiB per image, 25 million pixels, two-hour audio product limit, eight jobs, two queued operations, 512 MiB minimum free space. A product limit is not a performance guarantee. Refer to CONFIGURATION.md and IMPLEMENTATION_STATUS.md.

## Outside current scope

No lip synchronization, speaker diarization, automatic subtitle translation, cloud synchronization, Internet hosting/authentication, YouTube publishing, Xcode integration or guaranteed identical AI characters. No claim of native macOS verification or long-form human speech transcription accuracy yet.

## Local production tools

Durable project history/reopen/duplicate, acknowledged design recovery drafts, reusable branding including media, pointer/keyboard title and logo manipulation with resize handles/guides, audio-assisted subtitle cue editing, pre-export layout checks and SRT download are implemented. Output formats: landscape 1920 × 1080, portrait 1080 × 1920 and square 1080 × 1080 at 30 fps. Each format uses its own frame-coordinate composition and a newly approved preview. Running jobs are not resumed automatically after interruption.
