// @vitest-environment jsdom
import { afterEach, it, expect, vi } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { LanguageSelector } from "./LanguageSelector";
import { readLocale, setLocale, t } from "./i18n";
import { getText } from "./text";
afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
  localStorage.clear();
  setLocale("en");
});
it("defaults to English and keeps the preference", async () => {
  localStorage.clear();
  expect(readLocale()).toBe("en");
  setLocale("en");
  render(<LanguageSelector />);
  await userEvent.selectOptions(
    screen.getByLabelText("Interface language"),
    "es",
  );
  expect(document.documentElement.lang).toBe("es");
  expect(readLocale()).toBe("es");
  expect(getText().steps[0]).toBe("Archivos");
  await userEvent.selectOptions(
    screen.getByLabelText("Idioma de la interfaz"),
    "en",
  );
  expect(t("Guardar diseño")).toBe("Save design");
  expect(document.title).toContain("Local studio");
});
it("translates numbered warnings and leaves unknown content unchanged", () => {
  setLocale("en");
  expect(t("Texto denso en el subtítulo 34; revisa la prueba.")).toBe(
    "Dense text in subtitle 34; review the preview.",
  );
  expect(t("My own episode title")).toBe("My own episode title");
  setLocale("es");
  expect(t("Texto denso en el subtítulo 34; revisa la prueba.")).toContain(
    "34",
  );
});
it("works with blocked browser storage", () => {
  vi.spyOn(Storage.prototype, "getItem").mockImplementation(() => {
    throw Error("blocked");
  });
  vi.spyOn(Storage.prototype, "setItem").mockImplementation(() => {
    throw Error("blocked");
  });
  expect(readLocale()).toBe("en");
  setLocale("es");
  expect(t("Save design")).toBe("Guardar diseño");
});
