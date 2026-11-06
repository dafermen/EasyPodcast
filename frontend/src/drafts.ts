/** Active draft savers are registered only while their editor has pending changes. */
const savers = new Set<() => Promise<void>>();
/** Register a save operation and return its lifecycle cleanup. */
export function registerDraft(save: () => Promise<void>) {
  savers.add(save);
  return () => {
    savers.delete(save);
  };
}
/** Await recovery writes before switching projects or creating a portable backup. */
export async function flushDrafts() {
  await Promise.all([...savers].map((save) => save()));
}
