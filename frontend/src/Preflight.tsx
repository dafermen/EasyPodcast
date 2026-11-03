import { useEffect, useState } from "react";
import { api, isActive } from "./api";
import { t } from "./i18n";
import type { Job } from "./types";
interface Report {
  ready: boolean;
  blockers: string[];
  warnings: string[];
  width: number;
  height: number;
}
/** Display server-measured blockers and review warnings before spending time on rendering. */
export function Preflight({
  job,
  token,
  dirty,
}: {
  job: Job;
  token: string;
  dirty: boolean;
}) {
  const signature = JSON.stringify([
    job.id,
    job.config,
    job.subtitles_approved,
    job.warnings,
    job.artifacts,
    job.state,
  ]);
  const [report, setReport] = useState<Report | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    if (dirty || isActive(job)) return;
    let current = true;
    setError("");
    api<Report>(`/jobs/${job.id}/preflight`, token)
      .then((value) => {
        if (current && Array.isArray(value.blockers)) setReport(value);
      })
      .catch((e) => {
        if (current) setError(e.message);
      });
    return () => {
      current = false;
    };
  }, [signature, token, dirty]);
  return (
    <details className="preflight" open>
      <summary>{t("Pre-export checks")}</summary>
      {dirty ? (
        <p>{t("Save your design to check the current layout.")}</p>
      ) : error ? (
        <p role="alert">{t(error)}</p>
      ) : report ? (
        <>
          <p role="status">
            {report.ready
              ? t("No layout blockers found. Review the rendered preview.")
              : t("Resolve these issues before rendering.")}
          </p>
          <ul>
            {report.blockers.map((item, i) => (
              <li className="error-text" key={`b${i}`}>
                {t(item)}
              </li>
            ))}
            {report.warnings.map((item, i) => (
              <li key={`w${i}`}>{t(item)}</li>
            ))}
          </ul>
          <small>
            {report.width} × {report.height}
          </small>
        </>
      ) : (
        <p>{t("Checking layout…")}</p>
      )}
    </details>
  );
}
