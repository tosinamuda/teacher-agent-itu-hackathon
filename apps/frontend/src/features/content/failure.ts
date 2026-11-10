const QUOTED = /'((?:[^'\\]|\\.)*)'|"((?:[^"\\]|\\.)*)"/g;

/**
 * A failed generation's reason as a teacher reads it. The server reports the checks the agent
 * left unfixed as a list; the first is said, and how many more there are.
 */
export function failureLine(error: string): string {
  const left = /^the writer left issues: \[([\s\S]*)\]$/.exec(error.trim());
  const issues = left
    ? [...left[1].matchAll(QUOTED)].map((found) => found[1] ?? found[2])
    : [];
  if (issues.length === 0) return error;
  const more = issues.length > 1 ? ` (and ${issues.length - 1} more)` : "";
  return `The checks still found: ${issues[0]}${more}`;
}
