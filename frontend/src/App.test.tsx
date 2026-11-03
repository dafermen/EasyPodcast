import { beforeEach } from "vitest";
import { setLocale } from "./i18n";
beforeEach(() => setLocale("es"));
// @vitest-environment jsdom
import { afterEach, describe, it, expect, vi } from "vitest";
import {
  render,
  screen,
  cleanup,
  waitFor,
  fireEvent,
} from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { App } from "./main";
const caps = {
  render_ready: true,
  ffmpeg: true,
  ffprobe: true,
  h264: true,
  aac: true,
  font: true,
  filters: { ass: true },
  image_provider: false,
  limits: {
    audio_bytes: 1073741824,
    srt_bytes: 5242880,
    image_bytes: 20971520,
    duration_seconds: 7200,
    queue: 2,
  },
};
const design = {
  title: "Mi episodio",
  description: "",
  image_style: "illustration",
  atmosphere: "Estudio",
  visualizer: "waveform",
  color: "#5EEAD4",
  sensitivity: 1,
  wave_y: 0.52,
  wave_height: 0.16,
  font_size: 48,
  subtitle_color: "#FFFFFF",
  outline: 3,
  subtitle_margin: 80,
  subtitle_width: 0.85,
  max_lines: 2,
  crf: 21,
  preset: "veryfast",
  trim_subtitles: false,
};
const job = {
  id: "test-job",
  token: "test-token",
  state: "ready",
  phase: "Listo",
  progress: null,
  error: null,
  metadata: { duration: 26, audio_tracks: 1, codec: "pcm_s16le" },
  warnings: [],
  config: design,
  background_approved: false,
  preview_approved: false,
  background_mode: "local",
  artifacts: ["background"],
  expires_at: "2026-11-03T00:00:00Z",
};
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});
describe("episode assistant", () => {
  it("offers a fresh upload after a job disappears", async () => {
    const fetch = vi
      .fn()
      .mockImplementation(async (url: string, options?: { method: string }) => {
        if (url.endsWith("/capabilities"))
          return { ok: true, json: async () => caps };
        if (options?.method === "POST")
          return { ok: true, json: async () => job };
        return {
          ok: false,
          status: 404,
          json: async () => ({ detail: "El episodio se perdió al reiniciar." }),
        };
      });
    vi.stubGlobal("fetch", fetch);
    render(<App />);
    const user = userEvent.setup({ applyAccept: false });
    await screen.findByText("Motor audiovisual listo");
    await user.upload(
      screen.getByLabelText(/Audio del episodio/),
      new File(["audio"], "demo.wav", { type: "audio/wav" }),
    );
    await user.upload(
      screen.getByLabelText(/Subtítulos SRT/),
      new File(["srt"], "demo.srt"),
    );
    fireEvent.submit(
      screen.getByRole("button", { name: "Crear episodio" }).closest("form")!,
    );
    const reset = await screen.findByRole(
      "button",
      { name: "Cargar un nuevo episodio" },
      { timeout: 4000 },
    );
    expect(
      screen.getByText("Este episodio ya no se puede procesar."),
    ).toBeTruthy();
    await user.click(reset);
    expect(screen.getByRole("button", { name: "Crear episodio" })).toBeTruthy();
  });
  it("uploads files, explains optional IA and opens design", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockImplementation(async (url: string) => ({
        ok: true,
        json: async () => (url.endsWith("/capabilities") ? caps : job),
      })),
    );
    render(<App />);
    const user = userEvent.setup({ applyAccept: false });
    await screen.findByText("Motor audiovisual listo");
    expect(
      (screen.getByRole("button", { name: "02 Diseño" }) as HTMLButtonElement)
        .disabled,
    ).toBe(true);
    await user.upload(
      screen.getByLabelText(/Audio del episodio/),
      new File(["synthetic"], "demo.wav", { type: "audio/wav" }),
    );
    await user.upload(
      screen.getByLabelText(/Subtítulos SRT/),
      new File(["synthetic"], "demo.srt", { type: "application/x-subrip" }),
    );
    expect(
      (screen.getByLabelText(/Audio del episodio/) as HTMLInputElement).files
        ?.length,
    ).toBe(1);
    expect(
      (screen.getByLabelText(/Subtítulos SRT/) as HTMLInputElement).files
        ?.length,
    ).toBe(1);
    fireEvent.submit(
      screen.getByRole("button", { name: "Crear episodio" }).closest("form")!,
    );
    await screen.findByRole("heading", { name: "Diseño" });
    expect(
      (
        screen.getByRole("button", {
          name: "Generar imagen con IA",
        }) as HTMLButtonElement
      ).disabled,
    ).toBe(true);
    expect(screen.getByText(/falta configurar el proveedor/)).toBeTruthy();
    await user.type(screen.getByLabelText("Título", { exact: true }), " nuevo");
    await waitFor(() =>
      expect(
        (
          screen.getByRole("button", {
            name: "Guardar diseño",
          }) as HTMLButtonElement
        ).disabled,
      ).toBe(false),
    );
    expect(
      (
        screen.getByRole("button", {
          name: "Aprobar fondo y continuar →",
        }) as HTMLButtonElement
      ).disabled,
    ).toBe(true);
  });
  it("announces connection failures", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockRejectedValue(new Error("Backend no disponible")),
    );
    render(<App />);
    expect(
      (await screen.findAllByRole("alert"))
        .map((item) => item.textContent)
        .join(" "),
    ).toContain("Backend no disponible");
  });
  it("creates an audio-only job and waits for transcription", async () => {
    const fetch = vi.fn().mockImplementation(async (url: string) => ({
      ok: true,
      json: async () =>
        url.endsWith("/capabilities")
          ? { ...caps, transcription: { available: true } }
          : {
              ...job,
              state: "transcribing",
              subtitles_ready: false,
              subtitles_approved: false,
            },
    }));
    vi.stubGlobal("fetch", fetch);
    render(<App />);
    const user = userEvent.setup({ applyAccept: false });
    await screen.findByText("Motor audiovisual listo");
    await user.selectOptions(
      screen.getByLabelText("Origen de los subtítulos"),
      "generate",
    );
    expect(screen.queryByLabelText(/Subtítulos SRT/)).toBeNull();
    await user.upload(
      screen.getByLabelText(/Audio del episodio/),
      new File(["synthetic"], "demo.wav", { type: "audio/wav" }),
    );
    fireEvent.submit(
      screen.getByRole("button", { name: "Crear episodio" }).closest("form")!,
    );
    await screen.findByRole("heading", { name: "Generando subtítulos" });
    expect(
      fetch.mock.calls.some(([url]) =>
        String(url).includes("subtitle_mode=generate"),
      ),
    ).toBe(true);
    expect(
      (screen.getByRole("button", { name: "02 Diseño" }) as HTMLButtonElement)
        .disabled,
    ).toBe(true);
  });
});

it("switches interface language without resetting an unsaved episode title", async () => {
  setLocale("en");
  vi.stubGlobal(
    "fetch",
    vi.fn().mockImplementation(async (url: string) => ({
      ok: true,
      json: async () =>
        url.endsWith("/capabilities")
          ? caps
          : { ...job, phase: "Listo para diseñar" },
    })),
  );
  render(<App />);
  const user = userEvent.setup({ applyAccept: false });
  await screen.findByText("Media engine ready");
  await user.upload(
    screen.getByLabelText(/Episode audio/),
    new File(["audio"], "demo.wav", { type: "audio/wav" }),
  );
  await user.upload(
    screen.getByLabelText(/Subtitles UTF-8/),
    new File(["srt"], "demo.srt"),
  );
  fireEvent.submit(
    screen.getByRole("button", { name: "Create episode" }).closest("form")!,
  );
  const title = await screen.findByLabelText("Title");
  await user.clear(title);
  await user.type(title, "My unchanged title");
  await user.selectOptions(screen.getByLabelText("Interface language"), "es");
  expect((screen.getByLabelText("Título") as HTMLInputElement).value).toBe(
    "My unchanged title",
  );
  expect(
    (
      screen.getByRole("button", {
        name: "Aprobar fondo y continuar →",
      }) as HTMLButtonElement
    ).disabled,
  ).toBe(true);
  await user.selectOptions(
    screen.getByLabelText("Idioma de la interfaz"),
    "en",
  );
  expect(screen.getByRole("button", { name: "Save design" })).toBeTruthy();
  expect((screen.getByLabelText("Title") as HTMLInputElement).value).toBe(
    "My unchanged title",
  );
});
