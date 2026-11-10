# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-1",
  "topic_key": "jss1-math-whole-numbers",
  "topic": "Whole Numbers",
  "subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning",
  "subtopic_title": "Quantitative reasoning",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-whole-numbers-quantitative-reasoning-po01",
        "source_performance_objective_index": 1,
        "text": "Solve problems in quantitative aptitude reasoning using large numbers"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "quantitative-reasoning-ao-solve-large-number-problems",
          "text": "Solve problems in quantitative aptitude reasoning using large numbers."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch01-b043",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.5 Counting in big numbers",
      "h3": "Worked example 1.6: Comparing large numbers"
    },
    "content_text": "",
    "prompt_text": "Arrange the following numbers from the smallest to the largest:\n50.5 billion; 0.055 trillion; 500.5 million",
    "answer_text": "Step 1: Write all the numbers as digits only.\n\n50.5 billion without the decimal point: $505\\times1,000,000,000=505,000,000,000$\nWith the decimal point: 50500000000.0\nCorrectly grouped: 50,500,000,000\n\n0.055 trillion without the decimal point: $0.055\\times1,000,000,000,000=55,000,000,000,000$\nWith the decimal point: 55000000000.000\nCorrectly grouped: 55,000,000,000\n\n500.5 million without the decimal point: $5,005\\times1,000,000=5,005,000,000$\nWith the decimal point: 500500000.0\nCorrectly grouped: 500,500,000\n\nStep 2: Write the numbers one below the other. Align them on the last digit.\n\n$$\n\\begin{array}{r}\n 50,500,000,000 \\\\\n 55,000,000,000 \\\\\n 500,500,000 \\\\\n \\end{array}\n$$\n\nStep 3: Use the list from Step 2 to write the numbers in the required order.\n\nFrom Step 2 is is easy to compare the numbers. Arranged from small to large:\n\n$$\n\\begin{array}{r}\n 500,500,000 \\\\\n 50,500,000,000 \\\\\n 55,000,000,000 \\\\\n \\end{array}\n$$\n\nTherefore, the numbers arranged from smallest to largest are 500.5 million; 50.5 billion; 0.055 trillion.",
    "primary_subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning"
  },
  {
    "record_id": "ch01-b044",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.5 Counting in big numbers",
      "h3": "Exercise 1.11: Compare large numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.11: Compare large numbers",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning"
  },
  {
    "record_id": "ch01-b044-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.5 Counting in big numbers",
      "h3": "Exercise 1.11: Compare large numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.11: Compare large numbers\n\n1. Which number is larger, 0.08 trillion or 800 billion?",
    "answer_text": "0.08 trillion without the decimal point: $8\\times1,000,000,000,000=8,000,000,000,000$\nWith the decimal point: 80000000000.00\nCorrectly grouped: 80,000,000,000\nThis is 80 billion.\n\nTherefore, 800 billion is the larger number.",
    "primary_subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning"
  },
  {
    "record_id": "ch01-b044-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.5 Counting in big numbers",
      "h3": "Exercise 1.11: Compare large numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.11: Compare large numbers\n\n2. Which number is smaller, 120 billion or 1.2 trillion?",
    "answer_text": "1.2 trillion without the decimal point: $12\\times1,000,000,000,000=12,000,000,000,000$\nWith the decimal point: 1200000000000.0\nCorrectly grouped: 1,200,000,000,000\n\n120 billion: $120\\times1,000,000,000=120,000,000,000$\n\nCompare the numbers:\n\n$$\n\\begin{array}{r}\n1,200,000,000,000 \\\\\n120,000,000,000 \\\\\n\\end{array}\n$$\n\nTherefore, 120 billion is the smaller number.",
    "primary_subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning"
  },
  {
    "record_id": "ch01-b044-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.5 Counting in big numbers",
      "h3": "Exercise 1.11: Compare large numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.11: Compare large numbers\n\n3. Arrange the following numbers from the largest to the smallest: 3,600 million; 3 billion; 0.36 trillion.",
    "answer_text": "3,600 million: $3,600\\times1,000,000=3,600,000,000$\n\n3 billion: $3\\times1,000,000,000=3,000,000,000$\n\n0.36 trillion without the decimal point: $36\\times1,000,000,000,000=36,000,000,000,000$\nWith the decimal point: 360000000000.00\nCorrectly grouped: 360,000,000,000\n\nCompare the numbers:\n\n$$\n\\begin{array}{r}\n3,600,000,000 \\\\\n3,000,000,000 \\\\\n360,000,000,000 \\\\\n\\end{array}\n$$\n\nTherefore, the numbers from the largest to the smallest are 0.36 trillion; 3,600 million; 3 billion.",
    "primary_subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning"
  },
  {
    "record_id": "ch01-b047",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.6 Using large numbers in everyday life",
      "h3": "Exercise 1.13: Use large numbers to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.13: Use large numbers to solve problems",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning"
  },
  {
    "record_id": "ch01-b047-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.6 Using large numbers in everyday life",
      "h3": "Exercise 1.13: Use large numbers to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.13: Use large numbers to solve problems\n\n1. Scientists estimate that the average child has $10^5$ hairs on her head.\n\na. Write out the full number in digits.\n\nb. Give the name of this number.",
    "answer_text": "a. \n\n$$\n10^5=10\\times10\\times10\\times10\\times10=100,000\n$$\n\nb. One hundred thousand",
    "primary_subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning"
  },
  {
    "record_id": "ch01-b047-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.6 Using large numbers in everyday life",
      "h3": "Exercise 1.13: Use large numbers to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.13: Use large numbers to solve problems\n\n2. During May 2019, Nigeria's population was recorded as 200,233,151.\n\na. Write the number in words.\n\nb. It is estimated that the population will almost double by 2050 to 400,400,000. Write this as a mixture of digits and words, so that it will be easier to read.",
    "answer_text": "a. Two hundred million two hundred and thirty three thousand one hundred and fifty one\n\nb. Use a place value table to help you.\n\n$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|c|c|c|}\n\\hline\n\\text{trillion} &\\text{hb} &\\text{tb} &\\text{billion} & \\text{hm} & \\text{tm} & \\text{million} &\\text{hth} & \\text{tth} & \\text{thousand} & \\text{ h } & \\text{ t } & \\text{ u }  \\\\\n\\hline\n &  &  &  & 4 & 0 & 0 & 4 & 0 & 0 & 0 & 0 & 0  \\\\\n\\hline\n\\end{array}\n$$\n\nThe number can be written as 400.4 million.",
    "primary_subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning"
  },
  {
    "record_id": "ch01-b047-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.6 Using large numbers in everyday life",
      "h3": "Exercise 1.13: Use large numbers to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.13: Use large numbers to solve problems\n\n3. In 2018, the Federal Government of Nigeria estimated a total revenue of ₦6,607,000,000,000.\n\na. Write the number as a mixture of digits and words, so that it will be easier for the general public to read.\n\nb. It was estimated that oil revenue would be ₦2.442 trillion of the total revenue and non-oil revenue would be ₦4,165,000,000,000. Determine which revenue is more, the oil revenue or the non-oil revenue.",
    "answer_text": "a. Use a place value table to help you.\n\n$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|c|c|c|}\n\\hline\n\\text{trillion} &\\text{hb} &\\text{tb} &\\text{billion} & \\text{hm} & \\text{tm} & \\text{million} &\\text{hth} & \\text{tth} & \\text{thousand} & \\text{ h } & \\text{ t } & \\text{ u }  \\\\\n\\hline\n6 & 6 & 0 & 7 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0  \\\\\n\\hline\n\\end{array}\n$$\n\nThe number can be written as ₦6.607 trillion.\n\nb. $2.442\\times1,000,000,000,000=2,442,000,000,000$\n\n$$\n\\begin{array}{l r}\n\\text{Oil:} & ₦2,442,000,000,000 \\\\\n\\text{Non-oil:} & ₦4,165,000,000,000 \\\\\n\\end{array}\n$$\n\nThe non-oil revenue is more.",
    "primary_subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning"
  },
  {
    "record_id": "ch01-b047-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.6 Using large numbers in everyday life",
      "h3": "Exercise 1.13: Use large numbers to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.13: Use large numbers to solve problems\n\n4. The side length of a cube is 1 m.\n\na. Convert the side length to centimetres. Then determine the volume of the cube in cubic centimetres. Write the answer in words.\n\nb. Convert the side length to millimetres. Then determine the volume of the cube in cubic millimetres. Write the answer in words.",
    "answer_text": "a. 1 m = 100 cm\n\n$$\n\\begin{array}{l l}\n\\text{volume} &=\\text{side}\\times\\text{side}\\times\\text{side} \\\\\n&=100\\times100\\times100\\\\\n&=1,000,000\\text{ cm}^3\n\\end{array}\n$$\n\nThe volume is one million cubic centimetres.\n\nb. 1 m = 1,000 mm\n\n$$\n\\begin{array}{l l}\n\\text{volume} &=\\text{side}\\times\\text{side}\\times\\text{side} \\\\\n&=1,000\\times1,000\\times1,000\\\\\n&=1,000,000,000\\text{ mm}^3\n\\end{array}\n$$\n\nThe volume is one billion cubic millimetres.",
    "primary_subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning"
  },
  {
    "record_id": "ch01-b047-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.6 Using large numbers in everyday life",
      "h3": "Exercise 1.13: Use large numbers to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.13: Use large numbers to solve problems\n\n5. There are 31,536,000 seconds in one year.\n\na. Calculate the number of seconds in ten years. Write the answer in words.\n\nb. Determine whether your previous answer is more or less than 0.3 billion.",
    "answer_text": "a. $31,536,000\\times10=315,360,000$\n\nThere are three hundred and fifteen million three hundred and sixty thousand seconds in ten years.\n\nb. $0.3\\times1,000,000,000=300,000,000$\n\nThe previous answer is more than 0.3 billion.",
    "primary_subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning"
  },
  {
    "record_id": "ch01-b047-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.6 Using large numbers in everyday life",
      "h3": "Exercise 1.13: Use large numbers to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.13: Use large numbers to solve problems\n\n6. In 2018, the Federal Government of Nigeria estimated the following budget allocations to three of their ministries: ₦435.01 billion to Education, ₦444.43 billion to Defence and ₦269.34 billion to Health. Calculate the total allocation to all three ministries. Write the full number and give its name.",
    "answer_text": "$$\n\\begin{array}{r r r}\n & 435.01\\times1,000,000,000 & = 435,010,000,000 \\\\\n +& 444.43\\times1,000,000,000 & = 444,430,000,000 \\\\\n+& 269.34\\times1,000,000,000 & = 269,340,000,000 \\\\\n\\hline\n& &  1,148,780,000,000\\\\\n\\hline\n\\end{array}\n$$\n\nThe total allocation is ₦1,148,780,000,000. It is one trillion one hundred and forty eight billion seven hundred and eighty million naira.",
    "primary_subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning"
  },
  {
    "record_id": "ch01-b048",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.7 Summary",
      "h3": null
    },
    "content_text": "- In the base ten number system, we use the digits 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 to represent any other number.\n- The numbers 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 are called units in the base ten number system.\n- The numbers 10; 20; 30; 40; 50; 60; 70; 80; 90 are called tens in the base ten number system.\n- The numbers 100; 200; 300; 400; 500; 600; 700; 800; 900 are called hundreds in the base ten number system.\n- The numbers 1,000; 2,000; 3,000; 4,000; 5,000; 6,000; 7,000; 8,000; 9,000 are called thousands in the base ten number system.\n- The numbers 10,000; 20,000; 30,000; 40,000; 50,000; 60,000; 70,000; 80,000; 90,000 are called ten thousands in the base ten number system.\n- Decimal fractions are written using the base ten number system. The digits of the numerator are written after a decimal point. The denominator is 10; 100; 1,000; 10,000 and so on. For example, the decimal fraction 0.25 is equal to $\\frac{25}{100}$.\n- We use commas to group the digits in large numbers in threes, so that they are easier to read. We group the digits from the decimal point, going to the left. For example, 4589762.35 is written as 4,589,762.35.\n- The place value of a digit is the value of that digit according to its position in the number.\n- We may use powers of ten to express large numbers. The power tells us how many times 10 must be multiplied by itself. For example, $10^4$ means $10\\times10\\times10\\times10$. Here is a list of the powers of ten.\n\n$$\n\\begin{array}{|l|l|l|}\n  \\hline\n  \\textbf{Name} & \\textbf{Number} & \\textbf{Powers of ten}  \\\\\n  \\hline\n   \\text{Ten} & 10 & 10=10^1    \\\\\n  \\hline\n   \\text{Hundred} & 100 & 10\\times10=10^2    \\\\\n  \\hline\n  \\text{Thousand} & 1,000 & 10\\times10\\times10=10^3    \\\\\n  \\hline\n  \\text{Ten thousand} & 10,000 & 10\\times10\\times10\\times10=10^4    \\\\\n  \\hline\n  \\text{Hundred thousand} & 100,000 & 10\\times10\\times10\\times10\\times10=10^5    \\\\\n  \\hline\n  \\text{Million} & 1,000,000 & 10\\times10\\times10\\times10\\times10\\times10=10^6    \\\\\n  \\hline\n  \\text{Ten million} & 10,000,000 & 10\\times10\\times10\\times10\\times10\\times10\\times10=10^7 \\\\\n  \\hline\n  \\text{Hundred million} & 100,000,000 & 10\\times10\\times10\\times10\\times10\\times10\\times10\\times10=10^8 \\\\\n  \\hline\n  \\text{Billion} & 1,000,000,000 & 10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10=10^9 \\\\\n  \\hline\n  \\text{Ten billion} & 10,000,000,000 & 10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10=10^{10} \\\\\n  \\hline\n  \\text{Hundred billion} & 100,000,000,000 & 10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10=10^{11} \\\\\n  \\hline\n  \\text{Trillion} & 1,000,000,000,000 & 10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10=10^{12} \\\\\n  \\hline\n   \\end{array}\n$$\n\n- We can use the above list to draw up a place value table. This makes it easer to work with large numbers.\n\n$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|c|c|c|}\n  \\hline\n  \\text{trillion} &\\text{hb} &\\text{tb} &\\text{billion} & \\text{hm} & \\text{tm} & \\text{million} &\\text{hth} & \\text{tth} & \\text{thousand} & \\text{ h } & \\text{ t } & \\text{ u }  \\\\\n  \\hline\n   &  &  &  &  &  &  &  &  &  &  &  &   \\\\\n  \\hline\n  \\end{array}\n$$\n\n- We may use a place value table to help us count with large numbers. Whenever we want to proceed after we reached the digit 9 in any column of the table, the 9 becomes 0 and the digit in the column to the left increases by 1.\n- Large numbers are sometimes expressed as a mixture of digits and words to make them easier to read. For example, 0.5 billion is the number 500,000,000 with the name five hundred million.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
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
  "topic_key": "jss1-math-whole-numbers",
  "topic": "Whole Numbers",
  "subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning",
  "subtopic_title": "Quantitative reasoning",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-whole-numbers-quantitative-reasoning-po01",
        "source_performance_objective_index": 1,
        "text": "Solve problems in quantitative aptitude reasoning using large numbers"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "quantitative-reasoning-ao-solve-large-number-problems",
          "text": "Solve problems in quantitative aptitude reasoning using large numbers."
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
    "record_id": "ch01-b043",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.5 Counting in big numbers",
      "h3": "Worked example 1.6: Comparing large numbers"
    },
    "content_text": "",
    "prompt_text": "Arrange the following numbers from the smallest to the largest:\n50.5 billion; 0.055 trillion; 500.5 million",
    "answer_text": "Step 1: Write all the numbers as digits only.\n\n50.5 billion without the decimal point: $505\\times1,000,000,000=505,000,000,000$\nWith the decimal point: 50500000000.0\nCorrectly grouped: 50,500,000,000\n\n0.055 trillion without the decimal point: $0.055\\times1,000,000,000,000=55,000,000,000,000$\nWith the decimal point: 55000000000.000\nCorrectly grouped: 55,000,000,000\n\n500.5 million without the decimal point: $5,005\\times1,000,000=5,005,000,000$\nWith the decimal point: 500500000.0\nCorrectly grouped: 500,500,000\n\nStep 2: Write the numbers one below the other. Align them on the last digit.\n\n$$\n\\begin{array}{r}\n 50,500,000,000 \\\\\n 55,000,000,000 \\\\\n 500,500,000 \\\\\n \\end{array}\n$$\n\nStep 3: Use the list from Step 2 to write the numbers in the required order.\n\nFrom Step 2 is is easy to compare the numbers. Arranged from small to large:\n\n$$\n\\begin{array}{r}\n 500,500,000 \\\\\n 50,500,000,000 \\\\\n 55,000,000,000 \\\\\n \\end{array}\n$$\n\nTherefore, the numbers arranged from smallest to largest are 500.5 million; 50.5 billion; 0.055 trillion.",
    "primary_subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning"
  },
  {
    "record_id": "ch01-b044",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.5 Counting in big numbers",
      "h3": "Exercise 1.11: Compare large numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.11: Compare large numbers",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning"
  },
  {
    "record_id": "ch01-b044-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.5 Counting in big numbers",
      "h3": "Exercise 1.11: Compare large numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.11: Compare large numbers\n\n1. Which number is larger, 0.08 trillion or 800 billion?",
    "answer_text": "0.08 trillion without the decimal point: $8\\times1,000,000,000,000=8,000,000,000,000$\nWith the decimal point: 80000000000.00\nCorrectly grouped: 80,000,000,000\nThis is 80 billion.\n\nTherefore, 800 billion is the larger number.",
    "primary_subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning"
  },
  {
    "record_id": "ch01-b044-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.5 Counting in big numbers",
      "h3": "Exercise 1.11: Compare large numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.11: Compare large numbers\n\n2. Which number is smaller, 120 billion or 1.2 trillion?",
    "answer_text": "1.2 trillion without the decimal point: $12\\times1,000,000,000,000=12,000,000,000,000$\nWith the decimal point: 1200000000000.0\nCorrectly grouped: 1,200,000,000,000\n\n120 billion: $120\\times1,000,000,000=120,000,000,000$\n\nCompare the numbers:\n\n$$\n\\begin{array}{r}\n1,200,000,000,000 \\\\\n120,000,000,000 \\\\\n\\end{array}\n$$\n\nTherefore, 120 billion is the smaller number.",
    "primary_subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning"
  },
  {
    "record_id": "ch01-b044-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.5 Counting in big numbers",
      "h3": "Exercise 1.11: Compare large numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.11: Compare large numbers\n\n3. Arrange the following numbers from the largest to the smallest: 3,600 million; 3 billion; 0.36 trillion.",
    "answer_text": "3,600 million: $3,600\\times1,000,000=3,600,000,000$\n\n3 billion: $3\\times1,000,000,000=3,000,000,000$\n\n0.36 trillion without the decimal point: $36\\times1,000,000,000,000=36,000,000,000,000$\nWith the decimal point: 360000000000.00\nCorrectly grouped: 360,000,000,000\n\nCompare the numbers:\n\n$$\n\\begin{array}{r}\n3,600,000,000 \\\\\n3,000,000,000 \\\\\n360,000,000,000 \\\\\n\\end{array}\n$$\n\nTherefore, the numbers from the largest to the smallest are 0.36 trillion; 3,600 million; 3 billion.",
    "primary_subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning"
  },
  {
    "record_id": "ch01-b047",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.6 Using large numbers in everyday life",
      "h3": "Exercise 1.13: Use large numbers to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.13: Use large numbers to solve problems",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning"
  },
  {
    "record_id": "ch01-b047-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.6 Using large numbers in everyday life",
      "h3": "Exercise 1.13: Use large numbers to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.13: Use large numbers to solve problems\n\n1. Scientists estimate that the average child has $10^5$ hairs on her head.\n\na. Write out the full number in digits.\n\nb. Give the name of this number.",
    "answer_text": "a. \n\n$$\n10^5=10\\times10\\times10\\times10\\times10=100,000\n$$\n\nb. One hundred thousand",
    "primary_subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning"
  },
  {
    "record_id": "ch01-b047-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.6 Using large numbers in everyday life",
      "h3": "Exercise 1.13: Use large numbers to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.13: Use large numbers to solve problems\n\n2. During May 2019, Nigeria's population was recorded as 200,233,151.\n\na. Write the number in words.\n\nb. It is estimated that the population will almost double by 2050 to 400,400,000. Write this as a mixture of digits and words, so that it will be easier to read.",
    "answer_text": "a. Two hundred million two hundred and thirty three thousand one hundred and fifty one\n\nb. Use a place value table to help you.\n\n$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|c|c|c|}\n\\hline\n\\text{trillion} &\\text{hb} &\\text{tb} &\\text{billion} & \\text{hm} & \\text{tm} & \\text{million} &\\text{hth} & \\text{tth} & \\text{thousand} & \\text{ h } & \\text{ t } & \\text{ u }  \\\\\n\\hline\n &  &  &  & 4 & 0 & 0 & 4 & 0 & 0 & 0 & 0 & 0  \\\\\n\\hline\n\\end{array}\n$$\n\nThe number can be written as 400.4 million.",
    "primary_subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning"
  },
  {
    "record_id": "ch01-b047-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.6 Using large numbers in everyday life",
      "h3": "Exercise 1.13: Use large numbers to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.13: Use large numbers to solve problems\n\n3. In 2018, the Federal Government of Nigeria estimated a total revenue of ₦6,607,000,000,000.\n\na. Write the number as a mixture of digits and words, so that it will be easier for the general public to read.\n\nb. It was estimated that oil revenue would be ₦2.442 trillion of the total revenue and non-oil revenue would be ₦4,165,000,000,000. Determine which revenue is more, the oil revenue or the non-oil revenue.",
    "answer_text": "a. Use a place value table to help you.\n\n$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|c|c|c|}\n\\hline\n\\text{trillion} &\\text{hb} &\\text{tb} &\\text{billion} & \\text{hm} & \\text{tm} & \\text{million} &\\text{hth} & \\text{tth} & \\text{thousand} & \\text{ h } & \\text{ t } & \\text{ u }  \\\\\n\\hline\n6 & 6 & 0 & 7 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0  \\\\\n\\hline\n\\end{array}\n$$\n\nThe number can be written as ₦6.607 trillion.\n\nb. $2.442\\times1,000,000,000,000=2,442,000,000,000$\n\n$$\n\\begin{array}{l r}\n\\text{Oil:} & ₦2,442,000,000,000 \\\\\n\\text{Non-oil:} & ₦4,165,000,000,000 \\\\\n\\end{array}\n$$\n\nThe non-oil revenue is more.",
    "primary_subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning"
  },
  {
    "record_id": "ch01-b047-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.6 Using large numbers in everyday life",
      "h3": "Exercise 1.13: Use large numbers to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.13: Use large numbers to solve problems\n\n4. The side length of a cube is 1 m.\n\na. Convert the side length to centimetres. Then determine the volume of the cube in cubic centimetres. Write the answer in words.\n\nb. Convert the side length to millimetres. Then determine the volume of the cube in cubic millimetres. Write the answer in words.",
    "answer_text": "a. 1 m = 100 cm\n\n$$\n\\begin{array}{l l}\n\\text{volume} &=\\text{side}\\times\\text{side}\\times\\text{side} \\\\\n&=100\\times100\\times100\\\\\n&=1,000,000\\text{ cm}^3\n\\end{array}\n$$\n\nThe volume is one million cubic centimetres.\n\nb. 1 m = 1,000 mm\n\n$$\n\\begin{array}{l l}\n\\text{volume} &=\\text{side}\\times\\text{side}\\times\\text{side} \\\\\n&=1,000\\times1,000\\times1,000\\\\\n&=1,000,000,000\\text{ mm}^3\n\\end{array}\n$$\n\nThe volume is one billion cubic millimetres.",
    "primary_subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning"
  },
  {
    "record_id": "ch01-b047-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.6 Using large numbers in everyday life",
      "h3": "Exercise 1.13: Use large numbers to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.13: Use large numbers to solve problems\n\n5. There are 31,536,000 seconds in one year.\n\na. Calculate the number of seconds in ten years. Write the answer in words.\n\nb. Determine whether your previous answer is more or less than 0.3 billion.",
    "answer_text": "a. $31,536,000\\times10=315,360,000$\n\nThere are three hundred and fifteen million three hundred and sixty thousand seconds in ten years.\n\nb. $0.3\\times1,000,000,000=300,000,000$\n\nThe previous answer is more than 0.3 billion.",
    "primary_subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning"
  },
  {
    "record_id": "ch01-b047-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.6 Using large numbers in everyday life",
      "h3": "Exercise 1.13: Use large numbers to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.13: Use large numbers to solve problems\n\n6. In 2018, the Federal Government of Nigeria estimated the following budget allocations to three of their ministries: ₦435.01 billion to Education, ₦444.43 billion to Defence and ₦269.34 billion to Health. Calculate the total allocation to all three ministries. Write the full number and give its name.",
    "answer_text": "$$\n\\begin{array}{r r r}\n & 435.01\\times1,000,000,000 & = 435,010,000,000 \\\\\n +& 444.43\\times1,000,000,000 & = 444,430,000,000 \\\\\n+& 269.34\\times1,000,000,000 & = 269,340,000,000 \\\\\n\\hline\n& &  1,148,780,000,000\\\\\n\\hline\n\\end{array}\n$$\n\nThe total allocation is ₦1,148,780,000,000. It is one trillion one hundred and forty eight billion seven hundred and eighty million naira.",
    "primary_subtopic_id": "jss1-math-whole-numbers-quantitative-reasoning"
  },
  {
    "record_id": "ch01-b048",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.7 Summary",
      "h3": null
    },
    "content_text": "- In the base ten number system, we use the digits 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 to represent any other number.\n- The numbers 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 are called units in the base ten number system.\n- The numbers 10; 20; 30; 40; 50; 60; 70; 80; 90 are called tens in the base ten number system.\n- The numbers 100; 200; 300; 400; 500; 600; 700; 800; 900 are called hundreds in the base ten number system.\n- The numbers 1,000; 2,000; 3,000; 4,000; 5,000; 6,000; 7,000; 8,000; 9,000 are called thousands in the base ten number system.\n- The numbers 10,000; 20,000; 30,000; 40,000; 50,000; 60,000; 70,000; 80,000; 90,000 are called ten thousands in the base ten number system.\n- Decimal fractions are written using the base ten number system. The digits of the numerator are written after a decimal point. The denominator is 10; 100; 1,000; 10,000 and so on. For example, the decimal fraction 0.25 is equal to $\\frac{25}{100}$.\n- We use commas to group the digits in large numbers in threes, so that they are easier to read. We group the digits from the decimal point, going to the left. For example, 4589762.35 is written as 4,589,762.35.\n- The place value of a digit is the value of that digit according to its position in the number.\n- We may use powers of ten to express large numbers. The power tells us how many times 10 must be multiplied by itself. For example, $10^4$ means $10\\times10\\times10\\times10$. Here is a list of the powers of ten.\n\n$$\n\\begin{array}{|l|l|l|}\n  \\hline\n  \\textbf{Name} & \\textbf{Number} & \\textbf{Powers of ten}  \\\\\n  \\hline\n   \\text{Ten} & 10 & 10=10^1    \\\\\n  \\hline\n   \\text{Hundred} & 100 & 10\\times10=10^2    \\\\\n  \\hline\n  \\text{Thousand} & 1,000 & 10\\times10\\times10=10^3    \\\\\n  \\hline\n  \\text{Ten thousand} & 10,000 & 10\\times10\\times10\\times10=10^4    \\\\\n  \\hline\n  \\text{Hundred thousand} & 100,000 & 10\\times10\\times10\\times10\\times10=10^5    \\\\\n  \\hline\n  \\text{Million} & 1,000,000 & 10\\times10\\times10\\times10\\times10\\times10=10^6    \\\\\n  \\hline\n  \\text{Ten million} & 10,000,000 & 10\\times10\\times10\\times10\\times10\\times10\\times10=10^7 \\\\\n  \\hline\n  \\text{Hundred million} & 100,000,000 & 10\\times10\\times10\\times10\\times10\\times10\\times10\\times10=10^8 \\\\\n  \\hline\n  \\text{Billion} & 1,000,000,000 & 10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10=10^9 \\\\\n  \\hline\n  \\text{Ten billion} & 10,000,000,000 & 10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10=10^{10} \\\\\n  \\hline\n  \\text{Hundred billion} & 100,000,000,000 & 10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10=10^{11} \\\\\n  \\hline\n  \\text{Trillion} & 1,000,000,000,000 & 10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10=10^{12} \\\\\n  \\hline\n   \\end{array}\n$$\n\n- We can use the above list to draw up a place value table. This makes it easer to work with large numbers.\n\n$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|c|c|c|}\n  \\hline\n  \\text{trillion} &\\text{hb} &\\text{tb} &\\text{billion} & \\text{hm} & \\text{tm} & \\text{million} &\\text{hth} & \\text{tth} & \\text{thousand} & \\text{ h } & \\text{ t } & \\text{ u }  \\\\\n  \\hline\n   &  &  &  &  &  &  &  &  &  &  &  &   \\\\\n  \\hline\n  \\end{array}\n$$\n\n- We may use a place value table to help us count with large numbers. Whenever we want to proceed after we reached the digit 9 in any column of the table, the 9 becomes 0 and the digit in the column to the left increases by 1.\n- Large numbers are sometimes expressed as a mixture of digits and words to make them easier to read. For example, 0.5 billion is the number 500,000,000 with the name five hundred million.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
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
