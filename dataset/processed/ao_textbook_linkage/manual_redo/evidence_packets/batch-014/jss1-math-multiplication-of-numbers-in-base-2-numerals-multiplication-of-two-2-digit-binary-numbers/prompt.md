# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-2",
  "topic_key": "jss1-math-multiplication-of-numbers-in-base-2-numerals",
  "topic": "Multiplication of Numbers in Base 2 Numerals",
  "subtopic_id": "jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers",
  "subtopic_title": "Multiplication of two 2-digit binary numbers",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers-po01",
        "source_performance_objective_index": 1,
        "text": "Multiply two 2-digit binary numbers"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "multiplication-of-binary-numbers-ao-multiply-two-2-digit-binary-numbers",
          "text": "Multiply two 2-digit binary numbers."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch08-b018",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.3 Multiplication",
      "h3": null
    },
    "content_text": "Last year you learnt how to multiply integers using long multiplication. We use the same principles when\nmultiplying numbers in the base two number system.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b019",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.3 Multiplication",
      "h3": "Worked example 8.7: Revision of multiplication in the base ten number system"
    },
    "content_text": "",
    "prompt_text": "Multiply 32 by 14.",
    "answer_text": "Step 1: Write the numbers one below the other. Line up the units, tens, hundreds, and so on.\n\n$$\n\\begin{array}{r r}\n & \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n & 3\\,2 \\\\\n \\times & 1\\,4 \\\\\n \\hline\n\\end{array}\n$$\n\nStep 2: Multiply the first (top) number by the units of the second number.\n\n$$\n\\begin{array}{r r}\n & \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n & 3\\,2 \\\\\n \\times & 1\\,\\color{red}{4} \\\\\n \\hline\n & 1\\,2\\,8\n\\end{array}\n$$\n\nStep 3: Start a new line. Insert a zero in the units column.\n\n$$\n\\begin{array}{r r}\n & \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n & 3\\,2 \\\\\n \\times & 1\\,4 \\\\\n \\hline\n & 1\\,2\\,8 \\\\\n & 0\n\\end{array}\n$$\n\nStep 4: Multiply the first (top) number by the tens of the second number.\n\n$$\n\\begin{array}{r r}\n & \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n & 3\\,2 \\\\\n \\times & \\color{red}{1}\\, \\color{black}{4} \\\\\n \\hline\n & 1\\,2\\,8 \\\\\n & 3\\,2\\,0\n\\end{array}\n$$\n\nStep 5: Add the two numbers from Step 4.\n\n$$\n\\begin{array}{r r}\n & \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n & 3\\,2 \\\\\n \\times & 1\\, 4 \\\\\n \\hline\n & 1\\,2\\,8 \\\\\n & 3\\,2\\,0 \\\\\n \\hline\n & 4\\,4\\,8 \\\\\n \\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b020",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.3 Multiplication",
      "h3": null
    },
    "content_text": "Multiplication of the digits 0 and 1 work the same in the base ten and base two number systems:\n\n$0\\times0=0$\n\n$1\\times0=0$\n\n$0\\times1=0$\n\n$1\\times1=1$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b021",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.3 Multiplication",
      "h3": "Worked example 8.8: Multiplication in the base two number system"
    },
    "content_text": "",
    "prompt_text": "Multiply $11_\\text{two}$ by $11_\\text{two}$.",
    "answer_text": "Step 1: Write the numbers one below the other, without the subscript \"two\". Line up the units ($2^0$), twos ($2^1$), fours ($2^2$), eights ($2^3$), and so on.\n\n$$\n\\begin{array}{r r}\n & \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n & 1\\;\\;1\\;\\, \\\\\n \\times& 1\\;\\;1\\;\\, \\\\\n \\hline\n\\end{array}\n$$\n\nStep 2: Multiply the first (top) number by the units of the second number.\n\n$$\n\\begin{array}{r r}\n & \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n & 1\\;\\;1\\;\\, \\\\\n \\times& 1\\;\\;\\color{red}{1}\\;\\, \\\\\n \\hline\n & 1\\;\\;1\\;\\, \n\\end{array}\n$$\n\nStep 3: Start a new line. Insert a zero in the units ($2^0$) column.\n\n$$\n\\begin{array}{r r}\n & \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n & 1\\;\\;1\\;\\, \\\\\n \\times& 1\\;\\;\\color{red}{1}\\;\\, \\\\\n \\hline\n & 1\\;\\;1\\;\\, \\\\\n & 0 \\;\\,\n\\end{array}\n$$\n\nStep 4: Multiply the first (top) number by the twos ($2^1$) of the second number.\n\n$$\n\\begin{array}{r r}\n & \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n & 1\\;\\;1\\;\\, \\\\\n \\times& \\color{red}{1} \\;\\;\\color{black}{1}\\;\\, \\\\\n \\hline\n & 1\\;\\;1\\;\\, \\\\\n & 1\\;\\;1\\;\\;0 \\;\\,\n\\end{array}\n$$\n\nStep 5: Add the two numbers from Step 4.\n\nThis adding step in a multiplication works differently in the base two number system. You need to use the base two addition rules: $1+1=10$ and $1+1+1=11$.\n\nIf the answer in any column is 10 or 11, carry over the left-hand 1 and write down the right-hand 0 or 1.\n\n$$\n\\begin{array}{r r}\n & \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n & 1\\;\\;1\\;\\, \\\\\n \\times& 1 \\;\\; 1\\;\\, \\\\\n \\hline\n & 1\\;\\;1\\;\\, \\\\\n & ^1\\;^1 1\\;\\;1\\;\\;0 \\;\\, \\\\\n \\hline\n & 1\\;\\;0\\;\\;0\\;\\;1\\;\\, \\\\\n \\hline\n\\end{array}\n$$\n\nStep 6: Check your answer using the base ten number system.\n\n$$\n\\begin{align}\n11_2&=2^1+2^0 \\\\\n&=2+1 \\\\\n&=3_{10}\\\\\n\\end{align}\n$$\n\n$$\\quad$$\n\n$$3 \\times 3 = 9$$\n\n$$\\quad$$\n\n$$\n\\begin{align}\n9_{10}&=8+1 \\\\\n&=2^3+0+0+2^0 \\\\\n&=1001_2\\\\\n\\end{align}\n$$\n\nThe answer is correct.",
    "primary_subtopic_id": "jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b022",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.3 Binary multiplication",
      "h3": "Exercise 8.3: Multiply binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.3: Multiply binary numbers\n\nCalculate each of the following in the base two number system.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b022-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.3 Binary multiplication",
      "h3": "Exercise 8.3: Multiply binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.3: Multiply binary numbers\n\n1. 10 \\times 10",
    "answer_text": "$$\n\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n& 1\\;\\;0\\;\\, \\\\\n\\times& 1 \\;\\; 0\\;\\, \\\\\n\\hline\n& 0\\;\\;0\\;\\, \\\\\n& 1\\;\\;0\\;\\;0 \\;\\, \\\\\n\\hline\n& 1\\;\\;0\\;\\;0\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b022-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.3 Binary multiplication",
      "h3": "Exercise 8.3: Multiply binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.3: Multiply binary numbers\n\n2. 10 \\times 11",
    "answer_text": "$$\n\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n& 1\\;\\;0\\;\\, \\\\\n\\times& 1 \\;\\; 1\\;\\, \\\\\n\\hline\n& 1\\;\\;0\\;\\, \\\\\n& 1\\;\\;0\\;\\;0 \\;\\, \\\\\n\\hline\n& 1\\;\\;1\\;\\;0\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b022-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.3 Binary multiplication",
      "h3": "Exercise 8.3: Multiply binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.3: Multiply binary numbers\n\n3. 100 \\times 10",
    "answer_text": "$$\n\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n& 1\\;\\;0\\;\\;0\\;\\, \\\\\n\\times& 1 \\;\\; 0\\;\\, \\\\\n\\hline\n& 0\\;\\;0\\;\\;0\\;\\, \\\\\n& 1\\;\\;0\\;\\;0\\;\\;0 \\;\\, \\\\\n\\hline\n& 1\\;\\;0\\;\\;0\\;\\;0\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b022-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.3 Binary multiplication",
      "h3": "Exercise 8.3: Multiply binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.3: Multiply binary numbers\n\n4. 110 \\times 11",
    "answer_text": "$$\n\\begin{array}{r r}\n& \\color{blue}{2^4 \\,2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n& 1\\;\\;1\\;\\;0\\;\\, \\\\\n\\times& 1 \\;\\; 1\\;\\, \\\\\n\\hline\n& 1\\;\\;1\\;\\;0\\;\\, \\\\\n& ^1 \\;^1 1\\;\\;1\\;\\;0\\;\\;0 \\;\\, \\\\\n\\hline\n& 1\\;\\;0\\;\\;0\\;\\;1\\;\\;0\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b022-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.3 Binary multiplication",
      "h3": "Exercise 8.3: Multiply binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.3: Multiply binary numbers\n\n5. 111 \\times 11",
    "answer_text": "$$\n\\begin{array}{r r}\n& \\color{blue}{2^4 \\,2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n& 1\\;\\;1\\;\\;1\\;\\, \\\\\n\\times& 1 \\;\\; 1\\;\\, \\\\\n\\hline\n& ^1 1\\;\\;1\\;\\;1\\;\\, \\\\\n& ^1 \\;^1 1\\;\\;1\\;\\;1\\;\\;0 \\;\\, \\\\\n\\hline\n& 1\\;\\;0\\;\\;1\\;\\;0\\;\\;1\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b023",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.4 Summary",
      "h3": null
    },
    "content_text": "From Chapter 3 you know that:\n- 2_\\text{ten}=10_\\text{two}\n- 3_\\text{ten}=11_\\text{two}\n\nUse the following basic rules when adding binary numbers:\n- 0+0=0\n- 0+1=1\n- 1+0=1\n- 1+1=10\n- 1+1+1=11\n\nUse the following basic rules when subtracting binary numbers:\n- 0-0=0\n- 1-0=0\n- 1-1=0\n- 10-1=1\n- 11-1=10\n\nMultiplication of the digits 0 and 1 work the same in the base ten and base two number systems:\n- 0\\times0=0\n- 1\\times0=0\n- 0\\times1=0\n- 1\\times1=1\n\nThe adding step in a multiplication works differently in the base two number system, because you need to use the base two addition rules.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
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
  "topic_key": "jss1-math-multiplication-of-numbers-in-base-2-numerals",
  "topic": "Multiplication of Numbers in Base 2 Numerals",
  "subtopic_id": "jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers",
  "subtopic_title": "Multiplication of two 2-digit binary numbers",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers-po01",
        "source_performance_objective_index": 1,
        "text": "Multiply two 2-digit binary numbers"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "multiplication-of-binary-numbers-ao-multiply-two-2-digit-binary-numbers",
          "text": "Multiply two 2-digit binary numbers."
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
    "record_id": "ch08-b018",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.3 Multiplication",
      "h3": null
    },
    "content_text": "Last year you learnt how to multiply integers using long multiplication. We use the same principles when\nmultiplying numbers in the base two number system.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b019",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.3 Multiplication",
      "h3": "Worked example 8.7: Revision of multiplication in the base ten number system"
    },
    "content_text": "",
    "prompt_text": "Multiply 32 by 14.",
    "answer_text": "Step 1: Write the numbers one below the other. Line up the units, tens, hundreds, and so on.\n\n$$\n\\begin{array}{r r}\n & \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n & 3\\,2 \\\\\n \\times & 1\\,4 \\\\\n \\hline\n\\end{array}\n$$\n\nStep 2: Multiply the first (top) number by the units of the second number.\n\n$$\n\\begin{array}{r r}\n & \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n & 3\\,2 \\\\\n \\times & 1\\,\\color{red}{4} \\\\\n \\hline\n & 1\\,2\\,8\n\\end{array}\n$$\n\nStep 3: Start a new line. Insert a zero in the units column.\n\n$$\n\\begin{array}{r r}\n & \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n & 3\\,2 \\\\\n \\times & 1\\,4 \\\\\n \\hline\n & 1\\,2\\,8 \\\\\n & 0\n\\end{array}\n$$\n\nStep 4: Multiply the first (top) number by the tens of the second number.\n\n$$\n\\begin{array}{r r}\n & \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n & 3\\,2 \\\\\n \\times & \\color{red}{1}\\, \\color{black}{4} \\\\\n \\hline\n & 1\\,2\\,8 \\\\\n & 3\\,2\\,0\n\\end{array}\n$$\n\nStep 5: Add the two numbers from Step 4.\n\n$$\n\\begin{array}{r r}\n & \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n & 3\\,2 \\\\\n \\times & 1\\, 4 \\\\\n \\hline\n & 1\\,2\\,8 \\\\\n & 3\\,2\\,0 \\\\\n \\hline\n & 4\\,4\\,8 \\\\\n \\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b020",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.3 Multiplication",
      "h3": null
    },
    "content_text": "Multiplication of the digits 0 and 1 work the same in the base ten and base two number systems:\n\n$0\\times0=0$\n\n$1\\times0=0$\n\n$0\\times1=0$\n\n$1\\times1=1$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b021",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.3 Multiplication",
      "h3": "Worked example 8.8: Multiplication in the base two number system"
    },
    "content_text": "",
    "prompt_text": "Multiply $11_\\text{two}$ by $11_\\text{two}$.",
    "answer_text": "Step 1: Write the numbers one below the other, without the subscript \"two\". Line up the units ($2^0$), twos ($2^1$), fours ($2^2$), eights ($2^3$), and so on.\n\n$$\n\\begin{array}{r r}\n & \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n & 1\\;\\;1\\;\\, \\\\\n \\times& 1\\;\\;1\\;\\, \\\\\n \\hline\n\\end{array}\n$$\n\nStep 2: Multiply the first (top) number by the units of the second number.\n\n$$\n\\begin{array}{r r}\n & \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n & 1\\;\\;1\\;\\, \\\\\n \\times& 1\\;\\;\\color{red}{1}\\;\\, \\\\\n \\hline\n & 1\\;\\;1\\;\\, \n\\end{array}\n$$\n\nStep 3: Start a new line. Insert a zero in the units ($2^0$) column.\n\n$$\n\\begin{array}{r r}\n & \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n & 1\\;\\;1\\;\\, \\\\\n \\times& 1\\;\\;\\color{red}{1}\\;\\, \\\\\n \\hline\n & 1\\;\\;1\\;\\, \\\\\n & 0 \\;\\,\n\\end{array}\n$$\n\nStep 4: Multiply the first (top) number by the twos ($2^1$) of the second number.\n\n$$\n\\begin{array}{r r}\n & \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n & 1\\;\\;1\\;\\, \\\\\n \\times& \\color{red}{1} \\;\\;\\color{black}{1}\\;\\, \\\\\n \\hline\n & 1\\;\\;1\\;\\, \\\\\n & 1\\;\\;1\\;\\;0 \\;\\,\n\\end{array}\n$$\n\nStep 5: Add the two numbers from Step 4.\n\nThis adding step in a multiplication works differently in the base two number system. You need to use the base two addition rules: $1+1=10$ and $1+1+1=11$.\n\nIf the answer in any column is 10 or 11, carry over the left-hand 1 and write down the right-hand 0 or 1.\n\n$$\n\\begin{array}{r r}\n & \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n & 1\\;\\;1\\;\\, \\\\\n \\times& 1 \\;\\; 1\\;\\, \\\\\n \\hline\n & 1\\;\\;1\\;\\, \\\\\n & ^1\\;^1 1\\;\\;1\\;\\;0 \\;\\, \\\\\n \\hline\n & 1\\;\\;0\\;\\;0\\;\\;1\\;\\, \\\\\n \\hline\n\\end{array}\n$$\n\nStep 6: Check your answer using the base ten number system.\n\n$$\n\\begin{align}\n11_2&=2^1+2^0 \\\\\n&=2+1 \\\\\n&=3_{10}\\\\\n\\end{align}\n$$\n\n$$\\quad$$\n\n$$3 \\times 3 = 9$$\n\n$$\\quad$$\n\n$$\n\\begin{align}\n9_{10}&=8+1 \\\\\n&=2^3+0+0+2^0 \\\\\n&=1001_2\\\\\n\\end{align}\n$$\n\nThe answer is correct.",
    "primary_subtopic_id": "jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b022",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.3 Binary multiplication",
      "h3": "Exercise 8.3: Multiply binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.3: Multiply binary numbers\n\nCalculate each of the following in the base two number system.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b022-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.3 Binary multiplication",
      "h3": "Exercise 8.3: Multiply binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.3: Multiply binary numbers\n\n1. 10 \\times 10",
    "answer_text": "$$\n\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n& 1\\;\\;0\\;\\, \\\\\n\\times& 1 \\;\\; 0\\;\\, \\\\\n\\hline\n& 0\\;\\;0\\;\\, \\\\\n& 1\\;\\;0\\;\\;0 \\;\\, \\\\\n\\hline\n& 1\\;\\;0\\;\\;0\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b022-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.3 Binary multiplication",
      "h3": "Exercise 8.3: Multiply binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.3: Multiply binary numbers\n\n2. 10 \\times 11",
    "answer_text": "$$\n\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n& 1\\;\\;0\\;\\, \\\\\n\\times& 1 \\;\\; 1\\;\\, \\\\\n\\hline\n& 1\\;\\;0\\;\\, \\\\\n& 1\\;\\;0\\;\\;0 \\;\\, \\\\\n\\hline\n& 1\\;\\;1\\;\\;0\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b022-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.3 Binary multiplication",
      "h3": "Exercise 8.3: Multiply binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.3: Multiply binary numbers\n\n3. 100 \\times 10",
    "answer_text": "$$\n\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n& 1\\;\\;0\\;\\;0\\;\\, \\\\\n\\times& 1 \\;\\; 0\\;\\, \\\\\n\\hline\n& 0\\;\\;0\\;\\;0\\;\\, \\\\\n& 1\\;\\;0\\;\\;0\\;\\;0 \\;\\, \\\\\n\\hline\n& 1\\;\\;0\\;\\;0\\;\\;0\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b022-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.3 Binary multiplication",
      "h3": "Exercise 8.3: Multiply binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.3: Multiply binary numbers\n\n4. 110 \\times 11",
    "answer_text": "$$\n\\begin{array}{r r}\n& \\color{blue}{2^4 \\,2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n& 1\\;\\;1\\;\\;0\\;\\, \\\\\n\\times& 1 \\;\\; 1\\;\\, \\\\\n\\hline\n& 1\\;\\;1\\;\\;0\\;\\, \\\\\n& ^1 \\;^1 1\\;\\;1\\;\\;0\\;\\;0 \\;\\, \\\\\n\\hline\n& 1\\;\\;0\\;\\;0\\;\\;1\\;\\;0\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b022-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.3 Binary multiplication",
      "h3": "Exercise 8.3: Multiply binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.3: Multiply binary numbers\n\n5. 111 \\times 11",
    "answer_text": "$$\n\\begin{array}{r r}\n& \\color{blue}{2^4 \\,2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n& 1\\;\\;1\\;\\;1\\;\\, \\\\\n\\times& 1 \\;\\; 1\\;\\, \\\\\n\\hline\n& ^1 1\\;\\;1\\;\\;1\\;\\, \\\\\n& ^1 \\;^1 1\\;\\;1\\;\\;1\\;\\;0 \\;\\, \\\\\n\\hline\n& 1\\;\\;0\\;\\;1\\;\\;0\\;\\;1\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b023",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.4 Summary",
      "h3": null
    },
    "content_text": "From Chapter 3 you know that:\n- 2_\\text{ten}=10_\\text{two}\n- 3_\\text{ten}=11_\\text{two}\n\nUse the following basic rules when adding binary numbers:\n- 0+0=0\n- 0+1=1\n- 1+0=1\n- 1+1=10\n- 1+1+1=11\n\nUse the following basic rules when subtracting binary numbers:\n- 0-0=0\n- 1-0=0\n- 1-1=0\n- 10-1=1\n- 11-1=10\n\nMultiplication of the digits 0 and 1 work the same in the base ten and base two number systems:\n- 0\\times0=0\n- 1\\times0=0\n- 0\\times1=0\n- 1\\times1=1\n\nThe adding step in a multiplication works differently in the base two number system, because you need to use the base two addition rules.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
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
