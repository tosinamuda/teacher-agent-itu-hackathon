// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";

import { EvaluationRating, H1PacketDetail } from "../types";
import { H1RubricForm } from "./H1RubricForm";

vi.mock("@/shared/router", () => ({ useRouter: () => ({ push: vi.fn(), replace: vi.fn() }) }));

afterEach(cleanup);

const CRITERIA = ["accuracy", "clarity"];

const packet = (existing_rating: EvaluationRating | null): H1PacketDetail => ({
  evaluation_packet_id: "EP-1",
  packet_code: "H1-001",
  hypothesis: "H1",
  status: "assigned",
  objectives: [],
  reference_sheet: {
    curriculum_objectives: [],
    entry_behaviour: [],
    lesson_sequence: [],
    instructional_materials: [],
    evaluation: [],
  },
  candidate_pack: { scope: "class_level", manifest: { steps: [] } },
  rubric: CRITERIA.map((id) => ({
    criterion_id: id,
    label: id,
    description: id,
    scale_min: 1,
    scale_max: 5,
  })),
  major_issue_flags: [],
  existing_rating,
});

it("shows a saved rating's scores", () => {
  render(
    <H1RubricForm
      detail={packet({
        rating_id: "R-1",
        evaluation_packet_id: "EP-1",
        rater_id: "RT-1",
        hypothesis: "H1",
        overall_score: 3.5,
        rubric_scores: { accuracy: 4, clarity: 3 },
      })}
      isSaving={false}
      onSubmit={async () => {}}
    />
  );

  expect(screen.getByText("Score locked ✓")).toBeTruthy();
  expect(screen.getAllByText(/\/ 5$/).map((cell) => cell.textContent)).toEqual(["4 / 5", "3 / 5"]);
});

it("saves a new rating and then reads as saved, keeping the comment on screen", async () => {
  const onSubmit = vi.fn(async () => {});
  render(<H1RubricForm detail={packet(null)} isSaving={false} onSubmit={onSubmit} />);

  // One scale per criterion, in rubric order.
  fireEvent.click(screen.getAllByRole("button", { name: "4 Strong" })[0]);
  fireEvent.click(screen.getAllByRole("button", { name: "3 Adequate" })[1]);
  fireEvent.click(screen.getByRole("button", { name: /Add comments/ }));
  fireEvent.change(screen.getByPlaceholderText("Strengths"), { target: { value: "Clear steps." } });
  await waitFor(() => expect(screen.getByText("Unsaved changes")).toBeTruthy());

  fireEvent.click(screen.getByRole("button", { name: "Save rating" }));

  await waitFor(() =>
    expect(onSubmit).toHaveBeenCalledWith(
      expect.objectContaining({ rubric_scores: { accuracy: 4, clarity: 3 } })
    )
  );
  await waitFor(() => expect(screen.getByText(/^Saved at/)).toBeTruthy());
  expect(screen.queryByText("Unsaved changes")).toBeNull();
  expect((screen.getByPlaceholderText("Strengths") as HTMLTextAreaElement).value).toBe(
    "Clear steps."
  );
});
