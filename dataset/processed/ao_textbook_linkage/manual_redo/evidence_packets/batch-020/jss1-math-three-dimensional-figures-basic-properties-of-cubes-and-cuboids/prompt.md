# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-4",
  "topic_key": "jss1-math-three-dimensional-figures",
  "topic": "Three dimensional figures",
  "subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids",
  "subtopic_title": "Basic properties of cubes and cuboids.",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids-po01",
        "source_performance_objective_index": 1,
        "text": "Identify the properties of cubes and cuboids"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cubes",
          "text": "Identify the properties of cubes."
        },
        {
          "atomic_objective_id": "basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cuboids",
          "text": "Identify the properties of cuboids."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch13-b002",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": null
    },
    "content_text": "One of the groups of 3D objects is called **prisms**. Examples of prisms are shown below.\n\nA prism has certain properties:\n\n- A prism is a type of solid (3D object) that has a **polygon** as a base.\n- The top face of a prism is exactly the same as the base of the prism.\n- The top face of a prism is parallel to the base of the prism.\n- The side faces of a prism are rectangles that are perpendicular to the base.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b003",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": null
    },
    "content_text": "**prism** A prism is a solid figure with the top and bottom faces parallel to each other. The top and bottom faces are polygons and are exactly the same. The side faces of a prism are rectangles.\n\n**polygon** A polygon is a closed flat shape with three or more straight sides.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b004",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": null
    },
    "content_text": "We are going to study the properties of two types of prisms, namely cubes and cuboids.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b005",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Cubes"
    },
    "content_text": "A cube is a 3D object that is formed by six equal squares.\n\nThere are many real-life objects in the shape of a cube. A dice is a cube. Children often play with blocks in the form of cubes. You may also have seen a box in the shape of a cube.\n\nThere are certain words that we need to use when we describe the properties of 3D objects, such as face, base, edge and vertex.\n\nThe properties of a cube are:\n\n- The flat parts of a cube are called **faces**. A cube has six faces, and each face is a square. All the squares have the same size.\n- The **base** is one of the faces. In the diagram below, the base is shaded.\n- The line where two faces meet is called an **edge**.\n- A cube has 12 edges.\n- The point where three edges meet is called a **vertex**.\n- A cube has 8 vertices.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b006",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Cubes"
    },
    "content_text": "**cube** A cube is a 3D object that is formed by six equal squares.\n\n**face** A face is a flat surface of a 3D shape.\n\n**base** The base is the flat surface at the bottom of a 3D object on which the object stands.\n\n**edge** The edge is the line where two faces meet.\n\n**vertex** The vertex is a point where three edges meet. The plural of vertex is vertices.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b007",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Cubes"
    },
    "content_text": "A cube is a prism, because the base and top face are squares, and a square is a polygon. The side faces of a cube are also squares, which are a special type of rectangle. The side faces are perpendicular to the base of the cube.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b008",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Worked example 13.1: Identifying the parts of a cube"
    },
    "content_text": "",
    "prompt_text": "Consider the cube given below.\n\n1. What is the shaded area labelled $A$ called?\n2. What is the point labelled $B$ (in the first diagram) called?\n3. What is the line labelled $CD$ called?",
    "answer_text": "Question 1\n\nStep 1: Recall the properties of a cube.\n\nA cube is formed by six squares, called faces.\nThe faces of a cube meet each other at an edge.\nThe edges of a cube meet each other at a vertex.\n\nStep 2: Identify the shaded part and give the correct answer.\n\nThe shaded area labelled $A$ is a face of the cube.\n\nQuestion 2\n\nStep 1: Recall the properties of a cube.\n\nA cube is formed by six squares, called faces.\nThe faces of a cube meet each other at an edge.\nThe edges of a cube meet each other at a vertex.\n\nStep 2: Identify the point labelled $B$ and give the correct answer.\n\nThe point labelled $B$ is a vertex of the cube.\n\nQuestion 3\n\nStep 1: Recall the properties of a cube.\n\nA cube is formed by six squares, called faces.\nThe faces of a cube meet each other at an edge.\nThe edges of a cube meet each other at a vertex.\n\nStep 2: Identify the line labelled $CD$ and give the correct answer.\n\nLine $CD$ is an edge of the cube.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b009",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Worked example 13.2: Describing the properties of a cube"
    },
    "content_text": "",
    "prompt_text": "Consider the 3D object given below.\n\n1. How many faces does a cube have?\n2. What is the shape of the faces of a cube?\n3. How many edges does a cube have?\n4. How many vertices does a cube have?",
    "answer_text": "Question 1\n\nStep 1: Recall what the face of a cube is.\n\nThe flat parts of a cube are called faces. A cube has six faces and each face is a square.\n\nStep 2: Visualise a cube and give the correct answer.\n\nA cube has 6 faces.\n\nQuestion 2\n\nStep 1: Recall the properties of a cube.\n\nA cube has 6 faces and each face is a square. All the squares have the same size.\n\nStep 2: Give the correct answer.\n\nAll the faces of a cube are squares.\n\nQuestion 3\n\nStep 1: Recall what the edge of a cube is.\n\nThe faces of a cube meet each other at an edge.\n\nStep 2: Visualise a cube and give the correct answer.\n\nA cube has 12 edges.\n\nQuestion 4\n\nStep 1: Recall what the vertices of a cube are.\n\nThe edges of a cube meet each other at a vertex.\n\nStep 2: Visualise a cube and give the correct answer.\n\nA cube has 8 vertices.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b010",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.1: Identify the parts of a cube"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.1: Identify the parts of a cube\n\nConsider the diagram of the 3D object below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-011.png]",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b010-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.1: Identify the parts of a cube"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.1: Identify the parts of a cube\n\nConsider the diagram of the 3D object below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-011.png]\n\n1. What is the name of the 3D object?",
    "answer_text": "The 3D object is a cube.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b010-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.1: Identify the parts of a cube"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.1: Identify the parts of a cube\n\nConsider the diagram of the 3D object below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-011.png]\n\n2. What is the name of the shaded area labelled $A$?",
    "answer_text": "The shaded area labelled $A$ is a face of the cube.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b010-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.1: Identify the parts of a cube"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.1: Identify the parts of a cube\n\nConsider the diagram of the 3D object below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-011.png]\n\n3. What shape is the shaded area labelled $A$?",
    "answer_text": "Each face of a cube is a square, so the shaded area labelled $A$ is a face of a cube.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b010-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.1: Identify the parts of a cube"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.1: Identify the parts of a cube\n\nConsider the diagram of the 3D object below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-011.png]\n\n4. What is the name of the line labelled $BC$?",
    "answer_text": "The line $BC$ is an edge of the cube. The faces of a cube meet each other at an edge.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b010-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.1: Identify the parts of a cube"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.1: Identify the parts of a cube\n\nConsider the diagram of the 3D object below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-011.png]\n\n5. What is the name of the point labelled $D$?",
    "answer_text": "The point $D$ is a vertex of the cube. The edges of a cube meet each other at a vertex.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b011",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.2: Describe the properties of a cube"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.2: Describe the properties of a cube",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b011-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.2: Describe the properties of a cube"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.2: Describe the properties of a cube\n\n1. Select a word from Column B that best fits the description in Column A. Write down only the number for the description in Column A, and the capital letter that gives the correct answer from Column B.\n\n| Column A | Column B |\n| --- | --- |\n| a) The six squares that form the flat parts of a cube. | A edges |\n| b) The lines where two faces of a cube meet each other. | B vertices |\n| c) The points where the edges of a cube meet each other. | C faces |",
    "answer_text": "a) C\nb) A\nc) B",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b011-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.2: Describe the properties of a cube"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.2: Describe the properties of a cube\n\n2. Complete the table given below.\n\n**Properties of a cube**\n\n| Number and shape of faces | Number of edges | Number of vertices |\n| --- | --- | --- |\n|  |  |  |",
    "answer_text": "**Properties of a cube**\n\n| Number and shape of faces | Number of edges | Number of vertices |\n| --- | --- | --- |\n| 6 squares | 12 edges | 8 vertices |",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b012",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Cuboids"
    },
    "content_text": "A **cuboid** is formed by three pairs of rectangles. Each pair of rectangles is opposite each other and equal in size.\n\nThere are many real life objects in the shape of a cuboid, such as those shown in the examples below. A brick is a cuboid. When you buy new shoes in a box, the shoe box is in the shape of a cuboid. Many different foods, for example, breakfast cereals, are sold in boxes in the shape of cuboids.\n\nThe properties of a cuboid are:\n\n- A cuboid has six *faces* and each face is a rectangle. The two faces that are opposite each other are equal. So a cuboid has three pairs of equal rectangles.\n- Two faces of a cuboid meet each other at an *edge*. A cuboid has twelve edges: four edges around the top face of the cuboid, four edges around the side faces, and four edges around the base of the cuboid.\n- The edges of a cuboid meet each other at a *vertex*. A cuboid has eight vertices: four at the top of the cuboid and four at the base of the cuboid.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b013",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Cuboids"
    },
    "content_text": "Remember that vertices is the plural of vertex. So we refer to one vertex and eight vertices.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b014",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Cuboids"
    },
    "content_text": "**cuboid** A cuboid is a prism formed by three pairs of rectangles. The rectangles opposite each other are equal to each other.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b015",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Cuboids"
    },
    "content_text": "A cuboid is a prism, because it has a rectangle as a base and a rectangle is a polygon. The side faces of a cuboid are rectangles that are perpendicular to the base of the cuboid.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b016",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Worked example 13.3: Identifying the parts of a cuboid"
    },
    "content_text": "",
    "prompt_text": "Consider the cuboid given below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-022.png]\n\nQuestion 1: What is the shaded area labelled $D$ called?\n\nQuestion 2: What is the line labelled $EF$ called?\n\nQuestion 3: What is the point labelled $G$ called?",
    "answer_text": "Question 1\n\nStep 1: Recall the properties of a cuboid.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-023.png]\n\nA cuboid is formed by three pairs of equal rectangles, called faces. Opposite faces are equal.  \nThe faces of a cuboid meet each other at an edge.  \nThe edges of a cuboid meet each other at a vertex.\n\nStep 2: Identify the shaded part and give the correct answer.\n\nThe shaded area labelled $D$ is a face of the cuboid.\n\nQuestion 2\n\nStep 1: Recall the properties of a cuboid.\n\nA cuboid is formed by three pairs of equal rectangles, called faces. Opposite faces are equal.  \nThe faces of a cuboid meet each other at an edge.  \nThe edges of a cuboid meet each other at a vertex.\n\nStep 2: Identify the line labelled $EF$ and give the correct answer.\n\nLine $EF$ is an edge of the cuboid.\n\nQuestion 3\n\nStep 1: Recall the properties of a cuboid.\n\nA cuboid is formed by three pairs of equal rectangles, called faces. Opposite faces are equal.  \nThe faces of a cuboid meet each other at an edge.  \nThe edges of a cuboid meet each other at a vertex.\n\nStep 2: Identify the point labelled $G$ and give the correct answer.\n\nPoint $G$ is a vertex of the cuboid.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b017",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Worked example 13.4: Describing the properties of a cuboid"
    },
    "content_text": "",
    "prompt_text": "Consider the 3D object given below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-013.png]\n\nQuestion 1: How many faces does a cuboid have?\n\nQuestion 2: What are the shapes of the faces of a cuboid?\n\nQuestion 3: How many edges does a cuboid have?\n\nQuestion 4: How many vertices does a cuboid have?",
    "answer_text": "Question 1\n\nStep 1: Recall what the face of a cuboid is.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-019.png]\n\nThe flat parts of a cuboid are called faces.  \nA cuboid is formed by three pairs of equal rectangles. The opposite faces of a cuboid are equal.\n\nStep 2: Visualise a cuboid and give the correct answer.\n\nA cuboid has 6 faces.\n\nQuestion 2\n\nStep 1: Recall the properties of a cuboid.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-023.png]\n\nA cuboid is formed by three pairs of equal rectangles.\n\nStep 2. Give the correct answer.\n\nAll the faces of a cuboid are rectangles.\n\nQuestion 3\n\nStep 1: Recall what the edge of a cuboid is.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-020.png]\n\nThe faces of a cuboid meet each other at an edge.\n\nStep 2: Visualise a cuboid and give the correct answer.\n\nA cuboid has 12 edges.\n\nQuestion 4\n\nStep 1: Recall what the vertices of a cuboid are.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-021.png]\n\nThe edges of a cuboid meet each other at a vertex.\n\nStep 2: Visualise a cuboid and give the correct answer.\n\nA cuboid has 8 vertices.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b018",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.3: Describe the parts of a cuboid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.3: Describe the parts of a cuboid\n\nConsider the diagram of 3D object below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-022.png]",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b018-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.3: Describe the parts of a cuboid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.3: Describe the parts of a cuboid\n\nConsider the diagram of 3D object below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-022.png]\n\n1. What is the name of the 3D object?",
    "answer_text": "The 3D object is a cuboid.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b018-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.3: Describe the parts of a cuboid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.3: Describe the parts of a cuboid\n\nConsider the diagram of 3D object below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-022.png]\n\n2. What part of the 3D object is shaded and labelled $D$?",
    "answer_text": "The shaded area is a face of the cuboid.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b018-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.3: Describe the parts of a cuboid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.3: Describe the parts of a cuboid\n\nConsider the diagram of 3D object below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-022.png]\n\n3. What shape is the shaded area labelled $D$?",
    "answer_text": "Each face of a cuboid is a rectangle, so the shaded area is a rectangle.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b018-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.3: Describe the parts of a cuboid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.3: Describe the parts of a cuboid\n\nConsider the diagram of 3D object below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-022.png]\n\n4. Name and describe the line labelled $EG$.",
    "answer_text": "The line $EG$ is an edge of the cuboid. The faces of a cuboid meet each other at an edge.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b018-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.3: Describe the parts of a cuboid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.3: Describe the parts of a cuboid\n\nConsider the diagram of 3D object below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-022.png]\n\n5. Name and describe the point labelled $F$?",
    "answer_text": "The point $F$ is a vertex of the cuboid. The edges of a cuboid meet each other at a vertex.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b019",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.4: Describe the properties of a cuboid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.4: Describe the properties of a cuboid",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b019-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.4: Describe the properties of a cuboid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.4: Describe the properties of a cuboid\n\n1. Select a word from Column B that best fits the description in Column A. Write down only the number for the description in Column A, and the capital letter that gives the correct answer from Column B.\n\n| Column A | Column B |\n\n| --- | --- |\n\n| a) The three pairs of equal rectangles that form the flat parts of a cuboid. | A vertices |\n\n| b) The lines where the faces of a cuboid meet each other. | B faces |\n\n| c) The points where the edges of a cuboid meet each other. | C edges |",
    "answer_text": "a) B\nb) C\nc) A",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b019-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.4: Describe the properties of a cuboid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.4: Describe the properties of a cuboid\n\n2. Complete the table given below.\n\n**Properties of a cuboid**\n\n| Number and shape of faces | Number of edges | Number of vertices |\n\n| --- | --- | --- |\n\n|  |  |  |",
    "answer_text": "**Properties of a cuboid**\n\n| Number and shape of faces | Number of edges | Number of vertices |\n\n| --- | --- | --- |\n\n| 6 rectangles | 12 edges | 8 vertices |",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
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
  "subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids",
  "subtopic_title": "Basic properties of cubes and cuboids.",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids-po01",
        "source_performance_objective_index": 1,
        "text": "Identify the properties of cubes and cuboids"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cubes",
          "text": "Identify the properties of cubes."
        },
        {
          "atomic_objective_id": "basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cuboids",
          "text": "Identify the properties of cuboids."
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
    "record_id": "ch13-b002",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": null
    },
    "content_text": "One of the groups of 3D objects is called **prisms**. Examples of prisms are shown below.\n\nA prism has certain properties:\n\n- A prism is a type of solid (3D object) that has a **polygon** as a base.\n- The top face of a prism is exactly the same as the base of the prism.\n- The top face of a prism is parallel to the base of the prism.\n- The side faces of a prism are rectangles that are perpendicular to the base.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b003",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": null
    },
    "content_text": "**prism** A prism is a solid figure with the top and bottom faces parallel to each other. The top and bottom faces are polygons and are exactly the same. The side faces of a prism are rectangles.\n\n**polygon** A polygon is a closed flat shape with three or more straight sides.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b004",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": null
    },
    "content_text": "We are going to study the properties of two types of prisms, namely cubes and cuboids.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b005",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Cubes"
    },
    "content_text": "A cube is a 3D object that is formed by six equal squares.\n\nThere are many real-life objects in the shape of a cube. A dice is a cube. Children often play with blocks in the form of cubes. You may also have seen a box in the shape of a cube.\n\nThere are certain words that we need to use when we describe the properties of 3D objects, such as face, base, edge and vertex.\n\nThe properties of a cube are:\n\n- The flat parts of a cube are called **faces**. A cube has six faces, and each face is a square. All the squares have the same size.\n- The **base** is one of the faces. In the diagram below, the base is shaded.\n- The line where two faces meet is called an **edge**.\n- A cube has 12 edges.\n- The point where three edges meet is called a **vertex**.\n- A cube has 8 vertices.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b006",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Cubes"
    },
    "content_text": "**cube** A cube is a 3D object that is formed by six equal squares.\n\n**face** A face is a flat surface of a 3D shape.\n\n**base** The base is the flat surface at the bottom of a 3D object on which the object stands.\n\n**edge** The edge is the line where two faces meet.\n\n**vertex** The vertex is a point where three edges meet. The plural of vertex is vertices.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b007",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Cubes"
    },
    "content_text": "A cube is a prism, because the base and top face are squares, and a square is a polygon. The side faces of a cube are also squares, which are a special type of rectangle. The side faces are perpendicular to the base of the cube.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b008",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Worked example 13.1: Identifying the parts of a cube"
    },
    "content_text": "",
    "prompt_text": "Consider the cube given below.\n\n1. What is the shaded area labelled $A$ called?\n2. What is the point labelled $B$ (in the first diagram) called?\n3. What is the line labelled $CD$ called?",
    "answer_text": "Question 1\n\nStep 1: Recall the properties of a cube.\n\nA cube is formed by six squares, called faces.\nThe faces of a cube meet each other at an edge.\nThe edges of a cube meet each other at a vertex.\n\nStep 2: Identify the shaded part and give the correct answer.\n\nThe shaded area labelled $A$ is a face of the cube.\n\nQuestion 2\n\nStep 1: Recall the properties of a cube.\n\nA cube is formed by six squares, called faces.\nThe faces of a cube meet each other at an edge.\nThe edges of a cube meet each other at a vertex.\n\nStep 2: Identify the point labelled $B$ and give the correct answer.\n\nThe point labelled $B$ is a vertex of the cube.\n\nQuestion 3\n\nStep 1: Recall the properties of a cube.\n\nA cube is formed by six squares, called faces.\nThe faces of a cube meet each other at an edge.\nThe edges of a cube meet each other at a vertex.\n\nStep 2: Identify the line labelled $CD$ and give the correct answer.\n\nLine $CD$ is an edge of the cube.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b009",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Worked example 13.2: Describing the properties of a cube"
    },
    "content_text": "",
    "prompt_text": "Consider the 3D object given below.\n\n1. How many faces does a cube have?\n2. What is the shape of the faces of a cube?\n3. How many edges does a cube have?\n4. How many vertices does a cube have?",
    "answer_text": "Question 1\n\nStep 1: Recall what the face of a cube is.\n\nThe flat parts of a cube are called faces. A cube has six faces and each face is a square.\n\nStep 2: Visualise a cube and give the correct answer.\n\nA cube has 6 faces.\n\nQuestion 2\n\nStep 1: Recall the properties of a cube.\n\nA cube has 6 faces and each face is a square. All the squares have the same size.\n\nStep 2: Give the correct answer.\n\nAll the faces of a cube are squares.\n\nQuestion 3\n\nStep 1: Recall what the edge of a cube is.\n\nThe faces of a cube meet each other at an edge.\n\nStep 2: Visualise a cube and give the correct answer.\n\nA cube has 12 edges.\n\nQuestion 4\n\nStep 1: Recall what the vertices of a cube are.\n\nThe edges of a cube meet each other at a vertex.\n\nStep 2: Visualise a cube and give the correct answer.\n\nA cube has 8 vertices.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b010",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.1: Identify the parts of a cube"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.1: Identify the parts of a cube\n\nConsider the diagram of the 3D object below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-011.png]",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b010-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.1: Identify the parts of a cube"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.1: Identify the parts of a cube\n\nConsider the diagram of the 3D object below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-011.png]\n\n1. What is the name of the 3D object?",
    "answer_text": "The 3D object is a cube.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b010-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.1: Identify the parts of a cube"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.1: Identify the parts of a cube\n\nConsider the diagram of the 3D object below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-011.png]\n\n2. What is the name of the shaded area labelled $A$?",
    "answer_text": "The shaded area labelled $A$ is a face of the cube.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b010-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.1: Identify the parts of a cube"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.1: Identify the parts of a cube\n\nConsider the diagram of the 3D object below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-011.png]\n\n3. What shape is the shaded area labelled $A$?",
    "answer_text": "Each face of a cube is a square, so the shaded area labelled $A$ is a face of a cube.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b010-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.1: Identify the parts of a cube"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.1: Identify the parts of a cube\n\nConsider the diagram of the 3D object below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-011.png]\n\n4. What is the name of the line labelled $BC$?",
    "answer_text": "The line $BC$ is an edge of the cube. The faces of a cube meet each other at an edge.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b010-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.1: Identify the parts of a cube"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.1: Identify the parts of a cube\n\nConsider the diagram of the 3D object below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-011.png]\n\n5. What is the name of the point labelled $D$?",
    "answer_text": "The point $D$ is a vertex of the cube. The edges of a cube meet each other at a vertex.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b011",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.2: Describe the properties of a cube"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.2: Describe the properties of a cube",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b011-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.2: Describe the properties of a cube"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.2: Describe the properties of a cube\n\n1. Select a word from Column B that best fits the description in Column A. Write down only the number for the description in Column A, and the capital letter that gives the correct answer from Column B.\n\n| Column A | Column B |\n| --- | --- |\n| a) The six squares that form the flat parts of a cube. | A edges |\n| b) The lines where two faces of a cube meet each other. | B vertices |\n| c) The points where the edges of a cube meet each other. | C faces |",
    "answer_text": "a) C\nb) A\nc) B",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b011-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.2: Describe the properties of a cube"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.2: Describe the properties of a cube\n\n2. Complete the table given below.\n\n**Properties of a cube**\n\n| Number and shape of faces | Number of edges | Number of vertices |\n| --- | --- | --- |\n|  |  |  |",
    "answer_text": "**Properties of a cube**\n\n| Number and shape of faces | Number of edges | Number of vertices |\n| --- | --- | --- |\n| 6 squares | 12 edges | 8 vertices |",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b012",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Cuboids"
    },
    "content_text": "A **cuboid** is formed by three pairs of rectangles. Each pair of rectangles is opposite each other and equal in size.\n\nThere are many real life objects in the shape of a cuboid, such as those shown in the examples below. A brick is a cuboid. When you buy new shoes in a box, the shoe box is in the shape of a cuboid. Many different foods, for example, breakfast cereals, are sold in boxes in the shape of cuboids.\n\nThe properties of a cuboid are:\n\n- A cuboid has six *faces* and each face is a rectangle. The two faces that are opposite each other are equal. So a cuboid has three pairs of equal rectangles.\n- Two faces of a cuboid meet each other at an *edge*. A cuboid has twelve edges: four edges around the top face of the cuboid, four edges around the side faces, and four edges around the base of the cuboid.\n- The edges of a cuboid meet each other at a *vertex*. A cuboid has eight vertices: four at the top of the cuboid and four at the base of the cuboid.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b013",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Cuboids"
    },
    "content_text": "Remember that vertices is the plural of vertex. So we refer to one vertex and eight vertices.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b014",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Cuboids"
    },
    "content_text": "**cuboid** A cuboid is a prism formed by three pairs of rectangles. The rectangles opposite each other are equal to each other.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b015",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Cuboids"
    },
    "content_text": "A cuboid is a prism, because it has a rectangle as a base and a rectangle is a polygon. The side faces of a cuboid are rectangles that are perpendicular to the base of the cuboid.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b016",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Worked example 13.3: Identifying the parts of a cuboid"
    },
    "content_text": "",
    "prompt_text": "Consider the cuboid given below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-022.png]\n\nQuestion 1: What is the shaded area labelled $D$ called?\n\nQuestion 2: What is the line labelled $EF$ called?\n\nQuestion 3: What is the point labelled $G$ called?",
    "answer_text": "Question 1\n\nStep 1: Recall the properties of a cuboid.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-023.png]\n\nA cuboid is formed by three pairs of equal rectangles, called faces. Opposite faces are equal.  \nThe faces of a cuboid meet each other at an edge.  \nThe edges of a cuboid meet each other at a vertex.\n\nStep 2: Identify the shaded part and give the correct answer.\n\nThe shaded area labelled $D$ is a face of the cuboid.\n\nQuestion 2\n\nStep 1: Recall the properties of a cuboid.\n\nA cuboid is formed by three pairs of equal rectangles, called faces. Opposite faces are equal.  \nThe faces of a cuboid meet each other at an edge.  \nThe edges of a cuboid meet each other at a vertex.\n\nStep 2: Identify the line labelled $EF$ and give the correct answer.\n\nLine $EF$ is an edge of the cuboid.\n\nQuestion 3\n\nStep 1: Recall the properties of a cuboid.\n\nA cuboid is formed by three pairs of equal rectangles, called faces. Opposite faces are equal.  \nThe faces of a cuboid meet each other at an edge.  \nThe edges of a cuboid meet each other at a vertex.\n\nStep 2: Identify the point labelled $G$ and give the correct answer.\n\nPoint $G$ is a vertex of the cuboid.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b017",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Worked example 13.4: Describing the properties of a cuboid"
    },
    "content_text": "",
    "prompt_text": "Consider the 3D object given below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-013.png]\n\nQuestion 1: How many faces does a cuboid have?\n\nQuestion 2: What are the shapes of the faces of a cuboid?\n\nQuestion 3: How many edges does a cuboid have?\n\nQuestion 4: How many vertices does a cuboid have?",
    "answer_text": "Question 1\n\nStep 1: Recall what the face of a cuboid is.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-019.png]\n\nThe flat parts of a cuboid are called faces.  \nA cuboid is formed by three pairs of equal rectangles. The opposite faces of a cuboid are equal.\n\nStep 2: Visualise a cuboid and give the correct answer.\n\nA cuboid has 6 faces.\n\nQuestion 2\n\nStep 1: Recall the properties of a cuboid.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-023.png]\n\nA cuboid is formed by three pairs of equal rectangles.\n\nStep 2. Give the correct answer.\n\nAll the faces of a cuboid are rectangles.\n\nQuestion 3\n\nStep 1: Recall what the edge of a cuboid is.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-020.png]\n\nThe faces of a cuboid meet each other at an edge.\n\nStep 2: Visualise a cuboid and give the correct answer.\n\nA cuboid has 12 edges.\n\nQuestion 4\n\nStep 1: Recall what the vertices of a cuboid are.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-021.png]\n\nThe edges of a cuboid meet each other at a vertex.\n\nStep 2: Visualise a cuboid and give the correct answer.\n\nA cuboid has 8 vertices.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b018",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.3: Describe the parts of a cuboid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.3: Describe the parts of a cuboid\n\nConsider the diagram of 3D object below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-022.png]",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b018-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.3: Describe the parts of a cuboid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.3: Describe the parts of a cuboid\n\nConsider the diagram of 3D object below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-022.png]\n\n1. What is the name of the 3D object?",
    "answer_text": "The 3D object is a cuboid.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b018-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.3: Describe the parts of a cuboid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.3: Describe the parts of a cuboid\n\nConsider the diagram of 3D object below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-022.png]\n\n2. What part of the 3D object is shaded and labelled $D$?",
    "answer_text": "The shaded area is a face of the cuboid.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b018-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.3: Describe the parts of a cuboid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.3: Describe the parts of a cuboid\n\nConsider the diagram of 3D object below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-022.png]\n\n3. What shape is the shaded area labelled $D$?",
    "answer_text": "Each face of a cuboid is a rectangle, so the shaded area is a rectangle.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b018-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.3: Describe the parts of a cuboid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.3: Describe the parts of a cuboid\n\nConsider the diagram of 3D object below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-022.png]\n\n4. Name and describe the line labelled $EG$.",
    "answer_text": "The line $EG$ is an edge of the cuboid. The faces of a cuboid meet each other at an edge.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b018-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.3: Describe the parts of a cuboid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.3: Describe the parts of a cuboid\n\nConsider the diagram of 3D object below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-022.png]\n\n5. Name and describe the point labelled $F$?",
    "answer_text": "The point $F$ is a vertex of the cuboid. The edges of a cuboid meet each other at a vertex.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b019",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.4: Describe the properties of a cuboid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.4: Describe the properties of a cuboid",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b019-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.4: Describe the properties of a cuboid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.4: Describe the properties of a cuboid\n\n1. Select a word from Column B that best fits the description in Column A. Write down only the number for the description in Column A, and the capital letter that gives the correct answer from Column B.\n\n| Column A | Column B |\n\n| --- | --- |\n\n| a) The three pairs of equal rectangles that form the flat parts of a cuboid. | A vertices |\n\n| b) The lines where the faces of a cuboid meet each other. | B faces |\n\n| c) The points where the edges of a cuboid meet each other. | C edges |",
    "answer_text": "a) B\nb) C\nc) A",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
  },
  {
    "record_id": "ch13-b019-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.1 Cubes and cuboids",
      "h3": "Exercise 13.4: Describe the properties of a cuboid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.4: Describe the properties of a cuboid\n\n2. Complete the table given below.\n\n**Properties of a cuboid**\n\n| Number and shape of faces | Number of edges | Number of vertices |\n\n| --- | --- | --- |\n\n|  |  |  |",
    "answer_text": "**Properties of a cuboid**\n\n| Number and shape of faces | Number of edges | Number of vertices |\n\n| --- | --- | --- |\n\n| 6 rectangles | 12 edges | 8 vertices |",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids"
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
