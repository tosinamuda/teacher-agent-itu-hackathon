import { apiFetch } from "@/shared/api/client";

import {
  LessonResults,
  RaterSchedule,
  StudyInstrument,
  StudyRatings,
  StudyRatingsTally,
  StudyWideResults,
} from "./types";

/** Every study rating of one revision note. */
export const getStudyRatings = (noteId: string): Promise<StudyRatings> =>
  apiFetch<StudyRatings>(`/evaluation/study-ratings?note=${encodeURIComponent(noteId)}`);

/** How many study ratings each lesson's notes hold; a lesson with none is left out. */
export const getStudyRatingsTally = (planVersionIds: string[]): Promise<StudyRatingsTally[]> =>
  apiFetch<StudyRatingsTally[]>(
    `/evaluation/study-ratings/tally?${planVersionIds
      .map((id) => `plan_version_id=${encodeURIComponent(id)}`)
      .join("&")}`
  );

/** Who rated the experiment's lesson in the study, set by set, and which lessons Part 2 compared. */
export const getStudyRaterSchedule = (experimentId: string): Promise<RaterSchedule> =>
  apiFetch<RaterSchedule>(`/experiments/${encodeURIComponent(experimentId)}/rater-schedule`);

/** The lesson's study ratings described: Part 1 means by condition, Part 2 choices counted. */
export const getStudyLessonResults = (experimentId: string): Promise<LessonResults> =>
  apiFetch<LessonResults>(`/experiments/${encodeURIComponent(experimentId)}/study-results`);

/** A study's ratings across its lessons, described, with each objective as a data point. */
export const getStudyWideResults = (investigationId: string): Promise<StudyWideResults> =>
  apiFetch<StudyWideResults>(
    `/experiments/investigations/${encodeURIComponent(investigationId)}/study-results`
  );

/** The rating instrument the study's raters used. */
export const getStudyInstrument = (): Promise<StudyInstrument> =>
  apiFetch<StudyInstrument>("/evaluation/study-ratings/instrument");
