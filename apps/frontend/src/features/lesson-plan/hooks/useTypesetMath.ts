import { useEffect, useState, type RefObject } from "react";

declare global {
  interface Window {
    MathJax?: {
      typesetPromise?: (elements?: Element[]) => Promise<unknown>;
      startup?: { promise?: Promise<unknown> };
    };
  }
}

const MATHJAX_SRC = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js";
const MATHJAX_SCRIPT_ID = "mathjax-script";

/**
 * Load MathJax once per document (was `next/script` under Next). The config
 * object must exist on `window` BEFORE the library script executes, and a
 * second mount must not inject a second script tag — it just waits on the
 * existing one.
 */
function loadMathJax(onReady: () => void): () => void {
  if (window.MathJax?.typesetPromise) {
    onReady();
    return () => {};
  }
  if (!document.getElementById(MATHJAX_SCRIPT_ID)) {
    window.MathJax = {
      // MathJax reads this plain config object at startup, then replaces it
      // with the live API. Cast through the global type for the handoff.
      tex: {
        inlineMath: [
          ["\\(", "\\)"],
          ["$", "$"],
        ],
        displayMath: [
          ["\\[", "\\]"],
          ["$$", "$$"],
        ],
      },
      svg: { fontCache: "global" },
    } as unknown as Window["MathJax"];
    const script = document.createElement("script");
    script.id = MATHJAX_SCRIPT_ID;
    script.src = MATHJAX_SRC;
    script.async = true;
    document.head.appendChild(script);
  }
  const existing = document.getElementById(MATHJAX_SCRIPT_ID);
  existing?.addEventListener("load", onReady);
  return () => existing?.removeEventListener("load", onReady);
}

/** Typesets the maths inside `container` whenever `content` changes. */
export function useTypesetMath(
  container: RefObject<HTMLElement | null>,
  content: unknown,
): void {
  const [ready, setReady] = useState(false);

  useEffect(() => loadMathJax(() => setReady(true)), []);

  useEffect(() => {
    const element = container.current;
    if (!ready || !element || !window.MathJax?.typesetPromise) return;
    const run = async () => {
      try {
        await window.MathJax?.startup?.promise;
        await window.MathJax?.typesetPromise?.([element]);
      } catch (error) {
        console.error("MathJax typesetting failed", error);
      }
    };
    void run();
  }, [ready, container, content]);
}
