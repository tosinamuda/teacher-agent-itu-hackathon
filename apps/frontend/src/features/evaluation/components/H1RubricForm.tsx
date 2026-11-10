import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "@/shared/router";
import { useState } from "react";
import { Controller, useForm, useWatch } from "react-hook-form";
import { z } from "zod";

import { Button } from "@/shared/components/ui/Button";

import { CompactScoreField } from "./CompactScoreField";
import { EvaluationDisclosure } from "./EvaluationDisclosure";
import { MajorIssueFlagField } from "./MajorIssueFlagField";
import { EvaluationNoteFields, H1PacketDetail } from "../types";

const H1_SCORE_OPTIONS = [
  { value: 1, label: "1 Poor" },
  { value: 2, label: "2 Weak" },
  { value: 3, label: "3 Adequate" },
  { value: 4, label: "4 Strong" },
  { value: 5, label: "5 Excellent" },
];

const schema = z.object({
  rubric_scores: z.record(z.string(), z.number().int().min(1).max(5).optional()),
  notes: z.object({
    strengths: z.string().optional(),
    concerns: z.string().optional(),
    recommendation: z.string().optional(),
    major_issues: z.array(z.string()).optional(),
    major_issue_other: z.string().optional(),
  }),
});

type FormValues = z.infer<typeof schema>;

type H1RubricFormProps = {
  detail: H1PacketDetail;
  isSaving: boolean;
  nextPacketHref?: string;
  onSubmit: (payload: {
    rubric_scores: Record<string, number>;
    notes?: EvaluationNoteFields | null;
  }) => Promise<void>;
};

const noteSummary = (notes: FormValues["notes"]) => {
  const count = [notes.strengths, notes.concerns, notes.recommendation].filter(
    (value) => value && value.trim()
  ).length;
  if (count === 0) {
    return "Optional rater comments";
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

const isValidH1Score = (value: unknown): value is number =>
  typeof value === "number" && Number.isInteger(value) && value >= 1 && value <= 5;

/**
 * Saves thesis H1 packet scores using the fixed four-dimension rubric.
 *
 * Rendered in the workspace rating sidebar as a fill-height flex column: the
 * fields scroll while the save footer stays pinned below them.
 *
 * Lock-per-candidate: once submitted, an H1 score is LOCKED (the server rejects
 * re-saves) so each anonymous candidate in a lesson block is rated independently
 * rather than revised against its siblings.
 */
export function H1RubricForm({
  detail,
  isSaving,
  nextPacketHref,
  onSubmit,
}: H1RubricFormProps) {
  const router = useRouter();
  const isLocked = Boolean(detail.existing_rating);
  const [lastSavedAt, setLastSavedAt] = useState<string | null>(
    detail.existing_rating?.submitted_at ?? detail.existing_rating?.updated_at ?? null
  );
  const [hasSavedRating, setHasSavedRating] = useState(Boolean(detail.existing_rating));

  const form = useForm<FormValues>({
    resolver: zodResolver(schema),
    mode: "onChange",
    defaultValues: {
      rubric_scores: Object.fromEntries(
        detail.rubric.map((criterion) => [
          criterion.criterion_id,
          detail.existing_rating?.rubric_scores?.[criterion.criterion_id] ?? undefined,
        ])
      ),
      notes: {
        strengths: String(detail.existing_rating?.notes?.strengths ?? ""),
        concerns: String(detail.existing_rating?.notes?.concerns ?? ""),
        recommendation: String(detail.existing_rating?.notes?.recommendation ?? ""),
        major_issues: Array.isArray(detail.existing_rating?.notes?.major_issues)
          ? (detail.existing_rating?.notes?.major_issues as string[])
          : [],
        major_issue_other: String(detail.existing_rating?.notes?.major_issue_other ?? ""),
      },
    },
  });

  const notes = useWatch({
    control: form.control,
    name: "notes",
  });
  const rubricScores = useWatch({
    control: form.control,
    name: "rubric_scores",
  });
  const canSave = detail.rubric.every((criterion) =>
    isValidH1Score(rubricScores?.[criterion.criterion_id])
  );
  const hasUnsavedChanges = form.formState.isDirty;
  const showSaveAction = !hasSavedRating || hasUnsavedChanges;
  const showNextAction = Boolean(nextPacketHref && hasSavedRating && !hasUnsavedChanges);
  const nextActionLabel = hasUnsavedChanges ? "Save and open next revision note" : "Open next revision note";
  const statusMessage = !canSave
    ? "Select a score for each criterion before saving"
    : showNextAction && !showSaveAction
    ? "This rating is saved. Open the next revision note when you are ready."
    : hasUnsavedChanges
    ? "Unsaved changes"
    : formatSavedLabel(lastSavedAt);

  const saveValues = async (values: FormValues, navigateToNext: boolean) => {
    const rubricScoresPayload = Object.fromEntries(
      detail.rubric.map((criterion) => [
        criterion.criterion_id,
        values.rubric_scores[criterion.criterion_id] as number,
      ])
    );

    const majorIssues = values.notes.major_issues ?? [];
    const notesPayload: EvaluationNoteFields = {
      ...values.notes,
      major_issues: majorIssues,
      major_issue_other: majorIssues.includes("other")
        ? values.notes.major_issue_other
        : undefined,
    };

    await onSubmit({
      rubric_scores: rubricScoresPayload,
      notes: notesPayload,
    });
    const savedAt = new Date().toISOString();
    setLastSavedAt(savedAt);
    setHasSavedRating(true);
    form.reset(values);
    if (navigateToNext && nextPacketHref) {
      router.push(nextPacketHref);
    }
  };

  if (isLocked) {
    return (
      <section className="min-h-0 flex-1 space-y-3 p-4 min-[1200px]:overflow-y-auto">
        <div className="rounded-none border border-[color:var(--line)] bg-[color:var(--accent-soft)] px-4 py-3">
          <p className="text-sm font-semibold text-[color:var(--accent-deep)]">
            Score locked ✓
          </p>
          <p className="mt-1 text-sm leading-6 text-[color:var(--ink)]">
            You have scored this candidate. Scores lock on submission so each
            candidate is rated independently — continue to the next one.
          </p>
        </div>
        <dl className="space-y-2">
          {detail.rubric.map((criterion) => (
            <div
              key={criterion.criterion_id}
              className="flex items-center justify-between gap-3 rounded-none border border-[color:var(--line)] bg-white px-3 py-2"
            >
              <dt className="text-sm text-[color:var(--ink)]">
                {criterion.display_label || criterion.label}
              </dt>
              <dd className="text-sm font-semibold text-[color:var(--accent-deep)]">
                {detail.existing_rating?.rubric_scores?.[criterion.criterion_id] ?? "—"} / 5
              </dd>
            </div>
          ))}
        </dl>
        {nextPacketHref ? (
          <Button onClick={() => router.push(nextPacketHref)} size="sm" type="button">
            Open next revision note
          </Button>
        ) : null}
      </section>
    );
  }

  return (
    <form
      className="flex min-h-0 flex-1 flex-col"
      onSubmit={form.handleSubmit(async (values) => {
        await saveValues(values, true);
      })}
    >
      {/* The fields scroll INSIDE this wrapper while the save footer stays a
          sibling below it — the footer must never overlay the score buttons,
          or clicks on half-covered buttons land on the footer. */}
      <div className="min-h-0 flex-1 space-y-4 p-4 min-[1200px]:overflow-y-auto">
        {detail.rating_guidance?.length ? (
          <div className="space-y-2 border-l-2 border-[color:var(--line)] bg-[color:var(--panel)] px-3 py-2">
            {detail.rating_guidance.map((note) => (
              <p key={note} className="text-sm leading-6 text-[color:var(--muted)]">
                {note}
              </p>
            ))}
          </div>
        ) : null}
        <div className="space-y-3">
          {detail.rubric.map((criterion) => (
            <Controller
              key={criterion.criterion_id}
              control={form.control}
              name={`rubric_scores.${criterion.criterion_id}` as const}
              render={({ field }) => (
                <CompactScoreField
                  label={criterion.display_label || criterion.label}
                  onChange={(nextValue) => field.onChange(nextValue as number)}
                  options={H1_SCORE_OPTIONS}
                  value={field.value}
                />
              )}
            />
          ))}
        </div>

        <Controller
          control={form.control}
          name="notes.major_issues"
          render={({ field }) => {
            const selected = field.value ?? [];
            return (
              <MajorIssueFlagField
                flags={detail.major_issue_flags}
                onToggle={(key) =>
                  field.onChange(
                    selected.includes(key)
                      ? selected.filter((value) => value !== key)
                      : [...selected, key]
                  )
                }
                otherProps={form.register("notes.major_issue_other")}
                selected={selected}
                showOther={selected.includes("other")}
              />
            );
          }}
        />

        <EvaluationDisclosure
          defaultOpen={false}
          summary={noteSummary(notes)}
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
      </div>

      <div className="shrink-0 border-t border-[color:var(--line)] bg-(--surface) px-4 pb-3 pt-3">
        <div className="space-y-3">
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
    </form>
  );
}
