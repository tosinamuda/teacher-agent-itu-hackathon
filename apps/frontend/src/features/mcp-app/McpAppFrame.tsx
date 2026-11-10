import {
  AppBridge,
  McpUiStyleVariableKey,
  McpUiStyles,
  PostMessageTransport,
} from "@modelcontextprotocol/ext-apps/app-bridge";
import { useEffect, useRef, useState } from "react";

import type { LoadedView } from "./useMcpView";
import { isOpenableLink, viewDocument } from "./uiResource";
import { commentFromMessage, deliverComment } from "./viewMessage";

const HOST = { name: "plan-to-tutor-web", version: "1" };
const FIRST_HEIGHT = 160;

/** The app's own tokens, under the names an MCP App reads, so the view matches the page. */
const STYLE_VARIABLES: Partial<Record<McpUiStyleVariableKey, string>> = {
  "--color-background-primary": "--surface",
  "--color-background-secondary": "--sunken",
  "--color-text-primary": "--ink",
  "--color-text-secondary": "--ink-2",
  "--color-border-primary": "--line",
  "--color-text-info": "--accent-deep",
  "--color-text-success": "--success-ink",
  "--font-sans": "--font-body",
};

function hostStyles(): McpUiStyles {
  const root = getComputedStyle(document.documentElement);
  const variables: Partial<McpUiStyles> = {};
  for (const [name, source] of Object.entries(STYLE_VARIABLES)) {
    const value = root.getPropertyValue(source).trim();
    if (value) variables[name as McpUiStyleVariableKey] = value;
  }
  // A variable the app does not set is absent, which a view reads as undefined.
  return variables as McpUiStyles;
}

/**
 * An MCP App's page in a frame of its own: it runs with no access to this page, talks to it
 * only over postMessage, and is given the result it draws once it has started.
 */
export function McpAppFrame({ view, revision }: { view: LoadedView; revision: string }) {
  const frame = useRef<HTMLIFrameElement>(null);
  const bridgeRef = useRef<AppBridge | null>(null);
  const [height, setHeight] = useState(FIRST_HEIGHT);
  const [shown, setShown] = useState(false);

  useEffect(() => {
    const iframe = frame.current;
    const target = iframe?.contentWindow;
    if (!iframe || !target) return;
    let live = true;
    let started = false;
    // No client is given, so the bridge does not pass the view's own tool or resource requests on
    // to the server as the teacher: a view can ask the host only for what the host handles below.
    const bridge = new AppBridge(
      null,
      HOST,
      { openLinks: {}, message: { text: {} } },
      { hostContext: { theme: "light", displayMode: "inline", styles: { variables: hostStyles() } } }
    );
    bridge.oninitialized = () => {
      started = true;
      void bridge.sendToolInput({ arguments: view.input });
      void bridge.sendToolResult(view.result).then(() => live && setShown(true));
    };
    // A comment the view sends is the teacher's own message: the chat of this content takes it,
    // shows it, and answers it, as it does a message typed there.
    bridge.onmessage = async (params) => {
      const comment = commentFromMessage(params, view.input.content_id);
      return comment && deliverComment(comment) ? {} : { isError: true };
    };
    bridge.onsizechange = ({ height: next }) => {
      if (next && live) setHeight(Math.ceil(next));
    };
    bridge.onopenlink = async ({ url }) => {
      if (!isOpenableLink(url)) return { isError: true };
      window.open(url, "_blank", "noopener,noreferrer");
      return {};
    };
    // The listener is attached before the page is loaded, so its first message is heard.
    bridgeRef.current = bridge;
    void bridge.connect(new PostMessageTransport(target, target)).then(() => {
      if (live) iframe.srcdoc = viewDocument(view.html, view.csp);
    });
    return () => {
      live = false;
      bridgeRef.current = null;
      // A view that has started is told it is going before the bridge stops listening; one that
      // has not started has nothing to tell.
      if (!started) {
        void bridge.close();
        return;
      }
      void bridge
        .teardownResource({})
        .catch(() => undefined)
        .finally(() => bridge.close());
    };
  }, [view]);

  // The page draws what is on the server again when the item's version or status changes.
  const drawn = useRef(revision);
  useEffect(() => {
    const bridge = bridgeRef.current;
    if (drawn.current === revision || !bridge || !shown) return;
    drawn.current = revision;
    void view.client
      .callTool({ name: "show_content", arguments: view.input })
      .then((result) => bridge.sendToolResult(result))
      .catch(() => undefined);
  }, [revision, shown, view]);

  return (
    <div className="relative">
      {shown ? null : (
        <p className="absolute left-0 top-0 text-sm text-(--muted)" data-mcp-view-loading>
          Loading…
        </p>
      )}
      <iframe
        ref={frame}
        title="Content"
        sandbox="allow-scripts"
        data-mcp-view={shown ? "ready" : "starting"}
        style={{ height, width: "100%", border: 0, display: "block" }}
      />
    </div>
  );
}
