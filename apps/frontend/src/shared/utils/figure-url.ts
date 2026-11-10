import { API_BASE_URL } from "@/shared/api/client";

/**
 * Rewrite a remote textbook figure URL to the backend's local cache
 * (`/static/figures/<file>`) so rendering does not depend on the external textbook CDN.
 * Non-textbook URLs pass through unchanged; the caller should add an `onError`
 * fallback to the original URL in case the local cache is missing the file.
 */
export function localFigureSrc(url: string): string {
  if (!/electricbookworks\.github\.io|siyavula/.test(url)) return url;
  const filename = url.split("/").pop();
  return filename ? `${API_BASE_URL}/static/figures/${filename}` : url;
}
