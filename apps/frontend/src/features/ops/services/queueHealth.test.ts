import { describe, expect, it } from "vitest";

import type { OpsHealth, RunnerInfo } from "../api";
import { readQueueHealth } from "./queueHealth";

function runner(overrides: Partial<RunnerInfo> = {}): RunnerInfo {
  return {
    runner: "api:1",
    online: true,
    slots: 4,
    running: 0,
    started_at: null,
    seen_at: null,
    ...overrides,
  };
}

function health(overrides: Partial<OpsHealth> = {}): OpsHealth {
  return {
    runners: [runner()],
    counts: { queued: 0, running: 0, succeeded: 0, failed: 0, cancelled: 0 },
    oldest_queued_age_seconds: null,
    slots_per_runner: 4,
    ...overrides,
  };
}

const waiting = (count: number, ageSeconds: number): Partial<OpsHealth> => ({
  counts: { queued: count, running: 0, succeeded: 0, failed: 0, cancelled: 0 },
  oldest_queued_age_seconds: ageSeconds,
});

describe("readQueueHealth", () => {
  it("reads an online runner with nothing waiting as running", () => {
    const read = readQueueHealth(health());

    expect(read.state).toBe("running");
    expect(read.tone).toBe("ok");
    expect(read.detail).toContain("Nothing is waiting");
  });

  it("reads no runner online as down, however little is waiting", () => {
    const read = readQueueHealth(health({ runners: [runner({ online: false })] }));

    expect(read.state).toBe("no-runner");
    expect(read.tone).toBe("danger");
  });

  it("separates every slot busy from a runner that cannot claim", () => {
    const busy = readQueueHealth(
      health({ runners: [runner({ running: 4 })], ...waiting(3, 600) }),
    );
    const stuck = readQueueHealth(
      health({ runners: [runner({ running: 1 })], ...waiting(2, 120) }),
    );

    expect(busy.state).toBe("busy");
    expect(busy.tone).toBe("warn");
    expect(stuck.state).toBe("stuck");
    expect(stuck.tone).toBe("danger");
  });

  it("gives a job just queued beside a free slot its turn", () => {
    const read = readQueueHealth(health({ ...waiting(1, 2) }));

    expect(read.state).toBe("running");
    expect(read.detail).toContain("1 waiting; the oldest for 2s");
  });
});
