# Write the wrong options and their codes

A learner who picks a wrong option shows a misconception. The code of the option names it, and
the learner's revision note is written to correct it.

- Make each wrong option the answer that one specific error gives. For "Find the perimeter of a
  rectangle 5 cm by 3 cm" (answer 16 cm), 15 cm is the area, so its code is
  `area_perimeter_confusion`; 8 cm adds one length and one breadth, so its code is
  `added_two_sides_only`.
- Give a code to each of the three wrong options, and never to the correct option. Each
  `distractors` entry names a letter that is on the question and is not `correct_option`.
- Write the code in snake_case: lowercase words joined by underscores, short, and specific to
  the maths error. It reads as a phrase when the underscores become spaces:
  `missing_factor_of_two` reads "Missing factor of two".
  - Wrong: `wrong_answer`, `error_1`, `careless`, `B_is_wrong`.
  - Right: `numerator_denominator_swapped`, `fraction_equal_one_misconception`.
- Give the same error the same code in both questions on the objective. The learner's
  misconception for the objective is the code they pick most often.
- Draw a wrong option from the numbers in the stem, or from the answer a specific error gives.
  Never bring in a number the stem does not hold, and never use a filler option such as "Both
  are equal", "Cannot be determined" or "All of the above". Use "Both are equal" only when
  the two numbers really are equal and that is the misconception being tested.
