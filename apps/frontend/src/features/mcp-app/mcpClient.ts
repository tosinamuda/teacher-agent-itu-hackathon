import { Client, StreamableHTTPClientTransport } from "@modelcontextprotocol/client";

import { API_BASE_URL } from "@/shared/api/client";
import { getAuthCode } from "@/shared/lib/auth";

/** Where the API serves the content engine's MCP server. */
export const MCP_PATH = "/mcp";

/** A client of the API's MCP server, signed in with the teacher's access code. */
export async function connectMcp(): Promise<Client> {
  const code = getAuthCode();
  const transport = new StreamableHTTPClientTransport(new URL(`${API_BASE_URL}${MCP_PATH}`), {
    requestInit: { headers: code ? { "x-teacher-code": code } : {} },
  });
  const client = new Client({ name: "plan-to-tutor-web", version: "1" });
  await client.connect(transport);
  return client;
}
