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
  const [srt, setSrt] = useState("");
  const [original, setOriginal] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [reload, setReload] = useState(0);
  const active = isActive(job);
  useEffect(() => {
    if (!job.subtitles_ready || active) return;
    setError("");
    let current = true;
    api<{ srt: string }>(`/jobs/${job.id}/subtitles`, token)
      .then((data) => {
        if (current) {
          setSrt(data.srt);
          setOriginal(data.srt);
        }
      })
      .catch((e) => setError(e.message));
    return () => {
      current = false;
    };
  }, [job.id, job.subtitles_ready, active, token, reload]);
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
  const dirty = srt !== original;
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
      <SubtitleTimeline job={job} srt={srt} onChange={setSrt} disabled={busy} />
      <details>
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
            disabled={busy}
            onChange={(e) => setSrt(e.target.value)}
            spellCheck={false}
          />
        </label>
      </details>
      <button
        disabled={busy || !dirty}
        onClick={() =>
          run(async () => {
            const next = await api<Job>(
              `/jobs/${job.id}/subtitles`,
              token,
              "PUT",
              JSON.stringify({ srt }),
            );
            onChange(next);
            setOriginal(srt);
          })
        }
      >
        {" "}
        {t("Guardar correcciones del SRT")}{" "}
      </button>
      {error && (
        <div>
          <p role="alert">{t(error)}</p>
          <button disabled={busy} onClick={() => setReload((n) => n + 1)}>
            {" "}
            {t("Volver a cargar el SRT")}{" "}
          </button>
        </div>
      )}
      <button
        className="primary"
        disabled={busy || dirty || !srt}
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
