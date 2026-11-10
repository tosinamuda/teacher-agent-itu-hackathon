# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-1",
  "topic_key": "jss1-math-fractions",
  "topic": "Fractions",
  "subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning",
  "subtopic_title": "Quantitative aptitude reasoning",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-fractions-quantitative-aptitude-reasoning-po01",
        "source_performance_objective_index": 1,
        "text": "Solve problems in quantitative aptitude"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "fractions-quantitative-reasoning-ao-solve-problems",
          "text": "Solve problems in quantitative aptitude."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch04-b056",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": null
    },
    "content_text": "Fractions are very useful in everyday life. We use equivalent fractions to compare different fractions and to convert one type of fraction to another.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
  },
  {
    "record_id": "ch04-b057",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": "Exercise 4.12: Use equivalent fractions to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.12: Use equivalent fractions to solve problems",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
  },
  {
    "record_id": "ch04-b057-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": "Exercise 4.12: Use equivalent fractions to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.12: Use equivalent fractions to solve problems\n\n1. A teacher has 25 learners in her class. At break time, she decides to give each of them one quarter of an orange to eat. How many oranges does she need?",
    "answer_text": "Parts in one whole: 4\nTotal parts: 25\nShe needs $\\frac{25}{4}$ oranges.\n\n$$\n\\require{enclose}\n\\begin{array}{r}\n6\\\\\n4 \\enclose{longdiv}{25}\\\\\n\\underline{-24} \\\\\n1\n\\end{array}\n$$\n\nWhole number: 6\nFraction: $\\frac{1}{4}$\nShe needs $6\\frac{1}{4}$ oranges.",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
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
    "record_id": "ch04-b057-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": "Exercise 4.12: Use equivalent fractions to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.12: Use equivalent fractions to solve problems\n\n3. The floor of a room is tiled with 64 identical tiles. A carpet is put in the centre of the room. The carpet covers $\\frac{3}{8}$ of the tiled surface. How many tiles are under the carpet?",
    "answer_text": "$$\n\\frac{3}{8}=\\frac{\\square}{64}\n$$\n\n$$\n\\frac{3\\times8}{8\\times8}=\\frac{24}{64}\n$$\n\nThere are 24 tiles under the carpet.",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
  },
  {
    "record_id": "ch04-b057-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": "Exercise 4.12: Use equivalent fractions to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.12: Use equivalent fractions to solve problems\n\n4. A bag with 72 sweets is divided between Musa, Umar and Isa. Musa gets 27 sweets, Umar gets 12 sweets, and Isa gets the rest of the sweets. Determine which fraction of the bag each boy received.",
    "answer_text": "Musa:\n$$\n\\frac{27}{72}=\\frac{27\\div9}{72\\div9}=\\frac{3}{8}\n$$\n\nUmar:\n$$\n\\frac{12}{72}=\\frac{12\\div12}{72\\div12}=\\frac{1}{6}\n$$\n\nIsa received $72-27-12=33$ sweets:\n$$\n\\frac{33}{72}=\\frac{33\\div3}{72\\div3}=\\frac{11}{24}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
  },
  {
    "record_id": "ch04-b057-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": "Exercise 4.12: Use equivalent fractions to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.12: Use equivalent fractions to solve problems\n\n5. Atinuke and Eniola buy a bag of rice. Atinuke gets $\\frac{3}{7}$ of the bag, Eniola gets $\\frac{5}{9}$ of the bag and a little bit is left over. Who received the larger portion of rice, Atinuke or Eniola?",
    "answer_text": "$$\n\\text{LCD}=63\n$$\n\n$$\n\\frac{3}{7}=\\frac{3\\times9}{7\\times9}=\\frac{27}{63}\n$$\n\n$$\n\\frac{5}{9}=\\frac{5\\times7}{9\\times7}=\\frac{35}{63}\n$$\n\nEniola received the larger portion of the rice.",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
  },
  {
    "record_id": "ch04-b057-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": "Exercise 4.12: Use equivalent fractions to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.12: Use equivalent fractions to solve problems\n\n6. A wall with a surface area of 1 m^2 is painted. The painter knocks over the can of paint and some of the paint cannot be recovered. She is only able to paint 0.85 m^2 of the wall. Express the fraction of the wall that was painted as a common fraction.",
    "answer_text": "There are 2 digits after the decimal point:\n$$\n\\frac{85}{100}=\\frac{85\\div5}{100\\div5}=\\frac{17}{20}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
  },
  {
    "record_id": "ch04-b057-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": "Exercise 4.12: Use equivalent fractions to solve problems"
    },
    "content_text": "Source math retained:\n\\frac{5}{8}\n\\require{enclose} \\begin{array}{l} \\phantom{00} 0.6 2 5\\\\ 8 \\enclose{longdiv}{5.0 0 0} \\underline{-0}\\downarrow \\downarrow \\downarrow \\\\ \\phantom{00} 5 0 \\\\ \\underline{-4 8} \\\\ \\phantom{000} 2 0 \\\\ \\phantom{00}\\underline{-1 6} \\\\ \\phantom{00000} 4 0 \\\\ \\phantom{000}\\underline{-4 0} \\\\ \\phantom{000000} 0 \\\\ \\end{array}\n\\therefore \\frac{5}{8}=0.625",
    "prompt_text": "### Exercise 4.12: Use equivalent fractions to solve problems\n\n7. Amadi has to walk 1 km to school. After walking $\\frac{5}{8}$ of the way, he realises that he forgot a book at home and he turns around. Determine the distance Amadi walked before he turned around. Give the answer in kilometres.\n\n$$\n\\require{enclose}\n\\begin{array}{l}\n\\phantom{00} 0.6\\,2\\,5\\\\\n8 \\enclose{longdiv}{5.0\\,0\\,0}\\\\\n\\,\\underline{-0}\\downarrow\\,\\downarrow\\,\\downarrow  \\\\\n\\phantom{00} 5\\,0 \\\\\n\\,\\underline{-4\\,8} \\\\\n\\,\\phantom{000} 2\\,0  \\\\\n\\phantom{00}\\underline{-1\\,6} \\\\\n\\phantom{00000} 4\\,0   \\\\\n\\;\\phantom{000}\\underline{-4\\,0}  \\\\\n\\;\\phantom{000000} 0   \\\\\n\\end{array}\n$$\n\n$$\n\\therefore \\frac{5}{8}=0.625\n$$\n\nAmadi walked 0.625 km before he turned around.",
    "answer_text": "$$\n\\require{enclose}\n\\begin{array}{l}\n\\phantom{00} 0.6\\,2\\,5\\\\\n8 \\enclose{longdiv}{5.0\\,0\\,0}\\\\\n\\,\\underline{-0}\\downarrow\\,\\downarrow\\,downarrow  \\\\\n\\phantom{00} 5\\,0 \\\\\n\\,\\underline{-4\\,8} \\\\\n\\,\\phantom{000} 2\\,0  \\\\\n\\phantom{00}\\underline{-1\\,6} \\\\\n\\phantom{00000} 4\\,0   \\\\\n\\;\\phantom{000}\\underline{-4\\,0}  \\\\\n\\;\\phantom{000000} 0   \\\\\n\\end{array}\n$$\n\n$$\n\\therefore \\frac{5}{8}=0.625\n$$\n\nAmadi walked 0.625 km before he turned around.",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
  },
  {
    "record_id": "ch04-b057-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": "Exercise 4.12: Use equivalent fractions to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.12: Use equivalent fractions to solve problems\n\n8. Jummai got 88% for a class test. The test was for 25 marks. Calculate Jummai's mark out of 25.",
    "answer_text": "$$\n\\frac{88}{100}=\\frac{\\square}{25}\n$$\n\n$$\n\\frac{88\\div4}{100\\div4}=\\frac{22}{25}\n$$\n\nJummai's mark was 22 out of 25.",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
  },
  {
    "record_id": "ch04-b057-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": "Exercise 4.12: Use equivalent fractions to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.12: Use equivalent fractions to solve problems\n\n9. There are 30 students in a class. If 21 students are girls, what percentage of the class is female?",
    "answer_text": "Fraction of the class that is female: $\\frac{21}{30}$\n\n$$\n30=2\\times3\\times5\n$$\n\n$$\n100=2^2\\times 5^2\n$$\n\n$$\n\\therefore \\text{LCM}=3\\times2^2\\times5^2=3\\times4\\times25=300\n$$\n\n$$\n\\frac{21\\times10}{30\\times10}=\\frac{210}{300}\n$$\n\n$$\n\\frac{210\\div3}{300\\div3}=\\frac{70}{100}\n$$\n\n$$\n\\therefore\\frac{21}{30}=70\\%\n$$\n\n70% of the class is female.",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
  },
  {
    "record_id": "ch04-b057-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": "Exercise 4.12: Use equivalent fractions to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.12: Use equivalent fractions to solve problems\n\n10. A children's clothing store advertises a 15% discount on a dress of ₦3,000. Calculate the value of the discount.",
    "answer_text": "$$\n\\frac{15}{100}=\\frac{\\square}{3,000}\n$$\n\n$$\n\\frac{15\\times30}{100\\times30}=\\frac{450}{3,000}\n$$\n\nThe discount is ₦450.",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
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
  "subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning",
  "subtopic_title": "Quantitative aptitude reasoning",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-fractions-quantitative-aptitude-reasoning-po01",
        "source_performance_objective_index": 1,
        "text": "Solve problems in quantitative aptitude"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "fractions-quantitative-reasoning-ao-solve-problems",
          "text": "Solve problems in quantitative aptitude."
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
    "record_id": "ch04-b056",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": null
    },
    "content_text": "Fractions are very useful in everyday life. We use equivalent fractions to compare different fractions and to convert one type of fraction to another.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
  },
  {
    "record_id": "ch04-b057",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": "Exercise 4.12: Use equivalent fractions to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.12: Use equivalent fractions to solve problems",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
  },
  {
    "record_id": "ch04-b057-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": "Exercise 4.12: Use equivalent fractions to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.12: Use equivalent fractions to solve problems\n\n1. A teacher has 25 learners in her class. At break time, she decides to give each of them one quarter of an orange to eat. How many oranges does she need?",
    "answer_text": "Parts in one whole: 4\nTotal parts: 25\nShe needs $\\frac{25}{4}$ oranges.\n\n$$\n\\require{enclose}\n\\begin{array}{r}\n6\\\\\n4 \\enclose{longdiv}{25}\\\\\n\\underline{-24} \\\\\n1\n\\end{array}\n$$\n\nWhole number: 6\nFraction: $\\frac{1}{4}$\nShe needs $6\\frac{1}{4}$ oranges.",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
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
    "record_id": "ch04-b057-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": "Exercise 4.12: Use equivalent fractions to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.12: Use equivalent fractions to solve problems\n\n3. The floor of a room is tiled with 64 identical tiles. A carpet is put in the centre of the room. The carpet covers $\\frac{3}{8}$ of the tiled surface. How many tiles are under the carpet?",
    "answer_text": "$$\n\\frac{3}{8}=\\frac{\\square}{64}\n$$\n\n$$\n\\frac{3\\times8}{8\\times8}=\\frac{24}{64}\n$$\n\nThere are 24 tiles under the carpet.",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
  },
  {
    "record_id": "ch04-b057-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": "Exercise 4.12: Use equivalent fractions to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.12: Use equivalent fractions to solve problems\n\n4. A bag with 72 sweets is divided between Musa, Umar and Isa. Musa gets 27 sweets, Umar gets 12 sweets, and Isa gets the rest of the sweets. Determine which fraction of the bag each boy received.",
    "answer_text": "Musa:\n$$\n\\frac{27}{72}=\\frac{27\\div9}{72\\div9}=\\frac{3}{8}\n$$\n\nUmar:\n$$\n\\frac{12}{72}=\\frac{12\\div12}{72\\div12}=\\frac{1}{6}\n$$\n\nIsa received $72-27-12=33$ sweets:\n$$\n\\frac{33}{72}=\\frac{33\\div3}{72\\div3}=\\frac{11}{24}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
  },
  {
    "record_id": "ch04-b057-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": "Exercise 4.12: Use equivalent fractions to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.12: Use equivalent fractions to solve problems\n\n5. Atinuke and Eniola buy a bag of rice. Atinuke gets $\\frac{3}{7}$ of the bag, Eniola gets $\\frac{5}{9}$ of the bag and a little bit is left over. Who received the larger portion of rice, Atinuke or Eniola?",
    "answer_text": "$$\n\\text{LCD}=63\n$$\n\n$$\n\\frac{3}{7}=\\frac{3\\times9}{7\\times9}=\\frac{27}{63}\n$$\n\n$$\n\\frac{5}{9}=\\frac{5\\times7}{9\\times7}=\\frac{35}{63}\n$$\n\nEniola received the larger portion of the rice.",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
  },
  {
    "record_id": "ch04-b057-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": "Exercise 4.12: Use equivalent fractions to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.12: Use equivalent fractions to solve problems\n\n6. A wall with a surface area of 1 m^2 is painted. The painter knocks over the can of paint and some of the paint cannot be recovered. She is only able to paint 0.85 m^2 of the wall. Express the fraction of the wall that was painted as a common fraction.",
    "answer_text": "There are 2 digits after the decimal point:\n$$\n\\frac{85}{100}=\\frac{85\\div5}{100\\div5}=\\frac{17}{20}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
  },
  {
    "record_id": "ch04-b057-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": "Exercise 4.12: Use equivalent fractions to solve problems"
    },
    "content_text": "Source math retained:\n\\frac{5}{8}\n\\require{enclose} \\begin{array}{l} \\phantom{00} 0.6 2 5\\\\ 8 \\enclose{longdiv}{5.0 0 0} \\underline{-0}\\downarrow \\downarrow \\downarrow \\\\ \\phantom{00} 5 0 \\\\ \\underline{-4 8} \\\\ \\phantom{000} 2 0 \\\\ \\phantom{00}\\underline{-1 6} \\\\ \\phantom{00000} 4 0 \\\\ \\phantom{000}\\underline{-4 0} \\\\ \\phantom{000000} 0 \\\\ \\end{array}\n\\therefore \\frac{5}{8}=0.625",
    "prompt_text": "### Exercise 4.12: Use equivalent fractions to solve problems\n\n7. Amadi has to walk 1 km to school. After walking $\\frac{5}{8}$ of the way, he realises that he forgot a book at home and he turns around. Determine the distance Amadi walked before he turned around. Give the answer in kilometres.\n\n$$\n\\require{enclose}\n\\begin{array}{l}\n\\phantom{00} 0.6\\,2\\,5\\\\\n8 \\enclose{longdiv}{5.0\\,0\\,0}\\\\\n\\,\\underline{-0}\\downarrow\\,\\downarrow\\,\\downarrow  \\\\\n\\phantom{00} 5\\,0 \\\\\n\\,\\underline{-4\\,8} \\\\\n\\,\\phantom{000} 2\\,0  \\\\\n\\phantom{00}\\underline{-1\\,6} \\\\\n\\phantom{00000} 4\\,0   \\\\\n\\;\\phantom{000}\\underline{-4\\,0}  \\\\\n\\;\\phantom{000000} 0   \\\\\n\\end{array}\n$$\n\n$$\n\\therefore \\frac{5}{8}=0.625\n$$\n\nAmadi walked 0.625 km before he turned around.",
    "answer_text": "$$\n\\require{enclose}\n\\begin{array}{l}\n\\phantom{00} 0.6\\,2\\,5\\\\\n8 \\enclose{longdiv}{5.0\\,0\\,0}\\\\\n\\,\\underline{-0}\\downarrow\\,\\downarrow\\,downarrow  \\\\\n\\phantom{00} 5\\,0 \\\\\n\\,\\underline{-4\\,8} \\\\\n\\,\\phantom{000} 2\\,0  \\\\\n\\phantom{00}\\underline{-1\\,6} \\\\\n\\phantom{00000} 4\\,0   \\\\\n\\;\\phantom{000}\\underline{-4\\,0}  \\\\\n\\;\\phantom{000000} 0   \\\\\n\\end{array}\n$$\n\n$$\n\\therefore \\frac{5}{8}=0.625\n$$\n\nAmadi walked 0.625 km before he turned around.",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
  },
  {
    "record_id": "ch04-b057-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": "Exercise 4.12: Use equivalent fractions to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.12: Use equivalent fractions to solve problems\n\n8. Jummai got 88% for a class test. The test was for 25 marks. Calculate Jummai's mark out of 25.",
    "answer_text": "$$\n\\frac{88}{100}=\\frac{\\square}{25}\n$$\n\n$$\n\\frac{88\\div4}{100\\div4}=\\frac{22}{25}\n$$\n\nJummai's mark was 22 out of 25.",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
  },
  {
    "record_id": "ch04-b057-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": "Exercise 4.12: Use equivalent fractions to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.12: Use equivalent fractions to solve problems\n\n9. There are 30 students in a class. If 21 students are girls, what percentage of the class is female?",
    "answer_text": "Fraction of the class that is female: $\\frac{21}{30}$\n\n$$\n30=2\\times3\\times5\n$$\n\n$$\n100=2^2\\times 5^2\n$$\n\n$$\n\\therefore \\text{LCM}=3\\times2^2\\times5^2=3\\times4\\times25=300\n$$\n\n$$\n\\frac{21\\times10}{30\\times10}=\\frac{210}{300}\n$$\n\n$$\n\\frac{210\\div3}{300\\div3}=\\frac{70}{100}\n$$\n\n$$\n\\therefore\\frac{21}{30}=70\\%\n$$\n\n70% of the class is female.",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
  },
  {
    "record_id": "ch04-b057-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": "Exercise 4.12: Use equivalent fractions to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.12: Use equivalent fractions to solve problems\n\n10. A children's clothing store advertises a 15% discount on a dress of ₦3,000. Calculate the value of the discount.",
    "answer_text": "$$\n\\frac{15}{100}=\\frac{\\square}{3,000}\n$$\n\n$$\n\\frac{15\\times30}{100\\times30}=\\frac{450}{3,000}\n$$\n\nThe discount is ₦450.",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
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
