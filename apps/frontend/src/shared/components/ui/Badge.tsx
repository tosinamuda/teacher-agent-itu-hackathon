import { HTMLAttributes } from "react";
import { twMerge } from "tailwind-merge";

interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "accent" | "success" | "warning" | "error" | "outline";
}

export const Badge = ({
  className,
  variant = "default",
  children,
  ...props
}: BadgeProps) => {
  const variants = {
    default: "bg-(--sunken) text-(--ink-2)",
    accent: "bg-(--accent-soft) text-(--accent)",
    success: "bg-(--success-tint) text-(--success-ink)",
    warning: "bg-(--warning-tint) text-(--warning-ink)",
    error: "bg-(--danger-tint) text-(--danger-ink)",
    outline: "bg-(--surface) border border-(--line-2) text-(--ink-2)",
  };

  return (
    <span
      className={twMerge(
        "inline-flex items-center rounded-none px-2.5 py-1 text-xs font-medium",
        variants[variant],
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
};
