import { useState } from "react";
import { Modal } from "@/shared/components/ui/Modal";
import { Button } from "@/shared/components/ui/Button";
import { useSyllabusMutations } from "../hooks/useSyllabusMutations";

interface EditWeekModalProps {
  isOpen: boolean;
  onClose: () => void;
  weekId: string;
  currentTopic: string;
}

// Inner component that resets state when key changes
const EditWeekModalContent = ({
  weekId,
  currentTopic,
  updateWeek,
  onClose,
}: {
  weekId: string;
  currentTopic: string;
  updateWeek: ReturnType<typeof useSyllabusMutations>["updateWeek"];
  onClose: () => void;
}) => {
  const [topic, setTopic] = useState(currentTopic);

  return (
    <form
      id="edit-week-form"
      onSubmit={(e) => {
        e.preventDefault();
        updateWeek.mutate(
          { weekId, payload: { title: topic } },
          { onSuccess: onClose }
        );
      }}
    >
      <div className="space-y-4">
        <div className="space-y-2">
          <label className="text-sm font-medium">Topic</label>
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-accent/50"
            placeholder="e.g. Introduction to Algebra"
            autoFocus
          />
        </div>
      </div>
    </form>
  );
};

export const EditWeekModal = ({
  isOpen,
  onClose,
  weekId,
  currentTopic,
}: EditWeekModalProps) => {
  const { updateWeek } = useSyllabusMutations();

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Edit Week Topic"
      footer={
        <>
          <Button variant="ghost" onClick={onClose}>
            Cancel
          </Button>
          <Button
            form="edit-week-form"
            type="submit"
            disabled={updateWeek.isPending}
          >
            {updateWeek.isPending ? "Saving..." : "Save Changes"}
          </Button>
        </>
      }
    >
      {/* Key resets component state when weekId or currentTopic changes */}
      <EditWeekModalContent
        key={`${weekId}-${currentTopic}`}
        weekId={weekId}
        currentTopic={currentTopic}
        updateWeek={updateWeek}
        onClose={onClose}
      />
    </Modal>
  );
};

interface EditDayModalProps {
  isOpen: boolean;
  onClose: () => void;
  mode: "ADD" | "EDIT";
  weekId?: string;
  day?: {
    id: string;
    subtopic_title: string | null;
    period_number: number;
  };
}

// Inner component that resets state when key changes
const EditDayModalContent = ({
  mode,
  weekId,
  day,
  addDay,
  updateDay,
  onClose,
}: {
  mode: "ADD" | "EDIT";
  weekId?: string;
  day?: EditDayModalProps["day"];
  addDay: ReturnType<typeof useSyllabusMutations>["addDay"];
  updateDay: ReturnType<typeof useSyllabusMutations>["updateDay"];
  onClose: () => void;
}) => {
  const [subtopicId, setSubtopicId] = useState(
    mode === "EDIT" && day ? day.subtopic_title || "" : ""
  );
  const [dayNumber, setDayNumber] = useState(
    mode === "EDIT" && day ? day.period_number : 1
  );

  return (
    <form
      id="edit-day-form"
      onSubmit={(e) => {
        e.preventDefault();
        if (mode === "ADD") {
          if (!weekId) return;
          addDay.mutate(
            {
              weekId,
              payload: {
                period_number: dayNumber || 99,
                subtopic_id: subtopicId,
              },
            },
            { onSuccess: onClose }
          );
        } else {
          if (!day) return;
          updateDay.mutate(
            {
              dayId: day.id,
              payload: {
                subtopic_id: subtopicId,
                period_number: dayNumber,
              },
            },
            { onSuccess: onClose }
          );
        }
      }}
    >
      <div className="space-y-4">
        <div className="space-y-2">
          <label className="text-sm font-medium">Subtopic ID</label>
          <input
            type="text"
            value={subtopicId}
            onChange={(e) => setSubtopicId(e.target.value)}
            className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-accent/50"
            placeholder="e.g. jss1-math-fractions-equivalent-fractions"
            autoFocus
            required
          />
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium">Sequence Number</label>
          <input
            type="number"
            value={dayNumber}
            onChange={(e) => setDayNumber(parseInt(e.target.value) || 0)}
            className="w-24 px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-accent/50"
          />
          <p className="text-xs text-muted-foreground">
            Used for ordering within the week.
          </p>
        </div>
      </div>
    </form>
  );
};

export const EditDayModal = ({
  isOpen,
  onClose,
  mode,
  weekId,
  day,
}: EditDayModalProps) => {
  const { addDay, updateDay } = useSyllabusMutations();
  const isPending = addDay.isPending || updateDay.isPending;

  // Create a stable key based on mode and day data
  const contentKey =
    mode === "EDIT" && day
      ? `edit-${day.id}-${day.subtopic_title}`
      : `add-${weekId}`;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={mode === "ADD" ? "Add Session" : "Edit Session"}
      footer={
        <>
          <Button variant="ghost" onClick={onClose}>
            Cancel
          </Button>
          <Button form="edit-day-form" type="submit" disabled={isPending}>
            {isPending
              ? "Saving..."
              : mode === "ADD"
              ? "Add Session"
              : "Save Changes"}
          </Button>
        </>
      }
    >
      {/* Key resets component state when mode/day changes */}
      <EditDayModalContent
        key={contentKey}
        mode={mode}
        weekId={weekId}
        day={day}
        addDay={addDay}
        updateDay={updateDay}
        onClose={onClose}
      />
    </Modal>
  );
};
