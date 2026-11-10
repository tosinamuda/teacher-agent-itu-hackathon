import { Pager } from "@/shared/components/renderer/Pager";

import { marksText, questionsByObjective } from "../examQuestions";
import type { EngineManifest } from "../types";
import { NoteText } from "./NoteText";

/** Exam questions, an objective at a time: each question numbered, with its marks; the answer on request. */
export function ExamQuestionsView({ manifest }: { manifest: EngineManifest }) {
  const groups = questionsByObjective(manifest);
  if (groups.length === 0)
    return (
      <p className="text-sm text-(--muted)">There are no exam questions yet.</p>
    );

  return (
    <Pager count={groups.length} label="Objective">
      {(index) => {
        const group = groups[index];
        return (
          <article className="flex min-h-0 flex-1 flex-col gap-4 overflow-y-auto overscroll-contain border border-(--line) bg-(--surface) p-5">
            <header className="flex items-baseline justify-between gap-4 border-b border-(--line) pb-3">
              <h2 className="text-base font-semibold text-(--ink)">
                {group.label}
              </h2>
              <span className="shrink-0 text-xs text-(--ink-2)">
                {group.questions.length}{" "}
                {group.questions.length === 1 ? "question" : "questions"} ·{" "}
                {marksText(group.totalMarks)}
              </span>
            </header>
            <ol className="flex flex-col divide-y divide-(--line)">
              {group.questions.map((question, at) => (
                <li
                  key={at}
                  className="flex flex-col gap-3 py-4 first:pt-0 last:pb-0"
                >
                  <div className="flex items-start gap-4">
                    <span className="w-6 shrink-0 text-sm font-semibold text-(--ink-2)">
                      {at + 1}.
                    </span>
                    <div className="min-w-0 flex-1 text-base text-(--ink)">
                      <NoteText text={question.question} />
                    </div>
                    {question.marks !== null ? (
                      <span className="shrink-0 border border-(--line-2) px-2 py-0.5 text-xs text-(--ink-2)">
                        {marksText(question.marks)}
                      </span>
                    ) : null}
                  </div>
                  {question.answer || question.markingScheme ? (
                    <details className="ml-10 text-sm">
                      <summary className="cursor-pointer text-xs font-semibold text-(--ink-2) hover:text-(--ink)">
                        Answer and marking scheme
                      </summary>
                      <div className="mt-2 flex flex-col gap-3 border-l-2 border-(--line) pl-4">
                        {question.answer ? (
                          <div>
                            <p className="text-[11px] font-semibold uppercase tracking-[0.12em] text-(--faint)">
                              Answer
                            </p>
                            <NoteText text={question.answer} />
                          </div>
                        ) : null}
                        {question.markingScheme ? (
                          <div>
                            <p className="text-[11px] font-semibold uppercase tracking-[0.12em] text-(--faint)">
                              Marking scheme
                            </p>
                            <NoteText text={question.markingScheme} />
                          </div>
                        ) : null}
                      </div>
                    </details>
                  ) : null}
                </li>
              ))}
            </ol>
          </article>
        );
      }}
    </Pager>
  );
}
