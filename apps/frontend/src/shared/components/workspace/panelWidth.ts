import { useCallback, useState } from "react";

export const DEFAULT_PANEL_WIDTH = 360;
export const MIN_PANEL_WIDTH = 300;
export const MAX_PANEL_WIDTH = 720;
const KEY = "right-panel-width";

export const clampPanelWidth = (width: number): number =>
  Math.min(MAX_PANEL_WIDTH, Math.max(MIN_PANEL_WIDTH, Math.round(width)));

function stored(): number {
  try {
    const value = Number(window.localStorage.getItem(KEY));
    return Number.isFinite(value) && value > 0
      ? clampPanelWidth(value)
      : DEFAULT_PANEL_WIDTH;
  } catch {
    return DEFAULT_PANEL_WIDTH;
  }
}

/** The right panel's width, which the teacher can change and which is remembered in this browser. */
export function usePanelWidth(): [number, (width: number) => void] {
  const [width, setWidth] = useState(stored);
  const change = useCallback((next: number) => {
    const clamped = clampPanelWidth(next);
    setWidth(clamped);
    try {
      window.localStorage.setItem(KEY, String(clamped));
    } catch {
      /* the width still changes; it is just not remembered */
    }
  }, []);
  return [width, change];
}
