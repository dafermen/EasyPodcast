import { useEffect, useState } from "react";
export type Theme = "classic" | "studio";
const storageKey = "easypodcast-theme";
export function readTheme(): Theme {
  try {
    return localStorage.getItem(storageKey) === "studio" ? "studio" : "classic";
  } catch {
    return "classic";
  }
}
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
      Tema de la interfaz
      <select value={theme} onChange={(e) => setTheme(e.target.value as Theme)}>
        <option value="classic">Clásico · claro</option>
        <option value="studio">Estudio · azul noche</option>
      </select>
    </label>
  );
}
