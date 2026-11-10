import type { Chat } from "./chatApi";

export const chatName = (chat: Chat): string =>
  chat.title ?? (chat.slot === 0 ? "This content" : `Chat ${chat.slot + 1}`);

/** The chats on a piece of content, any of which can be opened, and a way to start another. */
export function ChatPicker({
  chats,
  selected,
  onSelect,
  onStart,
  starting,
}: {
  chats: readonly Chat[];
  selected: string | null;
  onSelect: (chatId: string) => void;
  onStart: () => void;
  starting: boolean;
}) {
  return (
    <div className="flex flex-wrap items-center gap-1.5 border-b border-(--line) pb-3 text-xs">
      {chats.map((chat) => (
        <button
          key={chat.chat_id}
          type="button"
          onClick={() => onSelect(chat.chat_id)}
          title={chat.created_by ? `Started by ${chat.created_by}` : undefined}
          className={`border px-2.5 py-1 transition ${
            chat.chat_id === selected
              ? "border-(--accent) bg-(--accent-soft) font-semibold text-(--accent)"
              : "border-(--line-2) bg-(--surface) text-(--ink-2) hover:border-(--accent)"
          }`}
        >
          {chatName(chat)}
          {chat.working ? (
            <span className="ml-1.5 animate-pulse text-(--accent)">●</span>
          ) : null}
        </button>
      ))}
      <button
        type="button"
        onClick={onStart}
        disabled={starting}
        className="border border-dashed border-(--line-2) px-2.5 py-1 text-(--ink-2) transition hover:border-(--accent) disabled:opacity-60"
      >
        + New chat
      </button>
    </div>
  );
}
