import { Link } from "@/shared/router";

import { useLessonContent, useContentTypes } from "../hooks/useContent";
import { currentContent, contentStatus } from "../status";
import {
  Audience,
  ContentSummary,
  ContentTypeInfo,
  ContentTypeSlug,
} from "../types";
import { CreateMaterial } from "./CreateMaterial";
import { MaterialRow } from "./MaterialRow";

function ContentRow({
  info,
  item,
  planVersionId,
  noteApproved,
  madeElsewhere,
}: {
  info: ContentTypeInfo;
  item: ContentSummary | undefined;
  planVersionId: string;
  noteApproved: boolean;
  madeElsewhere: string | undefined;
}) {
  if (!item && !madeElsewhere && info.made_from_a_plan_version) {
    return (
      <CreateMaterial
        info={info}
        planVersionId={planVersionId}
        noteApproved={noteApproved}
      />
    );
  }
  return (
    <MaterialRow
      info={info}
      status={contentStatus(item)}
      action={
        item ? (
          <Link
            href={`/research/teacher/content/${item.id}`}
            className="text-sm font-semibold text-(--accent-deep) hover:underline"
          >
            Review it →
          </Link>
        ) : null
      }
    >
      {!item && madeElsewhere ? (
        <p className="text-xs text-(--muted)">{madeElsewhere}</p>
      ) : null}
    </MaterialRow>
  );
}

const SECTIONS: { audience: Audience; title: string; lede: string }[] = [
  {
    audience: "teacher",
    title: "Teaching content",
    lede: "What you teach from: your plan and the note for each step.",
  },
  {
    audience: "learner",
    title: "Learning materials",
    lede: "What your students get. Each reaches no one until you approve it.",
  },
];

/**
 * Every content type for this lesson, from the server's list of types, grouped by who it is
 * for: where each stands, what it must do, and the teacher's next action.
 *
 * `madeElsewhere` names, per type, the step that makes it on this page instead of the card.
 */
export function LessonContentCard({
  planVersionId,
  madeElsewhere = {},
  without = [],
}: {
  planVersionId: string;
  madeElsewhere?: Partial<Record<ContentTypeSlug, string>>;
  /** Types the page already shows in full, so their rows are left out. */
  without?: readonly ContentTypeSlug[];
}) {
  const types = useContentTypes();
  const lessonContent = useLessonContent(planVersionId);
  const loaded = lessonContent.data ?? [];
  const noteApproved =
    currentContent(loaded, "lesson-note")?.review_status === "approved";

  if (types.isLoading || lessonContent.isLoading) {
    return <p className="text-sm text-(--muted)">Loading…</p>;
  }
  if (types.isError || lessonContent.isError) {
    return (
      <p className="text-sm text-(--danger-ink)">
        Couldn&apos;t load this lesson&apos;s content.
      </p>
    );
  }
  return (
    <>
      {SECTIONS.map((section) => (
        <section
          key={section.audience}
          className="space-y-3 rounded-2xl border border-(--line) bg-(--surface) p-5"
        >
          <div className="space-y-1">
            <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--accent-deep)">
              {section.title}
            </p>
            <p className="text-sm text-(--ink-2)">{section.lede}</p>
          </div>
          <ul className="space-y-3">
            {(types.data ?? [])
              .filter((info) => info.audience === section.audience)
              .filter((info) => !without.includes(info.type))
              .filter(
                (info) => !info.retired || currentContent(loaded, info.type),
              )
              .map((info) => (
                <ContentRow
                  key={info.type}
                  info={info}
                  item={currentContent(loaded, info.type)}
                  planVersionId={planVersionId}
                  noteApproved={noteApproved}
                  madeElsewhere={madeElsewhere[info.type]}
                />
              ))}
          </ul>
        </section>
      ))}
    </>
  );
}
