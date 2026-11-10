/**
 * A distractor's snake_case misconception code as prose: "missing_factor_of_two" reads
 * "Missing factor of two". Distractors carry only the code; no description is written for it.
 */
export function humaniseMisconceptionCode(code: string): string {
  const prose = code.replaceAll("_", " ").trim();
  return prose.charAt(0).toUpperCase() + prose.slice(1);
}
