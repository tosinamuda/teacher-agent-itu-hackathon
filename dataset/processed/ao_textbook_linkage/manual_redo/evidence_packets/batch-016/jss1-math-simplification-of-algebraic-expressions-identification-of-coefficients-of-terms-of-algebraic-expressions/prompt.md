# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-3",
  "topic_key": "jss1-math-simplification-of-algebraic-expressions",
  "topic": "Simplification of Algebraic Expressions",
  "subtopic_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions",
  "subtopic_title": "Identification of coefficients of terms of algebraic expressions",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions-po01",
        "source_performance_objective_index": 1,
        "text": "Identify the coefficient of a given algebraic term"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "identification-of-coefficients-ao-identify-coefficient",
          "text": "Identify the coefficient of a given algebraic term."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions-po02",
        "source_performance_objective_index": 2,
        "text": "Identify the positive and negative coefficients of a given algebraic term"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "identification-of-coefficients-ao-identify-positive-coefficient",
          "text": "Identify the positive coefficient of a given algebraic term."
        },
        {
          "atomic_objective_id": "identification-of-coefficients-ao-identify-negative-coefficient",
          "text": "Identify the negative coefficient of a given algebraic term."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch10-b014",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Constants and coefficients"
    },
    "content_text": "There are two other words you also need to know and understand when working with algebraic terms: constant and coefficient.\n\nThe following algebraic expression contains two terms:\n\n$$-4x + 5$$\n\n5 is called a **constant** term as the value will always be 5 and it will not vary. The value of the $-4x$ term will vary depending on the value of the variable $x$. In the $-4x$ term, the $x$ is called the variable and the $-4$ is called the **coefficient**.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions"
  },
  {
    "record_id": "ch10-b015",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Constants and coefficients"
    },
    "content_text": "**constant** A constant is a term without a variable. A constant can have a negative value (if it has a minus sign in front of it) or a positive value (if it has a plus sign or no sign in front of it).\n\n**coefficient** The coefficient is the number (factor) being multiplied by the variable. A coefficient can have a negative value (if it has a minus sign in front of it) or a positive value (if it has a plus sign or no sign in front of it).",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions"
  },
  {
    "record_id": "ch10-b016",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Constants and coefficients"
    },
    "content_text": "Here are some more examples of terms that will vary in value, depending on the value of the variable:\n\n$$\np + p + p = 3p\n$$\n\n$$\ny + y = 2y\n$$\n\n$$\nm + m + m + m + m = 5m\n$$\n\nIn $3p$, the 3 is the coefficient of $p$. We know there are three $p$s.\n\n- If $p = 2$, then $3p = 2 + 2 + 2 = 3 \\times 2 = 6$.\n- If $p = 5$, then $3p = 3 \\times 5 = 15$.\n\nIn $2y$, the 2 is the coefficient of $y$. We know there are two $y$s.\n\n- If $y = 10$, then $2y = 2 \\times 10 = 20$.\n- If $y = \\frac{1}{2}$, then $2y = 2 \\times \\frac{1}{2} = 1$.\n\nIn $5m$, the 5 is the coefficient of $m$. We know there are five $m$s.\n\n- If $m = 1$, then $5m = 5 \\times 1 = 5$.\n- If $m = 7$, then $5m = 5 \\times 7 = 35$.\n\nIn $a$, the coefficient of $a$ is 1. We know there is only one $a$.\n\n- If $a = 1$, then $a = 1 \\times 1 = 1$.\n- If $a = \\frac{2}{3}$, then $a = 1 \\times \\frac{2}{3} = \\frac{2}{3}$.\n\nThe terminology we use in algebra that we have learnt so far are summarised here:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-10-001.png)",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions"
  },
  {
    "record_id": "ch10-b017",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Worked example 10.3: Identifying the different parts of an algebraic expression"
    },
    "content_text": "",
    "prompt_text": "For the algebraic expression below, write down the number of terms, the constant term, the coefficient of $x$, the coefficient of $y$ and the coefficient of $k$.\n\n$$\n2x + y -4k -6\n$$",
    "answer_text": "Step 1: Identify and count the number of terms.\n\n$$\n\\begin{array}{l}\n2x\\space \\enclose{circle}[mathcolor=\"red\"]{+} \\space y\\space \\enclose{circle}[mathcolor=\"red\"]{-} \\space 4k\\space \\enclose{circle}[mathcolor=\"red\"]{-} \\space6\n\\end{array}\n$$\n\nThere are 4 terms.\n\nStep 2: The constant is the term that doesn't have a variable. The plus or minus sign in front of the term is part of the constant.\n\n$-6$ is the constant.\n\nStep 3: To find the coefficient of $x$, look for the term that contains an $x$. The plus or minus sign in front of the term is part of the coefficient.\n\nIn algebra, we normally do not write down the plus sign in front of the very first term.\n\nThe coefficient of $x$ is $+2$ or 2.\n\nStep 4: To find the coefficient of $y$, look for the term that contains a $y$. The plus or minus sign in front of the term is part of the coefficient.\n\nIn algebra, we normally do not write down the number 1 if it is the coefficient of a variable.\n\nThe coefficient of $y$ is $+1$ or 1.\n\nStep 5: To find the coefficient of $k$, look for the term that contains a $k$. The plus or minus sign in front of the term is part of the coefficient.\n\nThe coefficient of $k$ is $-4$.",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions"
  },
  {
    "record_id": "ch10-b018",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.3: Identify parts of an algebraic expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.3: Identify parts of an algebraic expression",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions"
  },
  {
    "record_id": "ch10-b018-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.3: Identify parts of an algebraic expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.3: Identify parts of an algebraic expression\n\n1. How many terms does this expression contain?\n\n$$\n3 \times m + 2\n$$",
    "answer_text": "2",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions"
  },
  {
    "record_id": "ch10-b018-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.3: Identify parts of an algebraic expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.3: Identify parts of an algebraic expression\n\n2. What is the constant in this algebraic expression?\n\n$$\n-3+7yz+x\n$$",
    "answer_text": "$-3$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions"
  },
  {
    "record_id": "ch10-b018-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.3: Identify parts of an algebraic expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.3: Identify parts of an algebraic expression\n\n3. What is the coefficient of this term?\n\n$$\n8\times p\n$$",
    "answer_text": "8",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions"
  },
  {
    "record_id": "ch10-b018-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.3: Identify parts of an algebraic expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.3: Identify parts of an algebraic expression\n\n4. Answer the questions about this expression: $3 \times 7x - 5y -1$.\n\na) How many terms does this expression have?\nb) What is the coefficient of $x$?\nc) What is the coefficient of $y$?\nd) What is the value of the constant term?",
    "answer_text": "a) 3\nb) 21 or 3 \times 7\nc) $-5$\nd) $-1$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions"
  },
  {
    "record_id": "ch10-b018-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.3: Identify parts of an algebraic expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.3: Identify parts of an algebraic expression\n\n5. Answer the questions about this expression: $10 - x - 2y + z$.\n\na) How many terms does this expression have?\nb) What is the coefficient of $x$?\nc) What is the coefficient of $z$?\nd) What is the value of the constant term?",
    "answer_text": "a) 4\nb) $-1$\nc) 1\nd) 10",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions"
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
  "subtopic_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions",
  "subtopic_title": "Identification of coefficients of terms of algebraic expressions",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions-po01",
        "source_performance_objective_index": 1,
        "text": "Identify the coefficient of a given algebraic term"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "identification-of-coefficients-ao-identify-coefficient",
          "text": "Identify the coefficient of a given algebraic term."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions-po02",
        "source_performance_objective_index": 2,
        "text": "Identify the positive and negative coefficients of a given algebraic term"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "identification-of-coefficients-ao-identify-positive-coefficient",
          "text": "Identify the positive coefficient of a given algebraic term."
        },
        {
          "atomic_objective_id": "identification-of-coefficients-ao-identify-negative-coefficient",
          "text": "Identify the negative coefficient of a given algebraic term."
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
    "record_id": "ch10-b014",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Constants and coefficients"
    },
    "content_text": "There are two other words you also need to know and understand when working with algebraic terms: constant and coefficient.\n\nThe following algebraic expression contains two terms:\n\n$$-4x + 5$$\n\n5 is called a **constant** term as the value will always be 5 and it will not vary. The value of the $-4x$ term will vary depending on the value of the variable $x$. In the $-4x$ term, the $x$ is called the variable and the $-4$ is called the **coefficient**.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions"
  },
  {
    "record_id": "ch10-b015",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Constants and coefficients"
    },
    "content_text": "**constant** A constant is a term without a variable. A constant can have a negative value (if it has a minus sign in front of it) or a positive value (if it has a plus sign or no sign in front of it).\n\n**coefficient** The coefficient is the number (factor) being multiplied by the variable. A coefficient can have a negative value (if it has a minus sign in front of it) or a positive value (if it has a plus sign or no sign in front of it).",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions"
  },
  {
    "record_id": "ch10-b016",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Constants and coefficients"
    },
    "content_text": "Here are some more examples of terms that will vary in value, depending on the value of the variable:\n\n$$\np + p + p = 3p\n$$\n\n$$\ny + y = 2y\n$$\n\n$$\nm + m + m + m + m = 5m\n$$\n\nIn $3p$, the 3 is the coefficient of $p$. We know there are three $p$s.\n\n- If $p = 2$, then $3p = 2 + 2 + 2 = 3 \\times 2 = 6$.\n- If $p = 5$, then $3p = 3 \\times 5 = 15$.\n\nIn $2y$, the 2 is the coefficient of $y$. We know there are two $y$s.\n\n- If $y = 10$, then $2y = 2 \\times 10 = 20$.\n- If $y = \\frac{1}{2}$, then $2y = 2 \\times \\frac{1}{2} = 1$.\n\nIn $5m$, the 5 is the coefficient of $m$. We know there are five $m$s.\n\n- If $m = 1$, then $5m = 5 \\times 1 = 5$.\n- If $m = 7$, then $5m = 5 \\times 7 = 35$.\n\nIn $a$, the coefficient of $a$ is 1. We know there is only one $a$.\n\n- If $a = 1$, then $a = 1 \\times 1 = 1$.\n- If $a = \\frac{2}{3}$, then $a = 1 \\times \\frac{2}{3} = \\frac{2}{3}$.\n\nThe terminology we use in algebra that we have learnt so far are summarised here:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-10-001.png)",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions"
  },
  {
    "record_id": "ch10-b017",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Worked example 10.3: Identifying the different parts of an algebraic expression"
    },
    "content_text": "",
    "prompt_text": "For the algebraic expression below, write down the number of terms, the constant term, the coefficient of $x$, the coefficient of $y$ and the coefficient of $k$.\n\n$$\n2x + y -4k -6\n$$",
    "answer_text": "Step 1: Identify and count the number of terms.\n\n$$\n\\begin{array}{l}\n2x\\space \\enclose{circle}[mathcolor=\"red\"]{+} \\space y\\space \\enclose{circle}[mathcolor=\"red\"]{-} \\space 4k\\space \\enclose{circle}[mathcolor=\"red\"]{-} \\space6\n\\end{array}\n$$\n\nThere are 4 terms.\n\nStep 2: The constant is the term that doesn't have a variable. The plus or minus sign in front of the term is part of the constant.\n\n$-6$ is the constant.\n\nStep 3: To find the coefficient of $x$, look for the term that contains an $x$. The plus or minus sign in front of the term is part of the coefficient.\n\nIn algebra, we normally do not write down the plus sign in front of the very first term.\n\nThe coefficient of $x$ is $+2$ or 2.\n\nStep 4: To find the coefficient of $y$, look for the term that contains a $y$. The plus or minus sign in front of the term is part of the coefficient.\n\nIn algebra, we normally do not write down the number 1 if it is the coefficient of a variable.\n\nThe coefficient of $y$ is $+1$ or 1.\n\nStep 5: To find the coefficient of $k$, look for the term that contains a $k$. The plus or minus sign in front of the term is part of the coefficient.\n\nThe coefficient of $k$ is $-4$.",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions"
  },
  {
    "record_id": "ch10-b018",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.3: Identify parts of an algebraic expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.3: Identify parts of an algebraic expression",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions"
  },
  {
    "record_id": "ch10-b018-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.3: Identify parts of an algebraic expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.3: Identify parts of an algebraic expression\n\n1. How many terms does this expression contain?\n\n$$\n3 \times m + 2\n$$",
    "answer_text": "2",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions"
  },
  {
    "record_id": "ch10-b018-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.3: Identify parts of an algebraic expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.3: Identify parts of an algebraic expression\n\n2. What is the constant in this algebraic expression?\n\n$$\n-3+7yz+x\n$$",
    "answer_text": "$-3$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions"
  },
  {
    "record_id": "ch10-b018-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.3: Identify parts of an algebraic expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.3: Identify parts of an algebraic expression\n\n3. What is the coefficient of this term?\n\n$$\n8\times p\n$$",
    "answer_text": "8",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions"
  },
  {
    "record_id": "ch10-b018-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.3: Identify parts of an algebraic expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.3: Identify parts of an algebraic expression\n\n4. Answer the questions about this expression: $3 \times 7x - 5y -1$.\n\na) How many terms does this expression have?\nb) What is the coefficient of $x$?\nc) What is the coefficient of $y$?\nd) What is the value of the constant term?",
    "answer_text": "a) 3\nb) 21 or 3 \times 7\nc) $-5$\nd) $-1$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions"
  },
  {
    "record_id": "ch10-b018-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.2 Working with algebraic expressions",
      "h3": "Exercise 10.3: Identify parts of an algebraic expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.3: Identify parts of an algebraic expression\n\n5. Answer the questions about this expression: $10 - x - 2y + z$.\n\na) How many terms does this expression have?\nb) What is the coefficient of $x$?\nc) What is the coefficient of $z$?\nd) What is the value of the constant term?",
    "answer_text": "a) 4\nb) $-1$\nc) 1\nd) 10",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions"
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
