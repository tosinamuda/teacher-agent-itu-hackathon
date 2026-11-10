import { ContentBlock } from "./lesson-schema";

/** One learner-facing section of a revision note (a manifest step). */
export type ReviewNoteSection = {
  step_id: string;
  title?: string | null;
  personalisation_band?: string | null;
  blocks: ContentBlock[];
};
