/** The three personalisation bands a revision note can be pitched at. */
export type ReviewBand = "extend" | "reinforce" | "remediate";

/** Student-facing insight copy for each band, keyed off the assessment result. */
export const BAND_INSIGHT: Record<ReviewBand, { title: string; body: string }> = {
  extend: {
    title: "You're ready to go further",
    body: "You did well on your assessment — this note builds on what you know with richer ideas and tougher practice to extend your understanding.",
  },
  reinforce: {
    title: "Let's lock it in",
    body: "You've got the main idea — this note reinforces the key steps with extra worked examples and practice so it really sticks.",
  },
  remediate: {
    title: "Let's build it up step by step",
    body: "This note goes back over the lesson from the basics, with clear worked examples to help you grasp the concept.",
  },
};

export const normaliseBand = (raw?: string | null): ReviewBand | null => {
  const band = raw?.toLowerCase().trim();
  if (band === "extend" || band === "reinforce" || band === "remediate") return band;
  return null;
};
