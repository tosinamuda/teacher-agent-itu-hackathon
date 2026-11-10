# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-1",
  "topic_key": "jss1-math-whole-numbers",
  "topic": "Whole Numbers",
  "subtopic_id": "jss1-math-whole-numbers-trillions",
  "subtopic_title": "Trillions",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-whole-numbers-trillions-po01",
        "source_performance_objective_index": 1,
        "text": "Count and write in trillions"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "trillions-ao-count-trillions",
          "text": "Count in trillions."
        },
        {
          "atomic_objective_id": "trillions-ao-write-trillions",
          "text": "Write in trillions."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-whole-numbers-trillions-po02",
        "source_performance_objective_index": 2,
        "text": "Apply the counting, writing, and reading of large numbers in everyday life"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "everyday-life-ao-apply-counting-large-numbers",
          "text": "Apply counting of large numbers in everyday life."
        },
        {
          "atomic_objective_id": "everyday-life-ao-apply-writing-large-numbers",
          "text": "Apply writing of large numbers in everyday life."
        },
        {
          "atomic_objective_id": "everyday-life-ao-apply-reading-large-numbers",
          "text": "Apply reading of large numbers in everyday life."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch01-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": null,
      "h3": null
    },
    "content_text": "Last year you learnt how to write and read numbers up to one million. You also counted in millions. In this chapter, you will revise some of last year's work. You will also learn to read, write and count in even larger numbers. To help you to do this, you will first learn more about our main system of counting.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b002",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.1 The base ten number system",
      "h3": null
    },
    "content_text": "The most common number system used for everyday counting is the **base ten number system**. It is also called the decimal number system. The number 10 is the base of this number system.\n\nWhen we count using the base ten number system, we actually put objects in groups of ten. For example, count these stars:\n\n$$\n\\star \\space \\star \\space \\star \\space\\star \\space\\star \\space\\star \\space\\star \\space\\star \\space\\star \\space\\star \\space \\star\n$$\n\nThere are 12 stars. The number 12 means we have 1 group of ten stars and 2 stars left over.\n\nIn this system, we use the numbers 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 to make any other number, no matter how big or how small it is. When the numbers 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 are used as part of another number, we often call them **digits**.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b003",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.1 The base ten number system",
      "h3": null
    },
    "content_text": "**base ten number system** The base ten number system is a number system that counts in groups of 10, and uses uses the digits 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 to represent any other number. It is also called the decimal number system.\n\n**digits** Digits are the numbers 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 that are used to form other numbers.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b004",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.1 The base ten number system",
      "h3": null
    },
    "content_text": "In the base ten number system, we go to a new group each time we reach the number 10. The numbers 1 to 9 are called **units**. Zero is used as a placeholder. The number after 9 is 10, which means that we have 1 group of ten and nothing left over. The zero shows that there are no units in the number 10.\n\nWe may count in **tens** until we reach 9 groups of 10: 10; 20; 30; 40; 50; 60; 70; 80; 90. When we add another group of ten, we have 100. The number 100 means that we have 1 group of 100, zero groups of ten and zero units.\n\nSimilarly, we may count in **hundreds** until we reach 9 groups of 100: 100; 200; 300; 400; 500; 600; 700; 800; 900. When we add another group of 100, we have 1,000. The number 1,000 means that we have 1 thousand, zero hundreds, zero tens and zero units.\n\nWhen we count in **thousands**, 1,000; 2,000; 3,000; 4,000; 5,000; 6,000; 7,000; 8,000; 9,000, we eventually reach 10 groups of 1,000, which is 10,000. This number is called **ten thousand**.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b005",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.1 The base ten number system",
      "h3": null
    },
    "content_text": "**units** Units are the numbers 1; 2; 3; 4; 5; 6; 7; 8; 9 in the base ten number system.\n\n**tens** Tens are the numbers 10; 20; 30; 40; 50; 60; 70; 80; 90 in the base ten number system.\n\n**hundreds** Hundreds are the numbers 100; 200; 300; 400; 500; 600; 700; 800; 900 in the base ten number system.\n\n**thousands** Thousands are the numbers 1,000; 2,000; 3,000; 4,000; 5,000; 6,000; 7,000; 8,000; 9,000 in the base ten number system.\n\n**ten thousands** Ten thousands are the numbers 10,000; 20,000; 30,000; 40,000; 50,000; 60,000; 70,000; 80,000; 90,000 in the base ten number system.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b006",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.1 The base ten number system",
      "h3": "Grouping digits"
    },
    "content_text": "You may have noticed that we write a thousand as 1,000 rather than 1000. Similarly, we write ten thousand as 10,000 rather than 10000. We use a comma to group the digits. Grouping digits makes it easier to read large numbers.\n\nLater you will work with decimal fractions. An example of a decimal fraction is 0.25. It is the same as $\\frac{1}{4}$. We use a decimal point to separate whole numbers from fractions. In the number 2.5, the decimal point separates the whole number 2 from the fraction 0.5.\n\nUsually, we group only the digits representing whole numbers, that is, the digits to the left of the decimal point. The digits are grouped in threes, starting at the decimal point and going to the left. For example, the number 2516.2 is written as 2,516.2 and not as 251,6.2.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b007",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.1 The base ten number system",
      "h3": "Exercise 1.1: Group the digits in large numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.1: Group the digits in large numbers\n\nRewrite each of the following numbers with the digits correctly grouped.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b007-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.1 The base ten number system",
      "h3": "Exercise 1.1: Group the digits in large numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.1: Group the digits in large numbers\n\nRewrite each of the following numbers with the digits correctly grouped.\n\n1. 25618.231",
    "answer_text": "25,618.231",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b007-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.1 The base ten number system",
      "h3": "Exercise 1.1: Group the digits in large numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.1: Group the digits in large numbers\n\nRewrite each of the following numbers with the digits correctly grouped.\n\n2. 100985.0021",
    "answer_text": "100,985.0021",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b007-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.1 The base ten number system",
      "h3": "Exercise 1.1: Group the digits in large numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.1: Group the digits in large numbers\n\nRewrite each of the following numbers with the digits correctly grouped.\n\n3. 201050.11",
    "answer_text": "201,050.11",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b007-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.1 The base ten number system",
      "h3": "Exercise 1.1: Group the digits in large numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.1: Group the digits in large numbers\n\nRewrite each of the following numbers with the digits correctly grouped.\n\n4. 5555.55",
    "answer_text": "5,555.55",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b007-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.1 The base ten number system",
      "h3": "Exercise 1.1: Group the digits in large numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.1: Group the digits in large numbers\n\nRewrite each of the following numbers with the digits correctly grouped.\n\n5. 121212.1212",
    "answer_text": "121,212.1212",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b008",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.1 The base ten number system",
      "h3": "Grouping digits"
    },
    "content_text": "In some countries, people use spaces instead of commas to group digits. For example, they write the number 504,816 as 504 816. In some countries, they also use a decimal comma instead of a decimal point. For example, they write the number 1,500.5 as 1 500,5.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b009",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Place value in numbers larger than zero"
    },
    "content_text": "Each digit in a number tells you the specific value of that digit. The **place value** of a digit tells us what the value of that digit is, based on that number's position (place) in the number.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b010",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Place value in numbers larger than zero"
    },
    "content_text": "**place value** Place value is the value of a digit according to its position in a number.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b011",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Worked example 1.1: Finding the place value of a digit"
    },
    "content_text": "",
    "prompt_text": "Give the place value of each digit in the number 52,143.",
    "answer_text": "Step 1: Create a table that represents the place values, with one column for each place. Put each digit of the number into the correct position in the table.\n\n$$\n\\begin{array}{|c|c|c|c|c|}\n \\hline\n \\text{ten thousands} & \\text{thousands} & \\text{hundreds} & \\;\\; \\text{tens}\\;\\; & \\;\\; \\text{units}\\;\\; \\\\\n (10,000) & (1,000) & (100) & (10) & (1) \\\\\n \\text{tth} & \\text{th} & \\text{h} & \\text{t} & \\text{u} \\\\\n \\hline\n 5 & 2 & 1 & 4 & 3 \\\\\n \\hline\n \\end{array}\n$$\n\nStep 2: Use the table to help you to write down the place value of each digit.\n\nThere are 5 groups of 10,000, so the value of this 5 is $5\\times 10,000=50,000$.\nThere are 2 groups of 1,000, so the value of this 2 is $2\\times1,000=2,000$.\nThere is 1 group of 100, so the value of this 1 is $1\\times100=100$.\nThere are 4 groups of 10, so the value of this 4 is $4\\times10=40$.\nThere are 3 units, so the value of this 3 is $3\\times 1=3$.",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b012",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Exercise 1.2: Find the place value of a number"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.2: Find the place value of a number\n\nUse place value tables to determine the place value of the number 6 in each number.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b012-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Exercise 1.2: Find the place value of a number"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.2: Find the place value of a number\n\nUse place value tables to determine the place value of the number 6 in each number.\n\n1. 164",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|}\n\\hline\n\\text{tth} & \\text{th} & \\text{h} & \\text{t} & \\text{u} \\\\\n(10,000) & (1,000) & (100) & (10) & (1) \\\\\n\\hline\n\\space & \\space & 1 & 6 & 4 \\\\\n\\hline\n\\end{array}\n$$\n\nThe place value is: $6\\times10=60$",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b012-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Exercise 1.2: Find the place value of a number"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.2: Find the place value of a number\n\nUse place value tables to determine the place value of the number 6 in each number.\n\n2. 1,026",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|}\n\\hline\n\\text{tth} & \\text{th} & \\text{h} & \\text{t} & \\text{u} \\\\\n(10,000) & (1,000) & (100) & (10) & (1) \\\\\n\\hline\n\\space & 1 & 0 & 2 & 6 \\\\\n\\hline\n\\end{array}\n$$\n\nThe place value is: $6\\times1=6$",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b012-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Exercise 1.2: Find the place value of a number"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.2: Find the place value of a number\n\nUse place value tables to determine the place value of the number 6 in each number.\n\n3. 68,417",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|}\n\\hline\n\\text{tth} & \\text{th} & \\text{h} & \\text{t} & \\text{u} \\\\\n(10,000) & (1,000) & (100) & (10) & (1) \\\\\n\\hline\n6 & 8 & 4 & 1 & 7 \\\\\n\\hline\n\\end{array}\n$$\n\nThe place value is: $6\\times10,000=60,000$",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b012-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Exercise 1.2: Find the place value of a number"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.2: Find the place value of a number\n\nUse place value tables to determine the place value of the number 6 in each number.\n\n4. 13,650",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|}\n\\hline\n\\text{tth} & \\text{th} & \\text{h} & \\text{t} & \\text{u} \\\\\n(10,000) & (1,000) & (100) & (10) & (1) \\\\\n\\hline\n1 & 3 & 6 & 5 & 0 \\\\\n\\hline\n\\end{array}\n$$\n\nThe place value is: $6\\times100=600$",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b012-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Exercise 1.2: Find the place value of a number"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.2: Find the place value of a number\n\nUse place value tables to determine the place value of the number 6 in each number.\n\n5. 26,009",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|}\n\\hline\n\\text{tth} & \\text{th} & \\text{h} & \\text{t} & \\text{u} \\\\\n(10,000) & (1,000) & (100) & (10) & (1) \\\\\n\\hline\n2 & 6 & 0 & 0 & 9 \\\\\n\\hline\n\\end{array}\n$$\n\nThe place value is: $6\\times1,000=6,000$",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b042",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.5 Counting in big numbers",
      "h3": "Counting in trillions"
    },
    "content_text": "Our table with powers of ten can be expanded further, to include even larger numbers.\n\n$$\n\\begin{array}{|l|l|l|}\n  \\hline\n    \\textbf{Name} & \\textbf{Number} & \\textbf{Powers of ten}  \\\\\n    \\hline\n     \\text{Ten} & 10 & 10=10^1    \\\\\n    \\hline\n     \\text{Hundred} & 100 & 10\\times10=10^2    \\\\\n    \\hline\n    \\text{Thousand} & 1,000 & 10\\times10\\times10=10^3    \\\\\n    \\hline\n    \\text{Ten thousand} & 10,000 & 10\\times10\\times10\\times10=10^4    \\\\\n    \\hline\n    \\text{Hundred thousand} & 100,000 & 10\\times10\\times10\\times10\\times10=10^5    \\\\\n    \\hline\n    \\text{Million} & 1,000,000 & 10\\times10\\times10\\times10\\times10\\times10=10^6    \\\\\n    \\hline\n    \\text{Ten million} & 10,000,000 & 10\\times10\\times10\\times10\\times10\\times10\\times10=10^7 \\\\\n    \\hline\n    \\text{Hundred million} & 100,000,000 & 10\\times10\\times10\\times10\\times10\\times10\\times10\\times10=10^8 \\\\\n    \\hline\n    \\text{Billion} & 1,000,000,000 & 10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10=10^9 \\\\\n    \\hline\n    \\text{Ten billion} & 10,000,000,000 & 10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10=10^{10} \\\\\n    \\hline\n    \\text{Hundred billion} & 100,000,000,000 & 10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10=10^{11} \\\\\n    \\hline\n    \\text{Trillion} & 1,000,000,000,000 & 10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10=10^{12} \\\\\n    \\hline\n     \\end{array}\n$$\n\nThe number 1,000,000,000,000 is named one trillion. Try to imagine how large one trillion is:\n\n- A human cannot live for one trillion seconds; it is equal to almost 31,708 years.\n- Suppose the whole surface of Nigeria is tiled with 50 kobo coins. One trillion 50 kobo coins will form 412 layers over the surface of Nigeria.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-trillions"
  },
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
    "record_id": "ch01-b045",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.5 Counting in big numbers",
      "h3": "Exercise 1.12: Count in trillions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.12: Count in trillions",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-trillions"
  },
  {
    "record_id": "ch01-b045-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.5 Counting in big numbers",
      "h3": "Exercise 1.12: Count in trillions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.12: Count in trillions\n\n1. Count in trillions from 3.5 trillion to 6.5 trillion. Write down the numbers as digits only and include their full names.",
    "answer_text": "3.5 trillion = 3,500,000,000,000: three trillion five hundred billion\n4.5 trillion = 4,500,000,000,000: four trillion five hundred billion\n5.5 trillion = 5,500,000,000,000: five trillion five hundred billion\n6.5 trillion = 6,500,000,000,000: six trillion five hundred billion",
    "primary_subtopic_id": "jss1-math-whole-numbers-trillions"
  },
  {
    "record_id": "ch01-b045-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.5 Counting in big numbers",
      "h3": "Exercise 1.12: Count in trillions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.12: Count in trillions\n\n2. Count in 0.5 trillions from 37.5 trillion to 40.5 trillion. Write down the numbers as digits only and include their full names.",
    "answer_text": "37.5 trillion = 37,500,000,000,000: thirty seven trillion five hundred billion\n38 trillion = 38,000,000,000,000: thirty eight trillion\n38.5 trillion = 38,500,000,000,000: thirty eight trillion five hundred billion\n39 trillion = 39,000,000,000,000: thirty nine trillion\n39.5 trillion = 39,500,000,000,000: thirty nine trillion five hundred billion\n40 trillion = 40,000,000,000,000: forty trillion\n40.5 trillion = 40,500,000,000,000: forty trillion five hundred billion",
    "primary_subtopic_id": "jss1-math-whole-numbers-trillions"
  },
  {
    "record_id": "ch01-b045-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.5 Counting in big numbers",
      "h3": "Exercise 1.12: Count in trillions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.12: Count in trillions\n\n3. Count in 0.25 trillions from 9 trillion to 10.5 trillion. Write down the numbers as digits only and include their full names.",
    "answer_text": "9 trillion = 9,000,000,000,000: nine trillion\n9.25 trillion = 9,250,000,000,000: nine trillion two hundred and fifty billion\n9.5 trillion = 9,500,000,000,000: nine trillion five hundred billion\n9.75 trillion = 9,750,000,000,000: nine trillion seven hundred and fifty billion\n10 trillion = 10,000,000,000,000: ten trillion\n10.25 trillion = 10,250,000,000,000: ten trillion two hundred and fifty billion\n10.5 trillion = 10,500,000,000,000: ten trillion five hundred billion",
    "primary_subtopic_id": "jss1-math-whole-numbers-trillions"
  },
  {
    "record_id": "ch01-b045-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.5 Counting in big numbers",
      "h3": "Exercise 1.12: Count in trillions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.12: Count in trillions\n\n4. Count in 3 trillions from 987 trillion to 999 trillion. Write down the numbers as digits only and include their full names.",
    "answer_text": "987 trillion = 987,000,000,000,000: nine hundred and eighty seven trillion\n990 trillion = 990,000,000,000,000: nine hundred and ninety trillion\n993 trillion = 993,000,000,000,000: nine hundred and ninety three trillion\n996 trillion = 996,000,000,000,000: nine hundred and ninety six trillion\n999 trillion = 999,000,000,000,000: nine hundred and ninety nine trillion",
    "primary_subtopic_id": "jss1-math-whole-numbers-trillions"
  },
  {
    "record_id": "ch01-b045-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.5 Counting in big numbers",
      "h3": "Exercise 1.12: Count in trillions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.12: Count in trillions\n\n5. Count in 4 trillions from 892 trillion to 908 trillion. Write down the numbers as digits only and include their full names.",
    "answer_text": "892 trillion = 892,000,000,000,000: eight hundred and ninety two trillion\n896 trillion = 896,000,000,000,000: eight hundred and ninety six trillion\n900 trillion = 900,000,000,000,000: nine hundred trillion\n904 trillion = 904,000,000,000,000: nine hundred and four trillion\n908 trillion = 908,000,000,000,000: nine hundred and eight trillion",
    "primary_subtopic_id": "jss1-math-whole-numbers-trillions"
  },
  {
    "record_id": "ch01-b046",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.6 Using large numbers in everyday life",
      "h3": null
    },
    "content_text": "In your daily life, you may come across large numbers in newspapers, on television shows and in some of your other school subjects.\n\nWhenever you get stuck with a large number, write the number in a place value table to help you make sense of it. Remember the order of the place value table:\n\n$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|c|c|c|}\n  \\hline\n    \\textbf{trillion} &\\text{hundred billion} &\\text{ten billion} &\\textbf{billion} & \\text{hundred million} & \\text{ten million} & \\textbf{million} &\\text{hundred thousand} & \\text{ten thousand} & \\textbf{thousand} & \\text{hundred} & \\text{  ten  } & \\text{  unit  }  \\\\\n    (1,000,000,000,000) & (100,000,000,000) & (10,000,000,000) & (1,000,000,000) & (100,000,000) & (10,000,000) & (1,000,000) & (100,000) & (10,000) & (1,000) & (100) & (10) & (1) \\\\\n    \\hline\n     & & & & & & & & & & & &    \\\\\n    \\hline\n    \\end{array}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-trillions"
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
  "subtopic_id": "jss1-math-whole-numbers-trillions",
  "subtopic_title": "Trillions",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-whole-numbers-trillions-po01",
        "source_performance_objective_index": 1,
        "text": "Count and write in trillions"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "trillions-ao-count-trillions",
          "text": "Count in trillions."
        },
        {
          "atomic_objective_id": "trillions-ao-write-trillions",
          "text": "Write in trillions."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-whole-numbers-trillions-po02",
        "source_performance_objective_index": 2,
        "text": "Apply the counting, writing, and reading of large numbers in everyday life"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "everyday-life-ao-apply-counting-large-numbers",
          "text": "Apply counting of large numbers in everyday life."
        },
        {
          "atomic_objective_id": "everyday-life-ao-apply-writing-large-numbers",
          "text": "Apply writing of large numbers in everyday life."
        },
        {
          "atomic_objective_id": "everyday-life-ao-apply-reading-large-numbers",
          "text": "Apply reading of large numbers in everyday life."
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
    "record_id": "ch01-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": null,
      "h3": null
    },
    "content_text": "Last year you learnt how to write and read numbers up to one million. You also counted in millions. In this chapter, you will revise some of last year's work. You will also learn to read, write and count in even larger numbers. To help you to do this, you will first learn more about our main system of counting.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b002",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.1 The base ten number system",
      "h3": null
    },
    "content_text": "The most common number system used for everyday counting is the **base ten number system**. It is also called the decimal number system. The number 10 is the base of this number system.\n\nWhen we count using the base ten number system, we actually put objects in groups of ten. For example, count these stars:\n\n$$\n\\star \\space \\star \\space \\star \\space\\star \\space\\star \\space\\star \\space\\star \\space\\star \\space\\star \\space\\star \\space \\star\n$$\n\nThere are 12 stars. The number 12 means we have 1 group of ten stars and 2 stars left over.\n\nIn this system, we use the numbers 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 to make any other number, no matter how big or how small it is. When the numbers 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 are used as part of another number, we often call them **digits**.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b003",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.1 The base ten number system",
      "h3": null
    },
    "content_text": "**base ten number system** The base ten number system is a number system that counts in groups of 10, and uses uses the digits 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 to represent any other number. It is also called the decimal number system.\n\n**digits** Digits are the numbers 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 that are used to form other numbers.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b004",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.1 The base ten number system",
      "h3": null
    },
    "content_text": "In the base ten number system, we go to a new group each time we reach the number 10. The numbers 1 to 9 are called **units**. Zero is used as a placeholder. The number after 9 is 10, which means that we have 1 group of ten and nothing left over. The zero shows that there are no units in the number 10.\n\nWe may count in **tens** until we reach 9 groups of 10: 10; 20; 30; 40; 50; 60; 70; 80; 90. When we add another group of ten, we have 100. The number 100 means that we have 1 group of 100, zero groups of ten and zero units.\n\nSimilarly, we may count in **hundreds** until we reach 9 groups of 100: 100; 200; 300; 400; 500; 600; 700; 800; 900. When we add another group of 100, we have 1,000. The number 1,000 means that we have 1 thousand, zero hundreds, zero tens and zero units.\n\nWhen we count in **thousands**, 1,000; 2,000; 3,000; 4,000; 5,000; 6,000; 7,000; 8,000; 9,000, we eventually reach 10 groups of 1,000, which is 10,000. This number is called **ten thousand**.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b005",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.1 The base ten number system",
      "h3": null
    },
    "content_text": "**units** Units are the numbers 1; 2; 3; 4; 5; 6; 7; 8; 9 in the base ten number system.\n\n**tens** Tens are the numbers 10; 20; 30; 40; 50; 60; 70; 80; 90 in the base ten number system.\n\n**hundreds** Hundreds are the numbers 100; 200; 300; 400; 500; 600; 700; 800; 900 in the base ten number system.\n\n**thousands** Thousands are the numbers 1,000; 2,000; 3,000; 4,000; 5,000; 6,000; 7,000; 8,000; 9,000 in the base ten number system.\n\n**ten thousands** Ten thousands are the numbers 10,000; 20,000; 30,000; 40,000; 50,000; 60,000; 70,000; 80,000; 90,000 in the base ten number system.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b006",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.1 The base ten number system",
      "h3": "Grouping digits"
    },
    "content_text": "You may have noticed that we write a thousand as 1,000 rather than 1000. Similarly, we write ten thousand as 10,000 rather than 10000. We use a comma to group the digits. Grouping digits makes it easier to read large numbers.\n\nLater you will work with decimal fractions. An example of a decimal fraction is 0.25. It is the same as $\\frac{1}{4}$. We use a decimal point to separate whole numbers from fractions. In the number 2.5, the decimal point separates the whole number 2 from the fraction 0.5.\n\nUsually, we group only the digits representing whole numbers, that is, the digits to the left of the decimal point. The digits are grouped in threes, starting at the decimal point and going to the left. For example, the number 2516.2 is written as 2,516.2 and not as 251,6.2.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b007",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.1 The base ten number system",
      "h3": "Exercise 1.1: Group the digits in large numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.1: Group the digits in large numbers\n\nRewrite each of the following numbers with the digits correctly grouped.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b007-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.1 The base ten number system",
      "h3": "Exercise 1.1: Group the digits in large numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.1: Group the digits in large numbers\n\nRewrite each of the following numbers with the digits correctly grouped.\n\n1. 25618.231",
    "answer_text": "25,618.231",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b007-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.1 The base ten number system",
      "h3": "Exercise 1.1: Group the digits in large numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.1: Group the digits in large numbers\n\nRewrite each of the following numbers with the digits correctly grouped.\n\n2. 100985.0021",
    "answer_text": "100,985.0021",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b007-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.1 The base ten number system",
      "h3": "Exercise 1.1: Group the digits in large numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.1: Group the digits in large numbers\n\nRewrite each of the following numbers with the digits correctly grouped.\n\n3. 201050.11",
    "answer_text": "201,050.11",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b007-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.1 The base ten number system",
      "h3": "Exercise 1.1: Group the digits in large numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.1: Group the digits in large numbers\n\nRewrite each of the following numbers with the digits correctly grouped.\n\n4. 5555.55",
    "answer_text": "5,555.55",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b007-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.1 The base ten number system",
      "h3": "Exercise 1.1: Group the digits in large numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.1: Group the digits in large numbers\n\nRewrite each of the following numbers with the digits correctly grouped.\n\n5. 121212.1212",
    "answer_text": "121,212.1212",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b008",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.1 The base ten number system",
      "h3": "Grouping digits"
    },
    "content_text": "In some countries, people use spaces instead of commas to group digits. For example, they write the number 504,816 as 504 816. In some countries, they also use a decimal comma instead of a decimal point. For example, they write the number 1,500.5 as 1 500,5.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b009",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Place value in numbers larger than zero"
    },
    "content_text": "Each digit in a number tells you the specific value of that digit. The **place value** of a digit tells us what the value of that digit is, based on that number's position (place) in the number.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b010",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Place value in numbers larger than zero"
    },
    "content_text": "**place value** Place value is the value of a digit according to its position in a number.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b011",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Worked example 1.1: Finding the place value of a digit"
    },
    "content_text": "",
    "prompt_text": "Give the place value of each digit in the number 52,143.",
    "answer_text": "Step 1: Create a table that represents the place values, with one column for each place. Put each digit of the number into the correct position in the table.\n\n$$\n\\begin{array}{|c|c|c|c|c|}\n \\hline\n \\text{ten thousands} & \\text{thousands} & \\text{hundreds} & \\;\\; \\text{tens}\\;\\; & \\;\\; \\text{units}\\;\\; \\\\\n (10,000) & (1,000) & (100) & (10) & (1) \\\\\n \\text{tth} & \\text{th} & \\text{h} & \\text{t} & \\text{u} \\\\\n \\hline\n 5 & 2 & 1 & 4 & 3 \\\\\n \\hline\n \\end{array}\n$$\n\nStep 2: Use the table to help you to write down the place value of each digit.\n\nThere are 5 groups of 10,000, so the value of this 5 is $5\\times 10,000=50,000$.\nThere are 2 groups of 1,000, so the value of this 2 is $2\\times1,000=2,000$.\nThere is 1 group of 100, so the value of this 1 is $1\\times100=100$.\nThere are 4 groups of 10, so the value of this 4 is $4\\times10=40$.\nThere are 3 units, so the value of this 3 is $3\\times 1=3$.",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b012",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Exercise 1.2: Find the place value of a number"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.2: Find the place value of a number\n\nUse place value tables to determine the place value of the number 6 in each number.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b012-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Exercise 1.2: Find the place value of a number"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.2: Find the place value of a number\n\nUse place value tables to determine the place value of the number 6 in each number.\n\n1. 164",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|}\n\\hline\n\\text{tth} & \\text{th} & \\text{h} & \\text{t} & \\text{u} \\\\\n(10,000) & (1,000) & (100) & (10) & (1) \\\\\n\\hline\n\\space & \\space & 1 & 6 & 4 \\\\\n\\hline\n\\end{array}\n$$\n\nThe place value is: $6\\times10=60$",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b012-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Exercise 1.2: Find the place value of a number"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.2: Find the place value of a number\n\nUse place value tables to determine the place value of the number 6 in each number.\n\n2. 1,026",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|}\n\\hline\n\\text{tth} & \\text{th} & \\text{h} & \\text{t} & \\text{u} \\\\\n(10,000) & (1,000) & (100) & (10) & (1) \\\\\n\\hline\n\\space & 1 & 0 & 2 & 6 \\\\\n\\hline\n\\end{array}\n$$\n\nThe place value is: $6\\times1=6$",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b012-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Exercise 1.2: Find the place value of a number"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.2: Find the place value of a number\n\nUse place value tables to determine the place value of the number 6 in each number.\n\n3. 68,417",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|}\n\\hline\n\\text{tth} & \\text{th} & \\text{h} & \\text{t} & \\text{u} \\\\\n(10,000) & (1,000) & (100) & (10) & (1) \\\\\n\\hline\n6 & 8 & 4 & 1 & 7 \\\\\n\\hline\n\\end{array}\n$$\n\nThe place value is: $6\\times10,000=60,000$",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b012-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Exercise 1.2: Find the place value of a number"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.2: Find the place value of a number\n\nUse place value tables to determine the place value of the number 6 in each number.\n\n4. 13,650",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|}\n\\hline\n\\text{tth} & \\text{th} & \\text{h} & \\text{t} & \\text{u} \\\\\n(10,000) & (1,000) & (100) & (10) & (1) \\\\\n\\hline\n1 & 3 & 6 & 5 & 0 \\\\\n\\hline\n\\end{array}\n$$\n\nThe place value is: $6\\times100=600$",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b012-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.2 Place value",
      "h3": "Exercise 1.2: Find the place value of a number"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.2: Find the place value of a number\n\nUse place value tables to determine the place value of the number 6 in each number.\n\n5. 26,009",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|}\n\\hline\n\\text{tth} & \\text{th} & \\text{h} & \\text{t} & \\text{u} \\\\\n(10,000) & (1,000) & (100) & (10) & (1) \\\\\n\\hline\n2 & 6 & 0 & 0 & 9 \\\\\n\\hline\n\\end{array}\n$$\n\nThe place value is: $6\\times1,000=6,000$",
    "primary_subtopic_id": "jss1-math-whole-numbers-millions-and-billions"
  },
  {
    "record_id": "ch01-b042",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.5 Counting in big numbers",
      "h3": "Counting in trillions"
    },
    "content_text": "Our table with powers of ten can be expanded further, to include even larger numbers.\n\n$$\n\\begin{array}{|l|l|l|}\n  \\hline\n    \\textbf{Name} & \\textbf{Number} & \\textbf{Powers of ten}  \\\\\n    \\hline\n     \\text{Ten} & 10 & 10=10^1    \\\\\n    \\hline\n     \\text{Hundred} & 100 & 10\\times10=10^2    \\\\\n    \\hline\n    \\text{Thousand} & 1,000 & 10\\times10\\times10=10^3    \\\\\n    \\hline\n    \\text{Ten thousand} & 10,000 & 10\\times10\\times10\\times10=10^4    \\\\\n    \\hline\n    \\text{Hundred thousand} & 100,000 & 10\\times10\\times10\\times10\\times10=10^5    \\\\\n    \\hline\n    \\text{Million} & 1,000,000 & 10\\times10\\times10\\times10\\times10\\times10=10^6    \\\\\n    \\hline\n    \\text{Ten million} & 10,000,000 & 10\\times10\\times10\\times10\\times10\\times10\\times10=10^7 \\\\\n    \\hline\n    \\text{Hundred million} & 100,000,000 & 10\\times10\\times10\\times10\\times10\\times10\\times10\\times10=10^8 \\\\\n    \\hline\n    \\text{Billion} & 1,000,000,000 & 10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10=10^9 \\\\\n    \\hline\n    \\text{Ten billion} & 10,000,000,000 & 10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10=10^{10} \\\\\n    \\hline\n    \\text{Hundred billion} & 100,000,000,000 & 10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10=10^{11} \\\\\n    \\hline\n    \\text{Trillion} & 1,000,000,000,000 & 10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10\\times10=10^{12} \\\\\n    \\hline\n     \\end{array}\n$$\n\nThe number 1,000,000,000,000 is named one trillion. Try to imagine how large one trillion is:\n\n- A human cannot live for one trillion seconds; it is equal to almost 31,708 years.\n- Suppose the whole surface of Nigeria is tiled with 50 kobo coins. One trillion 50 kobo coins will form 412 layers over the surface of Nigeria.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-trillions"
  },
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
    "record_id": "ch01-b045",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.5 Counting in big numbers",
      "h3": "Exercise 1.12: Count in trillions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.12: Count in trillions",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-trillions"
  },
  {
    "record_id": "ch01-b045-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.5 Counting in big numbers",
      "h3": "Exercise 1.12: Count in trillions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.12: Count in trillions\n\n1. Count in trillions from 3.5 trillion to 6.5 trillion. Write down the numbers as digits only and include their full names.",
    "answer_text": "3.5 trillion = 3,500,000,000,000: three trillion five hundred billion\n4.5 trillion = 4,500,000,000,000: four trillion five hundred billion\n5.5 trillion = 5,500,000,000,000: five trillion five hundred billion\n6.5 trillion = 6,500,000,000,000: six trillion five hundred billion",
    "primary_subtopic_id": "jss1-math-whole-numbers-trillions"
  },
  {
    "record_id": "ch01-b045-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.5 Counting in big numbers",
      "h3": "Exercise 1.12: Count in trillions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.12: Count in trillions\n\n2. Count in 0.5 trillions from 37.5 trillion to 40.5 trillion. Write down the numbers as digits only and include their full names.",
    "answer_text": "37.5 trillion = 37,500,000,000,000: thirty seven trillion five hundred billion\n38 trillion = 38,000,000,000,000: thirty eight trillion\n38.5 trillion = 38,500,000,000,000: thirty eight trillion five hundred billion\n39 trillion = 39,000,000,000,000: thirty nine trillion\n39.5 trillion = 39,500,000,000,000: thirty nine trillion five hundred billion\n40 trillion = 40,000,000,000,000: forty trillion\n40.5 trillion = 40,500,000,000,000: forty trillion five hundred billion",
    "primary_subtopic_id": "jss1-math-whole-numbers-trillions"
  },
  {
    "record_id": "ch01-b045-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.5 Counting in big numbers",
      "h3": "Exercise 1.12: Count in trillions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.12: Count in trillions\n\n3. Count in 0.25 trillions from 9 trillion to 10.5 trillion. Write down the numbers as digits only and include their full names.",
    "answer_text": "9 trillion = 9,000,000,000,000: nine trillion\n9.25 trillion = 9,250,000,000,000: nine trillion two hundred and fifty billion\n9.5 trillion = 9,500,000,000,000: nine trillion five hundred billion\n9.75 trillion = 9,750,000,000,000: nine trillion seven hundred and fifty billion\n10 trillion = 10,000,000,000,000: ten trillion\n10.25 trillion = 10,250,000,000,000: ten trillion two hundred and fifty billion\n10.5 trillion = 10,500,000,000,000: ten trillion five hundred billion",
    "primary_subtopic_id": "jss1-math-whole-numbers-trillions"
  },
  {
    "record_id": "ch01-b045-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.5 Counting in big numbers",
      "h3": "Exercise 1.12: Count in trillions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.12: Count in trillions\n\n4. Count in 3 trillions from 987 trillion to 999 trillion. Write down the numbers as digits only and include their full names.",
    "answer_text": "987 trillion = 987,000,000,000,000: nine hundred and eighty seven trillion\n990 trillion = 990,000,000,000,000: nine hundred and ninety trillion\n993 trillion = 993,000,000,000,000: nine hundred and ninety three trillion\n996 trillion = 996,000,000,000,000: nine hundred and ninety six trillion\n999 trillion = 999,000,000,000,000: nine hundred and ninety nine trillion",
    "primary_subtopic_id": "jss1-math-whole-numbers-trillions"
  },
  {
    "record_id": "ch01-b045-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.5 Counting in big numbers",
      "h3": "Exercise 1.12: Count in trillions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 1.12: Count in trillions\n\n5. Count in 4 trillions from 892 trillion to 908 trillion. Write down the numbers as digits only and include their full names.",
    "answer_text": "892 trillion = 892,000,000,000,000: eight hundred and ninety two trillion\n896 trillion = 896,000,000,000,000: eight hundred and ninety six trillion\n900 trillion = 900,000,000,000,000: nine hundred trillion\n904 trillion = 904,000,000,000,000: nine hundred and four trillion\n908 trillion = 908,000,000,000,000: nine hundred and eight trillion",
    "primary_subtopic_id": "jss1-math-whole-numbers-trillions"
  },
  {
    "record_id": "ch01-b046",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 1: Numbers big and small",
      "h2": "1.6 Using large numbers in everyday life",
      "h3": null
    },
    "content_text": "In your daily life, you may come across large numbers in newspapers, on television shows and in some of your other school subjects.\n\nWhenever you get stuck with a large number, write the number in a place value table to help you make sense of it. Remember the order of the place value table:\n\n$$\n\\begin{array}{|c|c|c|c|c|c|c|c|c|c|c|c|c|}\n  \\hline\n    \\textbf{trillion} &\\text{hundred billion} &\\text{ten billion} &\\textbf{billion} & \\text{hundred million} & \\text{ten million} & \\textbf{million} &\\text{hundred thousand} & \\text{ten thousand} & \\textbf{thousand} & \\text{hundred} & \\text{  ten  } & \\text{  unit  }  \\\\\n    (1,000,000,000,000) & (100,000,000,000) & (10,000,000,000) & (1,000,000,000) & (100,000,000) & (10,000,000) & (1,000,000) & (100,000) & (10,000) & (1,000) & (100) & (10) & (1) \\\\\n    \\hline\n     & & & & & & & & & & & &    \\\\\n    \\hline\n    \\end{array}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-whole-numbers-trillions"
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
