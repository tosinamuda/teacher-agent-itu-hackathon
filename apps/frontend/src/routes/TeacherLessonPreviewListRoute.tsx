import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";

import { ReviewBasePackButton } from "@/features/pack-review/components/ReviewBasePackButton";
import { apiFetch } from "@/shared/api/client";
import { Link } from "@/shared/router";

type PlanVersionSummary = {
  plan_id: string;
  version_id: string;
  session_id: string;
  subject: string;
  track: string;
  grade: string;
  term?: string | null;
  week?: number | null;
  day_index?: number | null;
  topic?: string | null;
  subtopic?: string | null;
  status: string;
  artefact_id?: string | null;
};

/** `/research/teacher/lesson-preview` — moved verbatim from the Next page
 *  module (route-layer component; composes pack-review + shared api). */
export function TeacherLessonPreviewListRoute() {
  const [subject, setSubject] = useState("");
  const [grade, setGrade] = useState("");
  const [term, setTerm] = useState("");
  const [week, setWeek] = useState("");
  const [pageIndex, setPageIndex] = useState(0);

  const track = useMemo(
    () => (subject ? (subject.includes("Further") ? "Further" : "General") : ""),
    [subject]
  );

  const planVersionsQuery = useQuery({
    queryKey: ["lessonPreviewPlanVersions", subject, term, week, grade, track],
    queryFn: () => {
      const params = new URLSearchParams();
      if (subject) params.set("subject", subject);
      if (track) params.set("track", track);
      if (grade) params.set("grade", grade);
      if (term) params.set("term", term);
      if (week) params.set("week", week);
      const query = params.toString();
      return apiFetch<PlanVersionSummary[]>(`/artefacts/lesson-plans${query ? `?${query}` : ""}`);
    },
  });

  const compiledVersions = useMemo(
    () => planVersionsQuery.data?.filter((version) => version.artefact_id) ?? [],
    [planVersionsQuery.data]
  );

  const pageSize = 8;
  const totalPages = Math.max(1, Math.ceil(compiledVersions.length / pageSize));
  const pageStart = pageIndex * pageSize;
  const pageRows = compiledVersions.slice(pageStart, pageStart + pageSize);

  return (
    <main className="page">
      <header className="generator__header animate-fade-up">
        <div>
          <div className="pill">Phase 2 · Lesson Preview</div>
          <h1>Preview compiled lesson steps.</h1>
          <p>Filter by grade, subject, term, or week to review a compiled pack.</p>
        </div>
      </header>

      <section className="panel animate-fade-up delay-1">
        <div className="panel__title">
          <h2>Compiled Lessons</h2>
          <span>Preview a compiled pack for the selected filters.</span>
        </div>
        <div className="flex flex-col rounded-2xl border border-dashed border-(--line) bg-(--surface) p-4">
          <div className="text-xs font-semibold uppercase tracking-[0.18em] text-(--muted)">
            Filters
          </div>
          <div className="grid gap-3 lg:grid-cols-4">
            <div className="field">
              <label>Class</label>
              <select
                value={grade}
                onChange={(event) => {
                  setGrade(event.target.value);
                  setPageIndex(0);
                }}
              >
                <option value="">All grades</option>
                <option value="SS1">SS1</option>
              </select>
            </div>
            <div className="field">
              <label>Subject</label>
              <select
                value={subject}
                onChange={(event) => {
                  setSubject(event.target.value);
                  setPageIndex(0);
                }}
              >
                <option value="">All subjects</option>
                <option value="Mathematics (General)">Mathematics (General)</option>
                <option value="Mathematics (Further)">Mathematics (Further)</option>
              </select>
            </div>
            <div className="field">
              <label>Term</label>
              <select
                value={term}
                onChange={(event) => {
                  setTerm(event.target.value);
                  setPageIndex(0);
                }}
              >
                <option value="">All terms</option>
                <option value="First Term">First Term</option>
                <option value="Second Term">Second Term</option>
                <option value="Third Term">Third Term</option>
              </select>
            </div>
            <div className="field">
              <label>Week</label>
              <select
                value={week}
                onChange={(event) => {
                  setWeek(event.target.value);
                  setPageIndex(0);
                }}
              >
                <option value="">All weeks</option>
                {Array.from({ length: 13 }, (_, index) => (
                  <option key={index + 1} value={String(index + 1)}>
                    Week {index + 1}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
        {planVersionsQuery.isLoading && <p className="hint">Loading packs…</p>}
        {planVersionsQuery.isError && <p className="hint error">Failed to load packs.</p>}
        {!planVersionsQuery.isLoading && compiledVersions.length === 0 && (
          <div className="empty-state">
            <h3>No compiled packs yet.</h3>
            <p>Compile a pack in Lesson Plan to preview it here.</p>
          </div>
        )}
        {pageRows.length > 0 && (
          <div className="overflow-x-auto">
            <table className="w-full border-separate border-spacing-y-3 text-left text-sm">
              <thead className="text-(--muted)">
                <tr>
                  <th className="px-4">Lesson</th>
                  <th className="px-4">Week/Day</th>
                  <th className="px-4">Status</th>
                  <th className="px-4">Pack</th>
                  <th className="px-4">Action</th>
                </tr>
              </thead>
              <tbody>
                {pageRows.map((version) => (
                  <tr
                    key={version.version_id}
                    className="rounded-2xl bg-(--surface)"
                  >
                    <td className="px-4 py-3">
                      <div className="font-semibold">
                        {version.subtopic ?? version.session_id}
                      </div>
                      <div className="text-xs text-(--muted)">
                        {version.topic ?? "Lesson"}
                      </div>
                    </td>
                    <td className="px-4 py-3 text-sm text-(--muted)">
                      Week {version.week ?? "?"} · Day {version.day_index ?? "?"}
                    </td>
                    <td className="px-4 py-3">
                      <span className={`status-pill ${version.status}`}>
                        {version.status.toUpperCase()}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm text-(--muted)">
                      {version.artefact_id ?? "—"}
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex flex-wrap items-center gap-2">
                        {version.artefact_id && (
                          <Link
                            className="btn btn--ghost"
                            href={`/research/teacher/lesson-preview/${version.artefact_id}`}
                          >
                            Preview
                          </Link>
                        )}
                        <ReviewBasePackButton planVersionId={version.version_id} />
                        <Link
                          className="btn btn--ghost"
                          href={`/research/teacher/diagnostics/${version.version_id}`}
                        >
                          Review assessment
                        </Link>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        {compiledVersions.length > pageSize && (
          <div className="mt-4 flex flex-wrap items-center justify-between gap-3 text-sm">
            <span className="text-(--muted)">
              Page {pageIndex + 1} of {totalPages}
            </span>
            <div className="flex items-center gap-2">
              <button
                type="button"
                className="btn btn--ghost"
                onClick={() => setPageIndex((prev) => Math.max(prev - 1, 0))}
                disabled={pageIndex === 0}
              >
                Previous
              </button>
              <button
                type="button"
                className="btn btn--ghost"
                onClick={() => setPageIndex((prev) => Math.min(prev + 1, totalPages - 1))}
                disabled={pageIndex >= totalPages - 1}
              >
                Next
              </button>
            </div>
          </div>
        )}
      </section>
    </main>
  );
}
