# Localization and themes

## Defaults and storage

English (`en`) and Spanish (`es`) are supported. A new or invalid preference defaults to English. Studio is the default theme; an explicit Classic preference is preserved. Browser localStorage keys are easypodcast-language and easypodcast-theme. Only preferences are stored; never store job tokens or media in these keys. Blocked storage falls back to in-memory selection.

LanguageSelector calls setLocale. i18n.ts notifies subscribers using useSyncExternalStore, updates html lang and the document title, and persists the selection. App subscribes so child labels are reevaluated. getText() returns shared labels at render time instead of freezing translations at import time. Font and logo choice labels are translated when rendered. Dates use the selected locale.

## Translation catalog

frontend/src/locales/en.json maps existing Spanish UI phrases to English. Spanish source phrases are stable catalog keys, retained to avoid changing backend message contracts in this release. t() handles exact keys, reverse English lookup for stored errors, and known fragments in numbered backend warnings. Unknown text is preserved. Raw API messages remain legacy Spanish; localization is a browser presentation feature.

Never translate user title, atmosphere, description, SRT content, filenames or transcription output. Interface language does not select Whisper language or translate speech. Technical enum IDs and JSON keys never change.

To add a UI message, add its Spanish key and English value, then call t() in render or action code. Keep accessible labels and status text translated too. Do not evaluate translations in module-level option arrays: store keys there and translate labels in JSX. To add a third language, extend Locale, catalog lookup, selector and locale/date tests.

## Themes

ThemeSelector writes data-theme on the document root. Classic CSS remains the baseline. Studio rules are scoped under data-theme=studio; they style interface surfaces and controls while leaving the canvas and media untouched. Studio uses bundled Outfit, midnight blue, cyan primary actions, violet focus and green background approval. CSS breakpoints collapse the editing columns and wrap header controls on smaller screens.

Test both languages and themes, reload persistence, unavailable storage, error messages and narrow layouts. Theme/language changes during an episode must not reset the job or dirty its design.
