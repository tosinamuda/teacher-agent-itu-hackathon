import type { RouteObject } from "react-router";
import { Outlet, useParams } from "react-router";

import { ExperimentShell } from "@/features/experiments/components/ExperimentShell";
import { AssessmentPreviewPage } from "@/features/experiments/pages/AssessmentPreviewPage";
import { ConditionPackPreviewPage } from "@/features/experiments/pages/ConditionPackPreviewPage";
import { LearnerPackComparePage } from "@/features/experiments/pages/LearnerPackComparePage";
import ExperimentComparePage from "@/features/experiments/pages/ExperimentComparePage";
import { ExperimentHypothesisLabPage } from "@/features/experiments/pages/ExperimentHypothesisLabPage";
import ExperimentLivePage from "@/features/experiments/pages/ExperimentLivePage";
import { ExperimentOverviewPage } from "@/features/experiments/pages/ExperimentOverviewPage";
import ExperimentResultsPage from "@/features/experiments/pages/ExperimentResultsPage";
import ExperimentRunPage from "@/features/experiments/pages/ExperimentRunPage";
import { ExperimentsPage } from "@/features/experiments/pages/ExperimentsPage";
import ExperimentStoryPage from "@/features/experiments/pages/ExperimentStoryPage";
import { InvestigationShell } from "@/features/experiments/components/InvestigationShell";
import InvestigationOverviewPage from "@/features/experiments/pages/InvestigationOverviewPage";
import InvestigationResultsPage from "@/features/experiments/pages/InvestigationResultsPage";
import WalkthroughPage from "@/features/walkthrough/WalkthroughPage";
import { LessonPlanPreviewPage } from "@/features/experiments/pages/LessonPlanPreviewPage";
import { NewExperimentPage } from "@/features/experiments/pages/NewExperimentPage";
import NewInvestigationPage from "@/features/experiments/pages/NewInvestigationPage";
import { ResearchLandingPage } from "@/features/experiments/pages/ResearchLandingPage";
import { StoryNavigatorPage } from "@/features/experiments/pages/StoryNavigatorPage";
import { AuditItemPage } from "@/features/evaluation/pages/AuditItemPage";
import { AuditQueuePage } from "@/features/evaluation/pages/AuditQueuePage";
import { RaterLandingPage } from "@/features/evaluation/pages/RaterLandingPage";
import { RaterPacketPage } from "@/features/evaluation/pages/RaterPacketPage";
import { RaterQueuePage } from "@/features/evaluation/pages/RaterQueuePage";
import { ResearchHome } from "@/features/home/pages/ResearchHome";
import { OpsPage } from "@/features/ops/pages/OpsPage";
import { PluginsPage } from "@/features/plugins/pages/PluginsPage";
import { ResearchLearnerDirectoryPage } from "@/features/learners/pages/ResearchLearnerDirectoryPage";
import { RaterAssignmentsPage } from "@/features/rater-assignments/pages/RaterAssignmentsPage";
import { NewResearchSchoolPage } from "@/features/researcher-setup/pages/NewResearchSchoolPage";
import { ResearchSchoolSetupDetailPage } from "@/features/researcher-setup/pages/ResearchSchoolSetupDetailPage";
import { ResearchSchoolSetupPage } from "@/features/researcher-setup/pages/ResearchSchoolSetupPage";
import { StudentProvider } from "@/features/student/context/StudentContext";
import StudentExitAssessmentPage from "@/features/student/pages/StudentExitAssessmentPage";
import { StudentLessonPage } from "@/features/student/pages/StudentLessonPage";
import { StudentReviewNotePage } from "@/features/student/pages/StudentReviewNotePage";
import { UsersPage } from "@/features/users/pages/UsersPage";

import { HypothesisLabRedirect, SchoolSetupDetailsRedirect } from "./redirects";
import { StudentRootRoute } from "./StudentRootRoute";
import { teacherRoutes } from "./teacher-routes";

/** Tabbed shell around every `/research/experiments/:experimentId/*` page. */
function ExperimentLayout() {
  const { experimentId = "" } = useParams();
  return (
    <ExperimentShell experimentId={experimentId}>
      <Outlet />
    </ExperimentShell>
  );
}

function ExperimentOverviewRoute() {
  const { experimentId = "" } = useParams();
  return <ExperimentOverviewPage experimentId={experimentId} />;
}

function HypothesisLabRoute({ hypothesis }: { hypothesis: "H1" | "H2" }) {
  const { experimentId = "" } = useParams();
  return (
    <ExperimentHypothesisLabPage
      key={`${experimentId}:${hypothesis}`}
      experimentId={experimentId}
      hypothesis={hypothesis}
    />
  );
}

function ExperimentParamRoute({
  render,
}: {
  render: (experimentId: string) => React.ReactElement;
}) {
  const { experimentId = "" } = useParams();
  return render(experimentId);
}

/** Static segments win over `:conditionCode`, exactly as Next resolved it —
 *  the dynamic entry only fires for the condition codes c0–c3. */
function ConditionPreviewRoute() {
  const { experimentId = "", conditionCode = "" } = useParams();
  return <ConditionPackPreviewPage experimentId={experimentId} conditionCode={conditionCode} />;
}

function LearnerPackCompareRoute() {
  const { experimentId = "", learnerId = "" } = useParams();
  return <LearnerPackComparePage experimentId={experimentId} learnerId={learnerId} />;
}

function InvestigationLayout() {
  const { investigationId = "" } = useParams();
  return (
    <InvestigationShell investigationId={investigationId}>
      <Outlet />
    </InvestigationShell>
  );
}

function InvestigationParamRoute({
  render,
}: {
  render: (investigationId: string) => React.ReactElement;
}) {
  const { investigationId = "" } = useParams();
  return render(investigationId);
}

function SchoolSetupSectionRoute({ section }: { section: "details" | "classes" | "learners" }) {
  const { schoolId = "" } = useParams();
  return <ResearchSchoolSetupDetailPage schoolId={schoolId} section={section} />;
}

function RaterPacketRoute({ hypothesis }: { hypothesis: "H1" | "H2" }) {
  const { packetId = "" } = useParams();
  return <RaterPacketPage hypothesis={hypothesis} packetId={packetId} />;
}

function AuditItemRoute() {
  const { itemId = "" } = useParams();
  return <AuditItemPage auditItemId={itemId} />;
}

function StudentLessonRoute() {
  const { planVersionId = "" } = useParams();
  return (
    <StudentProvider>
      <StudentLessonPage planVersionId={planVersionId} />
    </StudentProvider>
  );
}

/** Children of the `/research` shell (researcher, rater, student, teacher). */
export const researchRoutes: RouteObject[] = [
  { index: true, element: <ResearchHome /> },
  { path: "investigations", element: <ResearchLandingPage /> },
  { path: "investigations/new", element: <NewInvestigationPage /> },
  {
    path: "investigations/:investigationId",
    element: <InvestigationLayout />,
    children: [
      {
        index: true,
        element: (
          <InvestigationParamRoute
            render={(id) => <InvestigationOverviewPage investigationId={id} />}
          />
        ),
      },
      {
        path: "results",
        element: (
          <InvestigationParamRoute
            render={(id) => <InvestigationResultsPage investigationId={id} />}
          />
        ),
      },
      {
        path: "walkthrough",
        element: (
          <InvestigationParamRoute render={(id) => <WalkthroughPage investigationId={id} />} />
        ),
      },
    ],
  },
  {
    path: "experiments",
    element: (
      <ExperimentsPage actionPathPrefix="/research/experiments" title="Experiments" />
    ),
  },
  { path: "experiments/new", element: <NewExperimentPage /> },
  {
    path: "experiments/:experimentId",
    element: <ExperimentLayout />,
    children: [
      { index: true, element: <ExperimentOverviewRoute /> },
      { path: "h1", element: <HypothesisLabRoute hypothesis="H1" /> },
      { path: "h2", element: <HypothesisLabRoute hypothesis="H2" /> },
      { path: "h2/learners/:learnerId", element: <LearnerPackCompareRoute /> },
      {
        path: "lesson-plan",
        element: <ExperimentParamRoute render={(id) => <LessonPlanPreviewPage experimentId={id} />} />,
      },
      {
        path: "assessment",
        element: <ExperimentParamRoute render={(id) => <AssessmentPreviewPage experimentId={id} />} />,
      },
      {
        path: "run",
        element: <ExperimentParamRoute render={(id) => <ExperimentRunPage experimentId={id} />} />,
      },
      {
        path: "live",
        element: <ExperimentParamRoute render={(id) => <ExperimentLivePage experimentId={id} />} />,
      },
      {
        path: "raters",
        element: <ExperimentParamRoute render={(id) => <RaterAssignmentsPage experimentId={id} />} />,
      },
      {
        path: "results",
        element: <ExperimentParamRoute render={(id) => <ExperimentResultsPage experimentId={id} />} />,
      },
      {
        path: "story",
        element: <ExperimentParamRoute render={(id) => <ExperimentStoryPage experimentId={id} />} />,
      },
      {
        path: "compare",
        element: <ExperimentParamRoute render={(id) => <ExperimentComparePage experimentId={id} />} />,
      },
      { path: ":conditionCode", element: <ConditionPreviewRoute /> },
    ],
  },
  {
    path: "h1",
    element: (
      <ExperimentsPage
        actionPathPrefix="/research/h1"
        hypothesis="H1"
        title="H1 curriculum-alignment experiments"
      />
    ),
  },
  { path: "h1/:experimentId", element: <HypothesisLabRedirect hypothesis="h1" /> },
  {
    path: "h2",
    element: (
      <ExperimentsPage
        actionPathPrefix="/research/h2"
        hypothesis="H2"
        title="H2 personalization experiments"
      />
    ),
  },
  { path: "h2/:experimentId", element: <HypothesisLabRedirect hypothesis="h2" /> },
  { path: "story", element: <StoryNavigatorPage /> },
  { path: "learners", element: <ResearchLearnerDirectoryPage /> },
  { path: "ops", element: <OpsPage /> },
  { path: "plugins", element: <PluginsPage tab="plugins" /> },
  { path: "plugins/generators", element: <PluginsPage tab="generators" /> },
  { path: "setup", element: <ResearchSchoolSetupPage /> },
  { path: "setup/school/new", element: <NewResearchSchoolPage /> },
  { path: "setup/users", element: <UsersPage /> },
  { path: "setup/:schoolId", element: <SchoolSetupDetailsRedirect /> },
  { path: "setup/:schoolId/details", element: <SchoolSetupSectionRoute section="details" /> },
  { path: "setup/:schoolId/classes", element: <SchoolSetupSectionRoute section="classes" /> },
  { path: "setup/:schoolId/learners", element: <SchoolSetupSectionRoute section="learners" /> },
  { path: "rater", element: <RaterLandingPage /> },
  { path: "rater/h1", element: <RaterQueuePage hypothesis="H1" /> },
  { path: "rater/h1/:packetId", element: <RaterPacketRoute hypothesis="H1" /> },
  { path: "rater/h2", element: <RaterQueuePage hypothesis="H2" /> },
  { path: "rater/h2/:packetId", element: <RaterPacketRoute hypothesis="H2" /> },
  { path: "rater/audit", element: <AuditQueuePage /> },
  { path: "rater/audit/:itemId", element: <AuditItemRoute /> },
  { path: "student", element: <StudentRootRoute /> },
  {
    path: "student/exit-assessment",
    element: (
      <StudentProvider>
        <StudentExitAssessmentPage />
      </StudentProvider>
    ),
  },
  { path: "student/lesson/:planVersionId", element: <StudentLessonRoute /> },
  {
    path: "student/pack-runner",
    element: (
      <StudentProvider>
        <StudentReviewNotePage />
      </StudentProvider>
    ),
  },
  ...teacherRoutes,
];
