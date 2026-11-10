import { useState } from "react";

import { Badge } from "@/shared/components/ui/Badge";
import { Button } from "@/shared/components/ui/Button";

type EndStudyControlProps = {
  isEnded: boolean;
  endedBy?: string | null;
  onEnd: () => void;
  isEnding: boolean;
};

/**
 * Research-manager end-study action: shows the study lifecycle state and, while
 * active, an inline confirm before closing it (ending a study stops new executions).
 */
export function EndStudyControl({ isEnded, endedBy, onEnd, isEnding }: EndStudyControlProps) {
  const [confirming, setConfirming] = useState(false);

  if (isEnded) {
    return (
      <div className="flex items-center gap-2">
        <Badge variant="success">Ended</Badge>
        {endedBy ? <span className="text-xs text-(--muted)">by {endedBy}</span> : null}
      </div>
    );
  }

  if (confirming) {
    return (
      <div className="flex items-center gap-2">
        <span className="text-xs text-(--muted)">End this study?</span>
        <Button size="sm" variant="danger" onClick={onEnd} isLoading={isEnding}>
          Confirm end
        </Button>
        <Button size="sm" variant="ghost" onClick={() => setConfirming(false)} disabled={isEnding}>
          Cancel
        </Button>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-2">
      <Badge variant="accent">Active</Badge>
      <Button size="sm" variant="secondary" onClick={() => setConfirming(true)}>
        End study
      </Button>
    </div>
  );
}
