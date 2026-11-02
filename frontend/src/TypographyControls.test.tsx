// @vitest-environment jsdom
import { afterEach, it, expect, vi } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { TypographyControls, logoStyle } from "./TypographyControls";
import type { Design } from "./types";
afterEach(cleanup);
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
