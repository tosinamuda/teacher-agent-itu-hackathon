# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-4",
  "topic_key": "jss1-math-construction",
  "topic": "Construction",
  "subtopic_id": "jss1-math-construction-bisection-of-a-given-line-segment",
  "subtopic_title": "Bisection of a given line segment.",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-construction-bisection-of-a-given-line-segment-po01",
        "source_performance_objective_index": 1,
        "text": "Bisect a given line segment"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "bisection-of-a-given-line-segment-ao-bisect-line-segment",
          "text": "Bisect a given line segment."
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
    "record_id": "ch14-b021",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.3 Line bisector",
      "h3": null
    },
    "content_text": "A line segment is part of a straight line. A line segment has a beginning and an end. When we are asked to **bisect** a line segment, we are asked to divide the line segment into two equal parts.\n\nThe **bisector** is the line segment that divides the given line segment into two equal parts.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-bisection-of-a-given-line-segment"
  },
  {
    "record_id": "ch14-b022",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.3 Line bisector",
      "h3": null
    },
    "content_text": "**bisect** When we bisect a line segment or an angle, we divide the line segment or the angle exactly in half.\n\n**bisector** A bisector is the line segment that divides the given line segment into two equal parts.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-bisection-of-a-given-line-segment"
  },
  {
    "record_id": "ch14-b023",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.3 Line bisector",
      "h3": "Worked example 14.4: Bisecting a line segment"
    },
    "content_text": "",
    "prompt_text": "You are given line segment $AB$ as shown in the diagram below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-049.png\n\nBisect $AB$ and label the bisector $PQ$.",
    "answer_text": "Step 1: Draw the first set of two arcs.\n\nOpen the compass so that the distance between the two points is more than half of the length of $AB$. Test this on line $AB$.\n\nPut the compass on point $A$ (the blue dot) and draw two arcs as shown. One arc is above $AB$ and one arc is below $AB$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-050.png\n\nStep 2: Draw the second set of two arcs.\n\nKeep the compass open at exactly the same width as for Step 1.\n\nPut the compass on point $B$ (the orange dot) and draw two arcs as shown. One arc is above $AB$ and one arc is below $AB$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-051.png\n\nStep 3: Draw the bisector.\n\nLabel the points where the arcs intersect as point $P$ and point $Q$.\n\nUse a ruler and draw a line through point $P$ and point $Q$. $PQ$ is the bisector of line segment $AB$ at point $R$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-052.png\n\nStep 4: Check your work.\n\nMeasure the lengths of the two parts of line segment $AB$. If $AR$ is equal to $RB$, your construction is accurate.",
    "primary_subtopic_id": "jss1-math-construction-bisection-of-a-given-line-segment"
  },
  {
    "record_id": "ch14-b024",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.3 Line bisector",
      "h3": null
    },
    "content_text": "Take note that if you measure the angles at $R$, you will find they are $90^{\\circ}$. We say that the bisector is perpendicular to the original line segment. The symbol for perpendicular is $\\perp$, so we write: $PQ \\perp AB$.\n\nWhen we do a construction to bisect a line, the bisector is always perpendicular to the line. This means we can call the bisector a \"perpendicular line bisector\".",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-bisection-of-a-given-line-segment"
  },
  {
    "record_id": "ch14-b025",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.3 Line bisector",
      "h3": null
    },
    "content_text": "If you find it easier, you may draw two bigger arcs instead of four smaller arcs when you construct the bisector of a line segment, as shown in the diagram below.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-bisection-of-a-given-line-segment"
  },
  {
    "record_id": "ch14-b026",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.3 Line bisector",
      "h3": null
    },
    "content_text": "Source image reference for drawing two bigger arcs instead of four smaller arcs when bisecting a line segment: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-053.png",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-bisection-of-a-given-line-segment"
  },
  {
    "record_id": "ch14-b027",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.3 Line bisector",
      "h3": "Exercise 14.4: Bisect a line segment"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.4: Bisect a line segment",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-bisection-of-a-given-line-segment"
  },
  {
    "record_id": "ch14-b027-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.3 Line bisector",
      "h3": "Exercise 14.4: Bisect a line segment"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.4: Bisect a line segment\n\n1. Draw line segment $CD$ as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-054.png\n\nBisect the line segment and label the bisector $PQ$.\n\nRemember to check your work.",
    "answer_text": "Follow the Steps as shown in Worked example 14.4.\n\nSource solution image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-055.png\n\nIf you have worked accurately, the length of line segment $CR$ will be the same as the length of line segment $RD$.",
    "primary_subtopic_id": "jss1-math-construction-bisection-of-a-given-line-segment"
  },
  {
    "record_id": "ch14-b027-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.3 Line bisector",
      "h3": "Exercise 14.4: Bisect a line segment"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.4: Bisect a line segment\n\n2. Draw line segment $EF$ as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-056.png\n\nBisect the line segment and label the bisector $PQ$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.4.\n\nSource solution image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-057.png\n\nIf you have worked accurately, the length of line segment $ER$ will be the same as the length of line segment $RF$.",
    "primary_subtopic_id": "jss1-math-construction-bisection-of-a-given-line-segment"
  },
  {
    "record_id": "ch14-b027-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.3 Line bisector",
      "h3": "Exercise 14.4: Bisect a line segment"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.4: Bisect a line segment\n\n3. Draw line segment $MN$ as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-058.png\n\nBisect the line segment and label the bisector $PQ$. Remember to check your work.",
    "answer_text": "Follow the Steps as shown in Worked example 14.4.\n\nSource solution image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-059.png\n\nIf you have worked accurately, the length of line segment $MR$ will be the same as the length of line segment $RN$.",
    "primary_subtopic_id": "jss1-math-construction-bisection-of-a-given-line-segment"
  },
  {
    "record_id": "ch14-b027-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.3 Line bisector",
      "h3": "Exercise 14.4: Bisect a line segment"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.4: Bisect a line segment\n\n4. Draw line segment $ST$ as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-060.png\n\nBisect the line segment and label the bisector $PQ$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.4.\n\nSource solution image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-061.png\n\nIf you have worked accurately, the length of line segment $SR$ will be the same as the length of line segment $RT$.",
    "primary_subtopic_id": "jss1-math-construction-bisection-of-a-given-line-segment"
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
  "subtopic_id": "jss1-math-construction-bisection-of-a-given-line-segment",
  "subtopic_title": "Bisection of a given line segment.",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-construction-bisection-of-a-given-line-segment-po01",
        "source_performance_objective_index": 1,
        "text": "Bisect a given line segment"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "bisection-of-a-given-line-segment-ao-bisect-line-segment",
          "text": "Bisect a given line segment."
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
    "record_id": "ch14-b021",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.3 Line bisector",
      "h3": null
    },
    "content_text": "A line segment is part of a straight line. A line segment has a beginning and an end. When we are asked to **bisect** a line segment, we are asked to divide the line segment into two equal parts.\n\nThe **bisector** is the line segment that divides the given line segment into two equal parts.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-bisection-of-a-given-line-segment"
  },
  {
    "record_id": "ch14-b022",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.3 Line bisector",
      "h3": null
    },
    "content_text": "**bisect** When we bisect a line segment or an angle, we divide the line segment or the angle exactly in half.\n\n**bisector** A bisector is the line segment that divides the given line segment into two equal parts.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-bisection-of-a-given-line-segment"
  },
  {
    "record_id": "ch14-b023",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.3 Line bisector",
      "h3": "Worked example 14.4: Bisecting a line segment"
    },
    "content_text": "",
    "prompt_text": "You are given line segment $AB$ as shown in the diagram below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-049.png\n\nBisect $AB$ and label the bisector $PQ$.",
    "answer_text": "Step 1: Draw the first set of two arcs.\n\nOpen the compass so that the distance between the two points is more than half of the length of $AB$. Test this on line $AB$.\n\nPut the compass on point $A$ (the blue dot) and draw two arcs as shown. One arc is above $AB$ and one arc is below $AB$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-050.png\n\nStep 2: Draw the second set of two arcs.\n\nKeep the compass open at exactly the same width as for Step 1.\n\nPut the compass on point $B$ (the orange dot) and draw two arcs as shown. One arc is above $AB$ and one arc is below $AB$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-051.png\n\nStep 3: Draw the bisector.\n\nLabel the points where the arcs intersect as point $P$ and point $Q$.\n\nUse a ruler and draw a line through point $P$ and point $Q$. $PQ$ is the bisector of line segment $AB$ at point $R$.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-052.png\n\nStep 4: Check your work.\n\nMeasure the lengths of the two parts of line segment $AB$. If $AR$ is equal to $RB$, your construction is accurate.",
    "primary_subtopic_id": "jss1-math-construction-bisection-of-a-given-line-segment"
  },
  {
    "record_id": "ch14-b024",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.3 Line bisector",
      "h3": null
    },
    "content_text": "Take note that if you measure the angles at $R$, you will find they are $90^{\\circ}$. We say that the bisector is perpendicular to the original line segment. The symbol for perpendicular is $\\perp$, so we write: $PQ \\perp AB$.\n\nWhen we do a construction to bisect a line, the bisector is always perpendicular to the line. This means we can call the bisector a \"perpendicular line bisector\".",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-bisection-of-a-given-line-segment"
  },
  {
    "record_id": "ch14-b025",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.3 Line bisector",
      "h3": null
    },
    "content_text": "If you find it easier, you may draw two bigger arcs instead of four smaller arcs when you construct the bisector of a line segment, as shown in the diagram below.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-bisection-of-a-given-line-segment"
  },
  {
    "record_id": "ch14-b026",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.3 Line bisector",
      "h3": null
    },
    "content_text": "Source image reference for drawing two bigger arcs instead of four smaller arcs when bisecting a line segment: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-053.png",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-bisection-of-a-given-line-segment"
  },
  {
    "record_id": "ch14-b027",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.3 Line bisector",
      "h3": "Exercise 14.4: Bisect a line segment"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.4: Bisect a line segment",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-construction-bisection-of-a-given-line-segment"
  },
  {
    "record_id": "ch14-b027-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.3 Line bisector",
      "h3": "Exercise 14.4: Bisect a line segment"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.4: Bisect a line segment\n\n1. Draw line segment $CD$ as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-054.png\n\nBisect the line segment and label the bisector $PQ$.\n\nRemember to check your work.",
    "answer_text": "Follow the Steps as shown in Worked example 14.4.\n\nSource solution image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-055.png\n\nIf you have worked accurately, the length of line segment $CR$ will be the same as the length of line segment $RD$.",
    "primary_subtopic_id": "jss1-math-construction-bisection-of-a-given-line-segment"
  },
  {
    "record_id": "ch14-b027-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.3 Line bisector",
      "h3": "Exercise 14.4: Bisect a line segment"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.4: Bisect a line segment\n\n2. Draw line segment $EF$ as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-056.png\n\nBisect the line segment and label the bisector $PQ$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.4.\n\nSource solution image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-057.png\n\nIf you have worked accurately, the length of line segment $ER$ will be the same as the length of line segment $RF$.",
    "primary_subtopic_id": "jss1-math-construction-bisection-of-a-given-line-segment"
  },
  {
    "record_id": "ch14-b027-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.3 Line bisector",
      "h3": "Exercise 14.4: Bisect a line segment"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.4: Bisect a line segment\n\n3. Draw line segment $MN$ as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-058.png\n\nBisect the line segment and label the bisector $PQ$. Remember to check your work.",
    "answer_text": "Follow the Steps as shown in Worked example 14.4.\n\nSource solution image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-059.png\n\nIf you have worked accurately, the length of line segment $MR$ will be the same as the length of line segment $RN$.",
    "primary_subtopic_id": "jss1-math-construction-bisection-of-a-given-line-segment"
  },
  {
    "record_id": "ch14-b027-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 14: Constructions",
      "h2": "14.3 Line bisector",
      "h3": "Exercise 14.4: Bisect a line segment"
    },
    "content_text": "",
    "prompt_text": "### Exercise 14.4: Bisect a line segment\n\n4. Draw line segment $ST$ as shown below.\n\nSource image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-060.png\n\nBisect the line segment and label the bisector $PQ$.",
    "answer_text": "Follow the Steps as shown in Worked example 14.4.\n\nSource solution image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-061.png\n\nIf you have worked accurately, the length of line segment $SR$ will be the same as the length of line segment $RT$.",
    "primary_subtopic_id": "jss1-math-construction-bisection-of-a-given-line-segment"
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
