import { beforeEach } from "vitest";
import { setLocale } from "./i18n";
beforeEach(() => setLocale("es"));
// @vitest-environment jsdom
import { afterEach, it, expect, vi } from "vitest";
import { cleanup, render, screen, fireEvent } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { TypographyControls, logoStyle } from "./TypographyControls";
import type { Design } from "./types";
afterEach(cleanup);
it("offers friendly fonts and an independent bold switch", async () => {
  const change = vi.fn();
  render(
    <TypographyControls
      design={
        {
          font_size: 48,
          title_font: "sans",
          subtitle_font: "sans",
          title_bold: true,
          logo_position: "top-right",
        } as Design
      }
      disabled={false}
      hasLogo={false}
      change={change}
    />,
  );
  const user = userEvent.setup();
  await user.click(screen.getByLabelText("Negrilla en el título"));
  expect(change).toHaveBeenCalledWith("title_bold", false);
  for (const family of [
    "nunito",
    "fredoka",
    "quicksand",
    "poppins",
    "baloo2",
    "outfit",
    "balsamiqsans",
    "lexend",
    "atkinsonhyperlegible",
    "comicneue",
  ]) {
    await user.selectOptions(
      screen.getByLabelText("Fuente del título"),
      family,
    );
    expect(change).toHaveBeenCalledWith("title_font", family);
  }
});
it("changes font, title size and logo position independently", async () => {
  const change = vi.fn();
  const design = {
    title_font: "sans",
    subtitle_font: "sans",
    title_font_size: 64,
    font_size: 48,
    logo_position: "top-right",
    logo_margin: 40,
  } as Design;
  render(
    <TypographyControls
      design={design}
      disabled={false}
      hasLogo={true}
      change={change}
    />,
  );
  const user = userEvent.setup();
  await user.selectOptions(screen.getByLabelText("Fuente del título"), "serif");
  expect(change).toHaveBeenCalledWith("title_font", "serif");
  await user.selectOptions(
    screen.getByLabelText("Fuente de subtítulos"),
    "mono",
  );
  expect(change).toHaveBeenCalledWith("subtitle_font", "mono");
  await user.selectOptions(
    screen.getByLabelText("Posición del logo"),
    "bottom-left",
  );
  expect(change).toHaveBeenCalledWith("logo_position", "bottom-left");
  expect(
    logoStyle({ ...design, logo_position: "bottom-left" }).bottom,
  ).toBeDefined();
});
it("explains missing logo", () => {
  render(
    <TypographyControls
      design={{ font_size: 48 } as Design}
      disabled={false}
      hasLogo={false}
      change={vi.fn()}
    />,
  );
  expect(
    (screen.getByLabelText("Posición del logo") as HTMLSelectElement).disabled,
  ).toBe(true);
  expect(screen.getByText(/Carga un logo en Archivos/)).toBeTruthy();
});

it("moves the title independently in both directions", () => {
  const change = vi.fn();
  render(
    <TypographyControls
      design={{ title_offset_x: 0, title_offset_y: 0 } as Design}
      disabled={false}
      hasLogo={false}
      change={change}
    />,
  );
  fireEvent.change(screen.getByLabelText(/Desplazamiento horizontal/), {
    target: { value: "-200" },
  });
  fireEvent.change(screen.getByLabelText(/Desplazamiento vertical/), {
    target: { value: "80" },
  });
  expect(change).toHaveBeenCalledWith("title_offset_x", -200);
  expect(change).toHaveBeenCalledWith("title_offset_y", 80);
});
