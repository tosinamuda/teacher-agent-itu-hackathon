# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-2",
  "topic_key": "jss1-math-addition-of-numbers-in-base-2-numerals",
  "topic": "Addition of Numbers in Base 2 Numerals",
  "subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers",
  "subtopic_title": "Addition of two or three 3-digit binary numbers",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers-po01",
        "source_performance_objective_index": 1,
        "text": "Add two or three 3-digit binary numbers"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "addition-of-binary-numbers-ao-add-two-or-three-3-digit-binary-numbers",
          "text": "Add two or three 3-digit binary numbers."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch08-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": null,
      "h3": null
    },
    "content_text": "In Chapter 3 you learnt about the base two number system. The base two or binary number system counts in groups of 2, and uses only the digits 0 and 1 to represent any number. The numbers in the base two number system are called binary numbers.\n\nWe can use place value tables in the base two number system. The place values are powers of 2. For example:\n\n$$\n\\begin{array}{|c|c|c|c|c|c|}\n    \\hline\n    \\text{thirty twos} & \\text{sixteens} & \\text{eights} & \\text{fours} & \\text{twos} & \\text{units} \\\\\n    (2^5) & (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n    \\hline\n    &  &  & & & \\\\\n    \\hline\n    \\end{array}\n$$\n\nThe binary numbers that correspond to the decimal numbers 1 to 10 are:\n\n$$\n\\begin{array}{|c|c|}\n    \\hline\n    \\text{decimal number} & \\text{binary number} \\\\\n    \\hline\n    1& 1 \\\\\n    2& 10 \\\\\n    3& 11 \\\\\n    4& 100 \\\\\n    5& 101 \\\\\n    6& 110 \\\\\n    7& 111 \\\\\n    8& 1000 \\\\\n    9& 1001 \\\\\n    10& 1010 \\\\\n    \\hline\n    \\end{array}\n$$\n\nWe use subscripts to tell us which system a certain combination of digits belong to. For example:\n- $100_{10}$ or $100_{\\text{ten}}$ means one hundred\n- $100_2$ or $100_{\\text{two}}$ means four\n\nIn this chapter you will learn how to add, subtract and multiply binary numbers.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch08-b002",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": null
    },
    "content_text": "When we add binary numbers, we follow the same principles as when we add numbers in the base ten number system.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b003",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Worked example 8.1: Revision of addition in the base ten number system"
    },
    "content_text": "",
    "prompt_text": "Find the total of $794+648+89$.",
    "answer_text": "Step 1: Write the numbers one below the other. Line up the units, tens, hundreds, thousands, and so on.\n$$\\begin{array}{r r}\n & \\text{th}\\, \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n & 7\\,9\\,4 \\\\\n +& 6\\,4\\,8 \\\\\n +& 8\\,9 \\\\\n \\hline\n \\end{array}$$\nStep 2: Add the units. Divide the answer by 10. Carry over the quotient and write down the remainder.\nRemember that the quotient is the result you get after you have divided.\n$$4+8+9=21$$\n$$21=(2\\times10)+1$$\n$$\\begin{array}{r r}\n & \\text{th}\\, \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n &_{2} &\\phantom{0}\\\\\n & 7\\,9\\,4 \\\\\n +& 6\\,4\\,8 \\\\\n +& 8\\,9 \\\\\n \\hline\n &1\\\\\n \\hline\n \\end{array}$$\nStep 3: Repeat Step 2 for the tens column.\n$$2+9+4+8=23$$\n$$23=(2\\times10)+3$$\n$$\\begin{array}{r r}\n & \\text{th}\\, \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n &_{2}\\,_{2} &\\phantom{0}\\\\\n & 7\\,9\\,4 \\\\\n +& 6\\,4\\,8 \\\\\n +& 8\\,9 \\\\\n \\hline\n &3\\,1\\\\\n \\hline\n \\end{array}$$\nStep 4: Repeat Step 3 for the hundreds column.\n$$2+7+6=15$$\n$$15=(1\\times10)+5$$\n$$\\begin{array}{r r}\n & \\text{th}\\, \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n &_{1}\\,_{2}\\,_{2} &\\phantom{0}\\\\\n & 7\\,9\\,4 \\\\\n +& 6\\,4\\,8 \\\\\n +& 8\\,9 \\\\\n \\hline\n &5\\,3\\,1\\\\\n \\hline\n \\end{array}$$\nStep 5: Bring down the quotient that was carried over to the thousands column.\n$$\\begin{array}{r r}\n & \\text{th}\\, \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n &_{1}\\,_{2}\\,_{2} &\\phantom{0}\\\\\n & 7\\,9\\,4 \\\\\n +& 6\\,4\\,8 \\\\\n +& 8\\,9 \\\\\n \\hline\n &1,\\,5\\,3\\,1\\\\\n \\hline\n \\end{array}$$\nThe answer is 1,531.",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b004",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": null
    },
    "content_text": "In the base two number system, we work in groups of 2. So, instead of dividing by 10, we divide by 2.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b005",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Worked example 8.2: Addition in the base two number system (Method 1)"
    },
    "content_text": "",
    "prompt_text": "Find the sum of $101_\\text{two}$ and $111_\\text{two}$.",
    "answer_text": "Step 1: Write the numbers one below the other, without the subscript \"two\". Line up the units ($2^0$), twos ($2^1$), fours ($2^2$) and eights ($2^3$).\n$$\\begin{array}{r r}\n & \\color{blue}{2^3 \\; 2^2 \\; 2^1 \\; 2^0 }\\\\\n & 1\\;\\;0\\;\\;1\\;\\, \\\\\n +& 1\\;\\;1\\;\\;1\\;\\, \\\\\n \\hline\n \\end{array}$$\nStep 2: Add the units (in the $2^0$ column). Divide the answer by 2. Carry over the quotient and write down the remainder.\n$$1+1=2$$\n$$2=(1\\times2)+0$$\n$$\\begin{array}{r r}\n & \\color{blue}{2^3 \\; 2^2 \\; 2^1 \\; 2^0 }\\\\\n &_{1} \\phantom{000}\\\\\n & 1\\;\\;0\\;\\;1\\;\\, \\\\\n +& 1\\;\\;1\\;\\;1\\;\\, \\\\\n \\hline\n & 0\\;\\, \\\\\n \\hline\n \\end{array}$$\nStep 3: Repeat Step 2 for the twos ($2^1$) column.\n$$1+1=2$$\n$$2=(1\\times2)+0$$\n$$\\begin{array}{r r}\n & \\color{blue}{2^3 \\; 2^2 \\; 2^1 \\; 2^0 }\\\\\n &_{1}\\;\\;_{1} \\phantom{000}\\\\\n & 1\\;\\;0\\;\\;1\\;\\, \\\\\n +& 1\\;\\;1\\;\\;1\\;\\, \\\\\n \\hline\n & 0\\;\\;0\\;\\, \\\\\n \\hline\n \\end{array}$$\nStep 4: Repeat Step 3 for the fours ($2^2$) column.\n$$1+1+1=3$$\n$$3=(1\\times2)+1$$\n$$\\begin{array}{r r}\n & \\color{blue}{2^3 \\; 2^2 \\; 2^1 \\; 2^0 }\\\\\n &_{1}\\;\\;_{1}\\;\\;_{1} \\phantom{000}\\\\\n & 1\\;\\;0\\;\\;1\\;\\, \\\\\n +& 1\\;\\;1\\;\\;1\\;\\, \\\\\n \\hline\n & 1\\;\\;0\\;\\;0\\;\\, \\\\\n \\hline\n \\end{array}$$\nStep 5: Bring down the quotient that was carried over to the eights ($2^3$) column.\n$$\\begin{array}{r r}\n & \\color{blue}{2^3 \\; 2^2 \\; 2^1 \\; 2^0 }\\\\\n &_{1}\\;\\;_{1}\\;\\;_{1} \\phantom{000}\\\\\n & 1\\;\\;0\\;\\;1\\;\\, \\\\\n +& 1\\;\\;1\\;\\;1\\;\\, \\\\\n \\hline\n &1\\;\\; 1\\;\\;0\\;\\;0\\;\\, \\\\\n \\hline\n \\end{array}$$\nThe answer is $1100_\\text{two}$.\nStep 6: Check your answer by converting to the base ten number system, adding, and then converting back to a base two number.\n$$\\begin{align}\n101_2&=2^2+0+2^0 \\\\\n&=4+1 \\\\\n&=5_{10}\\\\\n\\end{align}$$\n$$\\begin{align}\n111_2&=2^2+2^1+2^0 \\\\\n&=4+2+1 \\\\\n&=7_{10}\\\\\n\\end{align}$$\n$$5+7=12$$\n$$\\begin{align}\n12_{10}&=8+4 \\\\\n&=2^3+2^2+0+0 \\\\\n&=1100_2\\\\\n\\end{align}$$\nThe answer is correct.",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b006",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": null
    },
    "content_text": "Another way to do addition in the base two number system is to use these basic rules:\n\n0+0=0\n0+1=1\n1+0=1\n1+1=10\n1+1+1=11",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b007",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": null
    },
    "content_text": "Remember:\n\n$2_\\text{ten}=10_\\text{two}$\n$3_\\text{ten}=11_\\text{two}$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b008",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Worked example 8.3: Addition in the base two number system (Method 2)"
    },
    "content_text": "",
    "prompt_text": "Find the sum of $101_\\text{two}$ and $111_\\text{two}$.",
    "answer_text": "Step 1: Write the numbers one below the other, without the subscript \"two\". Line up the units ($2^0$), twos ($2^1$), fours ($2^2$) and eights ($2^3$).\n\n$$\n\\\begin{array}{r r}\n & \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n & 1\\;\\;0\\;\\;1\\;\\, \\\\\n +& 1\\;\\;1\\;\\;1\\;\\, \\\\\n \\hline\n \\end{array}\n$$\n\nStep 2: Add the units in the base two number system. If the answer is 10 or 11, carry over the left-hand 1 and write down the right-hand 0 or 1.\n\nRemember to use $1+1=10$ and $1+1+1=11$.\n\n$$\n\\\begin{array}{r r}\n & \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n &_{1} \\phantom{000}\\\\\n & 1\\;\\;0\\;\\;1\\;\\, \\\\\n +& 1\\;\\;1\\;\\;1\\;\\, \\\\\n \\hline\n & 0\\;\\, \\\\\n \\hline\n \\end{array}\n$$\n\nStep 3: Repeat Step 2 for the twos ($2^1$) column.\n\n$$1+1=10$$\n\n$$\n\\\begin{array}{r r}\n & \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n &_{1}\\;\\;_{1} \\phantom{000}\\\\\n & 1\\;\\;0\\;\\;1\\;\\, \\\\\n +& 1\\;\\;1\\;\\;1\\;\\, \\\\\n \\hline\n & 0\\;\\;0\\;\\, \\\\\n \\hline\n \\end{array}\n$$\n\nStep 4: Repeat Step 3 for the fours ($2^2$) column.\n\n$$1+1+1=11$$\n\n$$\n\\\begin{array}{r r}\n & \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n &_{1}\\;\\;_{1}\\;\\;_{1} \\phantom{000}\\\\\n & 1\\;\\;0\\;\\;1\\;\\, \\\\\n +& 1\\;\\;1\\;\\;1\\;\\, \\\\\n \\hline\n & 1\\;\\;0\\;\\;0\\;\\, \\\\\n \\hline\n \\end{array}\n$$\n\nStep 5: Bring down the one that was carried over to the eights ($2^3$) column.\n\n$$\n\\\begin{array}{r r}\n & \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n &_{1}\\;\\;_{1}\\;\\;_{1} \\phantom{000}\\\\\n & 1\\;\\;0\\;\\;1\\;\\, \\\\\n +& 1\\;\\;1\\;\\;1\\;\\, \\\\\n \\hline\n &1\\;\\; 1\\;\\;0\\;\\;0\\;\\, \\\\\n \\hline\n \\end{array}\n$$\n\nThe answer is $1100_\\text{two}$.\n\nStep 6: Check your answer using the base ten number system.\n\n$$\n\\\begin{align}\n101_2&=2^2+0+2^0 \\\\\n&=4+1 \\\\\n&=5_{10}\\\\\n\\end{align}\n$$\n$$\\quad$$\n$$\n\\\begin{align}\n111_2&=2^2+2^1+2^0 \\\\\n&=4+2+1 \\\\\n&=7_{10}\\\\\n\\end{align}\n$$\n$$\\quad$$\n$$5+7=12$$\n$$\\quad$$\n$$\n\\\begin{align}\n12_{10}&=8+4 \\\\\n&=2^3+2^2+0+0 \\\\\n&=1100_2\\\\\n\\end{align}\n$$\n\nThe answer is correct.",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b009",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Exercise 8.1: Add binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.1: Add binary numbers\n\nCalculate each of the following in the base two number system.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b009-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Exercise 8.1: Add binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.1: Add binary numbers\n\n1. $$100+10$$",
    "answer_text": "$$\n\\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n& \\phantom{000}\\newline\n& 1\\;\\;0\\;\\;0\\;\\, \\\\\n+& 1\\;\\;0\\;\\, \\\\\n\\hline\n&1\\;\\; 1\\;\\;0\\;\\;0\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b009-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Exercise 8.1: Add binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.1: Add binary numbers\n\n2. $$101+11$$",
    "answer_text": "Remember to use $1+1=10$ where you need to.\n\n$$\n\\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n&_{1}\\;\\;_{1}\\;\\;_{1} \\phantom{000}\\newline\n& 1\\;\\;0\\;\\;1\\;\\, \\\\\n+& 1\\;\\;1\\;\\, \\\\\n\\hline\n&1\\;\\; 0\\;\\;0\\;\\;0\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b009-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Exercise 8.1: Add binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.1: Add binary numbers\n\n3. $$110+11$$",
    "answer_text": "$$\n\\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n&_{1}\\;\\;_{1} \\phantom{00000}\\newline\n& 1\\;\\;1\\;\\;0\\;\\, \\\\\n+& 1\\;\\;1\\;\\, \\\\\n\\hline\n&1\\;\\; 0\\;\\;0\\;\\;1\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b009-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Exercise 8.1: Add binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.1: Add binary numbers\n\n4. $$111+10$$",
    "answer_text": "$$\n\\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n&_{1}\\;\\;_{1} \\phantom{00000}\\newline\n& 1\\;\\;1\\;\\;1\\;\\, \\\\\n+& 1\\;\\;0\\;\\, \\\\\n\\hline\n&1\\;\\; 0\\;\\;0\\;\\;1\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b009-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Exercise 8.1: Add binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.1: Add binary numbers\n\n5. $$100+101$$",
    "answer_text": "$$\n\\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n&_{1}\\;\\;\\phantom{000000}\\newline\n& 1\\;\\;0\\;\\;0\\;\\, \\\\\n+& 1\\;\\;0\\;\\;1\\;\\, \\\\\n\\hline\n&1\\;\\; 0\\;\\;0\\;\\;1\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b009-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Exercise 8.1: Add binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.1: Add binary numbers\n\n6. $$101+110$$",
    "answer_text": "$$\n\\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n&_{1}\\;\\;\\phantom{000000}\\newline\n& 1\\;\\;0\\;\\;1\\;\\, \\\\\n+& 1\\;\\;1\\;\\;0\\;\\, \\\\\n\\hline\n&1\\;\\; 0\\;\\;1\\;\\;1\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b009-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Exercise 8.1: Add binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.1: Add binary numbers\n\n7. $$110+111$$",
    "answer_text": "Remember to use $1+1=10$ and $1+1+1=11$ where you need to.\n\n$$\n\\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n&_{1}\\;\\;_{1}\\phantom{00000}\\newline\n& 1\\;\\;1\\;\\;0\\;\\, \\\\\n+& 1\\;\\;1\\;\\;1\\;\\, \\\\\n\\hline\n&1\\;\\; 1\\;\\;0\\;\\;1\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b009-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Exercise 8.1: Add binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.1: Add binary numbers\n\n8. $$111+111$$",
    "answer_text": "$$\n\\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n&_{1}\\;\\;_{1}\\;\\;_{1}\\phantom{000}\\newline\n& 1\\;\\;1\\;\\;1\\;\\, \\\\\n+& 1\\;\\;1\\;\\;1\\;\\, \\\\\n\\hline\n&1\\;\\; 1\\;\\;1\\;\\;0\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b009-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Exercise 8.1: Add binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.1: Add binary numbers\n\n9. $$1010+11$$",
    "answer_text": "$$\n\\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n&_{1}\\phantom{00000}\\newline\n& 1\\;\\;0\\;\\;1\\;\\;0\\;\\, \\\\\n+& 1\\;\\;1\\;\\, \\\\\n\\hline\n&1\\;\\; 1\\;\\;0\\;\\;1\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b009-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Exercise 8.1: Add binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.1: Add binary numbers\n\n10. $$1111+11$$",
    "answer_text": "$$\n\\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n&_{1}\\;\\;_{1}\\;\\;_{1}\\;\\;_{1}\\phantom{000}\\newline\n& 1\\;\\;1\\;\\;1\\;\\;1\\;\\, \\\\\n+& 1\\;\\;1\\;\\, \\\\\n\\hline\n&1\\;\\;0\\;\\; 0\\;\\;1\\;\\;0\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
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
  "topic_key": "jss1-math-addition-of-numbers-in-base-2-numerals",
  "topic": "Addition of Numbers in Base 2 Numerals",
  "subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers",
  "subtopic_title": "Addition of two or three 3-digit binary numbers",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers-po01",
        "source_performance_objective_index": 1,
        "text": "Add two or three 3-digit binary numbers"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "addition-of-binary-numbers-ao-add-two-or-three-3-digit-binary-numbers",
          "text": "Add two or three 3-digit binary numbers."
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
    "record_id": "ch08-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": null,
      "h3": null
    },
    "content_text": "In Chapter 3 you learnt about the base two number system. The base two or binary number system counts in groups of 2, and uses only the digits 0 and 1 to represent any number. The numbers in the base two number system are called binary numbers.\n\nWe can use place value tables in the base two number system. The place values are powers of 2. For example:\n\n$$\n\\begin{array}{|c|c|c|c|c|c|}\n    \\hline\n    \\text{thirty twos} & \\text{sixteens} & \\text{eights} & \\text{fours} & \\text{twos} & \\text{units} \\\\\n    (2^5) & (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n    \\hline\n    &  &  & & & \\\\\n    \\hline\n    \\end{array}\n$$\n\nThe binary numbers that correspond to the decimal numbers 1 to 10 are:\n\n$$\n\\begin{array}{|c|c|}\n    \\hline\n    \\text{decimal number} & \\text{binary number} \\\\\n    \\hline\n    1& 1 \\\\\n    2& 10 \\\\\n    3& 11 \\\\\n    4& 100 \\\\\n    5& 101 \\\\\n    6& 110 \\\\\n    7& 111 \\\\\n    8& 1000 \\\\\n    9& 1001 \\\\\n    10& 1010 \\\\\n    \\hline\n    \\end{array}\n$$\n\nWe use subscripts to tell us which system a certain combination of digits belong to. For example:\n- $100_{10}$ or $100_{\\text{ten}}$ means one hundred\n- $100_2$ or $100_{\\text{two}}$ means four\n\nIn this chapter you will learn how to add, subtract and multiply binary numbers.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch08-b002",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": null
    },
    "content_text": "When we add binary numbers, we follow the same principles as when we add numbers in the base ten number system.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b003",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Worked example 8.1: Revision of addition in the base ten number system"
    },
    "content_text": "",
    "prompt_text": "Find the total of $794+648+89$.",
    "answer_text": "Step 1: Write the numbers one below the other. Line up the units, tens, hundreds, thousands, and so on.\n$$\\begin{array}{r r}\n & \\text{th}\\, \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n & 7\\,9\\,4 \\\\\n +& 6\\,4\\,8 \\\\\n +& 8\\,9 \\\\\n \\hline\n \\end{array}$$\nStep 2: Add the units. Divide the answer by 10. Carry over the quotient and write down the remainder.\nRemember that the quotient is the result you get after you have divided.\n$$4+8+9=21$$\n$$21=(2\\times10)+1$$\n$$\\begin{array}{r r}\n & \\text{th}\\, \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n &_{2} &\\phantom{0}\\\\\n & 7\\,9\\,4 \\\\\n +& 6\\,4\\,8 \\\\\n +& 8\\,9 \\\\\n \\hline\n &1\\\\\n \\hline\n \\end{array}$$\nStep 3: Repeat Step 2 for the tens column.\n$$2+9+4+8=23$$\n$$23=(2\\times10)+3$$\n$$\\begin{array}{r r}\n & \\text{th}\\, \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n &_{2}\\,_{2} &\\phantom{0}\\\\\n & 7\\,9\\,4 \\\\\n +& 6\\,4\\,8 \\\\\n +& 8\\,9 \\\\\n \\hline\n &3\\,1\\\\\n \\hline\n \\end{array}$$\nStep 4: Repeat Step 3 for the hundreds column.\n$$2+7+6=15$$\n$$15=(1\\times10)+5$$\n$$\\begin{array}{r r}\n & \\text{th}\\, \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n &_{1}\\,_{2}\\,_{2} &\\phantom{0}\\\\\n & 7\\,9\\,4 \\\\\n +& 6\\,4\\,8 \\\\\n +& 8\\,9 \\\\\n \\hline\n &5\\,3\\,1\\\\\n \\hline\n \\end{array}$$\nStep 5: Bring down the quotient that was carried over to the thousands column.\n$$\\begin{array}{r r}\n & \\text{th}\\, \\text{h}\\, \\text{t}\\, \\text{u} \\\\\n &_{1}\\,_{2}\\,_{2} &\\phantom{0}\\\\\n & 7\\,9\\,4 \\\\\n +& 6\\,4\\,8 \\\\\n +& 8\\,9 \\\\\n \\hline\n &1,\\,5\\,3\\,1\\\\\n \\hline\n \\end{array}$$\nThe answer is 1,531.",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b004",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": null
    },
    "content_text": "In the base two number system, we work in groups of 2. So, instead of dividing by 10, we divide by 2.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b005",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Worked example 8.2: Addition in the base two number system (Method 1)"
    },
    "content_text": "",
    "prompt_text": "Find the sum of $101_\\text{two}$ and $111_\\text{two}$.",
    "answer_text": "Step 1: Write the numbers one below the other, without the subscript \"two\". Line up the units ($2^0$), twos ($2^1$), fours ($2^2$) and eights ($2^3$).\n$$\\begin{array}{r r}\n & \\color{blue}{2^3 \\; 2^2 \\; 2^1 \\; 2^0 }\\\\\n & 1\\;\\;0\\;\\;1\\;\\, \\\\\n +& 1\\;\\;1\\;\\;1\\;\\, \\\\\n \\hline\n \\end{array}$$\nStep 2: Add the units (in the $2^0$ column). Divide the answer by 2. Carry over the quotient and write down the remainder.\n$$1+1=2$$\n$$2=(1\\times2)+0$$\n$$\\begin{array}{r r}\n & \\color{blue}{2^3 \\; 2^2 \\; 2^1 \\; 2^0 }\\\\\n &_{1} \\phantom{000}\\\\\n & 1\\;\\;0\\;\\;1\\;\\, \\\\\n +& 1\\;\\;1\\;\\;1\\;\\, \\\\\n \\hline\n & 0\\;\\, \\\\\n \\hline\n \\end{array}$$\nStep 3: Repeat Step 2 for the twos ($2^1$) column.\n$$1+1=2$$\n$$2=(1\\times2)+0$$\n$$\\begin{array}{r r}\n & \\color{blue}{2^3 \\; 2^2 \\; 2^1 \\; 2^0 }\\\\\n &_{1}\\;\\;_{1} \\phantom{000}\\\\\n & 1\\;\\;0\\;\\;1\\;\\, \\\\\n +& 1\\;\\;1\\;\\;1\\;\\, \\\\\n \\hline\n & 0\\;\\;0\\;\\, \\\\\n \\hline\n \\end{array}$$\nStep 4: Repeat Step 3 for the fours ($2^2$) column.\n$$1+1+1=3$$\n$$3=(1\\times2)+1$$\n$$\\begin{array}{r r}\n & \\color{blue}{2^3 \\; 2^2 \\; 2^1 \\; 2^0 }\\\\\n &_{1}\\;\\;_{1}\\;\\;_{1} \\phantom{000}\\\\\n & 1\\;\\;0\\;\\;1\\;\\, \\\\\n +& 1\\;\\;1\\;\\;1\\;\\, \\\\\n \\hline\n & 1\\;\\;0\\;\\;0\\;\\, \\\\\n \\hline\n \\end{array}$$\nStep 5: Bring down the quotient that was carried over to the eights ($2^3$) column.\n$$\\begin{array}{r r}\n & \\color{blue}{2^3 \\; 2^2 \\; 2^1 \\; 2^0 }\\\\\n &_{1}\\;\\;_{1}\\;\\;_{1} \\phantom{000}\\\\\n & 1\\;\\;0\\;\\;1\\;\\, \\\\\n +& 1\\;\\;1\\;\\;1\\;\\, \\\\\n \\hline\n &1\\;\\; 1\\;\\;0\\;\\;0\\;\\, \\\\\n \\hline\n \\end{array}$$\nThe answer is $1100_\\text{two}$.\nStep 6: Check your answer by converting to the base ten number system, adding, and then converting back to a base two number.\n$$\\begin{align}\n101_2&=2^2+0+2^0 \\\\\n&=4+1 \\\\\n&=5_{10}\\\\\n\\end{align}$$\n$$\\begin{align}\n111_2&=2^2+2^1+2^0 \\\\\n&=4+2+1 \\\\\n&=7_{10}\\\\\n\\end{align}$$\n$$5+7=12$$\n$$\\begin{align}\n12_{10}&=8+4 \\\\\n&=2^3+2^2+0+0 \\\\\n&=1100_2\\\\\n\\end{align}$$\nThe answer is correct.",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b006",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": null
    },
    "content_text": "Another way to do addition in the base two number system is to use these basic rules:\n\n0+0=0\n0+1=1\n1+0=1\n1+1=10\n1+1+1=11",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b007",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": null
    },
    "content_text": "Remember:\n\n$2_\\text{ten}=10_\\text{two}$\n$3_\\text{ten}=11_\\text{two}$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b008",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Worked example 8.3: Addition in the base two number system (Method 2)"
    },
    "content_text": "",
    "prompt_text": "Find the sum of $101_\\text{two}$ and $111_\\text{two}$.",
    "answer_text": "Step 1: Write the numbers one below the other, without the subscript \"two\". Line up the units ($2^0$), twos ($2^1$), fours ($2^2$) and eights ($2^3$).\n\n$$\n\\\begin{array}{r r}\n & \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n & 1\\;\\;0\\;\\;1\\;\\, \\\\\n +& 1\\;\\;1\\;\\;1\\;\\, \\\\\n \\hline\n \\end{array}\n$$\n\nStep 2: Add the units in the base two number system. If the answer is 10 or 11, carry over the left-hand 1 and write down the right-hand 0 or 1.\n\nRemember to use $1+1=10$ and $1+1+1=11$.\n\n$$\n\\\begin{array}{r r}\n & \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n &_{1} \\phantom{000}\\\\\n & 1\\;\\;0\\;\\;1\\;\\, \\\\\n +& 1\\;\\;1\\;\\;1\\;\\, \\\\\n \\hline\n & 0\\;\\, \\\\\n \\hline\n \\end{array}\n$$\n\nStep 3: Repeat Step 2 for the twos ($2^1$) column.\n\n$$1+1=10$$\n\n$$\n\\\begin{array}{r r}\n & \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n &_{1}\\;\\;_{1} \\phantom{000}\\\\\n & 1\\;\\;0\\;\\;1\\;\\, \\\\\n +& 1\\;\\;1\\;\\;1\\;\\, \\\\\n \\hline\n & 0\\;\\;0\\;\\, \\\\\n \\hline\n \\end{array}\n$$\n\nStep 4: Repeat Step 3 for the fours ($2^2$) column.\n\n$$1+1+1=11$$\n\n$$\n\\\begin{array}{r r}\n & \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n &_{1}\\;\\;_{1}\\;\\;_{1} \\phantom{000}\\\\\n & 1\\;\\;0\\;\\;1\\;\\, \\\\\n +& 1\\;\\;1\\;\\;1\\;\\, \\\\\n \\hline\n & 1\\;\\;0\\;\\;0\\;\\, \\\\\n \\hline\n \\end{array}\n$$\n\nStep 5: Bring down the one that was carried over to the eights ($2^3$) column.\n\n$$\n\\\begin{array}{r r}\n & \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n &_{1}\\;\\;_{1}\\;\\;_{1} \\phantom{000}\\\\\n & 1\\;\\;0\\;\\;1\\;\\, \\\\\n +& 1\\;\\;1\\;\\;1\\;\\, \\\\\n \\hline\n &1\\;\\; 1\\;\\;0\\;\\;0\\;\\, \\\\\n \\hline\n \\end{array}\n$$\n\nThe answer is $1100_\\text{two}$.\n\nStep 6: Check your answer using the base ten number system.\n\n$$\n\\\begin{align}\n101_2&=2^2+0+2^0 \\\\\n&=4+1 \\\\\n&=5_{10}\\\\\n\\end{align}\n$$\n$$\\quad$$\n$$\n\\\begin{align}\n111_2&=2^2+2^1+2^0 \\\\\n&=4+2+1 \\\\\n&=7_{10}\\\\\n\\end{align}\n$$\n$$\\quad$$\n$$5+7=12$$\n$$\\quad$$\n$$\n\\\begin{align}\n12_{10}&=8+4 \\\\\n&=2^3+2^2+0+0 \\\\\n&=1100_2\\\\\n\\end{align}\n$$\n\nThe answer is correct.",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b009",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Exercise 8.1: Add binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.1: Add binary numbers\n\nCalculate each of the following in the base two number system.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b009-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Exercise 8.1: Add binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.1: Add binary numbers\n\n1. $$100+10$$",
    "answer_text": "$$\n\\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n& \\phantom{000}\\newline\n& 1\\;\\;0\\;\\;0\\;\\, \\\\\n+& 1\\;\\;0\\;\\, \\\\\n\\hline\n&1\\;\\; 1\\;\\;0\\;\\;0\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b009-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Exercise 8.1: Add binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.1: Add binary numbers\n\n2. $$101+11$$",
    "answer_text": "Remember to use $1+1=10$ where you need to.\n\n$$\n\\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n&_{1}\\;\\;_{1}\\;\\;_{1} \\phantom{000}\\newline\n& 1\\;\\;0\\;\\;1\\;\\, \\\\\n+& 1\\;\\;1\\;\\, \\\\\n\\hline\n&1\\;\\; 0\\;\\;0\\;\\;0\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b009-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Exercise 8.1: Add binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.1: Add binary numbers\n\n3. $$110+11$$",
    "answer_text": "$$\n\\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n&_{1}\\;\\;_{1} \\phantom{00000}\\newline\n& 1\\;\\;1\\;\\;0\\;\\, \\\\\n+& 1\\;\\;1\\;\\, \\\\\n\\hline\n&1\\;\\; 0\\;\\;0\\;\\;1\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b009-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Exercise 8.1: Add binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.1: Add binary numbers\n\n4. $$111+10$$",
    "answer_text": "$$\n\\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n&_{1}\\;\\;_{1} \\phantom{00000}\\newline\n& 1\\;\\;1\\;\\;1\\;\\, \\\\\n+& 1\\;\\;0\\;\\, \\\\\n\\hline\n&1\\;\\; 0\\;\\;0\\;\\;1\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b009-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Exercise 8.1: Add binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.1: Add binary numbers\n\n5. $$100+101$$",
    "answer_text": "$$\n\\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n&_{1}\\;\\;\\phantom{000000}\\newline\n& 1\\;\\;0\\;\\;0\\;\\, \\\\\n+& 1\\;\\;0\\;\\;1\\;\\, \\\\\n\\hline\n&1\\;\\; 0\\;\\;0\\;\\;1\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b009-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Exercise 8.1: Add binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.1: Add binary numbers\n\n6. $$101+110$$",
    "answer_text": "$$\n\\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n&_{1}\\;\\;\\phantom{000000}\\newline\n& 1\\;\\;0\\;\\;1\\;\\, \\\\\n+& 1\\;\\;1\\;\\;0\\;\\, \\\\\n\\hline\n&1\\;\\; 0\\;\\;1\\;\\;1\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b009-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Exercise 8.1: Add binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.1: Add binary numbers\n\n7. $$110+111$$",
    "answer_text": "Remember to use $1+1=10$ and $1+1+1=11$ where you need to.\n\n$$\n\\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n&_{1}\\;\\;_{1}\\phantom{00000}\\newline\n& 1\\;\\;1\\;\\;0\\;\\, \\\\\n+& 1\\;\\;1\\;\\;1\\;\\, \\\\\n\\hline\n&1\\;\\; 1\\;\\;0\\;\\;1\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b009-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Exercise 8.1: Add binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.1: Add binary numbers\n\n8. $$111+111$$",
    "answer_text": "$$\n\\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n&_{1}\\;\\;_{1}\\;\\;_{1}\\phantom{000}\\newline\n& 1\\;\\;1\\;\\;1\\;\\, \\\\\n+& 1\\;\\;1\\;\\;1\\;\\, \\\\\n\\hline\n&1\\;\\; 1\\;\\;1\\;\\;0\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b009-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Exercise 8.1: Add binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.1: Add binary numbers\n\n9. $$1010+11$$",
    "answer_text": "$$\n\\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n&_{1}\\phantom{00000}\\newline\n& 1\\;\\;0\\;\\;1\\;\\;0\\;\\, \\\\\n+& 1\\;\\;1\\;\\, \\\\\n\\hline\n&1\\;\\; 1\\;\\;0\\;\\;1\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
  },
  {
    "record_id": "ch08-b009-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 8: Operations with binary numbers",
      "h2": "8.1 Addition",
      "h3": "Exercise 8.1: Add binary numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 8.1: Add binary numbers\n\n10. $$1111+11$$",
    "answer_text": "$$\n\\\begin{array}{r r}\n& \\color{blue}{2^3 \\, 2^2 \\, 2^1 \\, 2^0 }\\\\\n&_{1}\\;\\;_{1}\\;\\;_{1}\\;\\;_{1}\\phantom{000}\\newline\n& 1\\;\\;1\\;\\;1\\;\\;1\\;\\, \\\\\n+& 1\\;\\;1\\;\\, \\\\\n\\hline\n&1\\;\\;0\\;\\; 0\\;\\;1\\;\\;0\\;\\, \\\\\n\\hline\n\\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers"
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
