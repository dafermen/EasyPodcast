# Local transcription

Choose Generate from audio in the first step. Upload audio without SRT, choose the spoken language and Tiny/Base, then create the episode. The shared worker queue runs transcription before the user can approve subtitles and continue to Design.

Python converts the selected audio stream into mono 16 kHz float32 PCM using FFmpeg. It supervises transcription/worker.mjs, which runs Transformers.js Whisper CPU q8. Supported language options are auto, en, es, pt, fr, de and it. The interface language is unrelated.

The Node worker processes overlapping windows of at most 30 seconds, accepting words from unique 20-second cores. It skips very quiet windows and clamps/validates timing. Python validates returned Word objects and groups them into short cues: up to eight words, roughly 64 characters, six seconds or a gap larger than one second. Progress is based on processed audio duration; model loading is indeterminate.

Model files download from Hugging Face on first use and live in a persistent cache separate from temporary media. Set TRANSCRIPTION_ALLOW_DOWNLOAD=false after populating the cache for offline use. Install dependencies with npm ci in transcription. Neither the audio nor SRT is sent to OpenAI for transcription.

Word timestamps are estimates, not forced alignment. Review recognition and synchronization. Generated cues can highlight the current word using ASS events. Uploaded SRT or edited generated text has no trustworthy word alignment and uses standard subtitles. Editing removes the original timing data. Download the original SRT before editing if needed.

Cancellation, active-time and free-space limits supervise both FFmpeg and Node. Intermediate PCM and partial JSON are removed in finally blocks. Failed generation can be retried or replaced with a new SRT workflow. Real Tiny recognition on short synthetic speech was previously verified; long human recordings, Base quality and bilingual accuracy still require evaluation. No speaker diarization or automatic translation is promised.
