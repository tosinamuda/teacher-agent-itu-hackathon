import { useRef } from "react";

import {
  DEFAULT_PANEL_WIDTH,
  MAX_PANEL_WIDTH,
  MIN_PANEL_WIDTH,
} from "./panelWidth";

const STEP = 24;

/** The edge of the right panel: drag it to change the panel's width, or focus it and use the arrows. */
export function PanelResizer({
  width,
  onChange,
}: {
  width: number;
  onChange: (width: number) => void;
}) {
  const drag = useRef<{ x: number; width: number } | null>(null);
  return (
    <div
      role="separator"
      aria-orientation="vertical"
      aria-label="Resize the panel"
      aria-valuenow={width}
      aria-valuemin={MIN_PANEL_WIDTH}
      aria-valuemax={MAX_PANEL_WIDTH}
      tabIndex={0}
      title="Drag to resize. Double-click to reset."
      onPointerDown={(event) => {
        event.currentTarget.setPointerCapture(event.pointerId);
        drag.current = { x: event.clientX, width };
      }}
      onPointerMove={(event) => {
        // The panel is on the right: dragging left makes it wider.
        if (drag.current)
          onChange(drag.current.width + (drag.current.x - event.clientX));
      }}
      onPointerUp={() => {
        drag.current = null;
      }}
      onDoubleClick={() => onChange(DEFAULT_PANEL_WIDTH)}
      onKeyDown={(event) => {
        if (event.key === "ArrowLeft") onChange(width + STEP);
        else if (event.key === "ArrowRight") onChange(width - STEP);
        else return;
        event.preventDefault();
      }}
      className="absolute inset-y-0 left-0 z-20 hidden w-1.5 cursor-col-resize touch-none hover:bg-(--accent)/30 focus-visible:bg-(--accent)/40 focus-visible:outline-hidden lg:block"
    />
  );
}
