import { usePathname, useRouter, useSearchParams } from "@/shared/router";

export type WalkthroughState = {
  lesson: string | null;
  draw: number;
  learner: string | null;
  step: number;
};

/**
 * Where the walkthrough is, kept in the URL: the lesson (by its code), draw, learner and step.
 * A bookmark opens on the example it was saved at.
 */
export function useWalkthroughState(): [
  WalkthroughState,
  (change: Partial<WalkthroughState>) => void,
] {
  const params = useSearchParams();
  const pathname = usePathname();
  const router = useRouter();
  const state: WalkthroughState = {
    lesson: params.get("lesson"),
    draw: Number(params.get("draw")) || 1,
    learner: params.get("learner"),
    step: Math.max(Number(params.get("step")) || 1, 1),
  };
  const update = (change: Partial<WalkthroughState>) => {
    const next = { ...state, ...change };
    const query = new URLSearchParams();
    if (next.lesson) query.set("lesson", next.lesson);
    query.set("draw", String(next.draw));
    if (next.learner) query.set("learner", next.learner);
    query.set("step", String(next.step));
    router.replace(`${pathname}?${query.toString()}`);
  };
  return [state, update];
}
