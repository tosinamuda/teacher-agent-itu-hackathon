import { useMemo, useState } from "react";

import { useRouter } from "@/shared/router";

import { planPath } from "../lib/planPaths";

import { AttachmentField } from "@/shared/components/ui/AttachmentField";
import { Button } from "@/shared/components/ui/Button";
import { Card } from "@/shared/components/ui/Card";
import { RichContentEditor } from "@/shared/components/ui/RichContentEditor";

import { ImportFromDocument } from "../components/ImportFromDocument";
import { ManualObjectiveCard } from "../components/ManualObjectiveCard";
import { StringListField } from "../components/StringListField";
import {
  useApprovePlan,
  useCreateExperimentManualPlan,
  useCreateManualPlan,
  useManualPlanContext,
} from "../hooks/useManualPlanEntry";
import {
  buildManualSessionPlanContent,
  emptyManualPlanDraft,
  emptyObjectiveDraft,
  manualDraftIssues,
  type ManualPlanDraft,
} from "../manualDraft";

const fieldClass =
  "w-full border border-(--line-2) bg-(--surface) px-3 py-2 text-sm text-(--ink) outline-none focus:border-(--accent)";
const labelClass =
  "text-[11px] font-semibold uppercase tracking-[0.14em] text-(--muted)";

/**
 * Manual lesson-plan entry (FD-01): a teacher or researcher transcribes a
 * teacher-authored plan, maps each objective to a curriculum objective, then
 * creates a draft and freezes it (without auto-generating a diagnostic — the
 * teacher brings their own classwork). The lesson is fixed by the URL/experiment,
 * so its identity is shown read-only, never edited by hand.
 */
export default function ManualPlanEntryPage({
  initialSessionId = "",
  experimentId,
}: {
  initialSessionId?: string;
  experimentId?: string;
}) {
  const router = useRouter();
  const sessionId = initialSessionId;
  const [draft, setDraft] = useState<ManualPlanDraft>(emptyManualPlanDraft);
  const [createdVersionId, setCreatedVersionId] = useState<string | null>(null);
  const [originalDocId, setOriginalDocId] = useState<string | null>(null);

  const context = useManualPlanContext(sessionId);
  const createPlan = useCreateManualPlan();
  const createExperimentPlan = useCreateExperimentManualPlan();
  const approvePlan = useApprovePlan();

  const curriculumOptions = useMemo(
    () => context.data?.curriculum_objectives ?? [],
    [context.data],
  );
  const curriculumById = useMemo(
    () =>
      new Map(
        curriculumOptions.map((option) => [
          option.curriculum_objective_id,
          option,
        ]),
      ),
    [curriculumOptions],
  );
  const issues = manualDraftIssues(draft);
  const patch = (next: Partial<ManualPlanDraft>) =>
    setDraft((current) => ({ ...current, ...next }));

  const creating = experimentId
    ? createExperimentPlan.isPending
    : createPlan.isPending;
  const createError = experimentId
    ? createExperimentPlan.isError
      ? (createExperimentPlan.error as Error).message
      : null
    : createPlan.isError
      ? (createPlan.error as Error).message
      : null;

  const submit = () => {
    setCreatedVersionId(null);
    const sessionPlan = buildManualSessionPlanContent(draft, curriculumById);
    if (experimentId) {
      createExperimentPlan.mutate(
        {
          experimentId,
          sessionPlan,
          originalDocumentAttachmentId: originalDocId,
        },
        {
          onSuccess: () =>
            router.push(`/research/teacher/experiment-plans/${experimentId}`),
        },
      );
      return;
    }
    createPlan.mutate(
      { sessionId, sessionPlan },
      { onSuccess: (result) => router.push(planPath(result.version_id)) },
    );
  };

  return (
    <main className="mx-auto flex w-full max-w-3xl flex-col gap-6 py-8">
      <header className="space-y-1">
        <h1 className="text-2xl font-semibold text-(--ink)">
          {experimentId
            ? "Enter a teacher-authored plan"
            : "Write the plan by hand"}
        </h1>
        <p className="text-xs text-(--muted)">
          The lesson and its curriculum objective are fixed.
        </p>
      </header>

      {context.isLoading ? (
        <Card padding="lg">
          <p className="text-sm text-(--muted)">Loading lesson…</p>
        </Card>
      ) : context.isError || !context.data ? (
        <Card padding="lg">
          <p className="text-sm text-(--danger-ink)">
            Could not load that lesson.
          </p>
        </Card>
      ) : (
        <>
          {experimentId ? (
            <>
              <Card variant="glass" padding="lg" className="space-y-1">
                <p className={labelClass}>Lesson</p>
                <h2 className="text-lg font-semibold text-(--ink)">
                  {context.data.subtopic}
                </h2>
                <p className="text-sm text-(--muted)">
                  {[
                    context.data.subject,
                    context.data.grade,
                    context.data.term,
                    `Week ${context.data.week}`,
                  ]
                    .filter(Boolean)
                    .join(" · ")}
                </p>
                <p className="text-sm text-(--ink-2)">
                  Topic: {context.data.topic}
                </p>
                <p className="text-xs text-(--muted)">
                  {context.data.curriculum_objectives.length} curriculum
                  objective
                  {context.data.curriculum_objectives.length === 1
                    ? ""
                    : "s"}{" "}
                  to map your objectives to.
                </p>
              </Card>

              <ImportFromDocument
                sessionId={context.data.session_id}
                experimentId={experimentId}
                onImported={(plan) =>
                  experimentId
                    ? router.push(
                        `/research/teacher/experiment-plans/${experimentId}`,
                      )
                    : setCreatedVersionId(plan.plan_version_id)
                }
              />
            </>
          ) : null}

          {experimentId ? (
            <Card variant="glass" padding="lg" className="space-y-2">
              <AttachmentField
                value={originalDocId}
                kind="lesson_plan_document"
                label="Photo of the teacher's original plan (optional)"
                onChange={setOriginalDocId}
              />
            </Card>
          ) : null}

          <Card variant="glass" padding="lg" className="space-y-3">
            <p className={labelClass}>Introduction</p>
            <input
              className={fieldClass}
              value={draft.intro.title}
              placeholder="Intro title"
              onChange={(event) =>
                patch({ intro: { ...draft.intro, title: event.target.value } })
              }
            />
            <RichContentEditor
              value={draft.intro.content}
              onChange={(text) =>
                patch({ intro: { ...draft.intro, content: text } })
              }
              rows={2}
              placeholder="How the lesson opens / prior knowledge activated"
            />
          </Card>

          <Card variant="glass" padding="lg" className="space-y-4">
            <div className="flex items-center justify-between">
              <p className={labelClass}>Objectives</p>
              <Button
                variant="secondary"
                onClick={() =>
                  patch({
                    objectives: [...draft.objectives, emptyObjectiveDraft()],
                  })
                }
              >
                + Add objective
              </Button>
            </div>
            {draft.objectives.map((objective, index) => (
              <ManualObjectiveCard
                key={index}
                objective={objective}
                index={index}
                curriculumOptions={curriculumOptions}
                onChange={(next) =>
                  patch({
                    objectives: draft.objectives.map((current, i) =>
                      i === index ? next : current,
                    ),
                  })
                }
                onRemove={() =>
                  patch({
                    objectives: draft.objectives.filter((_, i) => i !== index),
                  })
                }
              />
            ))}
          </Card>

          <Card variant="glass" padding="lg" className="space-y-2">
            <span className={labelClass}>Evaluation summary</span>
            <textarea
              rows={2}
              className={fieldClass}
              value={draft.evaluationSummary}
              onChange={(event) =>
                patch({ evaluationSummary: event.target.value })
              }
            />
          </Card>

          <Card variant="glass" padding="lg" className="space-y-5">
            <div className="space-y-1">
              <StringListField
                label="Common misconceptions to address while teaching"
                items={draft.misconceptions}
                onChange={(items) => patch({ misconceptions: items })}
              />
            </div>
            <StringListField
              label="Instructional materials"
              items={draft.instructionalMaterials}
              onChange={(items) => patch({ instructionalMaterials: items })}
            />
            <StringListField
              label="Entry behaviour"
              items={draft.entryBehaviour}
              onChange={(items) => patch({ entryBehaviour: items })}
            />
            <StringListField
              label="References"
              items={draft.references}
              onChange={(items) => patch({ references: items })}
            />
          </Card>

          {experimentId && issues.length > 0 ? (
            <Card
              padding="md"
              className="border border-(--warning-ink)/30 bg-(--warning-tint)/30"
            >
              <p className="mb-2 text-[11px] font-semibold uppercase tracking-[0.14em] text-(--warning-ink)">
                Before you can create the plan
              </p>
              <ul className="list-disc space-y-1 pl-5 text-sm text-(--ink-2)">
                {issues.map((issue) => (
                  <li key={issue}>{issue}</li>
                ))}
              </ul>
            </Card>
          ) : null}

          {createError ? (
            <p className="text-sm text-(--danger-ink)">
              {createError || "Could not create the plan."}
            </p>
          ) : null}

          {experimentId && createdVersionId ? (
            <ConfirmFreeze
              versionId={createdVersionId}
              isFreezing={approvePlan.isPending}
              isFrozen={approvePlan.isSuccess}
              error={
                approvePlan.isError
                  ? (approvePlan.error as Error).message
                  : null
              }
              onFreeze={() =>
                approvePlan.mutate({ versionId: createdVersionId })
              }
            />
          ) : (
            <div className="sticky bottom-0 -mx-1 flex items-center gap-3 border border-(--line-2) bg-(--surface) px-4 py-3">
              <p className="flex-1 text-sm text-(--ink)">
                {issues.length > 0 ? (
                  <>
                    <span className="font-semibold">
                      {issues.length} left to fill
                    </span>
                    <span className="sr-only">: {issues.join(". ")}</span>
                  </>
                ) : (
                  "Ready to create"
                )}
              </p>
              <Button
                isLoading={creating}
                disabled={issues.length > 0}
                onClick={submit}
              >
                {experimentId
                  ? "Create plan & continue to freeze"
                  : "Create draft plan"}
              </Button>
            </div>
          )}
        </>
      )}
    </main>
  );
}

function ConfirmFreeze({
  versionId,
  isFreezing,
  isFrozen,
  error,
  onFreeze,
}: {
  versionId: string;
  isFreezing: boolean;
  isFrozen: boolean;
  error: string | null;
  onFreeze: () => void;
}) {
  return (
    <Card variant="glass" padding="lg" className="space-y-2">
      <p className="text-sm text-(--ink)">
        Draft created (version <span className="font-mono">{versionId}</span>).
      </p>
      {isFrozen ? (
        <p className="text-sm text-(--accent-deep)">
          Plan confirmed and frozen. No diagnostic was generated — add the
          teacher&apos;s classwork next.
        </p>
      ) : (
        <Button isLoading={isFreezing} onClick={onFreeze}>
          Confirm &amp; freeze (no diagnostic)
        </Button>
      )}
      {error ? <p className="text-sm text-(--danger-ink)">{error}</p> : null}
    </Card>
  );
}
