import { Button } from "@/shared/components/ui/Button";

import { EvaluationDisclosure } from "./EvaluationDisclosure";
import { ContextRow, DrawerSection, ObjectivesPanel, ReferenceSheetContent } from "./PacketMetaPanels";
import {
  formatMasteredSection,
  getCompactLearnerTraits,
  getLearnerSummary,
} from "../services/raterPresentation";
import { H1PacketDetail, H2PacketDetail } from "../types";

/** Renders the H1 packet drawer with lesson reference details. */
export function H1DrawerContent({ detail }: { detail: H1PacketDetail }) {
  const referenceSummary = [
    detail.reference_sheet.subject,
    detail.reference_sheet.grade,
    detail.reference_sheet.term,
    detail.reference_sheet.week ? `Week ${detail.reference_sheet.week}` : null,
  ]
    .filter(Boolean)
    .join(" · ");

  return (
    <div className="space-y-5">
      <DrawerSection title="Lesson reference">
        <dl className="grid gap-3">
          <ContextRow label="Class" value={detail.reference_sheet.grade} />
          <ContextRow label="Subject" value={detail.reference_sheet.subject} />
          <ContextRow label="Subtopic" value={detail.reference_sheet.subtopic} />
        </dl>
      </DrawerSection>

      <EvaluationDisclosure summary={referenceSummary} title="Lesson reference sheet">
        <ReferenceSheetContent referenceSheet={detail.reference_sheet} />
      </EvaluationDisclosure>
    </div>
  );
}

/** Renders the H2 packet drawer with learner context and reference aids. */
export function H2DrawerContent({
  detail,
  onOpenCandidatePack,
}: {
  detail: H2PacketDetail;
  /** Opens the full-pack preview for one anonymous candidate. */
  onOpenCandidatePack: (candidateId: string) => void;
}) {
  const learnerTraits = getCompactLearnerTraits(detail.focal_learner.preferences);

  return (
    <div className="space-y-5">
      <DrawerSection title="Learner context">
        <p className="text-base font-semibold text-[color:var(--ink)]">
          {getLearnerSummary(detail.focal_learner)}
        </p>
        <p className="text-sm leading-6 text-[color:var(--muted)]">
          This learner profile is the context used for the comparison in this revision note.
        </p>
        {learnerTraits.length ? (
          <dl className="space-y-3">
            {learnerTraits.map((trait) => (
              <ContextRow key={trait.key} label={trait.key} value={trait.value} />
            ))}
          </dl>
        ) : null}
      </DrawerSection>

      <EvaluationDisclosure
        summary={`${detail.objectives.length} objective${detail.objectives.length === 1 ? "" : "s"} · ${
          detail.focal_learner.mastered_sections.length
        } mastered section${detail.focal_learner.mastered_sections.length === 1 ? "" : "s"}`}
        title="Reference aids"
      >
        <div className="space-y-5">
          <div className="space-y-3">
            <p className="text-sm font-semibold text-[color:var(--ink)]">Lesson objectives</p>
            <ObjectivesPanel objectives={detail.objectives} />
          </div>

          <div className="space-y-3">
            <p className="text-sm font-semibold text-[color:var(--ink)]">Mastered sections</p>
            {detail.focal_learner.mastered_sections.length ? (
              <ul className="space-y-2">
                {detail.focal_learner.mastered_sections.map((section, index) => (
                  <li
                    key={`${formatMasteredSection(section)}-${index}`}
                    className="rounded-none border border-[color:var(--line)] bg-white px-4 py-3 text-sm text-[color:var(--muted)]"
                  >
                    {formatMasteredSection(section)}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-[color:var(--muted)]">No mastered sections recorded.</p>
            )}
          </div>

          <div className="space-y-3">
            <p className="text-sm font-semibold text-[color:var(--ink)]">Full-pack references</p>
            <div className="flex flex-col gap-3">
              {detail.candidates.map((candidate) => (
                <Button
                  key={candidate.candidate_id}
                  onClick={() => onOpenCandidatePack(candidate.candidate_id)}
                  type="button"
                  variant="outline"
                >
                  View full {candidate.label} pack
                </Button>
              ))}
            </div>
          </div>
        </div>
      </EvaluationDisclosure>
    </div>
  );
}
