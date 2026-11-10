# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-2",
  "topic_key": "jss1-math-addition-and-subtraction",
  "topic": "Addition and Subtraction",
  "subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values",
  "subtopic_title": "Addition and subtraction of numbers and place values",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values-po01",
        "source_performance_objective_index": 1,
        "text": "Add and subtract correctly"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "addition-and-subtraction-ao-add-correctly",
          "text": "Add numbers correctly."
        },
        {
          "atomic_objective_id": "addition-and-subtraction-ao-subtract-correctly",
          "text": "Subtract numbers correctly."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values-po02",
        "source_performance_objective_index": 2,
        "text": "State place value of digits"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "addition-and-subtraction-ao-state-place-value-of-digits",
          "text": "State place value of digits."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
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
  },
  {
    "record_id": "ch01-b025",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.4 How to add in groups of ten using place value",
      "h3": null
    },
    "content_text": "In the base ten number system, we can have a maximum of 9 digits for one place value. For example, the number 90 means 9 groups of 10, so we have a 9 in the tens place value. We may write it as 9 x 10 = 90. If we add another group of 10, we have 10 x 10 = 100. This means we have 1 group of 100, so we have a 1 in the hundreds place value. Ten groups of 10 is named one hundred.\n\nSimilarly, the number 900 means 9 groups of 100. We may write it as 9 x 100 = 900. So there is a 9 in the hundreds place value. If we add another group of 100, we have 10 x 100 = 1,000. So we will then have a 1 in the thousands place value. Ten groups of 100 is named one thousand.\n\nHere are the names of some large numbers made up of groups of 10.\n\n$$\n\\begin{array}{|l|l|l|l|}\n  \\hline\n    \\textbf{Groups} & \\textbf{Meaning} & \\textbf{Value} &\\textbf{Name}  \\\\\n    \\hline\n     \\text{Ten groups of 1,000} & 10\\times1,000 & 10,000 & \\text{Ten thousand}    \\\\\n    \\hline\n    \\text{Ten groups of 10,000} & 10\\times10,000 & 100,000 & \\text{One hundred thousand}    \\\\\n    \\hline\n    \\text{Ten groups of 100,000} & 10\\times100,000 & 1,000,000 & \\text{One million}    \\\\\n    \\hline\n    \\text{Ten groups of 1,000,000} & 10\\times1,000,000 & 10,000,000 & \\text{Ten million}    \\\\\n    \\hline\n    \\text{Ten groups of 10,000,000} & 10\\times10,000,000 & 100,000,000 & \\text{One hundred million}    \\\\\n    \\hline\n    \\text{Ten groups of 100,000,000} & 10\\times100,000,000 & 1,000,000,000 & \\text{One billion}    \\\\\n    \\hline\n    \\text{Ten groups of 1,000,000,000} & 10\\times1,000,000,000 & 10,000,000,000 & \\text{Ten billion}    \\\\\n    \\hline\n    \\text{Ten groups of 10,000,000,000} & 10\\times10,000,000,000 & 100,000,000,000 & \\text{One hundred billion}    \\\\\n    \\hline\n    \\text{Ten groups of 100,000,000,000} & 10\\times100,000,000,000 & 1,000,000,000,000 & \\text{One trillion}    \\\\\n    \\hline\n     \\end{array}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch01-b026",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.4 How to add in groups of ten using place value",
      "h3": "Beyond the digit 9"
    },
    "content_text": "Whenever we reach the digit 9 in any column of a place value table, and then want to add one more group:\n\n- the digit 9 becomes 0\n- the digit in the column to the left must increase by 1.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch01-b027",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.4 How to add in groups of ten using place value",
      "h3": "Worked example 1.3: Dealing with the digit 9"
    },
    "content_text": "",
    "prompt_text": "Add 10,000 to the number 591,432.",
    "answer_text": "Step 1: Write the given number in a place value table. Find the column in which the digit will have to change.\n\n$$\n\\begin{array}{|c|c|c|c|c|c|}\n \\hline\n \\text{hth} & \\text{tth} & \\text{th} & \\text{h} & \\text{  t  } & \\text{  u  }  \\\\\n  (100,000) & (10,000) & (1,000) & (100) & (10) & (1) \\\\\n \\hline\n   5 & 9 & 1 & 4 & 3 & 2  \\\\\n \\hline\n \\end{array}\n$$\n\nIf 10,000 is added, the digit in the column labelled \"**tth**\" will change.\n\nStep 2: Change the 9 to 0. In the column to the left, increase the digit by 1.\n\n$$\n\\begin{array}{|c|c|c|c|c|c|}\n \\hline\n  \\text{hth} & \\text{tth} & \\text{th} & \\text{h} & \\text{  t  } & \\text{  u  }  \\\\\n  (100,000) & (10,000) & (1,000) & (100) & (10) & (1) \\\\\n \\hline\n   6 & 0 & 1 & 4 & 3 & 2  \\\\\n \\hline\n \\end{array}\n$$\n\nStep 3: Write down the answer with the digits grouped in threes.\n\n$$\n591,432+10,000=601,432\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch01-b028",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.4 How to add in groups of ten using place value",
      "h3": "Exercise 1.4: Do addition with numbers that have the digit 9"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.4: Do addition with numbers that have the digit 9",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch01-b028-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.4 How to add in groups of ten using place value",
      "h3": "Exercise 1.4: Do addition with numbers that have the digit 9"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.4: Do addition with numbers that have the digit 9\n\n1. Add 1,000 to the number 89,015.",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|c|}\n\\hline\n\\text{hth} & \\text{tth} & \\text{th} & \\text{h} & \\text{  t  } & \\text{  u  }  \\\\\n (100,000) & (10,000) & (1,000) & (100) & (10) & (1) \\\\\n\\hline\n   & 8 & 9 & 0 & 1 & 5  \\\\\n\\hline\n\\end{array}\n$$\n\nChange the 9 to 0 in the \"**th**\" column, and add 1 to the \"**tth**\" column.\n\n$$\n\\begin{array}{|c|c|c|c|c|c|}\n\\hline\n \\text{hth} & \\text{tth} & \\text{th} & \\text{h} & \\text{  t  } & \\text{  u  }  \\\\\n (100,000) & (10,000) & (1,000) & (100) & (10) & (1) \\\\\n\\hline\n   & 9 & 0 & 0 & 1 & 5  \\\\\n\\hline\n\\end{array}\n$$\n\n$$\n89,015+1,000=90,015\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch01-b028-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.4 How to add in groups of ten using place value",
      "h3": "Exercise 1.4: Do addition with numbers that have the digit 9"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.4: Do addition with numbers that have the digit 9\n\n2. Add 100 to the number 9,938.",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|c|}\n\\hline\n\\text{hth} & \\text{tth} & \\text{th} & \\text{h} & \\text{  t  } & \\text{  u  }  \\\\\n (100,000) & (10,000) & (1,000) & (100) & (10) & (1) \\\\\n\\hline\n   &  & 9 & 9 & 3 & 8  \\\\\n\\hline\n\\end{array}\n$$\n\nMake the 9 in the \"**h**\" column 0, and increase the \"**th**\" column by 1. Note that there is also a 9 in the **th** column. So change that 9 into 0 also, and add 1 to the next column to the left, which is **tth**.\n\n$$\n\\begin{array}{|c|c|c|c|c|c|}\n\\hline\n\\text{hth} & \\text{tth} & \\text{th} & \\text{h} & \\text{  t  } & \\text{  u  }  \\\\\n (100,000) & (10,000) & (1,000) & (100) & (10) & (1) \\\\\n\\hline\n   & 1 & 0 & 0 & 3 & 8  \\\\\n\\hline\n\\end{array}\n$$\n\n$$\n9,938+100=10,038\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch01-b028-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.4 How to add in groups of ten using place value",
      "h3": "Exercise 1.4: Do addition with numbers that have the digit 9"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.4: Do addition with numbers that have the digit 9\n\n3. Add 10 to the number 7,992.",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|c|}\n\\hline\n\\text{hth} & \\text{tth} & \\text{th} & \\text{h} & \\text{  t  } & \\text{  u  }  \\\\\n (100,000) & (10,000) & (1,000) & (100) & (10) & (1) \\\\\n\\hline\n   &  & 7 & 9 & 9 & 2  \\\\\n\\hline\n\\end{array}\n$$\n\nThe \"**t**\" column becomes 0 and the \"**h**\" column increases by 1. Note that there is a 9 in the **h** column too. When 1 is added to 9, it becomes 0, and the column to its left increases by 1.\n\n$$\n\\begin{array}{|c|c|c|c|c|c|}\n\\hline\n\\text{hth} & \\text{tth} & \\text{th} & \\text{h} & \\text{  t  } & \\text{  u  }  \\\\\n (100,000) & (10,000) & (1,000) & (100) & (10) & (1) \\\\\n\\hline\n   &  & 8 & 0 & 0 & 2  \\\\\n\\hline\n\\end{array}\n$$\n\n$$\n7,992+10=8,002\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch05-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.1 Revise place values",
      "h3": null
    },
    "content_text": "In Chapter 1 you learnt that the place value of a digit tells us what the value of that digit is, based on its position in a number. You used place value tables to determine the place value of specific digits in a number. For example, the number two million three hundred and five thousand two hundred and fourteen, may be written in a place value table as follows:\n\n$$\n\\begin{array}{|c|c|c|c|c|c|c|}\n  \\hline\n    \\text{million} &\\text{hundred thousand} & \\text{ten thousand} & \\; \\text{thousand} \\; & \\; \\text{hundred} \\; & \\;\\; \\text{ten} \\;\\; & \\;\\; \\text{unit}\\;\\;  \\\\\n    (1,000,000) & (100,000) & (10,000) & (1,000) & (100) & (10) & (1) \\\\\n    \\hline\n     2 & 3 & 0 & 5 & 2 & 1 & 4     \\\\\n    \\hline\n    \\end{array}\n$$\n\nThe place values of the non-zero digits in 2,305,214 are therefore:\n$2\\times1,000,000=2,000,000$\n$3\\times100,000=300,000$\n$5\\times1,000=5,000$\n$2\\times 100=200$\n$1\\times10=10$\n$4\\times1=4$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch05-b002",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.1 Revise place values",
      "h3": "Exercise 5.1: Determine place values"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.1: Determine place values",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch05-b002-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.1 Revise place values",
      "h3": "Exercise 5.1: Determine place values"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.1: Determine place values\n\n1. Determine the place value of the digit 8 in each of the following numbers.\n\n1. 987\n2. 2,804\n3. 168,417\n4. 3,806,640\n5. 26,008",
    "answer_text": "1. 987\nThe place value is: $8\\times10=80$\n\n2. 2,804\nThe place value is: $8\\times100=800$\n\n3. 168,417\nThe place value is: $8\\times1,000=8,000$\n\n4. 3,806,640\nThe place value is: $8\\times100,000=800,000$\n\n5. 26,008\nThe place value is: $8\\times1=8$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch05-b002-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.1 Revise place values",
      "h3": "Exercise 5.1: Determine place values"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.1: Determine place values\n\n2. Determine the two place values of the digit 3 in each of the following numbers.\n\n1. 363\n2. 3,031\n3. 32,358\n4. 331,047\n5. 3,158,325",
    "answer_text": "1. 363\nThe place values are 300 and 3.\n\n2. 3,031\nThe place values are 3,000 and 30.\n\n3. 32,358\nThe place values are 30,000 and 300.\n\n4. 331,047\nThe place values are 300,000 and 30,000.\n\n5. 3,158,325\nThe place values are 3,000,000 and 300.",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch05-b003",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.2 Addition and subtraction of large numbers",
      "h3": null
    },
    "content_text": "It is important to be aware of place values when we add or subtract large numbers. For example, we cannot subtract hundreds from units, or thousands from tens.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch05-b004",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.2 Addition and subtraction of large numbers",
      "h3": "Worked example 5.1: Adding whole numbers"
    },
    "content_text": "",
    "prompt_text": "Find the total of $403+628+1,023+49$.",
    "answer_text": "Step 1: Write the numbers one below the other. Line up the units, tens, hundreds, thousands, and so on.\n\n$$\n\\begin{array}{r r}\n  & \\text{th}\\, \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n  & 4\\,0\\,3 \\\\\n + & 6\\,2\\,8 \\\\\n + & 1,0\\,2\\,3 \\\\\n + & 4\\,9 \\\\\n \\hline\n \\end{array}\n$$\n\nStep 2: Add the units column. If the answer is more than 9, write the units of the answer underneath the units column. Write the tens of the answer at the top of the tens column.\n\n$$3+8+3+9=23$$\n\n$$\n\\begin{array}{r r}\n  & \\text{th}\\, \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n  &_{2} \\,\\phantom{0}\\\\\n  & 4\\,0\\,3 \\\\\n + & 6\\,2\\,8 \\\\\n + & 1,0\\,2\\,3 \\\\\n + & 4\\,9 \\\\\n \\hline\n &3\\\\\n \\hline\n \\end{array}\n$$\n\nStep 3: Add the tens column. Include the tens from Step 2. If the answer is more than 9, write the tens of the answer underneath the tens column. Write the hundreds of the answer at the top of the hundreds column.\n\n$$2+0+2+2+4=10$$\n\n$$\n\\begin{array}{r r}\n  & \\text{th}\\, \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n  &_{1}\\, _{2} \\,\\phantom{0}\\\\\n  & 4\\,0\\,3 \\\\\n + & 6\\,2\\,8 \\\\\n + & 1,0\\,2\\,3 \\\\\n + & 4\\,9 \\\\\n \\hline\n &0\\,3\\\\\n \\hline\n \\end{array}\n$$\n\nStep 4: Repeat Step 3 with the hundreds and thousands. Remember to insert a comma to show thousands.\n\n$$\\text{Hundreds}:\\space1+4+6+0=11$$\n$$\\text{Thousands}:\\space1+1=2$$\n\n$$\n\\begin{array}{r r}\n  & \\text{th}\\, \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n  &_{1}\\;\\,_1\\, _2 \\,\\phantom{0}\\\\\n  & 4\\,0\\,3 \\\\\n + & 6\\,2\\,8 \\\\\n + & 1,0\\,2\\,3 \\\\\n + & 4\\,9 \\\\\n \\hline\n &2,1\\,0\\,3\\\\\n \\hline\n \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch05-b005",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.2 Addition and subtraction of large numbers",
      "h3": "Worked example 5.2: Subtracting whole numbers"
    },
    "content_text": "",
    "prompt_text": "Subtract 178 from 4,032.",
    "answer_text": "Step 1: Write the numbers one below the other. Line up the units, tens, hundreds, thousands, and so on.\n\n$$\n\\begin{array}{r r}\n  & \\text{th}\\, \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n & 4,0\\,3\\,2 \\\\\n         - & 1\\,7\\,8 \\\\\n \\hline\n \\end{array}\n$$\n\nStep 2: Subtract the units column. If there are not enough units to subtract from, move one group from the tens column to the units column.\n\n- We cannot subtract 8 from 2.\n- There are 3 groups of 10 in the tens column. Move one of them to the units column.\n- The units column now has the value $10+2=12$.\n- The tens column has only 2 groups of 10 left.\n\n$$\n\\begin{array}{r r}\n  & \\text{th}\\;\\, \\text{h}\\;\\, \\text{t}\\;\\, \\text{u}\\; \\\\\n  &_{2}\\;\\,_{12} \\\\\n & 4,0\\,\\cancel{3}\\cancel{2} \\\\\n         - & 1\\;\\,7\\;8\\;\\, \\\\\n \\hline\n \\end{array}\n$$\n\nNow we can subtract the units: $12-8=4$\n\n$$\n\\begin{array}{r r}\n  & \\text{th}\\;\\, \\text{h}\\;\\, \\text{t}\\;\\, \\text{u}\\; \\\\\n  &_{2}\\;\\,_{12} \\\\\n & 4,0\\,\\cancel{3}\\cancel{2} \\\\\n- & 1\\;\\,7\\;8\\;\\, \\\\\n   \\hline\n  &4\\;\\,\\\\\n   \\hline\n   \\end{array}\n$$\n\nStep 3: Repeat Step 2 with the tens column. If necessary, move one group from the hundreds column to the tens column.\n\n- We cannot subtract 7 from 2.\n- There are no groups in the hundreds column. We must move one group from the thousands column to the hundreds column.\n- There are 4 groups of 1,000 in the thousands column. Move one of them to the hundreds column.\n- The hundreds column now has 1 group of 1,000. This is equal to 10 groups of 100.\n- The thousands column has only 3 groups of 1,000 left.\n\n$$\n\\begin{array}{r r}\n  & \\text{th}\\phantom{0}\\; \\text{h}\\phantom{0}\\; \\text{t}\\phantom{0} \\text{u}\\; \\\\\n  &_{3}\\;\\;_{10}\\,\\;\\;_{2}\\,\\;_{12}\\, \\\\\n & \\cancel{4},\\cancel{0}\\,\\cancel{3}\\cancel{2} \\\\\n         - & 1\\;\\;\\,7\\;\\,8\\; \\\\\n \\hline\n &4\\;\\,\\\\\n \\hline\n \\end{array}\n$$\n\nNow we can move one group from the hundreds column to the tens column.\n\nThe tens column now has 12 groups of 10.\nThe hundreds column only has 9 groups of 100 left.\n\n$$\n\\begin{array}{r r}\n  & \\text{th}\\phantom{0}\\; \\text{h}\\phantom{0}\\; \\text{t}\\phantom{0} \\text{u}\\; \\\\\n  &_{3}\\;\\;\\; _{9}\\;\\;_{12}\\,_{12}\\, \\\\\n & \\cancel{4},\\cancel{0}\\,\\cancel{3}\\cancel{2} \\\\\n         - & 1\\;\\;\\,7\\;\\,8\\; \\\\\n    \\hline\n &4\\;\\,\\\\\n \\hline\n \\end{array}\n$$\n\nNow we can subtract the tens: $12-7=5$\n\n$$\n\\begin{array}{r r}\n  & \\text{th}\\phantom{0}\\; \\text{h}\\phantom{0}\\; \\text{t}\\phantom{0} \\text{u}\\; \\\\\n  &_{3}\\;\\;\\; _{9}\\;\\;_{12}\\,_{12}\\, \\\\\n & \\cancel{4},\\cancel{0}\\,\\cancel{3}\\cancel{2} \\\\\n         - & 1\\;\\;\\,7\\;\\,8\\; \\\\\n    \\hline\n &5\\;\\,4\\;\\\\\n \\hline\n \\end{array}\n$$\n\nStep 4: Repeat Step 3 with the hundreds and thousands.\n\n$$\\text{Hundreds}:\\space9-1=8$$\n$$\n\\begin{array}{r r}\n  & \\text{th}\\phantom{0}\\; \\text{h}\\phantom{0}\\; \\text{t}\\phantom{0} \\text{u}\\; \\\\\n  &_{3}\\;\\;\\; _{9}\\;\\;_{12}\\,_{12}\\, \\\\\n & \\cancel{4},\\cancel{0}\\,\\cancel{3}\\cancel{2} \\\\\n         - & 1\\;\\;\\,7\\;\\,8\\; \\\\\n    \\hline\n &8\\;\\;\\,5\\;\\,4\\;\\\\\n \\hline\n \\end{array}\n$$\n$$\\text{Thousands}:\\space3-0=3$$\n$$\n\\begin{array}{r r}\n  & \\text{th}\\phantom{0}\\; \\text{h}\\phantom{0}\\; \\text{t}\\phantom{0} \\text{u}\\; \\\\\n  &_{3}\\;\\;\\; _{9}\\;\\;_{12}\\,_{12}\\, \\\\\n & \\cancel{4},\\cancel{0}\\,\\cancel{3}\\cancel{2} \\\\\n         - & 1\\;\\;\\,7\\;\\,8\\; \\\\\n    \\hline\n &3,\\phantom{0}8\\;\\;\\,5\\;\\,4\\;\\\\\n \\hline\n \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch05-b006",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.2 Addition and subtraction of large numbers",
      "h3": "Exercise 5.2: Add and subtract whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.2: Add and subtract whole numbers",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch05-b006-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.2 Addition and subtraction of large numbers",
      "h3": "Exercise 5.2: Add and subtract whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.2: Add and subtract whole numbers\n\n1. Add the following numbers.\n\n1. $9,000+800+70+6$\n2. $5,050+55+5+500$\n3. $2,804+1,999+3,333$\n4. $42+1,005+936+41$\n5. $909+9,090+9,009+9$",
    "answer_text": "1. $9,000+800+70+6$\n$$\n\\begin{array}{r r}\n& 9,000 \\\\\n+ & 800 \\\\\n+ & 70 \\\\\n+ & 6 \\\\\n\\hline\n&9,876\\\\\n\\hline\n\\end{array}\n$$\n\n2. $5,050+55+5+500$\n$$\n\\begin{array}{r r}\n&_{1\\space1} \\phantom{0}\\\\\n& 5,050 \\\\\n+ & 55 \\\\\n+ & 5 \\\\\n+ & 500 \\\\\n\\hline\n&5,610\\\\\n\\hline\n\\end{array}\n$$\n\n3. $2,804+1,999+3,333$\n$$\n\\begin{array}{r r}\n&_2\\; _1\\, _1 \\phantom{0}\\\\\n& 2,804 \\\\\n+ & 1,999 \\\\\n+ & 3,333 \\\\\n\\hline\n&8,136\\\\\n\\hline\n\\end{array}\n$$\n\n4. $42+1,005+936+41$\n$$\n\\begin{array}{r r}\n&_1\\;_1\\,_1\\phantom{0}\\\\\n& 42 \\\\\n+ & 1,005 \\\\\n+ & 936 \\\\\n+ & 41 \\\\\n\\hline\n&2,024\\\\\n\\hline\n\\end{array}\n$$\n\n5. $909+9,090+9,009+9$\n$$\n\\begin{array}{r r}\n&_1\\;_1\\,_2\\phantom{0}\\\\\n& 909 \\\\\n+ & 9,090 \\\\\n+ & 9,009 \\\\\n+ & 9 \\\\\n\\hline\n&19,017\\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch05-b006-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.2 Addition and subtraction of large numbers",
      "h3": "Exercise 5.2: Add and subtract whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.2: Add and subtract whole numbers\n\n2. Subtract the following numbers.\n\n1. $8,642-2,468$\n2. $1,723-958$\n3. $7,777-888$\n4. $10,000-8,734$\n5. $50,000-599$",
    "answer_text": "1. $8,642-2,468$\n$$\n\\begin{array}{r r}\n&_5\\,\\;_{13}\\,_{12}\\,\\\\\n& 8,\\cancel{6}\\cancel{4}\\cancel{2} \\\\\n- & 2,\\;4\\;\\;6\\;\\,8\\; \\\\\n\\hline\n& 6,\\;1\\;\\;7\\;\\,4\\;\\\\\n\\hline\n\\end{array}\n$$\n\n2. $1,723-958$\n$$\n\\begin{array}{r r}\n&_0\\;\\;\\; _{16}\\; _{11}\\, _{13}\\,\\\\\n& \\cancel{1},\\cancel{7}\\cancel{2}\\cancel{3} \\\\\n- & 9\\;\\;5\\;\\,8\\; \\\\\n\\hline\n& 7\\;\\;6\\;\\,5\\;\\\\\n\\hline\n\\end{array}\n$$\n\n3. $7,777-888$\n$$\n\\begin{array}{r r}\n&_6\\;\\;\\; _{16}\\; _{16}\\, _{17}\\,\\\\\n& \\cancel{7},\\cancel{7}\\cancel{7}\\cancel{7} \\\\\n- & 8\\;\\;8\\;\\,8\\; \\\\\n\\hline\n& 6,\\;\\;8\\;\\;8\\;\\,9\\;\\\\\n\\hline\n\\end{array}\n$$\n\n4. $10,000-8,734$\n$$\n\\begin{array}{r r}\n&_0\\;\\;\\;_9\\;\\;\\; _9\\;\\; _9\\;\\, _{10}\\,\\\\\n& \\cancel{1}\\cancel{0},\\cancel{0}\\cancel{0}\\cancel{0} \\\\\n- & 8,\\;\\;7\\;\\;3\\;\\,4\\; \\\\\n\\hline\n& 1,\\;\\;2\\;\\;6\\;\\,6\\;\\\\\n\\hline\n\\end{array}\n$$\n\n5. $50,000-599$\n$$\n\\begin{array}{r r}\n&_4\\;\\;\\;_9\\;\\;\\; _9\\;\\; _9\\;\\, _{10}\\,\\\\\n& \\cancel{5}\\cancel{0},\\cancel{0}\\cancel{0}\\cancel{0} \\\\\n- & 5\\;\\;9\\;\\,9\\; \\\\\n\\hline\n& 4\\;\\;9,\\;\\;4\\;\\;0\\;\\,1\\;\\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch05-b006-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.2 Addition and subtraction of large numbers",
      "h3": "Exercise 5.2: Add and subtract whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.2: Add and subtract whole numbers\n\n3. Determine the difference in the two place values of 5 in the following numbers.\n\nTo determine the difference between two numbers, subtract the smaller number from the larger number.\n\n1. 1,025,568\n2. 58,753\n3. 5,198,352",
    "answer_text": "1. 1,025,568\nThe place values are 5,000 and 500.\n$$\n\\begin{array}{r r}\n&_4 \\phantom{00} _{10}\\phantom{00}\\\\\n& \\cancel{5},\\cancel{0}00 \\\\\n- & 5\\;00 \\\\\n\\hline\n& 4\\,,\\;5\\;00\\\\\n\\hline\n\\end{array}\n$$\n\n2. 58,753\nThe place values are 50,000 and 50.\n$$\n\\begin{array}{r r}\n&_4\\;\\;\\,_9\\;\\;\\;\\, _{10}\\phantom{0}\\\\\n& \\cancel{5}\\cancel{0},\\cancel{0}\\cancel{0}0 \\\\\n- & 5\\;0 \\\\\n\\hline\n& 4\\;\\;9\\,,\\;9\\;5\\;0\\\\\n\\hline\n\\end{array}\n$$\n\n3. 5,198,352\nThe place values are 5,000,000 and 50.\n$$\n\\begin{array}{r r}\n&_4\\;\\;\\;_9\\;\\;\\,_9\\;\\; _9\\;\\;\\;\\; _9\\;\\; _{10}\\phantom{0}\\\\\n& \\cancel{5},\\cancel{0}\\cancel{0}\\cancel{0},\\cancel{0}\\cancel{0}0 \\\\\n- & 5\\;0 \\\\\n\\hline\n& 4,\\;\\;9\\;\\;9\\;\\;9\\;,\\;9\\;\\,5\\;0\\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch05-b033",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.6 Summary",
      "h3": null
    },
    "content_text": "- The place value of a digit tells us what the value of that digit is, based on its position in a number.\n- When we add or subtract large numbers, we line up the units, tens, hundreds and thousands of the numbers.\n- A number line is a straight line, divided into equal segments, that shows the positions of numbers.\n- Positive numbers are larger than zero and lie to the right of zero on a number line.\n- Negative numbers are smaller than zero and lie to the left of zero on a number line.\n- Zero is neither positive nor negative.\n- The symbol < means \"smaller than\", and 3<5 means three is smaller than five. The symbol > means \"greater than\", and 5>3 means five is greater than three.\n- When we add one integer to another, we may see it as units that are added along the number line. When we add positive numbers, we count to the right on a number line. When we add negative numbers, we count to the left on a number line.\n- Subtracting a number is the same as adding the \"opposite\" of the number. For example, $2-7$ is the same as $2+(-7)$.\n- Subtraction may also be seen as the difference between two numbers. For example, there are 5 units between the numbers 2 and 7. If the number which is subtracted from lies to the negative side of the number that is subtracted, the difference is negative: $2-7=-5$. If the number which is subtracted from lies to the positive side of the number that is subtracted, the difference is positive: $7-2=5$.\n- A thermometer is an instrument used to measure temperature. Temperatures above $0\\space ^\\circ\\text C$ are positive. Temperatures below $0\\space ^\\circ\\text C$ are negative.\n- A positive bank balance means you have money in the bank. A negative bank balance means you owe the bank money.\n- For movement along a straight line, we take one direction as positive. The opposite direction is negative.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
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
  "topic_key": "jss1-math-addition-and-subtraction",
  "topic": "Addition and Subtraction",
  "subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values",
  "subtopic_title": "Addition and subtraction of numbers and place values",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values-po01",
        "source_performance_objective_index": 1,
        "text": "Add and subtract correctly"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "addition-and-subtraction-ao-add-correctly",
          "text": "Add numbers correctly."
        },
        {
          "atomic_objective_id": "addition-and-subtraction-ao-subtract-correctly",
          "text": "Subtract numbers correctly."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values-po02",
        "source_performance_objective_index": 2,
        "text": "State place value of digits"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "addition-and-subtraction-ao-state-place-value-of-digits",
          "text": "State place value of digits."
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
  },
  {
    "record_id": "ch01-b025",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.4 How to add in groups of ten using place value",
      "h3": null
    },
    "content_text": "In the base ten number system, we can have a maximum of 9 digits for one place value. For example, the number 90 means 9 groups of 10, so we have a 9 in the tens place value. We may write it as 9 x 10 = 90. If we add another group of 10, we have 10 x 10 = 100. This means we have 1 group of 100, so we have a 1 in the hundreds place value. Ten groups of 10 is named one hundred.\n\nSimilarly, the number 900 means 9 groups of 100. We may write it as 9 x 100 = 900. So there is a 9 in the hundreds place value. If we add another group of 100, we have 10 x 100 = 1,000. So we will then have a 1 in the thousands place value. Ten groups of 100 is named one thousand.\n\nHere are the names of some large numbers made up of groups of 10.\n\n$$\n\\begin{array}{|l|l|l|l|}\n  \\hline\n    \\textbf{Groups} & \\textbf{Meaning} & \\textbf{Value} &\\textbf{Name}  \\\\\n    \\hline\n     \\text{Ten groups of 1,000} & 10\\times1,000 & 10,000 & \\text{Ten thousand}    \\\\\n    \\hline\n    \\text{Ten groups of 10,000} & 10\\times10,000 & 100,000 & \\text{One hundred thousand}    \\\\\n    \\hline\n    \\text{Ten groups of 100,000} & 10\\times100,000 & 1,000,000 & \\text{One million}    \\\\\n    \\hline\n    \\text{Ten groups of 1,000,000} & 10\\times1,000,000 & 10,000,000 & \\text{Ten million}    \\\\\n    \\hline\n    \\text{Ten groups of 10,000,000} & 10\\times10,000,000 & 100,000,000 & \\text{One hundred million}    \\\\\n    \\hline\n    \\text{Ten groups of 100,000,000} & 10\\times100,000,000 & 1,000,000,000 & \\text{One billion}    \\\\\n    \\hline\n    \\text{Ten groups of 1,000,000,000} & 10\\times1,000,000,000 & 10,000,000,000 & \\text{Ten billion}    \\\\\n    \\hline\n    \\text{Ten groups of 10,000,000,000} & 10\\times10,000,000,000 & 100,000,000,000 & \\text{One hundred billion}    \\\\\n    \\hline\n    \\text{Ten groups of 100,000,000,000} & 10\\times100,000,000,000 & 1,000,000,000,000 & \\text{One trillion}    \\\\\n    \\hline\n     \\end{array}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch01-b026",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.4 How to add in groups of ten using place value",
      "h3": "Beyond the digit 9"
    },
    "content_text": "Whenever we reach the digit 9 in any column of a place value table, and then want to add one more group:\n\n- the digit 9 becomes 0\n- the digit in the column to the left must increase by 1.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch01-b027",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.4 How to add in groups of ten using place value",
      "h3": "Worked example 1.3: Dealing with the digit 9"
    },
    "content_text": "",
    "prompt_text": "Add 10,000 to the number 591,432.",
    "answer_text": "Step 1: Write the given number in a place value table. Find the column in which the digit will have to change.\n\n$$\n\\begin{array}{|c|c|c|c|c|c|}\n \\hline\n \\text{hth} & \\text{tth} & \\text{th} & \\text{h} & \\text{  t  } & \\text{  u  }  \\\\\n  (100,000) & (10,000) & (1,000) & (100) & (10) & (1) \\\\\n \\hline\n   5 & 9 & 1 & 4 & 3 & 2  \\\\\n \\hline\n \\end{array}\n$$\n\nIf 10,000 is added, the digit in the column labelled \"**tth**\" will change.\n\nStep 2: Change the 9 to 0. In the column to the left, increase the digit by 1.\n\n$$\n\\begin{array}{|c|c|c|c|c|c|}\n \\hline\n  \\text{hth} & \\text{tth} & \\text{th} & \\text{h} & \\text{  t  } & \\text{  u  }  \\\\\n  (100,000) & (10,000) & (1,000) & (100) & (10) & (1) \\\\\n \\hline\n   6 & 0 & 1 & 4 & 3 & 2  \\\\\n \\hline\n \\end{array}\n$$\n\nStep 3: Write down the answer with the digits grouped in threes.\n\n$$\n591,432+10,000=601,432\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch01-b028",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.4 How to add in groups of ten using place value",
      "h3": "Exercise 1.4: Do addition with numbers that have the digit 9"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.4: Do addition with numbers that have the digit 9",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch01-b028-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.4 How to add in groups of ten using place value",
      "h3": "Exercise 1.4: Do addition with numbers that have the digit 9"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.4: Do addition with numbers that have the digit 9\n\n1. Add 1,000 to the number 89,015.",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|c|}\n\\hline\n\\text{hth} & \\text{tth} & \\text{th} & \\text{h} & \\text{  t  } & \\text{  u  }  \\\\\n (100,000) & (10,000) & (1,000) & (100) & (10) & (1) \\\\\n\\hline\n   & 8 & 9 & 0 & 1 & 5  \\\\\n\\hline\n\\end{array}\n$$\n\nChange the 9 to 0 in the \"**th**\" column, and add 1 to the \"**tth**\" column.\n\n$$\n\\begin{array}{|c|c|c|c|c|c|}\n\\hline\n \\text{hth} & \\text{tth} & \\text{th} & \\text{h} & \\text{  t  } & \\text{  u  }  \\\\\n (100,000) & (10,000) & (1,000) & (100) & (10) & (1) \\\\\n\\hline\n   & 9 & 0 & 0 & 1 & 5  \\\\\n\\hline\n\\end{array}\n$$\n\n$$\n89,015+1,000=90,015\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch01-b028-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.4 How to add in groups of ten using place value",
      "h3": "Exercise 1.4: Do addition with numbers that have the digit 9"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.4: Do addition with numbers that have the digit 9\n\n2. Add 100 to the number 9,938.",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|c|}\n\\hline\n\\text{hth} & \\text{tth} & \\text{th} & \\text{h} & \\text{  t  } & \\text{  u  }  \\\\\n (100,000) & (10,000) & (1,000) & (100) & (10) & (1) \\\\\n\\hline\n   &  & 9 & 9 & 3 & 8  \\\\\n\\hline\n\\end{array}\n$$\n\nMake the 9 in the \"**h**\" column 0, and increase the \"**th**\" column by 1. Note that there is also a 9 in the **th** column. So change that 9 into 0 also, and add 1 to the next column to the left, which is **tth**.\n\n$$\n\\begin{array}{|c|c|c|c|c|c|}\n\\hline\n\\text{hth} & \\text{tth} & \\text{th} & \\text{h} & \\text{  t  } & \\text{  u  }  \\\\\n (100,000) & (10,000) & (1,000) & (100) & (10) & (1) \\\\\n\\hline\n   & 1 & 0 & 0 & 3 & 8  \\\\\n\\hline\n\\end{array}\n$$\n\n$$\n9,938+100=10,038\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch01-b028-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.4 How to add in groups of ten using place value",
      "h3": "Exercise 1.4: Do addition with numbers that have the digit 9"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.4: Do addition with numbers that have the digit 9\n\n3. Add 10 to the number 7,992.",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|c|}\n\\hline\n\\text{hth} & \\text{tth} & \\text{th} & \\text{h} & \\text{  t  } & \\text{  u  }  \\\\\n (100,000) & (10,000) & (1,000) & (100) & (10) & (1) \\\\\n\\hline\n   &  & 7 & 9 & 9 & 2  \\\\\n\\hline\n\\end{array}\n$$\n\nThe \"**t**\" column becomes 0 and the \"**h**\" column increases by 1. Note that there is a 9 in the **h** column too. When 1 is added to 9, it becomes 0, and the column to its left increases by 1.\n\n$$\n\\begin{array}{|c|c|c|c|c|c|}\n\\hline\n\\text{hth} & \\text{tth} & \\text{th} & \\text{h} & \\text{  t  } & \\text{  u  }  \\\\\n (100,000) & (10,000) & (1,000) & (100) & (10) & (1) \\\\\n\\hline\n   &  & 8 & 0 & 0 & 2  \\\\\n\\hline\n\\end{array}\n$$\n\n$$\n7,992+10=8,002\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch05-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.1 Revise place values",
      "h3": null
    },
    "content_text": "In Chapter 1 you learnt that the place value of a digit tells us what the value of that digit is, based on its position in a number. You used place value tables to determine the place value of specific digits in a number. For example, the number two million three hundred and five thousand two hundred and fourteen, may be written in a place value table as follows:\n\n$$\n\\begin{array}{|c|c|c|c|c|c|c|}\n  \\hline\n    \\text{million} &\\text{hundred thousand} & \\text{ten thousand} & \\; \\text{thousand} \\; & \\; \\text{hundred} \\; & \\;\\; \\text{ten} \\;\\; & \\;\\; \\text{unit}\\;\\;  \\\\\n    (1,000,000) & (100,000) & (10,000) & (1,000) & (100) & (10) & (1) \\\\\n    \\hline\n     2 & 3 & 0 & 5 & 2 & 1 & 4     \\\\\n    \\hline\n    \\end{array}\n$$\n\nThe place values of the non-zero digits in 2,305,214 are therefore:\n$2\\times1,000,000=2,000,000$\n$3\\times100,000=300,000$\n$5\\times1,000=5,000$\n$2\\times 100=200$\n$1\\times10=10$\n$4\\times1=4$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch05-b002",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.1 Revise place values",
      "h3": "Exercise 5.1: Determine place values"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.1: Determine place values",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch05-b002-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.1 Revise place values",
      "h3": "Exercise 5.1: Determine place values"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.1: Determine place values\n\n1. Determine the place value of the digit 8 in each of the following numbers.\n\n1. 987\n2. 2,804\n3. 168,417\n4. 3,806,640\n5. 26,008",
    "answer_text": "1. 987\nThe place value is: $8\\times10=80$\n\n2. 2,804\nThe place value is: $8\\times100=800$\n\n3. 168,417\nThe place value is: $8\\times1,000=8,000$\n\n4. 3,806,640\nThe place value is: $8\\times100,000=800,000$\n\n5. 26,008\nThe place value is: $8\\times1=8$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch05-b002-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.1 Revise place values",
      "h3": "Exercise 5.1: Determine place values"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.1: Determine place values\n\n2. Determine the two place values of the digit 3 in each of the following numbers.\n\n1. 363\n2. 3,031\n3. 32,358\n4. 331,047\n5. 3,158,325",
    "answer_text": "1. 363\nThe place values are 300 and 3.\n\n2. 3,031\nThe place values are 3,000 and 30.\n\n3. 32,358\nThe place values are 30,000 and 300.\n\n4. 331,047\nThe place values are 300,000 and 30,000.\n\n5. 3,158,325\nThe place values are 3,000,000 and 300.",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch05-b003",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.2 Addition and subtraction of large numbers",
      "h3": null
    },
    "content_text": "It is important to be aware of place values when we add or subtract large numbers. For example, we cannot subtract hundreds from units, or thousands from tens.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch05-b004",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.2 Addition and subtraction of large numbers",
      "h3": "Worked example 5.1: Adding whole numbers"
    },
    "content_text": "",
    "prompt_text": "Find the total of $403+628+1,023+49$.",
    "answer_text": "Step 1: Write the numbers one below the other. Line up the units, tens, hundreds, thousands, and so on.\n\n$$\n\\begin{array}{r r}\n  & \\text{th}\\, \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n  & 4\\,0\\,3 \\\\\n + & 6\\,2\\,8 \\\\\n + & 1,0\\,2\\,3 \\\\\n + & 4\\,9 \\\\\n \\hline\n \\end{array}\n$$\n\nStep 2: Add the units column. If the answer is more than 9, write the units of the answer underneath the units column. Write the tens of the answer at the top of the tens column.\n\n$$3+8+3+9=23$$\n\n$$\n\\begin{array}{r r}\n  & \\text{th}\\, \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n  &_{2} \\,\\phantom{0}\\\\\n  & 4\\,0\\,3 \\\\\n + & 6\\,2\\,8 \\\\\n + & 1,0\\,2\\,3 \\\\\n + & 4\\,9 \\\\\n \\hline\n &3\\\\\n \\hline\n \\end{array}\n$$\n\nStep 3: Add the tens column. Include the tens from Step 2. If the answer is more than 9, write the tens of the answer underneath the tens column. Write the hundreds of the answer at the top of the hundreds column.\n\n$$2+0+2+2+4=10$$\n\n$$\n\\begin{array}{r r}\n  & \\text{th}\\, \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n  &_{1}\\, _{2} \\,\\phantom{0}\\\\\n  & 4\\,0\\,3 \\\\\n + & 6\\,2\\,8 \\\\\n + & 1,0\\,2\\,3 \\\\\n + & 4\\,9 \\\\\n \\hline\n &0\\,3\\\\\n \\hline\n \\end{array}\n$$\n\nStep 4: Repeat Step 3 with the hundreds and thousands. Remember to insert a comma to show thousands.\n\n$$\\text{Hundreds}:\\space1+4+6+0=11$$\n$$\\text{Thousands}:\\space1+1=2$$\n\n$$\n\\begin{array}{r r}\n  & \\text{th}\\, \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n  &_{1}\\;\\,_1\\, _2 \\,\\phantom{0}\\\\\n  & 4\\,0\\,3 \\\\\n + & 6\\,2\\,8 \\\\\n + & 1,0\\,2\\,3 \\\\\n + & 4\\,9 \\\\\n \\hline\n &2,1\\,0\\,3\\\\\n \\hline\n \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch05-b005",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.2 Addition and subtraction of large numbers",
      "h3": "Worked example 5.2: Subtracting whole numbers"
    },
    "content_text": "",
    "prompt_text": "Subtract 178 from 4,032.",
    "answer_text": "Step 1: Write the numbers one below the other. Line up the units, tens, hundreds, thousands, and so on.\n\n$$\n\\begin{array}{r r}\n  & \\text{th}\\, \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n & 4,0\\,3\\,2 \\\\\n         - & 1\\,7\\,8 \\\\\n \\hline\n \\end{array}\n$$\n\nStep 2: Subtract the units column. If there are not enough units to subtract from, move one group from the tens column to the units column.\n\n- We cannot subtract 8 from 2.\n- There are 3 groups of 10 in the tens column. Move one of them to the units column.\n- The units column now has the value $10+2=12$.\n- The tens column has only 2 groups of 10 left.\n\n$$\n\\begin{array}{r r}\n  & \\text{th}\\;\\, \\text{h}\\;\\, \\text{t}\\;\\, \\text{u}\\; \\\\\n  &_{2}\\;\\,_{12} \\\\\n & 4,0\\,\\cancel{3}\\cancel{2} \\\\\n         - & 1\\;\\,7\\;8\\;\\, \\\\\n \\hline\n \\end{array}\n$$\n\nNow we can subtract the units: $12-8=4$\n\n$$\n\\begin{array}{r r}\n  & \\text{th}\\;\\, \\text{h}\\;\\, \\text{t}\\;\\, \\text{u}\\; \\\\\n  &_{2}\\;\\,_{12} \\\\\n & 4,0\\,\\cancel{3}\\cancel{2} \\\\\n- & 1\\;\\,7\\;8\\;\\, \\\\\n   \\hline\n  &4\\;\\,\\\\\n   \\hline\n   \\end{array}\n$$\n\nStep 3: Repeat Step 2 with the tens column. If necessary, move one group from the hundreds column to the tens column.\n\n- We cannot subtract 7 from 2.\n- There are no groups in the hundreds column. We must move one group from the thousands column to the hundreds column.\n- There are 4 groups of 1,000 in the thousands column. Move one of them to the hundreds column.\n- The hundreds column now has 1 group of 1,000. This is equal to 10 groups of 100.\n- The thousands column has only 3 groups of 1,000 left.\n\n$$\n\\begin{array}{r r}\n  & \\text{th}\\phantom{0}\\; \\text{h}\\phantom{0}\\; \\text{t}\\phantom{0} \\text{u}\\; \\\\\n  &_{3}\\;\\;_{10}\\,\\;\\;_{2}\\,\\;_{12}\\, \\\\\n & \\cancel{4},\\cancel{0}\\,\\cancel{3}\\cancel{2} \\\\\n         - & 1\\;\\;\\,7\\;\\,8\\; \\\\\n \\hline\n &4\\;\\,\\\\\n \\hline\n \\end{array}\n$$\n\nNow we can move one group from the hundreds column to the tens column.\n\nThe tens column now has 12 groups of 10.\nThe hundreds column only has 9 groups of 100 left.\n\n$$\n\\begin{array}{r r}\n  & \\text{th}\\phantom{0}\\; \\text{h}\\phantom{0}\\; \\text{t}\\phantom{0} \\text{u}\\; \\\\\n  &_{3}\\;\\;\\; _{9}\\;\\;_{12}\\,_{12}\\, \\\\\n & \\cancel{4},\\cancel{0}\\,\\cancel{3}\\cancel{2} \\\\\n         - & 1\\;\\;\\,7\\;\\,8\\; \\\\\n    \\hline\n &4\\;\\,\\\\\n \\hline\n \\end{array}\n$$\n\nNow we can subtract the tens: $12-7=5$\n\n$$\n\\begin{array}{r r}\n  & \\text{th}\\phantom{0}\\; \\text{h}\\phantom{0}\\; \\text{t}\\phantom{0} \\text{u}\\; \\\\\n  &_{3}\\;\\;\\; _{9}\\;\\;_{12}\\,_{12}\\, \\\\\n & \\cancel{4},\\cancel{0}\\,\\cancel{3}\\cancel{2} \\\\\n         - & 1\\;\\;\\,7\\;\\,8\\; \\\\\n    \\hline\n &5\\;\\,4\\;\\\\\n \\hline\n \\end{array}\n$$\n\nStep 4: Repeat Step 3 with the hundreds and thousands.\n\n$$\\text{Hundreds}:\\space9-1=8$$\n$$\n\\begin{array}{r r}\n  & \\text{th}\\phantom{0}\\; \\text{h}\\phantom{0}\\; \\text{t}\\phantom{0} \\text{u}\\; \\\\\n  &_{3}\\;\\;\\; _{9}\\;\\;_{12}\\,_{12}\\, \\\\\n & \\cancel{4},\\cancel{0}\\,\\cancel{3}\\cancel{2} \\\\\n         - & 1\\;\\;\\,7\\;\\,8\\; \\\\\n    \\hline\n &8\\;\\;\\,5\\;\\,4\\;\\\\\n \\hline\n \\end{array}\n$$\n$$\\text{Thousands}:\\space3-0=3$$\n$$\n\\begin{array}{r r}\n  & \\text{th}\\phantom{0}\\; \\text{h}\\phantom{0}\\; \\text{t}\\phantom{0} \\text{u}\\; \\\\\n  &_{3}\\;\\;\\; _{9}\\;\\;_{12}\\,_{12}\\, \\\\\n & \\cancel{4},\\cancel{0}\\,\\cancel{3}\\cancel{2} \\\\\n         - & 1\\;\\;\\,7\\;\\,8\\; \\\\\n    \\hline\n &3,\\phantom{0}8\\;\\;\\,5\\;\\,4\\;\\\\\n \\hline\n \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch05-b006",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.2 Addition and subtraction of large numbers",
      "h3": "Exercise 5.2: Add and subtract whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.2: Add and subtract whole numbers",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch05-b006-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.2 Addition and subtraction of large numbers",
      "h3": "Exercise 5.2: Add and subtract whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.2: Add and subtract whole numbers\n\n1. Add the following numbers.\n\n1. $9,000+800+70+6$\n2. $5,050+55+5+500$\n3. $2,804+1,999+3,333$\n4. $42+1,005+936+41$\n5. $909+9,090+9,009+9$",
    "answer_text": "1. $9,000+800+70+6$\n$$\n\\begin{array}{r r}\n& 9,000 \\\\\n+ & 800 \\\\\n+ & 70 \\\\\n+ & 6 \\\\\n\\hline\n&9,876\\\\\n\\hline\n\\end{array}\n$$\n\n2. $5,050+55+5+500$\n$$\n\\begin{array}{r r}\n&_{1\\space1} \\phantom{0}\\\\\n& 5,050 \\\\\n+ & 55 \\\\\n+ & 5 \\\\\n+ & 500 \\\\\n\\hline\n&5,610\\\\\n\\hline\n\\end{array}\n$$\n\n3. $2,804+1,999+3,333$\n$$\n\\begin{array}{r r}\n&_2\\; _1\\, _1 \\phantom{0}\\\\\n& 2,804 \\\\\n+ & 1,999 \\\\\n+ & 3,333 \\\\\n\\hline\n&8,136\\\\\n\\hline\n\\end{array}\n$$\n\n4. $42+1,005+936+41$\n$$\n\\begin{array}{r r}\n&_1\\;_1\\,_1\\phantom{0}\\\\\n& 42 \\\\\n+ & 1,005 \\\\\n+ & 936 \\\\\n+ & 41 \\\\\n\\hline\n&2,024\\\\\n\\hline\n\\end{array}\n$$\n\n5. $909+9,090+9,009+9$\n$$\n\\begin{array}{r r}\n&_1\\;_1\\,_2\\phantom{0}\\\\\n& 909 \\\\\n+ & 9,090 \\\\\n+ & 9,009 \\\\\n+ & 9 \\\\\n\\hline\n&19,017\\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch05-b006-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.2 Addition and subtraction of large numbers",
      "h3": "Exercise 5.2: Add and subtract whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.2: Add and subtract whole numbers\n\n2. Subtract the following numbers.\n\n1. $8,642-2,468$\n2. $1,723-958$\n3. $7,777-888$\n4. $10,000-8,734$\n5. $50,000-599$",
    "answer_text": "1. $8,642-2,468$\n$$\n\\begin{array}{r r}\n&_5\\,\\;_{13}\\,_{12}\\,\\\\\n& 8,\\cancel{6}\\cancel{4}\\cancel{2} \\\\\n- & 2,\\;4\\;\\;6\\;\\,8\\; \\\\\n\\hline\n& 6,\\;1\\;\\;7\\;\\,4\\;\\\\\n\\hline\n\\end{array}\n$$\n\n2. $1,723-958$\n$$\n\\begin{array}{r r}\n&_0\\;\\;\\; _{16}\\; _{11}\\, _{13}\\,\\\\\n& \\cancel{1},\\cancel{7}\\cancel{2}\\cancel{3} \\\\\n- & 9\\;\\;5\\;\\,8\\; \\\\\n\\hline\n& 7\\;\\;6\\;\\,5\\;\\\\\n\\hline\n\\end{array}\n$$\n\n3. $7,777-888$\n$$\n\\begin{array}{r r}\n&_6\\;\\;\\; _{16}\\; _{16}\\, _{17}\\,\\\\\n& \\cancel{7},\\cancel{7}\\cancel{7}\\cancel{7} \\\\\n- & 8\\;\\;8\\;\\,8\\; \\\\\n\\hline\n& 6,\\;\\;8\\;\\;8\\;\\,9\\;\\\\\n\\hline\n\\end{array}\n$$\n\n4. $10,000-8,734$\n$$\n\\begin{array}{r r}\n&_0\\;\\;\\;_9\\;\\;\\; _9\\;\\; _9\\;\\, _{10}\\,\\\\\n& \\cancel{1}\\cancel{0},\\cancel{0}\\cancel{0}\\cancel{0} \\\\\n- & 8,\\;\\;7\\;\\;3\\;\\,4\\; \\\\\n\\hline\n& 1,\\;\\;2\\;\\;6\\;\\,6\\;\\\\\n\\hline\n\\end{array}\n$$\n\n5. $50,000-599$\n$$\n\\begin{array}{r r}\n&_4\\;\\;\\;_9\\;\\;\\; _9\\;\\; _9\\;\\, _{10}\\,\\\\\n& \\cancel{5}\\cancel{0},\\cancel{0}\\cancel{0}\\cancel{0} \\\\\n- & 5\\;\\;9\\;\\,9\\; \\\\\n\\hline\n& 4\\;\\;9,\\;\\;4\\;\\;0\\;\\,1\\;\\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch05-b006-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.2 Addition and subtraction of large numbers",
      "h3": "Exercise 5.2: Add and subtract whole numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.2: Add and subtract whole numbers\n\n3. Determine the difference in the two place values of 5 in the following numbers.\n\nTo determine the difference between two numbers, subtract the smaller number from the larger number.\n\n1. 1,025,568\n2. 58,753\n3. 5,198,352",
    "answer_text": "1. 1,025,568\nThe place values are 5,000 and 500.\n$$\n\\begin{array}{r r}\n&_4 \\phantom{00} _{10}\\phantom{00}\\\\\n& \\cancel{5},\\cancel{0}00 \\\\\n- & 5\\;00 \\\\\n\\hline\n& 4\\,,\\;5\\;00\\\\\n\\hline\n\\end{array}\n$$\n\n2. 58,753\nThe place values are 50,000 and 50.\n$$\n\\begin{array}{r r}\n&_4\\;\\;\\,_9\\;\\;\\;\\, _{10}\\phantom{0}\\\\\n& \\cancel{5}\\cancel{0},\\cancel{0}\\cancel{0}0 \\\\\n- & 5\\;0 \\\\\n\\hline\n& 4\\;\\;9\\,,\\;9\\;5\\;0\\\\\n\\hline\n\\end{array}\n$$\n\n3. 5,198,352\nThe place values are 5,000,000 and 50.\n$$\n\\begin{array}{r r}\n&_4\\;\\;\\;_9\\;\\;\\,_9\\;\\; _9\\;\\;\\;\\; _9\\;\\; _{10}\\phantom{0}\\\\\n& \\cancel{5},\\cancel{0}\\cancel{0}\\cancel{0},\\cancel{0}\\cancel{0}0 \\\\\n- & 5\\;0 \\\\\n\\hline\n& 4,\\;\\;9\\;\\;9\\;\\;9\\;,\\;9\\;\\,5\\;0\\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values"
  },
  {
    "record_id": "ch05-b033",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.6 Summary",
      "h3": null
    },
    "content_text": "- The place value of a digit tells us what the value of that digit is, based on its position in a number.\n- When we add or subtract large numbers, we line up the units, tens, hundreds and thousands of the numbers.\n- A number line is a straight line, divided into equal segments, that shows the positions of numbers.\n- Positive numbers are larger than zero and lie to the right of zero on a number line.\n- Negative numbers are smaller than zero and lie to the left of zero on a number line.\n- Zero is neither positive nor negative.\n- The symbol < means \"smaller than\", and 3<5 means three is smaller than five. The symbol > means \"greater than\", and 5>3 means five is greater than three.\n- When we add one integer to another, we may see it as units that are added along the number line. When we add positive numbers, we count to the right on a number line. When we add negative numbers, we count to the left on a number line.\n- Subtracting a number is the same as adding the \"opposite\" of the number. For example, $2-7$ is the same as $2+(-7)$.\n- Subtraction may also be seen as the difference between two numbers. For example, there are 5 units between the numbers 2 and 7. If the number which is subtracted from lies to the negative side of the number that is subtracted, the difference is negative: $2-7=-5$. If the number which is subtracted from lies to the positive side of the number that is subtracted, the difference is positive: $7-2=5$.\n- A thermometer is an instrument used to measure temperature. Temperatures above $0\\space ^\\circ\\text C$ are positive. Temperatures below $0\\space ^\\circ\\text C$ are negative.\n- A positive bank balance means you have money in the bank. A negative bank balance means you owe the bank money.\n- For movement along a straight line, we take one direction as positive. The opposite direction is negative.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
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
