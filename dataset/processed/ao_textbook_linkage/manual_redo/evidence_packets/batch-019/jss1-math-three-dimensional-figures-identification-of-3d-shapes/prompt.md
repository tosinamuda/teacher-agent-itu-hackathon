# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-4",
  "topic_key": "jss1-math-three-dimensional-figures",
  "topic": "Three dimensional figures",
  "subtopic_id": "jss1-math-three-dimensional-figures-identification-of-3d-shapes",
  "subtopic_title": "Identification of three-dimensional shapes",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-three-dimensional-figures-identification-of-3d-shapes-po01",
        "source_performance_objective_index": 1,
        "text": "Identify common three-dimensional shapes"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "identification-of-3d-shapes-ao-identify-common-shapes",
          "text": "Identify common three-dimensional shapes."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-three-dimensional-figures-identification-of-3d-shapes-po02",
        "source_performance_objective_index": 2,
        "text": "Distinguish between 2D and 3D shapes"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "identification-of-3d-shapes-ao-distinguish-2d-and-3d",
          "text": "Distinguish between 2D and 3D shapes."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch13-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": null,
      "h3": null
    },
    "content_text": "A three-dimensional (3D) object has three dimensions that we can measure: length, breadth (or width), and height.\n\nYou will remember that a two-dimensional shape has only two dimensions that we can measure, which are length and breadth. So a two-dimensional shape is a shape on a flat surface.\n\nBut a three-dimensional object is like any object in the real world, such as a shoe, or a house, or a mobile phone. Three-dimensional objects are also called solid objects, because they stand up and have thickness.\n\nThe 3D objects that we will work with have specific properties.\n\n- Some 3D objects have flat faces, and others have curved faces.\n- The faces of some 3D objects are perpendicular to the base, and the faces of others tilt at an angle, to meet each other at a single point.\n\nYou will study the properties of different 3D objects in this chapter. Prisms (for example, cubes and cuboids), pyramids, cones, cylinders and spheres are all examples of 3D objects that have different properties.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-identification-of-3d-shapes"
  },
  {
    "record_id": "ch13-b047",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.5 Spheres",
      "h3": "Exercise 13.12: Describe the properties of 3D objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.12: Describe the properties of 3D objects",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-identification-of-3d-shapes"
  },
  {
    "record_id": "ch13-b047-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.5 Spheres",
      "h3": "Exercise 13.12: Describe the properties of 3D objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.12: Describe the properties of 3D objects\n\n1. Identify each of the 3D objects labelled A to F shown in the diagram.",
    "answer_text": "A: cube\nB: cuboid\nC: pyramid\nD: cone\nE: cylinder\nF: sphere",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-identification-of-3d-shapes"
  },
  {
    "record_id": "ch13-b047-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.5 Spheres",
      "h3": "Exercise 13.12: Describe the properties of 3D objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.12: Describe the properties of 3D objects\n\n2. Consider the following 3D objects: cube, cuboid, pyramid, cone, cylinder and sphere. Write the name of each of the 3D objects in the correct column of the table below.\n\n| Only flat faces | Only curved faces | Flat and curved faces |\n| --- | --- | --- |\n|  |  |  |",
    "answer_text": "| Only flat faces | Only curved faces | Flat and curved faces |\n| --- | --- | --- |\n| cube; cuboid; pyramid | sphere | cone; cylinder |",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-identification-of-3d-shapes"
  },
  {
    "record_id": "ch13-b047-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.5 Spheres",
      "h3": "Exercise 13.12: Describe the properties of 3D objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.12: Describe the properties of 3D objects\n\n3. Select a word from Column B that best fits the description in Column A.\n\n| Column A | Column B |\n| --- | --- |\n| a) A 3D object with no edges and no vertices. | A pyramid |\n| b) A 3D object formed by one square and four triangles. | B cone |\n| c) A 3D object with three pairs of equal rectangles. | C cube |\n| d) A 3D object formed by six squares. | D sphere |\n| e) A 3D object formed by one circle and one curved surface. | E cylinder |\n| f) A 3D object formed by two circles and one curved surface. | F cuboid |",
    "answer_text": "a) D\nb) A\nc) F\nd) C\ne) B\nf) E",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-identification-of-3d-shapes"
  },
  {
    "record_id": "ch13-b047-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.5 Spheres",
      "h3": "Exercise 13.12: Describe the properties of 3D objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.12: Describe the properties of 3D objects\n\n4. Complete the table below.\n\n| Name of 3D object | Number of faces | Number of edges | Number or vertices |\n| --- | --- | --- | --- |\n| cube |  |  |  |\n| cuboid |  |  |  |\n| pyramid (square as base) |  |  |  |\n| cone |  |  |  |\n| cylinder |  |  |  |\n| sphere |  |  |  |",
    "answer_text": "| Name of 3D object | Number of faces | Number of edges | Number or vertices |\n| --- | --- | --- | --- |\n| cube | 6 | 12 | 8 |\n| cuboid | 6 | 12 | 8 |\n| pyramid (square as base) | 5 | 8 | 5 |\n| cone | 2 | 1 | 1 |\n| cylinder | 3 | 2 | 0 |\n| sphere | 1 | 0 | 0 |",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-identification-of-3d-shapes"
  },
  {
    "record_id": "ch13-b053",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.7 Summary",
      "h3": null
    },
    "content_text": "A three-dimensional (3D) object has three dimensions that we can measure: length, breadth (or width), and height.\n\nWe use the main parts of a 3D object to describe its properties:\n- A 3D object has faces. The faces can be flat or curved.\n- The faces of a 3D object meet each other at an edge. The edge can be a straight line or a curve.\n- The edges of a 3D object meet each other at a vertex. (Vertex is singular and vertices are plural.)\n- The vertex at the top of a pyramid or a cone is called an apex.\n\n**Properties of 3D objects**\n\n- cube: 6 squares, 12 edges, 8 vertices\n- cuboid: 3 pairs of equal rectangles = 6 rectangles, 12 edges, 8 vertices\n- pyramid (square as base): 1 square + 4 triangles = 5 faces, 8 edges, 5 vertices\n- cone: 1 circle + 1 curved face = 2 faces, 1 edge, 1 vertex\n- cylinder: 2 circles + 1 curved face = 3 faces, 2 edges, 0 vertices\n- sphere: 1 curved face, 0 edges, 0 vertices\n\nVolume is the amount of space that an object takes up. It is measured in cubic units.\n\nThe volume of a prism is calculated using the formula $V_\\text{prism} = \\text{area of base} \\times \\text{height of the prism}$.\n\nA cube is a prism. The formula for the volume of a cube is $V_\\text{cube} = s \\times s \\times s\\\\$.\n\nA cuboid is a prism. The formula for the volume of a cuboid is $V_\\text{cuboid} = l \\times b \\times h$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-identification-of-3d-shapes"
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
  "theme_key": "jss1-theme-4",
  "topic_key": "jss1-math-three-dimensional-figures",
  "topic": "Three dimensional figures",
  "subtopic_id": "jss1-math-three-dimensional-figures-identification-of-3d-shapes",
  "subtopic_title": "Identification of three-dimensional shapes",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-three-dimensional-figures-identification-of-3d-shapes-po01",
        "source_performance_objective_index": 1,
        "text": "Identify common three-dimensional shapes"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "identification-of-3d-shapes-ao-identify-common-shapes",
          "text": "Identify common three-dimensional shapes."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-three-dimensional-figures-identification-of-3d-shapes-po02",
        "source_performance_objective_index": 2,
        "text": "Distinguish between 2D and 3D shapes"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "identification-of-3d-shapes-ao-distinguish-2d-and-3d",
          "text": "Distinguish between 2D and 3D shapes."
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
    "record_id": "ch13-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": null,
      "h3": null
    },
    "content_text": "A three-dimensional (3D) object has three dimensions that we can measure: length, breadth (or width), and height.\n\nYou will remember that a two-dimensional shape has only two dimensions that we can measure, which are length and breadth. So a two-dimensional shape is a shape on a flat surface.\n\nBut a three-dimensional object is like any object in the real world, such as a shoe, or a house, or a mobile phone. Three-dimensional objects are also called solid objects, because they stand up and have thickness.\n\nThe 3D objects that we will work with have specific properties.\n\n- Some 3D objects have flat faces, and others have curved faces.\n- The faces of some 3D objects are perpendicular to the base, and the faces of others tilt at an angle, to meet each other at a single point.\n\nYou will study the properties of different 3D objects in this chapter. Prisms (for example, cubes and cuboids), pyramids, cones, cylinders and spheres are all examples of 3D objects that have different properties.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-identification-of-3d-shapes"
  },
  {
    "record_id": "ch13-b047",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.5 Spheres",
      "h3": "Exercise 13.12: Describe the properties of 3D objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.12: Describe the properties of 3D objects",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-identification-of-3d-shapes"
  },
  {
    "record_id": "ch13-b047-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.5 Spheres",
      "h3": "Exercise 13.12: Describe the properties of 3D objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.12: Describe the properties of 3D objects\n\n1. Identify each of the 3D objects labelled A to F shown in the diagram.",
    "answer_text": "A: cube\nB: cuboid\nC: pyramid\nD: cone\nE: cylinder\nF: sphere",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-identification-of-3d-shapes"
  },
  {
    "record_id": "ch13-b047-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.5 Spheres",
      "h3": "Exercise 13.12: Describe the properties of 3D objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.12: Describe the properties of 3D objects\n\n2. Consider the following 3D objects: cube, cuboid, pyramid, cone, cylinder and sphere. Write the name of each of the 3D objects in the correct column of the table below.\n\n| Only flat faces | Only curved faces | Flat and curved faces |\n| --- | --- | --- |\n|  |  |  |",
    "answer_text": "| Only flat faces | Only curved faces | Flat and curved faces |\n| --- | --- | --- |\n| cube; cuboid; pyramid | sphere | cone; cylinder |",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-identification-of-3d-shapes"
  },
  {
    "record_id": "ch13-b047-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.5 Spheres",
      "h3": "Exercise 13.12: Describe the properties of 3D objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.12: Describe the properties of 3D objects\n\n3. Select a word from Column B that best fits the description in Column A.\n\n| Column A | Column B |\n| --- | --- |\n| a) A 3D object with no edges and no vertices. | A pyramid |\n| b) A 3D object formed by one square and four triangles. | B cone |\n| c) A 3D object with three pairs of equal rectangles. | C cube |\n| d) A 3D object formed by six squares. | D sphere |\n| e) A 3D object formed by one circle and one curved surface. | E cylinder |\n| f) A 3D object formed by two circles and one curved surface. | F cuboid |",
    "answer_text": "a) D\nb) A\nc) F\nd) C\ne) B\nf) E",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-identification-of-3d-shapes"
  },
  {
    "record_id": "ch13-b047-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.5 Spheres",
      "h3": "Exercise 13.12: Describe the properties of 3D objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.12: Describe the properties of 3D objects\n\n4. Complete the table below.\n\n| Name of 3D object | Number of faces | Number of edges | Number or vertices |\n| --- | --- | --- | --- |\n| cube |  |  |  |\n| cuboid |  |  |  |\n| pyramid (square as base) |  |  |  |\n| cone |  |  |  |\n| cylinder |  |  |  |\n| sphere |  |  |  |",
    "answer_text": "| Name of 3D object | Number of faces | Number of edges | Number or vertices |\n| --- | --- | --- | --- |\n| cube | 6 | 12 | 8 |\n| cuboid | 6 | 12 | 8 |\n| pyramid (square as base) | 5 | 8 | 5 |\n| cone | 2 | 1 | 1 |\n| cylinder | 3 | 2 | 0 |\n| sphere | 1 | 0 | 0 |",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-identification-of-3d-shapes"
  },
  {
    "record_id": "ch13-b053",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.7 Summary",
      "h3": null
    },
    "content_text": "A three-dimensional (3D) object has three dimensions that we can measure: length, breadth (or width), and height.\n\nWe use the main parts of a 3D object to describe its properties:\n- A 3D object has faces. The faces can be flat or curved.\n- The faces of a 3D object meet each other at an edge. The edge can be a straight line or a curve.\n- The edges of a 3D object meet each other at a vertex. (Vertex is singular and vertices are plural.)\n- The vertex at the top of a pyramid or a cone is called an apex.\n\n**Properties of 3D objects**\n\n- cube: 6 squares, 12 edges, 8 vertices\n- cuboid: 3 pairs of equal rectangles = 6 rectangles, 12 edges, 8 vertices\n- pyramid (square as base): 1 square + 4 triangles = 5 faces, 8 edges, 5 vertices\n- cone: 1 circle + 1 curved face = 2 faces, 1 edge, 1 vertex\n- cylinder: 2 circles + 1 curved face = 3 faces, 2 edges, 0 vertices\n- sphere: 1 curved face, 0 edges, 0 vertices\n\nVolume is the amount of space that an object takes up. It is measured in cubic units.\n\nThe volume of a prism is calculated using the formula $V_\\text{prism} = \\text{area of base} \\times \\text{height of the prism}$.\n\nA cube is a prism. The formula for the volume of a cube is $V_\\text{cube} = s \\times s \\times s\\\\$.\n\nA cuboid is a prism. The formula for the volume of a cuboid is $V_\\text{cuboid} = l \\times b \\times h$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-identification-of-3d-shapes"
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
