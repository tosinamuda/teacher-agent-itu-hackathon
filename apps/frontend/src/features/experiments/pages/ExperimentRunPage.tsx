import { SyntheticTestPanel } from "../components/SyntheticTestPanel";
import { useExperiment } from "../hooks/useExperiments";

/** Run tab: the synthetic test harness (the "do" surface). Progress streams to Live. */
export default function ExperimentRunPage({ experimentId }: { experimentId: string }) {
  const { data: experiment } = useExperiment(experimentId);
  if (experiment?.lifecycle_status === "ended") {
    return <p className="py-6 text-sm text-(--muted)">Nothing runs on an ended experiment.</p>;
  }
  return (
    <div className="space-y-4 py-6">
      <p className="text-sm text-(--muted)">
        A dry run with a synthetic teacher, class and raters. It streams on Live; ratings land on
        Results.
      </p>
      <SyntheticTestPanel
        experimentId={experimentId}
        readiness={experiment?.readiness}
        context={{
          schoolName: experiment?.school_name,
          className: experiment?.class_name,
          subjectName: experiment?.subject_name,
          gradeLevel: experiment?.grade_level,
          term: experiment?.term,
          lessonTitle: experiment?.lesson_title,
        }}
      />
    </div>
  );
}
