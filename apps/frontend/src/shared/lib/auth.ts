const TOKEN_KEY = "teacher_code";
export const TEACHER_AUTH_CHANGED_EVENT = "teacher-auth-changed";

const notifyTeacherAuthChanged = () => {
  if (typeof window === "undefined") return;
  window.dispatchEvent(new Event(TEACHER_AUTH_CHANGED_EVENT));
};

export const getAuthCode = (): string | null => {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
};

export const setAuthCode = (code: string) => {
  localStorage.setItem(TOKEN_KEY, code);
  notifyTeacherAuthChanged();
};

export const clearAuthCode = () => {
  localStorage.removeItem(TOKEN_KEY);
  notifyTeacherAuthChanged();
};
