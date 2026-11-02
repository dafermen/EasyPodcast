// @vitest-environment jsdom
import { afterEach, it, expect, vi } from "vitest";
import { render, screen, cleanup } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { SubtitleReview } from "./SubtitleReview";
import type { Job } from "./types";
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});
it("requires review and disables approval while the SRT has unsaved edits", async () => {
  const job = {
    id: "a",
    state: "completed",
    subtitles_ready: true,
    word_timestamps: true,
  } as Job;
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        srt: "1\n00:00:00,000 --> 00:00:01,000\nClear English\n",
      }),
    }),
  );
  render(
    <SubtitleReview
      job={job}
      token="token"
      onChange={vi.fn()}
      onContinue={vi.fn()}
    />,
  );
  const user = userEvent.setup();
  await user.click(screen.getByText("Revisar o corregir SRT"));
  const field = await screen.findByLabelText("Subtítulos sincronizados");
  await user.type(field, " nuevo");
  expect(
    (
      screen.getByRole("button", {
        name: "Aprobar subtítulos y diseñar →",
      }) as HTMLButtonElement
    ).disabled,
  ).toBe(true);
  expect(screen.getByText(/Guardar cambios elimina los tiempos/)).toBeTruthy();
});
