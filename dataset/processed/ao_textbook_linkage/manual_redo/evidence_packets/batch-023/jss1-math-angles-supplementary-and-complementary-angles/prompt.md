# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-4",
  "topic_key": "jss1-math-angles",
  "topic": "Angles",
  "subtopic_id": "jss1-math-angles-supplementary-and-complementary-angles",
  "subtopic_title": "Supplementary and complementary angles",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-angles-supplementary-and-complementary-angles-po01",
        "source_performance_objective_index": 1,
        "text": "Define supplementary angles and complementary angles"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "supplementary-and-complementary-angles-ao-define-supplementary-angles",
          "text": "Define supplementary angles."
        },
        {
          "atomic_objective_id": "supplementary-and-complementary-angles-ao-define-complementary-angles",
          "text": "Define complementary angles."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-angles-supplementary-and-complementary-angles-po02",
        "source_performance_objective_index": 2,
        "text": "Calculate the supplement or complement of a given angle"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "supplementary-and-complementary-angles-ao-calculate-supplement",
          "text": "Calculate the supplement of a given angle."
        },
        {
          "atomic_objective_id": "supplementary-and-complementary-angles-ao-calculate-complement",
          "text": "Calculate the complement of a given angle."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch15-b021",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Angles on a straight line"
    },
    "content_text": "A straight line is also called a straight angle. A straight angle is equal to $180^{\\circ}$. If a straight line is formed by more than one angle, the sum of those angles will be $180^{\\circ}$. We say the angles are **supplementary angles**.\n\nIn the first diagram, the two angles are supplementary angles, because they form a straight line:\n\n$$\n\\hat{P}_1 + \\hat{P}_2 = 180^{\\circ}\n$$\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-024.png]\n\nWe can also say that the two angles in the diagram above are **adjacent angles**. Adjacent angles are next to each other. Two adjacent angles share the same vertex and they also share one common arm.\n\nIn the second diagram below, $\\hat{M}_1$ and $\\hat{M}_2$ have the same vertex, but they do not share a common arm.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-025.png]\n\n$\\hat{M}_1$ and $\\hat{M}_2$ are not adjacent angles, because they do not share a common arm.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b022",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Angles on a straight line"
    },
    "content_text": "Adjacent angles do not always have to be supplementary. In the diagram below the two angles are adjacent, but they do not add up to $180^{\\circ}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b023",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Angles on a straight line"
    },
    "content_text": "Source diagram for the note above, showing adjacent angles that do not add up to $180^{\\circ}$.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-026.png]",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b024",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Angles on a straight line"
    },
    "content_text": "**supplementary angles** Two (or more) angles are supplementary if they add up to $180^{\\circ}$.\n\n**adjacent angles** Adjacent angles are next to each other. Two adjacent angles share the same vertex and a common arm.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b025",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Worked example 15.8: Calculating angles on a straight line"
    },
    "content_text": "",
    "prompt_text": "Consider the diagram given below. You are given the following information:\n\n- $\\overset{\\leftrightarrow}{ST}$ is a straight line\n- $a = 65^{\\circ}$\n- $b = 68^{\\circ}$\n- $c = x^{\\circ}$\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_050.png\n\nWhat is the value of $x$?",
    "answer_text": "Step 1: Read the given information and consider the diagram carefully.\n\nBegin the answer by writing down the facts you know.\n\nThe angles must have a sum of $180^{\\circ}$, because they form a straight line.\n\n$$\na + b + c = 180^{\\circ}\n$$\n\nStep 2: Substitute all the values, including the unknown value, $x$.\n\n$$\n\\begin{align}\na + b + c & = 180^{\\circ} \\\\\n65^{\\circ} + 68^{\\circ} + x & = 180^{\\circ} \\\\\n\\end{align}\n$$\n\nStep 3: Solve the equation.\n\n$$\n\\begin{align}\na + b + c & = 180^{\\circ} \\\\\n65^{\\circ} + 68^{\\circ} + x & = 180^{\\circ} \\\\\n133^{\\circ} + x & = 180^{\\circ}\\\\\nx & = 180^{\\circ} - 133^{\\circ}\\\\\n\\therefore x & = 47^{\\circ} \\\\\n\\end{align}\n$$\n\nYou could now complete the diagram by replacing the $x$.\n\nCompleted diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-1_029.png",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b026",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Angles on a straight line"
    },
    "content_text": "When we refer to lines and line segments we can use different notations:\n\n- $\\overline{EF}$ means the line segment from point $E$ to point $F$.\n- $\\overset{\\leftrightarrow}{EF}$ means the line through points $E$ and $F$.\n- Most of the time we simply write $EF$ for the line through point $E$ and point $F$ and also for the line segment from point $E$ to point $F$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b027",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Exercise 15.3: Calculate angles on a straight line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.3: Calculate angles on a straight line",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b027-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Exercise 15.3: Calculate angles on a straight line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.3: Calculate angles on a straight line\n\n1. $YZ$ is a straight line, with angles as shown in the diagram below.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-027.png\n\nWhat is the value of $x$?",
    "answer_text": "The angles must have a sum of $180^{\\circ}$, because they form a straight line.\n\n$$\n\\begin{align}\n90^{\\circ} + x & = 180^{\\circ} \\\\\n\\therefore x & = 90^{\\circ} \\\\\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b027-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Exercise 15.3: Calculate angles on a straight line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.3: Calculate angles on a straight line\n\n2. $YZ$ is a straight line, with angles as shown below.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_007.png\n\nWhat is the value of $x$?",
    "answer_text": "The angles must have a sum of $180^{\\circ}$, because they form a straight line.\n\n$$\n\\begin{align}\nx + 56^{\\circ} + 63^{\\circ} & = 180^{\\circ} \\\\\nx + 119^{\\circ} & = 180^{\\circ}\\\\\n\\therefore x & = 61^{\\circ} \\\\\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b027-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Exercise 15.3: Calculate angles on a straight line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.3: Calculate angles on a straight line\n\n3. $ST$ is a straight line, with angles as shown below.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_035.png\n\nWhat is the value of $x$?",
    "answer_text": "The angles must have a sum of $180^{\\circ}$, because they form a straight line.\n\n$$\n\\begin{align}\nx + 59^{\\circ} + 74^{\\circ} & = 180^{\\circ} \\\\\nx + 133^{\\circ} & = 180^{\\circ}\\\\\n\\therefore x & = 47^{\\circ} \\\\\n\\end{align}\n$$\n\nCompleted diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-1_031.png",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b027-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Exercise 15.3: Calculate angles on a straight line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.3: Calculate angles on a straight line\n\n4. Examine the diagram below, and answer the two questions that follow.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_027.png\n\n1. Calculate $x$.\n2. What type of angle is represented by $x$?",
    "answer_text": "The angles must have a sum of $180^{\\circ}$, because they form a straight line.\n\n$$\n\\begin{align}\n37^{\\circ} + x + 55^{\\circ} & = 180^{\\circ} \\\\\n92^{\\circ} + x & = 180^{\\circ}\\\\\n\\therefore x & = 88^{\\circ} \\\\\n\\end{align}\n$$\n\nCompleted diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-1_026.png\n\nThe angle represented by $x$ is an acute angle.",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b027-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Exercise 15.3: Calculate angles on a straight line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.3: Calculate angles on a straight line\n\n5. Examine the diagram below, and answer the questions that follow.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_008.png\n\n1. Calculate $x$.\n2. What type of angle is represented by $x$?",
    "answer_text": "The angles must have a sum of $180^{\\circ}$, because they form a straight line.\n\n$$\n\\begin{align}\nx + 58^{\\circ} + 30^{\\circ} & = 180^{\\circ} \\\\\nx + 88^{\\circ} & = 180^{\\circ}\\\\\n\\therefore x & = 92^{\\circ} \\\\\n\\end{align}\n$$\n\nCompleted diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-1_050.png\n\nThe angle represented by $x$ is an obtuse angle.",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b027-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Exercise 15.3: Calculate angles on a straight line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.3: Calculate angles on a straight line\n\n6. Examine the diagram below, and answer the two questions that follow.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_012.png\n\n1. Calculate $x$.\n2. What type of angle is represented by $x$?",
    "answer_text": "The angles must have a sum of $180^{\\circ}$, because they form a straight line.\n\n$$\n\\begin{align}\nx + 78^{\\circ} + 40^{\\circ} & = 180^{\\circ} \\\\\nx + 118^{\\circ} & = 180^{\\circ} \\\\\n\\therefore x & = 62^{\\circ} \\\\\n\\end{align}\n$$\n\nCompleted diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-1_057.png\n\nThe angle represented by $x$ is an acute angle.",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b027-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Exercise 15.3: Calculate angles on a straight line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.3: Calculate angles on a straight line\n\n7. In the diagram below, line $YZ$ is a straight line with angles labelled above and below it.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_016.png\n\nFind the values of $x$ and $y$, giving reasons for your answer. (Remember to check your answers.)",
    "answer_text": "All of the angles above $YZ$ add up to $180^{\\circ}$:\n\n$$\n\\begin{align}\nx + 65^{\\circ} + 60^{\\circ} & = 180^{\\circ} \\quad(\\text{angles on a straight line}) \\\\\nx + 125^{\\circ} & = 180^{\\circ}\\\\\nx & = 180^{\\circ} - 125^{\\circ}\\\\\n\\therefore x & = 55^{\\circ} \\\\\n\\end{align}\n$$\n\nIn the same way, all of the angles below $YZ$ add up to $180^{\\circ}$:\n\n$$\n\\begin{align}\n26^{\\circ} + 82^{\\circ} + 35^{\\circ} + y & = 180^{\\circ} \\quad(\\text{angles on a straight line}) \\\\\n143^{\\circ} + y & = 180^{\\circ} \\\\\ny & = 180^{\\circ} - 143^{\\circ} \\\\\n\\therefore y & = 37^{\\circ} \\\\\n\\end{align}\n$$\n\nCompleted diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-1_007.png\n\nThe angles in a full turn (revolution) must add up to $360^{\\circ}$. This is a good way to check your answers:\n\n$$\n\\begin{align}\n55^{\\circ} + 65^{\\circ} + 60^{\\circ} + 26^{\\circ} + 82^{\\circ} + 35^{\\circ} + 37^{\\circ} & = 360^{\\circ} \\\\\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b027-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Exercise 15.3: Calculate angles on a straight line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.3: Calculate angles on a straight line\n\n8. In the diagram below, $YZ$ is a straight line with angles labelled above and below it.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_056.png\n\nFind the values of $x$ and $y$, giving reasons for your answer. (Remember to check your answers.)",
    "answer_text": "All of the angles above $YZ$ add up to $180^{\\circ}$:\n\n$$\n\\begin{align}\n15^{\\circ} + 141^{\\circ} + x & = 180^{\\circ}\\quad(\\text{angles on a straight line}) \\\\\n156^{\\circ} + x & = 180^{\\circ}\\\\\nx &= 180^{\\circ} - 156^{\\circ}\\\\\n\\therefore x & = 24^{\\circ} \\\\\n\\end{align}\n$$\n\nIn the same way, all of the angles below $YZ$ add up to $180^{\\circ}$:\n\n$$\n\\begin{align}\n44^{\\circ} + y + 45^{\\circ} + 75^{\\circ} & = 180^{\\circ} \\quad(\\text{angles on a straight line}) \\\\\n164^{\\circ} + y  & = 180^{\\circ}\\\\\ny & = 180^{\\circ} - 164^{\\circ}\\\\\n\\therefore y & = 16^{\\circ} \\\\\n\\end{align}\n$$\n\nHere is the completed diagram, with all of the angle values labelled:\n\nCompleted diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-1_038.png\n\nCheck your answers:\n\n$$\n\\begin{align}\n15^{\\circ} + 141^{\\circ} + 24^{\\circ} + 44^{\\circ} + 16^{\\circ} + 45^{\\circ} + 75^{\\circ} & = 360^{\\circ} \\\\\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b028",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Angles on a straight line"
    },
    "content_text": "You will not usually be asked to redraw the diagram to give the missing angle size.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b063-i03c",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.4 Practical applications",
      "h3": "Exercise 15.11: Solve real-world problems with angles"
    },
    "content_text": "Source math retained:\nx\nP\\hat{R}S\n120^{\\circ}\nRS\nTU\nPQ\nP\\hat{R}S\nR\\hat{T}U\nR\\hat{T}U\n120^{\\circ}\nR\\hat{T}U\nU\\hat{T}Q\n180^{\\circ}\nU\\hat{T}Q\nx\n\\begin{align} x + 120^{\\circ} & = 180^{\\circ} \\\\ \\therefore x & = 60^{\\circ} \\end{align}\nx\n60^{\\circ}",
    "prompt_text": "### Exercise 15.11: Solve real-world problems with angles\n\n3c. In the diagram below, what should the size of the angle marked $x$ be if $P\\hat{R}S$ is equal to $120^{\\circ}$?\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-039.png",
    "answer_text": "$RS$ and $TU$ are parallel lines and $PQ$ is a transversal.\n\n$P\\hat{R}S$ and $R\\hat{T}U$ are corresponding angles, which means they are equal. Therefore, $R\\hat{T}U = 120^{\\circ}$.\n\n$R\\hat{T}U$ and $U\\hat{T}Q$ are on a straight line, so they add up to $180^{\\circ}$. $U\\hat{T}Q$ is $x$.\n\n$$\n\begin{align}\nx + 120^{\\circ} &= 180^{\\circ} \\\n\therefore x &= 60^{\\circ}\n\\end{align}\n$$\n\nThe size of the angle marked $x$ is $60^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-vertically-opposite-adjacent-alternate-and-corresponding-angles"
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
  "subtopic_id": "jss1-math-angles-supplementary-and-complementary-angles",
  "subtopic_title": "Supplementary and complementary angles",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-angles-supplementary-and-complementary-angles-po01",
        "source_performance_objective_index": 1,
        "text": "Define supplementary angles and complementary angles"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "supplementary-and-complementary-angles-ao-define-supplementary-angles",
          "text": "Define supplementary angles."
        },
        {
          "atomic_objective_id": "supplementary-and-complementary-angles-ao-define-complementary-angles",
          "text": "Define complementary angles."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-angles-supplementary-and-complementary-angles-po02",
        "source_performance_objective_index": 2,
        "text": "Calculate the supplement or complement of a given angle"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "supplementary-and-complementary-angles-ao-calculate-supplement",
          "text": "Calculate the supplement of a given angle."
        },
        {
          "atomic_objective_id": "supplementary-and-complementary-angles-ao-calculate-complement",
          "text": "Calculate the complement of a given angle."
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
    "record_id": "ch15-b021",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Angles on a straight line"
    },
    "content_text": "A straight line is also called a straight angle. A straight angle is equal to $180^{\\circ}$. If a straight line is formed by more than one angle, the sum of those angles will be $180^{\\circ}$. We say the angles are **supplementary angles**.\n\nIn the first diagram, the two angles are supplementary angles, because they form a straight line:\n\n$$\n\\hat{P}_1 + \\hat{P}_2 = 180^{\\circ}\n$$\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-024.png]\n\nWe can also say that the two angles in the diagram above are **adjacent angles**. Adjacent angles are next to each other. Two adjacent angles share the same vertex and they also share one common arm.\n\nIn the second diagram below, $\\hat{M}_1$ and $\\hat{M}_2$ have the same vertex, but they do not share a common arm.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-025.png]\n\n$\\hat{M}_1$ and $\\hat{M}_2$ are not adjacent angles, because they do not share a common arm.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b022",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Angles on a straight line"
    },
    "content_text": "Adjacent angles do not always have to be supplementary. In the diagram below the two angles are adjacent, but they do not add up to $180^{\\circ}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b023",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Angles on a straight line"
    },
    "content_text": "Source diagram for the note above, showing adjacent angles that do not add up to $180^{\\circ}$.\n\n[Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-026.png]",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b024",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Angles on a straight line"
    },
    "content_text": "**supplementary angles** Two (or more) angles are supplementary if they add up to $180^{\\circ}$.\n\n**adjacent angles** Adjacent angles are next to each other. Two adjacent angles share the same vertex and a common arm.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b025",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Worked example 15.8: Calculating angles on a straight line"
    },
    "content_text": "",
    "prompt_text": "Consider the diagram given below. You are given the following information:\n\n- $\\overset{\\leftrightarrow}{ST}$ is a straight line\n- $a = 65^{\\circ}$\n- $b = 68^{\\circ}$\n- $c = x^{\\circ}$\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_050.png\n\nWhat is the value of $x$?",
    "answer_text": "Step 1: Read the given information and consider the diagram carefully.\n\nBegin the answer by writing down the facts you know.\n\nThe angles must have a sum of $180^{\\circ}$, because they form a straight line.\n\n$$\na + b + c = 180^{\\circ}\n$$\n\nStep 2: Substitute all the values, including the unknown value, $x$.\n\n$$\n\\begin{align}\na + b + c & = 180^{\\circ} \\\\\n65^{\\circ} + 68^{\\circ} + x & = 180^{\\circ} \\\\\n\\end{align}\n$$\n\nStep 3: Solve the equation.\n\n$$\n\\begin{align}\na + b + c & = 180^{\\circ} \\\\\n65^{\\circ} + 68^{\\circ} + x & = 180^{\\circ} \\\\\n133^{\\circ} + x & = 180^{\\circ}\\\\\nx & = 180^{\\circ} - 133^{\\circ}\\\\\n\\therefore x & = 47^{\\circ} \\\\\n\\end{align}\n$$\n\nYou could now complete the diagram by replacing the $x$.\n\nCompleted diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-1_029.png",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b026",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Angles on a straight line"
    },
    "content_text": "When we refer to lines and line segments we can use different notations:\n\n- $\\overline{EF}$ means the line segment from point $E$ to point $F$.\n- $\\overset{\\leftrightarrow}{EF}$ means the line through points $E$ and $F$.\n- Most of the time we simply write $EF$ for the line through point $E$ and point $F$ and also for the line segment from point $E$ to point $F$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b027",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Exercise 15.3: Calculate angles on a straight line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.3: Calculate angles on a straight line",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b027-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Exercise 15.3: Calculate angles on a straight line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.3: Calculate angles on a straight line\n\n1. $YZ$ is a straight line, with angles as shown in the diagram below.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-027.png\n\nWhat is the value of $x$?",
    "answer_text": "The angles must have a sum of $180^{\\circ}$, because they form a straight line.\n\n$$\n\\begin{align}\n90^{\\circ} + x & = 180^{\\circ} \\\\\n\\therefore x & = 90^{\\circ} \\\\\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b027-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Exercise 15.3: Calculate angles on a straight line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.3: Calculate angles on a straight line\n\n2. $YZ$ is a straight line, with angles as shown below.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_007.png\n\nWhat is the value of $x$?",
    "answer_text": "The angles must have a sum of $180^{\\circ}$, because they form a straight line.\n\n$$\n\\begin{align}\nx + 56^{\\circ} + 63^{\\circ} & = 180^{\\circ} \\\\\nx + 119^{\\circ} & = 180^{\\circ}\\\\\n\\therefore x & = 61^{\\circ} \\\\\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b027-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Exercise 15.3: Calculate angles on a straight line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.3: Calculate angles on a straight line\n\n3. $ST$ is a straight line, with angles as shown below.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_035.png\n\nWhat is the value of $x$?",
    "answer_text": "The angles must have a sum of $180^{\\circ}$, because they form a straight line.\n\n$$\n\\begin{align}\nx + 59^{\\circ} + 74^{\\circ} & = 180^{\\circ} \\\\\nx + 133^{\\circ} & = 180^{\\circ}\\\\\n\\therefore x & = 47^{\\circ} \\\\\n\\end{align}\n$$\n\nCompleted diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-1_031.png",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b027-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Exercise 15.3: Calculate angles on a straight line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.3: Calculate angles on a straight line\n\n4. Examine the diagram below, and answer the two questions that follow.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_027.png\n\n1. Calculate $x$.\n2. What type of angle is represented by $x$?",
    "answer_text": "The angles must have a sum of $180^{\\circ}$, because they form a straight line.\n\n$$\n\\begin{align}\n37^{\\circ} + x + 55^{\\circ} & = 180^{\\circ} \\\\\n92^{\\circ} + x & = 180^{\\circ}\\\\\n\\therefore x & = 88^{\\circ} \\\\\n\\end{align}\n$$\n\nCompleted diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-1_026.png\n\nThe angle represented by $x$ is an acute angle.",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b027-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Exercise 15.3: Calculate angles on a straight line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.3: Calculate angles on a straight line\n\n5. Examine the diagram below, and answer the questions that follow.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_008.png\n\n1. Calculate $x$.\n2. What type of angle is represented by $x$?",
    "answer_text": "The angles must have a sum of $180^{\\circ}$, because they form a straight line.\n\n$$\n\\begin{align}\nx + 58^{\\circ} + 30^{\\circ} & = 180^{\\circ} \\\\\nx + 88^{\\circ} & = 180^{\\circ}\\\\\n\\therefore x & = 92^{\\circ} \\\\\n\\end{align}\n$$\n\nCompleted diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-1_050.png\n\nThe angle represented by $x$ is an obtuse angle.",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b027-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Exercise 15.3: Calculate angles on a straight line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.3: Calculate angles on a straight line\n\n6. Examine the diagram below, and answer the two questions that follow.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_012.png\n\n1. Calculate $x$.\n2. What type of angle is represented by $x$?",
    "answer_text": "The angles must have a sum of $180^{\\circ}$, because they form a straight line.\n\n$$\n\\begin{align}\nx + 78^{\\circ} + 40^{\\circ} & = 180^{\\circ} \\\\\nx + 118^{\\circ} & = 180^{\\circ} \\\\\n\\therefore x & = 62^{\\circ} \\\\\n\\end{align}\n$$\n\nCompleted diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-1_057.png\n\nThe angle represented by $x$ is an acute angle.",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b027-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Exercise 15.3: Calculate angles on a straight line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.3: Calculate angles on a straight line\n\n7. In the diagram below, line $YZ$ is a straight line with angles labelled above and below it.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_016.png\n\nFind the values of $x$ and $y$, giving reasons for your answer. (Remember to check your answers.)",
    "answer_text": "All of the angles above $YZ$ add up to $180^{\\circ}$:\n\n$$\n\\begin{align}\nx + 65^{\\circ} + 60^{\\circ} & = 180^{\\circ} \\quad(\\text{angles on a straight line}) \\\\\nx + 125^{\\circ} & = 180^{\\circ}\\\\\nx & = 180^{\\circ} - 125^{\\circ}\\\\\n\\therefore x & = 55^{\\circ} \\\\\n\\end{align}\n$$\n\nIn the same way, all of the angles below $YZ$ add up to $180^{\\circ}$:\n\n$$\n\\begin{align}\n26^{\\circ} + 82^{\\circ} + 35^{\\circ} + y & = 180^{\\circ} \\quad(\\text{angles on a straight line}) \\\\\n143^{\\circ} + y & = 180^{\\circ} \\\\\ny & = 180^{\\circ} - 143^{\\circ} \\\\\n\\therefore y & = 37^{\\circ} \\\\\n\\end{align}\n$$\n\nCompleted diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-1_007.png\n\nThe angles in a full turn (revolution) must add up to $360^{\\circ}$. This is a good way to check your answers:\n\n$$\n\\begin{align}\n55^{\\circ} + 65^{\\circ} + 60^{\\circ} + 26^{\\circ} + 82^{\\circ} + 35^{\\circ} + 37^{\\circ} & = 360^{\\circ} \\\\\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b027-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Exercise 15.3: Calculate angles on a straight line"
    },
    "content_text": "",
    "prompt_text": "### Exercise 15.3: Calculate angles on a straight line\n\n8. In the diagram below, $YZ$ is a straight line with angles labelled above and below it.\n\nDiagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_056.png\n\nFind the values of $x$ and $y$, giving reasons for your answer. (Remember to check your answers.)",
    "answer_text": "All of the angles above $YZ$ add up to $180^{\\circ}$:\n\n$$\n\\begin{align}\n15^{\\circ} + 141^{\\circ} + x & = 180^{\\circ}\\quad(\\text{angles on a straight line}) \\\\\n156^{\\circ} + x & = 180^{\\circ}\\\\\nx &= 180^{\\circ} - 156^{\\circ}\\\\\n\\therefore x & = 24^{\\circ} \\\\\n\\end{align}\n$$\n\nIn the same way, all of the angles below $YZ$ add up to $180^{\\circ}$:\n\n$$\n\\begin{align}\n44^{\\circ} + y + 45^{\\circ} + 75^{\\circ} & = 180^{\\circ} \\quad(\\text{angles on a straight line}) \\\\\n164^{\\circ} + y  & = 180^{\\circ}\\\\\ny & = 180^{\\circ} - 164^{\\circ}\\\\\n\\therefore y & = 16^{\\circ} \\\\\n\\end{align}\n$$\n\nHere is the completed diagram, with all of the angle values labelled:\n\nCompleted diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-1_038.png\n\nCheck your answers:\n\n$$\n\\begin{align}\n15^{\\circ} + 141^{\\circ} + 24^{\\circ} + 44^{\\circ} + 16^{\\circ} + 45^{\\circ} + 75^{\\circ} & = 360^{\\circ} \\\\\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b028",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.2 Angles on straight and intersecting lines",
      "h3": "Angles on a straight line"
    },
    "content_text": "You will not usually be asked to redraw the diagram to give the missing angle size.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line"
  },
  {
    "record_id": "ch15-b063-i03c",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 15: Angles",
      "h2": "15.4 Practical applications",
      "h3": "Exercise 15.11: Solve real-world problems with angles"
    },
    "content_text": "Source math retained:\nx\nP\\hat{R}S\n120^{\\circ}\nRS\nTU\nPQ\nP\\hat{R}S\nR\\hat{T}U\nR\\hat{T}U\n120^{\\circ}\nR\\hat{T}U\nU\\hat{T}Q\n180^{\\circ}\nU\\hat{T}Q\nx\n\\begin{align} x + 120^{\\circ} & = 180^{\\circ} \\\\ \\therefore x & = 60^{\\circ} \\end{align}\nx\n60^{\\circ}",
    "prompt_text": "### Exercise 15.11: Solve real-world problems with angles\n\n3c. In the diagram below, what should the size of the angle marked $x$ be if $P\\hat{R}S$ is equal to $120^{\\circ}$?\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-039.png",
    "answer_text": "$RS$ and $TU$ are parallel lines and $PQ$ is a transversal.\n\n$P\\hat{R}S$ and $R\\hat{T}U$ are corresponding angles, which means they are equal. Therefore, $R\\hat{T}U = 120^{\\circ}$.\n\n$R\\hat{T}U$ and $U\\hat{T}Q$ are on a straight line, so they add up to $180^{\\circ}$. $U\\hat{T}Q$ is $x$.\n\n$$\n\begin{align}\nx + 120^{\\circ} &= 180^{\\circ} \\\n\therefore x &= 60^{\\circ}\n\\end{align}\n$$\n\nThe size of the angle marked $x$ is $60^{\\circ}$.",
    "primary_subtopic_id": "jss1-math-angles-identification-and-properties-of-vertically-opposite-adjacent-alternate-and-corresponding-angles"
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
