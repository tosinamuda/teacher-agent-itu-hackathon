import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "@/shared/api/client";
import { getAuthCode, TEACHER_AUTH_CHANGED_EVENT } from "@/shared/lib/auth";
import type { TeachingWorkspace } from "@/features/teaching-workspace/types";
import { readLastWorkspace, rememberWorkspace } from "../lib/lastClass";

interface TeachingWorkspaceContextType {
  workspaces: TeachingWorkspace[];
  currentWorkspace: TeachingWorkspace | null;
  teacherId: string | null;
  setWorkspace: (workspace: TeachingWorkspace) => void;
  isLoading: boolean;
}

const TeachingWorkspaceContext = createContext<
  TeachingWorkspaceContextType | undefined
>(undefined);

export function TeachingWorkspaceProvider({
  children,
}: {
  children: ReactNode;
}) {
  const [teacherCode, setTeacherCode] = useState<string | null>(null);
  const [isTeacherCodeReady, setIsTeacherCodeReady] = useState(false);
  const [selectedWorkspaceId, setSelectedWorkspaceId] = useState<string | null>(
    null,
  );

  useEffect(() => {
    const syncTeacherCode = () => {
      setTeacherCode(getAuthCode());
      setIsTeacherCodeReady(true);
    };

    syncTeacherCode();
    window.addEventListener("storage", syncTeacherCode);
    window.addEventListener(
      TEACHER_AUTH_CHANGED_EVENT,
      syncTeacherCode as EventListener,
    );

    return () => {
      window.removeEventListener("storage", syncTeacherCode);
      window.removeEventListener(
        TEACHER_AUTH_CHANGED_EVENT,
        syncTeacherCode as EventListener,
      );
    };
  }, []);

  // Open into the class this teacher last used; the primary class when there is none.
  useEffect(() => {
    setSelectedWorkspaceId(readLastWorkspace(teacherCode));
  }, [teacherCode]);

  const { data: workspaces = [], isLoading } = useQuery({
    queryKey: ["teaching", "workspaces", teacherCode],
    queryFn: () => apiFetch<TeachingWorkspace[]>("/teaching/workspaces"),
    enabled: isTeacherCodeReady && Boolean(teacherCode),
  });

  const currentWorkspace = useMemo(
    () =>
      workspaces.find((workspace) => workspace.id === selectedWorkspaceId) ||
      workspaces.find((workspace) => workspace.is_primary) ||
      workspaces[0] ||
      null,
    [selectedWorkspaceId, workspaces],
  );

  const teacherId = currentWorkspace?.teacher_id || null;

  const setWorkspace = (workspace: TeachingWorkspace) => {
    setSelectedWorkspaceId(workspace.id);
    rememberWorkspace(teacherCode, workspace.id);
  };

  return (
    <TeachingWorkspaceContext.Provider
      value={{
        workspaces,
        currentWorkspace,
        teacherId,
        setWorkspace,
        isLoading: isLoading || !isTeacherCodeReady,
      }}
    >
      {children}
    </TeachingWorkspaceContext.Provider>
  );
}

export function useTeachingWorkspace() {
  const context = useContext(TeachingWorkspaceContext);
  if (context === undefined) {
    throw new Error(
      "useTeachingWorkspace must be used within a TeachingWorkspaceProvider",
    );
  }
  return context;
}
