import { ContentSummary, ContentTypeSlug, ExpertSources } from "./types";

export type ContentStatus = {
  label: string;
  variant: "default" | "accent" | "success" | "warning";
};

export const NOT_CREATED: ContentStatus = {
  label: "Not created",
  variant: "default",
};

/**
 * A spec's audience as a teacher reads it. The stored spec names the reader by a
 * placeholder the server fills from the lesson's grade when it generates.
 */
export function audienceLine(audience: string): string {
  return audience.replaceAll("{reader}", "a learner");
}

/** The class-level content of a type for this lesson: the newest one, if any. */
export function currentContent(
  items: ContentSummary[],
  type: ContentTypeSlug,
): ContentSummary | undefined {
  return items.find((item) => item.type === type && item.level === "class");
}

/**
 * Where one type stands for a lesson. Approving a class test is sending it to students,
 * so its approved state reads as sent.
 */
export function contentStatus(item: ContentSummary | undefined): ContentStatus {
  if (!item) return NOT_CREATED;
  if (item.review_status === "rejected") {
    return { label: "Rejected", variant: "default" };
  }
  if (item.review_status !== "approved") {
    return { label: "Awaiting your review", variant: "warning" };
  }
  return item.type === "class-test"
    ? { label: "Sent to students", variant: "success" }
    : { label: "Approved", variant: "success" };
}

/** The choices of expert content a revision note can be grounded in, as a teacher reads them. */
export const EXPERT_SOURCES: { value: ExpertSources; label: string }[] = [
  { value: "lesson-note", label: "Your lesson note" },
  { value: "textbook", label: "The textbook" },
  { value: "both", label: "Both" },
];

/** What a revision note was grounded in, from its provenance; nothing where it records none. */
export function groundingLine(
  provenance: ContentSummary["provenance"],
): string | null {
  const { expert_sources: sources, lesson_note: note } = provenance;
  if (!sources) return null;
  if (sources === "textbook") return "Grounded in the textbook";
  if (!note)
    return "Grounded in the textbook: the lesson had no approved lesson note";
  const version = `lesson note version ${note.version}`;
  return sources === "both"
    ? `Grounded in ${version} and the textbook`
    : `Grounded in ${version}`;
}
