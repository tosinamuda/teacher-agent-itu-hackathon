import { DiagnosticItemList } from "@/features/diagnostic-review/components/DiagnosticItemList";
import { DiagnosticPayload } from "@/features/diagnostic-review/types";
import { PackManifestPreview } from "@/features/pack-review/components/PackManifestPreview";
import { PackManifest } from "@/features/pack-review/types";
import {
  SessionPlanData,
  SessionPlanView,
} from "@/features/lesson-plan/components/SessionPlanView";

import { usePlanVersion } from "@/features/lesson-plan/hooks/usePlanVersion";
import { McpAppView } from "@/features/mcp-app/McpAppView";

import { useSpec } from "../hooks/useContent";
import { ContentItem, EngineManifest, LessonNoteManifest } from "../types";
import { EngineContentView } from "./EngineContentView";
import { ExamQuestionsView } from "./ExamQuestionsView";
import { LessonNoteView } from "./LessonNoteView";
import { SlideDeckView } from "./SlideDeckView";

/**
 * Engine-built content, in the page the engine's MCP server draws it in. The app draws it from
 * the part schemas of the spec revision it was built with when the server has no page for it.
 */
function EngineContent({ item }: { item: ContentItem }) {
  const spec = useSpec(item.type, item.provenance.specification?.revision);
  return (
    <McpAppView
      tool="show_content"
      input={{ content_id: item.id }}
      revision={`${item.version}:${item.review_status}`}
      fallback={
        <EngineContentView
          manifest={item.content as unknown as EngineManifest}
          spec={spec.data ?? null}
        />
      }
    />
  );
}

/** A lesson note beside its plan's steps, so it can be read as the teacher prepares it. */
function LessonNoteContent({ item }: { item: ContentItem }) {
  const plan = usePlanVersion(item.plan_version_id);
  return (
    <LessonNoteView
      manifest={item.content as unknown as LessonNoteManifest}
      steps={plan.data?.session_plan.steps}
      paged
    />
  );
}

/** A content item, drawn the way its type is read. */
export function ContentView({
  item,
  section,
  onSectionChange,
}: {
  item: ContentItem;
  section?: number;
  onSectionChange?: (index: number) => void;
}) {
  switch (item.type) {
    case "revision-note":
      return (
        <PackManifestPreview
          manifest={item.content as unknown as PackManifest}
          section={section}
          onSectionChange={onSectionChange}
        />
      );
    case "class-test":
      return (
        <DiagnosticItemList
          items={(item.content as unknown as DiagnosticPayload).items}
          planVersionId={item.plan_version_id}
          paged
        />
      );
    case "lesson-plan":
      return (
        <SessionPlanView
          sessionPlan={item.content as unknown as SessionPlanData}
        />
      );
    case "lesson-note":
      return <LessonNoteContent item={item} />;
    case "exam-questions":
      return <ExamQuestionsView manifest={item.content as unknown as EngineManifest} />;
    case "slide-deck":
      return (
        <SlideDeckView manifest={item.content as unknown as EngineManifest} />
      );
    default:
      return <EngineContent item={item} />;
  }
}
