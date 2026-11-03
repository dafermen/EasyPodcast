/** UI-only localization. Never pass user-authored episode content to t(). */
import { useSyncExternalStore } from "react";
import english from "./locales/en.json";
export type Locale = "en" | "es";
const key = "easypodcast-language";
const catalog: Record<string, string> = english;
const reverse = Object.fromEntries(
  Object.entries(catalog).map(([es, en]) => [en, es]),
);
// Cache long message fragments once; short UI words must not rewrite arbitrary text.
const fragments = Object.entries(catalog)
  .filter(([es]) => es.length > 12 || es === "El archivo ")
  .sort((a, b) => b[0].length - a[0].length);
const listeners = new Set<() => void>();
/** Read the stored supported locale or fall back to English. */
export function readLocale(): Locale {
  try {
    return localStorage.getItem(key) === "es" ? "es" : "en";
  } catch {
    return "en";
  }
}
let locale: Locale = readLocale();
/** Expose the current in-memory locale snapshot for React subscriptions. */
export function getLocale() {
  return locale;
}
/** Persist the locale, update document language/title and notify subscribers. */
export function setLocale(value: Locale) {
  locale = value;
  if (typeof document !== "undefined") {
    document.documentElement.lang = value;
    document.title =
      value === "en"
        ? "EasyPodcast · Local studio"
        : "EasyPodcast · Estudio local";
  }
  try {
    localStorage.setItem(key, value);
  } catch {
    /* Keep the in-memory preference usable. */
  }
  listeners.forEach((notify) => notify());
}
/** Subscribe React to the locale store without placing preferences in episode state. */
export function useLocale() {
  return useSyncExternalStore(
    (notify) => {
      listeners.add(notify);
      return () => {
        listeners.delete(notify);
      };
    },
    getLocale,
    () => "en" as Locale,
  );
}
/** Translate known UI strings and backend message fragments without modifying data. */
export function t(value: string): string {
  if (locale === "es") {
    if (reverse[value]) return reverse[value];
    return value;
  }
  if (catalog[value]) return catalog[value];
  // Numbered validation messages are assembled by the backend from stable fragments.

  return fragments.reduce(
    (result, [es, en]) => result.split(es).join(en),
    value,
  );
}
