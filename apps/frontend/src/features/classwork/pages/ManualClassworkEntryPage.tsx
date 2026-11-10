import { useEffect, useMemo, useState } from "react";

import { Link } from "@/shared/router";

import { Button } from "@/shared/components/ui/Button";
import { Card } from "@/shared/components/ui/Card";

import type { ClassworkCoverage } from "../api/manualClasswork";
import { ManualClassworkItemCard } from "../components/ManualClassworkItemCard";
import {
  buildManualClassworkPayload,
  draftFromExistingItems,
  emptyClassworkItem,
  manualClassworkIssues,
  type ClassworkDraft,
} from "../manualClassworkDraft";
import {
  useClassworkContext,
  useCreateExperimentManualClasswork,
  useDeriveMisconceptions,
} from "../hooks/useManualClasswork";

const labelClass = "text-[11px] font-semibold uppercase tracking-[0.14em] text-(--muted)";

/**
 * Manual classwork entry (FD-02): the teacher transcribes the lesson's real
 * classwork as MCQ items tagged to the frozen plan's objectives. Items persist as
 * exit-ticket items the scoring pipeline reads directly; a coverage report flags
 * objectives with no items. Edit-in-place — the form loads any items already saved.
 */
export default function ManualClassworkEntryPage({
  experimentId,
  planVersionId,
}: {
  experimentId: string;
  planVersionId: string;
}) {
  const context = useClassworkContext(planVersionId);
  const createClasswork = useCreateExperimentManualClasswork();
  const derive = useDeriveMisconceptions();
  const [draft, setDraft] = useState<ClassworkDraft>(() => ({ items: [emptyClassworkItem()] }));
  const [seeded, setSeeded] = useState(false);
  const [coverage, setCoverage] = useState<ClassworkCoverage | null>(null);

  useEffect(() => {
    if (context.data && !seeded) {
      setDraft(draftFromExistingItems(context.data.items));
      setSeeded(true);
    }
  }, [context.data, seeded]);

  const objectives = useMemo(() => context.data?.objectives ?? [], [context.data]);
  const objectiveIds = useMemo(
    () => new Set(objectives.map((objective) => objective.lesson_objective_id)),
    [objectives]
  );
  const issues = manualClassworkIssues(draft, objectiveIds);
  const released = context.data?.released ?? false;
  const objectiveText = useMemo(
    () => new Map(objectives.map((objective) => [objective.lesson_objective_id, objective.objective_text])),
    [objectives]
  );

  const patchItem = (index: number, next: (typeof draft.items)[number]) =>
    setDraft((current) => ({
      items: current.items.map((item, i) => (i === index ? next : item)),
    }));

  const submit = () => {
    setCoverage(null);
    createClasswork.mutate(
      { experimentId, items: buildManualClassworkPayload(draft).items },
      { onSuccess: setCoverage }
    );
  };

  // FD-03: items complete enough to derive distractor misconceptions for.
  const derivable = draft.items
    .map((item, index) => ({ item, index }))
    .filter(
      ({ item }) =>
        item.stem.trim() &&
        item.correctOption &&
        item.options.filter((option) => option.text.trim()).length >= 2
    );

  const suggestMisconceptions = () => {
    const items = derivable.map(({ item }) => ({
      stem: item.stem,
      options: Object.fromEntries(
        item.options.filter((option) => option.text.trim()).map((option) => [option.key, option.text])
      ),
      correct_option: item.correctOption,
      lesson_objective_id: item.lessonObjectiveId || null,
    }));
    derive.mutate(
      { planVersionId, items },
      {
        onSuccess: (response) =>
          setDraft((current) => {
            const next = [...current.items];
            derivable.forEach(({ index }, sentIndex) => {
              const suggested = response.items[sentIndex]?.option_misconceptions ?? {};
              next[index] = {
                ...next[index],
                distractorMisconceptions: { ...next[index].distractorMisconceptions, ...suggested },
              };
            });
            return { items: next };
          }),
      }
    );
  };

  const createError = createClasswork.isError ? (createClasswork.error as Error).message : null;

  return (
    <main className="mx-auto flex w-full max-w-3xl flex-col gap-6 py-8">
      <header className="space-y-1">
        <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--accent-deep)">
          Manual classwork
        </p>
        <h1 className="text-2xl font-semibold text-(--ink)">Enter the lesson&apos;s classwork</h1>
        <p className="text-sm text-(--muted)">
          Transcribe the classwork the teacher already gave, tagged to this lesson&apos;s objectives.
          It becomes the post-class diagnostic — no separate assessment is generated.
        </p>
      </header>

      {context.isLoading ? (
        <Card padding="lg">
          <p className="text-sm text-(--muted)">Loading lesson…</p>
        </Card>
      ) : context.isError || !context.data ? (
        <Card padding="lg">
          <p className="text-sm text-(--danger-ink)">Could not load this lesson&apos;s classwork.</p>
        </Card>
      ) : released ? (
        <Card padding="lg" className="space-y-2">
          <p className={labelClass}>Locked</p>
          <p className="text-sm text-(--ink)">
            This assessment has been released to students, so its classwork is frozen and can no
            longer be edited.
          </p>
          <Link
            href={`/research/teacher/experiment-plans/${experimentId}`}
            className="text-sm font-semibold text-(--accent-deep) hover:underline"
          >
            ← Back to lesson preparation
          </Link>
        </Card>
      ) : (
        <>
          <Card variant="glass" padding="lg" className="space-y-1">
            <p className={labelClass}>Lesson</p>
            <h2 className="text-lg font-semibold text-(--ink)">
              {context.data.subtopic || context.data.topic}
            </h2>
            <p className="text-sm text-(--muted)">
              {[context.data.subject, context.data.topic].filter(Boolean).join(" · ")}
            </p>
            <p className="text-xs text-(--muted)">
              {objectives.length} objective{objectives.length === 1 ? "" : "s"} to tag your items to.
            </p>
          </Card>

          <Card variant="glass" padding="lg" className="space-y-4">
            <div className="flex items-center justify-between">
              <p className={labelClass}>Classwork items</p>
              <div className="flex items-center gap-2">
                <Button
                  variant="secondary"
                  isLoading={derive.isPending}
                  disabled={derivable.length === 0}
                  onClick={suggestMisconceptions}
                >
                  Suggest misconceptions
                </Button>
                <Button
                  variant="secondary"
                  onClick={() =>
                    setDraft((current) => ({ items: [...current.items, emptyClassworkItem()] }))
                  }
                >
                  + Add item
                </Button>
              </div>
            </div>
            {derive.isError ? (
              <p className="text-sm text-(--danger-ink)">
                Could not suggest misconceptions — please try again.
              </p>
            ) : null}
            <p className="text-xs text-(--muted)">
              &ldquo;Suggest misconceptions&rdquo; uses AI to propose a tag for each wrong option —
              review and edit them; they only save when you save the classwork.
            </p>
            {draft.items.map((item, index) => (
              <ManualClassworkItemCard
                key={index}
                item={item}
                index={index}
                objectives={objectives}
                knowledgeComponents={context.data.knowledge_components}
                onChange={(next) => patchItem(index, next)}
                onRemove={() =>
                  setDraft((current) => ({
                    items: current.items.filter((_, i) => i !== index),
                  }))
                }
              />
            ))}
          </Card>

          {issues.length > 0 ? (
            <Card padding="md" className="border border-(--warning-ink)/30 bg-(--warning-tint)/30">
              <p className="mb-2 text-[11px] font-semibold uppercase tracking-[0.14em] text-(--warning-ink)">
                Before you can save
              </p>
              <ul className="list-disc space-y-1 pl-5 text-sm text-(--ink-2)">
                {issues.map((issue) => (
                  <li key={issue}>{issue}</li>
                ))}
              </ul>
            </Card>
          ) : null}

          {createError ? (
            <p className="text-sm text-(--danger-ink)">{createError}</p>
          ) : null}

          {coverage ? (
            <CoverageReport coverage={coverage} objectiveText={objectiveText} experimentId={experimentId} />
          ) : (
            <Button
              isLoading={createClasswork.isPending}
              disabled={issues.length > 0}
              onClick={submit}
            >
              Save classwork
            </Button>
          )}
        </>
      )}
    </main>
  );
}

function CoverageReport({
  coverage,
  objectiveText,
  experimentId,
}: {
  coverage: ClassworkCoverage;
  objectiveText: Map<string, string | null | undefined>;
  experimentId: string;
}) {
  const gaps = coverage.objectives_without_items.length;
  return (
    <Card variant="glass" padding="lg" className="space-y-3">
      <p className={labelClass}>
        Saved — {coverage.total_items} item{coverage.total_items === 1 ? "" : "s"} across{" "}
        {coverage.objectives.length} objective{coverage.objectives.length === 1 ? "" : "s"}
      </p>
      <ul className="space-y-1 text-sm">
        {coverage.objectives.map((objective) => (
          <li key={objective.lesson_objective_id} className="flex items-center justify-between gap-3">
            <span className="text-(--ink-2)">
              {objectiveText.get(objective.lesson_objective_id) ?? objective.lesson_objective_id}
            </span>
            {objective.has_items ? (
              <span className="text-(--muted)">
                {objective.item_count} item{objective.item_count === 1 ? "" : "s"}
              </span>
            ) : (
              <span className="font-semibold text-(--warning-ink)">no items — no diagnostic signal</span>
            )}
          </li>
        ))}
      </ul>
      {gaps > 0 ? (
        <p className="text-xs text-(--warning-ink)">
          {gaps} objective{gaps === 1 ? "" : "s"} have no classwork — those objectives won&apos;t be
          diagnosed. Add items, or continue if that&apos;s intended.
        </p>
      ) : null}
      <Link
        href={`/research/teacher/experiment-plans/${experimentId}`}
        className="text-sm font-semibold text-(--accent-deep) hover:underline"
      >
        ← Back to lesson preparation
      </Link>
    </Card>
  );
}
