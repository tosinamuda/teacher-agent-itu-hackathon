import React, { useEffect } from "react";
import { createPortal } from "react-dom";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
  maxWidthClassName?: string;
}

export const Modal = ({
  isOpen,
  onClose,
  title,
  children,
  footer,
  maxWidthClassName = "max-w-lg",
}: ModalProps) => {
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    if (isOpen) {
      document.addEventListener("keydown", handleEsc);
      document.body.style.overflow = "hidden";
    }
    return () => {
      document.removeEventListener("keydown", handleEsc);
      document.body.style.overflow = "unset";
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  // Use portal if possible, but for simplicity render here (assuming top level z-index works)
  // Actually, better to use portal to avoid stacking context issues.
  // But strictly standard React 19 might be different? Next.js is React 19 RC.
  // portal is standard.

  const content = (
    <div className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-black/50 p-4 backdrop-blur-sm animate-in fade-in duration-200 sm:py-8">
      <div
        className={`w-full overflow-hidden rounded-xl bg-white animate-in zoom-in-95 duration-200 ${maxWidthClassName}`}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between p-4 border-b">
          <h3 className="font-semibold text-lg">{title}</h3>
          <button
            onClick={onClose}
            className="text-(--ink-2) hover:text-(--ink-2) p-1 rounded-none hover:bg-(--sunken) transition-colors"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="w-5 h-5"
            >
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>

        <div className="max-h-[80vh] overflow-y-auto p-4">{children}</div>

        {footer && (
          <div className="p-4 border-t bg-(--sunken) flex justify-end gap-2">
            {footer}
          </div>
        )}
      </div>
    </div>
  );

  // Check if document exists (SSR safety)
  if (typeof document === "undefined") return null;

  return createPortal(content, document.body);
};
