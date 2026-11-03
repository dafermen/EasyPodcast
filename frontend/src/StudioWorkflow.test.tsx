// @vitest-environment jsdom
import { afterEach, it, expect, vi, beforeEach } from "vitest";
import { cleanup, render, screen, fireEvent } from "@testing-library/react";
import { frameSize, canvasDelta, logoBox, CanvasEditor } from "./CanvasEditor";
import { parseTimeline, timelineSrt } from "./SubtitleTimeline";
import { setLocale } from "./i18n";
import type { Design, Job } from "./types";
import { DraftAutosave, ProjectLibrary } from "./ProjectLibrary";
beforeEach(() => setLocale("en"));
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  vi.useRealTimers();
});
it("maps output sizes and pointer movement without depending on screen resolution", () => {
  expect(frameSize({ output_format: "portrait" } as Design)).toEqual([
    1080, 1920,
  ]);
  expect(
    canvasDelta(50, 25, { width: 540, height: 960 }, [1080, 1920]),
  ).toEqual([100, 50]);
  const box = logoBox(
    { logo_x: 0.98, logo_y: 0.99, logo_scale: 2 } as Design,
    [1080, 1920],
    { width: 100, height: 80 },
  );
  expect(box).toEqual({ left: 880, top: 1760, width: 200, height: 160 });
});
it("moves the title with the keyboard and exposes resize handles", () => {
  const change = vi.fn();
  const design = {
    title: "My title",
    title_font: "sans",
    subtitle_font: "sans",
    font_size: 48,
    subtitle_margin: 80,
    wave_y: 0.52,
    title_offset_x: 0,
    title_offset_y: 0,
    logo_position: "top-right",
    logo_margin: 40,
  } as Design;
  render(
    <div className="canvas">
      <CanvasEditor
        job={{ id: "a", artifacts: ["background", "logo"] } as Job}
        design={design}
        revision={0}
        disabled={false}
        change={change}
      />
    </div>,
  );
  fireEvent.keyDown(
    screen.getByRole("group", { name: "Move title with drag or arrow keys" }),
    { key: "ArrowRight" },
  );
  expect(change).toHaveBeenCalledWith("title_offset_x", 10);
  expect(screen.getByRole("button", { name: "Resize logo" })).toBeTruthy();
});
it("roundtrips subtitle text and corrected millisecond timing", () => {
  const cues = parseTimeline("1\n00:00:01,250 --> 00:00:02,500\nHello world\n");
  expect(cues[0]).toEqual({ start: 1.25, end: 2.5, text: "Hello world" });
  cues[0].start = 0.5;
  cues[0].text = "Corrected phrase";
  expect(parseTimeline(timelineSrt(cues))).toEqual(cues);
});
it("debounces a recovery draft with its base version without approving it", async () => {
  vi.useFakeTimers();
  const fetch = vi
    .fn()
    .mockResolvedValue({ ok: true, json: async () => ({ saved: true }) });
  vi.stubGlobal("fetch", fetch);
  const design = { title: "Draft" } as Design;
  const job = {
    id: "a",
    project_id: "project",
    config: { title: "Saved" },
  } as Job;
  render(<DraftAutosave job={job} design={design} dirty />);
  expect(fetch).not.toHaveBeenCalled();
  await vi.advanceTimersByTimeAsync(950);
  const call = fetch.mock.calls.find(([url]) => String(url).includes("/draft"));
  expect(call).toBeTruthy();
  expect(JSON.parse(call![1].body)).toEqual({ design, base: job.config });
  expect(
    fetch.mock.calls.every(([url]) => !String(url).includes("approve")),
  ).toBe(true);
});
it("opens a saved project only after flushing the current draft", async () => {
  const order: string[] = [];
  const result = { id: "restored", token: "new-token" };
  vi.stubGlobal(
    "fetch",
    vi.fn().mockImplementation(async (url: string) => ({
      ok: true,
      json: async () =>
        url.endsWith("/projects")
          ? [
              {
                id: "p",
                title: "Saved episode",
                updated: 1,
                created: 1,
                state: "ready",
                has_draft: true,
              },
            ]
          : url.endsWith("/open")
            ? (order.push("open"), result)
            : { ready: true },
    })),
  );
  const onOpen = vi.fn();
  render(
    <ProjectLibrary
      disabled={false}
      beforeOpen={async () => {
        order.push("flush");
      }}
      onOpen={onOpen}
    />,
  );
  fireEvent.click(await screen.findByText("Continue project"));
  await vi.waitFor(() => expect(onOpen).toHaveBeenCalledWith(result));
  expect(order).toEqual(["flush", "open"]);
});
