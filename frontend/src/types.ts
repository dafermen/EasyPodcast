/** Full episode settings contract. Runtime validation belongs to backend Pydantic models. */
export interface Design {
  /** Episode title drawn in the video; never translated by the interface locale. */
  title: string;
  /** Optional visual context sent only to an explicitly selected image provider. */
  description: string;
  /** Allowlisted image-generation style, not an arbitrary instruction. */
  image_style: "illustration" | "realistic";
  /** User-authored visual palette/context; independent of interface language. */
  atmosphere: string;
  /** Choose waveform or frequency spectrum for the audio-reactive layer. */
  visualizer: "waveform" | "spectrum";
  /** Visualizer color as a strict RGB hex value. */
  color: string;
  /** Gain on the visual analysis branch, not the exported sound volume. */
  sensitivity: number;
  /** Visualizer top position as a fraction of the 1080-pixel canvas height. */
  wave_y: number;
  /** Visualizer height as a fraction of the canvas height. */
  wave_height: number;
  /** Subtitle font size in 1080p video pixels. */
  font_size: number;
  /** Allowlisted bundled subtitle font family ID. */
  subtitle_font:
    | "sans"
    | "serif"
    | "mono"
    | "nunito"
    | "fredoka"
    | "quicksand"
    | "poppins"
    | "baloo2"
    | "outfit"
    | "balsamiqsans"
    | "lexend"
    | "atkinsonhyperlegible"
    | "comicneue";
  /** Allowlisted bundled title font family ID. */
  title_font: Design["subtitle_font"];
  /** Select the real Bold title weight when enabled. */
  title_bold: boolean;
  /** Title font size in 1080p video pixels. */
  title_font_size: number;
  /** Horizontal offset from the centered title anchor, in pixels; negative moves left. */
  title_offset_x: number;
  /** Vertical offset from the original 100-pixel title top, in pixels; negative moves up. */
  title_offset_y: number;
  /** One of six allowlisted edge/vertical logo placements. */
  logo_position:
    | "top-left"
    | "top-right"
    | "middle-left"
    | "middle-right"
    | "bottom-left"
    | "bottom-right";
  /** Logo inset from the selected canvas edge, in video pixels. */
  logo_margin: number;
  /** Subtitle RGB hex color; text is still escaped separately for ASS. */
  subtitle_color: string;
  /** Subtitle outline thickness in video pixels. */
  outline: number;
  /** Subtitle bottom inset in video pixels. */
  subtitle_margin: number;
  /** Fraction of canvas width allowed for subtitle wrapping. */
  subtitle_width: number;
  /** Maximum wrapped subtitle lines; excessive text raises an error rather than truncating. */
  max_lines: number;
  /** H.264 constant-rate-factor quality; lower values increase quality/file size. */
  crf: number;
  /** Allowlisted encoder speed/compression tradeoff. */
  preset: "ultrafast" | "veryfast" | "fast" | "medium";
  /** Explicit permission to clip cues extending beyond the audio. */
  trim_subtitles: boolean;
  /** Highlight estimated active words only when trustworthy timing exists. */
  highlight_words: boolean;
  /** RGB hex color for the currently active recognized word. */
  highlight_color: string;
}
/** Token-free polling snapshot; the upload response supplies a separate secret token. */
export interface Job {
  id: string;
  state: string;
  phase: string;
  progress: number | null;
  error: string | null;
  metadata: { duration: number; audio_tracks: number; codec: string };
  warnings: string[];
  config: Design;
  background_approved: boolean;
  preview_approved: boolean;
  background_mode: string;
  artifacts: string[];
  expires_at: string;
  subtitle_source: "upload" | "generate";
  subtitles_ready: boolean;
  subtitles_approved: boolean;
  word_timestamps: boolean;
}
/** Startup dependency checks and operational limits exposed by the local backend. */
export interface Capabilities {
  ffmpeg: boolean;
  ffprobe: boolean;
  h264: boolean;
  aac: boolean;
  font: boolean;
  filters: Record<string, boolean>;
  render_ready: boolean;
  image_provider: boolean;
  transcription?: {
    available: boolean;
    local: boolean;
    word_timestamps: boolean;
    models: string[];
    languages: string[];
    model_download_allowed: boolean;
  };
  limits: {
    audio_bytes: number;
    srt_bytes: number;
    image_bytes: number;
    duration_seconds: number;
    pixels: number;
    queue: number;
    concurrent_renders: number;
    jobs: number;
  };
}
