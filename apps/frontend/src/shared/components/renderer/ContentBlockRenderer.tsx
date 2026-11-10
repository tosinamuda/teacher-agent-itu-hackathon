import { ContentBlock } from "@/shared/types/lesson-schema";
import { ExplanationBlock } from "./ExplanationBlock";
import { VisualBlock } from "./VisualBlock";
import { WorkedExampleBlock } from "./WorkedExampleBlock";
import { PracticeBlock } from "./PracticeBlock";

export function ContentBlockRenderer({ block }: { block: ContentBlock }) {
  switch (block.type) {
    case "explanation":
      return <ExplanationBlock block={block} />;
    case "visual":
      return <VisualBlock block={block} />;
    case "worked_example":
      return <WorkedExampleBlock block={block} />;
    case "practice":
      return <PracticeBlock block={block} />;
    default:
      console.warn("Unknown block type:", (block as { type?: string }).type);
      return null;
  }
}
