import { Link } from "@/shared/router";
import { useQuery } from "@tanstack/react-query";

import { ClassTestText } from "@/shared/components/renderer/ClassTestText";
import { Card } from "@/shared/components/ui/Card";

import { useExperiment } from "../hooks/useExperiments";
import { getDiagnosticQuestions } from "../lib/api";

/**
 * Researcher-facing READ-ONLY preview of the exit-ticket diagnostic the
 * students take. Renders the MCQ items grouped by lesson objective — same
 * data the student takes in `/research/student/exit-assessment`, but without the
 * answer-capture controls and with all options visible (no answer key —
 * the diagnostic items don't carry answers in this payload).
 */
export function AssessmentPreviewPage({ experimentId }: { experimentId: string }) {
  const experimentQuery = useExperiment(experimentId);
  const experiment = experimentQuery.data;
  const planVersionId = experiment?.plan_version_id;

  const diagnosticQuery = useQuery({
    queryKey: ["diagnostic-questions", planVersionId],
    queryFn: () => getDiagnosticQuestions(planVersionId!),
    enabled: Boolean(planVersionId),
  });

  if (experimentQuery.isLoading || diagnosticQuery.isLoading) {
    return (
      <main className="w-full py-4">
        <Card padding="lg">
          <p className="text-sm text-(--muted)">Loading exit assessment…</p>
        </Card>
      </main>
    );
  }

  if (!experiment || !planVersionId) {
    return (
      <main className="w-full py-4">
        <Card padding="lg">
          <p className="text-sm text-(--muted)">No experiment or lesson plan to preview.</p>
        </Card>
      </main>
    );
  }

  if (diagnosticQuery.isError || !diagnosticQuery.data) {
    return (
      <main className="w-full py-4">
        <Card padding="lg" className="space-y-2">
          <h1 className="text-xl font-semibold text-(--ink)">
            No exit assessment for this plan yet
          </h1>
          <p className="text-sm text-(--muted)">
            The diagnostic items are derived once the lesson plan is approved.
          </p>
          <Link
            className="text-sm font-semibold text-(--accent-deep) hover:underline"
            href={`/research/experiments/${experimentId}`}
          >
            Back to Overview
          </Link>
        </Card>
      </main>
    );
  }

  const diagnostic = diagnosticQuery.data;
  return (
    <main className="flex w-full flex-col gap-3 py-2">
      <div className="flex flex-wrap items-baseline justify-between gap-3 border-b border-(--line) pb-2">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-(--muted)">
            Exit assessment · read only
          </p>
          <p className="text-sm text-(--muted)">
            The MCQ items students take after the lesson. View only — answers are intentionally
            not shown (no answer key in this payload); the per-student responses live in the
            workflow row above.
          </p>
        </div>
        {diagnostic.subject || diagnostic.topic ? (
          <p className="text-xs text-(--muted)">
            {[diagnostic.subject, diagnostic.topic, diagnostic.subtopic].filter(Boolean).join(" · ")}
          </p>
        ) : null}
      </div>

      {diagnostic.objectives.length === 0 ? (
        <Card padding="lg">
          <p className="text-sm text-(--muted)">No items yet.</p>
        </Card>
      ) : (
        <div className="space-y-3">
          {diagnostic.objectives.map((objective, objectiveIndex) => (
            <Card key={objective.lesson_objective_id} padding="lg" className="space-y-3">
              <header className="space-y-1">
                <p className="text-xs font-semibold uppercase tracking-[0.16em] text-(--muted)">
                  Objective {objectiveIndex + 1}
                </p>
                <p className="text-sm font-semibold text-(--ink)">
                  {objective.objective_text ?? objective.lesson_objective_id}
                </p>
              </header>
              <ol className="space-y-3">
                {objective.items.map((item, itemIndex) => (
                  <li key={item.item_id} className="border-l-2 border-(--line) pl-3">
                    <div className="flex items-baseline gap-2 text-sm text-(--ink)">
                      <span className="font-mono text-xs text-(--muted)">
                        Q{itemIndex + 1}
                      </span>
                      <ClassTestText text={item.stem} />
                    </div>
                    <ul className="mt-2 space-y-1 text-sm text-(--muted)">
                      {Object.entries(item.options).map(([key, value]) => (
                        <li key={key} className="flex gap-2">
                          <span className="font-semibold text-(--ink)">{key}.</span>
                          <ClassTestText text={value} />
                        </li>
                      ))}
                    </ul>
                    {item.difficulty ? (
                      <p className="mt-1 text-xs text-(--muted)">
                        Difficulty: {item.difficulty}
                      </p>
                    ) : null}
                  </li>
                ))}
              </ol>
            </Card>
          ))}
        </div>
      )}
    </main>
  );
}
