const KNOWN: Record<string, string> = {
  approve_the_plan_first:
    "Approve this lesson's plan first. The marks are matched to its objectives.",
  class_results_already_imported:
    "Class results are already imported on this lesson.",
  study_results_not_found: "That lesson has no marked classwork to bring in.",
};

/** What a teacher reads when an import is refused, from the API's error text. */
export function importErrorText(message: string): string {
  for (const [code, text] of Object.entries(KNOWN)) {
    if (message.includes(code)) return text;
  }
  if (message.includes("the_plan_lacks_the_objectives")) {
    return "This lesson's plan does not cover the objectives those marks belong to. Pick the lesson this plan was reused from.";
  }
  return "Could not import the class results. Nothing was saved.";
}
