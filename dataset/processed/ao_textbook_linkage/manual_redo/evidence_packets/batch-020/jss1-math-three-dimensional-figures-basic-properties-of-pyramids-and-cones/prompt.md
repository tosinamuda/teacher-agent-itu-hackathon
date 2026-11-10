# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-4",
  "topic_key": "jss1-math-three-dimensional-figures",
  "topic": "Three dimensional figures",
  "subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones",
  "subtopic_title": "Basic properties of pyramids and cones.",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones-po01",
        "source_performance_objective_index": 1,
        "text": "Identify the properties of pyramids and cones"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "basic-properties-of-pyramids-and-cones-ao-identify-properties-of-pyramids",
          "text": "Identify the properties of pyramids."
        },
        {
          "atomic_objective_id": "basic-properties-of-pyramids-and-cones-ao-identify-properties-of-cones",
          "text": "Identify the properties of cones."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch13-b020",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": null
    },
    "content_text": "A **pyramid** is an object that has a polygon as its base and sides that **converge** (meet each other) at one single point. The sides are *not* perpendicular to the base.\n\nThere are many real life objects in the form of a pyramid. The pyramids of Egypt are well known.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-024.png]\n\nA pile of eggs can be stacked in a pyramid.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-025.png]\n\nThe roof of a house can be in the shape of a pyramid.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-026.png]\n\nA pyramid can have any polygon, for example a rectangle, a pentagon, or a hexagon, as its base.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-027.png]\n\nWe will focus on a pyramid that has a square as its base.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-028.png]\n\nThe properties of a pyramid are:\n\n- A square-based pyramid has five *faces*.\n\n- A square-based pyramid has a square as a *base*.\n\n- The side faces are four equal isosceles triangles.\n\n- The faces of a pyramid meet each other at an *edge*.\n\n- A square-based pyramid has eight edges: four around the base and four formed by the triangular side faces.\n\n- The edges of a pyramid meet each other at a *vertex*.\n\n- A square-based pyramid has five vertices: four at the base and one at the top where the triangles meet each other.\n\nThe top vertex has a special name. The edges of the triangles that form the side faces converge at a vertex called the **apex**.\n\nWe call a pyramid a \"right pyramid\" if the line between the apex and the centre of the base is perpendicular to the base.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b021",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": null
    },
    "content_text": "**pyramid** A pyramid is a 3D object that has a polygon as its base. The side faces are triangles that meet each other at one single point, the apex.\n\n**converge** To converge is to move towards each other and to meet at one point.\n\n**apex** The apex is the top-most point that is furthest from the base of a 3D object.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b022",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": null
    },
    "content_text": "A pyramid is NOT a prism, because the side faces are not rectangles and the side faces are not perpendicular to the base.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b023",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": "Worked example 13.5: Describing the parts of a pyramid"
    },
    "content_text": "",
    "prompt_text": "Consider the square-based pyramid given below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-033.png]\n\nQuestion 1: What is the name of the shaded area labelled $P$?\n\nQuestion 2: What is the shape of the base of this pyramid?\n\nQuestion 3: What is the shape of the side faces of the pyramid?\n\nQuestion 4: What is the name of the line labelled $QR$?\n\nQuestion 5: What is the name of the point labelled $S$?\n\nQuestion 6: What is the special name of the point labelled $Q$?",
    "answer_text": "Question 1\n\nStep 1: Recall the properties of a pyramid.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-034.png]\n\nStep 2: Identify the shaded area and give the correct answer.\n\nThe shaded area is a face of the pyramid.\n\nQuestion 2\n\nStep 1: Identify the shape of the base of the pyramid and give the correct answer.\n\nThe base of the pyramid is a square.\n\nQuestion 3\n\nStep 1: Identify the shape of the side faces and give the correct answer.\n\nThe side faces are triangles.\n\nQuestion 4\n\nStep 1: Recall the properties of a pyramid.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-034.png]\n\nStep 2: Identify the line labelled $QR$ and give the correct answer.\n\nThe line labelled $QR$ is an edge of the pyramid.\n\nQuestion 5\n\nStep 1: Recall the properties of a pyramid.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-034.png]\n\nStep 2: Identify the point labelled $S$ and give the correct answer.\n\nThe point labelled $S$ is a vertex of the pyramid.\n\nQuestion 6\n\nStep 1: Recall the properties of a pyramid.\n\nThe top vertex has a special name. The edges of the triangles that form the side faces converge at a vertex called the apex.\n\nStep 2: Identify the point labelled $Q$ and give the correct answer.\n\nThe point labelled $Q$ is the apex of the pyramid.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b024",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": "Exercise 13.5: Identify the parts of a pyramid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.5: Identify the parts of a pyramid\n\nConsider the 3D object given below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-028.png]",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b024-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": "Exercise 13.5: Identify the parts of a pyramid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.5: Identify the parts of a pyramid\n\nConsider the 3D object given below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-028.png]\n\n1. What is the name of the 3D object?",
    "answer_text": "The 3D object is a pyramid. The base of this pyramid is a square, so it is a square-based pyramid.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b024-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": "Exercise 13.5: Identify the parts of a pyramid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.5: Identify the parts of a pyramid\n\nConsider the 3D object given below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-028.png]\n\n2. How many faces does the object have?",
    "answer_text": "The object (a pyramid) has one base and four side faces, so the pyramid has five faces.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b024-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": "Exercise 13.5: Identify the parts of a pyramid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.5: Identify the parts of a pyramid\n\nConsider the 3D object given below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-028.png]\n\n3. What are the shapes of the faces?",
    "answer_text": "The base is a square and the side faces are triangles.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b024-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": "Exercise 13.5: Identify the parts of a pyramid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.5: Identify the parts of a pyramid\n\nConsider the 3D object given below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-028.png]\n\n4. How many edges does the pyramid have?",
    "answer_text": "The pyramid has 8 edges.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b024-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": "Exercise 13.5: Identify the parts of a pyramid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.5: Identify the parts of a pyramid\n\nConsider the 3D object given below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-028.png]\n\n5. How many vertices does the pyramid have?",
    "answer_text": "The pyramid has 5 vertices.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b024-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": "Exercise 13.5: Identify the parts of a pyramid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.5: Identify the parts of a pyramid\n\nConsider the 3D object given below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-028.png]\n\n6. What is the name of the one point where all the triangles meet each other?",
    "answer_text": "The special vertex at the top is called the apex.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b025",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": "Exercise 13.6: Describe the properties of a pyramid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.6: Describe the properties of a pyramid",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b025-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": "Exercise 13.6: Describe the properties of a pyramid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.6: Describe the properties of a pyramid\n\n1. Select a word from Column B that best fits the description in Column A.\n\n| Column A | Column B |\n\n| --- | --- |\n\n| a) The base and triangles that form the flat parts of a pyramid. | A vertices |\n\n| b) The lines where the faces of a pyramid meet each other. | B apex |\n\n| c) The points where the edges of a pyramid meet each other. | C edges |\n\n| d) The special point where all the side faces meet each other. | D faces |",
    "answer_text": "a) D\nb) C\nc) A\nd) B",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b025-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": "Exercise 13.6: Describe the properties of a pyramid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.6: Describe the properties of a pyramid\n\n2. Complete the table given below.\n\n**Properties of a square-based pyramid**\n\n| Number and shape of faces | Number of edges | Number of vertices |\n\n| --- | --- | --- |\n\n|  |  |  |",
    "answer_text": "**Properties of a square-based pyramid**\n\n| Number and shape of faces | Number of edges | Number of vertices |\n\n| --- | --- | --- |\n\n| 1 square and 4 triangles | 8 edges | 5 vertices |",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b026",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": null
    },
    "content_text": "A **cone** is another example of a 3D object that has an apex.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-035.png]\n\nThere are many examples of cones in real life.\n\nWe can buy ice cream in a cone. The part of the ice cream that you hold in your hand is the cone.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-036.png]",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b027",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": null
    },
    "content_text": "The round ball of ice cream that you eat is a sphere. You will study the properties of a sphere later in this chapter.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b028",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": null
    },
    "content_text": "We can make a party hat in the form of a cone.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-037.png]\n\nThe roof of a house can be in the form of a cone.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-038.png]",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b029",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": null
    },
    "content_text": "The circular walls of the round houses are cylinders. You will study the properties of a cylinder later in this chapter.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b030",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": null
    },
    "content_text": "The properties of a cone are:\n\n- A cone has two *faces*. One of the faces is flat and the other face is curved.\n- The *base* of a cone is a flat circle.\n- [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-039.png]\n- A cone has only one side face, and this face is curved.\n- Draw a circle and cut it out. Then cut out a \"slice\" (a sector) of the circle as shown below.\n- [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-040.png]\n- Curl the paper around so that $AB$ fits onto $AC$. You are now holding the curved face of a cone in your hand. Although this face is curved, it can be laid flat, so it is still a face.\n- A cone has only one *edge*. The edge of a cone is not a straight line; it is a curve.\n- [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-041.png]\n- The edge of a cone is the circumference of the circle that forms the base of the cone.\n- A cone has only one *vertex*.\n- The vertex of a cone is at the top of the cone.\n- [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-042.png]\n\nThe one vertex of a cone is also called the *apex* of the cone. From the base, the curved face becomes narrower until it forms a point at the top, which is the apex.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b031",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": null
    },
    "content_text": "**cone** A cone is a 3D object with a circle as its base. A cone has one curved side face that comes to a point, the apex.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b032",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": null
    },
    "content_text": "A cone is NOT a prism: a cone has a circle as its base, and a circle is not a polygon. A prism has a polygon as a base.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b033",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": "Worked example 13.6: Identifying the parts of a cone"
    },
    "content_text": "",
    "prompt_text": "Consider the diagram of the cone given below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-043.png]\n\n1. What is the name of the shaded area labelled $X$?\n2. What shape is the shaded area labelled $X$?\n3. Is the edge of a cone a straight line or a curve?\n4. What is the name of the point labelled $Y$?",
    "answer_text": "1. What is the name of the shaded area labelled $X$?\n\nStep 1: Recall the properties of a cone.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-044.png]\n\nA cone has a circle as its base. It has only one curved side face that narrows until it forms a point at the top, which is the apex.\n\nStep 2: Identify the shaded area and give the correct answer.\n\nThe shaded area labelled $X$ is the base of the cone.\n\n2. What shape is the shaded area labelled $X$?\n\nStep 1: Recall the properties of a cone.\n\nA cone has a circle as its base.\n\nStep 2: Identify the shape and give the correct answer.\n\nThe base of the cone, labelled $X$, is a circle.\n\n3. Is the edge of a cone a straight line or a curve?\n\nStep 1: Recall the properties of a cone.\n\nA cone has a circle as its base. It has only one curved side face that tapers to a single point at the apex.\n\nStep 2: Identify the edge of the cone and give the correct answer.\n\nThe edge of a cone is curved. The edge of a cone is the circumference of the circle that is the base of the cone.\n\n4. What is the name of the point labelled $Y$?\n\nStep 1: Recall the properties of a cone.\n\nA cone has a circle as its base. It has only one curved side face that tapers to a single point at the apex.\n\nStep 2: Identify the point labelled $Y$ and give the correct answer.\n\nThe point $Y$ is the vertex of the cone. It is also called the apex of the cone.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b034",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": "Exercise 13.7: Describe the parts of a cone"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.7: Describe the parts of a cone\n\nConsider the diagram of a cone given below. The diagram labels the base with $X$ and the apex with $Y$.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b034-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": "Exercise 13.7: Describe the parts of a cone"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.7: Describe the parts of a cone\n\nConsider the diagram of a cone given below. The diagram labels the base with $X$ and the apex with $Y$.\n\n1. What is the name of the 3D object?",
    "answer_text": "The 3D object is a cone.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b034-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": "Exercise 13.7: Describe the parts of a cone"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.7: Describe the parts of a cone\n\nConsider the diagram of a cone given below. The diagram labels the base with $X$ and the apex with $Y$.\n\n2. What letter on the diagram shows the base of the object?",
    "answer_text": "The letter $X$ shows the base of the cone.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b034-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": "Exercise 13.7: Describe the parts of a cone"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.7: Describe the parts of a cone\n\nConsider the diagram of a cone given below. The diagram labels the base with $X$ and the apex with $Y$.\n\n3. What shape is the base of the object?",
    "answer_text": "The base of the cone is a circle.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b034-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": "Exercise 13.7: Describe the parts of a cone"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.7: Describe the parts of a cone\n\nConsider the diagram of a cone given below. The diagram labels the base with $X$ and the apex with $Y$.\n\n4. What is the name of the point labelled $Y$?",
    "answer_text": "The point $Y$ is the vertex of the cone. It is also called the apex of the cone.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b034-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": "Exercise 13.7: Describe the parts of a cone"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.7: Describe the parts of a cone\n\nConsider the diagram of a cone given below. The diagram labels the base with $X$ and the apex with $Y$.\n\n5. Why is the edge of a cone not a straight line but a curve?",
    "answer_text": "The edge of a cone is a curve, because the edge of a cone is the circumference of the circle that is the base of the cone.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b035",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": "Exercise 13.8: Describe the properties of a cone"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.8: Describe the properties of a cone",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b035-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": "Exercise 13.8: Describe the properties of a cone"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.8: Describe the properties of a cone\n\n1. Select a word from Column B that best fits the description in Column A.\n\n| Column A | Column B |\n| --- | --- |\n| a) The flat circle that forms part of a cone. | A vertex or apex |\n| b) The circumference of the circle which is the base of the cone. | B base |\n| c) The point at the top of a cone. | C edge |",
    "answer_text": "a) B\nb) C\nc) A",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b035-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": "Exercise 13.8: Describe the properties of a cone"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.8: Describe the properties of a cone\n\n2. Complete the following table.\n\n**Properties of a cone**\n\n| Number and shape of faces | Number of edges | Number of vertices |\n| --- | --- | --- |\n|  |  |  |",
    "answer_text": "**Properties of a cone**\n\n| Number and shape of faces | Number of edges | Number of vertices |\n| --- | --- | --- |\n| 1 flat circle as base and 1 curved side face | 1 curved edge | 1 vertex (the apex) |",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
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
  "subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones",
  "subtopic_title": "Basic properties of pyramids and cones.",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones-po01",
        "source_performance_objective_index": 1,
        "text": "Identify the properties of pyramids and cones"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "basic-properties-of-pyramids-and-cones-ao-identify-properties-of-pyramids",
          "text": "Identify the properties of pyramids."
        },
        {
          "atomic_objective_id": "basic-properties-of-pyramids-and-cones-ao-identify-properties-of-cones",
          "text": "Identify the properties of cones."
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
    "record_id": "ch13-b020",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": null
    },
    "content_text": "A **pyramid** is an object that has a polygon as its base and sides that **converge** (meet each other) at one single point. The sides are *not* perpendicular to the base.\n\nThere are many real life objects in the form of a pyramid. The pyramids of Egypt are well known.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-024.png]\n\nA pile of eggs can be stacked in a pyramid.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-025.png]\n\nThe roof of a house can be in the shape of a pyramid.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-026.png]\n\nA pyramid can have any polygon, for example a rectangle, a pentagon, or a hexagon, as its base.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-027.png]\n\nWe will focus on a pyramid that has a square as its base.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-028.png]\n\nThe properties of a pyramid are:\n\n- A square-based pyramid has five *faces*.\n\n- A square-based pyramid has a square as a *base*.\n\n- The side faces are four equal isosceles triangles.\n\n- The faces of a pyramid meet each other at an *edge*.\n\n- A square-based pyramid has eight edges: four around the base and four formed by the triangular side faces.\n\n- The edges of a pyramid meet each other at a *vertex*.\n\n- A square-based pyramid has five vertices: four at the base and one at the top where the triangles meet each other.\n\nThe top vertex has a special name. The edges of the triangles that form the side faces converge at a vertex called the **apex**.\n\nWe call a pyramid a \"right pyramid\" if the line between the apex and the centre of the base is perpendicular to the base.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b021",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": null
    },
    "content_text": "**pyramid** A pyramid is a 3D object that has a polygon as its base. The side faces are triangles that meet each other at one single point, the apex.\n\n**converge** To converge is to move towards each other and to meet at one point.\n\n**apex** The apex is the top-most point that is furthest from the base of a 3D object.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b022",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": null
    },
    "content_text": "A pyramid is NOT a prism, because the side faces are not rectangles and the side faces are not perpendicular to the base.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b023",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": "Worked example 13.5: Describing the parts of a pyramid"
    },
    "content_text": "",
    "prompt_text": "Consider the square-based pyramid given below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-033.png]\n\nQuestion 1: What is the name of the shaded area labelled $P$?\n\nQuestion 2: What is the shape of the base of this pyramid?\n\nQuestion 3: What is the shape of the side faces of the pyramid?\n\nQuestion 4: What is the name of the line labelled $QR$?\n\nQuestion 5: What is the name of the point labelled $S$?\n\nQuestion 6: What is the special name of the point labelled $Q$?",
    "answer_text": "Question 1\n\nStep 1: Recall the properties of a pyramid.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-034.png]\n\nStep 2: Identify the shaded area and give the correct answer.\n\nThe shaded area is a face of the pyramid.\n\nQuestion 2\n\nStep 1: Identify the shape of the base of the pyramid and give the correct answer.\n\nThe base of the pyramid is a square.\n\nQuestion 3\n\nStep 1: Identify the shape of the side faces and give the correct answer.\n\nThe side faces are triangles.\n\nQuestion 4\n\nStep 1: Recall the properties of a pyramid.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-034.png]\n\nStep 2: Identify the line labelled $QR$ and give the correct answer.\n\nThe line labelled $QR$ is an edge of the pyramid.\n\nQuestion 5\n\nStep 1: Recall the properties of a pyramid.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-034.png]\n\nStep 2: Identify the point labelled $S$ and give the correct answer.\n\nThe point labelled $S$ is a vertex of the pyramid.\n\nQuestion 6\n\nStep 1: Recall the properties of a pyramid.\n\nThe top vertex has a special name. The edges of the triangles that form the side faces converge at a vertex called the apex.\n\nStep 2: Identify the point labelled $Q$ and give the correct answer.\n\nThe point labelled $Q$ is the apex of the pyramid.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b024",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": "Exercise 13.5: Identify the parts of a pyramid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.5: Identify the parts of a pyramid\n\nConsider the 3D object given below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-028.png]",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b024-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": "Exercise 13.5: Identify the parts of a pyramid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.5: Identify the parts of a pyramid\n\nConsider the 3D object given below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-028.png]\n\n1. What is the name of the 3D object?",
    "answer_text": "The 3D object is a pyramid. The base of this pyramid is a square, so it is a square-based pyramid.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b024-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": "Exercise 13.5: Identify the parts of a pyramid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.5: Identify the parts of a pyramid\n\nConsider the 3D object given below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-028.png]\n\n2. How many faces does the object have?",
    "answer_text": "The object (a pyramid) has one base and four side faces, so the pyramid has five faces.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b024-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": "Exercise 13.5: Identify the parts of a pyramid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.5: Identify the parts of a pyramid\n\nConsider the 3D object given below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-028.png]\n\n3. What are the shapes of the faces?",
    "answer_text": "The base is a square and the side faces are triangles.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b024-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": "Exercise 13.5: Identify the parts of a pyramid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.5: Identify the parts of a pyramid\n\nConsider the 3D object given below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-028.png]\n\n4. How many edges does the pyramid have?",
    "answer_text": "The pyramid has 8 edges.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b024-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": "Exercise 13.5: Identify the parts of a pyramid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.5: Identify the parts of a pyramid\n\nConsider the 3D object given below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-028.png]\n\n5. How many vertices does the pyramid have?",
    "answer_text": "The pyramid has 5 vertices.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b024-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": "Exercise 13.5: Identify the parts of a pyramid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.5: Identify the parts of a pyramid\n\nConsider the 3D object given below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-028.png]\n\n6. What is the name of the one point where all the triangles meet each other?",
    "answer_text": "The special vertex at the top is called the apex.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b025",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": "Exercise 13.6: Describe the properties of a pyramid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.6: Describe the properties of a pyramid",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b025-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": "Exercise 13.6: Describe the properties of a pyramid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.6: Describe the properties of a pyramid\n\n1. Select a word from Column B that best fits the description in Column A.\n\n| Column A | Column B |\n\n| --- | --- |\n\n| a) The base and triangles that form the flat parts of a pyramid. | A vertices |\n\n| b) The lines where the faces of a pyramid meet each other. | B apex |\n\n| c) The points where the edges of a pyramid meet each other. | C edges |\n\n| d) The special point where all the side faces meet each other. | D faces |",
    "answer_text": "a) D\nb) C\nc) A\nd) B",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b025-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.2 Pyramids",
      "h3": "Exercise 13.6: Describe the properties of a pyramid"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.6: Describe the properties of a pyramid\n\n2. Complete the table given below.\n\n**Properties of a square-based pyramid**\n\n| Number and shape of faces | Number of edges | Number of vertices |\n\n| --- | --- | --- |\n\n|  |  |  |",
    "answer_text": "**Properties of a square-based pyramid**\n\n| Number and shape of faces | Number of edges | Number of vertices |\n\n| --- | --- | --- |\n\n| 1 square and 4 triangles | 8 edges | 5 vertices |",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b026",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": null
    },
    "content_text": "A **cone** is another example of a 3D object that has an apex.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-035.png]\n\nThere are many examples of cones in real life.\n\nWe can buy ice cream in a cone. The part of the ice cream that you hold in your hand is the cone.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-036.png]",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b027",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": null
    },
    "content_text": "The round ball of ice cream that you eat is a sphere. You will study the properties of a sphere later in this chapter.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b028",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": null
    },
    "content_text": "We can make a party hat in the form of a cone.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-037.png]\n\nThe roof of a house can be in the form of a cone.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-038.png]",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b029",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": null
    },
    "content_text": "The circular walls of the round houses are cylinders. You will study the properties of a cylinder later in this chapter.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b030",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": null
    },
    "content_text": "The properties of a cone are:\n\n- A cone has two *faces*. One of the faces is flat and the other face is curved.\n- The *base* of a cone is a flat circle.\n- [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-039.png]\n- A cone has only one side face, and this face is curved.\n- Draw a circle and cut it out. Then cut out a \"slice\" (a sector) of the circle as shown below.\n- [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-040.png]\n- Curl the paper around so that $AB$ fits onto $AC$. You are now holding the curved face of a cone in your hand. Although this face is curved, it can be laid flat, so it is still a face.\n- A cone has only one *edge*. The edge of a cone is not a straight line; it is a curve.\n- [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-041.png]\n- The edge of a cone is the circumference of the circle that forms the base of the cone.\n- A cone has only one *vertex*.\n- The vertex of a cone is at the top of the cone.\n- [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-042.png]\n\nThe one vertex of a cone is also called the *apex* of the cone. From the base, the curved face becomes narrower until it forms a point at the top, which is the apex.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b031",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": null
    },
    "content_text": "**cone** A cone is a 3D object with a circle as its base. A cone has one curved side face that comes to a point, the apex.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b032",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": null
    },
    "content_text": "A cone is NOT a prism: a cone has a circle as its base, and a circle is not a polygon. A prism has a polygon as a base.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b033",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": "Worked example 13.6: Identifying the parts of a cone"
    },
    "content_text": "",
    "prompt_text": "Consider the diagram of the cone given below.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-043.png]\n\n1. What is the name of the shaded area labelled $X$?\n2. What shape is the shaded area labelled $X$?\n3. Is the edge of a cone a straight line or a curve?\n4. What is the name of the point labelled $Y$?",
    "answer_text": "1. What is the name of the shaded area labelled $X$?\n\nStep 1: Recall the properties of a cone.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-044.png]\n\nA cone has a circle as its base. It has only one curved side face that narrows until it forms a point at the top, which is the apex.\n\nStep 2: Identify the shaded area and give the correct answer.\n\nThe shaded area labelled $X$ is the base of the cone.\n\n2. What shape is the shaded area labelled $X$?\n\nStep 1: Recall the properties of a cone.\n\nA cone has a circle as its base.\n\nStep 2: Identify the shape and give the correct answer.\n\nThe base of the cone, labelled $X$, is a circle.\n\n3. Is the edge of a cone a straight line or a curve?\n\nStep 1: Recall the properties of a cone.\n\nA cone has a circle as its base. It has only one curved side face that tapers to a single point at the apex.\n\nStep 2: Identify the edge of the cone and give the correct answer.\n\nThe edge of a cone is curved. The edge of a cone is the circumference of the circle that is the base of the cone.\n\n4. What is the name of the point labelled $Y$?\n\nStep 1: Recall the properties of a cone.\n\nA cone has a circle as its base. It has only one curved side face that tapers to a single point at the apex.\n\nStep 2: Identify the point labelled $Y$ and give the correct answer.\n\nThe point $Y$ is the vertex of the cone. It is also called the apex of the cone.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b034",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": "Exercise 13.7: Describe the parts of a cone"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.7: Describe the parts of a cone\n\nConsider the diagram of a cone given below. The diagram labels the base with $X$ and the apex with $Y$.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b034-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": "Exercise 13.7: Describe the parts of a cone"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.7: Describe the parts of a cone\n\nConsider the diagram of a cone given below. The diagram labels the base with $X$ and the apex with $Y$.\n\n1. What is the name of the 3D object?",
    "answer_text": "The 3D object is a cone.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b034-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": "Exercise 13.7: Describe the parts of a cone"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.7: Describe the parts of a cone\n\nConsider the diagram of a cone given below. The diagram labels the base with $X$ and the apex with $Y$.\n\n2. What letter on the diagram shows the base of the object?",
    "answer_text": "The letter $X$ shows the base of the cone.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b034-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": "Exercise 13.7: Describe the parts of a cone"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.7: Describe the parts of a cone\n\nConsider the diagram of a cone given below. The diagram labels the base with $X$ and the apex with $Y$.\n\n3. What shape is the base of the object?",
    "answer_text": "The base of the cone is a circle.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b034-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": "Exercise 13.7: Describe the parts of a cone"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.7: Describe the parts of a cone\n\nConsider the diagram of a cone given below. The diagram labels the base with $X$ and the apex with $Y$.\n\n4. What is the name of the point labelled $Y$?",
    "answer_text": "The point $Y$ is the vertex of the cone. It is also called the apex of the cone.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b034-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": "Exercise 13.7: Describe the parts of a cone"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.7: Describe the parts of a cone\n\nConsider the diagram of a cone given below. The diagram labels the base with $X$ and the apex with $Y$.\n\n5. Why is the edge of a cone not a straight line but a curve?",
    "answer_text": "The edge of a cone is a curve, because the edge of a cone is the circumference of the circle that is the base of the cone.",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b035",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": "Exercise 13.8: Describe the properties of a cone"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.8: Describe the properties of a cone",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b035-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": "Exercise 13.8: Describe the properties of a cone"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.8: Describe the properties of a cone\n\n1. Select a word from Column B that best fits the description in Column A.\n\n| Column A | Column B |\n| --- | --- |\n| a) The flat circle that forms part of a cone. | A vertex or apex |\n| b) The circumference of the circle which is the base of the cone. | B base |\n| c) The point at the top of a cone. | C edge |",
    "answer_text": "a) B\nb) C\nc) A",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
  },
  {
    "record_id": "ch13-b035-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 13: Three-dimensional objects",
      "h2": "13.3 Cones",
      "h3": "Exercise 13.8: Describe the properties of a cone"
    },
    "content_text": "",
    "prompt_text": "### Exercise 13.8: Describe the properties of a cone\n\n2. Complete the following table.\n\n**Properties of a cone**\n\n| Number and shape of faces | Number of edges | Number of vertices |\n| --- | --- | --- |\n|  |  |  |",
    "answer_text": "**Properties of a cone**\n\n| Number and shape of faces | Number of edges | Number of vertices |\n| --- | --- | --- |\n| 1 flat circle as base and 1 curved side face | 1 curved edge | 1 vertex (the apex) |",
    "primary_subtopic_id": "jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones"
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
