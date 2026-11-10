# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-2",
  "topic_key": "jss1-math-multiplications-and-divisions-of-fractions",
  "topic": "Multiplications and Divisions of Fractions",
  "subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-word-problems-involving-multiplication-and-division-of-fractions",
  "subtopic_title": "Word problems involving multiplication and division of fractions",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-multiplications-and-divisions-of-fractions-word-problems-involving-multiplication-and-division-of-fractions-po01",
        "source_performance_objective_index": 1,
        "text": "Solve word problems involving multiplication and division of fractions"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "word-problems-multiplication-and-division-of-fractions-ao-solve-multiplication-word-problems",
          "text": "Solve word problems involving multiplication of fractions."
        },
        {
          "atomic_objective_id": "word-problems-multiplication-and-division-of-fractions-ao-solve-division-word-problems",
          "text": "Solve word problems involving division of fractions."
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
    "record_id": "ch06-b053",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.3 Practical applications",
      "h3": null
    },
    "content_text": "You can use your knowledge of fractions to solve problems. Here are some hints:\n\n- Remember that the denominator of a fraction tells us how many parts a whole is divided into. The numerator tells us how many of those parts we are dealing with.\n- Read the problem carefully. If at all possible, draw a diagram to represent the situation.\n- Percentages are fractions. For example, 70% of 25 may be written as $\\frac{70}{100}\\times25$.\n- A whole, for example all the sweets or the full length of time or all the money, is represented by the number 1.\n- Decide whether you must add, subtract, multiply or divide:\n  - `find the sum` means you must add\n  - `find the difference` means you must subtract\n  - `of` means you must multiply\n  - `share between` means you must divide",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-word-problems-involving-multiplication-and-division-of-fractions"
  },
  {
    "record_id": "ch06-b054",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.3 Practical applications",
      "h3": "Exercise 6.10: Use operations with fractions to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.10: Use operations with fractions to solve problems",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-word-problems-involving-multiplication-and-division-of-fractions"
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
    "record_id": "ch06-b054-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.3 Practical applications",
      "h3": "Exercise 6.10: Use operations with fractions to solve problems"
    },
    "content_text": "Source math retained:\n\\frac{9}{10}\n\\frac{1}{6}\n\\begin{array}{l}\\phantom{00}\\frac{9}{10}-\\frac{1}{6} \\\\ =\\frac{27}{30}-\\frac{5}{30} \\\\ =\\frac{27-5}{30} \\\\ =\\frac{22}{30} \\\\ =\\frac{11}{15}\\end{array}\n\\frac{11}{15}",
    "prompt_text": "### Exercise 6.10: Use operations with fractions to solve problems\n\n4. Only $\\frac{9}{10}$ of the Mathematics class came to school on Friday. At the start of the lesson, the principal called $\\frac{1}{6}$ of the class to his office. What fraction of the class had Mathematics on Friday?",
    "answer_text": "$$\\begin{array}{l}\\phantom{00}\\frac{9}{10}-\\frac{1}{6} \\\\newline =\\frac{27}{30}-\\frac{5}{30} \\\\newline =\\frac{27-5}{30} \\\\newline =\\frac{22}{30} \\\\newline =\\frac{11}{15}\\end{array}$$\n$\\frac{11}{15}$ of the class had Mathematics on Friday.",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-word-problems-involving-multiplication-and-division-of-fractions"
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
    "record_id": "ch06-b054-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.3 Practical applications",
      "h3": "Exercise 6.10: Use operations with fractions to solve problems"
    },
    "content_text": "Source math retained:\n\\begin{array}{l}\\phantom{000}15\\%\\times1,500 \\\\ =\\frac{15}{100}\\times1,500 \\\\ =\\frac{15\\times1,500}{100} \\\\ =\\frac{15\\times15}{1} \\\\ =\\frac{225}{1}\\end{array}\n₦1,500-₦225=₦1,275",
    "prompt_text": "### Exercise 6.10: Use operations with fractions to solve problems\n\n9. A clothing store offers a discount of 15% on a pair of shoes that originally cost ₦1,500. Calculate the new, discount price.",
    "answer_text": "$$\\begin{array}{l}\\phantom{000}15\\%\\times1,500 \\\\newline =\\frac{15}{100}\\times1,500 \\\\newline =\\frac{15\\times1,500}{100} \\\\newline =\\frac{15\\times15}{1} \\\\newline =\\frac{225}{1}\\end{array}$$\nThe new, discount price is $₦1,500-₦225=₦1,275$.",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
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
  "theme_key": "jss1-theme-2",
  "topic_key": "jss1-math-multiplications-and-divisions-of-fractions",
  "topic": "Multiplications and Divisions of Fractions",
  "subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-word-problems-involving-multiplication-and-division-of-fractions",
  "subtopic_title": "Word problems involving multiplication and division of fractions",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-multiplications-and-divisions-of-fractions-word-problems-involving-multiplication-and-division-of-fractions-po01",
        "source_performance_objective_index": 1,
        "text": "Solve word problems involving multiplication and division of fractions"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "word-problems-multiplication-and-division-of-fractions-ao-solve-multiplication-word-problems",
          "text": "Solve word problems involving multiplication of fractions."
        },
        {
          "atomic_objective_id": "word-problems-multiplication-and-division-of-fractions-ao-solve-division-word-problems",
          "text": "Solve word problems involving division of fractions."
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
    "record_id": "ch06-b053",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.3 Practical applications",
      "h3": null
    },
    "content_text": "You can use your knowledge of fractions to solve problems. Here are some hints:\n\n- Remember that the denominator of a fraction tells us how many parts a whole is divided into. The numerator tells us how many of those parts we are dealing with.\n- Read the problem carefully. If at all possible, draw a diagram to represent the situation.\n- Percentages are fractions. For example, 70% of 25 may be written as $\\frac{70}{100}\\times25$.\n- A whole, for example all the sweets or the full length of time or all the money, is represented by the number 1.\n- Decide whether you must add, subtract, multiply or divide:\n  - `find the sum` means you must add\n  - `find the difference` means you must subtract\n  - `of` means you must multiply\n  - `share between` means you must divide",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-word-problems-involving-multiplication-and-division-of-fractions"
  },
  {
    "record_id": "ch06-b054",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.3 Practical applications",
      "h3": "Exercise 6.10: Use operations with fractions to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 6.10: Use operations with fractions to solve problems",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-word-problems-involving-multiplication-and-division-of-fractions"
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
    "record_id": "ch06-b054-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.3 Practical applications",
      "h3": "Exercise 6.10: Use operations with fractions to solve problems"
    },
    "content_text": "Source math retained:\n\\frac{9}{10}\n\\frac{1}{6}\n\\begin{array}{l}\\phantom{00}\\frac{9}{10}-\\frac{1}{6} \\\\ =\\frac{27}{30}-\\frac{5}{30} \\\\ =\\frac{27-5}{30} \\\\ =\\frac{22}{30} \\\\ =\\frac{11}{15}\\end{array}\n\\frac{11}{15}",
    "prompt_text": "### Exercise 6.10: Use operations with fractions to solve problems\n\n4. Only $\\frac{9}{10}$ of the Mathematics class came to school on Friday. At the start of the lesson, the principal called $\\frac{1}{6}$ of the class to his office. What fraction of the class had Mathematics on Friday?",
    "answer_text": "$$\\begin{array}{l}\\phantom{00}\\frac{9}{10}-\\frac{1}{6} \\\\newline =\\frac{27}{30}-\\frac{5}{30} \\\\newline =\\frac{27-5}{30} \\\\newline =\\frac{22}{30} \\\\newline =\\frac{11}{15}\\end{array}$$\n$\\frac{11}{15}$ of the class had Mathematics on Friday.",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-word-problems-involving-multiplication-and-division-of-fractions"
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
    "record_id": "ch06-b054-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 6: Operations with fractions",
      "h2": "6.3 Practical applications",
      "h3": "Exercise 6.10: Use operations with fractions to solve problems"
    },
    "content_text": "Source math retained:\n\\begin{array}{l}\\phantom{000}15\\%\\times1,500 \\\\ =\\frac{15}{100}\\times1,500 \\\\ =\\frac{15\\times1,500}{100} \\\\ =\\frac{15\\times15}{1} \\\\ =\\frac{225}{1}\\end{array}\n₦1,500-₦225=₦1,275",
    "prompt_text": "### Exercise 6.10: Use operations with fractions to solve problems\n\n9. A clothing store offers a discount of 15% on a pair of shoes that originally cost ₦1,500. Calculate the new, discount price.",
    "answer_text": "$$\\begin{array}{l}\\phantom{000}15\\%\\times1,500 \\\\newline =\\frac{15}{100}\\times1,500 \\\\newline =\\frac{15\\times1,500}{100} \\\\newline =\\frac{15\\times15}{1} \\\\newline =\\frac{225}{1}\\end{array}$$\nThe new, discount price is $₦1,500-₦225=₦1,275$.",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
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
