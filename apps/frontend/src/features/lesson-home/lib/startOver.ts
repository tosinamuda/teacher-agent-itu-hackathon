const LABELS: [table: string, one: string, many: string][] = [
  ["plan_versions", "plan", "plans"],
  ["artefacts", "material", "materials"],
  ["exit_ticket_submissions", "learner's results", "learners' results"],
  ["study_classwork_scripts", "imported marked script", "imported marked scripts"],
];

/** The rows to be cleared, in words a teacher reads: "1 plan, 7 materials, 3 learners' results". */
export function summariseStartOver(counts: Record<string, number>): string {
  return LABELS.flatMap(([table, one, many]) => {
    const count = counts[table] ?? 0;
    return count > 0 ? [`${count} ${count === 1 ? one : many}`] : [];
  }).join(", ");
}
