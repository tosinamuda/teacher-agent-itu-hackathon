import { useEffect, useState } from "react";

import { Button } from "@/shared/components/ui/Button";

type Props = {
  /** Where the selected text is on screen. */
  rect: DOMRect;
  /** The teacher's request for what should change about the selected text. */
  onAsk: (request: string) => void;
  /** Present when the plan can be edited by hand. */
  onEdit?: () => void;
  onDismiss: () => void;
};

/**
 * What can be done with the words the teacher selected in the plan: ask the agent to change them,
 * right here, or edit by hand.
 */
export function SelectionBubble({ rect, onAsk, onEdit, onDismiss }: Props) {
  const [asking, setAsking] = useState(false);
  const [request, setRequest] = useState("");

  useEffect(() => {
    const away = (event: Event) => {
      if (!(event.target as Element | null)?.closest("[data-selection-bubble]"))
        onDismiss();
    };
    const escape = (event: KeyboardEvent) => {
      if (event.key === "Escape") onDismiss();
    };
    document.addEventListener("mousedown", away);
    document.addEventListener("keydown", escape);
    return () => {
      document.removeEventListener("mousedown", away);
      document.removeEventListener("keydown", escape);
    };
  }, [onDismiss]);

  const send = () => {
    const said = request.trim();
    if (said) onAsk(said);
  };

  return (
    <div
      data-selection-bubble
      role="toolbar"
      aria-label="What to do with the selected text"
      style={{ position: "fixed", left: rect.left, top: rect.bottom + 8 }}
      className="z-30"
    >
      {asking ? (
        <div className="flex w-80 flex-col gap-2 border border-(--line-2) bg-(--surface) p-3">
          <textarea
            autoFocus
            rows={2}
            value={request}
            placeholder="What should change?"
            aria-label="What should change?"
            onChange={(event) => setRequest(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                send();
              }
            }}
            className="w-full border border-(--line-2) bg-(--surface) p-2 text-sm text-(--ink) outline-none focus:border-(--accent)"
          />
          <div className="flex items-center gap-2">
            <Button size="sm" disabled={!request.trim()} onClick={send}>
              Send
            </Button>
            <Button size="sm" variant="ghost" onClick={onDismiss}>
              Cancel
            </Button>
          </div>
        </div>
      ) : (
        <div className="flex items-center gap-4 bg-(--ink) px-3 py-2 text-xs text-(--surface)">
          <button
            type="button"
            className="font-semibold"
            onClick={() => setAsking(true)}
          >
            Ask the agent about this
          </button>
          {onEdit ? (
            <button type="button" onClick={onEdit}>
              Edit this by hand
            </button>
          ) : null}
        </div>
      )}
    </div>
  );
}
