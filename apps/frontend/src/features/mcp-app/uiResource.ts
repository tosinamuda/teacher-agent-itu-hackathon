/** What a host needs from an MCP App's `ui://` resource: which one, and the page's security. */

export const MCP_APP_MIME = "text/html;profile=mcp-app";

/** The origins a view asks to reach, as its resource declares them. */
export type ViewCsp = {
  connectDomains?: string[];
  resourceDomains?: string[];
  frameDomains?: string[];
  baseUriDomains?: string[];
};

const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === "object" && value !== null && !Array.isArray(value);

/** The `ui://` resource a tool draws its result in, from the tool's metadata. */
export function viewUriOf(tool: { _meta?: Record<string, unknown> }): string | null {
  const meta = tool._meta;
  if (!meta) return null;
  const nested = isRecord(meta.ui) ? meta.ui.resourceUri : undefined;
  const uri = typeof nested === "string" ? nested : meta["ui/resourceUri"];
  return typeof uri === "string" && uri.startsWith("ui://") ? uri : null;
}

/** The view's declared origins, from its resource's metadata; none when it declares none. */
export function cspOf(meta: Record<string, unknown> | undefined): ViewCsp {
  const ui = meta && isRecord(meta.ui) ? meta.ui : undefined;
  const csp = ui && isRecord(ui.csp) ? ui.csp : {};
  const domains = (name: string): string[] | undefined => {
    const value = csp[name];
    return Array.isArray(value) ? value.filter((v): v is string => typeof v === "string") : undefined;
  };
  return {
    connectDomains: domains("connectDomains"),
    resourceDomains: domains("resourceDomains"),
    frameDomains: domains("frameDomains"),
    baseUriDomains: domains("baseUriDomains"),
  };
}

/** An origin, with a leading `*.` allowed; anything else could add a directive of its own. */
const ORIGIN = /^(https?|wss?):\/\/(\*\.)?[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*(:\d+)?$/;

const origins = (domains: string[] | undefined): string =>
  (domains ?? []).filter((domain) => ORIGIN.test(domain)).join(" ");

const sources = (...parts: string[]): string => parts.filter(Boolean).join(" ");

/**
 * The page's Content-Security-Policy: nothing is reachable but what its resource declares,
 * and the one inline script and style of the page itself run.
 */
export function contentSecurityPolicy(csp: ViewCsp): string {
  const resources = origins(csp.resourceDomains);
  return [
    "default-src 'none'",
    `script-src ${sources("'unsafe-inline'", resources)}`,
    `style-src ${sources("'unsafe-inline'", resources)}`,
    `img-src ${sources("data: blob:", resources)}`,
    `font-src ${sources("data:", resources)}`,
    `media-src ${sources("data: blob:", resources)}`,
    `connect-src ${sources(origins(csp.connectDomains)) || "'none'"}`,
    `frame-src ${sources(origins(csp.frameDomains)) || "'none'"}`,
    `base-uri ${sources(origins(csp.baseUriDomains)) || "'none'"}`,
    "form-action 'none'",
  ].join("; ");
}

/** The page as the frame loads it, with its policy first, before anything it could load. */
export function viewDocument(html: string, csp: ViewCsp): string {
  const meta = `<meta http-equiv="Content-Security-Policy" content="${contentSecurityPolicy(csp)}">`;
  const head = /<head[^>]*>/i.exec(html);
  if (!head) return `${meta}${html}`;
  const end = head.index + head[0].length;
  return `${html.slice(0, end)}${meta}${html.slice(end)}`;
}

/** Whether a view may ask the host to open an address: web pages only. */
export const isOpenableLink = (url: string): boolean => {
  try {
    const { protocol } = new URL(url);
    return protocol === "https:" || protocol === "http:";
  } catch {
    return false;
  }
};
