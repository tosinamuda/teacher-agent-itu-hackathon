# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-2",
  "topic_key": "jss1-math-addition-and-subtraction-of-fractions",
  "topic": "Addition and Subtraction of Fractions",
  "subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions",
  "subtopic_title": "Addition and subtraction of fractions",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions-po01",
        "source_performance_objective_index": 1,
        "text": "Solve problems on addition and subtraction of fractions"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "addition-and-subtraction-of-fractions-ao-solve-addition-problems",
          "text": "Solve problems on addition of fractions."
        },
        {
          "atomic_objective_id": "addition-and-subtraction-of-fractions-ao-solve-subtraction-problems",
          "text": "Solve problems on subtraction of fractions."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch06-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": null
    },
    "content_text": "In Chapter 4, you learnt that a common fraction is written as two whole numbers, one on top of the other: $\\frac{\\text{numerator}}{\\text{denominator}}$.\n\n- The denominator represents all the parts of a whole. For example, in the fraction $\\frac{2}{7}$, each whole is divided into 7 parts.\n- The numerator represents only the parts of a whole we are dealing with. For example, in the fraction $\\frac{2}{7}$, we are dealing with only 2 out of 7 parts.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b002",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Adding fractions with the same denominator"
    },
    "content_text": "Usman and Adamu are at a birthday party. There is a cake that is cut into 4 pieces:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-001.png)\n\nSuppose Usman gets $\\frac{1}{4}$ of the cake:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-035.png)\n\nSuppose Adamu also gets $\\frac{1}{4}$ of the cake:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-002.png)\n\nIf they put their pieces of cake together, they have $\\frac{2}{4}$ of the cake:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-003.png)\n\nWe write this as:\n\n$$\n\\frac{1}{4}+\\frac{1}{4}=\\frac{2}{4}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b003",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Adding fractions with the same denominator"
    },
    "content_text": "Remember that the denominator of a fraction tells us into how many parts a whole is divided. In this case, one whole cake is divided into 4 pieces. Together, the boys have 2 of those pieces.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b004",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Adding fractions with the same denominator"
    },
    "content_text": "In Chapter 4, you learnt how to write a fraction in its simplest form. This is when the numerator and denominator have no common factor.\n\nThe simplest form of $\\frac{2}{4}$ is $\\frac{1}{2}$.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-004.png)\n\nWe may therefore write:\n\n$$\n\\frac{1}{4}+\\frac{1}{4}=\\frac{1}{2}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b005",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Subtracting fractions with the same denominator"
    },
    "content_text": "Suppose another cake arrives at the birthday party that Usman and Adamu are attending. This cake is also cut into 4 pieces. Someone immediately takes a piece, so that only 3 of the 4 pieces are left. The cake may now be represented as follows.\n\nThere is $\\frac{3}{4}$ of the cake left:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-036.png)\n\nDanladi did not have any cake yet. He gets 1 piece, which is $\\frac{1}{4}$ of the cake:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-005.png)\n\nAfter Danladi took his piece, $\\frac{2}{4}$ of the cake is left:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-037.png)\n\nWe write this as:\n\n$$\n\\frac{3}{4}-\\frac{1}{4}=\\frac{2}{4}\n$$\nThe simplest form of $\\frac{2}{4}$ is $\\frac{1}{2}$.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-006.png)\n\nWe may therefore write:\n\n$$\n\\frac{3}{4}-\\frac{1}{4}=\\frac{1}{2}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b006",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Worked example 6.1: Adding fractions with the same denominator"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n\n$\\frac{7}{10}+\\frac{1}{10}$",
    "answer_text": "Method 1 (Using diagrams)\n\n1. The denominator shows into how many parts one whole must be divided. Represent this in a diagram. In this case, there must be 10 parts.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-007.png)\n\n2. Shade the number of parts shown by the first numerator. The first numerator is 7.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-008.png)\n\n3. Now also shade the number of parts shown by the second numerator. The second numerator is 1. We must shade another 1 part.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-009.png)\n\n4. Write the total shaded part as a fraction:\n\n$$\n\\frac{8}{10}\n$$\n\n5. Write the fraction in its simplest form.\n\n$$\n\\frac{8\\div 2}{10\\div 2}=\\frac{4}{5}\n$$\n\n6. The full calculation is:\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{7}{10}+\\frac{1}{10}\\newline\n =\\frac{8}{10} \n =\\frac{4}{5}\n \\end{array}\n$$\n\nMethod 2 (Calculating directly)\n\n1. The denominator shows into how many parts one whole must be divided. Write down the denominator.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{7}{10}+\\frac{1}{10}\\newline\n =\\frac{\\phantom{00000}}{10} \n \\end{array}\n$$\n\n2. Write down the numerators that must be added.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{7}{10}+\\frac{1}{10}\\newline\n =\\frac{7+1}{10} \n \\end{array}\n$$\n\n3. Add the numerators.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{7}{10}+\\frac{1}{10}\\newline\n =\\frac{7+1}{10} \n =\\frac{8}{10} \n \\end{array}\n$$\n\n4. Simplify the answer.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{7}{10}+\\frac{1}{10}\\newline\n =\\frac{7+1}{10} \n =\\frac{8}{10} \n =\\frac{4}{5}\n \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b007",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Worked example 6.2: Subtracting fractions with the same denominator"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n\n$$\n\\frac{7}{9}-\\frac{3}{9}\n$$",
    "answer_text": "Method 1: Using diagrams\n\n1. The denominator shows into how many parts one whole must be divided. Represent this in a diagram. In this case, there must be 9 parts.\n\n2. Shade the number of parts shown by the first numerator. The first numerator is 7.\n\n3. Scratch out the number of parts shown by the numerator that is subtracted. The second numerator is 3. We must scratch out 3 parts.\n\n4. Redraw the diagram, shading only the parts that are left over. There are 4 parts left over.\n\n5. Write the shaded part as a fraction.\n\n$$\n\\frac{4}{9}\n$$\n\n6. Check whether the fraction is in its simplest form.\n\nIn this case, the numerator and denominator have no common factors.\n\n7. The full calculation is:\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{7}{9}-\\frac{3}{9}\\newline\n =\\frac{4}{9} \\newline\n \\end{array}\n$$\n\nMethod 2: Calculating directly\n\n1. The denominator shows into how many parts one whole must be divided. Write down the denominator.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{7}{9}-\\frac{3}{9}\\newline\n =\\frac{\\phantom{0000}}{9} \\newline\n \\end{array}\n$$\n\n2. Write down the numerators that must be subtracted.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{7}{9}-\\frac{3}{9}\\newline\n =\\frac{7-3}{9} \\newline\n \\end{array}\n$$\n\n3. Subtract the numerators.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{7}{9}-\\frac{3}{9}\\newline\n =\\frac{7-3}{9} \\newline\n =\\frac{4}{9} \\newline\n \\end{array}\n$$\n\n4. Simplify the answer if necessary. In this case, is it not necessary.",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b008",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.1: Add and subtract fractions that have the same denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.1: Add and subtract fractions that have the same denominators\n\nCalculate each of the following.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b008-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.1: Add and subtract fractions that have the same denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.1: Add and subtract fractions that have the same denominators\n\nCalculate each of the following.\n\n1. \\frac{3}{11}+\\frac{5}{11}",
    "answer_text": "$$\n\\begin{array}{l}\n\\phantom{00}\\frac{3}{11}+\\frac{5}{11}\\newline\n=\\frac{3+5}{11} \\\\\n=\\frac{8}{11} \\\\\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b008-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.1: Add and subtract fractions that have the same denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.1: Add and subtract fractions that have the same denominators\n\nCalculate each of the following.\n\n2. \\frac{7}{12}+\\frac{3}{12}",
    "answer_text": "$$\n\\begin{array}{l}\n\\phantom{00}\\frac{7}{12}+\\frac{3}{12}\\newline\n=\\frac{7+3}{12} \\\\\n=\\frac{10}{12} \\\\\n=\\frac{5}{6}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b008-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.1: Add and subtract fractions that have the same denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.1: Add and subtract fractions that have the same denominators\n\nCalculate each of the following.\n\n3. \\frac{11}{36}+\\frac{13}{36}",
    "answer_text": "$$\n\\begin{array}{l}\n\\phantom{00}\\frac{11}{36}+\\frac{13}{36}\\newline\n=\\frac{11+13}{36} \\\\\n=\\frac{24}{36} \\\\\n=\\frac{2}{3}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b008-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.1: Add and subtract fractions that have the same denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.1: Add and subtract fractions that have the same denominators\n\nCalculate each of the following.\n\n4. \\frac{15}{17}-\\frac{9}{17}",
    "answer_text": "$$\n\\begin{array}{l}\n\\phantom{00}\\frac{15}{17}-\\frac{9}{17}\\newline\n=\\frac{15-9}{17} \\\\\n=\\frac{6}{17} \\\\\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b008-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.1: Add and subtract fractions that have the same denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.1: Add and subtract fractions that have the same denominators\n\nCalculate each of the following.\n\n5. \\frac{19}{20}-\\frac{7}{20}",
    "answer_text": "$$\n\\begin{array}{l}\n\\phantom{00}\\frac{19}{20}-\\frac{7}{20}\\newline\n=\\frac{19-7}{20} \\\\\n=\\frac{12}{20} \\\\\n=\\frac{3}{5}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b008-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.1: Add and subtract fractions that have the same denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.1: Add and subtract fractions that have the same denominators\n\nCalculate each of the following.\n\n6. \\frac{41}{48}-\\frac{5}{48}",
    "answer_text": "$$\n\\begin{array}{l}\n\\phantom{00}\\frac{41}{48}-\\frac{5}{48}\\newline\n=\\frac{41-5}{48} \\\\\n=\\frac{36}{48} \\\\\n=\\frac{3}{4}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b009",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Adding and subtracting fractions with different denominators"
    },
    "content_text": "Suppose we want to determine the following:\n\n$$\n\\frac{2}{3}+\\frac{1}{2}\n$$\n\n$$\n\\frac{2}{3}-\\frac{1}{2}\n$$\n\n\\frac{2}{3} of a cake may be represented as:\n\n\\frac{1}{2} of a cake may be represented as:\n\nWe can divide one cake into either 2 pieces or 3 pieces. We cannot divide the cake into both. To overcome this problem, we have to express both fractions with the same denominator. The lowest common denominator (LCD) of 2 and 3 is 6. The equivalent fractions of \\frac{2}{3} and \\frac{1}{2}, with 6 as their denominator, are:\n\n$$\n\\frac{2}{3}=\\frac{2\\times2}{3\\times2}=\\frac{4}{6}\n$$\n\n$$\n\\frac{1}{2}=\\frac{1\\times3}{2\\times3}=\\frac{3}{6}\n$$\n\nNow we can follow the same method as before.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b010",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Adding and subtracting fractions with different denominators"
    },
    "content_text": "If necessary, go back to Chapter 4 for information about the lowest common denominator (LCD) of two or more fractions. Revise how find equivalent fractions that all have the LCD as their denominator.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b011",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Worked example 6.3: Adding fractions with different denominators"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n\n$$\n\\frac{2}{3}+\\frac{1}{2}\n$$",
    "answer_text": "Step 1: Compare the denominators. If they are different, find the LCD.\n\nThe LCD of 2 and 3 is 6.\n\nStep 2: Find equivalent fractions with the LCD as their denominators.\n\n$$\n\\frac{2}{3}=\\frac{4}{6}\n$$\n\n$$\n\\frac{1}{2}=\\frac{3}{6}\n$$\n\nStep 3: Use the LCD to represent the parts of one whole in a diagram.\n\nIn this case, there must be 6 parts.\n\nStep 4: Shade the number of parts shown by the first numerator of the equivalent fraction.\n\nThis is 4.\n\nStep 5: Shade the additional parts shown by the second numerator of the equivalent fraction.\n\nThe second numerator is 3. We must shade another 3 parts.\n\nThere are only 2 \"gaps\" in the shape that can be shaded. Therefore, we need to add another shape.\n\nStep 6: Write the total shaded part as a fraction.\n\nThe fraction is \\frac{7}{6}.\n\nRemember, the denominator shows into how many parts one whole is divided. The numerator shows the total number of those parts that we are dealing with.\n\nStep 7: Write the answer in its simplest form or as a mixed number.\n\n$$\n\\frac{7}{6}=1\\frac{1}{6}\n$$\n\nStep 8: Write out the whole calculation.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{2}{3}+\\frac{1}{2}\\newline\n =\\frac{4}{6}+\\frac{3}{6}\\newline\n =\\frac{4+3}{6} \\newline\n =\\frac{7}{6} \\newline\n =1\\frac{1}{6}\n \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b012",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Worked example 6.4: Subtracting fractions with different denominators"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n\n$$\n\\frac{2}{3}-\\frac{1}{2}\n$$",
    "answer_text": "Step 1: Compare the denominators. If they are different, find the LCD.\n\nThe LCD of 2 and 3 is 6.\n\nStep 2: Find equivalent fractions with the LCD as their denominators.\n\n$$\n\\frac{2}{3}=\\frac{4}{6}\n$$\n\n$$\n\\frac{1}{2}=\\frac{3}{6}\n$$\n\nStep 3: Use the LCD to represent the parts of one whole in a diagram.\n\nIn this case, there must be 6 parts.\n\nStep 4: Shade the number of parts shown by the first numerator of the equivalent fraction.\n\nThis is 4.\n\nStep 5: Scratch out the number of parts shown by the numerator of the equivalent fraction that is subtracted. Then redraw the diagram with only the parts that are left over shaded.\n\nThe second numerator is 3. We must scratch out 3 parts.\n\nThere is only one part left over.\n\nStep 6: Write the shaded part as a fraction.\n\n$$\n\\frac{1}{6}\n$$\n\nStep 7: Check whether the fraction is in its simplest form.\n\nIn this case, the numerator and denominator have no common factors.\n\nStep 8: Write out the whole calculation.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{2}{3}-\\frac{1}{2}\\newline\n =\\frac{4}{6}-\\frac{3}{6}\\newline\n =\\frac{4-3}{6} \\newline\n =\\frac{1}{6}\n \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b013",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Adding and subtracting fractions with different denominators"
    },
    "content_text": "As you get used to adding and subtracting fractions, it will no longer be necessary to draw diagrams. Just be sure to always write out the calculation in full.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b014",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.2: Add and subtract fractions that have different denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.2: Add and subtract fractions that have different denominators\n\nCalculate each of the following.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b014-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.2: Add and subtract fractions that have different denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.2: Add and subtract fractions that have different denominators\n\nCalculate each of the following.\n\n1. \\frac{3}{4}+\\frac{1}{8}",
    "answer_text": "LCD = 8\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{3}{4}+\\frac{5}{8}\\newline\n=\\frac{6}{8}+\\frac{1}{8} \\\\\n=\\frac{6+1}{8} \\\\\n=\\frac{7}{8}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b014-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.2: Add and subtract fractions that have different denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.2: Add and subtract fractions that have different denominators\n\nCalculate each of the following.\n\n2. \\frac{2}{3}+\\frac{2}{7}",
    "answer_text": "LCD = 21\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{2}{3}+\\frac{2}{7}\\newline\n=\\frac{14}{21}+\\frac{6}{21} \\\\\n=\\frac{14+6}{21} \\\\\n=\\frac{20}{21}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b014-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.2: Add and subtract fractions that have different denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.2: Add and subtract fractions that have different denominators\n\nCalculate each of the following.\n\n3. \\frac{11}{30}+\\frac{4}{12}",
    "answer_text": "30=2\\times3\\times5\n12=2^2\\times3\n\\text{LCD} = 2^2\\times3\\times5= 60\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{11}{30}+\\frac{4}{12}\\newline\n=\\frac{22}{60}+\\frac{20}{60} \\\\\n=\\frac{22+20}{60} \\\\\n=\\frac{42}{60} \\\\\n=\\frac{7}{10}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b014-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.2: Add and subtract fractions that have different denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.2: Add and subtract fractions that have different denominators\n\nCalculate each of the following.\n\n4. \\frac{10}{15}+\\frac{8}{20}",
    "answer_text": "15=3\\times5\n20=2^2\\times5\n\\text{LCD} = 2^2\\times3\\times5= 60\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{10}{15}+\\frac{8}{20}\\newline\n=\\frac{40}{60}+\\frac{24}{60} \\\\\n=\\frac{40+24}{60} \\\\\n=\\frac{64}{60} \\\\\n=\\frac{16}{15}\\\\\n=1\\frac{1}{15}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b014-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.2: Add and subtract fractions that have different denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.2: Add and subtract fractions that have different denominators\n\nCalculate each of the following.\n\n5. \\frac{1}{8}+\\frac{5}{6}+\\frac{5}{10}",
    "answer_text": "8=2^3\n6=2\\times3\n10=2\\times5\n\\text{LCD} = 2^3\\times3\\times5= 120\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{1}{8}+\\frac{5}{6}+\\frac{5}{10}\\newline\n=\\frac{15}{120}+\\frac{100}{120}+\\frac{60}{120} \\\\\n=\\frac{15+100+60}{120} \\\\\n=\\frac{175}{120} \\\\\n=\\frac{35}{24}\\\\\n=1\\frac{11}{24}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b014-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.2: Add and subtract fractions that have different denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.2: Add and subtract fractions that have different denominators\n\nCalculate each of the following.\n\n6. \\frac{11}{15}-\\frac{3}{5}",
    "answer_text": "LCD = 15\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{11}{15}-\\frac{3}{5}\\newline\n=\\frac{11}{15}-\\frac{9}{15}\\\\\n=\\frac{11-9}{15} \\\\\n=\\frac{2}{15}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b014-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.2: Add and subtract fractions that have different denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.2: Add and subtract fractions that have different denominators\n\nCalculate each of the following.\n\n7. \\frac{5}{6}-\\frac{2}{5}",
    "answer_text": "LCD = 30\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{5}{6}-\\frac{2}{5}\\newline\n=\\frac{25}{30}-\\frac{12}{30}\\\\\n=\\frac{25-12}{30} \\\\\n=\\frac{13}{30}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b014-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.2: Add and subtract fractions that have different denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.2: Add and subtract fractions that have different denominators\n\nCalculate each of the following.\n\n8. \\frac{9}{12}-\\frac{3}{15}",
    "answer_text": "12=2^2\\times3\n15=3\\times5\n\\text{LCD} = 2^2\\times3\\times5= 60\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{9}{12}-\\frac{3}{15}\\newline\n=\\frac{45}{60}-\\frac{12}{60}\\\\\n=\\frac{45-12}{60} \\\\\n=\\frac{33}{60} \\\\\n=\\frac{11}{20}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b014-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.2: Add and subtract fractions that have different denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.2: Add and subtract fractions that have different denominators\n\nCalculate each of the following.\n\n9. \\frac{23}{24}-\\frac{12}{18}",
    "answer_text": "24=2^3\\times3\n18=2\\times3^2\n\\text{LCD} = 2^3\\times3^2= 72\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{23}{24}-\\frac{12}{18}\\newline\n=\\frac{69}{72}-\\frac{48}{72}\\\\\n=\\frac{69-48}{72} \\\\\n=\\frac{21}{72} \\\\\n=\\frac{7}{24}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b014-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.2: Add and subtract fractions that have different denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.2: Add and subtract fractions that have different denominators\n\nCalculate each of the following.\n\n10. \\frac{9}{10}-\\frac{1}{6}-\\frac{2}{15}",
    "answer_text": "10=2\\times5\n6=2\\times3\n15=3\\times5\n\\text{LCD} = 2\\times3\\times5= 30\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{9}{10}-\\frac{1}{6}-\\frac{2}{15}\\newline\n=\\frac{27}{30}-\\frac{5}{30}-\\frac{4}{30} \\\\\n=\\frac{27-5-4}{30} \\\\\n=\\frac{18}{30} \\\\\n=\\frac{3}{5}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b015",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Adding and subtracting mixed numbers"
    },
    "content_text": "Remember that a mixed number is made up of a whole number and a proper fraction. There are various methods that may be used to add and subtract mixed numbers. It is recommended that you first convert all mixed numbers to improper fractions before you add or subtract.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b016",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Adding and subtracting mixed numbers"
    },
    "content_text": "If necessary, go back to Chapter 4 and revise how to convert mixed numbers to improper fractions.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b017",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Worked example 6.5: Adding mixed numbers"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n\n$$\n2\\frac{4}{5}+1\\frac{2}{3}\n$$",
    "answer_text": "Step 1: Convert the mixed numbers to improper fractions.\n\n$$\n2\\frac{4}{5}=\\frac{(2\\times5)+4}{5}=\\frac{14}{5}\n$$\n\n$$\n1\\frac{2}{3}=\\frac{(1\\times3)+2}{3}=\\frac{5}{3}\n$$\n\nStep 2: If the denominators differ, find equivalent fractions with the LCD as their denominators.\n\nThe LCD of 3 and 5 is 15.\n\n$$\n\\frac{14}{5}=\\frac{42}{15}\n$$\n\n$$\n\\frac{5}{3}=\\frac{25}{15}\n$$\n\nStep 3: Write down the LCD and add the numerators of the equivalent fractions.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{42}{15}+\\frac{25}{15}\\\\\n =\\frac{42+25}{15} \\\\\n =\\frac{67}{15}\n \\end{array}\n$$\n\nStep 4: Simplify the answer by converting the improper fraction to a mixed number.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{42}{15}+\\frac{25}{15}\\\\\n =\\frac{42+25}{15} \\\\\n =\\frac{67}{15} \\\\\n =4\\frac{7}{15} \\\\\n \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b018",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.3: Add and subtract mixed numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.3: Add and subtract mixed numbers\n\nCalculate each of the following.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b018-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.3: Add and subtract mixed numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.3: Add and subtract mixed numbers\n\n1. $2\\frac{1}{6}+1\\frac{3}{8}$",
    "answer_text": "$$\n2\\frac{1}{6}=\\frac{13}{6}\n$$\n\n$$\n1\\frac{3}{8}=\\frac{11}{8}\n$$\n\n$6=2\\times3$\n\n$8=2^3$\n\n$\\text{LCD} = 2^3\\times3= 24$\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{13}{6}+\\frac{11}{8}\\\\\n=\\frac{52}{24}+\\frac{33}{24} \\\\\n=\\frac{52+33}{24} \\\\\n=\\frac{85}{24} \\\\\n=3\\frac{13}{24}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b018-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.3: Add and subtract mixed numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.3: Add and subtract mixed numbers\n\n2. $2\\frac{5}{12}-1\\frac{3}{28}$",
    "answer_text": "$$\n2\\frac{5}{12}=\\frac{29}{12}\n$$\n\n$$\n1\\frac{3}{28}=\\frac{31}{28}\n$$\n\n$12=2^2\\times3$\n\n$28=2^2\\times7$\n\n$\\text{LCD} = 2^2\\times3\\times7= 84$\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{29}{12}-\\frac{31}{28}\\\\\n=\\frac{203}{84}+\\frac{93}{84} \\\\\n=\\frac{203-93}{84} \\\\\n=\\frac{110}{84} \\\\\n=\\frac{55}{42}\\\\\n=1 \\frac{13}{42}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b018-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.3: Add and subtract mixed numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.3: Add and subtract mixed numbers\n\n3. $1\\frac{7}{8}+2\\frac{3}{10}-3\\frac{1}{20}$",
    "answer_text": "$$\n1\\frac{7}{8}=\\frac{15}{8}\n$$\n\n$$\n2\\frac{3}{10}=\\frac{23}{10}\n$$\n\n$$\n3\\frac{1}{20}=\\frac{61}{20}\n$$\n\n$8=2^3$\n\n$10=2\\times5$\n\n$20=2^2\\times5$\n\n$\\text{LCD} = 2^3\\times5= 40$\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{15}{8}+\\frac{23}{10}-\\frac{61}{20}\\\\\n=\\frac{75}{40}+\\frac{92}{40}-\\frac{122}{40} \\\\\n=\\frac{75+92-122}{40} \\\\\n=\\frac{45}{40} \\\\\n=\\frac{9}{8}\\\\\n=1 \\frac{1}{8}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b054-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.3 Practical applications",
      "h3": "Exercise 6.10: Use operations with fractions to solve problems"
    },
    "content_text": "Source math retained:\n\\frac{1}{4}\n\\frac{3}{10}\n\\begin{array}{l}\\phantom{00}\\frac{1}{4}+\\frac{3}{10} \\\\ =\\frac{5}{20}+\\frac{6}{20} \\\\ =\\frac{5+6}{20} \\\\ =\\frac{11}{20}\\end{array}\n\\frac{11}{20}",
    "prompt_text": "### Exercise 6.10: Use operations with fractions to solve problems\n\n1. Chijindum spends $\\frac{1}{4}$ of his pocket money on clothes and $\\frac{3}{10}$ on sweets. What fraction of his pocket money did he spend altogether?",
    "answer_text": "$$\\begin{array}{l}\\phantom{00}\\frac{1}{4}+\\frac{3}{10} \\\\newline =\\frac{5}{20}+\\frac{6}{20} \\\\newline =\\frac{5+6}{20} \\\\newline =\\frac{11}{20}\\end{array}$$\nChijindum spends $\\frac{11}{20}$ of his pocket money altogether.",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-word-problems-on-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b054-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.3 Practical applications",
      "h3": "Exercise 6.10: Use operations with fractions to solve problems"
    },
    "content_text": "Source math retained:\n\\frac{1}{4}\n\\frac{3}{8}\n\\begin{array}{l}\\phantom{00}1-\\frac{1}{4}-\\frac{3}{8} \\\\ =\\frac{8}{8}-\\frac{2}{8}-\\frac{3}{8} \\\\ =\\frac{8-2-3}{8} \\\\ =\\frac{3}{8} \\\\\\end{array}\n\\frac{3}{8}",
    "prompt_text": "### Exercise 6.10: Use operations with fractions to solve problems\n\n5. Talatu decides to share a packet of sweets with her siblings. She gives $\\frac{1}{4}$ of the packet to her sister and $\\frac{3}{8}$ to her brother. What fraction of the sweets does she keep for herself?",
    "answer_text": "$$\\begin{array}{l}\\phantom{00}1-\\frac{1}{4}-\\frac{3}{8} \\\\newline =\\frac{8}{8}-\\frac{2}{8}-\\frac{3}{8} \\\\newline =\\frac{8-2-3}{8} \\\\newline =\\frac{3}{8} \\\\newline\\end{array}$$\nTalatu kept $\\frac{3}{8}$ of the sweets for herself.",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-word-problems-on-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b054-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.3 Practical applications",
      "h3": "Exercise 6.10: Use operations with fractions to solve problems"
    },
    "content_text": "Source math retained:\n\\frac{1}{5}\n1\\frac{2}{3}\n2\\frac{1}{6}\n\\begin{array}{l}\\phantom{00}\\frac{1}{5}+1\\frac{2}{3}+2\\frac{1}{6} \\\\ =\\frac{1}{5}+\\frac{5}{3}+\\frac{13}{6} \\\\ =\\frac{6}{30}+\\frac{50}{30}+\\frac{65}{30} \\\\ =\\frac{6+50+65}{30} \\\\ =\\frac{121}{30} \\\\ =4\\frac{1}{30} \\text{hours}\\end{array}\n4\\frac{1}{30}",
    "prompt_text": "### Exercise 6.10: Use operations with fractions to solve problems\n\n8. Habib goes home after school. He spends a $\\frac{1}{5}$ hour having lunch, then watches television for $1\\frac{2}{3}$ hours, and then does his homework for $2\\frac{1}{6}$ hours. How long did all these activities take?",
    "answer_text": "$$\\begin{array}{l}\\phantom{00}\\frac{1}{5}+1\\frac{2}{3}+2\\frac{1}{6} \\\\newline =\\frac{1}{5}+\\frac{5}{3}+\\frac{13}{6} \\\\newline =\\frac{6}{30}+\\frac{50}{30}+\\frac{65}{30} \\\\newline =\\frac{6+50+65}{30} \\\\newline =\\frac{121}{30} \\\\newline =4\\frac{1}{30}\\space\\text{hours}\\end{array}$$\nThese activities take $4\\frac{1}{30}$ hours.",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-word-problems-on-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b055",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.6 Summary",
      "h3": null
    },
    "content_text": "- To add or subtract fractions with the same denominator:\n  - Write down the denominator.\n  - Then add or subtract the numerators.\n- To add or subtract fractions with different denominators:\n  - Find the LCD.\n  - Find equivalent fractions with the LCD as denominator.\n  - Then add or subtract the numerators.\n- To multiply fractions and whole numbers:\n  - Write down the denominator of the fraction.\n  - Multiply the numerator of the fraction by the whole number.\n- To multiply fractions with fractions:\n  - Multiply the numerators.\n  - Multiply the denominators.\n- The reciprocal of a fraction is the \"opposite\" of the fraction, which we get by swapping the numerator and denominator. Whole numbers also have reciprocals. For example:\n  - The reciprocal of $\\frac{4}{9}$ is $\\frac{9}{4}$.\n  - The reciprocal of 8 is $\\frac{1}{8}$.\n- Dividing by a fraction or whole number is the same as multiplying by its reciprocal. For example:\n  - $$\\frac{4}{9}\\div 8=\\frac{4}{9}\\times\\frac{1}{8}$$\n  - $$\\frac{4}{9}\\div \\frac{3}{5}=\\frac{4}{9}\\times\\frac{5}{3}$$\n- Before you add, subtract, multiply or divide mixed numbers, first convert them to improper fractions.\n- When you have to multiply fractions with large numerators or denominators, simplify first.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
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
  "theme_key": "jss1-theme-2",
  "topic_key": "jss1-math-addition-and-subtraction-of-fractions",
  "topic": "Addition and Subtraction of Fractions",
  "subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions",
  "subtopic_title": "Addition and subtraction of fractions",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions-po01",
        "source_performance_objective_index": 1,
        "text": "Solve problems on addition and subtraction of fractions"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "addition-and-subtraction-of-fractions-ao-solve-addition-problems",
          "text": "Solve problems on addition of fractions."
        },
        {
          "atomic_objective_id": "addition-and-subtraction-of-fractions-ao-solve-subtraction-problems",
          "text": "Solve problems on subtraction of fractions."
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
    "record_id": "ch06-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": null
    },
    "content_text": "In Chapter 4, you learnt that a common fraction is written as two whole numbers, one on top of the other: $\\frac{\\text{numerator}}{\\text{denominator}}$.\n\n- The denominator represents all the parts of a whole. For example, in the fraction $\\frac{2}{7}$, each whole is divided into 7 parts.\n- The numerator represents only the parts of a whole we are dealing with. For example, in the fraction $\\frac{2}{7}$, we are dealing with only 2 out of 7 parts.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b002",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Adding fractions with the same denominator"
    },
    "content_text": "Usman and Adamu are at a birthday party. There is a cake that is cut into 4 pieces:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-001.png)\n\nSuppose Usman gets $\\frac{1}{4}$ of the cake:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-035.png)\n\nSuppose Adamu also gets $\\frac{1}{4}$ of the cake:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-002.png)\n\nIf they put their pieces of cake together, they have $\\frac{2}{4}$ of the cake:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-003.png)\n\nWe write this as:\n\n$$\n\\frac{1}{4}+\\frac{1}{4}=\\frac{2}{4}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b003",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Adding fractions with the same denominator"
    },
    "content_text": "Remember that the denominator of a fraction tells us into how many parts a whole is divided. In this case, one whole cake is divided into 4 pieces. Together, the boys have 2 of those pieces.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b004",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Adding fractions with the same denominator"
    },
    "content_text": "In Chapter 4, you learnt how to write a fraction in its simplest form. This is when the numerator and denominator have no common factor.\n\nThe simplest form of $\\frac{2}{4}$ is $\\frac{1}{2}$.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-004.png)\n\nWe may therefore write:\n\n$$\n\\frac{1}{4}+\\frac{1}{4}=\\frac{1}{2}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b005",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Subtracting fractions with the same denominator"
    },
    "content_text": "Suppose another cake arrives at the birthday party that Usman and Adamu are attending. This cake is also cut into 4 pieces. Someone immediately takes a piece, so that only 3 of the 4 pieces are left. The cake may now be represented as follows.\n\nThere is $\\frac{3}{4}$ of the cake left:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-036.png)\n\nDanladi did not have any cake yet. He gets 1 piece, which is $\\frac{1}{4}$ of the cake:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-005.png)\n\nAfter Danladi took his piece, $\\frac{2}{4}$ of the cake is left:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-037.png)\n\nWe write this as:\n\n$$\n\\frac{3}{4}-\\frac{1}{4}=\\frac{2}{4}\n$$\nThe simplest form of $\\frac{2}{4}$ is $\\frac{1}{2}$.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-006.png)\n\nWe may therefore write:\n\n$$\n\\frac{3}{4}-\\frac{1}{4}=\\frac{1}{2}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b006",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Worked example 6.1: Adding fractions with the same denominator"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n\n$\\frac{7}{10}+\\frac{1}{10}$",
    "answer_text": "Method 1 (Using diagrams)\n\n1. The denominator shows into how many parts one whole must be divided. Represent this in a diagram. In this case, there must be 10 parts.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-007.png)\n\n2. Shade the number of parts shown by the first numerator. The first numerator is 7.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-008.png)\n\n3. Now also shade the number of parts shown by the second numerator. The second numerator is 1. We must shade another 1 part.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-009.png)\n\n4. Write the total shaded part as a fraction:\n\n$$\n\\frac{8}{10}\n$$\n\n5. Write the fraction in its simplest form.\n\n$$\n\\frac{8\\div 2}{10\\div 2}=\\frac{4}{5}\n$$\n\n6. The full calculation is:\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{7}{10}+\\frac{1}{10}\\newline\n =\\frac{8}{10} \n =\\frac{4}{5}\n \\end{array}\n$$\n\nMethod 2 (Calculating directly)\n\n1. The denominator shows into how many parts one whole must be divided. Write down the denominator.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{7}{10}+\\frac{1}{10}\\newline\n =\\frac{\\phantom{00000}}{10} \n \\end{array}\n$$\n\n2. Write down the numerators that must be added.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{7}{10}+\\frac{1}{10}\\newline\n =\\frac{7+1}{10} \n \\end{array}\n$$\n\n3. Add the numerators.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{7}{10}+\\frac{1}{10}\\newline\n =\\frac{7+1}{10} \n =\\frac{8}{10} \n \\end{array}\n$$\n\n4. Simplify the answer.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{7}{10}+\\frac{1}{10}\\newline\n =\\frac{7+1}{10} \n =\\frac{8}{10} \n =\\frac{4}{5}\n \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b007",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Worked example 6.2: Subtracting fractions with the same denominator"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n\n$$\n\\frac{7}{9}-\\frac{3}{9}\n$$",
    "answer_text": "Method 1: Using diagrams\n\n1. The denominator shows into how many parts one whole must be divided. Represent this in a diagram. In this case, there must be 9 parts.\n\n2. Shade the number of parts shown by the first numerator. The first numerator is 7.\n\n3. Scratch out the number of parts shown by the numerator that is subtracted. The second numerator is 3. We must scratch out 3 parts.\n\n4. Redraw the diagram, shading only the parts that are left over. There are 4 parts left over.\n\n5. Write the shaded part as a fraction.\n\n$$\n\\frac{4}{9}\n$$\n\n6. Check whether the fraction is in its simplest form.\n\nIn this case, the numerator and denominator have no common factors.\n\n7. The full calculation is:\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{7}{9}-\\frac{3}{9}\\newline\n =\\frac{4}{9} \\newline\n \\end{array}\n$$\n\nMethod 2: Calculating directly\n\n1. The denominator shows into how many parts one whole must be divided. Write down the denominator.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{7}{9}-\\frac{3}{9}\\newline\n =\\frac{\\phantom{0000}}{9} \\newline\n \\end{array}\n$$\n\n2. Write down the numerators that must be subtracted.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{7}{9}-\\frac{3}{9}\\newline\n =\\frac{7-3}{9} \\newline\n \\end{array}\n$$\n\n3. Subtract the numerators.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{7}{9}-\\frac{3}{9}\\newline\n =\\frac{7-3}{9} \\newline\n =\\frac{4}{9} \\newline\n \\end{array}\n$$\n\n4. Simplify the answer if necessary. In this case, is it not necessary.",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b008",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.1: Add and subtract fractions that have the same denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.1: Add and subtract fractions that have the same denominators\n\nCalculate each of the following.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b008-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.1: Add and subtract fractions that have the same denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.1: Add and subtract fractions that have the same denominators\n\nCalculate each of the following.\n\n1. \\frac{3}{11}+\\frac{5}{11}",
    "answer_text": "$$\n\\begin{array}{l}\n\\phantom{00}\\frac{3}{11}+\\frac{5}{11}\\newline\n=\\frac{3+5}{11} \\\\\n=\\frac{8}{11} \\\\\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b008-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.1: Add and subtract fractions that have the same denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.1: Add and subtract fractions that have the same denominators\n\nCalculate each of the following.\n\n2. \\frac{7}{12}+\\frac{3}{12}",
    "answer_text": "$$\n\\begin{array}{l}\n\\phantom{00}\\frac{7}{12}+\\frac{3}{12}\\newline\n=\\frac{7+3}{12} \\\\\n=\\frac{10}{12} \\\\\n=\\frac{5}{6}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b008-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.1: Add and subtract fractions that have the same denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.1: Add and subtract fractions that have the same denominators\n\nCalculate each of the following.\n\n3. \\frac{11}{36}+\\frac{13}{36}",
    "answer_text": "$$\n\\begin{array}{l}\n\\phantom{00}\\frac{11}{36}+\\frac{13}{36}\\newline\n=\\frac{11+13}{36} \\\\\n=\\frac{24}{36} \\\\\n=\\frac{2}{3}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b008-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.1: Add and subtract fractions that have the same denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.1: Add and subtract fractions that have the same denominators\n\nCalculate each of the following.\n\n4. \\frac{15}{17}-\\frac{9}{17}",
    "answer_text": "$$\n\\begin{array}{l}\n\\phantom{00}\\frac{15}{17}-\\frac{9}{17}\\newline\n=\\frac{15-9}{17} \\\\\n=\\frac{6}{17} \\\\\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b008-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.1: Add and subtract fractions that have the same denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.1: Add and subtract fractions that have the same denominators\n\nCalculate each of the following.\n\n5. \\frac{19}{20}-\\frac{7}{20}",
    "answer_text": "$$\n\\begin{array}{l}\n\\phantom{00}\\frac{19}{20}-\\frac{7}{20}\\newline\n=\\frac{19-7}{20} \\\\\n=\\frac{12}{20} \\\\\n=\\frac{3}{5}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b008-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.1: Add and subtract fractions that have the same denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.1: Add and subtract fractions that have the same denominators\n\nCalculate each of the following.\n\n6. \\frac{41}{48}-\\frac{5}{48}",
    "answer_text": "$$\n\\begin{array}{l}\n\\phantom{00}\\frac{41}{48}-\\frac{5}{48}\\newline\n=\\frac{41-5}{48} \\\\\n=\\frac{36}{48} \\\\\n=\\frac{3}{4}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b009",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Adding and subtracting fractions with different denominators"
    },
    "content_text": "Suppose we want to determine the following:\n\n$$\n\\frac{2}{3}+\\frac{1}{2}\n$$\n\n$$\n\\frac{2}{3}-\\frac{1}{2}\n$$\n\n\\frac{2}{3} of a cake may be represented as:\n\n\\frac{1}{2} of a cake may be represented as:\n\nWe can divide one cake into either 2 pieces or 3 pieces. We cannot divide the cake into both. To overcome this problem, we have to express both fractions with the same denominator. The lowest common denominator (LCD) of 2 and 3 is 6. The equivalent fractions of \\frac{2}{3} and \\frac{1}{2}, with 6 as their denominator, are:\n\n$$\n\\frac{2}{3}=\\frac{2\\times2}{3\\times2}=\\frac{4}{6}\n$$\n\n$$\n\\frac{1}{2}=\\frac{1\\times3}{2\\times3}=\\frac{3}{6}\n$$\n\nNow we can follow the same method as before.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b010",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Adding and subtracting fractions with different denominators"
    },
    "content_text": "If necessary, go back to Chapter 4 for information about the lowest common denominator (LCD) of two or more fractions. Revise how find equivalent fractions that all have the LCD as their denominator.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b011",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Worked example 6.3: Adding fractions with different denominators"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n\n$$\n\\frac{2}{3}+\\frac{1}{2}\n$$",
    "answer_text": "Step 1: Compare the denominators. If they are different, find the LCD.\n\nThe LCD of 2 and 3 is 6.\n\nStep 2: Find equivalent fractions with the LCD as their denominators.\n\n$$\n\\frac{2}{3}=\\frac{4}{6}\n$$\n\n$$\n\\frac{1}{2}=\\frac{3}{6}\n$$\n\nStep 3: Use the LCD to represent the parts of one whole in a diagram.\n\nIn this case, there must be 6 parts.\n\nStep 4: Shade the number of parts shown by the first numerator of the equivalent fraction.\n\nThis is 4.\n\nStep 5: Shade the additional parts shown by the second numerator of the equivalent fraction.\n\nThe second numerator is 3. We must shade another 3 parts.\n\nThere are only 2 \"gaps\" in the shape that can be shaded. Therefore, we need to add another shape.\n\nStep 6: Write the total shaded part as a fraction.\n\nThe fraction is \\frac{7}{6}.\n\nRemember, the denominator shows into how many parts one whole is divided. The numerator shows the total number of those parts that we are dealing with.\n\nStep 7: Write the answer in its simplest form or as a mixed number.\n\n$$\n\\frac{7}{6}=1\\frac{1}{6}\n$$\n\nStep 8: Write out the whole calculation.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{2}{3}+\\frac{1}{2}\\newline\n =\\frac{4}{6}+\\frac{3}{6}\\newline\n =\\frac{4+3}{6} \\newline\n =\\frac{7}{6} \\newline\n =1\\frac{1}{6}\n \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b012",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Worked example 6.4: Subtracting fractions with different denominators"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n\n$$\n\\frac{2}{3}-\\frac{1}{2}\n$$",
    "answer_text": "Step 1: Compare the denominators. If they are different, find the LCD.\n\nThe LCD of 2 and 3 is 6.\n\nStep 2: Find equivalent fractions with the LCD as their denominators.\n\n$$\n\\frac{2}{3}=\\frac{4}{6}\n$$\n\n$$\n\\frac{1}{2}=\\frac{3}{6}\n$$\n\nStep 3: Use the LCD to represent the parts of one whole in a diagram.\n\nIn this case, there must be 6 parts.\n\nStep 4: Shade the number of parts shown by the first numerator of the equivalent fraction.\n\nThis is 4.\n\nStep 5: Scratch out the number of parts shown by the numerator of the equivalent fraction that is subtracted. Then redraw the diagram with only the parts that are left over shaded.\n\nThe second numerator is 3. We must scratch out 3 parts.\n\nThere is only one part left over.\n\nStep 6: Write the shaded part as a fraction.\n\n$$\n\\frac{1}{6}\n$$\n\nStep 7: Check whether the fraction is in its simplest form.\n\nIn this case, the numerator and denominator have no common factors.\n\nStep 8: Write out the whole calculation.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{2}{3}-\\frac{1}{2}\\newline\n =\\frac{4}{6}-\\frac{3}{6}\\newline\n =\\frac{4-3}{6} \\newline\n =\\frac{1}{6}\n \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b013",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Adding and subtracting fractions with different denominators"
    },
    "content_text": "As you get used to adding and subtracting fractions, it will no longer be necessary to draw diagrams. Just be sure to always write out the calculation in full.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b014",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.2: Add and subtract fractions that have different denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.2: Add and subtract fractions that have different denominators\n\nCalculate each of the following.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b014-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.2: Add and subtract fractions that have different denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.2: Add and subtract fractions that have different denominators\n\nCalculate each of the following.\n\n1. \\frac{3}{4}+\\frac{1}{8}",
    "answer_text": "LCD = 8\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{3}{4}+\\frac{5}{8}\\newline\n=\\frac{6}{8}+\\frac{1}{8} \\\\\n=\\frac{6+1}{8} \\\\\n=\\frac{7}{8}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b014-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.2: Add and subtract fractions that have different denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.2: Add and subtract fractions that have different denominators\n\nCalculate each of the following.\n\n2. \\frac{2}{3}+\\frac{2}{7}",
    "answer_text": "LCD = 21\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{2}{3}+\\frac{2}{7}\\newline\n=\\frac{14}{21}+\\frac{6}{21} \\\\\n=\\frac{14+6}{21} \\\\\n=\\frac{20}{21}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b014-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.2: Add and subtract fractions that have different denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.2: Add and subtract fractions that have different denominators\n\nCalculate each of the following.\n\n3. \\frac{11}{30}+\\frac{4}{12}",
    "answer_text": "30=2\\times3\\times5\n12=2^2\\times3\n\\text{LCD} = 2^2\\times3\\times5= 60\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{11}{30}+\\frac{4}{12}\\newline\n=\\frac{22}{60}+\\frac{20}{60} \\\\\n=\\frac{22+20}{60} \\\\\n=\\frac{42}{60} \\\\\n=\\frac{7}{10}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b014-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.2: Add and subtract fractions that have different denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.2: Add and subtract fractions that have different denominators\n\nCalculate each of the following.\n\n4. \\frac{10}{15}+\\frac{8}{20}",
    "answer_text": "15=3\\times5\n20=2^2\\times5\n\\text{LCD} = 2^2\\times3\\times5= 60\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{10}{15}+\\frac{8}{20}\\newline\n=\\frac{40}{60}+\\frac{24}{60} \\\\\n=\\frac{40+24}{60} \\\\\n=\\frac{64}{60} \\\\\n=\\frac{16}{15}\\\\\n=1\\frac{1}{15}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b014-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.2: Add and subtract fractions that have different denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.2: Add and subtract fractions that have different denominators\n\nCalculate each of the following.\n\n5. \\frac{1}{8}+\\frac{5}{6}+\\frac{5}{10}",
    "answer_text": "8=2^3\n6=2\\times3\n10=2\\times5\n\\text{LCD} = 2^3\\times3\\times5= 120\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{1}{8}+\\frac{5}{6}+\\frac{5}{10}\\newline\n=\\frac{15}{120}+\\frac{100}{120}+\\frac{60}{120} \\\\\n=\\frac{15+100+60}{120} \\\\\n=\\frac{175}{120} \\\\\n=\\frac{35}{24}\\\\\n=1\\frac{11}{24}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b014-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.2: Add and subtract fractions that have different denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.2: Add and subtract fractions that have different denominators\n\nCalculate each of the following.\n\n6. \\frac{11}{15}-\\frac{3}{5}",
    "answer_text": "LCD = 15\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{11}{15}-\\frac{3}{5}\\newline\n=\\frac{11}{15}-\\frac{9}{15}\\\\\n=\\frac{11-9}{15} \\\\\n=\\frac{2}{15}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b014-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.2: Add and subtract fractions that have different denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.2: Add and subtract fractions that have different denominators\n\nCalculate each of the following.\n\n7. \\frac{5}{6}-\\frac{2}{5}",
    "answer_text": "LCD = 30\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{5}{6}-\\frac{2}{5}\\newline\n=\\frac{25}{30}-\\frac{12}{30}\\\\\n=\\frac{25-12}{30} \\\\\n=\\frac{13}{30}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b014-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.2: Add and subtract fractions that have different denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.2: Add and subtract fractions that have different denominators\n\nCalculate each of the following.\n\n8. \\frac{9}{12}-\\frac{3}{15}",
    "answer_text": "12=2^2\\times3\n15=3\\times5\n\\text{LCD} = 2^2\\times3\\times5= 60\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{9}{12}-\\frac{3}{15}\\newline\n=\\frac{45}{60}-\\frac{12}{60}\\\\\n=\\frac{45-12}{60} \\\\\n=\\frac{33}{60} \\\\\n=\\frac{11}{20}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b014-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.2: Add and subtract fractions that have different denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.2: Add and subtract fractions that have different denominators\n\nCalculate each of the following.\n\n9. \\frac{23}{24}-\\frac{12}{18}",
    "answer_text": "24=2^3\\times3\n18=2\\times3^2\n\\text{LCD} = 2^3\\times3^2= 72\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{23}{24}-\\frac{12}{18}\\newline\n=\\frac{69}{72}-\\frac{48}{72}\\\\\n=\\frac{69-48}{72} \\\\\n=\\frac{21}{72} \\\\\n=\\frac{7}{24}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b014-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.2: Add and subtract fractions that have different denominators"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.2: Add and subtract fractions that have different denominators\n\nCalculate each of the following.\n\n10. \\frac{9}{10}-\\frac{1}{6}-\\frac{2}{15}",
    "answer_text": "10=2\\times5\n6=2\\times3\n15=3\\times5\n\\text{LCD} = 2\\times3\\times5= 30\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{9}{10}-\\frac{1}{6}-\\frac{2}{15}\\newline\n=\\frac{27}{30}-\\frac{5}{30}-\\frac{4}{30} \\\\\n=\\frac{27-5-4}{30} \\\\\n=\\frac{18}{30} \\\\\n=\\frac{3}{5}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b015",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Adding and subtracting mixed numbers"
    },
    "content_text": "Remember that a mixed number is made up of a whole number and a proper fraction. There are various methods that may be used to add and subtract mixed numbers. It is recommended that you first convert all mixed numbers to improper fractions before you add or subtract.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b016",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Adding and subtracting mixed numbers"
    },
    "content_text": "If necessary, go back to Chapter 4 and revise how to convert mixed numbers to improper fractions.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b017",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Worked example 6.5: Adding mixed numbers"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n\n$$\n2\\frac{4}{5}+1\\frac{2}{3}\n$$",
    "answer_text": "Step 1: Convert the mixed numbers to improper fractions.\n\n$$\n2\\frac{4}{5}=\\frac{(2\\times5)+4}{5}=\\frac{14}{5}\n$$\n\n$$\n1\\frac{2}{3}=\\frac{(1\\times3)+2}{3}=\\frac{5}{3}\n$$\n\nStep 2: If the denominators differ, find equivalent fractions with the LCD as their denominators.\n\nThe LCD of 3 and 5 is 15.\n\n$$\n\\frac{14}{5}=\\frac{42}{15}\n$$\n\n$$\n\\frac{5}{3}=\\frac{25}{15}\n$$\n\nStep 3: Write down the LCD and add the numerators of the equivalent fractions.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{42}{15}+\\frac{25}{15}\\\\\n =\\frac{42+25}{15} \\\\\n =\\frac{67}{15}\n \\end{array}\n$$\n\nStep 4: Simplify the answer by converting the improper fraction to a mixed number.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{42}{15}+\\frac{25}{15}\\\\\n =\\frac{42+25}{15} \\\\\n =\\frac{67}{15} \\\\\n =4\\frac{7}{15} \\\\\n \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b018",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.3: Add and subtract mixed numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.3: Add and subtract mixed numbers\n\nCalculate each of the following.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b018-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.3: Add and subtract mixed numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.3: Add and subtract mixed numbers\n\n1. $2\\frac{1}{6}+1\\frac{3}{8}$",
    "answer_text": "$$\n2\\frac{1}{6}=\\frac{13}{6}\n$$\n\n$$\n1\\frac{3}{8}=\\frac{11}{8}\n$$\n\n$6=2\\times3$\n\n$8=2^3$\n\n$\\text{LCD} = 2^3\\times3= 24$\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{13}{6}+\\frac{11}{8}\\\\\n=\\frac{52}{24}+\\frac{33}{24} \\\\\n=\\frac{52+33}{24} \\\\\n=\\frac{85}{24} \\\\\n=3\\frac{13}{24}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b018-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.3: Add and subtract mixed numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.3: Add and subtract mixed numbers\n\n2. $2\\frac{5}{12}-1\\frac{3}{28}$",
    "answer_text": "$$\n2\\frac{5}{12}=\\frac{29}{12}\n$$\n\n$$\n1\\frac{3}{28}=\\frac{31}{28}\n$$\n\n$12=2^2\\times3$\n\n$28=2^2\\times7$\n\n$\\text{LCD} = 2^2\\times3\\times7= 84$\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{29}{12}-\\frac{31}{28}\\\\\n=\\frac{203}{84}+\\frac{93}{84} \\\\\n=\\frac{203-93}{84} \\\\\n=\\frac{110}{84} \\\\\n=\\frac{55}{42}\\\\\n=1 \\frac{13}{42}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b018-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.1 Addition and subtraction of fractions",
      "h3": "Exercise 6.3: Add and subtract mixed numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.3: Add and subtract mixed numbers\n\n3. $1\\frac{7}{8}+2\\frac{3}{10}-3\\frac{1}{20}$",
    "answer_text": "$$\n1\\frac{7}{8}=\\frac{15}{8}\n$$\n\n$$\n2\\frac{3}{10}=\\frac{23}{10}\n$$\n\n$$\n3\\frac{1}{20}=\\frac{61}{20}\n$$\n\n$8=2^3$\n\n$10=2\\times5$\n\n$20=2^2\\times5$\n\n$\\text{LCD} = 2^3\\times5= 40$\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{15}{8}+\\frac{23}{10}-\\frac{61}{20}\\\\\n=\\frac{75}{40}+\\frac{92}{40}-\\frac{122}{40} \\\\\n=\\frac{75+92-122}{40} \\\\\n=\\frac{45}{40} \\\\\n=\\frac{9}{8}\\\\\n=1 \\frac{1}{8}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b054-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.3 Practical applications",
      "h3": "Exercise 6.10: Use operations with fractions to solve problems"
    },
    "content_text": "Source math retained:\n\\frac{1}{4}\n\\frac{3}{10}\n\\begin{array}{l}\\phantom{00}\\frac{1}{4}+\\frac{3}{10} \\\\ =\\frac{5}{20}+\\frac{6}{20} \\\\ =\\frac{5+6}{20} \\\\ =\\frac{11}{20}\\end{array}\n\\frac{11}{20}",
    "prompt_text": "### Exercise 6.10: Use operations with fractions to solve problems\n\n1. Chijindum spends $\\frac{1}{4}$ of his pocket money on clothes and $\\frac{3}{10}$ on sweets. What fraction of his pocket money did he spend altogether?",
    "answer_text": "$$\\begin{array}{l}\\phantom{00}\\frac{1}{4}+\\frac{3}{10} \\\\newline =\\frac{5}{20}+\\frac{6}{20} \\\\newline =\\frac{5+6}{20} \\\\newline =\\frac{11}{20}\\end{array}$$\nChijindum spends $\\frac{11}{20}$ of his pocket money altogether.",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-word-problems-on-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b054-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.3 Practical applications",
      "h3": "Exercise 6.10: Use operations with fractions to solve problems"
    },
    "content_text": "Source math retained:\n\\frac{1}{4}\n\\frac{3}{8}\n\\begin{array}{l}\\phantom{00}1-\\frac{1}{4}-\\frac{3}{8} \\\\ =\\frac{8}{8}-\\frac{2}{8}-\\frac{3}{8} \\\\ =\\frac{8-2-3}{8} \\\\ =\\frac{3}{8} \\\\\\end{array}\n\\frac{3}{8}",
    "prompt_text": "### Exercise 6.10: Use operations with fractions to solve problems\n\n5. Talatu decides to share a packet of sweets with her siblings. She gives $\\frac{1}{4}$ of the packet to her sister and $\\frac{3}{8}$ to her brother. What fraction of the sweets does she keep for herself?",
    "answer_text": "$$\\begin{array}{l}\\phantom{00}1-\\frac{1}{4}-\\frac{3}{8} \\\\newline =\\frac{8}{8}-\\frac{2}{8}-\\frac{3}{8} \\\\newline =\\frac{8-2-3}{8} \\\\newline =\\frac{3}{8} \\\\newline\\end{array}$$\nTalatu kept $\\frac{3}{8}$ of the sweets for herself.",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-word-problems-on-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b054-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.3 Practical applications",
      "h3": "Exercise 6.10: Use operations with fractions to solve problems"
    },
    "content_text": "Source math retained:\n\\frac{1}{5}\n1\\frac{2}{3}\n2\\frac{1}{6}\n\\begin{array}{l}\\phantom{00}\\frac{1}{5}+1\\frac{2}{3}+2\\frac{1}{6} \\\\ =\\frac{1}{5}+\\frac{5}{3}+\\frac{13}{6} \\\\ =\\frac{6}{30}+\\frac{50}{30}+\\frac{65}{30} \\\\ =\\frac{6+50+65}{30} \\\\ =\\frac{121}{30} \\\\ =4\\frac{1}{30} \\text{hours}\\end{array}\n4\\frac{1}{30}",
    "prompt_text": "### Exercise 6.10: Use operations with fractions to solve problems\n\n8. Habib goes home after school. He spends a $\\frac{1}{5}$ hour having lunch, then watches television for $1\\frac{2}{3}$ hours, and then does his homework for $2\\frac{1}{6}$ hours. How long did all these activities take?",
    "answer_text": "$$\\begin{array}{l}\\phantom{00}\\frac{1}{5}+1\\frac{2}{3}+2\\frac{1}{6} \\\\newline =\\frac{1}{5}+\\frac{5}{3}+\\frac{13}{6} \\\\newline =\\frac{6}{30}+\\frac{50}{30}+\\frac{65}{30} \\\\newline =\\frac{6+50+65}{30} \\\\newline =\\frac{121}{30} \\\\newline =4\\frac{1}{30}\\space\\text{hours}\\end{array}$$\nThese activities take $4\\frac{1}{30}$ hours.",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-word-problems-on-addition-and-subtraction-of-fractions"
  },
  {
    "record_id": "ch06-b055",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.6 Summary",
      "h3": null
    },
    "content_text": "- To add or subtract fractions with the same denominator:\n  - Write down the denominator.\n  - Then add or subtract the numerators.\n- To add or subtract fractions with different denominators:\n  - Find the LCD.\n  - Find equivalent fractions with the LCD as denominator.\n  - Then add or subtract the numerators.\n- To multiply fractions and whole numbers:\n  - Write down the denominator of the fraction.\n  - Multiply the numerator of the fraction by the whole number.\n- To multiply fractions with fractions:\n  - Multiply the numerators.\n  - Multiply the denominators.\n- The reciprocal of a fraction is the \"opposite\" of the fraction, which we get by swapping the numerator and denominator. Whole numbers also have reciprocals. For example:\n  - The reciprocal of $\\frac{4}{9}$ is $\\frac{9}{4}$.\n  - The reciprocal of 8 is $\\frac{1}{8}$.\n- Dividing by a fraction or whole number is the same as multiplying by its reciprocal. For example:\n  - $$\\frac{4}{9}\\div 8=\\frac{4}{9}\\times\\frac{1}{8}$$\n  - $$\\frac{4}{9}\\div \\frac{3}{5}=\\frac{4}{9}\\times\\frac{5}{3}$$\n- Before you add, subtract, multiply or divide mixed numbers, first convert them to improper fractions.\n- When you have to multiply fractions with large numerators or denominators, simplify first.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions"
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
