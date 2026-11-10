import { ContentItem, ReviewRecord } from "./types";

const CHECK_LABELS: Record<string, string> = {
  objective_coverage: "Every objective has a section",
  scope_compliance: "No section for an objective outside the lesson",
  source_refs_present: "Every section cites a source",
  source_refs_valid: "Every citation names a passage the section was given",
  objective_preservation: "No objective dropped from the class note",
  no_added_objectives: "No objective added to the class note",
  practice_is_checkable: "Every section has practice, each with an answer",
  explanation_present: "Every section explains the idea in full",
  adaptation_limits:
    "The class note's drawings kept, and only what may adapt changed",
  misconception_repair:
    "A misconception repaired where the learner's state names one",
  note_substance: "Every step's note holds enough to teach from",
  no_second_thoughts: "No second thought left in the text",
  size_rule_correct: "No false rule about which number is larger",
  rounding_correct: "Every rounding in the text is right",
  distinct_questions: "No step repeats another step's question",
  rounding_taught:
    "Rounding the class is asked for is shown and practised first",
  question_shape:
    "Each question has one correct option, distinct options, its numbers in the stem and a misconception code for each wrong option",
  distinct_stems: "No two questions of an objective share a stem",
  scale_reached: "An objective that names a size is tested at that size",
  second_reading: "A second reader answered each question without its key",
  content_grounding: "No claim outside the passages (a model's reading)",
  internal_consistency: "No contradiction inside a section (a model's reading)",
  learner_facing_register: "Written for the learner (a model's reading)",
};

/** A check as a teacher reads it; a check this app does not know is shown by its own name. */
export function checkLabel(check: string): string {
  return CHECK_LABELS[check] ?? check.replaceAll("_", " ");
}

/**
 * The spec revision the note was written to: its generator's own when it has one, since a
 * plugin's spec is stored under the plugin, and the type's when the pipeline wrote it.
 */
export function specRevisionOf(item: ContentItem): number | undefined {
  return (
    item.provenance.generator?.spec_revision ??
    item.provenance.specification?.revision
  );
}

export type SectionCitations = {
  title: string;
  refs: string[];
};

type StoredStep = {
  title?: string | null;
  blocks?: { source_refs?: string[] }[];
};

/** The passages each section of a stored note cites, each reference once, in the note's order. */
export function sectionCitations(item: ContentItem): SectionCitations[] {
  const steps = (item.content as { steps?: StoredStep[] }).steps ?? [];
  return steps.map((step, index) => ({
    title: step.title?.trim() || `Section ${index + 1}`,
    refs: [
      ...new Set(
        (step.blocks ?? []).flatMap((block) => block.source_refs ?? []),
      ),
    ],
  }));
}

/** The recorded passage for a reference, when the record holds it. */
export function passageFor(record: ReviewRecord, ref: string) {
  return record.passages.find((passage) => passage.source_ref === ref);
}
