import { useMemo, useState } from "react";

import { Link } from "@/shared/router";

import { Card } from "@/shared/components/ui/Card";

import type { OnBehalfRequest } from "../api/onBehalf";
import type { WorkedQuestion } from "../lib/markedWork";
import { ResponseEntryForm } from "../components/ResponseEntryForm";
import {
  useClassRoster,
  useEnterOnBehalfResponses,
  useExperimentClass,
  useOnBehalfContext,
} from "../hooks/useOnBehalf";

const labelClass = "text-[11px] font-semibold uppercase tracking-[0.14em] text-(--muted)";
const fieldClass =
  "w-full border border-(--line-2) bg-(--surface) px-3 py-2 text-sm text-(--ink) outline-none focus:border-(--accent)";

/**
 * Record students' classwork results on their behalf (FD-04): a researcher/teacher
 * picks a student, enters what they answered (per question or as scores), optionally
 * attaches their marked sheet, and saves — the system grades + derives learner state.
 */
export default function OnBehalfEntryPage({
  experimentId,
  planVersionId,
}: {
  experimentId: string;
  planVersionId: string;
}) {
  const context = useOnBehalfContext(planVersionId);
  const experimentClass = useExperimentClass(experimentId);
  const roster = useClassRoster(experimentClass.data?.class_id);
  const enter = useEnterOnBehalfResponses();

  const [submittedLocal, setSubmittedLocal] = useState<Set<string>>(new Set());
  const [selectedStudentId, setSelectedStudentId] = useState("");
  const [savedFor, setSavedFor] = useState<string | null>(null);
  const [questions, setQuestions] = useState<WorkedQuestion[]>([]);

  const submitted = useMemo(
    () => new Set([...(context.data?.submitted_student_ids ?? []), ...submittedLocal]),
    [context.data, submittedLocal]
  );
  const learners = roster.data?.data ?? [];
  const available = learners.filter((learner) => !submitted.has(learner.student_id));
  const selected = learners.find((learner) => learner.student_id === selectedStudentId);

  const submit = (payload: Omit<OnBehalfRequest, "student_id">) => {
    if (!selectedStudentId) return;
    const studentName = selected?.full_name ?? selectedStudentId;
    enter.mutate(
      { planVersionId, request: { ...payload, student_id: selectedStudentId } },
      {
        onSuccess: () => {
          setSubmittedLocal((current) => new Set(current).add(selectedStudentId));
          setSavedFor(studentName);
          setSelectedStudentId("");
        },
      }
    );
  };

  const loading = context.isLoading || experimentClass.isLoading || roster.isLoading;

  return (
    <main className="mx-auto flex w-full max-w-3xl flex-col gap-6 py-8">
      <header className="space-y-1">
        <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--accent-deep)">
          Classwork results
        </p>
        <h1 className="text-2xl font-semibold text-(--ink)">Record results on behalf of students</h1>
        <p className="text-sm text-(--muted)">
          Enter what each student answered on the classwork. Their scores drive each
          student&apos;s personalised revision note — no student login needed.
        </p>
      </header>

      {loading ? (
        <Card padding="lg">
          <p className="text-sm text-(--muted)">Loading the class…</p>
        </Card>
      ) : context.isError || !context.data ? (
        <Card padding="lg">
          <p className="text-sm text-(--danger-ink)">Could not load this lesson&apos;s classwork.</p>
        </Card>
      ) : (
        <>
          {savedFor ? (
            <Card padding="md" className="border border-(--accent)/40 bg-(--accent-soft)/40">
              <p className="text-sm text-(--accent-deep)">Saved {savedFor}&apos;s responses.</p>
            </Card>
          ) : null}

          <Card variant="glass" padding="lg" className="space-y-3">
            <label className="block space-y-1">
              <span className={labelClass}>Student</span>
              <select
                className={fieldClass}
                value={selectedStudentId}
                onChange={(event) => setSelectedStudentId(event.target.value)}
              >
                <option value="">— pick a student to record —</option>
                {available.map((learner) => (
                  <option key={learner.student_id} value={learner.student_id}>
                    {learner.full_name}
                  </option>
                ))}
              </select>
            </label>
            <p className="text-xs text-(--muted)">
              {available.length} of {learners.length} student{learners.length === 1 ? "" : "s"} left
              to record.
              {context.data.items.length === 0
                ? " No classwork items entered yet — you can still record per-objective scores."
                : ""}
            </p>
          </Card>

          {selected ? (
            <Card variant="glass" padding="lg">
              <ResponseEntryForm
                key={selected.student_id}
                studentName={selected.full_name}
                items={context.data.items}
                objectives={context.data.objectives}
                questions={questions}
                onQuestionsChange={setQuestions}
                busy={enter.isPending}
                onSubmit={submit}
              />
              {enter.isError ? (
                <p className="mt-3 text-sm text-(--danger-ink)">
                  {(enter.error as Error).message || "Could not save — please try again."}
                </p>
              ) : null}
            </Card>
          ) : available.length === 0 && learners.length > 0 ? (
            <Card padding="lg">
              <p className="text-sm text-(--ink)">All students recorded. </p>
              <Link
                href={`/research/teacher/experiment-plans/${experimentId}`}
                className="text-sm font-semibold text-(--accent-deep) hover:underline"
              >
                ← Back to lesson preparation
              </Link>
            </Card>
          ) : null}
        </>
      )}
    </main>
  );
}
