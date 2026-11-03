import { setLocale, t, useLocale, type Locale } from "./i18n";
/** Switch the UI locale while leaving spoken audio language and episode text unchanged. */
export function LanguageSelector() {
  const locale = useLocale();
  return (
    <label className="language-selector">
      {t("Idioma de la interfaz")}
      <select
        value={locale}
        onChange={(e) => setLocale(e.target.value as Locale)}
      >
        <option value="en">English</option>
        <option value="es">Español</option>
      </select>
    </label>
  );
}
