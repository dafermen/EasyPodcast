import { LibraryTools, storageSize } from "./LibraryTools";
import { registerDraft } from "./drafts";
import { useEffect, useState, useRef } from "react";
import { api } from "./api";
import { t, getLocale } from "./i18n";
import type { Job, Design } from "./types";
export interface ProjectSummary {
  id: string;
  title: string;
  created: number;
  updated: number;
  state: string;
  has_draft: boolean;
  bytes?: number;
}
/** Resume at the latest review/export stage that still has valid artifacts and approvals. */
export function resumeStep(job: Job) {
  if (job.subtitle_draft_available) return 0;
  if (!job.subtitles_approved) return 0;
  if (job.preview_approved && job.artifacts.includes("video")) return 3;
  if (job.background_approved && job.artifacts.includes("preview")) return 2;
  return 1;
}
/** Durable local project browser. Job tokens returned on open remain in React memory. */
export function ProjectLibrary({
  onOpen,
  disabled,
  revision = 0,
  beforeOpen,
  onTrashed,
}: {
  onOpen: (job: Job & { token: string }) => void;
  disabled: boolean;
  revision?: number;
  beforeOpen?: () => Promise<void>;
  onTrashed?: (id: string) => void;
}) {
  const [query, setQuery] = useState("");
  const [sort, setSort] = useState("updated");
  const details = useRef<HTMLDetailsElement>(null);
  const [items, setItems] = useState<ProjectSummary[]>([]);
  const [error, setError] = useState("");
  const [working, setWorking] = useState(false);
  const [reload, setReload] = useState(0);
  useEffect(() => {
    let current = true;
    api<{ ready: boolean }>("/library/session", undefined, "POST")
      .then(() => api<ProjectSummary[]>("/projects"))
      .then((data) => {
        if (current) setItems(Array.isArray(data) ? data : []);
      })
      .catch((e) => {
        if (current) setError(e.message);
      });
    return () => {
      current = false;
    };
  }, [reload, revision]);
  /** Flush the current draft and request an authenticated saved-project reopen or duplication. */
  async function open(id: string, duplicate = false) {
    setWorking(true);
    setError("");
    try {
      await beforeOpen?.();
      onOpen(
        await api<Job & { token: string }>(
          `/projects/${id}/${duplicate ? "duplicate" : "open"}`,
          undefined,
          "POST",
        ),
      );
      if (details.current) details.current.open = false;
      setReload((n) => n + 1);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not open project.");
    } finally {
      setWorking(false);
    }
  }
  return (
    <details className="project-library" ref={details}>
      <summary>
        {t("Project library")} · {items.length}
      </summary>
      <p className="note">
        {t(
          "Saved projects survive browser reloads and backend restarts. Open creates a fresh editing session.",
        )}
      </p>
      <button
        type="button"
        onClick={() => setReload((n) => n + 1)}
        disabled={working}
      >
        {t("Refresh library")}
      </button>
      {error && <p role="alert">{t(error)}</p>}
      <label>
        {t("Search projects")}
        <input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </label>
      <label>
        {t("Sort projects")}
        <select value={sort} onChange={(e) => setSort(e.target.value)}>
          <option value="updated">{t("Recently updated")}</option>
          <option value="title">{t("Name")}</option>
          <option value="bytes">{t("Largest first")}</option>
        </select>
      </label>
      <LibraryTools
        projects={items}
        beforeAction={beforeOpen}
        onTrashed={onTrashed}
        disabled={disabled || working}
        onChanged={() => setReload((n) => n + 1)}
      />
      <div className="project-grid">
        {items
          .filter((item) =>
            item.title.toLocaleLowerCase().includes(query.toLocaleLowerCase()),
          )
          .sort((a, b) =>
            sort === "title"
              ? a.title.localeCompare(b.title)
              : sort === "bytes"
                ? (b.bytes || 0) - (a.bytes || 0)
                : b.updated - a.updated,
          )
          .map((item) => (
            <article key={item.id} className="project-card">
              <img
                src={`/api/projects/${item.id}/thumbnail`}
                alt=""
                loading="lazy"
              />
              <div>
                <strong>{item.title}</strong>
                <p className="note">
                  {new Date(item.updated * 1000).toLocaleString(
                    getLocale() === "en" ? "en-US" : "es-ES",
                  )}{" "}
                  · {t(item.state)} · {storageSize(item.bytes)}
                  {item.has_draft ? ` · ${t("Recovery draft available")}` : ""}
                </p>
                <button
                  disabled={disabled || working}
                  onClick={() => open(item.id)}
                >
                  {t("Continue project")}
                </button>{" "}
                <button
                  disabled={disabled || working}
                  onClick={() => open(item.id, true)}
                >
                  {t("Duplicate")}
                </button>
              </div>
            </article>
          ))}
      </div>
      {!items.length && (
        <p>{t("Your saved episodes will appear here after upload.")}</p>
      )}
    </details>
  );
}
/** Debounced recovery copy; it never silently approves or replaces the live configuration. */
export function DraftAutosave({
  job,
  design,
  dirty,
}: {
  job: Job;
  design: Design | null;
  dirty: boolean;
}) {
  const [status, setStatus] = useState("");
  const baseVersion = JSON.stringify(job.config);
  const draftVersion = JSON.stringify(design);
  useEffect(() => {
    if (!job.project_id || !design || !dirty) {
      setStatus("");
      return;
    }
    let current = true;
    setStatus("Saving recovery draft…");
    const flush = () => {
      void fetch(`/api/projects/${job.project_id}/draft`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify({ design, base: job.config }),
        keepalive: true,
      }).catch(() => {});
    };
    const unregister = registerDraft(async () => {
      await api("/library/session", undefined, "POST");
      const result = await api<{ saved: boolean }>(
        `/projects/${job.project_id}/draft`,
        undefined,
        "PUT",
        JSON.stringify({ design, base: job.config }),
      );
      if (!result.saved)
        throw new Error(
          "A newer design is saved. Review before recovering this draft.",
        );
    });
    window.addEventListener("pagehide", flush);
    const timer = setTimeout(() => {
      api("/library/session", undefined, "POST")
        .then(() =>
          api<{ saved: boolean }>(
            `/projects/${job.project_id}/draft`,
            undefined,
            "PUT",
            JSON.stringify({ design, base: job.config }),
          ),
        )
        .then((result) => {
          if (current)
            setStatus(
              result.saved
                ? "Recovery draft saved"
                : "A newer design is saved. Review before recovering this draft.",
            );
        })
        .catch(() => {
          if (current)
            setStatus(
              "Draft could not be saved. Keep this tab open and save the design.",
            );
        });
    }, 900);
    return () => {
      current = false;
      unregister();
      clearTimeout(timer);
      window.removeEventListener("pagehide", flush);
    };
  }, [job.project_id, baseVersion, draftVersion, dirty]);
  return (
    <p role="status" className="note">
      {job.archive_error
        ? t(job.archive_error)
        : t(status || "Project recovery is enabled")}
    </p>
  );
}
/** Save/apply reusable branding, including background/logo but excluding episode audio/subtitles. */
export function BrandTemplates({
  job,
  token,
  dirty,
  disabled,
  onChange,
}: {
  job: Job;
  token: string;
  dirty: boolean;
  disabled: boolean;
  onChange: (job: Job) => void;
}) {
  const [name, setName] = useState("");
  const [status, setStatus] = useState("");
  const [items, setItems] = useState<{ id: string; title: string }[]>([]);
  const [selected, setSelected] = useState("");
  const [error, setError] = useState("");
  const [working, setWorking] = useState(false);
  /** Reload local brand-template summaries through the library session. */
  async function refresh() {
    try {
      await api("/library/session", undefined, "POST");
      const data = await api<{ id: string; title: string }[]>("/templates");
      setItems(Array.isArray(data) ? data : []);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not load templates.");
    }
  }
  useEffect(() => {
    void refresh();
  }, []);
  /** Wrap subtitle operations with busy/error feedback. */
  async function run(action: () => Promise<void>) {
    setWorking(true);
    setError("");
    try {
      await action();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Template operation failed.");
    } finally {
      setWorking(false);
    }
  }
  return (
    <fieldset className="design-entry">
      <legend>{t("Brand templates")}</legend>
      <p className="note">
        {t(
          "Reuse fonts, colors, positions, background and logo. The current episode title and subtitles are kept.",
        )}
      </p>
      <label>
        {t("Template name")}
        <input
          value={name}
          maxLength={120}
          placeholder={job.config.title}
          disabled={disabled || working}
          onChange={(e) => setName(e.target.value)}
        />
      </label>
      <button
        disabled={disabled || dirty || working}
        onClick={() =>
          run(async () => {
            const created = await api<{ id: string }>(
              `/jobs/${job.id}/templates`,
              token,
              "POST",
              JSON.stringify({ title: name.trim() || job.config.title }),
            );
            await refresh();
            setSelected(created.id);
            setStatus("Brand template saved.");
          })
        }
      >
        {t("Save current design as template")}
      </button>
      <label>
        {t("Choose a template")}
        <select
          value={selected}
          disabled={disabled || working}
          onChange={(e) => setSelected(e.target.value)}
        >
          <option value="">{t("Select…")}</option>
          {items.map((item) => (
            <option key={item.id} value={item.id}>
              {item.title}
            </option>
          ))}
        </select>
      </label>
      <button
        disabled={disabled || dirty || working || !selected}
        onClick={() =>
          run(async () =>
            onChange(
              await api<Job>(
                `/jobs/${job.id}/templates/${selected}`,
                token,
                "POST",
              ),
            ),
          )
        }
      >
        {t("Apply template")}
      </button>
      {status && <p role="status">{t(status)}</p>}
      {error && <p role="alert">{t(error)}</p>}
    </fieldset>
  );
}
