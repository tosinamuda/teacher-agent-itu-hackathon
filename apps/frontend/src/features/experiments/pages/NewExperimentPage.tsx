import { Link } from "@/shared/router";
import { useEffect, useMemo } from "react";
import { useRouter, useSearchParams } from "@/shared/router";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm, useWatch } from "react-hook-form";
import { z } from "zod";

import { Button } from "@/shared/components/ui/Button";
import { Card } from "@/shared/components/ui/Card";

import {
  useCreateExperiment,
  useExperimentWorkspaceLessons,
  useExperimentWorkspaces,
} from "../hooks/useExperiments";
import { useInvestigations } from "../hooks/useInvestigations";

const formSchema = z.object({
  investigation_id: z.string().min(1, "Select a study."),
  school_id: z.string().min(1, "Select a school."),
  teacher_workspace_id: z.string().min(1, "Select a workspace."),
  lesson_period_id: z.string().min(1, "Select a lesson."),
});

type FormValues = z.infer<typeof formSchema>;

const fieldClass =
  "w-full min-w-0 rounded-none border border-[color:var(--line)] bg-(--surface) px-4 py-2 text-sm text-[color:var(--ink)] outline-none transition focus:border-[color:var(--accent)]";

/** Workspace label WITHOUT the school (already chosen in step 1): class · subject · term · teacher. */
const workspaceLabel = (workspace: {
  class_name: string;
  subject_name: string;
  term: string;
  teacher_name?: string | null;
}) =>
  [workspace.class_name, workspace.subject_name, workspace.term, workspace.teacher_name]
    .filter(Boolean)
    .join(" · ");

/** A lesson is studiable only if it carries a real topic (subtopic) — a teacher
 *  authors a plan for that subtopic. Empty placeholder slots (title "Lesson"/blank,
 *  no subtopic) have nothing to study, so they are hidden from the picker. */
const lessonTopic = (lesson: { lesson_title: string; lesson_subtitle?: string | null }) => {
  const topic = (lesson.lesson_subtitle || lesson.lesson_title || "").trim();
  return topic && topic.toLowerCase() !== "lesson" ? topic : null;
};

/** Lesson label: "Week N · {subtopic}". */
const lessonLabel = (lesson: {
  week_number: number;
  lesson_title: string;
  lesson_subtitle?: string | null;
}) => `Week ${lesson.week_number} · ${lessonTopic(lesson)}`;

const STEPS_WITH_STUDY = [
  "Choose study",
  "Choose school",
  "Choose workspace",
  "Choose lesson",
  "Create experiment",
];

const STEPS_PREFILLED_STUDY = [
  "Choose school",
  "Choose workspace",
  "Choose lesson",
  "Create experiment",
];

/** Renders the selector-driven experiment creation flow (filed into a study). */
export function NewExperimentPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const createMutation = useCreateExperiment();
  const workspacesQuery = useExperimentWorkspaces();
  const studiesQuery = useInvestigations();
  const prefilledSchoolId = searchParams.get("schoolId");
  const prefilledInvestigationId = searchParams.get("investigationId");

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      investigation_id: "",
      school_id: "",
      teacher_workspace_id: "",
      lesson_period_id: "",
    },
  });

  const schoolId = useWatch({ control: form.control, name: "school_id" });
  const workspaceId = useWatch({
    control: form.control,
    name: "teacher_workspace_id",
  });
  const lessonPeriodId = useWatch({ control: form.control, name: "lesson_period_id" });

  const lessonsQuery = useExperimentWorkspaceLessons(workspaceId || null);
  // Only studiable lessons (those with a real subtopic) — empty placeholder slots
  // are filtered out, so the picker never shows indistinguishable "Lesson" rows.
  const lessons = (lessonsQuery.data ?? []).filter((lesson) => lessonTopic(lesson) !== null);
  // A workspace whose scheme of work has no topic-bearing lessons has nothing to
  // study — surface that instead of an empty dropdown + a cryptic submit error.
  const workspaceHasNoLessons =
    Boolean(workspaceId) && !lessonsQuery.isLoading && lessons.length === 0;

  const studies = useMemo(
    () => (studiesQuery.data ?? []).filter((study) => study.status !== "ended"),
    [studiesQuery.data]
  );
  const workspaces = useMemo(() => workspacesQuery.data ?? [], [workspacesQuery.data]);
  const schools = useMemo(
    () =>
      Array.from(
        new Map(
          workspaces.map((workspace) => [
            workspace.school_id,
            {
              id: workspace.school_id,
              label: `${workspace.school_name} (${workspace.school_code})`,
            },
          ])
        ).values()
      ),
    [workspaces]
  );
  const filteredWorkspaces = useMemo(
    () =>
      schoolId
        ? workspaces.filter((workspace) => workspace.school_id === schoolId)
        : workspaces,
    [schoolId, workspaces]
  );

  useEffect(() => {
    if (!prefilledSchoolId || schoolId) {
      return;
    }
    const matchingSchool = workspaces.some(
      (workspace) => workspace.school_id === prefilledSchoolId
    );
    if (matchingSchool) {
      form.setValue("school_id", prefilledSchoolId);
    }
  }, [form, prefilledSchoolId, schoolId, workspaces]);

  // Prefill (and lock) the study when launched from a study's "Add experiment".
  useEffect(() => {
    if (prefilledInvestigationId) {
      form.setValue("investigation_id", prefilledInvestigationId);
    }
  }, [form, prefilledInvestigationId]);

  const submit = form.handleSubmit(async (values) => {
    const experiment = await createMutation.mutateAsync({
      investigation_id: values.investigation_id,
      teacher_workspace_id: values.teacher_workspace_id,
      lesson_period_id: values.lesson_period_id,
    });
    router.push(`/research/experiments/${experiment.experiment_id}`);
  });

  return (
    <main className="mx-auto flex w-full max-w-4xl flex-col gap-6 px-6 py-10">
      <header className="space-y-3">
        <div className="text-[11px] font-semibold uppercase tracking-[0.18em] text-[color:var(--accent)]">
          New experiment
        </div>
        <h1 className="text-4xl font-semibold tracking-tight text-[color:var(--ink)]">
          Create a lesson-scoped experiment container.
        </h1>
        <p className="text-base leading-relaxed text-[color:var(--muted)]">
          Pick the lesson to study — no plan needed up front. The assigned teacher authors + freezes
          the experiment&apos;s own plan next; hypothesis choice (H1 / H2) happens later in the lab.
        </p>
      </header>

      {(() => {
        const steps = prefilledInvestigationId
          ? STEPS_PREFILLED_STUDY
          : STEPS_WITH_STUDY;
        const stepCols = prefilledInvestigationId ? "md:grid-cols-4" : "md:grid-cols-5";
        const prefilledStudy = prefilledInvestigationId
          ? studies.find((s) => s.investigation_id === prefilledInvestigationId)
          : null;
        const stepOffset = prefilledInvestigationId ? 1 : 0;
        return (
      <Card variant="glass" padding="lg" className="space-y-5">
        <div className={`grid gap-3 ${stepCols}`}>
          {steps.map((step, index) => (
            <div
              key={step}
              className="rounded-3xl border border-[color:var(--line)] bg-(--surface) p-4"
            >
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[color:var(--muted)]">
                Step {index + 1}
              </p>
              <p className="mt-2 text-sm font-semibold text-[color:var(--ink)]">{step}</p>
            </div>
          ))}
        </div>

        <form className="grid gap-4 md:grid-cols-2" onSubmit={submit}>
          {prefilledInvestigationId ? (
            <div className="md:col-span-2 flex flex-wrap items-baseline gap-2 border-l-2 border-(--accent) bg-(--accent-soft) px-3 py-2 text-sm">
              <span className="text-[11px] font-semibold uppercase tracking-[0.14em] text-(--accent)">
                Study
              </span>
              <span className="font-medium text-(--ink)">
                {prefilledStudy?.title ?? "(loading…)"}
              </span>
              {prefilledStudy?.investigation_code ? (
                <span className="font-mono text-xs text-(--muted)">
                  · {prefilledStudy.investigation_code}
                </span>
              ) : null}
              <input type="hidden" {...form.register("investigation_id")} />
            </div>
          ) : (
            <label className="min-w-0 space-y-2 md:col-span-2">
              <span className="text-xs font-semibold uppercase tracking-[0.16em] text-[color:var(--muted)]">
                Step 1 · Study
              </span>
              <select className={fieldClass} {...form.register("investigation_id")}>
                <option value="">Select study</option>
                {studies.map((study) => (
                  <option key={study.investigation_id} value={study.investigation_id}>
                    {study.title} ({study.investigation_code})
                  </option>
                ))}
              </select>
              <span className="text-xs text-(--muted)">
                Every experiment belongs to a study.{" "}
                <Link href="/research/investigations/new" className="font-semibold underline">
                  New study
                </Link>
              </span>
            </label>
          )}
          <label className="min-w-0 space-y-2">
            <span className="text-xs font-semibold uppercase tracking-[0.16em] text-[color:var(--muted)]">
              Step {2 - stepOffset} · School
            </span>
            <select
              className={fieldClass}
              {...form.register("school_id", {
                onChange: () => {
                  form.setValue("teacher_workspace_id", "");
                  form.setValue("lesson_period_id", "");
                },
              })}
            >
              <option value="">Select school</option>
              {schools.map((school) => (
                <option key={school.id} value={school.id}>
                  {school.label}
                </option>
              ))}
            </select>
          </label>
          <label className="min-w-0 space-y-2">
            <span className="text-xs font-semibold uppercase tracking-[0.16em] text-[color:var(--muted)]">
              Step {3 - stepOffset} · Workspace
            </span>
            <select
              className={fieldClass}
              {...form.register("teacher_workspace_id", {
                onChange: () => {
                  form.setValue("lesson_period_id", "");
                },
              })}
            >
              <option value="">Select workspace</option>
              {filteredWorkspaces.map((workspace) => (
                <option key={workspace.teacher_workspace_id} value={workspace.teacher_workspace_id}>
                  {workspaceLabel(workspace)}
                </option>
              ))}
            </select>
          </label>
          <label className="min-w-0 space-y-2">
            <span className="text-xs font-semibold uppercase tracking-[0.16em] text-[color:var(--muted)]">
              Step {4 - stepOffset} · Lesson
            </span>
            <select
              className={fieldClass}
              disabled={!workspaceId || workspaceHasNoLessons}
              {...form.register("lesson_period_id")}
            >
              <option value="">
                {workspaceHasNoLessons ? "No topic-bearing lessons" : "Select lesson"}
              </option>
              {lessons.map((lesson) => (
                <option key={lesson.lesson_period_id} value={lesson.lesson_period_id}>
                  {lessonLabel(lesson)}
                </option>
              ))}
            </select>
          </label>
          {workspaceHasNoLessons ? (
            <p className="text-sm text-(--danger-ink) md:col-span-2">
              This workspace&apos;s scheme of work has no lessons with a topic yet — nothing to
              study. Pick a workspace with a mapped curriculum (e.g. a JSS1 Mathematics research
              class), or map subtopics to its scheme of work in{" "}
              <Link href="/research/setup" className="font-semibold underline">
                Setup
              </Link>
              .
            </p>
          ) : (
            <p className="text-xs text-(--muted) md:col-span-2">
              The experiment is created against this lesson. The assigned teacher then authors and
              freezes the experiment&apos;s own plan — that freeze triggers C0–C3.
            </p>
          )}

          {createMutation.isError && (
            <p className="text-sm text-(--danger-ink) md:col-span-2">
              {createMutation.error instanceof Error
                ? createMutation.error.message
                : "Failed to create experiment."}
            </p>
          )}

          <div className="flex flex-wrap items-center gap-3 md:col-span-2">
            <Button type="submit" isLoading={createMutation.isPending} disabled={!lessonPeriodId}>
              Create experiment
            </Button>
            <Link
              className="text-sm font-semibold text-[color:var(--accent-deep)] hover:underline"
              href="/research"
            >
              Back to research
            </Link>
          </div>
        </form>
      </Card>
        );
      })()}
    </main>
  );
}
