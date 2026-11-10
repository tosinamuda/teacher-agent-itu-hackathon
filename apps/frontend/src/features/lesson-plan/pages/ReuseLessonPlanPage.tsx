import { useState } from "react";

import { Button } from "@/shared/components/ui/Button";
import { Link, useRouter } from "@/shared/router";

import type { PlanSource } from "../api/reusePlan";
import { CurriculumChoices } from "../components/CurriculumChoices";
import { PlanSourcePicker } from "../components/PlanSourcePicker";
import { ThisLesson } from "../components/ThisLesson";
import { useReuseLessonPlan } from "../hooks/useReuseLessonPlan";

const errorMessage = (error: unknown): string =>
  error instanceof Error ? error.message : "Something went wrong.";

/**
 * Use a plan that already exists as this lesson's plan: an approved plan of another lesson, or a
 * plan file. It keeps its steps and is saved as a draft to read through and accept.
 */
export function ReuseLessonPlanPage({
  lessonPeriodId,
}: {
  lessonPeriodId: string;
}) {
  const router = useRouter();
  const reuse = useReuseLessonPlan(lessonPeriodId);
  const [source, setSource] = useState<PlanSource | null>(null);
  const [chosen, setChosen] = useState<Record<string, string>>({});
  const needsChoice =
    reuse.data?.status === "needs_curriculum_choice" ? reuse.data : null;
  const ready =
    source !== null &&
    (needsChoice === null ||
      needsChoice.unmapped.every(
        (objective) => chosen[objective.lesson_objective_id],
      ));

  const submit = () => {
    if (!source) return;
    reuse.mutate(
      { source, choices: chosen },
      {
        onSuccess: (result) => {
          if (result.status === "reused")
            router.push(`/research/teacher/lesson-plan/${result.plan.plan_id}`);
        },
      },
    );
  };

  return (
    <main className="mx-auto flex w-full max-w-2xl flex-col gap-6 py-6">
      <Link
        href={`/research/teacher/lessons/${lessonPeriodId}`}
        className="text-sm text-(--ink-2) hover:text-(--ink)"
      >
        ‹ Back to the lesson
      </Link>
      <header className="flex flex-col gap-1">
        <h1 className="text-2xl font-semibold text-(--ink)">
          Use an existing plan
        </h1>
        <p className="text-sm text-(--ink-2)">
          Choose a plan that already exists. It keeps its steps and the wording
          of its objectives. You read it through and accept it as you would any
          plan.
        </p>
      </header>
      <ThisLesson lessonPeriodId={lessonPeriodId} />
      <PlanSourcePicker
        exceptLessonId={lessonPeriodId}
        onChange={(next) => {
          setSource(next);
          setChosen({});
          reuse.reset();
        }}
      />
      {needsChoice ? (
        <CurriculumChoices
          unmapped={needsChoice.unmapped}
          choices={needsChoice.choices}
          chosen={chosen}
          onChoose={(objective, curriculum) =>
            setChosen((now) => ({ ...now, [objective]: curriculum }))
          }
        />
      ) : null}
      {reuse.isError ? (
        <p role="alert" className="text-sm text-(--danger-ink)">
          {errorMessage(reuse.error)}
        </p>
      ) : null}
      <div>
        <Button isLoading={reuse.isPending} disabled={!ready} onClick={submit}>
          Use this plan
        </Button>
      </div>
    </main>
  );
}
