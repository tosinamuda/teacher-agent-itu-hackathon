import { ContentBlockRenderer } from "@/shared/components/renderer/ContentBlockRenderer";

import { alignSections } from "../lib/compareAlign";
import { ComparePackManifest, ComparePackStep } from "../lib/experiments";

type SectionCompareProps = {
  leftLabel: string;
  rightLabel: string;
  leftBadge?: string;
  rightBadge?: string;
  left: ComparePackManifest | null;
  right: ComparePackManifest | null;
  /** Set inside a white panel, so the sticky labels are backed by the panel's colour. */
  onSurface?: boolean;
};

function Cell({ step, label }: { step: ComparePackStep | null; label: string }) {
  return (
    <div className="min-w-0 space-y-3">
      {/* Stacked on a narrow screen, each note names itself; side by side, the sticky row does. */}
      <p className="text-xs text-(--muted) md:hidden">{label}</p>
      {step ? (
        step.blocks.map((block, index) => (
          <ContentBlockRenderer key={block.id ?? `${step.step_id}-${index}`} block={block} />
        ))
      ) : (
        <p className="text-sm text-(--muted)">No section here.</p>
      )}
    </div>
  );
}

function Label({ text, badge }: { text: string; badge?: string }) {
  return (
    <p className="text-sm font-medium text-(--ink)">
      {text}
      {badge ? <span className="ml-2 font-normal text-(--muted)">{badge}</span> : null}
    </p>
  );
}

/**
 * Two packs compared side by side, aligned section by section (the same lesson objective on
 * each side), so they read like for like. The two labels stay in view while scrolling.
 */
export function SectionCompare({
  leftLabel,
  rightLabel,
  leftBadge,
  rightBadge,
  left,
  right,
  onSurface = false,
}: SectionCompareProps) {
  const rows = alignSections(left, right);
  if (rows.length === 0) {
    return <p className="text-sm text-(--muted)">Nothing to compare.</p>;
  }

  return (
    <div className="space-y-8">
      <div
        className={`sticky top-0 z-10 hidden grid-cols-2 gap-8 border-b border-(--line) py-2 md:grid ${
          onSurface ? "bg-(--surface)" : "bg-(--bg)"
        }`}
      >
        <Label text={leftLabel} badge={leftBadge} />
        <Label text={rightLabel} badge={rightBadge} />
      </div>
      {rows.map((row) => (
        <section key={row.key} className="space-y-3">
          <h3 className="font-semibold text-(--ink)">{row.title}</h3>
          <div className="grid gap-6 md:grid-cols-2 md:gap-8">
            <Cell step={row.left} label={leftLabel} />
            <Cell step={row.right} label={rightLabel} />
          </div>
        </section>
      ))}
    </div>
  );
}
