# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-3",
  "topic_key": "jss1-math-simple-equations",
  "topic": "Simple Equations",
  "subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations",
  "subtopic_title": "Solution of simple equations",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-simple-equations-solution-of-simple-equations-po01",
        "source_performance_objective_index": 1,
        "text": "Solve simple equations and cross-check the answers"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "solution-of-simple-equations-ao-solve-simple-equations",
          "text": "Solve simple equations."
        },
        {
          "atomic_objective_id": "solution-of-simple-equations-ao-cross-check-answers",
          "text": "Cross-check the answers to simple equations."
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
    "record_id": "ch11-b012",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "The solution of an equation"
    },
    "content_text": "You have learnt how to find the values that make open sentences true. Look at the following algebraic equation:\n\n$$\n3+x=5\n$$\n\nIt is easy to see that the only value for $x$ that will make this equation true is 2. This is because $3+2=5$. We say the number 2 is the **solution** of the equation and we write it as:\n\n$$\nx=2\n$$\n\nWhen we find the solution of an equation, we say we **solve** the equation.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b013",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "The solution of an equation"
    },
    "content_text": "**solution** The solution of an equation is the value of the variable that makes the equation true.\n\n**solve** When we solve an equation, we find the value of the variable that makes the equation true.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b014",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "The solution of an equation"
    },
    "content_text": "To solve an equation, we must isolate the variable. If $x$ is the variable, we must get the equation in the form:\n\n$$\nx=\\text{value}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b015",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Representing an equation as a balancing scale"
    },
    "content_text": "To help us solve an algebraic equation, we can show it as a balancing scale. The picture shows what a scale looks like. This scale is balanced, because nothing has been placed on it.\n\nIf we place a mass piece on one of the pans, the scale becomes unbalanced.\n\nWe can balance the scale again by placing an identical mass piece on the other pan.\n\nAs long as identical mass pieces are placed on both pans, the scale will remain in balance.\n\nIn an equation, the equals sign shows that two expressions (or an expression and a value) are equal to each other. We can think of each side of the equation as one of the pans of a scale. As long as we do exactly the same on each side of the equation, the equation will remain true.\n\nConsider the following algebraic equation:\n\n$$\nx-5=14\n$$\n\nWe can represent it on the pans of a scale as follows.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b016",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Representing an equation as a balancing scale"
    },
    "content_text": "Go back to Chapter 9 if you need to revise inverse operations. Remember that addition and subtraction are inverse operations, and multiplication and division are inverse operations.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b017",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Representing an equation as a balancing scale"
    },
    "content_text": "Whatever we add to the one pan, we must also add to the other pan. The scale now shows:\n\nRemember that $-5+5=0$. Therefore, if we simplify both sides, we get the solution of the equation:\n\n$$\nx=19\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b018",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Worked example 11.4: Finding the solution of an equation"
    },
    "content_text": "",
    "prompt_text": "Solve the following equation:\n\n$$\n2x+x-10=2\n$$",
    "answer_text": "Step 1: If either side of the equation can be simplified, do that first. On the left side, you can add like terms.\n\n$$\n\\begin{align}\n2x+x-10&=2 \\\\\n3x-10&=2\n\\end{align}\n$$\n\nStep 2: If there is a constant term on the same side as the variable, add its additive inverse. Remember to do this on both sides of the equation.\n\n$$\n\\begin{align}\n2x+x-10&=2 \\\\\n3x-10\\; \\color{red}{+\\;10}&=2\\; \\color{red}{+\\;10} \\\\\n3x&=12\n\\end{align}\n$$\n\nStep 3: If the variable has a coefficient, apply the multiplicative inverse of the coefficient. Remember to do this on both sides of the equation.\n\nRemember, multiplication and division are inverse operations. For example, $\\frac{4}{1}\\times \\frac{1}{4} = \\frac{4}{4}=1$.\n\n$$\n\\begin{align}\n2x+x-10&=2 \\\\\n3x-10\\; \\color{red}{+\\;10}&=2\\; \\color{red}{+\\;10} \\\\\n3x&=12 \\\\\n\\frac{3x}{\\color{red}{3}}&=\\frac{12}{\\color{red}{3}} \\\\\n\\therefore x&=4\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b019",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Checking the solution"
    },
    "content_text": "We always check the solution we worked out to make sure that it makes the equation true. An equation is true if the left-hand side is equal to (has the same value as) the right-hand side.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b020",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Worked example 11.5: Checking the solution"
    },
    "content_text": "",
    "prompt_text": "In the previous worked example, the solution of the equation:\n\n$$\n2x+x-10=2\n$$\n\nwas found to be:\n\n$$\nx=4\n$$\n\nCheck this solution.",
    "answer_text": "Step 1: Replace the variable on the left-hand side (LHS) of the original equation with the solution. Work out the value of the left-hand side.\n\n$$\n\\begin{align}\n\\text{LHS}&=2x+x-10 \\\\\n&=2(4)+4-10 \\\\\n&=8+4-10 \\\\\n&=2\n\\end{align}\n$$\n\nRemember that $2(4)$ means $2\\times 4$.\n\nStep 2: Repeat Step 1 for the right-hand side (RHS) of the original equation.\n\n$$\n\\text{RHS}=2\n$$\n\nStep 3: Compare your answers from Steps 1 and 2. If they are the same, your solution is correct. If not, you made a mistake somewhere. Solve the equation again.\n\n$\\text{LHS}=\\text{RHS}$\n\nThe solution is correct.",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b021",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.3: Solve equations and check the solutions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.3: Solve equations and check the solutions\n\nSolve each of the following equations and check the solutions.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b021-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.3: Solve equations and check the solutions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.3: Solve equations and check the solutions\n\nSolve each of the following equations and check the solutions.\n\n1. $$\n11x=33\n$$",
    "answer_text": "$$\n\\begin{align}\n\\frac{11x}{11}&=\\frac{33}{11} \\\\\n\\therefore x&=3\n\\end{align}\n$$\n\nChecking:\n\n$$\n\\begin{align}\n11(3)&=33 \\\\\n33&=33 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b021-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.3: Solve equations and check the solutions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.3: Solve equations and check the solutions\n\nSolve each of the following equations and check the solutions.\n\n2. $$\n18+p=6\n$$",
    "answer_text": "$$\n\\begin{align}\n18-18+p&=6-18 \\\\\n\\therefore p&=-12 \\\\\n\\end{align}\n$$\n\nChecking:\n\n$$\n\\begin{align}\n18+(-12)&=6 \\\\\n6&=6 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b021-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.3: Solve equations and check the solutions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.3: Solve equations and check the solutions\n\nSolve each of the following equations and check the solutions.\n\n3. $$\n\\frac{1}{4}y=5\n$$",
    "answer_text": "$$\n\\begin{align}\n\\frac{4}{1}\\times \\frac{1}{4}y&=\\frac{4}{1}\\times5 \\\\\ny&=\\frac{4\\times5}{1} \\\\\n\\therefore y&=20\n\\end{align}\n$$\n\nChecking:\n\n$$\n\\begin{align}\n\\frac{1}{4}(20)&=5 \\\\\n\\frac{1\\times 20}{4}&=5 \\\\\n5&=5 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b021-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.3: Solve equations and check the solutions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.3: Solve equations and check the solutions\n\nSolve each of the following equations and check the solutions.\n\n4. $$\n4x+5=17\n$$",
    "answer_text": "$$\n\\begin{align}\n4x+5-5&=17-5 \\\\\n4x&=12 \\\\\n\\frac{4x}{4}&=\\frac{12}{4} \\\\\n\\therefore x&=3\n\\end{align}\n$$\n\nChecking:\n\n$$\n\\begin{align}\n4(3)+5&=17 \\\\\n12+5&=17 \\\\\n17&=17 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b021-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.3: Solve equations and check the solutions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.3: Solve equations and check the solutions\n\nSolve each of the following equations and check the solutions.\n\n5. $$\n10+5a=40\n$$",
    "answer_text": "$$\n\\begin{align}\n10-10+5a&=40-10 \\\\\n5a&=30 \\\\\n\\frac{5a}{5}&=\\frac{30}{5} \\\\\n\\therefore a&=6\n\\end{align}\n$$\n\nChecking:\n\n$$\n\\begin{align}\n10+5(6)&=40 \\\\\n10+30&=40 \\\\\n40&=40 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b021-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.3: Solve equations and check the solutions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.3: Solve equations and check the solutions\n\nSolve each of the following equations and check the solutions.\n\n6. $$\n13=2x-3\n$$",
    "answer_text": "$$\n\\begin{align}\n13+3&=2x-3+3 \\\\\n16&=2x \\\\\n\\frac{16}{2}&=\\frac{2x}{2} \\\\\n\\therefore 8&=x \\\\\n\\therefore x&=8\n\\end{align}\n$$\n\n$8=x$ and $x=8$ mean exactly the same thing.\n\nChecking:\n\n$$\n\\begin{align}\n13&=2(8)-3 \\\\\n13&=16-3 \\\\\n13&=13 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b021-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.3: Solve equations and check the solutions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.3: Solve equations and check the solutions\n\nSolve each of the following equations and check the solutions.\n\n7. $$\n\\frac{1}{2}t+1=5\n$$",
    "answer_text": "$$\n\\begin{align}\n\\frac{1}{2}t+1-1&=5-1 \\\\\n\\frac{1}{2}t&=4 \\\\\n\\frac{2}{1}\\times \\frac{1}{2}t&=4\\times \\frac{2}{1} \\\\\n\\therefore t&=8\n\\end{align}\n$$\n\nChecking:\n\n$$\n\\begin{align}\n\\frac{1}{2}t+1&=5 \\\\\n\\frac{1}{2}(8)+1&=5 \\\\\n\\frac{1 \\times 8}{2}+1&=5 \\\\\n4+1&=5 \\\\\n5&=5 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b021-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.3: Solve equations and check the solutions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.3: Solve equations and check the solutions\n\nSolve each of the following equations and check the solutions.\n\n8. $$\n36+\\frac{3}{4}y=44\n$$",
    "answer_text": "$$\n\\begin{align}\n36-36+\\frac{3}{4}y&=44-36 \\\\\n\\frac{3}{4}y&=8 \\\\\n\\frac{4}{3}\\times \\frac{3}{4}y&=8\\times \\frac{4}{3} \\\\\ny&=\\frac{8\\times4}{3} \\\\\n\\therefore y&=\\frac{32}{3} \\\\\n\\end{align}\n$$\n\nChecking:\n\n$$\n\\begin{align}\n36+\\frac{3}{4} \\left(\\frac{32}{3}\\right) &=44 \\\\\n36+\\frac{3\\times 32}{4 \\times3}&=44 \\\\\n36+\\frac{3\\times 32}{3 \\times4}&=44 \\\\\n36+\\frac{1\\times 8}{1 \\times1}&=44 \\\\\n36+8&=44 \\\\\n44&=44 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$\n\nGo back to Chapter 6 to revise how to multiply and divide fractions.",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b021-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.3: Solve equations and check the solutions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.3: Solve equations and check the solutions\n\nSolve each of the following equations and check the solutions.\n\n9. $$\n1-2x+11x=19\n$$",
    "answer_text": "$$\n\\begin{align}\n1+9x&=19 \\\\\n1-1+9x&=19-1 \\\\\n9x&=18 \\\\\n\\frac{9x}{9}&=\\frac{18}{9} \\\\\n\\therefore x&=2 \\\\\n\\end{align}\n$$\n\nChecking:\n\n$$\n\\begin{align}\n1-2(2)+11(2)&=19 \\\\\n1-4+22&=19 \\\\\n23-4&=19 \\\\\n19&=19 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$\n\nRemember that you must always follow the correct order of operations: BODMAS (Brackets, Of, Division, Multiplication, Addition, Subtraction).",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b021-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.3: Solve equations and check the solutions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.3: Solve equations and check the solutions\n\nSolve each of the following equations and check the solutions.\n\n10. $$\n39=21+5q-4q+2q\n$$",
    "answer_text": "$$\n\\begin{align}\n39&=21+7q-4q \\\\\n39&=21+3q \\\\\n39-21&=21-21+3q \\\\\n18&=3q \\\\\n\\frac{18}{3}&=\\frac{3q}{3} \\\\\n6&=q \\\\\n\\therefore q&=6\n\\end{align}\n$$\n\nChecking:\n\n$$\n\\begin{align}\n39&=21+5(6)-4(6)+2(6) \\\\\n39&=21+30-24+12 \\\\\n39&=63-24 \\\\\n39&=39 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b022",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Equations with variables on both sides of the equals sign"
    },
    "content_text": "Consider the following equation:\n\n$$\n18-5x=4x\n$$\n\nTo solve an equation, we must isolate the variable. We must get the equation in the form:\n\n$$\nx=\\text{value}\n$$\n\nIn all the equations we have solved so far, the terms with variables were on one side of the equation only. The equation above has a term with a variable on each side of the equation. We need to work with the terms until there is a variable only on the left-hand side or the right-hand side of the equation. There are two ways to do this, as shown in the following worked example.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b023",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Worked example 11.6: Solving an equation with variables on both sides"
    },
    "content_text": "",
    "prompt_text": "Solve the following equation:\n\n$$\n18-5x=4x\n$$",
    "answer_text": "Option 1: Use the additive inverse of a term with a variable to add or subtract it from both sides. We will start on the left-hand side.\n\n$$\n\\begin{align}\n18-5x\\; \\color{red}{+\\;5x}&=4x \\; \\color{red}{+\\;5x} \\\\\n18 &= 9x \\\\\n\\frac{18}{9}&=\\frac{9x}{9} \\\\\n2&=x \\\\\n\\therefore x&=2\n\\end{align}\n$$\n\nOption 2: We will also use the additive inverse, but starting on the right-hand side.\n\n$$\n\\begin{align}\n18-5x\\; \\color{red}{-\\;4x}&=4x \\; \\color{red}{-\\;4x} \\\\\n18-9x &= 0 \\\\\n18-9x\\; \\color{green}{+\\;9x}&=0+ \\color{green}{9x} \\\\\n18&=9x \\\\\n\\frac{18}{9}&=\\frac{9x}{9} \\\\\n2&=x \\\\\n\\therefore x&=2\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b024",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.4: Solve equations with variables on both sides"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.4: Solve equations with variables on both sides\n\nSolve each of the following equations and check the solutions.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b024-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.4: Solve equations with variables on both sides"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.4: Solve equations with variables on both sides\n\nSolve each of the following equations and check the solutions.\n\n1. $$\n2x+9=5x\n$$",
    "answer_text": "$$\n\\begin{align}\n2x-2x+9&=5x-2x \\\\\n9&=3x \\\\\n\\frac{9}{3}&=\\frac{3x}{3} \\\\\n3&=x \\\\\n\\therefore x&=3\n\\end{align}\n$$\n\nChecking:\n\n$$\n\\begin{align}\n2(3)+9&=5(3) \\\\\n6+9&=15 \\\\\n15&=15 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b024-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.4: Solve equations with variables on both sides"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.4: Solve equations with variables on both sides\n\nSolve each of the following equations and check the solutions.\n\n2. $$\n8+4p=6p-12\n$$",
    "answer_text": "$$\n\\begin{align}\n8+4p-4p&=6p-4p-12 \\\\\n8&=2p-12 \\\\\n8+12&=2p-12+12 \\\\\n20&=2p \\\\\n\\frac{20}{2}&=\\frac{2p}{2} \\\\\n10&=p \\\\\n\\therefore p&=10\n\\end{align}\n$$\n\nChecking:\n\n$$\n\\begin{align}\n8+4(10)&=6(10)-12 \\\\\n8+40&=60-12 \\\\\n48&=48 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b024-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.4: Solve equations with variables on both sides"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.4: Solve equations with variables on both sides\n\nSolve each of the following equations and check the solutions.\n\n3. $$\n5a+7+a=4a+13\n$$",
    "answer_text": "$$\n\\begin{align}\n6a+7&=4a+13 \\\\\n6a-4a+7&=4a-4a+13 \\\\\n2a+7&=13 \\\\\n2a+7-7&=13-7 \\\\\n2a&=6 \\\\\n\\frac{2a}{2}&=\\frac{6}{2} \\\\\n\\therefore a&=3\n\\end{align}\n$$\n\nChecking:\n\n$$\n\\begin{align}\n5(3)+7+3&=4(3)+13 \\\\\n15+7+3&=12+13 \\\\\n25&=25 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b024-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.4: Solve equations with variables on both sides"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.4: Solve equations with variables on both sides\n\nSolve each of the following equations and check the solutions.\n\n4. $$\n6-3y=-2-2y\n$$",
    "answer_text": "$$\n\\begin{align}\n6-3y+2y&=-2-2y+2y \\\\\n6-y&=-2 \\\\\n6-y+y&=-2+y \\\\\n6&=-2+y \\\\\n6+2&=-2+2+y \\\\\n8&=y \\\\\n\\therefore y&=8\n\\end{align}\n$$\n\nIn your answer you need to get to a positive variable, $+y$, which is the same as $y$. So if you have a negative variable, as you do in the line $6-y=-2$, simply add the positive of the variable on both sides of the equation, as shown in the line after that.\n\nChecking:\n\n$$\n\\begin{align}\n6-3(8)&=-2-2(8) \\\\\n6-24&=-2-16 \\\\\n-18&=-18 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b024-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.4: Solve equations with variables on both sides"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.4: Solve equations with variables on both sides\n\nSolve each of the following equations and check the solutions.\n\n5. $$\n10-6t+5=5t-30+t+3t\n$$",
    "answer_text": "$$\n\\begin{align}\n15-6t&=9t-30 \\\\\n15-6t-9t&=9t-9t-30 \\\\\n15-15t&=-30 \\\\\n15-15t+15t&=-30+15t \\\\\n15&=-30+15t \\\\\n15+30&=-30+30+15t \\\\\n45&=15t \\\\\n\\frac{45}{15}&=\\frac{15t}{15} \\\\\n3&=t\\\\\n\\therefore t&=3\n\\end{align}\n$$\n\nIf you have a variable that has a negative coefficient, such as $-15t$, simply add the positive of the term on both sides of the equation, so that you are working with a variable that has a positive coefficient.\n\nChecking:\n\n$$\n\\begin{align}\n10-6(3)+5&=5(3)-30+3+3(3) \\\\\n10-18+5&=15-30+3+9 \\\\\n15-18&=27-30 \\\\\n-3&=-3 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$\n\nRemember to follow the correct order of operations: BODMAS (Brackets, Of, Division, Multiplication, Addition, Subtraction).",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
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
  "subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations",
  "subtopic_title": "Solution of simple equations",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-simple-equations-solution-of-simple-equations-po01",
        "source_performance_objective_index": 1,
        "text": "Solve simple equations and cross-check the answers"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "solution-of-simple-equations-ao-solve-simple-equations",
          "text": "Solve simple equations."
        },
        {
          "atomic_objective_id": "solution-of-simple-equations-ao-cross-check-answers",
          "text": "Cross-check the answers to simple equations."
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
    "record_id": "ch11-b012",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "The solution of an equation"
    },
    "content_text": "You have learnt how to find the values that make open sentences true. Look at the following algebraic equation:\n\n$$\n3+x=5\n$$\n\nIt is easy to see that the only value for $x$ that will make this equation true is 2. This is because $3+2=5$. We say the number 2 is the **solution** of the equation and we write it as:\n\n$$\nx=2\n$$\n\nWhen we find the solution of an equation, we say we **solve** the equation.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b013",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "The solution of an equation"
    },
    "content_text": "**solution** The solution of an equation is the value of the variable that makes the equation true.\n\n**solve** When we solve an equation, we find the value of the variable that makes the equation true.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b014",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "The solution of an equation"
    },
    "content_text": "To solve an equation, we must isolate the variable. If $x$ is the variable, we must get the equation in the form:\n\n$$\nx=\\text{value}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b015",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Representing an equation as a balancing scale"
    },
    "content_text": "To help us solve an algebraic equation, we can show it as a balancing scale. The picture shows what a scale looks like. This scale is balanced, because nothing has been placed on it.\n\nIf we place a mass piece on one of the pans, the scale becomes unbalanced.\n\nWe can balance the scale again by placing an identical mass piece on the other pan.\n\nAs long as identical mass pieces are placed on both pans, the scale will remain in balance.\n\nIn an equation, the equals sign shows that two expressions (or an expression and a value) are equal to each other. We can think of each side of the equation as one of the pans of a scale. As long as we do exactly the same on each side of the equation, the equation will remain true.\n\nConsider the following algebraic equation:\n\n$$\nx-5=14\n$$\n\nWe can represent it on the pans of a scale as follows.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b016",
    "record_type": "hint",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Representing an equation as a balancing scale"
    },
    "content_text": "Go back to Chapter 9 if you need to revise inverse operations. Remember that addition and subtraction are inverse operations, and multiplication and division are inverse operations.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b017",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Representing an equation as a balancing scale"
    },
    "content_text": "Whatever we add to the one pan, we must also add to the other pan. The scale now shows:\n\nRemember that $-5+5=0$. Therefore, if we simplify both sides, we get the solution of the equation:\n\n$$\nx=19\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b018",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Worked example 11.4: Finding the solution of an equation"
    },
    "content_text": "",
    "prompt_text": "Solve the following equation:\n\n$$\n2x+x-10=2\n$$",
    "answer_text": "Step 1: If either side of the equation can be simplified, do that first. On the left side, you can add like terms.\n\n$$\n\\begin{align}\n2x+x-10&=2 \\\\\n3x-10&=2\n\\end{align}\n$$\n\nStep 2: If there is a constant term on the same side as the variable, add its additive inverse. Remember to do this on both sides of the equation.\n\n$$\n\\begin{align}\n2x+x-10&=2 \\\\\n3x-10\\; \\color{red}{+\\;10}&=2\\; \\color{red}{+\\;10} \\\\\n3x&=12\n\\end{align}\n$$\n\nStep 3: If the variable has a coefficient, apply the multiplicative inverse of the coefficient. Remember to do this on both sides of the equation.\n\nRemember, multiplication and division are inverse operations. For example, $\\frac{4}{1}\\times \\frac{1}{4} = \\frac{4}{4}=1$.\n\n$$\n\\begin{align}\n2x+x-10&=2 \\\\\n3x-10\\; \\color{red}{+\\;10}&=2\\; \\color{red}{+\\;10} \\\\\n3x&=12 \\\\\n\\frac{3x}{\\color{red}{3}}&=\\frac{12}{\\color{red}{3}} \\\\\n\\therefore x&=4\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b019",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Checking the solution"
    },
    "content_text": "We always check the solution we worked out to make sure that it makes the equation true. An equation is true if the left-hand side is equal to (has the same value as) the right-hand side.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b020",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Worked example 11.5: Checking the solution"
    },
    "content_text": "",
    "prompt_text": "In the previous worked example, the solution of the equation:\n\n$$\n2x+x-10=2\n$$\n\nwas found to be:\n\n$$\nx=4\n$$\n\nCheck this solution.",
    "answer_text": "Step 1: Replace the variable on the left-hand side (LHS) of the original equation with the solution. Work out the value of the left-hand side.\n\n$$\n\\begin{align}\n\\text{LHS}&=2x+x-10 \\\\\n&=2(4)+4-10 \\\\\n&=8+4-10 \\\\\n&=2\n\\end{align}\n$$\n\nRemember that $2(4)$ means $2\\times 4$.\n\nStep 2: Repeat Step 1 for the right-hand side (RHS) of the original equation.\n\n$$\n\\text{RHS}=2\n$$\n\nStep 3: Compare your answers from Steps 1 and 2. If they are the same, your solution is correct. If not, you made a mistake somewhere. Solve the equation again.\n\n$\\text{LHS}=\\text{RHS}$\n\nThe solution is correct.",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b021",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.3: Solve equations and check the solutions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.3: Solve equations and check the solutions\n\nSolve each of the following equations and check the solutions.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b021-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.3: Solve equations and check the solutions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.3: Solve equations and check the solutions\n\nSolve each of the following equations and check the solutions.\n\n1. $$\n11x=33\n$$",
    "answer_text": "$$\n\\begin{align}\n\\frac{11x}{11}&=\\frac{33}{11} \\\\\n\\therefore x&=3\n\\end{align}\n$$\n\nChecking:\n\n$$\n\\begin{align}\n11(3)&=33 \\\\\n33&=33 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b021-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.3: Solve equations and check the solutions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.3: Solve equations and check the solutions\n\nSolve each of the following equations and check the solutions.\n\n2. $$\n18+p=6\n$$",
    "answer_text": "$$\n\\begin{align}\n18-18+p&=6-18 \\\\\n\\therefore p&=-12 \\\\\n\\end{align}\n$$\n\nChecking:\n\n$$\n\\begin{align}\n18+(-12)&=6 \\\\\n6&=6 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b021-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.3: Solve equations and check the solutions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.3: Solve equations and check the solutions\n\nSolve each of the following equations and check the solutions.\n\n3. $$\n\\frac{1}{4}y=5\n$$",
    "answer_text": "$$\n\\begin{align}\n\\frac{4}{1}\\times \\frac{1}{4}y&=\\frac{4}{1}\\times5 \\\\\ny&=\\frac{4\\times5}{1} \\\\\n\\therefore y&=20\n\\end{align}\n$$\n\nChecking:\n\n$$\n\\begin{align}\n\\frac{1}{4}(20)&=5 \\\\\n\\frac{1\\times 20}{4}&=5 \\\\\n5&=5 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b021-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.3: Solve equations and check the solutions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.3: Solve equations and check the solutions\n\nSolve each of the following equations and check the solutions.\n\n4. $$\n4x+5=17\n$$",
    "answer_text": "$$\n\\begin{align}\n4x+5-5&=17-5 \\\\\n4x&=12 \\\\\n\\frac{4x}{4}&=\\frac{12}{4} \\\\\n\\therefore x&=3\n\\end{align}\n$$\n\nChecking:\n\n$$\n\\begin{align}\n4(3)+5&=17 \\\\\n12+5&=17 \\\\\n17&=17 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b021-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.3: Solve equations and check the solutions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.3: Solve equations and check the solutions\n\nSolve each of the following equations and check the solutions.\n\n5. $$\n10+5a=40\n$$",
    "answer_text": "$$\n\\begin{align}\n10-10+5a&=40-10 \\\\\n5a&=30 \\\\\n\\frac{5a}{5}&=\\frac{30}{5} \\\\\n\\therefore a&=6\n\\end{align}\n$$\n\nChecking:\n\n$$\n\\begin{align}\n10+5(6)&=40 \\\\\n10+30&=40 \\\\\n40&=40 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b021-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.3: Solve equations and check the solutions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.3: Solve equations and check the solutions\n\nSolve each of the following equations and check the solutions.\n\n6. $$\n13=2x-3\n$$",
    "answer_text": "$$\n\\begin{align}\n13+3&=2x-3+3 \\\\\n16&=2x \\\\\n\\frac{16}{2}&=\\frac{2x}{2} \\\\\n\\therefore 8&=x \\\\\n\\therefore x&=8\n\\end{align}\n$$\n\n$8=x$ and $x=8$ mean exactly the same thing.\n\nChecking:\n\n$$\n\\begin{align}\n13&=2(8)-3 \\\\\n13&=16-3 \\\\\n13&=13 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b021-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.3: Solve equations and check the solutions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.3: Solve equations and check the solutions\n\nSolve each of the following equations and check the solutions.\n\n7. $$\n\\frac{1}{2}t+1=5\n$$",
    "answer_text": "$$\n\\begin{align}\n\\frac{1}{2}t+1-1&=5-1 \\\\\n\\frac{1}{2}t&=4 \\\\\n\\frac{2}{1}\\times \\frac{1}{2}t&=4\\times \\frac{2}{1} \\\\\n\\therefore t&=8\n\\end{align}\n$$\n\nChecking:\n\n$$\n\\begin{align}\n\\frac{1}{2}t+1&=5 \\\\\n\\frac{1}{2}(8)+1&=5 \\\\\n\\frac{1 \\times 8}{2}+1&=5 \\\\\n4+1&=5 \\\\\n5&=5 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b021-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.3: Solve equations and check the solutions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.3: Solve equations and check the solutions\n\nSolve each of the following equations and check the solutions.\n\n8. $$\n36+\\frac{3}{4}y=44\n$$",
    "answer_text": "$$\n\\begin{align}\n36-36+\\frac{3}{4}y&=44-36 \\\\\n\\frac{3}{4}y&=8 \\\\\n\\frac{4}{3}\\times \\frac{3}{4}y&=8\\times \\frac{4}{3} \\\\\ny&=\\frac{8\\times4}{3} \\\\\n\\therefore y&=\\frac{32}{3} \\\\\n\\end{align}\n$$\n\nChecking:\n\n$$\n\\begin{align}\n36+\\frac{3}{4} \\left(\\frac{32}{3}\\right) &=44 \\\\\n36+\\frac{3\\times 32}{4 \\times3}&=44 \\\\\n36+\\frac{3\\times 32}{3 \\times4}&=44 \\\\\n36+\\frac{1\\times 8}{1 \\times1}&=44 \\\\\n36+8&=44 \\\\\n44&=44 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$\n\nGo back to Chapter 6 to revise how to multiply and divide fractions.",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b021-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.3: Solve equations and check the solutions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.3: Solve equations and check the solutions\n\nSolve each of the following equations and check the solutions.\n\n9. $$\n1-2x+11x=19\n$$",
    "answer_text": "$$\n\\begin{align}\n1+9x&=19 \\\\\n1-1+9x&=19-1 \\\\\n9x&=18 \\\\\n\\frac{9x}{9}&=\\frac{18}{9} \\\\\n\\therefore x&=2 \\\\\n\\end{align}\n$$\n\nChecking:\n\n$$\n\\begin{align}\n1-2(2)+11(2)&=19 \\\\\n1-4+22&=19 \\\\\n23-4&=19 \\\\\n19&=19 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$\n\nRemember that you must always follow the correct order of operations: BODMAS (Brackets, Of, Division, Multiplication, Addition, Subtraction).",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b021-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.3: Solve equations and check the solutions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.3: Solve equations and check the solutions\n\nSolve each of the following equations and check the solutions.\n\n10. $$\n39=21+5q-4q+2q\n$$",
    "answer_text": "$$\n\\begin{align}\n39&=21+7q-4q \\\\\n39&=21+3q \\\\\n39-21&=21-21+3q \\\\\n18&=3q \\\\\n\\frac{18}{3}&=\\frac{3q}{3} \\\\\n6&=q \\\\\n\\therefore q&=6\n\\end{align}\n$$\n\nChecking:\n\n$$\n\\begin{align}\n39&=21+5(6)-4(6)+2(6) \\\\\n39&=21+30-24+12 \\\\\n39&=63-24 \\\\\n39&=39 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b022",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Equations with variables on both sides of the equals sign"
    },
    "content_text": "Consider the following equation:\n\n$$\n18-5x=4x\n$$\n\nTo solve an equation, we must isolate the variable. We must get the equation in the form:\n\n$$\nx=\\text{value}\n$$\n\nIn all the equations we have solved so far, the terms with variables were on one side of the equation only. The equation above has a term with a variable on each side of the equation. We need to work with the terms until there is a variable only on the left-hand side or the right-hand side of the equation. There are two ways to do this, as shown in the following worked example.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b023",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Worked example 11.6: Solving an equation with variables on both sides"
    },
    "content_text": "",
    "prompt_text": "Solve the following equation:\n\n$$\n18-5x=4x\n$$",
    "answer_text": "Option 1: Use the additive inverse of a term with a variable to add or subtract it from both sides. We will start on the left-hand side.\n\n$$\n\\begin{align}\n18-5x\\; \\color{red}{+\\;5x}&=4x \\; \\color{red}{+\\;5x} \\\\\n18 &= 9x \\\\\n\\frac{18}{9}&=\\frac{9x}{9} \\\\\n2&=x \\\\\n\\therefore x&=2\n\\end{align}\n$$\n\nOption 2: We will also use the additive inverse, but starting on the right-hand side.\n\n$$\n\\begin{align}\n18-5x\\; \\color{red}{-\\;4x}&=4x \\; \\color{red}{-\\;4x} \\\\\n18-9x &= 0 \\\\\n18-9x\\; \\color{green}{+\\;9x}&=0+ \\color{green}{9x} \\\\\n18&=9x \\\\\n\\frac{18}{9}&=\\frac{9x}{9} \\\\\n2&=x \\\\\n\\therefore x&=2\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b024",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.4: Solve equations with variables on both sides"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.4: Solve equations with variables on both sides\n\nSolve each of the following equations and check the solutions.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b024-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.4: Solve equations with variables on both sides"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.4: Solve equations with variables on both sides\n\nSolve each of the following equations and check the solutions.\n\n1. $$\n2x+9=5x\n$$",
    "answer_text": "$$\n\\begin{align}\n2x-2x+9&=5x-2x \\\\\n9&=3x \\\\\n\\frac{9}{3}&=\\frac{3x}{3} \\\\\n3&=x \\\\\n\\therefore x&=3\n\\end{align}\n$$\n\nChecking:\n\n$$\n\\begin{align}\n2(3)+9&=5(3) \\\\\n6+9&=15 \\\\\n15&=15 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b024-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.4: Solve equations with variables on both sides"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.4: Solve equations with variables on both sides\n\nSolve each of the following equations and check the solutions.\n\n2. $$\n8+4p=6p-12\n$$",
    "answer_text": "$$\n\\begin{align}\n8+4p-4p&=6p-4p-12 \\\\\n8&=2p-12 \\\\\n8+12&=2p-12+12 \\\\\n20&=2p \\\\\n\\frac{20}{2}&=\\frac{2p}{2} \\\\\n10&=p \\\\\n\\therefore p&=10\n\\end{align}\n$$\n\nChecking:\n\n$$\n\\begin{align}\n8+4(10)&=6(10)-12 \\\\\n8+40&=60-12 \\\\\n48&=48 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b024-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.4: Solve equations with variables on both sides"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.4: Solve equations with variables on both sides\n\nSolve each of the following equations and check the solutions.\n\n3. $$\n5a+7+a=4a+13\n$$",
    "answer_text": "$$\n\\begin{align}\n6a+7&=4a+13 \\\\\n6a-4a+7&=4a-4a+13 \\\\\n2a+7&=13 \\\\\n2a+7-7&=13-7 \\\\\n2a&=6 \\\\\n\\frac{2a}{2}&=\\frac{6}{2} \\\\\n\\therefore a&=3\n\\end{align}\n$$\n\nChecking:\n\n$$\n\\begin{align}\n5(3)+7+3&=4(3)+13 \\\\\n15+7+3&=12+13 \\\\\n25&=25 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b024-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.4: Solve equations with variables on both sides"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.4: Solve equations with variables on both sides\n\nSolve each of the following equations and check the solutions.\n\n4. $$\n6-3y=-2-2y\n$$",
    "answer_text": "$$\n\\begin{align}\n6-3y+2y&=-2-2y+2y \\\\\n6-y&=-2 \\\\\n6-y+y&=-2+y \\\\\n6&=-2+y \\\\\n6+2&=-2+2+y \\\\\n8&=y \\\\\n\\therefore y&=8\n\\end{align}\n$$\n\nIn your answer you need to get to a positive variable, $+y$, which is the same as $y$. So if you have a negative variable, as you do in the line $6-y=-2$, simply add the positive of the variable on both sides of the equation, as shown in the line after that.\n\nChecking:\n\n$$\n\\begin{align}\n6-3(8)&=-2-2(8) \\\\\n6-24&=-2-16 \\\\\n-18&=-18 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
  },
  {
    "record_id": "ch11-b024-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 11: Simple equations",
      "h2": "11.2 Solving equations",
      "h3": "Exercise 11.4: Solve equations with variables on both sides"
    },
    "content_text": "",
    "prompt_text": "### Exercise 11.4: Solve equations with variables on both sides\n\nSolve each of the following equations and check the solutions.\n\n5. $$\n10-6t+5=5t-30+t+3t\n$$",
    "answer_text": "$$\n\\begin{align}\n15-6t&=9t-30 \\\\\n15-6t-9t&=9t-9t-30 \\\\\n15-15t&=-30 \\\\\n15-15t+15t&=-30+15t \\\\\n15&=-30+15t \\\\\n15+30&=-30+30+15t \\\\\n45&=15t \\\\\n\\frac{45}{15}&=\\frac{15t}{15} \\\\\n3&=t\\\\\n\\therefore t&=3\n\\end{align}\n$$\n\nIf you have a variable that has a negative coefficient, such as $-15t$, simply add the positive of the term on both sides of the equation, so that you are working with a variable that has a positive coefficient.\n\nChecking:\n\n$$\n\\begin{align}\n10-6(3)+5&=5(3)-30+3+3(3) \\\\\n10-18+5&=15-30+3+9 \\\\\n15-18&=27-30 \\\\\n-3&=-3 \\\\\n\\therefore \\text{LHS}&=\\text{RHS}\n\\end{align}\n$$\n\nRemember to follow the correct order of operations: BODMAS (Brackets, Of, Division, Multiplication, Addition, Subtraction).",
    "primary_subtopic_id": "jss1-math-simple-equations-solution-of-simple-equations"
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
