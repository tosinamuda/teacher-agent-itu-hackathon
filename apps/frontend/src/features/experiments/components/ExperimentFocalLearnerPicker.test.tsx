// @vitest-environment jsdom
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, expect, it } from "vitest";

import { ExperimentFocalLearnerPicker } from "./ExperimentFocalLearnerPicker";

afterEach(cleanup);

const CANDIDATES = ["L1", "L2"].map((id) => ({
  learner_id: id,
  learner_name: `Learner ${id}`,
  latest_diagnostic_id: `DX-${id}`,
  has_evidence: true,
}));

it("shows a shortlist saved after it opened", () => {
  const props = { candidates: CANDIDATES, onSave: async () => {}, isSaving: false };
  const { rerender } = render(<ExperimentFocalLearnerPicker {...props} selectedLearnerIds={[]} />);

  rerender(<ExperimentFocalLearnerPicker {...props} selectedLearnerIds={["L2"]} />);

  const checked = (screen.getAllByRole("checkbox") as HTMLInputElement[]).map((box) => box.checked);
  expect(checked).toEqual([false, true]);
});
