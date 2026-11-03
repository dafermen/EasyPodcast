import type { Job } from "./types";
export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}
export const isActive = (job: Job | null) =>
  !!job &&
  [
    "queued",
    "transcribing",
    "generating_image",
    "rendering_preview",
    "rendering_video",
    "cancelling",
  ].includes(job.state);
export async function api<T>(
  path: string,
  token?: string,
  method = "GET",
  body?: BodyInit,
): Promise<T> {
  const headers: Record<string, string> = {};
  if (token) headers["X-Job-Token"] = token;
  if (typeof body === "string") headers["Content-Type"] = "application/json";
  const response = await fetch("/api" + path, {
    method,
    headers,
    body,
    credentials: "same-origin",
  });
  const data = await response.json();
  if (!response.ok) {
    const detail =
      typeof data.detail === "string"
        ? data.detail
        : "Revisa los campos y sus límites.";
    throw new ApiError(detail, response.status);
  }
  return data as T;
}
export const artifactUrl = (
  job: Job,
  kind: string,
  download = false,
  revision = 0,
) =>
  `/api/jobs/${job.id}/artifacts/${kind}?download=${download}&revision=${revision}`;
