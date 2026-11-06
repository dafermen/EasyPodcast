import { useEffect, useState } from "react";
import { api } from "./api";
import { t } from "./i18n";

/** Human-readable binary units for local storage and portable-package sizes. */
export function storageSize(value = 0) {
  if (value < 1024) return `${value} B`;
  const unit = Math.min(3, Math.floor(Math.log(value) / Math.log(1024)));
  return `${(value / 1024 ** unit).toFixed(1)} ${["B", "KiB", "MiB", "GiB"][unit]}`;
}
/** Saved project/template metadata used by administration controls. */
export interface LibraryItem {
  id: string;
  title: string;
  kind: "projects" | "templates";
  bytes?: number;
  updated?: number;
  confirm_name?: string;
}
/** Review ticket: validation does not install anything until explicit confirmation. */
interface ImportReview {
  ticket: string;
  items: { kind: string; title: string; bytes: number; in_trash: boolean }[];
  bytes: number;
}
/** Library management, recoverable deletion and streaming portable-package workflows. */
export function LibraryTools({
  projects,
  beforeAction,
  onChanged,
  onTrashed,
  disabled,
}: {
  projects: Omit<LibraryItem, "kind">[];
  beforeAction?: () => Promise<void>;
  onChanged: () => void;
  onTrashed?: (id: string) => void;
  disabled: boolean;
}) {
  const [templates, setTemplates] = useState<LibraryItem[]>([]);
  const [trash, setTrash] = useState<LibraryItem[]>([]);
  const [usage, setUsage] = useState<Record<string, number>>({});
  const [query, setQuery] = useState("");
  const [sort, setSort] = useState("updated");
  const [selected, setSelected] = useState<LibraryItem | null>(null);
  const [mode, setMode] = useState<"rename" | "trash" | "purge">("rename");
  const [name, setName] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [review, setReview] = useState<ImportReview | null>(null);
  const [download, setDownload] = useState<{
    url: string;
    filename: string;
    bytes: number;
  } | null>(null);
  const [status, setStatus] = useState("");
  const locked = busy || disabled;
  /** Refresh management summaries without exposing local paths or authentication capabilities. */
  async function refresh() {
    await api("/library/session", undefined, "POST");
    const [a, b, c] = await Promise.all([
      api<LibraryItem[]>("/templates"),
      api<LibraryItem[]>("/library/trash"),
      api<Record<string, number>>("/library/usage"),
    ]);
    setTemplates(
      Array.isArray(a) ? a.map((x) => ({ ...x, kind: "templates" })) : [],
    );
    setTrash(Array.isArray(b) ? b : []);
    setUsage(c || {});
  }
  useEffect(() => {
    void refresh().catch((e) => setError(e.message));
  }, [projects]);
  /** Serialize mutations and keep visible failures instead of claiming an unsuccessful save. */
  async function run(action: () => Promise<void>) {
    setBusy(true);
    setError("");
    setStatus("");
    try {
      await action();
      await refresh();
      onChanged();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Library operation failed.");
    } finally {
      setBusy(false);
    }
  }
  /** Present an explicit rename, recoverable Trash or typed permanent-deletion form. */
  function choose(item: LibraryItem, operation: typeof mode) {
    setSelected(item);
    setMode(operation);
    setName(operation === "rename" ? item.title : "");
  }
  const items: LibraryItem[] = [
    ...projects.map((p) => ({ ...p, kind: "projects" as const })),
    ...templates,
  ]
    .filter((i) =>
      i.title.toLocaleLowerCase().includes(query.toLocaleLowerCase()),
    )
    .sort((a, b) =>
      sort === "title"
        ? a.title.localeCompare(b.title)
        : sort === "bytes"
          ? (b.bytes || 0) - (a.bytes || 0)
          : (b.updated || 0) - (a.updated || 0),
    );
  return (
    <details className="library-tools">
      <summary>{t("Manage, transfer and back up")}</summary>
      <p className="note">
        {t(
          "Portable packages include media and recovery drafts. Imports create new copies and never overwrite existing projects.",
        )}
      </p>
      <p className="note">
        {t("Storage")}: {storageSize(usage.total_bytes)} · {t("Trash")}:{" "}
        {storageSize(usage.trash_bytes)} · {t("Free disk space")}:{" "}
        {storageSize(usage.free_bytes)}
      </p>
      <div className="library-actions">
        <button
          disabled={locked}
          onClick={() =>
            run(async () => {
              await beforeAction?.();
              setDownload(await api("/library/backup", undefined, "POST"));
            })
          }
        >
          {t("Prepare library backup")}
        </button>
        <label>
          {t("Import project or library ZIP")}
          <input
            type="file"
            accept=".zip,application/zip"
            disabled={locked || !!review}
            onChange={(e) => {
              const file = e.target.files?.[0];
              e.target.value = "";
              if (file)
                void run(async () => {
                  await beforeAction?.();
                  setReview(
                    await api("/library/import", undefined, "POST", file),
                  );
                });
            }}
          />
        </label>
      </div>
      {busy && (
        <p role="status">{t("Processing package or library change…")}</p>
      )}
      {download && (
        <p role="status">
          <a
            className="button primary"
            href={download.url}
            download={download.filename}
            onClick={() => {
              setTimeout(() => setDownload(null), 1000);
            }}
          >
            {t("Download ZIP")} · {storageSize(download.bytes)}
          </a>{" "}
          <span className="note">
            {t("Single-use download; expires in 30 minutes.")}{" "}
            <button
              disabled={locked}
              onClick={() =>
                run(async () => {
                  await api(
                    download.url.replace(/^\/api/, ""),
                    undefined,
                    "DELETE",
                  );
                  setDownload(null);
                })
              }
            >
              {t("Cancel prepared download")}
            </button>
          </span>
        </p>
      )}
      {review && (
        <section className="import-review" aria-label={t("Review import")}>
          <h3>{t("Review import")}</h3>
          <ul>
            {review.items.map((i, n) => (
              <li key={n}>
                {i.title} · {t(i.kind === "projects" ? "Project" : "Template")}{" "}
                · {storageSize(i.bytes)}
                {i.in_trash ? ` · ${t("Trash")}` : ""}
              </li>
            ))}
          </ul>
          <button
            className="primary"
            disabled={locked}
            onClick={() =>
              run(async () => {
                await api(
                  `/library/imports/${review.ticket}/confirm`,
                  undefined,
                  "POST",
                );
                setReview(null);
                setStatus("Import completed as new copies.");
              })
            }
          >
            {t("Import as new copies")}
          </button>{" "}
          <button
            disabled={locked}
            onClick={() =>
              run(async () => {
                await api(
                  `/library/imports/${review.ticket}`,
                  undefined,
                  "DELETE",
                );
                setReview(null);
              })
            }
          >
            {t("Cancel import")}
          </button>
        </section>
      )}
      <label>
        {t("Search projects and templates")}
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          type="search"
        />
      </label>
      <label>
        {t("Sort projects and templates")}
        <select value={sort} onChange={(e) => setSort(e.target.value)}>
          <option value="updated">{t("Recently updated")}</option>
          <option value="title">{t("Name")}</option>
          <option value="bytes">{t("Largest first")}</option>
        </select>
      </label>
      <div className="library-admin-list">
        {items.map((item) => (
          <article key={item.kind + item.id}>
            <strong>{item.title || t("Untitled")}</strong>
            <span className="note">
              {t(item.kind === "projects" ? "Project" : "Template")} ·{" "}
              {storageSize(item.bytes)}
            </span>
            <div className="library-actions">
              <button disabled={locked} onClick={() => choose(item, "rename")}>
                {t("Rename")}
              </button>
              <button disabled={locked} onClick={() => choose(item, "trash")}>
                {t("Move to Trash")}
              </button>
              {item.kind === "projects" && (
                <button
                  disabled={locked}
                  onClick={() =>
                    run(async () => {
                      await beforeAction?.();
                      setDownload(
                        await api(
                          `/projects/${item.id}/export`,
                          undefined,
                          "POST",
                        ),
                      );
                    })
                  }
                >
                  {t("Export project ZIP")}
                </button>
              )}
            </div>
          </article>
        ))}
      </div>
      <details>
        <summary>
          {t("Trash")} · {trash.length}
        </summary>
        <p className="note">
          {t(
            "Trash keeps files until you explicitly delete them permanently. Restore an item to use it again.",
          )}
        </p>
        {trash.map((item) => (
          <article className="trash-item" key={item.kind + item.id}>
            <strong>{item.title || t("Untitled")}</strong> ·{" "}
            {storageSize(item.bytes)}{" "}
            <button
              disabled={locked}
              onClick={() =>
                run(async () => {
                  await api(
                    `/library/trash/${item.kind}/${item.id}/restore`,
                    undefined,
                    "POST",
                  );
                })
              }
            >
              {t("Restore")}
            </button>{" "}
            <button disabled={locked} onClick={() => choose(item, "purge")}>
              {t("Delete permanently")}
            </button>
          </article>
        ))}
      </details>
      {selected && (
        <form
          className="library-confirm"
          onSubmit={(e) => {
            e.preventDefault();
            void run(async () => {
              await beforeAction?.();
              const path = `/library/items/${selected.kind}/${selected.id}`;
              if (mode === "rename")
                await api(
                  path,
                  undefined,
                  "PATCH",
                  JSON.stringify({ title: name.trim() }),
                );
              else if (mode === "trash") {
                await api(path + "/trash", undefined, "POST");
                if (selected.kind === "projects") onTrashed?.(selected.id);
              } else
                await api(
                  `/library/trash/${selected.kind}/${selected.id}`,
                  undefined,
                  "DELETE",
                  JSON.stringify({ confirmation: name }),
                );
              setSelected(null);
            });
          }}
        >
          <h3>
            {t(
              mode === "rename"
                ? "Rename"
                : mode === "trash"
                  ? "Move to Trash"
                  : "Delete permanently",
            )}
            : {selected.title}
          </h3>
          {mode === "rename" && (
            <p className="note">
              {t("This changes the library name, not the title in your video.")}
            </p>
          )}
          {mode === "trash" ? (
            <p>{t("This item can be restored from Trash.")}</p>
          ) : (
            <label>
              {t(
                mode === "rename"
                  ? "New name"
                  : "Type the exact item name to permanently delete it.",
              )}
              {mode === "purge" && (
                <strong>
                  {" "}
                  {selected.confirm_name || selected.title || selected.id}
                </strong>
              )}
              <input
                autoFocus
                maxLength={120}
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </label>
          )}
          <button
            className={mode === "purge" ? "danger" : "primary"}
            disabled={
              locked ||
              (mode === "rename" && !name.trim()) ||
              (mode === "purge" &&
                name !==
                  (selected.confirm_name || selected.title || selected.id))
            }
          >
            {t("Confirm")}
          </button>{" "}
          <button
            type="button"
            disabled={locked}
            onClick={() => setSelected(null)}
          >
            {t("Cancel")}
          </button>
        </form>
      )}
      {status && <p role="status">{t(status)}</p>}
      {error && <p role="alert">{t(error)}</p>}
    </details>
  );
}
