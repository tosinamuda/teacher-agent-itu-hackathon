/**
 * The class a teacher last opened, kept in the browser so the app opens into it. It is kept per
 * access code, so two teachers on one browser each get their own.
 */
const keyOf = (teacherCode: string) => `teaching.lastWorkspace.${teacherCode}`;

export function readLastWorkspace(teacherCode: string | null): string | null {
  if (!teacherCode) return null;
  try {
    return window.localStorage.getItem(keyOf(teacherCode));
  } catch {
    return null;
  }
}

export function rememberWorkspace(
  teacherCode: string | null,
  workspaceId: string,
): void {
  if (!teacherCode) return;
  try {
    window.localStorage.setItem(keyOf(teacherCode), workspaceId);
  } catch {
    // A browser that will not keep it just opens into the primary class next time.
  }
}
