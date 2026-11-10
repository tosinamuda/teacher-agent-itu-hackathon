import { describe, expect, it } from "vitest";

import { lastRevision, savedByHand } from "./lastRevision";
import type { NumberedVersion } from "./planVersions";

const version = (
  number: number,
  source_type: string,
  status = "draft",
): NumberedVersion =>
  ({
    number,
    source_type,
    status,
    version_id: `V${number}`,
  }) as NumberedVersion;

describe("lastRevision", () => {
  it("finds the agent's newest revision and the version before it", () => {
    const found = lastRevision([
      version(1, "generated"),
      version(2, "revised"),
    ]);

    expect(found?.latest.number).toBe(2);
    expect(found?.before.number).toBe(1);
  });

  it("is none when the newest version was written another way", () => {
    expect(
      lastRevision([version(1, "generated"), version(2, "manual")]),
    ).toBeNull();
    expect(lastRevision([version(1, "revised")])).toBeNull();
    expect(lastRevision([])).toBeNull();
  });

  it("is none once the plan is approved or closed", () => {
    expect(
      lastRevision([
        version(1, "generated"),
        version(2, "revised", "approved"),
      ]),
    ).toBeNull();
  });
});

describe("savedByHand", () => {
  it("tells the teacher's own edit from the agent's revision", () => {
    expect(savedByHand({ source: "manual_edit" })).toBe(true);
    expect(savedByHand({ revised_by: "engine" })).toBe(false);
    expect(savedByHand(undefined)).toBe(false);
  });
});
