# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-1",
  "topic_key": "jss1-math-hcf",
  "topic": "HCF",
  "subtopic_id": "jss1-math-hcf-quantitative-reasoning",
  "subtopic_title": "Quantitative reasoning",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-hcf-quantitative-reasoning-po01",
        "source_performance_objective_index": 1,
        "text": "Solve problems on quantitative aptitude involving LCM and HCF of whole numbers"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "hcf-quantitative-reasoning-ao-solve-problems-lcm",
          "text": "Solve problems on quantitative aptitude involving LCM of whole numbers."
        },
        {
          "atomic_objective_id": "hcf-quantitative-reasoning-ao-solve-problems-hcf",
          "text": "Solve problems on quantitative aptitude involving HCF of whole numbers."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch02-b042",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Lowest common multiple",
      "h3": "2.4 Practical applications"
    },
    "content_text": "You can use your knowledge of factors and multiples to solve problems. Here are some hints:\n\n- Decide whether the problem is about factors or multiples. Factors divide into a given number. Multiples are the products of a given number and the natural numbers.\n- If you have to divide two or more amounts into smaller units, finding the HCF might solve the problem.\n- If you have to find a larger amount from smaller units, finding the LCM might solve the problem.\n- When you get stuck, list all the factors, or list the first ten multiples of the given numbers. Try to connect the lists to the question.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-hcf-quantitative-reasoning"
  },
  {
    "record_id": "ch02-b043",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Lowest common multiple",
      "h3": "Exercise 2.11: Use factors and multiples to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.11: Use factors and multiples to solve problems",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-hcf-quantitative-reasoning"
  },
  {
    "record_id": "ch02-b043-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Lowest common multiple",
      "h3": "Exercise 2.11: Use factors and multiples to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.11: Use factors and multiples to solve problems\n\n1. Chinasa is a student. This year, her age is a multiple of 6. Next year, her age will be a multiple of 5. If Chinasa is younger than 40, how old will she be next year?",
    "answer_text": "Multiples of 6 smaller than 40: $6;\\space 12;\\space 18;\\space 24;\\space 30;\\space 36$\nMultiples of 5 smaller than 40: $5;\\space 10;\\space 15;\\space 20;\\space 25;\\space 30;\\space 35$\n\nHer age next year must be one more than her age this year. The number 25 (a multiple of 5) is one more than the number 24 (a multiple of 6).\n\nTherefore, she will be 25 next year.",
    "primary_subtopic_id": "jss1-math-hcf-quantitative-reasoning"
  },
  {
    "record_id": "ch02-b043-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Lowest common multiple",
      "h3": "Exercise 2.11: Use factors and multiples to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.11: Use factors and multiples to solve problems\n\n2. Zahrah decides to sell sweets for extra pocket money. She buys a bag of chocolate bars and a bag of toffees. At home, she opens the bags and discovers that she has 24 chocolate bars and 80 toffees. She decides to make up smaller packets to sell. She divides all the sweets into packets that have equal amounts of chocolate bars and toffees. What is the maximum number of packets she can make up?",
    "answer_text": "Find the largest number that can divide into 24 and 80, that is, the HCF.\n\n$24=2^3 \\times 3$\n$80=2^4 \\times 5$\n\n$$\n\\text{HCF}=2^3=2 \\times 2 \\times 2=8\n$$\n\nTherefore, the maximum number of packets Zahrah can make up is 8.",
    "primary_subtopic_id": "jss1-math-hcf-quantitative-reasoning"
  },
  {
    "record_id": "ch02-b043-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Lowest common multiple",
      "h3": "Exercise 2.11: Use factors and multiples to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.11: Use factors and multiples to solve problems\n\n3. It is school holidays. Suleiman, Umar and Faruq want to earn some pocket money. They decide to wash cars on the days that they do not have chores to do at home. Suleiman washes 4 cars per day and Uman washes 5 cars per day. Faruq is the fastest and washes 6 cars per day. At the end of the holidays, they find to their surprise that each of them washed the same total number of cars over the holidays.\n\na. Determine the minimum number of cars each person could have washed over the holidays.\n\nb. Calculate how many days of the school holidays each person washed cars.",
    "answer_text": "a. Find the smallest number that is a multiple of 4, 5 and 6, that is, the LCM.\n\n$4=2 \\times 2$\n$5=5$\n$6=2\\times3$\n\n$$\n\\text{LCM}=2\\times 2 \\times 5 \\times3 = 60\n$$\n\nb. Suleiman: $\\frac{60}{4}=15$ days\n\nUmar: $\\frac{60}{5}=12$ days\n\nFaruq: $\\frac{60}{6}=10$ days",
    "primary_subtopic_id": "jss1-math-hcf-quantitative-reasoning"
  },
  {
    "record_id": "ch02-b043-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Lowest common multiple",
      "h3": "Exercise 2.11: Use factors and multiples to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.11: Use factors and multiples to solve problems\n\n4. Chika's family has a few dogs and a few chickens. They have a total of 8 animals. The animals have 22 legs altogether. How many dogs and how many chickens does the family have?",
    "answer_text": "$$\n\\begin{array}{l r r r r r r r r}\n\\text{number of chickens}\\space\\space&1&2&3&4&5&6&7 \\\\\n\\text{number of legs}\\space\\space&2&4&6&8&10&12&14 \\\\\n\\space \\\\\n\\text{number of dogs}\\space\\space&1&2&3&4&5&6&7 \\\\\n\\text{number of legs}\\space\\space&4&8&12&16&20&24&28 \\\\\n\\end{array}\n$$\n\n1 chicken and 7 dogs have $2+28=30$ legs\n2 chickens and 6 dogs have $4+24=28$ legs\n3 chickens and 5 dogs have $6+20=26$ legs\n4 chickens and 4 dogs have $8+16=24$ legs\n5 chickens and 3 dogs have $10+12=22$ legs",
    "primary_subtopic_id": "jss1-math-hcf-quantitative-reasoning"
  },
  {
    "record_id": "ch02-b043-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Lowest common multiple",
      "h3": "Exercise 2.11: Use factors and multiples to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.11: Use factors and multiples to solve problems\n\n5. A class of 26 boys and 39 girls must be divided into small groups for an activity.\n\na. If the teacher wants equal numbers of boys and girls in each group, what is the maximum number of groups she can form?\n\nb. How many boys and how many girls are in each group?\n\nc. After the first activity, the teacher realises that there should be only 2 boys and 2 girls in each group. She decides to form a few groups with only girls. How many additional groups with 4 girls in each can she form?\n\nd. Will there be any of the additional groups with more than 4 members?",
    "answer_text": "a. Find the largest number that can divide into 26 and 39, that is, the HCF.\n\n$26=2 \\times 13$\n$39=3 \\times 13$\n\n$$\n\\text{HCF}=13\n$$\n\nThe teacher can form 13 groups.\n\nb. $\\frac{26}{13}=2$ boys\n\n$\\frac{39}{13}=3$ girls\n\nc. There are $39-26=13$ girls to divide into groups.\n\n$$\n\\frac{13}{4}=3\\text{ remainder 1}\n$$\n\nShe can from 3 additional groups.\n\nd. Yes. One girl is left over, so one group will have 5 members.",
    "primary_subtopic_id": "jss1-math-hcf-quantitative-reasoning"
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
  "subtopic_id": "jss1-math-hcf-quantitative-reasoning",
  "subtopic_title": "Quantitative reasoning",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-hcf-quantitative-reasoning-po01",
        "source_performance_objective_index": 1,
        "text": "Solve problems on quantitative aptitude involving LCM and HCF of whole numbers"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "hcf-quantitative-reasoning-ao-solve-problems-lcm",
          "text": "Solve problems on quantitative aptitude involving LCM of whole numbers."
        },
        {
          "atomic_objective_id": "hcf-quantitative-reasoning-ao-solve-problems-hcf",
          "text": "Solve problems on quantitative aptitude involving HCF of whole numbers."
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
    "record_id": "ch02-b042",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Lowest common multiple",
      "h3": "2.4 Practical applications"
    },
    "content_text": "You can use your knowledge of factors and multiples to solve problems. Here are some hints:\n\n- Decide whether the problem is about factors or multiples. Factors divide into a given number. Multiples are the products of a given number and the natural numbers.\n- If you have to divide two or more amounts into smaller units, finding the HCF might solve the problem.\n- If you have to find a larger amount from smaller units, finding the LCM might solve the problem.\n- When you get stuck, list all the factors, or list the first ten multiples of the given numbers. Try to connect the lists to the question.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-hcf-quantitative-reasoning"
  },
  {
    "record_id": "ch02-b043",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Lowest common multiple",
      "h3": "Exercise 2.11: Use factors and multiples to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.11: Use factors and multiples to solve problems",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-hcf-quantitative-reasoning"
  },
  {
    "record_id": "ch02-b043-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Lowest common multiple",
      "h3": "Exercise 2.11: Use factors and multiples to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.11: Use factors and multiples to solve problems\n\n1. Chinasa is a student. This year, her age is a multiple of 6. Next year, her age will be a multiple of 5. If Chinasa is younger than 40, how old will she be next year?",
    "answer_text": "Multiples of 6 smaller than 40: $6;\\space 12;\\space 18;\\space 24;\\space 30;\\space 36$\nMultiples of 5 smaller than 40: $5;\\space 10;\\space 15;\\space 20;\\space 25;\\space 30;\\space 35$\n\nHer age next year must be one more than her age this year. The number 25 (a multiple of 5) is one more than the number 24 (a multiple of 6).\n\nTherefore, she will be 25 next year.",
    "primary_subtopic_id": "jss1-math-hcf-quantitative-reasoning"
  },
  {
    "record_id": "ch02-b043-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Lowest common multiple",
      "h3": "Exercise 2.11: Use factors and multiples to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.11: Use factors and multiples to solve problems\n\n2. Zahrah decides to sell sweets for extra pocket money. She buys a bag of chocolate bars and a bag of toffees. At home, she opens the bags and discovers that she has 24 chocolate bars and 80 toffees. She decides to make up smaller packets to sell. She divides all the sweets into packets that have equal amounts of chocolate bars and toffees. What is the maximum number of packets she can make up?",
    "answer_text": "Find the largest number that can divide into 24 and 80, that is, the HCF.\n\n$24=2^3 \\times 3$\n$80=2^4 \\times 5$\n\n$$\n\\text{HCF}=2^3=2 \\times 2 \\times 2=8\n$$\n\nTherefore, the maximum number of packets Zahrah can make up is 8.",
    "primary_subtopic_id": "jss1-math-hcf-quantitative-reasoning"
  },
  {
    "record_id": "ch02-b043-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Lowest common multiple",
      "h3": "Exercise 2.11: Use factors and multiples to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.11: Use factors and multiples to solve problems\n\n3. It is school holidays. Suleiman, Umar and Faruq want to earn some pocket money. They decide to wash cars on the days that they do not have chores to do at home. Suleiman washes 4 cars per day and Uman washes 5 cars per day. Faruq is the fastest and washes 6 cars per day. At the end of the holidays, they find to their surprise that each of them washed the same total number of cars over the holidays.\n\na. Determine the minimum number of cars each person could have washed over the holidays.\n\nb. Calculate how many days of the school holidays each person washed cars.",
    "answer_text": "a. Find the smallest number that is a multiple of 4, 5 and 6, that is, the LCM.\n\n$4=2 \\times 2$\n$5=5$\n$6=2\\times3$\n\n$$\n\\text{LCM}=2\\times 2 \\times 5 \\times3 = 60\n$$\n\nb. Suleiman: $\\frac{60}{4}=15$ days\n\nUmar: $\\frac{60}{5}=12$ days\n\nFaruq: $\\frac{60}{6}=10$ days",
    "primary_subtopic_id": "jss1-math-hcf-quantitative-reasoning"
  },
  {
    "record_id": "ch02-b043-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Lowest common multiple",
      "h3": "Exercise 2.11: Use factors and multiples to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.11: Use factors and multiples to solve problems\n\n4. Chika's family has a few dogs and a few chickens. They have a total of 8 animals. The animals have 22 legs altogether. How many dogs and how many chickens does the family have?",
    "answer_text": "$$\n\\begin{array}{l r r r r r r r r}\n\\text{number of chickens}\\space\\space&1&2&3&4&5&6&7 \\\\\n\\text{number of legs}\\space\\space&2&4&6&8&10&12&14 \\\\\n\\space \\\\\n\\text{number of dogs}\\space\\space&1&2&3&4&5&6&7 \\\\\n\\text{number of legs}\\space\\space&4&8&12&16&20&24&28 \\\\\n\\end{array}\n$$\n\n1 chicken and 7 dogs have $2+28=30$ legs\n2 chickens and 6 dogs have $4+24=28$ legs\n3 chickens and 5 dogs have $6+20=26$ legs\n4 chickens and 4 dogs have $8+16=24$ legs\n5 chickens and 3 dogs have $10+12=22$ legs",
    "primary_subtopic_id": "jss1-math-hcf-quantitative-reasoning"
  },
  {
    "record_id": "ch02-b043-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.4 Lowest common multiple",
      "h3": "Exercise 2.11: Use factors and multiples to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.11: Use factors and multiples to solve problems\n\n5. A class of 26 boys and 39 girls must be divided into small groups for an activity.\n\na. If the teacher wants equal numbers of boys and girls in each group, what is the maximum number of groups she can form?\n\nb. How many boys and how many girls are in each group?\n\nc. After the first activity, the teacher realises that there should be only 2 boys and 2 girls in each group. She decides to form a few groups with only girls. How many additional groups with 4 girls in each can she form?\n\nd. Will there be any of the additional groups with more than 4 members?",
    "answer_text": "a. Find the largest number that can divide into 26 and 39, that is, the HCF.\n\n$26=2 \\times 13$\n$39=3 \\times 13$\n\n$$\n\\text{HCF}=13\n$$\n\nThe teacher can form 13 groups.\n\nb. $\\frac{26}{13}=2$ boys\n\n$\\frac{39}{13}=3$ girls\n\nc. There are $39-26=13$ girls to divide into groups.\n\n$$\n\\frac{13}{4}=3\\text{ remainder 1}\n$$\n\nShe can from 3 additional groups.\n\nd. Yes. One girl is left over, so one group will have 5 members.",
    "primary_subtopic_id": "jss1-math-hcf-quantitative-reasoning"
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
