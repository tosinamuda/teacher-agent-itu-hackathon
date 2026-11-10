# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-2",
  "topic_key": "jss1-math-multiplications-and-divisions-of-fractions",
  "topic": "Multiplications and Divisions of Fractions",
  "subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions",
  "subtopic_title": "Division of fractions",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions-po01",
        "source_performance_objective_index": 1,
        "text": "Solve problems on division of fractions"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "division-of-fractions-ao-solve-problems",
          "text": "Solve problems on division of fractions."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch06-b030",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.5 Dividing by a fraction",
      "h3": "Division: whole number ÷ fraction"
    },
    "content_text": "Suppose there are 4 cakes available for Oluchi's birthday party. The cakes are quite small, so she wants each person to have $\\frac{2}{3}$ of a cake. How will Oluchi know how many people will get cake?\n\nOluchi must calculate $4\\div\\frac{2}{3}$. Because she wants each person to get two thirds, $\\frac{2}{3}$, she must start by cutting each cake into 3 pieces.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-030.png)\n\nNow she must work out how many people can each get $\\frac{2}{3}$ of a cake.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b031",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Dividing fractions",
      "h3": "Worked example 6.10: Dividing using diagrams: whole number ÷ fraction"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n\n$$\n4\\div\\frac{2}{3}\n$$",
    "answer_text": "Step 1: Represent all the parts of the whole number, according to the denominator of the fraction.\n\nThe denominator of the fraction is 3. We must divide 4 shapes into 3 parts each.\n\n![diagram 1](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-030.png)\n\nStep 2: Determine how many times the numerator of the fraction can be counted.\n\nThe numerator is 2. This means every 2 parts represents one count.\n\n![diagram 2](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-031.png)\n\nStep 3: Write down the answer.\n\nThere are 6 different colours. We can count every $\\frac{2}{3}$ six times. This means at Oluchi's birthday party, 6 people can each get $\\frac{2}{3}$ of a cake.\n\n$$\n4\\div\\frac{2}{3}=6\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b032",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Dividing fractions",
      "h3": "Reciprocals of fractions"
    },
    "content_text": "Division may be seen as another form of multiplication. Dividing by a fraction is the same as multiplying by the \"opposite\" of the fraction. The \"opposite\" of a fraction is called its **reciprocal**. The reciprocal is the fraction we get when we swap the numerator and the denominator. For example, the reciprocal of $\\frac{2}{7}$ is $\\frac{7}{2}$ and the reciprocal of $\\frac{8}{3}$ is $\\frac{3}{8}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b033",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Dividing fractions",
      "h3": "Reciprocals of fractions"
    },
    "content_text": "**reciprocal** The \"opposite\" of a fraction, which we get by swapping the numerator and denominator.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b034",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Dividing fractions",
      "h3": "Reciprocals of fractions"
    },
    "content_text": "Whole numbers also have reciprocals. We may write any whole number as an improper fraction with the denominator 1. For example, $5=\\frac{5}{1}$ and $13=\\frac{13}{1}$. Now we get the reciprocal by swapping the numerator and denominator. The reciprocal of 5 is $\\frac{1}{5}$ and the reciprocal of 13 is $\\frac{1}{13}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b035",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Dividing fractions",
      "h3": "Reciprocals of fractions"
    },
    "content_text": "The reciprocal of a fraction is also called its multiplicative inverse. When you multiply a fraction and its multiplicative inverse, the answer is 1.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b036",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Dividing fractions",
      "h3": "Reciprocals of fractions"
    },
    "content_text": "We may use reciprocals in division that involves fractions.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b037",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Dividing fractions",
      "h3": "Worked example 6.11: Using a reciprocal to divide: whole number ÷ fraction"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n\n$$\n4\\div\\frac{2}{3}\n$$",
    "answer_text": "Step 1: Regard division as another form of multiplication.\n\nDividing by a fraction is the same as multiplying by the reciprocal of the fraction.\n\n$$\n4\\div\\frac{2}{3}=4\\times\\frac{3}{2}\n$$\n\nStep 2: Follow the short method for multiplying whole numbers and fractions.\n\nDenominator: $\\frac{\\phantom{00}}{2}$\n\nNumerator: $4\\times3=12$\n\nCalculation:\n\n$$\n\\begin{array}{l}\n \\phantom{00}4\\times\\frac{3}{2}\\\\\n =\\frac{4\\times3}{2} \\\\\n =\\frac{12}{2}\\\\\n =\\;6\n \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b038",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Dividing fractions",
      "h3": "Exercise 6.6: Divide whole numbers by fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.6: Divide whole numbers by fractions\n\nCalculate each of the following.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b038-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Dividing fractions",
      "h3": "Exercise 6.6: Divide whole numbers by fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.6: Divide whole numbers by fractions\n\n1.\n\n$$\n2\\div\\frac{1}{6}\n$$",
    "answer_text": "Multiply by the reciprocal of the fraction.\n\n$$\n\\begin{array}{l}\n\\phantom{00}2\\times\\frac{6}{1}\\\\\n=\\frac{2\\times6}{1} \\\\\n=\\frac{12}{1}\\\\\n=\\;12\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b038-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Dividing fractions",
      "h3": "Exercise 6.6: Divide whole numbers by fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.6: Divide whole numbers by fractions\n\n2.\n\n$$\n7\\div\\frac{4}{5}\n$$",
    "answer_text": "Multiply by the reciprocal of the fraction.\n\n$$\n\\begin{array}{l}\n\\phantom{00}7\\times\\frac{5}{4}\\\\\n=\\frac{7\\times5}{4} \\\\\n=\\frac{35}{4}\\\\\n=8\\frac{3}{4}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b038-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Dividing fractions",
      "h3": "Exercise 6.6: Divide whole numbers by fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.6: Divide whole numbers by fractions\n\n3.\n\n$$\n8\\div\\frac{3}{4}\n$$",
    "answer_text": "Multiply by the reciprocal of the fraction.\n\n$$\n\\begin{array}{l}\n\\phantom{00}8\\times\\frac{4}{3}\\\\\n=\\frac{8\\times4}{3} \\\\\n=\\frac{32}{3}\\\\\n=10\\frac{2}{3}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b039",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Division: fraction ÷ whole number"
    },
    "content_text": "At Ifetayo's birthday party, there is only $\\frac{3}{4}$ of one cake left. Ifetayo wants to share this equally between her two best friends, so that they can take it home.\n\nThe cake that is left may be represented as follows:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-024.png)\n\nNow Ifetayo must figure out how she is going to share this equally between her two friends.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b040",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Worked example 6.12: Dividing using a diagram: fraction ÷ whole number"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n$$\n\\frac{3}{4}\\div2\n$$",
    "answer_text": "Step 1: Use a diagram to represent the fraction.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-024.png)\n\nStep 2: Divide the shape further, according to the whole number.\nThe whole number is 2. If we want to share the shaded portion between 2 people, we must divide each shaded part into 2 parts.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-032.png)\n\nStep 3: Share the shaded parts equally, according to the whole number.\nThe whole number is 2. If we want to share the shaded parts equally between 2 people, we simply allocate them to person 1 and person 2.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-033.png)\n\nStep 4: Write down the fraction that each person gets.\nIf we divide $\\frac{3}{4}$ between two people, each person gets $\\frac{3}{8}$.\n\nStep 5: Write down the answer.\n$$\n\\frac{3}{4}\\div2=\\frac{3}{8}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b041",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Worked example 6.13: Using a reciprocal to divide: fraction ÷ whole number"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n$$\n\\frac{3}{4}\\div2\n$$",
    "answer_text": "Step 1: Regard division as another form of multiplication.\nDividing by a whole number is the same as multiplying by the reciprocal of the whole number.\n\n$$\n\\frac{3}{4}\\times\\frac{1}{2}\n$$\n\nStep 2: Follow the short method for multiplying fractions with fractions.\n$$\n\\frac{3}{4}\\times\\frac{1}{2}=\\frac{3\\times1}{4\\times2}=\\frac{3}{8}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b042",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Exercise 6.7: Divide fractions by whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.7: Divide fractions by whole numbers\n\nCalculate each of the following.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b042-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Exercise 6.7: Divide fractions by whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.7: Divide fractions by whole numbers\n\nCalculate each of the following.\n\n1. $$\n\\frac{4}{5}\\div6\n$$",
    "answer_text": "Multiply by the reciprocal of the whole number.\n\n$$\n\\frac{4}{5}\\times\\frac{1}{6}=\\frac{4\\times1}{5\\times6}=\\frac{4}{30}=\\frac{2}{15}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b042-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Exercise 6.7: Divide fractions by whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.7: Divide fractions by whole numbers\n\nCalculate each of the following.\n\n2. $$\n\\frac{6}{15}\\div4\n$$",
    "answer_text": "Multiply by the reciprocal of the whole number.\n\n$$\n\\frac{6}{15}\\times\\frac{1}{4}=\\frac{6\\times1}{15\\times4}=\\frac{6}{60}=\\frac{1}{10}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b042-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Exercise 6.7: Divide fractions by whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.7: Divide fractions by whole numbers\n\nCalculate each of the following.\n\n3. $$\n\\frac{8}{9}\\div 10\n$$",
    "answer_text": "Multiply by the reciprocal of the whole number.\n\n$$\n\\frac{8}{9}\\times\\frac{1}{10}=\\frac{8\\times1}{9\\times10}=\\frac{8}{90}=\\frac{4}{45}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b043",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Division: fraction ÷ fraction"
    },
    "content_text": "Remember that there was only $\\frac{3}{4}$ of one cake left at Ifetayo's birthday party. Suppose, instead of dividing this between her two best friends, she rather decides to give $\\frac{1}{8}$ of the cake to as many people as possible.\n\nWe already know the cake that is left may be represented as follows:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-024.png)\n\nNow Ifetayo must figure out how many people can get $\\frac{1}{8}$ of the cake to take home. She must calculate $\\frac{3}{4}\\div\\frac{1}{8}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b044",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Worked example 6.14: Using a diagram to divide: fraction ÷ fraction"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n$$\n\\frac{3}{4}\\div\\frac{1}{8}\n$$",
    "answer_text": "Step 1: Use a diagram to represent the first fraction.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-024.png)\n\nStep 2: Divide the shape further, until the parts are equal to the denominator of the second fraction.\nThe denominator of the second fraction is 8.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-032.png)\n\nStep 3: Determine how many times the numerator of the second fraction can be counted from the shaded parts.\nThe numerator of the second fraction is 1. This means every part represents one count. Remember that we can only count shaded parts.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-034.png)\n\nStep 4: Write down the answer.\nThere are six different colours. We can count every $\\frac{1}{8}$ six times. This means that 6 people can each take home $\\frac{1}{8}$ of the cake.\n\n$$\n\\frac{3}{4}\\div\\frac{1}{8}=6\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b045",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Worked example 6.15: Using a reciprocal to divide: fraction ÷ fraction"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n$$\n\\frac{3}{4}\\div\\frac{1}{8}\n$$",
    "answer_text": "Step 1: Regard division as another form of multiplication.\nDividing by a fraction is the same as multiplying by the reciprocal of the fraction.\n\n$$\n\\frac{3}{4}\\times\\frac{8}{1}\n$$\n\nStep 2: Follow the short method for multiplying fractions with fractions.\n$$\n\\frac{3}{4}\\times\\frac{8}{1}=\\frac{3\\times8}{4\\times1}=\\frac{24}{4}=6\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b046",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Exercise 6.8: Divide fractions by fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.8: Divide fractions by fractions\n\nCalculate each of the following.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b046-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Exercise 6.8: Divide fractions by fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.8: Divide fractions by fractions\n\nCalculate each of the following.\n\n1. $$\n\\frac{3}{7}\\div\\frac{1}{2}\n$$",
    "answer_text": "Multiply by the reciprocal of the second fraction.\n\n$$\n\\frac{3}{7}\\times\\frac{2}{1}=\\frac{3\\times2}{7\\times1}=\\frac{6}{7}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b046-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Exercise 6.8: Divide fractions by fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.8: Divide fractions by fractions\n\nCalculate each of the following.\n\n2. $$\n\\frac{10}{13}\\div\\frac{3}{4}\n$$",
    "answer_text": "Multiply by the reciprocal of the second fraction.\n\n$$\n\\frac{10}{13}\\times\\frac{4}{3}=\\frac{10\\times4}{13\\times3}=\\frac{40}{39}=1\\frac{1}{39}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b046-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Exercise 6.8: Divide fractions by fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.8: Divide fractions by fractions\n\nCalculate each of the following.\n\n3. $$\n\\frac{12}{15}\\div\\frac{3}{5}\n$$",
    "answer_text": "Multiply by the reciprocal of the second fraction.\n\n$$\n\\frac{12}{15}\\times\\frac{5}{3}=\\frac{12\\times5}{15\\times3}=\\frac{60}{45}=\\frac{4}{3}=1\\frac{1}{3}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b047",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Multiplying and dividing mixed numbers"
    },
    "content_text": "There are various methods that may be used to multiply and divide mixed numbers. It is recommended that you first convert all mixed numbers to improper fractions before you multiply or divide.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b048",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Multiplying and dividing mixed numbers"
    },
    "content_text": "If necessary, go back to Chapter 4 and revise how to convert mixed numbers to improper fractions.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b049",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Simplifying before multiplying"
    },
    "content_text": "Improper fractions sometimes involve large numbers that are not so easy to multiply. To make things easier, you should try to simplify the numerators and denominators before you multiply them.\n\nNote that the order in which we multiply numbers do not affect the answer. For example:\n\n- $3\\times5=15$ and $5\\times3=15$\n- $\\frac{4}{5}\\times\\frac{1}{3}=\\frac{4}{15}$ and $\\frac{1}{3}\\times\\frac{4}{5}=\\frac{4}{15}$\n\nIn Chapter 4 you learnt that equivalent factors have the same value. We find equivalent factors by multiplying or dividing the numerator and denominator by the same number. For example:\n\n$$\\frac{12\\div2}{16\\div 2}=\\frac{6}{8}$$\n\n$$\\frac{6\\div2}{8\\div2}=\\frac{3}{4}$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b050",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Worked example 6.16: Dividing mixed numbers"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n\n$$2\\frac{5}{8}\\div3\\frac{3}{4}$$",
    "answer_text": "Step 1: Convert the mixed numbers to improper fractions.\n\n$$2\\frac{5}{8}=\\frac{(8\\times2)+5}{8}=\\frac{21}{8}$$\n\n$$3\\frac{3}{4}=\\frac{(4\\times3)+3}{4}=\\frac{15}{4}$$\n\nStep 2: Regard division as another form of multiplication.\n\nDividing by a fraction is the same as multiplying by the reciprocal of the fraction.\n\n$$\\frac{21}{8}\\times\\frac{4}{15}$$\n\nStep 3: Write down the first step for multiplying fractions by fractions. Then see whether there are numerator and denominator pairs that have common factors.\n\n$$\\frac{21\\times4}{8\\times15}$$\n\nThe HCF of 4 and 8 is 4.\nThe HCF of 21 and 15 is 3.\n\nIf necessary, go back to Chapter 2 to revise how to find the highest common factor (HCF) of two or more numbers.\n\n$$\\frac{\\color{red}{4}\\; \\color{black}{\\times}\\; \\color{green}{21}}{\\color{red}{8}\\; \\color{black}{\\times}\\;\\color{green}{15}}$$\n\nStep 4: Divide by the common factors you identified in Step 3.\n\n$$\\frac{\\color{red}{4\\div4}\\; \\color{black}{\\times}\\; \\color{green}{21\\div3}}{\\color{red}{8\\div4}\\; \\color{black}{\\times}\\;\\color{green}{15\\div3}}$$\n\nStep 5: Write down the simplified expression and calculate the answer.\n\n$$\\frac{1\\times7}{2\\times5}=\\frac{7}{10}$$\n\nStep 6: Check that the answer is in its simplest form. Write improper fractions as mixed numbers.\n\nIn this case, the answer is in its simplest form.",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b051",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Simplifying before multiplying"
    },
    "content_text": "If necessary, go back to Chapter 4 and revise how to convert improper fractions to mixed numbers.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b052",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Exercise 6.9: Multiply and divide mixed numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.9: Multiply and divide mixed numbers",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b052-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Exercise 6.9: Multiply and divide mixed numbers"
    },
    "content_text": "Source math retained:\n7 rac{1}{8}= rac{(8 imes7)+1}{8}= rac{57}{8}\n4 rac{3}{4}= rac{(4 imes4)+3}{4}= rac{19}{4}\nrac{57}{8}\\div rac{19}{4}= rac{57}{8} \\times \\frac{4}{19}= \\frac{57\\times4}{8\\times19}\nrac{(57\\div19)\\times(4\\div4)}{(19\\div19)\\times(8\\div4)}=\\frac{3\\times1}{1\\times2}=\\frac{3}{2}=1\\frac{1}{2}",
    "prompt_text": "### Exercise 6.9: Multiply and divide mixed numbers\n\n3. $7\\frac{1}{8}\\div4\\frac{3}{4}$",
    "answer_text": "$$7\\frac{1}{8}=\\frac{(8\\times7)+1}{8}=\\frac{57}{8}$$\n$$4\\frac{3}{4}=\\frac{(4\\times4)+3}{4}=\\frac{19}{4}$$\n$$\\frac{57}{8}\\div\\frac{19}{4}=\\frac{57}{8} \\times \\frac{4}{19}= \\frac{57\\times4}{8\\times19}$$\nThe HCF of 4 and 8 is 4.\nThe HCF of 57 and 19 is 19.\n$$\\frac{(57\\div19)\\times(4\\div4)}{(19\\div19)\\times(8\\div4)}=\\frac{3\\times1}{1\\times2}=\\frac{3}{2}=1\\frac{1}{2}$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b052-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Exercise 6.9: Multiply and divide mixed numbers"
    },
    "content_text": "Source math retained:\n4 rac{1}{6}= rac{(6 imes4)+1}{6}= rac{25}{6}\n3 rac{8}{9}= rac{(9 imes3)+8}{9}= rac{35}{9}\nrac{25}{6}\\div rac{35}{9}= rac{25}{6} \\times \\frac{9}{35}= \\frac{25\\times9}{6\\times35}\nrac{(25\\div5)\\times(9\\div3)}{(35\\div5)\\times(6\\div3)}=\\frac{5\\times3}{7\\times2}=\\frac{15}{14}=1\\frac{1}{14}",
    "prompt_text": "### Exercise 6.9: Multiply and divide mixed numbers\n\n4. $4\\frac{1}{6}\\div3\\frac{8}{9}$",
    "answer_text": "$$4\\frac{1}{6}=\\frac{(6\\times4)+1}{6}=\\frac{25}{6}$$\n$$3\\frac{8}{9}=\\frac{(9\\times3)+8}{9}=\\frac{35}{9}$$\n$$\\frac{25}{6}\\div\\frac{35}{9}=\\frac{25}{6} \\times \\frac{9}{35}= \\frac{25\\times9}{6\\times35}$$\nThe HCF of 6 and 9 is 3.\nThe HCF of 35 and 25 is 5.\n$$\\frac{(25\\div5)\\times(9\\div3)}{(35\\div5)\\times(6\\div3)}=\\frac{5\\times3}{7\\times2}=\\frac{15}{14}=1\\frac{1}{14}$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b052-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Exercise 6.9: Multiply and divide mixed numbers"
    },
    "content_text": "Source math retained:\n6 rac{3}{10}= rac{(10 imes6)+3}{10}= rac{63}{10}\n1 rac{4}{5}= rac{(5 imes1)+4}{5}= rac{9}{5}\nrac{63}{10}\\div rac{9}{5}= rac{63}{10} \\times \\frac{5}{9}= \\frac{63\\times5}{10\\times9}\nrac{(63\\div9)\\times(5\\div5)}{(9\\div9)\\times(10\\div5)}=\\frac{7\\times1}{1\\times2}=\\frac{7}{2}=3\\frac{1}{2}",
    "prompt_text": "### Exercise 6.9: Multiply and divide mixed numbers\n\n5. $6\\frac{3}{10}\\div1\\frac{4}{5}$",
    "answer_text": "$$6\\frac{3}{10}=\\frac{(10\\times6)+3}{10}=\\frac{63}{10}$$\n$$1\\frac{4}{5}=\\frac{(5\\times1)+4}{5}=\\frac{9}{5}$$\n$$\\frac{63}{10}\\div\\frac{9}{5}=\\frac{63}{10} \\times \\frac{5}{9}= \\frac{63\\times5}{10\\times9}$$\nThe HCF of 5 and 10 is 5.\nThe HCF of 63 and 9 is 9.\n$$\\frac{(63\\div9)\\times(5\\div5)}{(9\\div9)\\times(10\\div5)}=\\frac{7\\times1}{1\\times2}=\\frac{7}{2}=3\\frac{1}{2}$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b054-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.3 Practical applications",
      "h3": "Exercise 6.10: Use operations with fractions to solve problems"
    },
    "content_text": "Source math retained:\n\\frac{6}{15}\n\\begin{array}{l}\\phantom{00}50\\div\\frac{6}{15} \\\\ =50\\times\\frac{15}{6} \\\\ =\\frac{50\\times15}{6} \\\\ =\\frac{750}{6} \\\\ = 125\\end{array}",
    "prompt_text": "### Exercise 6.10: Use operations with fractions to solve problems\n\n6. A local store owner buys rice in bags of 50 kg. He then makes up smaller bags to sell. If a small bag is $\\frac{6}{15}$ kg, how many small bags can he make up from one large bag?",
    "answer_text": "$$\\begin{array}{l}\\phantom{00}50\\div\\frac{6}{15} \\\\newline =50\\times\\frac{15}{6} \\\\newline =\\frac{50\\times15}{6} \\\\newline =\\frac{750}{6} \\\\newline =\\;125\\end{array}$$\nThe store owner can make up 125 small bags from one large bag.",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-word-problems-involving-multiplication-and-division-of-fractions"
  },
  {
    "record_id": "ch06-b054-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.3 Practical applications",
      "h3": "Exercise 6.10: Use operations with fractions to solve problems"
    },
    "content_text": "Source math retained:\n\\frac{14}{16}\n\\frac{1}{4}\n\\frac{14}{16}\\div\\frac{1}{4}=\\frac{14}{16}\\times\\frac{4}{1}=\\frac{14\\times4}{16\\times1}=\\frac{56}{16}=\\frac{7}{2} =3\\frac{1}{2}\n3\\frac{1}{2}",
    "prompt_text": "### Exercise 6.10: Use operations with fractions to solve problems\n\n7. There is $\\frac{14}{16}$ litre of vegetable oil left in a bottle. A baker must measure this out in cups of $\\frac{1}{4}$ litre each. How many cups will she measure out?",
    "answer_text": "$$\\frac{14}{16}\\div\\frac{1}{4}=\\frac{14}{16}\\times\\frac{4}{1}=\\frac{14\\times4}{16\\times1}=\\frac{56}{16}=\\frac{7}{2}=3\\frac{1}{2}$$\nThe baker can measure out $3\\frac{1}{2}$ cups.",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-word-problems-involving-multiplication-and-division-of-fractions"
  },
  {
    "record_id": "ch06-b054-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.3 Practical applications",
      "h3": "Exercise 6.10: Use operations with fractions to solve problems"
    },
    "content_text": "Source math retained:\n10\\frac{5}{6}\n2\\frac{1}{2}\n10\\frac{5}{6}=\\frac{65}{6}\n2\\frac{1}{2}=\\frac{5}{2}\n\\frac{65}{6}\\div\\frac{5}{2}=\\frac{65}{6} \\times \\frac{2}{5}= \\frac{65\\times2}{6\\times5}\n\\frac{(65\\div5)\\times(2\\div2)}{(5\\div5)\\times(6\\div2)}=\\frac{13\\times1}{1\\times3}=\\frac{13}{3}=4\\frac{1}{3}\n4\\frac{1}{3}",
    "prompt_text": "### Exercise 6.10: Use operations with fractions to solve problems\n\n10. A bag of garri has a mass of $10\\frac{5}{6}$ kg. How many small packets, each with a mass of $2\\frac{1}{2}$ kg, can be made up from the bag?",
    "answer_text": "$$10\\frac{5}{6}=\\frac{65}{6}$$\n$$2\\frac{1}{2}=\\frac{5}{2}$$\n$$\\frac{65}{6}\\div\\frac{5}{2}=\\frac{65}{6} \\times \\frac{2}{5}= \\frac{65\\times2}{6\\times5}$$\n$$\\frac{(65\\div5)\\times(2\\div2)}{(5\\div5)\\times(6\\div2)}=\\frac{13\\times1}{1\\times3}=\\frac{13}{3}=4\\frac{1}{3}$$\n$4\\frac{1}{3}$ small packets can be made up.",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-word-problems-involving-multiplication-and-division-of-fractions"
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
  "topic_key": "jss1-math-multiplications-and-divisions-of-fractions",
  "topic": "Multiplications and Divisions of Fractions",
  "subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions",
  "subtopic_title": "Division of fractions",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions-po01",
        "source_performance_objective_index": 1,
        "text": "Solve problems on division of fractions"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "division-of-fractions-ao-solve-problems",
          "text": "Solve problems on division of fractions."
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
    "record_id": "ch06-b030",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.5 Dividing by a fraction",
      "h3": "Division: whole number ÷ fraction"
    },
    "content_text": "Suppose there are 4 cakes available for Oluchi's birthday party. The cakes are quite small, so she wants each person to have $\\frac{2}{3}$ of a cake. How will Oluchi know how many people will get cake?\n\nOluchi must calculate $4\\div\\frac{2}{3}$. Because she wants each person to get two thirds, $\\frac{2}{3}$, she must start by cutting each cake into 3 pieces.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-030.png)\n\nNow she must work out how many people can each get $\\frac{2}{3}$ of a cake.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b031",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Dividing fractions",
      "h3": "Worked example 6.10: Dividing using diagrams: whole number ÷ fraction"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n\n$$\n4\\div\\frac{2}{3}\n$$",
    "answer_text": "Step 1: Represent all the parts of the whole number, according to the denominator of the fraction.\n\nThe denominator of the fraction is 3. We must divide 4 shapes into 3 parts each.\n\n![diagram 1](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-030.png)\n\nStep 2: Determine how many times the numerator of the fraction can be counted.\n\nThe numerator is 2. This means every 2 parts represents one count.\n\n![diagram 2](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-031.png)\n\nStep 3: Write down the answer.\n\nThere are 6 different colours. We can count every $\\frac{2}{3}$ six times. This means at Oluchi's birthday party, 6 people can each get $\\frac{2}{3}$ of a cake.\n\n$$\n4\\div\\frac{2}{3}=6\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b032",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Dividing fractions",
      "h3": "Reciprocals of fractions"
    },
    "content_text": "Division may be seen as another form of multiplication. Dividing by a fraction is the same as multiplying by the \"opposite\" of the fraction. The \"opposite\" of a fraction is called its **reciprocal**. The reciprocal is the fraction we get when we swap the numerator and the denominator. For example, the reciprocal of $\\frac{2}{7}$ is $\\frac{7}{2}$ and the reciprocal of $\\frac{8}{3}$ is $\\frac{3}{8}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b033",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Dividing fractions",
      "h3": "Reciprocals of fractions"
    },
    "content_text": "**reciprocal** The \"opposite\" of a fraction, which we get by swapping the numerator and denominator.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b034",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Dividing fractions",
      "h3": "Reciprocals of fractions"
    },
    "content_text": "Whole numbers also have reciprocals. We may write any whole number as an improper fraction with the denominator 1. For example, $5=\\frac{5}{1}$ and $13=\\frac{13}{1}$. Now we get the reciprocal by swapping the numerator and denominator. The reciprocal of 5 is $\\frac{1}{5}$ and the reciprocal of 13 is $\\frac{1}{13}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b035",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Dividing fractions",
      "h3": "Reciprocals of fractions"
    },
    "content_text": "The reciprocal of a fraction is also called its multiplicative inverse. When you multiply a fraction and its multiplicative inverse, the answer is 1.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b036",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Dividing fractions",
      "h3": "Reciprocals of fractions"
    },
    "content_text": "We may use reciprocals in division that involves fractions.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b037",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Dividing fractions",
      "h3": "Worked example 6.11: Using a reciprocal to divide: whole number ÷ fraction"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n\n$$\n4\\div\\frac{2}{3}\n$$",
    "answer_text": "Step 1: Regard division as another form of multiplication.\n\nDividing by a fraction is the same as multiplying by the reciprocal of the fraction.\n\n$$\n4\\div\\frac{2}{3}=4\\times\\frac{3}{2}\n$$\n\nStep 2: Follow the short method for multiplying whole numbers and fractions.\n\nDenominator: $\\frac{\\phantom{00}}{2}$\n\nNumerator: $4\\times3=12$\n\nCalculation:\n\n$$\n\\begin{array}{l}\n \\phantom{00}4\\times\\frac{3}{2}\\\\\n =\\frac{4\\times3}{2} \\\\\n =\\frac{12}{2}\\\\\n =\\;6\n \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b038",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Dividing fractions",
      "h3": "Exercise 6.6: Divide whole numbers by fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.6: Divide whole numbers by fractions\n\nCalculate each of the following.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b038-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Dividing fractions",
      "h3": "Exercise 6.6: Divide whole numbers by fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.6: Divide whole numbers by fractions\n\n1.\n\n$$\n2\\div\\frac{1}{6}\n$$",
    "answer_text": "Multiply by the reciprocal of the fraction.\n\n$$\n\\begin{array}{l}\n\\phantom{00}2\\times\\frac{6}{1}\\\\\n=\\frac{2\\times6}{1} \\\\\n=\\frac{12}{1}\\\\\n=\\;12\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b038-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Dividing fractions",
      "h3": "Exercise 6.6: Divide whole numbers by fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.6: Divide whole numbers by fractions\n\n2.\n\n$$\n7\\div\\frac{4}{5}\n$$",
    "answer_text": "Multiply by the reciprocal of the fraction.\n\n$$\n\\begin{array}{l}\n\\phantom{00}7\\times\\frac{5}{4}\\\\\n=\\frac{7\\times5}{4} \\\\\n=\\frac{35}{4}\\\\\n=8\\frac{3}{4}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b038-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Dividing fractions",
      "h3": "Exercise 6.6: Divide whole numbers by fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.6: Divide whole numbers by fractions\n\n3.\n\n$$\n8\\div\\frac{3}{4}\n$$",
    "answer_text": "Multiply by the reciprocal of the fraction.\n\n$$\n\\begin{array}{l}\n\\phantom{00}8\\times\\frac{4}{3}\\\\\n=\\frac{8\\times4}{3} \\\\\n=\\frac{32}{3}\\\\\n=10\\frac{2}{3}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b039",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Division: fraction ÷ whole number"
    },
    "content_text": "At Ifetayo's birthday party, there is only $\\frac{3}{4}$ of one cake left. Ifetayo wants to share this equally between her two best friends, so that they can take it home.\n\nThe cake that is left may be represented as follows:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-024.png)\n\nNow Ifetayo must figure out how she is going to share this equally between her two friends.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b040",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Worked example 6.12: Dividing using a diagram: fraction ÷ whole number"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n$$\n\\frac{3}{4}\\div2\n$$",
    "answer_text": "Step 1: Use a diagram to represent the fraction.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-024.png)\n\nStep 2: Divide the shape further, according to the whole number.\nThe whole number is 2. If we want to share the shaded portion between 2 people, we must divide each shaded part into 2 parts.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-032.png)\n\nStep 3: Share the shaded parts equally, according to the whole number.\nThe whole number is 2. If we want to share the shaded parts equally between 2 people, we simply allocate them to person 1 and person 2.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-033.png)\n\nStep 4: Write down the fraction that each person gets.\nIf we divide $\\frac{3}{4}$ between two people, each person gets $\\frac{3}{8}$.\n\nStep 5: Write down the answer.\n$$\n\\frac{3}{4}\\div2=\\frac{3}{8}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b041",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Worked example 6.13: Using a reciprocal to divide: fraction ÷ whole number"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n$$\n\\frac{3}{4}\\div2\n$$",
    "answer_text": "Step 1: Regard division as another form of multiplication.\nDividing by a whole number is the same as multiplying by the reciprocal of the whole number.\n\n$$\n\\frac{3}{4}\\times\\frac{1}{2}\n$$\n\nStep 2: Follow the short method for multiplying fractions with fractions.\n$$\n\\frac{3}{4}\\times\\frac{1}{2}=\\frac{3\\times1}{4\\times2}=\\frac{3}{8}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b042",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Exercise 6.7: Divide fractions by whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.7: Divide fractions by whole numbers\n\nCalculate each of the following.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b042-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Exercise 6.7: Divide fractions by whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.7: Divide fractions by whole numbers\n\nCalculate each of the following.\n\n1. $$\n\\frac{4}{5}\\div6\n$$",
    "answer_text": "Multiply by the reciprocal of the whole number.\n\n$$\n\\frac{4}{5}\\times\\frac{1}{6}=\\frac{4\\times1}{5\\times6}=\\frac{4}{30}=\\frac{2}{15}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b042-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Exercise 6.7: Divide fractions by whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.7: Divide fractions by whole numbers\n\nCalculate each of the following.\n\n2. $$\n\\frac{6}{15}\\div4\n$$",
    "answer_text": "Multiply by the reciprocal of the whole number.\n\n$$\n\\frac{6}{15}\\times\\frac{1}{4}=\\frac{6\\times1}{15\\times4}=\\frac{6}{60}=\\frac{1}{10}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b042-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Exercise 6.7: Divide fractions by whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.7: Divide fractions by whole numbers\n\nCalculate each of the following.\n\n3. $$\n\\frac{8}{9}\\div 10\n$$",
    "answer_text": "Multiply by the reciprocal of the whole number.\n\n$$\n\\frac{8}{9}\\times\\frac{1}{10}=\\frac{8\\times1}{9\\times10}=\\frac{8}{90}=\\frac{4}{45}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b043",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Division: fraction ÷ fraction"
    },
    "content_text": "Remember that there was only $\\frac{3}{4}$ of one cake left at Ifetayo's birthday party. Suppose, instead of dividing this between her two best friends, she rather decides to give $\\frac{1}{8}$ of the cake to as many people as possible.\n\nWe already know the cake that is left may be represented as follows:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-024.png)\n\nNow Ifetayo must figure out how many people can get $\\frac{1}{8}$ of the cake to take home. She must calculate $\\frac{3}{4}\\div\\frac{1}{8}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b044",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Worked example 6.14: Using a diagram to divide: fraction ÷ fraction"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n$$\n\\frac{3}{4}\\div\\frac{1}{8}\n$$",
    "answer_text": "Step 1: Use a diagram to represent the first fraction.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-024.png)\n\nStep 2: Divide the shape further, until the parts are equal to the denominator of the second fraction.\nThe denominator of the second fraction is 8.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-032.png)\n\nStep 3: Determine how many times the numerator of the second fraction can be counted from the shaded parts.\nThe numerator of the second fraction is 1. This means every part represents one count. Remember that we can only count shaded parts.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-034.png)\n\nStep 4: Write down the answer.\nThere are six different colours. We can count every $\\frac{1}{8}$ six times. This means that 6 people can each take home $\\frac{1}{8}$ of the cake.\n\n$$\n\\frac{3}{4}\\div\\frac{1}{8}=6\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b045",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Worked example 6.15: Using a reciprocal to divide: fraction ÷ fraction"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n$$\n\\frac{3}{4}\\div\\frac{1}{8}\n$$",
    "answer_text": "Step 1: Regard division as another form of multiplication.\nDividing by a fraction is the same as multiplying by the reciprocal of the fraction.\n\n$$\n\\frac{3}{4}\\times\\frac{8}{1}\n$$\n\nStep 2: Follow the short method for multiplying fractions with fractions.\n$$\n\\frac{3}{4}\\times\\frac{8}{1}=\\frac{3\\times8}{4\\times1}=\\frac{24}{4}=6\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b046",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Exercise 6.8: Divide fractions by fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.8: Divide fractions by fractions\n\nCalculate each of the following.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b046-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Exercise 6.8: Divide fractions by fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.8: Divide fractions by fractions\n\nCalculate each of the following.\n\n1. $$\n\\frac{3}{7}\\div\\frac{1}{2}\n$$",
    "answer_text": "Multiply by the reciprocal of the second fraction.\n\n$$\n\\frac{3}{7}\\times\\frac{2}{1}=\\frac{3\\times2}{7\\times1}=\\frac{6}{7}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b046-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Exercise 6.8: Divide fractions by fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.8: Divide fractions by fractions\n\nCalculate each of the following.\n\n2. $$\n\\frac{10}{13}\\div\\frac{3}{4}\n$$",
    "answer_text": "Multiply by the reciprocal of the second fraction.\n\n$$\n\\frac{10}{13}\\times\\frac{4}{3}=\\frac{10\\times4}{13\\times3}=\\frac{40}{39}=1\\frac{1}{39}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b046-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.7 Division of fractions",
      "h3": "Exercise 6.8: Divide fractions by fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.8: Divide fractions by fractions\n\nCalculate each of the following.\n\n3. $$\n\\frac{12}{15}\\div\\frac{3}{5}\n$$",
    "answer_text": "Multiply by the reciprocal of the second fraction.\n\n$$\n\\frac{12}{15}\\times\\frac{5}{3}=\\frac{12\\times5}{15\\times3}=\\frac{60}{45}=\\frac{4}{3}=1\\frac{1}{3}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b047",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Multiplying and dividing mixed numbers"
    },
    "content_text": "There are various methods that may be used to multiply and divide mixed numbers. It is recommended that you first convert all mixed numbers to improper fractions before you multiply or divide.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b048",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Multiplying and dividing mixed numbers"
    },
    "content_text": "If necessary, go back to Chapter 4 and revise how to convert mixed numbers to improper fractions.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b049",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Simplifying before multiplying"
    },
    "content_text": "Improper fractions sometimes involve large numbers that are not so easy to multiply. To make things easier, you should try to simplify the numerators and denominators before you multiply them.\n\nNote that the order in which we multiply numbers do not affect the answer. For example:\n\n- $3\\times5=15$ and $5\\times3=15$\n- $\\frac{4}{5}\\times\\frac{1}{3}=\\frac{4}{15}$ and $\\frac{1}{3}\\times\\frac{4}{5}=\\frac{4}{15}$\n\nIn Chapter 4 you learnt that equivalent factors have the same value. We find equivalent factors by multiplying or dividing the numerator and denominator by the same number. For example:\n\n$$\\frac{12\\div2}{16\\div 2}=\\frac{6}{8}$$\n\n$$\\frac{6\\div2}{8\\div2}=\\frac{3}{4}$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b050",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Worked example 6.16: Dividing mixed numbers"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n\n$$2\\frac{5}{8}\\div3\\frac{3}{4}$$",
    "answer_text": "Step 1: Convert the mixed numbers to improper fractions.\n\n$$2\\frac{5}{8}=\\frac{(8\\times2)+5}{8}=\\frac{21}{8}$$\n\n$$3\\frac{3}{4}=\\frac{(4\\times3)+3}{4}=\\frac{15}{4}$$\n\nStep 2: Regard division as another form of multiplication.\n\nDividing by a fraction is the same as multiplying by the reciprocal of the fraction.\n\n$$\\frac{21}{8}\\times\\frac{4}{15}$$\n\nStep 3: Write down the first step for multiplying fractions by fractions. Then see whether there are numerator and denominator pairs that have common factors.\n\n$$\\frac{21\\times4}{8\\times15}$$\n\nThe HCF of 4 and 8 is 4.\nThe HCF of 21 and 15 is 3.\n\nIf necessary, go back to Chapter 2 to revise how to find the highest common factor (HCF) of two or more numbers.\n\n$$\\frac{\\color{red}{4}\\; \\color{black}{\\times}\\; \\color{green}{21}}{\\color{red}{8}\\; \\color{black}{\\times}\\;\\color{green}{15}}$$\n\nStep 4: Divide by the common factors you identified in Step 3.\n\n$$\\frac{\\color{red}{4\\div4}\\; \\color{black}{\\times}\\; \\color{green}{21\\div3}}{\\color{red}{8\\div4}\\; \\color{black}{\\times}\\;\\color{green}{15\\div3}}$$\n\nStep 5: Write down the simplified expression and calculate the answer.\n\n$$\\frac{1\\times7}{2\\times5}=\\frac{7}{10}$$\n\nStep 6: Check that the answer is in its simplest form. Write improper fractions as mixed numbers.\n\nIn this case, the answer is in its simplest form.",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b051",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Simplifying before multiplying"
    },
    "content_text": "If necessary, go back to Chapter 4 and revise how to convert improper fractions to mixed numbers.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b052",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Exercise 6.9: Multiply and divide mixed numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.9: Multiply and divide mixed numbers",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b052-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Exercise 6.9: Multiply and divide mixed numbers"
    },
    "content_text": "Source math retained:\n7 rac{1}{8}= rac{(8 imes7)+1}{8}= rac{57}{8}\n4 rac{3}{4}= rac{(4 imes4)+3}{4}= rac{19}{4}\nrac{57}{8}\\div rac{19}{4}= rac{57}{8} \\times \\frac{4}{19}= \\frac{57\\times4}{8\\times19}\nrac{(57\\div19)\\times(4\\div4)}{(19\\div19)\\times(8\\div4)}=\\frac{3\\times1}{1\\times2}=\\frac{3}{2}=1\\frac{1}{2}",
    "prompt_text": "### Exercise 6.9: Multiply and divide mixed numbers\n\n3. $7\\frac{1}{8}\\div4\\frac{3}{4}$",
    "answer_text": "$$7\\frac{1}{8}=\\frac{(8\\times7)+1}{8}=\\frac{57}{8}$$\n$$4\\frac{3}{4}=\\frac{(4\\times4)+3}{4}=\\frac{19}{4}$$\n$$\\frac{57}{8}\\div\\frac{19}{4}=\\frac{57}{8} \\times \\frac{4}{19}= \\frac{57\\times4}{8\\times19}$$\nThe HCF of 4 and 8 is 4.\nThe HCF of 57 and 19 is 19.\n$$\\frac{(57\\div19)\\times(4\\div4)}{(19\\div19)\\times(8\\div4)}=\\frac{3\\times1}{1\\times2}=\\frac{3}{2}=1\\frac{1}{2}$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b052-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Exercise 6.9: Multiply and divide mixed numbers"
    },
    "content_text": "Source math retained:\n4 rac{1}{6}= rac{(6 imes4)+1}{6}= rac{25}{6}\n3 rac{8}{9}= rac{(9 imes3)+8}{9}= rac{35}{9}\nrac{25}{6}\\div rac{35}{9}= rac{25}{6} \\times \\frac{9}{35}= \\frac{25\\times9}{6\\times35}\nrac{(25\\div5)\\times(9\\div3)}{(35\\div5)\\times(6\\div3)}=\\frac{5\\times3}{7\\times2}=\\frac{15}{14}=1\\frac{1}{14}",
    "prompt_text": "### Exercise 6.9: Multiply and divide mixed numbers\n\n4. $4\\frac{1}{6}\\div3\\frac{8}{9}$",
    "answer_text": "$$4\\frac{1}{6}=\\frac{(6\\times4)+1}{6}=\\frac{25}{6}$$\n$$3\\frac{8}{9}=\\frac{(9\\times3)+8}{9}=\\frac{35}{9}$$\n$$\\frac{25}{6}\\div\\frac{35}{9}=\\frac{25}{6} \\times \\frac{9}{35}= \\frac{25\\times9}{6\\times35}$$\nThe HCF of 6 and 9 is 3.\nThe HCF of 35 and 25 is 5.\n$$\\frac{(25\\div5)\\times(9\\div3)}{(35\\div5)\\times(6\\div3)}=\\frac{5\\times3}{7\\times2}=\\frac{15}{14}=1\\frac{1}{14}$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b052-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Exercise 6.9: Multiply and divide mixed numbers"
    },
    "content_text": "Source math retained:\n6 rac{3}{10}= rac{(10 imes6)+3}{10}= rac{63}{10}\n1 rac{4}{5}= rac{(5 imes1)+4}{5}= rac{9}{5}\nrac{63}{10}\\div rac{9}{5}= rac{63}{10} \\times \\frac{5}{9}= \\frac{63\\times5}{10\\times9}\nrac{(63\\div9)\\times(5\\div5)}{(9\\div9)\\times(10\\div5)}=\\frac{7\\times1}{1\\times2}=\\frac{7}{2}=3\\frac{1}{2}",
    "prompt_text": "### Exercise 6.9: Multiply and divide mixed numbers\n\n5. $6\\frac{3}{10}\\div1\\frac{4}{5}$",
    "answer_text": "$$6\\frac{3}{10}=\\frac{(10\\times6)+3}{10}=\\frac{63}{10}$$\n$$1\\frac{4}{5}=\\frac{(5\\times1)+4}{5}=\\frac{9}{5}$$\n$$\\frac{63}{10}\\div\\frac{9}{5}=\\frac{63}{10} \\times \\frac{5}{9}= \\frac{63\\times5}{10\\times9}$$\nThe HCF of 5 and 10 is 5.\nThe HCF of 63 and 9 is 9.\n$$\\frac{(63\\div9)\\times(5\\div5)}{(9\\div9)\\times(10\\div5)}=\\frac{7\\times1}{1\\times2}=\\frac{7}{2}=3\\frac{1}{2}$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions"
  },
  {
    "record_id": "ch06-b054-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.3 Practical applications",
      "h3": "Exercise 6.10: Use operations with fractions to solve problems"
    },
    "content_text": "Source math retained:\n\\frac{6}{15}\n\\begin{array}{l}\\phantom{00}50\\div\\frac{6}{15} \\\\ =50\\times\\frac{15}{6} \\\\ =\\frac{50\\times15}{6} \\\\ =\\frac{750}{6} \\\\ = 125\\end{array}",
    "prompt_text": "### Exercise 6.10: Use operations with fractions to solve problems\n\n6. A local store owner buys rice in bags of 50 kg. He then makes up smaller bags to sell. If a small bag is $\\frac{6}{15}$ kg, how many small bags can he make up from one large bag?",
    "answer_text": "$$\\begin{array}{l}\\phantom{00}50\\div\\frac{6}{15} \\\\newline =50\\times\\frac{15}{6} \\\\newline =\\frac{50\\times15}{6} \\\\newline =\\frac{750}{6} \\\\newline =\\;125\\end{array}$$\nThe store owner can make up 125 small bags from one large bag.",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-word-problems-involving-multiplication-and-division-of-fractions"
  },
  {
    "record_id": "ch06-b054-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.3 Practical applications",
      "h3": "Exercise 6.10: Use operations with fractions to solve problems"
    },
    "content_text": "Source math retained:\n\\frac{14}{16}\n\\frac{1}{4}\n\\frac{14}{16}\\div\\frac{1}{4}=\\frac{14}{16}\\times\\frac{4}{1}=\\frac{14\\times4}{16\\times1}=\\frac{56}{16}=\\frac{7}{2} =3\\frac{1}{2}\n3\\frac{1}{2}",
    "prompt_text": "### Exercise 6.10: Use operations with fractions to solve problems\n\n7. There is $\\frac{14}{16}$ litre of vegetable oil left in a bottle. A baker must measure this out in cups of $\\frac{1}{4}$ litre each. How many cups will she measure out?",
    "answer_text": "$$\\frac{14}{16}\\div\\frac{1}{4}=\\frac{14}{16}\\times\\frac{4}{1}=\\frac{14\\times4}{16\\times1}=\\frac{56}{16}=\\frac{7}{2}=3\\frac{1}{2}$$\nThe baker can measure out $3\\frac{1}{2}$ cups.",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-word-problems-involving-multiplication-and-division-of-fractions"
  },
  {
    "record_id": "ch06-b054-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.3 Practical applications",
      "h3": "Exercise 6.10: Use operations with fractions to solve problems"
    },
    "content_text": "Source math retained:\n10\\frac{5}{6}\n2\\frac{1}{2}\n10\\frac{5}{6}=\\frac{65}{6}\n2\\frac{1}{2}=\\frac{5}{2}\n\\frac{65}{6}\\div\\frac{5}{2}=\\frac{65}{6} \\times \\frac{2}{5}= \\frac{65\\times2}{6\\times5}\n\\frac{(65\\div5)\\times(2\\div2)}{(5\\div5)\\times(6\\div2)}=\\frac{13\\times1}{1\\times3}=\\frac{13}{3}=4\\frac{1}{3}\n4\\frac{1}{3}",
    "prompt_text": "### Exercise 6.10: Use operations with fractions to solve problems\n\n10. A bag of garri has a mass of $10\\frac{5}{6}$ kg. How many small packets, each with a mass of $2\\frac{1}{2}$ kg, can be made up from the bag?",
    "answer_text": "$$10\\frac{5}{6}=\\frac{65}{6}$$\n$$2\\frac{1}{2}=\\frac{5}{2}$$\n$$\\frac{65}{6}\\div\\frac{5}{2}=\\frac{65}{6} \\times \\frac{2}{5}= \\frac{65\\times2}{6\\times5}$$\n$$\\frac{(65\\div5)\\times(2\\div2)}{(5\\div5)\\times(6\\div2)}=\\frac{13\\times1}{1\\times3}=\\frac{13}{3}=4\\frac{1}{3}$$\n$4\\frac{1}{3}$ small packets can be made up.",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-word-problems-involving-multiplication-and-division-of-fractions"
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
