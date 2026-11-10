# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-2",
  "topic_key": "jss1-math-estimation",
  "topic": "Estimation",
  "subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects",
  "subtopic_title": "Estimation of capacity and mass of objects",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects-po01",
        "source_performance_objective_index": 1,
        "text": "Estimate the capacity and mass of given objects"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "estimation-of-capacity-and-mass-of-objects-ao-estimate-capacity",
          "text": "Estimate the capacity of given objects."
        },
        {
          "atomic_objective_id": "estimation-of-capacity-and-mass-of-objects-ao-estimate-mass",
          "text": "Estimate the mass of given objects."
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
    "record_id": "ch07-b010",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": null
    },
    "content_text": "Volume is the amount of space occupied by an object or the amount of space inside a container. The amount of liquid that a container can hold is called the capacity of the container.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b011",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": null
    },
    "content_text": "**capacity**\nThe amount of liquid that a container can hold is called the capacity of the container.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b012",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": null
    },
    "content_text": "The SI unit for capacity is the litre. A capacity of one litre (1 L) is more or less equal to:\n\n- six cups of tea\n- a carton of milk\n- three cans of soft drink.\n\nOther units of measurement used often are multiples of ten of 1 L. The most common multiples are shown in the table below.\n\n$$\n\\begin{array}{|c|c|c|c|}\n      \\hline\n      \\textbf{Name} & \\textbf{Abbreviation} & \\textbf{Size} & \\textbf{Example} \\\\\n      \\hline\n      \\text{millilitre} & \\text{ml} & 1\\text{ ml}=\\frac{1}{1,000}\\text{ L}=0,001\\text{ L} & \\text{twenty drops of water } \\\\\n      \\hline\n      \\text{centilitre} & \\text{cl} & 1\\text{ cl}=\\frac{1}{100}\\text{ L}=0,01\\text{ L} & \\text{two teaspoons of water} \\\\\n      \\hline\n      \\text{kilolitre} & \\text{kl} & 1\\text{ kl}=1,000\\text{ L} & \\text{medium-sized inflatable swimming pool} \\\\\n      \\hline\n      \\end{array}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b013",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Worked example 7.2: Evaluating an estimation of capacity"
    },
    "content_text": "",
    "prompt_text": "Amaka is feeling sick. The doctor gives her a bottle of medicine. She estimates that the capacity of the bottle is 250 cl. Evaluate her estimation.",
    "answer_text": "Step 1: Evaluate whether the unit of measurement is appropriate.\n\nThink about how much liquid 1 cl is. It is about two teaspoons.\n\nOne teaspoon is about 5 ml. The instructions on a bottle of medicine normally tells you how many teaspoons to take at time. Therefore, both millilitres and centilitres are appropriate units.\n\nStep 2: Evaluate whether the value of the estimation makes sense.\n\nIf there is 250 cl in the bottle, it means the bottle holds 500 teaspoons of medicine.\n\nAt two teaspoons twice a day, it would take $\\frac{500}{4}=125$ days to finish the medicine. That is more than 4 months! It is not possible to get so much medicine from a normal medicine bottle.\n\nAmaka's estimation does not make sense. An estimation of 25 cl, which is 250 ml, would be a better estimation.",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b014",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Exercise 7.3: Estimate capacity of containers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.3: Estimate capacity of containers\n\nYou might use the containers listed below at school or at home. Estimate the capacity of the containers. Include an appropriate unit of measurement in each case. Then use measuring cylinders from the science laboratory, or a set of measuring spoons and cups used for baking, to get the real measurements. Compare the real measurements to your estimations.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b014-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Exercise 7.3: Estimate capacity of containers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.3: Estimate capacity of containers\n\nYou might use the containers listed below at school or at home. Estimate the capacity of the containers. Include an appropriate unit of measurement in each case. Then use measuring cylinders from the science laboratory, or a set of measuring spoons and cups used for baking, to get the real measurements. Compare the real measurements to your estimations.\n\n1. Tea cup",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b014-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Exercise 7.3: Estimate capacity of containers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.3: Estimate capacity of containers\n\nYou might use the containers listed below at school or at home. Estimate the capacity of the containers. Include an appropriate unit of measurement in each case. Then use measuring cylinders from the science laboratory, or a set of measuring spoons and cups used for baking, to get the real measurements. Compare the real measurements to your estimations.\n\n2. Soft drink bottle",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b014-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Exercise 7.3: Estimate capacity of containers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.3: Estimate capacity of containers\n\nYou might use the containers listed below at school or at home. Estimate the capacity of the containers. Include an appropriate unit of measurement in each case. Then use measuring cylinders from the science laboratory, or a set of measuring spoons and cups used for baking, to get the real measurements. Compare the real measurements to your estimations.\n\n3. Test tube",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b014-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Exercise 7.3: Estimate capacity of containers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.3: Estimate capacity of containers\n\nYou might use the containers listed below at school or at home. Estimate the capacity of the containers. Include an appropriate unit of measurement in each case. Then use measuring cylinders from the science laboratory, or a set of measuring spoons and cups used for baking, to get the real measurements. Compare the real measurements to your estimations.\n\n4. Lunch box",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b014-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Exercise 7.3: Estimate capacity of containers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.3: Estimate capacity of containers\n\nYou might use the containers listed below at school or at home. Estimate the capacity of the containers. Include an appropriate unit of measurement in each case. Then use measuring cylinders from the science laboratory, or a set of measuring spoons and cups used for baking, to get the real measurements. Compare the real measurements to your estimations.\n\n5. Water glass",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b015",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Exercise 7.4: Estimate capacity of everyday containers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.4: Estimate capacity of everyday containers\n\nEstimate the capacity of the following containers by deciding which one of the options a) to d) is the most correct.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b015-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Exercise 7.4: Estimate capacity of everyday containers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.4: Estimate capacity of everyday containers\n\nEstimate the capacity of the following containers by deciding which one of the options a) to d) is the most correct.\n\n1. Milk tin\na) 3 cl\nb) 25 ml\nc) 300 cl\nd) 350 ml",
    "answer_text": "350 ml",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b015-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Exercise 7.4: Estimate capacity of everyday containers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.4: Estimate capacity of everyday containers\n\nEstimate the capacity of the following containers by deciding which one of the options a) to d) is the most correct.\n\n2. Kerosene tin\na) 1.5 kl\nb) 7 ml\nc) 2 L\nd) 5 cl",
    "answer_text": "2 L",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b015-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Exercise 7.4: Estimate capacity of everyday containers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.4: Estimate capacity of everyday containers\n\nEstimate the capacity of the following containers by deciding which one of the options a) to d) is the most correct.\n\n3. Water bucket\na) 750 cl\nb) 35 cl\nc) 550 ml\nd) 45 L",
    "answer_text": "750 cl",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b015-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Exercise 7.4: Estimate capacity of everyday containers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.4: Estimate capacity of everyday containers\n\nEstimate the capacity of the following containers by deciding which one of the options a) to d) is the most correct.\n\n4. Petrol tank of a small car\na) 850 ml\nb) 50 L\nc) 950 L\nd) 15 kl",
    "answer_text": "50 L",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b015-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Exercise 7.4: Estimate capacity of everyday containers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.4: Estimate capacity of everyday containers\n\nEstimate the capacity of the following containers by deciding which one of the options a) to d) is the most correct.\n\n5. Petrol tanker (large truck that transports petrol)\na) 1,200 cl\nb) 950 cl\nc) 18 kl\nd) 75 L",
    "answer_text": "18 kl",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b016",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Estimate mass"
    },
    "content_text": "The mass of an object is a measure of how much matter is in that object. It tells us how heavy or how light the object is.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b017",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Estimate mass"
    },
    "content_text": "mass\n\nThe mass of an object is a measure of how much matter is in an object.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b018",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Estimate mass"
    },
    "content_text": "The SI unit for mass is the gram. A mass of one gram (1 g) is more or less equal to:\n\n- a small paperclip\n- one millilitre of pure water\n- a quarter teaspoon of sugar.\n\nOther units of measurement used often are multiples of ten of 1 g. The most common multiples are shown in the table below.\n\n$$\n\\begin{array}{|c|c|c|c|}\n      \\hline\n      \\textbf{Name} & \\textbf{Abbreviation} & \\textbf{Size} & \\textbf{Example} \\\\\n      \\hline\n      \\text{milligram} & \\text{mg} & 1\\text{ mg}=\\frac{1}{1,000}\\text{ g}=0,001\\text{ g} & \\text{small grain of sand } \\\\\n      \\hline\n      \\text{kilogram} & \\text{kg} & 1\\text{ kg}=1,000\\text{ g} & \\text{one litre of water} \\\\\n      \\hline\n      \\text{tonne} & \\text{t} & 1\\text{ t}=1,000,000\\text{ g}=1,000\\text{ kg} & \\text{small car } \\\\\n      \\hline\n      \\end{array}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b019",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Worked example 7.3: Evaluating an estimation of mass"
    },
    "content_text": "",
    "prompt_text": "Danladi's mother sends his to the corner shop to buy a cup of rice. He carries it home in a small bag. He estimates that the mass of the rice is 50 g. Evaluate his estimation.",
    "answer_text": "Step 1: Evaluate whether the unit of measurement is appropriate.\n\nThink about how light 1 g is. It is about a quarter teaspoon of sugar. This is not a lot compared to a cup of rice.\n\nIt might be better to use kilograms, but then Danladi would need to use a decimal point in his estimation. To avoid the decimal point, gram is an appropriate unit.\n\nStep 2: Evaluate whether the value of the estimation makes sense.\n\nThe mass of a teaspoon of sugar is about 4 g. So 50 g of sugar is $\\frac{50}{4}$ = 12.5 teaspoons. Even though the same amount of sugar and rice have different masses, there is a big difference between 12.5 teaspoons and 1 cup.\n\nDanladi's estimation does not make sense. An estimation of 150 g would be a better estimation.",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b020",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.5: Estimate mass of objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.5: Estimate mass of objects\n\nEstimate the mass of the following objects. Include an appropriate unit of measurement in each case. Then use an electronic balance from the science laboratory or a kitchen scale to get the real measurements. Compare the real measurements to your estimations.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b020-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.5: Estimate mass of objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.5: Estimate mass of objects\n\n1. Your eraser",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b020-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.5: Estimate mass of objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.5: Estimate mass of objects\n\n2. One of your pens",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b020-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.5: Estimate mass of objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.5: Estimate mass of objects\n\n3. Your thinnest textbook",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b020-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.5: Estimate mass of objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.5: Estimate mass of objects\n\n4. Full box of chalk",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b020-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.5: Estimate mass of objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.5: Estimate mass of objects\n\n5. Volleyball",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b021",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.6: Estimate mass of everyday objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.6: Estimate mass of everyday objects\n\nEstimate the mass of the following objects by deciding which one of the options a) to d) is the most correct.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b021-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.6: Estimate mass of everyday objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.6: Estimate mass of everyday objects\n\n1. 50 kobo coin\n   a. 8 mg\n   b. 5.5 g\n   c. 250 g\n   d. 1.5 kg",
    "answer_text": "b) 5.5 g",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b021-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.6: Estimate mass of everyday objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.6: Estimate mass of everyday objects\n\n2. Packet of sugar cubes\n   a. 475 g\n   b. 45 g\n   c. 550 mg\n   d. 45 kg",
    "answer_text": "a) 475 g",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b021-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.6: Estimate mass of everyday objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.6: Estimate mass of everyday objects\n\n3. Basketball\n   a. 950 mg\n   b. 45 g\n   c. 625 g\n   d. 12 kg",
    "answer_text": "c) 625 g",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b021-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.6: Estimate mass of everyday objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.6: Estimate mass of everyday objects\n\n4. A male teenager\n   a. 250 kg\n   b. 70 kg\n   c. 950 g\n   d. 0.5 t",
    "answer_text": "b) 70 kg",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b021-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.6: Estimate mass of everyday objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.6: Estimate mass of everyday objects\n\n5. An adult cow\n   a. 65 kg\n   b. 700 kg\n   c. 50 t\n   d. 850 g",
    "answer_text": "b) 700 kg",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b038-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.9: Evaluate test answers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.9: Evaluate test answers\n\n2. The capacity of a teaspoon is 5 L.",
    "answer_text": "The wrong unit was used. It must be 5 ml.",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b038-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.9: Evaluate test answers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.9: Evaluate test answers\n\n4. The mass of a woman is 27 kg.",
    "answer_text": "The numbers were swapped. It must be 72 kg.",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b038-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.9: Evaluate test answers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.9: Evaluate test answers\n\n5. $50\\text{ mg}=50,000\\text{ g}$",
    "answer_text": "Multiplication instead of division was done. It must be $50\\text{ mg}=\\frac{50}{1,000}=0.05\\text{ g}$.",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b041-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.10: Use estimation and approximation to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.10: Use estimation and approximation to solve problems\n\n5. A soft drink bottle has a capacity of 33 cl. At the factory, the bottles are filled from a container with a capacity of 21.3 kl. Approximately how many bottles can be filled from the container?",
    "answer_text": "$$\\begin{align}\n\\frac{21.3\\text{ kl}}{33\\text{ cl}} &= \\frac{2,130,000\\text{ cl}}{33\\text{ cl}} \\\\\n&\\approx \\frac{2,100,000}{30} \\\\\n&\\approx 70,000\\text{ bottles}\n\\end{align}$$",
    "primary_subtopic_id": "jss1-math-approximation-quantitative-reasoning"
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
    "record_id": "ch07-b041-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.10: Use estimation and approximation to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.10: Use estimation and approximation to solve problems\n\n7. A man gets 17 bowls of rice from a sack of 51.15 kg. What is the approximate mass of rice needed for 5 bowls?",
    "answer_text": "$$\\begin{align}\n\\frac{51.15\\text{ kg}}{17}\\times 5 &\\approx \\frac{50\\text{ kg}}{20}\\times 5 \\\\\n&\\approx \\frac{5}{2}\\text{ kg}\\times 5 \\\\\n&\\approx \\frac{25}{2}\\text{ kg} \\\\\n&\\approx 12.5\\text{ kg}\n\\end{align}$$",
    "primary_subtopic_id": "jss1-math-approximation-quantitative-reasoning"
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
  "subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects",
  "subtopic_title": "Estimation of capacity and mass of objects",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects-po01",
        "source_performance_objective_index": 1,
        "text": "Estimate the capacity and mass of given objects"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "estimation-of-capacity-and-mass-of-objects-ao-estimate-capacity",
          "text": "Estimate the capacity of given objects."
        },
        {
          "atomic_objective_id": "estimation-of-capacity-and-mass-of-objects-ao-estimate-mass",
          "text": "Estimate the mass of given objects."
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
    "record_id": "ch07-b010",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": null
    },
    "content_text": "Volume is the amount of space occupied by an object or the amount of space inside a container. The amount of liquid that a container can hold is called the capacity of the container.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b011",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": null
    },
    "content_text": "**capacity**\nThe amount of liquid that a container can hold is called the capacity of the container.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b012",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": null
    },
    "content_text": "The SI unit for capacity is the litre. A capacity of one litre (1 L) is more or less equal to:\n\n- six cups of tea\n- a carton of milk\n- three cans of soft drink.\n\nOther units of measurement used often are multiples of ten of 1 L. The most common multiples are shown in the table below.\n\n$$\n\\begin{array}{|c|c|c|c|}\n      \\hline\n      \\textbf{Name} & \\textbf{Abbreviation} & \\textbf{Size} & \\textbf{Example} \\\\\n      \\hline\n      \\text{millilitre} & \\text{ml} & 1\\text{ ml}=\\frac{1}{1,000}\\text{ L}=0,001\\text{ L} & \\text{twenty drops of water } \\\\\n      \\hline\n      \\text{centilitre} & \\text{cl} & 1\\text{ cl}=\\frac{1}{100}\\text{ L}=0,01\\text{ L} & \\text{two teaspoons of water} \\\\\n      \\hline\n      \\text{kilolitre} & \\text{kl} & 1\\text{ kl}=1,000\\text{ L} & \\text{medium-sized inflatable swimming pool} \\\\\n      \\hline\n      \\end{array}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b013",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Worked example 7.2: Evaluating an estimation of capacity"
    },
    "content_text": "",
    "prompt_text": "Amaka is feeling sick. The doctor gives her a bottle of medicine. She estimates that the capacity of the bottle is 250 cl. Evaluate her estimation.",
    "answer_text": "Step 1: Evaluate whether the unit of measurement is appropriate.\n\nThink about how much liquid 1 cl is. It is about two teaspoons.\n\nOne teaspoon is about 5 ml. The instructions on a bottle of medicine normally tells you how many teaspoons to take at time. Therefore, both millilitres and centilitres are appropriate units.\n\nStep 2: Evaluate whether the value of the estimation makes sense.\n\nIf there is 250 cl in the bottle, it means the bottle holds 500 teaspoons of medicine.\n\nAt two teaspoons twice a day, it would take $\\frac{500}{4}=125$ days to finish the medicine. That is more than 4 months! It is not possible to get so much medicine from a normal medicine bottle.\n\nAmaka's estimation does not make sense. An estimation of 25 cl, which is 250 ml, would be a better estimation.",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b014",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Exercise 7.3: Estimate capacity of containers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.3: Estimate capacity of containers\n\nYou might use the containers listed below at school or at home. Estimate the capacity of the containers. Include an appropriate unit of measurement in each case. Then use measuring cylinders from the science laboratory, or a set of measuring spoons and cups used for baking, to get the real measurements. Compare the real measurements to your estimations.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b014-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Exercise 7.3: Estimate capacity of containers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.3: Estimate capacity of containers\n\nYou might use the containers listed below at school or at home. Estimate the capacity of the containers. Include an appropriate unit of measurement in each case. Then use measuring cylinders from the science laboratory, or a set of measuring spoons and cups used for baking, to get the real measurements. Compare the real measurements to your estimations.\n\n1. Tea cup",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b014-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Exercise 7.3: Estimate capacity of containers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.3: Estimate capacity of containers\n\nYou might use the containers listed below at school or at home. Estimate the capacity of the containers. Include an appropriate unit of measurement in each case. Then use measuring cylinders from the science laboratory, or a set of measuring spoons and cups used for baking, to get the real measurements. Compare the real measurements to your estimations.\n\n2. Soft drink bottle",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b014-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Exercise 7.3: Estimate capacity of containers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.3: Estimate capacity of containers\n\nYou might use the containers listed below at school or at home. Estimate the capacity of the containers. Include an appropriate unit of measurement in each case. Then use measuring cylinders from the science laboratory, or a set of measuring spoons and cups used for baking, to get the real measurements. Compare the real measurements to your estimations.\n\n3. Test tube",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b014-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Exercise 7.3: Estimate capacity of containers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.3: Estimate capacity of containers\n\nYou might use the containers listed below at school or at home. Estimate the capacity of the containers. Include an appropriate unit of measurement in each case. Then use measuring cylinders from the science laboratory, or a set of measuring spoons and cups used for baking, to get the real measurements. Compare the real measurements to your estimations.\n\n4. Lunch box",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b014-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Exercise 7.3: Estimate capacity of containers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.3: Estimate capacity of containers\n\nYou might use the containers listed below at school or at home. Estimate the capacity of the containers. Include an appropriate unit of measurement in each case. Then use measuring cylinders from the science laboratory, or a set of measuring spoons and cups used for baking, to get the real measurements. Compare the real measurements to your estimations.\n\n5. Water glass",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b015",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Exercise 7.4: Estimate capacity of everyday containers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.4: Estimate capacity of everyday containers\n\nEstimate the capacity of the following containers by deciding which one of the options a) to d) is the most correct.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b015-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Exercise 7.4: Estimate capacity of everyday containers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.4: Estimate capacity of everyday containers\n\nEstimate the capacity of the following containers by deciding which one of the options a) to d) is the most correct.\n\n1. Milk tin\na) 3 cl\nb) 25 ml\nc) 300 cl\nd) 350 ml",
    "answer_text": "350 ml",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b015-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Exercise 7.4: Estimate capacity of everyday containers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.4: Estimate capacity of everyday containers\n\nEstimate the capacity of the following containers by deciding which one of the options a) to d) is the most correct.\n\n2. Kerosene tin\na) 1.5 kl\nb) 7 ml\nc) 2 L\nd) 5 cl",
    "answer_text": "2 L",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b015-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Exercise 7.4: Estimate capacity of everyday containers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.4: Estimate capacity of everyday containers\n\nEstimate the capacity of the following containers by deciding which one of the options a) to d) is the most correct.\n\n3. Water bucket\na) 750 cl\nb) 35 cl\nc) 550 ml\nd) 45 L",
    "answer_text": "750 cl",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b015-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Exercise 7.4: Estimate capacity of everyday containers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.4: Estimate capacity of everyday containers\n\nEstimate the capacity of the following containers by deciding which one of the options a) to d) is the most correct.\n\n4. Petrol tank of a small car\na) 850 ml\nb) 50 L\nc) 950 L\nd) 15 kl",
    "answer_text": "50 L",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b015-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.2 Capacity",
      "h3": "Exercise 7.4: Estimate capacity of everyday containers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.4: Estimate capacity of everyday containers\n\nEstimate the capacity of the following containers by deciding which one of the options a) to d) is the most correct.\n\n5. Petrol tanker (large truck that transports petrol)\na) 1,200 cl\nb) 950 cl\nc) 18 kl\nd) 75 L",
    "answer_text": "18 kl",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b016",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Estimate mass"
    },
    "content_text": "The mass of an object is a measure of how much matter is in that object. It tells us how heavy or how light the object is.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b017",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Estimate mass"
    },
    "content_text": "mass\n\nThe mass of an object is a measure of how much matter is in an object.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b018",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Estimate mass"
    },
    "content_text": "The SI unit for mass is the gram. A mass of one gram (1 g) is more or less equal to:\n\n- a small paperclip\n- one millilitre of pure water\n- a quarter teaspoon of sugar.\n\nOther units of measurement used often are multiples of ten of 1 g. The most common multiples are shown in the table below.\n\n$$\n\\begin{array}{|c|c|c|c|}\n      \\hline\n      \\textbf{Name} & \\textbf{Abbreviation} & \\textbf{Size} & \\textbf{Example} \\\\\n      \\hline\n      \\text{milligram} & \\text{mg} & 1\\text{ mg}=\\frac{1}{1,000}\\text{ g}=0,001\\text{ g} & \\text{small grain of sand } \\\\\n      \\hline\n      \\text{kilogram} & \\text{kg} & 1\\text{ kg}=1,000\\text{ g} & \\text{one litre of water} \\\\\n      \\hline\n      \\text{tonne} & \\text{t} & 1\\text{ t}=1,000,000\\text{ g}=1,000\\text{ kg} & \\text{small car } \\\\\n      \\hline\n      \\end{array}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b019",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Worked example 7.3: Evaluating an estimation of mass"
    },
    "content_text": "",
    "prompt_text": "Danladi's mother sends his to the corner shop to buy a cup of rice. He carries it home in a small bag. He estimates that the mass of the rice is 50 g. Evaluate his estimation.",
    "answer_text": "Step 1: Evaluate whether the unit of measurement is appropriate.\n\nThink about how light 1 g is. It is about a quarter teaspoon of sugar. This is not a lot compared to a cup of rice.\n\nIt might be better to use kilograms, but then Danladi would need to use a decimal point in his estimation. To avoid the decimal point, gram is an appropriate unit.\n\nStep 2: Evaluate whether the value of the estimation makes sense.\n\nThe mass of a teaspoon of sugar is about 4 g. So 50 g of sugar is $\\frac{50}{4}$ = 12.5 teaspoons. Even though the same amount of sugar and rice have different masses, there is a big difference between 12.5 teaspoons and 1 cup.\n\nDanladi's estimation does not make sense. An estimation of 150 g would be a better estimation.",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b020",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.5: Estimate mass of objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.5: Estimate mass of objects\n\nEstimate the mass of the following objects. Include an appropriate unit of measurement in each case. Then use an electronic balance from the science laboratory or a kitchen scale to get the real measurements. Compare the real measurements to your estimations.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b020-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.5: Estimate mass of objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.5: Estimate mass of objects\n\n1. Your eraser",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b020-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.5: Estimate mass of objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.5: Estimate mass of objects\n\n2. One of your pens",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b020-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.5: Estimate mass of objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.5: Estimate mass of objects\n\n3. Your thinnest textbook",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b020-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.5: Estimate mass of objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.5: Estimate mass of objects\n\n4. Full box of chalk",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b020-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.5: Estimate mass of objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.5: Estimate mass of objects\n\n5. Volleyball",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b021",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.6: Estimate mass of everyday objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.6: Estimate mass of everyday objects\n\nEstimate the mass of the following objects by deciding which one of the options a) to d) is the most correct.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b021-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.6: Estimate mass of everyday objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.6: Estimate mass of everyday objects\n\n1. 50 kobo coin\n   a. 8 mg\n   b. 5.5 g\n   c. 250 g\n   d. 1.5 kg",
    "answer_text": "b) 5.5 g",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b021-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.6: Estimate mass of everyday objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.6: Estimate mass of everyday objects\n\n2. Packet of sugar cubes\n   a. 475 g\n   b. 45 g\n   c. 550 mg\n   d. 45 kg",
    "answer_text": "a) 475 g",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b021-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.6: Estimate mass of everyday objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.6: Estimate mass of everyday objects\n\n3. Basketball\n   a. 950 mg\n   b. 45 g\n   c. 625 g\n   d. 12 kg",
    "answer_text": "c) 625 g",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b021-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.6: Estimate mass of everyday objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.6: Estimate mass of everyday objects\n\n4. A male teenager\n   a. 250 kg\n   b. 70 kg\n   c. 950 g\n   d. 0.5 t",
    "answer_text": "b) 70 kg",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b021-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.1 Estimation",
      "h3": "Exercise 7.6: Estimate mass of everyday objects"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.6: Estimate mass of everyday objects\n\n5. An adult cow\n   a. 65 kg\n   b. 700 kg\n   c. 50 t\n   d. 850 g",
    "answer_text": "b) 700 kg",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b038-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.9: Evaluate test answers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.9: Evaluate test answers\n\n2. The capacity of a teaspoon is 5 L.",
    "answer_text": "The wrong unit was used. It must be 5 ml.",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b038-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.9: Evaluate test answers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.9: Evaluate test answers\n\n4. The mass of a woman is 27 kg.",
    "answer_text": "The numbers were swapped. It must be 72 kg.",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b038-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.9: Evaluate test answers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.9: Evaluate test answers\n\n5. $50\\text{ mg}=50,000\\text{ g}$",
    "answer_text": "Multiplication instead of division was done. It must be $50\\text{ mg}=\\frac{50}{1,000}=0.05\\text{ g}$.",
    "primary_subtopic_id": "jss1-math-estimation-estimation-of-capacity-and-mass-of-objects"
  },
  {
    "record_id": "ch07-b041-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.10: Use estimation and approximation to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.10: Use estimation and approximation to solve problems\n\n5. A soft drink bottle has a capacity of 33 cl. At the factory, the bottles are filled from a container with a capacity of 21.3 kl. Approximately how many bottles can be filled from the container?",
    "answer_text": "$$\\begin{align}\n\\frac{21.3\\text{ kl}}{33\\text{ cl}} &= \\frac{2,130,000\\text{ cl}}{33\\text{ cl}} \\\\\n&\\approx \\frac{2,100,000}{30} \\\\\n&\\approx 70,000\\text{ bottles}\n\\end{align}$$",
    "primary_subtopic_id": "jss1-math-approximation-quantitative-reasoning"
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
    "record_id": "ch07-b041-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 7: Estimation and approximation",
      "h2": "7.3 Practical applications",
      "h3": "Exercise 7.10: Use estimation and approximation to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 7.10: Use estimation and approximation to solve problems\n\n7. A man gets 17 bowls of rice from a sack of 51.15 kg. What is the approximate mass of rice needed for 5 bowls?",
    "answer_text": "$$\\begin{align}\n\\frac{51.15\\text{ kg}}{17}\\times 5 &\\approx \\frac{50\\text{ kg}}{20}\\times 5 \\\\\n&\\approx \\frac{5}{2}\\text{ kg}\\times 5 \\\\\n&\\approx \\frac{25}{2}\\text{ kg} \\\\\n&\\approx 12.5\\text{ kg}\n\\end{align}$$",
    "primary_subtopic_id": "jss1-math-approximation-quantitative-reasoning"
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
