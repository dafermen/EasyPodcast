import { t } from "./i18n";
/** Compute shared UI labels at render time so language changes remain reactive. */
export function getText() {
  return {
    app: "EasyPodcast",
    tagline: t("Tu voz, lista para verse."),
    steps: [t("Archivos"), t("Diseño"), t("Vista previa"), t("Exportar")],
    upload: t("Crear episodio"),
    uploading: t("Validando archivos…"),
    privacy: t(
      "Audio y subtítulos se procesan en tu equipo. No se envían al proveedor de imágenes.",
    ),
    local: t("Fondo local de demostración · sin IA"),
    uploadMode: t("Imagen propia"),
    openai: t("Imagen generada con OpenAI"),
  };
}
