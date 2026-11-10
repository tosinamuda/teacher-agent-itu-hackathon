// @vitest-environment jsdom
import { cleanup, render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes, useLocation } from "react-router";
import { afterEach, expect, it } from "vitest";

import { LegacyLessonPlanRedirect, NavigateWithSearch } from "./redirects";

afterEach(cleanup);

function Where() {
  const { pathname, search } = useLocation();
  return <p>{`${pathname}${search}`}</p>;
}

function visit(entry: string) {
  render(
    <MemoryRouter initialEntries={[entry]}>
      <Routes>
        <Route
          path="/lesson-plan"
          element={<NavigateWithSearch to="/research/teacher/lesson-plan" />}
        />
        <Route path="/lesson-plan/:planId" element={<LegacyLessonPlanRedirect />} />
        <Route path="*" element={<Where />} />
      </Routes>
    </MemoryRouter>,
  );
}

it("sends the top-level generator to the teacher route and keeps the query", () => {
  visit("/lesson-plan?session_id=S-1");
  expect(screen.getByText("/research/teacher/lesson-plan?session_id=S-1")).toBeTruthy();
});

it("sends a plan to the teacher route that edits it", () => {
  visit("/lesson-plan/LPV-1?tab=edit");
  expect(screen.getByText("/research/teacher/lesson-plan/LPV-1?tab=edit")).toBeTruthy();
});
