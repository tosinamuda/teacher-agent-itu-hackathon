# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-4",
  "topic_key": "jss1-math-construction",
  "topic": "Construction",
  "subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines",
  "subtopic_title": "Construction of parallel and perpendicular lines.",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines-po01",
        "source_performance_objective_index": 1,
        "text": "Construct parallel and perpendicular lines"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "construction-of-parallel-and-perpendicular-lines-ao-construct-parallel-lines",
          "text": "Construct parallel lines."
        },
        {
          "atomic_objective_id": "construction-of-parallel-and-perpendicular-lines-ao-construct-perpendicular-lines",
          "text": "Construct perpendicular lines."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch14-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": null,
      "h3": null
    },
    "content_text": "A construction in Mathematics is an accurate drawing of angles and lines. You are only allowed to use a straightedge and a pair of compasses with a pencil in it when you do constructions.\n\n1. A straightedge\n\nA straightedge is an instrument made of plastic, metal or wood that has a straight edge. You use it to draw straight lines. It is a ruler without any markings on it, because when you do constructions you are not allowed to take any measurements.\n\nMost of the time you will use your ruler when you do constructions and have to draw straight lines. The important thing to remember is that although there are markings on the ruler, you should not use them at all. You may only use the ruler to draw a straight line.\n\n2. A pair of compasses\n\nA pair of compasses is an instrument to draw circles. It can also be called \"a compass\".\n\nA compass has two legs:\n- One leg has a sharp point so that you can put it firmly into position on a piece of paper or page in a notebook. When you draw a circle the sharp point will stay on the dot where you positioned it. The sharp point will not move.\n- The other leg has space to insert a pencil. When you draw a circle, you move this leg around, and the pencil will draw the circle on the page.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b002",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": null,
      "h3": null
    },
    "content_text": "The two legs of the compass are joined at the hinge. Make sure that the metal pin at the hinge is fitted tightly so that the two legs of the compass will not open too easily. Also make sure that your pencil is sharpened. A blunt pencil will lead to diagrams that are not accurate.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b003",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": null,
      "h3": null
    },
    "content_text": "Do not confuse the compass that we use in mathematical constructions with the compass that we use to find direction.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b004",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": null,
      "h3": null
    },
    "content_text": "All the constructions in this chapter are based on the properties of a circle.\n\nIn the diagram below, $BC$ is the diameter of the circle. $A$ is the centre of the circle. This means that $AB$ is a radius of the circle and $AC$ is also a radius of the circle. So, $AB$ is equal to $AC$.\n\nWhen we do constructions we often do not draw a complete circle.\n\nThe solid lines drawn at $B$ and $C$ are called **arcs**. An arc is part of the circumference of a circle.\n\nWe will draw arcs in all the constructions that we are going to do. It is important to remember that if we draw two arcs while our compass stays in the same position, we are drawing two radiuses with equal lengths. Even if we do not draw a complete circle, and we only draw an arc at $B$ and at $C$, $AB$ is still a radius of the circle and $AC$ is still a radius of the circle. So, $AB$ is equal to $AC$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b005",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": null,
      "h3": null
    },
    "content_text": "**arc** An arc is a part of the circumference of a circle.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b006",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": null
    },
    "content_text": "Lines that are perpendicular **intersect** each other at right angles (at $90^{\\circ}$). When we are asked to construct a **perpendicular line**, we will be given one of the lines, as well as a point. We then have to construct a line through the given point so that the new line is perpendicular to the given line.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b007",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": null
    },
    "content_text": "**intersect** When two lines intersect, they cross each other.\n\n**perpendicular line** A perpendicular line cuts another line at a right angle.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b008",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": null
    },
    "content_text": "The point that is given can be on the line, or it can be a small distance away from the line.\n\nIn the first diagram, point $P$ is *on* line $AB$. In the second diagram, point $P$ is some distance *away* from line $AB$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b009",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": "Worked example 14.1: Constructing a perpendicular line from a point on the line"
    },
    "content_text": "",
    "prompt_text": "You are given line $AB$ with a point $P$ on the line.\n\nConstruct line $PQ$ so that $PQ$ is perpendicular to $AB$.",
    "answer_text": "Step 1: Mark equal distances to both sides of point $P$ on line $AB$.\n\nPut the compass on point $P$. Draw an arc to the left of point $P$. Then, while keeping the compass open by exactly the same amount, draw an arc to the right of point $P$. These arcs should intersect line $AB$.\n\nStep 2: Draw an arc from the left.\n\nPut the compass point on the arc at the left. Draw an arc so that it is above point $P$.\n\nStep 3: Draw an arc from the right.\n\nKeep the compass exactly the same width open as for Step 2. Put the compass point on the arc at the right. Draw an arc so that it intersects the arc from Step 2.\n\nStep 4: Draw the perpendicular line.\n\nPoint $Q$ is where the two arcs from Step 2 and Step 3 are intersecting each other. Use a ruler and draw a line from point $P$ and through point $Q$.\n\nStep 5: Check your construction.\n\nUse a protractor to measure $Q\\hat{P}A$ and $Q\\hat{P}B$. If each of them is equal to $90^{\\circ}$, you have made an accurate construction.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b010",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": null
    },
    "content_text": "When copying the lines in order to do constructions, the lines only need to be more or less the same length as given in the questions, and in more or less the same direction. It is a good idea to rotate your workbook if you have to do a construction involving a line that is not horizontal on the page in front of you. Never erase the construction lines after you have completed a construction.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b011",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": "Exercise 14.1: Construct a perpendicular line from a point on the line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.1: Construct a perpendicular line from a point on the line",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b011-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": "Exercise 14.1: Construct a perpendicular line from a point on the line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.1: Construct a perpendicular line from a point on the line\n\n1. Draw line $CD$ as shown below. $P$ is a point on the line. Construct $PQ$ perpendicular to line $CD$. Remember to check your work.",
    "answer_text": "Follow the Steps as shown in Worked example 14.1.\n\nIf you have worked accurately, $Q \\hat {P} C$ and $Q \\hat{P}D$ will both be equal to $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b011-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": "Exercise 14.1: Construct a perpendicular line from a point on the line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.1: Construct a perpendicular line from a point on the line\n\n2. Draw line $EF$ as shown below. $P$ is a point on the line. Construct $PQ$ perpendicular to line $EF$. Remember to check your work.",
    "answer_text": "Follow the Steps as shown in Worked example 14.1.\n\nIf you have worked accurately, $Q\\hat{P}E$ and $Q\\hat{P}F$ will both be equal to $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b011-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": "Exercise 14.1: Construct a perpendicular line from a point on the line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.1: Construct a perpendicular line from a point on the line\n\n3. Draw line $MN$ as shown below. $P$ is a point on the line. Construct $PQ$ perpendicular to line $MN$. Remember to check your work.",
    "answer_text": "Follow the Steps as shown in Worked example 14.1.\n\nIf you have worked accurately, $Q\\hat{P}M$ and $Q\\hat{P}N$ will both be equal to $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b011-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": "Exercise 14.1: Construct a perpendicular line from a point on the line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.1: Construct a perpendicular line from a point on the line\n\n4. Draw line $ST$ as shown below. $P$ is a point on the line. Construct $PQ$ perpendicular to line $ST$. Remember to check your work.",
    "answer_text": "Follow the Steps as shown in Worked example 14.1.\n\nIf you have worked accurately, $Q\\hat{P}S$ and $Q\\hat{P}T$ will both be equal to $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b012",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": "Worked example 14.2: Constructing a perpendicular line from a point away from the line"
    },
    "content_text": "",
    "prompt_text": "You are given line $AB$ with a point $P$ away from the line.\n\nConstruct line $PQ$ so that $PQ$ is perpendicular to $AB$.",
    "answer_text": "Step 1: Mark equal distances from point $P$ on line $AB$.\n\nPut the point of the compass on point $P$. Draw an arc to the left of point $P$ on the line. While keeping the compass exactly the same width open, draw an arc on the line to the right of point $P$. These arcs should intersect line $AB$.\n\nStep 2: Work from the left and draw an arc below line $AB$.\n\nPut the compass point on the left arc of Step 1. Draw an arc so that it is underneath point $P$.\n\nStep 3: Work from the right and draw a second arc below line $AB$.\n\nKeep the compass the same width open as for Step 2. Put the compass point on the arc to the right arc of Step 1. Draw an arc so that it crosses the arc from Step 2.\n\nStep 4: Draw the perpendicular line.\n\nPoint $Q$ is where the two arcs from Step 2 and Step 3 cross each other. Use a ruler and draw a line from point $P$ and through point $Q$.\n\nStep 5: Check your construction.\n\nUse a protractor and measure the angles where line $AB$ and line $PQ$ intersect. If each angle is equal to $90^{\\circ}$, you have made an accurate construction.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b013",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": null
    },
    "content_text": "Remember to rotate your workbook if you need to, and not to erase your construction lines. Also, always check your work.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b014",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": "Exercise 14.2: Construct a perpendicular line from a point away from the line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.2: Construct a perpendicular line from a point away from the line",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b014-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": "Exercise 14.2: Construct a perpendicular line from a point away from the line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.2: Construct a perpendicular line from a point away from the line\n\n1. Draw line $CD$ as shown below. Point $P$ is a point away from the line.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-028.png\n\nConstruct $PQ$ perpendicular to line $CD$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.2.\n\nSolution image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-029.png\n\nIf you have worked accurately, the two lines will intersect each other at an angle of $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b014-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": "Exercise 14.2: Construct a perpendicular line from a point away from the line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.2: Construct a perpendicular line from a point away from the line\n\n2. Draw line $EF$ as shown below. Point $P$ is a point away from the line.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-030.png\n\nConstruct $PQ$ perpendicular to line $EF$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.2.\n\nSolution image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-031.png\n\nIf you have worked accurately, the two lines will intersect each other at an angle of $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b014-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": "Exercise 14.2: Construct a perpendicular line from a point away from the line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.2: Construct a perpendicular line from a point away from the line\n\n3. Draw line $MN$ as shown below. Point $P$ is a point away from the line.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-032.png\n\nConstruct $PQ$ perpendicular to line $MN$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.2.\n\nSolution image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-033.png\n\nIf you have worked accurately, the two lines will intersect each other at an angle of $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b014-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": "Exercise 14.2: Construct a perpendicular line from a point away from the line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.2: Construct a perpendicular line from a point away from the line\n\n4. Draw line $ST$ as shown below. Point $P$ is a point away from the line.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-034.png\n\nConstruct $PQ$ perpendicular to line $ST$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.2.\n\nSolution image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-035.png\n\nIf you have worked accurately, the two lines will intersect each other at an angle of $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b015",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.2 Parallel lines",
      "h3": null
    },
    "content_text": "**Parallel lines** are lines that are always the same distance apart from each other. They never meet or cross each other. When we are asked to construct parallel lines, we will be given a line and a point. We then have to construct a line through the given point, and then another line that is parallel to the first line.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b016",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.2 Parallel lines",
      "h3": null
    },
    "content_text": "**parallel lines** Parallel lines are lines that always remain the same distance apart, and never meet or cross each other.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b017",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.2 Parallel lines",
      "h3": null
    },
    "content_text": "You will learn more about parallel lines in Chapter 15, but it will be easier to construct parallel lines if you know the following:\n\nIf two parallel lines are crossed by another line, then the angles marked in the diagram below will be equal to each other.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-036.png\n\nTo construct a parallel line, you will be given the line shown in blue in the diagram, as well as the blue dot. The plan is to measure $\\hat 1$ and then to construct $\\hat 2$ so that the two angles are equal. If the two angles are equal, the lines will be parallel.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-037.png",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b018",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.2 Parallel lines",
      "h3": "Worked example 14.3: Constructing parallel lines"
    },
    "content_text": "",
    "prompt_text": "$P$ is a point away from line $AB$.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-038.png\n\nConstruct line $PQ$ through point $P$ so that $PQ$ is parallel to $AB$.",
    "answer_text": "Step 1: Use a ruler (or a straightedge) to draw a line to form an acute angle.\n\nDraw a straight line through $P$ and that also goes through the line $AB$. This forms an angle where the two lines intersect.\n\nStep image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-039.png\n\nStep 2: Draw an arc from the vertex of the acute angle.\n\nPut the compass point on the orange dot and draw the arc that goes through both lines. Make sure that the arc is below point $P$.\n\nStep image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-040.png\n\nStep 3: Draw the second arc from point $P$.\n\nKeep the compass at the same width to draw the second arc. Put the compass point on point $P$ and draw the second arc above $P$. Make sure that the second arc goes lower than point $P$ on the right hand side.\n\nStep image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-041.png\n\nStep 4: Use the compass to measure the distance between the two points where the first arc intersects the lines.\n\nPut the point of the compass where the first arc intersects the line $AB$ at point $R$. Put the pencil end of the compass where this arc intersects the line through $P$ at point $S$.\n\nStep image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-042.png\n\nIMPORTANT: Do not draw a line between point $R$ and point $S$. You are only measuring the distance.\n\nStep 5: Mark the same length on the second arc.\n\nKeep the compass in exactly the same position. Put the compass point on point $T$, and draw an arc to find point $Q$. Point $Q$ will be where this new arc intersects the second orange arc. The distance between point $T$ and point $Q$ should be exactly the same as the distance between point $R$ and point $S$.\n\nStep image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-043.png\n\nIMPORTANT: Do not draw a line between point $T$ and point $Q$. You are only measuring off the correct distance.\n\nStep 6: Draw a line through point $P$ and point $Q$.\n\nWhen you draw a line through point $P$ and point $Q$, line $PQ$ will be parallel to line $AB$.\n\nStep image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-044.png\n\nStep 7: Check your construction.\n\nUse a protractor to measure $\\hat 1$ and $\\hat 2$. If the two angles are equal to each other, your construction is accurate.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b019",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.2 Parallel lines",
      "h3": null
    },
    "content_text": "Remember, you can rotate your workbook to make it easier to work with a line that is not horizontal. Do not erase your construction lines after you have completed a construction, and always check your work by measuring the angles.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b020",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.2 Parallel lines",
      "h3": "Exercise 14.3: Construct a parallel line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.3: Construct a parallel line",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b020-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.2 Parallel lines",
      "h3": "Exercise 14.3: Construct a parallel line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.3: Construct a parallel line\n\n1. Draw line $CD$ as shown below. Point $P$ is a point away from the line.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-028.png\n\nConstruct $PQ$ parallel to line $CD$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.3.\n\nSolution image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-045.png\n\nIf you have worked accurately, the two angles labelled $\\hat{1}$ and $\\hat{2}$ will be equal.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b020-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.2 Parallel lines",
      "h3": "Exercise 14.3: Construct a parallel line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.3: Construct a parallel line\n\n2. Draw line $EF$ as shown below. Point $P$ is a point away from the line.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-030.png\n\nConstruct $PQ$ parallel to line $EF$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.3.\n\nSolution image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-046.png\n\nIf you have worked accurately, the two angles labelled $\\hat{1}$ and $\\hat{2}$ will be equal.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b020-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.2 Parallel lines",
      "h3": "Exercise 14.3: Construct a parallel line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.3: Construct a parallel line\n\n3. Draw line $MN$ as shown below. Point $P$ is a point away from the line.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-032.png\n\nConstruct $PQ$ parallel to line $MN$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.3.\n\nSolution image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-047.png\n\nIf you have worked accurately, the two angles labelled $\\hat{1}$ and $\\hat{2}$ will be equal.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b020-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.2 Parallel lines",
      "h3": "Exercise 14.3: Construct a parallel line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.3: Construct a parallel line\n\n4. Draw line $ST$ as shown below. Point $P$ is a point away from the line.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-034.png\n\nConstruct $PQ$ parallel to line $ST$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.3.\n\nSolution image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-048.png\n\nIf you have worked accurately, the two angles labelled $\\hat{1}$ and $\\hat{2}$ will be equal.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b036",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.6 Summary",
      "h3": null
    },
    "content_text": "- A construction in Mathematics is an accurate drawing of angles and lines.\n- You are only allowed to use a straightedge and a pair of compasses with a pencil in it when you do a construction.\n- You may use a ruler if you do not have a straightedge, but do not use the markings on the ruler.\n- You will draw arcs in all the constructions. An arc is part of the circumference of a circle.\n- You have to practise the following constructions:\n  - Construct a perpendicular line from a point *on* the line.\n  - Construct a perpendicular line from a point *away* from the line.\n  - Construct a parallel line through a given point.\n  - Bisect a line segment.\n  - Construct an angle of 60 degrees.\n  - Construct a right angle (an angle of 90 degrees).\n- Never erase the construction lines after you have completed a construction.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch15-b061",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.4 Practical applications",
      "h3": null
    },
    "content_text": "When we know about different angles and how they are formed we can apply our knowledge in real life. For example, we can use angles to describe the position of a shop, or how we want to paint decorations. Many people use angles in their jobs every day.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-vertically-opposite-adjacent-alternate-and-corresponding-angles"
  },
  {
    "record_id": "ch15-b063",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.4 Practical applications",
      "h3": "Exercise 15.11: Solve real-world problems with angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.11: Solve real-world problems with angles",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-vertically-opposite-adjacent-alternate-and-corresponding-angles"
  },
  {
    "record_id": "ch15-b063-i03a",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.4 Practical applications",
      "h3": "Exercise 15.11: Solve real-world problems with angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.11: Solve real-world problems with angles\n\n3a. Babatunde and his brother earn income by doing welding jobs. They use their knowledge of angles and lines often in their work. The photo below shows the rails in front of a house that they designed and made.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-039.png\n\nWhat is the relationship between the bottom rail marked $AB$ and the balusters marked $AC$ and $BD$?",
    "answer_text": "$AB$ is perpendicular to $AC$ and $AB$ is also perpendicular to $BD$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch15-b063-i03b",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.4 Practical applications",
      "h3": "Exercise 15.11: Solve real-world problems with angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.11: Solve real-world problems with angles\n\n3b. In the same rail diagram, what is the relationship between the balusters marked $AC$ and $BD$?\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-039.png",
    "answer_text": "$AC$ and $BD$ are parallel.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
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
  "topic_key": "jss1-math-construction",
  "topic": "Construction",
  "subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines",
  "subtopic_title": "Construction of parallel and perpendicular lines.",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines-po01",
        "source_performance_objective_index": 1,
        "text": "Construct parallel and perpendicular lines"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "construction-of-parallel-and-perpendicular-lines-ao-construct-parallel-lines",
          "text": "Construct parallel lines."
        },
        {
          "atomic_objective_id": "construction-of-parallel-and-perpendicular-lines-ao-construct-perpendicular-lines",
          "text": "Construct perpendicular lines."
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
    "record_id": "ch14-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": null,
      "h3": null
    },
    "content_text": "A construction in Mathematics is an accurate drawing of angles and lines. You are only allowed to use a straightedge and a pair of compasses with a pencil in it when you do constructions.\n\n1. A straightedge\n\nA straightedge is an instrument made of plastic, metal or wood that has a straight edge. You use it to draw straight lines. It is a ruler without any markings on it, because when you do constructions you are not allowed to take any measurements.\n\nMost of the time you will use your ruler when you do constructions and have to draw straight lines. The important thing to remember is that although there are markings on the ruler, you should not use them at all. You may only use the ruler to draw a straight line.\n\n2. A pair of compasses\n\nA pair of compasses is an instrument to draw circles. It can also be called \"a compass\".\n\nA compass has two legs:\n- One leg has a sharp point so that you can put it firmly into position on a piece of paper or page in a notebook. When you draw a circle the sharp point will stay on the dot where you positioned it. The sharp point will not move.\n- The other leg has space to insert a pencil. When you draw a circle, you move this leg around, and the pencil will draw the circle on the page.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b002",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": null,
      "h3": null
    },
    "content_text": "The two legs of the compass are joined at the hinge. Make sure that the metal pin at the hinge is fitted tightly so that the two legs of the compass will not open too easily. Also make sure that your pencil is sharpened. A blunt pencil will lead to diagrams that are not accurate.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b003",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": null,
      "h3": null
    },
    "content_text": "Do not confuse the compass that we use in mathematical constructions with the compass that we use to find direction.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b004",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": null,
      "h3": null
    },
    "content_text": "All the constructions in this chapter are based on the properties of a circle.\n\nIn the diagram below, $BC$ is the diameter of the circle. $A$ is the centre of the circle. This means that $AB$ is a radius of the circle and $AC$ is also a radius of the circle. So, $AB$ is equal to $AC$.\n\nWhen we do constructions we often do not draw a complete circle.\n\nThe solid lines drawn at $B$ and $C$ are called **arcs**. An arc is part of the circumference of a circle.\n\nWe will draw arcs in all the constructions that we are going to do. It is important to remember that if we draw two arcs while our compass stays in the same position, we are drawing two radiuses with equal lengths. Even if we do not draw a complete circle, and we only draw an arc at $B$ and at $C$, $AB$ is still a radius of the circle and $AC$ is still a radius of the circle. So, $AB$ is equal to $AC$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b005",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": null,
      "h3": null
    },
    "content_text": "**arc** An arc is a part of the circumference of a circle.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b006",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": null
    },
    "content_text": "Lines that are perpendicular **intersect** each other at right angles (at $90^{\\circ}$). When we are asked to construct a **perpendicular line**, we will be given one of the lines, as well as a point. We then have to construct a line through the given point so that the new line is perpendicular to the given line.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b007",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": null
    },
    "content_text": "**intersect** When two lines intersect, they cross each other.\n\n**perpendicular line** A perpendicular line cuts another line at a right angle.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b008",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": null
    },
    "content_text": "The point that is given can be on the line, or it can be a small distance away from the line.\n\nIn the first diagram, point $P$ is *on* line $AB$. In the second diagram, point $P$ is some distance *away* from line $AB$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b009",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": "Worked example 14.1: Constructing a perpendicular line from a point on the line"
    },
    "content_text": "",
    "prompt_text": "You are given line $AB$ with a point $P$ on the line.\n\nConstruct line $PQ$ so that $PQ$ is perpendicular to $AB$.",
    "answer_text": "Step 1: Mark equal distances to both sides of point $P$ on line $AB$.\n\nPut the compass on point $P$. Draw an arc to the left of point $P$. Then, while keeping the compass open by exactly the same amount, draw an arc to the right of point $P$. These arcs should intersect line $AB$.\n\nStep 2: Draw an arc from the left.\n\nPut the compass point on the arc at the left. Draw an arc so that it is above point $P$.\n\nStep 3: Draw an arc from the right.\n\nKeep the compass exactly the same width open as for Step 2. Put the compass point on the arc at the right. Draw an arc so that it intersects the arc from Step 2.\n\nStep 4: Draw the perpendicular line.\n\nPoint $Q$ is where the two arcs from Step 2 and Step 3 are intersecting each other. Use a ruler and draw a line from point $P$ and through point $Q$.\n\nStep 5: Check your construction.\n\nUse a protractor to measure $Q\\hat{P}A$ and $Q\\hat{P}B$. If each of them is equal to $90^{\\circ}$, you have made an accurate construction.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b010",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": null
    },
    "content_text": "When copying the lines in order to do constructions, the lines only need to be more or less the same length as given in the questions, and in more or less the same direction. It is a good idea to rotate your workbook if you have to do a construction involving a line that is not horizontal on the page in front of you. Never erase the construction lines after you have completed a construction.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b011",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": "Exercise 14.1: Construct a perpendicular line from a point on the line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.1: Construct a perpendicular line from a point on the line",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b011-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": "Exercise 14.1: Construct a perpendicular line from a point on the line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.1: Construct a perpendicular line from a point on the line\n\n1. Draw line $CD$ as shown below. $P$ is a point on the line. Construct $PQ$ perpendicular to line $CD$. Remember to check your work.",
    "answer_text": "Follow the Steps as shown in Worked example 14.1.\n\nIf you have worked accurately, $Q \\hat {P} C$ and $Q \\hat{P}D$ will both be equal to $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b011-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": "Exercise 14.1: Construct a perpendicular line from a point on the line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.1: Construct a perpendicular line from a point on the line\n\n2. Draw line $EF$ as shown below. $P$ is a point on the line. Construct $PQ$ perpendicular to line $EF$. Remember to check your work.",
    "answer_text": "Follow the Steps as shown in Worked example 14.1.\n\nIf you have worked accurately, $Q\\hat{P}E$ and $Q\\hat{P}F$ will both be equal to $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b011-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": "Exercise 14.1: Construct a perpendicular line from a point on the line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.1: Construct a perpendicular line from a point on the line\n\n3. Draw line $MN$ as shown below. $P$ is a point on the line. Construct $PQ$ perpendicular to line $MN$. Remember to check your work.",
    "answer_text": "Follow the Steps as shown in Worked example 14.1.\n\nIf you have worked accurately, $Q\\hat{P}M$ and $Q\\hat{P}N$ will both be equal to $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b011-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": "Exercise 14.1: Construct a perpendicular line from a point on the line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.1: Construct a perpendicular line from a point on the line\n\n4. Draw line $ST$ as shown below. $P$ is a point on the line. Construct $PQ$ perpendicular to line $ST$. Remember to check your work.",
    "answer_text": "Follow the Steps as shown in Worked example 14.1.\n\nIf you have worked accurately, $Q\\hat{P}S$ and $Q\\hat{P}T$ will both be equal to $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b012",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": "Worked example 14.2: Constructing a perpendicular line from a point away from the line"
    },
    "content_text": "",
    "prompt_text": "You are given line $AB$ with a point $P$ away from the line.\n\nConstruct line $PQ$ so that $PQ$ is perpendicular to $AB$.",
    "answer_text": "Step 1: Mark equal distances from point $P$ on line $AB$.\n\nPut the point of the compass on point $P$. Draw an arc to the left of point $P$ on the line. While keeping the compass exactly the same width open, draw an arc on the line to the right of point $P$. These arcs should intersect line $AB$.\n\nStep 2: Work from the left and draw an arc below line $AB$.\n\nPut the compass point on the left arc of Step 1. Draw an arc so that it is underneath point $P$.\n\nStep 3: Work from the right and draw a second arc below line $AB$.\n\nKeep the compass the same width open as for Step 2. Put the compass point on the arc to the right arc of Step 1. Draw an arc so that it crosses the arc from Step 2.\n\nStep 4: Draw the perpendicular line.\n\nPoint $Q$ is where the two arcs from Step 2 and Step 3 cross each other. Use a ruler and draw a line from point $P$ and through point $Q$.\n\nStep 5: Check your construction.\n\nUse a protractor and measure the angles where line $AB$ and line $PQ$ intersect. If each angle is equal to $90^{\\circ}$, you have made an accurate construction.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b013",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": null
    },
    "content_text": "Remember to rotate your workbook if you need to, and not to erase your construction lines. Also, always check your work.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b014",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": "Exercise 14.2: Construct a perpendicular line from a point away from the line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.2: Construct a perpendicular line from a point away from the line",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b014-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": "Exercise 14.2: Construct a perpendicular line from a point away from the line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.2: Construct a perpendicular line from a point away from the line\n\n1. Draw line $CD$ as shown below. Point $P$ is a point away from the line.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-028.png\n\nConstruct $PQ$ perpendicular to line $CD$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.2.\n\nSolution image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-029.png\n\nIf you have worked accurately, the two lines will intersect each other at an angle of $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b014-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": "Exercise 14.2: Construct a perpendicular line from a point away from the line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.2: Construct a perpendicular line from a point away from the line\n\n2. Draw line $EF$ as shown below. Point $P$ is a point away from the line.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-030.png\n\nConstruct $PQ$ perpendicular to line $EF$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.2.\n\nSolution image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-031.png\n\nIf you have worked accurately, the two lines will intersect each other at an angle of $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b014-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": "Exercise 14.2: Construct a perpendicular line from a point away from the line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.2: Construct a perpendicular line from a point away from the line\n\n3. Draw line $MN$ as shown below. Point $P$ is a point away from the line.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-032.png\n\nConstruct $PQ$ perpendicular to line $MN$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.2.\n\nSolution image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-033.png\n\nIf you have worked accurately, the two lines will intersect each other at an angle of $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b014-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.1 Perpendicular lines",
      "h3": "Exercise 14.2: Construct a perpendicular line from a point away from the line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.2: Construct a perpendicular line from a point away from the line\n\n4. Draw line $ST$ as shown below. Point $P$ is a point away from the line.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-034.png\n\nConstruct $PQ$ perpendicular to line $ST$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.2.\n\nSolution image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-035.png\n\nIf you have worked accurately, the two lines will intersect each other at an angle of $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b015",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.2 Parallel lines",
      "h3": null
    },
    "content_text": "**Parallel lines** are lines that are always the same distance apart from each other. They never meet or cross each other. When we are asked to construct parallel lines, we will be given a line and a point. We then have to construct a line through the given point, and then another line that is parallel to the first line.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b016",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.2 Parallel lines",
      "h3": null
    },
    "content_text": "**parallel lines** Parallel lines are lines that always remain the same distance apart, and never meet or cross each other.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b017",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.2 Parallel lines",
      "h3": null
    },
    "content_text": "You will learn more about parallel lines in Chapter 15, but it will be easier to construct parallel lines if you know the following:\n\nIf two parallel lines are crossed by another line, then the angles marked in the diagram below will be equal to each other.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-036.png\n\nTo construct a parallel line, you will be given the line shown in blue in the diagram, as well as the blue dot. The plan is to measure $\\hat 1$ and then to construct $\\hat 2$ so that the two angles are equal. If the two angles are equal, the lines will be parallel.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-037.png",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b018",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.2 Parallel lines",
      "h3": "Worked example 14.3: Constructing parallel lines"
    },
    "content_text": "",
    "prompt_text": "$P$ is a point away from line $AB$.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-038.png\n\nConstruct line $PQ$ through point $P$ so that $PQ$ is parallel to $AB$.",
    "answer_text": "Step 1: Use a ruler (or a straightedge) to draw a line to form an acute angle.\n\nDraw a straight line through $P$ and that also goes through the line $AB$. This forms an angle where the two lines intersect.\n\nStep image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-039.png\n\nStep 2: Draw an arc from the vertex of the acute angle.\n\nPut the compass point on the orange dot and draw the arc that goes through both lines. Make sure that the arc is below point $P$.\n\nStep image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-040.png\n\nStep 3: Draw the second arc from point $P$.\n\nKeep the compass at the same width to draw the second arc. Put the compass point on point $P$ and draw the second arc above $P$. Make sure that the second arc goes lower than point $P$ on the right hand side.\n\nStep image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-041.png\n\nStep 4: Use the compass to measure the distance between the two points where the first arc intersects the lines.\n\nPut the point of the compass where the first arc intersects the line $AB$ at point $R$. Put the pencil end of the compass where this arc intersects the line through $P$ at point $S$.\n\nStep image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-042.png\n\nIMPORTANT: Do not draw a line between point $R$ and point $S$. You are only measuring the distance.\n\nStep 5: Mark the same length on the second arc.\n\nKeep the compass in exactly the same position. Put the compass point on point $T$, and draw an arc to find point $Q$. Point $Q$ will be where this new arc intersects the second orange arc. The distance between point $T$ and point $Q$ should be exactly the same as the distance between point $R$ and point $S$.\n\nStep image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-043.png\n\nIMPORTANT: Do not draw a line between point $T$ and point $Q$. You are only measuring off the correct distance.\n\nStep 6: Draw a line through point $P$ and point $Q$.\n\nWhen you draw a line through point $P$ and point $Q$, line $PQ$ will be parallel to line $AB$.\n\nStep image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-044.png\n\nStep 7: Check your construction.\n\nUse a protractor to measure $\\hat 1$ and $\\hat 2$. If the two angles are equal to each other, your construction is accurate.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b019",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.2 Parallel lines",
      "h3": null
    },
    "content_text": "Remember, you can rotate your workbook to make it easier to work with a line that is not horizontal. Do not erase your construction lines after you have completed a construction, and always check your work by measuring the angles.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b020",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.2 Parallel lines",
      "h3": "Exercise 14.3: Construct a parallel line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.3: Construct a parallel line",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b020-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.2 Parallel lines",
      "h3": "Exercise 14.3: Construct a parallel line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.3: Construct a parallel line\n\n1. Draw line $CD$ as shown below. Point $P$ is a point away from the line.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-028.png\n\nConstruct $PQ$ parallel to line $CD$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.3.\n\nSolution image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-045.png\n\nIf you have worked accurately, the two angles labelled $\\hat{1}$ and $\\hat{2}$ will be equal.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b020-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.2 Parallel lines",
      "h3": "Exercise 14.3: Construct a parallel line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.3: Construct a parallel line\n\n2. Draw line $EF$ as shown below. Point $P$ is a point away from the line.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-030.png\n\nConstruct $PQ$ parallel to line $EF$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.3.\n\nSolution image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-046.png\n\nIf you have worked accurately, the two angles labelled $\\hat{1}$ and $\\hat{2}$ will be equal.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b020-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.2 Parallel lines",
      "h3": "Exercise 14.3: Construct a parallel line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.3: Construct a parallel line\n\n3. Draw line $MN$ as shown below. Point $P$ is a point away from the line.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-032.png\n\nConstruct $PQ$ parallel to line $MN$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.3.\n\nSolution image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-047.png\n\nIf you have worked accurately, the two angles labelled $\\hat{1}$ and $\\hat{2}$ will be equal.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b020-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.2 Parallel lines",
      "h3": "Exercise 14.3: Construct a parallel line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.3: Construct a parallel line\n\n4. Draw line $ST$ as shown below. Point $P$ is a point away from the line.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-034.png\n\nConstruct $PQ$ parallel to line $ST$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.3.\n\nSolution image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-048.png\n\nIf you have worked accurately, the two angles labelled $\\hat{1}$ and $\\hat{2}$ will be equal.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch14-b036",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.6 Summary",
      "h3": null
    },
    "content_text": "- A construction in Mathematics is an accurate drawing of angles and lines.\n- You are only allowed to use a straightedge and a pair of compasses with a pencil in it when you do a construction.\n- You may use a ruler if you do not have a straightedge, but do not use the markings on the ruler.\n- You will draw arcs in all the constructions. An arc is part of the circumference of a circle.\n- You have to practise the following constructions:\n  - Construct a perpendicular line from a point *on* the line.\n  - Construct a perpendicular line from a point *away* from the line.\n  - Construct a parallel line through a given point.\n  - Bisect a line segment.\n  - Construct an angle of 60 degrees.\n  - Construct a right angle (an angle of 90 degrees).\n- Never erase the construction lines after you have completed a construction.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch15-b061",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.4 Practical applications",
      "h3": null
    },
    "content_text": "When we know about different angles and how they are formed we can apply our knowledge in real life. For example, we can use angles to describe the position of a shop, or how we want to paint decorations. Many people use angles in their jobs every day.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-vertically-opposite-adjacent-alternate-and-corresponding-angles"
  },
  {
    "record_id": "ch15-b063",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.4 Practical applications",
      "h3": "Exercise 15.11: Solve real-world problems with angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.11: Solve real-world problems with angles",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-vertically-opposite-adjacent-alternate-and-corresponding-angles"
  },
  {
    "record_id": "ch15-b063-i03a",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.4 Practical applications",
      "h3": "Exercise 15.11: Solve real-world problems with angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.11: Solve real-world problems with angles\n\n3a. Babatunde and his brother earn income by doing welding jobs. They use their knowledge of angles and lines often in their work. The photo below shows the rails in front of a house that they designed and made.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-039.png\n\nWhat is the relationship between the bottom rail marked $AB$ and the balusters marked $AC$ and $BD$?",
    "answer_text": "$AB$ is perpendicular to $AC$ and $AB$ is also perpendicular to $BD$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
  },
  {
    "record_id": "ch15-b063-i03b",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.4 Practical applications",
      "h3": "Exercise 15.11: Solve real-world problems with angles"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.11: Solve real-world problems with angles\n\n3b. In the same rail diagram, what is the relationship between the balusters marked $AC$ and $BD$?\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-039.png",
    "answer_text": "$AC$ and $BD$ are parallel.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-parallel-and-perpendicular-lines"
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
