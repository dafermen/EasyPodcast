// @vitest-environment jsdom
import { afterEach, it, expect, vi } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ThemeSelector, readTheme } from "./ThemeSelector";
afterEach(() => {
  cleanup();
  localStorage.clear();
  delete document.documentElement.dataset.theme;
  vi.restoreAllMocks();
});
it("keeps classic by default and remembers studio without touching episode settings", async () => {
  const view = render(<ThemeSelector />);
  expect(document.documentElement.dataset.theme).toBe("classic");
  await userEvent.selectOptions(
    screen.getByLabelText("Tema de la interfaz"),
    "studio",
  );
  expect(document.documentElement.dataset.theme).toBe("studio");
  expect(localStorage.getItem("easypodcast-theme")).toBe("studio");
  view.unmount();
  render(<ThemeSelector />);
  expect(
    (screen.getByLabelText("Tema de la interfaz") as HTMLSelectElement).value,
  ).toBe("studio");
  await userEvent.selectOptions(
    screen.getByLabelText("Tema de la interfaz"),
    "classic",
  );
  expect(document.documentElement.dataset.theme).toBe("classic");
});
it("ignores unknown preferences and works when storage is blocked", async () => {
  localStorage.setItem("easypodcast-theme", "invalid");
  expect(readTheme()).toBe("classic");
  vi.spyOn(Storage.prototype, "getItem").mockImplementation(() => {
    throw new Error("blocked");
  });
  vi.spyOn(Storage.prototype, "setItem").mockImplementation(() => {
    throw new Error("blocked");
  });
  render(<ThemeSelector />);
  await userEvent.selectOptions(
    screen.getByLabelText("Tema de la interfaz"),
    "studio",
  );
  expect(document.documentElement.dataset.theme).toBe("studio");
});
