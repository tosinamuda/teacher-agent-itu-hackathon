# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-4",
  "topic_key": "jss1-math-plane-shapes",
  "topic": "Plane shapes",
  "subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle",
  "subtopic_title": "Perimeter of regular polygon, square, rectangle, triangle, trapezium, parallelogram and circle.",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle-po01",
        "source_performance_objective_index": 1,
        "text": "Find the perimeter of a regular polygon: square, rectangle, triangle, trapezium, parallelogram and circle"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "perimeter-of-plane-shapes-ao-find-perimeter",
          "text": "Find the perimeter of a regular polygon: square, rectangle, triangle, trapezium, parallelogram and circle."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch12-b009",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": null
    },
    "content_text": "If you trace your finger around the edge of a book or a plate, you have traced the **perimeter** of the shape with your finger. The perimeter of a football field is the white line around the entire field.\n\nPerimeter is a distance, so it is measured in units of length (such as mm, cm, m or km).",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b010",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": null
    },
    "content_text": "**perimeter** Perimeter is the distance around the outside of a shape.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b011",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Counting steps to find perimeter"
    },
    "content_text": "We can use a practical method to find the perimeter of a 2D shape if the shape is drawn on a grid.\n\nBecause perimeter is the distance around the outside of a shape, to find the perimeter of a polygon, we add up the lengths of all of the sides as if we are walking all the way around the edge of the shape. It is important to begin and end at the same corner of the shape.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b012",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Worked example 12.3: Finding the perimeter of a square"
    },
    "content_text": "",
    "prompt_text": "Determine the perimeter of the square shown in the diagram by counting the steps.",
    "answer_text": "Step 1: Begin to walk at Point J and follow the arrows to walk around the shape. Count each step as you walk.\n\nNumber of steps for blue arrow = 9 steps\n\nNumber of steps for pink arrow = 9 steps\n\nNumber of steps for green arrow = 9 steps\n\nNumber of steps for red arrow = 9 steps\n\nStep 2: Calculate the total number of steps that you have taken.\n\n$$\n\\begin{array}{ll} \\text{Perimeter} & {= \\text{9} + \\text{9} + \\text{9} + \\text{9}}\\\\ &= \\text{36 steps} \\end{array}\n$$\n\nTotal number of steps = 36 steps\n\nStep 3: Give the answer\n\nThe distance around the shape is 36 steps, so the perimeter of the square is 36 steps.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b013",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Worked example 12.4: Finding the perimeter of a rectangle"
    },
    "content_text": "",
    "prompt_text": "Determine the perimeter of the rectangle provided by counting the steps. The length of one side of each small square represents 1 km.",
    "answer_text": "Step 1: Begin to walk at Point J and follow the arrows to walk around the shape. Count each step as you walk.\n\nNumber of steps for red arrow = 9 steps\n\nNumber of steps for blue arrow = 4 steps\n\nNumber of steps for green arrow = 9 steps\n\nNumber of steps for pink arrow = 4 steps\n\nStep 2: Calculate the total number of steps that you have taken.\n\n$$\n\\begin{array}{ll} \\text{Perimeter} &{= \\text{9} + \\text{4} + \\text{9} + \\text{4}} \\\\ &{= \\text{26 steps}} \\end{array}\n$$\n\nTotal number of steps = 26 steps\n\nStep 3: Give the answer.\n\nThe distance around the shape is 26 steps, so the perimeter of the rectangle is 26 km.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b014",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.3: Count steps to find perimeter"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.3: Count steps to find perimeter",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b014-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.3: Count steps to find perimeter"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.3: Count steps to find perimeter\n\n1. Find the perimeter the rectangle given below by using the grid on which it is plotted. The length of one side of each small square represents 1 km.",
    "answer_text": "To find the perimeter of a polygon, we add up all of the sides as if we are walking around the edge of the shape.\n\nIf we start at Point J and walk around the shape, we get:\n\n$$\n\\begin{array}{ll} \\text{Perimeter} &{= \\text{5} + \\text{6} + \\text{5} + \\text{6}} \\\\ &{= \\text{22 km}} \\end{array}\n$$\n\nTotal number of steps = 22 steps\n\nThe distance around the shape is 22 steps, so the perimeter of the rectangle is 22 km.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b014-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.3: Count steps to find perimeter"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.3: Count steps to find perimeter\n\n2. Find the perimeter of the following shape. Begin at the dot and follow the direction shown by the arrow. The length of one side of each small square represents 1 cm.",
    "answer_text": "To find the perimeter of a polygon, we add up all of the sides as if we are walking around the edge of the shape.\n\nIf we start at the dot and walk around the shape, we get:\n\n$$\n\\begin{array}{ll} \\text{Perimeter} & {= \\text{3} + \\text{6} + \\text{3} + \\text{6}} \\\\ &{= \\text{18 cm}} \\end{array}\n$$\n\nTotal number of steps = 18 steps\n\nThe perimeter of the shape is 18 cm.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b014-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.3: Count steps to find perimeter"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.3: Count steps to find perimeter\n\n3. Find the perimeter of this shape. The length of one side of each small square is 1 cm.",
    "answer_text": "Number of steps for red arrow = 4 steps\n\nNumber of steps for purple arrow = 4 steps\n\nNumber of steps for green arrow = 4 steps\n\nNumber of steps for pink arrow = 4 steps\n\n$$\n\\begin{array}{ll} \\text{Perimeter} & {= \\text{4} + \\text{4} + \\text{4} + \\text{4}} \\\\ &{= \\text{16 steps}} \\end{array}\n$$\n\nTotal number of steps = 16 steps\n\nThe perimeter of the square is 16 cm.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b014-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.3: Count steps to find perimeter"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.3: Count steps to find perimeter\n\n4. Find the perimeter of this shape. The length of one side of each small square is 1 km.",
    "answer_text": "$\\text{Sum of steps} = 2 + 1 + 1 + 1 + 1 + 2$\n\n$= \\text{8 steps}$\n\nThe distance around the shape is 8 steps.\n\nThe perimeter of the shape is 8 km.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b014-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.3: Count steps to find perimeter"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.3: Count steps to find perimeter\n\n5. Find the perimeter of this shape. The length of one side of each small square is 1 cm.",
    "answer_text": "$$\n\\begin{array}{ll} \\text{Perimeter} &= {5 \\text{ steps across} + 10 \\text{ steps down} + 2 \\text{ steps across} + 1 \\text { step up} + 3 \\text{ steps across} + 9 \\text{ steps up}} \\\\ &= {5 + 10 + 2 + 1 + 3 + 9} \\\\ &= {\\text{30}\\ {\\text{steps}}} \\\\ \\end{array}\n$$\n\nThe perimeter is 30 cm.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b014-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.3: Count steps to find perimeter"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.3: Count steps to find perimeter\n\n6. Find the perimeter the shape. The length of one side of each small square is 1 m.",
    "answer_text": "$$\n\\begin{array}{ll} \\text{Perimeter} &= {8\\text{ steps across} + 5\\text{ steps up} + 2\\text{ steps across} + } {2\\text{ steps down} + 6\\text{ steps across} + 3\\text{ steps down}} \\\\ &= {8 + 5 + 2 + 2 + 6 + 3} \\\\ &= {\\text{26}\\ {\\text{steps}}} \\\\ \\end{array}\n$$\n\nThe perimeter is 26 m.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b015",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Perimeter of regular polygons"
    },
    "content_text": "If a shape is not drawn on grid paper, it will not be possible to \"walk\" around the shape and count the steps to find the perimeter. Then, to find the **perimeter of a polygon**, we need to know the lengths of all the sides of the shape.\n\nWhen working out the perimeter, it is important to look at a diagram and to check whether or not it is a **regular polygon** that you are working with.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b016",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Perimeter of regular polygons"
    },
    "content_text": "**regular polygon** In a regular polygon, all the sides have the same length and all the angles are equal.\n\n**perimeter of a polygon** The perimeter of any polygon is the sum of the lengths of all the sides.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b017",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Units of measurement for lengths"
    },
    "content_text": "Perimeter is a distance, and is measured using units of length, such as mm, cm, m or km.\n\n- Millimetres (mm) and centimetres (cm) are appropriate for measuring short lengths. They are used on your ruler.\n- Metres (m) are longer. One metre is about the length of one big step, or three rulers placed end to end. There are 100 centimetres in one metre.\n\n100 cm = 1 m\n\n- Kilometres (km) are good for measuring longer distances. It takes about 20 minutes to walk one kilometre (if you are walking at a relaxed speed). There are 1,000 metres in one kilometre.\n\n1,000 m = 1 km",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b018",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Worked example 12.5: Calculating perimeter of a regular polygon"
    },
    "content_text": "",
    "prompt_text": "Calculate the perimeter of the regular polygon shown in the diagram. The length of one side from $W$ to $V$ is 12 millimetres.",
    "answer_text": "Step 1: Check whether the shape is a regular polygon.\n\nIf the instruction tells you that the diagram shows a regular polygon, then you can take this as a given. If you are not told, you can measure. This shape has six equal sides and six equal angles, so it is a regular polygon (named a regular hexagon).\n\nStep 2: Work out what calculation to do.\n\nYou know that one side is 12 mm. So you need to multiply the number of sides by 12 mm.\n\nStep 3: Do the calculation, and remember to write the correct units in the answer.\n\n$$\n\\begin{array}{ll}\n\\text{Perimeter} & {= 6 \\times \\text{12 mm}} \\\\\n& {= \\text{72 mm}} \\\\\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b019",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Units of measurement for lengths"
    },
    "content_text": "As you have seen in the worked example above, we can use a formula to calculate the perimeter of a regular polygon, because all the sides have the same lengths.\n\n$$\n\\text {Perimeter of regular polygon = number of sides} \\times \\text{length of one side}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b020",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.4 Calculate perimeter of regular polygons"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.4 Calculate perimeter of regular polygons",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b020-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.4 Calculate perimeter of regular polygons"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.4 Calculate perimeter of regular polygons\n\n1. Calculate the perimeter of the regular polygon below. The length of one side is 7 centimetres.",
    "answer_text": "It is stated that the shape is a regular polygon, so the shape has equal sides. There are 5 sides, and the length of one side is 7 cm.\n\n$$\n\\begin{array}{ll}\n\\text{Perimeter}& {= \\text{number of sides} \\times \\text{length of one side}}\\\\\n& {= 5 \\times \\text{7 cm}}\\\\\n& {= \\text {35 cm}}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b020-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.4 Calculate perimeter of regular polygons"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.4 Calculate perimeter of regular polygons\n\n2. Calculate the perimeter of the regular polygon below. The length of one side is 4.5 metres.",
    "answer_text": "The shape has 4 equal sides, and the length of one side of the square is 4.5 m.\n\n$$\n\\begin{array}{ll}\n\\text{Perimeter} &= \\text{number of sides} \\times \\text{length of one side}\\\\\n&= 4 \\times \\text{4.5 m}\\\\\n&= \\text{18 m}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b020-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.4 Calculate perimeter of regular polygons"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.4 Calculate perimeter of regular polygons\n\n3. Calculate the perimeter of the regular polygon below. The length of one side is 20 centimetres.",
    "answer_text": "The shape has 8 equal sides, and the length of one side is 20 cm.\n\n$$\n\\begin{array}{ll}\n\\text{Perimeter}& = \\text{number of sides} \\times \\text{length of one side}\\\\\n&= 8 \\times \\text{20 cm}\\\\\n&= \\text{160 cm}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b020-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.4 Calculate perimeter of regular polygons"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.4 Calculate perimeter of regular polygons\n\n4. Calculate the perimeter of the regular polygon below. The length of one side from $W$ to $V$ is 2.6 kilometres.",
    "answer_text": "The shape has 10 equal sides, and the length of one side of the regular decagon is 2.6 km.\n\n$$\n\\begin{array}{l}\n\\text{Perimeter}& = \\text{number of sides} \\times \\text{length of one side}\\\\\n&= 10 \\times \\text{2.6 km} \\\\\n&= \\text{26 km} \\\\\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b020-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.4 Calculate perimeter of regular polygons"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.4 Calculate perimeter of regular polygons\n\n5. Calculate the perimeter of the regular polygon below. The length of one side is 30 millimetres.",
    "answer_text": "The shape has 3 equal sides, and the length of one side of the equilateral triangle is 30 mm.\n\n$$\n\\begin{align}\n\\text{Perimeter} &= \\text{number of sides} \\times \\text{length of one side}\\\\\n&= 3 \\times \\text{30 mm}\\\\\n&= \\text{90 mm}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b021",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Perimeter of irregular polygons"
    },
    "content_text": "All polygons are not regular polygons. It is possible to draw a polygon where each side has a different length. It is also possible to draw a polygon where some of the sides are equal in length, but others have different lengths.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b022",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Perimeter of irregular polygons"
    },
    "content_text": "**irregular polygon** In an irregular polygon, all the sides are not the same length and all the angles are not equal.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b023",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Perimeter of irregular polygons"
    },
    "content_text": "To determine the perimeter of an irregular polygon, we have to find the sum of the lengths of all the sides. We cannot use a formula, so we simply add the lengths of all the sides.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b024",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Worked example 12.6: Calculating perimeter of an irregular triangle"
    },
    "content_text": "",
    "prompt_text": "Find the perimeter of the triangle given below.",
    "answer_text": "Step 1: Look at the diagram and take note of the information given.\n\nThe triangle is not a regular polygon. Each side of the triangle has a different length.\n\nStep 2: Think of how you \"walked\" around a polygon. Write down the calculation that you must do.\n\n$$\n\\text{Perimeter} = \\text{3 cm} + \\text{4 cm} + \\text{5 cm}\n$$\n\nStep 3: Do the calculation, and remember to write the correct units in the answer.\n\n$$\n\\begin{align}\n\\text{Perimeter} &= \\text{3 cm} + \\text{4 cm} + \\text{5 cm}\\\\\n&= \\text{12 cm}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b025",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Worked example 12.7: Calculating perimeter of a parallelogram"
    },
    "content_text": "",
    "prompt_text": "Find the perimeter of the parallelogram given below.",
    "answer_text": "Step 1: Look at the diagram and take note of the information given.\n\nIn a parallelogram, the opposite sides have equal lengths. Fill in the missing lengths.\n\nStep 2: Think of how you \"walked\" around a polygon. Write down the calculation that you must do.\n\n$$\n\\text{Perimeter} = \\text{20 mm} + \\text{7 mm} + \\text{20 mm} + \\text{7 mm}\n$$\n\nStep 3: Do the calculation, writing the units as part of the answer.\n\n$$\n\\begin{align}\n\\text{Perimeter} &= \\text{20 mm} + \\text{7 mm} + \\text{20 mm} + \\text{7 mm}\\\\\n&= \\text{54 mm}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b026",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.5: Calculate perimeter of irregular polygons"
    },
    "content_text": "Source math retained:\n\\begin{align} \\text{Perimeter}& = \\text{5 m} + \\text{7 m} + \\text{3 m} + \\text{10 m}\\\\ &= \\text{25 m} \\end{align}",
    "prompt_text": "### Exercise 12.5: Calculate perimeter of irregular polygons",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b026-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.5: Calculate perimeter of irregular polygons"
    },
    "content_text": "Source math retained:\n\\begin{align} \\text{Perimeter of rectangle}& = 2l + 2b \\\\ &= 2 \\times \\text{50} + 2 \\times \\text{15} \\\\ &= \\text{100} + \\text{30} \\\\ &= \\text{130 mm} \\end{align}",
    "prompt_text": "### Exercise 12.5: Calculate perimeter of irregular polygons\n\n1. Give the name of the irregular polygon shown in the diagram, and calculate its perimeter.",
    "answer_text": "$$\n\\begin{align}\n\\text{Perimeter} &= \\text{7 cm} + \\text{8 cm} + \\text{9 cm}\\\\\n&= \\text{24 cm}\n\\end{align}\n$$\n\nThe name of the polygon: triangle.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b026-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.5: Calculate perimeter of irregular polygons"
    },
    "content_text": "Source math retained:\n\\begin{array}{ll} \\text{Perimeter of rectangle}& = 2l + 2b \\\\ & {= 2 \\times 7.25 + 2 \\times 5} \\\\ & {= 14.5 + 10} \\\\\\ & {= \\text{24.5 m}} \\end{array}",
    "prompt_text": "### Exercise 12.5: Calculate perimeter of irregular polygons\n\n2. Give the name of the irregular polygon shown in the diagram, and find its perimeter.",
    "answer_text": "$$\n\\begin{align}\n\\text{Perimeter} &= \\text{18 mm} + \\text{62 mm} + \\text{18 mm} + \\text{62 mm}\\\\\n&= \\text{160 mm}\n\\end{align}\n$$\n\nThe name of the polygon: rectangle.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b026-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.5: Calculate perimeter of irregular polygons"
    },
    "content_text": "Source math retained:\n\\begin{align} \\text{Perimeter}& = \\text{5 m} + \\text{7 m} + \\text{3 m} + \\text{10 m}\\\\ &= \\text{25 m} \\end{align}",
    "prompt_text": "### Exercise 12.5: Calculate perimeter of irregular polygons\n\n3. Give the name of the irregular polygon shown in the diagram, and find its perimeter.",
    "answer_text": "$$\n\\begin{align}\n\\text{Perimeter}&= \\text{5 m} + \\text{7 m} + \\text{3 m} + \\text{10 m}\\\\\n&= \\text{25 m}\n\\end{align}\n$$\n\nThe name of the polygon: trapezium.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b026-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.5: Calculate perimeter of irregular polygons"
    },
    "content_text": "Source math retained:\n\\begin{align} \\text{Perimeter} & = \\text{120 mm} + \\text{80 mm} + \\text{120 mm} + \\text{80 mm}\\\\ &= \\text{400 mm} \\end{align}",
    "prompt_text": "### Exercise 12.5: Calculate perimeter of irregular polygons\n\n4. Give the name of the irregular polygon shown in the diagram, and find its perimeter.",
    "answer_text": "$$\n\\begin{align}\n\\text{Perimeter} &= \\text{120 mm} + \\text{80 mm} + \\text{120 mm} + \\text{80 mm}\\\\\n&= \\text{400 mm}\n\\end{align}\n$$\n\nThe name of the polygon: parallelogram.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b026-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.5: Calculate perimeter of irregular polygons"
    },
    "content_text": "Source math retained:\n\\begin{align} \\text{Perimeter of rectangle}& = 2l + 2b \\\\ &= 2 \\times \\text{50} + 2 \\times \\text{15} \\\\ &= \\text{100} + \\text{30} \\\\ &= \\text{130 mm} \\end{align}",
    "prompt_text": "### Exercise 12.5: Calculate perimeter of irregular polygons\n\n5. Study the diagram below and calculate the perimeter of this shape by using the given lengths in cm.",
    "answer_text": "The perimeter of a two-dimensional object is the distance around its edge. The diagram below shows the perimeter in red and blue.\n\nTo find the perimeter, we need to add up all six sides of the shape. We can start at any corner we want and go around until we get back where we started. We will start at the corner labelled \"Start\".\n\n$$\n\\begin{array}{ll}\n\\text{Perimeter } &{ = \\text{Sum of lengths of sides}} \\\\\n&{= 6 + 7 + 4 + 3 + 2 + 4}\\\\\n& {= \\text{26 cm}}\n\\end{array}\n$$\n\nYou do not have to start at the same corner: you can start at any corner and you will get the same total distance. This is because the distance around the shape is the same no matter where you start.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b026-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.5: Calculate perimeter of irregular polygons"
    },
    "content_text": "Source math retained:\n\\begin{array}{ll} \\text{Perimeter of rectangle}& = 2l + 2b \\\\ & {= 2 \\times 7.25 + 2 \\times 5} \\\\ & {= 14.5 + 10} \\\\\\ & {= \\text{24.5 m}} \\end{array}",
    "prompt_text": "### Exercise 12.5: Calculate perimeter of irregular polygons\n\n6. Study the diagram below and calculate the perimeter of this object by using the given lengths in m.",
    "answer_text": "The diagram below shows the perimeter in red and blue.\n\nWe will start at the corner labelled \"Start\".\n\n$$\n\\begin{array}{ll}\n\\text{Perimeter} & {= \\text{Sum of lengths of sides}} \\\\\n&{= 7 + 7 + 2 + 5 + 5 + 2} \\\\\n& {= \\text{28 m}}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b026-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.5: Calculate perimeter of irregular polygons"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.5: Calculate perimeter of irregular polygons\n\n7. The diagram below shows a view from above Ms Chidi's house and land. The property has a fence going around the outside. What is the perimeter of the property, if measurements are given in metres?",
    "answer_text": "To calculate the perimeter, we add up all the boundary lines that form the perimeter of this property.\n\nIf we start at the black dot shown on the diagram and walk all around the boundary, we get:\n\n$$\n\\begin{array}{ll}\n\\text{Perimeter} &{= \\text{11} + \\text{22} + \\text{19} + \\text{4}}\\\\\n&{= \\text{56 m}}\n\\end{array}\n$$\n\nThe perimeter of the property is 56 m.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b027",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Formulae to find the perimeter of a rectangle and a square"
    },
    "content_text": "It can take long to find the perimeter of a polygon by counting the steps or adding the lengths of the sides. Luckily, there are formulae that we can use for some shapes. The formulae are based on the fact that the perimeter of a shape is the distance around the shape, and that these shapes have some sides that are equal.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b028",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Worked example 12.8: Using a formula to find the perimeter of a rectangle"
    },
    "content_text": "",
    "prompt_text": "Find the perimeter of the rectangle given below.",
    "answer_text": "Step 1: Look at the diagram and take note of the information given. Fill in the missing lengths.\n\nThe opposite sides of a rectangle are the same length. Let the longer side be $l$ and the shorter side be $b$.\n\nStep 2: Think of a shorter way than adding all the side lengths.\n\nIn a rectangle, you know that the two lengths are equal, and the two breadths are equal. This means you can use a formula to calculate the perimeter of a rectangle.\n\n$$\n\\begin{array}{ll}\n\\text{Perimeter of rectangle} & {= l + b + l + b} \\\\\n& {= 2 \\times l + 2 \\times b} \\\\\n& {= 2l + 2b} \\\\\n\\end{array}\n$$\n\nStep 3: Fill in the correct values.\n\n$$\n\\begin{array}{ll}\n\\text{Perimeter of rectangle} &= 2l + 2b\\\\\n&= 2 \\times \\text{15} + 2 \\times \\text{4} \\\\\n\\end{array}\n$$\n\nStep 4: Do the calculation, using BODMAS to remember the order of operations, so you need to multiply before you add. Write in the correct units at the end of the answer.\n\n$$\n\\begin{array}{ll}\n\\text{Perimeter of rectangle} &= 2l + 2b \\\\\n&= 2 \\times \\text{15} + 2 \\times \\text{4} \\\\\n&= \\text{38 cm}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b029",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Formulae to find the perimeter of a rectangle and a square"
    },
    "content_text": "For any parallelogram, including a rectangle, the two lengths are the same length, and the two breadths are the same length. This means we can use the formula we reached in the worked example above to calculate the perimeter of a parallelogram:\n\n$$\n\\text{Perimeter of parallelogram} = 2l + 2b\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b030",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Worked example 12.9: Using a formula to find the perimeter of a square"
    },
    "content_text": "",
    "prompt_text": "Find the perimeter of the square given below.",
    "answer_text": "Step 1: Look at the diagram and take note of the information given. Fill in the missing lengths. In a square all four sides are equal.\n\nStep 2: Think of a shorter way than adding all the side lengths.\n\nAll of the sides of a square are the same length. If we let the side be $s$, then the perimeter is:\n\n$$\n\\begin{array}{ll}\n\\text{Perimeter of square} &= s + s + s + s\\\\\n& {= 4 \\times s} \\\\\n& {= 4s}\n\\end{array}\n$$\n\nStep 3: Fill in the correct values.\n\n$$\n\\begin{array}{ll}\n\\text{Perimeter of square} &= 4s \\\\\n&= 4 \\times \\text{60}\n\\end{array}\n$$\n\nStep 4: Do the calculation, and remember to add the correct units to the answer.\n\n$$\n\\begin{array}{ll}\n\\text {Perimeter of square} &= 4s \\\\\n&= 4 \\times \\text{60} \\\\\n&= \\text{240 mm}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b031",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Formulae to find the perimeter of a rectangle and a square"
    },
    "content_text": "The four sides of a square and of a rhombus are all equal. We can therefore use the following formula to calculate the perimeter of a square and a rhombus:\n\n$$\n\\text{Perimeter of square and rhombus} = 4s\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b032",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Formulae to calculate perimeter"
    },
    "content_text": "The table below lists the formulae for the perimeter of the two-dimensional shapes you will be working with. In a formula, we can use $P$ as a symbol for perimeter.\n\nrectangle: ${P} = 2l + 2b$\n\nparallelogram: ${P} = 2l + 2b$\n\nsquare: ${P} = 4s$\n\nrhombus: ${P} = 4s$\n\ntriangle: ${P} = \\text{side 1} + \\text{side 2} + \\text{side 3} = s_1 + s_2 + s_3$\n\ntrapezium: ${P} = \\text{side 1} + \\text{side 2} + \\text{side 3} + \\text{side 4} = s_1 + s_2 + s_3 + s_4$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b033",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.6: Calculate perimeter using formulae"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.6: Calculate perimeter using formulae",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b033-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.6: Calculate perimeter using formulae"
    },
    "content_text": "Source math retained:\n\\begin{align} \\text{Perimeter of rectangle}& = 2l + 2b \\\\ &= 2 \\times \\text{50} + 2 \\times \\text{15} \\\\ &= \\text{100} + \\text{30} \\\\ &= \\text{130 mm} \\end{align}",
    "prompt_text": "### Exercise 12.6: Calculate perimeter using formulae\n\n1. Calculate the perimeter of the rectangle given below.",
    "answer_text": "$$\n\\begin{align}\n\\text{Perimeter of rectangle}&= 2l + 2b \\\\\n&= 2 \\times \\text{50} + 2 \\times \\text{15} \\\\\n&= \\text{100} + \\text{30} \\\\\n&= \\text{130 mm}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b033-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.6: Calculate perimeter using formulae"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.6: Calculate perimeter using formulae\n\n2. Calculate the perimeter of the square given below.",
    "answer_text": "$$\n\\begin{align}\n\\text{Perimeter of square}&= 4s\\\\\n&= 4 \\times \\text{120} \\\\\n&= \\text{480 cm}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b033-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.6: Calculate perimeter using formulae"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.6: Calculate perimeter using formulae\n\n3. Calculate the perimeter of the triangle given below.",
    "answer_text": "$$\n\\begin{align}\n\\text{Perimeter of triangle}&= s_1 + s_2 + s_3 \\\\\n&= \\text{14} + \\text{14} + \\text{9} \\\\\n&= \\text{37 m}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b033-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.6: Calculate perimeter using formulae"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.6: Calculate perimeter using formulae\n\n4. Calculate the perimeter of the parallelogram given below.",
    "answer_text": "$$\n\\begin{align}\n\\text{Perimeter of parallelogram}&= 2l + 2b \\\\\n&= 2 \\times \\text{90} + 2 \\times \\text{20} \\\\\n&= \\text{180} + \\text{40} \\\\\n&= \\text{220 mm}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b033-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.6: Calculate perimeter using formulae"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.6: Calculate perimeter using formulae\n\n5. Calculate the perimeter of the trapezium given below.",
    "answer_text": "$$\n\\begin{align}\n\\text{Perimeter of trapezium}&= s_1 + s_2 + s_3 + s_4\\\\\n&= \\text{31} + \\text{85} + \\text{31} + \\text{120}\\\\\n&= \\text{267 cm}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b033-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.6: Calculate perimeter using formulae"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.6: Calculate perimeter using formulae\n\n6. Consider the following square. Determine the perimeter of the square.",
    "answer_text": "$$\n\\begin{align}\n\\text{Perimeter of square}&= 4s\\\\\n&= 4 \\times \\text{6.1} \\\\\n&= \\text{24.4 cm}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b033-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.6: Calculate perimeter using formulae"
    },
    "content_text": "Source math retained:\n\\begin{array}{ll} \\text{Perimeter of rectangle}& = 2l + 2b \\\\ & {= 2 \\times 7.25 + 2 \\times 5} \\\\ & {= 14.5 + 10} \\\\\\ & {= \\text{24.5 m}} \\end{array}",
    "prompt_text": "### Exercise 12.6: Calculate perimeter using formulae\n\n7. Consider the following rectangle. Determine the perimeter of the rectangle.",
    "answer_text": "$$\n\\begin{array}{ll}\n\\text{Perimeter of rectangle}&= 2l + 2b \\\\\n& {= 2 \\times 7.25 + 2 \\times 5} \\\\\n& {= 14.5 + 10} \\\\\\\n& {= \\text{24.5 m}}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b033-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.6: Calculate perimeter using formulae"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.6: Calculate perimeter using formulae\n\n8. Calculate the perimeter of a triangle with the following side lengths: $\\frac {1}{4} \\text{m}; \\frac {1}{3} \\text{m and} \\frac {1}{2} \\text{m}$.",
    "answer_text": "In your calculation, remember to find the lowest common denominator of the fractions before you add them.\n\n$$\n\\begin{align}\n\\text{Perimeter of triangle}&= s_1 + s_2 + s_3 \\\\\n&= \\tfrac {1}{4}  + \\tfrac {1}{3} + \\tfrac {1}{2} \\\\\n&= \\tfrac {3}{12}  + \\tfrac {4}{12} + \\tfrac {6}{12} \\\\\n&= \\tfrac {13}{12} \\\\\n&= 1 \\tfrac {1}{12} \\text{m}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b033-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.6: Calculate perimeter using formulae"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.6: Calculate perimeter using formulae\n\n9. Calculate the perimeter of a rhombus with side length $\\frac {3}{8}$ km.",
    "answer_text": "$$\n\\begin{align}\n\\text{Perimeter of rhombus}&= 4s\\\\\n&= 4 \\times \\tfrac {3}{8} \\\\\n&= \\tfrac {4 \\times 3}{1 \\times 8}\\\\\n&= \\tfrac {12}{8} \\\\\n&= \\tfrac {3}{2} \\\\\n&= 1 \\tfrac {1}{2} \\text{km}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b033-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.6: Calculate perimeter using formulae"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.6: Calculate perimeter using formulae\n\n10. Calculate the perimeter of the trapezium given below.",
    "answer_text": "$$\n\\begin{align}\n\\text{Perimeter of trapezium}&= s_1 + s_2 + s_3 + s_4 \\\\\n&= 19y + 5y + 11y + 8y \\\\\n&= 43y \\text{ cm}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b033-i11",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.6: Calculate perimeter using formulae"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.6: Calculate perimeter using formulae\n\n11. The diagram below shows a notebook. What is the perimeter of the notebook if all the measurements are given in centimetres?",
    "answer_text": "The notebook is in the shape of a rectangle.\n\n$$\n\\begin{align}\n\\text{Perimeter of rectangle} &= 2l + 2b \\\\\n&= 2 \\times 25 + 2 \\times 15 \\\\\n&= \\text{50} + \\text{30} \\\\\n&= \\text{80 cm}\n\\end{align}\n$$\n\nThe perimeter of the notebook is $\\text{80 cm}$.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b034",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Using a formula to find the circumference of a circle"
    },
    "content_text": "We know that the perimeter of a circle is called its circumference. The circumference of a circle is a curve, so we cannot measure it with a ruler. We can use a formula to calculate the circumference of a circle. There are two formulae that we can use, which both mean the same thing:\n\n$$\n\\begin{array}{ll}\n\\boxed{C = \\pi \\times d} & {\\quad\\text{ or }\\quad\\boxed{C = 2 \\times \\pi \\times r}} \\\\\n\\end{array}\n$$\n\nIn these formulae, $C$ stands for circumference, $d$ stands for the **diameter** of the circle, and $r$ stands for the **radius** of the circle. We will mostly use the first formula with diameter, but you can use the radius formula if you prefer.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b035",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Using a formula to find the circumference of a circle"
    },
    "content_text": "**radius** The radius of a circle is the distance from the centre to the circumference.\n\n**diameter** The diameter of a circle is the length of a line passing through the centre of the circle, and touching the circumference at both ends.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b036",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Using a formula to find the circumference of a circle"
    },
    "content_text": "The diameter of a circle is double the radius, so $d = 2 \\times r$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b037",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Using a formula to find the circumference of a circle"
    },
    "content_text": "You will see that the symbol $\\pi$ is used in both formulae. This name of this symbol is \"pi\". **$\\pi$** is the ratio of the circumference of a circle to its diameter.\n\n$$\n\\begin{array}{l}\n\\pi = \\frac{C}{d}\n\\end{array}\n$$\n\nThe value of $\\pi$ is the same for all circles, large or small. We can see this by doing a quick experiment. Draw a circle with a compass. Place a piece of string along the circumference, and then measure the length of the string using a ruler. Next, use the ruler to measure the diameter of the circle. If we divide the circumference by the diameter, we will get a value that is approximately 3.14. If we do the same thing, but with a larger or a smaller circle, we will get the same value, every time!",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b038",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Using a formula to find the circumference of a circle"
    },
    "content_text": "$\\pi$ (pi) is the ratio of the circumference of a circle to its diameter. The values we use for $\\pi$ are 3.14 and $\\frac{22}{7}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b039",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Using a formula to find the circumference of a circle"
    },
    "content_text": "Look at the value of $\\pi$ that your calculator gives you, and compare this to the value of $\\frac{22}{7}$. Are they the same number?\n\n$\\pi$ is an unending number approximately equal to $\\frac{22}{7}$ or 3.14. Here are the first 200 digits of $\\pi$:\n\n$$\n\\begin{array}{ll}\n & \\text{3.141592653589793238462643383279502884197169399375105820974944} \\\\\n & 59230781640628620899862803482534211706798214808651328230664709 \\\\\n & 38446095505822317253594081284811174502841027019385211055596446 \\\\\n & 2294895493038196... \\\\\n\\end{array}\n$$\n\nScientists using powerful computers have calculated the value of $\\pi$ to over 13 trillion decimal places. But they will never be able to reach the end of this number, since the end does not exist.\n\nWhen we do calculations with $\\pi$, we cannot use the exact value of $\\pi$. Instead, we use an approximation of the value of $\\pi$. One commonly used value is 3.14, which is $\\pi$ rounded to two decimal places. Another approximation is $\\frac{22}{7}$. If we divide 22 by 7 on a calculator, we get 3.142857143. This is very close to $\\pi$ to two decimal places, but it is a slightly better approximation.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b040",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Worked example 12.10: Calculating circumference using diameter"
    },
    "content_text": "",
    "prompt_text": "The circle below has a diameter of 8 m. What is the circumference of this circle?",
    "answer_text": "Step 1: Write down the formula for the circumference of a circle:\n\n$$\n\\begin{array}{l}\n C = \\pi \\times d\n \\end{array}\n$$\n\nStep 2: The question tells us that the diameter of the circle is 8 m. Substitute 8 for the $d$ in the formula to find the circumference of the circle.\n\nWe will use 3.14 for $\\pi$.\n\n$$\n\\begin{array}{ll}\n C  &{= \\pi \\times d} \\\\\n & {= 3.14 \\times 8}\n \\end{array}\n$$\n\nStep 3: Do the calculation and remember to show the correct units with the answer.\n\n$$\n\\begin{array}{ll}\n C  &{= \\pi \\times d}\\\\\n &{= 3.14 \\times 8} \\\\\n &{= \\text{25.12 m}}\n \\end{array}\n$$\n\nThe circumference of the circle is 25.12 m.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b041",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Using a formula to find the circumference of a circle"
    },
    "content_text": "If you have a $\\pi$ button on your calculator, you may use it to work out the answer. But if the question gives you a value to use, such as 3.14, use that value.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b042",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Worked example 12.11: Calculating circumference using radius"
    },
    "content_text": "",
    "prompt_text": "The circle below has a radius of 2 cm. What is the circumference of the circle? Use 3.14 for $\\pi$.",
    "answer_text": "Step 1: Write down the formula for the circumference of a circle.\n\n$$\n\\begin{array}{ll}\n C  {= \\pi \\times d}\n \\end{array}\n$$\n\nOr you can use $C = \\pi \\times 2r$.\n\nStep 2: The question tells us that the radius of the circle is 2 cm. So the diameter is 4 cm. Substitute 4 for the $d$ in the formula. Also substitute 3.14 for $\\pi$.\n\n$$\n\\begin{array}{ll}\n C & {= \\pi \\times d} \\\\\n & {= 3.14 \\times 4} \\\\\n \\end{array}\n$$\n\nAs you can see, if you used $C = \\pi \\times 2r$, you would also get $3.14 \\times 4$.\n\nStep 3: Calculate the circumference of the circle. Remember to show the correct units in your answer.\n\n$$\n\\begin{array}{ll}\n C & {= \\pi \\times d}\\\\\n &{= 3.14 \\times 4}\\\\\n &{= \\text{12.56 cm}}\n \\end{array}\n$$\n\nThe circumference of the circle is 12.56 cm.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b043",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.7: Calculate the circumference of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.7: Calculate the circumference of a circle\n\nUse 3.14 for $\\pi$ in all your calculations.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b043-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.7: Calculate the circumference of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.7: Calculate the circumference of a circle\n\nUse 3.14 for $\\pi$ in all your calculations.\n\n1. The circle below has a diameter of 9 cm. What is the circumference of the circle?",
    "answer_text": "$$\n\\begin{array}{ll}\nC &{= \\pi \\times d}\\\\\n&{= 3.14 \\times 9}\\\\\n&{= \\text{28.26}\\ \\text{cm}}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b043-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.7: Calculate the circumference of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.7: Calculate the circumference of a circle\n\nUse 3.14 for $\\pi$ in all your calculations.\n\n2. The circle below has a radius of 5 cm. What is the circumference of the circle?",
    "answer_text": "If the radius is 5 cm, then the diameter is 10 cm.\n\n$$\n\\begin{array}{ll}\nC & {= \\pi \\times d}\\\\\n&{= 3.14 \\times 10}\\\\\n&{= \\text{31.4 cm}}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b043-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.7: Calculate the circumference of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.7: Calculate the circumference of a circle\n\nUse 3.14 for $\\pi$ in all your calculations.\n\n3. If a circle has a diameter of 11 m, what is the circumference of the circle?",
    "answer_text": "$$\n\\begin{array}{ll}\nC & {= \\pi \\times d} \\\\\n&{= 3.14 \\times 11} \\\\\n&{= \\text{34.54}\\ \\text{m}}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b043-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.7: Calculate the circumference of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.7: Calculate the circumference of a circle\n\nUse 3.14 for $\\pi$ in all your calculations.\n\n4. If a circle has a radius of 10 m, what is the circumference of the circle?",
    "answer_text": "If the radius is 10 cm, then the diameter is 20 cm.\n\n$$\n\\begin{array}{ll}\nC  &{= \\pi  \\times d}\\\\\n&{= 3.14 \\times 20} \\\\\n&{= \\text{62.8 m}}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b043-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.7: Calculate the circumference of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.7: Calculate the circumference of a circle\n\nUse 3.14 for $\\pi$ in all your calculations.\n\n5. What is the circumference of a circle that has a diameter of 40 mm?",
    "answer_text": "$$\n\\begin{array}{ll}\nC& {= \\pi \\times d} \\\\\n&{= 3.14 \\times 40} \\\\\n&{= \\text{125.6 mm}}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b043-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.7: Calculate the circumference of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.7: Calculate the circumference of a circle\n\nUse 3.14 for $\\pi$ in all your calculations.\n\n6. What is the circumference of a circle that has a radius of 50 mm?",
    "answer_text": "If radius is 50 mm, then diameter is 100 mm.\n\n$$\n\\begin{array}{ll}\nC & {= \\pi \\times d}\\\\\n&{= 3.14 \\times 100} \\\\\n&{= \\text{314 mm}}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b069",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.4 Practical applications",
      "h3": null
    },
    "content_text": "In real life we often need to calculate a perimeter or area. Then it is useful to know the correct formula as well as how to use the formula.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-area-of-regular-plane-shapes-such-as-squares-rectangles-parallelograms-etc"
  },
  {
    "record_id": "ch12-b071",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.4 Practical applications",
      "h3": "Exercise 12.12 :Find perimeter and area in real life situations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.12: Find perimeter and area in real life situations",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-area-of-regular-plane-shapes-such-as-squares-rectangles-parallelograms-etc"
  },
  {
    "record_id": "ch12-b071-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.4 Practical applications",
      "h3": "Exercise 12.12 :Find perimeter and area in real life situations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.12: Find perimeter and area in real life situations\n\n1. The diagram below shows a notebook with all the measurements given in centimetres.\n\nFind the perimeter of the notebook.",
    "answer_text": "The notebook is in the shape of a rectangle, so you use the formulae for the perimeter of a rectangle.\n\n$$\n\\begin{align}\nP  & = 2l + 2b\\\\\n& {= 2 \\times 25 + 2 \\times 15}\\\\\n& {= \\text{50} + \\ \\text{30}}\\\\\n& {= \\text{80}\\ \\text{cm}}\n \\end{align}\n$$\n\nThe notebook has a perimeter of 80 cm.",
    "primary_subtopic_id": "jss1-math-plane-shapes-area-of-regular-plane-shapes-such-as-squares-rectangles-parallelograms-etc"
  },
  {
    "record_id": "ch12-b071-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.4 Practical applications",
      "h3": "Exercise 12.12 :Find perimeter and area in real life situations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.12: Find perimeter and area in real life situations\n\n2. The diagram below shows a notebook with all the measurements given in centimetres.\n\nFind the area of the notebook.",
    "answer_text": "Use the formula for the area of a rectangle.\n\n$$\n\\begin{align}\nA  & = l \\times b\\\\\n& {= 25 \\times 15}\\\\\n& {= \\text{375}\\ \\text{cm}^{2}}\n \\end{align}\n$$\n\nThe notebook has an area of 375 cm$^{2}$.",
    "primary_subtopic_id": "jss1-math-plane-shapes-area-of-regular-plane-shapes-such-as-squares-rectangles-parallelograms-etc"
  },
  {
    "record_id": "ch12-b071-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.4 Practical applications",
      "h3": "Exercise 12.12 :Find perimeter and area in real life situations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.12: Find perimeter and area in real life situations\n\n3. Adanna is renovating her house, and she wants to have a blind made for the window. The blind will be a flat piece of fabric that reaches to the outside edge of the window. The window is in the shape of a square, and at the outside edge, the sides are all 65 centimetres.\n\nAdanna wants to have a velvet strip around the edge of the blind. Find the perimeter of the window to work out the length of the velvet strip.",
    "answer_text": "The window is in the shape of a square, so use the formula for the perimeter of a square.\n\n$$\n\\begin{align}\nP  & = 4s \\\\\n& {= 4 \\times 65}\\\\\n& {= \\text{260}\\ \\text{cm}}\n \\end{align}\n$$\n\nThe perimeter of the window is 260 cm, so the velvet strip will be 260 cm long.",
    "primary_subtopic_id": "jss1-math-plane-shapes-area-of-regular-plane-shapes-such-as-squares-rectangles-parallelograms-etc"
  },
  {
    "record_id": "ch12-b071-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.4 Practical applications",
      "h3": "Exercise 12.12 :Find perimeter and area in real life situations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.12: Find perimeter and area in real life situations\n\n4. Adanna is renovating her house, and she wants to have a blind made for the window. The blind will be a flat piece of fabric that reaches to the outside edge of the window. The window is in the shape of a square, and at the outside edge, the sides are all 65 centimetres.\n\nFind the area of the window to work out how big the blind has to be.",
    "answer_text": "Use the formula for area of a square.\n\n$$\n\\begin{align}\nA & = s^{2} \\\\\n& {= 65 \\times 65}\\\\\n& {= 4,\\!225\\ \\text{cm}^{2}}\n\\end{align}\n$$\n\nThe blind will be 4,225 cm$^{2}$.",
    "primary_subtopic_id": "jss1-math-plane-shapes-area-of-regular-plane-shapes-such-as-squares-rectangles-parallelograms-etc"
  },
  {
    "record_id": "ch12-b071-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.4 Practical applications",
      "h3": "Exercise 12.12 :Find perimeter and area in real life situations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.12: Find perimeter and area in real life situations\n\n5. Talatu paints plates to sell to tourists. She paints the plates purple with a white circle in the centre.\n\nThe diagram below shows the plate. $O$ is the centre of the plate. The radius of the small white circle is 3 cm and the radius of the big blue circle is 7 cm.\n\nDetermine the area of the purple region. Use 3.14 for $\\pi$.",
    "answer_text": "To calculate the area of the purple region, you need to calculate the area of each of the two circles, and then subtract one area from the other.\n\n**Area of big circle:**\n\n$$\n\\begin{array}{ll}\nA_\\text{1} & {= \\pi \\times R^{2}} \\\\\n& {= 3.14 \\times 7^{2}} \\\\\n& {= 3.14 \\times 49} \\\\\n& {= 153.86\\ {\\text{cm}^{2}}} \\\\\n\\end{array}\n$$\n\n**Area of small circle:**\n\n$$\n\\begin{array}{ll}\nA_\\text{2} & {= \\pi \\times r^{2}} \\\\\n& {= 3.14 \\times 3^{2}} \\\\\n& {= 3.14 \\times 9} \\\\\n& {= 28.26\\ {\\text{cm}^{2}}} \\\\\n\\end{array}\n$$\n\n**Area of purple region:**\n\n$$\n\\begin{array}{ll}\nA & {= A_\\text{1} - A_\\text{2}} \\\\\n& {= 153.86 - 28.26} \\\\\n& {= \\text{125.6}\\ {\\text{cm}^{2}}}\n\\end{array}\n$$\n\nThe area of the purple region is 125.6 cm$^{2}$.",
    "primary_subtopic_id": "jss1-math-plane-shapes-area-of-regular-plane-shapes-such-as-squares-rectangles-parallelograms-etc"
  },
  {
    "record_id": "ch12-b072",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.5 Summary",
      "h3": null
    },
    "content_text": "A two-dimensional (2D) shape has two dimensions that we can measure: length and breadth (or width).\n\nA polygon is a closed flat shape with three or more straight sides. A triangle has three sides and three angles. A quadrilateral has four sides and four angles. Examples of quadrilaterals are square, rectangle, rhombus, parallelogram, and trapezium.\n\nA circle is a 2D shape with a curved edge, so a circle is not a polygon. The perimeter of a circle is called its circumference. A line segment that goes all the way across the circle and passes through the centre is called a diameter. A line segment from the centre of the circle to a point on the circumference is called a radius.\n\nPerimeter is the distance around the outside of a shape. We can use the following formulae to calculate the perimeter of regular polygons:\n\n- rectangle: $P = 2l + 2b$\n- parallelogram: $P = 2l + 2b$\n- square: $P = 4s$\n- rhombus: $P = 4s$\n- triangle: $P = \\text{side 1} + \\text{side 2} + \\text{side 3} = s_1 + s_2 + s_3$\n- trapezium: $P = \\text{side 1} + \\text{side 2} + \\text{side 3} + \\text{side 4} = s_1 + s_2 + s_3 + s_4$\n\nArea is the amount of flat space taken up by a shape. We can use formulae to calculate the area of two-dimensional shapes:\n\n- rectangle: $A = l \\times b$\n- square: $A = s \\times s = s^{2}$\n- triangle: $A = \\frac{b \\times h}{2}$\n- parallelogram: $A = b \\times h$\n- trapezium: $A = \\frac{h}{2}\\left( a + b \\right)$\n- circle: $A = \\pi \\times r^{2}$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
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
  "topic_key": "jss1-math-plane-shapes",
  "topic": "Plane shapes",
  "subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle",
  "subtopic_title": "Perimeter of regular polygon, square, rectangle, triangle, trapezium, parallelogram and circle.",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle-po01",
        "source_performance_objective_index": 1,
        "text": "Find the perimeter of a regular polygon: square, rectangle, triangle, trapezium, parallelogram and circle"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "perimeter-of-plane-shapes-ao-find-perimeter",
          "text": "Find the perimeter of a regular polygon: square, rectangle, triangle, trapezium, parallelogram and circle."
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
    "record_id": "ch12-b009",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": null
    },
    "content_text": "If you trace your finger around the edge of a book or a plate, you have traced the **perimeter** of the shape with your finger. The perimeter of a football field is the white line around the entire field.\n\nPerimeter is a distance, so it is measured in units of length (such as mm, cm, m or km).",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b010",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": null
    },
    "content_text": "**perimeter** Perimeter is the distance around the outside of a shape.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b011",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Counting steps to find perimeter"
    },
    "content_text": "We can use a practical method to find the perimeter of a 2D shape if the shape is drawn on a grid.\n\nBecause perimeter is the distance around the outside of a shape, to find the perimeter of a polygon, we add up the lengths of all of the sides as if we are walking all the way around the edge of the shape. It is important to begin and end at the same corner of the shape.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b012",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Worked example 12.3: Finding the perimeter of a square"
    },
    "content_text": "",
    "prompt_text": "Determine the perimeter of the square shown in the diagram by counting the steps.",
    "answer_text": "Step 1: Begin to walk at Point J and follow the arrows to walk around the shape. Count each step as you walk.\n\nNumber of steps for blue arrow = 9 steps\n\nNumber of steps for pink arrow = 9 steps\n\nNumber of steps for green arrow = 9 steps\n\nNumber of steps for red arrow = 9 steps\n\nStep 2: Calculate the total number of steps that you have taken.\n\n$$\n\\begin{array}{ll} \\text{Perimeter} & {= \\text{9} + \\text{9} + \\text{9} + \\text{9}}\\\\ &= \\text{36 steps} \\end{array}\n$$\n\nTotal number of steps = 36 steps\n\nStep 3: Give the answer\n\nThe distance around the shape is 36 steps, so the perimeter of the square is 36 steps.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b013",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Worked example 12.4: Finding the perimeter of a rectangle"
    },
    "content_text": "",
    "prompt_text": "Determine the perimeter of the rectangle provided by counting the steps. The length of one side of each small square represents 1 km.",
    "answer_text": "Step 1: Begin to walk at Point J and follow the arrows to walk around the shape. Count each step as you walk.\n\nNumber of steps for red arrow = 9 steps\n\nNumber of steps for blue arrow = 4 steps\n\nNumber of steps for green arrow = 9 steps\n\nNumber of steps for pink arrow = 4 steps\n\nStep 2: Calculate the total number of steps that you have taken.\n\n$$\n\\begin{array}{ll} \\text{Perimeter} &{= \\text{9} + \\text{4} + \\text{9} + \\text{4}} \\\\ &{= \\text{26 steps}} \\end{array}\n$$\n\nTotal number of steps = 26 steps\n\nStep 3: Give the answer.\n\nThe distance around the shape is 26 steps, so the perimeter of the rectangle is 26 km.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b014",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.3: Count steps to find perimeter"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.3: Count steps to find perimeter",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b014-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.3: Count steps to find perimeter"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.3: Count steps to find perimeter\n\n1. Find the perimeter the rectangle given below by using the grid on which it is plotted. The length of one side of each small square represents 1 km.",
    "answer_text": "To find the perimeter of a polygon, we add up all of the sides as if we are walking around the edge of the shape.\n\nIf we start at Point J and walk around the shape, we get:\n\n$$\n\\begin{array}{ll} \\text{Perimeter} &{= \\text{5} + \\text{6} + \\text{5} + \\text{6}} \\\\ &{= \\text{22 km}} \\end{array}\n$$\n\nTotal number of steps = 22 steps\n\nThe distance around the shape is 22 steps, so the perimeter of the rectangle is 22 km.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b014-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.3: Count steps to find perimeter"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.3: Count steps to find perimeter\n\n2. Find the perimeter of the following shape. Begin at the dot and follow the direction shown by the arrow. The length of one side of each small square represents 1 cm.",
    "answer_text": "To find the perimeter of a polygon, we add up all of the sides as if we are walking around the edge of the shape.\n\nIf we start at the dot and walk around the shape, we get:\n\n$$\n\\begin{array}{ll} \\text{Perimeter} & {= \\text{3} + \\text{6} + \\text{3} + \\text{6}} \\\\ &{= \\text{18 cm}} \\end{array}\n$$\n\nTotal number of steps = 18 steps\n\nThe perimeter of the shape is 18 cm.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b014-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.3: Count steps to find perimeter"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.3: Count steps to find perimeter\n\n3. Find the perimeter of this shape. The length of one side of each small square is 1 cm.",
    "answer_text": "Number of steps for red arrow = 4 steps\n\nNumber of steps for purple arrow = 4 steps\n\nNumber of steps for green arrow = 4 steps\n\nNumber of steps for pink arrow = 4 steps\n\n$$\n\\begin{array}{ll} \\text{Perimeter} & {= \\text{4} + \\text{4} + \\text{4} + \\text{4}} \\\\ &{= \\text{16 steps}} \\end{array}\n$$\n\nTotal number of steps = 16 steps\n\nThe perimeter of the square is 16 cm.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b014-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.3: Count steps to find perimeter"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.3: Count steps to find perimeter\n\n4. Find the perimeter of this shape. The length of one side of each small square is 1 km.",
    "answer_text": "$\\text{Sum of steps} = 2 + 1 + 1 + 1 + 1 + 2$\n\n$= \\text{8 steps}$\n\nThe distance around the shape is 8 steps.\n\nThe perimeter of the shape is 8 km.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b014-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.3: Count steps to find perimeter"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.3: Count steps to find perimeter\n\n5. Find the perimeter of this shape. The length of one side of each small square is 1 cm.",
    "answer_text": "$$\n\\begin{array}{ll} \\text{Perimeter} &= {5 \\text{ steps across} + 10 \\text{ steps down} + 2 \\text{ steps across} + 1 \\text { step up} + 3 \\text{ steps across} + 9 \\text{ steps up}} \\\\ &= {5 + 10 + 2 + 1 + 3 + 9} \\\\ &= {\\text{30}\\ {\\text{steps}}} \\\\ \\end{array}\n$$\n\nThe perimeter is 30 cm.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b014-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.3: Count steps to find perimeter"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.3: Count steps to find perimeter\n\n6. Find the perimeter the shape. The length of one side of each small square is 1 m.",
    "answer_text": "$$\n\\begin{array}{ll} \\text{Perimeter} &= {8\\text{ steps across} + 5\\text{ steps up} + 2\\text{ steps across} + } {2\\text{ steps down} + 6\\text{ steps across} + 3\\text{ steps down}} \\\\ &= {8 + 5 + 2 + 2 + 6 + 3} \\\\ &= {\\text{26}\\ {\\text{steps}}} \\\\ \\end{array}\n$$\n\nThe perimeter is 26 m.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b015",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Perimeter of regular polygons"
    },
    "content_text": "If a shape is not drawn on grid paper, it will not be possible to \"walk\" around the shape and count the steps to find the perimeter. Then, to find the **perimeter of a polygon**, we need to know the lengths of all the sides of the shape.\n\nWhen working out the perimeter, it is important to look at a diagram and to check whether or not it is a **regular polygon** that you are working with.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b016",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Perimeter of regular polygons"
    },
    "content_text": "**regular polygon** In a regular polygon, all the sides have the same length and all the angles are equal.\n\n**perimeter of a polygon** The perimeter of any polygon is the sum of the lengths of all the sides.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b017",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Units of measurement for lengths"
    },
    "content_text": "Perimeter is a distance, and is measured using units of length, such as mm, cm, m or km.\n\n- Millimetres (mm) and centimetres (cm) are appropriate for measuring short lengths. They are used on your ruler.\n- Metres (m) are longer. One metre is about the length of one big step, or three rulers placed end to end. There are 100 centimetres in one metre.\n\n100 cm = 1 m\n\n- Kilometres (km) are good for measuring longer distances. It takes about 20 minutes to walk one kilometre (if you are walking at a relaxed speed). There are 1,000 metres in one kilometre.\n\n1,000 m = 1 km",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b018",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Worked example 12.5: Calculating perimeter of a regular polygon"
    },
    "content_text": "",
    "prompt_text": "Calculate the perimeter of the regular polygon shown in the diagram. The length of one side from $W$ to $V$ is 12 millimetres.",
    "answer_text": "Step 1: Check whether the shape is a regular polygon.\n\nIf the instruction tells you that the diagram shows a regular polygon, then you can take this as a given. If you are not told, you can measure. This shape has six equal sides and six equal angles, so it is a regular polygon (named a regular hexagon).\n\nStep 2: Work out what calculation to do.\n\nYou know that one side is 12 mm. So you need to multiply the number of sides by 12 mm.\n\nStep 3: Do the calculation, and remember to write the correct units in the answer.\n\n$$\n\\begin{array}{ll}\n\\text{Perimeter} & {= 6 \\times \\text{12 mm}} \\\\\n& {= \\text{72 mm}} \\\\\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b019",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Units of measurement for lengths"
    },
    "content_text": "As you have seen in the worked example above, we can use a formula to calculate the perimeter of a regular polygon, because all the sides have the same lengths.\n\n$$\n\\text {Perimeter of regular polygon = number of sides} \\times \\text{length of one side}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b020",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.4 Calculate perimeter of regular polygons"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.4 Calculate perimeter of regular polygons",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b020-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.4 Calculate perimeter of regular polygons"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.4 Calculate perimeter of regular polygons\n\n1. Calculate the perimeter of the regular polygon below. The length of one side is 7 centimetres.",
    "answer_text": "It is stated that the shape is a regular polygon, so the shape has equal sides. There are 5 sides, and the length of one side is 7 cm.\n\n$$\n\\begin{array}{ll}\n\\text{Perimeter}& {= \\text{number of sides} \\times \\text{length of one side}}\\\\\n& {= 5 \\times \\text{7 cm}}\\\\\n& {= \\text {35 cm}}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b020-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.4 Calculate perimeter of regular polygons"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.4 Calculate perimeter of regular polygons\n\n2. Calculate the perimeter of the regular polygon below. The length of one side is 4.5 metres.",
    "answer_text": "The shape has 4 equal sides, and the length of one side of the square is 4.5 m.\n\n$$\n\\begin{array}{ll}\n\\text{Perimeter} &= \\text{number of sides} \\times \\text{length of one side}\\\\\n&= 4 \\times \\text{4.5 m}\\\\\n&= \\text{18 m}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b020-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.4 Calculate perimeter of regular polygons"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.4 Calculate perimeter of regular polygons\n\n3. Calculate the perimeter of the regular polygon below. The length of one side is 20 centimetres.",
    "answer_text": "The shape has 8 equal sides, and the length of one side is 20 cm.\n\n$$\n\\begin{array}{ll}\n\\text{Perimeter}& = \\text{number of sides} \\times \\text{length of one side}\\\\\n&= 8 \\times \\text{20 cm}\\\\\n&= \\text{160 cm}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b020-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.4 Calculate perimeter of regular polygons"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.4 Calculate perimeter of regular polygons\n\n4. Calculate the perimeter of the regular polygon below. The length of one side from $W$ to $V$ is 2.6 kilometres.",
    "answer_text": "The shape has 10 equal sides, and the length of one side of the regular decagon is 2.6 km.\n\n$$\n\\begin{array}{l}\n\\text{Perimeter}& = \\text{number of sides} \\times \\text{length of one side}\\\\\n&= 10 \\times \\text{2.6 km} \\\\\n&= \\text{26 km} \\\\\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b020-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.4 Calculate perimeter of regular polygons"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.4 Calculate perimeter of regular polygons\n\n5. Calculate the perimeter of the regular polygon below. The length of one side is 30 millimetres.",
    "answer_text": "The shape has 3 equal sides, and the length of one side of the equilateral triangle is 30 mm.\n\n$$\n\\begin{align}\n\\text{Perimeter} &= \\text{number of sides} \\times \\text{length of one side}\\\\\n&= 3 \\times \\text{30 mm}\\\\\n&= \\text{90 mm}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b021",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Perimeter of irregular polygons"
    },
    "content_text": "All polygons are not regular polygons. It is possible to draw a polygon where each side has a different length. It is also possible to draw a polygon where some of the sides are equal in length, but others have different lengths.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b022",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Perimeter of irregular polygons"
    },
    "content_text": "**irregular polygon** In an irregular polygon, all the sides are not the same length and all the angles are not equal.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b023",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Perimeter of irregular polygons"
    },
    "content_text": "To determine the perimeter of an irregular polygon, we have to find the sum of the lengths of all the sides. We cannot use a formula, so we simply add the lengths of all the sides.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b024",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Worked example 12.6: Calculating perimeter of an irregular triangle"
    },
    "content_text": "",
    "prompt_text": "Find the perimeter of the triangle given below.",
    "answer_text": "Step 1: Look at the diagram and take note of the information given.\n\nThe triangle is not a regular polygon. Each side of the triangle has a different length.\n\nStep 2: Think of how you \"walked\" around a polygon. Write down the calculation that you must do.\n\n$$\n\\text{Perimeter} = \\text{3 cm} + \\text{4 cm} + \\text{5 cm}\n$$\n\nStep 3: Do the calculation, and remember to write the correct units in the answer.\n\n$$\n\\begin{align}\n\\text{Perimeter} &= \\text{3 cm} + \\text{4 cm} + \\text{5 cm}\\\\\n&= \\text{12 cm}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b025",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Worked example 12.7: Calculating perimeter of a parallelogram"
    },
    "content_text": "",
    "prompt_text": "Find the perimeter of the parallelogram given below.",
    "answer_text": "Step 1: Look at the diagram and take note of the information given.\n\nIn a parallelogram, the opposite sides have equal lengths. Fill in the missing lengths.\n\nStep 2: Think of how you \"walked\" around a polygon. Write down the calculation that you must do.\n\n$$\n\\text{Perimeter} = \\text{20 mm} + \\text{7 mm} + \\text{20 mm} + \\text{7 mm}\n$$\n\nStep 3: Do the calculation, writing the units as part of the answer.\n\n$$\n\\begin{align}\n\\text{Perimeter} &= \\text{20 mm} + \\text{7 mm} + \\text{20 mm} + \\text{7 mm}\\\\\n&= \\text{54 mm}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b026",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.5: Calculate perimeter of irregular polygons"
    },
    "content_text": "Source math retained:\n\\begin{align} \\text{Perimeter}& = \\text{5 m} + \\text{7 m} + \\text{3 m} + \\text{10 m}\\\\ &= \\text{25 m} \\end{align}",
    "prompt_text": "### Exercise 12.5: Calculate perimeter of irregular polygons",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b026-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.5: Calculate perimeter of irregular polygons"
    },
    "content_text": "Source math retained:\n\\begin{align} \\text{Perimeter of rectangle}& = 2l + 2b \\\\ &= 2 \\times \\text{50} + 2 \\times \\text{15} \\\\ &= \\text{100} + \\text{30} \\\\ &= \\text{130 mm} \\end{align}",
    "prompt_text": "### Exercise 12.5: Calculate perimeter of irregular polygons\n\n1. Give the name of the irregular polygon shown in the diagram, and calculate its perimeter.",
    "answer_text": "$$\n\\begin{align}\n\\text{Perimeter} &= \\text{7 cm} + \\text{8 cm} + \\text{9 cm}\\\\\n&= \\text{24 cm}\n\\end{align}\n$$\n\nThe name of the polygon: triangle.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b026-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.5: Calculate perimeter of irregular polygons"
    },
    "content_text": "Source math retained:\n\\begin{array}{ll} \\text{Perimeter of rectangle}& = 2l + 2b \\\\ & {= 2 \\times 7.25 + 2 \\times 5} \\\\ & {= 14.5 + 10} \\\\\\ & {= \\text{24.5 m}} \\end{array}",
    "prompt_text": "### Exercise 12.5: Calculate perimeter of irregular polygons\n\n2. Give the name of the irregular polygon shown in the diagram, and find its perimeter.",
    "answer_text": "$$\n\\begin{align}\n\\text{Perimeter} &= \\text{18 mm} + \\text{62 mm} + \\text{18 mm} + \\text{62 mm}\\\\\n&= \\text{160 mm}\n\\end{align}\n$$\n\nThe name of the polygon: rectangle.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b026-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.5: Calculate perimeter of irregular polygons"
    },
    "content_text": "Source math retained:\n\\begin{align} \\text{Perimeter}& = \\text{5 m} + \\text{7 m} + \\text{3 m} + \\text{10 m}\\\\ &= \\text{25 m} \\end{align}",
    "prompt_text": "### Exercise 12.5: Calculate perimeter of irregular polygons\n\n3. Give the name of the irregular polygon shown in the diagram, and find its perimeter.",
    "answer_text": "$$\n\\begin{align}\n\\text{Perimeter}&= \\text{5 m} + \\text{7 m} + \\text{3 m} + \\text{10 m}\\\\\n&= \\text{25 m}\n\\end{align}\n$$\n\nThe name of the polygon: trapezium.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b026-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.5: Calculate perimeter of irregular polygons"
    },
    "content_text": "Source math retained:\n\\begin{align} \\text{Perimeter} & = \\text{120 mm} + \\text{80 mm} + \\text{120 mm} + \\text{80 mm}\\\\ &= \\text{400 mm} \\end{align}",
    "prompt_text": "### Exercise 12.5: Calculate perimeter of irregular polygons\n\n4. Give the name of the irregular polygon shown in the diagram, and find its perimeter.",
    "answer_text": "$$\n\\begin{align}\n\\text{Perimeter} &= \\text{120 mm} + \\text{80 mm} + \\text{120 mm} + \\text{80 mm}\\\\\n&= \\text{400 mm}\n\\end{align}\n$$\n\nThe name of the polygon: parallelogram.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b026-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.5: Calculate perimeter of irregular polygons"
    },
    "content_text": "Source math retained:\n\\begin{align} \\text{Perimeter of rectangle}& = 2l + 2b \\\\ &= 2 \\times \\text{50} + 2 \\times \\text{15} \\\\ &= \\text{100} + \\text{30} \\\\ &= \\text{130 mm} \\end{align}",
    "prompt_text": "### Exercise 12.5: Calculate perimeter of irregular polygons\n\n5. Study the diagram below and calculate the perimeter of this shape by using the given lengths in cm.",
    "answer_text": "The perimeter of a two-dimensional object is the distance around its edge. The diagram below shows the perimeter in red and blue.\n\nTo find the perimeter, we need to add up all six sides of the shape. We can start at any corner we want and go around until we get back where we started. We will start at the corner labelled \"Start\".\n\n$$\n\\begin{array}{ll}\n\\text{Perimeter } &{ = \\text{Sum of lengths of sides}} \\\\\n&{= 6 + 7 + 4 + 3 + 2 + 4}\\\\\n& {= \\text{26 cm}}\n\\end{array}\n$$\n\nYou do not have to start at the same corner: you can start at any corner and you will get the same total distance. This is because the distance around the shape is the same no matter where you start.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b026-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.5: Calculate perimeter of irregular polygons"
    },
    "content_text": "Source math retained:\n\\begin{array}{ll} \\text{Perimeter of rectangle}& = 2l + 2b \\\\ & {= 2 \\times 7.25 + 2 \\times 5} \\\\ & {= 14.5 + 10} \\\\\\ & {= \\text{24.5 m}} \\end{array}",
    "prompt_text": "### Exercise 12.5: Calculate perimeter of irregular polygons\n\n6. Study the diagram below and calculate the perimeter of this object by using the given lengths in m.",
    "answer_text": "The diagram below shows the perimeter in red and blue.\n\nWe will start at the corner labelled \"Start\".\n\n$$\n\\begin{array}{ll}\n\\text{Perimeter} & {= \\text{Sum of lengths of sides}} \\\\\n&{= 7 + 7 + 2 + 5 + 5 + 2} \\\\\n& {= \\text{28 m}}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b026-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.5: Calculate perimeter of irregular polygons"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.5: Calculate perimeter of irregular polygons\n\n7. The diagram below shows a view from above Ms Chidi's house and land. The property has a fence going around the outside. What is the perimeter of the property, if measurements are given in metres?",
    "answer_text": "To calculate the perimeter, we add up all the boundary lines that form the perimeter of this property.\n\nIf we start at the black dot shown on the diagram and walk all around the boundary, we get:\n\n$$\n\\begin{array}{ll}\n\\text{Perimeter} &{= \\text{11} + \\text{22} + \\text{19} + \\text{4}}\\\\\n&{= \\text{56 m}}\n\\end{array}\n$$\n\nThe perimeter of the property is 56 m.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b027",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Formulae to find the perimeter of a rectangle and a square"
    },
    "content_text": "It can take long to find the perimeter of a polygon by counting the steps or adding the lengths of the sides. Luckily, there are formulae that we can use for some shapes. The formulae are based on the fact that the perimeter of a shape is the distance around the shape, and that these shapes have some sides that are equal.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b028",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Worked example 12.8: Using a formula to find the perimeter of a rectangle"
    },
    "content_text": "",
    "prompt_text": "Find the perimeter of the rectangle given below.",
    "answer_text": "Step 1: Look at the diagram and take note of the information given. Fill in the missing lengths.\n\nThe opposite sides of a rectangle are the same length. Let the longer side be $l$ and the shorter side be $b$.\n\nStep 2: Think of a shorter way than adding all the side lengths.\n\nIn a rectangle, you know that the two lengths are equal, and the two breadths are equal. This means you can use a formula to calculate the perimeter of a rectangle.\n\n$$\n\\begin{array}{ll}\n\\text{Perimeter of rectangle} & {= l + b + l + b} \\\\\n& {= 2 \\times l + 2 \\times b} \\\\\n& {= 2l + 2b} \\\\\n\\end{array}\n$$\n\nStep 3: Fill in the correct values.\n\n$$\n\\begin{array}{ll}\n\\text{Perimeter of rectangle} &= 2l + 2b\\\\\n&= 2 \\times \\text{15} + 2 \\times \\text{4} \\\\\n\\end{array}\n$$\n\nStep 4: Do the calculation, using BODMAS to remember the order of operations, so you need to multiply before you add. Write in the correct units at the end of the answer.\n\n$$\n\\begin{array}{ll}\n\\text{Perimeter of rectangle} &= 2l + 2b \\\\\n&= 2 \\times \\text{15} + 2 \\times \\text{4} \\\\\n&= \\text{38 cm}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b029",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Formulae to find the perimeter of a rectangle and a square"
    },
    "content_text": "For any parallelogram, including a rectangle, the two lengths are the same length, and the two breadths are the same length. This means we can use the formula we reached in the worked example above to calculate the perimeter of a parallelogram:\n\n$$\n\\text{Perimeter of parallelogram} = 2l + 2b\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b030",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Worked example 12.9: Using a formula to find the perimeter of a square"
    },
    "content_text": "",
    "prompt_text": "Find the perimeter of the square given below.",
    "answer_text": "Step 1: Look at the diagram and take note of the information given. Fill in the missing lengths. In a square all four sides are equal.\n\nStep 2: Think of a shorter way than adding all the side lengths.\n\nAll of the sides of a square are the same length. If we let the side be $s$, then the perimeter is:\n\n$$\n\\begin{array}{ll}\n\\text{Perimeter of square} &= s + s + s + s\\\\\n& {= 4 \\times s} \\\\\n& {= 4s}\n\\end{array}\n$$\n\nStep 3: Fill in the correct values.\n\n$$\n\\begin{array}{ll}\n\\text{Perimeter of square} &= 4s \\\\\n&= 4 \\times \\text{60}\n\\end{array}\n$$\n\nStep 4: Do the calculation, and remember to add the correct units to the answer.\n\n$$\n\\begin{array}{ll}\n\\text {Perimeter of square} &= 4s \\\\\n&= 4 \\times \\text{60} \\\\\n&= \\text{240 mm}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b031",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Formulae to find the perimeter of a rectangle and a square"
    },
    "content_text": "The four sides of a square and of a rhombus are all equal. We can therefore use the following formula to calculate the perimeter of a square and a rhombus:\n\n$$\n\\text{Perimeter of square and rhombus} = 4s\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b032",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Formulae to calculate perimeter"
    },
    "content_text": "The table below lists the formulae for the perimeter of the two-dimensional shapes you will be working with. In a formula, we can use $P$ as a symbol for perimeter.\n\nrectangle: ${P} = 2l + 2b$\n\nparallelogram: ${P} = 2l + 2b$\n\nsquare: ${P} = 4s$\n\nrhombus: ${P} = 4s$\n\ntriangle: ${P} = \\text{side 1} + \\text{side 2} + \\text{side 3} = s_1 + s_2 + s_3$\n\ntrapezium: ${P} = \\text{side 1} + \\text{side 2} + \\text{side 3} + \\text{side 4} = s_1 + s_2 + s_3 + s_4$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b033",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.6: Calculate perimeter using formulae"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.6: Calculate perimeter using formulae",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b033-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.6: Calculate perimeter using formulae"
    },
    "content_text": "Source math retained:\n\\begin{align} \\text{Perimeter of rectangle}& = 2l + 2b \\\\ &= 2 \\times \\text{50} + 2 \\times \\text{15} \\\\ &= \\text{100} + \\text{30} \\\\ &= \\text{130 mm} \\end{align}",
    "prompt_text": "### Exercise 12.6: Calculate perimeter using formulae\n\n1. Calculate the perimeter of the rectangle given below.",
    "answer_text": "$$\n\\begin{align}\n\\text{Perimeter of rectangle}&= 2l + 2b \\\\\n&= 2 \\times \\text{50} + 2 \\times \\text{15} \\\\\n&= \\text{100} + \\text{30} \\\\\n&= \\text{130 mm}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b033-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.6: Calculate perimeter using formulae"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.6: Calculate perimeter using formulae\n\n2. Calculate the perimeter of the square given below.",
    "answer_text": "$$\n\\begin{align}\n\\text{Perimeter of square}&= 4s\\\\\n&= 4 \\times \\text{120} \\\\\n&= \\text{480 cm}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b033-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.6: Calculate perimeter using formulae"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.6: Calculate perimeter using formulae\n\n3. Calculate the perimeter of the triangle given below.",
    "answer_text": "$$\n\\begin{align}\n\\text{Perimeter of triangle}&= s_1 + s_2 + s_3 \\\\\n&= \\text{14} + \\text{14} + \\text{9} \\\\\n&= \\text{37 m}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b033-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.6: Calculate perimeter using formulae"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.6: Calculate perimeter using formulae\n\n4. Calculate the perimeter of the parallelogram given below.",
    "answer_text": "$$\n\\begin{align}\n\\text{Perimeter of parallelogram}&= 2l + 2b \\\\\n&= 2 \\times \\text{90} + 2 \\times \\text{20} \\\\\n&= \\text{180} + \\text{40} \\\\\n&= \\text{220 mm}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b033-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.6: Calculate perimeter using formulae"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.6: Calculate perimeter using formulae\n\n5. Calculate the perimeter of the trapezium given below.",
    "answer_text": "$$\n\\begin{align}\n\\text{Perimeter of trapezium}&= s_1 + s_2 + s_3 + s_4\\\\\n&= \\text{31} + \\text{85} + \\text{31} + \\text{120}\\\\\n&= \\text{267 cm}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b033-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.6: Calculate perimeter using formulae"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.6: Calculate perimeter using formulae\n\n6. Consider the following square. Determine the perimeter of the square.",
    "answer_text": "$$\n\\begin{align}\n\\text{Perimeter of square}&= 4s\\\\\n&= 4 \\times \\text{6.1} \\\\\n&= \\text{24.4 cm}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b033-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.6: Calculate perimeter using formulae"
    },
    "content_text": "Source math retained:\n\\begin{array}{ll} \\text{Perimeter of rectangle}& = 2l + 2b \\\\ & {= 2 \\times 7.25 + 2 \\times 5} \\\\ & {= 14.5 + 10} \\\\\\ & {= \\text{24.5 m}} \\end{array}",
    "prompt_text": "### Exercise 12.6: Calculate perimeter using formulae\n\n7. Consider the following rectangle. Determine the perimeter of the rectangle.",
    "answer_text": "$$\n\\begin{array}{ll}\n\\text{Perimeter of rectangle}&= 2l + 2b \\\\\n& {= 2 \\times 7.25 + 2 \\times 5} \\\\\n& {= 14.5 + 10} \\\\\\\n& {= \\text{24.5 m}}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b033-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.6: Calculate perimeter using formulae"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.6: Calculate perimeter using formulae\n\n8. Calculate the perimeter of a triangle with the following side lengths: $\\frac {1}{4} \\text{m}; \\frac {1}{3} \\text{m and} \\frac {1}{2} \\text{m}$.",
    "answer_text": "In your calculation, remember to find the lowest common denominator of the fractions before you add them.\n\n$$\n\\begin{align}\n\\text{Perimeter of triangle}&= s_1 + s_2 + s_3 \\\\\n&= \\tfrac {1}{4}  + \\tfrac {1}{3} + \\tfrac {1}{2} \\\\\n&= \\tfrac {3}{12}  + \\tfrac {4}{12} + \\tfrac {6}{12} \\\\\n&= \\tfrac {13}{12} \\\\\n&= 1 \\tfrac {1}{12} \\text{m}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b033-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.6: Calculate perimeter using formulae"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.6: Calculate perimeter using formulae\n\n9. Calculate the perimeter of a rhombus with side length $\\frac {3}{8}$ km.",
    "answer_text": "$$\n\\begin{align}\n\\text{Perimeter of rhombus}&= 4s\\\\\n&= 4 \\times \\tfrac {3}{8} \\\\\n&= \\tfrac {4 \\times 3}{1 \\times 8}\\\\\n&= \\tfrac {12}{8} \\\\\n&= \\tfrac {3}{2} \\\\\n&= 1 \\tfrac {1}{2} \\text{km}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b033-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.6: Calculate perimeter using formulae"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.6: Calculate perimeter using formulae\n\n10. Calculate the perimeter of the trapezium given below.",
    "answer_text": "$$\n\\begin{align}\n\\text{Perimeter of trapezium}&= s_1 + s_2 + s_3 + s_4 \\\\\n&= 19y + 5y + 11y + 8y \\\\\n&= 43y \\text{ cm}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b033-i11",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.6: Calculate perimeter using formulae"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.6: Calculate perimeter using formulae\n\n11. The diagram below shows a notebook. What is the perimeter of the notebook if all the measurements are given in centimetres?",
    "answer_text": "The notebook is in the shape of a rectangle.\n\n$$\n\\begin{align}\n\\text{Perimeter of rectangle} &= 2l + 2b \\\\\n&= 2 \\times 25 + 2 \\times 15 \\\\\n&= \\text{50} + \\text{30} \\\\\n&= \\text{80 cm}\n\\end{align}\n$$\n\nThe perimeter of the notebook is $\\text{80 cm}$.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b034",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Using a formula to find the circumference of a circle"
    },
    "content_text": "We know that the perimeter of a circle is called its circumference. The circumference of a circle is a curve, so we cannot measure it with a ruler. We can use a formula to calculate the circumference of a circle. There are two formulae that we can use, which both mean the same thing:\n\n$$\n\\begin{array}{ll}\n\\boxed{C = \\pi \\times d} & {\\quad\\text{ or }\\quad\\boxed{C = 2 \\times \\pi \\times r}} \\\\\n\\end{array}\n$$\n\nIn these formulae, $C$ stands for circumference, $d$ stands for the **diameter** of the circle, and $r$ stands for the **radius** of the circle. We will mostly use the first formula with diameter, but you can use the radius formula if you prefer.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b035",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Using a formula to find the circumference of a circle"
    },
    "content_text": "**radius** The radius of a circle is the distance from the centre to the circumference.\n\n**diameter** The diameter of a circle is the length of a line passing through the centre of the circle, and touching the circumference at both ends.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b036",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Using a formula to find the circumference of a circle"
    },
    "content_text": "The diameter of a circle is double the radius, so $d = 2 \\times r$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b037",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Using a formula to find the circumference of a circle"
    },
    "content_text": "You will see that the symbol $\\pi$ is used in both formulae. This name of this symbol is \"pi\". **$\\pi$** is the ratio of the circumference of a circle to its diameter.\n\n$$\n\\begin{array}{l}\n\\pi = \\frac{C}{d}\n\\end{array}\n$$\n\nThe value of $\\pi$ is the same for all circles, large or small. We can see this by doing a quick experiment. Draw a circle with a compass. Place a piece of string along the circumference, and then measure the length of the string using a ruler. Next, use the ruler to measure the diameter of the circle. If we divide the circumference by the diameter, we will get a value that is approximately 3.14. If we do the same thing, but with a larger or a smaller circle, we will get the same value, every time!",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b038",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Using a formula to find the circumference of a circle"
    },
    "content_text": "$\\pi$ (pi) is the ratio of the circumference of a circle to its diameter. The values we use for $\\pi$ are 3.14 and $\\frac{22}{7}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b039",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Using a formula to find the circumference of a circle"
    },
    "content_text": "Look at the value of $\\pi$ that your calculator gives you, and compare this to the value of $\\frac{22}{7}$. Are they the same number?\n\n$\\pi$ is an unending number approximately equal to $\\frac{22}{7}$ or 3.14. Here are the first 200 digits of $\\pi$:\n\n$$\n\\begin{array}{ll}\n & \\text{3.141592653589793238462643383279502884197169399375105820974944} \\\\\n & 59230781640628620899862803482534211706798214808651328230664709 \\\\\n & 38446095505822317253594081284811174502841027019385211055596446 \\\\\n & 2294895493038196... \\\\\n\\end{array}\n$$\n\nScientists using powerful computers have calculated the value of $\\pi$ to over 13 trillion decimal places. But they will never be able to reach the end of this number, since the end does not exist.\n\nWhen we do calculations with $\\pi$, we cannot use the exact value of $\\pi$. Instead, we use an approximation of the value of $\\pi$. One commonly used value is 3.14, which is $\\pi$ rounded to two decimal places. Another approximation is $\\frac{22}{7}$. If we divide 22 by 7 on a calculator, we get 3.142857143. This is very close to $\\pi$ to two decimal places, but it is a slightly better approximation.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b040",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Worked example 12.10: Calculating circumference using diameter"
    },
    "content_text": "",
    "prompt_text": "The circle below has a diameter of 8 m. What is the circumference of this circle?",
    "answer_text": "Step 1: Write down the formula for the circumference of a circle:\n\n$$\n\\begin{array}{l}\n C = \\pi \\times d\n \\end{array}\n$$\n\nStep 2: The question tells us that the diameter of the circle is 8 m. Substitute 8 for the $d$ in the formula to find the circumference of the circle.\n\nWe will use 3.14 for $\\pi$.\n\n$$\n\\begin{array}{ll}\n C  &{= \\pi \\times d} \\\\\n & {= 3.14 \\times 8}\n \\end{array}\n$$\n\nStep 3: Do the calculation and remember to show the correct units with the answer.\n\n$$\n\\begin{array}{ll}\n C  &{= \\pi \\times d}\\\\\n &{= 3.14 \\times 8} \\\\\n &{= \\text{25.12 m}}\n \\end{array}\n$$\n\nThe circumference of the circle is 25.12 m.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b041",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Using a formula to find the circumference of a circle"
    },
    "content_text": "If you have a $\\pi$ button on your calculator, you may use it to work out the answer. But if the question gives you a value to use, such as 3.14, use that value.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b042",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Worked example 12.11: Calculating circumference using radius"
    },
    "content_text": "",
    "prompt_text": "The circle below has a radius of 2 cm. What is the circumference of the circle? Use 3.14 for $\\pi$.",
    "answer_text": "Step 1: Write down the formula for the circumference of a circle.\n\n$$\n\\begin{array}{ll}\n C  {= \\pi \\times d}\n \\end{array}\n$$\n\nOr you can use $C = \\pi \\times 2r$.\n\nStep 2: The question tells us that the radius of the circle is 2 cm. So the diameter is 4 cm. Substitute 4 for the $d$ in the formula. Also substitute 3.14 for $\\pi$.\n\n$$\n\\begin{array}{ll}\n C & {= \\pi \\times d} \\\\\n & {= 3.14 \\times 4} \\\\\n \\end{array}\n$$\n\nAs you can see, if you used $C = \\pi \\times 2r$, you would also get $3.14 \\times 4$.\n\nStep 3: Calculate the circumference of the circle. Remember to show the correct units in your answer.\n\n$$\n\\begin{array}{ll}\n C & {= \\pi \\times d}\\\\\n &{= 3.14 \\times 4}\\\\\n &{= \\text{12.56 cm}}\n \\end{array}\n$$\n\nThe circumference of the circle is 12.56 cm.",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b043",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.7: Calculate the circumference of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.7: Calculate the circumference of a circle\n\nUse 3.14 for $\\pi$ in all your calculations.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b043-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.7: Calculate the circumference of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.7: Calculate the circumference of a circle\n\nUse 3.14 for $\\pi$ in all your calculations.\n\n1. The circle below has a diameter of 9 cm. What is the circumference of the circle?",
    "answer_text": "$$\n\\begin{array}{ll}\nC &{= \\pi \\times d}\\\\\n&{= 3.14 \\times 9}\\\\\n&{= \\text{28.26}\\ \\text{cm}}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b043-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.7: Calculate the circumference of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.7: Calculate the circumference of a circle\n\nUse 3.14 for $\\pi$ in all your calculations.\n\n2. The circle below has a radius of 5 cm. What is the circumference of the circle?",
    "answer_text": "If the radius is 5 cm, then the diameter is 10 cm.\n\n$$\n\\begin{array}{ll}\nC & {= \\pi \\times d}\\\\\n&{= 3.14 \\times 10}\\\\\n&{= \\text{31.4 cm}}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b043-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.7: Calculate the circumference of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.7: Calculate the circumference of a circle\n\nUse 3.14 for $\\pi$ in all your calculations.\n\n3. If a circle has a diameter of 11 m, what is the circumference of the circle?",
    "answer_text": "$$\n\\begin{array}{ll}\nC & {= \\pi \\times d} \\\\\n&{= 3.14 \\times 11} \\\\\n&{= \\text{34.54}\\ \\text{m}}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b043-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.7: Calculate the circumference of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.7: Calculate the circumference of a circle\n\nUse 3.14 for $\\pi$ in all your calculations.\n\n4. If a circle has a radius of 10 m, what is the circumference of the circle?",
    "answer_text": "If the radius is 10 cm, then the diameter is 20 cm.\n\n$$\n\\begin{array}{ll}\nC  &{= \\pi  \\times d}\\\\\n&{= 3.14 \\times 20} \\\\\n&{= \\text{62.8 m}}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b043-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.7: Calculate the circumference of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.7: Calculate the circumference of a circle\n\nUse 3.14 for $\\pi$ in all your calculations.\n\n5. What is the circumference of a circle that has a diameter of 40 mm?",
    "answer_text": "$$\n\\begin{array}{ll}\nC& {= \\pi \\times d} \\\\\n&{= 3.14 \\times 40} \\\\\n&{= \\text{125.6 mm}}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b043-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.2 Perimeter of two-dimensional shapes",
      "h3": "Exercise 12.7: Calculate the circumference of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.7: Calculate the circumference of a circle\n\nUse 3.14 for $\\pi$ in all your calculations.\n\n6. What is the circumference of a circle that has a radius of 50 mm?",
    "answer_text": "If radius is 50 mm, then diameter is 100 mm.\n\n$$\n\\begin{array}{ll}\nC & {= \\pi \\times d}\\\\\n&{= 3.14 \\times 100} \\\\\n&{= \\text{314 mm}}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b069",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.4 Practical applications",
      "h3": null
    },
    "content_text": "In real life we often need to calculate a perimeter or area. Then it is useful to know the correct formula as well as how to use the formula.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-area-of-regular-plane-shapes-such-as-squares-rectangles-parallelograms-etc"
  },
  {
    "record_id": "ch12-b071",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.4 Practical applications",
      "h3": "Exercise 12.12 :Find perimeter and area in real life situations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.12: Find perimeter and area in real life situations",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-area-of-regular-plane-shapes-such-as-squares-rectangles-parallelograms-etc"
  },
  {
    "record_id": "ch12-b071-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.4 Practical applications",
      "h3": "Exercise 12.12 :Find perimeter and area in real life situations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.12: Find perimeter and area in real life situations\n\n1. The diagram below shows a notebook with all the measurements given in centimetres.\n\nFind the perimeter of the notebook.",
    "answer_text": "The notebook is in the shape of a rectangle, so you use the formulae for the perimeter of a rectangle.\n\n$$\n\\begin{align}\nP  & = 2l + 2b\\\\\n& {= 2 \\times 25 + 2 \\times 15}\\\\\n& {= \\text{50} + \\ \\text{30}}\\\\\n& {= \\text{80}\\ \\text{cm}}\n \\end{align}\n$$\n\nThe notebook has a perimeter of 80 cm.",
    "primary_subtopic_id": "jss1-math-plane-shapes-area-of-regular-plane-shapes-such-as-squares-rectangles-parallelograms-etc"
  },
  {
    "record_id": "ch12-b071-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.4 Practical applications",
      "h3": "Exercise 12.12 :Find perimeter and area in real life situations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.12: Find perimeter and area in real life situations\n\n2. The diagram below shows a notebook with all the measurements given in centimetres.\n\nFind the area of the notebook.",
    "answer_text": "Use the formula for the area of a rectangle.\n\n$$\n\\begin{align}\nA  & = l \\times b\\\\\n& {= 25 \\times 15}\\\\\n& {= \\text{375}\\ \\text{cm}^{2}}\n \\end{align}\n$$\n\nThe notebook has an area of 375 cm$^{2}$.",
    "primary_subtopic_id": "jss1-math-plane-shapes-area-of-regular-plane-shapes-such-as-squares-rectangles-parallelograms-etc"
  },
  {
    "record_id": "ch12-b071-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.4 Practical applications",
      "h3": "Exercise 12.12 :Find perimeter and area in real life situations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.12: Find perimeter and area in real life situations\n\n3. Adanna is renovating her house, and she wants to have a blind made for the window. The blind will be a flat piece of fabric that reaches to the outside edge of the window. The window is in the shape of a square, and at the outside edge, the sides are all 65 centimetres.\n\nAdanna wants to have a velvet strip around the edge of the blind. Find the perimeter of the window to work out the length of the velvet strip.",
    "answer_text": "The window is in the shape of a square, so use the formula for the perimeter of a square.\n\n$$\n\\begin{align}\nP  & = 4s \\\\\n& {= 4 \\times 65}\\\\\n& {= \\text{260}\\ \\text{cm}}\n \\end{align}\n$$\n\nThe perimeter of the window is 260 cm, so the velvet strip will be 260 cm long.",
    "primary_subtopic_id": "jss1-math-plane-shapes-area-of-regular-plane-shapes-such-as-squares-rectangles-parallelograms-etc"
  },
  {
    "record_id": "ch12-b071-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.4 Practical applications",
      "h3": "Exercise 12.12 :Find perimeter and area in real life situations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.12: Find perimeter and area in real life situations\n\n4. Adanna is renovating her house, and she wants to have a blind made for the window. The blind will be a flat piece of fabric that reaches to the outside edge of the window. The window is in the shape of a square, and at the outside edge, the sides are all 65 centimetres.\n\nFind the area of the window to work out how big the blind has to be.",
    "answer_text": "Use the formula for area of a square.\n\n$$\n\\begin{align}\nA & = s^{2} \\\\\n& {= 65 \\times 65}\\\\\n& {= 4,\\!225\\ \\text{cm}^{2}}\n\\end{align}\n$$\n\nThe blind will be 4,225 cm$^{2}$.",
    "primary_subtopic_id": "jss1-math-plane-shapes-area-of-regular-plane-shapes-such-as-squares-rectangles-parallelograms-etc"
  },
  {
    "record_id": "ch12-b071-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.4 Practical applications",
      "h3": "Exercise 12.12 :Find perimeter and area in real life situations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.12: Find perimeter and area in real life situations\n\n5. Talatu paints plates to sell to tourists. She paints the plates purple with a white circle in the centre.\n\nThe diagram below shows the plate. $O$ is the centre of the plate. The radius of the small white circle is 3 cm and the radius of the big blue circle is 7 cm.\n\nDetermine the area of the purple region. Use 3.14 for $\\pi$.",
    "answer_text": "To calculate the area of the purple region, you need to calculate the area of each of the two circles, and then subtract one area from the other.\n\n**Area of big circle:**\n\n$$\n\\begin{array}{ll}\nA_\\text{1} & {= \\pi \\times R^{2}} \\\\\n& {= 3.14 \\times 7^{2}} \\\\\n& {= 3.14 \\times 49} \\\\\n& {= 153.86\\ {\\text{cm}^{2}}} \\\\\n\\end{array}\n$$\n\n**Area of small circle:**\n\n$$\n\\begin{array}{ll}\nA_\\text{2} & {= \\pi \\times r^{2}} \\\\\n& {= 3.14 \\times 3^{2}} \\\\\n& {= 3.14 \\times 9} \\\\\n& {= 28.26\\ {\\text{cm}^{2}}} \\\\\n\\end{array}\n$$\n\n**Area of purple region:**\n\n$$\n\\begin{array}{ll}\nA & {= A_\\text{1} - A_\\text{2}} \\\\\n& {= 153.86 - 28.26} \\\\\n& {= \\text{125.6}\\ {\\text{cm}^{2}}}\n\\end{array}\n$$\n\nThe area of the purple region is 125.6 cm$^{2}$.",
    "primary_subtopic_id": "jss1-math-plane-shapes-area-of-regular-plane-shapes-such-as-squares-rectangles-parallelograms-etc"
  },
  {
    "record_id": "ch12-b072",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.5 Summary",
      "h3": null
    },
    "content_text": "A two-dimensional (2D) shape has two dimensions that we can measure: length and breadth (or width).\n\nA polygon is a closed flat shape with three or more straight sides. A triangle has three sides and three angles. A quadrilateral has four sides and four angles. Examples of quadrilaterals are square, rectangle, rhombus, parallelogram, and trapezium.\n\nA circle is a 2D shape with a curved edge, so a circle is not a polygon. The perimeter of a circle is called its circumference. A line segment that goes all the way across the circle and passes through the centre is called a diameter. A line segment from the centre of the circle to a point on the circumference is called a radius.\n\nPerimeter is the distance around the outside of a shape. We can use the following formulae to calculate the perimeter of regular polygons:\n\n- rectangle: $P = 2l + 2b$\n- parallelogram: $P = 2l + 2b$\n- square: $P = 4s$\n- rhombus: $P = 4s$\n- triangle: $P = \\text{side 1} + \\text{side 2} + \\text{side 3} = s_1 + s_2 + s_3$\n- trapezium: $P = \\text{side 1} + \\text{side 2} + \\text{side 3} + \\text{side 4} = s_1 + s_2 + s_3 + s_4$\n\nArea is the amount of flat space taken up by a shape. We can use formulae to calculate the area of two-dimensional shapes:\n\n- rectangle: $A = l \\times b$\n- square: $A = s \\times s = s^{2}$\n- triangle: $A = \\frac{b \\times h}{2}$\n- parallelogram: $A = b \\times h$\n- trapezium: $A = \\frac{h}{2}\\left( a + b \\right)$\n- circle: $A = \\pi \\times r^{2}$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
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
