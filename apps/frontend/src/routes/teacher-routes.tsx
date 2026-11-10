import type { RouteObject } from "react-router";
import { useParams } from "react-router";

import ManualClassworkEntryPage from "@/features/classwork/pages/ManualClassworkEntryPage";
import DiagnosticReviewPage from "@/features/diagnostic-review/pages/DiagnosticReviewPage";
import OnBehalfEntryPage from "@/features/responses/pages/OnBehalfEntryPage";
import { TeacherExperimentPlanReviewPage } from "@/features/experiments/pages/TeacherExperimentPlanReviewPage";
import { TeacherExperimentPlansPage } from "@/features/experiments/pages/TeacherExperimentPlansPage";
import { useExperimentSummary } from "@/features/experiments/hooks/useExperiments";
import { TeacherLessonPrepPage } from "@/features/experiments/pages/TeacherLessonPrepPage";
import { NewLearnerPage } from "@/features/learners/pages/NewStudentPage";
import { LearnerDetailPage } from "@/features/learners/pages/StudentDetailPage";
import { SettingsPage } from "@/features/settings/SettingsPage";
import { LearnerListPage } from "@/features/learners/pages/StudentListPage";
import { ClassLandingPage } from "@/features/class-landing/pages/ClassLandingPage";
import { LessonEvidencePage } from "@/features/class-evidence/pages/LessonEvidencePage";
import { LessonLearnerEvidencePage } from "@/features/class-evidence/pages/LessonLearnerEvidencePage";
import { LessonHomePage } from "@/features/lesson-home/pages/LessonHomePage";
import { ImportPlanPage } from "@/features/lesson-plan/pages/ImportPlanPage";
import { MakePlanPage } from "@/features/lesson-plan/pages/MakePlanPage";
import { makePlanPath, writePlanPath } from "@/features/lesson-plan/lib/planPaths";
import { PlanPage } from "@/features/lesson-plan/pages/PlanPage";
import ManualPlanEntryPage from "@/features/lesson-plan/pages/ManualPlanEntryPage";
import { ReuseLessonPlanPage } from "@/features/lesson-plan/pages/ReuseLessonPlanPage";
import { ReuseLessonNotePage } from "@/features/lesson-home/pages/ReuseLessonNotePage";
import { ReusePlanPage } from "@/features/lesson-plan/pages/ReusePlanPage";
import { ContentReviewPage } from "@/features/content/pages/ContentReviewPage";
import LessonPreviewPage from "@/features/pack-review/pages/LessonPreviewPage";
import PackReviewQueuePage from "@/features/pack-review/pages/PackReviewQueuePage";
import TeacherTodoPage from "@/features/teaching-workspace/pages/TeacherTodoPage";

import { LessonPlanEntryRedirect, LessonPlanPathRedirect, NavigateWithSearch } from "./redirects";
import { TeacherLessonPreviewListRoute } from "./TeacherLessonPreviewListRoute";
import { TeacherSyllabusRoute } from "./TeacherSyllabusRoute";

function ExperimentPlanRoute({ review }: { review?: boolean }) {
  const { experimentId = "" } = useParams();
  return review ? (
    <TeacherExperimentPlanReviewPage experimentId={experimentId} />
  ) : (
    <TeacherLessonPrepPage experimentId={experimentId} />
  );
}

function LearnerDetailRoute() {
  const { learnerId = "" } = useParams();
  return <LearnerDetailPage learnerId={learnerId} />;
}

function LessonHomeRoute() {
  const { lessonPeriodId = "" } = useParams();
  return <LessonHomePage lessonPeriodId={lessonPeriodId} />;
}

function ReuseLessonPlanRoute() {
  const { lessonPeriodId = "" } = useParams();
  return <ReuseLessonPlanPage lessonPeriodId={lessonPeriodId} />;
}

function ReuseLessonNoteRoute() {
  const { lessonPeriodId = "" } = useParams();
  return <ReuseLessonNotePage lessonPeriodId={lessonPeriodId} />;
}

function LessonEvidenceRoute() {
  const { lessonPeriodId = "" } = useParams();
  return <LessonEvidencePage lessonPeriodId={lessonPeriodId} />;
}

function LessonLearnerEvidenceRoute() {
  const { lessonPeriodId = "", studentId = "" } = useParams();
  return <LessonLearnerEvidencePage lessonPeriodId={lessonPeriodId} studentId={studentId} />;
}

function LessonPlanEditRoute() {
  const { planId = "" } = useParams();
  return <PlanPage planId={planId} />;
}

function MakePlanRoute() {
  const { lessonPeriodId = "" } = useParams();
  return <MakePlanPage lessonPeriodId={lessonPeriodId} />;
}

function ImportPlanRoute() {
  const { lessonPeriodId = "" } = useParams();
  return <ImportPlanPage lessonPeriodId={lessonPeriodId} />;
}

function WritePlanRoute() {
  const { lessonPeriodId = "" } = useParams();
  return <ManualPlanEntryPage initialSessionId={lessonPeriodId} />;
}

function ExperimentManualPlanRoute() {
  const { experimentId = "" } = useParams();
  const experiment = useExperimentSummary(experimentId);
  const lessonId = experiment.data?.lesson_period_id ?? "";
  if (!lessonId) {
    return <div className="p-6 text-sm text-(--muted)">Loading lesson…</div>;
  }
  return (
    <ManualPlanEntryPage
      experimentId={experimentId}
      initialSessionId={lessonId}
    />
  );
}

function ExperimentReusePlanRoute() {
  const { experimentId = "" } = useParams();
  return <ReusePlanPage experimentId={experimentId} />;
}

function ExperimentManualClassworkRoute() {
  const { experimentId = "" } = useParams();
  const experiment = useExperimentSummary(experimentId);
  const planVersionId = experiment.data?.plan_version_id ?? "";
  if (!planVersionId) {
    return <div className="p-6 text-sm text-(--muted)">Loading lesson…</div>;
  }
  return (
    <ManualClassworkEntryPage
      experimentId={experimentId}
      planVersionId={planVersionId}
    />
  );
}

function ExperimentOnBehalfResponsesRoute() {
  const { experimentId = "" } = useParams();
  const experiment = useExperimentSummary(experimentId);
  const planVersionId = experiment.data?.plan_version_id ?? "";
  if (!planVersionId) {
    return <div className="p-6 text-sm text-(--muted)">Loading lesson…</div>;
  }
  return (
    <OnBehalfEntryPage
      experimentId={experimentId}
      planVersionId={planVersionId}
    />
  );
}

function LessonPreviewDetailRoute() {
  const { artefactId = "" } = useParams();
  return <LessonPreviewPage artefactId={artefactId} />;
}

function DiagnosticReviewRoute() {
  const { planVersionId = "" } = useParams();
  return <DiagnosticReviewPage planVersionId={planVersionId} />;
}

function ContentReviewRoute({
  contentParam = "contentId",
}: {
  contentParam?: string;
}) {
  const params = useParams();
  return <ContentReviewPage contentId={params[contentParam] ?? ""} />;
}

/** `/research/teacher/*` children (spliced into the research route table). */
export const teacherRoutes: RouteObject[] = [
  { path: "teacher/to-do", element: <TeacherTodoPage /> },
  {
    path: "teacher/experiment-plans",
    element: <TeacherExperimentPlansPage view="to-prepare" />,
  },
  {
    path: "teacher/experiment-plans/all",
    element: <TeacherExperimentPlansPage view="all" />,
  },
  {
    path: "teacher/experiment-plans/:experimentId",
    element: <ExperimentPlanRoute />,
  },
  {
    path: "teacher/experiment-plans/:experimentId/plan",
    element: <ExperimentPlanRoute review />,
  },
  {
    path: "teacher/experiment-plans/:experimentId/manual",
    element: <ExperimentManualPlanRoute />,
  },
  {
    path: "teacher/experiment-plans/:experimentId/reuse",
    element: <ExperimentReusePlanRoute />,
  },
  {
    path: "teacher/experiment-plans/:experimentId/classwork",
    element: <ExperimentManualClassworkRoute />,
  },
  {
    path: "teacher/experiment-plans/:experimentId/responses",
    element: <ExperimentOnBehalfResponsesRoute />,
  },
  { path: "teacher/settings", element: <SettingsPage /> },
  { path: "teacher/learners", element: <LearnerListPage /> },
  { path: "teacher/learners/new", element: <NewLearnerPage /> },
  { path: "teacher/learners/:learnerId", element: <LearnerDetailRoute /> },
  { path: "teacher/lessons", element: <ClassLandingPage /> },
  { path: "teacher/lessons/:lessonPeriodId", element: <LessonHomeRoute /> },
  {
    path: "teacher/lessons/:lessonPeriodId/evidence",
    element: <LessonEvidenceRoute />,
  },
  {
    path: "teacher/lessons/:lessonPeriodId/evidence/:studentId",
    element: <LessonLearnerEvidenceRoute />,
  },
  { path: "teacher/lessons/:lessonPeriodId/reuse-plan", element: <ReuseLessonPlanRoute /> },
  { path: "teacher/lessons/:lessonPeriodId/reuse-note", element: <ReuseLessonNoteRoute /> },
  { path: "teacher/lessons/:lessonPeriodId/plan/new", element: <MakePlanRoute /> },
  { path: "teacher/lessons/:lessonPeriodId/plan/import", element: <ImportPlanRoute /> },
  { path: "teacher/lessons/:lessonPeriodId/plan/write", element: <WritePlanRoute /> },
  { path: "teacher/lesson-plan", element: <LessonPlanEntryRedirect to={makePlanPath} /> },
  { path: "teacher/lesson-plan/new", element: <LessonPlanEntryRedirect to={makePlanPath} /> },
  { path: "teacher/lesson-plan/manual", element: <LessonPlanEntryRedirect to={writePlanPath} /> },
  { path: "teacher/lesson-plan/manual/:sessionId", element: <LessonPlanPathRedirect to={writePlanPath} /> },
  { path: "teacher/lesson-plan/:planId", element: <LessonPlanEditRoute /> },
  {
    path: "teacher/lesson-preview",
    element: <TeacherLessonPreviewListRoute />,
  },
  {
    path: "teacher/lesson-preview/:artefactId",
    element: <LessonPreviewDetailRoute />,
  },
  { path: "teacher/pack-reviews", element: <PackReviewQueuePage /> },
  {
    path: "teacher/pack-reviews/:artefactId",
    element: <ContentReviewRoute contentParam="artefactId" />,
  },
  {
    path: "teacher/pack-runner",
    element: <NavigateWithSearch to="/research/teacher/lesson-preview" />,
  },
  {
    path: "teacher/diagnostics/:planVersionId",
    element: <DiagnosticReviewRoute />,
  },
  { path: "teacher/content/:contentId", element: <ContentReviewRoute /> },
  { path: "teacher/syllabus", element: <TeacherSyllabusRoute /> },
];
