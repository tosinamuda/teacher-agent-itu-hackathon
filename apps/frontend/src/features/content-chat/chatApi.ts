import { API_BASE_URL, apiFetch } from "@/shared/api/client";
import { getAuthCode } from "@/shared/lib/auth";

import { SseParser, type ServerEvent } from "./sse";

/** One chat on a piece of content. */
export type Chat = {
  chat_id: string;
  /** 0 is the content's own chat: the one its agent began in. */
  slot: number;
  title: string | null;
  created_by: string | null;
  created_at: string;
  working: boolean;
};

/** Where in the content the teacher pointed, and the text they selected there. */
export type ChatHighlight = {
  selected_text: string;
  unit_id?: string;
  path?: string;
  step_id?: string;
  block_id?: string;
  lesson_objective_id?: string;
};

const chats = (contentId: string) =>
  `/content/${encodeURIComponent(contentId)}/chats`;

export const listChats = (contentId: string): Promise<Chat[]> =>
  apiFetch<Chat[]>(chats(contentId));

export const startChat = (contentId: string, title?: string): Promise<Chat> =>
  apiFetch<Chat>(chats(contentId), {
    method: "POST",
    body: JSON.stringify({ title }),
  });

/** Taken at once and answered in the background: the answer arrives on the chat's stream. */
export const sendMessage = (
  contentId: string,
  chatId: string,
  text: string,
  highlight?: ChatHighlight | null,
): Promise<{ waiting: number }> =>
  apiFetch<{ waiting: number }>(
    `${chats(contentId)}/${encodeURIComponent(chatId)}/messages`,
    {
      method: "POST",
      body: JSON.stringify({ text, ...highlight }),
    },
  );

/** Stops what the chat's agent is doing and drops the messages waiting. Nothing is saved. */
export const stopChat = (
  contentId: string,
  chatId: string,
): Promise<{ stopped: boolean; dropped: number }> =>
  apiFetch<{ stopped: boolean; dropped: number }>(
    `${chats(contentId)}/${encodeURIComponent(chatId)}/stop`,
    { method: "POST" },
  );

/**
 * Follows a chat's stream from the event after `after`, calling `onEvent` for each, until the
 * server ends it, the connection drops, or `signal` aborts.
 */
export async function followChat(
  contentId: string,
  chatId: string,
  after: number,
  signal: AbortSignal,
  onEvent: (event: ServerEvent) => void,
): Promise<void> {
  const code = getAuthCode();
  const url = `${API_BASE_URL}${chats(contentId)}/${encodeURIComponent(chatId)}/events?after=${after}`;
  const response = await fetch(url, {
    headers: code ? { "x-teacher-code": code } : {},
    signal,
  });
  if (!response.ok || !response.body)
    throw new Error(`The chat could not be followed: ${response.status}`);
  const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
  const parser = new SseParser();
  for (;;) {
    const { done, value } = await reader.read();
    if (done) return;
    parser.push(value).forEach(onEvent);
  }
}
