import { Navigate, useLocation, useParams, useSearchParams } from "react-router";

/**
 * Redirect components for legacy paths (pre-/research URL space) and
 * param-carrying shortcuts. Each mirrors a `redirect()` page that lived under
 * Next's `src/app/`.
 */

/** Static redirect that carries the query string along. */
export function NavigateWithSearch({ to }: { to: string }) {
  const { search } = useLocation();
  return <Navigate to={`${to}${search}`} replace />;
}

/** `/experiments/:experimentId` → the researcher experiment detail. */
export function LegacyExperimentRedirect() {
  const { experimentId = "" } = useParams();
  return <Navigate to={`/research/experiments/${experimentId}`} replace />;
}

/** `/lesson-plan/:planId` → the generator editing that plan under the teacher routes. */
export function LegacyLessonPlanRedirect() {
  const { planId = "" } = useParams();
  const { search } = useLocation();
  return <Navigate to={`/research/teacher/lesson-plan/${planId}${search}`} replace />;
}

/** `/experiments/setup/:schoolId(?tab=…)` → research setup, query preserved. */
export function LegacySchoolSetupRedirect() {
  const { schoolId = "" } = useParams();
  const { search } = useLocation();
  return <Navigate to={`/research/setup/${schoolId}${search}`} replace />;
}

/** `/research/setup/:schoolId` → its details tab (query preserved). */
export function SchoolSetupDetailsRedirect() {
  const { schoolId = "" } = useParams();
  const { search } = useLocation();
  return <Navigate to={`/research/setup/${schoolId}/details${search}`} replace />;
}

/** `/research/h1/:experimentId` → the experiment's H1 lab (same for H2). */
export function HypothesisLabRedirect({ hypothesis }: { hypothesis: "h1" | "h2" }) {
  const { experimentId = "" } = useParams();
  return <Navigate to={`/research/experiments/${experimentId}/${hypothesis}`} replace />;
}

/** Unmatched paths — Next served its default 404 here. */
export function NotFoundRoute() {
  return (
    <main className="mx-auto max-w-md py-20 text-center text-sm text-(--muted)">
      <h1 className="mb-2 text-lg font-semibold text-(--ink)">Page not found</h1>
      <p>
        Nothing lives at this address.{" "}
        <a className="font-semibold text-(--accent-deep) underline" href="/research">
          Go to the workspace
        </a>
        .
      </p>
    </main>
  );
}

/** An old plan-making address, which named the lesson in `session_id`, → the page for that lesson. */
export function LessonPlanEntryRedirect({ to }: { to: (lessonPeriodId: string) => string }) {
  const [params] = useSearchParams();
  const lessonPeriodId = params.get("session_id");
  return <Navigate to={lessonPeriodId ? to(lessonPeriodId) : "/research/teacher/lessons"} replace />;
}

/** An old address that named the lesson in its path → the page for that lesson. */
export function LessonPlanPathRedirect({ to }: { to: (lessonPeriodId: string) => string }) {
  const { sessionId = "" } = useParams();
  return <Navigate to={to(sessionId)} replace />;
}
