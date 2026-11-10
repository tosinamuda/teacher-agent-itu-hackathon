# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-1",
  "topic_key": "jss1-math-fractions",
  "topic": "Fractions",
  "subtopic_id": "jss1-math-fractions-meaning-of-fraction",
  "subtopic_title": "Meaning of fraction",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-fractions-meaning-of-fraction-po01",
        "source_performance_objective_index": 1,
        "text": "Explain the meaning of a fraction"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "meaning-of-fraction-ao-explain-meaning",
          "text": "Explain the meaning of a fraction."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-fractions-meaning-of-fraction-po02",
        "source_performance_objective_index": 2,
        "text": "Identify parts of a fraction (numerator and denominator)"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "meaning-of-fraction-ao-identify-numerator",
          "text": "Identify the numerator of a fraction."
        },
        {
          "atomic_objective_id": "meaning-of-fraction-ao-identify-denominator",
          "text": "Identify the denominator of a fraction."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch01-b013",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Place value in decimal fractions"
    },
    "content_text": "A fraction means a part of a whole. One way to write a fraction is to write one whole number on top of another whole number with a dividing line between them. For example, $\\frac{2}{10}$ means two parts of a whole that is divided in ten.\nThe name of the top number is the numerator, and the name of the bottom number is the denominator: $\\dfrac{\\text{numerator}}{\\text{denominator}}$\n\nA **decimal fraction** is a way to write a fraction using the base ten number system. Instead of writing one number on top of another, we write only the numerator after a decimal point. For example, the decimal fraction 0.2 means the numerator is 2 and the denominator is 10, so we may write it as $\\frac{2}{10}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-decimals-and-vice-versa"
  },
  {
    "record_id": "ch04-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.1 Types of fractions",
      "h3": null
    },
    "content_text": "A fraction is part of a whole. There are different ways to write fractions. One way is to write the fraction as one whole number on top of another whole number with a dividing line between, as $\\frac{\\text{numerator}}{\\text{denominator}}$.\n\nThe bottom number is called the denominator. It represents all the parts that the whole is divided into. The top number is called the numerator. It represents only the parts of the whole we are dealing with. Fractions that are written like this are called common fractions.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-meaning-of-fraction"
  },
  {
    "record_id": "ch04-b002",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.1 Types of fractions",
      "h3": "4.1 Types of fractions"
    },
    "content_text": "**fraction** A fraction is a part of a whole.\n\n**denominator** The denominator is the number written below the line in a fraction; it represents all the parts of a whole.\n\n**numerator** The numerator is the number written above the line in a fraction; it represents only the parts of a whole we are dealing with.\n\n**common fraction** A common fraction is a fraction that is written in the form $\\frac{\\text{numerator}}{\\text{denominator}}$, where the numerator and denominator are both whole numbers.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-meaning-of-fraction"
  },
  {
    "record_id": "ch04-b003",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.1 Types of fractions",
      "h3": "4.1 Types of fractions"
    },
    "content_text": "For example, if you cut a cake into seven pieces, you can say that the whole cake is made up of $\\frac{7}{7}$.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-001.png)\n\nSuppose you eat two of the pieces.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-002.png)\n\n- The fraction of the cake you ate is $\\frac{2}{7}$. The denominator shows that the cake was cut into 7 pieces. The numerator shows that 2 pieces were eaten.\n- The fraction of the cake that is left over is $\\frac{5}{7}$. The denominator still shows that the cake was cut into 7 pieces. The numerator now shows that 5 pieces are left over.\n\nThe fractions $\\frac{2}{7}$ and $\\frac{5}{7}$ are **proper fractions**. A proper fraction is smaller than 1. Its numerator is smaller than its denominator.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-meaning-of-fraction"
  },
  {
    "record_id": "ch04-b058",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.7 Summary",
      "h3": null
    },
    "content_text": "- A common fraction is written as $\\frac{\\text{numerator}}{\\text{denominator}}$.\n- A proper fraction is smaller than 1, for example $\\frac{2}{7}$.\n- A mixed number consists of a whole number and a proper fraction, for example $5\\frac{1}{6}$.\n- An improper fraction is larger than 1, for example $\\frac{9}{4}$.\n- Equivalent fractions have different numerators and denominators but the same value, for example $\\frac{1}{2}=\\frac{2}{4}=\\frac{4}{8}$.\n- A fraction is in its simplest form when the numerator and denominator have no common factor.\n- To compare fractions, we must express them with the same denominators. The lowest common denominator is the smallest whole number into which all the denominators can divide without a remainder.\n- A decimal fraction is written in decimal notation, where the numerator is written after a decimal point and the denominator is a power of ten.\n- In decimal notation, the decimal point separates whole numbers from fractions.\n- If there are three digits after the decimal point, the denominator is $10\\times10\\times10=1,000$.\n- A percentage is a fraction with denominator 100, written with only the numerator followed by a percentage symbol.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
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
  "topic_key": "jss1-math-fractions",
  "topic": "Fractions",
  "subtopic_id": "jss1-math-fractions-meaning-of-fraction",
  "subtopic_title": "Meaning of fraction",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-fractions-meaning-of-fraction-po01",
        "source_performance_objective_index": 1,
        "text": "Explain the meaning of a fraction"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "meaning-of-fraction-ao-explain-meaning",
          "text": "Explain the meaning of a fraction."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-fractions-meaning-of-fraction-po02",
        "source_performance_objective_index": 2,
        "text": "Identify parts of a fraction (numerator and denominator)"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "meaning-of-fraction-ao-identify-numerator",
          "text": "Identify the numerator of a fraction."
        },
        {
          "atomic_objective_id": "meaning-of-fraction-ao-identify-denominator",
          "text": "Identify the denominator of a fraction."
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
    "record_id": "ch01-b013",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Place value in decimal fractions"
    },
    "content_text": "A fraction means a part of a whole. One way to write a fraction is to write one whole number on top of another whole number with a dividing line between them. For example, $\\frac{2}{10}$ means two parts of a whole that is divided in ten.\nThe name of the top number is the numerator, and the name of the bottom number is the denominator: $\\dfrac{\\text{numerator}}{\\text{denominator}}$\n\nA **decimal fraction** is a way to write a fraction using the base ten number system. Instead of writing one number on top of another, we write only the numerator after a decimal point. For example, the decimal fraction 0.2 means the numerator is 2 and the denominator is 10, so we may write it as $\\frac{2}{10}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-decimals-and-vice-versa"
  },
  {
    "record_id": "ch04-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.1 Types of fractions",
      "h3": null
    },
    "content_text": "A fraction is part of a whole. There are different ways to write fractions. One way is to write the fraction as one whole number on top of another whole number with a dividing line between, as $\\frac{\\text{numerator}}{\\text{denominator}}$.\n\nThe bottom number is called the denominator. It represents all the parts that the whole is divided into. The top number is called the numerator. It represents only the parts of the whole we are dealing with. Fractions that are written like this are called common fractions.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-meaning-of-fraction"
  },
  {
    "record_id": "ch04-b002",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.1 Types of fractions",
      "h3": "4.1 Types of fractions"
    },
    "content_text": "**fraction** A fraction is a part of a whole.\n\n**denominator** The denominator is the number written below the line in a fraction; it represents all the parts of a whole.\n\n**numerator** The numerator is the number written above the line in a fraction; it represents only the parts of a whole we are dealing with.\n\n**common fraction** A common fraction is a fraction that is written in the form $\\frac{\\text{numerator}}{\\text{denominator}}$, where the numerator and denominator are both whole numbers.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-meaning-of-fraction"
  },
  {
    "record_id": "ch04-b003",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.1 Types of fractions",
      "h3": "4.1 Types of fractions"
    },
    "content_text": "For example, if you cut a cake into seven pieces, you can say that the whole cake is made up of $\\frac{7}{7}$.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-001.png)\n\nSuppose you eat two of the pieces.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-002.png)\n\n- The fraction of the cake you ate is $\\frac{2}{7}$. The denominator shows that the cake was cut into 7 pieces. The numerator shows that 2 pieces were eaten.\n- The fraction of the cake that is left over is $\\frac{5}{7}$. The denominator still shows that the cake was cut into 7 pieces. The numerator now shows that 5 pieces are left over.\n\nThe fractions $\\frac{2}{7}$ and $\\frac{5}{7}$ are **proper fractions**. A proper fraction is smaller than 1. Its numerator is smaller than its denominator.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-meaning-of-fraction"
  },
  {
    "record_id": "ch04-b058",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.7 Summary",
      "h3": null
    },
    "content_text": "- A common fraction is written as $\\frac{\\text{numerator}}{\\text{denominator}}$.\n- A proper fraction is smaller than 1, for example $\\frac{2}{7}$.\n- A mixed number consists of a whole number and a proper fraction, for example $5\\frac{1}{6}$.\n- An improper fraction is larger than 1, for example $\\frac{9}{4}$.\n- Equivalent fractions have different numerators and denominators but the same value, for example $\\frac{1}{2}=\\frac{2}{4}=\\frac{4}{8}$.\n- A fraction is in its simplest form when the numerator and denominator have no common factor.\n- To compare fractions, we must express them with the same denominators. The lowest common denominator is the smallest whole number into which all the denominators can divide without a remainder.\n- A decimal fraction is written in decimal notation, where the numerator is written after a decimal point and the denominator is a power of ten.\n- In decimal notation, the decimal point separates whole numbers from fractions.\n- If there are three digits after the decimal point, the denominator is $10\\times10\\times10=1,000$.\n- A percentage is a fraction with denominator 100, written with only the numerator followed by a percentage symbol.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
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
