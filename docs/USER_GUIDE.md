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

## Keeping your work

Keep original media and download results. Jobs are temporary: default completed retention is 24 hours, failures/cancellations 15 minutes and active operation limit 4 hours. Polling does not extend retention. Restart loses jobs; reload loses the current token. A cached preview can remain visible after the backend job has disappeared. Retained JSON can recover settings, not lost media. Delete episode and files requests managed cleanup, waiting for active operations/readers.
