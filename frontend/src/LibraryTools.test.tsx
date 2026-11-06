// @vitest-environment jsdom
import { afterEach, beforeEach, expect, it, vi } from "vitest";
import {
  cleanup,
  render,
  screen,
  fireEvent,
  waitFor,
} from "@testing-library/react";
import { LibraryTools } from "./LibraryTools";
import { SubtitleReview } from "./SubtitleReview";
import { flushDrafts } from "./drafts";
import { setLocale } from "./i18n";
import type { Job } from "./types";
beforeEach(() => setLocale("en"));
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});
/** A predictable server response for package review and isolated administration UI tests. */
function setup() {
  const fetch = vi.fn(async (url: string) => ({
    ok: true,
    json: async () =>
      url.endsWith("/templates")
        ? []
        : url.endsWith("/library/trash")
          ? [
              {
                id: "t",
                kind: "projects",
                title: "Trashed episode",
                confirm_name: "Trashed episode",
                bytes: 100,
              },
            ]
          : url.endsWith("/library/import")
            ? {
                ticket: "ticket",
                items: [
                  { kind: "projects", title: "Incoming episode", bytes: 300 },
                ],
                bytes: 300,
              }
            : url.endsWith("/subtitles")
              ? {
                  srt: "1\n00:00:00,000 --> 00:00:01,000\nHello\n",
                  base_digest: "a".repeat(64),
                  base_version: 2,
                  draft: "incomplete recovered text",
                }
              : { saved: true },
  }));
  vi.stubGlobal("fetch", fetch);
  return fetch;
}
it("requires typed confirmation before permanent deletion", async () => {
  const fetch = setup();
  render(<LibraryTools projects={[]} disabled={false} onChanged={() => {}} />);
  fireEvent.click(
    await screen.findByRole("button", { name: "Delete permanently" }),
  );
  const confirm = screen.getByRole("button", {
    name: "Confirm",
  }) as HTMLButtonElement;
  expect(confirm.disabled).toBe(true);
  fireEvent.change(screen.getByLabelText(/Type the exact/), {
    target: { value: "wrong" },
  });
  expect(confirm.disabled).toBe(true);
  fireEvent.change(screen.getByLabelText(/Type the exact/), {
    target: { value: "Trashed episode" },
  });
  expect(confirm.disabled).toBe(false);
  expect(
    fetch.mock.calls.some(([url]) => url.includes("/trash/projects/")),
  ).toBe(false);
  fireEvent.click(confirm);
  await waitFor(() =>
    expect(
      fetch.mock.calls.some(([url]) => url.includes("/trash/projects/t")),
    ).toBe(true),
  );
});
it("reviews imported ZIP contents before confirming installation", async () => {
  const fetch = setup();
  render(<LibraryTools projects={[]} disabled={false} onChanged={() => {}} />);
  fireEvent.change(screen.getByLabelText("Import project or library ZIP"), {
    target: { files: [new File(["zip"], "project.zip")] },
  });
  expect(await screen.findByText(/Incoming episode/)).toBeTruthy();
  expect(fetch.mock.calls.some(([url]) => url.endsWith("/confirm"))).toBe(
    false,
  );
  fireEvent.click(screen.getByRole("button", { name: "Import as new copies" }));
  await waitFor(() =>
    expect(
      fetch.mock.calls.some(([url]) => url.endsWith("/imports/ticket/confirm")),
    ).toBe(true),
  );
});
it("recovers incomplete subtitle text and flushes its current generation before switching", async () => {
  const fetch = setup();
  render(
    <SubtitleReview
      job={
        {
          id: "j",
          project_id: "p",
          state: "ready",
          subtitles_ready: true,
          metadata: { duration: 5 },
        } as Job
      }
      token="secret"
      onChange={() => {}}
      onContinue={() => {}}
    />,
  );
  const field = (await screen.findByLabelText(
    "Timed subtitles",
  )) as HTMLTextAreaElement;
  await waitFor(() => expect(field.value).toBe("incomplete recovered text"));
  fireEvent.change(field, { target: { value: "still incomplete" } });
  await flushDrafts();
  const call = fetch.mock.calls.find(([url]) =>
    url.endsWith("/subtitle-draft"),
  );
  expect(call).toBeTruthy();
  // Inspect the request through the mock to verify the concurrency generation is retained.
  const options = (fetch.mock.calls as unknown as [string, RequestInit][]).find(
    ([url]) => url.endsWith("/subtitle-draft"),
  )![1];
  expect(JSON.parse(options.body as string)).toEqual({
    srt: "still incomplete",
    base_digest: "a".repeat(64),
    base_version: 2,
  });
  expect(
    (
      screen.getByRole("button", {
        name: "Approve subtitles and design →",
      }) as HTMLButtonElement
    ).disabled,
  ).toBe(true);
});
