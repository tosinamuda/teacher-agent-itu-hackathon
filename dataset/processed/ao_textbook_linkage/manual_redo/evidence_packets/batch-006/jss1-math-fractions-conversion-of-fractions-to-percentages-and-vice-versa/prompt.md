# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-1",
  "topic_key": "jss1-math-fractions",
  "topic": "Fractions",
  "subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa",
  "subtopic_title": "Conversion of fractions to percentages and vice versa",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa-po01",
        "source_performance_objective_index": 1,
        "text": "Convert fractions to percentages and percentages to fractions"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "fractions-to-percentages-ao-convert-fractions-to-percentages",
          "text": "Convert fractions to percentages."
        },
        {
          "atomic_objective_id": "fractions-to-percentages-ao-convert-percentages-to-fractions",
          "text": "Convert percentages to fractions."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch04-b046",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": null
    },
    "content_text": "As well as writing a fraction as a common fraction or a decimal fraction, we may also express a fraction as a **percentage**. A percentage is a fraction in which the denominator is always 100. Only the numerator is written down, followed by a percentage symbol: %. The symbol shows that the number we wrote down gives the parts of a whole that is divided into 100.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b047",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": null
    },
    "content_text": "**percentage** A percentage is a fraction in which the denominator is 100 and where only the numerator is written down, followed by a percentage symbol.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b048",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": null
    },
    "content_text": "This figure is divided into 100 parts. There are 22 blocks that are shaded. The common fraction $\\frac{22}{100}$ tells you what part is shaded. To express this as a percentage, we write only the numerator, followed by a percentage symbol: 22%.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-020.png)",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b049",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": null
    },
    "content_text": "If we shade all the blocks in the figure, the shaded fraction will be $\\frac{100}{100}=1$. One full whole is therefore 100%.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b050",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": "Converting percentages to common fractions"
    },
    "content_text": "It is easy to convert percentages to common fractions. We simply use the form $\\frac{\\text{numerator}}{\\text{denominator}}$. We know that the denominator is always 100, so we have $\\frac{\\text{numerator}}{100}$. The numerator is the number before the percentage symbol.\n\nFor example, $36\\% = \\frac{36}{100}$. The simplest form of this fraction is $\\frac{36\\div4}{100\\div4}=\\frac{9}{25}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b051",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": "Exercise 4.10: Convert percentages to common fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.10: Convert percentages to common fractions\n\nConvert the following percentages to common fractions.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b051-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": "Exercise 4.10: Convert percentages to common fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.10: Convert percentages to common fractions\n\n1. 55%",
    "answer_text": "$$\n\\frac{55}{100}\n$$\n\nIn its simplest form:\n$$\n\\frac{55\\div5}{100\\div5}=\\frac{11}{20}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b051-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": "Exercise 4.10: Convert percentages to common fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.10: Convert percentages to common fractions\n\n2. 80%",
    "answer_text": "$$\n\\frac{80}{100}\n$$\n\nIn its simplest form:\n$$\n\\frac{80\\div20}{100\\div20}=\\frac{4}{5}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b051-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": "Exercise 4.10: Convert percentages to common fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.10: Convert percentages to common fractions\n\n3. 4%",
    "answer_text": "$$\n\\frac{4}{100}\n$$\n\nIn its simplest form:\n$$\n\\frac{4\\div4}{100\\div4}=\\frac{1}{25}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b052",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": "Converting common fractions to percentages"
    },
    "content_text": "To express a common fraction as a percentage, we need to know how many parts out of 100 we are dealing with. Consider the fraction $\\frac{2}{5}$. It shows that we are dealing with 2 parts of a whole that is divided into 5. This square has 100 small blocks in the background, but it is divided into 5 equal rectangles.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-021.png)\n\nWe may represent the fraction $\\frac{2}{5}$ by shading 2 of the 5 rectangles.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-022.png)\n\nIf you count the small blocks that are shaded, you will see that 40 out of the 100 small blocks are shaded. This means that $\\frac{2}{5}=\\frac{40}{100}$. The fraction $\\frac{40}{100}$ has a denominator of 100, so it may be written as a percentage: 40%.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b053",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": "Worked example 4.8: Converting common fractions to percentages"
    },
    "content_text": "",
    "prompt_text": "Write $\\frac{7}{8}$ as a percentage.\n\nStep 1: Find the LCM of 100 and the denominator.\n\n$8=2^3$\n$100=2^2\\times 5^2$\n$\\therefore \\text{LCM}=2^3\\times5^2=8\\times25=200$\n\nStep 2: Find the equivalent fraction in which the denominator is equal to the number obtained in Step 1.\n\n$$\n\\frac{7\\times25}{8\\times25}=\\frac{175}{200}\n$$\n\nStep 3: Simplify the fraction from Step 2 until its denominator is 100.\n\n$$\n\\frac{175\\div2}{200\\div2}=\\frac{87.5}{100}\n$$\n\nA common fraction cannot have a decimal fraction as its numerator or denominator. The \"fraction\" obtained in Step 3 is just used to help us get to the answer.\n\nStep 4: Write down the numerator from Step 3, followed by a percentage symbol.\n\n$$\n\\frac{7}{8}=87.5\\%\n$$",
    "answer_text": "Step 1: Find the LCM of 100 and the denominator.\n\n$$\n8=2^3\n$$\n\n$$\n100=2^2\\times 5^2\n$$\n\n$$\n\\therefore \\text{LCM}=2^3\\times5^2=8\\times25=200\n$$\n\nStep 2: Find the equivalent fraction in which the denominator is equal to the number obtained in Step 1.\n\n$$\n\\frac{7\\times25}{8\\times25}=\\frac{175}{200}\n$$\n\nStep 3: Simplify the fraction from Step 2 until its denominator is 100.\n\n$$\n\\frac{175\\div2}{200\\div2}=\\frac{87.5}{100}\n$$\n\nA common fraction cannot have a decimal fraction as its numerator or denominator. The \"fraction\" obtained in Step 3 is just used to help us get to the answer.\n\nStep 4: Write down the numerator from Step 3, followed by a percentage symbol.\n\n$$\n\\frac{7}{8}=87.5\\%\n$$",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b054",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": "Converting common fractions to percentages"
    },
    "content_text": "There are other ways to convert common fractions to percentages. You will learn more about this in Chapter 6.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b055",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": "Exercise 4.11: Convert common fractions to percentages"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.11: Convert common fractions to percentages",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b055-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": "Exercise 4.11: Convert common fractions to percentages"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.11: Convert common fractions to percentages\n\n1. $\\frac{3}{5}$\n\n$$\n\\frac{5}{5}\n$$\n\n$$\n100=2^2\\times 5^2\n$$\n\n$$\n\\therefore \\text{LCM}=2^2\\times5^2=4\\times25=100\n$$\n\n$$\n\\frac{3\\times20}{5\\times20}=\\frac{60}{100}\n$$\n\n$$\n\\therefore\\frac{3}{5}=60\\%\n$$",
    "answer_text": "$$\n5=5\n$$\n\n$$\n100=2^2\\times 5^2\n$$\n\n$$\n\\therefore \\text{LCM}=2^2\\times5^2=4\\times25=100\n$$\n\n$$\n\\frac{3\\times20}{5\\times20}=\\frac{60}{100}\n$$\n\n$$\n\\therefore\\frac{3}{5}=60\\%\n$$",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b055-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": "Exercise 4.11: Convert common fractions to percentages"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.11: Convert common fractions to percentages\n\n2. $\\frac{13}{25}$",
    "answer_text": "$$\n25=5^2\n$$\n\n$$\n100=2^2\\times 5^2\n$$\n\n$$\n\\therefore \\text{LCM}=2^2\\times5^2=4\\times25=100\n$$\n\n$$\n\\frac{13\\times4}{25\\times4}=\\frac{52}{100}\n$$\n\n$$\n\\therefore\\frac{13}{25}=52\\%\n$$",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b055-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": "Exercise 4.11: Convert common fractions to percentages"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.11: Convert common fractions to percentages\n\n3. $\\frac{1}{6}$\n\n$$\n6=2\\times3\n$$\n\n$$\n100=2^2\\times 5^2\n$$\n\n$$\n\\therefore \\text{LCM}=3\\times2^2\\times5^2=3\\times4\\times25=300\n$$\n\n$$\n\\frac{1\\times50}{6\\times50}=\\frac{50}{300}\n$$\n\n$$\n\\frac{50\\div3}{300\\div3}=\\frac{?}{100}\n$$\n\nUse long division to determine the numerator:\n\n$$\n\\require{enclose}\n\\begin{array}{l}\n\\phantom{00} 16.6\\,6 \\\\\n3 \\enclose{longdiv}{50.0\\,0}\\\\\n\\,\\underline{-3}\\!\\downarrow\\,\\downarrow\\, \\downarrow \\\\\n\\phantom{00} 2\\,0 \\\\\n\\;\\underline{-1\\,8} \\\\\n\\,\\phantom{000} 2\\,0  \\\\\n\\phantom{00}\\underline{-1\\,8} \\\\\n\\phantom{00000} 2\\,0   \\\\\n\\end{array}\n$$\n\nWe keep on getting the same remainder, so this division produces a recurring decimal. We write a dot above the digit that repeats.\n\n$$\n\\frac{50\\div3}{300\\div3}=\\frac{16.\\dot{6}}{100}\n$$\n\n$$\n\\therefore\\frac{1}{6}=16.\\dot{6}\\%\n$$",
    "answer_text": "$$\n6=2\\times3\n$$\n\n$$\n100=2^2\\times 5^2\n$$\n\n$$\n\\therefore \\text{LCM}=3\\times2^2\\times5^2=3\\times4\\times25=300\n$$\n\n$$\n\\frac{1\\times50}{6\\times50}=\\frac{50}{300}\n$$\n\n$$\n\\frac{50\\div3}{300\\div3}=\\frac{16.\\dot{6}}{100}\n$$\n\n$$\n\\therefore\\frac{1}{6}=16.\\dot{6}\\%\n$$",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
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
  "subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa",
  "subtopic_title": "Conversion of fractions to percentages and vice versa",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa-po01",
        "source_performance_objective_index": 1,
        "text": "Convert fractions to percentages and percentages to fractions"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "fractions-to-percentages-ao-convert-fractions-to-percentages",
          "text": "Convert fractions to percentages."
        },
        {
          "atomic_objective_id": "fractions-to-percentages-ao-convert-percentages-to-fractions",
          "text": "Convert percentages to fractions."
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
    "record_id": "ch04-b046",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": null
    },
    "content_text": "As well as writing a fraction as a common fraction or a decimal fraction, we may also express a fraction as a **percentage**. A percentage is a fraction in which the denominator is always 100. Only the numerator is written down, followed by a percentage symbol: %. The symbol shows that the number we wrote down gives the parts of a whole that is divided into 100.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b047",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": null
    },
    "content_text": "**percentage** A percentage is a fraction in which the denominator is 100 and where only the numerator is written down, followed by a percentage symbol.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b048",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": null
    },
    "content_text": "This figure is divided into 100 parts. There are 22 blocks that are shaded. The common fraction $\\frac{22}{100}$ tells you what part is shaded. To express this as a percentage, we write only the numerator, followed by a percentage symbol: 22%.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-020.png)",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b049",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": null
    },
    "content_text": "If we shade all the blocks in the figure, the shaded fraction will be $\\frac{100}{100}=1$. One full whole is therefore 100%.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b050",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": "Converting percentages to common fractions"
    },
    "content_text": "It is easy to convert percentages to common fractions. We simply use the form $\\frac{\\text{numerator}}{\\text{denominator}}$. We know that the denominator is always 100, so we have $\\frac{\\text{numerator}}{100}$. The numerator is the number before the percentage symbol.\n\nFor example, $36\\% = \\frac{36}{100}$. The simplest form of this fraction is $\\frac{36\\div4}{100\\div4}=\\frac{9}{25}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b051",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": "Exercise 4.10: Convert percentages to common fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.10: Convert percentages to common fractions\n\nConvert the following percentages to common fractions.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b051-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": "Exercise 4.10: Convert percentages to common fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.10: Convert percentages to common fractions\n\n1. 55%",
    "answer_text": "$$\n\\frac{55}{100}\n$$\n\nIn its simplest form:\n$$\n\\frac{55\\div5}{100\\div5}=\\frac{11}{20}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b051-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": "Exercise 4.10: Convert percentages to common fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.10: Convert percentages to common fractions\n\n2. 80%",
    "answer_text": "$$\n\\frac{80}{100}\n$$\n\nIn its simplest form:\n$$\n\\frac{80\\div20}{100\\div20}=\\frac{4}{5}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b051-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": "Exercise 4.10: Convert percentages to common fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.10: Convert percentages to common fractions\n\n3. 4%",
    "answer_text": "$$\n\\frac{4}{100}\n$$\n\nIn its simplest form:\n$$\n\\frac{4\\div4}{100\\div4}=\\frac{1}{25}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b052",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": "Converting common fractions to percentages"
    },
    "content_text": "To express a common fraction as a percentage, we need to know how many parts out of 100 we are dealing with. Consider the fraction $\\frac{2}{5}$. It shows that we are dealing with 2 parts of a whole that is divided into 5. This square has 100 small blocks in the background, but it is divided into 5 equal rectangles.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-021.png)\n\nWe may represent the fraction $\\frac{2}{5}$ by shading 2 of the 5 rectangles.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-022.png)\n\nIf you count the small blocks that are shaded, you will see that 40 out of the 100 small blocks are shaded. This means that $\\frac{2}{5}=\\frac{40}{100}$. The fraction $\\frac{40}{100}$ has a denominator of 100, so it may be written as a percentage: 40%.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b053",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": "Worked example 4.8: Converting common fractions to percentages"
    },
    "content_text": "",
    "prompt_text": "Write $\\frac{7}{8}$ as a percentage.\n\nStep 1: Find the LCM of 100 and the denominator.\n\n$8=2^3$\n$100=2^2\\times 5^2$\n$\\therefore \\text{LCM}=2^3\\times5^2=8\\times25=200$\n\nStep 2: Find the equivalent fraction in which the denominator is equal to the number obtained in Step 1.\n\n$$\n\\frac{7\\times25}{8\\times25}=\\frac{175}{200}\n$$\n\nStep 3: Simplify the fraction from Step 2 until its denominator is 100.\n\n$$\n\\frac{175\\div2}{200\\div2}=\\frac{87.5}{100}\n$$\n\nA common fraction cannot have a decimal fraction as its numerator or denominator. The \"fraction\" obtained in Step 3 is just used to help us get to the answer.\n\nStep 4: Write down the numerator from Step 3, followed by a percentage symbol.\n\n$$\n\\frac{7}{8}=87.5\\%\n$$",
    "answer_text": "Step 1: Find the LCM of 100 and the denominator.\n\n$$\n8=2^3\n$$\n\n$$\n100=2^2\\times 5^2\n$$\n\n$$\n\\therefore \\text{LCM}=2^3\\times5^2=8\\times25=200\n$$\n\nStep 2: Find the equivalent fraction in which the denominator is equal to the number obtained in Step 1.\n\n$$\n\\frac{7\\times25}{8\\times25}=\\frac{175}{200}\n$$\n\nStep 3: Simplify the fraction from Step 2 until its denominator is 100.\n\n$$\n\\frac{175\\div2}{200\\div2}=\\frac{87.5}{100}\n$$\n\nA common fraction cannot have a decimal fraction as its numerator or denominator. The \"fraction\" obtained in Step 3 is just used to help us get to the answer.\n\nStep 4: Write down the numerator from Step 3, followed by a percentage symbol.\n\n$$\n\\frac{7}{8}=87.5\\%\n$$",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b054",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": "Converting common fractions to percentages"
    },
    "content_text": "There are other ways to convert common fractions to percentages. You will learn more about this in Chapter 6.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b055",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": "Exercise 4.11: Convert common fractions to percentages"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.11: Convert common fractions to percentages",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b055-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": "Exercise 4.11: Convert common fractions to percentages"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.11: Convert common fractions to percentages\n\n1. $\\frac{3}{5}$\n\n$$\n\\frac{5}{5}\n$$\n\n$$\n100=2^2\\times 5^2\n$$\n\n$$\n\\therefore \\text{LCM}=2^2\\times5^2=4\\times25=100\n$$\n\n$$\n\\frac{3\\times20}{5\\times20}=\\frac{60}{100}\n$$\n\n$$\n\\therefore\\frac{3}{5}=60\\%\n$$",
    "answer_text": "$$\n5=5\n$$\n\n$$\n100=2^2\\times 5^2\n$$\n\n$$\n\\therefore \\text{LCM}=2^2\\times5^2=4\\times25=100\n$$\n\n$$\n\\frac{3\\times20}{5\\times20}=\\frac{60}{100}\n$$\n\n$$\n\\therefore\\frac{3}{5}=60\\%\n$$",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b055-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": "Exercise 4.11: Convert common fractions to percentages"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.11: Convert common fractions to percentages\n\n2. $\\frac{13}{25}$",
    "answer_text": "$$\n25=5^2\n$$\n\n$$\n100=2^2\\times 5^2\n$$\n\n$$\n\\therefore \\text{LCM}=2^2\\times5^2=4\\times25=100\n$$\n\n$$\n\\frac{13\\times4}{25\\times4}=\\frac{52}{100}\n$$\n\n$$\n\\therefore\\frac{13}{25}=52\\%\n$$",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
  },
  {
    "record_id": "ch04-b055-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.5 Percentages",
      "h3": "Exercise 4.11: Convert common fractions to percentages"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.11: Convert common fractions to percentages\n\n3. $\\frac{1}{6}$\n\n$$\n6=2\\times3\n$$\n\n$$\n100=2^2\\times 5^2\n$$\n\n$$\n\\therefore \\text{LCM}=3\\times2^2\\times5^2=3\\times4\\times25=300\n$$\n\n$$\n\\frac{1\\times50}{6\\times50}=\\frac{50}{300}\n$$\n\n$$\n\\frac{50\\div3}{300\\div3}=\\frac{?}{100}\n$$\n\nUse long division to determine the numerator:\n\n$$\n\\require{enclose}\n\\begin{array}{l}\n\\phantom{00} 16.6\\,6 \\\\\n3 \\enclose{longdiv}{50.0\\,0}\\\\\n\\,\\underline{-3}\\!\\downarrow\\,\\downarrow\\, \\downarrow \\\\\n\\phantom{00} 2\\,0 \\\\\n\\;\\underline{-1\\,8} \\\\\n\\,\\phantom{000} 2\\,0  \\\\\n\\phantom{00}\\underline{-1\\,8} \\\\\n\\phantom{00000} 2\\,0   \\\\\n\\end{array}\n$$\n\nWe keep on getting the same remainder, so this division produces a recurring decimal. We write a dot above the digit that repeats.\n\n$$\n\\frac{50\\div3}{300\\div3}=\\frac{16.\\dot{6}}{100}\n$$\n\n$$\n\\therefore\\frac{1}{6}=16.\\dot{6}\\%\n$$",
    "answer_text": "$$\n6=2\\times3\n$$\n\n$$\n100=2^2\\times 5^2\n$$\n\n$$\n\\therefore \\text{LCM}=3\\times2^2\\times5^2=3\\times4\\times25=300\n$$\n\n$$\n\\frac{1\\times50}{6\\times50}=\\frac{50}{300}\n$$\n\n$$\n\\frac{50\\div3}{300\\div3}=\\frac{16.\\dot{6}}{100}\n$$\n\n$$\n\\therefore\\frac{1}{6}=16.\\dot{6}\\%\n$$",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa"
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
