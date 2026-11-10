import { describe, expect, it } from "vitest";

import { formatRelativeTime, parseApiMoment } from "./relativeTime";

const NOW = Date.parse("2026-09-27T14:05:00Z");

describe("parseApiMoment", () => {
  it("reads a time sent without an offset as UTC", () => {
    expect(parseApiMoment("2026-09-27T14:00:00")).toBe(Date.parse("2026-09-27T14:00:00Z"));
    expect(parseApiMoment("2026-09-27T14:00:00.123456")).toBe(
      Date.parse("2026-09-27T14:00:00.123Z"),
    );
  });

  it("keeps the offset a time was sent with", () => {
    expect(parseApiMoment("2026-09-27T14:00:00Z")).toBe(Date.parse("2026-09-27T14:00:00Z"));
    expect(parseApiMoment("2026-09-27T16:00:00+02:00")).toBe(Date.parse("2026-09-27T14:00:00Z"));
  });
});

describe("formatRelativeTime", () => {
  it("says minutes for a time five minutes old, however it was sent", () => {
    expect(formatRelativeTime("2026-09-27T14:00:00", NOW)).toBe("5 min ago");
    expect(formatRelativeTime("2026-09-27T14:00:00Z", NOW)).toBe("5 min ago");
    expect(formatRelativeTime("2026-09-27T16:00:00+02:00", NOW)).toBe("5 min ago");
  });

  it("counts hours and days", () => {
    expect(formatRelativeTime("2026-09-27T12:05:00Z", NOW)).toBe("2 hr ago");
    expect(formatRelativeTime("2026-09-26T14:05:00Z", NOW)).toBe("1 day ago");
  });

  it("says nothing for a missing or unreadable time", () => {
    expect(formatRelativeTime(undefined, NOW)).toBeUndefined();
    expect(formatRelativeTime("not a time", NOW)).toBeUndefined();
  });
});
