/** Which lesson a teacher page belongs to, as far as its address says. */
export type LessonRoute =
  | { kind: "lesson"; lessonPeriodId: string }
  | { kind: "plan"; planId: string }
  | { kind: "content"; contentId: string }
  | { kind: "pack"; artefactId: string }
  | { kind: "diagnostic"; planVersionId: string };

const ROUTES: [RegExp, (id: string) => LessonRoute][] = [
  [
    /^\/research\/teacher\/lessons\/([^/]+)/,
    (lessonPeriodId) => ({ kind: "lesson", lessonPeriodId }),
  ],
  // "new" and "manual" are the generator and the manual entry, which have no lesson yet.
  [
    /^\/research\/teacher\/lesson-plan\/(?!new$|manual)([^/]+)$/,
    (planId) => ({ kind: "plan", planId }),
  ],
  [
    /^\/research\/teacher\/content\/([^/]+)/,
    (contentId) => ({ kind: "content", contentId }),
  ],
  [
    /^\/research\/teacher\/pack-reviews\/([^/]+)/,
    (artefactId) => ({ kind: "pack", artefactId }),
  ],
  [
    /^\/research\/teacher\/diagnostics\/([^/]+)/,
    (planVersionId) => ({ kind: "diagnostic", planVersionId }),
  ],
];

export function lessonRouteOf(pathname: string): LessonRoute | null {
  for (const [pattern, make] of ROUTES) {
    const match = pattern.exec(pathname);
    if (match) return make(decodeURIComponent(match[1]));
  }
  return null;
}
