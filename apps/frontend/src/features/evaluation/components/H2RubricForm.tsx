import { useRouter } from "@/shared/router";
import { ReactNode, useCallback, useMemo, useState } from "react";
import { useForm, useWatch } from "react-hook-form";

import { Button } from "@/shared/components/ui/Button";

import { EvaluationDisclosure } from "./EvaluationDisclosure";
import { H2PacketHeader } from "./H2PacketHeader";
import { H2SectionRatingStrip } from "./H2SectionRatingStrip";
import { ReviewPackStepCard } from "./ReviewPackStepCard";
import {
  buildInitialDrafts,
  candidateFormKey,
  H2CandidateDrafts,
  H2RubricFormValues,
  H2SectionDraft,
  isSectionComplete,
  isSectionStarted,
  mergeDraft,
  sectionCandidatesStatus,
  sectionFormKey,
  sectionStatusSummary,
} from "../services/h2Rating";
import {
  formatMasteredSection,
  getCompactLearnerTraits,
  getLearnerSummary,
  misconceptionText,
} from "../services/raterPresentation";
import {
  EvaluationNoteFields,
  H2CandidateScoresSaveRequest,
  H2PacketDetail,
} from "../types";

type H2RubricFormProps = {
  detail: H2PacketDetail;
  isSaving: boolean;
  onOpenPacketBrief?: () => void;
  nextPacketHref?: string;
  onSubmit: (payload: {
    candidate_section_scores: H2CandidateScoresSaveRequest[];
    notes?: EvaluationNoteFields | null;
  }) => Promise<void>;
};

const notesSummary = (notes: H2RubricFormValues["notes"]) => {
  const count = [notes.strengths, notes.concerns, notes.recommendation].filter((value) =>
    value.trim()
  ).length;
  if (count === 0) {
    return "Optional revision-note comments";
  }
  return `${count} comment field${count === 1 ? "" : "s"} added`;
};

const formatSavedLabel = (timestamp: string | null) => {
  if (!timestamp) {
    return "No changes saved yet";
  }

  return `Saved at ${new Intl.DateTimeFormat(undefined, {
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date(timestamp))}`;
};

const formatLearnerProfileText = (
  detail: H2PacketDetail,
  learnerTraits: ReturnType<typeof getCompactLearnerTraits>
) => {
  const summary = getLearnerSummary(detail.focal_learner);
  const traitText = learnerTraits.map((trait) => `${trait.key}: ${trait.value}`).join(" · ");

  if (!traitText) {
    return summary;
  }

  return `${summary} · ${traitText}`;
};

const WorkspacePane = ({
  title,
  description,
  headerDetail,
  children,
}: {
  title: string;
  description: string;
  headerDetail?: ReactNode;
  children: ReactNode;
}) => (
  <section className="flex h-full min-h-0 flex-col overflow-hidden rounded-none border border-[color:var(--line)] bg-[color:var(--panel)]">
    <header className="shrink-0 border-b border-[color:var(--line)] px-4 py-3">
      <p className="text-sm font-semibold text-[color:var(--ink)]">{title}</p>
      <p className="mt-1 text-sm leading-6 text-[color:var(--muted)]">{description}</p>
      {headerDetail ? <div className="mt-3">{headerDetail}</div> : null}
    </header>
    <div className="min-h-0 p-4 min-[1200px]:overflow-y-auto">{children}</div>
  </section>
);

const RatingBand = ({
  canGoPrevious,
  children,
  isRevealed,
  nextLabel,
  onNext,
  onPrevious,
  onRateNow,
  onSkipForNow,
  sectionStatus,
  showWarning,
}: {
  canGoPrevious: boolean;
  children?: ReactNode;
  isRevealed: boolean;
  nextLabel: string;
  onNext: () => void;
  onPrevious: () => void;
  onRateNow: () => void;
  onSkipForNow: () => void;
  sectionStatus: string;
  showWarning: boolean;
}) => (
  <section className="rounded-none border border-[color:var(--line)] bg-[color:var(--panel)]">
    <header className="flex flex-wrap items-center justify-between gap-3 border-b border-[color:var(--line)] px-4 py-3">
      <div>
        <p className="text-sm font-semibold text-[color:var(--ink)]">Section rating</p>
        <p className="mt-0.5 text-sm leading-6 text-[color:var(--muted)]">
          {isRevealed
            ? "Score each candidate independently."
            : "Read every candidate version above first, then reveal the scoring controls."}
        </p>
      </div>
      <p className="text-xs font-medium text-[color:var(--accent-deep)]">{sectionStatus}</p>
    </header>

    <div className="p-4">
      {isRevealed ? (
        <div className="grid gap-3 md:grid-cols-2">{children}</div>
      ) : (
        <div className="flex flex-wrap items-center justify-between gap-3 rounded-none border border-dashed border-[color:var(--line)] bg-white px-4 py-4">
          <p className="text-sm leading-6 text-[color:var(--muted)]">
            Open the scoring controls when you are ready to judge this section.
          </p>
          <Button onClick={onRateNow} size="sm" type="button">
            Rate this section
          </Button>
        </div>
      )}
    </div>

    <div className="border-t border-[color:var(--line)] bg-(--surface) px-4 py-4">
      {showWarning ? (
        <div className="mb-4 rounded-none border border-[color:var(--line)] bg-[color:var(--panel)] px-4 py-3">
          <p className="text-sm leading-6 text-[color:var(--muted)]">
            This section is not fully rated yet. Rate it now or skip it and return before the
            final save.
          </p>
          <div className="mt-3 flex flex-wrap gap-2">
            <Button onClick={onRateNow} size="sm" type="button">
              Rate now
            </Button>
            <Button onClick={onSkipForNow} size="sm" type="button" variant="outline">
              Skip for now
            </Button>
          </div>
        </div>
      ) : null}

      <div className="flex flex-wrap items-center justify-end gap-2">
        <Button
          disabled={!canGoPrevious}
          onClick={onPrevious}
          size="sm"
          type="button"
          variant="outline"
        >
          Previous
        </Button>
        <Button onClick={onNext} size="sm" type="button">
          {nextLabel}
        </Button>
      </div>
    </div>
  </section>
);

/** Wraps one candidate's rating strip with its label and progress line. */
const RatingGroup = ({
  title,
  subtitle,
  status,
  children,
}: {
  title: string;
  subtitle: string;
  status: string;
  children: ReactNode;
}) => (
  <div className="space-y-2 rounded-none border border-[color:var(--line)] bg-(--surface) p-3">
    <div className="space-y-1">
      <p className="text-xs font-semibold uppercase tracking-[0.14em] text-[color:var(--accent-deep)]">
        {title}
      </p>
      <p className="text-xs leading-5 text-[color:var(--muted)]">{subtitle}</p>
      <p className="text-[11px] font-medium text-[color:var(--accent-deep)]">{status}</p>
    </div>
    {children}
  </div>
);

/**
 * Renders the BLINDED H2 packet workspace: anonymous candidate versions compared
 * section by section, each candidate scored independently. The form never knows
 * which candidate is the class pack and which is personalised — scores are keyed
 * by `candidate_id` and de-anonymised server-side.
 */
export function H2RubricForm({
  detail,
  isSaving,
  onOpenPacketBrief,
  nextPacketHref,
  onSubmit,
}: H2RubricFormProps) {
  const router = useRouter();
  const candidates = useMemo(
    () => [...detail.candidates].sort((a, b) => a.display_order - b.display_order),
    [detail.candidates]
  );
  const initialDrafts = useMemo(() => buildInitialDrafts(detail), [detail]);
  const learnerTraits = useMemo(
    () => getCompactLearnerTraits(detail.focal_learner.preferences),
    [detail.focal_learner.preferences]
  );
  // A section is finished only once EVERY candidate's strip is fully scored —
  // the rater scores each candidate independently.
  const isSectionAllRated = useCallback(
    (drafts: H2CandidateDrafts, formKey: string) =>
      candidates.every((candidate) =>
        isSectionComplete(drafts[candidateFormKey(candidate.display_order)]?.[formKey])
      ),
    [candidates]
  );
  const initialIndex = useMemo(() => {
    const firstIncomplete = detail.sections.findIndex(
      (_section, index) => !isSectionAllRated(initialDrafts, sectionFormKey(index))
    );
    return firstIncomplete >= 0 ? firstIncomplete : 0;
  }, [detail.sections, initialDrafts, isSectionAllRated]);
  const [activeIndex, setActiveIndex] = useState(initialIndex);
  const [revealedSections, setRevealedSections] = useState<Record<string, boolean>>(() =>
    Object.fromEntries(
      detail.sections.map((section, index) => [
        section.section_id,
        candidates.some((candidate) =>
          isSectionStarted(
            initialDrafts[candidateFormKey(candidate.display_order)]?.[sectionFormKey(index)]
          )
        ),
      ])
    )
  );
  const [navigationWarningFor, setNavigationWarningFor] = useState<string | null>(null);
  const [lastSavedAt, setLastSavedAt] = useState<string | null>(
    detail.existing_rating?.submitted_at ?? detail.existing_rating?.updated_at ?? null
  );
  const [hasSavedRating, setHasSavedRating] = useState(Boolean(detail.existing_rating));

  const form = useForm<H2RubricFormValues>({
    mode: "onChange",
    // The stepper renders only the active section, so each section's score fields
    // unmount as the rater advances. Keep their values registered so prefilled
    // (and freshly entered) scores for non-active sections survive navigation —
    // otherwise completeness/save would only ever see the current section.
    shouldUnregister: false,
    defaultValues: {
      candidate_scores: initialDrafts,
      notes: {
        strengths: String(detail.existing_rating?.notes?.strengths ?? ""),
        concerns: String(detail.existing_rating?.notes?.concerns ?? ""),
        recommendation: String(detail.existing_rating?.notes?.recommendation ?? ""),
      },
    },
  });

  const notes = useWatch({
    control: form.control,
    name: "notes",
  });

  // The stepper mounts only the active section's score fields, so a parent watch
  // only ever reflects the current section. Keep every candidate × section draft in
  // state (seeded with the prefilled values) and refresh the active section into it
  // on navigation, so completeness and the save payload see ALL sections.
  const [candidateScores, setCandidateScores] = useState<H2CandidateDrafts>(initialDrafts);
  const candidateScoresWatch = useWatch({
    control: form.control,
    name: "candidate_scores",
  });

  const isFinalStep = activeIndex >= detail.sections.length;
  const activeSection = isFinalStep ? null : detail.sections[activeIndex];
  const activeSectionKey = sectionFormKey(activeIndex);
  // The watch only carries dimensions the rater has touched on this step, so fold
  // it over each candidate's seeded/accumulated draft for the full live picture.
  const activeDraftFor = useCallback(
    (candidateKey: string): H2SectionDraft =>
      mergeDraft(
        candidateScores[candidateKey]?.[activeSectionKey],
        (candidateScoresWatch as H2CandidateDrafts | undefined)?.[candidateKey]?.[
          activeSectionKey
        ]
      ),
    [candidateScores, candidateScoresWatch, activeSectionKey]
  );
  const activeCandidateDrafts = candidates.map((candidate) => ({
    label: candidate.label,
    draft: activeSection ? activeDraftFor(candidateFormKey(candidate.display_order)) : undefined,
  }));
  const learnerProfileText = formatLearnerProfileText(detail, learnerTraits);
  const activeObjectiveId = activeSection?.lesson_objective_id ?? null;
  const activeObjectiveText =
    detail.objectives.find(
      (objective) => objective.lesson_objective_id === activeObjectiveId
    )?.objective_text ?? activeSection?.objective_text ?? "Objective unavailable";
  const activeObjectiveMisconception = misconceptionText(
    detail.focal_learner.objective_states?.find(
      (state) => state.lesson_objective_id === activeObjectiveId
    )
  );
  const activeSectionTitle = activeSection?.title ?? "Current section";
  const masteredSection = detail.focal_learner.mastered_sections[0]
    ? formatMasteredSection(detail.focal_learner.mastered_sections[0])
    : null;
  const ratedCount = detail.sections.filter((_section, index) =>
    isSectionAllRated(candidateScores, sectionFormKey(index))
  ).length;
  const missingSections = detail.sections.filter(
    (_section, index) => !isSectionAllRated(candidateScores, sectionFormKey(index))
  );
  const canFinalize = missingSections.length === 0;
  const canSave = canFinalize;
  const hasUnsavedChanges = form.formState.isDirty;
  const showSaveAction = !hasSavedRating || hasUnsavedChanges;
  const showNextAction = Boolean(nextPacketHref && hasSavedRating && !hasUnsavedChanges);
  const nextActionLabel = hasUnsavedChanges
    ? "Save and open next revision note"
    : "Open next revision note";
  const statusMessage = !canSave
    ? "Finish every candidate's section scores before saving"
    : showNextAction && !showSaveAction
    ? "This rating is saved. Open the next revision note when you are ready."
    : hasUnsavedChanges
    ? "Unsaved changes"
    : formatSavedLabel(lastSavedAt);

  const revealSection = (sectionId: string) => {
    setNavigationWarningFor(null);
    setRevealedSections((current) => ({
      ...current,
      [sectionId]: true,
    }));
  };

  // Snapshot the mounted section's live (merged) values into the accumulated
  // drafts so they survive the stepper unmounting it on navigation.
  const captureActiveSection = () => {
    if (isFinalStep || !activeSection) {
      return;
    }
    setCandidateScores((previous) => {
      const next: H2CandidateDrafts = { ...previous };
      for (const candidate of candidates) {
        const candidateKey = candidateFormKey(candidate.display_order);
        next[candidateKey] = {
          ...next[candidateKey],
          [activeSectionKey]: activeDraftFor(candidateKey),
        };
      }
      return next;
    });
  };

  const goToStep = (nextIndex: number) => {
    captureActiveSection();
    setNavigationWarningFor(null);
    setActiveIndex(nextIndex);
  };

  const handleNext = () => {
    if (!activeSection) {
      return;
    }
    if (!activeCandidateDrafts.every(({ draft }) => isSectionComplete(draft))) {
      setNavigationWarningFor(activeSection.section_id);
      return;
    }
    goToStep(Math.min(detail.sections.length, activeIndex + 1));
  };

  const toSectionRow = (section_id: string, draft: H2SectionDraft) => ({
    section_id,
    learner_state_suitability: Number(draft.learner_state_suitability),
    scaffolding_appropriateness: Number(draft.scaffolding_appropriateness),
    challenge_calibration: Number(draft.challenge_calibration),
    misconception_support:
      draft.misconception_support === "na" ? null : Number(draft.misconception_support),
    objective_preservation: Number(draft.objective_preservation),
  });

  const saveValues = async (values: H2RubricFormValues, navigateToNext: boolean) => {
    if (!canSave) {
      return;
    }

    // Fold the mounted section's live values over the accumulated drafts so the
    // payload reflects every section, including any edit on the active step.
    const merged: H2CandidateDrafts = { ...candidateScores };
    if (activeSection) {
      for (const candidate of candidates) {
        const candidateKey = candidateFormKey(candidate.display_order);
        merged[candidateKey] = {
          ...merged[candidateKey],
          [activeSectionKey]: activeDraftFor(candidateKey),
        };
      }
    }

    await onSubmit({
      candidate_section_scores: candidates.map((candidate) => ({
        candidate_id: candidate.candidate_id,
        section_scores: detail.sections.map((section, index) =>
          toSectionRow(
            section.section_id,
            merged[candidateFormKey(candidate.display_order)][sectionFormKey(index)]
          )
        ),
      })),
      notes: values.notes,
    });

    const savedAt = new Date().toISOString();
    setLastSavedAt(savedAt);
    setHasSavedRating(true);
    setCandidateScores(merged);
    form.reset({
      candidate_scores: merged,
      notes: values.notes,
    });
    if (navigateToNext && nextPacketHref) {
      router.push(nextPacketHref);
    }
  };

  return (
    <form
      className="flex min-h-0 flex-col gap-4 px-4 py-4 min-[1200px]:h-full min-[1200px]:overflow-hidden min-[1200px]:px-6"
      onSubmit={form.handleSubmit(async (values) => {
        await saveValues(values, true);
      })}
    >
      {isFinalStep ? (
        <>
          <section className="shrink-0 rounded-none border border-[color:var(--line)] bg-white px-5 py-4">
            <div className="flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
              <div className="min-w-0 flex-1 space-y-2">
                <p className="text-sm font-medium text-[color:var(--muted)]">Finalize this revision note</p>
                <h1 className="text-2xl font-semibold text-[color:var(--ink)]">
                  Finish the candidate comparison
                </h1>
                <p className="text-sm leading-6 text-[color:var(--muted)]">
                  Review any missing sections, then save the revision note.
                </p>
              </div>
              <div className="rounded-none border border-[color:var(--line)] bg-[color:var(--panel)] px-4 py-3 xl:w-[22rem] xl:shrink-0">
                <p className="text-xs font-semibold uppercase tracking-[0.14em] text-[color:var(--muted)]">
                  Completion
                </p>
                <p className="mt-2 text-base font-semibold text-[color:var(--ink)]">
                  {ratedCount} of {detail.sections.length} sections rated
                </p>
                <p className="mt-2 text-sm text-[color:var(--muted)]">
                  {canFinalize
                    ? "All section comparisons are complete."
                    : "You need to finish every section before saving."}
                </p>
              </div>
            </div>
          </section>

          <section className="rounded-none border border-[color:var(--line)] bg-white p-4 min-[1200px]:flex-1 min-[1200px]:min-h-0 min-[1200px]:overflow-hidden">
            <div className="flex flex-col gap-4 min-[1200px]:h-full min-[1200px]:min-h-0 min-[1200px]:flex-row">
              <div className="min-h-0 min-w-0 flex-1 rounded-none border border-[color:var(--line)] bg-[color:var(--panel)] p-4 min-[1200px]:overflow-y-auto">
                <div className="space-y-3">
                  <p className="text-sm font-semibold text-[color:var(--ink)]">Section checklist</p>
                  {detail.sections.map((section, index) => {
                    const complete = isSectionAllRated(candidateScores, sectionFormKey(index));
                    return (
                      <button
                        key={section.section_id}
                        className="flex w-full items-center justify-between rounded-none border border-[color:var(--line)] bg-white px-4 py-3 text-left transition hover:border-[color:var(--accent)]"
                        onClick={() => goToStep(index)}
                        type="button"
                      >
                        <div className="space-y-1">
                          <p className="text-sm font-semibold text-[color:var(--ink)]">
                            {section.title ?? `Section ${index + 1}`}
                          </p>
                          <p className="text-sm text-[color:var(--muted)]">
                            {section.objective_text ?? "Objective not available"}
                          </p>
                        </div>
                        <span
                          className={`rounded-none px-3 py-1 text-xs font-semibold ${
                            complete
                              ? "bg-[color:var(--accent-soft)] text-[color:var(--accent-deep)]"
                              : "bg-white text-[color:var(--muted)]"
                          }`}
                        >
                          {complete ? "Rated" : "Needs rating"}
                        </span>
                      </button>
                    );
                  })}
                </div>
              </div>

              <div className="min-h-0 shrink-0 rounded-none border border-[color:var(--line)] bg-[color:var(--panel)] p-4 min-[1200px]:w-[22rem] min-[1200px]:overflow-y-auto">
                <div className="space-y-6">
                  <EvaluationDisclosure
                    defaultOpen={false}
                    summary={notesSummary(
                      notes ?? {
                        strengths: "",
                        concerns: "",
                        recommendation: "",
                      }
                    )}
                    title="Add comments"
                  >
                    <div className="space-y-3">
                      <textarea
                        className="min-h-24 w-full rounded-none border border-[color:var(--line)] bg-white px-4 py-3 text-sm text-[color:var(--ink)] outline-none transition focus:border-[color:var(--accent)]"
                        placeholder="Strengths"
                        {...form.register("notes.strengths")}
                      />
                      <textarea
                        className="min-h-24 w-full rounded-none border border-[color:var(--line)] bg-white px-4 py-3 text-sm text-[color:var(--ink)] outline-none transition focus:border-[color:var(--accent)]"
                        placeholder="Concerns"
                        {...form.register("notes.concerns")}
                      />
                      <textarea
                        className="min-h-24 w-full rounded-none border border-[color:var(--line)] bg-white px-4 py-3 text-sm text-[color:var(--ink)] outline-none transition focus:border-[color:var(--accent)]"
                        placeholder="Recommendation"
                        {...form.register("notes.recommendation")}
                      />
                    </div>
                  </EvaluationDisclosure>

                  {!canFinalize ? (
                    <div className="rounded-none border border-[color:var(--line)] bg-white px-4 py-3 text-sm text-[color:var(--muted)]">
                      Finish these sections before saving:{" "}
                      {missingSections
                        .map((section) => section.title ?? section.objective_text ?? section.section_id)
                        .join(", ")}
                    </div>
                  ) : null}

                  <div className="space-y-3 border-t border-[color:var(--line)] pt-4">
                    <p className="text-sm text-[color:var(--muted)]">{statusMessage}</p>
                    <div className="flex flex-wrap items-center justify-end gap-2">
                      {showSaveAction ? (
                        <Button disabled={!canSave} isLoading={isSaving} size="sm" type="submit">
                          {nextPacketHref ? "Save & open next revision note" : "Save rating"}
                        </Button>
                      ) : null}
                      {showNextAction ? (
                        <Button
                          disabled={!canSave}
                          isLoading={isSaving}
                          onClick={form.handleSubmit(async (values) => {
                            await saveValues(values, true);
                          })}
                          size="sm"
                          type="button"
                          variant="outline"
                        >
                          {nextActionLabel}
                        </Button>
                      ) : null}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </>
      ) : activeSection ? (
        <>
          <H2PacketHeader
            activeIndex={activeIndex}
            activeObjectiveText={activeObjectiveText}
            activeObjectiveMisconception={activeObjectiveMisconception}
            activeSectionTitle={activeSectionTitle}
            learnerSummary={getLearnerSummary(detail.focal_learner)}
            learnerTraits={learnerTraits}
            lessonSubtitle={detail.lesson_subtitle}
            lessonTitle={detail.lesson_title}
            masteredSection={masteredSection}
            objectiveCount={detail.objectives.length}
            sectionStatus={sectionCandidatesStatus(activeCandidateDrafts)}
            onOpenPacketBrief={onOpenPacketBrief}
            sectionCount={detail.sections.length}
          />

          <section className="rounded-none border border-[color:var(--line)] bg-white p-3 min-[1200px]:flex-1 min-[1200px]:min-h-0 min-[1200px]:overflow-y-auto">
            <div className="flex flex-col gap-3">
              {/* The candidate versions take the FULL width, side by side, so the
                  rater can compare them properly; the rating band sits below. */}
              <div className="flex flex-col gap-3 xl:flex-row">
                {candidates.map((candidate, index) => {
                  const step = activeSection.candidate_steps[candidate.candidate_id] ?? null;
                  return (
                    <div
                      key={candidate.candidate_id}
                      className="min-w-0 xl:h-[70vh] xl:min-h-0 xl:flex-1"
                    >
                      <WorkspacePane
                        description="One candidate version of this section for this learner."
                        headerDetail={
                          index === 0 ? (
                            <div className="rounded-none border border-[color:var(--line)] bg-white px-3 py-3">
                              <p className="text-[0.65rem] font-semibold uppercase tracking-[0.16em] text-[color:var(--muted)]">
                                Learner context in view
                              </p>
                              <p className="mt-2 text-sm font-semibold text-[color:var(--ink)]">
                                {learnerProfileText}
                              </p>
                            </div>
                          ) : undefined
                        }
                        title={candidate.label}
                      >
                        {step ? (
                          <ReviewPackStepCard step={step} tone="candidate" />
                        ) : (
                          <div className="rounded-none border border-dashed border-[color:var(--danger)] bg-[color:var(--danger-tint)] p-4">
                            <p className="text-sm font-semibold text-[color:var(--danger)]">
                              No section from this candidate
                            </p>
                            <p className="mt-1 text-sm text-[color:var(--ink)]">
                              {candidate.label} has no section for this objective. Penalise its
                              lesson-goal score accordingly.
                            </p>
                          </div>
                        )}
                      </WorkspacePane>
                    </div>
                  );
                })}
              </div>

              <RatingBand
                canGoPrevious={activeIndex > 0}
                isRevealed={Boolean(revealedSections[activeSection.section_id])}
                nextLabel={
                  activeIndex === detail.sections.length - 1
                    ? "Finalize rating"
                    : "Next section"
                }
                onNext={handleNext}
                onPrevious={() => goToStep(Math.max(0, activeIndex - 1))}
                onRateNow={() => revealSection(activeSection.section_id)}
                onSkipForNow={() =>
                  goToStep(Math.min(detail.sections.length, activeIndex + 1))
                }
                sectionStatus={sectionCandidatesStatus(activeCandidateDrafts)}
                showWarning={navigationWarningFor === activeSection.section_id}
              >
                {candidates.map((candidate) => {
                  const candidateKey = candidateFormKey(candidate.display_order);
                  return (
                    <RatingGroup
                      key={candidate.candidate_id}
                      status={sectionStatusSummary(activeDraftFor(candidateKey))}
                      subtitle={`Score ${candidate.label}'s version of this section.`}
                      title={candidate.label}
                    >
                      <H2SectionRatingStrip
                        control={form.control}
                        namePrefix={`candidate_scores.${candidateKey}.${activeSectionKey}`}
                      />
                    </RatingGroup>
                  );
                })}
              </RatingBand>
            </div>
          </section>
        </>
      ) : null}
    </form>
  );
}
