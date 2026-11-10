import { useQueryClient } from "@tanstack/react-query";
import { useEffect, useEffectEvent, useRef, useState } from "react";

import { Button } from "@/shared/components/ui/Button";
import {
  COMMENT_EVENT,
  type ViewComment,
} from "@/features/mcp-app/viewMessage";
import { Drawer } from "@/shared/components/ui/Drawer";

import { listChats, type ChatHighlight } from "./chatApi";
import { ChatPicker } from "./ChatPicker";
import { ChatTranscript } from "./ChatTranscript";
import { useChatTranscript } from "./useChatTranscript";
import {
  useContentChats,
  useSendMessage,
  useStartChat,
  useStopChat,
} from "./useContentChats";

/** The chat with the agent that wrote a piece of content, for a page to hold in its own panel. */
export function ContentConversation({
  contentId,
  open,
  highlight,
  onSent,
  onClearHighlight,
  onWorkingChange,
}: {
  contentId: string;
  open: boolean;
  highlight: ChatHighlight | null;
  /** Called after a message is sent, with what it pointed at. */
  onSent: (pointed: ChatHighlight | null) => void;
  onClearHighlight?: () => void;
  /** Called when the agent starts or stops work on a message. */
  onWorkingChange?: (working: boolean) => void;
}) {
  const queryClient = useQueryClient();
  const chats = useContentChats(contentId, open);
  const start = useStartChat(contentId);
  const send = useSendMessage(contentId);
  const stop = useStopChat(contentId);
  const [chosen, setChosen] = useState<string | null>(null);
  const [text, setText] = useState("");
  const box = useRef<HTMLTextAreaElement>(null);
  const list = chats.data ?? [];
  const chatId =
    chosen && list.some((c) => c.chat_id === chosen)
      ? chosen
      : (list[0]?.chat_id ?? null);
  const { transcript, queued, addQueued, dropQueued, clearQueued } =
    useChatTranscript(contentId, open ? chatId : null);

  useEffect(() => {
    if (chatId !== null && chosen === null) setChosen(chatId);
  }, [chatId, chosen]);

  // Pointing at words in the plan starts a message about them.
  useEffect(() => {
    if (highlight) box.current?.focus();
  }, [highlight]);

  // A message goes to the chat that is open, or starts one when the content has none.
  const deliver = async (message: string, pointed: ChatHighlight | null) => {
    addQueued(message);
    try {
      const known = await queryClient.ensureQueryData({
        queryKey: ["contentChats", contentId],
        queryFn: () => listChats(contentId),
      });
      const open =
        chosen && known.some((c) => c.chat_id === chosen)
          ? chosen
          : known[0]?.chat_id;
      const target = open ?? (await start.mutateAsync(undefined)).chat_id;
      setChosen(target);
      await send.mutateAsync({
        chatId: target,
        text: message,
        highlight: pointed,
      });
    } catch (error) {
      dropQueued(message);
      throw error;
    }
  };

  const submit = async () => {
    const message = text.trim();
    if (!message) return;
    setText("");
    try {
      await deliver(message, highlight);
      onSent(highlight);
    } catch {
      setText(message);
    }
  };

  // A comment a view of this content sends is a message from the teacher, like one typed here.
  const takeComment = useEffectEvent((comment: ViewComment) => {
    void deliver(comment.text, comment.highlight).catch(() => undefined);
  });
  useEffect(() => {
    const onComment = (event: Event) => {
      const comment = (event as CustomEvent<ViewComment>).detail;
      if (comment.contentId === contentId) takeComment(comment);
    };
    window.addEventListener(COMMENT_EVENT, onComment);
    return () => window.removeEventListener(COMMENT_EVENT, onComment);
  }, [contentId]);

  const busy = transcript.working || queued.length > 0;
  const working = transcript.working;
  useEffect(() => {
    onWorkingChange?.(working);
  }, [working, onWorkingChange]);
  const halt = () => {
    if (chatId === null) return;
    clearQueued();
    stop.mutate(chatId);
  };
  return (
    <div className="flex h-full flex-col gap-3">
      <ChatPicker
        chats={list}
        selected={chatId}
        onSelect={setChosen}
        onStart={() =>
          start.mutate(undefined, {
            onSuccess: (chat) => setChosen(chat.chat_id),
          })
        }
        starting={start.isPending}
      />
      {chats.isError ? (
        <p className="text-xs text-(--danger-ink)">
          The chats could not be read.
        </p>
      ) : null}
      {chatId === null && !chats.isLoading ? (
        <p className="text-xs text-(--muted)">
          Say what to change. The agent that wrote this carries on from where it
          was.
        </p>
      ) : null}
      <ChatTranscript transcript={transcript} queued={queued} />
      {highlight ? (
        <p className="flex items-start gap-2 bg-(--accent-soft) px-2 py-1.5 text-xs text-(--ink)">
          <span className="font-semibold text-(--accent-deep)">
            Pointing at
          </span>
          <span className="line-clamp-2 flex-1">{highlight.selected_text}</span>
          {onClearHighlight ? (
            <button
              type="button"
              aria-label="Stop pointing"
              onClick={onClearHighlight}
            >
              ✕
            </button>
          ) : null}
        </p>
      ) : null}
      {send.isError || start.isError ? (
        <p className="text-xs text-(--danger-ink)">
          The message was refused. Try again.
        </p>
      ) : null}
      <div className="sticky bottom-0 space-y-2 border-t border-(--line) bg-(--surface) pb-1 pt-3">
        <textarea
          ref={box}
          value={text}
          rows={3}
          maxLength={4000}
          onChange={(event) => setText(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              void submit();
            }
          }}
          placeholder="Message the agent"
          aria-label="Message the agent"
          className="w-full border border-(--line) bg-(--surface) p-2 text-sm outline-none focus:border-(--accent)"
        />
        <div className="flex items-center gap-2">
          <Button
            size="sm"
            disabled={!text.trim()}
            onClick={() => void submit()}
          >
            {busy ? "Send (queued)" : "Send"}
          </Button>
          {busy && chatId !== null ? (
            <Button
              size="sm"
              variant="danger"
              isLoading={stop.isPending}
              onClick={halt}
            >
              Stop
            </Button>
          ) : null}
        </div>
      </div>
    </div>
  );
}

/**
 * A button that opens the chats about one piece of content, for any type of content. A page that
 * lets the teacher select part of the content passes it as `highlight`, which goes with the
 * next message and is cleared by `onSent`.
 */
export function ContentChat({
  contentId,
  highlight = null,
  onSent = () => undefined,
}: {
  contentId: string;
  highlight?: ChatHighlight | null;
  onSent?: () => void;
}) {
  const [open, setOpen] = useState(false);
  useEffect(() => {
    const onComment = (event: Event) => {
      const comment = (event as CustomEvent<ViewComment>).detail;
      if (comment.contentId !== contentId) return;
      comment.taken = true;
      setOpen(true);
    };
    window.addEventListener(COMMENT_EVENT, onComment);
    return () => window.removeEventListener(COMMENT_EVENT, onComment);
  }, [contentId]);
  return (
    <>
      <Button size="sm" variant="outline" onClick={() => setOpen(true)}>
        Chat with the agent
      </Button>
      <Drawer
        open={open}
        onClose={() => setOpen(false)}
        title="Chat"
        side="right"
        width="w-[560px] max-w-[94vw]"
      >
        <ContentConversation
          contentId={contentId}
          open={open}
          highlight={highlight}
          onSent={onSent}
        />
      </Drawer>
    </>
  );
}
