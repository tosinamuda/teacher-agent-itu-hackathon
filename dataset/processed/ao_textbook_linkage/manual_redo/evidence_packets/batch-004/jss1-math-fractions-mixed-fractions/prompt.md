# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-1",
  "topic_key": "jss1-math-fractions",
  "topic": "Fractions",
  "subtopic_id": "jss1-math-fractions-mixed-fractions",
  "subtopic_title": "Mixed fractions",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-fractions-mixed-fractions-po01",
        "source_performance_objective_index": 1,
        "text": "Convert improper fractions to mixed fractions and vice versa"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "mixed-fractions-ao-convert-improper-to-mixed",
          "text": "Convert improper fractions to mixed fractions."
        },
        {
          "atomic_objective_id": "mixed-fractions-ao-convert-mixed-to-improper",
          "text": "Convert mixed fractions to improper fractions."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch04-b006",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.1 Types of fractions",
      "h3": "4.1 Types of fractions"
    },
    "content_text": "A **mixed number** is made up of a whole number and a proper fraction. For example, $2\\frac{1}{2}$ apples mean you have two whole apples and one half of another apple.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-012.png)",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-mixed-fractions"
  },
  {
    "record_id": "ch04-b007",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.1 Types of fractions",
      "h3": "4.1 Types of fractions"
    },
    "content_text": "**mixed number** A mixed number is a number that is made up of a whole number and a proper fraction.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-mixed-fractions"
  },
  {
    "record_id": "ch04-b008",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.1 Types of fractions",
      "h3": "4.1 Types of fractions"
    },
    "content_text": "A mixed number may be expressed as an **improper fraction**. An improper fraction is larger than 1. Its numerator is larger than its denominator. Suppose we cut the two whole apples shown above into halves as well. We will then have five halves.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-013.png)\n\nThese five halves may be written as $\\frac{5}{2}$. The denominator tells us that there are 2 parts in one whole apple, so we are dealing with halves. The numerator tells us that we have 5 halves. Therefore, the mixed number $2\\frac{1}{2}$ may be expressed as the improper fraction $\\frac{5}{2}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-mixed-fractions"
  },
  {
    "record_id": "ch04-b009",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.1 Types of fractions",
      "h3": "4.1 Types of fractions"
    },
    "content_text": "**improper fraction** An improper fraction is a fraction that is larger than 1, so the numerator is larger than the denominator.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-types-of-fractions"
  },
  {
    "record_id": "ch04-b010",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Worked example 4.1: Expressing mixed numbers as improper fractions"
    },
    "content_text": "",
    "prompt_text": "Write $5\\frac{3}{4}$ as an improper fraction.",
    "answer_text": "Step 1: Use the denominator to see how many parts there are in one whole.\n\n            The denominator of the proper fraction in this mixed number is 4.\n            This means that each whole is divided into 4 parts. We are dealing with quarters.\n\n            Step 2: Determine how may parts the whole number represents. Multiply the whole number by the denominator from Step 1.\n\n            The whole number in this mixed number is 5.\n            If there are 4 parts in one whole, there must be $5\\times4=20$ parts in five wholes.\n\n            Step 3: Add the additional parts that are given by the numerator of the proper fraction.\n\n            The numerator of the proper fraction is 3.\n            So, as well as the 20 parts given by the whole number, we have another 3 parts.\n            The total parts are $20+3=23$.\n\n            Step 4: Write the improper fraction in the form $\\frac{\\text{numerator}}{\\text{denominator}}$.\n\n            The numerator gives the total parts we have: 23\n            The denominator tells us how many parts there are in one whole: 4\n\n            $$\n\\therefore 5\\frac{3}{4}=\\frac{23}{4}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-mixed-fractions"
  },
  {
    "record_id": "ch04-b011",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Worked example 4.2: Expressing improper fractions as mixed numbers"
    },
    "content_text": "",
    "prompt_text": "Write $\\frac{26}{3}$ as a mixed number.",
    "answer_text": "Step 1: Use the denominator to see how many parts there are in one whole.\n\n            The denominator of this improper fraction is 3.\n            This means that each whole is divided into 3 parts. We are dealing with thirds.\n\n            Step 2: Determine how many whole numbers can be formed from the total parts we have. To do this, divide the numerator by the denominator from Step 1.\n\n            The numerator gives the total parts we have: 26\n            If there are 3 parts in one whole, we can form 8 wholes from 26 parts: $8\\times3=24$\n\n            $$\n            \\require{enclose}\n            \\begin{array}{r}\n            8\\\\\n            3\\enclose{longdiv}{26}\\\\\n            \\underline{-24} \\newline\n            2\n            \\end{array}\n            $$\n\n            The whole number part of the mixed number is: 8\n\n            Step 3: Determine what fraction is left over after we formed the whole numbers.\n\n            You know that the denominator, which tells us how many parts there are in one whole, is 3.\n            To work out the numerator, use the parts that are left over after we formed the whole numbers. If you look at the long division, the remainder is 2.\n\n            After we formed the whole numbers, the fraction $\\frac{2}{3}$ is left over.\n\n            Step 4: Write down the mixed number as a whole number followed by a proper fraction.\n\n            $$\n\\therefore \\frac{26}{3}=8\\frac{2}{3}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-mixed-fractions"
  },
  {
    "record_id": "ch04-b012",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.2: Convert between mixed numbers and improper fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.2: Convert between mixed numbers and improper fractions",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-mixed-fractions"
  },
  {
    "record_id": "ch04-b012-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.2: Convert between mixed numbers and improper fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.2: Convert between mixed numbers and improper fractions\n\n1. Express the following mixed numbers as improper fractions.\n\n   1. $6\\frac{3}{7}$\n   2. $2\\frac{5}{11}$\n   3. $13\\frac{2}{3}$",
    "answer_text": "1. $6\\frac{3}{7}$\n\n            Parts in one whole: 7\n            Parts in 6 wholes: $6\\times7=42$\n            Total parts: $42+3=45$\n\n            $$\n\\therefore 6\\frac{3}{7}=\\frac{45}{7}\n$$\n\n            2. $2\\frac{5}{11}$\n\n            Parts in one whole: 11\n            Parts in 2 wholes: $2\\times11=22$\n            Total parts: $22+5=27$\n\n            $$\n\\therefore 2\\frac{5}{11}=\\frac{27}{11}\n$$\n\n            3. $13\\frac{2}{3}$\n\n            Parts in one whole: 3\n            Parts in 13 wholes: $13\\times3=39$\n            Total parts: $39+2=41$\n\n            $$\n\\therefore 13\\frac{2}{3}=\\frac{41}{3}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-mixed-fractions"
  },
  {
    "record_id": "ch04-b012-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.2: Convert between mixed numbers and improper fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.2: Convert between mixed numbers and improper fractions\n\n2. Express the following improper fractions as mixed numbers.\n\n   1. $\\frac{30}{7}$\n   2. $\\frac{112}{9}$\n   3. $\\frac{85}{11}$",
    "answer_text": "1. $\\frac{30}{7}$\n\n            Parts in one whole: 7\n            Total parts: 30\n\n            $$\n\\require{enclose}\n\\begin{array}{r}\n     4\\newline\n7 \\enclose{longdiv}{30}\\newline\n\\underline{-28} \\newline\n2\n\\end{array}\n$$\n\n            Whole number: 4\n            Fraction: $\\frac{2}{7}$\n\n            $$\n\\therefore \\frac{30}{7}=4\\frac{2}{7}\n$$\n\n            2. $\\frac{112}{9}$\n\n            Parts in one whole: 9\n            Total parts: 112\n\n            $$\n\\require{enclose}\n\\begin{array}{r}\n12\\newline\n9 \\enclose{longdiv}{112}\\newline\n\\underline{-9}\\phantom{0} \\newline\n22 \\newline\n\\underline{-18} \\newline\n4\n\\end{array}\n$$\n\n            Whole number: 12\n            Fraction: $\\frac{4}{9}$\n\n            $$\n\\therefore \\frac{112}{9}=12\\frac{4}{9}\n$$\n\n            3. $\\frac{85}{11}$\n\n            Parts in one whole: 11\n            Total parts: 85\n\n            $$\n\\require{enclose}\n\\begin{array}{r}\n7\\newline\n11 \\enclose{longdiv}{85}\\newline\n\\underline{-77} \\newline\n8 \\newline\n\\end{array}\n$$\n\n            Whole number: 7\n            Fraction: $\\frac{8}{11}$\n\n            $$\n\\therefore \\frac{85}{11}=7\\frac{8}{11}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-mixed-fractions"
  },
  {
    "record_id": "ch04-b013",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.1 Types of fractions",
      "h3": null
    },
    "content_text": "Once you understand how to express a mixed number as an improper fraction, you may use this short method. Example: 3\\frac{3}{5}. Denominator: \\frac{\\phantom{00}}{5}. Numerator: (5\\times3)+3=18. Answer: \\frac{18}{5}.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-mixed-fractions"
  },
  {
    "record_id": "ch04-b057-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": "Exercise 4.12: Use equivalent fractions to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.12: Use equivalent fractions to solve problems\n\n2. After a birthday party, $2\\frac{2}{5}$ cakes are left over. If the leftover cake is cut into equal pieces, how many people could get one piece each?",
    "answer_text": "Parts in one whole: 5\nParts in 2 cakes: $2\\times5=10$\nAdditional pieces: 2\nTotal pieces available: $10+2=12$",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
  },
  {
    "record_id": "ch04-b058",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.7 Summary",
      "h3": null
    },
    "content_text": "- A common fraction is written as $\\frac{\\text{numerator}}{\\text{denominator}}$.\n- A proper fraction is smaller than 1, for example $\\frac{2}{7}$.\n- A mixed number consists of a whole number and a proper fraction, for example $5\\frac{1}{6}$.\n- An improper fraction is larger than 1, for example $\\frac{9}{4}$.\n- Equivalent fractions have different numerators and denominators but the same value, for example $\\frac{1}{2}=\\frac{2}{4}=\\frac{4}{8}$.\n- A fraction is in its simplest form when the numerator and denominator have no common factor.\n- To compare fractions, we must express them with the same denominators. The lowest common denominator is the smallest whole number into which all the denominators can divide without a remainder.\n- A decimal fraction is written in decimal notation, where the numerator is written after a decimal point and the denominator is a power of ten.\n- In decimal notation, the decimal point separates whole numbers from fractions.\n- If there are three digits after the decimal point, the denominator is $10\\times10\\times10=1,000$.\n- A percentage is a fraction with denominator 100, written with only the numerator followed by a percentage symbol.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
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
  "theme_key": "jss1-theme-1",
  "topic_key": "jss1-math-fractions",
  "topic": "Fractions",
  "subtopic_id": "jss1-math-fractions-mixed-fractions",
  "subtopic_title": "Mixed fractions",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-fractions-mixed-fractions-po01",
        "source_performance_objective_index": 1,
        "text": "Convert improper fractions to mixed fractions and vice versa"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "mixed-fractions-ao-convert-improper-to-mixed",
          "text": "Convert improper fractions to mixed fractions."
        },
        {
          "atomic_objective_id": "mixed-fractions-ao-convert-mixed-to-improper",
          "text": "Convert mixed fractions to improper fractions."
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
    "record_id": "ch04-b006",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.1 Types of fractions",
      "h3": "4.1 Types of fractions"
    },
    "content_text": "A **mixed number** is made up of a whole number and a proper fraction. For example, $2\\frac{1}{2}$ apples mean you have two whole apples and one half of another apple.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-012.png)",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-mixed-fractions"
  },
  {
    "record_id": "ch04-b007",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.1 Types of fractions",
      "h3": "4.1 Types of fractions"
    },
    "content_text": "**mixed number** A mixed number is a number that is made up of a whole number and a proper fraction.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-mixed-fractions"
  },
  {
    "record_id": "ch04-b008",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.1 Types of fractions",
      "h3": "4.1 Types of fractions"
    },
    "content_text": "A mixed number may be expressed as an **improper fraction**. An improper fraction is larger than 1. Its numerator is larger than its denominator. Suppose we cut the two whole apples shown above into halves as well. We will then have five halves.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-013.png)\n\nThese five halves may be written as $\\frac{5}{2}$. The denominator tells us that there are 2 parts in one whole apple, so we are dealing with halves. The numerator tells us that we have 5 halves. Therefore, the mixed number $2\\frac{1}{2}$ may be expressed as the improper fraction $\\frac{5}{2}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-mixed-fractions"
  },
  {
    "record_id": "ch04-b009",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.1 Types of fractions",
      "h3": "4.1 Types of fractions"
    },
    "content_text": "**improper fraction** An improper fraction is a fraction that is larger than 1, so the numerator is larger than the denominator.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-types-of-fractions"
  },
  {
    "record_id": "ch04-b010",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Worked example 4.1: Expressing mixed numbers as improper fractions"
    },
    "content_text": "",
    "prompt_text": "Write $5\\frac{3}{4}$ as an improper fraction.",
    "answer_text": "Step 1: Use the denominator to see how many parts there are in one whole.\n\n            The denominator of the proper fraction in this mixed number is 4.\n            This means that each whole is divided into 4 parts. We are dealing with quarters.\n\n            Step 2: Determine how may parts the whole number represents. Multiply the whole number by the denominator from Step 1.\n\n            The whole number in this mixed number is 5.\n            If there are 4 parts in one whole, there must be $5\\times4=20$ parts in five wholes.\n\n            Step 3: Add the additional parts that are given by the numerator of the proper fraction.\n\n            The numerator of the proper fraction is 3.\n            So, as well as the 20 parts given by the whole number, we have another 3 parts.\n            The total parts are $20+3=23$.\n\n            Step 4: Write the improper fraction in the form $\\frac{\\text{numerator}}{\\text{denominator}}$.\n\n            The numerator gives the total parts we have: 23\n            The denominator tells us how many parts there are in one whole: 4\n\n            $$\n\\therefore 5\\frac{3}{4}=\\frac{23}{4}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-mixed-fractions"
  },
  {
    "record_id": "ch04-b011",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Worked example 4.2: Expressing improper fractions as mixed numbers"
    },
    "content_text": "",
    "prompt_text": "Write $\\frac{26}{3}$ as a mixed number.",
    "answer_text": "Step 1: Use the denominator to see how many parts there are in one whole.\n\n            The denominator of this improper fraction is 3.\n            This means that each whole is divided into 3 parts. We are dealing with thirds.\n\n            Step 2: Determine how many whole numbers can be formed from the total parts we have. To do this, divide the numerator by the denominator from Step 1.\n\n            The numerator gives the total parts we have: 26\n            If there are 3 parts in one whole, we can form 8 wholes from 26 parts: $8\\times3=24$\n\n            $$\n            \\require{enclose}\n            \\begin{array}{r}\n            8\\\\\n            3\\enclose{longdiv}{26}\\\\\n            \\underline{-24} \\newline\n            2\n            \\end{array}\n            $$\n\n            The whole number part of the mixed number is: 8\n\n            Step 3: Determine what fraction is left over after we formed the whole numbers.\n\n            You know that the denominator, which tells us how many parts there are in one whole, is 3.\n            To work out the numerator, use the parts that are left over after we formed the whole numbers. If you look at the long division, the remainder is 2.\n\n            After we formed the whole numbers, the fraction $\\frac{2}{3}$ is left over.\n\n            Step 4: Write down the mixed number as a whole number followed by a proper fraction.\n\n            $$\n\\therefore \\frac{26}{3}=8\\frac{2}{3}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-mixed-fractions"
  },
  {
    "record_id": "ch04-b012",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.2: Convert between mixed numbers and improper fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.2: Convert between mixed numbers and improper fractions",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-mixed-fractions"
  },
  {
    "record_id": "ch04-b012-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.2: Convert between mixed numbers and improper fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.2: Convert between mixed numbers and improper fractions\n\n1. Express the following mixed numbers as improper fractions.\n\n   1. $6\\frac{3}{7}$\n   2. $2\\frac{5}{11}$\n   3. $13\\frac{2}{3}$",
    "answer_text": "1. $6\\frac{3}{7}$\n\n            Parts in one whole: 7\n            Parts in 6 wholes: $6\\times7=42$\n            Total parts: $42+3=45$\n\n            $$\n\\therefore 6\\frac{3}{7}=\\frac{45}{7}\n$$\n\n            2. $2\\frac{5}{11}$\n\n            Parts in one whole: 11\n            Parts in 2 wholes: $2\\times11=22$\n            Total parts: $22+5=27$\n\n            $$\n\\therefore 2\\frac{5}{11}=\\frac{27}{11}\n$$\n\n            3. $13\\frac{2}{3}$\n\n            Parts in one whole: 3\n            Parts in 13 wholes: $13\\times3=39$\n            Total parts: $39+2=41$\n\n            $$\n\\therefore 13\\frac{2}{3}=\\frac{41}{3}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-mixed-fractions"
  },
  {
    "record_id": "ch04-b012-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.2: Convert between mixed numbers and improper fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.2: Convert between mixed numbers and improper fractions\n\n2. Express the following improper fractions as mixed numbers.\n\n   1. $\\frac{30}{7}$\n   2. $\\frac{112}{9}$\n   3. $\\frac{85}{11}$",
    "answer_text": "1. $\\frac{30}{7}$\n\n            Parts in one whole: 7\n            Total parts: 30\n\n            $$\n\\require{enclose}\n\\begin{array}{r}\n     4\\newline\n7 \\enclose{longdiv}{30}\\newline\n\\underline{-28} \\newline\n2\n\\end{array}\n$$\n\n            Whole number: 4\n            Fraction: $\\frac{2}{7}$\n\n            $$\n\\therefore \\frac{30}{7}=4\\frac{2}{7}\n$$\n\n            2. $\\frac{112}{9}$\n\n            Parts in one whole: 9\n            Total parts: 112\n\n            $$\n\\require{enclose}\n\\begin{array}{r}\n12\\newline\n9 \\enclose{longdiv}{112}\\newline\n\\underline{-9}\\phantom{0} \\newline\n22 \\newline\n\\underline{-18} \\newline\n4\n\\end{array}\n$$\n\n            Whole number: 12\n            Fraction: $\\frac{4}{9}$\n\n            $$\n\\therefore \\frac{112}{9}=12\\frac{4}{9}\n$$\n\n            3. $\\frac{85}{11}$\n\n            Parts in one whole: 11\n            Total parts: 85\n\n            $$\n\\require{enclose}\n\\begin{array}{r}\n7\\newline\n11 \\enclose{longdiv}{85}\\newline\n\\underline{-77} \\newline\n8 \\newline\n\\end{array}\n$$\n\n            Whole number: 7\n            Fraction: $\\frac{8}{11}$\n\n            $$\n\\therefore \\frac{85}{11}=7\\frac{8}{11}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-mixed-fractions"
  },
  {
    "record_id": "ch04-b013",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.1 Types of fractions",
      "h3": null
    },
    "content_text": "Once you understand how to express a mixed number as an improper fraction, you may use this short method. Example: 3\\frac{3}{5}. Denominator: \\frac{\\phantom{00}}{5}. Numerator: (5\\times3)+3=18. Answer: \\frac{18}{5}.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-mixed-fractions"
  },
  {
    "record_id": "ch04-b057-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": "Exercise 4.12: Use equivalent fractions to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.12: Use equivalent fractions to solve problems\n\n2. After a birthday party, $2\\frac{2}{5}$ cakes are left over. If the leftover cake is cut into equal pieces, how many people could get one piece each?",
    "answer_text": "Parts in one whole: 5\nParts in 2 cakes: $2\\times5=10$\nAdditional pieces: 2\nTotal pieces available: $10+2=12$",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
  },
  {
    "record_id": "ch04-b058",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.7 Summary",
      "h3": null
    },
    "content_text": "- A common fraction is written as $\\frac{\\text{numerator}}{\\text{denominator}}$.\n- A proper fraction is smaller than 1, for example $\\frac{2}{7}$.\n- A mixed number consists of a whole number and a proper fraction, for example $5\\frac{1}{6}$.\n- An improper fraction is larger than 1, for example $\\frac{9}{4}$.\n- Equivalent fractions have different numerators and denominators but the same value, for example $\\frac{1}{2}=\\frac{2}{4}=\\frac{4}{8}$.\n- A fraction is in its simplest form when the numerator and denominator have no common factor.\n- To compare fractions, we must express them with the same denominators. The lowest common denominator is the smallest whole number into which all the denominators can divide without a remainder.\n- A decimal fraction is written in decimal notation, where the numerator is written after a decimal point and the denominator is a power of ten.\n- In decimal notation, the decimal point separates whole numbers from fractions.\n- If there are three digits after the decimal point, the denominator is $10\\times10\\times10=1,000$.\n- A percentage is a fraction with denominator 100, written with only the numerator followed by a percentage symbol.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
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
