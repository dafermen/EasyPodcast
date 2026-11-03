import { t } from "./i18n";
import { useEffect, useState } from "react";
export type Theme = "classic" | "studio";
const storageKey = "easypodcast-theme";
/** Read an explicit browser preference, otherwise use Studio, including blocked storage. */
export function readTheme(): Theme {
  try {
    return localStorage.getItem(storageKey) === "classic"
      ? "classic"
      : "studio";
  } catch {
    return "studio";
  }
}
/** Apply and persist the interface theme without touching episode design. */
export function ThemeSelector() {
  const [theme, setTheme] = useState<Theme>(readTheme);
  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    try {
      localStorage.setItem(storageKey, theme);
    } catch {
      /* Selection still works without storage. */
    }
  }, [theme]);
  return (
    <label className="theme-selector">
      {" "}
      {t("Tema de la interfaz")}{" "}
      <select value={theme} onChange={(e) => setTheme(e.target.value as Theme)}>
        <option value="classic">{t("Clásico · claro")}</option>
        <option value="studio">{t("Estudio · azul noche")}</option>
      </select>
    </label>
  );
}
