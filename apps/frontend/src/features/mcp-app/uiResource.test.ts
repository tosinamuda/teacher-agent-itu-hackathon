import { describe, expect, it } from "vitest";

import {
  contentSecurityPolicy,
  cspOf,
  isOpenableLink,
  viewDocument,
  viewUriOf,
} from "./uiResource";

describe("viewUriOf", () => {
  it("reads the resource a tool draws in, nested or flat", () => {
    expect(viewUriOf({ _meta: { ui: { resourceUri: "ui://content/viewer.html" } } })).toBe(
      "ui://content/viewer.html"
    );
    expect(viewUriOf({ _meta: { "ui/resourceUri": "ui://content/viewer.html" } })).toBe(
      "ui://content/viewer.html"
    );
  });

  it("is none for a tool with no view, or a resource that is not ui://", () => {
    expect(viewUriOf({})).toBeNull();
    expect(viewUriOf({ _meta: { ui: {} } })).toBeNull();
    expect(viewUriOf({ _meta: { ui: { resourceUri: "https://example.org/x.html" } } })).toBeNull();
  });
});

describe("cspOf", () => {
  it("reads the declared origins", () => {
    const meta = { ui: { csp: { resourceDomains: ["https://cdn.jsdelivr.net"] } } };

    expect(cspOf(meta).resourceDomains).toEqual(["https://cdn.jsdelivr.net"]);
    expect(cspOf(meta).connectDomains).toBeUndefined();
    expect(cspOf(undefined)).toEqual({
      connectDomains: undefined,
      resourceDomains: undefined,
      frameDomains: undefined,
      baseUriDomains: undefined,
    });
  });
});

describe("contentSecurityPolicy", () => {
  it("reaches nothing but what the view declares", () => {
    const policy = contentSecurityPolicy({ resourceDomains: ["https://cdn.jsdelivr.net"] });

    expect(policy).toContain("default-src 'none'");
    expect(policy).toContain("script-src 'unsafe-inline' https://cdn.jsdelivr.net");
    expect(policy).toContain("style-src 'unsafe-inline' https://cdn.jsdelivr.net");
    expect(policy).toContain("connect-src 'none'");
    expect(policy).toContain("frame-src 'none'");
    expect(policy).toContain("base-uri 'none'");
    expect(policy).toContain("form-action 'none'");
  });

  it("drops an origin that is not one, so a declaration cannot add a directive", () => {
    const policy = contentSecurityPolicy({
      connectDomains: ["https://api.example.org", "https://x.org; script-src *", "javascript:alert(1)"],
    });

    expect(policy).toContain("connect-src https://api.example.org;");
    expect(policy).not.toContain("script-src *");
    expect(policy).not.toContain("javascript:");
  });

  it("allows a wildcard subdomain and a port", () => {
    expect(contentSecurityPolicy({ connectDomains: ["https://*.example.org:8443"] })).toContain(
      "connect-src https://*.example.org:8443;"
    );
  });
});

describe("viewDocument", () => {
  it("puts the policy first in the head", () => {
    const html = viewDocument("<!doctype html><html><head><title>x</title></head></html>", {});

    expect(html).toMatch(/<head><meta http-equiv="Content-Security-Policy" content="default-src 'none'/);
    expect(html.indexOf("Content-Security-Policy")).toBeLessThan(html.indexOf("<title>"));
  });

  it("puts it before a page that has no head", () => {
    expect(viewDocument("<p>hi</p>", {})).toMatch(/^<meta http-equiv="Content-Security-Policy"/);
  });
});

describe("isOpenableLink", () => {
  it("opens web pages only", () => {
    expect(isOpenableLink("https://example.org/a")).toBe(true);
    expect(isOpenableLink("http://localhost:3000")).toBe(true);
    expect(isOpenableLink("javascript:alert(1)")).toBe(false);
    expect(isOpenableLink("data:text/html,x")).toBe(false);
    expect(isOpenableLink("not a url")).toBe(false);
  });
});
