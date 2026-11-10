# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-2",
  "topic_key": "jss1-math-estimation",
  "topic": "Estimation",
  "subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances",
  "subtopic_title": "Estimation of dimensions and distances",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-estimation-estimation-of-dimensions-and-distances-po01",
        "source_performance_objective_index": 1,
        "text": "Estimate the dimensions and distances within the school"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "estimation-of-dimensions-and-distances-ao-estimate-dimensions",
          "text": "Estimate the dimensions within the school."
        },
        {
          "atomic_objective_id": "estimation-of-dimensions-and-distances-ao-estimate-distances",
          "text": "Estimate the distances within the school."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch07-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": null
    },
    "content_text": "**Estimation** is the process of making a guess about the size or cost of something, without doing the actual measurement or calculation. Estimations are sometimes needed because we do not have all the facts, or because we are pressed for time. Estimation can also help you to see whether the answer to a problem makes sense.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b002",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": null
    },
    "content_text": "**estimation**\nEstimation is the process of making a guess without doing the actual measurement or calculation.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b003",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Estimating distances and dimensions"
    },
    "content_text": "A **distance** can be described as the length of the space between two points. An example of a distance is the length of the path between the door of the classroom and the door to the principal's office.\n\nThe **dimensions** of an object are the measurable lengths that we use to determine the size of the object. Examples of dimensions are the length, breadth (or width) and height of a box.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b004",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Estimating distances and dimensions"
    },
    "content_text": "**distance**\nDistance is the length of the space between two points.\n\n**dimensions**\nThe dimensions of an object are the measurable lengths that we use to determine the size of the object, such as its length, breadth and height.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b005",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Estimating distances and dimensions"
    },
    "content_text": "When we estimate distances and dimensions, it is important to use the correct unit of measurement. The **SI unit** for length is the metre. A length of one metre (1 m) is more or less equal to:\n\n- the height of a 6-year-old child\n- a large step of an adult\n- the length of a prayer rug.\n\nOther units of measurement used often are multiples of ten of 1 m. The most common multiples are shown in the table below.\n\n$$\n\\begin{array}{|c|c|c|c|c|}\n      \\hline\n      \\textbf{Name} & \\textbf{Abbreviation} & \\textbf{Size} & \\textbf{Example} \\\\\n      \\hline\n      \\text{millimetre} & \\text{mm} & 1\\text{ mm}=\\frac{1}{1,000}\\text{ m}=0,001\\text{ m} & \\text{thickness of a plastic bank card } \\\\\n      \\hline\n      \\text{centimetre} & \\text{cm} & 1\\text{ cm}=\\frac{1}{100}\\text{ m}=0,01\\text{ m} & \\text{width of a finger nail} \\\\\n      \\hline\n      \\text{kilometre} & \\text{km} & 1\\text{ km}=1,000\\text{ m} & \\text{distance walked in 12 minutes} \\\\\n      \\hline\n      \\end{array}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b006",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Estimating distances and dimensions"
    },
    "content_text": "**SI unit**\nAn SI unit is a basic unit of measurement that forms part of the International System of Units.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b007",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Worked example 7.1: Evaluating an estimation of a dimension"
    },
    "content_text": "",
    "prompt_text": "Adebankole is 14 years old. He estimated his own height as 160 cm. Evaluate his estimation.",
    "answer_text": "Step 1: Evaluate whether the unit of measurement is appropriate.\n\nLook at your ruler to see how long 1 cm is. It is quite short compared to the height of a teenager.\n\nIt might be better to use metres, but then Adebankole would need to use a decimal point in his estimation. To avoid the decimal point, centimetres is an appropriate unit.\n\nStep 2: Evaluate whether the value of the estimation makes sense.\n\nThe height of a 6-year-old child is roughly 1 m. That is equal to 100 cm. So Adebankole's height is most probably more than 100 cm.\n\nMost humans are not taller than 2 m, which is equal to 200 cm.\n\nAdebankole's estimation is between 100 cm and 200 cm, so it makes sense.",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b008",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.1: Estimate distances and dimensions in your classroom"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.1: Estimate distances and dimensions in your classroom\n\nEstimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measure to get the real measurements. Compare the real measurements to your estimations.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b008-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.1: Estimate distances and dimensions in your classroom"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.1: Estimate distances and dimensions in your classroom\n\nEstimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measure to get the real measurements. Compare the real measurements to your estimations.\n\n1. Length of your pencil",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b008-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.1: Estimate distances and dimensions in your classroom"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.1: Estimate distances and dimensions in your classroom\n\nEstimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measure to get the real measurements. Compare the real measurements to your estimations.\n\n2. Width of your eraser",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b008-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.1: Estimate distances and dimensions in your classroom"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.1: Estimate distances and dimensions in your classroom\n\nEstimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measure to get the real measurements. Compare the real measurements to your estimations.\n\n3. Length of your Mathematics workbook",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b008-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.1: Estimate distances and dimensions in your classroom"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.1: Estimate distances and dimensions in your classroom\n\nEstimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measure to get the real measurements. Compare the real measurements to your estimations.\n\n4. Height of your thickest textbook",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b008-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.1: Estimate distances and dimensions in your classroom"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.1: Estimate distances and dimensions in your classroom\n\nEstimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measure to get the real measurements. Compare the real measurements to your estimations.\n\n5. Length of the classroom",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b008-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.1: Estimate distances and dimensions in your classroom"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.1: Estimate distances and dimensions in your classroom\n\nEstimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measure to get the real measurements. Compare the real measurements to your estimations.\n\n6. Width of the classroom",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b008-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.1: Estimate distances and dimensions in your classroom"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.1: Estimate distances and dimensions in your classroom\n\nEstimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measure to get the real measurements. Compare the real measurements to your estimations.\n\n7. Width of the blackboard",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b008-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.1: Estimate distances and dimensions in your classroom"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.1: Estimate distances and dimensions in your classroom\n\nEstimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measure to get the real measurements. Compare the real measurements to your estimations.\n\n8. Height of your teacher's table",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b008-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.1: Estimate distances and dimensions in your classroom"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.1: Estimate distances and dimensions in your classroom\n\nEstimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measure to get the real measurements. Compare the real measurements to your estimations.\n\n9. Width of the classroom door",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b008-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.1: Estimate distances and dimensions in your classroom"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.1: Estimate distances and dimensions in your classroom\n\nEstimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measure to get the real measurements. Compare the real measurements to your estimations.\n\n10. Distance from the doorknob of the Mathematics classroom to the doorknob of the classroom next to it",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b009",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.2: Estimate everyday distances and dimensions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.2: Estimate everyday distances and dimensions\n\nEstimate the following distances and dimensions by deciding which one of the options a) to d) is the most correct.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b009-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.2: Estimate everyday distances and dimensions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.2: Estimate everyday distances and dimensions\n\nEstimate the following distances and dimensions by deciding which one of the options a) to d) is the most correct.\n\n1. Diameter of a 50 kobo coin\na) 5 mm\nb) 24.5 mm\nc) 80.5 mm\nd) 120 mm",
    "answer_text": "24.5 mm",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b009-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.2: Estimate everyday distances and dimensions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.2: Estimate everyday distances and dimensions\n\nEstimate the following distances and dimensions by deciding which one of the options a) to d) is the most correct.\n\n2. Length of a ₦10 note\na) 20 mm\nb) 1.5 cm\nc) 25 cm\nd) 130 mm",
    "answer_text": "130 mm",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b009-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.2: Estimate everyday distances and dimensions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.2: Estimate everyday distances and dimensions\n\nEstimate the following distances and dimensions by deciding which one of the options a) to d) is the most correct.\n\n3. Height of a standard door\na) 450 mm\nb) 35 cm\nc) 2.1 m\nd) 12 m",
    "answer_text": "2.1 m",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b009-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.2: Estimate everyday distances and dimensions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.2: Estimate everyday distances and dimensions\n\nEstimate the following distances and dimensions by deciding which one of the options a) to d) is the most correct.\n\n4. Maximum length of a standard football field\na) 120 m\nb) 25 m\nc) 850 cm\nd) 950 m",
    "answer_text": "120 m",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b009-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.2: Estimate everyday distances and dimensions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.2: Estimate everyday distances and dimensions\n\nEstimate the following distances and dimensions by deciding which one of the options a) to d) is the most correct.\n\n5. Shortest driving distance from Murtala Muhammed International Airport to Ibadan\na) 127 km\nb) 1,270 m\nc) 11,270 km\nd) 100,270 mm",
    "answer_text": "127 km",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b038-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.9: Evaluate test answers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.9: Evaluate test answers\n\n3. The width of the classroom is 90 m.",
    "answer_text": "There should not be a zero. It must be 9 m.",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b041-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.10: Use estimation and approximation to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.10: Use estimation and approximation to solve problems\n\n3. A student's steps are 60 cm long. He takes 8,315 steps from his front door to the school gate. Approximately how far does he live from the school?",
    "answer_text": "$$\\begin{align}\n60\\text{ cm}\\times8,315 &\\approx 60\\text{ cm}\\times8,000 \\\\\n&\\approx 480,000\\text{ cm} \\\\\n&\\approx 4,800\\text{ m} \\\\\n&\\approx 4,8\\text{ km}\n\\end{align}$$",
    "primary_subtopic_id": "jss1-math-estimation-quantitative-reasoning-involving-estimation"
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
  "topic_key": "jss1-math-estimation",
  "topic": "Estimation",
  "subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances",
  "subtopic_title": "Estimation of dimensions and distances",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-estimation-estimation-of-dimensions-and-distances-po01",
        "source_performance_objective_index": 1,
        "text": "Estimate the dimensions and distances within the school"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "estimation-of-dimensions-and-distances-ao-estimate-dimensions",
          "text": "Estimate the dimensions within the school."
        },
        {
          "atomic_objective_id": "estimation-of-dimensions-and-distances-ao-estimate-distances",
          "text": "Estimate the distances within the school."
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
    "record_id": "ch07-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": null
    },
    "content_text": "**Estimation** is the process of making a guess about the size or cost of something, without doing the actual measurement or calculation. Estimations are sometimes needed because we do not have all the facts, or because we are pressed for time. Estimation can also help you to see whether the answer to a problem makes sense.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b002",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": null
    },
    "content_text": "**estimation**\nEstimation is the process of making a guess without doing the actual measurement or calculation.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b003",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Estimating distances and dimensions"
    },
    "content_text": "A **distance** can be described as the length of the space between two points. An example of a distance is the length of the path between the door of the classroom and the door to the principal's office.\n\nThe **dimensions** of an object are the measurable lengths that we use to determine the size of the object. Examples of dimensions are the length, breadth (or width) and height of a box.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b004",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Estimating distances and dimensions"
    },
    "content_text": "**distance**\nDistance is the length of the space between two points.\n\n**dimensions**\nThe dimensions of an object are the measurable lengths that we use to determine the size of the object, such as its length, breadth and height.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b005",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Estimating distances and dimensions"
    },
    "content_text": "When we estimate distances and dimensions, it is important to use the correct unit of measurement. The **SI unit** for length is the metre. A length of one metre (1 m) is more or less equal to:\n\n- the height of a 6-year-old child\n- a large step of an adult\n- the length of a prayer rug.\n\nOther units of measurement used often are multiples of ten of 1 m. The most common multiples are shown in the table below.\n\n$$\n\\begin{array}{|c|c|c|c|c|}\n      \\hline\n      \\textbf{Name} & \\textbf{Abbreviation} & \\textbf{Size} & \\textbf{Example} \\\\\n      \\hline\n      \\text{millimetre} & \\text{mm} & 1\\text{ mm}=\\frac{1}{1,000}\\text{ m}=0,001\\text{ m} & \\text{thickness of a plastic bank card } \\\\\n      \\hline\n      \\text{centimetre} & \\text{cm} & 1\\text{ cm}=\\frac{1}{100}\\text{ m}=0,01\\text{ m} & \\text{width of a finger nail} \\\\\n      \\hline\n      \\text{kilometre} & \\text{km} & 1\\text{ km}=1,000\\text{ m} & \\text{distance walked in 12 minutes} \\\\\n      \\hline\n      \\end{array}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b006",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Estimating distances and dimensions"
    },
    "content_text": "**SI unit**\nAn SI unit is a basic unit of measurement that forms part of the International System of Units.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b007",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Worked example 7.1: Evaluating an estimation of a dimension"
    },
    "content_text": "",
    "prompt_text": "Adebankole is 14 years old. He estimated his own height as 160 cm. Evaluate his estimation.",
    "answer_text": "Step 1: Evaluate whether the unit of measurement is appropriate.\n\nLook at your ruler to see how long 1 cm is. It is quite short compared to the height of a teenager.\n\nIt might be better to use metres, but then Adebankole would need to use a decimal point in his estimation. To avoid the decimal point, centimetres is an appropriate unit.\n\nStep 2: Evaluate whether the value of the estimation makes sense.\n\nThe height of a 6-year-old child is roughly 1 m. That is equal to 100 cm. So Adebankole's height is most probably more than 100 cm.\n\nMost humans are not taller than 2 m, which is equal to 200 cm.\n\nAdebankole's estimation is between 100 cm and 200 cm, so it makes sense.",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b008",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.1: Estimate distances and dimensions in your classroom"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.1: Estimate distances and dimensions in your classroom\n\nEstimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measure to get the real measurements. Compare the real measurements to your estimations.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b008-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.1: Estimate distances and dimensions in your classroom"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.1: Estimate distances and dimensions in your classroom\n\nEstimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measure to get the real measurements. Compare the real measurements to your estimations.\n\n1. Length of your pencil",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b008-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.1: Estimate distances and dimensions in your classroom"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.1: Estimate distances and dimensions in your classroom\n\nEstimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measure to get the real measurements. Compare the real measurements to your estimations.\n\n2. Width of your eraser",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b008-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.1: Estimate distances and dimensions in your classroom"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.1: Estimate distances and dimensions in your classroom\n\nEstimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measure to get the real measurements. Compare the real measurements to your estimations.\n\n3. Length of your Mathematics workbook",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b008-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.1: Estimate distances and dimensions in your classroom"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.1: Estimate distances and dimensions in your classroom\n\nEstimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measure to get the real measurements. Compare the real measurements to your estimations.\n\n4. Height of your thickest textbook",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b008-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.1: Estimate distances and dimensions in your classroom"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.1: Estimate distances and dimensions in your classroom\n\nEstimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measure to get the real measurements. Compare the real measurements to your estimations.\n\n5. Length of the classroom",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b008-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.1: Estimate distances and dimensions in your classroom"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.1: Estimate distances and dimensions in your classroom\n\nEstimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measure to get the real measurements. Compare the real measurements to your estimations.\n\n6. Width of the classroom",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b008-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.1: Estimate distances and dimensions in your classroom"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.1: Estimate distances and dimensions in your classroom\n\nEstimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measure to get the real measurements. Compare the real measurements to your estimations.\n\n7. Width of the blackboard",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b008-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.1: Estimate distances and dimensions in your classroom"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.1: Estimate distances and dimensions in your classroom\n\nEstimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measure to get the real measurements. Compare the real measurements to your estimations.\n\n8. Height of your teacher's table",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b008-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.1: Estimate distances and dimensions in your classroom"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.1: Estimate distances and dimensions in your classroom\n\nEstimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measure to get the real measurements. Compare the real measurements to your estimations.\n\n9. Width of the classroom door",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b008-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.1: Estimate distances and dimensions in your classroom"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.1: Estimate distances and dimensions in your classroom\n\nEstimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measure to get the real measurements. Compare the real measurements to your estimations.\n\n10. Distance from the doorknob of the Mathematics classroom to the doorknob of the classroom next to it",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b009",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.2: Estimate everyday distances and dimensions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.2: Estimate everyday distances and dimensions\n\nEstimate the following distances and dimensions by deciding which one of the options a) to d) is the most correct.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b009-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.2: Estimate everyday distances and dimensions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.2: Estimate everyday distances and dimensions\n\nEstimate the following distances and dimensions by deciding which one of the options a) to d) is the most correct.\n\n1. Diameter of a 50 kobo coin\na) 5 mm\nb) 24.5 mm\nc) 80.5 mm\nd) 120 mm",
    "answer_text": "24.5 mm",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b009-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.2: Estimate everyday distances and dimensions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.2: Estimate everyday distances and dimensions\n\nEstimate the following distances and dimensions by deciding which one of the options a) to d) is the most correct.\n\n2. Length of a ₦10 note\na) 20 mm\nb) 1.5 cm\nc) 25 cm\nd) 130 mm",
    "answer_text": "130 mm",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b009-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.2: Estimate everyday distances and dimensions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.2: Estimate everyday distances and dimensions\n\nEstimate the following distances and dimensions by deciding which one of the options a) to d) is the most correct.\n\n3. Height of a standard door\na) 450 mm\nb) 35 cm\nc) 2.1 m\nd) 12 m",
    "answer_text": "2.1 m",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b009-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.2: Estimate everyday distances and dimensions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.2: Estimate everyday distances and dimensions\n\nEstimate the following distances and dimensions by deciding which one of the options a) to d) is the most correct.\n\n4. Maximum length of a standard football field\na) 120 m\nb) 25 m\nc) 850 cm\nd) 950 m",
    "answer_text": "120 m",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b009-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.2: Estimate everyday distances and dimensions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.2: Estimate everyday distances and dimensions\n\nEstimate the following distances and dimensions by deciding which one of the options a) to d) is the most correct.\n\n5. Shortest driving distance from Murtala Muhammed International Airport to Ibadan\na) 127 km\nb) 1,270 m\nc) 11,270 km\nd) 100,270 mm",
    "answer_text": "127 km",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b038-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.9: Evaluate test answers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.9: Evaluate test answers\n\n3. The width of the classroom is 90 m.",
    "answer_text": "There should not be a zero. It must be 9 m.",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-dimensions-and-distances"
  },
  {
    "record_id": "ch07-b041-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.10: Use estimation and approximation to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.10: Use estimation and approximation to solve problems\n\n3. A student's steps are 60 cm long. He takes 8,315 steps from his front door to the school gate. Approximately how far does he live from the school?",
    "answer_text": "$$\\begin{align}\n60\\text{ cm}\\times8,315 &\\approx 60\\text{ cm}\\times8,000 \\\\\n&\\approx 480,000\\text{ cm} \\\\\n&\\approx 4,800\\text{ m} \\\\\n&\\approx 4,8\\text{ km}\n\\end{align}$$",
    "primary_subtopic_id": "jss1-math-estimation-quantitative-reasoning-involving-estimation"
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
