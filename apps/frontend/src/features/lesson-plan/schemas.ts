import { z } from "zod";

export const formSchema = z.object({
  subject: z.string().min(1),
  grade: z.string().min(1),
  term: z.string().min(1),
  // Registered with { valueAsNumber: true }, so the form already yields a number —
  // no coercion needed, and input/output types match (keeps zodResolver v5 typed).
  week: z.number().min(1).max(13),
  session_id: z.string().min(1, "Please select a session"),
  teacher_id: z.string().min(1),
});

export type FormValues = z.infer<typeof formSchema>;
