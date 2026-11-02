import { describe, it, expect, vi, afterEach } from "vitest";
import { api, isActive, artifactUrl } from "./api";
import type { Job } from "./types";
afterEach(() => vi.unstubAllGlobals());
describe("API contract", () => {
  it("sends the token in a header and never in the artifact URL", async () => {
    const fetch = vi
      .fn()
      .mockResolvedValue({ ok: true, json: async () => ({ id: "abc" }) });
    vi.stubGlobal("fetch", fetch);
    await api(
      "/jobs/abc",
      "private-token",
      "POST",
      JSON.stringify({ start: 0 }),
    );
    expect(fetch.mock.calls[0][1].headers["X-Job-Token"]).toBe("private-token");
    expect(artifactUrl({ id: "abc" } as Job, "video", true)).not.toContain(
      "private-token",
    );
  });
  it("shows actionable backend errors", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        json: async () => ({ detail: "El trabajo ha vencido." }),
      }),
    );
    await expect(api("/jobs/abc")).rejects.toThrow("ha vencido");
  });
  it("allows a retry after cancellation and failure", () => {
    expect(isActive({ state: "cancelling" } as Job)).toBe(true);
    expect(isActive({ state: "cancelled" } as Job)).toBe(false);
    expect(isActive({ state: "failed" } as Job)).toBe(false);
  });
});
