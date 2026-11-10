import { Outlet } from "react-router";

import { TeachingWorkspaceProvider } from "@/features/teaching-workspace/context/TeachingWorkspaceContext";
import { AppHeader } from "@/shared/components/layouts/AppHeader";
import { QueryProvider } from "@/shared/providers/QueryProvider";

/** App frame for every route — providers + header (was Next's root layout). */
export function RootLayout() {
  return (
    <QueryProvider>
      <TeachingWorkspaceProvider>
        <div className="flex min-h-screen flex-col">
          <AppHeader />
          <div className="flex-1">
            <Outlet />
          </div>
        </div>
      </TeachingWorkspaceProvider>
    </QueryProvider>
  );
}
