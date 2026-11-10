import {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import { apiFetch } from "@/shared/api/client";
import { clearAuthCode } from "@/shared/lib/auth";
import { useRefreshAuthMe } from "@/shared/hooks/useAuthMe";
import { LearnerProfile } from "@/features/learners/types";

interface StudentContextType {
  studentId: string | null;
  student: LearnerProfile | null;
  isLoading: boolean;
  error: string | null;
  login: (code: string) => Promise<void>;
  logout: () => void;
}

const StudentContext = createContext<StudentContextType | undefined>(undefined);

/** The slice of /auth/me the portal needs: the signed-in student binding. */
type AuthMeSlice = { role: string; student_id: string | null };

export function StudentProvider({ children }: { children: ReactNode }) {
  const refreshAuthMe = useRefreshAuthMe();
  const [studentId, setStudentId] = useState<string | null>(null);
  const [student, setStudent] = useState<LearnerProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Restore session. A signed-in STUDENT is always bound to their own learner
  // profile (identity comes from auth — submissions are attributed server-side
  // to the signed-in user, so letting them "act as" another learner would only
  // misattribute their work). The stored-id fallback remains for non-student
  // roles previewing the portal.
  useEffect(() => {
    const restore = async () => {
      try {
        const me = await apiFetch<AuthMeSlice>("/auth/me");
        if (me.role === "student" && me.student_id) {
          await verifyStudent(me.student_id);
          return;
        }
      } catch {
        // Not signed in / auth unavailable — fall through to the stored id.
      }
      const storedId = localStorage.getItem("plan_to_tutor_student_id");
      if (storedId) {
        verifyStudent(storedId);
      } else {
        setIsLoading(false);
      }
    };
    void restore();
  }, []);

  const verifyStudent = async (id: string) => {
    setIsLoading(true);
    setError(null);
    try {
      // Use existing endpoint to verify and fetch profile
      const profile = await apiFetch<LearnerProfile>(
        `/learners/${id}`
      );
      setStudent(profile);
      setStudentId(profile.student_id);
      localStorage.setItem("plan_to_tutor_student_id", profile.student_id);
    } catch (err) {
      console.error(err);
      setError("Invalid student code or network error.");
      localStorage.removeItem("plan_to_tutor_student_id");
      setStudentId(null);
      setStudent(null);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (code: string) => {
    try {
      const me = await apiFetch<AuthMeSlice>("/auth/me");
      if (me.role === "student" && me.student_id) {
        // A signed-in student can only ever open their OWN workspace —
        // whatever code they type, bind to the authenticated profile.
        await verifyStudent(me.student_id);
        return;
      }
    } catch {
      // Not signed in / auth unavailable — verify the typed code directly.
    }
    await verifyStudent(code);
  };

  // Logging out must end the AUTH session too, not just the portal binding.
  // Clearing only the stored student id left the previous student signed in,
  // and `login()` force-binds whoever types next to the authenticated profile
  // — on a shared classroom device the second student would land inside the
  // first student's workspace.
  const logout = () => {
    localStorage.removeItem("plan_to_tutor_student_id");
    clearAuthCode();
    refreshAuthMe();
    setStudentId(null);
    setStudent(null);
    setError(null);
  };

  return (
    <StudentContext.Provider
      value={{
        studentId,
        student,
        isLoading,
        error,
        login,
        logout,
      }}
    >
      {children}
    </StudentContext.Provider>
  );
}

export function useStudentAuth() {
  const context = useContext(StudentContext);
  if (context === undefined) {
    throw new Error("useStudentAuth must be used within a StudentProvider");
  }
  return context;
}
