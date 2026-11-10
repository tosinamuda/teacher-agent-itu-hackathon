# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-4",
  "topic_key": "jss1-math-angles",
  "topic": "Angles",
  "subtopic_id": "jss1-math-angles-measurement-of-angles",
  "subtopic_title": "Measurement of angles.",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-angles-measurement-of-angles-po01",
        "source_performance_objective_index": 1,
        "text": "Measure angles"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "measurement-of-angles-ao-measure-angles",
          "text": "Measure angles."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch15-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": null,
      "h3": null
    },
    "content_text": "In this chapter you will work with **angles**. You will learn how to label and measure angles. You will also learn about the different angles that are formed on a straight line when straight lines cross each other.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b002",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": null,
      "h3": null
    },
    "content_text": "**angle** An angle is the amount of turn between two straight lines that have a common end point. The common end point is called the vertex of the angle.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-001.png",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b003",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": null
    },
    "content_text": "We measure angles in degrees. Before we can measure angles, we need to know how to label angles.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b004",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Labelling angles"
    },
    "content_text": "When we label an angle, we name the angle, so that we know which angle it is that we are talking about.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b005",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Worked example 15.1: Labelling angles"
    },
    "content_text": "",
    "prompt_text": "Consider the following diagram.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_030.png\n\nGive the correct label for the marked angle.",
    "answer_text": "Step 1: Remember that there are three different ways to indicate an angle.\n\n- We may indicate an angle with a $\\hat{\\phantom{0}}$ above the name of the point where the angle is formed.\n- We may show $\\angle$ in front of the name of the point.\n- We may use the names of the lines that form the angle.\n\nStep 2: Find the marked angle on the diagram.\n\nThere is only one angle at point $U$.\n\nStep 3: Give the correct answer.\n\nWe can label this angle as $\\hat{U}$ or $\\angle U$.\n\nWe could also label this angle as $V\\hat{U}T$ or $T\\hat{U}V$.\n\nHint: To use the names of the lines that form the angle, trace over the angle with your finger, and label the angle in the order of line labels that you followed.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b006",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Labelling angles"
    },
    "content_text": "From now on we will use only one notation. We will label the angle at point $A$ as $\\hat{A}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b007",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Worked example 15.2: Labelling angles"
    },
    "content_text": "",
    "prompt_text": "Consider the following diagram.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_031.png\n\nGive the correct label for the marked angle.",
    "answer_text": "Step 1: Find the marked angle in the diagram.\n\nThere are two different angles at point $A$. If we just write $\\hat{A}$, it will be unclear which angle we mean.\n\nSupporting image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-1_021.png\n\nTo make sure that we are understood correctly, we have to label the marked angle using the names of the lines that form it.\n\nStep 2: Give the correct answer.\n\nThe marked angle can be labelled as $C\\hat{A}D$ or $D\\hat{A}C$.\n\nSupporting image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-2_004.png",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b008",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Labelling angles"
    },
    "content_text": "It is easy to make a mistake if you have to refer to an angle as $C\\hat{A}D$ or $D\\hat{A}C$. It is also time consuming, so we often use small numbers to label angles. We use these to refer more easily to a specific angle. You can tell that these small numbers are not the sizes of the angles, as they are not labelled with the degree symbol and the numbers are much too small.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b009",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Worked example 15.3: Labelling angles"
    },
    "content_text": "",
    "prompt_text": "Consider the following diagram.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_061.png\n\nGive the correct label for the marked angle.",
    "answer_text": "Step 1: Find the marked angle in the diagram.\n\nThere are two different angles at point $S$, so if we just write $\\hat{S}$ it will be unclear which angle we mean.\n\nAsk yourself the following: At what point and number is the marked angle?\n\nReference image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-1_047.png\n\nStep 2: Give the correct answer.\n\nTo make sure that we are understood, we use the point label $S$ and the relevant number ($\\text{1}$) to label the angle as ${\\hat{S}}_{1}$.\n\nIt would also be correct to label the angle as $P\\hat{S}Q$ or $Q\\hat{S}P$. However, we do not label angles as $P{\\hat{S}}_{1}Q$, because it is not necessary to use both the angle number and all three line labels.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b010",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.1: Label angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.1: Label angles",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b010-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.1: Label angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.1: Label angles\n\n1. Consider the following diagram. Give the correct label for the marked angle.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_025.png",
    "answer_text": "There is only one angle at point $D$, so we can label this angle as $\\hat{D}$ without any confusion.\n\nWe could also label this angle as $A\\hat{D}B$ or $B\\hat{D}A$. If you trace your finger over the points in this order, you will draw the angle.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b010-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.1: Label angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.1: Label angles\n\n2. Consider the following diagram. Give the correct label for the marked angle.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-002.png",
    "answer_text": "There are two different angles at point $Q$. If we just write $\\hat{Q}$ it will be unclear which angle we mean.\n\nThe marked angle can be labelled as $S\\hat{Q}R$ or $R\\hat{Q}S$.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b010-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.1: Label angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.1: Label angles\n\n3. Consider the following diagram. Give the correct label for the marked angle.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_063.png",
    "answer_text": "There are two different angles at point $D$. If we just write $\\hat{D}$ it will be unclear which angle we mean.\n\nWe use the point label $D$ and the relevant number $(\\text{2}$) to label the angle as ${\\hat{D}}_{2}$.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b010-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.1: Label angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.1: Label angles\n\n4. Consider the following diagram. Give the correct label for the marked angle.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_044.png",
    "answer_text": "There are four different angles at point $T$. If we just write $\\hat{T}$ it will be unclear which angle we mean.\n\nTo make sure that we are understood, we use the point label $T$ and the relevant number ($\\text{4}$) to label the angle as ${\\hat{T}}_{4}$.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b010-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.1: Label angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.1: Label angles\n\n5. Consider the following diagram. How would you mark ${\\hat{T}}_{3}$?\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-003.png",
    "answer_text": "Mark the angle labelled ${\\hat{T}}_{3}$ on the diagram as shown in the solution image.\n\nSolution image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-004.png",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b011",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Measuring angles"
    },
    "content_text": "We measure angles in degrees. We use a protractor to measure an angle.\n\nProtractor image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-005.png\n\nTake note of the following when you use a protractor:\n\n- A protractor has a centre, which can also be called the origin.\n  Origin image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-006.png\n  When you measure an angle you have to make sure that the centre (or origin) of the protractor is exactly on the vertex of the angle that you want to measure.\n\n- The centre (or origin) of a protractor is on the base line of the protractor.\n  Base line image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-007.png\n  When you measure an angle you also have to make sure that one side of the base line of the protractor is exactly on one of the arms of the angle that you want to measure.\n\n- There are two zeroes on a protractor.\n  If you begin measuring from the zero on the left hand side of the protractor, you use the outer scale on the protractor.\n  Outer-scale image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-008.png\n  If you begin measuring from the zero on the right hand side of the protractor, you use the inner scale on the protractor.\n  Inner-scale image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-009.png",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b012",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Measuring angles"
    },
    "content_text": "It is a good idea to estimate the size of an angle before you measure the angle. Then you can be sure that you are reading off the correct answer from the protractor.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b013",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Types of angles"
    },
    "content_text": "Different types of angles have different names. The names you may need to use when working with angles are given in the table below.\n\n| Name of angle | Size of angle |\n| --- | --- |\n| acute angle | between $0^{\\circ}$ and $90^{\\circ}$ |\n| right angle | $90^{\\circ}$ |\n| obtuse angle | between $90^{\\circ}$ and $180^{\\circ}$ |\n| straight angle | $180^{\\circ}$ |\n| reflex angle | between $180^{\\circ}$ and $360^{\\circ}$ |\n| revolution | $360^{\\circ}$ |",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b014",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Worked example 15.4: Measuring a right angle"
    },
    "content_text": "",
    "prompt_text": "Use a protractor to measure the given angle in the diagram below.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-010.png",
    "answer_text": "Step 1: Consider the diagram and estimate the size of the angle.\n\nThe diagram shows two arms: $AC$ and $AB$. It seems as if they form a right angle, which is shaded green. A right angle is equal to $90^{\\circ}$.\n\nStep 2: Place the protractor correctly on the angle.\n\nPlacement image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-011.png\n\n- The centre of the protractor should be on the vertex of the angle.\n- The base line of the protractor should be on one arm of the angle.\n\nStep 3: Choose the scale you will use.\n\nThe arm on which the base line lies is to the right side of the protractor. On the right side, it is the inner scale that starts from 0, so use the inner scale.\n\nStep 4: Read off the size of the angle from the protractor, and give the answer. Name the angle correctly, and remember to include the degree symbol.\n\n$$\nB\\hat{A}C = 90^{\\circ}\n$$",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b015",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Worked example 15.5: Measuring an acute angle"
    },
    "content_text": "",
    "prompt_text": "Use a protractor to measure the marked angle shown below.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-012.png",
    "answer_text": "Step 1: Consider the diagram and estimate the size of the angle.\n\nThe angle shaded red is between two arms: $PS$ and $PT$. It seems that the marked angle is an acute angle.\n\nAn acute angle is between $0^{\\circ}$ and $90^{\\circ}$. This angle is nearer to $90^{\\circ}$ than to $0^{\\circ}$.\n\nStep 2: Place the protractor correctly on the angle.\n\nPlacement image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-013.png\n\n- The centre of the protractor should be on the vertex of the angle.\n- The base line of the protractor should be on one arm of the angle.\n\nStep 3: Choose the correct scale.\n\nThe arm on which the base line lies is to the right side of the protractor, so use the inner scale.\n\nStep 4: Read off the size of the angle from the protractor, and check against your estimation.\n\n$67^{\\circ}$ is an acute angle, and is closer to $90^{\\circ}$ than to $0^{\\circ}$.\n\nStep 5: Name the angle, and give the answer.\n\n$$\nS\\hat{P}T = 67^{\\circ}\n$$",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b016",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Worked example 15.6: Measuring an obtuse angle"
    },
    "content_text": "",
    "prompt_text": "Use a protractor to measure the marked angle shown below.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-014.png\n\nUse the dotted lines shown to help with your estimation. The dotted lines have a $90^{\\circ}$ angle between them.",
    "answer_text": "Step 1: Consider the diagram and estimate the size of the angle.\n\nThe diagram shows two arms: $AB$ and $AC$. It seems as if they form an obtuse angle, which is shaded red.\n\nAn obtuse angle is between $90^{\\circ}$ and $180^{\\circ}$. This angle is almost a full straight angle, so it must be very close to $180^{\\circ}$.\n\nStep 2: Place the protractor correctly on the angle.\n\nPlacement image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-015.png\n\n- The centre of the protractor should be on the vertex of the angle.\n- The base line of the protractor should be on one arm of the angle.\n\nStep 3: Choose the correct scale.\n\nThe arm on which the base line lies is to the right side of the protractor, so use the inner scale.\n\nStep 4: Read off the size of the angle from the protractor, and check against your estimation.\n\n$175^{\\circ}$ is an obtuse angle, and is close to $180^{\\circ}$.\n\nStep 5: Name the angle, and give the answer.\n\n$$\nB\\hat{A}C = 175^{\\circ}\n$$",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b017",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Worked example 15.7: Measuring a reflex angle"
    },
    "content_text": "",
    "prompt_text": "Use a protractor and measure the angle shown below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-016.png]",
    "answer_text": "Step 1: Consider the diagram and estimate the size of the angle.\n\nThe diagram shows two arms: $XY$ and $XZ$. They form a reflex angle, which is shaded red.\n\nA reflex angle is between $180^{\\circ}$ and $360^{\\circ}$. This angle is very near to $360^{\\circ}$.\n\nStep 2: Find a way to measure this reflex angle.\n\nAn ordinary protractor can only measure angles between $0^{\\circ}$ to $180^{\\circ}$. We cannot measure a reflex angle with an ordinary protractor. We have to measure the angle that is not shaded and then subtract the answer from $360^{\\circ}$.\n\nStep 3: Place the protractor correctly on the angle to measure.\n\n[Protractor placement image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-017.png]\n\n- The centre of the protractor should be on the vertex of the angle.\n- The base line of the protractor should be on one arm of the angle.\n\nStep 4: Choose the scale and read off the size of the angle.\n\nThe acute angle measures $18^{\\circ}$.\n\nStep 5: Subtract the measured angle from $360^{\\circ}$ and give the correct answer. Check against your estimation, and name the reflex angle correctly.\n\nReflex $Z\\hat{X}Y = 360^{\\circ} - 18^{\\circ} = 342^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b018",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Types of angles"
    },
    "content_text": "Remember that reflex angles are always less than $360^{\\circ}$, but more than $180^{\\circ}$. A full turn or revolution is equal to $360^{\\circ}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b019",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.2: Measure angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.2: Measure angles",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b019-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.2: Measure angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.2: Measure angles\n\n1. Use a protractor and measure the angle shown below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-018.png]",
    "answer_text": "Estimate the size of the angle: The angle is an acute angle, so the measurement should be between $0^{\\circ}$ and $90^{\\circ}$.\n\nMeasure the angle with a protractor.\n\nAnswer: $B\\hat{A}C = 53^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b019-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.2: Measure angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.2: Measure angles\n\n2. Use a protractor and measure the angle shown below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-019.png]",
    "answer_text": "Estimate: acute angle, so between $0^{\\circ}$ and $90^{\\circ}$.\n\nAnswer: $B\\hat{A}C = 59^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b019-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.2: Measure angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.2: Measure angles\n\n3. Use a protractor and measure the angle shown below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-020.png]",
    "answer_text": "Estimate: obtuse angle, so between $90^{\\circ}$ and $180^{\\circ}$.\n\nAnswer: $B\\hat{A}C = 112^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b019-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.2: Measure angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.2: Measure angles\n\n4. Use a protractor and measure the angle shown below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-021.png]",
    "answer_text": "Estimate: obtuse angle, so between $90^{\\circ}$ and $180^{\\circ}$.\n\nAnswer: $B\\hat{A}C = 150^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b019-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.2: Measure angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.2: Measure angles\n\n5. Use a protractor and measure the angle shown below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-022.png]",
    "answer_text": "Estimate: reflex angle, so between $180^{\\circ}$ and $360^{\\circ}$.\n\nMeasure the angle that is not shaded and then subtract the answer from $360^{\\circ}$.\n\nAcute $Z\\hat{X}Y = 70^{\\circ}$.\n\nSubtract to find the size of the reflex angle: Reflex $Z\\hat{X}Y = 360^{\\circ} - 70^{\\circ} = 290^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b019-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.2: Measure angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.2: Measure angles\n\n6. Use a protractor and measure the angle shown below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-023.png]",
    "answer_text": "Estimate: reflex angle, so between $180^{\\circ}$ and $360^{\\circ}$.\n\nMeasure the angle that is not shaded and then subtract the answer from $360^{\\circ}$.\n\nAcute $C\\hat{A}B = 49^{\\circ}$.\n\nSubtract to find the size of the reflex angle: Reflex $C\\hat{A}B = 360^{\\circ} - 49^{\\circ} = 311^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b064",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.5 Summary",
      "h3": null
    },
    "content_text": "An angle is the amount of turn between two straight lines that have a common end point, called the vertex of the angle.\n\nWe use a protractor to measure angles in degrees. Always estimate an angle before you measure it, so you can check whether your answer seems correct.\n\nDifferent types of angles used in this chapter include:\n\n- acute angle: between $0^{\\circ}$ and $90^{\\circ}$\n- right angle: $90^{\\circ}$\n- obtuse angle: between $90^{\\circ}$ and $180^{\\circ}$\n- straight angle: $180^{\\circ}$\n- reflex angle: between $180^{\\circ}$ and $360^{\\circ}$\n- revolution: $360^{\\circ}$\n\nA straight line is also called a straight angle. A straight angle is equal to $180^{\\circ}$.\n\nIf a straight line is formed by more than one angle, the sum of those angles will be $180^{\\circ}$. We say the angles are supplementary angles.\n\nAdjacent angles are next to each other. Two adjacent angles share the same vertex and one common arm.\n\nWhen two lines cross each other, we say they are intersecting lines.\n\nTwo intersecting straight lines form vertically opposite angles, which have the same vertex and are on opposite sides of the vertex. Vertically opposite angles are equal.\n\nParallel lines are always the same distance apart, and are indicated using arrow symbols.\n\nA transversal intersects two or more parallel lines.\n\nThere are three types of angles formed by parallel lines and a transversal:\n\n- Corresponding angles are in matching positions on the parallel lines and the transversal, and make an F shape. Corresponding angles on parallel lines are equal.\n- Co-interior angles are inside the parallel lines and on the same side of the transversal. They make a U shape. Co-interior angles on parallel lines are supplementary and add up to $180^{\\circ}$.\n- Alternate angles are inside the parallel lines, but on different sides of the transversal. They make an N shape. Alternate angles on parallel lines are equal.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
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
  "topic_key": "jss1-math-angles",
  "topic": "Angles",
  "subtopic_id": "jss1-math-angles-measurement-of-angles",
  "subtopic_title": "Measurement of angles.",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-angles-measurement-of-angles-po01",
        "source_performance_objective_index": 1,
        "text": "Measure angles"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "measurement-of-angles-ao-measure-angles",
          "text": "Measure angles."
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
    "record_id": "ch15-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": null,
      "h3": null
    },
    "content_text": "In this chapter you will work with **angles**. You will learn how to label and measure angles. You will also learn about the different angles that are formed on a straight line when straight lines cross each other.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b002",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": null,
      "h3": null
    },
    "content_text": "**angle** An angle is the amount of turn between two straight lines that have a common end point. The common end point is called the vertex of the angle.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-001.png",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b003",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": null
    },
    "content_text": "We measure angles in degrees. Before we can measure angles, we need to know how to label angles.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b004",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Labelling angles"
    },
    "content_text": "When we label an angle, we name the angle, so that we know which angle it is that we are talking about.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b005",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Worked example 15.1: Labelling angles"
    },
    "content_text": "",
    "prompt_text": "Consider the following diagram.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_030.png\n\nGive the correct label for the marked angle.",
    "answer_text": "Step 1: Remember that there are three different ways to indicate an angle.\n\n- We may indicate an angle with a $\\hat{\\phantom{0}}$ above the name of the point where the angle is formed.\n- We may show $\\angle$ in front of the name of the point.\n- We may use the names of the lines that form the angle.\n\nStep 2: Find the marked angle on the diagram.\n\nThere is only one angle at point $U$.\n\nStep 3: Give the correct answer.\n\nWe can label this angle as $\\hat{U}$ or $\\angle U$.\n\nWe could also label this angle as $V\\hat{U}T$ or $T\\hat{U}V$.\n\nHint: To use the names of the lines that form the angle, trace over the angle with your finger, and label the angle in the order of line labels that you followed.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b006",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Labelling angles"
    },
    "content_text": "From now on we will use only one notation. We will label the angle at point $A$ as $\\hat{A}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b007",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Worked example 15.2: Labelling angles"
    },
    "content_text": "",
    "prompt_text": "Consider the following diagram.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_031.png\n\nGive the correct label for the marked angle.",
    "answer_text": "Step 1: Find the marked angle in the diagram.\n\nThere are two different angles at point $A$. If we just write $\\hat{A}$, it will be unclear which angle we mean.\n\nSupporting image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-1_021.png\n\nTo make sure that we are understood correctly, we have to label the marked angle using the names of the lines that form it.\n\nStep 2: Give the correct answer.\n\nThe marked angle can be labelled as $C\\hat{A}D$ or $D\\hat{A}C$.\n\nSupporting image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-2_004.png",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b008",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Labelling angles"
    },
    "content_text": "It is easy to make a mistake if you have to refer to an angle as $C\\hat{A}D$ or $D\\hat{A}C$. It is also time consuming, so we often use small numbers to label angles. We use these to refer more easily to a specific angle. You can tell that these small numbers are not the sizes of the angles, as they are not labelled with the degree symbol and the numbers are much too small.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b009",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Worked example 15.3: Labelling angles"
    },
    "content_text": "",
    "prompt_text": "Consider the following diagram.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_061.png\n\nGive the correct label for the marked angle.",
    "answer_text": "Step 1: Find the marked angle in the diagram.\n\nThere are two different angles at point $S$, so if we just write $\\hat{S}$ it will be unclear which angle we mean.\n\nAsk yourself the following: At what point and number is the marked angle?\n\nReference image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-1_047.png\n\nStep 2: Give the correct answer.\n\nTo make sure that we are understood, we use the point label $S$ and the relevant number ($\\text{1}$) to label the angle as ${\\hat{S}}_{1}$.\n\nIt would also be correct to label the angle as $P\\hat{S}Q$ or $Q\\hat{S}P$. However, we do not label angles as $P{\\hat{S}}_{1}Q$, because it is not necessary to use both the angle number and all three line labels.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b010",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.1: Label angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.1: Label angles",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b010-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.1: Label angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.1: Label angles\n\n1. Consider the following diagram. Give the correct label for the marked angle.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_025.png",
    "answer_text": "There is only one angle at point $D$, so we can label this angle as $\\hat{D}$ without any confusion.\n\nWe could also label this angle as $A\\hat{D}B$ or $B\\hat{D}A$. If you trace your finger over the points in this order, you will draw the angle.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b010-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.1: Label angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.1: Label angles\n\n2. Consider the following diagram. Give the correct label for the marked angle.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-002.png",
    "answer_text": "There are two different angles at point $Q$. If we just write $\\hat{Q}$ it will be unclear which angle we mean.\n\nThe marked angle can be labelled as $S\\hat{Q}R$ or $R\\hat{Q}S$.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b010-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.1: Label angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.1: Label angles\n\n3. Consider the following diagram. Give the correct label for the marked angle.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_063.png",
    "answer_text": "There are two different angles at point $D$. If we just write $\\hat{D}$ it will be unclear which angle we mean.\n\nWe use the point label $D$ and the relevant number $(\\text{2}$) to label the angle as ${\\hat{D}}_{2}$.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b010-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.1: Label angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.1: Label angles\n\n4. Consider the following diagram. Give the correct label for the marked angle.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_044.png",
    "answer_text": "There are four different angles at point $T$. If we just write $\\hat{T}$ it will be unclear which angle we mean.\n\nTo make sure that we are understood, we use the point label $T$ and the relevant number ($\\text{4}$) to label the angle as ${\\hat{T}}_{4}$.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b010-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.1: Label angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.1: Label angles\n\n5. Consider the following diagram. How would you mark ${\\hat{T}}_{3}$?\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-003.png",
    "answer_text": "Mark the angle labelled ${\\hat{T}}_{3}$ on the diagram as shown in the solution image.\n\nSolution image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-004.png",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b011",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Measuring angles"
    },
    "content_text": "We measure angles in degrees. We use a protractor to measure an angle.\n\nProtractor image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-005.png\n\nTake note of the following when you use a protractor:\n\n- A protractor has a centre, which can also be called the origin.\n  Origin image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-006.png\n  When you measure an angle you have to make sure that the centre (or origin) of the protractor is exactly on the vertex of the angle that you want to measure.\n\n- The centre (or origin) of a protractor is on the base line of the protractor.\n  Base line image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-007.png\n  When you measure an angle you also have to make sure that one side of the base line of the protractor is exactly on one of the arms of the angle that you want to measure.\n\n- There are two zeroes on a protractor.\n  If you begin measuring from the zero on the left hand side of the protractor, you use the outer scale on the protractor.\n  Outer-scale image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-008.png\n  If you begin measuring from the zero on the right hand side of the protractor, you use the inner scale on the protractor.\n  Inner-scale image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-009.png",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b012",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Measuring angles"
    },
    "content_text": "It is a good idea to estimate the size of an angle before you measure the angle. Then you can be sure that you are reading off the correct answer from the protractor.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b013",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Types of angles"
    },
    "content_text": "Different types of angles have different names. The names you may need to use when working with angles are given in the table below.\n\n| Name of angle | Size of angle |\n| --- | --- |\n| acute angle | between $0^{\\circ}$ and $90^{\\circ}$ |\n| right angle | $90^{\\circ}$ |\n| obtuse angle | between $90^{\\circ}$ and $180^{\\circ}$ |\n| straight angle | $180^{\\circ}$ |\n| reflex angle | between $180^{\\circ}$ and $360^{\\circ}$ |\n| revolution | $360^{\\circ}$ |",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b014",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Worked example 15.4: Measuring a right angle"
    },
    "content_text": "",
    "prompt_text": "Use a protractor to measure the given angle in the diagram below.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-010.png",
    "answer_text": "Step 1: Consider the diagram and estimate the size of the angle.\n\nThe diagram shows two arms: $AC$ and $AB$. It seems as if they form a right angle, which is shaded green. A right angle is equal to $90^{\\circ}$.\n\nStep 2: Place the protractor correctly on the angle.\n\nPlacement image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-011.png\n\n- The centre of the protractor should be on the vertex of the angle.\n- The base line of the protractor should be on one arm of the angle.\n\nStep 3: Choose the scale you will use.\n\nThe arm on which the base line lies is to the right side of the protractor. On the right side, it is the inner scale that starts from 0, so use the inner scale.\n\nStep 4: Read off the size of the angle from the protractor, and give the answer. Name the angle correctly, and remember to include the degree symbol.\n\n$$\nB\\hat{A}C = 90^{\\circ}\n$$",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b015",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Worked example 15.5: Measuring an acute angle"
    },
    "content_text": "",
    "prompt_text": "Use a protractor to measure the marked angle shown below.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-012.png",
    "answer_text": "Step 1: Consider the diagram and estimate the size of the angle.\n\nThe angle shaded red is between two arms: $PS$ and $PT$. It seems that the marked angle is an acute angle.\n\nAn acute angle is between $0^{\\circ}$ and $90^{\\circ}$. This angle is nearer to $90^{\\circ}$ than to $0^{\\circ}$.\n\nStep 2: Place the protractor correctly on the angle.\n\nPlacement image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-013.png\n\n- The centre of the protractor should be on the vertex of the angle.\n- The base line of the protractor should be on one arm of the angle.\n\nStep 3: Choose the correct scale.\n\nThe arm on which the base line lies is to the right side of the protractor, so use the inner scale.\n\nStep 4: Read off the size of the angle from the protractor, and check against your estimation.\n\n$67^{\\circ}$ is an acute angle, and is closer to $90^{\\circ}$ than to $0^{\\circ}$.\n\nStep 5: Name the angle, and give the answer.\n\n$$\nS\\hat{P}T = 67^{\\circ}\n$$",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b016",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Worked example 15.6: Measuring an obtuse angle"
    },
    "content_text": "",
    "prompt_text": "Use a protractor to measure the marked angle shown below.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-014.png\n\nUse the dotted lines shown to help with your estimation. The dotted lines have a $90^{\\circ}$ angle between them.",
    "answer_text": "Step 1: Consider the diagram and estimate the size of the angle.\n\nThe diagram shows two arms: $AB$ and $AC$. It seems as if they form an obtuse angle, which is shaded red.\n\nAn obtuse angle is between $90^{\\circ}$ and $180^{\\circ}$. This angle is almost a full straight angle, so it must be very close to $180^{\\circ}$.\n\nStep 2: Place the protractor correctly on the angle.\n\nPlacement image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-015.png\n\n- The centre of the protractor should be on the vertex of the angle.\n- The base line of the protractor should be on one arm of the angle.\n\nStep 3: Choose the correct scale.\n\nThe arm on which the base line lies is to the right side of the protractor, so use the inner scale.\n\nStep 4: Read off the size of the angle from the protractor, and check against your estimation.\n\n$175^{\\circ}$ is an obtuse angle, and is close to $180^{\\circ}$.\n\nStep 5: Name the angle, and give the answer.\n\n$$\nB\\hat{A}C = 175^{\\circ}\n$$",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b017",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Worked example 15.7: Measuring a reflex angle"
    },
    "content_text": "",
    "prompt_text": "Use a protractor and measure the angle shown below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-016.png]",
    "answer_text": "Step 1: Consider the diagram and estimate the size of the angle.\n\nThe diagram shows two arms: $XY$ and $XZ$. They form a reflex angle, which is shaded red.\n\nA reflex angle is between $180^{\\circ}$ and $360^{\\circ}$. This angle is very near to $360^{\\circ}$.\n\nStep 2: Find a way to measure this reflex angle.\n\nAn ordinary protractor can only measure angles between $0^{\\circ}$ to $180^{\\circ}$. We cannot measure a reflex angle with an ordinary protractor. We have to measure the angle that is not shaded and then subtract the answer from $360^{\\circ}$.\n\nStep 3: Place the protractor correctly on the angle to measure.\n\n[Protractor placement image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-017.png]\n\n- The centre of the protractor should be on the vertex of the angle.\n- The base line of the protractor should be on one arm of the angle.\n\nStep 4: Choose the scale and read off the size of the angle.\n\nThe acute angle measures $18^{\\circ}$.\n\nStep 5: Subtract the measured angle from $360^{\\circ}$ and give the correct answer. Check against your estimation, and name the reflex angle correctly.\n\nReflex $Z\\hat{X}Y = 360^{\\circ} - 18^{\\circ} = 342^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b018",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Types of angles"
    },
    "content_text": "Remember that reflex angles are always less than $360^{\\circ}$, but more than $180^{\\circ}$. A full turn or revolution is equal to $360^{\\circ}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b019",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.2: Measure angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.2: Measure angles",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b019-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.2: Measure angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.2: Measure angles\n\n1. Use a protractor and measure the angle shown below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-018.png]",
    "answer_text": "Estimate the size of the angle: The angle is an acute angle, so the measurement should be between $0^{\\circ}$ and $90^{\\circ}$.\n\nMeasure the angle with a protractor.\n\nAnswer: $B\\hat{A}C = 53^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b019-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.2: Measure angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.2: Measure angles\n\n2. Use a protractor and measure the angle shown below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-019.png]",
    "answer_text": "Estimate: acute angle, so between $0^{\\circ}$ and $90^{\\circ}$.\n\nAnswer: $B\\hat{A}C = 59^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b019-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.2: Measure angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.2: Measure angles\n\n3. Use a protractor and measure the angle shown below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-020.png]",
    "answer_text": "Estimate: obtuse angle, so between $90^{\\circ}$ and $180^{\\circ}$.\n\nAnswer: $B\\hat{A}C = 112^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b019-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.2: Measure angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.2: Measure angles\n\n4. Use a protractor and measure the angle shown below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-021.png]",
    "answer_text": "Estimate: obtuse angle, so between $90^{\\circ}$ and $180^{\\circ}$.\n\nAnswer: $B\\hat{A}C = 150^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b019-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.2: Measure angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.2: Measure angles\n\n5. Use a protractor and measure the angle shown below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-022.png]",
    "answer_text": "Estimate: reflex angle, so between $180^{\\circ}$ and $360^{\\circ}$.\n\nMeasure the angle that is not shaded and then subtract the answer from $360^{\\circ}$.\n\nAcute $Z\\hat{X}Y = 70^{\\circ}$.\n\nSubtract to find the size of the reflex angle: Reflex $Z\\hat{X}Y = 360^{\\circ} - 70^{\\circ} = 290^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b019-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.1 Labelling and measuring angles",
      "h3": "Exercise 15.2: Measure angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.2: Measure angles\n\n6. Use a protractor and measure the angle shown below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-023.png]",
    "answer_text": "Estimate: reflex angle, so between $180^{\\circ}$ and $360^{\\circ}$.\n\nMeasure the angle that is not shaded and then subtract the answer from $360^{\\circ}$.\n\nAcute $C\\hat{A}B = 49^{\\circ}$.\n\nSubtract to find the size of the reflex angle: Reflex $C\\hat{A}B = 360^{\\circ} - 49^{\\circ} = 311^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
  },
  {
    "record_id": "ch15-b064",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.5 Summary",
      "h3": null
    },
    "content_text": "An angle is the amount of turn between two straight lines that have a common end point, called the vertex of the angle.\n\nWe use a protractor to measure angles in degrees. Always estimate an angle before you measure it, so you can check whether your answer seems correct.\n\nDifferent types of angles used in this chapter include:\n\n- acute angle: between $0^{\\circ}$ and $90^{\\circ}$\n- right angle: $90^{\\circ}$\n- obtuse angle: between $90^{\\circ}$ and $180^{\\circ}$\n- straight angle: $180^{\\circ}$\n- reflex angle: between $180^{\\circ}$ and $360^{\\circ}$\n- revolution: $360^{\\circ}$\n\nA straight line is also called a straight angle. A straight angle is equal to $180^{\\circ}$.\n\nIf a straight line is formed by more than one angle, the sum of those angles will be $180^{\\circ}$. We say the angles are supplementary angles.\n\nAdjacent angles are next to each other. Two adjacent angles share the same vertex and one common arm.\n\nWhen two lines cross each other, we say they are intersecting lines.\n\nTwo intersecting straight lines form vertically opposite angles, which have the same vertex and are on opposite sides of the vertex. Vertically opposite angles are equal.\n\nParallel lines are always the same distance apart, and are indicated using arrow symbols.\n\nA transversal intersects two or more parallel lines.\n\nThere are three types of angles formed by parallel lines and a transversal:\n\n- Corresponding angles are in matching positions on the parallel lines and the transversal, and make an F shape. Corresponding angles on parallel lines are equal.\n- Co-interior angles are inside the parallel lines and on the same side of the transversal. They make a U shape. Co-interior angles on parallel lines are supplementary and add up to $180^{\\circ}$.\n- Alternate angles are inside the parallel lines, but on different sides of the transversal. They make an N shape. Alternate angles on parallel lines are equal.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-measurement-of-angles"
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
