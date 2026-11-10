import { ButtonHTMLAttributes, forwardRef } from "react";
import { twMerge } from "tailwind-merge";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost" | "outline" | "danger";
  size?: "sm" | "md" | "lg";
  isLoading?: boolean;
}

type ButtonVariant = NonNullable<ButtonProps["variant"]>;
type ButtonSize = NonNullable<ButtonProps["size"]>;

const BASE =
  "inline-flex items-center whitespace-nowrap justify-center rounded-none font-medium transition-colors duration-150 focus:outline-hidden focus-visible:ring-2 focus-visible:ring-(--accent) disabled:opacity-60 disabled:cursor-not-allowed";

// Terracotta marks the one primary action. Every other button is neutral.
const VARIANTS: Record<ButtonVariant, string> = {
  primary:
    "bg-(--accent) text-white hover:bg-(--accent-bright) border border-transparent",
  secondary:
    "bg-(--sunken) text-(--ink) hover:bg-(--line) border border-(--line-2)",
  ghost: "bg-transparent text-(--ink-2) hover:text-(--ink)",
  outline:
    "bg-(--surface) border border-(--line-2) text-(--ink) hover:bg-(--sunken)",
  danger:
    "bg-(--surface) text-(--danger) border border-(--danger-tint) hover:bg-(--danger-tint)",
};

const SIZES: Record<ButtonSize, string> = {
  sm: "px-3 py-1.5 text-xs",
  md: "px-4 py-2 text-sm",
  lg: "px-5 py-3 text-base",
};

/** The classes of a button, for a link that has to look like one. */
export function buttonClass({
  variant = "primary",
  size = "md",
  className,
}: {
  variant?: ButtonVariant;
  size?: ButtonSize;
  className?: string;
}) {
  return twMerge(BASE, VARIANTS[variant], SIZES[size], className);
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant = "primary",
      size = "md",
      isLoading,
      children,
      disabled,
      ...props
    },
    ref,
  ) => {
    return (
      <button
        ref={ref}
        className={buttonClass({ variant, size, className })}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading && (
          <svg className="mr-2 h-4 w-4 animate-spin" viewBox="0 0 24 24">
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
              fill="none"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        )}
        {children}
      </button>
    );
  },
);

Button.displayName = "Button";
