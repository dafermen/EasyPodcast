import { registerDraft } from "./drafts";
import { SubtitleTimeline } from "./SubtitleTimeline";
import { t } from "./i18n";
import { useEffect, useState } from "react";
import { api, artifactUrl, isActive } from "./api";
import type { Job } from "./types";

/** Load, edit and explicitly approve SRT while preserving honest word-timing availability. */
export function SubtitleReview({
  job,
  token,
  onChange,
  onContinue,
}: {
  job: Job;
  token: string;
  onChange: (job: Job) => void;
  onContinue: () => void;
}) {
  const [baseline, setBaseline] = useState<{
    base_digest: string;
    base_version: number;
  } | null>(null);
  const [draftStatus, setDraftStatus] = useState("");
  const [recovered, setRecovered] = useState(false);
  const [srt, setSrt] = useState("");
  const [original, setOriginal] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [loading, setLoading] = useState(true);
  const [reload, setReload] = useState(0);
  const active = isActive(job);
  useEffect(() => {
    if (!job.subtitles_ready || active) return;
    setError("");
    setBaseline(null);
    setLoading(true);
    setSrt("");
    setOriginal("");
    setRecovered(false);
    let current = true;
    api<{
      srt: string;
      base_digest?: string;
      base_version?: number;
      draft?: string | null;
      draft_conflict?: boolean;
    }>(`/jobs/${job.id}/subtitles`, token)
      .then((data) => {
        if (current) {
          setSrt(data.draft ?? data.srt);
          setRecovered(data.draft != null);
          setDraftStatus(
            data.draft_conflict
              ? "Saved subtitles changed. Review the recovered text before saving."
              : data.draft != null
                ? "Subtitle recovery draft restored. Review and save corrections."
                : "",
          );
          if (data.base_digest)
            setBaseline({
              base_digest: data.base_digest,
              base_version: data.base_version || 0,
            });
          setOriginal(data.srt);
        }
      })
      .catch((e) => {
        if (current) setError(e.message);
      })
      .finally(() => {
        if (current) setLoading(false);
      });
    return () => {
      current = false;
    };
  }, [job.id, job.subtitles_ready, active, token, reload]);
  const dirty = srt !== original;
  useEffect(() => {
    if (!baseline || !job.project_id || !dirty || busy || active) return;
    let current = true;
    const payload = JSON.stringify({ srt, ...baseline });
    /** Persist raw caption text against the original digest and edit generation. */
    async function save() {
      await api("/library/session", undefined, "POST");
      const result = await api<{ saved: boolean }>(
        `/projects/${job.project_id}/subtitle-draft`,
        undefined,
        "PUT",
        payload,
      );
      if (!result.saved)
        throw new Error(
          "Saved subtitles changed. Reload them before saving these corrections.",
        );
      if (current) setDraftStatus("Subtitle recovery draft saved");
    }
    const unregister = registerDraft(save);
    setDraftStatus("Saving subtitle recovery draft…");
    const timer = setTimeout(() => {
      void save().catch((e) => {
        if (current) setDraftStatus(e.message);
      });
    }, 900);
    const pagehide = () => {
      if (new Blob([payload]).size < 60000)
        void fetch(`/api/projects/${job.project_id}/subtitle-draft`, {
          method: "PUT",
          credentials: "same-origin",
          headers: { "Content-Type": "application/json" },
          body: payload,
          keepalive: true,
        }).catch(() => {});
    };
    window.addEventListener("pagehide", pagehide);
    return () => {
      current = false;
      clearTimeout(timer);
      unregister();
      window.removeEventListener("pagehide", pagehide);
    };
  }, [baseline, job.project_id, dirty, srt, busy, active]);
  /** Wrap subtitle operations with busy/error feedback. */
  async function run(action: () => Promise<void>) {
    setBusy(true);
    setError("");
    try {
      await action();
    } catch (e) {
      setError(
        e instanceof Error ? e.message : t("Error al actualizar subtítulos."),
      );
    } finally {
      setBusy(false);
    }
  }
  if (active)
    return (
      <div className="fields">
        <h3>{t("Generando subtítulos")}</h3>
        <p>
          {" "}
          {t(
            "La transcripción se ejecuta en tu equipo. La primera vez se descarga el modelo. El progreso aparece en el panel del episodio.",
          )}{" "}
        </p>
      </div>
    );
  if (!job.subtitles_ready)
    return (
      <div className="fields">
        <p>
          {(job.error ? t(job.error) : "") ||
            t("Todavía no hay subtítulos disponibles.")}
        </p>
        <button
          disabled={busy}
          onClick={() =>
            run(async () =>
              onChange(
                await api<Job>(`/jobs/${job.id}/transcribe`, token, "POST"),
              ),
            )
          }
        >
          {" "}
          {t("Reintentar transcripción")}{" "}
        </button>
        {error && <p role="alert">{t(error)}</p>}
      </div>
    );
  return (
    <div className="fields">
      <h3>{t("Revisa los subtítulos")}</h3>
      <p>
        {job.word_timestamps
          ? t(
              "Incluyen tiempos estimados por palabra: el resaltado amarillo estará disponible en Diseño.",
            )
          : t("SRT sin tiempos por palabra: se mostrarán subtítulos normales.")}
      </p>
      <a className="button" href={artifactUrl(job, "subtitles", true)}>
        {" "}
        {t("Descargar SRT")}{" "}
      </a>
      <SubtitleTimeline
        job={job}
        srt={srt}
        onChange={setSrt}
        disabled={busy || loading}
      />
      {draftStatus && <p role="status">{t(draftStatus)}</p>}
      {(dirty || recovered) && (
        <button
          disabled={busy || loading}
          onClick={() => {
            if (
              window.confirm(
                t(
                  "Discard the subtitle recovery draft and reload saved subtitles?",
                ),
              )
            )
              void run(async () => {
                await api(
                  `/projects/${job.project_id}/subtitle-draft`,
                  undefined,
                  "DELETE",
                );
                setSrt(original);
                setRecovered(false);
                setReload((n) => n + 1);
              });
          }}
        >
          {t("Discard subtitle draft")}
        </button>
      )}
      <details open={recovered || undefined}>
        <summary>{t("Revisar o corregir SRT")}</summary>
        <p className="note">
          {" "}
          {t(
            "Guardar cambios elimina los tiempos por palabra y desactiva el resaltado. Puedes descargar el original antes de editar.",
          )}{" "}
        </p>
        <label>
          {" "}
          {t("Subtítulos sincronizados")}{" "}
          <textarea
            rows={14}
            value={srt}
            disabled={busy || loading}
            onChange={(e) => setSrt(e.target.value)}
            spellCheck={false}
          />
        </label>
      </details>
      <button
        disabled={busy || loading || (!dirty && !recovered)}
        onClick={() =>
          run(async () => {
            const next = await api<Job>(
              `/jobs/${job.id}/subtitles`,
              token,
              "PUT",
              JSON.stringify({ srt, ...baseline }),
            );
            onChange(next);
            setOriginal(srt);
            setRecovered(false);
            setReload((n) => n + 1);
          })
        }
      >
        {" "}
        {t("Guardar correcciones del SRT")}{" "}
      </button>
      {error && (
        <div>
          <p role="alert">{t(error)}</p>
          <button
            disabled={busy || loading}
            onClick={() => setReload((n) => n + 1)}
          >
            {" "}
            {t("Volver a cargar el SRT")}{" "}
          </button>
        </div>
      )}
      <button
        className="primary"
        disabled={busy || loading || dirty || recovered || !srt}
        onClick={() =>
          run(async () => {
            onChange(
              await api<Job>(
                `/jobs/${job.id}/subtitles/approve`,
                token,
                "POST",
              ),
            );
            onContinue();
          })
        }
      >
        {" "}
        {t("Aprobar subtítulos y diseñar →")}{" "}
      </button>
    </div>
  );
}
