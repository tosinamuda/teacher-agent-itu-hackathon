# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-4",
  "topic_key": "jss1-math-plane-shapes",
  "topic": "Plane shapes",
  "subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle",
  "subtopic_title": "Similarities and differences between the following: Square, rectangle, triangle, trapezium, parallelogram and circle.",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle-po01",
        "source_performance_objective_index": 1,
        "text": "State the similarities and differences between the following: square, rectangle, triangle, trapezium, parallelogram and circle"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "similarities-and-differences-between-plane-shapes-ao-state-similarities",
          "text": "State the similarities between square, rectangle, triangle, trapezium, parallelogram and circle."
        },
        {
          "atomic_objective_id": "similarities-and-differences-between-plane-shapes-ao-state-differences",
          "text": "State the differences between square, rectangle, triangle, trapezium, parallelogram and circle."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch12-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": null
    },
    "content_text": "A two-dimensional (2D) shape has two dimensions that we can measure: we can measure the length and we can measure the breadth (sometimes called the width) of the shape. For example, a square is a 2D shape. All the sides of a square are straight lines. A circle is also a 2D shape, but a circle has a curved edge.\n\nWe use a special name for the 2D shapes that are formed by straight lines. They are called **polygons**. We name polygons by counting the number of straight sides that they have. A polygon with five sides is called a pentagon and a polygon with six sides is a hexagon.\n\nThere is a whole group of polygons with four sides, and they are the **quadrilaterals**. You have worked with squares, rectangles, parallelograms, rhombuses and trapeziums before. All of them are examples of quadrilaterals.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b002",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": null
    },
    "content_text": "**polygon** A polygon is a closed flat shape with three or more straight sides.\n\n**quadrilateral** A quadrilateral is a polygon that has four sides and four angles.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b003",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Properties of two-dimensional shapes"
    },
    "content_text": "The properties of these two-dimensional shapes are listed below.\n\n**A. Square**\n- A square has four equal sides and four right angles.\n- The opposite sides of a square are parallel.\n\n**B. Rectangle**\n- A rectangle has two pairs of equal sides. The longer side of a rectangle is the *length* and the shorter side is the *breadth*.\n- A rectangle has four right angles.\n- The opposite sides of a rectangle are parallel.\n\n**C. Parallelogram**\n- A parallelogram has two pairs of opposite sides that are parallel and equal.\n- The opposite angles are equal.\n\n**D. Rhombus**\n- A rhombus has four equal sides.\n- Opposite sides are parallel.\n- The opposite angles are equal.\n- Two of the angles are acute (more closed) angles, and two are obtuse (more open) angles.\n\n**E. Trapezium**\n- A trapezium has one pair of parallel sides.\n- The sides may all be different in length.\n\n**F. Triangle**\n- A triangle has three sides and three angles. All the sides and angles can be different sizes.\n- There are different types of triangles. The triangle shown is an equilateral triangle, which has all three sides equal in length and all three angles equal.\n\n**G. Circle**\n- The properties and different parts of a circle are explained further on.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b004",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Worked example 12.1: Comparing two-dimensional shapes"
    },
    "content_text": "",
    "prompt_text": "Look at the two shapes. State which shape is NOT a polygon, and identify and name the quadrilateral.",
    "answer_text": "Step 1: Remember the definition of a polygon.\n\nA polygon is a closed flat shape with three or more straight sides.\n\nStep 2: Identify the shape without straight sides.\n\nAnswer: The circle has curved sides, so it is not a polygon.\n\nStep 3: Remember the definition of a quadrilateral.\n\nA quadrilateral is a polygon that has four sides and four angles.\n\nStep 4: Identify the shape that has four sides and four angles, and name the shape.\n\nAnswer: The quadrilateral is a trapezium.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b005",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.1: Compare two-dimensional shapes"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.1: Compare two-dimensional shapes",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b005-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.1: Compare two-dimensional shapes"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.1: Compare two-dimensional shapes\n\n1. Compare a square and a rectangle. What is similar? What is different?",
    "answer_text": "Similar: A square has four right angles. A rectangle also has four right angles.\n\nDifferent: A square has four equal sides. A rectangle has two longer sides and two shorter sides.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b005-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.1: Compare two-dimensional shapes"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.1: Compare two-dimensional shapes\n\n2. Compare a square and a rhombus. What is similar? What is different?",
    "answer_text": "Similar: A square has four equal sides. A rhombus also has four equal sides.\n\nDifferent: A square has four right angles. A rhombus has two acute angles and two obtuse angles.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b005-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.1: Compare two-dimensional shapes"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.1: Compare two-dimensional shapes\n\n3. Compare a trapezium and a parallelogram. What is similar? What is different?",
    "answer_text": "Similar: A trapezium is a quadrilateral. A parallelogram is also a quadrilateral.\n\nDifferent: A trapezium has one pair of parallel sides. A parallelogram has two pairs of parallel sides.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b005-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.1: Compare two-dimensional shapes"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.1: Compare two-dimensional shapes\n\n4. Compare a parallelogram and a rhombus. What is similar? What is different?",
    "answer_text": "Similar: A parallelogram has two pairs of parallel sides. A rhombus also has two pairs of parallel sides.\n\nDifferent: A parallelogram has two longer sides and two shorter sides. A rhombus has four equal sides.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b005-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.1: Compare two-dimensional shapes"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.1: Compare two-dimensional shapes\n\n5. Compare a triangle and a square. What is similar? What is different?",
    "answer_text": "Similar: A triangle is a polygon. A square is also a polygon.\n\nDifferent: A triangle has three sides. A square has four sides.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b006",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Parts and properties of a circle"
    },
    "content_text": "A circle is a 2D shape with a curved edge, so a circle is not a polygon. We use special names for the different parts of a circle.\n\n- The perimeter of a circle (the length around the circle) is called its *circumference*.\n- A line segment that goes all the way across the circle and passes through the centre is called a *diameter*.\n- A line segment from the centre of the circle to a point on the circumference is called a *radius*.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b007",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Worked example 12.2: Identifying parts of a circle"
    },
    "content_text": "",
    "prompt_text": "In the diagram below, $O$ is the centre of the circle. $T$, $S$, and $V$ are labels for parts of the circle. Which of the labels identifies the circumference of the circle?",
    "answer_text": "Step 1: Identify the parts of the circle.\n\nA line segment that goes all the way across the circle and passes through the centre is called a diameter.\n\nA line segment from the centre of the circle to a point on the circumference is called a radius.\n\nThe perimeter of a circle (the length around the circle) is called its circumference.\n\nStep 2: Read the question again and give the correct answer.\n\n$V$ is the circumference of the circle.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b008",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.2: Identify parts of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.2: Identify parts of a circle",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b008-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.2: Identify parts of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.2: Identify parts of a circle\n\n1. In the diagram below, $O$ is the centre of the circle. $T$, $S$ and $V$ are labels for parts of the circle.\n\n(a) Which of the labels identifies a diameter of the circle?",
    "answer_text": "$V$ is a diameter of the circle.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b008-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.2: Identify parts of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.2: Identify parts of a circle\n\n2. In the diagram below, $O$ is the centre of the circle. $T$, $S$ and $V$ are labels for parts of the circle.\n\n(b) Which of the labels identifies a radius of the circle?",
    "answer_text": "$S$ is a radius of the circle.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b008-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.2: Identify parts of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.2: Identify parts of a circle\n\n3. In the diagram below, $O$ is the centre of the circle. $T$, $S$ and $V$ are labels for parts of the circle.\n\n(c) Which of the labels identifies the circumference of the circle?",
    "answer_text": "$T$ is the circumference of the circle.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b008-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.2: Identify parts of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.2: Identify parts of a circle\n\n4. A diagram of a circle is given. $O$ is the centre of the circle.\n\n(a) Which part of the circle is labelled $T$?",
    "answer_text": "$T$ is a line segment from the centre of the circle to a point on the circumference, so $T$ is a radius.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b008-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.2: Identify parts of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.2: Identify parts of a circle\n\n5. A diagram of a circle is given. $O$ is the centre of the circle.\n\n(b) Which part of the circle is labelled $S$?",
    "answer_text": "$S$ is a line segment that goes all the way across the circle and passes through the centre, so $S$ is a diameter.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b008-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.2: Identify parts of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.2: Identify parts of a circle\n\n6. A diagram of a circle is given. $O$ is the centre of the circle.\n\n(c) Which part of the circle is labelled $V$?",
    "answer_text": "$V$ shows the perimeter of the circle (the length around the circle), so $V$ is the circumference.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b008-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.2: Identify parts of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.2: Identify parts of a circle\n\n7. Select a word from Column B that best fits the description in Column A.\n\na) A line segment that goes all the way across the circle and passes through the centre.\n\nColumn B: A: Circumference, B: Radius, C: Diameter",
    "answer_text": "C",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b008-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.2: Identify parts of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.2: Identify parts of a circle\n\n8. Select a word from Column B that best fits the description in Column A.\n\nb) The perimeter of a circle (the length around the circle).\n\nColumn B: A: Circumference, B: Radius, C: Diameter",
    "answer_text": "A",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b008-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.2: Identify parts of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.2: Identify parts of a circle\n\n9. Select a word from Column B that best fits the description in Column A.\n\nc) A line segment from the centre of the circle to a point on the circumference.\n\nColumn B: A: Circumference, B: Radius, C: Diameter",
    "answer_text": "B",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
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
  "subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle",
  "subtopic_title": "Similarities and differences between the following: Square, rectangle, triangle, trapezium, parallelogram and circle.",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle-po01",
        "source_performance_objective_index": 1,
        "text": "State the similarities and differences between the following: square, rectangle, triangle, trapezium, parallelogram and circle"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "similarities-and-differences-between-plane-shapes-ao-state-similarities",
          "text": "State the similarities between square, rectangle, triangle, trapezium, parallelogram and circle."
        },
        {
          "atomic_objective_id": "similarities-and-differences-between-plane-shapes-ao-state-differences",
          "text": "State the differences between square, rectangle, triangle, trapezium, parallelogram and circle."
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
    "record_id": "ch12-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": null
    },
    "content_text": "A two-dimensional (2D) shape has two dimensions that we can measure: we can measure the length and we can measure the breadth (sometimes called the width) of the shape. For example, a square is a 2D shape. All the sides of a square are straight lines. A circle is also a 2D shape, but a circle has a curved edge.\n\nWe use a special name for the 2D shapes that are formed by straight lines. They are called **polygons**. We name polygons by counting the number of straight sides that they have. A polygon with five sides is called a pentagon and a polygon with six sides is a hexagon.\n\nThere is a whole group of polygons with four sides, and they are the **quadrilaterals**. You have worked with squares, rectangles, parallelograms, rhombuses and trapeziums before. All of them are examples of quadrilaterals.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b002",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": null
    },
    "content_text": "**polygon** A polygon is a closed flat shape with three or more straight sides.\n\n**quadrilateral** A quadrilateral is a polygon that has four sides and four angles.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b003",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Properties of two-dimensional shapes"
    },
    "content_text": "The properties of these two-dimensional shapes are listed below.\n\n**A. Square**\n- A square has four equal sides and four right angles.\n- The opposite sides of a square are parallel.\n\n**B. Rectangle**\n- A rectangle has two pairs of equal sides. The longer side of a rectangle is the *length* and the shorter side is the *breadth*.\n- A rectangle has four right angles.\n- The opposite sides of a rectangle are parallel.\n\n**C. Parallelogram**\n- A parallelogram has two pairs of opposite sides that are parallel and equal.\n- The opposite angles are equal.\n\n**D. Rhombus**\n- A rhombus has four equal sides.\n- Opposite sides are parallel.\n- The opposite angles are equal.\n- Two of the angles are acute (more closed) angles, and two are obtuse (more open) angles.\n\n**E. Trapezium**\n- A trapezium has one pair of parallel sides.\n- The sides may all be different in length.\n\n**F. Triangle**\n- A triangle has three sides and three angles. All the sides and angles can be different sizes.\n- There are different types of triangles. The triangle shown is an equilateral triangle, which has all three sides equal in length and all three angles equal.\n\n**G. Circle**\n- The properties and different parts of a circle are explained further on.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b004",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Worked example 12.1: Comparing two-dimensional shapes"
    },
    "content_text": "",
    "prompt_text": "Look at the two shapes. State which shape is NOT a polygon, and identify and name the quadrilateral.",
    "answer_text": "Step 1: Remember the definition of a polygon.\n\nA polygon is a closed flat shape with three or more straight sides.\n\nStep 2: Identify the shape without straight sides.\n\nAnswer: The circle has curved sides, so it is not a polygon.\n\nStep 3: Remember the definition of a quadrilateral.\n\nA quadrilateral is a polygon that has four sides and four angles.\n\nStep 4: Identify the shape that has four sides and four angles, and name the shape.\n\nAnswer: The quadrilateral is a trapezium.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b005",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.1: Compare two-dimensional shapes"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.1: Compare two-dimensional shapes",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b005-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.1: Compare two-dimensional shapes"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.1: Compare two-dimensional shapes\n\n1. Compare a square and a rectangle. What is similar? What is different?",
    "answer_text": "Similar: A square has four right angles. A rectangle also has four right angles.\n\nDifferent: A square has four equal sides. A rectangle has two longer sides and two shorter sides.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b005-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.1: Compare two-dimensional shapes"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.1: Compare two-dimensional shapes\n\n2. Compare a square and a rhombus. What is similar? What is different?",
    "answer_text": "Similar: A square has four equal sides. A rhombus also has four equal sides.\n\nDifferent: A square has four right angles. A rhombus has two acute angles and two obtuse angles.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b005-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.1: Compare two-dimensional shapes"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.1: Compare two-dimensional shapes\n\n3. Compare a trapezium and a parallelogram. What is similar? What is different?",
    "answer_text": "Similar: A trapezium is a quadrilateral. A parallelogram is also a quadrilateral.\n\nDifferent: A trapezium has one pair of parallel sides. A parallelogram has two pairs of parallel sides.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b005-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.1: Compare two-dimensional shapes"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.1: Compare two-dimensional shapes\n\n4. Compare a parallelogram and a rhombus. What is similar? What is different?",
    "answer_text": "Similar: A parallelogram has two pairs of parallel sides. A rhombus also has two pairs of parallel sides.\n\nDifferent: A parallelogram has two longer sides and two shorter sides. A rhombus has four equal sides.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b005-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.1: Compare two-dimensional shapes"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.1: Compare two-dimensional shapes\n\n5. Compare a triangle and a square. What is similar? What is different?",
    "answer_text": "Similar: A triangle is a polygon. A square is also a polygon.\n\nDifferent: A triangle has three sides. A square has four sides.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b006",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Parts and properties of a circle"
    },
    "content_text": "A circle is a 2D shape with a curved edge, so a circle is not a polygon. We use special names for the different parts of a circle.\n\n- The perimeter of a circle (the length around the circle) is called its *circumference*.\n- A line segment that goes all the way across the circle and passes through the centre is called a *diameter*.\n- A line segment from the centre of the circle to a point on the circumference is called a *radius*.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b007",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Worked example 12.2: Identifying parts of a circle"
    },
    "content_text": "",
    "prompt_text": "In the diagram below, $O$ is the centre of the circle. $T$, $S$, and $V$ are labels for parts of the circle. Which of the labels identifies the circumference of the circle?",
    "answer_text": "Step 1: Identify the parts of the circle.\n\nA line segment that goes all the way across the circle and passes through the centre is called a diameter.\n\nA line segment from the centre of the circle to a point on the circumference is called a radius.\n\nThe perimeter of a circle (the length around the circle) is called its circumference.\n\nStep 2: Read the question again and give the correct answer.\n\n$V$ is the circumference of the circle.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b008",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.2: Identify parts of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.2: Identify parts of a circle",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b008-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.2: Identify parts of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.2: Identify parts of a circle\n\n1. In the diagram below, $O$ is the centre of the circle. $T$, $S$ and $V$ are labels for parts of the circle.\n\n(a) Which of the labels identifies a diameter of the circle?",
    "answer_text": "$V$ is a diameter of the circle.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b008-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.2: Identify parts of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.2: Identify parts of a circle\n\n2. In the diagram below, $O$ is the centre of the circle. $T$, $S$ and $V$ are labels for parts of the circle.\n\n(b) Which of the labels identifies a radius of the circle?",
    "answer_text": "$S$ is a radius of the circle.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b008-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.2: Identify parts of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.2: Identify parts of a circle\n\n3. In the diagram below, $O$ is the centre of the circle. $T$, $S$ and $V$ are labels for parts of the circle.\n\n(c) Which of the labels identifies the circumference of the circle?",
    "answer_text": "$T$ is the circumference of the circle.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b008-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.2: Identify parts of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.2: Identify parts of a circle\n\n4. A diagram of a circle is given. $O$ is the centre of the circle.\n\n(a) Which part of the circle is labelled $T$?",
    "answer_text": "$T$ is a line segment from the centre of the circle to a point on the circumference, so $T$ is a radius.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b008-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.2: Identify parts of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.2: Identify parts of a circle\n\n5. A diagram of a circle is given. $O$ is the centre of the circle.\n\n(b) Which part of the circle is labelled $S$?",
    "answer_text": "$S$ is a line segment that goes all the way across the circle and passes through the centre, so $S$ is a diameter.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b008-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.2: Identify parts of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.2: Identify parts of a circle\n\n6. A diagram of a circle is given. $O$ is the centre of the circle.\n\n(c) Which part of the circle is labelled $V$?",
    "answer_text": "$V$ shows the perimeter of the circle (the length around the circle), so $V$ is the circumference.",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b008-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.2: Identify parts of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.2: Identify parts of a circle\n\n7. Select a word from Column B that best fits the description in Column A.\n\na) A line segment that goes all the way across the circle and passes through the centre.\n\nColumn B: A: Circumference, B: Radius, C: Diameter",
    "answer_text": "C",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b008-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.2: Identify parts of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.2: Identify parts of a circle\n\n8. Select a word from Column B that best fits the description in Column A.\n\nb) The perimeter of a circle (the length around the circle).\n\nColumn B: A: Circumference, B: Radius, C: Diameter",
    "answer_text": "A",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
  },
  {
    "record_id": "ch12-b008-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 12: Two-dimensional shapes",
      "h2": "12.1 Types and properties of shapes",
      "h3": "Exercise 12.2: Identify parts of a circle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 12.2: Identify parts of a circle\n\n9. Select a word from Column B that best fits the description in Column A.\n\nc) A line segment from the centre of the circle to a point on the circumference.\n\nColumn B: A: Circumference, B: Radius, C: Diameter",
    "answer_text": "B",
    "primary_subtopic_id": "jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle"
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
