# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-3",
  "topic_key": "jss1-math-simplification-of-algebraic-expressions",
  "topic": "Simplification of Algebraic Expressions",
  "subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning",
  "subtopic_title": "Quantitative reasoning",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning-po01",
        "source_performance_objective_index": 1,
        "text": "Solve quantitative aptitude problems on the use of brackets"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "simplification-of-algebraic-expressions-quantitative-reasoning-ao-solve-problems",
          "text": "Solve quantitative aptitude problems on the use of brackets."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch10-b046",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Using area to show the distributive law in practice"
    },
    "content_text": "We can use areas to show the distributive law in practice. For example, look at the two rectangles shown below. There are two ways in which we can write the total area of the two rectangles.\n\n**Method 1**: Calculate the area of each rectangle separately, and then add the areas.\n\n- Area of smaller rectangle: $A = 3 \\times 2$ square units\n- Area of larger rectangle: $A = 3 \\times 4$ square units\n- Total area of the two rectangles:\n\n$$\n\\begin{align}\nA&=(3 \\times 2) + (3 \\times 4) \\\\\n&=6+12 \\\\\n&=18 \\text{ square units}\n\\end{align}\n$$\n\n**Method 2**: Calculate the total area of the combined rectangle.\n\n- Width of total rectangle: $3$\n- Length of total rectangle: $2 + 4$\n- Total area of the two rectangles:\n\n$$\n\\begin{align}\nA&=3 \\times (2 + 4) \\\\\n&=3 \\times 6 \\\\\n&=18 \\text{ square units}\n\\end{align}\n$$\n\nFrom this practical example we can see that:\n\n$$\n3\\times(2+4) = (3 \\times 2) + (3 \\times 4)\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b047",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.10: Use algebraic expressions to show the distributive law in practice"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.10: Use algebraic expressions to show the distributive law in practice",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b047-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.10: Use algebraic expressions to show the distributive law in practice"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.10: Use algebraic expressions to show the distributive law in practice\n\n1. Write down two different expressions for the total area of the two rectangles shown below. Draw sketches to show your working, and use the variables in terms of $a, b$ and $c$ in your expressions.",
    "answer_text": "$$\nA = ab + ac\n$$\n\nor\n\n$$\nA = a(b+c)\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b047-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.10: Use algebraic expressions to show the distributive law in practice"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.10: Use algebraic expressions to show the distributive law in practice\n\n2. Write down the total area of the rectangles given below in two different ways.",
    "answer_text": "$$\nA = 4(8c + y)\n$$\n\nor\n\n$$\nA= 32c + 4y\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b048",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Using algebraic expressions to solve everyday problems"
    },
    "content_text": "Algebraic expressions can be very useful when you need to solve everyday problems. It allows us to use variables as representations of numbers where the value may vary.\n\nSuppose you get ₦500 pocket money every month and you want to keep track of what is happening to your money. You spend your pocket money on sweets, transport and data for your mobile. You can set up an expression to represent this:\n\n$$\n\\text{money available}=₦\\,500-(s+t+d)=₦\\,500-s-t-d\n$$\n\nAt any time during the month, you can put the amounts of money you spent on each item into your expression. This will give you the amount of money you have left for the rest of the month.\n\nAlgebraic expressions can also be used to solve mathematical problems. Here are some tips that you may find useful:\n\n1. Three consecutive numbers can be represented as $x,\\space x+1, \\space x+2$.\n2. More than, for example 5 more than $x$: $x+5$.\n3. Less than, for example 5 less than $x$: $x-5$.\n4. Double or twice, for example double $y$ or twice $y$: $2y$.\n5. Half, for example half of $y$: $y \\div 2$ or $\\frac{1}{2}y$.\n6. Seconds in $m$ minutes and $h$ hours: $60m$ and $3,600h$.\n7. Kobo in $n$ naira: $100n$.\n8. Total cost, for example total cost of $p\\text{ pens}$ and $r\\text{ rulers}$: $p+r$.\n9. Area of a rectangle: $A=l \\times b$.\n10. Perimeter of a rectangle: $P=2l+2b$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b049",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.11: Use algebraic expressions for practical problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.11: Use algebraic expressions for practical problems",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b049-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.11: Use algebraic expressions for practical problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.11: Use algebraic expressions for practical problems\n\n1. A father is $x$ years old. His daughter is currently half his age. How old will his daughter be in 10 years' time?",
    "answer_text": "$$\n\\tfrac{1}{2}x+10\n$$\n\nThe age of the daughter will be $\\frac{1}{2}x+10$, where $x$ is the current age of the father.",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b049-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.11: Use algebraic expressions for practical problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.11: Use algebraic expressions for practical problems\n\n2. A long-distance athlete covers an average distance of $x\\text{ metres}$ per minute. How far does she run in $y\\text{ hours}$?",
    "answer_text": "$$\nx\\times y \\times 60=60xy\\text{ metres}\n$$\n\nIn $y\\text{ hours}$, the athlete runs $60xy\\text{ metres}$.",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b049-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.11: Use algebraic expressions for practical problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.11: Use algebraic expressions for practical problems\n\n3. A shop owner sells maize at $₦\\,x$ per cup. She also sells rice per cup, at double the price of the maize. If she sold 50 cups of maize and 45 cups of rice, what was her income?",
    "answer_text": "The price of her rice is $₦\\,2x$ per cup.\n\n$$\n\\begin{align}\n&\\phantom{000}50\\times x+45\\times 2x \\\\\n&=50x+90x \\\\\n&=140x\n\\end{align}\n$$\n\nHer income is $₦\\,140x$, where $₦\\,x$ is the price of one cup of maize.",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b049-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.11: Use algebraic expressions for practical problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.11: Use algebraic expressions for practical problems\n\n4. A small sachet of milk costs $₦\\,x$ and a small sachet of noodles costs $₦\\,20$ more. Work out the cost of 4 sachets of milk and 8 sachets of noodles.",
    "answer_text": "A small sachet of noodles costs $₦\\,x+20$.\n\n$$\n\\begin{align}\n&\\phantom{000}4\\times x+8\\times (x+20) \\\\\n&=4x+8(x+20) \\\\\n&=4x+8x+160 \\\\\n&=12x+160\n\\end{align}\n$$\n\nThe cost is $₦\\,12x+160$, where $₦\\,x$ is the price of a small sachet of milk.",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b049-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.11: Use algebraic expressions for practical problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.11: Use algebraic expressions for practical problems\n\n5. The length of a rectangle is 3Â cm more than its breadth. Calculate the perimeter of the rectangle.",
    "answer_text": "$$\n\\begin{align}\nP&=2l+2b \\\\\n&=2(b+3)+2b \\\\\n&=2b+6+2b \\\\\n&=4b+6\n\\end{align}\n$$\n\nThe perimeter is $4b+6\\text{ cm}$, where $b \\text{ cm}$ is the breadth.",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b049-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.11: Use algebraic expressions for practical problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.11: Use algebraic expressions for practical problems\n\n6. The sum of three consecutive numbers is $y$. If the first of the three numbers is $a$, determine $y$.",
    "answer_text": "The numbers are $a$, $a+1$ and $a+2$.\n\n$$\n\\begin{align}\ny&=a+(a+1)+(a+2) \\\\\n&=a+a+1+a+2 \\\\\n&=a+a+a+1+2 \\\\\n&=3a+3\n\\end{align}\n$$\n\n$y=3a+3$, where $a$ is the first number.",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b049-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.11: Use algebraic expressions for practical problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.11: Use algebraic expressions for practical problems\n\n7. In a Mathematics test, Safiyah scored $p$ marks. Nkechi scored 7 marks more than Safiyah. Fadekemi scored 4 marks less than Nkechi. Work out the total mark of the three girls together.",
    "answer_text": "Safiyah: $p$  \nNkechi: $p+7$  \nFadekemi: $(p+7)-4$\n\n$$\n\\begin{align}\n&\\phantom{000}p+p+7+p+7-4 \\\\\n&=p+p+p+7+7-4 \\\\\n&=3p+10\n\\end{align}\n$$\n\nTheir total mark is $3p+10$, where $p$ is Safiyah's mark.",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b049-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.11: Use algebraic expressions for practical problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.11: Use algebraic expressions for practical problems\n\n8. Abodunrin has $₦\\,n$ and Ikenna has $₦\\,20$ more. Abodunrin spends 500 kobo and Ikenna spends 750 kobo. Calculate how many kobos they have left altogether.",
    "answer_text": "Abodunrin: $100n-500$  \nIkenna: $100(n+20)-750$\n\n$$\n\\begin{align}\n&\\phantom{000}100n-500+100(n+20)-750 \\\\\n&=100n-500+100n+2,000-750 \\\\\n&=100n+100n-500+2,000-750 \\\\\n&=200n+750\n\\end{align}\n$$\n\nThey have $200n+750$ kobo left, where $₦\\,n$ is the original amount of money Abodunrin had.",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b049-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.11: Use algebraic expressions for practical problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.11: Use algebraic expressions for practical problems\n\n9. A pencil costs $₦\\,x$. A ruler costs $₦\\,10$ less than a pencil. A pen costs $₦\\,5$ more than a ruler. The price of a small exercise book is twice the price of a ruler. Calculate the cost of 3 pencils, 2 rulers and 4 exercise books.",
    "answer_text": "Pencil: $x$  \nRuler: $x-10$  \nPen: $(x-10)+5$  \nExercise book: $2\\times (x-10)=2x-20$\n\n$$\n\\begin{align}\n&\\phantom{000}3x+2(x-10)+4(2x-20) \\\\\n&=3x+2x-20+8x-80 \\\\\n&=3x+2x+8x-20-80 \\\\\n&=13x-100\n\\end{align}\n$$\n\nThe cost is $₦\\,13x-100$, where $₦\\,x$ is the price of a pencil.",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b049-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.11: Use algebraic expressions for practical problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.11: Use algebraic expressions for practical problems\n\n10. Rectangle 1 has a breadth of $2x\\text{ cm}$ and a length of $y\\text{ cm}$. Rectangle 2 has a breadth half as long as the breadth of Rectangle 1. The length of Rectangle 2 is $10\\text{ cm}$ longer than that of Rectangle 1. Calculate by how much the area of Rectangle 2 is larger than the area of Rectangle 1.",
    "answer_text": "Breadth of Rectangle 1: $2x$  \nLength of Rectangle 1: $y$  \nBreadth of Rectangle 2: $2x \\div 2=x$  \nLength of Rectangle 2: $y+10$\n\n$$\n\\begin{align}\nA_2-A_1&=x \\times (y+10)-2x\\times y \\\\\n&= x(y+10)-2xy\\\\\n&=xy+10x-2xy \\\\\n&=10x-2xy+xy \\\\\n&=10x-xy\n\\end{align}\n$$\n\nThe area of Rectangle 2 is $10x-xy\\text{ cm}$ larger than the area of Rectangle 1.",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b050",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Summary",
      "h3": null
    },
    "content_text": "- An algebraic expression is a mathematical statement that contains a combination of numbers, symbols, variables and mathematical operators. It does not have an equals sign.\n- A term can be a single number (positive or negative), or a variable, or one or more numbers and variables that are being multiplied together. Terms are separated by + or âˆ’ signs.\n- The coefficient is the number (factor) being multiplied by the variable. A coefficient can have a positive or negative value.\n- A constant is a term without a variable. A constant can have a positive or negative value.\n- To simplify an expression is to give it in its simplest form. We do this by collecting (combining) like terms using addition or subtraction.\n- Like terms contain the same variable or variables.\n- Unlike terms contain different variables.\n- When we remove a bracket with a negative sign in front of it, we change the signs of all the terms inside the bracket.\n- To expand an algebraic expression is to multiply what is outside the brackets (the coefficient of the bracket) by each of the terms that is inside the bracket.\n- The distributive law states that the multiplying factor (the coefficient) can be distributed across each of the terms inside a bracket, so &amp;#240;&amp;#157;&amp;#145;&amp;#142;x(&amp;#240;&amp;#157;&amp;#145;&amp;#143;+&amp;#240;&amp;#157;&amp;#145;&amp;#144;)=&amp;#240;&amp;#157;&amp;#145;&amp;#142;x&amp;#240;&amp;#157;&amp;#145;&amp;#143;+&amp;#240;&amp;#157;&amp;#145;&amp;#142;x&amp;#240;&amp;#157;&amp;#145;&amp;#144;.\n- When we simplify algebraic expressions, we must use the correct order of operations: Brackets, Of, Divide, Multiply, Add, Subtract.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-collection-and-simplification-of-like-and-unlike-terms-in-algebraic-expressions"
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
  "theme_key": "jss1-theme-3",
  "topic_key": "jss1-math-simplification-of-algebraic-expressions",
  "topic": "Simplification of Algebraic Expressions",
  "subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning",
  "subtopic_title": "Quantitative reasoning",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning-po01",
        "source_performance_objective_index": 1,
        "text": "Solve quantitative aptitude problems on the use of brackets"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "simplification-of-algebraic-expressions-quantitative-reasoning-ao-solve-problems",
          "text": "Solve quantitative aptitude problems on the use of brackets."
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
    "record_id": "ch10-b046",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Using area to show the distributive law in practice"
    },
    "content_text": "We can use areas to show the distributive law in practice. For example, look at the two rectangles shown below. There are two ways in which we can write the total area of the two rectangles.\n\n**Method 1**: Calculate the area of each rectangle separately, and then add the areas.\n\n- Area of smaller rectangle: $A = 3 \\times 2$ square units\n- Area of larger rectangle: $A = 3 \\times 4$ square units\n- Total area of the two rectangles:\n\n$$\n\\begin{align}\nA&=(3 \\times 2) + (3 \\times 4) \\\\\n&=6+12 \\\\\n&=18 \\text{ square units}\n\\end{align}\n$$\n\n**Method 2**: Calculate the total area of the combined rectangle.\n\n- Width of total rectangle: $3$\n- Length of total rectangle: $2 + 4$\n- Total area of the two rectangles:\n\n$$\n\\begin{align}\nA&=3 \\times (2 + 4) \\\\\n&=3 \\times 6 \\\\\n&=18 \\text{ square units}\n\\end{align}\n$$\n\nFrom this practical example we can see that:\n\n$$\n3\\times(2+4) = (3 \\times 2) + (3 \\times 4)\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b047",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.10: Use algebraic expressions to show the distributive law in practice"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.10: Use algebraic expressions to show the distributive law in practice",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b047-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.10: Use algebraic expressions to show the distributive law in practice"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.10: Use algebraic expressions to show the distributive law in practice\n\n1. Write down two different expressions for the total area of the two rectangles shown below. Draw sketches to show your working, and use the variables in terms of $a, b$ and $c$ in your expressions.",
    "answer_text": "$$\nA = ab + ac\n$$\n\nor\n\n$$\nA = a(b+c)\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b047-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.10: Use algebraic expressions to show the distributive law in practice"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.10: Use algebraic expressions to show the distributive law in practice\n\n2. Write down the total area of the rectangles given below in two different ways.",
    "answer_text": "$$\nA = 4(8c + y)\n$$\n\nor\n\n$$\nA= 32c + 4y\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b048",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Using algebraic expressions to solve everyday problems"
    },
    "content_text": "Algebraic expressions can be very useful when you need to solve everyday problems. It allows us to use variables as representations of numbers where the value may vary.\n\nSuppose you get ₦500 pocket money every month and you want to keep track of what is happening to your money. You spend your pocket money on sweets, transport and data for your mobile. You can set up an expression to represent this:\n\n$$\n\\text{money available}=₦\\,500-(s+t+d)=₦\\,500-s-t-d\n$$\n\nAt any time during the month, you can put the amounts of money you spent on each item into your expression. This will give you the amount of money you have left for the rest of the month.\n\nAlgebraic expressions can also be used to solve mathematical problems. Here are some tips that you may find useful:\n\n1. Three consecutive numbers can be represented as $x,\\space x+1, \\space x+2$.\n2. More than, for example 5 more than $x$: $x+5$.\n3. Less than, for example 5 less than $x$: $x-5$.\n4. Double or twice, for example double $y$ or twice $y$: $2y$.\n5. Half, for example half of $y$: $y \\div 2$ or $\\frac{1}{2}y$.\n6. Seconds in $m$ minutes and $h$ hours: $60m$ and $3,600h$.\n7. Kobo in $n$ naira: $100n$.\n8. Total cost, for example total cost of $p\\text{ pens}$ and $r\\text{ rulers}$: $p+r$.\n9. Area of a rectangle: $A=l \\times b$.\n10. Perimeter of a rectangle: $P=2l+2b$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b049",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.11: Use algebraic expressions for practical problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.11: Use algebraic expressions for practical problems",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b049-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.11: Use algebraic expressions for practical problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.11: Use algebraic expressions for practical problems\n\n1. A father is $x$ years old. His daughter is currently half his age. How old will his daughter be in 10 years' time?",
    "answer_text": "$$\n\\tfrac{1}{2}x+10\n$$\n\nThe age of the daughter will be $\\frac{1}{2}x+10$, where $x$ is the current age of the father.",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b049-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.11: Use algebraic expressions for practical problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.11: Use algebraic expressions for practical problems\n\n2. A long-distance athlete covers an average distance of $x\\text{ metres}$ per minute. How far does she run in $y\\text{ hours}$?",
    "answer_text": "$$\nx\\times y \\times 60=60xy\\text{ metres}\n$$\n\nIn $y\\text{ hours}$, the athlete runs $60xy\\text{ metres}$.",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b049-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.11: Use algebraic expressions for practical problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.11: Use algebraic expressions for practical problems\n\n3. A shop owner sells maize at $₦\\,x$ per cup. She also sells rice per cup, at double the price of the maize. If she sold 50 cups of maize and 45 cups of rice, what was her income?",
    "answer_text": "The price of her rice is $₦\\,2x$ per cup.\n\n$$\n\\begin{align}\n&\\phantom{000}50\\times x+45\\times 2x \\\\\n&=50x+90x \\\\\n&=140x\n\\end{align}\n$$\n\nHer income is $₦\\,140x$, where $₦\\,x$ is the price of one cup of maize.",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b049-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.11: Use algebraic expressions for practical problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.11: Use algebraic expressions for practical problems\n\n4. A small sachet of milk costs $₦\\,x$ and a small sachet of noodles costs $₦\\,20$ more. Work out the cost of 4 sachets of milk and 8 sachets of noodles.",
    "answer_text": "A small sachet of noodles costs $₦\\,x+20$.\n\n$$\n\\begin{align}\n&\\phantom{000}4\\times x+8\\times (x+20) \\\\\n&=4x+8(x+20) \\\\\n&=4x+8x+160 \\\\\n&=12x+160\n\\end{align}\n$$\n\nThe cost is $₦\\,12x+160$, where $₦\\,x$ is the price of a small sachet of milk.",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b049-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.11: Use algebraic expressions for practical problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.11: Use algebraic expressions for practical problems\n\n5. The length of a rectangle is 3Â cm more than its breadth. Calculate the perimeter of the rectangle.",
    "answer_text": "$$\n\\begin{align}\nP&=2l+2b \\\\\n&=2(b+3)+2b \\\\\n&=2b+6+2b \\\\\n&=4b+6\n\\end{align}\n$$\n\nThe perimeter is $4b+6\\text{ cm}$, where $b \\text{ cm}$ is the breadth.",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b049-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.11: Use algebraic expressions for practical problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.11: Use algebraic expressions for practical problems\n\n6. The sum of three consecutive numbers is $y$. If the first of the three numbers is $a$, determine $y$.",
    "answer_text": "The numbers are $a$, $a+1$ and $a+2$.\n\n$$\n\\begin{align}\ny&=a+(a+1)+(a+2) \\\\\n&=a+a+1+a+2 \\\\\n&=a+a+a+1+2 \\\\\n&=3a+3\n\\end{align}\n$$\n\n$y=3a+3$, where $a$ is the first number.",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b049-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.11: Use algebraic expressions for practical problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.11: Use algebraic expressions for practical problems\n\n7. In a Mathematics test, Safiyah scored $p$ marks. Nkechi scored 7 marks more than Safiyah. Fadekemi scored 4 marks less than Nkechi. Work out the total mark of the three girls together.",
    "answer_text": "Safiyah: $p$  \nNkechi: $p+7$  \nFadekemi: $(p+7)-4$\n\n$$\n\\begin{align}\n&\\phantom{000}p+p+7+p+7-4 \\\\\n&=p+p+p+7+7-4 \\\\\n&=3p+10\n\\end{align}\n$$\n\nTheir total mark is $3p+10$, where $p$ is Safiyah's mark.",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b049-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.11: Use algebraic expressions for practical problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.11: Use algebraic expressions for practical problems\n\n8. Abodunrin has $₦\\,n$ and Ikenna has $₦\\,20$ more. Abodunrin spends 500 kobo and Ikenna spends 750 kobo. Calculate how many kobos they have left altogether.",
    "answer_text": "Abodunrin: $100n-500$  \nIkenna: $100(n+20)-750$\n\n$$\n\\begin{align}\n&\\phantom{000}100n-500+100(n+20)-750 \\\\\n&=100n-500+100n+2,000-750 \\\\\n&=100n+100n-500+2,000-750 \\\\\n&=200n+750\n\\end{align}\n$$\n\nThey have $200n+750$ kobo left, where $₦\\,n$ is the original amount of money Abodunrin had.",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b049-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.11: Use algebraic expressions for practical problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.11: Use algebraic expressions for practical problems\n\n9. A pencil costs $₦\\,x$. A ruler costs $₦\\,10$ less than a pencil. A pen costs $₦\\,5$ more than a ruler. The price of a small exercise book is twice the price of a ruler. Calculate the cost of 3 pencils, 2 rulers and 4 exercise books.",
    "answer_text": "Pencil: $x$  \nRuler: $x-10$  \nPen: $(x-10)+5$  \nExercise book: $2\\times (x-10)=2x-20$\n\n$$\n\\begin{align}\n&\\phantom{000}3x+2(x-10)+4(2x-20) \\\\\n&=3x+2x-20+8x-80 \\\\\n&=3x+2x+8x-20-80 \\\\\n&=13x-100\n\\end{align}\n$$\n\nThe cost is $₦\\,13x-100$, where $₦\\,x$ is the price of a pencil.",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b049-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Practical applications",
      "h3": "Exercise 10.11: Use algebraic expressions for practical problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.11: Use algebraic expressions for practical problems\n\n10. Rectangle 1 has a breadth of $2x\\text{ cm}$ and a length of $y\\text{ cm}$. Rectangle 2 has a breadth half as long as the breadth of Rectangle 1. The length of Rectangle 2 is $10\\text{ cm}$ longer than that of Rectangle 1. Calculate by how much the area of Rectangle 2 is larger than the area of Rectangle 1.",
    "answer_text": "Breadth of Rectangle 1: $2x$  \nLength of Rectangle 1: $y$  \nBreadth of Rectangle 2: $2x \\div 2=x$  \nLength of Rectangle 2: $y+10$\n\n$$\n\\begin{align}\nA_2-A_1&=x \\times (y+10)-2x\\times y \\\\\n&= x(y+10)-2xy\\\\\n&=xy+10x-2xy \\\\\n&=10x-2xy+xy \\\\\n&=10x-xy\n\\end{align}\n$$\n\nThe area of Rectangle 2 is $10x-xy\\text{ cm}$ larger than the area of Rectangle 1.",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning"
  },
  {
    "record_id": "ch10-b050",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.6 Summary",
      "h3": null
    },
    "content_text": "- An algebraic expression is a mathematical statement that contains a combination of numbers, symbols, variables and mathematical operators. It does not have an equals sign.\n- A term can be a single number (positive or negative), or a variable, or one or more numbers and variables that are being multiplied together. Terms are separated by + or âˆ’ signs.\n- The coefficient is the number (factor) being multiplied by the variable. A coefficient can have a positive or negative value.\n- A constant is a term without a variable. A constant can have a positive or negative value.\n- To simplify an expression is to give it in its simplest form. We do this by collecting (combining) like terms using addition or subtraction.\n- Like terms contain the same variable or variables.\n- Unlike terms contain different variables.\n- When we remove a bracket with a negative sign in front of it, we change the signs of all the terms inside the bracket.\n- To expand an algebraic expression is to multiply what is outside the brackets (the coefficient of the bracket) by each of the terms that is inside the bracket.\n- The distributive law states that the multiplying factor (the coefficient) can be distributed across each of the terms inside a bracket, so &amp;#240;&amp;#157;&amp;#145;&amp;#142;x(&amp;#240;&amp;#157;&amp;#145;&amp;#143;+&amp;#240;&amp;#157;&amp;#145;&amp;#144;)=&amp;#240;&amp;#157;&amp;#145;&amp;#142;x&amp;#240;&amp;#157;&amp;#145;&amp;#143;+&amp;#240;&amp;#157;&amp;#145;&amp;#142;x&amp;#240;&amp;#157;&amp;#145;&amp;#144;.\n- When we simplify algebraic expressions, we must use the correct order of operations: Brackets, Of, Divide, Multiply, Add, Subtract.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-collection-and-simplification-of-like-and-unlike-terms-in-algebraic-expressions"
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
