/**
 * The reason in a refused request's or a failed job's error, as a person reads it.
 *
 * Both carry `{"detail": …}` as their message; a detail that is not text is shown as JSON.
 */
export function errorDetail(error: unknown, fallback: string): string {
  const message = error instanceof Error ? error.message : "";
  if (!message) return fallback;
  try {
    const parsed: unknown = JSON.parse(message);
    if (parsed && typeof parsed === "object" && "detail" in parsed) {
      const detail = (parsed as { detail: unknown }).detail;
      return typeof detail === "string" ? detail : JSON.stringify(detail);
    }
  } catch {
    return message;
  }
  return message;
}
