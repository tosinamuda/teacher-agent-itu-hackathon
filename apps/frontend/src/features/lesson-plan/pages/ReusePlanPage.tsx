import { useState } from "react";

import { Button } from "@/shared/components/ui/Button";
import { Link, useRouter } from "@/shared/router";

import type { PlanSource } from "../api/reusePlan";
import { CurriculumChoices } from "../components/CurriculumChoices";
import { PlanSourcePicker } from "../components/PlanSourcePicker";
import { useReuseExperimentPlan } from "../hooks/useReuseExperimentPlan";

const errorMessage = (error: unknown): string =>
  error instanceof Error ? error.message : "Something went wrong.";

/**
 * Reuse a plan that already exists as this lesson's plan: an approved plan of another lesson,
 * or a plan file. The plan keeps its content and is saved as a draft to read through and accept.
 */
export function ReusePlanPage({ experimentId }: { experimentId: string }) {
  const router = useRouter();
  const reuse = useReuseExperimentPlan(experimentId);
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
          if (result.status === "reused") {
            router.push(
              `/research/teacher/experiment-plans/${experimentId}/plan`,
            );
          }
        },
      },
    );
  };

  return (
    <main className="mx-auto flex w-full max-w-2xl flex-col gap-6 py-8">
      <Link
        href={`/research/teacher/experiment-plans/${experimentId}`}
        className="text-sm text-(--accent-deep) hover:underline"
      >
        ← Back to the lesson
      </Link>
      <header className="space-y-1">
        <h1 className="text-2xl font-semibold text-(--ink)">
          Reuse an existing plan
        </h1>
        <p className="text-sm text-(--ink-2)">
          Choose a plan that already exists. It keeps its steps and its
          objectives&apos; wording, and you read it through and accept it as
          with any plan.
        </p>
      </header>
      <PlanSourcePicker
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
          Reuse this plan
        </Button>
      </div>
    </main>
  );
}
