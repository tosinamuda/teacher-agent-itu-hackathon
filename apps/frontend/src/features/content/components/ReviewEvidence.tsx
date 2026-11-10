import { RichText } from "@/shared/components/renderer/RichText";

import { useSpec } from "../hooks/useContent";
import {
  checkLabel,
  passageFor,
  sectionCitations,
  specRevisionOf,
} from "../evidence";
import { ContentItem } from "../types";

function Checks({ item }: { item: ContentItem }) {
  const record = item.review;
  if (!record || record.checks.length === 0) return null;
  const passed = record.checks.filter((check) => check.passed).length;
  return (
    <details open={passed < record.checks.length} className="text-xs">
      <summary className="cursor-pointer text-sm font-semibold text-(--ink)">
        Checks{" "}
        <span className="font-normal text-(--muted)">
          · {passed} of {record.checks.length} passed
        </span>
      </summary>
      <ul className="mt-1.5 space-y-1">
        {record.checks.map((check) => (
          <li key={check.check} className="flex items-start gap-2">
            <span
              aria-hidden
              className={
                check.passed ? "text-(--accent-deep)" : "text-(--danger-ink)"
              }
            >
              {check.passed ? "✓" : "✕"}
            </span>
            <span className="sr-only">
              {check.passed ? "Passed" : "Not met"}
            </span>
            <span className="text-(--ink-2)">
              {checkLabel(check.check)}
              {!check.passed && check.message ? (
                <span className="block text-(--muted)">{check.message}</span>
              ) : null}
            </span>
          </li>
        ))}
      </ul>
      {record.version !== item.version ? (
        <p className="mt-1.5 text-(--muted)">
          These ran on version {record.version}; it has changed since.
        </p>
      ) : null}
    </details>
  );
}

function Passages({ item, section }: { item: ContentItem; section: number }) {
  const record = item.review;
  const cited = sectionCitations(item)[section];
  if (!record || !cited) return null;
  return (
    <details className="text-xs">
      <summary className="cursor-pointer text-sm font-semibold text-(--ink)">
        Cited in this section{" "}
        <span className="font-normal text-(--muted)">
          · {cited.refs.length === 0 ? "none" : cited.refs.length}
        </span>
      </summary>
      <p className="mt-1.5 text-(--muted)">{cited.title}</p>
      {cited.refs.length === 0 ? (
        <p className="mt-1 text-(--muted)">This section cites no passage.</p>
      ) : null}
      <div className="mt-1.5 space-y-1.5">
        {cited.refs.map((ref) => {
          const passage = passageFor(record, ref);
          return (
            <details key={ref} className="border-l-2 border-(--line) pl-2">
              <summary className="cursor-pointer text-(--ink-2)">
                {ref}
                {passage?.title ? ` · ${passage.title}` : ""}
              </summary>
              <div className="prose prose-sm relative mt-1 max-h-56 max-w-none overflow-y-auto overscroll-contain text-xs text-(--muted)">
                {passage ? (
                  <RichText text={passage.excerpt} tables />
                ) : (
                  <p>The passage was not recorded.</p>
                )}
              </div>
            </details>
          );
        })}
      </div>
    </details>
  );
}

function WrittenTo({ item }: { item: ContentItem }) {
  const spec = useSpec(item.type, specRevisionOf(item));
  const requirements = spec.data?.requirements ?? [];
  if (requirements.length === 0) return null;
  return (
    <details className="text-xs">
      <summary className="cursor-pointer text-sm font-semibold text-(--ink)">
        What it was written to ({requirements.length})
      </summary>
      <p className="mt-1.5 text-(--muted)">
        The requirements the writer was given. The app checks some of them,
        above; read the note against the rest.
      </p>
      <ul className="mt-1.5 list-disc space-y-1 pl-4 text-(--ink-2)">
        {requirements.map((requirement) => (
          <li key={requirement}>{requirement}</li>
        ))}
      </ul>
    </details>
  );
}

/** The evidence beside content: the checks, for a note what the section being read cites, and what it was written to. */
export function ReviewEvidence({
  item,
  section = 0,
}: {
  item: ContentItem;
  section?: number;
}) {
  if (!item.review) return null;
  return (
    <section className="space-y-3">
      <h2 className="text-base font-semibold text-(--ink)">Evidence</h2>
      <Checks item={item} />
      {item.type === "revision-note" ? (
        <Passages item={item} section={section} />
      ) : null}
      <WrittenTo item={item} />
    </section>
  );
}
