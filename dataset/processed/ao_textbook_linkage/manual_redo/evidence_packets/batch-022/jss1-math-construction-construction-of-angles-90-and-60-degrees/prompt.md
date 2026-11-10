# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-4",
  "topic_key": "jss1-math-construction",
  "topic": "Construction",
  "subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees",
  "subtopic_title": "Construction of angles 90 and 60 degrees.",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees-po01",
        "source_performance_objective_index": 1,
        "text": "Construct angles 90 and 60 degrees"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "construction-of-angles-90-and-60-degrees-ao-construct-90-degree-angle",
          "text": "Construct 90 degree angles."
        },
        {
          "atomic_objective_id": "construction-of-angles-90-and-60-degrees-ao-construct-60-degree-angle",
          "text": "Construct 60 degree angles."
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
    "record_id": "ch14-b028",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.4 Sixty-degree angles",
      "h3": null
    },
    "content_text": "Here is a fun activity for you to do: Use a compass and draw a circle. Keep the position of the legs of the compass the same for the whole activity.\n\nMake a dot anywhere on the circumference of the circle.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-062.png\n\nPut the compass on the dot and start to make small arcs on the circumference of the circle:\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-063.png\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-064.png\n\nYou will find that you can fit in exactly six of these small arcs:\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-065.png\n\nYou know that a full turn (or revolution) is equal to $360^{\\circ}$, so if we join the centre of the circle to each one of the six small arcs, we form six angles of $60^{\\circ}$ each.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-066.png\n\nIf you are asked to construct an angle of $60^{\\circ}$, you simply do a part of the fun activity that you have done above.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b029",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.4 Sixty-degree angles",
      "h3": "Worked example 14.5: Constructing an angle of 60 degrees"
    },
    "content_text": "",
    "prompt_text": "You are given a line segment $BD$ as shown below. Construct $AB$ so that $C$ is a point on $AB$ and $A\\hat{B}C = 60^{\\circ}$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-067.png",
    "answer_text": "Step 1: Draw the first big arc.\n\nPut the compass point at point $B$ and draw a big arc. Label point $C$ where the arc crosses line segment $BD$. Keep the compass at the same width for Step 2.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-068.png\n\nStep 2: Draw a small arc that crosses the first big arc.\n\nKeep the compass at the same width as for Step 1. Put the compass point at point $C$ and make an arc to cross the big arc that you drew in Step 1.\n\nLabel the point of intersection $A$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-069.png\n\nStep 3: Complete the construction.\n\nUse a ruler and draw a line segment from point $B$ through point $A$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-070.png\n\nStep 4: Check your work.\n\nUse a protractor to measure $A\\hat{B}C$. The angle should be equal to $60^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b030",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.4 Sixty-degree angles",
      "h3": null
    },
    "content_text": "When you construct an angle of $60^{\\circ}$ you are actually constructing a triangle with three equal sides. In an equilateral triangle all three sides have equal lengths and each of the angles are equal to $60^{\\circ}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b031",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.4 Sixty-degree angles",
      "h3": null
    },
    "content_text": "Source image reference for the sixty-degree-angle construction context: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-071.png",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b032",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.4 Sixty-degree angles",
      "h3": "Exercise 14.5: Construct an angle of 60 degrees"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.5: Construct an angle of 60 degrees",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b032-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.4 Sixty-degree angles",
      "h3": "Exercise 14.5: Construct an angle of 60 degrees"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.5: Construct an angle of 60 degrees\n\n1. Draw line segment $CD$ as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-054.png\n\nConstruct $FC$ so that $F\\hat{C}D = 60^{\\circ}$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.5.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-072.png\n\nIf you have worked accurately, $F\\hat{C}D$ will be equal to $60^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b032-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.4 Sixty-degree angles",
      "h3": "Exercise 14.5: Construct an angle of 60 degrees"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.5: Construct an angle of 60 degrees\n\n2. Draw line segment $EF$ as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-056.png\n\nConstruct $DE$ so that $D\\hat{E}F = 60^{\\circ}$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.5.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-073.png\n\nIf you have worked accurately, $D\\hat{E}F$ will be equal to $60^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b032-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.4 Sixty-degree angles",
      "h3": "Exercise 14.5: Construct an angle of 60 degrees"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.5: Construct an angle of 60 degrees\n\n3. Draw line segment $MN$ as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-058.png\n\nConstruct $LM$ so that $L\\hat{M}N = 60^{\\circ}$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.5.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-074.png\n\nIf you have worked accurately, $L\\hat{M}N$ will be equal to $60^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b032-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.4 Sixty-degree angles",
      "h3": "Exercise 14.5: Construct an angle of 60 degrees"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.5: Construct an angle of 60 degrees\n\n4. Draw line segment $ST$ as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-060.png\n\nConstruct $PS$ so that $P\\hat{S}T = 60^{\\circ}$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.5.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-075.png\n\nIf you have worked accurately, $P\\hat{S}T$ will be equal to $60^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b033",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.5 Right angle",
      "h3": null
    },
    "content_text": "A right angle is an angle of 90 degrees. In real life we often see right angles. For example, the corners of your workbook are right angles, the corners of a door are right angles, and the corners of most tables are right angles.\n\nWhen you are asked to construct an angle of $90^{\\circ}$, you will again make use of the fun activity in which you made six small arcs on the circumference of a circle.\n\nIn this construction you will make only two arcs: you will mark where to form an angle of $60^{\\circ}$ and where to form an angle of $120^{\\circ}$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-076.png\n\nAn angle of $90^{\\circ}$ is exactly halfway between $60^{\\circ}$ and $120^{\\circ}$, so you will construct the one arm of the right angle exactly in the middle of the arcs for $60^{\\circ}$ and $120^{\\circ}$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-077.png",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b034",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.5 Right angle",
      "h3": "Worked example 14.6: Constructing a right angle"
    },
    "content_text": "",
    "prompt_text": "You are given a line segment $BD$ as shown below. Construct $AB$ so that $A\\hat{B}C = 90^{\\circ}$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-067.png",
    "answer_text": "Step 1: Draw the first big arc.\n\nPut the compass point at point $B$ and draw a big arc. Label point $C$ where the arc intersects line segment $BD$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-078.png\n\nStep 2: Draw the first small arc for an angle of $60^{\\circ}$.\n\nKeep the compass at the same width for the following two arcs. Put the compass on point $C$ and make an arc on the big arc that was drawn in Step 1.\n\nLabel the point of intersection $P$. Point $P$ shows the mark for an angle of $60^{\\circ}$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-079.png\n\nStep 3: Draw the second small arc for an angle of $120^{\\circ}$.\n\nThe compass should still be at exactly the same width as for the first big arc. Put the compass on point $P$ and make another arc on the big arc that was drawn in Step 1.\n\nLabel the point of intersection point $Q$. Point $Q$ shows the mark for an angle of $120^{\\circ}$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-080.png\n\nStep 4: Draw the first arc to find the right angle.\n\nWe want to find the line for an angle of $90^{\\circ}$ and we know that this line should be exactly in the middle between the arcs for the angles of $60^{\\circ}$ and $120^{\\circ}$.\n\nThe compass can now be less open, but it should stay at the same width for these next two arcs. Put the compass on point $P$ and make an arc as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-081.png\n\nStep 5: Draw the second arc to find the right angle.\n\nKeep the compass at the same width as for Step 4. Put the compass on point $Q$ and draw an arc. Label the point of intersection between the two arcs $A$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-082.png\n\nStep 6: Complete the construction.\n\nUse a ruler and draw a line segment from point $B$ and through point $A$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-083.png\n\nStep 7: Check your work.\n\nUse a protractor to measure $A\\hat{B}C$. The angle should be equal to $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b035",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.5 Right angle",
      "h3": "Exercise 14.6: Construct a right angle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.6: Construct a right angle",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b035-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.5 Right angle",
      "h3": "Exercise 14.6: Construct a right angle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.6: Construct a right angle\n\n1. Draw line segment $CD$ as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-054.png\n\nConstruct $FC$ so that $F\\hat{C}D = 90^{\\circ}$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.6.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-084.png\n\nIf you have worked accurately, $F\\hat{C}D$ will be equal to $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b035-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.5 Right angle",
      "h3": "Exercise 14.6: Construct a right angle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.6: Construct a right angle\n\n2. Draw line segment $EF$ as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-056.png\n\nConstruct $DE$ so that $D\\hat{E}F = 90^{\\circ}$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.6.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-085.png\n\nIf you have worked accurately, $D\\hat{E}F$ will be equal to $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b035-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.5 Right angle",
      "h3": "Exercise 14.6: Construct a right angle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.6: Construct a right angle\n\n3. Draw line segment $MN$ as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-0858.png\n\nConstruct $LM$ so that $L\\hat{M}N = 90^{\\circ}$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.6.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-086.png\n\nIf you have worked accurately, $L\\hat{M}N$ will be equal to $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b035-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.5 Right angle",
      "h3": "Exercise 14.6: Construct a right angle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.6: Construct a right angle\n\n4. Draw line segment $ST$ as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-060.png\n\nConstruct $PS$ so that $P\\hat{S}T = 90^{\\circ}$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.6.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-087.png\n\nIf you have worked accurately, $P\\hat{S}T$ will be equal to $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
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
  "subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees",
  "subtopic_title": "Construction of angles 90 and 60 degrees.",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees-po01",
        "source_performance_objective_index": 1,
        "text": "Construct angles 90 and 60 degrees"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "construction-of-angles-90-and-60-degrees-ao-construct-90-degree-angle",
          "text": "Construct 90 degree angles."
        },
        {
          "atomic_objective_id": "construction-of-angles-90-and-60-degrees-ao-construct-60-degree-angle",
          "text": "Construct 60 degree angles."
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
    "record_id": "ch14-b028",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.4 Sixty-degree angles",
      "h3": null
    },
    "content_text": "Here is a fun activity for you to do: Use a compass and draw a circle. Keep the position of the legs of the compass the same for the whole activity.\n\nMake a dot anywhere on the circumference of the circle.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-062.png\n\nPut the compass on the dot and start to make small arcs on the circumference of the circle:\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-063.png\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-064.png\n\nYou will find that you can fit in exactly six of these small arcs:\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-065.png\n\nYou know that a full turn (or revolution) is equal to $360^{\\circ}$, so if we join the centre of the circle to each one of the six small arcs, we form six angles of $60^{\\circ}$ each.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-066.png\n\nIf you are asked to construct an angle of $60^{\\circ}$, you simply do a part of the fun activity that you have done above.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b029",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.4 Sixty-degree angles",
      "h3": "Worked example 14.5: Constructing an angle of 60 degrees"
    },
    "content_text": "",
    "prompt_text": "You are given a line segment $BD$ as shown below. Construct $AB$ so that $C$ is a point on $AB$ and $A\\hat{B}C = 60^{\\circ}$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-067.png",
    "answer_text": "Step 1: Draw the first big arc.\n\nPut the compass point at point $B$ and draw a big arc. Label point $C$ where the arc crosses line segment $BD$. Keep the compass at the same width for Step 2.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-068.png\n\nStep 2: Draw a small arc that crosses the first big arc.\n\nKeep the compass at the same width as for Step 1. Put the compass point at point $C$ and make an arc to cross the big arc that you drew in Step 1.\n\nLabel the point of intersection $A$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-069.png\n\nStep 3: Complete the construction.\n\nUse a ruler and draw a line segment from point $B$ through point $A$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-070.png\n\nStep 4: Check your work.\n\nUse a protractor to measure $A\\hat{B}C$. The angle should be equal to $60^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b030",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.4 Sixty-degree angles",
      "h3": null
    },
    "content_text": "When you construct an angle of $60^{\\circ}$ you are actually constructing a triangle with three equal sides. In an equilateral triangle all three sides have equal lengths and each of the angles are equal to $60^{\\circ}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b031",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.4 Sixty-degree angles",
      "h3": null
    },
    "content_text": "Source image reference for the sixty-degree-angle construction context: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-071.png",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b032",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.4 Sixty-degree angles",
      "h3": "Exercise 14.5: Construct an angle of 60 degrees"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.5: Construct an angle of 60 degrees",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b032-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.4 Sixty-degree angles",
      "h3": "Exercise 14.5: Construct an angle of 60 degrees"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.5: Construct an angle of 60 degrees\n\n1. Draw line segment $CD$ as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-054.png\n\nConstruct $FC$ so that $F\\hat{C}D = 60^{\\circ}$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.5.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-072.png\n\nIf you have worked accurately, $F\\hat{C}D$ will be equal to $60^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b032-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.4 Sixty-degree angles",
      "h3": "Exercise 14.5: Construct an angle of 60 degrees"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.5: Construct an angle of 60 degrees\n\n2. Draw line segment $EF$ as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-056.png\n\nConstruct $DE$ so that $D\\hat{E}F = 60^{\\circ}$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.5.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-073.png\n\nIf you have worked accurately, $D\\hat{E}F$ will be equal to $60^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b032-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.4 Sixty-degree angles",
      "h3": "Exercise 14.5: Construct an angle of 60 degrees"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.5: Construct an angle of 60 degrees\n\n3. Draw line segment $MN$ as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-058.png\n\nConstruct $LM$ so that $L\\hat{M}N = 60^{\\circ}$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.5.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-074.png\n\nIf you have worked accurately, $L\\hat{M}N$ will be equal to $60^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b032-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.4 Sixty-degree angles",
      "h3": "Exercise 14.5: Construct an angle of 60 degrees"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.5: Construct an angle of 60 degrees\n\n4. Draw line segment $ST$ as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-060.png\n\nConstruct $PS$ so that $P\\hat{S}T = 60^{\\circ}$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.5.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-075.png\n\nIf you have worked accurately, $P\\hat{S}T$ will be equal to $60^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b033",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.5 Right angle",
      "h3": null
    },
    "content_text": "A right angle is an angle of 90 degrees. In real life we often see right angles. For example, the corners of your workbook are right angles, the corners of a door are right angles, and the corners of most tables are right angles.\n\nWhen you are asked to construct an angle of $90^{\\circ}$, you will again make use of the fun activity in which you made six small arcs on the circumference of a circle.\n\nIn this construction you will make only two arcs: you will mark where to form an angle of $60^{\\circ}$ and where to form an angle of $120^{\\circ}$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-076.png\n\nAn angle of $90^{\\circ}$ is exactly halfway between $60^{\\circ}$ and $120^{\\circ}$, so you will construct the one arm of the right angle exactly in the middle of the arcs for $60^{\\circ}$ and $120^{\\circ}$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-077.png",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b034",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.5 Right angle",
      "h3": "Worked example 14.6: Constructing a right angle"
    },
    "content_text": "",
    "prompt_text": "You are given a line segment $BD$ as shown below. Construct $AB$ so that $A\\hat{B}C = 90^{\\circ}$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-067.png",
    "answer_text": "Step 1: Draw the first big arc.\n\nPut the compass point at point $B$ and draw a big arc. Label point $C$ where the arc intersects line segment $BD$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-078.png\n\nStep 2: Draw the first small arc for an angle of $60^{\\circ}$.\n\nKeep the compass at the same width for the following two arcs. Put the compass on point $C$ and make an arc on the big arc that was drawn in Step 1.\n\nLabel the point of intersection $P$. Point $P$ shows the mark for an angle of $60^{\\circ}$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-079.png\n\nStep 3: Draw the second small arc for an angle of $120^{\\circ}$.\n\nThe compass should still be at exactly the same width as for the first big arc. Put the compass on point $P$ and make another arc on the big arc that was drawn in Step 1.\n\nLabel the point of intersection point $Q$. Point $Q$ shows the mark for an angle of $120^{\\circ}$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-080.png\n\nStep 4: Draw the first arc to find the right angle.\n\nWe want to find the line for an angle of $90^{\\circ}$ and we know that this line should be exactly in the middle between the arcs for the angles of $60^{\\circ}$ and $120^{\\circ}$.\n\nThe compass can now be less open, but it should stay at the same width for these next two arcs. Put the compass on point $P$ and make an arc as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-081.png\n\nStep 5: Draw the second arc to find the right angle.\n\nKeep the compass at the same width as for Step 4. Put the compass on point $Q$ and draw an arc. Label the point of intersection between the two arcs $A$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-082.png\n\nStep 6: Complete the construction.\n\nUse a ruler and draw a line segment from point $B$ and through point $A$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-083.png\n\nStep 7: Check your work.\n\nUse a protractor to measure $A\\hat{B}C$. The angle should be equal to $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b035",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.5 Right angle",
      "h3": "Exercise 14.6: Construct a right angle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.6: Construct a right angle",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b035-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.5 Right angle",
      "h3": "Exercise 14.6: Construct a right angle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.6: Construct a right angle\n\n1. Draw line segment $CD$ as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-054.png\n\nConstruct $FC$ so that $F\\hat{C}D = 90^{\\circ}$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.6.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-084.png\n\nIf you have worked accurately, $F\\hat{C}D$ will be equal to $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b035-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.5 Right angle",
      "h3": "Exercise 14.6: Construct a right angle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.6: Construct a right angle\n\n2. Draw line segment $EF$ as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-056.png\n\nConstruct $DE$ so that $D\\hat{E}F = 90^{\\circ}$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.6.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-085.png\n\nIf you have worked accurately, $D\\hat{E}F$ will be equal to $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b035-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.5 Right angle",
      "h3": "Exercise 14.6: Construct a right angle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.6: Construct a right angle\n\n3. Draw line segment $MN$ as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-0858.png\n\nConstruct $LM$ so that $L\\hat{M}N = 90^{\\circ}$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.6.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-086.png\n\nIf you have worked accurately, $L\\hat{M}N$ will be equal to $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
  },
  {
    "record_id": "ch14-b035-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.5 Right angle",
      "h3": "Exercise 14.6: Construct a right angle"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.6: Construct a right angle\n\n4. Draw line segment $ST$ as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-060.png\n\nConstruct $PS$ so that $P\\hat{S}T = 90^{\\circ}$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.6.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-087.png\n\nIf you have worked accurately, $P\\hat{S}T$ will be equal to $90^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-construction-construction-of-angles-90-and-60-degrees"
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
