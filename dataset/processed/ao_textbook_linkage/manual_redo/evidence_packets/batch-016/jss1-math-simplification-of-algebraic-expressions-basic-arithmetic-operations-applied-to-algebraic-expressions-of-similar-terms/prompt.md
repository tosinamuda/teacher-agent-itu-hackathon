# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-3",
  "topic_key": "jss1-math-simplification-of-algebraic-expressions",
  "topic": "Simplification of Algebraic Expressions",
  "subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms",
  "subtopic_title": "Basic arithmetic operations applied to algebraic expressions of similar terms",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms-po01",
        "source_performance_objective_index": 1,
        "text": "Perform basic arithmetic operations on expressions of similar terms"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "basic-arithmetic-operations-on-similar-terms-ao-perform-operations",
          "text": "Perform basic arithmetic operations on expressions of similar terms."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch10-b009",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": null
    },
    "content_text": "When you learnt to add or subtract objects you learnt that, for example:\n\n- 1 apple + 1 apple + 1 apple + 1 apple can be written as 4 apples\n\nWhen you started working with multiplication you learnt that, for example:\n\n- 1 apple + 1 apple + 1 apple + 1 apple can be written as 4 $\\times$ (1 apple) = 4 apples\n- 2 apples + 2 apples + 2 apples can be written as 3 $\\times$ (2 apples) = 6 apples\n- 9 + 9 + 9 + 9 can also be written as 4 $\\times$ 9\n- 3 + 3 + 3 + 3 + 3 + 3 + 3 can also be written as 7 $\\times$ 3\n\nThe same principles apply in algebra. But remember that in algebra, we use a letter or variable to replace a number. For example:\n\n$$a + a + a + a = 4 \\times a$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b010",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": null
    },
    "content_text": "In algebra, we normally do not write the multiplication sign between a number and a variable. For example, we write $4 \\times a$ as $4a$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b011",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": null
    },
    "content_text": "Here are a few more examples:\n\n$$x + x + x + x + x + x + x = 7 \\times x = 7x$$\n$$p + p + p = 3 \\times p = 3p$$\n$$y + y = 2 \\times y = 2y$$\n$$m + m + m + m + m = 5 \\times m = 5m$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b012",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Worked example 10.2: Writing algebraic expressions"
    },
    "content_text": "",
    "prompt_text": "Write the following expression using a simpler notation:\n\n$$\ny + y + y + y + y\n$$",
    "answer_text": "Step 1: Check what operations are being used.\n\nIn this case, only addition is used.\n\nStep 2: Count the number of $y$s.\n\nThere are 5 $y$s.\n\nStep 3: Write the algebraic expression in a simpler notation.\n\n$$\n5y\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b013",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.2: Simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.2: Simplify expressions\n\nWrite the following expressions in a simpler notation:",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b013-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.2: Simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.2: Simplify expressions\n\n1. $$x+x$$",
    "answer_text": "$$2x$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b013-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.2: Simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.2: Simplify expressions\n\n2. $$3+3+3+3+3+3+3$$",
    "answer_text": "$7 \\times 3$ or 21",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b013-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.2: Simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.2: Simplify expressions\n\n3. $$8\\times p$$",
    "answer_text": "$$8p$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b013-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.2: Simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.2: Simplify expressions\n\n4. $$3 \\times 7 \\times y$$",
    "answer_text": "$$21y$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b013-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.2: Simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.2: Simplify expressions\n\n5. $$x + x + x + x + x$$",
    "answer_text": "$$5x$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b013-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.2: Simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.2: Simplify expressions\n\n6. $$2x + 2x + 2x$$",
    "answer_text": "$3 \\times 2x$ or $6x$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b013-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.2: Simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.2: Simplify expressions\n\n7. $$k + k + k + k + k + k$$",
    "answer_text": "$$6k$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b013-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.2: Simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.2: Simplify expressions\n\n8. $$5 \\times m$$",
    "answer_text": "$$5m$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b013-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.2: Simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.2: Simplify expressions\n\n9. $$5x + 5x + 5x + 5x$$",
    "answer_text": "$4 \\times 5x$ or $20x$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b013-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.2: Simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.2: Simplify expressions\n\n10. $$(-2) + (-2) + (-2)$$",
    "answer_text": "$3 \\times (-2)$ or $-6$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b019",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": null
    },
    "content_text": "We have seen that we can add $p + p + p$ to get $3p$.\n\nThese three terms are called **like terms** because they all contain the same variable, $p$.\n\nWe can also add $3x + 4x$. Because both terms have the variable $x$, we can combine the terms using the operation that is given, which in this case is addition. The correct answer is:\n\n$$\n\\begin{array}{l}\n{3x + 4x = 7x}\n\\end{array}\n$$\n\nWe can also subtract like terms. We can simplify the expression $10a - 2a$ using subtraction. The correct answer is:\n\n$$\n\\begin{array}{l}\n{10a - 2a = 8a}\n\\end{array}\n$$\n\nWhen we collect or combine the like terms in this way, we are giving an expression in its simplest form, which is called **simplifying an expression**.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-like-and-unlike-terms-in-algebraic-expressions"
  },
  {
    "record_id": "ch10-b020",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": null
    },
    "content_text": "**like terms** Like terms contain the same variable or variables.\n\n**simplify an expression** To simplify an expression is to give it in its simplest form. We do this by collecting (combining) like terms using addition or subtraction.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-like-and-unlike-terms-in-algebraic-expressions"
  },
  {
    "record_id": "ch10-b021",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": null
    },
    "content_text": "We can add or subtract any number of like terms.\n\nFor example:\n\n$$\n4x + 2x + 5x + 10x = 21x\n$$\n\n$$\n10x - 2x + 3x - x + 14x = 24x\n$$\n\nTerms that do not have the same variables are called **unlike terms**. If we find an expression with unlike terms, we cannot add or subtract these terms. For example: $3x + 3y$ contains two unlike terms. They have the same coefficient but not the same variable. This expression cannot be simplified further.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-like-and-unlike-terms-in-algebraic-expressions"
  },
  {
    "record_id": "ch10-b022",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": null
    },
    "content_text": "**unlike terms** Unlike terms contain different variables.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-like-and-unlike-terms-in-algebraic-expressions"
  },
  {
    "record_id": "ch10-b023",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": "Exercise 10.4: Add and subtract like terms"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.4: Add and subtract like terms\n\nSimplify the following expressions.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b023-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": "Exercise 10.4: Add and subtract like terms"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.4: Add and subtract like terms\n\n1. $2h + 3h$",
    "answer_text": "$$\n5h\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b023-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": "Exercise 10.4: Add and subtract like terms"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.4: Add and subtract like terms\n\n2. $18p - 16p$",
    "answer_text": "$$\n2p\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b023-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": "Exercise 10.4: Add and subtract like terms"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.4: Add and subtract like terms\n\n3. $9x - 10x$",
    "answer_text": "$-x$ or $-1x$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b023-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": "Exercise 10.4: Add and subtract like terms"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.4: Add and subtract like terms\n\n4. $13x +2y$",
    "answer_text": "$13x + 2y$\n\n(There are no like terms.)",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b023-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": "Exercise 10.4: Add and subtract like terms"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.4: Add and subtract like terms\n\n5. $-20b + b$",
    "answer_text": "$$\n-19b\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b023-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": "Exercise 10.4: Add and subtract like terms"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.4: Add and subtract like terms\n\n6. $28k - k + 13k$",
    "answer_text": "$$\n40k\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b023-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": "Exercise 10.4: Add and subtract like terms"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.4: Add and subtract like terms\n\n7. $28k - 28k$",
    "answer_text": "$$\n0\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b023-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": "Exercise 10.4: Add and subtract like terms"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.4: Add and subtract like terms\n\n8. $-7x + 7x - 12x + 24x$",
    "answer_text": "$$\n12x\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b023-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": "Exercise 10.4: Add and subtract like terms"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.4: Add and subtract like terms\n\n9. $11a + 11b$",
    "answer_text": "$11a + 11b$\n\n(There are no like terms.)",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b023-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": "Exercise 10.4: Add and subtract like terms"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.4: Add and subtract like terms\n\n10. $3x -2$",
    "answer_text": "$3x - 2$\n\n(There are no like terms.)",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
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
  "subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms",
  "subtopic_title": "Basic arithmetic operations applied to algebraic expressions of similar terms",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms-po01",
        "source_performance_objective_index": 1,
        "text": "Perform basic arithmetic operations on expressions of similar terms"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "basic-arithmetic-operations-on-similar-terms-ao-perform-operations",
          "text": "Perform basic arithmetic operations on expressions of similar terms."
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
    "record_id": "ch10-b009",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": null
    },
    "content_text": "When you learnt to add or subtract objects you learnt that, for example:\n\n- 1 apple + 1 apple + 1 apple + 1 apple can be written as 4 apples\n\nWhen you started working with multiplication you learnt that, for example:\n\n- 1 apple + 1 apple + 1 apple + 1 apple can be written as 4 $\\times$ (1 apple) = 4 apples\n- 2 apples + 2 apples + 2 apples can be written as 3 $\\times$ (2 apples) = 6 apples\n- 9 + 9 + 9 + 9 can also be written as 4 $\\times$ 9\n- 3 + 3 + 3 + 3 + 3 + 3 + 3 can also be written as 7 $\\times$ 3\n\nThe same principles apply in algebra. But remember that in algebra, we use a letter or variable to replace a number. For example:\n\n$$a + a + a + a = 4 \\times a$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b010",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": null
    },
    "content_text": "In algebra, we normally do not write the multiplication sign between a number and a variable. For example, we write $4 \\times a$ as $4a$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b011",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": null
    },
    "content_text": "Here are a few more examples:\n\n$$x + x + x + x + x + x + x = 7 \\times x = 7x$$\n$$p + p + p = 3 \\times p = 3p$$\n$$y + y = 2 \\times y = 2y$$\n$$m + m + m + m + m = 5 \\times m = 5m$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b012",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Worked example 10.2: Writing algebraic expressions"
    },
    "content_text": "",
    "prompt_text": "Write the following expression using a simpler notation:\n\n$$\ny + y + y + y + y\n$$",
    "answer_text": "Step 1: Check what operations are being used.\n\nIn this case, only addition is used.\n\nStep 2: Count the number of $y$s.\n\nThere are 5 $y$s.\n\nStep 3: Write the algebraic expression in a simpler notation.\n\n$$\n5y\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b013",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.2: Simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.2: Simplify expressions\n\nWrite the following expressions in a simpler notation:",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b013-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.2: Simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.2: Simplify expressions\n\n1. $$x+x$$",
    "answer_text": "$$2x$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b013-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.2: Simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.2: Simplify expressions\n\n2. $$3+3+3+3+3+3+3$$",
    "answer_text": "$7 \\times 3$ or 21",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b013-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.2: Simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.2: Simplify expressions\n\n3. $$8\\times p$$",
    "answer_text": "$$8p$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b013-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.2: Simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.2: Simplify expressions\n\n4. $$3 \\times 7 \\times y$$",
    "answer_text": "$$21y$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b013-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.2: Simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.2: Simplify expressions\n\n5. $$x + x + x + x + x$$",
    "answer_text": "$$5x$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b013-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.2: Simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.2: Simplify expressions\n\n6. $$2x + 2x + 2x$$",
    "answer_text": "$3 \\times 2x$ or $6x$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b013-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.2: Simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.2: Simplify expressions\n\n7. $$k + k + k + k + k + k$$",
    "answer_text": "$$6k$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b013-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.2: Simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.2: Simplify expressions\n\n8. $$5 \\times m$$",
    "answer_text": "$$5m$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b013-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.2: Simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.2: Simplify expressions\n\n9. $$5x + 5x + 5x + 5x$$",
    "answer_text": "$4 \\times 5x$ or $20x$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b013-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.2: Simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.2: Simplify expressions\n\n10. $$(-2) + (-2) + (-2)$$",
    "answer_text": "$3 \\times (-2)$ or $-6$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b019",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": null
    },
    "content_text": "We have seen that we can add $p + p + p$ to get $3p$.\n\nThese three terms are called **like terms** because they all contain the same variable, $p$.\n\nWe can also add $3x + 4x$. Because both terms have the variable $x$, we can combine the terms using the operation that is given, which in this case is addition. The correct answer is:\n\n$$\n\\begin{array}{l}\n{3x + 4x = 7x}\n\\end{array}\n$$\n\nWe can also subtract like terms. We can simplify the expression $10a - 2a$ using subtraction. The correct answer is:\n\n$$\n\\begin{array}{l}\n{10a - 2a = 8a}\n\\end{array}\n$$\n\nWhen we collect or combine the like terms in this way, we are giving an expression in its simplest form, which is called **simplifying an expression**.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-like-and-unlike-terms-in-algebraic-expressions"
  },
  {
    "record_id": "ch10-b020",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": null
    },
    "content_text": "**like terms** Like terms contain the same variable or variables.\n\n**simplify an expression** To simplify an expression is to give it in its simplest form. We do this by collecting (combining) like terms using addition or subtraction.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-like-and-unlike-terms-in-algebraic-expressions"
  },
  {
    "record_id": "ch10-b021",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": null
    },
    "content_text": "We can add or subtract any number of like terms.\n\nFor example:\n\n$$\n4x + 2x + 5x + 10x = 21x\n$$\n\n$$\n10x - 2x + 3x - x + 14x = 24x\n$$\n\nTerms that do not have the same variables are called **unlike terms**. If we find an expression with unlike terms, we cannot add or subtract these terms. For example: $3x + 3y$ contains two unlike terms. They have the same coefficient but not the same variable. This expression cannot be simplified further.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-like-and-unlike-terms-in-algebraic-expressions"
  },
  {
    "record_id": "ch10-b022",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": null
    },
    "content_text": "**unlike terms** Unlike terms contain different variables.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-like-and-unlike-terms-in-algebraic-expressions"
  },
  {
    "record_id": "ch10-b023",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": "Exercise 10.4: Add and subtract like terms"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.4: Add and subtract like terms\n\nSimplify the following expressions.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b023-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": "Exercise 10.4: Add and subtract like terms"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.4: Add and subtract like terms\n\n1. $2h + 3h$",
    "answer_text": "$$\n5h\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b023-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": "Exercise 10.4: Add and subtract like terms"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.4: Add and subtract like terms\n\n2. $18p - 16p$",
    "answer_text": "$$\n2p\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b023-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": "Exercise 10.4: Add and subtract like terms"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.4: Add and subtract like terms\n\n3. $9x - 10x$",
    "answer_text": "$-x$ or $-1x$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b023-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": "Exercise 10.4: Add and subtract like terms"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.4: Add and subtract like terms\n\n4. $13x +2y$",
    "answer_text": "$13x + 2y$\n\n(There are no like terms.)",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b023-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": "Exercise 10.4: Add and subtract like terms"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.4: Add and subtract like terms\n\n5. $-20b + b$",
    "answer_text": "$$\n-19b\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b023-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": "Exercise 10.4: Add and subtract like terms"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.4: Add and subtract like terms\n\n6. $28k - k + 13k$",
    "answer_text": "$$\n40k\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b023-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": "Exercise 10.4: Add and subtract like terms"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.4: Add and subtract like terms\n\n7. $28k - 28k$",
    "answer_text": "$$\n0\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b023-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": "Exercise 10.4: Add and subtract like terms"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.4: Add and subtract like terms\n\n8. $-7x + 7x - 12x + 24x$",
    "answer_text": "$$\n12x\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b023-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": "Exercise 10.4: Add and subtract like terms"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.4: Add and subtract like terms\n\n9. $11a + 11b$",
    "answer_text": "$11a + 11b$\n\n(There are no like terms.)",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
  },
  {
    "record_id": "ch10-b023-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.3 Adding and subtracting like terms",
      "h3": "Exercise 10.4: Add and subtract like terms"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.4: Add and subtract like terms\n\n10. $3x -2$",
    "answer_text": "$3x - 2$\n\n(There are no like terms.)",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms"
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
