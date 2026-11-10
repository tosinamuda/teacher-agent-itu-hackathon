/** One server-sent event: its sequence number when the server kept it, its kind and its data. */
export type ServerEvent = {
  seq: number | null;
  kind: string;
  data: Record<string, unknown>;
};

/**
 * Reads server-sent frames out of text that arrives in pieces. A frame ends at a blank line and
 * has `id`, `event` and `data` lines; a line that starts with `:` is a keep-alive and is dropped.
 */
export class SseParser {
  private pending = "";

  /** The events whose frames are complete in what has arrived so far. */
  push(chunk: string): ServerEvent[] {
    this.pending += chunk.replace(/\r\n/g, "\n");
    const frames = this.pending.split("\n\n");
    this.pending = frames.pop() ?? "";
    return frames.flatMap((frame) => {
      const event = parseFrame(frame);
      return event ? [event] : [];
    });
  }
}

function parseFrame(frame: string): ServerEvent | null {
  let seq: number | null = null;
  let kind = "message";
  const data: string[] = [];
  for (const line of frame.split("\n")) {
    if (line === "" || line.startsWith(":")) continue;
    const at = line.indexOf(":");
    const field = at < 0 ? line : line.slice(0, at);
    const value = at < 0 ? "" : line.slice(at + 1).replace(/^ /, "");
    if (field === "id" && /^\d+$/.test(value)) seq = Number(value);
    else if (field === "event") kind = value;
    else if (field === "data") data.push(value);
  }
  if (data.length === 0) return null;
  try {
    const parsed: unknown = JSON.parse(data.join("\n"));
    if (typeof parsed !== "object" || parsed === null || Array.isArray(parsed))
      return null;
    return { seq, kind, data: parsed as Record<string, unknown> };
  } catch {
    return null;
  }
}
