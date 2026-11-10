# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-3",
  "topic_key": "jss1-math-simple-equations",
  "topic": "Simple Equations",
  "subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa",
  "subtopic_title": "Translation of word problems into equations and vice-versa",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa-po01",
        "source_performance_objective_index": 1,
        "text": "Translate word sentences into mathematical equations"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "translation-of-word-problems-into-equations-ao-translate-word-sentences",
          "text": "Translate word sentences into mathematical equations."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa-po02",
        "source_performance_objective_index": 2,
        "text": "Use mathematical equations to represent word sentences"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "translation-of-word-problems-into-equations-ao-use-equations-to-represent",
          "text": "Use mathematical equations to represent word sentences."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch11-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": null,
      "h3": null
    },
    "content_text": "You have learnt that an algebraic *expression* is a mathematical phrase or statement. Algebraic expressions do not have equals signs. In this chapter we will be dealing with algebraic *equations*. Algebraic equations are mathematical sentences with equals signs. You will learn how to formulate and solve algebraic equations.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b002",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": null
    },
    "content_text": "An **algebraic equation** is a mathematical sentence that contains a combination of numbers, symbols, variables and mathematical operators. It always has an equals sign.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b003",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": null
    },
    "content_text": "**algebraic equation** An algebraic equation is a mathematical sentence that contains a combination of numbers, symbols, variables and mathematical operators. It always has an equals sign.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b004",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "The difference between expressions and equations"
    },
    "content_text": "It is important that you understand the difference between algebraic expressions and algebraic equations. The table below lists the main differences.\n\n- An expression is a phrase. An equation is a sentence.\n- We simplify an expression. We solve an equation.\n- An expression does not have an equals sign. An equation has an equals sign.\n- An expression gives the relationship between variables. An equation shows that two expressions are equal.\n- The variables in an expression can have a whole range of values. The variables in an equation only has specific values.\n- Example expression: two more than a number, written as $x+2$.\n- Example equation: two more than a number is five, written as $x+2=5$.\n\nLet's look at an example from Chapter 10 to explain this further.\n\nSuppose a shop owner sells maize at $₦\\,x$ per cup. She also sells rice per cup, at double the price of the maize. On a specific day, she sold 50 cups of maize and 45 cups of rice.\n\n- We can write an *expression* for her income for the day: $50\\times x+45\\times 2x$.\n- We can simplify the expression to $50x+90x$, and simplify further to $140x$.\n- Her income for the day is therefore $₦\\,140x$.\n- Her income depends on the cost of a cup of maize, which can be any positive number.\n- If we know that her income for the day was $₦\\,7,700$, we can write an *equation*: $50\\times x+45\\times 2x = 7,700$.\n- We can simplify the equation to $140x=7,700$.\n- The only value that makes this sentence true is $55$.\n- Now we know that the price of a cup of maize is $₦\\,55$ and the price of a cup of rice is $2\\times55=₦\\,110$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b005",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Translate word sentences into algebraic equations"
    },
    "content_text": "In Section 9.3 of Chapter 9 and Section 10.6 of Chapter 10 you were given some examples of ways to write word phrases as mathematical statements. Revise those sections before you go on.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b006",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Worked example 11.1: Translating simple word sentences into algebraic equations"
    },
    "content_text": "",
    "prompt_text": "If a number is multiplied by 4, the answer is 6 more than the number. Write an equation to represent this.",
    "answer_text": "Step 1: Identify the unknown and make it $x$.\n\nIn this case, the unknown is the number. So, we say the number is $x$.\n\nStep 2: Write an expression or value for one part of the equation.\n\nOne of the phrases states that the number is multiplied by 4. We write this as $4x$.\n\nStep 3: Write an expression or value for the other part of the equation.\n\nAnother phrase refers to 6 more than the number. We write this as $x+6$.\n\nStep 4: Remember that an equation has an equals sign. Decide how the two expressions are equal to each other.\n\nThe words say the answer of the multiplication by 4 gives the addition of 6. Therefore:\n\n$$\n4x=x+6\n$$\n\nIf we solve the equation above, we get $x=2$. You will learn how to solve equations in the next section.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b007",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Worked example 11.2: Translating more complex word sentences into algebraic equations"
    },
    "content_text": "",
    "prompt_text": "A mother is twice as old as her daughter. In two years' time, their combined ages will be 52 years. Write an equation to represent this.",
    "answer_text": "Step 1: Identify the unknowns.\n\nThere are two unknowns:\n\n- The mother's age\n- The daughter's age\n\nStep 2: Make the one unknown $x$. Write an expression for the other unknown in terms of $x$.\n\n- Make the daughter's age $x$.\n- The mother's age is twice that. Therefore, the mother's age is $2x$.\n\nWe could also say the mother's age is $x$ and the daughter's age is $\\frac{1}{2}x$. However, it is often easier to solve equations with whole numbers as coefficients than equations with fractions as coefficients.\n\nStep 3: Write an expression or value for one part of the equation.\n\nOne phrase refers to their ages in two years' time:\n\n- The daughter will be $x+2$ years old.\n- The mother will be $2x+2$ years old.\n\nStep 4: Write an expression or value for the other part of the equation.\n\nAnother phrase says their combined ages will be 52.\n\nStep 5: Remember that an equation has an equals sign. Decide how the two expressions are equal to each other.\n\nTheir combined ages in two years' time is equal to 52. If we combine their ages, this means we add the ages. Therefore:\n\n$$\n(x+2)+(2x+2)=52\n$$\n\nIf we solve the equation above, we get $x=16$. This means the daughter is 16 years old and the mother is 32 years old. You will learn how to solve equations in the next section.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b008",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.1: Translate word sentences into equations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.1: Translate word sentences into equations\n\nWrite an algebraic equation for each of the following situations.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b008-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.1: Translate word sentences into equations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.1: Translate word sentences into equations\n\nWrite an algebraic equation for each of the following situations.\n\n1. If we add 23 to a number, the answer is 42.",
    "answer_text": "$$\nx+23=42\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b008-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.1: Translate word sentences into equations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.1: Translate word sentences into equations\n\nWrite an algebraic equation for each of the following situations.\n\n2. The difference between 75 and a number is 20.",
    "answer_text": "$$\n75-x=20\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b008-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.1: Translate word sentences into equations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.1: Translate word sentences into equations\n\nWrite an algebraic equation for each of the following situations.\n\n3. A pen costs twice as much as a ruler. The cost of 5 pens and 7 rulers is $₦\\,102$.",
    "answer_text": "$$\n5(2x)+7x=102\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b008-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.1: Translate word sentences into equations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.1: Translate word sentences into equations\n\nWrite an algebraic equation for each of the following situations.\n\n4. If we add 9 to half of a number, the answer is twice the number.",
    "answer_text": "$$\n\\frac{1}{2}x+9=2x\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b008-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.1: Translate word sentences into equations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.1: Translate word sentences into equations\n\nWrite an algebraic equation for each of the following situations.\n\n5. The sum of three consecutive numbers is 24.",
    "answer_text": "$$\nx+(x+1)+(x+2)=24\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b008-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.1: Translate word sentences into equations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.1: Translate word sentences into equations\n\nWrite an algebraic equation for each of the following situations.\n\n6. The length of a rectangle with a perimeter of 40 cm is three times more than its breadth.",
    "answer_text": "$$\n2x+2(3x)=40\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b008-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.1: Translate word sentences into equations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.1: Translate word sentences into equations\n\nWrite an algebraic equation for each of the following situations.\n\n7. The combined area of two rectangles is 49 square units. The area of one rectangle is six times more than the area of the other rectangle.",
    "answer_text": "$$\nx+6x=49\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b008-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.1: Translate word sentences into equations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.1: Translate word sentences into equations\n\nWrite an algebraic equation for each of the following situations.\n\n8. If the sum of a number and 6 is divided by 10, the answer is 24.",
    "answer_text": "$$\n\\frac{x+6}{10}=24\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b008-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.1: Translate word sentences into equations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.1: Translate word sentences into equations\n\nWrite an algebraic equation for each of the following situations.\n\n9. Danjuma has $₦\\,500$. He spends a certain amount on snacks and exactly the same amount on data. He then spends twice the amount he spent on snacks to buy stationery. He has $₦\\,40$ left.",
    "answer_text": "$$\n500-x-x-2x=40\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b008-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.1: Translate word sentences into equations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.1: Translate word sentences into equations\n\nWrite an algebraic equation for each of the following situations.\n\n10. Ngozi goes to school. She walks for a few minutes and then runs for 180 seconds. Then she walks again for half the time she walked in the beginning. Her journey takes 15 minutes.",
    "answer_text": "If we work in seconds:\n\n$$\n2x+180+x=15\\times 60\n$$\n\nIf we work in minutes:\n\n$$\n2x+\\frac{180}{60}+x=15\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b009",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Translate algebraic equations into word sentences"
    },
    "content_text": "We can also translate algebraic equations into word sentences. You can make up a story if you want to, or you can just think of the variable as a number.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b010",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Worked example 11.3: Translating algebraic equations into word sentences"
    },
    "content_text": "",
    "prompt_text": "Translate the following equation into a word sentence:\n\n$$\n3+y=10-2y\n$$",
    "answer_text": "Step 1: Assume that the variable is a number.\n\nIn this case the variable is $y$. So we assume that $y$ is a number.\n\nStep 2: Interpret one part of the equation.\n\n$3+y$ means we add a number to 3.\n\nStep 3: Interpret the other part of the equation.\n\n$10-2y$ means we subtract twice the number from 10. We can also say it is the difference between 10 and twice the number.\n\nStep 4: Say how the two parts are equal to each other.\n\nWhen we add 3 to a number, the answer is equal to the difference between 10 and twice the number.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b011",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.2: Translate equations into word sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.2: Translate equations into word sentences\n\nWrite a word sentence for each of the following algebraic equations.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b011-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.2: Translate equations into word sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.2: Translate equations into word sentences\n\nWrite a word sentence for each of the following algebraic equations.\n\n1. $$\nx+12=25\n$$",
    "answer_text": "If we add 12 to a number, the answer is 25.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b011-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.2: Translate equations into word sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.2: Translate equations into word sentences\n\nWrite a word sentence for each of the following algebraic equations.\n\n2. $$\n2y-8=30\n$$",
    "answer_text": "The difference between twice a number and 8 is 30.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b011-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.2: Translate equations into word sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.2: Translate equations into word sentences\n\nWrite a word sentence for each of the following algebraic equations.\n\n3. $$\n\\frac{2}{3}p=12\n$$",
    "answer_text": "Two thirds of a number is equal to 12.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b011-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.2: Translate equations into word sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.2: Translate equations into word sentences\n\nWrite a word sentence for each of the following algebraic equations.\n\n4. $$\n120-x-3x=60\n$$",
    "answer_text": "If we subtract a number and three times the same number from 120, the answer is 60.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b011-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.2: Translate equations into word sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.2: Translate equations into word sentences\n\nWrite a word sentence for each of the following algebraic equations.\n\n5. $$\n2c+\\frac{1}{2}c=10\n$$",
    "answer_text": "The sum of twice a number and half of the same number is 10.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b011-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.2: Translate equations into word sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.2: Translate equations into word sentences\n\nWrite a word sentence for each of the following algebraic equations.\n\n6. $$\n62=8z-\\frac{1}{4}z\n$$",
    "answer_text": "The difference between 8 times a number and a quarter of the same number is 62.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b011-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.2: Translate equations into word sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.2: Translate equations into word sentences\n\nWrite a word sentence for each of the following algebraic equations.\n\n7. $$\n2p+5p=p-10\n$$",
    "answer_text": "The sum of twice a number and five times the same number is equal to 10 less than the number.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b011-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.2: Translate equations into word sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.2: Translate equations into word sentences\n\nWrite a word sentence for each of the following algebraic equations.\n\n8. $$\n\\frac{a-10}{4}=20\n$$",
    "answer_text": "When the difference between a number and 10 is divided by 4, the answer is 20.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b011-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.2: Translate equations into word sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.2: Translate equations into word sentences\n\nWrite a word sentence for each of the following algebraic equations.\n\n9. $$\n2x+2(2x)=30\n$$",
    "answer_text": "The sum of twice a number and four times the same number is 30.\n\nOR\n\nThe length of a rectangle with a perimeter of 30 units is twice its breadth.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b025",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": null
    },
    "content_text": "Equations are very useful when you need to solve problems that are described in words. In Chapter 9, you learnt that these steps can be used to solve a problem that is described in words:\n\n1. **Understand the problem:** Read the question carefully a few times. Identify the information you have. Make sure you know what is asked. It may help to draw a picture.\n2. **Make a plan:** Identify the unknown(s). Make one unknown $x$. If there is more than one unknown, express all of them in terms of $x$. Write an equation that you can use to solve the problem.\n3. **Carry out the plan:** Solve the equation.\n4. **Look back:** Check your solution(s). Make sure that you have given the answers for everything that was asked.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b026",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": "Worked example 11.7: Solving a problem using an equation"
    },
    "content_text": "",
    "prompt_text": "The length of a rectangle with a perimeter of 120 cm is 10 cm longer than its breadth. Determine the length and the breadth of the rectangle in centimetres.",
    "answer_text": "Step 1: Understand the problem.\n\n- Given: $P$ = 120 cm\n- Given: Length equals breadth plus 10 cm\n- Asked: Length in cm\n- Asked: Breadth in cm\n\nStep 2: Devise a plan, which includes expressing all your unknown values in terms of a variable.\n\n- Breadth: $x$\n- Length: $x+10$\n- For a rectangle: $P=2l+2b$\n\nThe equation is:\n\n$$\n120=2(x+10)+2(x)\n$$\n\nStep 3: Carry out the plan.\n\n$$\n\\begin{align}\n120 &= 2(x+10) + 2x  \\\\\n120 &= 2x + 20 +2x \\\\\n120 &= 4x + 20 \\\\\n120-20 &= 4x+20-20 \\\\\n100&=4x \\\\\n\\frac{100}{4}&=\\frac{4x}{4} \\\\\n\\therefore 25&=x\n\\end{align}\n$$\n\nTherefore:\n\n$$\n\\begin{align}\n\\text{Breadth} &= 25\\text{ cm}  \\\\\n\\text{Length}\\phantom{0} &= 25+10 \\\\\n&=35\\text{ cm} \\\\\n\\end{align}\n$$\n\nStep 4: Look back to check.\n\n$$\n\\begin{align}\n120 &= 2(x+10) + 2x \\\\\n120 &= 2(25+10) +2(25) \\\\\n120&=2(35)+50 \\\\\n120&=70+50 \\\\\n120&=120 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$\n\nThe length is 35 cm and the breadth is 25 cm.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b027",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": "Exercise 11.5: Use equations to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.5: Use equations to solve problems",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b027-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": "Exercise 11.5: Use equations to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.5: Use equations to solve problems\n\n1. Erioluwa has $₦\\,82$. This is $₦\\,15$ more than Ifedolapo. How much money does Ifedolapo have?",
    "answer_text": "Let the amount of money that Ifedolapo has be $x$.\n\n$$\n\\begin{align}\nx&=82-15 \\\\\n\\therefore x&=67 \\\\\n\\end{align}\n$$\n\nIfedolapo has $₦\\,67$.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b027-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": "Exercise 11.5: Use equations to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.5: Use equations to solve problems\n\n2. Halima saved a certain amount of money. After she did some holiday work, she could add $₦\\,125$ to her savings. She now has $₦\\,203$. How much money did she have saved before she did the holiday work?",
    "answer_text": "Let the amount Halima had saved before the holiday work be $x$.\n\n$$\n\\begin{align}\nx+125&=203 \\\\\nx+125-125&=203-125 \\\\\n\\therefore x&=78 \\\\\n\\end{align}\n$$\n\nHalima had $₦\\,78$ saved before the holiday work.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b027-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": "Exercise 11.5: Use equations to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.5: Use equations to solve problems\n\n3. Oluchi walks 25% of a certain distance. If he walked 55 m, how far is the full distance?",
    "answer_text": "Let the full distance be $x$.\n\n$$\n\\begin{align}\n25 \\% \\times x &=55 \\\\\n\\frac{25}{100}\\times x&= 55 \\\\\n\\frac{1}{4}x&=55 \\\\\n\\frac{4}{1}\\times \\frac{1}{4} x &= 55 \\times \\frac{4}{1} \\\\\n\\therefore x &= 220\n\\end{align}\n$$\n\nThe full distance is 220 m.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b027-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": "Exercise 11.5: Use equations to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.5: Use equations to solve problems\n\n4. The sum of three consecutive numbers is 36. Determine the three numbers.",
    "answer_text": "Let the first number be $x$. Then the second number is $x+1$, and the third number is $x+2$.\n\n$$\n\\begin{align}\nx+(x+1)+(x+2) &=36 \\\\\nx+x+1+x+2 &= 36 \\\\\n3x+3 &=36 \\\\\n3x+3-3&=36-3 \\\\\n3x&=33 \\\\\n\\frac{3x}{3} &= \\frac{33}{3} \\\\\n\\therefore x &= 11 \\\\\nx+1 &= 12 \\\\\n\\text{and }x+2 &=13\n\\end{align}\n$$\n\nThe numbers are 11, 12 and 13.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b027-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": "Exercise 11.5: Use equations to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.5: Use equations to solve problems\n\n5. In a JSS1 class of 48 students, there are twice as many boys as girls. Determine how many boys and how many girls are in the class.",
    "answer_text": "Let the number of girls be $x$. Then the number of boys is $2x$.\n\n$$\n\\begin{align}\nx+2x&=48 \\\\\n3x&=48 \\\\\n\\frac{3x}{3}&=\\frac{48}{3} \\\\\n\\therefore x&=16 \\\\\n\\therefore 2x&=2(16) \\\\\n&=32\n\\end{align}\n$$\n\nThere are 16 girls and 32 boys in the class.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b027-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": "Exercise 11.5: Use equations to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.5: Use equations to solve problems\n\n6. A mother is three times older than her son. Their combined age is 84 years. Determine the ages of the mother and her son.",
    "answer_text": "Let the age of the son be $x$. Then the age of the mother is $3x$.\n\n$$\n\\begin{align}\nx+3x&=84 \\\\\n4x&=84 \\\\\n\\frac{4x}{4}&=\\frac{84}{4} \\\\\n\\therefore x&=21 \\\\\n\\therefore 3x&=3(21) \\\\\n&=63\n\\end{align}\n$$\n\nThe son is 21 years old and the mother is 63 years old.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b027-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": "Exercise 11.5: Use equations to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.5: Use equations to solve problems\n\n7. The difference between four times a number and the number plus 5 is 10. Determine the number.",
    "answer_text": "Let the number be $x$.\n\n$$\n\\begin{align}\n4x-(x+5) &=10 \\\\\n4x-x-5 &= 10 \\\\\n3x-5 &=10 \\\\\n3x-5+5&=10+5 \\\\\n3x&=15 \\\\\n\\frac{3x}{3} &= \\frac{15}{3} \\\\\n\\therefore x &= 5 \\\\\n\\end{align}\n$$\n\nThe number is 5.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b027-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": "Exercise 11.5: Use equations to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.5: Use equations to solve problems\n\n8. A pen costs $₦\\,4$ more than a ruler. The price for 3 pens and 8 rulers altogether is $₦\\,142$. Determine the price of a pen and the price of a ruler.",
    "answer_text": "Let the price of a ruler be $x$. Then the price of a pen is $x+4$.\n\n$$\n\\begin{align}\n3x+8(x+4) &=142 \\\\\n3x+8x+32 &= 142 \\\\\n11x+32 &=142 \\\\\n11x+32-32&=142-32 \\\\\n11x&=110 \\\\\n\\frac{11x}{11} &= \\frac{110}{11} \\\\\n\\therefore x &= 10 \\\\\n\\therefore x+4&=14\n\\end{align}\n$$\n\nThe price of a ruler is $₦\\,10$ and the price of a pen is $₦\\,14$.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b027-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": "Exercise 11.5: Use equations to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.5: Use equations to solve problems\n\n9. You must cut 68 cm of rope into three pieces. The second piece must have double the length of the first piece. The third piece must be 8 cm longer than the second piece. Determine the length of each of the three pieces of rope.",
    "answer_text": "Let the length of the first piece be $x$. Then then the length of the second piece is $2x$. The length of the third piece is then $2x+8$.\n\n$$\n\\begin{align}\nx+2x+(2x+8) &=68 \\\\\nx+2x+2x+8 &= 68 \\\\\n5x+8 &=68 \\\\\n5x+8-8&=68-8 \\\\\n5x&=60 \\\\\n\\frac{5x}{5} &= \\frac{60}{5} \\\\\n\\therefore x &= 12 \\\\\n\\therefore 2x&=2(12) \\\\\n&=24 \\\\\n\\text{and }2x+8&=2(12)+8 \\\\\n&=32\n\\end{align}\n$$\n\nThe pieces must be 12 cm, 24 cm and 32 cm long.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b027-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": "Exercise 11.5: Use equations to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.5: Use equations to solve problems\n\n10. Lami has twice as much money as Chinweike. Latifah has three times the amount of money that Chinweike has. Chinweike's money plus $₦\\,24$ is equal to the amount of money that Lami and Latifah have together. Determine how much money each girl has.",
    "answer_text": "Let the amount of money that Chinweike has be $x$. Then the amount of money that Lami has is $2x$. The amount of money that Latifah has is $3x$.\n\n$$\n\\begin{align}\n2x+3x &=x+24 \\\\\n5x &= x+24 \\\\\n5x-x &=x-x+24 \\\\\n4x&=24 \\\\\n\\frac{4x}{4} &= \\frac{24}{4} \\\\\n\\therefore x &= 6 \\\\\n\\therefore 2x&=2(6) \\\\\n&=12 \\\\\n\\text{and }3x&=3(6) \\\\\n&=18\n\\end{align}\n$$\n\nChinweike has $₦\\,6$, Lami has $₦\\,12$ and Latifah has $₦\\,18$.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b028",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.4 Summary",
      "h3": null
    },
    "content_text": "- An algebraic equation is a mathematical sentence that contains a combination of numbers, symbols, variables and mathematical operators. It always has an equals sign.\n- The main differences between algebraic expressions and algebraic equations are:\n  - An expression is a phrase and an equation is a sentence.\n  - An expression does not have an equals sign, while an equation has an equals sign.\n  - We simplify an expression, but solve an equation.\n  - The variables in an expression can have many values, while only certain values make an equation true.\n- We can translate word sentences into equations. We can also translate equations into word sentences.\n- The solution of an equation is the value of the variable that makes the equation true. When we find this solution, we solve the equation.\n- To solve an equation, we must isolate the variable. If $x$ is the variable, we must get the equation in the form: $x=\\text{value}$.\n- We can represent an equation as a balancing scale with two pans. Whatever we do on one side of an equation, we must also do on the other side.\n- We can check our solution for an equation by replacing the variable in the original equation with the solution. The solution is correct if the left-hand side has the same value as the right-hand side.\n- We can follow these steps to solve a problem that is described in words:\n  - Understand the problem by reading it carefully.\n  - Make a plan by identifying the unknown(s) and writing an equation.\n  - Carry out the plan by solving the equation.\n  - Look back by checking your solution.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
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
  "topic_key": "jss1-math-simple-equations",
  "topic": "Simple Equations",
  "subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa",
  "subtopic_title": "Translation of word problems into equations and vice-versa",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa-po01",
        "source_performance_objective_index": 1,
        "text": "Translate word sentences into mathematical equations"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "translation-of-word-problems-into-equations-ao-translate-word-sentences",
          "text": "Translate word sentences into mathematical equations."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa-po02",
        "source_performance_objective_index": 2,
        "text": "Use mathematical equations to represent word sentences"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "translation-of-word-problems-into-equations-ao-use-equations-to-represent",
          "text": "Use mathematical equations to represent word sentences."
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
    "record_id": "ch11-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": null,
      "h3": null
    },
    "content_text": "You have learnt that an algebraic *expression* is a mathematical phrase or statement. Algebraic expressions do not have equals signs. In this chapter we will be dealing with algebraic *equations*. Algebraic equations are mathematical sentences with equals signs. You will learn how to formulate and solve algebraic equations.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b002",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": null
    },
    "content_text": "An **algebraic equation** is a mathematical sentence that contains a combination of numbers, symbols, variables and mathematical operators. It always has an equals sign.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b003",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": null
    },
    "content_text": "**algebraic equation** An algebraic equation is a mathematical sentence that contains a combination of numbers, symbols, variables and mathematical operators. It always has an equals sign.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b004",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "The difference between expressions and equations"
    },
    "content_text": "It is important that you understand the difference between algebraic expressions and algebraic equations. The table below lists the main differences.\n\n- An expression is a phrase. An equation is a sentence.\n- We simplify an expression. We solve an equation.\n- An expression does not have an equals sign. An equation has an equals sign.\n- An expression gives the relationship between variables. An equation shows that two expressions are equal.\n- The variables in an expression can have a whole range of values. The variables in an equation only has specific values.\n- Example expression: two more than a number, written as $x+2$.\n- Example equation: two more than a number is five, written as $x+2=5$.\n\nLet's look at an example from Chapter 10 to explain this further.\n\nSuppose a shop owner sells maize at $₦\\,x$ per cup. She also sells rice per cup, at double the price of the maize. On a specific day, she sold 50 cups of maize and 45 cups of rice.\n\n- We can write an *expression* for her income for the day: $50\\times x+45\\times 2x$.\n- We can simplify the expression to $50x+90x$, and simplify further to $140x$.\n- Her income for the day is therefore $₦\\,140x$.\n- Her income depends on the cost of a cup of maize, which can be any positive number.\n- If we know that her income for the day was $₦\\,7,700$, we can write an *equation*: $50\\times x+45\\times 2x = 7,700$.\n- We can simplify the equation to $140x=7,700$.\n- The only value that makes this sentence true is $55$.\n- Now we know that the price of a cup of maize is $₦\\,55$ and the price of a cup of rice is $2\\times55=₦\\,110$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b005",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Translate word sentences into algebraic equations"
    },
    "content_text": "In Section 9.3 of Chapter 9 and Section 10.6 of Chapter 10 you were given some examples of ways to write word phrases as mathematical statements. Revise those sections before you go on.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b006",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Worked example 11.1: Translating simple word sentences into algebraic equations"
    },
    "content_text": "",
    "prompt_text": "If a number is multiplied by 4, the answer is 6 more than the number. Write an equation to represent this.",
    "answer_text": "Step 1: Identify the unknown and make it $x$.\n\nIn this case, the unknown is the number. So, we say the number is $x$.\n\nStep 2: Write an expression or value for one part of the equation.\n\nOne of the phrases states that the number is multiplied by 4. We write this as $4x$.\n\nStep 3: Write an expression or value for the other part of the equation.\n\nAnother phrase refers to 6 more than the number. We write this as $x+6$.\n\nStep 4: Remember that an equation has an equals sign. Decide how the two expressions are equal to each other.\n\nThe words say the answer of the multiplication by 4 gives the addition of 6. Therefore:\n\n$$\n4x=x+6\n$$\n\nIf we solve the equation above, we get $x=2$. You will learn how to solve equations in the next section.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b007",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Worked example 11.2: Translating more complex word sentences into algebraic equations"
    },
    "content_text": "",
    "prompt_text": "A mother is twice as old as her daughter. In two years' time, their combined ages will be 52 years. Write an equation to represent this.",
    "answer_text": "Step 1: Identify the unknowns.\n\nThere are two unknowns:\n\n- The mother's age\n- The daughter's age\n\nStep 2: Make the one unknown $x$. Write an expression for the other unknown in terms of $x$.\n\n- Make the daughter's age $x$.\n- The mother's age is twice that. Therefore, the mother's age is $2x$.\n\nWe could also say the mother's age is $x$ and the daughter's age is $\\frac{1}{2}x$. However, it is often easier to solve equations with whole numbers as coefficients than equations with fractions as coefficients.\n\nStep 3: Write an expression or value for one part of the equation.\n\nOne phrase refers to their ages in two years' time:\n\n- The daughter will be $x+2$ years old.\n- The mother will be $2x+2$ years old.\n\nStep 4: Write an expression or value for the other part of the equation.\n\nAnother phrase says their combined ages will be 52.\n\nStep 5: Remember that an equation has an equals sign. Decide how the two expressions are equal to each other.\n\nTheir combined ages in two years' time is equal to 52. If we combine their ages, this means we add the ages. Therefore:\n\n$$\n(x+2)+(2x+2)=52\n$$\n\nIf we solve the equation above, we get $x=16$. This means the daughter is 16 years old and the mother is 32 years old. You will learn how to solve equations in the next section.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b008",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.1: Translate word sentences into equations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.1: Translate word sentences into equations\n\nWrite an algebraic equation for each of the following situations.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b008-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.1: Translate word sentences into equations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.1: Translate word sentences into equations\n\nWrite an algebraic equation for each of the following situations.\n\n1. If we add 23 to a number, the answer is 42.",
    "answer_text": "$$\nx+23=42\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b008-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.1: Translate word sentences into equations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.1: Translate word sentences into equations\n\nWrite an algebraic equation for each of the following situations.\n\n2. The difference between 75 and a number is 20.",
    "answer_text": "$$\n75-x=20\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b008-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.1: Translate word sentences into equations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.1: Translate word sentences into equations\n\nWrite an algebraic equation for each of the following situations.\n\n3. A pen costs twice as much as a ruler. The cost of 5 pens and 7 rulers is $₦\\,102$.",
    "answer_text": "$$\n5(2x)+7x=102\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b008-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.1: Translate word sentences into equations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.1: Translate word sentences into equations\n\nWrite an algebraic equation for each of the following situations.\n\n4. If we add 9 to half of a number, the answer is twice the number.",
    "answer_text": "$$\n\\frac{1}{2}x+9=2x\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b008-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.1: Translate word sentences into equations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.1: Translate word sentences into equations\n\nWrite an algebraic equation for each of the following situations.\n\n5. The sum of three consecutive numbers is 24.",
    "answer_text": "$$\nx+(x+1)+(x+2)=24\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b008-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.1: Translate word sentences into equations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.1: Translate word sentences into equations\n\nWrite an algebraic equation for each of the following situations.\n\n6. The length of a rectangle with a perimeter of 40 cm is three times more than its breadth.",
    "answer_text": "$$\n2x+2(3x)=40\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b008-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.1: Translate word sentences into equations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.1: Translate word sentences into equations\n\nWrite an algebraic equation for each of the following situations.\n\n7. The combined area of two rectangles is 49 square units. The area of one rectangle is six times more than the area of the other rectangle.",
    "answer_text": "$$\nx+6x=49\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b008-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.1: Translate word sentences into equations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.1: Translate word sentences into equations\n\nWrite an algebraic equation for each of the following situations.\n\n8. If the sum of a number and 6 is divided by 10, the answer is 24.",
    "answer_text": "$$\n\\frac{x+6}{10}=24\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b008-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.1: Translate word sentences into equations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.1: Translate word sentences into equations\n\nWrite an algebraic equation for each of the following situations.\n\n9. Danjuma has $₦\\,500$. He spends a certain amount on snacks and exactly the same amount on data. He then spends twice the amount he spent on snacks to buy stationery. He has $₦\\,40$ left.",
    "answer_text": "$$\n500-x-x-2x=40\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b008-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.1: Translate word sentences into equations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.1: Translate word sentences into equations\n\nWrite an algebraic equation for each of the following situations.\n\n10. Ngozi goes to school. She walks for a few minutes and then runs for 180 seconds. Then she walks again for half the time she walked in the beginning. Her journey takes 15 minutes.",
    "answer_text": "If we work in seconds:\n\n$$\n2x+180+x=15\\times 60\n$$\n\nIf we work in minutes:\n\n$$\n2x+\\frac{180}{60}+x=15\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b009",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Translate algebraic equations into word sentences"
    },
    "content_text": "We can also translate algebraic equations into word sentences. You can make up a story if you want to, or you can just think of the variable as a number.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b010",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Worked example 11.3: Translating algebraic equations into word sentences"
    },
    "content_text": "",
    "prompt_text": "Translate the following equation into a word sentence:\n\n$$\n3+y=10-2y\n$$",
    "answer_text": "Step 1: Assume that the variable is a number.\n\nIn this case the variable is $y$. So we assume that $y$ is a number.\n\nStep 2: Interpret one part of the equation.\n\n$3+y$ means we add a number to 3.\n\nStep 3: Interpret the other part of the equation.\n\n$10-2y$ means we subtract twice the number from 10. We can also say it is the difference between 10 and twice the number.\n\nStep 4: Say how the two parts are equal to each other.\n\nWhen we add 3 to a number, the answer is equal to the difference between 10 and twice the number.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b011",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.2: Translate equations into word sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.2: Translate equations into word sentences\n\nWrite a word sentence for each of the following algebraic equations.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b011-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.2: Translate equations into word sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.2: Translate equations into word sentences\n\nWrite a word sentence for each of the following algebraic equations.\n\n1. $$\nx+12=25\n$$",
    "answer_text": "If we add 12 to a number, the answer is 25.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b011-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.2: Translate equations into word sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.2: Translate equations into word sentences\n\nWrite a word sentence for each of the following algebraic equations.\n\n2. $$\n2y-8=30\n$$",
    "answer_text": "The difference between twice a number and 8 is 30.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b011-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.2: Translate equations into word sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.2: Translate equations into word sentences\n\nWrite a word sentence for each of the following algebraic equations.\n\n3. $$\n\\frac{2}{3}p=12\n$$",
    "answer_text": "Two thirds of a number is equal to 12.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b011-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.2: Translate equations into word sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.2: Translate equations into word sentences\n\nWrite a word sentence for each of the following algebraic equations.\n\n4. $$\n120-x-3x=60\n$$",
    "answer_text": "If we subtract a number and three times the same number from 120, the answer is 60.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b011-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.2: Translate equations into word sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.2: Translate equations into word sentences\n\nWrite a word sentence for each of the following algebraic equations.\n\n5. $$\n2c+\\frac{1}{2}c=10\n$$",
    "answer_text": "The sum of twice a number and half of the same number is 10.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b011-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.2: Translate equations into word sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.2: Translate equations into word sentences\n\nWrite a word sentence for each of the following algebraic equations.\n\n6. $$\n62=8z-\\frac{1}{4}z\n$$",
    "answer_text": "The difference between 8 times a number and a quarter of the same number is 62.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b011-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.2: Translate equations into word sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.2: Translate equations into word sentences\n\nWrite a word sentence for each of the following algebraic equations.\n\n7. $$\n2p+5p=p-10\n$$",
    "answer_text": "The sum of twice a number and five times the same number is equal to 10 less than the number.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b011-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.2: Translate equations into word sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.2: Translate equations into word sentences\n\nWrite a word sentence for each of the following algebraic equations.\n\n8. $$\n\\frac{a-10}{4}=20\n$$",
    "answer_text": "When the difference between a number and 10 is divided by 4, the answer is 20.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b011-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.1 Formulating equations",
      "h3": "Exercise 11.2: Translate equations into word sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.2: Translate equations into word sentences\n\nWrite a word sentence for each of the following algebraic equations.\n\n9. $$\n2x+2(2x)=30\n$$",
    "answer_text": "The sum of twice a number and four times the same number is 30.\n\nOR\n\nThe length of a rectangle with a perimeter of 30 units is twice its breadth.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b025",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": null
    },
    "content_text": "Equations are very useful when you need to solve problems that are described in words. In Chapter 9, you learnt that these steps can be used to solve a problem that is described in words:\n\n1. **Understand the problem:** Read the question carefully a few times. Identify the information you have. Make sure you know what is asked. It may help to draw a picture.\n2. **Make a plan:** Identify the unknown(s). Make one unknown $x$. If there is more than one unknown, express all of them in terms of $x$. Write an equation that you can use to solve the problem.\n3. **Carry out the plan:** Solve the equation.\n4. **Look back:** Check your solution(s). Make sure that you have given the answers for everything that was asked.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b026",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": "Worked example 11.7: Solving a problem using an equation"
    },
    "content_text": "",
    "prompt_text": "The length of a rectangle with a perimeter of 120 cm is 10 cm longer than its breadth. Determine the length and the breadth of the rectangle in centimetres.",
    "answer_text": "Step 1: Understand the problem.\n\n- Given: $P$ = 120 cm\n- Given: Length equals breadth plus 10 cm\n- Asked: Length in cm\n- Asked: Breadth in cm\n\nStep 2: Devise a plan, which includes expressing all your unknown values in terms of a variable.\n\n- Breadth: $x$\n- Length: $x+10$\n- For a rectangle: $P=2l+2b$\n\nThe equation is:\n\n$$\n120=2(x+10)+2(x)\n$$\n\nStep 3: Carry out the plan.\n\n$$\n\\begin{align}\n120 &= 2(x+10) + 2x  \\\\\n120 &= 2x + 20 +2x \\\\\n120 &= 4x + 20 \\\\\n120-20 &= 4x+20-20 \\\\\n100&=4x \\\\\n\\frac{100}{4}&=\\frac{4x}{4} \\\\\n\\therefore 25&=x\n\\end{align}\n$$\n\nTherefore:\n\n$$\n\\begin{align}\n\\text{Breadth} &= 25\\text{ cm}  \\\\\n\\text{Length}\\phantom{0} &= 25+10 \\\\\n&=35\\text{ cm} \\\\\n\\end{align}\n$$\n\nStep 4: Look back to check.\n\n$$\n\\begin{align}\n120 &= 2(x+10) + 2x \\\\\n120 &= 2(25+10) +2(25) \\\\\n120&=2(35)+50 \\\\\n120&=70+50 \\\\\n120&=120 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$\n\nThe length is 35 cm and the breadth is 25 cm.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b027",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": "Exercise 11.5: Use equations to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.5: Use equations to solve problems",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b027-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": "Exercise 11.5: Use equations to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.5: Use equations to solve problems\n\n1. Erioluwa has $₦\\,82$. This is $₦\\,15$ more than Ifedolapo. How much money does Ifedolapo have?",
    "answer_text": "Let the amount of money that Ifedolapo has be $x$.\n\n$$\n\\begin{align}\nx&=82-15 \\\\\n\\therefore x&=67 \\\\\n\\end{align}\n$$\n\nIfedolapo has $₦\\,67$.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b027-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": "Exercise 11.5: Use equations to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.5: Use equations to solve problems\n\n2. Halima saved a certain amount of money. After she did some holiday work, she could add $₦\\,125$ to her savings. She now has $₦\\,203$. How much money did she have saved before she did the holiday work?",
    "answer_text": "Let the amount Halima had saved before the holiday work be $x$.\n\n$$\n\\begin{align}\nx+125&=203 \\\\\nx+125-125&=203-125 \\\\\n\\therefore x&=78 \\\\\n\\end{align}\n$$\n\nHalima had $₦\\,78$ saved before the holiday work.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b027-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": "Exercise 11.5: Use equations to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.5: Use equations to solve problems\n\n3. Oluchi walks 25% of a certain distance. If he walked 55 m, how far is the full distance?",
    "answer_text": "Let the full distance be $x$.\n\n$$\n\\begin{align}\n25 \\% \\times x &=55 \\\\\n\\frac{25}{100}\\times x&= 55 \\\\\n\\frac{1}{4}x&=55 \\\\\n\\frac{4}{1}\\times \\frac{1}{4} x &= 55 \\times \\frac{4}{1} \\\\\n\\therefore x &= 220\n\\end{align}\n$$\n\nThe full distance is 220 m.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b027-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": "Exercise 11.5: Use equations to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.5: Use equations to solve problems\n\n4. The sum of three consecutive numbers is 36. Determine the three numbers.",
    "answer_text": "Let the first number be $x$. Then the second number is $x+1$, and the third number is $x+2$.\n\n$$\n\\begin{align}\nx+(x+1)+(x+2) &=36 \\\\\nx+x+1+x+2 &= 36 \\\\\n3x+3 &=36 \\\\\n3x+3-3&=36-3 \\\\\n3x&=33 \\\\\n\\frac{3x}{3} &= \\frac{33}{3} \\\\\n\\therefore x &= 11 \\\\\nx+1 &= 12 \\\\\n\\text{and }x+2 &=13\n\\end{align}\n$$\n\nThe numbers are 11, 12 and 13.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b027-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": "Exercise 11.5: Use equations to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.5: Use equations to solve problems\n\n5. In a JSS1 class of 48 students, there are twice as many boys as girls. Determine how many boys and how many girls are in the class.",
    "answer_text": "Let the number of girls be $x$. Then the number of boys is $2x$.\n\n$$\n\\begin{align}\nx+2x&=48 \\\\\n3x&=48 \\\\\n\\frac{3x}{3}&=\\frac{48}{3} \\\\\n\\therefore x&=16 \\\\\n\\therefore 2x&=2(16) \\\\\n&=32\n\\end{align}\n$$\n\nThere are 16 girls and 32 boys in the class.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b027-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": "Exercise 11.5: Use equations to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.5: Use equations to solve problems\n\n6. A mother is three times older than her son. Their combined age is 84 years. Determine the ages of the mother and her son.",
    "answer_text": "Let the age of the son be $x$. Then the age of the mother is $3x$.\n\n$$\n\\begin{align}\nx+3x&=84 \\\\\n4x&=84 \\\\\n\\frac{4x}{4}&=\\frac{84}{4} \\\\\n\\therefore x&=21 \\\\\n\\therefore 3x&=3(21) \\\\\n&=63\n\\end{align}\n$$\n\nThe son is 21 years old and the mother is 63 years old.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b027-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": "Exercise 11.5: Use equations to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.5: Use equations to solve problems\n\n7. The difference between four times a number and the number plus 5 is 10. Determine the number.",
    "answer_text": "Let the number be $x$.\n\n$$\n\\begin{align}\n4x-(x+5) &=10 \\\\\n4x-x-5 &= 10 \\\\\n3x-5 &=10 \\\\\n3x-5+5&=10+5 \\\\\n3x&=15 \\\\\n\\frac{3x}{3} &= \\frac{15}{3} \\\\\n\\therefore x &= 5 \\\\\n\\end{align}\n$$\n\nThe number is 5.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b027-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": "Exercise 11.5: Use equations to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.5: Use equations to solve problems\n\n8. A pen costs $₦\\,4$ more than a ruler. The price for 3 pens and 8 rulers altogether is $₦\\,142$. Determine the price of a pen and the price of a ruler.",
    "answer_text": "Let the price of a ruler be $x$. Then the price of a pen is $x+4$.\n\n$$\n\\begin{align}\n3x+8(x+4) &=142 \\\\\n3x+8x+32 &= 142 \\\\\n11x+32 &=142 \\\\\n11x+32-32&=142-32 \\\\\n11x&=110 \\\\\n\\frac{11x}{11} &= \\frac{110}{11} \\\\\n\\therefore x &= 10 \\\\\n\\therefore x+4&=14\n\\end{align}\n$$\n\nThe price of a ruler is $₦\\,10$ and the price of a pen is $₦\\,14$.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b027-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": "Exercise 11.5: Use equations to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.5: Use equations to solve problems\n\n9. You must cut 68 cm of rope into three pieces. The second piece must have double the length of the first piece. The third piece must be 8 cm longer than the second piece. Determine the length of each of the three pieces of rope.",
    "answer_text": "Let the length of the first piece be $x$. Then then the length of the second piece is $2x$. The length of the third piece is then $2x+8$.\n\n$$\n\\begin{align}\nx+2x+(2x+8) &=68 \\\\\nx+2x+2x+8 &= 68 \\\\\n5x+8 &=68 \\\\\n5x+8-8&=68-8 \\\\\n5x&=60 \\\\\n\\frac{5x}{5} &= \\frac{60}{5} \\\\\n\\therefore x &= 12 \\\\\n\\therefore 2x&=2(12) \\\\\n&=24 \\\\\n\\text{and }2x+8&=2(12)+8 \\\\\n&=32\n\\end{align}\n$$\n\nThe pieces must be 12 cm, 24 cm and 32 cm long.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b027-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.3 Using equations to solve problems",
      "h3": "Exercise 11.5: Use equations to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.5: Use equations to solve problems\n\n10. Lami has twice as much money as Chinweike. Latifah has three times the amount of money that Chinweike has. Chinweike's money plus $₦\\,24$ is equal to the amount of money that Lami and Latifah have together. Determine how much money each girl has.",
    "answer_text": "Let the amount of money that Chinweike has be $x$. Then the amount of money that Lami has is $2x$. The amount of money that Latifah has is $3x$.\n\n$$\n\\begin{align}\n2x+3x &=x+24 \\\\\n5x &= x+24 \\\\\n5x-x &=x-x+24 \\\\\n4x&=24 \\\\\n\\frac{4x}{4} &= \\frac{24}{4} \\\\\n\\therefore x &= 6 \\\\\n\\therefore 2x&=2(6) \\\\\n&=12 \\\\\n\\text{and }3x&=3(6) \\\\\n&=18\n\\end{align}\n$$\n\nChinweike has $₦\\,6$, Lami has $₦\\,12$ and Latifah has $₦\\,18$.",
    "primary_subtopic_id": "jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa"
  },
  {
    "record_id": "ch11-b028",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.4 Summary",
      "h3": null
    },
    "content_text": "- An algebraic equation is a mathematical sentence that contains a combination of numbers, symbols, variables and mathematical operators. It always has an equals sign.\n- The main differences between algebraic expressions and algebraic equations are:\n  - An expression is a phrase and an equation is a sentence.\n  - An expression does not have an equals sign, while an equation has an equals sign.\n  - We simplify an expression, but solve an equation.\n  - The variables in an expression can have many values, while only certain values make an equation true.\n- We can translate word sentences into equations. We can also translate equations into word sentences.\n- The solution of an equation is the value of the variable that makes the equation true. When we find this solution, we solve the equation.\n- To solve an equation, we must isolate the variable. If $x$ is the variable, we must get the equation in the form: $x=\\text{value}$.\n- We can represent an equation as a balancing scale with two pans. Whatever we do on one side of an equation, we must also do on the other side.\n- We can check our solution for an equation by replacing the variable in the original equation with the solution. The solution is correct if the left-hand side has the same value as the right-hand side.\n- We can follow these steps to solve a problem that is described in words:\n  - Understand the problem by reading it carefully.\n  - Make a plan by identifying the unknown(s) and writing an equation.\n  - Carry out the plan by solving the equation.\n  - Look back by checking your solution.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
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
