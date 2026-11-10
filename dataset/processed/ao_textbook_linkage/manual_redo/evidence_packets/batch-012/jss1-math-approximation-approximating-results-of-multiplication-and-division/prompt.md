# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-2",
  "topic_key": "jss1-math-approximation",
  "topic": "Approximation",
  "subtopic_id": "jss1-math-approximation-approximating-results-of-multiplication-and-division",
  "subtopic_title": "Approximating results of multiplication and division",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-approximation-approximating-results-of-multiplication-and-division-po01",
        "source_performance_objective_index": 1,
        "text": "Approximate answers to multiplication and division problems to a given degree of accuracy"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "approximating-results-of-multiplication-and-division-ao-approximate-multiplication",
          "text": "Approximate answers to multiplication problems to a given degree of accuracy."
        },
        {
          "atomic_objective_id": "approximating-results-of-multiplication-and-division-ao-approximate-division",
          "text": "Approximate answers to division problems to a given degree of accuracy."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch07-b022",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": null
    },
    "content_text": "An approximate answer is almost correct, but not exact. Approximation is the process of using rounding to quickly determine a fairly accurate answer to a calculation. Approximation is very useful in situations where you have to do a calculation quickly and without paper, a pen or a calculator.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b023",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": null
    },
    "content_text": "approximation\n\nApproximation is the process of using rounding to quickly determine a fairly accurate answer to a calculation.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b034",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Using approximation in calculations"
    },
    "content_text": "The aim of using approximation in calculations is to round off numbers to values that you can work with more easily when you are using mental arithmetic. When we work with approximations, we use the symbol $\\approx$ instead of an equals sign. For example, $18+4\\approx20$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-approximating-results-of-multiplication-and-division"
  },
  {
    "record_id": "ch07-b035",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Worked example 7.7: Using approximation in calculations"
    },
    "content_text": "",
    "prompt_text": "Determine the approximate value of $475\\times 17$.",
    "answer_text": "Step 1: Round the numbers to multiples of ten that will allow an easy calculation.\n\n$$475\\times 17 \\approx 500 \\times20$$\n\nStep 2: Do the calculation using mental arithmetic.\n\n$$\\begin{align}475\\times 17 &\\approx 500 \\times20 \\\\\n&=10,000\\end{align}$$",
    "primary_subtopic_id": "jss1-math-approximation-approximating-results-of-multiplication-and-division"
  },
  {
    "record_id": "ch07-b036",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.8: Calculate approximate values"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.8: Calculate approximate values\n\nDetermine the approximate answer to each of the following.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-approximating-values-of-addition-and-subtraction"
  },
  {
    "record_id": "ch07-b036-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.8: Calculate approximate values"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.8: Calculate approximate values\n\n6. $$13 \\times 72$$",
    "answer_text": "$$\\begin{align}13 \\times 72 &\\approx 10 \\times 70 \\\\\n&\\approx 700\\end{align}$$",
    "primary_subtopic_id": "jss1-math-approximation-approximating-results-of-multiplication-and-division"
  },
  {
    "record_id": "ch07-b036-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.8: Calculate approximate values"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.8: Calculate approximate values\n\n7. $$233 \\times 36$$",
    "answer_text": "$$\\begin{align}233 \\times 36 &\\approx 200 \\times 40 \\\\\n&\\approx 8,000\\end{align}$$",
    "primary_subtopic_id": "jss1-math-approximation-approximating-results-of-multiplication-and-division"
  },
  {
    "record_id": "ch07-b036-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.8: Calculate approximate values"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.8: Calculate approximate values\n\n8. $$7\\frac{1}{5} \\times 2\\frac{7}{8}$$",
    "answer_text": "$$\\begin{align}7\\frac{1}{5} \\times 2\\frac{7}{8} &\\approx 7 \\times 3 \\\\\n&\\approx 21\\end{align}$$",
    "primary_subtopic_id": "jss1-math-approximation-approximating-results-of-multiplication-and-division"
  },
  {
    "record_id": "ch07-b036-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.8: Calculate approximate values"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.8: Calculate approximate values\n\n9. $$825 \\div 41$$",
    "answer_text": "$$\\begin{align}\\frac{825}{41} &\\approx \\frac{800}{40} \\\\\n&\\approx 20\\end{align}$$",
    "primary_subtopic_id": "jss1-math-approximation-approximating-results-of-multiplication-and-division"
  },
  {
    "record_id": "ch07-b036-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.8: Calculate approximate values"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.8: Calculate approximate values\n\n10. $$3,612 \\div 123$$",
    "answer_text": "$$\\begin{align}\\frac{3,612}{123} &\\approx \\frac{3,600}{120} \\\\\n&\\approx 30\\end{align}$$",
    "primary_subtopic_id": "jss1-math-approximation-approximating-results-of-multiplication-and-division"
  },
  {
    "record_id": "ch07-b039",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": null
    },
    "content_text": "Keep the following in mind when you use approximation in calculations:\n\n- Round off to the smallest multiple of ten that will allow an easy calculation. For example, if you round off to the nearest ten, your answer will be closer to the actual value than if you round off to the nearest hundred.\n- When you compare values, round off the same quantities to the same multiple of ten. For example, if you compare the capacity of containers, round off all the capacity values to the nearest ten.\n- When you divide similar quantities, first put them in the same unit. For example, if you divide two masses, first make sure they are both in grams or both in kilograms.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-application-of-approximation-in-everyday-life"
  },
  {
    "record_id": "ch07-b042",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.4 Summary",
      "h3": null
    },
    "content_text": "- Estimation is the process of making a guess about the size or cost of something, without doing the actual measurement or calculation.\n- Distance is the length of the space between two points.\n- The dimensions of an object are the measurable lengths that we use to determine the size of the object, such as its length, breadth and height.\n- Commonly used units of measurement for distances and dimensions are millimetre, centimetre, metre and kilometre. 1,000 mm = 100 cm = 1 m = 0.001 km.\n- The amount of liquid that a container can hold is called the capacity of the container.\n- Commonly used units of measurement for capacity are millilitre, centilitre, litre and kilolitre. 1,000 ml = 100 cl = 1 L = 0.001 kl.\n- The mass of an object is a measure of how much matter is in that object.\n- Commonly used units of measurement for mass are milligram, gram, kilogram and tonne. 1,000,000 mg = 1,000 g = 1 kg = 0.001 t.\n- Approximation is the process of using rounding to determine quickly a fairly accurate answer to a calculation.\n- Rounding off is the process of making a number less exact but easier to work with, by adjusting it to a specific multiple of 10.\n- When we round off a number to a specific multiple of 10, we have to identify the digit that represents the multiple. If the digits to the right of it give a value less than half of the required multiple of 10, the digit we identified remains the same. Otherwise, it increases by one. For example:\n  - 56,456 rounded to the nearest thousand is 56,000\n  - 56,856 rounded to the nearest thousand is 57,000\n- The aim of using approximation in calculations is to round off numbers to values that are more easily done when using mental arithmetic. When we work with approximations, we use the symbol $\\approx$ instead of an equals sign.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  }
]`: the reduced linked textbook records for that same subtopic, preserving source order

The reduced textbook record payload must contain only:

- `record_id`
- `record_type`
- `heading_path`
- `content_text`
- `prompt_text`
- `answer_text`
- `primary_subtopic_id`

---

You are building a teaching-evidence map for one subtopic of a JSS1 Mathematics curriculum. You will receive atomic objectives and textbook records. Your job is to link each textbook record to the atomic objective(s) it supports, assign a pedagogical role, identify shared foundations, allocate exercises, derive step blueprints, and select assessment items.

## Input

**Atomic Objectives for this subtopic:**

```json
{
  "theme_key": "jss1-theme-2",
  "topic_key": "jss1-math-approximation",
  "topic": "Approximation",
  "subtopic_id": "jss1-math-approximation-approximating-results-of-multiplication-and-division",
  "subtopic_title": "Approximating results of multiplication and division",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-approximation-approximating-results-of-multiplication-and-division-po01",
        "source_performance_objective_index": 1,
        "text": "Approximate answers to multiplication and division problems to a given degree of accuracy"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "approximating-results-of-multiplication-and-division-ao-approximate-multiplication",
          "text": "Approximate answers to multiplication problems to a given degree of accuracy."
        },
        {
          "atomic_objective_id": "approximating-results-of-multiplication-and-division-ao-approximate-division",
          "text": "Approximate answers to division problems to a given degree of accuracy."
        }
      ]
    }
  ]
}
```

**Textbook Records linked to this subtopic:**

```json
[
  {
    "record_id": "ch07-b022",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": null
    },
    "content_text": "An approximate answer is almost correct, but not exact. Approximation is the process of using rounding to quickly determine a fairly accurate answer to a calculation. Approximation is very useful in situations where you have to do a calculation quickly and without paper, a pen or a calculator.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b023",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": null
    },
    "content_text": "approximation\n\nApproximation is the process of using rounding to quickly determine a fairly accurate answer to a calculation.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b034",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Using approximation in calculations"
    },
    "content_text": "The aim of using approximation in calculations is to round off numbers to values that you can work with more easily when you are using mental arithmetic. When we work with approximations, we use the symbol $\\approx$ instead of an equals sign. For example, $18+4\\approx20$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-approximating-results-of-multiplication-and-division"
  },
  {
    "record_id": "ch07-b035",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Worked example 7.7: Using approximation in calculations"
    },
    "content_text": "",
    "prompt_text": "Determine the approximate value of $475\\times 17$.",
    "answer_text": "Step 1: Round the numbers to multiples of ten that will allow an easy calculation.\n\n$$475\\times 17 \\approx 500 \\times20$$\n\nStep 2: Do the calculation using mental arithmetic.\n\n$$\\begin{align}475\\times 17 &\\approx 500 \\times20 \\\\\n&=10,000\\end{align}$$",
    "primary_subtopic_id": "jss1-math-approximation-approximating-results-of-multiplication-and-division"
  },
  {
    "record_id": "ch07-b036",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.8: Calculate approximate values"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.8: Calculate approximate values\n\nDetermine the approximate answer to each of the following.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-approximating-values-of-addition-and-subtraction"
  },
  {
    "record_id": "ch07-b036-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.8: Calculate approximate values"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.8: Calculate approximate values\n\n6. $$13 \\times 72$$",
    "answer_text": "$$\\begin{align}13 \\times 72 &\\approx 10 \\times 70 \\\\\n&\\approx 700\\end{align}$$",
    "primary_subtopic_id": "jss1-math-approximation-approximating-results-of-multiplication-and-division"
  },
  {
    "record_id": "ch07-b036-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.8: Calculate approximate values"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.8: Calculate approximate values\n\n7. $$233 \\times 36$$",
    "answer_text": "$$\\begin{align}233 \\times 36 &\\approx 200 \\times 40 \\\\\n&\\approx 8,000\\end{align}$$",
    "primary_subtopic_id": "jss1-math-approximation-approximating-results-of-multiplication-and-division"
  },
  {
    "record_id": "ch07-b036-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.8: Calculate approximate values"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.8: Calculate approximate values\n\n8. $$7\\frac{1}{5} \\times 2\\frac{7}{8}$$",
    "answer_text": "$$\\begin{align}7\\frac{1}{5} \\times 2\\frac{7}{8} &\\approx 7 \\times 3 \\\\\n&\\approx 21\\end{align}$$",
    "primary_subtopic_id": "jss1-math-approximation-approximating-results-of-multiplication-and-division"
  },
  {
    "record_id": "ch07-b036-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.8: Calculate approximate values"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.8: Calculate approximate values\n\n9. $$825 \\div 41$$",
    "answer_text": "$$\\begin{align}\\frac{825}{41} &\\approx \\frac{800}{40} \\\\\n&\\approx 20\\end{align}$$",
    "primary_subtopic_id": "jss1-math-approximation-approximating-results-of-multiplication-and-division"
  },
  {
    "record_id": "ch07-b036-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.8: Calculate approximate values"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.8: Calculate approximate values\n\n10. $$3,612 \\div 123$$",
    "answer_text": "$$\\begin{align}\\frac{3,612}{123} &\\approx \\frac{3,600}{120} \\\\\n&\\approx 30\\end{align}$$",
    "primary_subtopic_id": "jss1-math-approximation-approximating-results-of-multiplication-and-division"
  },
  {
    "record_id": "ch07-b039",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": null
    },
    "content_text": "Keep the following in mind when you use approximation in calculations:\n\n- Round off to the smallest multiple of ten that will allow an easy calculation. For example, if you round off to the nearest ten, your answer will be closer to the actual value than if you round off to the nearest hundred.\n- When you compare values, round off the same quantities to the same multiple of ten. For example, if you compare the capacity of containers, round off all the capacity values to the nearest ten.\n- When you divide similar quantities, first put them in the same unit. For example, if you divide two masses, first make sure they are both in grams or both in kilograms.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-application-of-approximation-in-everyday-life"
  },
  {
    "record_id": "ch07-b042",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.4 Summary",
      "h3": null
    },
    "content_text": "- Estimation is the process of making a guess about the size or cost of something, without doing the actual measurement or calculation.\n- Distance is the length of the space between two points.\n- The dimensions of an object are the measurable lengths that we use to determine the size of the object, such as its length, breadth and height.\n- Commonly used units of measurement for distances and dimensions are millimetre, centimetre, metre and kilometre. 1,000 mm = 100 cm = 1 m = 0.001 km.\n- The amount of liquid that a container can hold is called the capacity of the container.\n- Commonly used units of measurement for capacity are millilitre, centilitre, litre and kilolitre. 1,000 ml = 100 cl = 1 L = 0.001 kl.\n- The mass of an object is a measure of how much matter is in that object.\n- Commonly used units of measurement for mass are milligram, gram, kilogram and tonne. 1,000,000 mg = 1,000 g = 1 kg = 0.001 t.\n- Approximation is the process of using rounding to determine quickly a fairly accurate answer to a calculation.\n- Rounding off is the process of making a number less exact but easier to work with, by adjusting it to a specific multiple of 10.\n- When we round off a number to a specific multiple of 10, we have to identify the digit that represents the multiple. If the digits to the right of it give a value less than half of the required multiple of 10, the digit we identified remains the same. Otherwise, it increases by one. For example:\n  - 56,456 rounded to the nearest thousand is 56,000\n  - 56,856 rounded to the nearest thousand is 57,000\n- The aim of using approximation in calculations is to round off numbers to values that are more easily done when using mental arithmetic. When we work with approximations, we use the symbol $\\approx$ instead of an equals sign.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  }
]
```

## Task

Produce a single JSON object following the output schema below.

### Phase 1 — Classify every record

For each textbook record, determine which atomic objective(s) it supports and what role it plays.

Deterministic rules:

- `definition` -> role is `foundation`
  Assign to all AOs only if the definition genuinely supports all of them; otherwise assign by content match.
- `summary` -> exclude from lesson steps
- `exercise_block` -> exclude; child `exercise_item` rows are handled individually
- `hint` -> exclude

Heading and prompt matching:

- For `worked_example` and `exercise_item`, read `heading_path` and `prompt_text`
- Match the named skill to the AO whose text describes that same skill
- `worked_example` -> role `worked_example`
- `exercise_item` -> role `exercise`

Judgment rules for `exposition` and `note`:

- If the record establishes concepts that every AO needs equally, assign it to all AOs with role `foundation`
- If it teaches a specific method or procedure for one AO, assign it to that AO with role `instruction`
- If it is a cross-reference note with no standalone teaching content, exclude it
- If it provides prerequisite knowledge for one AO but is not the main procedural teaching, assign it to that AO with role `foundation`

Every record must end in exactly one category:

1. Assigned to one or more AOs
2. Excluded by rule
3. Ambiguous and placed in `review_items`

Do not silently drop any record.

If a record does not directly match any current AO, inspect its actual
teaching content before deciding. Create a `candidate_atomic_objectives` entry
only when the record teaches a distinct, measurable skill that is not already
covered by the current AO list. Do not create candidates from keyword matches,
headings alone, vague context, or records that merely duplicate an existing AO.
Candidate AOs are proposals for expert review; they do not change the source
AO list.

### Phase 2 — Identify shared foundation

Find records tagged as `foundation` for every AO in the subtopic.

- Put their `record_id` values into `shared_foundation_record_ids`
- Preserve source textbook order exactly as the records appear in the input
- Remove those records from per-AO `record_links`

### Phase 3 — Allocate exercises

For each AO, split exercise links into:

- `practice_record_ids`: in-step practice, max 2
- an internal assessment pool for evaluation

Allocation rule:

- 3+ exercises -> first 2 for practice, rest for assessment pool
- 2 exercises -> first 1 for practice, second for assessment pool
- 1 exercise -> none for practice, the one exercise goes to assessment pool
- 0 exercises -> flag as `ao_no_exercises` in `status_reasons` if this blocks assessment

### Phase 4 — Derive step blueprint

`block_types` always includes `explanation`

- If the AO has a `worked_example` link, include `worked_example`
- If the AO has `practice_record_ids` or any assessment-pool exercise, include `practice`

Set `instructional_type`:

- `explain_example_practice` if `worked_example` is present
- `explain_practice` if `practice` is present but `worked_example` is not
- `explain_only` otherwise

### Phase 5 — Select assessment item

For each AO:

- If an assessment-pool exercise exists, reuse it directly
  - copy `prompt_text` exactly into `question`
  - copy `answer_text` exactly into `expected_answer`
  - set `method: "reused"`
  - set `source_exercise_id` to the record id
- If no exercise exists but instruction or worked-example evidence exists, write one grounded question
  - set `method: "llm_grounded"`
  - set `source_exercise_id: null`
- If neither exists, set `assessment: null`

The assessment must match the AO bloom level.

### Phase 6 — Determine subtopic status

- `mapped` -> every AO has at least one accepted record link, a usable blueprint, and an assessment
- `needs_review` -> any AO is missing records, missing assessment, or has review items
- `no_records` -> the subtopic has zero textbook records

When the row includes at least one candidate AO proposal, add
`candidate_new_atomic_objective` to `review_categories` and explain why in
`category_reasons`.

## Bloom Verb Map

```text
remember:    list, name, state, define, identify, recall, recognise, recognize, count, write, read
understand:  explain, describe, discuss, distinguish, classify, compare, interpret
apply:       convert, solve, calculate, apply, use, draw, construct, find, determine, compute,
             add, subtract, multiply, divide, round, estimate, approximate, express, present,
             bisect, measure
analyze:     analyze, analyse, differentiate, examine, verify
```

Default to `apply` if the AO verb is not listed.

## Output Schema

Return exactly one JSON object:

```json
{
  "subtopic_id": "string",
  "subtopic_title": "string",
  "status": "mapped | needs_review | no_records",
  "status_reasons": ["string"],
  "shared_foundation_record_ids": ["record_id"],
  "excluded_records": [
    {
      "record_id": "string",
      "record_type": "string",
      "reason": "string"
    }
  ],
  "review_items": [
    {
      "record_id": "string",
      "candidate_ao_ids": ["string"],
      "candidate_roles": ["string"],
      "issue": "string",
      "rationale": "string"
    }
  ],
  "candidate_atomic_objectives": [
    {
      "candidate_ao_id": "string",
      "candidate_kind": "prerequisite | missing_direct_objective | extension_or_enrichment | curriculum_textbook_mismatch",
      "proposed_objective_text": "string",
      "bloom_verb": "string",
      "bloom_level": "remember | understand | apply | analyze",
      "source_record_ids": ["record_id"],
      "evidence_quote": "string",
      "closest_existing_ao_ids": ["ao_id"],
      "rationale": "string",
      "status": "candidate_for_expert_review"
    }
  ],
  "atomic_objectives": [
    {
      "ao_id": "string",
      "ao_order": 1,
      "curriculum_objective_id": "string",
      "curriculum_objective_text": "string",
      "text": "string",
      "bloom_verb": "string",
      "bloom_level": "string",
      "record_links": [
        {
          "record_id": "string",
          "role": "foundation | instruction | worked_example | exercise",
          "method": "rule_type | rule_heading | judgment",
          "rationale": "string | null"
        }
      ],
      "practice_record_ids": ["record_id"],
      "step_blueprint": {
        "block_types": ["explanation", "worked_example", "practice"],
        "instructional_type": "explain_only | explain_practice | explain_example_practice"
      },
      "assessment": {
        "question": "string",
        "expected_answer": "string",
        "bloom_level": "string",
        "source_exercise_id": "string | null",
        "hints": ["string"],
        "method": "reused | llm_grounded"
      }
    }
  ]
}
```

## Rules

1. Do not invent record ids.
2. Do not invent textbook content.
3. Preserve AO order from the input.
4. Preserve source input order for textbook records.
5. Every record must be assigned, excluded, or added to `review_items`.
6. `rationale` is required only for `method: "judgment"`.
7. A record may support multiple AOs only when it genuinely supports all of them.
8. For `method: "reused"`, copy `prompt_text` and `answer_text` exactly.
9. Write mathematics using `$...$` inline and `$$...$$` for display.
10. Candidate AO source records must already be accounted for as shared
    foundation, AO links, or review items; do not use excluded records as
    candidate evidence.

Return only the JSON object. No commentary before or after.
