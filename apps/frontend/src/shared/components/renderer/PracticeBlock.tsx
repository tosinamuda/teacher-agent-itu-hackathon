import { useEffect, useRef, useState } from "react";
import { PracticeBlock as PracticeBlockType } from "@/shared/types/lesson-schema";
import { stripSourceCitations } from "@/shared/utils/strip-source-citations";

import { RichText } from "./RichText";

declare global {
  interface Window {
    MathJax?: {
      typesetPromise?: (elements?: Element[]) => Promise<unknown>;
      startup?: { promise?: Promise<unknown> };
    };
  }
}

export function PracticeBlock({ block }: { block: PracticeBlockType }) {
  const [showAnswer, setShowAnswer] = useState(false);
  const containerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (
      !showAnswer ||
      !containerRef.current ||
      !window.MathJax?.typesetPromise
    ) {
      return;
    }

    const container = containerRef.current;
    const run = async () => {
      try {
        await window.MathJax?.startup?.promise;
        await window.MathJax?.typesetPromise?.([container]);
      } catch (error) {
        console.error("MathJax practice answer typesetting failed", error);
      }
    };

    void run();
  }, [showAnswer, block.answer]);

  return (
    <div
      ref={containerRef}
      className="my-6 border-t border-[color:var(--line)] pt-5"
    >
      <div className="mb-3 font-bold uppercase tracking-wider text-[color:var(--ink)] text-xs">
        Your Turn
      </div>
      <div className="prose prose-sm mb-4 text-[color:var(--ink)]">
        <RichText text={block.question} prepare={stripSourceCitations} />
      </div>

      {showAnswer ? (
        <div className="rounded bg-[color:var(--accent-soft)] p-3 text-sm text-[color:var(--accent-deep)] animate-in fade-in">
          <span className="font-bold">Answer: </span>
          <div className="inline-block align-middle prose prose-sm max-w-none">
            <RichText text={block.answer} prepare={stripSourceCitations} />
          </div>
        </div>
      ) : (
        <button
          onClick={() => setShowAnswer(true)}
          className="rounded-md bg-[color:var(--surface-raised)] px-4 py-2 text-sm font-medium text-[color:var(--ink)] border border-[color:var(--line)] hover:bg-[color:var(--surface-sunken)] transition-colors"
        >
          Check Answer
        </button>
      )}

      {block.hints && block.hints.length > 0 && (
        <div className="mt-4 text-xs text-[color:var(--muted)]">
          <details>
            <summary className="cursor-pointer hover:underline">
              Need a hint?
            </summary>
            <ul className="mt-2 list-disc pl-4 space-y-1">
              {block.hints.map((hint, idx) => (
                <li key={idx}>
                  <RichText text={hint} prepare={stripSourceCitations} />
                </li>
              ))}
            </ul>
          </details>
        </div>
      )}
    </div>
  );
}
