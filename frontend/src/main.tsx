import { flushDrafts } from "./drafts";
import {
  ProjectLibrary,
  resumeStep,
  DraftAutosave,
  BrandTemplates,
} from "./ProjectLibrary";
import { Preflight } from "./Preflight";
import { CanvasEditor, frameSize } from "./CanvasEditor";
import { t } from "./i18n";
import { ThemeSelector } from "./ThemeSelector";
import { DesignEntry } from "./DesignEntry";
import { DesignActions } from "./DesignActions";
import React, { useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import { api, artifactUrl, isActive, ApiError } from "./api";
import type { Capabilities, Design, Job } from "./types";
import { getText } from "./text";
import { LanguageSelector } from "./LanguageSelector";
import { useLocale, setLocale } from "./i18n";
import "./style.css";
import { TypographyControls } from "./TypographyControls";
import { SubtitleReview } from "./SubtitleReview";

/** Own the current job, token, editable design and four-step workflow; subscribe to UI locale changes. */
export function App() {
  const locale = useLocale();
  const text = getText();
  useEffect(() => {
    setLocale(locale);
  }, [locale]);
  const [libraryRevision, setLibraryRevision] = useState(0);
  const [editingSubtitles, setEditingSubtitles] = useState(false);
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

  /** Run an async action with busy/error feedback and recognize an unavailable job. */
  async function perform(action: () => Promise<void>) {
    setBusy(true);
    setError("");
    try {
      await action();
    } catch (e) {
      setError(e instanceof Error ? e.message : t("Error inesperado."));
      if (job && e instanceof ApiError && [404, 410].includes(e.status))
        setUnavailable(true);
    } finally {
      setBusy(false);
    }
  }
  /** Submit selected File objects as multipart data and enter design or subtitle review. */
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
      setLibraryRevision((n) => n + 1);
      setUnavailable(false);
      setJob(result);
      setDesign(result.config);
      setDirty(false);
      setDesignMethod("manual");
      setImportedDesign(false);
      setSavedDesign(false);
      setStart(0);
      setStep(subtitleMode === "generate" ? 0 : 1);
    });
  }
  /** Update one draft Design field and mark it unsaved without contacting the backend. */
  function change<K extends keyof Design>(key: K, value: Design[K]) {
    setDesign((d) => (d ? { ...d, [key]: value } : d));
    setDirty(true);
    setSavedDesign(false);
  }
  /** Persist the complete Design and refresh the job snapshot only after success. */
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
    setLibraryRevision((n) => n + 1);
    setRevision((r) => r + 1);
  }
  /** Read a bounded design JSON, validate it through the backend and retain the previous design on failure. */
  async function importDesign(file: File) {
    if (!job) return;
    if (file.size > 16384)
      throw new Error(t("Configuración demasiado grande."));
    let data: unknown;
    try {
      data = JSON.parse(await file.text());
    } catch {
      throw new Error(
        t(
          "El archivo no contiene JSON válido. Usa un diseño exportado desde EasyPodcast.",
        ),
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
  /** POST one authenticated operation and replace the local job snapshot. */
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
  /** Download the in-memory design without needing an available backend job. */
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
        <a className="brand" href="/" aria-label={t("EasyPodcast inicio")}>
          <span className="mark">
            {" "}
            {t("e")}
            <span>{t("p")}</span>
          </span>
          {text.app}
        </a>
        <div className="header-tools">
          <LanguageSelector />
          <ThemeSelector />
          <span className="local-badge">
            <i /> {t("ESTUDIO LOCAL")}{" "}
          </span>
        </div>
      </header>
      <main>
        <div className="intro">
          <p className="eyebrow">{t("DEL AUDIO A LA PANTALLA")}</p>
          <h1>{text.tagline}</h1>
          <p>
            {" "}
            {t(
              "Convierte tu pódcast en un video con fondo, onda y subtítulos.",
            )}{" "}
            <br /> {t("Un episodio, cuatro pasos. Tú decides el ritmo.")}{" "}
          </p>
        </div>
        <nav aria-label={t("Pasos del episodio")}>
          {text.steps.map((label, index) => (
            <button
              key={label}
              className={index === step ? "step current" : "step"}
              aria-current={index === step ? "step" : undefined}
              disabled={index > 0 && (!job || job.subtitles_approved === false)}
              onClick={() => {
                void flushDrafts()
                  .then(() => setStep(index))
                  .catch((e) => setError(e.message));
              }}
            >
              <span>{String(index + 1).padStart(2, "0")}</span>
              {label}
            </button>
          ))}
        </nav>
        <ProjectLibrary
          disabled={busy || active}
          revision={libraryRevision}
          beforeOpen={flushDrafts}
          onTrashed={(id) => {
            if (job?.project_id === id) {
              setJob(null);
              setToken("");
              setDesign(null);
              setDirty(false);
              setStep(0);
            }
          }}
          onOpen={(result) => {
            setJob(result);
            setToken(result.token);
            setDesign(result.config);
            setDirty(false);
            setUnavailable(false);
            setSavedDesign(false);
            setDesignMethod("manual");
            setImportedDesign(false);
            setEditingSubtitles(!!result.subtitle_draft_available);
            setStart(0);
            setRevision((n) => n + 1);
            setStep(resumeStep(result));
          }}
        />
        {job && design && (
          <DraftAutosave job={job} design={design} dirty={dirty} />
        )}
        {error && (
          <div className="alert error" role="alert">
            {t(error)}
          </div>
        )}
        {unavailable && (
          <div className="alert error" role="status">
            <strong>{t("Este episodio ya no se puede procesar.")}</strong>
            <p>
              {" "}
              {t(
                "El servidor conserva los archivos solo hasta su vencimiento y los pierde al reiniciar. Una prueba que siga visible puede estar en la memoria del navegador. Puedes guardar el diseño y volver a cargar tus archivos originales.",
              )}{" "}
            </p>
            <button onClick={saveRetainedDesign} disabled={!design}>
              {" "}
              {t("Guardar diseño conservado (JSON)")}{" "}
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
              {" "}
              {t("Cargar un nuevo episodio")}{" "}
            </button>
          </div>
        )}
        <div className="workspace">
          <section className="panel controls">
            <div className="section-heading">
              <span className="eyebrow">
                {t("PASO")} {step + 1} {t("/ 4")}
              </span>
              <h2 ref={heading} tabIndex={-1}>
                {text.steps[step]}
              </h2>
            </div>
            {step === 0 && !job && (
              <form onSubmit={upload}>
                <p>
                  {" "}
                  {t(
                    "Sube tu audio y elige generar subtítulos localmente o cargar un SRT existente.",
                  )}{" "}
                </p>
                <label>
                  {" "}
                  {t("Origen de los subtítulos")}{" "}
                  <select
                    value={subtitleMode}
                    disabled={busy}
                    onChange={(e) =>
                      setSubtitleMode(e.target.value as "upload" | "generate")
                    }
                  >
                    <option value="upload">
                      {t("Ya tengo un archivo SRT")}
                    </option>
                    <option
                      value="generate"
                      disabled={!caps?.transcription?.available}
                    >
                      {" "}
                      {t("Generar desde el audio (local)")}{" "}
                    </option>
                  </select>
                </label>
                {!caps?.transcription?.available && (
                  <p className="note">
                    {" "}
                    {t(
                      "Motor local no instalado: ejecuta npm ci dentro de la carpeta transcription y reinicia EasyPodcast.",
                    )}{" "}
                  </p>
                )}
                {subtitleMode === "generate" && (
                  <>
                    <div className="pair">
                      <label>
                        {" "}
                        {t("Idioma del audio")}{" "}
                        <select
                          value={language}
                          disabled={busy}
                          onChange={(e) => setLanguage(e.target.value)}
                        >
                          <option value="en">{t("Inglés")}</option>
                          <option value="es">{t("Español")}</option>
                          <option value="auto">
                            {t("Detectar automáticamente")}
                          </option>
                          <option value="pt">{t("Portugués")}</option>
                          <option value="fr">{t("Francés")}</option>
                          <option value="de">{t("Alemán")}</option>
                          <option value="it">{t("Italiano")}</option>
                        </select>
                      </label>
                      <label>
                        {" "}
                        {t("Modelo local")}{" "}
                        <select
                          value={transcriptionModel}
                          disabled={busy}
                          onChange={(e) =>
                            setTranscriptionModel(e.target.value)
                          }
                        >
                          <option value="tiny">{t("Tiny · rápido")}</option>
                          <option value="base">
                            {" "}
                            {t("Base · más preciso, más lento")}{" "}
                          </option>
                        </select>
                      </label>
                    </div>
                    <p className="note">
                      {" "}
                      {t(
                        "Audio local, sin cargos de API. La primera vez se descarga el modelo desde Hugging Face; se conserva en caché. Los tiempos por palabra son estimados y debes revisar la prueba.",
                      )}{" "}
                    </p>
                  </>
                )}
                <label className="file-field">
                  {" "}
                  {t("Audio del episodio")}{" "}
                  <small>
                    {" "}
                    {t("MP3, WAV o M4A · hasta")}{" "}
                    {caps
                      ? Math.round(caps.limits.audio_bytes / 1024 ** 2)
                      : 1024}{" "}
                    {t("MiB")}{" "}
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
                    {" "}
                    {t("Subtítulos")}{" "}
                    <small>{t("SRT en UTF-8 · hasta 5 MiB")}</small>
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
                  {" "}
                  {t("Fondo propio")}{" "}
                  <small>{t("Opcional · PNG o JPEG")}</small>
                  <input
                    name="image"
                    type="file"
                    accept="image/png,image/jpeg"
                    disabled={busy || !!job}
                  />
                </label>
                <label>
                  {" "}
                  {t("Logo")}{" "}
                  <small>{t("Opcional · PNG con transparencia")}</small>
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
                  <p>
                    {t(
                      "Ya hay un episodio activo. Elimínalo para cargar otro.",
                    )}
                  </p>
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
                <label>
                  {t("Output format")}
                  <select
                    value={design.output_format ?? "landscape"}
                    disabled={disabled}
                    onChange={(e) =>
                      change(
                        "output_format",
                        e.target.value as Design["output_format"],
                      )
                    }
                  >
                    <option value="landscape">16:9 · 1920 × 1080</option>
                    <option value="portrait">9:16 · 1080 × 1920</option>
                    <option value="square">1:1 · 1080 × 1080</option>
                  </select>
                </label>
                <p className="note">
                  {t(
                    "Drag the title or logo on the canvas. Use arrow keys for precise moves. Resize the title with its corner handle; adjust logo scale below.",
                  )}
                </p>
                <BrandTemplates
                  job={job}
                  token={token}
                  dirty={dirty}
                  disabled={disabled}
                  onChange={(result) => {
                    setJob(result);
                    setDesign(result.config);
                    setDirty(false);
                    setRevision((n) => n + 1);
                  }}
                />
                <button
                  disabled={disabled}
                  onClick={() => {
                    void flushDrafts()
                      .then(() => setEditingSubtitles((v) => !v))
                      .catch((e) => setError(e.message));
                  }}
                >
                  {t("Review or edit subtitles")}
                </button>
                {editingSubtitles && (
                  <SubtitleReview
                    job={job}
                    token={token}
                    onChange={setJob}
                    onContinue={() => setEditingSubtitles(false)}
                  />
                )}

                {(designMethod === "manual" || importedDesign) && (
                  <>
                    <label>
                      {" "}
                      {t("Título")}{" "}
                      <input
                        value={design.title}
                        maxLength={120}
                        disabled={disabled}
                        onChange={(e) => change("title", e.target.value)}
                      />
                    </label>
                    <label>
                      {" "}
                      {t("Descripción visual")}{" "}
                      <textarea
                        value={design.description}
                        maxLength={1200}
                        disabled={disabled}
                        onChange={(e) => change("description", e.target.value)}
                      />
                    </label>
                    <div className="pair">
                      <label>
                        {" "}
                        {t("Estilo de imagen")}{" "}
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
                          <option value="illustration">
                            {t("Ilustración")}
                          </option>
                          <option value="realistic">{t("Realista")}</option>
                        </select>
                      </label>
                      <label>
                        {" "}
                        {t("Color de onda")}{" "}
                        <input
                          type="color"
                          value={design.color}
                          disabled={disabled}
                          onChange={(e) => change("color", e.target.value)}
                        />
                      </label>
                    </div>
                    <label>
                      {" "}
                      {t("Ambiente y paleta")}{" "}
                      <input
                        value={design.atmosphere}
                        maxLength={300}
                        disabled={disabled}
                        onChange={(e) => change("atmosphere", e.target.value)}
                      />
                    </label>
                    <div className="pair">
                      <label>
                        {" "}
                        {t("Visualizador")}{" "}
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
                          <option value="waveform">{t("Onda")}</option>
                          <option value="spectrum">
                            {t("Barras de frecuencia")}
                          </option>
                        </select>
                      </label>
                      <label>
                        {" "}
                        {t("Sensibilidad")}{" "}
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
                          />{" "}
                          {t("Resaltar la palabra actual")}{" "}
                        </label>
                        <label>
                          {" "}
                          {t("Color de resaltado")}{" "}
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
                        {" "}
                        {t(
                          "Resaltado por palabra disponible con subtítulos generados desde el audio. El SRT propio conserva subtítulos normales.",
                        )}{" "}
                      </p>
                    )}
                    <details>
                      <summary>{t("Composición y subtítulos")}</summary>
                      <div className="pair">
                        <label>
                          {" "}
                          {t("Posición onda")}{" "}
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
                          {" "}
                          {t("Altura onda")}{" "}
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
                          {" "}
                          {t("Color subtítulos")}{" "}
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
                          {" "}
                          {t("Margen inferior")}{" "}
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
                          {" "}
                          {t("Contorno")}{" "}
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
                        {" "}
                        {t("Ancho subtítulos")}{" "}
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
                        {" "}
                        {t("Máximo de líneas")}{" "}
                        <select
                          value={design.max_lines}
                          disabled={disabled}
                          onChange={(e) =>
                            change("max_lines", Number(e.target.value))
                          }
                        >
                          <option value="2">{t("Dos líneas")}</option>
                          <option value="3">{t("Tres líneas")}</option>
                        </select>
                      </label>
                      <label>
                        {" "}
                        {t("Preset CPU")}{" "}
                        <select
                          value={design.preset}
                          disabled={disabled}
                          onChange={(e) =>
                            change("preset", e.target.value as Design["preset"])
                          }
                        >
                          <option>{t("veryfast")}</option>
                          <option>{t("fast")}</option>
                          <option>{t("medium")}</option>
                          <option>{t("ultrafast")}</option>
                        </select>
                      </label>
                      <label>
                        {" "}
                        {t("Calidad CRF (menor = más calidad)")}{" "}
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
                      />{" "}
                      {t(
                        "Autorizar recorte de subtítulos que exceden el audio",
                      )}{" "}
                    </label>
                    <DesignActions
                      dirty={dirty}
                      disabled={disabled}
                      saved={savedDesign}
                      disabledMessage={
                        unavailable
                          ? t(
                              "El episodio ya no está disponible. Carga de nuevo tus archivos.",
                            )
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
                      <h3>{t("Opcional: generar otro fondo con IA")}</h3>
                      <p>
                        {" "}
                        {t(
                          "La IA recibe título, descripción y ajustes visuales. Tiene costes externos. No recibe tu audio ni SRT.",
                        )}{" "}
                      </p>
                      <button
                        disabled={disabled || dirty || !caps?.image_provider}
                        onClick={() => perform(() => action("background"))}
                      >
                        {" "}
                        {t("Generar imagen con IA")}{" "}
                      </button>
                      {!caps?.image_provider && (
                        <small>
                          {" "}
                          {t(
                            "IA opcional: falta configurar el proveedor en el backend.",
                          )}{" "}
                        </small>
                      )}
                    </div>
                  </>
                )}
              </div>
            )}
            {job && step === 2 && (
              <div className="fields">
                <Preflight job={job} token={token} dirty={dirty} />
                <p>
                  {" "}
                  {t(
                    "Renderiza hasta 20 segundos. Esta prueba es la referencia final de composición, sonido y subtítulos.",
                  )}{" "}
                </p>
                <label>
                  {" "}
                  {t("Inicio de la prueba (segundos)")}{" "}
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
                  {" "}
                  {t("Crear prueba de 20 segundos")}{" "}
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
                    {" "}
                    {t("Aprobar prueba y continuar →")}{" "}
                  </button>
                )}
                <button onClick={() => setStep(1)}>
                  {t("← Ajustar diseño")}
                </button>
              </div>
            )}
            {job && step === 3 && !unavailable && (
              <div className="fields">
                <p>
                  {" "}
                  {t(
                    "Exporta el episodio completo con el diseño de tu prueba aprobada.",
                  )}{" "}
                </p>
                <Preflight job={job} token={token} dirty={dirty} />
                <div className="output-spec">
                  {" "}
                  {t("MP4")}{" "}
                  <span>
                    {" "}
                    {frameSize(design).join(" × ")} · 30 fps <br />{" "}
                    {t("H.264 + AAC")}{" "}
                  </span>
                </div>
                <button
                  className="primary"
                  disabled={disabled || dirty || !job.preview_approved}
                  onClick={() => perform(() => action("render"))}
                >
                  {" "}
                  {t("Renderizar episodio")}{" "}
                </button>
                {job.artifacts.includes("video") && !active && (
                  <a
                    className="button primary"
                    href={artifactUrl(job, "video", true, revision)}
                  >
                    {" "}
                    {t("Descargar MP4")}{" "}
                  </a>
                )}
                <a
                  className="button"
                  href={artifactUrl(job, "subtitles", true)}
                >
                  {t("Descargar SRT")}
                </a>
                <a
                  className="button"
                  href={artifactUrl(job, "background", true, revision)}
                >
                  {" "}
                  {t("Descargar fondo")}{" "}
                </a>
                <a className="button" href={artifactUrl(job, "config", true)}>
                  {" "}
                  {t("Descargar diseño JSON")}{" "}
                </a>
                <p className="note">
                  {" "}
                  {t(
                    "Las descargas de video se transmiten directamente al navegador, sin cargar el MP4 completo en memoria.",
                  )}{" "}
                </p>
              </div>
            )}
          </section>
          <section className="preview-panel" aria-label={t("Previsualización")}>
            <div className="preview-top">
              <span>{t("LIENZO DEL EPISODIO")}</span>
              <span>{frameSize(design).join(" × ")}</span>
            </div>
            <div
              className="canvas"
              data-format={design?.output_format ?? "landscape"}
              style={{ aspectRatio: frameSize(design).join(" / ") }}
            >
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
                      {design && (
                        <CanvasEditor
                          job={job}
                          design={design}
                          revision={revision}
                          disabled={disabled || step !== 1}
                          change={change}
                        />
                      )}
                    </>
                  )}
                </>
              ) : (
                <div className="empty-canvas">
                  <div className="sound-symbol">{t("ııⅠııⅠıı")}</div>
                  <h3>
                    {job
                      ? t("Tu episodio está en proceso")
                      : t("Aquí empieza tu próximo episodio")}
                  </h3>
                  <p>
                    {job
                      ? t("El progreso aparece abajo.")
                      : t("Añade audio y subtítulos para preparar el lienzo.")}
                  </p>
                </div>
              )}
            </div>
            <div className="canvas-footer">
              <span>{job ? mode : t("Sin archivos cargados")}</span>
              <span>
                {job
                  ? `${job.metadata.duration.toFixed(1)} s · ${job.metadata.codec.toUpperCase()}`
                  : t("VISTA PREVIA")}
              </span>
            </div>
            {job && (
              <div className="job-status" aria-live="polite">
                <div className="status-line">
                  <strong>
                    {unavailable ? t("Episodio no disponible") : t(job.phase)}
                  </strong>
                  {active && (
                    <button
                      disabled={busy}
                      onClick={() => perform(() => action("cancel"))}
                    >
                      {" "}
                      {t("Cancelar")}{" "}
                    </button>
                  )}
                </div>
                {!unavailable && job.progress !== null && (
                  <>
                    <progress value={job.progress} max="1" />
                    <span>
                      {Math.floor(job.progress * 100)} {t("%")}
                    </span>
                  </>
                )}
                {job.error && <p className="error-text">{t(job.error)}</p>}
                {job.warnings.length > 0 && (
                  <details open>
                    <summary>
                      {t("Observaciones (")}
                      {job.warnings.length}
                      {t(")")}
                    </summary>
                    <ul>
                      {job.warnings.map((w, i) => (
                        <li key={i}>{t(w)}</li>
                      ))}
                    </ul>
                  </details>
                )}
                <p className="note">
                  {" "}
                  {t("Vence:")}{" "}
                  {new Date(job.expires_at).toLocaleString(
                    locale === "en" ? "en-US" : "es-ES",
                  )}
                  {t(
                    ". Temporary session expires; saved projects remain in the Library.",
                  )}{" "}
                </p>
                <button
                  className="danger"
                  disabled={busy}
                  onClick={() =>
                    perform(async () => {
                      await flushDrafts();
                      await api(`/jobs/${job.id}`, token, "DELETE");
                      setJob(null);
                      setToken("");
                      setDesign(null);
                      setStep(0);
                      setLibraryRevision((n) => n + 1);
                    })
                  }
                >
                  {" "}
                  {t("Close episode (saved project stays in Library)")}{" "}
                </button>
              </div>
            )}
            <details className="diagnostics">
              <summary>
                <span className={caps?.render_ready ? "dot ready" : "dot"} />
                {caps?.render_ready
                  ? t("Motor audiovisual listo")
                  : t("Diagnóstico de dependencias")}
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
                        {ok ? t("✓") : "×"} {key}
                      </span>
                    ))}
                  </div>
                  <p>
                    {" "}
                    {t("Límite de producto:")}{" "}
                    {caps.limits.duration_seconds / 60}{" "}
                    {t("min · un render simultáneo ·")} {caps.limits.queue}{" "}
                    {t(
                      "en cola. Benchmark sintético de 30 min disponible en la documentación; 120 min aún sin verificar.",
                    )}{" "}
                  </p>
                </>
              ) : (
                <p>{t("Conectando al backend…")}</p>
              )}
            </details>
          </section>
        </div>
      </main>
      <footer>
        {" "}
        {t("Hecho para escuchar. Diseñado para compartir.")}{" "}
        <span>{t("EasyPodcast · 0.6.0")}</span>
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
