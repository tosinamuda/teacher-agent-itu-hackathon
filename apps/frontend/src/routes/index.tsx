import type { RouteObject } from "react-router";
import { Navigate, Outlet } from "react-router";

import HomePage from "@/features/home/pages/HomePage";
import { ResearchShell } from "@/shared/components/layouts/ResearchShell";

import {
  LegacyExperimentRedirect,
  LegacyLessonPlanRedirect,
  LegacySchoolSetupRedirect,
  NavigateWithSearch,
  NotFoundRoute,
} from "./redirects";
import { researchRoutes } from "./research-routes";
import { RootLayout } from "./RootLayout";
import { RouteErrorPage } from "./RouteErrorPage";

function ResearchLayout() {
  return (
    <ResearchShell>
      <Outlet />
    </ResearchShell>
  );
}

/** Full route table — mirrors the deleted Next `src/app/` tree 1:1. */
export const routes: RouteObject[] = [
  {
    element: <RootLayout />,
    errorElement: <RouteErrorPage />,
    children: [
      { path: "/", element: <HomePage /> },
      { path: "/home", element: <HomePage /> },
      { path: "/lesson-plan", element: <NavigateWithSearch to="/research/teacher/lesson-plan" /> },
      {
        path: "/lesson-plan/new",
        element: <NavigateWithSearch to="/research/teacher/lesson-plan/new" />,
      },
      { path: "/lesson-plan/:planId", element: <LegacyLessonPlanRedirect /> },
      // Legacy URL space — server `redirect()` pages under Next.
      { path: "/experiments", element: <Navigate to="/research" replace /> },
      { path: "/experiments/new", element: <Navigate to="/research/experiments/new" replace /> },
      { path: "/experiments/setup", element: <Navigate to="/research/setup" replace /> },
      { path: "/experiments/setup/:schoolId", element: <LegacySchoolSetupRedirect /> },
      { path: "/experiments/:experimentId", element: <LegacyExperimentRedirect /> },
      { path: "/learners", element: <Navigate to="/research/learners" replace /> },
      { path: "/pack-runner", element: <NavigateWithSearch to="/experiments" /> },
      {
        path: "/research",
        element: <ResearchLayout />,
        children: researchRoutes,
      },
      { path: "*", element: <NotFoundRoute /> },
    ],
  },
];
