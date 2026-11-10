import type { ReactNode } from "react";

import { McpAppFrame } from "./McpAppFrame";
import { useMcpView } from "./useMcpView";

/**
 * What an MCP server draws for a tool's result, in the page. The server's own page is used
 * when it has one; ``fallback`` is the page's own drawing for a server that has none, or
 * that could not be reached. ``revision`` names the state of what is shown: the page is given
 * what is on the server again, in place, when it changes.
 */
export function McpAppView({
  tool,
  input,
  revision,
  fallback,
}: {
  tool: string;
  input: Record<string, unknown>;
  revision: string;
  fallback: ReactNode;
}) {
  const state = useMcpView(tool, input);

  if (state.status === "ready") return <McpAppFrame view={state.view} revision={revision} />;
  if (state.status === "loading") {
    return (
      <p data-mcp-view="loading" className="text-sm text-(--muted)">
        Loading…
      </p>
    );
  }
  return (
    <div data-mcp-view={state.status === "none" ? "none" : "failed"}>
      {state.status === "error" ? (
        <p className="mb-3 text-xs text-(--muted)">
          The server&apos;s view could not be shown, so this is the app&apos;s own.
        </p>
      ) : null}
      {fallback}
    </div>
  );
}
