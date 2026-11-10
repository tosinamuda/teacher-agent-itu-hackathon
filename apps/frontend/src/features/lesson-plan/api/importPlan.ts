import type { JobAccepted } from "@/shared/api/jobs";
import { postForm } from "@/shared/api/multipart";

/** What a plan import leaves behind: the draft plan version, and how it follows the document. */
export type ImportedPlan = { plan_version_id: string; summary: string };

/** The document types the server reads. */
export const READABLE_DOCUMENTS = ".txt,.md,.docx,.pdf";

/**
 * Queue writing the lesson's plan from a teacher's document: its pasted text or its file.
 * With an experiment, the plan becomes that experiment's plan.
 */
export function importPlanFromDocument(
  sessionId: string,
  document: { text?: string; file?: File },
  experimentId?: string,
): Promise<JobAccepted> {
  const form = new FormData();
  form.append("session_id", sessionId);
  if (document.text) form.append("text", document.text);
  if (document.file) form.append("file", document.file);
  if (experimentId) form.append("experiment_id", experimentId);
  return postForm<JobAccepted>("/plan-imports", form);
}
