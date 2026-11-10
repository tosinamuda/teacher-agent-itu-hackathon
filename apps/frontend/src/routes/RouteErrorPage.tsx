import { useEffect } from "react";
import { isRouteErrorResponse, useLocation, useRouteError } from "react-router";

import { Button } from "@/shared/components/ui/Button";

import { reloadIfStale } from "./staleBundle";

const CONTENT_PAGE = /^\/research\/teacher\/content\/[^/]+/;

function lessonPagePath(pathname: string): string {
  return pathname.match(CONTENT_PAGE)?.[0] ?? "/research";
}

function technicalMessage(error: unknown): string {
  if (isRouteErrorResponse(error)) return `${error.status} ${error.statusText}`;
  return error instanceof Error ? error.message : String(error);
}

/** Root `errorElement`: a plain-language page for any unhandled render or loader error. */
export function RouteErrorPage() {
  const error = useRouteError();
  const { pathname } = useLocation();

  useEffect(() => {
    void reloadIfStale(error);
  }, [error]);

  return (
    <main className="mx-auto max-w-md px-4 py-20 text-sm text-(--muted)">
      <h1 className="mb-2 text-lg font-semibold text-(--ink)">Something went wrong on this page</h1>
      <p className="mb-6">Reload to get the latest version.</p>
      <div className="mb-8 flex items-center gap-4">
        <Button onClick={() => window.location.reload()}>Reload</Button>
        <a className="font-semibold text-(--accent-deep) underline" href={lessonPagePath(pathname)}>
          Back to the lesson page
        </a>
      </div>
      <details>
        <summary className="cursor-pointer text-xs font-semibold text-(--muted)">Details</summary>
        <pre className="mt-2 overflow-x-auto whitespace-pre-wrap border border-(--line) bg-(--sunken) p-3 font-mono text-xs text-(--ink)">
          {technicalMessage(error)}
        </pre>
      </details>
    </main>
  );
}
