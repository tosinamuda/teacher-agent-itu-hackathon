# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-2",
  "topic_key": "jss1-math-multiplications-and-divisions-of-fractions",
  "topic": "Multiplications and Divisions of Fractions",
  "subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions",
  "subtopic_title": "Multiplication of fractions",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions-po01",
        "source_performance_objective_index": 1,
        "text": "Solve problems on multiplication of fractions"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "multiplication-of-fractions-ao-solve-problems",
          "text": "Solve problems on multiplication of fractions."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch06-b019",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Multiplication: whole number x fraction"
    },
    "content_text": "You might remember from previous years that multiplication is a form of addition. For example, $5 \\times \\triangle$ means $\\triangle + \\triangle + \\triangle + \\triangle + \\triangle$.\n\nIn the same way, $5\\times\\frac{1}{4}$ means $\\frac{1}{4}+\\frac{1}{4}+\\frac{1}{4}+\\frac{1}{4}+\\frac{1}{4}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b020",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Worked example 6.6: Multiplying: whole number x fraction"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n\n$$\n5\\times\\frac{1}{4}\n$$",
    "answer_text": "Step 1: Write the multiplication as an addition.\n\n$$\n5\\times\\frac{1}{4}=\\frac{1}{4}+\\frac{1}{4}+\\frac{1}{4}+\\frac{1}{4}+\\frac{1}{4}\n$$\n\nStep 2: The denominator shows into how many parts one whole must be divided. Represent this in a diagram.\n\nIn this case, there must be 4 parts.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-001.png)\n\nStep 3: Shade the number of parts shown by the first numerator.\n\nThis is 1.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-035.png)\n\nStep 4: Shade the number of parts shown by the rest of the numerators.\n\nWe must shade another $1+1+1+1$ parts.\n\nThere are only 3 \"gaps\" in the shape that can be shaded. Therefore, we need to add another shape.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-020.png)\n\nStep 6: Write the total shaded part as a fraction.\n\nThe fraction is $\\frac{5}{4}$.\n\nRemember, the denominator shows into how many parts one whole is divided. The numerator shows the total number of those parts that we are dealing with.\n\nStep 7: Write the answer in its simplest form or as a mixed number.\n\n$$\n\\frac{5}{4}=1\\frac{1}{4}\n$$\n\nStep 8: Write out the whole calculation.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{1}{4}+\\frac{1}{4}+\\frac{1}{4}+\\frac{1}{4}+\\frac{1}{4}\\\\\n =\\frac{1+1+1+1+1}{4} \\\\\n =\\frac{5}{4} \\\\\n =1\\frac{1}{4}\n \\end{array}\n$$\n\nNote the numerator: $1+1+1+1+1=5\\times1$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b021",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Multiplication: fraction x whole number"
    },
    "content_text": "By now you know that $\\frac{2}{5}$ of a cake may be represented as follows:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web//ebw-jss1-06-021.png)\n\nSuppose Azubuike ate $\\frac{2}{5}$ of 3 cakes. How much cake did he actually eat? We must multiply $\\frac{2}{5}$ by 3 cakes: $\\frac{2}{5}\\times3$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b022",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Worked example 6.7: Multiplying: fraction x whole number"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n\n$$\n\\frac{2}{5}\\times3\n$$",
    "answer_text": "Step 1: Use a diagram to represent the fraction.\n\nThe fraction is $\\frac{2}{5}$.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web//ebw-jss1-06-021.png)\n\nStep 2: Add diagrams as required by the whole number.\n\nThe whole number is 3. This means we have $\\frac{2}{5}+\\frac{2}{5}+\\frac{2}{5}$.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-022.png)\n\nStep 3: Put all the shaded parts together into one shape as far as possible, and then start using the next shape you need.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-023.png)\n\nStep 4: Write the total shaded part as a fraction.\n\nThe fraction is $\\frac{6}{5}$.\n\nRemember, the denominator shows into how many parts one whole is divided. The numerator shows the total number of those parts that we are dealing with.\n\nStep 5: Write the answer in its simplest form or as a mixed number.\n\n$$\n\\frac{6}{5}=1\\frac{1}{5}\n$$\n\nStep 8: Write out the whole calculation.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{2}{5}+\\frac{2}{5}+\\frac{2}{5}\\\\\n =\\frac{2+2+2}{5} \\\\\n =\\frac{6}{5} \\\\\n =1\\frac{1}{5}\n \\end{array}\n$$\n\nNote the numerator: $2+2+2=3\\times2$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b023",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Exercise 6.4: Multiply fractions and whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.4: Multiply fractions and whole numbers\n\nCalculate each of the following.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b023-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Exercise 6.4: Multiply fractions and whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.4: Multiply fractions and whole numbers\n\nCalculate each of the following.\n\n1.\n$$\n4\\times\\frac{6}{9}\n$$",
    "answer_text": "$$\n\\begin{array}{l}\n\\phantom{00}4\\times\\frac{6}{9}\\newline\n=\\frac{6}{9}+\\frac{6}{9}+\\frac{6}{9}+\\frac{6}{9} \\newline\n=\\frac{6+6+6+6}{9} \\newline\n=\\frac{24}{9} \\newline\n=\\frac{8}{3}\\newline\n=2\\frac{2}{3}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b023-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Exercise 6.4: Multiply fractions and whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.4: Multiply fractions and whole numbers\n\nCalculate each of the following.\n\n2.\n$$\n6\\times\\frac{3}{10}\n$$",
    "answer_text": "$$\n\\begin{array}{l}\n\\phantom{00}6\\times\\frac{3}{10}\\newline\n=\\frac{3}{10}+\\frac{3}{10}+\\frac{3}{10}+\\frac{3}{10}+\\frac{3}{10}+\\frac{3}{10} \\newline\n=\\frac{3+3+3+3+3+3}{10} \\newline\n=\\frac{18}{10} \\newline\n=\\frac{9}{5}\\newline\n=1\\frac{4}{5}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b023-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Exercise 6.4: Multiply fractions and whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.4: Multiply fractions and whole numbers\n\nCalculate each of the following.\n\n3.\n$$\n\\frac{3}{8}\\times5\n$$",
    "answer_text": "$$\n\\begin{array}{l}\n\\phantom{00}\\frac{3}{8}\\times5\\newline\n=\\frac{3}{8}+\\frac{3}{8}+\\frac{3}{8}+\\frac{3}{8}+\\frac{3}{8} \\newline\n=\\frac{3+3+3+3+3}{8} \\newline\n=\\frac{15}{8} \\newline\n=1\\frac{7}{8}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b023-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Exercise 6.4: Multiply fractions and whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.4: Multiply fractions and whole numbers\n\nCalculate each of the following.\n\n4.\n$$\n\\frac{9}{14}\\times4\n$$",
    "answer_text": "$$\n\\begin{array}{l}\n\\phantom{00}\\frac{9}{14}\\times4\\newline\n=\\frac{9}{14}+\\frac{9}{14}+\\frac{9}{14}+\\frac{9}{14} \\newline\n=\\frac{9+9+9+9}{14} \\newline\n=\\frac{36}{14} \\newline\n=\\frac{18}{7}\\newline\n=2\\frac{4}{7}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b024",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Multiplication: fraction x whole number"
    },
    "content_text": "Once you understand how to multiply whole numbers and fractions, you may use this short method.\n\nExample: $\\frac{2}{7}\\times6$\n\nDenominator (stays the same): $\\frac{\\phantom{00}}{7}$\n\nNumerator: $2\\times6=12$\n\nCalculation:\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{2}{7}\\times6\\newline\n=\\frac{2\\times6}{7} \\newline\n=\\frac{12}{7}\\newline\n=1\\frac{5}{7}\n\\end{array}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b025",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Multiplication: fraction x fraction"
    },
    "content_text": "When we write $\\frac{2}{3}\\times\\frac{3}{4}$, it means two thirds, $\\frac{2}{3}$, of three quarters, $\\frac{3}{4}$.\n\nBy now you know that $\\frac{3}{4}$ of a cake may be represented as follows:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-024.png)\n\nNow we want to know how much $\\frac{2}{3}$ of the shaded part is.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b026",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Worked example 6.8: Multiplying using a diagram: fraction x fraction"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n\n$$\n\\frac{2}{3}\\times\\frac{3}{4}\n$$",
    "answer_text": "Step 1: Use a diagram to represent one of the fractions.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-024.png)\n\nStep 2: Divide the shape further, according to the denominator of the other fraction.\n\nThe denominator of $\\frac{2}{3}$ is 3. This means we must divide each part of the shape further into 3 parts.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-025.png)\n\nStep 3: Use another colour to shade the correct portion of the shaded part, according to the numerator of the fraction used in Step 2.\n\nThe numerator of $\\frac{2}{3}$ is 2. This means that we are interested in 2 of every 3 parts. Remember that we only want $\\frac{2}{3}$ of the part that is already shaded, $\\frac{3}{4}$.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-026.png)\n\nStep 4: Write the newly shaded part as a fraction of the whole shape.\n\nRemember, the shape is now divided into 12 parts. The new shading covers 6 of those parts.\n\nThe fraction is $\\frac{6}{12}$.\n\nStep 5: Write the answer in its simplest form or as a mixed number.\n\n$$\n\\frac{6}{12}=\\frac{1}{2}\n$$\n\nStep 6: Write out the whole calculation.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{2}{3}\\times\\frac{3}{4}\\newline\n =\\frac{6}{12} \\\\\n =\\frac{1}{2} \\\\\n \\end{array}\n$$\n\nExact array needle: \\begin{array}{l} \\phantom{00}\\frac{2}{3}\\times\\frac{3}{4} =\\frac{6}{12} \\\\ =\\frac{1}{2} \\\\ \\end{array}\n\nIf you use the same method to determine $\\frac{3}{4}\\times\\frac{2}{3}$, you will get the same answer.",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b027",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Multiplication: fraction x fraction"
    },
    "content_text": "See whether you notice a pattern when we write the first two lines of the calculation in Step 6 of the previous worked example as follows:\n\n$$\n\\frac{2}{3}\\times\\frac{3}{4}=\\frac{6}{12}\n$$\n\nWhen we multiply two fractions, we may follow this method:\n\n$$\n\\frac{\\text{numerator 1}}{\\text{denominator 1}}\\times\\frac{\\text{numerator 2}}{\\text{denominator 2}}=\\frac{\\text{numerator 1}\\times\\text{numerator 2}}{\\text{denominator 1}\\times\\text{denominator 2}}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b028",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Worked example 6.9: Calculating fraction x fraction directly"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n\n$$\n\\frac{5}{6}\\times\\frac{3}{8}\n$$",
    "answer_text": "Step 1: Multiply the two numerators and multiply the two denominators.\n\n$$\n\\frac{5}{6}\\times\\frac{3}{8}=\\frac{5\\times3}{6\\times8}\n$$\n\nStep 2: Find the numerator and denominator of the answer.\n\n$$\n\\frac{5}{6}\\times\\frac{3}{8}=\\frac{5\\times3}{6\\times8}=\\frac{15}{48}\n$$\n\nStep 3: Write the answer in its simplest form or as a mixed number.\n\n$$\n\\frac{5}{6}\\times\\frac{3}{8}=\\frac{5\\times3}{6\\times8}=\\frac{15}{48}=\\frac{5}{16}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b029",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Exercise 6.5: Multiply fractions with fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.5: Multiply fractions with fractions",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b029-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Exercise 6.5: Multiply fractions with fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.5: Multiply fractions with fractions\n\n1. Use a diagram to determine $\\frac{1}{2}\\times\\frac{2}{5}$.",
    "answer_text": "Show $\\frac{2}{5}$ with a diagram:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-027.png)\n\nLook at $\\frac{1}{2}$: The denominator 2 means each part must be further divided into 2:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-028.png)\n\nThe numerator 1 means that we want 1 out of every 2 parts of the shaded area:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-029.png)\n\nThe new shading represents $\\frac{2}{10}$.\n\n$$\n\\frac{1}{2}\\times\\frac{2}{5}=\\frac{2}{10}=\\frac{1}{5}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b029-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Exercise 6.5: Multiply fractions with fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.5: Multiply fractions with fractions\n\n2. Calculate each of the following directly.\n\na.\n$$\n\\frac{4}{9}\\times\\frac{3}{5}\n$$\n\nb.\n$$\n\\frac{6}{7}\\times\\frac{9}{10}\n$$\n\nc.\n$$\n\\frac{11}{12}\\times\\frac{4}{5}\n$$",
    "answer_text": "a.\n$$\n\\frac{4}{9}\\times\\frac{3}{5}=\\frac{4\\times3}{9\\times5}=\\frac{12}{45}=\\frac{4}{15}\n$$\n\nb.\n$$\n\\frac{6}{7}\\times\\frac{9}{10}=\\frac{6\\times9}{7\\times10}=\\frac{54}{70}=\\frac{27}{35}\n$$\n\nc.\n$$\n\\frac{11}{12}\\times\\frac{4}{5}=\\frac{11\\times4}{12\\times5}=\\frac{44}{60}=\\frac{11}{15}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
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
    "record_id": "ch06-b052-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Exercise 6.9: Multiply and divide mixed numbers"
    },
    "content_text": "Source math retained:\n5 rac{1}{3}= rac{(3 imes5)+1}{3}= rac{16}{3}\n2 rac{3}{4}= rac{(4 imes2)+3}{4}= rac{11}{4}\nrac{16}{3} imes rac{11}{4}= rac{16 imes11}{3 imes4}\nrac{(16\\div4) imes11}{(4\\div4) imes3}= rac{4 imes11}{1 imes3}= rac{44}{3}=14 rac{2}{3}",
    "prompt_text": "### Exercise 6.9: Multiply and divide mixed numbers\n\n1. $5\\frac{1}{3}\\times2\\frac{3}{4}$",
    "answer_text": "$$5\\frac{1}{3}=\\frac{(3\\times5)+1}{3}=\\frac{16}{3}$$\n$$2\\frac{3}{4}=\\frac{(4\\times2)+3}{4}=\\frac{11}{4}$$\n$$\\frac{16}{3} \\times \\frac{11}{4}= \\frac{16\\times11}{3\\times4}$$\nThe HCF of 16 and 4 is 4.\n$$\\frac{(16\\div4)\\times11}{(4\\div4)\\times3}=\\frac{4\\times11}{1\\times3}=\\frac{44}{3}=14\\frac{2}{3}$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b052-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Exercise 6.9: Multiply and divide mixed numbers"
    },
    "content_text": "Source math retained:\n3 rac{3}{5}= rac{(5 imes3)+3}{5}= rac{18}{5}\n1 rac{6}{9}= rac{(9 imes1)+6}{9}= rac{15}{9}\nrac{18}{5} imes rac{15}{9}= rac{18 imes15}{5 imes9}\nrac{(18\\div9) imes(15\\div5)}{(9\\div9) imes(5\\div5)}= rac{2 imes3}{1 imes1}= rac{6}{1}=6",
    "prompt_text": "### Exercise 6.9: Multiply and divide mixed numbers\n\n2. $3\\frac{3}{5}\\times1\\frac{6}{9}$",
    "answer_text": "$$3\\frac{3}{5}=\\frac{(5\\times3)+3}{5}=\\frac{18}{5}$$\n$$1\\frac{6}{9}=\\frac{(9\\times1)+6}{9}=\\frac{15}{9}$$\n$$\\frac{18}{5} \\times \\frac{15}{9}= \\frac{18\\times15}{5\\times9}$$\nThe HCF of 18 and 9 is 9.\nThe HCF of 15 and 5 is 5.\n$$\\frac{(18\\div9)\\times(15\\div5)}{(9\\div9)\\times(5\\div5)}=\\frac{2\\times3}{1\\times1}=\\frac{6}{1}=6$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b054-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.3 Practical applications",
      "h3": "Exercise 6.10: Use operations with fractions to solve problems"
    },
    "content_text": "Source math retained:\n\\frac{5}{8}\n\\begin{array}{l}\\phantom{00}\\frac{5}{8}\\times3 \\\\ =\\frac{5\\times3}{8} \\\\ =\\frac{15}{8} \\\\ =1\\frac{7}{8} \\text{hours} \\\\\\end{array}\n1\\frac{7}{8}",
    "prompt_text": "### Exercise 6.10: Use operations with fractions to solve problems\n\n2. It takes Adanna $\\frac{5}{8}$ of an hour to walk to school. How long will it take her to walk to school, back home and back to school again?",
    "answer_text": "$$\\begin{array}{l}\\phantom{00}\\frac{5}{8}\\times3 \\\\newline =\\frac{5\\times3}{8} \\\\newline =\\frac{15}{8} \\\\newline =1\\frac{7}{8}\\space\\text{hours} \\\\newline\\end{array}$$\nIt will take Adanna $1\\frac{7}{8}$ hours.",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-word-problems-involving-multiplication-and-division-of-fractions"
  },
  {
    "record_id": "ch06-b054-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.3 Practical applications",
      "h3": "Exercise 6.10: Use operations with fractions to solve problems"
    },
    "content_text": "Source math retained:\n\\frac{5}{8}\n\\frac{9}{10}\n\\frac{9}{10}\\times\\frac{5}{8}=\\frac{9\\times5}{10\\times8}=\\frac{45}{80}=\\frac{9}{16}\n\\frac{9}{16}",
    "prompt_text": "### Exercise 6.10: Use operations with fractions to solve problems\n\n3. In a certain class, $\\frac{5}{8}$ of the class are girls and $\\frac{9}{10}$ of the girls take Mathematics. Calculate the fraction of the class that are girls and take Mathematics.",
    "answer_text": "$$\\frac{9}{10}\\times\\frac{5}{8}=\\frac{9\\times5}{10\\times8}=\\frac{45}{80}=\\frac{9}{16}$$\n$\\frac{9}{16}$ of the class are girls and take Mathematics.",
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
  "subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions",
  "subtopic_title": "Multiplication of fractions",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions-po01",
        "source_performance_objective_index": 1,
        "text": "Solve problems on multiplication of fractions"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "multiplication-of-fractions-ao-solve-problems",
          "text": "Solve problems on multiplication of fractions."
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
    "record_id": "ch06-b019",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Multiplication: whole number x fraction"
    },
    "content_text": "You might remember from previous years that multiplication is a form of addition. For example, $5 \\times \\triangle$ means $\\triangle + \\triangle + \\triangle + \\triangle + \\triangle$.\n\nIn the same way, $5\\times\\frac{1}{4}$ means $\\frac{1}{4}+\\frac{1}{4}+\\frac{1}{4}+\\frac{1}{4}+\\frac{1}{4}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b020",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Worked example 6.6: Multiplying: whole number x fraction"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n\n$$\n5\\times\\frac{1}{4}\n$$",
    "answer_text": "Step 1: Write the multiplication as an addition.\n\n$$\n5\\times\\frac{1}{4}=\\frac{1}{4}+\\frac{1}{4}+\\frac{1}{4}+\\frac{1}{4}+\\frac{1}{4}\n$$\n\nStep 2: The denominator shows into how many parts one whole must be divided. Represent this in a diagram.\n\nIn this case, there must be 4 parts.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-001.png)\n\nStep 3: Shade the number of parts shown by the first numerator.\n\nThis is 1.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-035.png)\n\nStep 4: Shade the number of parts shown by the rest of the numerators.\n\nWe must shade another $1+1+1+1$ parts.\n\nThere are only 3 \"gaps\" in the shape that can be shaded. Therefore, we need to add another shape.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-020.png)\n\nStep 6: Write the total shaded part as a fraction.\n\nThe fraction is $\\frac{5}{4}$.\n\nRemember, the denominator shows into how many parts one whole is divided. The numerator shows the total number of those parts that we are dealing with.\n\nStep 7: Write the answer in its simplest form or as a mixed number.\n\n$$\n\\frac{5}{4}=1\\frac{1}{4}\n$$\n\nStep 8: Write out the whole calculation.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{1}{4}+\\frac{1}{4}+\\frac{1}{4}+\\frac{1}{4}+\\frac{1}{4}\\\\\n =\\frac{1+1+1+1+1}{4} \\\\\n =\\frac{5}{4} \\\\\n =1\\frac{1}{4}\n \\end{array}\n$$\n\nNote the numerator: $1+1+1+1+1=5\\times1$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b021",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Multiplication: fraction x whole number"
    },
    "content_text": "By now you know that $\\frac{2}{5}$ of a cake may be represented as follows:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web//ebw-jss1-06-021.png)\n\nSuppose Azubuike ate $\\frac{2}{5}$ of 3 cakes. How much cake did he actually eat? We must multiply $\\frac{2}{5}$ by 3 cakes: $\\frac{2}{5}\\times3$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b022",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Worked example 6.7: Multiplying: fraction x whole number"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n\n$$\n\\frac{2}{5}\\times3\n$$",
    "answer_text": "Step 1: Use a diagram to represent the fraction.\n\nThe fraction is $\\frac{2}{5}$.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web//ebw-jss1-06-021.png)\n\nStep 2: Add diagrams as required by the whole number.\n\nThe whole number is 3. This means we have $\\frac{2}{5}+\\frac{2}{5}+\\frac{2}{5}$.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-022.png)\n\nStep 3: Put all the shaded parts together into one shape as far as possible, and then start using the next shape you need.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-023.png)\n\nStep 4: Write the total shaded part as a fraction.\n\nThe fraction is $\\frac{6}{5}$.\n\nRemember, the denominator shows into how many parts one whole is divided. The numerator shows the total number of those parts that we are dealing with.\n\nStep 5: Write the answer in its simplest form or as a mixed number.\n\n$$\n\\frac{6}{5}=1\\frac{1}{5}\n$$\n\nStep 8: Write out the whole calculation.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{2}{5}+\\frac{2}{5}+\\frac{2}{5}\\\\\n =\\frac{2+2+2}{5} \\\\\n =\\frac{6}{5} \\\\\n =1\\frac{1}{5}\n \\end{array}\n$$\n\nNote the numerator: $2+2+2=3\\times2$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b023",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Exercise 6.4: Multiply fractions and whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.4: Multiply fractions and whole numbers\n\nCalculate each of the following.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b023-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Exercise 6.4: Multiply fractions and whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.4: Multiply fractions and whole numbers\n\nCalculate each of the following.\n\n1.\n$$\n4\\times\\frac{6}{9}\n$$",
    "answer_text": "$$\n\\begin{array}{l}\n\\phantom{00}4\\times\\frac{6}{9}\\newline\n=\\frac{6}{9}+\\frac{6}{9}+\\frac{6}{9}+\\frac{6}{9} \\newline\n=\\frac{6+6+6+6}{9} \\newline\n=\\frac{24}{9} \\newline\n=\\frac{8}{3}\\newline\n=2\\frac{2}{3}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b023-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Exercise 6.4: Multiply fractions and whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.4: Multiply fractions and whole numbers\n\nCalculate each of the following.\n\n2.\n$$\n6\\times\\frac{3}{10}\n$$",
    "answer_text": "$$\n\\begin{array}{l}\n\\phantom{00}6\\times\\frac{3}{10}\\newline\n=\\frac{3}{10}+\\frac{3}{10}+\\frac{3}{10}+\\frac{3}{10}+\\frac{3}{10}+\\frac{3}{10} \\newline\n=\\frac{3+3+3+3+3+3}{10} \\newline\n=\\frac{18}{10} \\newline\n=\\frac{9}{5}\\newline\n=1\\frac{4}{5}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b023-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Exercise 6.4: Multiply fractions and whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.4: Multiply fractions and whole numbers\n\nCalculate each of the following.\n\n3.\n$$\n\\frac{3}{8}\\times5\n$$",
    "answer_text": "$$\n\\begin{array}{l}\n\\phantom{00}\\frac{3}{8}\\times5\\newline\n=\\frac{3}{8}+\\frac{3}{8}+\\frac{3}{8}+\\frac{3}{8}+\\frac{3}{8} \\newline\n=\\frac{3+3+3+3+3}{8} \\newline\n=\\frac{15}{8} \\newline\n=1\\frac{7}{8}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b023-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Exercise 6.4: Multiply fractions and whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.4: Multiply fractions and whole numbers\n\nCalculate each of the following.\n\n4.\n$$\n\\frac{9}{14}\\times4\n$$",
    "answer_text": "$$\n\\begin{array}{l}\n\\phantom{00}\\frac{9}{14}\\times4\\newline\n=\\frac{9}{14}+\\frac{9}{14}+\\frac{9}{14}+\\frac{9}{14} \\newline\n=\\frac{9+9+9+9}{14} \\newline\n=\\frac{36}{14} \\newline\n=\\frac{18}{7}\\newline\n=2\\frac{4}{7}\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b024",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Multiplication: fraction x whole number"
    },
    "content_text": "Once you understand how to multiply whole numbers and fractions, you may use this short method.\n\nExample: $\\frac{2}{7}\\times6$\n\nDenominator (stays the same): $\\frac{\\phantom{00}}{7}$\n\nNumerator: $2\\times6=12$\n\nCalculation:\n\n$$\n\\begin{array}{l}\n\\phantom{00}\\frac{2}{7}\\times6\\newline\n=\\frac{2\\times6}{7} \\newline\n=\\frac{12}{7}\\newline\n=1\\frac{5}{7}\n\\end{array}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b025",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Multiplication: fraction x fraction"
    },
    "content_text": "When we write $\\frac{2}{3}\\times\\frac{3}{4}$, it means two thirds, $\\frac{2}{3}$, of three quarters, $\\frac{3}{4}$.\n\nBy now you know that $\\frac{3}{4}$ of a cake may be represented as follows:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-024.png)\n\nNow we want to know how much $\\frac{2}{3}$ of the shaded part is.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b026",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Worked example 6.8: Multiplying using a diagram: fraction x fraction"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n\n$$\n\\frac{2}{3}\\times\\frac{3}{4}\n$$",
    "answer_text": "Step 1: Use a diagram to represent one of the fractions.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-024.png)\n\nStep 2: Divide the shape further, according to the denominator of the other fraction.\n\nThe denominator of $\\frac{2}{3}$ is 3. This means we must divide each part of the shape further into 3 parts.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-025.png)\n\nStep 3: Use another colour to shade the correct portion of the shaded part, according to the numerator of the fraction used in Step 2.\n\nThe numerator of $\\frac{2}{3}$ is 2. This means that we are interested in 2 of every 3 parts. Remember that we only want $\\frac{2}{3}$ of the part that is already shaded, $\\frac{3}{4}$.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-026.png)\n\nStep 4: Write the newly shaded part as a fraction of the whole shape.\n\nRemember, the shape is now divided into 12 parts. The new shading covers 6 of those parts.\n\nThe fraction is $\\frac{6}{12}$.\n\nStep 5: Write the answer in its simplest form or as a mixed number.\n\n$$\n\\frac{6}{12}=\\frac{1}{2}\n$$\n\nStep 6: Write out the whole calculation.\n\n$$\n\\begin{array}{l}\n \\phantom{00}\\frac{2}{3}\\times\\frac{3}{4}\\newline\n =\\frac{6}{12} \\\\\n =\\frac{1}{2} \\\\\n \\end{array}\n$$\n\nExact array needle: \\begin{array}{l} \\phantom{00}\\frac{2}{3}\\times\\frac{3}{4} =\\frac{6}{12} \\\\ =\\frac{1}{2} \\\\ \\end{array}\n\nIf you use the same method to determine $\\frac{3}{4}\\times\\frac{2}{3}$, you will get the same answer.",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b027",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Multiplication: fraction x fraction"
    },
    "content_text": "See whether you notice a pattern when we write the first two lines of the calculation in Step 6 of the previous worked example as follows:\n\n$$\n\\frac{2}{3}\\times\\frac{3}{4}=\\frac{6}{12}\n$$\n\nWhen we multiply two fractions, we may follow this method:\n\n$$\n\\frac{\\text{numerator 1}}{\\text{denominator 1}}\\times\\frac{\\text{numerator 2}}{\\text{denominator 2}}=\\frac{\\text{numerator 1}\\times\\text{numerator 2}}{\\text{denominator 1}\\times\\text{denominator 2}}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b028",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Worked example 6.9: Calculating fraction x fraction directly"
    },
    "content_text": "",
    "prompt_text": "Calculate:\n\n$$\n\\frac{5}{6}\\times\\frac{3}{8}\n$$",
    "answer_text": "Step 1: Multiply the two numerators and multiply the two denominators.\n\n$$\n\\frac{5}{6}\\times\\frac{3}{8}=\\frac{5\\times3}{6\\times8}\n$$\n\nStep 2: Find the numerator and denominator of the answer.\n\n$$\n\\frac{5}{6}\\times\\frac{3}{8}=\\frac{5\\times3}{6\\times8}=\\frac{15}{48}\n$$\n\nStep 3: Write the answer in its simplest form or as a mixed number.\n\n$$\n\\frac{5}{6}\\times\\frac{3}{8}=\\frac{5\\times3}{6\\times8}=\\frac{15}{48}=\\frac{5}{16}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b029",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Exercise 6.5: Multiply fractions with fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.5: Multiply fractions with fractions",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b029-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Exercise 6.5: Multiply fractions with fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.5: Multiply fractions with fractions\n\n1. Use a diagram to determine $\\frac{1}{2}\\times\\frac{2}{5}$.",
    "answer_text": "Show $\\frac{2}{5}$ with a diagram:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-027.png)\n\nLook at $\\frac{1}{2}$: The denominator 2 means each part must be further divided into 2:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-028.png)\n\nThe numerator 1 means that we want 1 out of every 2 parts of the shaded area:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-029.png)\n\nThe new shading represents $\\frac{2}{10}$.\n\n$$\n\\frac{1}{2}\\times\\frac{2}{5}=\\frac{2}{10}=\\frac{1}{5}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b029-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.4 Multiplying fractions and whole numbers",
      "h3": "Exercise 6.5: Multiply fractions with fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.5: Multiply fractions with fractions\n\n2. Calculate each of the following directly.\n\na.\n$$\n\\frac{4}{9}\\times\\frac{3}{5}\n$$\n\nb.\n$$\n\\frac{6}{7}\\times\\frac{9}{10}\n$$\n\nc.\n$$\n\\frac{11}{12}\\times\\frac{4}{5}\n$$",
    "answer_text": "a.\n$$\n\\frac{4}{9}\\times\\frac{3}{5}=\\frac{4\\times3}{9\\times5}=\\frac{12}{45}=\\frac{4}{15}\n$$\n\nb.\n$$\n\\frac{6}{7}\\times\\frac{9}{10}=\\frac{6\\times9}{7\\times10}=\\frac{54}{70}=\\frac{27}{35}\n$$\n\nc.\n$$\n\\frac{11}{12}\\times\\frac{4}{5}=\\frac{11\\times4}{12\\times5}=\\frac{44}{60}=\\frac{11}{15}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
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
    "record_id": "ch06-b052-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Exercise 6.9: Multiply and divide mixed numbers"
    },
    "content_text": "Source math retained:\n5 rac{1}{3}= rac{(3 imes5)+1}{3}= rac{16}{3}\n2 rac{3}{4}= rac{(4 imes2)+3}{4}= rac{11}{4}\nrac{16}{3} imes rac{11}{4}= rac{16 imes11}{3 imes4}\nrac{(16\\div4) imes11}{(4\\div4) imes3}= rac{4 imes11}{1 imes3}= rac{44}{3}=14 rac{2}{3}",
    "prompt_text": "### Exercise 6.9: Multiply and divide mixed numbers\n\n1. $5\\frac{1}{3}\\times2\\frac{3}{4}$",
    "answer_text": "$$5\\frac{1}{3}=\\frac{(3\\times5)+1}{3}=\\frac{16}{3}$$\n$$2\\frac{3}{4}=\\frac{(4\\times2)+3}{4}=\\frac{11}{4}$$\n$$\\frac{16}{3} \\times \\frac{11}{4}= \\frac{16\\times11}{3\\times4}$$\nThe HCF of 16 and 4 is 4.\n$$\\frac{(16\\div4)\\times11}{(4\\div4)\\times3}=\\frac{4\\times11}{1\\times3}=\\frac{44}{3}=14\\frac{2}{3}$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b052-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.2 Multiplication and division of fractions",
      "h3": "Exercise 6.9: Multiply and divide mixed numbers"
    },
    "content_text": "Source math retained:\n3 rac{3}{5}= rac{(5 imes3)+3}{5}= rac{18}{5}\n1 rac{6}{9}= rac{(9 imes1)+6}{9}= rac{15}{9}\nrac{18}{5} imes rac{15}{9}= rac{18 imes15}{5 imes9}\nrac{(18\\div9) imes(15\\div5)}{(9\\div9) imes(5\\div5)}= rac{2 imes3}{1 imes1}= rac{6}{1}=6",
    "prompt_text": "### Exercise 6.9: Multiply and divide mixed numbers\n\n2. $3\\frac{3}{5}\\times1\\frac{6}{9}$",
    "answer_text": "$$3\\frac{3}{5}=\\frac{(5\\times3)+3}{5}=\\frac{18}{5}$$\n$$1\\frac{6}{9}=\\frac{(9\\times1)+6}{9}=\\frac{15}{9}$$\n$$\\frac{18}{5} \\times \\frac{15}{9}= \\frac{18\\times15}{5\\times9}$$\nThe HCF of 18 and 9 is 9.\nThe HCF of 15 and 5 is 5.\n$$\\frac{(18\\div9)\\times(15\\div5)}{(9\\div9)\\times(5\\div5)}=\\frac{2\\times3}{1\\times1}=\\frac{6}{1}=6$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions"
  },
  {
    "record_id": "ch06-b054-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.3 Practical applications",
      "h3": "Exercise 6.10: Use operations with fractions to solve problems"
    },
    "content_text": "Source math retained:\n\\frac{5}{8}\n\\begin{array}{l}\\phantom{00}\\frac{5}{8}\\times3 \\\\ =\\frac{5\\times3}{8} \\\\ =\\frac{15}{8} \\\\ =1\\frac{7}{8} \\text{hours} \\\\\\end{array}\n1\\frac{7}{8}",
    "prompt_text": "### Exercise 6.10: Use operations with fractions to solve problems\n\n2. It takes Adanna $\\frac{5}{8}$ of an hour to walk to school. How long will it take her to walk to school, back home and back to school again?",
    "answer_text": "$$\\begin{array}{l}\\phantom{00}\\frac{5}{8}\\times3 \\\\newline =\\frac{5\\times3}{8} \\\\newline =\\frac{15}{8} \\\\newline =1\\frac{7}{8}\\space\\text{hours} \\\\newline\\end{array}$$\nIt will take Adanna $1\\frac{7}{8}$ hours.",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-word-problems-involving-multiplication-and-division-of-fractions"
  },
  {
    "record_id": "ch06-b054-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.3 Practical applications",
      "h3": "Exercise 6.10: Use operations with fractions to solve problems"
    },
    "content_text": "Source math retained:\n\\frac{5}{8}\n\\frac{9}{10}\n\\frac{9}{10}\\times\\frac{5}{8}=\\frac{9\\times5}{10\\times8}=\\frac{45}{80}=\\frac{9}{16}\n\\frac{9}{16}",
    "prompt_text": "### Exercise 6.10: Use operations with fractions to solve problems\n\n3. In a certain class, $\\frac{5}{8}$ of the class are girls and $\\frac{9}{10}$ of the girls take Mathematics. Calculate the fraction of the class that are girls and take Mathematics.",
    "answer_text": "$$\\frac{9}{10}\\times\\frac{5}{8}=\\frac{9\\times5}{10\\times8}=\\frac{45}{80}=\\frac{9}{16}$$\n$\\frac{9}{16}$ of the class are girls and take Mathematics.",
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
