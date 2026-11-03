import { beforeEach } from "vitest";
import { setLocale } from "./i18n";
beforeEach(() => setLocale("es"));
// @vitest-environment jsdom
import { afterEach, it, expect, vi } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { DesignEntry } from "./DesignEntry";
import { DesignActions } from "./DesignActions";
afterEach(cleanup);

it("starts with a clear manual/import choice", async () => {
  const setMethod = vi.fn();
  const onImport = vi.fn();
  const user = userEvent.setup();
  const { rerender } = render(
    <DesignEntry
      method="manual"
      setMethod={setMethod}
      disabled={false}
      imported={false}
      onImport={onImport}
    />,
  );
  expect(screen.queryByLabelText("Importar diseño JSON")).toBeNull();
  await user.click(screen.getByLabelText("Importar un diseño JSON"));
  expect(setMethod).toHaveBeenCalledWith("import");
  rerender(
    <DesignEntry
      method="import"
      setMethod={setMethod}
      disabled={false}
      imported={false}
      onImport={onImport}
    />,
  );
  const file = new File(["{}"], "design.json", { type: "application/json" });
  await user.upload(screen.getByLabelText("Importar diseño JSON"), file);
  expect(onImport).toHaveBeenCalledWith(file);
  expect(screen.getByText(/no audio, subtítulos, fondo ni logo/)).toBeTruthy();
});

it("makes the next step primary only after changes are saved", async () => {
  const onSave = vi.fn();
  const onContinue = vi.fn();
  const user = userEvent.setup();
  const { rerender } = render(
    <DesignActions
      dirty={true}
      disabled={false}
      saved={false}
      onSave={onSave}
      onContinue={onContinue}
    />,
  );
  const button = screen.getByRole("button", {
    name: "Aprobar fondo y continuar →",
  }) as HTMLButtonElement;
  expect(button.disabled).toBe(true);
  expect(button.classList.contains("primary")).toBe(true);
  await user.click(screen.getByRole("button", { name: "Guardar diseño" }));
  expect(onSave).toHaveBeenCalledTimes(1);
  rerender(
    <DesignActions
      dirty={false}
      disabled={false}
      saved={true}
      onSave={onSave}
      onContinue={onContinue}
    />,
  );
  expect(
    (
      screen.getByRole("button", {
        name: "✓ Diseño guardado",
      }) as HTMLButtonElement
    ).disabled,
  ).toBe(true);
  expect(screen.getByRole("status").textContent).toContain(
    "Revisa el fondo y pulsa Aprobar fondo",
  );
  expect(button.disabled).toBe(false);
  expect(onContinue).not.toHaveBeenCalled();
  await user.click(button);
  expect(onContinue).toHaveBeenCalledTimes(1);
});

it("blocks continuation while an operation is active", () => {
  render(
    <DesignActions
      dirty={false}
      disabled={true}
      saved={true}
      onSave={vi.fn()}
      onContinue={vi.fn()}
    />,
  );
  expect(
    (
      screen.getByRole("button", {
        name: "Aprobar fondo y continuar →",
      }) as HTMLButtonElement
    ).disabled,
  ).toBe(true);
});
