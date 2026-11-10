import { API_BASE_URL } from "@/shared/api/client";
import { getAuthCode } from "@/shared/lib/auth";

/**
 * POST a multipart form with the caller's access code. apiFetch sets a JSON Content-Type,
 * which would break the multipart boundary, so forms go through here.
 */
export async function postForm<T>(path: string, form: FormData): Promise<T> {
  const headers = new Headers();
  const token = getAuthCode();
  if (token) headers.set("x-teacher-code", token);
  const response = await fetch(`${API_BASE_URL}${path}`, { method: "POST", body: form, headers });
  if (!response.ok) {
    throw new Error((await response.text()) || `Request failed: ${response.status}`);
  }
  return (await response.json()) as T;
}
