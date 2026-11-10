import { InputHTMLAttributes, SelectHTMLAttributes, forwardRef } from "react";
import { twMerge } from "tailwind-merge";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, ...props }, ref) => {
    return (
      <div className="w-full space-y-1.5">
        {label && (
          <label className="text-sm font-medium text-(--ink) block">
            {label}
          </label>
        )}
        <input
          ref={ref}
          className={twMerge(
            "flex w-full rounded-xl border border-(--line) bg-(--surface) px-3 py-2.5 text-sm ring-offset-white file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-(--faint) focus:outline-hidden focus:ring-2 focus:ring-(--accent) focus:border-transparent disabled:cursor-not-allowed disabled:opacity-50 transition-all duration-200",
            error && "border-(--danger) focus:ring-rose-500",
            className
          )}
          {...props}
        />
        {error && <p className="text-xs text-(--danger) font-medium">{error}</p>}
      </div>
    );
  }
);
Input.displayName = "Input";

interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, label, error, children, ...props }, ref) => {
    return (
      <div className="w-full space-y-1.5">
        {label && (
          <label className="text-sm font-medium text-(--ink) block">
            {label}
          </label>
        )}
        <div className="relative">
          <select
            ref={ref}
            className={twMerge(
              "flex w-full appearance-none rounded-xl border border-(--line) bg-(--surface) px-3 py-2.5 text-sm ring-offset-white focus:outline-hidden focus:ring-2 focus:ring-(--accent) focus:border-transparent disabled:cursor-not-allowed disabled:opacity-50 transition-all duration-200",
              error && "border-(--danger) focus:ring-rose-500",
              className
            )}
            {...props}
          >
            {children}
          </select>
          {/* Custom chevron */}
          <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-(--ink-2)">
            <svg
              className="h-4 w-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </div>
        </div>
        {error && <p className="text-xs text-(--danger) font-medium">{error}</p>}
      </div>
    );
  }
);
Select.displayName = "Select";
