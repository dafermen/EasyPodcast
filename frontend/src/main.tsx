import { DesignEntry } from "./DesignEntry";
import { DesignActions } from "./DesignActions";
import React, { useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import { api, artifactUrl, isActive, ApiError } from "./api";
import type { Capabilities, Design, Job } from "./types";
import { text } from "./text";
import "./style.css";
import {
  TypographyControls,
  fontFamilies,
  logoStyle,
} from "./TypographyControls";
import { SubtitleReview } from "./SubtitleReview";

export function App() {
  const [caps, setCaps] = useState<Capabilities | null>(null);
  const [job, setJob] = useState<Job | null>(null);
  const [token, setToken] = useState("");
  const [design, setDesign] = useState<Design | null>(null);
  const [step, setStep] = useState(0);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [start, setStart] = useState(0);
  const [revision, setRevision] = useState(0);
  const [dirty, setDirty] = useState(false);
  const [designMethod, setDesignMethod] = useState<"manual" | "import">(
    "manual",
  );
  const [importedDesign, setImportedDesign] = useState(false);
  const [savedDesign, setSavedDesign] = useState(false);
  const [unavailable, setUnavailable] = useState(false);
  const [subtitleMode, setSubtitleMode] = useState<"upload" | "generate">(
    "upload",
  );
  const [language, setLanguage] = useState("en");
  const [transcriptionModel, setTranscriptionModel] = useState("tiny");
  const heading = useRef<HTMLHeadingElement>(null);
  const active = isActive(job);

  useEffect(() => {
    api<Capabilities>("/capabilities")
      .then(setCaps)
      .catch((e) => setError(e.message));
  }, []);
  useEffect(() => {
    heading.current?.focus();
  }, [step]);
  useEffect(() => {
    if (!job || !token) return;
    let stopped = false;
    const timer = setInterval(() => {
      api<Job>(`/jobs/${job.id}`, token)
        .then((next) => {
          if (stopped) return;
          setJob((previous) => {
            if (isActive(previous) && !isActive(next))
              setRevision((r) => r + 1);
            return next;
          });
        })
        .catch((e) => {
          if (!stopped) {
            setError(e.message);
            if (e instanceof ApiError && [404, 410].includes(e.status))
              setUnavailable(true);
            clearInterval(timer);
          }
        });
    }, 1500);
    return () => {
      stopped = true;
      clearInterval(timer);
    };
  }, [job?.id, token]);

  async function perform(action: () => Promise<void>) {
    setBusy(true);
    setError("");
    try {
      await action();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error inesperado.");
      if (job && e instanceof ApiError && [404, 410].includes(e.status))
        setUnavailable(true);
    } finally {
      setBusy(false);
    }
  }
  async function upload(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    for (const key of ["image", "logo"])
      if (!(data.get(key) as File)?.size) data.delete(key);
    await perform(async () => {
      const result = await api<Job & { token: string }>(
        `/jobs?subtitle_mode=${subtitleMode}&language=${language}&model=${transcriptionModel}`,
        undefined,
        "POST",
        data,
      );
      setToken(result.token);
      setUnavailable(false);
      setJob(result);
      setDesign(result.config);
      setDirty(false);
      setDesignMethod("manual");
      setImportedDesign(false);
      setSavedDesign(false);
      setStep(subtitleMode === "generate" ? 0 : 1);
    });
  }
  function change<K extends keyof Design>(key: K, value: Design[K]) {
    setDesign((d) => (d ? { ...d, [key]: value } : d));
    setDirty(true);
    setSavedDesign(false);
  }
  async function save() {
    if (!job || !design) return;
    const result = await api<Job>(
      `/jobs/${job.id}/config`,
      token,
      "PATCH",
      JSON.stringify(design),
    );
    setJob(result);
    setDesign(result.config);
    setDirty(false);
    setSavedDesign(true);
    setRevision((r) => r + 1);
  }
  async function importDesign(file: File) {
    if (!job) return;
    if (file.size > 16384) throw new Error("Configuración demasiado grande.");
    let data: unknown;
    try {
      data = JSON.parse(await file.text());
    } catch {
      throw new Error(
        "El archivo no contiene JSON válido. Usa un diseño exportado desde EasyPodcast.",
      );
    }
    const result = await api<Job>(
      `/jobs/${job.id}/config`,
      token,
      "PATCH",
      JSON.stringify(data),
    );
    setDesign(result.config);
    setJob(result);
    setDirty(false);
    setSavedDesign(true);
    setImportedDesign(true);
    setRevision((r) => r + 1);
  }
  async function action(path: string, body?: unknown) {
    if (!job) return;
    setJob(
      await api<Job>(
        `/jobs/${job.id}/${path}`,
        token,
        "POST",
        body === undefined ? undefined : JSON.stringify(body),
      ),
    );
  }
  const disabled = busy || active || unavailable;
  function saveRetainedDesign() {
    if (!design) return;
    const url = URL.createObjectURL(
      new Blob([JSON.stringify(design, null, 2)], { type: "application/json" }),
    );
    const link = document.createElement("a");
    link.href = url;
    link.download = "easypodcast-design.json";
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  const mode =
    job?.background_mode === "openai"
      ? text.openai
      : job?.background_mode === "upload"
        ? text.uploadMode
        : text.local;

  return (
    <div className="app">
      <header>
        <a className="brand" href="/" aria-label="EasyPodcast inicio">
          <span className="mark">
            e<span>p</span>
          </span>
          {text.app}
        </a>
        <span className="local-badge">
          <i /> ESTUDIO LOCAL
        </span>
      </header>
      <main>
        <div className="intro">
          <p className="eyebrow">DEL AUDIO A LA PANTALLA</p>
          <h1>{text.tagline}</h1>
          <p>
            Convierte tu pódcast en un video con fondo, onda y subtítulos.
            <br />
            Un episodio, cuatro pasos. Tú decides el ritmo.
          </p>
        </div>
        <nav aria-label="Pasos del episodio">
          {text.steps.map((label, index) => (
            <button
              key={label}
              className={index === step ? "step current" : "step"}
              aria-current={index === step ? "step" : undefined}
              disabled={index > 0 && (!job || job.subtitles_approved === false)}
              onClick={() => setStep(index)}
            >
              <span>{String(index + 1).padStart(2, "0")}</span>
              {label}
            </button>
          ))}
        </nav>
        {error && (
          <div className="alert error" role="alert">
            {error}
          </div>
        )}
        {unavailable && (
          <div className="alert error" role="status">
            <strong>Este episodio ya no se puede procesar.</strong>
            <p>
              El servidor conserva los archivos solo hasta su vencimiento y los
              pierde al reiniciar. Una prueba que siga visible puede estar en la
              memoria del navegador. Puedes guardar el diseño y volver a cargar
              tus archivos originales.
            </p>
            <button onClick={saveRetainedDesign} disabled={!design}>
              Guardar diseño conservado (JSON)
            </button>{" "}
            <button
              onClick={() => {
                setJob(null);
                setToken("");
                setDesign(null);
                setUnavailable(false);
                setError("");
                setDirty(false);
                setStep(0);
              }}
            >
              Cargar un nuevo episodio
            </button>
          </div>
        )}
        <div className="workspace">
          <section className="panel controls">
            <div className="section-heading">
              <span className="eyebrow">PASO {step + 1} / 4</span>
              <h2 ref={heading} tabIndex={-1}>
                {text.steps[step]}
              </h2>
            </div>
            {step === 0 && !job && (
              <form onSubmit={upload}>
                <p>
                  Sube tu audio y elige generar subtítulos localmente o cargar
                  un SRT existente.
                </p>
                <label>
                  Origen de los subtítulos
                  <select
                    value={subtitleMode}
                    disabled={busy}
                    onChange={(e) =>
                      setSubtitleMode(e.target.value as "upload" | "generate")
                    }
                  >
                    <option value="upload">Ya tengo un archivo SRT</option>
                    <option
                      value="generate"
                      disabled={!caps?.transcription?.available}
                    >
                      Generar desde el audio (local)
                    </option>
                  </select>
                </label>
                {!caps?.transcription?.available && (
                  <p className="note">
                    Motor local no instalado: ejecuta npm ci dentro de la
                    carpeta transcription y reinicia EasyPodcast.
                  </p>
                )}
                {subtitleMode === "generate" && (
                  <>
                    <div className="pair">
                      <label>
                        Idioma del audio
                        <select
                          value={language}
                          disabled={busy}
                          onChange={(e) => setLanguage(e.target.value)}
                        >
                          <option value="en">Inglés</option>
                          <option value="es">Español</option>
                          <option value="auto">Detectar automáticamente</option>
                          <option value="pt">Portugués</option>
                          <option value="fr">Francés</option>
                          <option value="de">Alemán</option>
                          <option value="it">Italiano</option>
                        </select>
                      </label>
                      <label>
                        Modelo local
                        <select
                          value={transcriptionModel}
                          disabled={busy}
                          onChange={(e) =>
                            setTranscriptionModel(e.target.value)
                          }
                        >
                          <option value="tiny">Tiny · rápido</option>
                          <option value="base">
                            Base · más preciso, más lento
                          </option>
                        </select>
                      </label>
                    </div>
                    <p className="note">
                      Audio local, sin cargos de API. La primera vez se descarga
                      el modelo desde Hugging Face; se conserva en caché. Los
                      tiempos por palabra son estimados y debes revisar la
                      prueba.
                    </p>
                  </>
                )}
                <label className="file-field">
                  Audio del episodio{" "}
                  <small>
                    MP3, WAV o M4A · hasta{" "}
                    {caps
                      ? Math.round(caps.limits.audio_bytes / 1024 ** 2)
                      : 1024}{" "}
                    MiB
                  </small>
                  <input
                    name="audio"
                    type="file"
                    accept=".mp3,.wav,.m4a,audio/*"
                    required
                    disabled={busy || !!job}
                  />
                </label>
                {subtitleMode === "upload" && (
                  <label className="file-field">
                    Subtítulos <small>SRT en UTF-8 · hasta 5 MiB</small>
                    <input
                      name="srt"
                      type="file"
                      accept=".srt"
                      required
                      disabled={busy || !!job}
                    />
                  </label>
                )}
                <label>
                  Fondo propio <small>Opcional · PNG o JPEG</small>
                  <input
                    name="image"
                    type="file"
                    accept="image/png,image/jpeg"
                    disabled={busy || !!job}
                  />
                </label>
                <label>
                  Logo <small>Opcional · PNG con transparencia</small>
                  <input
                    name="logo"
                    type="file"
                    accept="image/png"
                    disabled={busy || !!job}
                  />
                </label>
                <button className="primary" disabled={busy || !!job}>
                  {busy ? text.uploading : text.upload}
                </button>
                {job && (
                  <p>Ya hay un episodio activo. Elimínalo para cargar otro.</p>
                )}
                <p className="note">{text.privacy}</p>
              </form>
            )}
            {step === 0 && job && (
              <SubtitleReview
                job={job}
                token={token}
                onChange={setJob}
                onContinue={() => setStep(1)}
              />
            )}
            {job && design && step === 1 && (
              <div className="fields">
                <DesignEntry
                  method={designMethod}
                  setMethod={setDesignMethod}
                  imported={importedDesign}
                  disabled={disabled}
                  onImport={(file) => perform(() => importDesign(file))}
                />
                {(designMethod === "manual" || importedDesign) && (
                  <>
                    <label>
                      Título
                      <input
                        value={design.title}
                        maxLength={120}
                        disabled={disabled}
                        onChange={(e) => change("title", e.target.value)}
                      />
                    </label>
                    <label>
                      Descripción visual
                      <textarea
                        value={design.description}
                        maxLength={1200}
                        disabled={disabled}
                        onChange={(e) => change("description", e.target.value)}
                      />
                    </label>
                    <div className="pair">
                      <label>
                        Estilo de imagen
                        <select
                          value={design.image_style}
                          disabled={disabled}
                          onChange={(e) =>
                            change(
                              "image_style",
                              e.target.value as Design["image_style"],
                            )
                          }
                        >
                          <option value="illustration">Ilustración</option>
                          <option value="realistic">Realista</option>
                        </select>
                      </label>
                      <label>
                        Color de onda
                        <input
                          type="color"
                          value={design.color}
                          disabled={disabled}
                          onChange={(e) => change("color", e.target.value)}
                        />
                      </label>
                    </div>
                    <label>
                      Ambiente y paleta
                      <input
                        value={design.atmosphere}
                        maxLength={300}
                        disabled={disabled}
                        onChange={(e) => change("atmosphere", e.target.value)}
                      />
                    </label>
                    <div className="pair">
                      <label>
                        Visualizador
                        <select
                          value={design.visualizer}
                          disabled={disabled}
                          onChange={(e) =>
                            change(
                              "visualizer",
                              e.target.value as Design["visualizer"],
                            )
                          }
                        >
                          <option value="waveform">Onda</option>
                          <option value="spectrum">Barras de frecuencia</option>
                        </select>
                      </label>
                      <label>
                        Sensibilidad
                        <input
                          type="number"
                          min="0.2"
                          max="4"
                          step="0.1"
                          value={design.sensitivity}
                          disabled={disabled}
                          onChange={(e) =>
                            change("sensitivity", Number(e.target.value))
                          }
                        />
                      </label>
                    </div>
                    <TypographyControls
                      design={design}
                      disabled={disabled}
                      hasLogo={job.artifacts.includes("logo")}
                      change={change}
                    />
                    {job.word_timestamps ? (
                      <div className="pair">
                        <label className="check">
                          <input
                            type="checkbox"
                            checked={design.highlight_words}
                            disabled={disabled}
                            onChange={(e) =>
                              change("highlight_words", e.target.checked)
                            }
                          />
                          Resaltar la palabra actual
                        </label>
                        <label>
                          Color de resaltado
                          <input
                            type="color"
                            value={design.highlight_color}
                            disabled={disabled}
                            onChange={(e) =>
                              change("highlight_color", e.target.value)
                            }
                          />
                        </label>
                      </div>
                    ) : (
                      <p className="note">
                        Resaltado por palabra disponible con subtítulos
                        generados desde el audio. El SRT propio conserva
                        subtítulos normales.
                      </p>
                    )}
                    <details>
                      <summary>Composición y subtítulos</summary>
                      <div className="pair">
                        <label>
                          Posición onda
                          <input
                            type="number"
                            min="0.3"
                            max="0.65"
                            step="0.01"
                            value={design.wave_y}
                            disabled={disabled}
                            onChange={(e) =>
                              change("wave_y", Number(e.target.value))
                            }
                          />
                        </label>
                        <label>
                          Altura onda
                          <input
                            type="number"
                            min="0.06"
                            max="0.22"
                            step="0.01"
                            value={design.wave_height}
                            disabled={disabled}
                            onChange={(e) =>
                              change("wave_height", Number(e.target.value))
                            }
                          />
                        </label>
                      </div>
                      <div className="pair">
                        <label>
                          Color subtítulos
                          <input
                            type="color"
                            value={design.subtitle_color}
                            disabled={disabled}
                            onChange={(e) =>
                              change("subtitle_color", e.target.value)
                            }
                          />
                        </label>
                      </div>
                      <div className="pair">
                        <label>
                          Margen inferior
                          <input
                            type="number"
                            min="40"
                            max="180"
                            value={design.subtitle_margin}
                            disabled={disabled}
                            onChange={(e) =>
                              change("subtitle_margin", Number(e.target.value))
                            }
                          />
                        </label>
                        <label>
                          Contorno
                          <input
                            type="number"
                            min="1"
                            max="6"
                            value={design.outline}
                            disabled={disabled}
                            onChange={(e) =>
                              change("outline", Number(e.target.value))
                            }
                          />
                        </label>
                      </div>
                      <label>
                        Ancho subtítulos
                        <input
                          type="number"
                          min="0.5"
                          max="0.9"
                          step="0.05"
                          value={design.subtitle_width}
                          disabled={disabled}
                          onChange={(e) =>
                            change("subtitle_width", Number(e.target.value))
                          }
                        />
                      </label>
                      <label>
                        Máximo de líneas
                        <select
                          value={design.max_lines}
                          disabled={disabled}
                          onChange={(e) =>
                            change("max_lines", Number(e.target.value))
                          }
                        >
                          <option value="2">Dos líneas</option>
                          <option value="3">Tres líneas</option>
                        </select>
                      </label>
                      <label>
                        Preset CPU
                        <select
                          value={design.preset}
                          disabled={disabled}
                          onChange={(e) =>
                            change("preset", e.target.value as Design["preset"])
                          }
                        >
                          <option>veryfast</option>
                          <option>fast</option>
                          <option>medium</option>
                          <option>ultrafast</option>
                        </select>
                      </label>
                      <label>
                        Calidad CRF (menor = más calidad)
                        <input
                          type="number"
                          min="18"
                          max="28"
                          value={design.crf}
                          disabled={disabled}
                          onChange={(e) =>
                            change("crf", Number(e.target.value))
                          }
                        />
                      </label>
                    </details>
                    <label className="check">
                      <input
                        type="checkbox"
                        checked={design.trim_subtitles}
                        disabled={disabled}
                        onChange={(e) =>
                          change("trim_subtitles", e.target.checked)
                        }
                      />
                      Autorizar recorte de subtítulos que exceden el audio
                    </label>
                    <DesignActions
                      dirty={dirty}
                      disabled={disabled}
                      saved={savedDesign}
                      disabledMessage={
                        unavailable
                          ? "El episodio ya no está disponible. Carga de nuevo tus archivos."
                          : undefined
                      }
                      onSave={() => perform(save)}
                      onContinue={() =>
                        perform(async () => {
                          await action("background/approve");
                          setStep(2);
                        })
                      }
                    />
                    <div className="ai-box">
                      <h3>Opcional: generar otro fondo con IA</h3>
                      <p>
                        La IA recibe título, descripción y ajustes visuales.
                        Tiene costes externos. No recibe tu audio ni SRT.
                      </p>
                      <button
                        disabled={disabled || dirty || !caps?.image_provider}
                        onClick={() => perform(() => action("background"))}
                      >
                        Generar imagen con IA
                      </button>
                      {!caps?.image_provider && (
                        <small>
                          IA opcional: falta configurar el proveedor en el
                          backend.
                        </small>
                      )}
                    </div>
                  </>
                )}
              </div>
            )}
            {job && step === 2 && (
              <div className="fields">
                <p>
                  Renderiza hasta 20 segundos. Esta prueba es la referencia
                  final de composición, sonido y subtítulos.
                </p>
                <label>
                  Inicio de la prueba (segundos)
                  <input
                    type="number"
                    min="0"
                    max={Math.max(0, job.metadata.duration - 0.01)}
                    step="0.1"
                    value={start}
                    disabled={disabled}
                    onChange={(e) => setStart(Number(e.target.value))}
                  />
                </label>
                <button
                  className="primary"
                  disabled={disabled || dirty || !job.background_approved}
                  onClick={() => perform(() => action("preview", { start }))}
                >
                  Crear prueba de 20 segundos
                </button>
                {job.artifacts.includes("preview") && !active && (
                  <button
                    disabled={disabled || dirty}
                    onClick={() =>
                      perform(async () => {
                        await action("preview/approve");
                        setStep(3);
                      })
                    }
                  >
                    Aprobar prueba y continuar →
                  </button>
                )}
                <button onClick={() => setStep(1)}>← Ajustar diseño</button>
              </div>
            )}
            {job && step === 3 && !unavailable && (
              <div className="fields">
                <p>
                  Exporta el episodio completo con el diseño de tu prueba
                  aprobada.
                </p>
                <div className="output-spec">
                  MP4{" "}
                  <span>
                    1920 × 1080 · 30 fps
                    <br />
                    H.264 + AAC
                  </span>
                </div>
                <button
                  className="primary"
                  disabled={disabled || dirty || !job.preview_approved}
                  onClick={() => perform(() => action("render"))}
                >
                  Renderizar episodio
                </button>
                {job.artifacts.includes("video") && !active && (
                  <a
                    className="button primary"
                    href={artifactUrl(job, "video", true, revision)}
                  >
                    Descargar MP4
                  </a>
                )}
                <a
                  className="button"
                  href={artifactUrl(job, "background", true, revision)}
                >
                  Descargar fondo
                </a>
                <a className="button" href={artifactUrl(job, "config", true)}>
                  Descargar diseño JSON
                </a>
                <p className="note">
                  Las descargas de video se transmiten directamente al
                  navegador, sin cargar el MP4 completo en memoria.
                </p>
              </div>
            )}
          </section>
          <section className="preview-panel" aria-label="Previsualización">
            <div className="preview-top">
              <span>LIENZO DEL EPISODIO</span>
              <span>16:9 / 1080p</span>
            </div>
            <div className="canvas">
              {job && !active ? (
                <>
                  {job.artifacts.includes("preview") && step >= 2 ? (
                    <video
                      key={revision}
                      controls
                      preload="metadata"
                      src={artifactUrl(job, "preview", false, revision)}
                    />
                  ) : (
                    <>
                      <img
                        src={artifactUrl(job, "background", false, revision)}
                        alt="Fondo actual del episodio"
                      />
                      <div
                        className="canvas-title"
                        style={{
                          fontFamily:
                            fontFamilies[design?.title_font ?? "sans"],
                          fontSize: `${(design?.title_font_size ?? 64) / 19.2}cqw`,
                          fontWeight: (design?.title_bold ?? true) ? 700 : 400,
                        }}
                      >
                        {design?.title}
                      </div>
                      {design && job.artifacts.includes("logo") && (
                        <img
                          className="canvas-logo"
                          src={artifactUrl(job, "logo", false, revision)}
                          alt="Logo del episodio"
                          style={logoStyle(design)}
                        />
                      )}
                      <div className="safe-area">
                        Zona del visualizador · se renderiza con tu audio
                      </div>
                      <div
                        className="sample-caption"
                        style={{
                          fontFamily:
                            fontFamilies[design?.subtitle_font ?? "sans"],
                          fontSize: `${(design?.font_size ?? 48) / 19.2}cqw`,
                          bottom: `${(design?.subtitle_margin ?? 80) / 10.8}%`,
                        }}
                      >
                        Vista de composición aproximada
                      </div>
                    </>
                  )}
                </>
              ) : (
                <div className="empty-canvas">
                  <div className="sound-symbol">ııⅠııⅠıı</div>
                  <h3>
                    {job
                      ? "Tu episodio está en proceso"
                      : "Aquí empieza tu próximo episodio"}
                  </h3>
                  <p>
                    {job
                      ? "El progreso aparece abajo."
                      : "Añade audio y subtítulos para preparar el lienzo."}
                  </p>
                </div>
              )}
            </div>
            <div className="canvas-footer">
              <span>{job ? mode : "Sin archivos cargados"}</span>
              <span>
                {job
                  ? `${job.metadata.duration.toFixed(1)} s · ${job.metadata.codec.toUpperCase()}`
                  : "VISTA PREVIA"}
              </span>
            </div>
            {job && (
              <div className="job-status" aria-live="polite">
                <div className="status-line">
                  <strong>
                    {unavailable ? "Episodio no disponible" : job.phase}
                  </strong>
                  {active && (
                    <button
                      disabled={busy}
                      onClick={() => perform(() => action("cancel"))}
                    >
                      Cancelar
                    </button>
                  )}
                </div>
                {!unavailable && job.progress !== null && (
                  <>
                    <progress value={job.progress} max="1" />
                    <span>{Math.floor(job.progress * 100)} %</span>
                  </>
                )}
                {job.error && <p className="error-text">{job.error}</p>}
                {job.warnings.length > 0 && (
                  <details open>
                    <summary>Observaciones ({job.warnings.length})</summary>
                    <ul>
                      {job.warnings.map((w, i) => (
                        <li key={i}>{w}</li>
                      ))}
                    </ul>
                  </details>
                )}
                <p className="note">
                  Vence: {new Date(job.expires_at).toLocaleString("es")}. Al
                  reiniciar el backend se pierden los trabajos.
                </p>
                <button
                  className="danger"
                  disabled={busy}
                  onClick={() =>
                    perform(async () => {
                      await api(`/jobs/${job.id}`, token, "DELETE");
                      setJob(null);
                      setToken("");
                      setDesign(null);
                      setStep(0);
                    })
                  }
                >
                  Eliminar episodio y archivos
                </button>
              </div>
            )}
            <details className="diagnostics">
              <summary>
                <span className={caps?.render_ready ? "dot ready" : "dot"} />
                {caps?.render_ready
                  ? "Motor audiovisual listo"
                  : "Diagnóstico de dependencias"}
              </summary>
              {caps ? (
                <>
                  <div className="chips">
                    {Object.entries({
                      FFmpeg: caps.ffmpeg,
                      FFprobe: caps.ffprobe,
                      H264: caps.h264,
                      AAC: caps.aac,
                      Fuente: caps.font,
                      ...caps.filters,
                    }).map(([key, ok]) => (
                      <span key={key}>
                        {ok ? "✓" : "×"} {key}
                      </span>
                    ))}
                  </div>
                  <p>
                    Límite de producto: {caps.limits.duration_seconds / 60} min
                    · un render simultáneo · {caps.limits.queue} en cola.
                    Benchmark sintético de 30 min disponible en la
                    documentación; 120 min aún sin verificar.
                  </p>
                </>
              ) : (
                <p>Conectando al backend…</p>
              )}
            </details>
          </section>
        </div>
      </main>
      <footer>
        Hecho para escuchar. Diseñado para compartir.
        <span>EasyPodcast · 0.4.1</span>
      </footer>
    </div>
  );
}

const mount = document.getElementById("root");
if (mount)
  createRoot(mount).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
  );
