import type { Design } from "./types";

export const fontFamilies = {
  sans: "EpisodeSans",
  serif: "EpisodeSerif",
  mono: "EpisodeMono",
};
export const fontChoices = [
  ["sans", "Sans · DejaVu Sans"],
  ["serif", "Serif · DejaVu Serif"],
  ["mono", "Monoespaciada · DejaVu Sans Mono"],
] as const;
export const logoChoices = [
  ["top-left", "Arriba a la izquierda"],
  ["top-right", "Arriba a la derecha"],
  ["middle-left", "Centro a la izquierda"],
  ["middle-right", "Centro a la derecha"],
  ["bottom-left", "Abajo a la izquierda"],
  ["bottom-right", "Abajo a la derecha"],
] as const;

export function logoStyle(design: Design): React.CSSProperties {
  const left = design.logo_position.endsWith("left");
  const middle = design.logo_position.startsWith("middle");
  return {
    position: "absolute",
    maxWidth: "15.625%",
    maxHeight: "14.815%",
    width: "auto",
    height: "auto",
    ...(left
      ? { left: `${design.logo_margin / 19.2}%` }
      : { right: `${design.logo_margin / 19.2}%` }),
    ...(middle
      ? { top: "50%", transform: "translateY(-50%)" }
      : design.logo_position.startsWith("bottom")
        ? { bottom: `${design.logo_margin / 10.8}%` }
        : { top: `${design.logo_margin / 10.8}%` }),
  };
}

export function TypographyControls({
  design,
  disabled,
  hasLogo,
  change,
}: {
  design: Design;
  disabled: boolean;
  hasLogo: boolean;
  change: <K extends keyof Design>(key: K, value: Design[K]) => void;
}) {
  return (
    <fieldset className="typography-controls">
      <legend>Tipografía y logo</legend>
      <div className="pair">
        <label>
          Fuente del título
          <select
            value={design.title_font ?? "sans"}
            disabled={disabled}
            onChange={(e) =>
              change("title_font", e.target.value as Design["title_font"])
            }
          >
            {fontChoices.map(([id, label]) => (
              <option key={id} value={id}>
                {label}
              </option>
            ))}
          </select>
        </label>
        <label>
          Tamaño del título (px)
          <input
            type="number"
            min="28"
            max="110"
            value={design.title_font_size ?? 64}
            disabled={disabled}
            onChange={(e) => change("title_font_size", Number(e.target.value))}
          />
        </label>
      </div>
      <div className="pair">
        <label>
          Fuente de subtítulos
          <select
            value={design.subtitle_font ?? "sans"}
            disabled={disabled}
            onChange={(e) =>
              change("subtitle_font", e.target.value as Design["subtitle_font"])
            }
          >
            {fontChoices.map(([id, label]) => (
              <option key={id} value={id}>
                {label}
              </option>
            ))}
          </select>
        </label>
        <label>
          Tamaño de subtítulos (px)
          <input
            type="number"
            min="28"
            max="72"
            value={design.font_size}
            disabled={disabled}
            onChange={(e) => change("font_size", Number(e.target.value))}
          />
        </label>
      </div>
      <label>
        Posición del logo
        <select
          disabled={disabled || !hasLogo}
          value={design.logo_position ?? "top-right"}
          onChange={(e) =>
            change("logo_position", e.target.value as Design["logo_position"])
          }
        >
          {logoChoices.map(([id, label]) => (
            <option key={id} value={id}>
              {label}
            </option>
          ))}
        </select>
      </label>
      <label>
        Margen del logo (px)
        <input
          type="number"
          min="20"
          max="160"
          value={design.logo_margin ?? 40}
          disabled={disabled || !hasLogo}
          onChange={(e) => change("logo_margin", Number(e.target.value))}
        />
      </label>
      <p className="note">
        {hasLogo
          ? "Comprueba en la prueba que el logo no tape texto ni rostros."
          : "Carga un logo en Archivos para activar su posición."}{" "}
        Los tamaños se expresan para el video de 1920 × 1080.
      </p>
    </fieldset>
  );
}
