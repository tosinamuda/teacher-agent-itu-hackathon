const DEFAULT_API_BASE = "http://localhost:8000";
import { getAuthCode } from "@/shared/lib/auth";

// Baked in at build time by Vite (.env.production / the deploy pipeline).
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? DEFAULT_API_BASE;

function buildApiHeaders(options?: RequestInit): Headers {
  const method = options?.method ?? "GET";
  const headers = new Headers(options?.headers);
  const hasBody = options?.body != null;

  if (hasBody && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  if (!hasBody && (method === "GET" || method === "HEAD")) {
    headers.delete("Content-Type");
  }

  // Inject Auth Header
  const token = getAuthCode();
  if (token) {
    headers.set("x-teacher-code", token);
  }

  return headers;
}

async function apiRequest(path: string, options?: RequestInit): Promise<Response> {
  const method = options?.method ?? "GET";
  const headers = buildApiHeaders(options);

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    method,
    headers,
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed: ${response.status}`);
  }

  return response;
}

export async function apiFetch<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const response = await apiRequest(path, options);

  return (await response.json()) as T;
}

/** Fetches a binary API payload while keeping the original response headers. */
export async function apiFetchBlob(
  path: string,
  options?: RequestInit
): Promise<{ blob: Blob; response: Response }> {
  const response = await apiRequest(path, options);
  return {
    blob: await response.blob(),
    response,
  };
}
