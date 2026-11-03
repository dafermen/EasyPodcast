import { useRef, useState } from "react";
import { t } from "./i18n";
import { artifactUrl } from "./api";
import type { Job } from "./types";
export interface EditableCue {
  start: number;
  end: number;
  text: string;
}
/** Parse an SRT draft for timeline editing; server validation remains authoritative on save. */
export function parseTimeline(srt: string): EditableCue[] {
  return srt
    .trim()
    .split(/\r?\n\s*\r?\n/)
    .flatMap((block) => {
      const lines = block.split(/\r?\n/);
      const index = lines.findIndex((line) => line.includes("-->"));
      if (index < 0) return [];
      const match = lines[index].match(
        /(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)/,
      );
      if (!match) return [];
      const v = match.slice(1).map(Number);
      return [
        {
          start: v[0] * 3600 + v[1] * 60 + v[2] + v[3] / 1000,
          end: v[4] * 3600 + v[5] * 60 + v[6] + v[7] / 1000,
          text: lines.slice(index + 1).join("\n"),
        },
      ];
    });
}
/** Serialize editable cues with millisecond precision; invalid intervals are rejected by the backend. */
export function timelineSrt(cues: EditableCue[]) {
  function stamp(value: number) {
    const ms = Math.max(0, Math.round(value * 1000));
    return `${String(Math.floor(ms / 3600000)).padStart(2, "0")}:${String(Math.floor(ms / 60000) % 60).padStart(2, "0")}:${String(Math.floor(ms / 1000) % 60).padStart(2, "0")},${String(ms % 1000).padStart(3, "0")}`;
  }
  return (
    cues
      .map(
        (cue, i) =>
          `${i + 1}\n${stamp(cue.start)} --> ${stamp(cue.end)}\n${cue.text}`,
      )
      .join("\n\n") + "\n"
  );
}
/** Listen and seek to cues, edit their time/text, and keep the raw SRT editor synchronized. */
export function SubtitleTimeline({
  job,
  srt,
  onChange,
  disabled,
}: {
  job: Job;
  srt: string;
  onChange: (srt: string) => void;
  disabled: boolean;
}) {
  const audio = useRef<HTMLAudioElement>(null);
  const [time, setTime] = useState(0);
  const [page, setPage] = useState(0);
  const cues = parseTimeline(srt);
  const pageSize = 20;
  const pages = Math.max(1, Math.ceil(cues.length / pageSize));
  const currentPage = Math.min(page, pages - 1);
  /** Replace one editable cue field and serialize the new SRT draft. */
  function update(
    index: number,
    key: keyof EditableCue,
    value: string | number,
  ) {
    const next = cues.map((cue, i) =>
      i === index ? { ...cue, [key]: value } : cue,
    );
    onChange(timelineSrt(next));
  }
  return (
    <details className="subtitle-timeline">
      <summary>{t("Edit subtitles with audio")}</summary>
      <audio
        ref={audio}
        controls
        preload="metadata"
        src={artifactUrl(job, "audio")}
        onTimeUpdate={() => setTime(audio.current?.currentTime ?? 0)}
      />
      <p className="note">
        {t(
          "Listen, jump to a phrase, edit its text or timing, then save corrections below. Editing removes estimated word highlighting.",
        )}
      </p>
      <div className="cue-strip">
        {cues.map((cue, i) => (
          <button
            key={i}
            title={`${cue.start.toFixed(2)}s`}
            aria-label={`${t("Go to subtitle")} ${i + 1}`}
            style={{
              left: `${(cue.start / job.metadata.duration) * 100}%`,
              width: `${Math.max(0.2, ((cue.end - cue.start) / job.metadata.duration) * 100)}%`,
            }}
            className={time >= cue.start && time < cue.end ? "current" : ""}
            onClick={() => {
              if (audio.current) audio.current.currentTime = cue.start;
              setPage(Math.floor(i / pageSize));
            }}
          />
        ))}
      </div>
      <div className="cue-list">
        {cues
          .slice(currentPage * pageSize, (currentPage + 1) * pageSize)
          .map((cue, j) => {
            const index = currentPage * pageSize + j;
            return (
              <div
                key={index}
                className={`cue-row ${time >= cue.start && time < cue.end ? "current" : ""}`}
              >
                <button
                  onClick={() => {
                    if (audio.current) {
                      audio.current.currentTime = cue.start;
                      void audio.current.play().catch(() => {});
                    }
                  }}
                >
                  {t("Listen")} {index + 1}
                </button>
                <div className="pair">
                  <label>
                    {t("Start (seconds)")}
                    <input
                      type="number"
                      min="0"
                      step="0.01"
                      value={cue.start}
                      disabled={disabled}
                      onChange={(e) =>
                        update(index, "start", Number(e.target.value))
                      }
                    />
                  </label>
                  <label>
                    {t("End (seconds)")}
                    <input
                      type="number"
                      min="0"
                      step="0.01"
                      value={cue.end}
                      disabled={disabled}
                      onChange={(e) =>
                        update(index, "end", Number(e.target.value))
                      }
                    />
                  </label>
                </div>
                <label>
                  {t("Subtitle text")}
                  <textarea
                    value={cue.text}
                    disabled={disabled}
                    onChange={(e) => update(index, "text", e.target.value)}
                  />
                </label>
              </div>
            );
          })}
      </div>
      <div className="pair">
        <button disabled={!currentPage} onClick={() => setPage((n) => n - 1)}>
          {t("Previous phrases")}
        </button>
        <button
          disabled={currentPage >= pages - 1}
          onClick={() => setPage((n) => n + 1)}
        >
          {t("Next phrases")}
        </button>
      </div>
    </details>
  );
}
