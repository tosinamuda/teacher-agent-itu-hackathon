# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-2",
  "topic_key": "jss1-math-approximation",
  "topic": "Approximation",
  "subtopic_id": "jss1-math-approximation-application-of-approximation-in-everyday-life",
  "subtopic_title": "Application of approximation in everyday life",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-approximation-application-of-approximation-in-everyday-life-po01",
        "source_performance_objective_index": 1,
        "text": "Apply approximation involving basic operations in everyday life activities"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "application-of-approximation-in-everyday-life-ao-apply-approximation",
          "text": "Apply approximation involving basic operations in everyday life activities."
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
    "record_id": "ch07-b037",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": null
    },
    "content_text": "The advantages of being able to estimate and approximate have been mentioned already. This section provides more opportunity for you to practise.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-application-of-approximation-in-everyday-life"
  },
  {
    "record_id": "ch07-b038",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.9: Evaluate test answers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.9: Evaluate test answers\n\nEach of the following is an incorrect answer that was given by a student in a test. Say what mistake the student made and give the correct answer.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-quantitative-reasoning-involving-estimation"
  },
  {
    "record_id": "ch07-b038-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.9: Evaluate test answers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.9: Evaluate test answers\n\n1. The cost of 50 rulers at ₦10 each is ₦5,000.",
    "answer_text": "There is one zero too many. It must be ₦500.",
    "primary_subtopic_id": "jss1-math-approximation-quantitative-reasoning"
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
    "record_id": "ch07-b040",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Worked example 7.8: Using approximation in calculations"
    },
    "content_text": "",
    "prompt_text": "A shop owner has to choose the supplier from which she will order sugar cubes. One supplier offers 50 $\\times$ 450 g packs of sugar cubes at ₦19,599. Another supplier offers 20 $\\times$ 450 g packs of sugar cubes at ₦5,999. She wants to do a quick calculation to make a decision. She needs to approximate the price of one pack.",
    "answer_text": "Step 1: Decide what operation must be done: addition, subtraction, multiplication or division.\nSince the mass of the packs of sugar cubes are the same at both suppliers, the shop owner must determine the cost per pack.\nShe must divide the total cost by the number of packs.\n\nStep 2: Round the numbers to multiples of ten that will allow an easy calculation.\nRound both costs to the nearest thousand:\n₦19,599 ≈ ₦20,000\n₦5,999 ≈ ₦6,000\nThe numbers of packs are already given as a multiple of ten for both suppliers.\n\nStep 3: Do the calculation with the approximate values.\n₦20,000/50=₦400 for one pack\n₦6,000/20=₦300 for one pack\nThe price for one pack is lower for the supplier that offers 20 packs at ₦5,999.",
    "primary_subtopic_id": "jss1-math-approximation-application-of-approximation-in-everyday-life"
  },
  {
    "record_id": "ch07-b041",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.10: Use estimation and approximation to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.10: Use estimation and approximation to solve problems",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-application-of-approximation-in-everyday-life"
  },
  {
    "record_id": "ch07-b041-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.10: Use estimation and approximation to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.10: Use estimation and approximation to solve problems\n\n1. A litre of petrol costs ₦153. What is the approximate cost of filling up a small car with a tank of 52 L?",
    "answer_text": "$$\\begin{align}\n₦153\\times52 &\\approx ₦150\\times50 \\\\\n&\\approx ₦7,500 \\\\\n\\end{align}$$",
    "primary_subtopic_id": "jss1-math-approximation-application-of-approximation-in-everyday-life"
  },
  {
    "record_id": "ch07-b041-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.10: Use estimation and approximation to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.10: Use estimation and approximation to solve problems\n\n2. A fabric shop has a special offer of ₦7,475 for 9.75 m of Ankara print. Give the approximate cost per metre.",
    "answer_text": "$$\\begin{align}\n\\frac{₦7,475}{9.75} &\\approx \\frac{₦7,500}{10} \\\\\n&\\approx ₦750\n\\end{align}$$",
    "primary_subtopic_id": "jss1-math-approximation-application-of-approximation-in-everyday-life"
  },
  {
    "record_id": "ch07-b041-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.10: Use estimation and approximation to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.10: Use estimation and approximation to solve problems\n\n4. A university student rents a flat at ₦82,250 per month. She works out that her rent for the year is going to be ₦98,700 and lets her mother know. Her mother immediately sees that the amount cannot be correct. Do a rough check to determine what is wrong with the calculation.",
    "answer_text": "$$\\begin{align}\n₦82,250\\times 12 &\\approx ₦82,000 \\times 10 \\\\\n&\\approx ₦820,000 \\\\\n\\end{align}$$\nThe student probably left out a zero. The amount should be ₦987,000.",
    "primary_subtopic_id": "jss1-math-approximation-application-of-approximation-in-everyday-life"
  },
  {
    "record_id": "ch07-b041-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.10: Use estimation and approximation to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.10: Use estimation and approximation to solve problems\n\n6. A 5 L container of vegetable oil is sold at ₦2,899. Approximately how much money do you need for 31 L of vegetable oil?",
    "answer_text": "$$\\begin{align}\n\\frac{₦2,899}{5}\\times 31 &\\approx \\frac{₦3,000}{5}\\times 30 \\\\\n&\\approx ₦600\\times 30 \\\\\n&\\approx ₦18,000\n\\end{align}$$",
    "primary_subtopic_id": "jss1-math-approximation-application-of-approximation-in-everyday-life"
  },
  {
    "record_id": "ch07-b041-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.10: Use estimation and approximation to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.10: Use estimation and approximation to solve problems\n\n8. A supermarket has special offers on milk powder. One offer is two 1 kg tins at ₦7,595. Another offer is four 400 g tins at ₦6,399. Do a quick calculation to determine which offer is the cheapest.",
    "answer_text": "Offer 1:\n$$\\begin{align}\n\\frac{₦7,595}{2\\times1\\text{ kg}} &\\approx \\frac{₦7,600}{2} \\\\\n&\\approx ₦3,800\\text{/kg} \\\\\n\\end{align}$$\nOffer 2:\n$$\\begin{align}\n\\frac{₦6,399}{4\\times400\\text{ g}} &\\approx \\frac{₦6,400}{1.6} \\\\\n&\\approx ₦4,000\\text{/kg} \\\\\n\\end{align}$$\nOffer 1 is the cheapest.",
    "primary_subtopic_id": "jss1-math-approximation-application-of-approximation-in-everyday-life"
  },
  {
    "record_id": "ch07-b041-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.10: Use estimation and approximation to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.10: Use estimation and approximation to solve problems\n\n9. An internet provider charges ₦9,309 per month for an 8 Mbps line. At the end of a year, they let their customers know that there will be a price increase of 10.25%. Work out what the approximate new price will be.",
    "answer_text": "$$\\begin{align}\n\\frac{10.25}{100}\\times₦9,309+₦9,309 &\\approx \\frac{10}{100}\\times₦9,000+₦9,000 \\\\\n&\\approx \\frac{₦9,000}{10}+₦9,000 \\\\\n&\\approx ₦900+₦9,000 \\\\\n&\\approx ₦9,900\n\\end{align}$$",
    "primary_subtopic_id": "jss1-math-approximation-application-of-approximation-in-everyday-life"
  },
  {
    "record_id": "ch07-b041-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.10: Use estimation and approximation to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.10: Use estimation and approximation to solve problems\n\n10. A caterer has to give a quote for the food at a wedding. The mother of the bride tells her that they are expecting adult 323 guests. She thinks about three quarters of the families will bring their children along. Most families have four children. The food will cost ₦3,960 per adult guest and about half price for a child. Work out a rough quote.",
    "answer_text": "$$\\begin{align}\n\\text{Number of families}&\\approx \\frac{323}{2} \\\\\n&\\approx \\frac{320}{2} \\\\\n&\\approx 160\\\\\n\\end{align}$$\n$$\\begin{align}\n\\text{Number of children}&\\approx \\frac{3}{4}\\times160 \\times 4\\\\\n&\\approx 3\\times160 \\\\\n&\\approx 480\\\\\n\\end{align}$$\n$$\\begin{align}\n\\text{Cost of food}&\\approx 320\\times ₦4,000+480\\times \\frac{₦4,000}{2} \\\\\n&\\approx 320\\times ₦4,000+480\\times ₦2,000 \\\\\n&\\approx  ₦1,280,000+₦960,000 \\\\\n&\\approx ₦2,260,000\\\\\n\\end{align}$$",
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
  "subtopic_id": "jss1-math-approximation-application-of-approximation-in-everyday-life",
  "subtopic_title": "Application of approximation in everyday life",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-approximation-application-of-approximation-in-everyday-life-po01",
        "source_performance_objective_index": 1,
        "text": "Apply approximation involving basic operations in everyday life activities"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "application-of-approximation-in-everyday-life-ao-apply-approximation",
          "text": "Apply approximation involving basic operations in everyday life activities."
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
    "record_id": "ch07-b037",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": null
    },
    "content_text": "The advantages of being able to estimate and approximate have been mentioned already. This section provides more opportunity for you to practise.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-application-of-approximation-in-everyday-life"
  },
  {
    "record_id": "ch07-b038",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.9: Evaluate test answers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.9: Evaluate test answers\n\nEach of the following is an incorrect answer that was given by a student in a test. Say what mistake the student made and give the correct answer.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-quantitative-reasoning-involving-estimation"
  },
  {
    "record_id": "ch07-b038-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.9: Evaluate test answers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.9: Evaluate test answers\n\n1. The cost of 50 rulers at ₦10 each is ₦5,000.",
    "answer_text": "There is one zero too many. It must be ₦500.",
    "primary_subtopic_id": "jss1-math-approximation-quantitative-reasoning"
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
    "record_id": "ch07-b040",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Worked example 7.8: Using approximation in calculations"
    },
    "content_text": "",
    "prompt_text": "A shop owner has to choose the supplier from which she will order sugar cubes. One supplier offers 50 $\\times$ 450 g packs of sugar cubes at ₦19,599. Another supplier offers 20 $\\times$ 450 g packs of sugar cubes at ₦5,999. She wants to do a quick calculation to make a decision. She needs to approximate the price of one pack.",
    "answer_text": "Step 1: Decide what operation must be done: addition, subtraction, multiplication or division.\nSince the mass of the packs of sugar cubes are the same at both suppliers, the shop owner must determine the cost per pack.\nShe must divide the total cost by the number of packs.\n\nStep 2: Round the numbers to multiples of ten that will allow an easy calculation.\nRound both costs to the nearest thousand:\n₦19,599 ≈ ₦20,000\n₦5,999 ≈ ₦6,000\nThe numbers of packs are already given as a multiple of ten for both suppliers.\n\nStep 3: Do the calculation with the approximate values.\n₦20,000/50=₦400 for one pack\n₦6,000/20=₦300 for one pack\nThe price for one pack is lower for the supplier that offers 20 packs at ₦5,999.",
    "primary_subtopic_id": "jss1-math-approximation-application-of-approximation-in-everyday-life"
  },
  {
    "record_id": "ch07-b041",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.10: Use estimation and approximation to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.10: Use estimation and approximation to solve problems",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-approximation-application-of-approximation-in-everyday-life"
  },
  {
    "record_id": "ch07-b041-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.10: Use estimation and approximation to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.10: Use estimation and approximation to solve problems\n\n1. A litre of petrol costs ₦153. What is the approximate cost of filling up a small car with a tank of 52 L?",
    "answer_text": "$$\\begin{align}\n₦153\\times52 &\\approx ₦150\\times50 \\\\\n&\\approx ₦7,500 \\\\\n\\end{align}$$",
    "primary_subtopic_id": "jss1-math-approximation-application-of-approximation-in-everyday-life"
  },
  {
    "record_id": "ch07-b041-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.10: Use estimation and approximation to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.10: Use estimation and approximation to solve problems\n\n2. A fabric shop has a special offer of ₦7,475 for 9.75 m of Ankara print. Give the approximate cost per metre.",
    "answer_text": "$$\\begin{align}\n\\frac{₦7,475}{9.75} &\\approx \\frac{₦7,500}{10} \\\\\n&\\approx ₦750\n\\end{align}$$",
    "primary_subtopic_id": "jss1-math-approximation-application-of-approximation-in-everyday-life"
  },
  {
    "record_id": "ch07-b041-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.10: Use estimation and approximation to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.10: Use estimation and approximation to solve problems\n\n4. A university student rents a flat at ₦82,250 per month. She works out that her rent for the year is going to be ₦98,700 and lets her mother know. Her mother immediately sees that the amount cannot be correct. Do a rough check to determine what is wrong with the calculation.",
    "answer_text": "$$\\begin{align}\n₦82,250\\times 12 &\\approx ₦82,000 \\times 10 \\\\\n&\\approx ₦820,000 \\\\\n\\end{align}$$\nThe student probably left out a zero. The amount should be ₦987,000.",
    "primary_subtopic_id": "jss1-math-approximation-application-of-approximation-in-everyday-life"
  },
  {
    "record_id": "ch07-b041-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.10: Use estimation and approximation to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.10: Use estimation and approximation to solve problems\n\n6. A 5 L container of vegetable oil is sold at ₦2,899. Approximately how much money do you need for 31 L of vegetable oil?",
    "answer_text": "$$\\begin{align}\n\\frac{₦2,899}{5}\\times 31 &\\approx \\frac{₦3,000}{5}\\times 30 \\\\\n&\\approx ₦600\\times 30 \\\\\n&\\approx ₦18,000\n\\end{align}$$",
    "primary_subtopic_id": "jss1-math-approximation-application-of-approximation-in-everyday-life"
  },
  {
    "record_id": "ch07-b041-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.10: Use estimation and approximation to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.10: Use estimation and approximation to solve problems\n\n8. A supermarket has special offers on milk powder. One offer is two 1 kg tins at ₦7,595. Another offer is four 400 g tins at ₦6,399. Do a quick calculation to determine which offer is the cheapest.",
    "answer_text": "Offer 1:\n$$\\begin{align}\n\\frac{₦7,595}{2\\times1\\text{ kg}} &\\approx \\frac{₦7,600}{2} \\\\\n&\\approx ₦3,800\\text{/kg} \\\\\n\\end{align}$$\nOffer 2:\n$$\\begin{align}\n\\frac{₦6,399}{4\\times400\\text{ g}} &\\approx \\frac{₦6,400}{1.6} \\\\\n&\\approx ₦4,000\\text{/kg} \\\\\n\\end{align}$$\nOffer 1 is the cheapest.",
    "primary_subtopic_id": "jss1-math-approximation-application-of-approximation-in-everyday-life"
  },
  {
    "record_id": "ch07-b041-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.10: Use estimation and approximation to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.10: Use estimation and approximation to solve problems\n\n9. An internet provider charges ₦9,309 per month for an 8 Mbps line. At the end of a year, they let their customers know that there will be a price increase of 10.25%. Work out what the approximate new price will be.",
    "answer_text": "$$\\begin{align}\n\\frac{10.25}{100}\\times₦9,309+₦9,309 &\\approx \\frac{10}{100}\\times₦9,000+₦9,000 \\\\\n&\\approx \\frac{₦9,000}{10}+₦9,000 \\\\\n&\\approx ₦900+₦9,000 \\\\\n&\\approx ₦9,900\n\\end{align}$$",
    "primary_subtopic_id": "jss1-math-approximation-application-of-approximation-in-everyday-life"
  },
  {
    "record_id": "ch07-b041-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.10: Use estimation and approximation to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.10: Use estimation and approximation to solve problems\n\n10. A caterer has to give a quote for the food at a wedding. The mother of the bride tells her that they are expecting adult 323 guests. She thinks about three quarters of the families will bring their children along. Most families have four children. The food will cost ₦3,960 per adult guest and about half price for a child. Work out a rough quote.",
    "answer_text": "$$\\begin{align}\n\\text{Number of families}&\\approx \\frac{323}{2} \\\\\n&\\approx \\frac{320}{2} \\\\\n&\\approx 160\\\\\n\\end{align}$$\n$$\\begin{align}\n\\text{Number of children}&\\approx \\frac{3}{4}\\times160 \\times 4\\\\\n&\\approx 3\\times160 \\\\\n&\\approx 480\\\\\n\\end{align}$$\n$$\\begin{align}\n\\text{Cost of food}&\\approx 320\\times ₦4,000+480\\times \\frac{₦4,000}{2} \\\\\n&\\approx 320\\times ₦4,000+480\\times ₦2,000 \\\\\n&\\approx  ₦1,280,000+₦960,000 \\\\\n&\\approx ₦2,260,000\\\\\n\\end{align}$$",
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
