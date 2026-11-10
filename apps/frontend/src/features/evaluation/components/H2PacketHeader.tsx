import { ReactNode } from "react";

import { Button } from "@/shared/components/ui/Button";

import { CompactLearnerTrait } from "../services/raterPresentation";

type H2PacketHeaderProps = {
  activeIndex: number;
  activeObjectiveText: string;
  /**
   * The recorded misconception for the active objective (from
   * `focal_learner.objective_states[*].misconception_description`).
   * Surfaced so the rater knows when to mark Misconception help N/A — if
   * `null` / undefined, no misconception is recorded for this objective.
   */
  activeObjectiveMisconception?: string | null;
  activeSectionTitle?: string | null;
  learnerSummary: string;
  learnerTraits: CompactLearnerTrait[];
  lessonTitle?: string | null;
  lessonSubtitle?: string | null;
  masteredSection?: string | null;
  objectiveCount: number;
  onOpenPacketBrief?: () => void;
  sectionCount: number;
  sectionStatus: string;
};

const ContextCard = ({
  children,
  label,
  tone = "default",
}: {
  children: ReactNode;
  label: string;
  tone?: "default" | "accent";
}) => (
  <div className="min-w-0 px-4 py-3">
    <p className="text-[0.65rem] font-semibold uppercase tracking-[0.16em] text-[color:var(--muted)]">
      {label}
    </p>
    <div
      className={`mt-2 text-sm leading-5 ${
        tone === "accent" ? "text-[color:var(--accent-deep)]" : "text-[color:var(--ink)]"
      }`}
    >
      {children}
    </div>
  </div>
);

/** Renders the compact H2 section orientation strip. */
export function H2PacketHeader({
  activeIndex,
  activeObjectiveText,
  activeObjectiveMisconception,
  activeSectionTitle,
  learnerSummary,
  learnerTraits,
  lessonTitle,
  lessonSubtitle,
  masteredSection,
  objectiveCount,
  onOpenPacketBrief,
  sectionCount,
  sectionStatus,
}: H2PacketHeaderProps) {
  const learnerTraitSummary = learnerTraits.map((trait) => `${trait.key}: ${trait.value}`).join(" · ");
  const lessonFocus = lessonSubtitle ?? lessonTitle ?? "Lesson focus unavailable";
  const showSecondaryLessonLine = lessonSubtitle && lessonTitle && lessonTitle !== lessonSubtitle;

  return (
    <section className="shrink-0 rounded-none border border-[color:var(--line)] bg-white px-4 py-3">
      <div className="flex flex-col gap-3">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
            <p className="text-sm font-medium text-[color:var(--muted)]">
              Section {activeIndex + 1} of {sectionCount}
            </p>
            <p className="text-sm font-medium text-[color:var(--accent-deep)]">
              {objectiveCount} objective{objectiveCount === 1 ? "" : "s"} in scope
            </p>
            {activeSectionTitle ? (
              <p className="text-sm text-[color:var(--muted)]">{activeSectionTitle}</p>
            ) : null}
          </div>
          {onOpenPacketBrief ? (
            <Button onClick={onOpenPacketBrief} size="sm" type="button" variant="outline">
              View packet brief
            </Button>
          ) : null}
        </div>

        <div className="min-w-0">
          <h1 className="text-xl font-semibold text-[color:var(--ink)] sm:text-2xl">
            Compare the candidate versions
          </h1>
          <p className="mt-1 text-sm leading-6 text-[color:var(--muted)]">
            Decide how well each candidate version fits this learner without losing the lesson
            goal.
          </p>
        </div>

        <div className="min-w-0 rounded-none border border-[color:var(--line)] bg-[color:var(--panel)]">
          <div className="grid gap-0 sm:grid-cols-2 min-[1200px]:grid-cols-4">
            <div className="border-b border-[color:var(--line)] sm:border-r sm:last:border-r-0 min-[1200px]:border-b-0 min-[1200px]:border-r">
              <ContextCard label="Lesson focus">
                <p className="font-semibold text-[color:var(--ink)]">{lessonFocus}</p>
                {showSecondaryLessonLine ? (
                  <p className="mt-1 text-xs leading-5 text-[color:var(--muted)]">{lessonTitle}</p>
                ) : null}
              </ContextCard>
            </div>

            <div className="border-b border-[color:var(--line)] min-[1200px]:border-b-0 min-[1200px]:border-r">
              <ContextCard label="Active objective">
                <p>{activeObjectiveText}</p>
                <p className="mt-2 text-xs leading-5 text-[color:var(--muted)]">
                  {activeObjectiveMisconception?.trim()
                    ? `Recorded misconception: ${activeObjectiveMisconception.trim()}`
                    : "No misconception recorded — mark Misconception help N/A."}
                </p>
              </ContextCard>
            </div>

            <div className="border-b border-[color:var(--line)] sm:border-r sm:border-b-0 min-[1200px]:border-r">
              <ContextCard label="Learner profile in view">
                <div className="space-y-1.5">
                  <p className="font-semibold text-[color:var(--ink)]">{learnerSummary}</p>
                  {learnerTraitSummary ? (
                    <p className="text-xs leading-5 text-[color:var(--muted)]">{learnerTraitSummary}</p>
                  ) : null}
                  {masteredSection ? (
                    <p className="text-xs leading-5 text-[color:var(--muted)]">
                      Already secure: {masteredSection}
                    </p>
                  ) : null}
                </div>
              </ContextCard>
            </div>

            <div>
              <ContextCard label="Section status" tone="accent">
                <p>{sectionStatus}</p>
              </ContextCard>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
