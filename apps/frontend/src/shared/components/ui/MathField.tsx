import { createElement, useEffect, useRef, useState } from "react";

type MathfieldEl = HTMLElement & { value: string };

const INLINE_STYLE_ID = "lp-inline-math-style";

/**
 * Strip the field's built-in chrome for the inline variant: no menu toggle, and the
 * symbol-keyboard toggle only while the field is focused — so at rest an inline node
 * reads as plain rendered maths.
 */
function ensureInlineStyles() {
  if (document.getElementById(INLINE_STYLE_ID)) return;
  const style = document.createElement("style");
  style.id = INLINE_STYLE_ID;
  style.textContent = `
    math-field.lp-inline-math::part(menu-toggle) { display: none; }
    math-field.lp-inline-math:not(:focus-within)::part(virtual-keyboard-toggle) { display: none; }
  `;
  document.head.appendChild(style);
}

/**
 * A MathLive WYSIWYG math editor that emits LaTeX via `onChange`. MathLive is
 * browser-only and registers a custom element as a side effect, so it is loaded
 * with a dynamic import inside an effect (MathLive's own guidance for React/SSR).
 * The field is seeded once and left uncontrolled thereafter to avoid caret fights.
 *
 * The `inline` variant embeds the field in a line of text (no chrome) so an inline
 * math node can be edited where it sits; `autoFocus` opens a freshly inserted node
 * straight into entry.
 */
export function MathField({
  initialLatex = "",
  onChange,
  inline = false,
  autoFocus = false,
}: {
  initialLatex?: string;
  onChange: (latex: string) => void;
  inline?: boolean;
  autoFocus?: boolean;
}) {
  const ref = useRef<MathfieldEl | null>(null);
  const onChangeRef = useRef(onChange);
  onChangeRef.current = onChange;
  const [ready, setReady] = useState(false);

  useEffect(() => {
    let active = true;
    void import("mathlive").then((mod) => {
      if (!active) return;
      // Serve glyph fonts from the CDN (the default relative paths 404 under the
      // bundler) and disable keypress sounds.
      mod.MathfieldElement.fontsDirectory = "https://unpkg.com/mathlive@0.110.0/fonts";
      mod.MathfieldElement.soundsDirectory = null;
      ensureInlineStyles();
      setReady(true);
    });
    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    if (!ready) return;
    const el = ref.current;
    if (!el) return;
    if (initialLatex && el.value !== initialLatex) el.value = initialLatex;
    const handler = () => onChangeRef.current(el.value);
    el.addEventListener("input", handler);
    // Keep keystrokes inside the field — when embedded in the rich-text editor the
    // host must not also act on them (e.g. Backspace deleting the surrounding node).
    const stop = (event: Event) => event.stopPropagation();
    el.addEventListener("keydown", stop);
    el.addEventListener("keyup", stop);
    if (autoFocus) el.focus();
    return () => {
      el.removeEventListener("input", handler);
      el.removeEventListener("keydown", stop);
      el.removeEventListener("keyup", stop);
    };
    // Seed once on ready; uncontrolled thereafter.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ready]);

  if (!ready) {
    return inline ? (
      <span className="px-1 text-xs text-(--muted)">…</span>
    ) : (
      <div className="px-3 py-2 text-xs text-(--muted)">Loading math editor…</div>
    );
  }
  return createElement("math-field", {
    ref,
    className: inline ? "lp-inline-math" : undefined,
    style: inline
      ? {
          display: "inline-block",
          verticalAlign: "middle",
          border: "none",
          background: "transparent",
          padding: "0 2px",
          fontSize: "1.05em",
        }
      : {
          display: "block",
          width: "100%",
          border: "1px solid var(--line-2)",
          padding: "8px 12px",
          fontSize: "1.1rem",
          background: "var(--surface)",
        },
  });
}
