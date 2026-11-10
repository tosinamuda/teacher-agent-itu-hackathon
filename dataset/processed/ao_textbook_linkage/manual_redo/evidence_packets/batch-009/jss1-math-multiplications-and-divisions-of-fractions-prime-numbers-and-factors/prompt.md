# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-2",
  "topic_key": "jss1-math-multiplications-and-divisions-of-fractions",
  "topic": "Multiplications and Divisions of Fractions",
  "subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors",
  "subtopic_title": "Prime numbers and factors",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors-po01",
        "source_performance_objective_index": 1,
        "text": "Identify prime numbers"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "prime-numbers-and-factors-ao-identify-prime-numbers",
          "text": "Identify prime numbers."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors-po02",
        "source_performance_objective_index": 2,
        "text": "Find the factors of a given whole number"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "prime-numbers-and-factors-ao-find-factors",
          "text": "Find the factors of a given whole number."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors-po03",
        "source_performance_objective_index": 3,
        "text": "Express a number as a product of its prime factors"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "prime-numbers-and-factors-ao-express-prime-factors",
          "text": "Express a number as a product of its prime factors."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch02-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Factors"
    },
    "content_text": "A factor is any of the two or more whole numbers we multiply to get a product. For example: $6 \\times 2 = 12$. The numbers 6 and 2 are factors of 12.\n\nA factor is also described as a whole number that divides into a larger number without a remainder. For example: $\\frac{12}{6} = 2$. The number 6 divides perfectly into 12. Therefore, the number 6 is a factor of 12.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b002",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Factors"
    },
    "content_text": "factor\n\nA factor is a whole number that divides into a larger number without a remainder.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b003",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Worked example 2.1: Factors"
    },
    "content_text": "",
    "prompt_text": "Find all the factors of the number 60.",
    "answer_text": "Step 1: Any number larger than 1 has the number itself and 1 as factors.\n\n$$\n1 \\times 60=60\n$$\n\nStep 2: Start with 2 and see if it divides into 60 without a remainder.\n\n$$\n\\frac{60}{2} = 30\n$$\n\n$$\n2 \\times 30=60\n$$\n\nStep 3: Try each consecutive number to see if it divides into 60 without a remainder. Stop when you get to a number that you already have as an answer.\n\n$$\n\\begin{array}{2}\n \\frac{60}{3} = 20 \\hspace{10mm} &3 \\times 20 = 60 \\\\\n \\frac{60}{4} = 15 &4 \\times 15 = 60 \\\\\n \\frac{60}{5} = 12 &5 \\times 12 = 60 \\\\\n \\frac{60}{6} = 10 &6 \\times 10 = 60 \\\\\n \\end{array}\n$$\n\nThe numbers 7, 8 and 9 do not divide into 60 without a remainder, so they are not factors of 60.\n\nYou already have the number 10, as 60 divided by 6 is 10, so you can stop there.\n\n$$\n\\frac{60}{10} = 6\n$$\n\nStep 4: List all the factors from the smallest number to the largest number.\n\nThe factors of 60 are: 1; 2; 3; 4; 5; 6; 10; 12; 15; 20; 30; 60",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b004",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.1: Find factors"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.1: Find factors\n\nFind all the factors of the following numbers:",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b004-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.1: Find factors"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.1: Find factors\n\n1. 54",
    "answer_text": "$$\n\\begin{array}{2}\n\\text{1 and itself} \\hspace{10mm}&1 \\times 54=54 \\\\\n\\frac{54}{2} = 27 &2 \\times 27 = 54 \\\\\n\\frac{54}{3} = 18 &3 \\times 18 = 54 \\\\\n\\frac{54}{6} = 9 & 6 \\times 9 = 54 \\\\\n\\frac{54}{9} = 6 & \\text{already divided}\n\\end{array}\n$$\n\nThe factors of 54 are: 1; 2; 3; 6; 9; 18; 27; 54",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b004-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.1: Find factors"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.1: Find factors\n\n2. 39",
    "answer_text": "$$\n\\begin{array}{2}\n\\text{1 and itself} \\hspace{10mm}&1 \\times 39=39 \\\\\n\\frac{39}{3} = 13 & 3 \\times 13 = 39 \\\\\n\\frac{39}{13} = 3 & \\text{already divided}\n\\end{array}\n$$\n\nThe factors of 39 are: 1; 3; 13; 39",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b004-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.1: Find factors"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.1: Find factors\n\n3. 45",
    "answer_text": "$$\n\\begin{array}{2}\n\\text{1 and itself} \\hspace{10mm}&1 \\times 45=45 \\\\\n\\frac{45}{3} = 15 & 3 \\times 15 = 45 \\\\\n\\frac{45}{5} = 9 & 5 \\times 9 = 45 \\\\\n\\frac{45}{9} = 5 & \\text{already divided}\n\\end{array}\n$$\n\nThe factors of 45 are: 1; 3; 5; 9; 15; 45",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b005",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Prime factors"
    },
    "content_text": "The number 3 has only two factors: 1 and 3. Similarly, the number 11 has only two factors: 1 and 11. These are examples of prime numbers.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b006",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Prime factors"
    },
    "content_text": "prime number\n\nA prime number is a number that has only two factors: 1 and the number itself.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b007",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Prime factors"
    },
    "content_text": "The prime numbers between 1 and 100 are highlighted in the grid below.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-02-001.png)\n\nprime factors\nThese are the factors of a number that are also prime numbers. Any non-prime number can be broken down into prime factors. We can then write the number as a product of its prime factors.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b008",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Prime factors"
    },
    "content_text": "prime factor\n\nA prime factor is a factor that is also a prime number.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b009",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Worked example 2.2: Prime factors"
    },
    "content_text": "",
    "prompt_text": "Find the prime factors of 80.",
    "answer_text": "Step 1: Find the smallest prime number that is a factor of 80. Express 80 as a product of two factors.\n\n$$\n\\frac{80}{2}=40\n$$\n\n$$\n80=2 \\times 40\n$$\n\nStep 2: Find the smallest prime number that is a factor of the non-prime factor from Step 1. Express 80 as a product of three factors.\n\n$$\n\\frac{40}{2}=20\n$$\n\n$$\n80=2 \\times 2 \\times 20\n$$\n\nStep 3: Repeat Step 2 until 80 is expressed as a product of only prime numbers.\n\n$$\n\\frac{20}{2}=10\n$$\n\n$$\n80=2 \\times 2 \\times 2 \\times 10\n$$\n\n$$\n\\frac{10}{2}=5\n$$\n\n$$\n80=2 \\times 2 \\times 2 \\times 5\n$$\n\nRemember that 1 is not a prime number.",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b010",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.2: Express numbers as products of prime factors"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.2: Express numbers as products of prime factors\n\nExpress the following numbers as products of prime factors:",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b010-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.2: Express numbers as products of prime factors"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.2: Express numbers as products of prime factors\n\nExpress the following numbers as products of prime factors:\n\n1. 30",
    "answer_text": "$$\n\\begin{array}{2} & \\frac{30}{2}=15 &\\hspace{10 mm}30=2 \\times 15  ewline & \\frac{15}{3}=5 &\\hspace{10mm} 30=2 \\times 3 \\times 5 \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b010-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.2: Express numbers as products of prime factors"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.2: Express numbers as products of prime factors\n\nExpress the following numbers as products of prime factors:\n\n2. 140",
    "answer_text": "$$\n\\begin{array}{2} & \\frac{140}{2}=70 &\\hspace{10 mm}140=2 \\times 70  ewline & \\frac{70}{2}=35 &\\hspace{10mm} 140=2 \\times 2 \\times 35  ewline & \\frac{35}{5}=7 &\\hspace{10mm} 140=2 \\times 2 \\times 5 \\times 7  ewline \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b010-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.2: Express numbers as products of prime factors"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.2: Express numbers as products of prime factors\n\nExpress the following numbers as products of prime factors:\n\n3. 195",
    "answer_text": "$$\n\\begin{array}{2} & \\frac{195}{3}=65 &\\hspace{10 mm}195=3 \\times 65  ewline & \\frac{65}{5}=13 &\\hspace{10mm} 195=3 \\times 5 \\times 13  ewline \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b010-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.2: Express numbers as products of prime factors"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.2: Express numbers as products of prime factors\n\nExpress the following numbers as products of prime factors:\n\n4. 252",
    "answer_text": "$$\n\\begin{array}{2} & \\frac{252}{2}=126 &\\hspace{10 mm}252=2 \\times 126  ewline & \\frac{126}{2}=63 &\\hspace{10mm} 252=2 \\times 2 \\times 63  ewline & \\frac{63}{3}=21 &\\hspace{10mm} 252=2 \\times 2 \\times 3 \\times 21  ewline & \\frac{21}{3}=7 &\\hspace{10mm} 252=2 \\times 2 \\times 3 \\times 3 \\times 7  ewline \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b010-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.2: Express numbers as products of prime factors"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.2: Express numbers as products of prime factors\n\nExpress the following numbers as products of prime factors:\n\n5. 297",
    "answer_text": "$$\n\\begin{array}{2} & \\frac{297}{3}=99 &\\hspace{10 mm}297=3 \\times 99  ewline & \\frac{99}{3}=33 &\\hspace{10mm} 297=3 \\times 3 \\times 33  ewline & \\frac{33}{3}=11 &\\hspace{10mm} 297=3 \\times 3 \\times 3 \\times 11  ewline \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b011",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Index form"
    },
    "content_text": "Finding and writing down the prime factors of large numbers can become confusing. To make the process easier, we may use continued division and write the prime factors in index form. The index or power of a number tells us how many times we multiply the number by itself. For example, $2^4$ means $2 \\times 2 \\times 2 \\times 2$. In this case, 4 is the power or index of 2.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b012",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Index form"
    },
    "content_text": "index form\nIndex form tells you how many times to use the same number in a multiplication by writing a superscript next to the number, for example $3^2$ means multiply 3 by 3.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b013",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Index form"
    },
    "content_text": "An index of 1 means a number is not multiplied by itself. Therefore, $2$ and $2^1$ have the same meaning.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b014",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Worked example 2.3: Prime factors in index form"
    },
    "content_text": "",
    "prompt_text": "Find the prime factors of 180 and write them in index form.",
    "answer_text": "Step 1: Divide the smallest prime factor of 180 until it cannot divide any further.\n\n$$\n\\begin{array}{r | r}\n 2 & 180  ewline\n \\hline\n 2 & 90  ewline\n \\hline\n & 45\n\\end{array}\n$$\n\nStep 2: Move to the next prime factor of 180. Keep on dividing until it cannot divide any further.\n\n$$\n\\begin{array}{r | r}\n 2 & 180  ewline\n \\hline\n 2 & 90  ewline\n \\hline\n 3 & 45  ewline\n \\hline\n 3 & 15  ewline\n \\hline\n & 5\n\\end{array}\n$$\n\nStep 3: Repeat Step 2 until you get 1 as an answer.\n\n$$\n\\begin{array}{r | r}\n 2 & 180  ewline\n \\hline\n 2 & 90  ewline\n \\hline\n 3 & 45  ewline\n \\hline\n 3 & 15  ewline\n \\hline\n 5 & 5  ewline\n \\hline\n & 1\n\\end{array}\n$$\n\nStep 4: Write down all the prime factors of 180. Use superscripts to write the index of each prime factor, that is, how many times the prime factor divided.\n\n$$\n180 = 2^2 \\times 3^2 \\times 5\n$$\n\nThe index of each prime factor shows us how many times we must multiply each prime factor to get 180 again:\n\n$$\n180 = 2^2 \\times 3^2 \\times 5 = 2 \\times 2 \\times 3 \\times 3 \\times 5\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b015",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.3: Express numbers as products of prime factors in index form"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.3: Express numbers as products of prime factors in index form\n\nExpress the following numbers as prime factors in index form:",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b015-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.3: Express numbers as products of prime factors in index form"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.3: Express numbers as products of prime factors in index form\n\nExpress the following numbers as prime factors in index form:\n\n1. 60",
    "answer_text": "$$\n\\begin{array}{r | r}\n 2 & 60  ewline\n \\hline 2 & 30  ewline\n \\hline 3 & 15  ewline\n \\hline 5 & 5  ewline\n \\hline & 1\n\\end{array}\n$$\n\n$$\n60=2^2 \\times 3 \\times 5\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b015-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.3: Express numbers as products of prime factors in index form"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.3: Express numbers as products of prime factors in index form\n\nExpress the following numbers as prime factors in index form:\n\n2. 144",
    "answer_text": "$$\n\\begin{array}{r | r}\n 2 & 144  ewline\n \\hline 2 & 72  ewline\n \\hline 2 & 36  ewline\n \\hline 2 & 18  ewline\n \\hline 3 & 9  ewline\n \\hline 3 & 3  ewline\n \\hline & 1\n\\end{array}\n$$\n\n$$\n144=2^4 \\times 3^2\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b015-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.3: Express numbers as products of prime factors in index form"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.3: Express numbers as products of prime factors in index form\n\nExpress the following numbers as prime factors in index form:\n\n3. 198",
    "answer_text": "$$\n\\begin{array}{r | r}\n 2 & 198  ewline\n \\hline 3 & 99  ewline\n \\hline 3 & 33  ewline\n \\hline 11 & 11  ewline\n \\hline & 1\n\\end{array}\n$$\n\n$$\n198=2\\times 3^2 \\times 11\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b015-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.3: Express numbers as products of prime factors in index form"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.3: Express numbers as products of prime factors in index form\n\nExpress the following numbers as prime factors in index form:\n\n4. 300",
    "answer_text": "$$\n\\begin{array}{r | r}\n 2 & 300  ewline\n \\hline 2 & 150  ewline\n \\hline 3 & 75  ewline\n \\hline 5 & 25  ewline\n \\hline 5 & 5  ewline\n \\hline & 1\n\\end{array}\n$$\n\n$$\n300=2^2 \\times 3\\times 5^2\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b015-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.3: Express numbers as products of prime factors in index form"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.3: Express numbers as products of prime factors in index form\n\nExpress the following numbers as prime factors in index form:\n\n5. 3 375",
    "answer_text": "$$\n\\begin{array}{r | r}\n 3 & 3 375  ewline\n \\hline 3 & 1 125  ewline\n \\hline 3 & 375  ewline\n \\hline 5 & 125  ewline\n \\hline 5 & 25  ewline\n \\hline 5 & 5  ewline\n \\hline & 1\n\\end{array}\n$$\n\n$$\n3 375=3^3 \\times 5^3\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
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
  "subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors",
  "subtopic_title": "Prime numbers and factors",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors-po01",
        "source_performance_objective_index": 1,
        "text": "Identify prime numbers"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "prime-numbers-and-factors-ao-identify-prime-numbers",
          "text": "Identify prime numbers."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors-po02",
        "source_performance_objective_index": 2,
        "text": "Find the factors of a given whole number"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "prime-numbers-and-factors-ao-find-factors",
          "text": "Find the factors of a given whole number."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors-po03",
        "source_performance_objective_index": 3,
        "text": "Express a number as a product of its prime factors"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "prime-numbers-and-factors-ao-express-prime-factors",
          "text": "Express a number as a product of its prime factors."
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
    "record_id": "ch02-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Factors"
    },
    "content_text": "A factor is any of the two or more whole numbers we multiply to get a product. For example: $6 \\times 2 = 12$. The numbers 6 and 2 are factors of 12.\n\nA factor is also described as a whole number that divides into a larger number without a remainder. For example: $\\frac{12}{6} = 2$. The number 6 divides perfectly into 12. Therefore, the number 6 is a factor of 12.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b002",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Factors"
    },
    "content_text": "factor\n\nA factor is a whole number that divides into a larger number without a remainder.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b003",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Worked example 2.1: Factors"
    },
    "content_text": "",
    "prompt_text": "Find all the factors of the number 60.",
    "answer_text": "Step 1: Any number larger than 1 has the number itself and 1 as factors.\n\n$$\n1 \\times 60=60\n$$\n\nStep 2: Start with 2 and see if it divides into 60 without a remainder.\n\n$$\n\\frac{60}{2} = 30\n$$\n\n$$\n2 \\times 30=60\n$$\n\nStep 3: Try each consecutive number to see if it divides into 60 without a remainder. Stop when you get to a number that you already have as an answer.\n\n$$\n\\begin{array}{2}\n \\frac{60}{3} = 20 \\hspace{10mm} &3 \\times 20 = 60 \\\\\n \\frac{60}{4} = 15 &4 \\times 15 = 60 \\\\\n \\frac{60}{5} = 12 &5 \\times 12 = 60 \\\\\n \\frac{60}{6} = 10 &6 \\times 10 = 60 \\\\\n \\end{array}\n$$\n\nThe numbers 7, 8 and 9 do not divide into 60 without a remainder, so they are not factors of 60.\n\nYou already have the number 10, as 60 divided by 6 is 10, so you can stop there.\n\n$$\n\\frac{60}{10} = 6\n$$\n\nStep 4: List all the factors from the smallest number to the largest number.\n\nThe factors of 60 are: 1; 2; 3; 4; 5; 6; 10; 12; 15; 20; 30; 60",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b004",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.1: Find factors"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.1: Find factors\n\nFind all the factors of the following numbers:",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b004-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.1: Find factors"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.1: Find factors\n\n1. 54",
    "answer_text": "$$\n\\begin{array}{2}\n\\text{1 and itself} \\hspace{10mm}&1 \\times 54=54 \\\\\n\\frac{54}{2} = 27 &2 \\times 27 = 54 \\\\\n\\frac{54}{3} = 18 &3 \\times 18 = 54 \\\\\n\\frac{54}{6} = 9 & 6 \\times 9 = 54 \\\\\n\\frac{54}{9} = 6 & \\text{already divided}\n\\end{array}\n$$\n\nThe factors of 54 are: 1; 2; 3; 6; 9; 18; 27; 54",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b004-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.1: Find factors"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.1: Find factors\n\n2. 39",
    "answer_text": "$$\n\\begin{array}{2}\n\\text{1 and itself} \\hspace{10mm}&1 \\times 39=39 \\\\\n\\frac{39}{3} = 13 & 3 \\times 13 = 39 \\\\\n\\frac{39}{13} = 3 & \\text{already divided}\n\\end{array}\n$$\n\nThe factors of 39 are: 1; 3; 13; 39",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b004-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.1: Find factors"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.1: Find factors\n\n3. 45",
    "answer_text": "$$\n\\begin{array}{2}\n\\text{1 and itself} \\hspace{10mm}&1 \\times 45=45 \\\\\n\\frac{45}{3} = 15 & 3 \\times 15 = 45 \\\\\n\\frac{45}{5} = 9 & 5 \\times 9 = 45 \\\\\n\\frac{45}{9} = 5 & \\text{already divided}\n\\end{array}\n$$\n\nThe factors of 45 are: 1; 3; 5; 9; 15; 45",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b005",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Prime factors"
    },
    "content_text": "The number 3 has only two factors: 1 and 3. Similarly, the number 11 has only two factors: 1 and 11. These are examples of prime numbers.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b006",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Prime factors"
    },
    "content_text": "prime number\n\nA prime number is a number that has only two factors: 1 and the number itself.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b007",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Prime factors"
    },
    "content_text": "The prime numbers between 1 and 100 are highlighted in the grid below.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-02-001.png)\n\nprime factors\nThese are the factors of a number that are also prime numbers. Any non-prime number can be broken down into prime factors. We can then write the number as a product of its prime factors.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b008",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Prime factors"
    },
    "content_text": "prime factor\n\nA prime factor is a factor that is also a prime number.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b009",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Worked example 2.2: Prime factors"
    },
    "content_text": "",
    "prompt_text": "Find the prime factors of 80.",
    "answer_text": "Step 1: Find the smallest prime number that is a factor of 80. Express 80 as a product of two factors.\n\n$$\n\\frac{80}{2}=40\n$$\n\n$$\n80=2 \\times 40\n$$\n\nStep 2: Find the smallest prime number that is a factor of the non-prime factor from Step 1. Express 80 as a product of three factors.\n\n$$\n\\frac{40}{2}=20\n$$\n\n$$\n80=2 \\times 2 \\times 20\n$$\n\nStep 3: Repeat Step 2 until 80 is expressed as a product of only prime numbers.\n\n$$\n\\frac{20}{2}=10\n$$\n\n$$\n80=2 \\times 2 \\times 2 \\times 10\n$$\n\n$$\n\\frac{10}{2}=5\n$$\n\n$$\n80=2 \\times 2 \\times 2 \\times 5\n$$\n\nRemember that 1 is not a prime number.",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b010",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.2: Express numbers as products of prime factors"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.2: Express numbers as products of prime factors\n\nExpress the following numbers as products of prime factors:",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b010-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.2: Express numbers as products of prime factors"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.2: Express numbers as products of prime factors\n\nExpress the following numbers as products of prime factors:\n\n1. 30",
    "answer_text": "$$\n\\begin{array}{2} & \\frac{30}{2}=15 &\\hspace{10 mm}30=2 \\times 15  ewline & \\frac{15}{3}=5 &\\hspace{10mm} 30=2 \\times 3 \\times 5 \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b010-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.2: Express numbers as products of prime factors"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.2: Express numbers as products of prime factors\n\nExpress the following numbers as products of prime factors:\n\n2. 140",
    "answer_text": "$$\n\\begin{array}{2} & \\frac{140}{2}=70 &\\hspace{10 mm}140=2 \\times 70  ewline & \\frac{70}{2}=35 &\\hspace{10mm} 140=2 \\times 2 \\times 35  ewline & \\frac{35}{5}=7 &\\hspace{10mm} 140=2 \\times 2 \\times 5 \\times 7  ewline \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b010-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.2: Express numbers as products of prime factors"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.2: Express numbers as products of prime factors\n\nExpress the following numbers as products of prime factors:\n\n3. 195",
    "answer_text": "$$\n\\begin{array}{2} & \\frac{195}{3}=65 &\\hspace{10 mm}195=3 \\times 65  ewline & \\frac{65}{5}=13 &\\hspace{10mm} 195=3 \\times 5 \\times 13  ewline \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b010-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.2: Express numbers as products of prime factors"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.2: Express numbers as products of prime factors\n\nExpress the following numbers as products of prime factors:\n\n4. 252",
    "answer_text": "$$\n\\begin{array}{2} & \\frac{252}{2}=126 &\\hspace{10 mm}252=2 \\times 126  ewline & \\frac{126}{2}=63 &\\hspace{10mm} 252=2 \\times 2 \\times 63  ewline & \\frac{63}{3}=21 &\\hspace{10mm} 252=2 \\times 2 \\times 3 \\times 21  ewline & \\frac{21}{3}=7 &\\hspace{10mm} 252=2 \\times 2 \\times 3 \\times 3 \\times 7  ewline \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b010-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.2: Express numbers as products of prime factors"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.2: Express numbers as products of prime factors\n\nExpress the following numbers as products of prime factors:\n\n5. 297",
    "answer_text": "$$\n\\begin{array}{2} & \\frac{297}{3}=99 &\\hspace{10 mm}297=3 \\times 99  ewline & \\frac{99}{3}=33 &\\hspace{10mm} 297=3 \\times 3 \\times 33  ewline & \\frac{33}{3}=11 &\\hspace{10mm} 297=3 \\times 3 \\times 3 \\times 11  ewline \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b011",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Index form"
    },
    "content_text": "Finding and writing down the prime factors of large numbers can become confusing. To make the process easier, we may use continued division and write the prime factors in index form. The index or power of a number tells us how many times we multiply the number by itself. For example, $2^4$ means $2 \\times 2 \\times 2 \\times 2$. In this case, 4 is the power or index of 2.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b012",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Index form"
    },
    "content_text": "index form\nIndex form tells you how many times to use the same number in a multiplication by writing a superscript next to the number, for example $3^2$ means multiply 3 by 3.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b013",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Index form"
    },
    "content_text": "An index of 1 means a number is not multiplied by itself. Therefore, $2$ and $2^1$ have the same meaning.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b014",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Worked example 2.3: Prime factors in index form"
    },
    "content_text": "",
    "prompt_text": "Find the prime factors of 180 and write them in index form.",
    "answer_text": "Step 1: Divide the smallest prime factor of 180 until it cannot divide any further.\n\n$$\n\\begin{array}{r | r}\n 2 & 180  ewline\n \\hline\n 2 & 90  ewline\n \\hline\n & 45\n\\end{array}\n$$\n\nStep 2: Move to the next prime factor of 180. Keep on dividing until it cannot divide any further.\n\n$$\n\\begin{array}{r | r}\n 2 & 180  ewline\n \\hline\n 2 & 90  ewline\n \\hline\n 3 & 45  ewline\n \\hline\n 3 & 15  ewline\n \\hline\n & 5\n\\end{array}\n$$\n\nStep 3: Repeat Step 2 until you get 1 as an answer.\n\n$$\n\\begin{array}{r | r}\n 2 & 180  ewline\n \\hline\n 2 & 90  ewline\n \\hline\n 3 & 45  ewline\n \\hline\n 3 & 15  ewline\n \\hline\n 5 & 5  ewline\n \\hline\n & 1\n\\end{array}\n$$\n\nStep 4: Write down all the prime factors of 180. Use superscripts to write the index of each prime factor, that is, how many times the prime factor divided.\n\n$$\n180 = 2^2 \\times 3^2 \\times 5\n$$\n\nThe index of each prime factor shows us how many times we must multiply each prime factor to get 180 again:\n\n$$\n180 = 2^2 \\times 3^2 \\times 5 = 2 \\times 2 \\times 3 \\times 3 \\times 5\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b015",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.3: Express numbers as products of prime factors in index form"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.3: Express numbers as products of prime factors in index form\n\nExpress the following numbers as prime factors in index form:",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b015-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.3: Express numbers as products of prime factors in index form"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.3: Express numbers as products of prime factors in index form\n\nExpress the following numbers as prime factors in index form:\n\n1. 60",
    "answer_text": "$$\n\\begin{array}{r | r}\n 2 & 60  ewline\n \\hline 2 & 30  ewline\n \\hline 3 & 15  ewline\n \\hline 5 & 5  ewline\n \\hline & 1\n\\end{array}\n$$\n\n$$\n60=2^2 \\times 3 \\times 5\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b015-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.3: Express numbers as products of prime factors in index form"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.3: Express numbers as products of prime factors in index form\n\nExpress the following numbers as prime factors in index form:\n\n2. 144",
    "answer_text": "$$\n\\begin{array}{r | r}\n 2 & 144  ewline\n \\hline 2 & 72  ewline\n \\hline 2 & 36  ewline\n \\hline 2 & 18  ewline\n \\hline 3 & 9  ewline\n \\hline 3 & 3  ewline\n \\hline & 1\n\\end{array}\n$$\n\n$$\n144=2^4 \\times 3^2\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b015-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.3: Express numbers as products of prime factors in index form"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.3: Express numbers as products of prime factors in index form\n\nExpress the following numbers as prime factors in index form:\n\n3. 198",
    "answer_text": "$$\n\\begin{array}{r | r}\n 2 & 198  ewline\n \\hline 3 & 99  ewline\n \\hline 3 & 33  ewline\n \\hline 11 & 11  ewline\n \\hline & 1\n\\end{array}\n$$\n\n$$\n198=2\\times 3^2 \\times 11\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b015-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.3: Express numbers as products of prime factors in index form"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.3: Express numbers as products of prime factors in index form\n\nExpress the following numbers as prime factors in index form:\n\n4. 300",
    "answer_text": "$$\n\\begin{array}{r | r}\n 2 & 300  ewline\n \\hline 2 & 150  ewline\n \\hline 3 & 75  ewline\n \\hline 5 & 25  ewline\n \\hline 5 & 5  ewline\n \\hline & 1\n\\end{array}\n$$\n\n$$\n300=2^2 \\times 3\\times 5^2\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
  },
  {
    "record_id": "ch02-b015-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 2: Highest common factor and lowest common multiple",
      "h2": "2.1 Highest common factor",
      "h3": "Exercise 2.3: Express numbers as products of prime factors in index form"
    },
    "content_text": "",
    "prompt_text": "### Exercise 2.3: Express numbers as products of prime factors in index form\n\nExpress the following numbers as prime factors in index form:\n\n5. 3 375",
    "answer_text": "$$\n\\begin{array}{r | r}\n 3 & 3 375  ewline\n \\hline 3 & 1 125  ewline\n \\hline 3 & 375  ewline\n \\hline 5 & 125  ewline\n \\hline 5 & 25  ewline\n \\hline 5 & 5  ewline\n \\hline & 1\n\\end{array}\n$$\n\n$$\n3 375=3^3 \\times 5^3\n$$",
    "primary_subtopic_id": "jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors"
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
