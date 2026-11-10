import { beforeEach, describe, expect, it, vi } from "vitest";

import { connectMcp } from "./mcpClient";
import { loadView } from "./useMcpView";

vi.mock("./mcpClient", () => ({ connectMcp: vi.fn() }));

type FakeClient = {
  listTools: ReturnType<typeof vi.fn>;
  readResource: ReturnType<typeof vi.fn>;
  callTool: ReturnType<typeof vi.fn>;
  close: ReturnType<typeof vi.fn>;
};

const URI = "ui://content/viewer.html";
const PAGE = {
  contents: [
    {
      uri: URI,
      mimeType: "text/html;profile=mcp-app",
      text: "<html></html>",
      _meta: { ui: { csp: { resourceDomains: ["https://cdn.jsdelivr.net"] } } },
    },
  ],
};

function server(overrides: Partial<FakeClient> = {}): FakeClient {
  const client: FakeClient = {
    listTools: vi.fn().mockResolvedValue({
      tools: [{ name: "show_content", _meta: { ui: { resourceUri: URI } } }],
    }),
    readResource: vi.fn().mockResolvedValue(PAGE),
    callTool: vi.fn().mockResolvedValue({ content: [{ type: "text", text: "{}" }] }),
    close: vi.fn().mockResolvedValue(undefined),
    ...overrides,
  };
  vi.mocked(connectMcp).mockResolvedValue(client as never);
  return client;
}

beforeEach(() => vi.mocked(connectMcp).mockReset());

describe("loadView", () => {
  it("reads the page the tool is bound to and the tool's result, and keeps the connection", async () => {
    const client = server();

    const state = await loadView("show_content", { content_id: "c1" });

    expect(state.status).toBe("ready");
    if (state.status !== "ready") return;
    expect(state.view.html).toBe("<html></html>");
    expect(state.view.csp.resourceDomains).toEqual(["https://cdn.jsdelivr.net"]);
    expect(state.view.input).toEqual({ content_id: "c1" });
    expect(client.callTool).toHaveBeenCalledWith({
      name: "show_content",
      arguments: { content_id: "c1" },
    });
    expect(client.close).not.toHaveBeenCalled();
  });

  it("is none, and closes, when the server has no tool of that name or the tool has no page", async () => {
    const missing = server({ listTools: vi.fn().mockResolvedValue({ tools: [] }) });
    expect((await loadView("show_content", {})).status).toBe("none");
    expect(missing.close).toHaveBeenCalled();

    const unbound = server({
      listTools: vi.fn().mockResolvedValue({ tools: [{ name: "show_content" }] }),
    });
    expect((await loadView("show_content", {})).status).toBe("none");
    expect(unbound.close).toHaveBeenCalled();
  });

  it("is none for a page that is not an MCP App", async () => {
    const client = server({
      readResource: vi.fn().mockResolvedValue({
        contents: [{ uri: URI, mimeType: "text/plain", text: "hello" }],
      }),
    });

    expect((await loadView("show_content", {})).status).toBe("none");
    expect(client.close).toHaveBeenCalled();
    expect(client.callTool).not.toHaveBeenCalled();
  });

  it("fails, and closes, when the tool refuses the request", async () => {
    const client = server({
      callTool: vi.fn().mockResolvedValue({ isError: true, content: [] }),
    });

    await expect(loadView("show_content", { content_id: "c1" })).rejects.toThrow("refused");
    expect(client.close).toHaveBeenCalled();
  });
});
