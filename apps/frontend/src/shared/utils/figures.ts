/**
 * The TikZ drawings written into a teacher's or a model's text, and the id each is served
 * under: the SHA-256 of its trimmed `tikzpicture` source, exactly as the backend computes it
 * (`app/shared/tikz_figures.py`), so the browser can name a figure without asking for it.
 */

// A drawing, with the centring wrapper it is usually placed in.
const FIGURE =
  /(?:\\begin\{center\}\s*)?(\\begin\{tikzpicture\}[\s\S]*?\\end\{tikzpicture\})(?:\s*\\end\{center\})?/g;

export type TextPart = { kind: "text"; text: string } | { kind: "figure"; source: string };

/** The text in order, each drawing lifted out as a figure of its own. */
export function splitFigures(text: string): TextPart[] {
  const parts: TextPart[] = [];
  let last = 0;
  for (const match of text.matchAll(FIGURE)) {
    const start = match.index ?? 0;
    if (start > last) parts.push({ kind: "text", text: text.slice(last, start) });
    parts.push({ kind: "figure", source: match[1].trim() });
    last = start + match[0].length;
  }
  if (last < text.length) parts.push({ kind: "text", text: text.slice(last) });
  return parts;
}

export async function figureId(source: string): Promise<string> {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(source.trim()));
  return [...new Uint8Array(digest)].map((byte) => byte.toString(16).padStart(2, "0")).join("");
}
