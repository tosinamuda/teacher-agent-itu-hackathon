import { Card } from "@/shared/components/ui/Card";

import { EvaluationReviewPackManifest } from "../types";
import { ReviewPackStepCard } from "./ReviewPackStepCard";

type ReviewPackPreviewProps = {
  label: string;
  /** Any pack-shaped object carrying a manifest (full packs or blinded candidates). */
  pack: { manifest: EvaluationReviewPackManifest };
  tone?: "base" | "candidate";
  showStepNavigator?: boolean;
  anchorPrefix?: string;
  showLabel?: boolean;
};

/** Renders a full review pack in a read-only layout suitable for rating. */
export function ReviewPackPreview({
  label,
  pack,
  tone = "candidate",
  showStepNavigator = false,
  anchorPrefix = "review-pack",
  showLabel = true,
}: ReviewPackPreviewProps) {
  const manifest = pack.manifest;
  // Position, never step_id: a raw id reads `objective:<lop>` for the
  // objective-unit condition and `step:<plan step id>` for the others, so
  // exposing it in a link target would let a blinded rater sort packs by
  // condition. Pairing and provenance keep using step_id server-side.
  const stepAnchor = (index: number) =>
    `${anchorPrefix}-section-${String(index + 1).padStart(2, "0")}`;
  const heading = manifest.subtopic ?? manifest.topic ?? "Review pack";
  const supportingMeta =
    [
      manifest.subject,
      manifest.grade,
      manifest.term,
      manifest.week ? `Week ${manifest.week}` : null,
      `${manifest.steps.length} section${manifest.steps.length === 1 ? "" : "s"}`,
    ]
      .filter(Boolean)
      .join(" · ") || "Structured review material";

  return (
    <Card padding="lg" className="space-y-6">
      <div className="space-y-2">
        {showLabel ? (
          <p className="text-sm font-medium text-[color:var(--muted)]">{label}</p>
        ) : null}
        <div className="space-y-1">
          <h3 className="text-2xl font-semibold text-[color:var(--ink)]">{heading}</h3>
          <p className="text-base text-[color:var(--muted)]">{supportingMeta}</p>
        </div>
      </div>

      {showStepNavigator && manifest.steps.length > 0 ? (
        <div className="space-y-3 rounded-none border border-[color:var(--line)] bg-[color:var(--panel)] p-4">
          <p className="text-sm font-semibold text-[color:var(--ink)]">Jump to section</p>
          <div className="flex flex-wrap gap-2">
            {manifest.steps.map((step, index) => (
              <a
                key={step.step_id}
                className="rounded-none border border-[color:var(--line)] bg-white px-3 py-2 text-sm font-medium text-[color:var(--ink)] transition hover:border-[color:var(--accent)]"
                href={`#${stepAnchor(index)}`}
              >
                {index + 1}. {step.title ?? `Section ${index + 1}`}
              </a>
            ))}
          </div>
        </div>
      ) : null}

      {manifest.misconceptions?.length ? (
        <div className="rounded-none border border-[color:var(--line)] bg-[color:var(--panel)] p-4">
          <p className="text-sm font-semibold text-[color:var(--ink)]">Known misconceptions</p>
          <ul className="mt-2 space-y-1 text-sm text-[color:var(--muted)]">
            {manifest.misconceptions.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      ) : null}

      <div className="space-y-4">
        {manifest.steps.map((step, index) => (
          <ReviewPackStepCard
            key={step.step_id}
            anchorId={stepAnchor(index)}
            step={step}
            tone={tone}
          />
        ))}
      </div>
    </Card>
  );
}
