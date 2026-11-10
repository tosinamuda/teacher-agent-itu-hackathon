# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-4",
  "topic_key": "jss1-math-three-dimensional-figures",
  "topic": "Three dimensional figures",
  "subtopic_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids",
  "subtopic_title": "Volume of cubes and cuboids",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids-po01",
        "source_performance_objective_index": 1,
        "text": "Find volume of a cube and a cuboid"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "volume-of-cubes-and-cuboids-ao-find-volume-of-cube",
          "text": "Find volume of a cube."
        },
        {
          "atomic_objective_id": "volume-of-cubes-and-cuboids-ao-find-volume-of-cuboid",
          "text": "Find volume of a cuboid."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch13-b048",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.6 Volume of cubes and cuboids",
      "h3": null
    },
    "content_text": "Volume is the amount of the space that a 3D object takes up. Volume is a way of measuring the size of a whole 3D object. It is measured in cubic units.\n\nWhen we measure *length*, we measure one dimension. The length of the line below is $1 \\text{ cm}$. We say the length of the line is \"1 centimetre\".\n\nWhen we measure *area*, we measure two dimensions. The square below has a length of 1 cm and a breadth (or width) of 1 cm. The area of the square is $1 \\text{ cm}^{2}$. We say the area is \"1 square centimetre\".\n\nWhen we measure *volume*, we measure three dimensions. The cube below has a length of 1 cm, a breadth of 1 cm and a height of 1 cm. The volume of the cube is $1 \\text{ cm}^{3}$. We say the volume is \"1 cubic centimetre\".\n\nWhen we calculate the volume of a container, we work out how many cubes we can pack into the container. We start by finding out how many cubes will cover the base of the container.\n\nIn the container below, it is possible to pack 6 cubes across the length of the container and 4 cubes across the breadth of the container. To find the number of cubes for one layer, we multiply the number of cubes along the length by the number of cubes along the breadth:\n\n6 × 4 = 24\n\nTo fill the whole container, we pack more layers. In the container below it is possible to pack 8 layers. This container is a prism, so each layer will have the same number of cubes. To find the total number of cubes we multiply the number of cubes in one layer by the number of layers.\n\n$$\n\\begin{align}\n\\text{Total number of cubes} &= 24 \\times 8\\\\\n&= 192 \\text{ cubes}\n\\end{align}\n$$\n\nFrom this calculation, we can see that we calculate the volume of a prism by multiplying the area of the base of the prism by the height of the prism.\n\nThe volume of a prism is calculated using this formula:\n\n$$\nV_\\text{prism} = \\text{area of base} \\times \\text{height of the prism}\n$$\n\nThis formula can be used to calculate the volume of any prism. The prism can have a triangle or a pentagon or a hexagon as its base, and this formula will still hold.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b049",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.6 Volume of cubes and cuboids",
      "h3": "Worked example 13.9: Calculating the volume of a cube"
    },
    "content_text": "",
    "prompt_text": "Find the volume of the following cube. The cube has side length 3 cm.",
    "answer_text": "Step 1: A cube is a prism. Write down the formula to find the volume of a prism.\n\n$$\n\\text{Volume} = \\text{area of base} \\times \\text{height of the prism}\n$$\n\nStep 2: Find the area of the base of the cube. The base of a cube is a square.\n\n$$\n\\begin{align}\n\\text{Area of square} & = {s}^{2} \\\\\n& = {3}^{2} \\\\\n& = \\text{9 cm}^{2}\n\\end{align}\n$$\n\nStep 3: Multiply the area of the base by the height of the prism to find the volume.\n\n$$\n\\begin{align}\n\\text{Volume} & = \\text{area of base}\\times \\text{height of prism} \\\\\n& = 9\\times 3 \\\\\n& = \\text{27}\\text{ cm}^{3}\n\\end{align}\n$$\n\nStep 4: Write the final answer, and remember to give the correct units.\n\nThe volume of the cube is $\\text{27 cm}^{3}$.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b050",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.6 Volume of cubes and cuboids",
      "h3": "Worked example 13.10: Calculating the volume of a cuboid"
    },
    "content_text": "",
    "prompt_text": "The 3D object shown below is a cuboid. The height of the cuboid is 12 cm, the length is 13 cm, and the breadth is 6 cm. Calculate the volume of the object.\n\nThe diagram is not necessarily drawn to scale.",
    "answer_text": "Step 1: A cuboid is a prism. Write down the formula to find the volume of a prism.\n\n$$\n\\text{Volume} = \\text{area of base} \\times \\text{height of the prism}\n$$\n\nStep 2: Find the area of the base of the cuboid.\n\nThe purple rectangle at the bottom of the prism is the base of the cuboid. The purple rectangle at the bottom is the same size as the rectangle on the top.\n\n$$\n\\begin{align}\n\\text{Area of rectangle} & = l \\times b \\\\\n& = 13 \\times 6 \\\\\n& = \\text{78 cm}^{2}\n\\end{align}\n$$\n\nStep 3: Multiply the area of the base of the prism by the height of the prism to find the volume.\n\n$$\n\\begin{align}\n\\text{Volume} & = \\text{area of base}\\times \\text{height of prism} \\\\\n& = 78\\times 12 \\\\\n& = \\text{936 cm}^{3}\n\\end{align}\n$$\n\nStep 4: Write the final answer and remember to show the correct units.\n\nThe volume of the cuboid is 936 cm$^{3}$.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b051",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.6 Volume of cubes and cuboids",
      "h3": null
    },
    "content_text": "You may calculate the volume of a prism in one step, using these formulae.\n\n$$\n\\begin{align}\n\\text{Volume of a cuboid} &= \\text{area of base} \\times \\text{height of cuboid}\\\\\n&= l \\times b \\times h\n\\end{align}\n$$\n\n$$\n\\begin{align}\n\\text{Volume of a cube} &= \\text{area of base} \\times \\text{height of cube}\\\\\n&= s \\times s \\times s\n\\end{align}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b052",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.6 Volume of cubes and cuboids",
      "h3": "Exercise 13.13: Find the volume of cubes and cuboids"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.13: Find the volume of cubes and cuboids",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b052-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.6 Volume of cubes and cuboids",
      "h3": "Exercise 13.13: Find the volume of cubes and cuboids"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.13: Find the volume of cubes and cuboids\n\n1. The picture below shows a cube. The length, width and height of the cube are 5 cm. Find the volume of the cube.",
    "answer_text": "The volume of any prism is $V = \\text{area of base} \\times \\text{height of prism}$. A cube is a prism with a square as its base.\n\n$$\n\\begin{array}{ll}\n{V}_\\text{cube} & {= \\text{area of base} \\times \\text{height of cube}} \\\\\n& {= s \\times s \\times s}\\\\\n& {= 5 \\times 5 \\times 5}\\\\\n\\text{V}_{cube} & {= \\text{125 cm}^{3}} \\\\\n\\end{array}\n$$\n\nAnswer: The volume of the cube is 125 cm$^{3}$.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b052-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.6 Volume of cubes and cuboids",
      "h3": "Exercise 13.13: Find the volume of cubes and cuboids"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.13: Find the volume of cubes and cuboids\n\n2. The picture below shows a cube. The length, width and height of the cube are 30 mm. Find the volume of the cube.",
    "answer_text": "$$\n\\begin{array}{ll}\n{V}_\\text{cube} & {= s \\times s \\times s}\\\\\n& {= 30 \\times 30 \\times 30}\\\\\n& {= \\text{900} \\times \\text{30}} \\\\\n\\text{V}_{cube} & {= \\text{27,000 mm}^{3}} \\\\\n\\end{array}\n$$\n\nThe volume of the cube is 27,000 mm$^{3}$.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b052-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.6 Volume of cubes and cuboids",
      "h3": "Exercise 13.13: Find the volume of cubes and cuboids"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.13: Find the volume of cubes and cuboids\n\n3. The prism shown below is a cuboid. The height of the cuboid is 6 metres, the length is 12 metres and the breadth is 5 metres. Find the volume of the prism.",
    "answer_text": "The volume of any prism is $\\text{V = area of base} \\times \\text{height of prism}$. A cuboid is a prism with a rectangle as its base.\n\n$$\n\\begin{array}{ll}\nV_{\\text{cuboid}} & {= \\text{area of base} \\times \\text{height}} \\\\\n & {= l_{\\text{purple rectangle}} \\times b_{\\text{purple rectangle}}\\times h} \\\\\n & {= \\text{12} \\times \\text{5} \\times \\text{6}} \\\\\n & {= \\text{360}\\ {\\text{m}^{3}}} \\\\\n\\end{array}\n$$\n\nThe volume of the cuboid is 360 m$^{3}$.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b052-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.6 Volume of cubes and cuboids",
      "h3": "Exercise 13.13: Find the volume of cubes and cuboids"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.13: Find the volume of cubes and cuboids\n\n4. The prism shown below is a cuboid. The height of the cuboid is 8 cm; the length and breadth are 10 cm and 4 cm respectively. Determine the volume of the cuboid.",
    "answer_text": "$$\n\\begin{array}{ll}\nV_{\\text{cuboid}} & {= l_{\\text{purple rectangle}} \\times b_{\\text{purple rectangle}} \\times h} \\\\\n & {= \\text{10} \\times \\text{4} \\times \\text{8}} \\\\\n & {= \\text{320}\\ {\\text{cm}^{3}}} \\\\\n\\end{array}\n$$\n\nThe volume of the cuboid is 320 cm$^{3}$.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b052-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.6 Volume of cubes and cuboids",
      "h3": "Exercise 13.13: Find the volume of cubes and cuboids"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.13: Find the volume of cubes and cuboids\n\n5. The picture below shows a cube. The length, width and height of the cube are 4 metres. Find the volume of the cube.",
    "answer_text": "$$\n\\begin{array}{ll}\n{V}_\\text{cube} & {= s \\times s \\times s}\\\\\n& {= 4 \\times 4 \\times 4}\\\\\n\\text{V}_{cube} & {= \\text{64 m}^{3}} \\\\\n\\end{array}\n$$\n\nThe volume of the cube is 64 m$^{3}$.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b052-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.6 Volume of cubes and cuboids",
      "h3": "Exercise 13.13: Find the volume of cubes and cuboids"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.13: Find the volume of cubes and cuboids\n\n6. The prism below is a cuboid. The height of the cuboid is 12 mm, and the other dimensions of the cuboid are 11 mm and 8 mm. Find the volume of the cuboid.",
    "answer_text": "$$\n\\begin{array}{ll}\nV_{\\text{cuboid}} & = l \\times b \\times h \\\\\n& = \\text{11} \\times \\text{8} \\times \\text{12} \\\\\n& = \\text{1,056} \\text{ mm}^{3}\n\\end{array}\n$$\n\nThe volume of the cuboid is 1,056 mm$^{3}$.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids"
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
  "subtopic_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids",
  "subtopic_title": "Volume of cubes and cuboids",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids-po01",
        "source_performance_objective_index": 1,
        "text": "Find volume of a cube and a cuboid"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "volume-of-cubes-and-cuboids-ao-find-volume-of-cube",
          "text": "Find volume of a cube."
        },
        {
          "atomic_objective_id": "volume-of-cubes-and-cuboids-ao-find-volume-of-cuboid",
          "text": "Find volume of a cuboid."
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
    "record_id": "ch13-b048",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.6 Volume of cubes and cuboids",
      "h3": null
    },
    "content_text": "Volume is the amount of the space that a 3D object takes up. Volume is a way of measuring the size of a whole 3D object. It is measured in cubic units.\n\nWhen we measure *length*, we measure one dimension. The length of the line below is $1 \\text{ cm}$. We say the length of the line is \"1 centimetre\".\n\nWhen we measure *area*, we measure two dimensions. The square below has a length of 1 cm and a breadth (or width) of 1 cm. The area of the square is $1 \\text{ cm}^{2}$. We say the area is \"1 square centimetre\".\n\nWhen we measure *volume*, we measure three dimensions. The cube below has a length of 1 cm, a breadth of 1 cm and a height of 1 cm. The volume of the cube is $1 \\text{ cm}^{3}$. We say the volume is \"1 cubic centimetre\".\n\nWhen we calculate the volume of a container, we work out how many cubes we can pack into the container. We start by finding out how many cubes will cover the base of the container.\n\nIn the container below, it is possible to pack 6 cubes across the length of the container and 4 cubes across the breadth of the container. To find the number of cubes for one layer, we multiply the number of cubes along the length by the number of cubes along the breadth:\n\n6 × 4 = 24\n\nTo fill the whole container, we pack more layers. In the container below it is possible to pack 8 layers. This container is a prism, so each layer will have the same number of cubes. To find the total number of cubes we multiply the number of cubes in one layer by the number of layers.\n\n$$\n\\begin{align}\n\\text{Total number of cubes} &= 24 \\times 8\\\\\n&= 192 \\text{ cubes}\n\\end{align}\n$$\n\nFrom this calculation, we can see that we calculate the volume of a prism by multiplying the area of the base of the prism by the height of the prism.\n\nThe volume of a prism is calculated using this formula:\n\n$$\nV_\\text{prism} = \\text{area of base} \\times \\text{height of the prism}\n$$\n\nThis formula can be used to calculate the volume of any prism. The prism can have a triangle or a pentagon or a hexagon as its base, and this formula will still hold.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b049",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.6 Volume of cubes and cuboids",
      "h3": "Worked example 13.9: Calculating the volume of a cube"
    },
    "content_text": "",
    "prompt_text": "Find the volume of the following cube. The cube has side length 3 cm.",
    "answer_text": "Step 1: A cube is a prism. Write down the formula to find the volume of a prism.\n\n$$\n\\text{Volume} = \\text{area of base} \\times \\text{height of the prism}\n$$\n\nStep 2: Find the area of the base of the cube. The base of a cube is a square.\n\n$$\n\\begin{align}\n\\text{Area of square} & = {s}^{2} \\\\\n& = {3}^{2} \\\\\n& = \\text{9 cm}^{2}\n\\end{align}\n$$\n\nStep 3: Multiply the area of the base by the height of the prism to find the volume.\n\n$$\n\\begin{align}\n\\text{Volume} & = \\text{area of base}\\times \\text{height of prism} \\\\\n& = 9\\times 3 \\\\\n& = \\text{27}\\text{ cm}^{3}\n\\end{align}\n$$\n\nStep 4: Write the final answer, and remember to give the correct units.\n\nThe volume of the cube is $\\text{27 cm}^{3}$.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b050",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.6 Volume of cubes and cuboids",
      "h3": "Worked example 13.10: Calculating the volume of a cuboid"
    },
    "content_text": "",
    "prompt_text": "The 3D object shown below is a cuboid. The height of the cuboid is 12 cm, the length is 13 cm, and the breadth is 6 cm. Calculate the volume of the object.\n\nThe diagram is not necessarily drawn to scale.",
    "answer_text": "Step 1: A cuboid is a prism. Write down the formula to find the volume of a prism.\n\n$$\n\\text{Volume} = \\text{area of base} \\times \\text{height of the prism}\n$$\n\nStep 2: Find the area of the base of the cuboid.\n\nThe purple rectangle at the bottom of the prism is the base of the cuboid. The purple rectangle at the bottom is the same size as the rectangle on the top.\n\n$$\n\\begin{align}\n\\text{Area of rectangle} & = l \\times b \\\\\n& = 13 \\times 6 \\\\\n& = \\text{78 cm}^{2}\n\\end{align}\n$$\n\nStep 3: Multiply the area of the base of the prism by the height of the prism to find the volume.\n\n$$\n\\begin{align}\n\\text{Volume} & = \\text{area of base}\\times \\text{height of prism} \\\\\n& = 78\\times 12 \\\\\n& = \\text{936 cm}^{3}\n\\end{align}\n$$\n\nStep 4: Write the final answer and remember to show the correct units.\n\nThe volume of the cuboid is 936 cm$^{3}$.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b051",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.6 Volume of cubes and cuboids",
      "h3": null
    },
    "content_text": "You may calculate the volume of a prism in one step, using these formulae.\n\n$$\n\\begin{align}\n\\text{Volume of a cuboid} &= \\text{area of base} \\times \\text{height of cuboid}\\\\\n&= l \\times b \\times h\n\\end{align}\n$$\n\n$$\n\\begin{align}\n\\text{Volume of a cube} &= \\text{area of base} \\times \\text{height of cube}\\\\\n&= s \\times s \\times s\n\\end{align}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b052",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.6 Volume of cubes and cuboids",
      "h3": "Exercise 13.13: Find the volume of cubes and cuboids"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.13: Find the volume of cubes and cuboids",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b052-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.6 Volume of cubes and cuboids",
      "h3": "Exercise 13.13: Find the volume of cubes and cuboids"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.13: Find the volume of cubes and cuboids\n\n1. The picture below shows a cube. The length, width and height of the cube are 5 cm. Find the volume of the cube.",
    "answer_text": "The volume of any prism is $V = \\text{area of base} \\times \\text{height of prism}$. A cube is a prism with a square as its base.\n\n$$\n\\begin{array}{ll}\n{V}_\\text{cube} & {= \\text{area of base} \\times \\text{height of cube}} \\\\\n& {= s \\times s \\times s}\\\\\n& {= 5 \\times 5 \\times 5}\\\\\n\\text{V}_{cube} & {= \\text{125 cm}^{3}} \\\\\n\\end{array}\n$$\n\nAnswer: The volume of the cube is 125 cm$^{3}$.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b052-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.6 Volume of cubes and cuboids",
      "h3": "Exercise 13.13: Find the volume of cubes and cuboids"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.13: Find the volume of cubes and cuboids\n\n2. The picture below shows a cube. The length, width and height of the cube are 30 mm. Find the volume of the cube.",
    "answer_text": "$$\n\\begin{array}{ll}\n{V}_\\text{cube} & {= s \\times s \\times s}\\\\\n& {= 30 \\times 30 \\times 30}\\\\\n& {= \\text{900} \\times \\text{30}} \\\\\n\\text{V}_{cube} & {= \\text{27,000 mm}^{3}} \\\\\n\\end{array}\n$$\n\nThe volume of the cube is 27,000 mm$^{3}$.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b052-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.6 Volume of cubes and cuboids",
      "h3": "Exercise 13.13: Find the volume of cubes and cuboids"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.13: Find the volume of cubes and cuboids\n\n3. The prism shown below is a cuboid. The height of the cuboid is 6 metres, the length is 12 metres and the breadth is 5 metres. Find the volume of the prism.",
    "answer_text": "The volume of any prism is $\\text{V = area of base} \\times \\text{height of prism}$. A cuboid is a prism with a rectangle as its base.\n\n$$\n\\begin{array}{ll}\nV_{\\text{cuboid}} & {= \\text{area of base} \\times \\text{height}} \\\\\n & {= l_{\\text{purple rectangle}} \\times b_{\\text{purple rectangle}}\\times h} \\\\\n & {= \\text{12} \\times \\text{5} \\times \\text{6}} \\\\\n & {= \\text{360}\\ {\\text{m}^{3}}} \\\\\n\\end{array}\n$$\n\nThe volume of the cuboid is 360 m$^{3}$.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b052-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.6 Volume of cubes and cuboids",
      "h3": "Exercise 13.13: Find the volume of cubes and cuboids"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.13: Find the volume of cubes and cuboids\n\n4. The prism shown below is a cuboid. The height of the cuboid is 8 cm; the length and breadth are 10 cm and 4 cm respectively. Determine the volume of the cuboid.",
    "answer_text": "$$\n\\begin{array}{ll}\nV_{\\text{cuboid}} & {= l_{\\text{purple rectangle}} \\times b_{\\text{purple rectangle}} \\times h} \\\\\n & {= \\text{10} \\times \\text{4} \\times \\text{8}} \\\\\n & {= \\text{320}\\ {\\text{cm}^{3}}} \\\\\n\\end{array}\n$$\n\nThe volume of the cuboid is 320 cm$^{3}$.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b052-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.6 Volume of cubes and cuboids",
      "h3": "Exercise 13.13: Find the volume of cubes and cuboids"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.13: Find the volume of cubes and cuboids\n\n5. The picture below shows a cube. The length, width and height of the cube are 4 metres. Find the volume of the cube.",
    "answer_text": "$$\n\\begin{array}{ll}\n{V}_\\text{cube} & {= s \\times s \\times s}\\\\\n& {= 4 \\times 4 \\times 4}\\\\\n\\text{V}_{cube} & {= \\text{64 m}^{3}} \\\\\n\\end{array}\n$$\n\nThe volume of the cube is 64 m$^{3}$.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b052-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.6 Volume of cubes and cuboids",
      "h3": "Exercise 13.13: Find the volume of cubes and cuboids"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.13: Find the volume of cubes and cuboids\n\n6. The prism below is a cuboid. The height of the cuboid is 12 mm, and the other dimensions of the cuboid are 11 mm and 8 mm. Find the volume of the cuboid.",
    "answer_text": "$$\n\\begin{array}{ll}\nV_{\\text{cuboid}} & = l \\times b \\times h \\\\\n& = \\text{11} \\times \\text{8} \\times \\text{12} \\\\\n& = \\text{1,056} \\text{ mm}^{3}\n\\end{array}\n$$\n\nThe volume of the cuboid is 1,056 mm$^{3}$.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids"
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
