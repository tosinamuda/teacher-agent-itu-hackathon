# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-2",
  "topic_key": "jss1-math-approximation",
  "topic": "Approximation",
  "subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000",
  "subtopic_title": "Rounding off numbers to the nearest 10, 100 and 1000",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000-po01",
        "source_performance_objective_index": 1,
        "text": "Round numbers to the nearest 10, 100, and 1000"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-10",
          "text": "Round numbers to the nearest 10."
        },
        {
          "atomic_objective_id": "rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-100",
          "text": "Round numbers to the nearest 100."
        },
        {
          "atomic_objective_id": "rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-1000",
          "text": "Round numbers to the nearest 1000."
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
    "record_id": "ch07-b024",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Rounding off numbers"
    },
    "content_text": "When we round off numbers, we make them less exact, but easier to work with. We usually round off a number to a specific multiple of 10.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b025",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Rounding off numbers"
    },
    "content_text": "rounding off Rounding off is the process of making a number less exact but easier to work with, by adjusting it to a specific multiple of 10.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b026",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Rounding off numbers"
    },
    "content_text": "When we round off a number to a specific multiple of 10, we have to identify the digit that represents the multiple, and then determine whether than digit remains the same or increases by one.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b027",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Worked example 7.4: Rounding off to the nearest ten"
    },
    "content_text": "",
    "prompt_text": "A smartphone is advertised for ₦47,689. Round off this number to the nearest ten.",
    "answer_text": "Step 1: Write down half of the required multiple of 10.\n\n$$\n\\frac{1}{2}\\times 10=5\n$$\n\nStep 2: Determine which digit represents the required multiple of 10.\n\nYou may use a place value table to help you with this:\n\n$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|}\n\\hline\n\\text{billion} & \\text{hm} & \\text{tm} & \\text{million} &\\text{hth} & \\text{tth} & \\text{thousand} & \\text{ h } & \\text{ t } & \\text{ u }  \\\\\n\\hline\n& & & & & 4 & 7 & 6 & 8 & 9     \\\\\n\\hline\n\\end{array}\n$$\n\nThe 8 represents ten.\n\nStep 3: Consider the digits to the right of the one you identified in Step 2. If they are less than the value in Step 1, the digit you identified remains the same. If they are equal to or more than the value in Step 1, the digit you identified increases by 1.\n\nThe digit to the right of the 8 is 9.\n9&amp;gt;5\nThe 8 increases to a 9.\n\nStep 4: Write down the rounded number with the digit you determined in Step 3, and all the digits to the right become zero.\n\n₦47,690",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b028",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Rounding off numbers"
    },
    "content_text": "If we round off 47,689 to the nearest ten, we actually want to know whether this number is closer to 47,680 or 47,690. The number 47,689 is 1 unit away from 47,690 and 9 units away from 47,680. That is why it is rounded off to 47,690.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b029",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Worked example 7.5: Rounding off to the nearest hundred"
    },
    "content_text": "",
    "prompt_text": "A handbag is advertised for ₦2,950. Round off this number to the nearest hundred.",
    "answer_text": "Step 1: Write down half of the required multiple of 10.\n\n$$\n\\frac{1}{2}\\times 100=50\n$$\n\nStep 2: Determine which digit represents the required multiple of 10.\n\nYou may use a place value table to help you with this:\n\n$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|}\n\\hline\n\\text{billion} & \\text{hm} & \\text{tm} & \\text{million} &\\text{hth} & \\text{tth} & \\text{thousand} & \\text{ h } & \\text{ t } & \\text{ u }  \\\\\n\\hline\n& & & & & & 2 & 9 & 5 & 0     \\\\\n\\hline\n\\end{array}\n$$\n\nThe 9 represents the hundreds.\n\nStep 3: Consider the digits to the right of the one you identified in Step 2. If they are less than the value in Step 1, the digit you identified remains the same. If they are equal to or more than the value in Step 1, the digit you identified increases by 1.\n\nThe digits to the right of the 9 are 50.\n50=50\nThe 9 must increase by 1.\n\nStep 4: If the digit that must increase is a 9, it changes to a 0. The digit to its left increases by 1.\n\nThe 9 must change to a 0.\nThe 2 to the left of the 9 must change to a 3.\n\nStep 5: Write down the rounded number with the digits you determined in Step 4, and all the digits to the right become zeroes.\n\n₦3,000",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b030",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Rounding off numbers"
    },
    "content_text": "If we round off 2,950 to the nearest hundred, we actually want to know whether this number is closer to 2,900 or 3,000. The number 2,950 is exactly halfway between 2,900 and 3,000. By convention, we round up to the higher number.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b031",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Worked example 7.6: Rounding off to the nearest thousand"
    },
    "content_text": "",
    "prompt_text": "On a specific day, the population of Nigeria is 201,195,431. Round off this number to the nearest thousand.",
    "answer_text": "Step 1: Write down half of the required multiple of 10.\n\n$$\n\\frac{1}{2}\\times 1,000=500\n$$\n\nStep 2: Determine which digit represents the required multiple of 10.\n\nYou may use a place value table to help you with this:\n\n$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|}\n\\hline\n\\text{billion} & \\text{hm} & \\text{tm} & \\text{million} &\\text{hth} & \\text{tth} & \\text{thousand} & \\text{ h } & \\text{ t } & \\text{ u }  \\\\\n\\hline\n& 2 & 0 & 1 & 1 & 9 & 5 & 4 & 3 & 1     \\\\\n\\hline\n\\end{array}\n$$\n\nThe 5 represents the thousands.\n\nStep 3: Consider the digits to the right of the one you identified in Step 2. If they are less than the value in Step 1, the digit you identified remains the same. If they are equal to or more than the value in Step 1, the digit you identified increases by 1.\n\nThe digits to the right of the 5 are 431.\n431<500\nThe 5 remains the same.\n\nStep 4: Write down the rounded number with the digit you determined in Step 3, and all the digits to the right of it as zeroes.\n\n201,195,000",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b032",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Rounding off numbers"
    },
    "content_text": "If we round off 201,195,431 to the nearest thousand, we actually want to know whether this number is closer to 201,195,000 or 201,196,000. The number 201,195,431 is 431 units away from 201,195,000 and 569 units away from 201,196,000. That is why it is rounded off to 201,195,000.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b033",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.7: Round off numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.7: Round off numbers\n\nRound off each of the following numbers to the required multiple of 10.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b033-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.7: Round off numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.7: Round off numbers\n\n1. 26,548 to the nearest ten",
    "answer_text": "26,550",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b033-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.7: Round off numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.7: Round off numbers\n\n2. 48,849 to the nearest hundred",
    "answer_text": "48,800",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b033-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.7: Round off numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.7: Round off numbers\n\n3. 37,627 to the nearest thousand",
    "answer_text": "38,000",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b033-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.7: Round off numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.7: Round off numbers\n\n4. 58,503 to the nearest thousand",
    "answer_text": "59,000",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b033-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.7: Round off numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.7: Round off numbers\n\n5. 29,618 to the nearest thousand",
    "answer_text": "30,000",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b033-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.7: Round off numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.7: Round off numbers\n\n6. 5,319,432 to the nearest thousand",
    "answer_text": "5,319,000",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b033-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.7: Round off numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.7: Round off numbers\n\n7. 19,553 to the nearest thousand",
    "answer_text": "20,000",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b033-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.7: Round off numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.7: Round off numbers\n\n8. 2,905,047 to the nearest hundred",
    "answer_text": "2,905,000",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b033-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.7: Round off numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.7: Round off numbers\n\n9. 5,095 to the nearest ten",
    "answer_text": "5,100",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b033-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.7: Round off numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.7: Round off numbers\n\n10. 512,909,050 to the nearest hundred",
    "answer_text": "512,909,100",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
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
  "subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000",
  "subtopic_title": "Rounding off numbers to the nearest 10, 100 and 1000",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000-po01",
        "source_performance_objective_index": 1,
        "text": "Round numbers to the nearest 10, 100, and 1000"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-10",
          "text": "Round numbers to the nearest 10."
        },
        {
          "atomic_objective_id": "rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-100",
          "text": "Round numbers to the nearest 100."
        },
        {
          "atomic_objective_id": "rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-1000",
          "text": "Round numbers to the nearest 1000."
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
    "record_id": "ch07-b024",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Rounding off numbers"
    },
    "content_text": "When we round off numbers, we make them less exact, but easier to work with. We usually round off a number to a specific multiple of 10.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b025",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Rounding off numbers"
    },
    "content_text": "rounding off Rounding off is the process of making a number less exact but easier to work with, by adjusting it to a specific multiple of 10.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b026",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Rounding off numbers"
    },
    "content_text": "When we round off a number to a specific multiple of 10, we have to identify the digit that represents the multiple, and then determine whether than digit remains the same or increases by one.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b027",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Worked example 7.4: Rounding off to the nearest ten"
    },
    "content_text": "",
    "prompt_text": "A smartphone is advertised for ₦47,689. Round off this number to the nearest ten.",
    "answer_text": "Step 1: Write down half of the required multiple of 10.\n\n$$\n\\frac{1}{2}\\times 10=5\n$$\n\nStep 2: Determine which digit represents the required multiple of 10.\n\nYou may use a place value table to help you with this:\n\n$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|}\n\\hline\n\\text{billion} & \\text{hm} & \\text{tm} & \\text{million} &\\text{hth} & \\text{tth} & \\text{thousand} & \\text{ h } & \\text{ t } & \\text{ u }  \\\\\n\\hline\n& & & & & 4 & 7 & 6 & 8 & 9     \\\\\n\\hline\n\\end{array}\n$$\n\nThe 8 represents ten.\n\nStep 3: Consider the digits to the right of the one you identified in Step 2. If they are less than the value in Step 1, the digit you identified remains the same. If they are equal to or more than the value in Step 1, the digit you identified increases by 1.\n\nThe digit to the right of the 8 is 9.\n9&amp;gt;5\nThe 8 increases to a 9.\n\nStep 4: Write down the rounded number with the digit you determined in Step 3, and all the digits to the right become zero.\n\n₦47,690",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b028",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Rounding off numbers"
    },
    "content_text": "If we round off 47,689 to the nearest ten, we actually want to know whether this number is closer to 47,680 or 47,690. The number 47,689 is 1 unit away from 47,690 and 9 units away from 47,680. That is why it is rounded off to 47,690.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b029",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Worked example 7.5: Rounding off to the nearest hundred"
    },
    "content_text": "",
    "prompt_text": "A handbag is advertised for ₦2,950. Round off this number to the nearest hundred.",
    "answer_text": "Step 1: Write down half of the required multiple of 10.\n\n$$\n\\frac{1}{2}\\times 100=50\n$$\n\nStep 2: Determine which digit represents the required multiple of 10.\n\nYou may use a place value table to help you with this:\n\n$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|}\n\\hline\n\\text{billion} & \\text{hm} & \\text{tm} & \\text{million} &\\text{hth} & \\text{tth} & \\text{thousand} & \\text{ h } & \\text{ t } & \\text{ u }  \\\\\n\\hline\n& & & & & & 2 & 9 & 5 & 0     \\\\\n\\hline\n\\end{array}\n$$\n\nThe 9 represents the hundreds.\n\nStep 3: Consider the digits to the right of the one you identified in Step 2. If they are less than the value in Step 1, the digit you identified remains the same. If they are equal to or more than the value in Step 1, the digit you identified increases by 1.\n\nThe digits to the right of the 9 are 50.\n50=50\nThe 9 must increase by 1.\n\nStep 4: If the digit that must increase is a 9, it changes to a 0. The digit to its left increases by 1.\n\nThe 9 must change to a 0.\nThe 2 to the left of the 9 must change to a 3.\n\nStep 5: Write down the rounded number with the digits you determined in Step 4, and all the digits to the right become zeroes.\n\n₦3,000",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b030",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Rounding off numbers"
    },
    "content_text": "If we round off 2,950 to the nearest hundred, we actually want to know whether this number is closer to 2,900 or 3,000. The number 2,950 is exactly halfway between 2,900 and 3,000. By convention, we round up to the higher number.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b031",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Worked example 7.6: Rounding off to the nearest thousand"
    },
    "content_text": "",
    "prompt_text": "On a specific day, the population of Nigeria is 201,195,431. Round off this number to the nearest thousand.",
    "answer_text": "Step 1: Write down half of the required multiple of 10.\n\n$$\n\\frac{1}{2}\\times 1,000=500\n$$\n\nStep 2: Determine which digit represents the required multiple of 10.\n\nYou may use a place value table to help you with this:\n\n$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|}\n\\hline\n\\text{billion} & \\text{hm} & \\text{tm} & \\text{million} &\\text{hth} & \\text{tth} & \\text{thousand} & \\text{ h } & \\text{ t } & \\text{ u }  \\\\\n\\hline\n& 2 & 0 & 1 & 1 & 9 & 5 & 4 & 3 & 1     \\\\\n\\hline\n\\end{array}\n$$\n\nThe 5 represents the thousands.\n\nStep 3: Consider the digits to the right of the one you identified in Step 2. If they are less than the value in Step 1, the digit you identified remains the same. If they are equal to or more than the value in Step 1, the digit you identified increases by 1.\n\nThe digits to the right of the 5 are 431.\n431<500\nThe 5 remains the same.\n\nStep 4: Write down the rounded number with the digit you determined in Step 3, and all the digits to the right of it as zeroes.\n\n201,195,000",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b032",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Rounding off numbers"
    },
    "content_text": "If we round off 201,195,431 to the nearest thousand, we actually want to know whether this number is closer to 201,195,000 or 201,196,000. The number 201,195,431 is 431 units away from 201,195,000 and 569 units away from 201,196,000. That is why it is rounded off to 201,195,000.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b033",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.7: Round off numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.7: Round off numbers\n\nRound off each of the following numbers to the required multiple of 10.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b033-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.7: Round off numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.7: Round off numbers\n\n1. 26,548 to the nearest ten",
    "answer_text": "26,550",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b033-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.7: Round off numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.7: Round off numbers\n\n2. 48,849 to the nearest hundred",
    "answer_text": "48,800",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b033-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.7: Round off numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.7: Round off numbers\n\n3. 37,627 to the nearest thousand",
    "answer_text": "38,000",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b033-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.7: Round off numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.7: Round off numbers\n\n4. 58,503 to the nearest thousand",
    "answer_text": "59,000",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b033-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.7: Round off numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.7: Round off numbers\n\n5. 29,618 to the nearest thousand",
    "answer_text": "30,000",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b033-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.7: Round off numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.7: Round off numbers\n\n6. 5,319,432 to the nearest thousand",
    "answer_text": "5,319,000",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b033-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.7: Round off numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.7: Round off numbers\n\n7. 19,553 to the nearest thousand",
    "answer_text": "20,000",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b033-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.7: Round off numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.7: Round off numbers\n\n8. 2,905,047 to the nearest hundred",
    "answer_text": "2,905,000",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b033-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.7: Round off numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.7: Round off numbers\n\n9. 5,095 to the nearest ten",
    "answer_text": "5,100",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
  },
  {
    "record_id": "ch07-b033-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Approximation and rounding off",
      "h3": "Exercise 7.7: Round off numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.7: Round off numbers\n\n10. 512,909,050 to the nearest hundred",
    "answer_text": "512,909,100",
    "primary_subtopic_id": "jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000"
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
