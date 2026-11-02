export interface Design {
  title: string;
  description: string;
  image_style: "illustration" | "realistic";
  atmosphere: string;
  visualizer: "waveform" | "spectrum";
  color: string;
  sensitivity: number;
  wave_y: number;
  wave_height: number;
  font_size: number;
  subtitle_font: "sans" | "serif" | "mono";
  title_font: "sans" | "serif" | "mono";
  title_font_size: number;
  logo_position:
    | "top-left"
    | "top-right"
    | "middle-left"
    | "middle-right"
    | "bottom-left"
    | "bottom-right";
  logo_margin: number;
  subtitle_color: string;
  outline: number;
  subtitle_margin: number;
  subtitle_width: number;
  max_lines: number;
  crf: number;
  preset: "ultrafast" | "veryfast" | "fast" | "medium";
  trim_subtitles: boolean;
  highlight_words: boolean;
  highlight_color: string;
}
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
