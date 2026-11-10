/** Turns a raw apiFetch error body into a readable message (handles the 422 validation shape). */
export function parseGenerateError(error: unknown): string {
  const raw = error instanceof Error ? error.message : String(error ?? "");
  try {
    const parsed = JSON.parse(raw);
    const detail = parsed?.detail;
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail?.errors)) {
      return detail.errors
        .map((e: { message?: string; path?: string[] }) =>
          e.path?.length ? `${e.message} (${e.path.join(" › ")})` : e.message,
        )
        .filter(Boolean)
        .join("; ");
    }
    if (typeof detail?.message === "string") return detail.message;
  } catch {
    /* not JSON — fall through to the raw text */
  }
  return raw || "Generation failed. Please try again.";
}
