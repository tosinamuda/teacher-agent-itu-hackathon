# Atomic Objective Specification

Status: Manual authoring specification. This document defines how to decompose a curriculum performance objective into atomic objectives. Whole Numbers examples are included only to illustrate the rule.

## Definition

An atomic objective is the smallest teachable, observable, and assessable learner outcome that can be traced directly to one source performance objective.

## Core Rule

Atomic decomposition is a splitting exercise, not an expansion exercise.

- Split the source objective into smaller objectives.
- Preserve the original meaning and wording as closely as possible.
- Do not add new actions, directions, representations, tools, or constraints that are not stated in the source text.

## Authoring Rules

- One main action per atomic objective.
- One content scope per atomic objective.
- If the source objective contains multiple actions, split by action.
- If the source objective contains multiple distinct scopes, split by scope.
- If both are present, produce one valid action-scope objective for each combination stated by the source.
- If the source objective already has one main action and one clear scope, keep it as one atomic objective.
- Write each atomic objective as a short learner-outcome sentence.

## What Not To Invent

The author must not enrich the source objective during decomposition.

Do not introduce wording such as:

- `forward and backward`
- `in numerals and words`
- `with a place-value table`
- `compare`
- `convert`
- `interpret`
- `multi-step`

unless that wording already exists in the source objective.

## Recommended Output Shape

For manual authoring, the recommended review shape is:

```json
{
  "subtopic_id": "jss1-math-whole-numbers-millions-and-billions",
  "subtopic_title": "Millions and billions",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-whole-numbers-millions-and-billions-po01",
        "source_performance_objective_index": 1,
        "text": "Count and write in millions and billions"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "millions-and-billions-ao-count-millions",
          "text": "Count in millions."
        },
        {
          "atomic_objective_id": "millions-and-billions-ao-count-billions",
          "text": "Count in billions."
        }
      ]
    }
  ]
}
```

Required fields:

- `source.curriculum_objective_id`
- `source.source_performance_objective_index`
- `source.text`
- `atomic_decomposition[].atomic_objective_id`
- `atomic_decomposition[].text`

Bloom metadata and ordering metadata are deferred to a later pass. They are not part of this manual decomposition artifact.

## Whole Numbers Examples

### Example 1

Source performance objective:

`Count and write in millions and billions`

Valid nested decomposition:

```json
{
  "source": {
    "curriculum_objective_id": "jss1-math-whole-numbers-millions-and-billions-po01",
    "source_performance_objective_index": 1,
    "text": "Count and write in millions and billions"
  },
  "atomic_decomposition": [
    {
      "atomic_objective_id": "millions-and-billions-ao-count-millions",
      "text": "Count in millions."
    },
    {
      "atomic_objective_id": "millions-and-billions-ao-count-billions",
      "text": "Count in billions."
    },
    {
      "atomic_objective_id": "millions-and-billions-ao-write-millions",
      "text": "Write in millions."
    },
    {
      "atomic_objective_id": "millions-and-billions-ao-write-billions",
      "text": "Write in billions."
    }
  ]
}
```

Invalid decomposition:

- `Count forward and backward in millions.`
- `Write whole numbers in millions in numerals and words.`

These are invalid because they add details that are not stated in the source objective.

### Example 2

Source performance objective:

`Count and write in trillions`

Valid nested decomposition:

```json
{
  "source": {
    "curriculum_objective_id": "jss1-math-whole-numbers-trillions-po01",
    "source_performance_objective_index": 1,
    "text": "Count and write in trillions"
  },
  "atomic_decomposition": [
    {
      "atomic_objective_id": "trillions-ao-count-trillions",
      "text": "Count in trillions."
    },
    {
      "atomic_objective_id": "trillions-ao-write-trillions",
      "text": "Write in trillions."
    }
  ]
}
```

### Example 3

Source performance objective:

`Apply the counting, writing, and reading of large numbers in everyday life`

Valid nested decomposition:

```json
{
  "source": {
    "curriculum_objective_id": "jss1-math-whole-numbers-trillions-po02",
    "source_performance_objective_index": 2,
    "text": "Apply the counting, writing, and reading of large numbers in everyday life"
  },
  "atomic_decomposition": [
    {
      "atomic_objective_id": "everyday-life-ao-apply-counting-large-numbers",
      "text": "Apply counting of large numbers in everyday life."
    },
    {
      "atomic_objective_id": "everyday-life-ao-apply-writing-large-numbers",
      "text": "Apply writing of large numbers in everyday life."
    },
    {
      "atomic_objective_id": "everyday-life-ao-apply-reading-large-numbers",
      "text": "Apply reading of large numbers in everyday life."
    }
  ]
}
```

This objective is split by the three actions already named in the source. It must not be rewritten as `interpret large numbers with a place-value table` because that adds a method that the source objective does not state.

### Example 4

Source performance objective:

`Solve problems in quantitative aptitude reasoning using large numbers`

Valid nested decomposition:

```json
{
  "source": {
    "curriculum_objective_id": "jss1-math-whole-numbers-quantitative-reasoning-po01",
    "source_performance_objective_index": 1,
    "text": "Solve problems in quantitative aptitude reasoning using large numbers"
  },
  "atomic_decomposition": [
    {
      "atomic_objective_id": "quantitative-reasoning-ao-solve-large-number-problems",
      "text": "Solve problems in quantitative aptitude reasoning using large numbers."
    }
  ]
}
```

This remains a single atomic objective because the source already expresses one main action and one content scope.
