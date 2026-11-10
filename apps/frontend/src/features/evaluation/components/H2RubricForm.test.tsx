// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import type { ComponentProps } from "react";
import { afterEach, expect, it, vi } from "vitest";

import { EvaluationH2StoredSectionScore, H2PacketDetail } from "../types";
import { H2RubricForm } from "./H2RubricForm";

vi.mock("@/shared/router", () => ({ useRouter: () => ({ push: vi.fn(), replace: vi.fn() }) }));

afterEach(cleanup);

const scores = (value: number): EvaluationH2StoredSectionScore => ({
  learner_state_suitability: value,
  scaffolding_appropriateness: value,
  challenge_calibration: value,
  misconception_support: null,
  objective_preservation: value,
  section_score: value,
});

/** One section, two blinded candidates, and the rater's saved scores and comment. */
const PACKET: H2PacketDetail = {
  evaluation_packet_id: "EP-2",
  packet_code: "H2-001",
  hypothesis: "H2",
  status: "assigned",
  objectives: [{ lesson_objective_id: "lop01", objective_text: "Identify improper fractions" }],
  focal_learner: { focal_case_type: "partial", mastered_sections: [] },
  candidates: ["A", "B"].map((label, index) => ({
    candidate_id: `CAND-${label}`,
    label: `Candidate ${label}`,
    display_order: index,
    pack: { manifest: { steps: [] } },
  })),
  sections: [
    {
      section_id: "SEC-1",
      step_id: "s1",
      title: "Improper fractions",
      lesson_objective_id: "lop01",
      objective_text: "Identify improper fractions",
      candidate_steps: {
        "CAND-A": { step_id: "s1", title: "Improper fractions", blocks: [] },
        "CAND-B": { step_id: "s1", title: "Improper fractions", blocks: [] },
      },
    },
  ],
  rubric: [],
  existing_rating: {
    rating_id: "R-2",
    evaluation_packet_id: "EP-2",
    rater_id: "RT-1",
    hypothesis: "H2",
    overall_score: 3.5,
    rubric_scores: {},
    section_scores: { "SEC-1": { "CAND-A": scores(4), "CAND-B": scores(3) } },
    notes: { strengths: "Stays on the objective." },
    updated_at: "2026-09-27T10:00:00Z",
  },
};

const openComments = () => fireEvent.click(screen.getByRole("button", { name: /Add comments/ }));
const strengths = () => (screen.getByPlaceholderText("Strengths") as HTMLTextAreaElement).value;

it("opens a saved rating with its scores and comment filled in", () => {
  render(<H2RubricForm detail={PACKET} isSaving={false} onSubmit={async () => {}} />);

  expect(screen.getAllByText("4 Good")).toHaveLength(4);
  expect(screen.getAllByText("3 Adequate")).toHaveLength(4);

  fireEvent.click(screen.getByRole("button", { name: "Finalize rating" }));
  openComments();
  expect(strengths()).toBe("Stays on the objective.");
  expect(screen.getByText(/^Saved at/)).toBeTruthy();
});

it("saves a changed score and then reads as saved, keeping the comment", async () => {
  const onSubmit = vi.fn<ComponentProps<typeof H2RubricForm>["onSubmit"]>(async () => {});
  render(<H2RubricForm detail={PACKET} isSaving={false} onSubmit={onSubmit} />);

  fireEvent.click(screen.getAllByRole("button", { name: "5 Excellent" })[0]);
  fireEvent.click(screen.getByRole("button", { name: "Finalize rating" }));
  await waitFor(() => expect(screen.getByText("Unsaved changes")).toBeTruthy());

  fireEvent.click(screen.getByRole("button", { name: "Save rating" }));

  await waitFor(() => expect(onSubmit).toHaveBeenCalled());
  const saved = onSubmit.mock.calls[0][0].candidate_section_scores.map((row) => [
    row.candidate_id,
    row.section_scores[0].learner_state_suitability,
  ]);
  expect(saved).toEqual([
    ["CAND-A", 5],
    ["CAND-B", 3],
  ]);
  await waitFor(() => expect(screen.getByText(/^Saved at/)).toBeTruthy());
  expect(screen.queryByText("Unsaved changes")).toBeNull();
  openComments();
  expect(strengths()).toBe("Stays on the objective.");
});
