const RELOAD_FLAG = "lpcg:stale-bundle-reloaded";
const ENTRY_SCRIPT = /\/assets\/index-[\w-]+\.js/;
const CHUNK_LOAD_MESSAGE =
  /Failed to fetch dynamically imported module|error loading dynamically imported module|Importing a module script failed/;
const BUILD_CHECK_TIMEOUT_MS = 5000;

export function isChunkLoadError(error: unknown): boolean {
  return error instanceof Error && CHUNK_LOAD_MESSAGE.test(error.message);
}

function loadedEntryScript(): string | undefined {
  for (const script of document.querySelectorAll("script[src]")) {
    const match = script.getAttribute("src")?.match(ENTRY_SCRIPT);
    if (match) return match[0];
  }
  return undefined;
}

export async function newerBuildExists(): Promise<boolean> {
  const loaded = loadedEntryScript();
  if (!loaded) return false;
  try {
    const response = await fetch("/index.html", {
      cache: "no-store",
      signal: AbortSignal.timeout(BUILD_CHECK_TIMEOUT_MS),
    });
    if (!response.ok) return false;
    const published = (await response.text()).match(ENTRY_SCRIPT)?.[0];
    return published !== undefined && published !== loaded;
  } catch {
    return false;
  }
}

export function reloadOnce(): boolean {
  try {
    if (sessionStorage.getItem(RELOAD_FLAG)) return false;
    sessionStorage.setItem(RELOAD_FLAG, "1");
  } catch {
    return false;
  }
  window.location.reload();
  return true;
}

export async function reloadIfStale(error: unknown): Promise<void> {
  const stale = isChunkLoadError(error) || (error instanceof TypeError && (await newerBuildExists()));
  if (stale) reloadOnce();
}
