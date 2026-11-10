import { useCallback, useEffect, useState } from "react";

import type { ChatHighlight } from "@/features/content-chat/chatApi";

/** Container id the plan content is rendered under; selections outside it are ignored. */
export const PLAN_CONTENT_ID = "lesson-plan-content";

/** Walk up from a selected node to collect the nearest step/block/objective anchors. */
function resolveAnchor(node: Node | null): Partial<ChatHighlight> {
  let element: Element | null =
    node instanceof Element ? node : (node?.parentElement ?? null);
  const anchor: Partial<ChatHighlight> = {};
  while (element && element.id !== PLAN_CONTENT_ID) {
    const block = element.getAttribute("data-block-id");
    const step = element.getAttribute("data-step-id");
    const objective = element.getAttribute("data-objective-id");
    if (!anchor.block_id && block) anchor.block_id = block;
    if (!anchor.step_id && step) anchor.step_id = step;
    if (!anchor.lesson_objective_id && objective)
      anchor.lesson_objective_id = objective;
    element = element.parentElement;
  }
  return anchor;
}

/**
 * Capture the teacher's current text selection inside the plan content and the
 * stable ids it falls under, so it can be sent as revision context.
 */
export function useTextSelection() {
  const [selection, setSelection] = useState<ChatHighlight | null>(null);
  const [rect, setRect] = useState<DOMRect | null>(null);

  useEffect(() => {
    const handler = () => {
      const current = window.getSelection();
      const text = current?.toString().trim() ?? "";
      const node = current?.anchorNode ?? null;
      const container = document.getElementById(PLAN_CONTENT_ID);
      if (!text || !node || !container || !container.contains(node)) return;
      setSelection({ selected_text: text, ...resolveAnchor(node) });
      setRect(current?.getRangeAt(0).getBoundingClientRect() ?? null);
    };
    document.addEventListener("mouseup", handler);
    return () => document.removeEventListener("mouseup", handler);
  }, []);

  const clear = useCallback(() => {
    setSelection(null);
    setRect(null);
  }, []);
  /** Hides the bubble but keeps the selection, which is now the message's Pointing at. */
  const hideBubble = useCallback(() => setRect(null), []);
  return { selection, rect, clear, hideBubble };
}
