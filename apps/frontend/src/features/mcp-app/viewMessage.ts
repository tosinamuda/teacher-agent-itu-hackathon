import type { ChatHighlight } from "@/features/content-chat/chatApi";

/** Sent on the window when a view of some content sends the teacher's comment to the chat. */
export const COMMENT_EVENT = "content-chat:comment";

export type ViewComment = {
  contentId: string;
  text: string;
  highlight: ChatHighlight | null;
  /** Set by the chat of this content that takes the comment. */
  taken?: boolean;
};

/** Where in the content the page itself knows the teacher pointed. */
const POINTS = ["unit_id", "path"] as const;

const record = (value: unknown): Record<string, unknown> =>
  typeof value === "object" && value !== null && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : {};

const text = (value: unknown): string =>
  typeof value === "string" ? value.trim() : "";

function highlightOf(meta: unknown): ChatHighlight | null {
  const given = record(record(meta).highlight);
  const selected = text(given.selected_text);
  if (!selected) return null;
  const highlight: ChatHighlight = { selected_text: selected };
  for (const key of POINTS) {
    const value = text(given[key]);
    if (value) highlight[key] = value;
  }
  return highlight;
}

/**
 * The comment a view sent as a message (`ui/message`): its text, and where in the content the
 * teacher pointed, which the view puts in the `_meta` of its text block. None when the view sent
 * no text or does not show content with an id.
 */
export function commentFromMessage(
  params: unknown,
  contentId: unknown,
): ViewComment | null {
  const content = record(params).content;
  const blocks = (Array.isArray(content) ? content : []).map(record);
  const said = blocks
    .map((block) => text(block.text))
    .filter(Boolean)
    .join("\n\n");
  const id = text(contentId);
  if (!said || !id) return null;
  const pointed = blocks.map((block) => highlightOf(block._meta)).find(Boolean);
  return { contentId: id, text: said, highlight: pointed ?? null };
}

/** Hand a view's comment to the chat of its content; whether a chat took it. */
export function deliverComment(comment: ViewComment): boolean {
  const offered: ViewComment = { ...comment, taken: false };
  window.dispatchEvent(new CustomEvent(COMMENT_EVENT, { detail: offered }));
  return offered.taken === true;
}
