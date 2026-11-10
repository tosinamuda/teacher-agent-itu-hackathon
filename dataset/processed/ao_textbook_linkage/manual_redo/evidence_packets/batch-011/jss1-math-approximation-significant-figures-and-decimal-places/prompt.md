# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-2",
  "topic_key": "jss1-math-approximation",
  "topic": "Approximation",
  "subtopic_id": "jss1-math-approximation-significant-figures-and-decimal-places",
  "subtopic_title": "Significant figures and decimal places",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-approximation-significant-figures-and-decimal-places-po01",
        "source_performance_objective_index": 1,
        "text": "Determine the degree of accuracy of numbers"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "significant-figures-and-decimal-places-ao-determine-degree-of-accuracy",
          "text": "Determine the degree of accuracy of numbers."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-approximation-significant-figures-and-decimal-places-po02",
        "source_performance_objective_index": 2,
        "text": "Round numbers to given significant figures"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "significant-figures-and-decimal-places-ao-round-significant-figures",
          "text": "Round numbers to given significant figures."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-approximation-significant-figures-and-decimal-places-po03",
        "source_performance_objective_index": 3,
        "text": "Round numbers to given decimal places"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "significant-figures-and-decimal-places-ao-round-decimal-places",
          "text": "Round numbers to given decimal places."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch01-b017",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Place value in decimal fractions"
    },
    "content_text": "For decimal fractions, the place values we work with are $\\frac{1}{10}, \\frac{1}{100}, \\frac{1}{1,000}$ and $\\frac{1}{10,000}$. They are called **tenths**, **hundredths**, **thousandths** and **ten thousandths**.\n\nThese place values are represented from biggest to smallest, moving to the right after the decimal point:\n\n$$\n\\begin{array}{|c|c|c|c|c|c|}\n  \\hline\n    \\text{units} & \\text{.} & \\text{tenths} & \\text{hundredths} & \\text{thousandths} & \\text{ten thousandths} \\\\\n    (1) & \\text{.} & \\left( \\frac{1}{10} \\right) & \\left( \\frac{1}{100} \\right) & \\left( \\frac{1}{1,000} \\right) & \\left( \\frac{1}{10,000} \\right) \\\\\n    \\text{u} & \\text{.} & \\text{t} & \\text{h} & \\text{th} & \\text{tth} \\\\\n    \\hline\n    \\end{array}\n$$\n\nThe fractions for these place values are written in this way:\n\n- 0.1 means zero units and one $\\frac{1}{10}$\n- 0.01 means zero units, zero tenths and one $\\frac{1}{100}$\n- 0.001 means zero units, zero tenths, zero hundredths and one $\\frac{1}{1,000}$\n- 0.0001 means zero units, zero tenths, zero hundredths, zero thousandths and one $\\frac{1}{10,000}$.\n\nAs for whole numbers, we move to a new place value each time we reach 10. For example, this block of squares is divided into 100 parts.\n\nOne hundredth, which is $\\frac{1}{100}$, may be shown like this:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-01-001.png)\n\nFour parts of this block of 100 squares, which is $4\\times \\frac{1}{100}= \\frac{4}{100}$, may be shown like this:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-01-002.png)\n\nTen parts of $\\frac{1}{100}$, in other words, $10\\times\\frac{1}{100}$, may be shown like this:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-01-003.png)\n\nThere are 10 vertical columns in the block of squares. If 1 column out of 10 is shown in colour, we can write this as $\\frac{1}{10}$. Therefore, 10 parts of $\\frac{1}{100}$ is the same as $\\frac{1}{10}$.\n\nSimilarly:\n\n- 10 parts of $\\frac{1}{1,000}$ is the same as $\\frac{1}{100}$\n- 10 parts of $\\frac{1}{10,000}$ is the same as $\\frac{1}{1,000}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-decimals-and-vice-versa"
  },
  {
    "record_id": "ch01-b018",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Place value in decimal fractions"
    },
    "content_text": "**tenths** Tenths are the decimal fractions 0.1; 0.2; 0.3; 0.4; 0.5; 0.6; 0.7; 0.8; 0.9 in the base ten number system.\n\n**hundredths** Hundredths are the decimal fractions 0.01; 0.02; 0.03; 0.04; 0.05; 0.06; 0.07; 0.08; 0.09 in the base ten number system.\n\n**thousandths** Thousandths are the decimal fractions 0.001; 0.002; 0.003; 0.004; 0.005; 0.006; 0.007; 0.008; 0.009 in the base ten number system.\n\n**ten thousandths** Ten thousandths are the decimal fractions 0.0001; 0.0002; 0.0003; 0.0004; 0.0005; 0.0006; 0.0007; 0.0008; 0.0009 in the base ten number system.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-decimals-and-vice-versa"
  },
  {
    "record_id": "ch01-b019",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Worked example 1.2: Finding place value in decimal numbers"
    },
    "content_text": "",
    "prompt_text": "Write down the place values of all the non-zero digits in the following number: 73,025.048",
    "answer_text": "Step 1: Write the number in a place value table. Show the decimal point clearly in your table.\n\n$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|}\n \\hline\n \\text{tth} & \\text{th} & \\text{h} & \\text{t} & \\text{u} & \\text{.} & \\text{t} & \\text{h} & \\text{th} & \\text{tth} \\\\\n (10,000) & (1,000) & (100) & (10) & (1) & \\text{.} & (0.1) & (0.01) & (0.001) & (0.0001) \\\\\n \\hline\n 7 & 3 & 0 & 2 & 5 & . & 0 & 4 & 8 \\\\\n \\hline\n \\end{array}\n$$\n\nStep 2: Multiply each non-zero digit by the value of the column it is in.\n\n$7\\times10,000=70,000$\\\n$3\\times1,000=3,000$\\\n$2\\times10=20$\\\n$5\\times1=5$\\\n$4\\times 0.01=0.04$\\\n$8\\times 0.001=0.008$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch01-b020",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Place value in decimal fractions"
    },
    "content_text": "As you can see, we do not give the place value of the zeroes in a number, because 0 multiplied by anything equals 0. So the place value of any 0 will always be 0. The zeroes have to be included in a number to show the place values of the other digits. This is why we call 0 a placeholder.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-decimals-and-vice-versa"
  },
  {
    "record_id": "ch01-b021",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Exercise 1.3: Determine place value in numbers with decimal fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.3: Determine place value in numbers with decimal fractions\n\nWrite down the place value of the given digit in each case.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch01-b021-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Exercise 1.3: Determine place value in numbers with decimal fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.3: Determine place value in numbers with decimal fractions\n\nWrite down the place value of the given digit in each case.\n\n1. Give the values of the digits 5 and 8 in the number 5,023.08",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|}\n\\hline\n\\text{tth} & \\text{th} & \\text{h} & \\text{t} & \\text{u} & \\text{.} & \\text{t} & \\text{h} & \\text{th} & \\text{tth} \\\\\n(10,000) & (1,000) & (100) & (10) & (1) & \\text{.} & (0.1) & (0.01) & (0.001) & (0.0001) \\\\\n\\hline\n & 5 & 0 & 2 & 3 & . & 0 & 8 &  \\\\\n\\hline\n\\end{array}\n$$\n\nThe place values are:\n$5\\times1,000=5,000$\\\n$8\\times 0.01=0.08$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch01-b021-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Exercise 1.3: Determine place value in numbers with decimal fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.3: Determine place value in numbers with decimal fractions\n\nWrite down the place value of the given digit in each case.\n\n2. Give the values of the digits 1 and 4 in the number 75.1804",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|}\n\\hline\n\\text{tth} & \\text{th} & \\text{h} & \\text{t} & \\text{u} & \\text{.} & \\text{t} & \\text{h} & \\text{th} & \\text{tth} \\\\\n(10,000) & (1,000) & (100) & (10) & (1) & \\text{.} & (0.1) & (0.01) & (0.001) & (0.0001) \\\\\n\\hline\n &  &  & 7 & 5 & . & 1 & 8 & 0 & 4 \\\\\n\\hline\n\\end{array}\n$$\n\nThe place values are:\n$1\\times0.1=0.4$\\\n$4\\times 0.0001=0.0004$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch01-b021-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Exercise 1.3: Determine place value in numbers with decimal fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.3: Determine place value in numbers with decimal fractions\n\nWrite down the place value of the given digit in each case.\n\n3. Give the values of the digits 9 and 7 in the number 70,546.009",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|}\n\\hline\n\\text{tth} & \\text{th} & \\text{h} & \\text{t} & \\text{u} & \\text{.} & \\text{t} & \\text{h} & \\text{th} & \\text{tth} \\\\\n(10,000) & (1,000) & (100) & (10) & (1) & \\text{.} & (0.1) & (0.01) & (0.001) & (0.0001) \\\\\n\\hline\n 7 & 0 & 5 & 4 & 6 & . & 0 & 0 & 9 &   \\\\\n\\hline\n\\end{array}\n$$\n\nThe place values are:\n$7\\times10,000=70,000$\\\n$9\\times 0.001=0.009$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch01-b021-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Exercise 1.3: Determine place value in numbers with decimal fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.3: Determine place value in numbers with decimal fractions\n\nWrite down the place value of the given digit in each case.\n\n4. Give the two values of the digit 5 in the number 10,503.54",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|}\n\\hline\n\\text{tth} & \\text{th} & \\text{h} & \\text{t} & \\text{u} & \\text{.} & \\text{t} & \\text{h} & \\text{th} & \\text{tth} \\\\\n(10,000) & (1,000) & (100) & (10) & (1) & \\text{.} & (0.1) & (0.01) & (0.001) & (0.0001) \\\\\n\\hline\n 1 & 0 & 5 & 0 & 3 & . & 5 & 4 &  &   \\\\\n\\hline\n\\end{array}\n$$\n\nThe two place values are:\n$5\\times100=500$\\\n$5\\times 0.1=0.5$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch01-b021-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Exercise 1.3: Determine place value in numbers with decimal fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.3: Determine place value in numbers with decimal fractions\n\nWrite down the place value of the given digit in each case.\n\n5. Give the three values of the digit 9 in the number 99,148.319",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|}\n\\hline\n\\text{tth} & \\text{th} & \\text{h} & \\text{t} & \\text{u} & \\text{.} & \\text{t} & \\text{h} & \\text{th} & \\text{tth} \\\\\n(10,000) & (1,000) & (100) & (10) & (1) & \\text{.} & (0.1) & (0.01) & (0.001) & (0.0001) \\\\\n\\hline\n 9 & 9 & 1 & 4 & 8 & . & 3 & 1 & 9 &   \\\\\n\\hline\n\\end{array}\n$$\n\nThe three place values are:\n$9\\times10,000=90,000$\\\n$9\\times1,000=9,000$\\\n$9\\times 0.001=0.009$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
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
  "topic_key": "jss1-math-approximation",
  "topic": "Approximation",
  "subtopic_id": "jss1-math-approximation-significant-figures-and-decimal-places",
  "subtopic_title": "Significant figures and decimal places",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-approximation-significant-figures-and-decimal-places-po01",
        "source_performance_objective_index": 1,
        "text": "Determine the degree of accuracy of numbers"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "significant-figures-and-decimal-places-ao-determine-degree-of-accuracy",
          "text": "Determine the degree of accuracy of numbers."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-approximation-significant-figures-and-decimal-places-po02",
        "source_performance_objective_index": 2,
        "text": "Round numbers to given significant figures"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "significant-figures-and-decimal-places-ao-round-significant-figures",
          "text": "Round numbers to given significant figures."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-approximation-significant-figures-and-decimal-places-po03",
        "source_performance_objective_index": 3,
        "text": "Round numbers to given decimal places"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "significant-figures-and-decimal-places-ao-round-decimal-places",
          "text": "Round numbers to given decimal places."
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
    "record_id": "ch01-b017",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Place value in decimal fractions"
    },
    "content_text": "For decimal fractions, the place values we work with are $\\frac{1}{10}, \\frac{1}{100}, \\frac{1}{1,000}$ and $\\frac{1}{10,000}$. They are called **tenths**, **hundredths**, **thousandths** and **ten thousandths**.\n\nThese place values are represented from biggest to smallest, moving to the right after the decimal point:\n\n$$\n\\begin{array}{|c|c|c|c|c|c|}\n  \\hline\n    \\text{units} & \\text{.} & \\text{tenths} & \\text{hundredths} & \\text{thousandths} & \\text{ten thousandths} \\\\\n    (1) & \\text{.} & \\left( \\frac{1}{10} \\right) & \\left( \\frac{1}{100} \\right) & \\left( \\frac{1}{1,000} \\right) & \\left( \\frac{1}{10,000} \\right) \\\\\n    \\text{u} & \\text{.} & \\text{t} & \\text{h} & \\text{th} & \\text{tth} \\\\\n    \\hline\n    \\end{array}\n$$\n\nThe fractions for these place values are written in this way:\n\n- 0.1 means zero units and one $\\frac{1}{10}$\n- 0.01 means zero units, zero tenths and one $\\frac{1}{100}$\n- 0.001 means zero units, zero tenths, zero hundredths and one $\\frac{1}{1,000}$\n- 0.0001 means zero units, zero tenths, zero hundredths, zero thousandths and one $\\frac{1}{10,000}$.\n\nAs for whole numbers, we move to a new place value each time we reach 10. For example, this block of squares is divided into 100 parts.\n\nOne hundredth, which is $\\frac{1}{100}$, may be shown like this:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-01-001.png)\n\nFour parts of this block of 100 squares, which is $4\\times \\frac{1}{100}= \\frac{4}{100}$, may be shown like this:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-01-002.png)\n\nTen parts of $\\frac{1}{100}$, in other words, $10\\times\\frac{1}{100}$, may be shown like this:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-01-003.png)\n\nThere are 10 vertical columns in the block of squares. If 1 column out of 10 is shown in colour, we can write this as $\\frac{1}{10}$. Therefore, 10 parts of $\\frac{1}{100}$ is the same as $\\frac{1}{10}$.\n\nSimilarly:\n\n- 10 parts of $\\frac{1}{1,000}$ is the same as $\\frac{1}{100}$\n- 10 parts of $\\frac{1}{10,000}$ is the same as $\\frac{1}{1,000}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-decimals-and-vice-versa"
  },
  {
    "record_id": "ch01-b018",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Place value in decimal fractions"
    },
    "content_text": "**tenths** Tenths are the decimal fractions 0.1; 0.2; 0.3; 0.4; 0.5; 0.6; 0.7; 0.8; 0.9 in the base ten number system.\n\n**hundredths** Hundredths are the decimal fractions 0.01; 0.02; 0.03; 0.04; 0.05; 0.06; 0.07; 0.08; 0.09 in the base ten number system.\n\n**thousandths** Thousandths are the decimal fractions 0.001; 0.002; 0.003; 0.004; 0.005; 0.006; 0.007; 0.008; 0.009 in the base ten number system.\n\n**ten thousandths** Ten thousandths are the decimal fractions 0.0001; 0.0002; 0.0003; 0.0004; 0.0005; 0.0006; 0.0007; 0.0008; 0.0009 in the base ten number system.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-decimals-and-vice-versa"
  },
  {
    "record_id": "ch01-b019",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Worked example 1.2: Finding place value in decimal numbers"
    },
    "content_text": "",
    "prompt_text": "Write down the place values of all the non-zero digits in the following number: 73,025.048",
    "answer_text": "Step 1: Write the number in a place value table. Show the decimal point clearly in your table.\n\n$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|}\n \\hline\n \\text{tth} & \\text{th} & \\text{h} & \\text{t} & \\text{u} & \\text{.} & \\text{t} & \\text{h} & \\text{th} & \\text{tth} \\\\\n (10,000) & (1,000) & (100) & (10) & (1) & \\text{.} & (0.1) & (0.01) & (0.001) & (0.0001) \\\\\n \\hline\n 7 & 3 & 0 & 2 & 5 & . & 0 & 4 & 8 \\\\\n \\hline\n \\end{array}\n$$\n\nStep 2: Multiply each non-zero digit by the value of the column it is in.\n\n$7\\times10,000=70,000$\\\n$3\\times1,000=3,000$\\\n$2\\times10=20$\\\n$5\\times1=5$\\\n$4\\times 0.01=0.04$\\\n$8\\times 0.001=0.008$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch01-b020",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Place value in decimal fractions"
    },
    "content_text": "As you can see, we do not give the place value of the zeroes in a number, because 0 multiplied by anything equals 0. So the place value of any 0 will always be 0. The zeroes have to be included in a number to show the place values of the other digits. This is why we call 0 a placeholder.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-conversion-of-fractions-to-decimals-and-vice-versa"
  },
  {
    "record_id": "ch01-b021",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Exercise 1.3: Determine place value in numbers with decimal fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.3: Determine place value in numbers with decimal fractions\n\nWrite down the place value of the given digit in each case.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch01-b021-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Exercise 1.3: Determine place value in numbers with decimal fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.3: Determine place value in numbers with decimal fractions\n\nWrite down the place value of the given digit in each case.\n\n1. Give the values of the digits 5 and 8 in the number 5,023.08",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|}\n\\hline\n\\text{tth} & \\text{th} & \\text{h} & \\text{t} & \\text{u} & \\text{.} & \\text{t} & \\text{h} & \\text{th} & \\text{tth} \\\\\n(10,000) & (1,000) & (100) & (10) & (1) & \\text{.} & (0.1) & (0.01) & (0.001) & (0.0001) \\\\\n\\hline\n & 5 & 0 & 2 & 3 & . & 0 & 8 &  \\\\\n\\hline\n\\end{array}\n$$\n\nThe place values are:\n$5\\times1,000=5,000$\\\n$8\\times 0.01=0.08$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch01-b021-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Exercise 1.3: Determine place value in numbers with decimal fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.3: Determine place value in numbers with decimal fractions\n\nWrite down the place value of the given digit in each case.\n\n2. Give the values of the digits 1 and 4 in the number 75.1804",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|}\n\\hline\n\\text{tth} & \\text{th} & \\text{h} & \\text{t} & \\text{u} & \\text{.} & \\text{t} & \\text{h} & \\text{th} & \\text{tth} \\\\\n(10,000) & (1,000) & (100) & (10) & (1) & \\text{.} & (0.1) & (0.01) & (0.001) & (0.0001) \\\\\n\\hline\n &  &  & 7 & 5 & . & 1 & 8 & 0 & 4 \\\\\n\\hline\n\\end{array}\n$$\n\nThe place values are:\n$1\\times0.1=0.4$\\\n$4\\times 0.0001=0.0004$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch01-b021-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Exercise 1.3: Determine place value in numbers with decimal fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.3: Determine place value in numbers with decimal fractions\n\nWrite down the place value of the given digit in each case.\n\n3. Give the values of the digits 9 and 7 in the number 70,546.009",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|}\n\\hline\n\\text{tth} & \\text{th} & \\text{h} & \\text{t} & \\text{u} & \\text{.} & \\text{t} & \\text{h} & \\text{th} & \\text{tth} \\\\\n(10,000) & (1,000) & (100) & (10) & (1) & \\text{.} & (0.1) & (0.01) & (0.001) & (0.0001) \\\\\n\\hline\n 7 & 0 & 5 & 4 & 6 & . & 0 & 0 & 9 &   \\\\\n\\hline\n\\end{array}\n$$\n\nThe place values are:\n$7\\times10,000=70,000$\\\n$9\\times 0.001=0.009$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch01-b021-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Exercise 1.3: Determine place value in numbers with decimal fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.3: Determine place value in numbers with decimal fractions\n\nWrite down the place value of the given digit in each case.\n\n4. Give the two values of the digit 5 in the number 10,503.54",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|}\n\\hline\n\\text{tth} & \\text{th} & \\text{h} & \\text{t} & \\text{u} & \\text{.} & \\text{t} & \\text{h} & \\text{th} & \\text{tth} \\\\\n(10,000) & (1,000) & (100) & (10) & (1) & \\text{.} & (0.1) & (0.01) & (0.001) & (0.0001) \\\\\n\\hline\n 1 & 0 & 5 & 0 & 3 & . & 5 & 4 &  &   \\\\\n\\hline\n\\end{array}\n$$\n\nThe two place values are:\n$5\\times100=500$\\\n$5\\times 0.1=0.5$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch01-b021-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Exercise 1.3: Determine place value in numbers with decimal fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.3: Determine place value in numbers with decimal fractions\n\nWrite down the place value of the given digit in each case.\n\n5. Give the three values of the digit 9 in the number 99,148.319",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|}\n\\hline\n\\text{tth} & \\text{th} & \\text{h} & \\text{t} & \\text{u} & \\text{.} & \\text{t} & \\text{h} & \\text{th} & \\text{tth} \\\\\n(10,000) & (1,000) & (100) & (10) & (1) & \\text{.} & (0.1) & (0.01) & (0.001) & (0.0001) \\\\\n\\hline\n 9 & 9 & 1 & 4 & 8 & . & 3 & 1 & 9 &   \\\\\n\\hline\n\\end{array}\n$$\n\nThe three place values are:\n$9\\times10,000=90,000$\\\n$9\\times1,000=9,000$\\\n$9\\times 0.001=0.009$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
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
