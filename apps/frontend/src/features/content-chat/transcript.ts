import type { ServerEvent } from "./sse";

/** One line of a chat as it is drawn. */
export type Line =
  | { id: string; from: "teacher"; text: string; pointed?: string }
  | { id: string; from: "agent"; text: string; minor?: boolean }
  | {
      id: string;
      from: "tool";
      tool: string;
      unit?: string;
      detail?: string;
      /** What the call found, in a line. */
      observed?: string;
      /** What the agent thought just before the call: why it made it. */
      said?: string;
      failed: boolean;
    }
  | { id: string; from: "thinking"; text: string }
  | { id: string; from: "note"; text: string }
  | { id: string; from: "error"; text: string }
  | {
      id: string;
      from: "view";
      tool: string;
      input: Record<string, unknown>;
      version: number | null;
    };

/** A chat as the events so far make it. */
export type Transcript = {
  lines: Line[];
  /** The last kept event seen: where to resume from after a lost connection. */
  lastSeq: number;
  /** The agent's text so far, before it is a line. */
  partial: { partId: string; text: string } | null;
  /** The agent is busy with a message. */
  working: boolean;
  /** The tool the agent has just started, while it runs. */
  workingOn: string | null;
  /** The agent has spoken since its last tool call, so the turn's summary adds nothing. */
  wrote: boolean;
  /** The version the content last reached in this chat. */
  version: number | null;
};

export const empty: Transcript = {
  lines: [],
  lastSeq: 0,
  partial: null,
  working: false,
  workingOn: null,
  wrote: false,
  version: null,
};

const text = (value: unknown): string =>
  typeof value === "string" ? value : "";
const record = (value: unknown): Record<string, unknown> =>
  typeof value === "object" && value !== null && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : {};

/** The agent's own way of returning a structured answer: not something a person reads. */
const HIDDEN_TOOLS = new Set(["StructuredOutput"]);

/** The transcript after one more event; a kept event already seen is ignored. */
export function reduce(state: Transcript, event: ServerEvent): Transcript {
  if (event.seq !== null && event.seq <= state.lastSeq) return state;
  const next = event.seq !== null ? { ...state, lastSeq: event.seq } : state;
  const id = event.seq !== null ? `e${event.seq}` : `l${state.lines.length}`;
  const { data } = event;
  if (
    (event.kind === "tool" || event.kind === "working_on") &&
    HIDDEN_TOOLS.has(text(data.tool))
  ) {
    return next;
  }
  switch (event.kind) {
    case "user_message": {
      const pointed = text(record(data.highlight).selected_text) || undefined;
      const line: Line = {
        id,
        from: "teacher",
        text: text(data.text),
        pointed,
      };
      return {
        ...next,
        lines: [...next.lines, line],
        working: true,
        wrote: false,
      };
    }
    case "partial":
      return {
        ...next,
        working: true,
        partial: { partId: text(data.part_id), text: text(data.text) },
      };
    case "agent_text": {
      const same = next.partial?.partId === text(data.part_id);
      const line: Line = { id, from: "agent", text: text(data.text) };
      return {
        ...next,
        lines: [...next.lines, line],
        partial: same ? null : next.partial,
        wrote: true,
      };
    }
    case "thinking": {
      const line: Line = { id, from: "thinking", text: text(data.text) };
      return { ...next, lines: [...next.lines, line], working: true };
    }
    case "working_on":
      return { ...next, working: true, workingOn: text(data.tool) };
    case "tool": {
      const { kept, said } = takeSaid(next.lines);
      const line: Line = {
        id,
        from: "tool",
        tool: text(data.tool),
        unit: text(data.unit_id) || undefined,
        detail: text(data.detail) || undefined,
        observed: text(data.observed) || undefined,
        said: said || undefined,
        failed: data.status === "error",
      };
      return { ...next, lines: [...kept, line], workingOn: null, wrote: false };
    }
    case "status":
      return data.working === true
        ? { ...next, working: true }
        : { ...next, working: false, workingOn: null };
    case "turn_done":
      return finished(next, id, data);
    case "turn_stopped": {
      const line: Line = {
        id,
        from: "note",
        text: "Stopped. Nothing was saved.",
      };
      return {
        ...next,
        lines: [...mutedBeforeTheLast(next.lines), line],
        wrote: false,
        ...idle,
      };
    }
    case "turn_failed": {
      const line: Line = {
        id,
        from: "error",
        text: text(data.error) || "The turn failed.",
      };
      return { ...next, lines: [...next.lines, line], ...idle };
    }
    case "view": {
      const line: Line = {
        id,
        from: "view",
        tool: text(data.tool),
        input: record(data.input),
        version: next.version,
      };
      return { ...next, lines: [...next.lines, line] };
    }
    default:
      return next;
  }
}

const idle = { working: false, workingOn: null, partial: null } as const;

function finished(
  state: Transcript,
  id: string,
  data: Record<string, unknown>,
): Transcript {
  const spoken = [...state.lines];
  if (!state.wrote && text(data.summary)) {
    spoken.push({ id: `${id}s`, from: "agent", text: text(data.summary) });
  }
  const lines = mutedBeforeTheLast(spoken);
  const version =
    typeof data.version === "number" ? data.version : state.version;
  const note =
    data.changed === false
      ? "No change was made."
      : version !== null
        ? `Saved as version ${version}.`
        : "Saved.";
  lines.push({ id, from: "note", text: note });
  return { ...state, lines, version, wrote: false, ...idle };
}

/**
 * The lines without the thoughts the agent had just before a tool call, and what they said: they
 * are why it made the call, and the call's step holds them. What the agent said to the teacher
 * stays where it was written.
 */
function takeSaid(lines: readonly Line[]): { kept: Line[]; said: string } {
  let start = lines.length;
  while (start > 0 && lines[start - 1].from === "thinking") start -= 1;
  const said = lines
    .slice(start)
    .map((line) => ("text" in line ? line.text : ""))
    .filter(Boolean)
    .join("\n\n");
  return { kept: lines.slice(0, start), said };
}

/**
 * The lines with the agent's text in the turn just ended muted but for its last: the rest is the
 * agent working things out, and the last is what it tells the teacher.
 */
function mutedBeforeTheLast(lines: readonly Line[]): Line[] {
  const turn = lines.map((line) => line.from).lastIndexOf("teacher") + 1;
  const last = lines.map((line) => line.from).lastIndexOf("agent");
  return lines.map((line, index) =>
    index >= turn && index < last && line.from === "agent"
      ? { ...line, minor: true }
      : line,
  );
}

/** The transcript of a chat made of these events, in order. */
export const transcriptOf = (events: readonly ServerEvent[]): Transcript =>
  events.reduce(reduce, empty);
