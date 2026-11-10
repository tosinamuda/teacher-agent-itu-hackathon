import type { FormEvent } from "react";
import type { FieldValues, Path, PathValue, UseFormReturn } from "react-hook-form";

/**
 * Builds a `<form>` `onSubmit` handler that is resilient to browser autofill and
 * password managers.
 *
 * Those set an input's value WITHOUT firing the change event react-hook-form
 * listens to, so RHF's internal state stays empty and a visibly-filled form can
 * fail validation ("… is required"). This reads the named inputs' live DOM
 * values into RHF (via `setValue`) before it validates, then runs the form's
 * normal `handleSubmit`.
 *
 * @param form    the `useForm` return for this form
 * @param fields  the text-input field names to sync from the DOM on submit
 * @param onValid called with the validated values (RHF's `handleSubmit` callback)
 */
export function autofillSafeSubmit<T extends FieldValues>(
  form: UseFormReturn<T>,
  fields: Path<T>[],
  onValid: (values: T) => unknown
) {
  return (event: FormEvent<HTMLFormElement>) => {
    for (const field of fields) {
      const el = event.currentTarget.elements.namedItem(field);
      if (el instanceof HTMLInputElement) {
        form.setValue(field, el.value as PathValue<T, Path<T>>, { shouldValidate: false });
      }
    }
    void form.handleSubmit(onValid)(event);
  };
}
