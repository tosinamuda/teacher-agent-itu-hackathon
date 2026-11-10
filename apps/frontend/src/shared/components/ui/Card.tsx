import { HTMLAttributes, forwardRef } from "react";
import { twMerge } from "tailwind-merge";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "glass" | "plain";
  padding?: "none" | "sm" | "md" | "lg";
}

export const Card = forwardRef<HTMLDivElement, CardProps>(
  (
    { className, variant = "default", padding = "md", children, ...props },
    ref
  ) => {
    // Editorial: flat surface, single hairline, no shadow, square corners.
    const variants = {
      default: "bg-(--surface) border border-(--line)",
      glass: "bg-(--surface) border border-(--line)",
      plain: "bg-transparent border-none",
    };

    const paddings = {
      none: "p-0",
      sm: "p-4",
      md: "p-6",
      lg: "p-8",
    };

    return (
      <div
        ref={ref}
        className={twMerge(
          "rounded-none",
          variants[variant],
          paddings[padding],
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);

Card.displayName = "Card";

export const CardHeader = ({
  className,
  children,
}: HTMLAttributes<HTMLDivElement>) => (
  <div className={twMerge("flex flex-col gap-1 mb-4", className)}>
    {children}
  </div>
);

export const CardTitle = ({
  className,
  children,
}: HTMLAttributes<HTMLHeadingElement>) => (
  <h3
    className={twMerge(
      "text-lg font-display font-semibold text-(--ink)",
      className
    )}
  >
    {children}
  </h3>
);

export const CardDescription = ({
  className,
  children,
}: HTMLAttributes<HTMLParagraphElement>) => (
  <p className={twMerge("text-sm text-(--muted)", className)}>{children}</p>
);
export const CardContent = ({
  className,
  children,
}: HTMLAttributes<HTMLDivElement>) => (
  <div className={twMerge("", className)}>{children}</div>
);
