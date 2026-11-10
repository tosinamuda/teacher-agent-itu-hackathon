import { useEffect, useRef, useState } from "react";
import { useQuery } from "@tanstack/react-query";

import { getTextbookRecord } from "@/shared/api/textbookRecords";
import { groupReferencesByChapter } from "@/shared/utils/references";
import { ExplanationBlock } from "@/shared/components/renderer/ExplanationBlock";

/** One source chunk row: click to fetch + reveal its textbook content inline. */
function SourceRecordRow({ recordId, label }: { recordId: string; label: string }) {
  const [open, setOpen] = useState(false);
  const contentRef = useRef<HTMLDivElement | null>(null);
  const { data, isLoading, isError } = useQuery({
    queryKey: ["textbookRecord", recordId],
    queryFn: () => getTextbookRecord(recordId),
    enabled: open,
  });

  // The source content loads asynchronously (after the page's one-shot MathJax
  // typeset), so its `\(…\)` / `\[…\]` math must be typeset on arrival.
  useEffect(() => {
    const element = contentRef.current;
    const mathJax = (
      window as unknown as {
        MathJax?: {
          startup?: { promise?: Promise<unknown> };
          typesetPromise?: (els?: Element[]) => Promise<unknown>;
        };
      }
    ).MathJax;
    if (!data || !element || !mathJax?.typesetPromise) return;
    void (async () => {
      try {
        await mathJax.startup?.promise;
        await mathJax.typesetPromise?.([element]);
      } catch {
        /* best-effort — leave raw if typesetting fails */
      }
    })();
  }, [data]);

  return (
    <li className="overflow-hidden rounded-lg border border-(--line) bg-white">
      <button
        type="button"
        onClick={() => setOpen((value) => !value)}
        className="flex w-full items-center justify-between gap-2 px-3 py-1.5 text-left"
      >
        {/* Show a friendly "Source N" label, not the raw record id — the id is
            internal provenance, kept on hover for anyone who needs it. */}
        <span className="text-xs text-(--accent-deep)" title={recordId}>{label}</span>
        <span className="text-[11px] text-(--muted)">{open ? "Hide" : "Read source"}</span>
      </button>
      {open ? (
        <div
          ref={contentRef}
          className="border-t border-(--line) px-3 py-2 text-xs text-(--ink)"
        >
          {isLoading ? <p className="text-(--muted)">Loading source…</p> : null}
          {isError ? <p className="text-(--danger)">Couldn&apos;t load this source.</p> : null}
          {data ? (
            <div className="space-y-1">
              {data.heading ? (
                <p className="text-[11px] uppercase tracking-wide text-(--muted)">{data.heading}</p>
              ) : null}
              {/* Textbook source is Markdown + LaTeX — render it, don't dump raw. */}
              <ExplanationBlock
                block={{ id: `${recordId}-source`, type: "explanation", content: data.content }}
              />
            </div>
          ) : null}
        </div>
      ) : null}
    </li>
  );
}

/**
 * Renders a lesson plan's source references as one collapsible entry per chapter
 * (so the list no longer blows up), each expandable to its individual source chunks
 * — and each chunk is clickable to read the actual textbook content it was grounded on.
 */
export function SourceReferences({ references }: { references: string[] }) {
  const groups = groupReferencesByChapter(references);
  if (groups.length === 0) return null;

  return (
    <div className="space-y-1">
      {groups.map((group) => (
        <details key={group.label}>
          <summary className="flex cursor-pointer items-center gap-2 py-1 text-sm text-(--ink)">
            <span className="min-w-0 flex-1 [overflow-wrap:anywhere]">{group.label}</span>
            {group.records.length ? (
              <span className="shrink-0 text-[11px] text-(--muted)">
                {group.records.length} source{group.records.length > 1 ? "s" : ""}
              </span>
            ) : null}
          </summary>
          {group.records.length ? (
            <ul className="space-y-1 pb-2 pl-4">
              {group.records.map((record, index) => (
                <SourceRecordRow
                  key={record.recordId}
                  recordId={record.recordId}
                  label={`Source ${index + 1}`}
                />
              ))}
            </ul>
          ) : null}
        </details>
      ))}
    </div>
  );
}
