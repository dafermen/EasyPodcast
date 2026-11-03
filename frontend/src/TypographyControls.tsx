import { t } from "./i18n";
import type { Design } from "./types";

export const fontFamilies = {
  sans: "EpisodeSans",
  serif: "EpisodeSerif",
  mono: "EpisodeMono",
  nunito: "EpisodeNunito",
  fredoka: "EpisodeFredoka",
  quicksand: "EpisodeQuicksand",
  poppins: "EpisodePoppins",
  baloo2: "EpisodeBaloo2",
  outfit: "EpisodeOutfit",
  balsamiqsans: "EpisodeBalsamiqSans",
  lexend: "EpisodeLexend",
  atkinsonhyperlegible: "EpisodeAtkinsonHyperlegible",
  comicneue: "EpisodeComicNeue",
};
export const fontChoices = [
  ["sans", "Sans · DejaVu Sans"],
  ["serif", "Serif · DejaVu Serif"],
  ["mono", "Monoespaciada · DejaVu Sans Mono"],
  ["nunito", "Nunito · redondeada y amable"],
  ["fredoka", "Fredoka · juvenil y expresiva"],
  ["quicksand", "Rounded · basada en Quicksand"],
  ["poppins", "Poppins · moderna y clara"],
  ["baloo2", "Baloo 2"],
  ["outfit", "Outfit"],
  ["balsamiqsans", "Balsamiq Sans"],
  ["lexend", "Lexend"],
  ["atkinsonhyperlegible", "Atkinson Hyperlegible"],
  ["comicneue", "Comic Neue (estilo Comic Sans)"],
] as const;
export const logoChoices = [
  ["top-left", "Arriba a la izquierda"],
  ["top-right", "Arriba a la derecha"],
  ["middle-left", "Centro a la izquierda"],
  ["middle-right", "Centro a la derecha"],
  ["bottom-left", "Abajo a la izquierda"],
  ["bottom-right", "Abajo a la derecha"],
] as const;

/** Map the six logo placements to percentage-based composition CSS. */
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

/** Edit independent title/subtitle fonts, title offsets and bounded logo placement. */
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
      <legend>{t("Tipografía y logo")}</legend>
      <div className="pair">
        <label>
          {" "}
          {t("Desplazamiento horizontal del título (px)")}{" "}
          <input
            type="range"
            min="-600"
            max="600"
            step="10"
            value={design.title_offset_x ?? 0}
            disabled={disabled}
            onChange={(e) => change("title_offset_x", Number(e.target.value))}
          />
          <span>
            {design.title_offset_x ?? 0} {t("px · izquierda / derecha")}
          </span>
        </label>
        <label>
          {" "}
          {t("Desplazamiento vertical del título (px)")}{" "}
          <input
            type="range"
            min="-80"
            max="400"
            step="10"
            value={design.title_offset_y ?? 0}
            disabled={disabled}
            onChange={(e) => change("title_offset_y", Number(e.target.value))}
          />
          <span>
            {design.title_offset_y ?? 0} {t("px · arriba / abajo")}
          </span>
        </label>
      </div>
      <p className="note">
        {" "}
        {t(
          "0 conserva la posición original. Mueve los controles, guarda el diseño y revisa una nueva prueba. Un título largo puede necesitar menos desplazamiento o una letra más pequeña.",
        )}{" "}
      </p>
      <label className="check">
        <input
          type="checkbox"
          checked={design.title_bold ?? true}
          disabled={disabled}
          onChange={(e) => change("title_bold", e.target.checked)}
        />
        <strong>{t("Negrilla en el título")}</strong>
      </label>
      <div className="pair">
        <label>
          {" "}
          {t("Fuente del título")}{" "}
          <select
            value={design.title_font ?? "sans"}
            disabled={disabled}
            onChange={(e) =>
              change("title_font", e.target.value as Design["title_font"])
            }
          >
            {fontChoices.map(([id, label]) => (
              <option key={id} value={id}>
                {t(label)}
              </option>
            ))}
          </select>
        </label>
        <label>
          {" "}
          {t("Tamaño del título (px)")}{" "}
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
          {" "}
          {t("Fuente de subtítulos")}{" "}
          <select
            value={design.subtitle_font ?? "sans"}
            disabled={disabled}
            onChange={(e) =>
              change("subtitle_font", e.target.value as Design["subtitle_font"])
            }
          >
            {fontChoices.map(([id, label]) => (
              <option key={id} value={id}>
                {t(label)}
              </option>
            ))}
          </select>
        </label>
        <label>
          {" "}
          {t("Tamaño de subtítulos (px)")}{" "}
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
        {" "}
        {t("Posición del logo")}{" "}
        <select
          disabled={disabled || !hasLogo}
          value={design.logo_position ?? "top-right"}
          onChange={(e) =>
            change("logo_position", e.target.value as Design["logo_position"])
          }
        >
          {logoChoices.map(([id, label]) => (
            <option key={id} value={id}>
              {t(label)}
            </option>
          ))}
        </select>
      </label>
      <label>
        {" "}
        {t("Margen del logo (px)")}{" "}
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
          ? t("Comprueba en la prueba que el logo no tape texto ni rostros.")
          : t("Carga un logo en Archivos para activar su posición.")}{" "}
        {t("Los tamaños se expresan para el video de 1920 × 1080.")}{" "}
      </p>
    </fieldset>
  );
}
