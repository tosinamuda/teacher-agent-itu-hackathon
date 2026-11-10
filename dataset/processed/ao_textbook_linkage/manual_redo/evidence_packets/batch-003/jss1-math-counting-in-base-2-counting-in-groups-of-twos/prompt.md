# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-1",
  "topic_key": "jss1-math-counting-in-base-2",
  "topic": "Counting in Base 2",
  "subtopic_id": "jss1-math-counting-in-base-2-counting-in-groups-of-twos",
  "subtopic_title": "Counting in groups of twos",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-counting-in-base-2-counting-in-groups-of-twos-po01",
        "source_performance_objective_index": 1,
        "text": "Count in groups of twos"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "counting-in-base-2-ao-count-groups-of-twos",
          "text": "Count in groups of twos."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch03-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": null,
      "h3": null
    },
    "content_text": "In Chapter 1 you learnt that we use the base ten number system for everyday counting. When we count using the base ten number system, we put objects in groups of ten. We use the numbers 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 as digits to make any other number, no matter how big or how small it is.\n\nThe base ten number system is also called the decimal number system. The prefix \"deci-\" comes from a Latin word that means \"one tenth\".",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-counting-in-base-2-counting-in-groups-of-twos"
  },
  {
    "record_id": "ch03-b002",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.1 The base two number system",
      "h3": null
    },
    "content_text": "In this chapter you will learn about the base two number system. The base two number system is used in computers and other devices that also use computing functions. It is therefore a very important number system.\n\nWhen we count using the base two number system, we put objects in groups of two. We use only two digits, namely 0 and 1, to make up any number.\n\nThe base two number system is also called the binary number system. The prefix \"bi-\" comes from a Latin word that means \"two\" or \"twice\".",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-counting-in-base-2-counting-in-groups-of-twos"
  },
  {
    "record_id": "ch03-b003",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.1 The base two number system",
      "h3": null
    },
    "content_text": "**base ten number system** The base ten number system is a number system that counts in groups of 10, and uses the digits 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 to represent any number. It is also called the decimal number system.\n\n**base two number system** The base two number system is a number system that counts in groups of 2, and uses only the digits 0 and 1 to represent any number. It is also called the binary number system.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-counting-in-base-2-counting-in-groups-of-twos"
  },
  {
    "record_id": "ch03-b004",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.1 The base two number system",
      "h3": "Counting in the base two number system"
    },
    "content_text": "In the base two number system, we go to a new group each time we reach a number that is a power of 2. We therefore count as follows:\n\n$$\n\\begin{array}{l l}\n\\circledast & 1 \\text{ unit} \\\\\n\\color{green}{\\circledast \\, \\circledast} & 1 \\text{ group of two and } 0 \\text{ units} \\\\\n\\color{green}{\\circledast \\, \\circledast} \\, \\color{black}{\\circledast} & 1 \\text{ group of two and } 1 \\text{ unit} \\\\\n\\end{array}\n$$\n\nIf we add another object, we have 2 groups of two, which is 4. We continue counting as follows:\n\n$$\n\\begin{array}{l l}\n\\color{blue}{\\circledast \\, \\circledast \\, \\circledast \\, \\circledast} & 1 \\text{ group of four}, \\space 0 \\text{ groups of two and } 0 \\text{ units} \\\\\n\\color{blue}{\\circledast \\, \\circledast \\, \\circledast \\, \\circledast}\\, \\color{black}{\\circledast} & 1 \\text{ group of four}, \\space 0 \\text{ groups of two and } 1 \\text{ unit} \\\\\n\\color{blue}{\\circledast \\, \\circledast \\, \\circledast \\, \\circledast} \\, \\color{green}{\\circledast \\, \\circledast} & 1 \\text{ group of four}, \\space 1 \\text{ group of two and } 0 \\text{ units} \\\\\n\\color{blue}{\\circledast \\, \\circledast \\, \\circledast \\, \\circledast} \\, \\color{green}{\\circledast \\, \\circledast} \\, \\color{black}{\\circledast} & 1 \\text{ group of four}, \\space 1 \\text{ group of two and } 1 \\text{ unit} \\\\\n\\end{array}\n$$\n\nIf we add another object, we have 3 groups of two, which is 8. We continue counting as follows:\n\n$$\n\\begin{array}{l l}\n\\color{orange}{\\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast} & 1 \\text{ group of eight}, \\space 0 \\text{ groups of four}, \\space 0 \\text{ groups of two and } 0 \\text{ units} \\\\\n\\color{orange}{\\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast} \\, \\color{black}{\\circledast} & 1 \\text{ group of eight}, \\space 0 \\text{ groups of four}, \\space 0 \\text{ groups of two and } 1 \\text{ unit} \\\\\n\\color{orange}{\\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast} \\, \\color{green}{\\circledast \\, \\circledast} & 1 \\text{ group of eight}, \\space 0 \\text{ groups of four}, \\space 1 \\text{ group of two and } 0 \\text{ units} \\\\\n\\color{orange}{\\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast} \\, \\color{green}{\\circledast \\, \\circledast} \\, \\color{black}{\\circledast} & 1 \\text{ group of eight}, \\space 0 \\text{ groups of four}, \\space 1 \\text{ group of two and } 1 \\text{ unit} \\\\\n\\color{orange}{\\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast} \\, \\color{blue}{\\circledast \\, \\circledast \\, \\circledast \\, \\circledast} \\,  & 1 \\text{ group of eight}, \\space 1 \\text{ group of four}, \\space 0 \\text{ groups of two and } 0 \\text{ units} \\\\\n\\end{array}\n$$\n\nWe can carry on like this. When we have 4 groups of two, we count in 16s.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-counting-in-base-2-counting-in-groups-of-twos"
  },
  {
    "record_id": "ch03-b013",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": null
    },
    "content_text": "We can use a place value table to write the numbers 1 to 16 in the decimal number system as binary numbers:\n\n$$\n\\begin{array}{|c|c|c|c|c||c|c|}\n \\hline\n \\text{sixteens} & \\text{eights} & \\text{fours} & \\text{twos} & \\text{units} & \\text{binary number} & \\text{decimal number} \\\\\n (2^4) & (2^3) & (2^2) & (2^1) & (2^0) & & \\\\\n \\hline\n & & & & 1 & 1 & 1 \\\\\n \\hline\n & & & 1 & 0 & 10 & 2 \\\\\n \\hline\n & & & 1 & 1 & 11 & 3 \\\\\n \\hline\n & & 1 & 0 & 0 & 100 & 4 \\\\\n \\hline\n & & 1 & 0 & 1 & 101 & 5 \\\\\n \\hline\n & & 1 & 1 & 0 & 110 & 6 \\\\\n \\hline\n & & 1 & 1 & 1 & 111 & 7 \\\\\n \\hline\n & 1 & 0 & 0 & 0 & 1000 & 8 \\\\\n \\hline\n & 1 & 0 & 0 & 1 & 1001 & 9 \\\\\n \\hline\n & 1 & 0 & 1 & 0 & 1010 & 10 \\\\\n \\hline\n & 1 & 0 & 1 & 1 & 1011 & 11 \\\\\n \\hline\n & 1 & 1 & 0 & 0 & 1100 & 12 \\\\\n \\hline\n & 1 & 1 & 0 & 1 & 1101 & 13 \\\\\n \\hline\n & 1 & 1 & 1 & 0 & 1110 & 14 \\\\\n \\hline\n & 1 & 1 & 1 & 1 & 1111 & 15 \\\\\n \\hline\n 1 & 0 & 0 & 0 & 0 & 10000 & 16 \\\\\n \\hline\n \\end{array}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b014",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "Notation of decimal and binary numbers",
      "h3": null
    },
    "content_text": "When we work with decimal and binary numbers together, we need a way to identify whether a number is a decimal\n number or a binary number. For example, the digits 100 represent one hundred objects in the base ten number system,\n but they represent four objects in the base two number system.\n\nWe use subscripts to tell us which system a certain combination of digits belong to. For example:\n\n - \n $100_{10}$ or\n $100_{\\text{ten}}$ means one hundred\n\n - \n $100_2$ or\n $100_{\\text{two}}$ means four.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b015",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Worked example 3.2: Converting binary numbers to decimal numbers"
    },
    "content_text": "",
    "prompt_text": "Write\n $11010_\\text{two}$ as a base ten number.",
    "answer_text": "- \n Step 1: Draw up a place value table for the powers of 2. Use the number of digits in the given number to help\n you do this.\n\n The number\n $11010_2$ has 5 digits. The place value table must have 5 columns.\n\n Start at the right with\n $2^0$, and count to the left. So this place value table goes up to\n $2^4$.\n\n \n $$\n\\begin{array}{|c|c|c|c|c|}\n \\hline\n \\text{sixteens} & \\text{eights} & \\text{fours} & \\text{twos} & \\text{units} \\\\\n (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n & & & & \\\\\n \\hline\n \\end{array}\n$$ \n\n - \n Step 2: Write the given number in the place value table.\n\n \n $$\n\\begin{array}{|c|c|c|c|c|}\n \\hline\n \\text{sixteens} & \\text{eights} & \\text{fours} & \\text{twos} & \\text{units} \\\\\n (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n 1 & 1 & 0 & 1 & 0 \\\\\n \\hline\n \\end{array}\n$$ \n\n - \n Step 3: Write down the place value of each digit. Add all the values to get the base ten number.\n\n \n $$\n\\begin{align}\n & \\, 2^4+2^3+0+2^1+0 \\\\\n = & \\, 16+8+2 \\\\\n = & \\, 26\n \\end{align}\n$$ \n $$\n\\therefore 11010_\\text{two} = 26_\\text{ten}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b016",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.2: Convert binary numbers to base ten numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.2: Convert binary numbers to base ten numbers\n\nConvert each of the following binary numbers to base ten numbers.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b016-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.2: Convert binary numbers to base ten numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.2: Convert binary numbers to base ten numbers\n\n1. $101_\\text{two}$",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|}\n \\hline\n (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n & & 1 & 0 & 1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n4+1=5\n$$\n $$\n\\therefore 101_\\text{two}=5_\\text{ten}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b016-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.2: Convert binary numbers to base ten numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.2: Convert binary numbers to base ten numbers\n\n2. $1001_\\text{two}$",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|}\n \\hline\n (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n & 1 & 0 & 0 & 1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n8+1=9\n$$\n $$\n\\therefore 1001_\\text{two}=9_\\text{ten}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b016-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.2: Convert binary numbers to base ten numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.2: Convert binary numbers to base ten numbers\n\n3. $1111_\\text{two}$",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|}\n \\hline\n (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n & 1 & 1 & 1 & 1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n8+4+2+1=15\n$$\n $$\n\\therefore 1111_\\text{two}=15_\\text{ten}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b016-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.2: Convert binary numbers to base ten numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.2: Convert binary numbers to base ten numbers\n\n4. $10011_\\text{two}$",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|}\n \\hline\n (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n 1 & 0 & 0 & 1 & 1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n16+2+1=19\n$$\n $$\n\\therefore 10011_\\text{two}=19_\\text{ten}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b016-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.2: Convert binary numbers to base ten numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.2: Convert binary numbers to base ten numbers\n\n5. $11000_\\text{two}$",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|}\n \\hline\n (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n 1 & 1 & 0 & 0 & 0 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n16+8=24\n$$\n $$\n\\therefore 11000_\\text{two}=24_\\text{ten}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b016-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.2: Convert binary numbers to base ten numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.2: Convert binary numbers to base ten numbers\n\n6. $11110_\\text{two}$",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|}\n \\hline\n (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n 1 & 1 & 1 & 1 & 0 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n16+8+4+2=30\n$$\n $$\n\\therefore 11110_\\text{two}=30_\\text{ten}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b016-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.2: Convert binary numbers to base ten numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.2: Convert binary numbers to base ten numbers\n\n7. $101001_\\text{two}$",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|c|}\n \\hline\n (2^5) & (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n 1 & 0 & 1 & 0 & 0 & 1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n32+8+1=41\n$$\n $$\n\\therefore 101001_\\text{two}=41_\\text{ten}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b016-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.2: Convert binary numbers to base ten numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.2: Convert binary numbers to base ten numbers\n\n8. $111010_\\text{two}$",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|c|}\n \\hline\n (2^5) & (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n 1 & 1 & 1 & 0 & 1 & 0 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n32+16+8+2=58\n$$\n $$\n\\therefore 111010_\\text{two}=58_\\text{ten}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b016-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.2: Convert binary numbers to base ten numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.2: Convert binary numbers to base ten numbers\n\n9. $1000111_\\text{two}$",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|c|c|}\n \\hline\n (2^6) & (2^5) & (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n 1 & 0 & 0 & 0 & 1 & 1 & 1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n64+4+2+1=71\n$$\n $$\n\\therefore 1000111_\\text{two}=71_\\text{ten}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b016-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.2: Convert binary numbers to base ten numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.2: Convert binary numbers to base ten numbers\n\n10. $1010011_\\text{two}$",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|c|c|}\n \\hline\n (2^6) & (2^5) & (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n 1 & 0 & 1 & 0 & 0 & 1 & 1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n64+16+2+1=83\n$$\n $$\n\\therefore 1010011_\\text{two}=83_\\text{ten}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b017",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Worked example 3.3: Converting decimal numbers to binary numbers"
    },
    "content_text": "",
    "prompt_text": "Write\n $23_\\text{ten}$ as a base two number.",
    "answer_text": "- \n Step 1: Divide the given number repeatedly by 2, until you get zero. For each division, write down whether\n the remainder is 0 or 1.\n\n \n $$\n\\begin{array}{r|rr}\n 2 & 23 & \\\\\n \\hline\n 2 & 11 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 5 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 2 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 1 & \\text{remainder: }0 \\\\\n \\hline\n & 0 & \\text{remainder: }1 \\\\\n \\hline\n \\end{array}\n$$ \n\n - \n Step 2: Write down the remainders from bottom to top. This gives the corresponding binary number.\n\n $$\n10111\n$$\n $$\n\\therefore 23_\\text{ten}= 10111_\\text{two}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b017-note",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Worked example 3.3: Converting decimal numbers to binary numbers"
    },
    "content_text": "If you do not feel comfortable with the method explained here, you can write the decimal number as\n the sum of powers of 2 and then use a place value table. This is shown in Worked example 3.2.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b018",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.3: Convert decimal numbers to base two numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.3: Convert decimal numbers to base two numbers\n\nConvert each of the following decimal numbers to base two numbers.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b018-hint",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.3: Convert decimal numbers to base two numbers"
    },
    "content_text": "Remember that when you write the remainders, you start from the bottom one and go up to the top one.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b018-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.3: Convert decimal numbers to base two numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.3: Convert decimal numbers to base two numbers\n\n1. $7_\\text{ten}$",
    "answer_text": "$$\n\\begin{array}{r|rr}\n 2 & 7 & \\\\\n \\hline\n 2 & 3 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 1 & \\text{remainder: }1 \\\\\n \\hline\n & 0 & \\text{remainder: }1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n\\therefore 7_\\text{ten}=111_\\text{two}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b018-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.3: Convert decimal numbers to base two numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.3: Convert decimal numbers to base two numbers\n\n2. $11_\\text{ten}$",
    "answer_text": "$$\n\\begin{array}{r|rr}\n 2 & 11 & \\\\\n \\hline\n 2 & 5 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 2 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 1 & \\text{remainder: }0 \\\\\n \\hline\n & 0 & \\text{remainder: }1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n\\therefore 11_\\text{ten}=1011_\\text{two}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b018-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.3: Convert decimal numbers to base two numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.3: Convert decimal numbers to base two numbers\n\n3. $13_\\text{ten}$",
    "answer_text": "$$\n\\begin{array}{r|rr}\n 2 & 13 & \\\\\n \\hline\n 2 & 6 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 3 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 1 & \\text{remainder: }1 \\\\\n \\hline\n & 0 & \\text{remainder: }1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n\\therefore 13_\\text{ten}=1101_\\text{two}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b018-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.3: Convert decimal numbers to base two numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.3: Convert decimal numbers to base two numbers\n\n4. $20_\\text{ten}$",
    "answer_text": "$$\n\\begin{array}{r|rr}\n 2 & 20 & \\\\\n \\hline\n 2 & 10 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 5 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 2 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 1 & \\text{remainder: }0 \\\\\n \\hline \n & 0 & \\text{remainder: }1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n\\therefore 20_\\text{ten}=10100_\\text{two}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b018-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.3: Convert decimal numbers to base two numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.3: Convert decimal numbers to base two numbers\n\n5. $29_\\text{ten}$",
    "answer_text": "$$\n\\begin{array}{r|rr}\n 2 & 29 & \\\\\n \\hline\n 2 & 14 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 7 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 3 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 1 & \\text{remainder: }1 \\\\\n \\hline \n & 0 & \\text{remainder: }1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n\\therefore 29_\\text{ten}=11101_\\text{two}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b018-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.3: Convert decimal numbers to base two numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.3: Convert decimal numbers to base two numbers\n\n6. $36_\\text{ten}$",
    "answer_text": "$$\n\\begin{array}{r|rr}\n 2 & 36 & \\\\\n \\hline\n 2 & 18 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 9 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 4 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 2 & \\text{remainder: }0 \\\\\n \\hline \n 2 & 1 & \\text{remainder: }0 \\\\\n \\hline \n & 0 & \\text{remainder: }1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n\\therefore 36_\\text{ten}=100100_\\text{two}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b018-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.3: Convert decimal numbers to base two numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.3: Convert decimal numbers to base two numbers\n\n7. $44_\\text{ten}$",
    "answer_text": "$$\n\\begin{array}{r|rr}\n 2 & 44 & \\\\\n \\hline\n 2 & 22 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 11 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 5 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 2 & \\text{remainder: }1 \\\\\n \\hline \n 2 & 1 & \\text{remainder: }0 \\\\\n \\hline \n & 0 & \\text{remainder: }1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n\\therefore 44_\\text{ten}=101100_\\text{two}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b018-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.3: Convert decimal numbers to base two numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.3: Convert decimal numbers to base two numbers\n\n8. $65_\\text{ten}$",
    "answer_text": "$$\n\\begin{array}{r|rr}\n 2 & 65 & \\\\\n \\hline\n 2 & 32 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 16 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 8 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 4 & \\text{remainder: }0 \\\\\n \\hline \n 2 & 2 & \\text{remainder: }0 \\\\\n \\hline \n 2 & 1 & \\text{remainder: }0 \\\\\n \\hline \n & 0 & \\text{remainder: }1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n\\therefore 65_\\text{ten}=1000001_\\text{two}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b018-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.3: Convert decimal numbers to base two numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.3: Convert decimal numbers to base two numbers\n\n9. $78_\\text{ten}$",
    "answer_text": "$$\n\\begin{array}{r|rr}\n 2 & 78 & \\\\\n \\hline\n 2 & 39 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 19 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 9 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 4 & \\text{remainder: }1 \\\\\n \\hline \n 2 & 2 & \\text{remainder: }0 \\\\\n \\hline \n 2 & 1 & \\text{remainder: }0 \\\\\n \\hline \n & 0 & \\text{remainder: }1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n\\therefore 78_\\text{ten}=1001110_\\text{two}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b018-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.3: Convert decimal numbers to base two numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.3: Convert decimal numbers to base two numbers\n\n10. $97_\\text{ten}$",
    "answer_text": "$$\n\\begin{array}{r|rr}\n 2 & 97 & \\\\\n \\hline\n 2 & 48 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 24 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 12 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 6 & \\text{remainder: }0 \\\\\n \\hline \n 2 & 3 & \\text{remainder: }0 \\\\\n \\hline \n 2 & 1 & \\text{remainder: }1 \\\\\n \\hline \n & 0 & \\text{remainder: }1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n\\therefore 97_\\text{ten}=1100001_\\text{two}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b019",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.5 Summary",
      "h3": null
    },
    "content_text": "- The base two number system is a number system that counts in groups of 2, and uses only the digits 0 and 1 to\n represent any number.\n\n - In the base ten number system we work with powers of 10. In the base two number system, we work with powers of\n 2.\n\n - We can use place value tables in the base two number system. The place values are powers of 2. For example:\n\n \n $$\n\\begin{array}{|c|c|c|c|c|c|}\n \\hline\n \\text{thirty twos} & \\text{sixteens} & \\text{eights} & \\text{fours} & \\text{twos} & \\text{units} \\\\\n (2^5) & (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n & & & & & \\\\\n \\hline\n \\end{array}\n$$ \n\n - The numbers in the base two number system are called binary numbers. They are all represented by combinations of\n the digits 0 and 1.\n\n - The binary numbers that correspond to the decimal numbers 1 to 10 are: \n\n $$\n\\begin{array}{|c|c|}\n \\hline\n \\text{decimal number} & \\text{binary number} \\\\\n \\hline\n 1& 1 \\\\\n 2& 10 \\\\\n 3& 11 \\\\\n 4& 100 \\\\\n 5& 101 \\\\\n 6& 110 \\\\\n 7& 111 \\\\\n 8& 1000 \\\\\n 9& 1001 \\\\\n 10& 1010 \\\\\n \\hline\n \\end{array}\n$$ \n\n - We use subscripts to tell us which system a certain combination of digits belong to. For example:\n \n - \n $100_{10}$ or\n $100_{\\text{ten}}$ means one hundred\n\n - \n $100_2$ or\n $100_{\\text{two}}$ means four\n\n \n\n - We can convert binary numbers to decimal numbers, and decimal numbers to binary numbers.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
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
  "topic_key": "jss1-math-counting-in-base-2",
  "topic": "Counting in Base 2",
  "subtopic_id": "jss1-math-counting-in-base-2-counting-in-groups-of-twos",
  "subtopic_title": "Counting in groups of twos",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-counting-in-base-2-counting-in-groups-of-twos-po01",
        "source_performance_objective_index": 1,
        "text": "Count in groups of twos"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "counting-in-base-2-ao-count-groups-of-twos",
          "text": "Count in groups of twos."
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
    "record_id": "ch03-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": null,
      "h3": null
    },
    "content_text": "In Chapter 1 you learnt that we use the base ten number system for everyday counting. When we count using the base ten number system, we put objects in groups of ten. We use the numbers 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 as digits to make any other number, no matter how big or how small it is.\n\nThe base ten number system is also called the decimal number system. The prefix \"deci-\" comes from a Latin word that means \"one tenth\".",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-counting-in-base-2-counting-in-groups-of-twos"
  },
  {
    "record_id": "ch03-b002",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.1 The base two number system",
      "h3": null
    },
    "content_text": "In this chapter you will learn about the base two number system. The base two number system is used in computers and other devices that also use computing functions. It is therefore a very important number system.\n\nWhen we count using the base two number system, we put objects in groups of two. We use only two digits, namely 0 and 1, to make up any number.\n\nThe base two number system is also called the binary number system. The prefix \"bi-\" comes from a Latin word that means \"two\" or \"twice\".",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-counting-in-base-2-counting-in-groups-of-twos"
  },
  {
    "record_id": "ch03-b003",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.1 The base two number system",
      "h3": null
    },
    "content_text": "**base ten number system** The base ten number system is a number system that counts in groups of 10, and uses the digits 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 to represent any number. It is also called the decimal number system.\n\n**base two number system** The base two number system is a number system that counts in groups of 2, and uses only the digits 0 and 1 to represent any number. It is also called the binary number system.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-counting-in-base-2-counting-in-groups-of-twos"
  },
  {
    "record_id": "ch03-b004",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.1 The base two number system",
      "h3": "Counting in the base two number system"
    },
    "content_text": "In the base two number system, we go to a new group each time we reach a number that is a power of 2. We therefore count as follows:\n\n$$\n\\begin{array}{l l}\n\\circledast & 1 \\text{ unit} \\\\\n\\color{green}{\\circledast \\, \\circledast} & 1 \\text{ group of two and } 0 \\text{ units} \\\\\n\\color{green}{\\circledast \\, \\circledast} \\, \\color{black}{\\circledast} & 1 \\text{ group of two and } 1 \\text{ unit} \\\\\n\\end{array}\n$$\n\nIf we add another object, we have 2 groups of two, which is 4. We continue counting as follows:\n\n$$\n\\begin{array}{l l}\n\\color{blue}{\\circledast \\, \\circledast \\, \\circledast \\, \\circledast} & 1 \\text{ group of four}, \\space 0 \\text{ groups of two and } 0 \\text{ units} \\\\\n\\color{blue}{\\circledast \\, \\circledast \\, \\circledast \\, \\circledast}\\, \\color{black}{\\circledast} & 1 \\text{ group of four}, \\space 0 \\text{ groups of two and } 1 \\text{ unit} \\\\\n\\color{blue}{\\circledast \\, \\circledast \\, \\circledast \\, \\circledast} \\, \\color{green}{\\circledast \\, \\circledast} & 1 \\text{ group of four}, \\space 1 \\text{ group of two and } 0 \\text{ units} \\\\\n\\color{blue}{\\circledast \\, \\circledast \\, \\circledast \\, \\circledast} \\, \\color{green}{\\circledast \\, \\circledast} \\, \\color{black}{\\circledast} & 1 \\text{ group of four}, \\space 1 \\text{ group of two and } 1 \\text{ unit} \\\\\n\\end{array}\n$$\n\nIf we add another object, we have 3 groups of two, which is 8. We continue counting as follows:\n\n$$\n\\begin{array}{l l}\n\\color{orange}{\\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast} & 1 \\text{ group of eight}, \\space 0 \\text{ groups of four}, \\space 0 \\text{ groups of two and } 0 \\text{ units} \\\\\n\\color{orange}{\\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast} \\, \\color{black}{\\circledast} & 1 \\text{ group of eight}, \\space 0 \\text{ groups of four}, \\space 0 \\text{ groups of two and } 1 \\text{ unit} \\\\\n\\color{orange}{\\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast} \\, \\color{green}{\\circledast \\, \\circledast} & 1 \\text{ group of eight}, \\space 0 \\text{ groups of four}, \\space 1 \\text{ group of two and } 0 \\text{ units} \\\\\n\\color{orange}{\\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast} \\, \\color{green}{\\circledast \\, \\circledast} \\, \\color{black}{\\circledast} & 1 \\text{ group of eight}, \\space 0 \\text{ groups of four}, \\space 1 \\text{ group of two and } 1 \\text{ unit} \\\\\n\\color{orange}{\\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast \\, \\circledast} \\, \\color{blue}{\\circledast \\, \\circledast \\, \\circledast \\, \\circledast} \\,  & 1 \\text{ group of eight}, \\space 1 \\text{ group of four}, \\space 0 \\text{ groups of two and } 0 \\text{ units} \\\\\n\\end{array}\n$$\n\nWe can carry on like this. When we have 4 groups of two, we count in 16s.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-counting-in-base-2-counting-in-groups-of-twos"
  },
  {
    "record_id": "ch03-b013",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": null
    },
    "content_text": "We can use a place value table to write the numbers 1 to 16 in the decimal number system as binary numbers:\n\n$$\n\\begin{array}{|c|c|c|c|c||c|c|}\n \\hline\n \\text{sixteens} & \\text{eights} & \\text{fours} & \\text{twos} & \\text{units} & \\text{binary number} & \\text{decimal number} \\\\\n (2^4) & (2^3) & (2^2) & (2^1) & (2^0) & & \\\\\n \\hline\n & & & & 1 & 1 & 1 \\\\\n \\hline\n & & & 1 & 0 & 10 & 2 \\\\\n \\hline\n & & & 1 & 1 & 11 & 3 \\\\\n \\hline\n & & 1 & 0 & 0 & 100 & 4 \\\\\n \\hline\n & & 1 & 0 & 1 & 101 & 5 \\\\\n \\hline\n & & 1 & 1 & 0 & 110 & 6 \\\\\n \\hline\n & & 1 & 1 & 1 & 111 & 7 \\\\\n \\hline\n & 1 & 0 & 0 & 0 & 1000 & 8 \\\\\n \\hline\n & 1 & 0 & 0 & 1 & 1001 & 9 \\\\\n \\hline\n & 1 & 0 & 1 & 0 & 1010 & 10 \\\\\n \\hline\n & 1 & 0 & 1 & 1 & 1011 & 11 \\\\\n \\hline\n & 1 & 1 & 0 & 0 & 1100 & 12 \\\\\n \\hline\n & 1 & 1 & 0 & 1 & 1101 & 13 \\\\\n \\hline\n & 1 & 1 & 1 & 0 & 1110 & 14 \\\\\n \\hline\n & 1 & 1 & 1 & 1 & 1111 & 15 \\\\\n \\hline\n 1 & 0 & 0 & 0 & 0 & 10000 & 16 \\\\\n \\hline\n \\end{array}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b014",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "Notation of decimal and binary numbers",
      "h3": null
    },
    "content_text": "When we work with decimal and binary numbers together, we need a way to identify whether a number is a decimal\n number or a binary number. For example, the digits 100 represent one hundred objects in the base ten number system,\n but they represent four objects in the base two number system.\n\nWe use subscripts to tell us which system a certain combination of digits belong to. For example:\n\n - \n $100_{10}$ or\n $100_{\\text{ten}}$ means one hundred\n\n - \n $100_2$ or\n $100_{\\text{two}}$ means four.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b015",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Worked example 3.2: Converting binary numbers to decimal numbers"
    },
    "content_text": "",
    "prompt_text": "Write\n $11010_\\text{two}$ as a base ten number.",
    "answer_text": "- \n Step 1: Draw up a place value table for the powers of 2. Use the number of digits in the given number to help\n you do this.\n\n The number\n $11010_2$ has 5 digits. The place value table must have 5 columns.\n\n Start at the right with\n $2^0$, and count to the left. So this place value table goes up to\n $2^4$.\n\n \n $$\n\\begin{array}{|c|c|c|c|c|}\n \\hline\n \\text{sixteens} & \\text{eights} & \\text{fours} & \\text{twos} & \\text{units} \\\\\n (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n & & & & \\\\\n \\hline\n \\end{array}\n$$ \n\n - \n Step 2: Write the given number in the place value table.\n\n \n $$\n\\begin{array}{|c|c|c|c|c|}\n \\hline\n \\text{sixteens} & \\text{eights} & \\text{fours} & \\text{twos} & \\text{units} \\\\\n (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n 1 & 1 & 0 & 1 & 0 \\\\\n \\hline\n \\end{array}\n$$ \n\n - \n Step 3: Write down the place value of each digit. Add all the values to get the base ten number.\n\n \n $$\n\\begin{align}\n & \\, 2^4+2^3+0+2^1+0 \\\\\n = & \\, 16+8+2 \\\\\n = & \\, 26\n \\end{align}\n$$ \n $$\n\\therefore 11010_\\text{two} = 26_\\text{ten}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b016",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.2: Convert binary numbers to base ten numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.2: Convert binary numbers to base ten numbers\n\nConvert each of the following binary numbers to base ten numbers.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b016-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.2: Convert binary numbers to base ten numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.2: Convert binary numbers to base ten numbers\n\n1. $101_\\text{two}$",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|}\n \\hline\n (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n & & 1 & 0 & 1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n4+1=5\n$$\n $$\n\\therefore 101_\\text{two}=5_\\text{ten}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b016-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.2: Convert binary numbers to base ten numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.2: Convert binary numbers to base ten numbers\n\n2. $1001_\\text{two}$",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|}\n \\hline\n (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n & 1 & 0 & 0 & 1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n8+1=9\n$$\n $$\n\\therefore 1001_\\text{two}=9_\\text{ten}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b016-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.2: Convert binary numbers to base ten numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.2: Convert binary numbers to base ten numbers\n\n3. $1111_\\text{two}$",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|}\n \\hline\n (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n & 1 & 1 & 1 & 1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n8+4+2+1=15\n$$\n $$\n\\therefore 1111_\\text{two}=15_\\text{ten}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b016-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.2: Convert binary numbers to base ten numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.2: Convert binary numbers to base ten numbers\n\n4. $10011_\\text{two}$",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|}\n \\hline\n (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n 1 & 0 & 0 & 1 & 1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n16+2+1=19\n$$\n $$\n\\therefore 10011_\\text{two}=19_\\text{ten}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b016-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.2: Convert binary numbers to base ten numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.2: Convert binary numbers to base ten numbers\n\n5. $11000_\\text{two}$",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|}\n \\hline\n (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n 1 & 1 & 0 & 0 & 0 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n16+8=24\n$$\n $$\n\\therefore 11000_\\text{two}=24_\\text{ten}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b016-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.2: Convert binary numbers to base ten numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.2: Convert binary numbers to base ten numbers\n\n6. $11110_\\text{two}$",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|}\n \\hline\n (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n 1 & 1 & 1 & 1 & 0 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n16+8+4+2=30\n$$\n $$\n\\therefore 11110_\\text{two}=30_\\text{ten}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b016-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.2: Convert binary numbers to base ten numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.2: Convert binary numbers to base ten numbers\n\n7. $101001_\\text{two}$",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|c|}\n \\hline\n (2^5) & (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n 1 & 0 & 1 & 0 & 0 & 1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n32+8+1=41\n$$\n $$\n\\therefore 101001_\\text{two}=41_\\text{ten}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b016-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.2: Convert binary numbers to base ten numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.2: Convert binary numbers to base ten numbers\n\n8. $111010_\\text{two}$",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|c|}\n \\hline\n (2^5) & (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n 1 & 1 & 1 & 0 & 1 & 0 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n32+16+8+2=58\n$$\n $$\n\\therefore 111010_\\text{two}=58_\\text{ten}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b016-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.2: Convert binary numbers to base ten numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.2: Convert binary numbers to base ten numbers\n\n9. $1000111_\\text{two}$",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|c|c|}\n \\hline\n (2^6) & (2^5) & (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n 1 & 0 & 0 & 0 & 1 & 1 & 1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n64+4+2+1=71\n$$\n $$\n\\therefore 1000111_\\text{two}=71_\\text{ten}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b016-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.2: Convert binary numbers to base ten numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.2: Convert binary numbers to base ten numbers\n\n10. $1010011_\\text{two}$",
    "answer_text": "$$\n\\begin{array}{|c|c|c|c|c|c|c|}\n \\hline\n (2^6) & (2^5) & (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n 1 & 0 & 1 & 0 & 0 & 1 & 1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n64+16+2+1=83\n$$\n $$\n\\therefore 1010011_\\text{two}=83_\\text{ten}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b017",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Worked example 3.3: Converting decimal numbers to binary numbers"
    },
    "content_text": "",
    "prompt_text": "Write\n $23_\\text{ten}$ as a base two number.",
    "answer_text": "- \n Step 1: Divide the given number repeatedly by 2, until you get zero. For each division, write down whether\n the remainder is 0 or 1.\n\n \n $$\n\\begin{array}{r|rr}\n 2 & 23 & \\\\\n \\hline\n 2 & 11 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 5 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 2 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 1 & \\text{remainder: }0 \\\\\n \\hline\n & 0 & \\text{remainder: }1 \\\\\n \\hline\n \\end{array}\n$$ \n\n - \n Step 2: Write down the remainders from bottom to top. This gives the corresponding binary number.\n\n $$\n10111\n$$\n $$\n\\therefore 23_\\text{ten}= 10111_\\text{two}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b017-note",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Worked example 3.3: Converting decimal numbers to binary numbers"
    },
    "content_text": "If you do not feel comfortable with the method explained here, you can write the decimal number as\n the sum of powers of 2 and then use a place value table. This is shown in Worked example 3.2.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b018",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.3: Convert decimal numbers to base two numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.3: Convert decimal numbers to base two numbers\n\nConvert each of the following decimal numbers to base two numbers.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b018-hint",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.3: Convert decimal numbers to base two numbers"
    },
    "content_text": "Remember that when you write the remainders, you start from the bottom one and go up to the top one.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b018-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.3: Convert decimal numbers to base two numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.3: Convert decimal numbers to base two numbers\n\n1. $7_\\text{ten}$",
    "answer_text": "$$\n\\begin{array}{r|rr}\n 2 & 7 & \\\\\n \\hline\n 2 & 3 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 1 & \\text{remainder: }1 \\\\\n \\hline\n & 0 & \\text{remainder: }1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n\\therefore 7_\\text{ten}=111_\\text{two}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b018-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.3: Convert decimal numbers to base two numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.3: Convert decimal numbers to base two numbers\n\n2. $11_\\text{ten}$",
    "answer_text": "$$\n\\begin{array}{r|rr}\n 2 & 11 & \\\\\n \\hline\n 2 & 5 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 2 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 1 & \\text{remainder: }0 \\\\\n \\hline\n & 0 & \\text{remainder: }1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n\\therefore 11_\\text{ten}=1011_\\text{two}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b018-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.3: Convert decimal numbers to base two numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.3: Convert decimal numbers to base two numbers\n\n3. $13_\\text{ten}$",
    "answer_text": "$$\n\\begin{array}{r|rr}\n 2 & 13 & \\\\\n \\hline\n 2 & 6 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 3 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 1 & \\text{remainder: }1 \\\\\n \\hline\n & 0 & \\text{remainder: }1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n\\therefore 13_\\text{ten}=1101_\\text{two}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b018-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.3: Convert decimal numbers to base two numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.3: Convert decimal numbers to base two numbers\n\n4. $20_\\text{ten}$",
    "answer_text": "$$\n\\begin{array}{r|rr}\n 2 & 20 & \\\\\n \\hline\n 2 & 10 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 5 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 2 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 1 & \\text{remainder: }0 \\\\\n \\hline \n & 0 & \\text{remainder: }1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n\\therefore 20_\\text{ten}=10100_\\text{two}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b018-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.3: Convert decimal numbers to base two numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.3: Convert decimal numbers to base two numbers\n\n5. $29_\\text{ten}$",
    "answer_text": "$$\n\\begin{array}{r|rr}\n 2 & 29 & \\\\\n \\hline\n 2 & 14 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 7 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 3 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 1 & \\text{remainder: }1 \\\\\n \\hline \n & 0 & \\text{remainder: }1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n\\therefore 29_\\text{ten}=11101_\\text{two}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b018-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.3: Convert decimal numbers to base two numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.3: Convert decimal numbers to base two numbers\n\n6. $36_\\text{ten}$",
    "answer_text": "$$\n\\begin{array}{r|rr}\n 2 & 36 & \\\\\n \\hline\n 2 & 18 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 9 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 4 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 2 & \\text{remainder: }0 \\\\\n \\hline \n 2 & 1 & \\text{remainder: }0 \\\\\n \\hline \n & 0 & \\text{remainder: }1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n\\therefore 36_\\text{ten}=100100_\\text{two}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b018-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.3: Convert decimal numbers to base two numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.3: Convert decimal numbers to base two numbers\n\n7. $44_\\text{ten}$",
    "answer_text": "$$\n\\begin{array}{r|rr}\n 2 & 44 & \\\\\n \\hline\n 2 & 22 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 11 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 5 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 2 & \\text{remainder: }1 \\\\\n \\hline \n 2 & 1 & \\text{remainder: }0 \\\\\n \\hline \n & 0 & \\text{remainder: }1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n\\therefore 44_\\text{ten}=101100_\\text{two}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b018-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.3: Convert decimal numbers to base two numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.3: Convert decimal numbers to base two numbers\n\n8. $65_\\text{ten}$",
    "answer_text": "$$\n\\begin{array}{r|rr}\n 2 & 65 & \\\\\n \\hline\n 2 & 32 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 16 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 8 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 4 & \\text{remainder: }0 \\\\\n \\hline \n 2 & 2 & \\text{remainder: }0 \\\\\n \\hline \n 2 & 1 & \\text{remainder: }0 \\\\\n \\hline \n & 0 & \\text{remainder: }1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n\\therefore 65_\\text{ten}=1000001_\\text{two}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b018-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.3: Convert decimal numbers to base two numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.3: Convert decimal numbers to base two numbers\n\n9. $78_\\text{ten}$",
    "answer_text": "$$\n\\begin{array}{r|rr}\n 2 & 78 & \\\\\n \\hline\n 2 & 39 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 19 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 9 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 4 & \\text{remainder: }1 \\\\\n \\hline \n 2 & 2 & \\text{remainder: }0 \\\\\n \\hline \n 2 & 1 & \\text{remainder: }0 \\\\\n \\hline \n & 0 & \\text{remainder: }1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n\\therefore 78_\\text{ten}=1001110_\\text{two}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b018-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.3 Binary numbers",
      "h3": "Exercise 3.3: Convert decimal numbers to base two numbers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 3.3: Convert decimal numbers to base two numbers\n\n10. $97_\\text{ten}$",
    "answer_text": "$$\n\\begin{array}{r|rr}\n 2 & 97 & \\\\\n \\hline\n 2 & 48 & \\text{remainder: }1 \\\\\n \\hline\n 2 & 24 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 12 & \\text{remainder: }0 \\\\\n \\hline\n 2 & 6 & \\text{remainder: }0 \\\\\n \\hline \n 2 & 3 & \\text{remainder: }0 \\\\\n \\hline \n 2 & 1 & \\text{remainder: }1 \\\\\n \\hline \n & 0 & \\text{remainder: }1 \\\\\n \\hline\n \\end{array}\n$$ \n $$\n\\therefore 97_\\text{ten}=1100001_\\text{two}\n$$",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
  },
  {
    "record_id": "ch03-b019",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 3: Binary numbers",
      "h2": "3.5 Summary",
      "h3": null
    },
    "content_text": "- The base two number system is a number system that counts in groups of 2, and uses only the digits 0 and 1 to\n represent any number.\n\n - In the base ten number system we work with powers of 10. In the base two number system, we work with powers of\n 2.\n\n - We can use place value tables in the base two number system. The place values are powers of 2. For example:\n\n \n $$\n\\begin{array}{|c|c|c|c|c|c|}\n \\hline\n \\text{thirty twos} & \\text{sixteens} & \\text{eights} & \\text{fours} & \\text{twos} & \\text{units} \\\\\n (2^5) & (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\\\\n \\hline\n & & & & & \\\\\n \\hline\n \\end{array}\n$$ \n\n - The numbers in the base two number system are called binary numbers. They are all represented by combinations of\n the digits 0 and 1.\n\n - The binary numbers that correspond to the decimal numbers 1 to 10 are: \n\n $$\n\\begin{array}{|c|c|}\n \\hline\n \\text{decimal number} & \\text{binary number} \\\\\n \\hline\n 1& 1 \\\\\n 2& 10 \\\\\n 3& 11 \\\\\n 4& 100 \\\\\n 5& 101 \\\\\n 6& 110 \\\\\n 7& 111 \\\\\n 8& 1000 \\\\\n 9& 1001 \\\\\n 10& 1010 \\\\\n \\hline\n \\end{array}\n$$ \n\n - We use subscripts to tell us which system a certain combination of digits belong to. For example:\n \n - \n $100_{10}$ or\n $100_{\\text{ten}}$ means one hundred\n\n - \n $100_2$ or\n $100_{\\text{two}}$ means four\n\n \n\n - We can convert binary numbers to decimal numbers, and decimal numbers to binary numbers.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2"
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
