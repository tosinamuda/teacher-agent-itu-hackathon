import { apiFetch } from "./client";

/** A source textbook chunk, fetched on demand when a reference is opened. */
export type TextbookRecord = {
  record_id: string;
  record_type: string;
  chapter_id: string | null;
  chapter_title: string | null;
  heading: string | null;
  content: string;
  source_html_path: string | null;
  source_anchor_id: string | null;
};

/** Fetches one source textbook record's content by its record id (e.g. ch02-b005). */
export const getTextbookRecord = (recordId: string): Promise<TextbookRecord> =>
  apiFetch<TextbookRecord>(`/artefacts/textbook-records/${encodeURIComponent(recordId)}`);
