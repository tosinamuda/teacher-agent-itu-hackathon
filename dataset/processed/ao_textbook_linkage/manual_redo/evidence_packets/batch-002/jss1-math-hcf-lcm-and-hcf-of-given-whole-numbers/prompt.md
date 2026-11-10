# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-1",
  "topic_key": "jss1-math-hcf",
  "topic": "HCF",
  "subtopic_id": "jss1-math-hcf-lcm-and-hcf-of-given-whole-numbers",
  "subtopic_title": "LCM and HCF of given whole numbers",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-hcf-lcm-and-hcf-of-given-whole-numbers-po01",
        "source_performance_objective_index": 1,
        "text": "Identify the difference between LCM and HCF"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "lcm-and-hcf-ao-identify-difference",
          "text": "Identify the difference between LCM and HCF."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch02-b039",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.3 Compare HCF and LCM",
      "h3": null
    },
    "content_text": "Be careful to not confuse HCF and LCM. The differences are listed in the table.\n\n| HCF (highest common factor) | LCM (lowest common multiple) |\n| --- | --- |\n| A factor of two or more numbers | A multiple of two of more numbers |\n| HCF must divide into the given numbers | Given numbers must divide into LCM |\n| Only common prime factors to lowest index | All prime factors to highest index |\n| Smaller than or equal to given numbers | Larger than or equal to given numbers |",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-hcf-lcm-and-hcf-of-given-whole-numbers"
  },
  {
    "record_id": "ch02-b040",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.3 Compare HCF and LCM",
      "h3": "Worked example 2.10: HCF and LCM"
    },
    "content_text": "Source math retained:\n\begin{array}{r | r} 2 & 24 ewline \\hline 2 & 12 ewline \\hline 2 & 6 ewline \\hline 3 & 3 ewline \\hline & 1 \\end{array}\n24=2^3 imes 3\n\begin{array}{r | r} 2 & 32 ewline \\hline 2 & 16 ewline \\hline 2 & 8 ewline \\hline 2 & 4 ewline \\hline 2 & 2 ewline \\hline & 1 \\end{array}\n32=2^5\n2^3\n2^5 imes3\n2 imes2 imes2=8\n2 imes2 imes2 imes2 imes2 imes3=96",
    "prompt_text": "Find the HCF and the LCM of 24 and 32.",
    "answer_text": "Step 1: Express each number as a product of prime factors in index form.\n\n$$\\begin{array}{r | r}\n 2 & 24 \\\\\n \\hline\n 2 & 12 \\\\\n \\hline\n 2 & 6 \\\\\n \\hline\n 3 & 3 \\\\\n \\hline\n & 1\n \\end{array}$$\n\n$$24=2^3 \\times 3$$\n\n$$\\begin{array}{r | r}\n 2 & 32 \\\\\n \\hline\n 2 & 16 \\\\\n \\hline\n 2 & 8 \\\\\n \\hline\n 2 & 4 \\\\\n \\hline\n 2 & 2 \\\\\n \\hline\n & 1\n \\end{array}$$\n\n$$32=2^5$$\n\nStep 2: For the HCF, identify the common prime factors to the lowest index. For the LCM, list all the prime factors to the highest index.\n\n| HCF | LCM |\n| --- | --- |\n| $2^3$ | $2^5\\times3$ |\n| $2\\times2\\times2=8$ | $2\\times2\\times2\\times2\\times2\\times3=96$ |\n| Largest number that can divide into 24 and 32 | Smallest number into which 24 and 32 can divide |",
    "primary_subtopic_id": "jss1-math-hcf-lcm-and-hcf-of-given-whole-numbers"
  },
  {
    "record_id": "ch02-b041",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Lowest common multiple",
      "h3": "Exercise 2.10: Determine HCF and LCM"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.10: Determine HCF and LCM\n\nThe prime factorisation of three numbers are as follows:\n\n$2^2 \\times 3 \\times 5$\n$2^3 \\times 3 \\times 5$\n$2^2 \\times 3^2 \\times 5$",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-hcf-lcm-and-hcf-of-given-whole-numbers"
  },
  {
    "record_id": "ch02-b041-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Lowest common multiple",
      "h3": "Exercise 2.10: Determine HCF and LCM"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.10: Determine HCF and LCM\n\n1. Determine the LCM of the three numbers.",
    "answer_text": "$$\n\\text{LCM}=2^3 \\times 3^2 \\times 5=2 \\times 2 \\times 2 \\times 3 \\times 3 \\times 5=360\n$$",
    "primary_subtopic_id": "jss1-math-hcf-lcm-and-hcf-of-given-whole-numbers"
  },
  {
    "record_id": "ch02-b041-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Lowest common multiple",
      "h3": "Exercise 2.10: Determine HCF and LCM"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.10: Determine HCF and LCM\n\n2. Determine the HCF of the three numbers.",
    "answer_text": "$$\n\\text{HCF}=2^2 \\times 3 \\times 5=60\n$$",
    "primary_subtopic_id": "jss1-math-hcf-lcm-and-hcf-of-given-whole-numbers"
  },
  {
    "record_id": "ch02-b041-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Lowest common multiple",
      "h3": "Exercise 2.10: Determine HCF and LCM"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.10: Determine HCF and LCM\n\n3. Apart from the HCF, identify another common factor for the three numbers.",
    "answer_text": "$$\n2 \\times 3 \\times 5 = 30\n$$",
    "primary_subtopic_id": "jss1-math-hcf-lcm-and-hcf-of-given-whole-numbers"
  },
  {
    "record_id": "ch02-b041-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Lowest common multiple",
      "h3": "Exercise 2.10: Determine HCF and LCM"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.10: Determine HCF and LCM\n\n4. Calculate the three original numbers.",
    "answer_text": "$2^2 \\times 3 \\times 5 = 60$\n$2^3 \\times 3 \\times 5 = 120$\n$2^2 \\times 3^2 \\times 5= 180$",
    "primary_subtopic_id": "jss1-math-hcf-lcm-and-hcf-of-given-whole-numbers"
  },
  {
    "record_id": "ch02-b044",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Summary",
      "h3": "2.4 Summary"
    },
    "content_text": "- A factor is a whole number that divides into a larger number without a remainder. For example, 4 is a factor of 24.\n- A prime factor is a factor that is also a prime number. For example, 3 is a prime factor of 24, but 8 is not a prime factor.\n- We can express any non-prime number as a product of its prime factors. For example, 24 can be expressed as $2\\times 2\\times 2\\times 3$.\n- Index form is a way of writing as a superscript how many times a number is multiplied by itself. For example, $3^4$ means $3\\times 3\\times 3\\times 3$.\n- A common factor of two or more numbers is a factor of all the numbers. For example, 4 is a common factor of 8, 24 and 60.\n- The highest common factor (HCF) of two or more numbers is the largest factor of all the numbers. For example, 2 is a common factor of 12, 24 and 60, but 4 is the highest common factor of the three numbers.\n- A multiple is a whole number into which a smaller number divides without a remainder. For example, 24 is a multiple of 4.\n- A common multiple of two or more numbers is a multiple of all the numbers. For example, 24 is a common multiple of the numbers 2, 3, 4 and 6.\n- The lowest common multiple (LCM) of two or more numbers is the smallest whole number that is a multiple of all the numbers. For example, 24 is a common multiple of 3, 4 and 6, but 12 is the lowest common multiple of the three numbers.\n- When we express two or more numbers as prime factors in index form:\n  - the HCF is the product of the common prime factors to the lowest index\n  - the LCM is the product of all the prime factors to the highest index.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-hcf-lcm-and-hcf-of-given-whole-numbers"
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
  "theme_key": "jss1-theme-1",
  "topic_key": "jss1-math-hcf",
  "topic": "HCF",
  "subtopic_id": "jss1-math-hcf-lcm-and-hcf-of-given-whole-numbers",
  "subtopic_title": "LCM and HCF of given whole numbers",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-hcf-lcm-and-hcf-of-given-whole-numbers-po01",
        "source_performance_objective_index": 1,
        "text": "Identify the difference between LCM and HCF"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "lcm-and-hcf-ao-identify-difference",
          "text": "Identify the difference between LCM and HCF."
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
    "record_id": "ch02-b039",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.3 Compare HCF and LCM",
      "h3": null
    },
    "content_text": "Be careful to not confuse HCF and LCM. The differences are listed in the table.\n\n| HCF (highest common factor) | LCM (lowest common multiple) |\n| --- | --- |\n| A factor of two or more numbers | A multiple of two of more numbers |\n| HCF must divide into the given numbers | Given numbers must divide into LCM |\n| Only common prime factors to lowest index | All prime factors to highest index |\n| Smaller than or equal to given numbers | Larger than or equal to given numbers |",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-hcf-lcm-and-hcf-of-given-whole-numbers"
  },
  {
    "record_id": "ch02-b040",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.3 Compare HCF and LCM",
      "h3": "Worked example 2.10: HCF and LCM"
    },
    "content_text": "Source math retained:\n\begin{array}{r | r} 2 & 24 ewline \\hline 2 & 12 ewline \\hline 2 & 6 ewline \\hline 3 & 3 ewline \\hline & 1 \\end{array}\n24=2^3 imes 3\n\begin{array}{r | r} 2 & 32 ewline \\hline 2 & 16 ewline \\hline 2 & 8 ewline \\hline 2 & 4 ewline \\hline 2 & 2 ewline \\hline & 1 \\end{array}\n32=2^5\n2^3\n2^5 imes3\n2 imes2 imes2=8\n2 imes2 imes2 imes2 imes2 imes3=96",
    "prompt_text": "Find the HCF and the LCM of 24 and 32.",
    "answer_text": "Step 1: Express each number as a product of prime factors in index form.\n\n$$\\begin{array}{r | r}\n 2 & 24 \\\\\n \\hline\n 2 & 12 \\\\\n \\hline\n 2 & 6 \\\\\n \\hline\n 3 & 3 \\\\\n \\hline\n & 1\n \\end{array}$$\n\n$$24=2^3 \\times 3$$\n\n$$\\begin{array}{r | r}\n 2 & 32 \\\\\n \\hline\n 2 & 16 \\\\\n \\hline\n 2 & 8 \\\\\n \\hline\n 2 & 4 \\\\\n \\hline\n 2 & 2 \\\\\n \\hline\n & 1\n \\end{array}$$\n\n$$32=2^5$$\n\nStep 2: For the HCF, identify the common prime factors to the lowest index. For the LCM, list all the prime factors to the highest index.\n\n| HCF | LCM |\n| --- | --- |\n| $2^3$ | $2^5\\times3$ |\n| $2\\times2\\times2=8$ | $2\\times2\\times2\\times2\\times2\\times3=96$ |\n| Largest number that can divide into 24 and 32 | Smallest number into which 24 and 32 can divide |",
    "primary_subtopic_id": "jss1-math-hcf-lcm-and-hcf-of-given-whole-numbers"
  },
  {
    "record_id": "ch02-b041",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Lowest common multiple",
      "h3": "Exercise 2.10: Determine HCF and LCM"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.10: Determine HCF and LCM\n\nThe prime factorisation of three numbers are as follows:\n\n$2^2 \\times 3 \\times 5$\n$2^3 \\times 3 \\times 5$\n$2^2 \\times 3^2 \\times 5$",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-hcf-lcm-and-hcf-of-given-whole-numbers"
  },
  {
    "record_id": "ch02-b041-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Lowest common multiple",
      "h3": "Exercise 2.10: Determine HCF and LCM"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.10: Determine HCF and LCM\n\n1. Determine the LCM of the three numbers.",
    "answer_text": "$$\n\\text{LCM}=2^3 \\times 3^2 \\times 5=2 \\times 2 \\times 2 \\times 3 \\times 3 \\times 5=360\n$$",
    "primary_subtopic_id": "jss1-math-hcf-lcm-and-hcf-of-given-whole-numbers"
  },
  {
    "record_id": "ch02-b041-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Lowest common multiple",
      "h3": "Exercise 2.10: Determine HCF and LCM"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.10: Determine HCF and LCM\n\n2. Determine the HCF of the three numbers.",
    "answer_text": "$$\n\\text{HCF}=2^2 \\times 3 \\times 5=60\n$$",
    "primary_subtopic_id": "jss1-math-hcf-lcm-and-hcf-of-given-whole-numbers"
  },
  {
    "record_id": "ch02-b041-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Lowest common multiple",
      "h3": "Exercise 2.10: Determine HCF and LCM"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.10: Determine HCF and LCM\n\n3. Apart from the HCF, identify another common factor for the three numbers.",
    "answer_text": "$$\n2 \\times 3 \\times 5 = 30\n$$",
    "primary_subtopic_id": "jss1-math-hcf-lcm-and-hcf-of-given-whole-numbers"
  },
  {
    "record_id": "ch02-b041-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Lowest common multiple",
      "h3": "Exercise 2.10: Determine HCF and LCM"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.10: Determine HCF and LCM\n\n4. Calculate the three original numbers.",
    "answer_text": "$2^2 \\times 3 \\times 5 = 60$\n$2^3 \\times 3 \\times 5 = 120$\n$2^2 \\times 3^2 \\times 5= 180$",
    "primary_subtopic_id": "jss1-math-hcf-lcm-and-hcf-of-given-whole-numbers"
  },
  {
    "record_id": "ch02-b044",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Summary",
      "h3": "2.4 Summary"
    },
    "content_text": "- A factor is a whole number that divides into a larger number without a remainder. For example, 4 is a factor of 24.\n- A prime factor is a factor that is also a prime number. For example, 3 is a prime factor of 24, but 8 is not a prime factor.\n- We can express any non-prime number as a product of its prime factors. For example, 24 can be expressed as $2\\times 2\\times 2\\times 3$.\n- Index form is a way of writing as a superscript how many times a number is multiplied by itself. For example, $3^4$ means $3\\times 3\\times 3\\times 3$.\n- A common factor of two or more numbers is a factor of all the numbers. For example, 4 is a common factor of 8, 24 and 60.\n- The highest common factor (HCF) of two or more numbers is the largest factor of all the numbers. For example, 2 is a common factor of 12, 24 and 60, but 4 is the highest common factor of the three numbers.\n- A multiple is a whole number into which a smaller number divides without a remainder. For example, 24 is a multiple of 4.\n- A common multiple of two or more numbers is a multiple of all the numbers. For example, 24 is a common multiple of the numbers 2, 3, 4 and 6.\n- The lowest common multiple (LCM) of two or more numbers is the smallest whole number that is a multiple of all the numbers. For example, 24 is a common multiple of 3, 4 and 6, but 12 is the lowest common multiple of the three numbers.\n- When we express two or more numbers as prime factors in index form:\n  - the HCF is the product of the common prime factors to the lowest index\n  - the LCM is the product of all the prime factors to the highest index.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-hcf-lcm-and-hcf-of-given-whole-numbers"
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
