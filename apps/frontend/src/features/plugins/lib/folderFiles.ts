import type { PluginFiles } from "../types";

/** What the API takes: at most this many files, and this many bytes of text in all. */
export const MAX_FILES = 200;
export const MAX_BYTES = 1_000_000;

const SKIPPED = /(^|\/)(\.[^/]+|node_modules)(\/|$)/;

type PickedFile = {
  webkitRelativePath: string;
  name: string;
  size: number;
  text: () => Promise<string>;
};

/** The path of a picked file inside its folder: the folder's own name is left off. */
export function pathInFolder(picked: {
  webkitRelativePath: string;
  name: string;
}): string {
  const parts = (picked.webkitRelativePath || picked.name).split("/");
  return (parts.length > 1 ? parts.slice(1) : parts).join("/");
}

/** The text files of a picked folder by path, leaving out hidden files and `node_modules`. */
export async function filesOfFolder(
  picked: readonly PickedFile[],
): Promise<PluginFiles> {
  const kept = picked.filter((file) => !SKIPPED.test(pathInFolder(file)));
  if (kept.length === 0) throw new Error("The folder has no files.");
  if (kept.length > MAX_FILES)
    throw new Error(`The folder has more than ${MAX_FILES} files.`);
  if (kept.reduce((total, file) => total + file.size, 0) > MAX_BYTES) {
    throw new Error(`The folder holds more than ${MAX_BYTES} bytes.`);
  }
  const entries = await Promise.all(
    kept.map(async (file) => [pathInFolder(file), await file.text()] as const),
  );
  return Object.fromEntries(entries);
}
