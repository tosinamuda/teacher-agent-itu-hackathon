import { Link } from "@/shared/router";
import { useEffect, useMemo, useState } from "react";

import { Card } from "@/shared/components/ui/Card";

import { researcherSetupFieldClass } from "../constants";
import {
  useCreateResearchLearner,
  useResearchLearners,
  useSchoolClasses,
} from "../hooks/useSchoolSetup";
import { SchoolLearnerForm } from "./SchoolLearnerForm";

type SchoolLearnersTabProps = {
  schoolId: string;
};

/** Renders the learner assignment tab for a selected school. */
export function SchoolLearnersTab({ schoolId }: SchoolLearnersTabProps) {
  const [selectedClassId, setSelectedClassId] = useState("");
  const classesQuery = useSchoolClasses(schoolId);
  const createLearner = useCreateResearchLearner();
  const classes = useMemo(() => classesQuery.data ?? [], [classesQuery.data]);
  const learnersQuery = useResearchLearners(selectedClassId || undefined);
  const selectedClass = classes.find((item) => item.id === selectedClassId);
  const noClasses = !classesQuery.isLoading && classes.length === 0;

  useEffect(() => {
    if (!selectedClassId && classes.length > 0) {
      setSelectedClassId(classes[0].id);
    }
  }, [classes, selectedClassId]);

  return (
    <Card variant="glass" padding="lg" className="space-y-5">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[color:var(--muted)]">
          Learners
        </p>
        <h2 className="mt-1 text-lg font-semibold text-[color:var(--ink)]">
          Assign and review learners by class
        </h2>
      </div>

      {noClasses ? (
        <div className="rounded-2xl border border-dashed border-(--line) bg-(--surface) p-6 text-center">
          <p className="text-sm font-semibold text-(--ink)">No classes yet.</p>
          <p className="mt-1 text-sm text-(--muted)">
            Add a class workspace first, then come back here to enrol its learners.
          </p>
          <Link
            href={`/research/setup/${schoolId}/classes`}
            className="mt-3 inline-flex text-sm font-semibold text-(--accent-deep) hover:underline"
          >
            Go to Classes →
          </Link>
        </div>
      ) : (
        <>
          <div className="space-y-2">
            <p className="text-sm font-semibold text-[color:var(--ink)]">Class</p>
            <select
              className={researcherSetupFieldClass}
              value={selectedClassId}
              onChange={(event) => setSelectedClassId(event.target.value)}
            >
              <option value="">Select class</option>
              {classes.map((item) => (
                <option key={item.id} value={item.id}>
                  {item.name} {item.grade ? `· ${item.grade}` : ""}
                </option>
              ))}
            </select>
          </div>

          {selectedClass && (
            <SchoolLearnerForm
              classId={selectedClass.id}
              grade={selectedClass.grade ?? ""}
              isLoading={createLearner.isPending}
              onSubmit={(values) => createLearner.mutateAsync(values).then(() => undefined)}
            />
          )}

          <div className="space-y-3">
            <h3 className="text-base font-semibold text-[color:var(--ink)]">Current learners</h3>
            {!selectedClassId ? (
              <p className="text-sm text-[color:var(--muted)]">Select a class to view learners.</p>
            ) : learnersQuery.data?.data.length ? (
              learnersQuery.data.data.map((learner) => (
                <div
                  key={learner.student_id}
                  className="rounded-3xl border border-[color:var(--line)] bg-(--surface) p-4 text-sm text-[color:var(--muted)]"
                >
                  <p className="font-semibold text-[color:var(--ink)]">{learner.full_name}</p>
                  <p className="mt-1">
                    {learner.code ?? learner.student_id} · {learner.track}
                  </p>
                </div>
              ))
            ) : (
              <p className="text-sm text-[color:var(--muted)]">No learners in this class yet.</p>
            )}
          </div>
        </>
      )}
    </Card>
  );
}
