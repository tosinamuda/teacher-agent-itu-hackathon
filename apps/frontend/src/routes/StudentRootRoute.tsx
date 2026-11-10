import { StudentProvider, useStudentAuth } from "@/features/student/context/StudentContext";
import StudentLoginPage from "@/features/student/pages/StudentLoginPage";
import StudentWorkspacePage from "@/features/student/pages/StudentWorkspacePage";

function StudentRoot() {
  const { student, isLoading } = useStudentAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-(--sunken)">
        <div className="text-muted-foreground animate-pulse">Loading...</div>
      </div>
    );
  }

  if (!student) {
    return <StudentLoginPage />;
  }

  return <StudentWorkspacePage />;
}

/** `/research/student` — portal login until a learner binding resolves. */
export function StudentRootRoute() {
  return (
    <StudentProvider>
      <StudentRoot />
    </StudentProvider>
  );
}
