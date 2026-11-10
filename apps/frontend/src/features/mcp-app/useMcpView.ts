import type { CallToolResult, Client } from "@modelcontextprotocol/client";
import { useEffect, useState } from "react";

import { connectMcp } from "./mcpClient";
import { MCP_APP_MIME, ViewCsp, cspOf, viewUriOf } from "./uiResource";

/** A tool's `ui://` page, with the result it draws and the connection that served them. */
export type LoadedView = {
  client: Client;
  html: string;
  csp: ViewCsp;
  input: Record<string, unknown>;
  result: CallToolResult;
};

export type McpViewState =
  | { status: "loading" }
  | { status: "ready"; view: LoadedView }
  /** The server has no view for the tool: nothing went wrong. */
  | { status: "none" }
  | { status: "error"; message: string };

export async function loadView(tool: string, input: Record<string, unknown>): Promise<McpViewState> {
  const client = await connectMcp();
  try {
    const found = (await client.listTools()).tools.find((candidate) => candidate.name === tool);
    const uri = found ? viewUriOf(found) : null;
    if (!uri) {
      await client.close();
      return { status: "none" };
    }
    const page = (await client.readResource({ uri })).contents[0];
    if (!page || !("text" in page) || page.mimeType !== MCP_APP_MIME) {
      await client.close();
      return { status: "none" };
    }
    const result = await client.callTool({ name: tool, arguments: input });
    if (result.isError) throw new Error(`${tool} refused the request`);
    return {
      status: "ready",
      view: { client, html: page.text, csp: cspOf(page._meta), input, result },
    };
  } catch (error) {
    await client.close().catch(() => undefined);
    throw error;
  }
}

/** Loads the page a tool of the MCP server draws its result in, and its result. */
export function useMcpView(tool: string, input: Record<string, unknown>): McpViewState {
  const [state, setState] = useState<McpViewState>({ status: "loading" });
  const key = JSON.stringify(input);

  useEffect(() => {
    let current = true;
    let loaded: LoadedView | null = null;
    setState({ status: "loading" });
    loadView(tool, JSON.parse(key) as Record<string, unknown>)
      .then((next) => {
        if (next.status === "ready") loaded = next.view;
        if (current) setState(next);
        else void loaded?.client.close();
      })
      .catch((error: unknown) => {
        if (current) setState({ status: "error", message: String(error) });
      });
    return () => {
      current = false;
      void loaded?.client.close();
    };
  }, [tool, key]);

  return state;
}
