# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-3",
  "topic_key": "jss1-math-use-of-symbols",
  "topic": "Use of Symbols",
  "subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations",
  "subtopic_title": "Solving open sentences with two arithmetic operations",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations-po01",
        "source_performance_objective_index": 1,
        "text": "Solve open sentence problems involving two arithmetic operations"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "solving-open-sentences-with-two-operations-ao-solve-problems",
          "text": "Solve open sentence problems involving two arithmetic operations."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch09-b024",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": null
    },
    "content_text": "Open number sentences may have more than one operation, for example $4-2+x=10$. To solve number sentences like these, you must remember the correct order of operations that you learnt last year:\n\n1. **B**rackets\n2. **O**f\n3. **D**ivide\n4. **M**ultiply\n5. **A**dd\n6. **S**ubtract",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b025",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Worked example 9.7: Solving a problem using open sentences"
    },
    "content_text": "",
    "prompt_text": "Find the value of x:",
    "answer_text": "$$\nx \\div 2 + 3 = 8\n$$\n\nStep 1: Decide which inverse operation to do first.\n\nAccording to the order BODMAS, you must calculate $x \\div 2$ before $2+3$.\nThis means $x \\div 2$ must \"stay together\". You may insert brackets to help you.\nWe must use the inverse of addition first.\n\n$$\n(x \\div 2) +3 - 3 = 8 - 3\n$$\n\nStep 2: Simplify the number sentence from Step 1 until you have only one operation.\n\n$$\n\\begin{align}\n (x \\div 2) +3 - 3 &= 8 - 3 \\\\\n x \\div 2 &= 5\n\\end{align}\n$$\n\nStep 3: Use an inverse operation and simplify to get to the format $\\boldsymbol{variable}=\\textbf{ value}$.\n\n$$\n\\begin{align}\n x \\div 2 &= 5 \\\\\n x \\div 2 \\times 2 &= 5 \\times 2 \\\\\n x &= 10\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\nFind the value of the variable in the following open sentences:",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n1. 3 + x - 4 = 20",
    "answer_text": "$$\n\\begin{align}\n x - 1 &= 20 \\\\\n x - 1 + 1 &= 20 + 1 \\\\\n x &= 21\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n2. q \\times 3 + 5 = 29",
    "answer_text": "$$\n\\begin{align}\n (q \\times 3) + 5 - 5 &= 29 - 5 \\\\\n q \\times 3 &= 24 \\\\\n q \\times 3 \\div 3 &= 24 \\div 3 \\\\\n q &= 8\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n3. t + 10 \\div 2 = 12",
    "answer_text": "$$\n\\begin{align}\n t + (10 \\div 2) &= 12 \\\\\n t + 5 &= 12 \\\\\n t + 5 - 5 &= 12 - 5 \\\\\n t &= 7\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n4. 5 - x + 2 = 12",
    "answer_text": "$$\n\\begin{align}\n 5 + 2 - x &= 12 \\\\\n 7 - x &= 12 \\\\\n 7 - x + x &= 12 + x \\\\\n 7 &= 12 + x \\\\\n 7 - 12 &= 12 - 12 + x \\\\\n -5 &= x \\\\\n x &= -5\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n5. y \\times 5 - 7 = 13",
    "answer_text": "$$\n\\begin{align}\n (y \\times 5) - 7 &= 13 \\\\\n (y \\times 5) - 7 + 7 &= 13 + 7 \\\\\n y \\times 5 &= 20 \\\\\n y \\times 5 \\div 5 &= 20 \\div 5 \\\\\n y &= 4\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n6. p \\div 2 - 5 = 25",
    "answer_text": "$$\n\\begin{align}\n (p \\div 2) - 5 &= 25 \\\\\n (p \\div 2) - 5 + 5 &= 25 + 5 \\\\\n p \\div 2 &= 30 \\\\\n p \\div 2 \\times 2 &= 30 \\times 2 \\\\\n p &= 60\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n7. 5 \\times -2 = 6 + v",
    "answer_text": "$$\n\\begin{align}\n -10 &= 6 + v \\\\\n -10 - 6 &= 6 - 6 + v \\\\\n -16 &= v \\\\\n v &= -16\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n8. 2 \\times -6 = 24 \\div r",
    "answer_text": "$$\n\\begin{align}\n -12 &= 24 \\div r  \\\\\n -12 \\times r &= 24 \\div r \\times r \\\\\n -12 \\div -12 \\times r &= 24 \\div -12 \\\\\n r &= -2\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b031",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.4 Summary",
      "h3": null
    },
    "content_text": "- A closed number sentence is always true or always false.\n- In an open number sentence, there is some information missing that we need to find.\n- An open number sentence can use picture symbols or variables to show which information is missing.\n- The value of a variable can vary.\n- Finding the missing information, or finding the value of the variable, is called solving an open sentence.\n- We can solve an open sentence using mental maths or using the inverse operation.\n- We can use open sentences to solve problems described in words.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
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
  "theme_key": "jss1-theme-3",
  "topic_key": "jss1-math-use-of-symbols",
  "topic": "Use of Symbols",
  "subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations",
  "subtopic_title": "Solving open sentences with two arithmetic operations",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations-po01",
        "source_performance_objective_index": 1,
        "text": "Solve open sentence problems involving two arithmetic operations"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "solving-open-sentences-with-two-operations-ao-solve-problems",
          "text": "Solve open sentence problems involving two arithmetic operations."
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
    "record_id": "ch09-b024",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": null
    },
    "content_text": "Open number sentences may have more than one operation, for example $4-2+x=10$. To solve number sentences like these, you must remember the correct order of operations that you learnt last year:\n\n1. **B**rackets\n2. **O**f\n3. **D**ivide\n4. **M**ultiply\n5. **A**dd\n6. **S**ubtract",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b025",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Worked example 9.7: Solving a problem using open sentences"
    },
    "content_text": "",
    "prompt_text": "Find the value of x:",
    "answer_text": "$$\nx \\div 2 + 3 = 8\n$$\n\nStep 1: Decide which inverse operation to do first.\n\nAccording to the order BODMAS, you must calculate $x \\div 2$ before $2+3$.\nThis means $x \\div 2$ must \"stay together\". You may insert brackets to help you.\nWe must use the inverse of addition first.\n\n$$\n(x \\div 2) +3 - 3 = 8 - 3\n$$\n\nStep 2: Simplify the number sentence from Step 1 until you have only one operation.\n\n$$\n\\begin{align}\n (x \\div 2) +3 - 3 &= 8 - 3 \\\\\n x \\div 2 &= 5\n\\end{align}\n$$\n\nStep 3: Use an inverse operation and simplify to get to the format $\\boldsymbol{variable}=\\textbf{ value}$.\n\n$$\n\\begin{align}\n x \\div 2 &= 5 \\\\\n x \\div 2 \\times 2 &= 5 \\times 2 \\\\\n x &= 10\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\nFind the value of the variable in the following open sentences:",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n1. 3 + x - 4 = 20",
    "answer_text": "$$\n\\begin{align}\n x - 1 &= 20 \\\\\n x - 1 + 1 &= 20 + 1 \\\\\n x &= 21\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n2. q \\times 3 + 5 = 29",
    "answer_text": "$$\n\\begin{align}\n (q \\times 3) + 5 - 5 &= 29 - 5 \\\\\n q \\times 3 &= 24 \\\\\n q \\times 3 \\div 3 &= 24 \\div 3 \\\\\n q &= 8\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n3. t + 10 \\div 2 = 12",
    "answer_text": "$$\n\\begin{align}\n t + (10 \\div 2) &= 12 \\\\\n t + 5 &= 12 \\\\\n t + 5 - 5 &= 12 - 5 \\\\\n t &= 7\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n4. 5 - x + 2 = 12",
    "answer_text": "$$\n\\begin{align}\n 5 + 2 - x &= 12 \\\\\n 7 - x &= 12 \\\\\n 7 - x + x &= 12 + x \\\\\n 7 &= 12 + x \\\\\n 7 - 12 &= 12 - 12 + x \\\\\n -5 &= x \\\\\n x &= -5\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n5. y \\times 5 - 7 = 13",
    "answer_text": "$$\n\\begin{align}\n (y \\times 5) - 7 &= 13 \\\\\n (y \\times 5) - 7 + 7 &= 13 + 7 \\\\\n y \\times 5 &= 20 \\\\\n y \\times 5 \\div 5 &= 20 \\div 5 \\\\\n y &= 4\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n6. p \\div 2 - 5 = 25",
    "answer_text": "$$\n\\begin{align}\n (p \\div 2) - 5 &= 25 \\\\\n (p \\div 2) - 5 + 5 &= 25 + 5 \\\\\n p \\div 2 &= 30 \\\\\n p \\div 2 \\times 2 &= 30 \\times 2 \\\\\n p &= 60\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n7. 5 \\times -2 = 6 + v",
    "answer_text": "$$\n\\begin{align}\n -10 &= 6 + v \\\\\n -10 - 6 &= 6 - 6 + v \\\\\n -16 &= v \\\\\n v &= -16\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n8. 2 \\times -6 = 24 \\div r",
    "answer_text": "$$\n\\begin{align}\n -12 &= 24 \\div r  \\\\\n -12 \\times r &= 24 \\div r \\times r \\\\\n -12 \\div -12 \\times r &= 24 \\div -12 \\\\\n r &= -2\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b031",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.4 Summary",
      "h3": null
    },
    "content_text": "- A closed number sentence is always true or always false.\n- In an open number sentence, there is some information missing that we need to find.\n- An open number sentence can use picture symbols or variables to show which information is missing.\n- The value of a variable can vary.\n- Finding the missing information, or finding the value of the variable, is called solving an open sentence.\n- We can solve an open sentence using mental maths or using the inverse operation.\n- We can use open sentences to solve problems described in words.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
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
