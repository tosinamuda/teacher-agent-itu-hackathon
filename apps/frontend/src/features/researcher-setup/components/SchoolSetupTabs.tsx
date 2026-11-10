import { Link } from "@/shared/router";

import { SchoolSetupTab } from "../types";

type SchoolSetupTabsProps = {
  activeTab: SchoolSetupTab;
  schoolId: string;
};

const tabs: Array<{ id: SchoolSetupTab; label: string }> = [
  { id: "details", label: "Details" },
  { id: "classes", label: "Classes" },
  { id: "learners", label: "Learners" },
];

/** Path-segment sub-navigation for a school's setup sections (underline-active). */
export function SchoolSetupTabs({ activeTab, schoolId }: SchoolSetupTabsProps) {
  return (
    <nav className="flex flex-wrap gap-6 border-b border-(--line) text-sm">
      {tabs.map((tab) => (
        <Link
          key={tab.id}
          href={`/research/setup/${schoolId}/${tab.id}`}
          className={`-mb-px border-b-2 pb-2 font-medium transition-colors ${
            activeTab === tab.id
              ? "border-(--accent) text-(--ink)"
              : "border-transparent text-(--ink-2) hover:text-(--ink)"
          }`}
        >
          {tab.label}
        </Link>
      ))}
    </nav>
  );
}
