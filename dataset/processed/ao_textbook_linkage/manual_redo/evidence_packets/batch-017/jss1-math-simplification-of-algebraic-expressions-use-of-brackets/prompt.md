# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-3",
  "topic_key": "jss1-math-simplification-of-algebraic-expressions",
  "topic": "Simplification of Algebraic Expressions",
  "subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets",
  "subtopic_title": "Use of brackets",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets-po01",
        "source_performance_objective_index": 1,
        "text": "Insert/remove brackets and simplify expressions"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "use-of-brackets-ao-insert-brackets",
          "text": "Insert brackets in expressions."
        },
        {
          "atomic_objective_id": "use-of-brackets-ao-remove-brackets",
          "text": "Remove brackets from expressions."
        },
        {
          "atomic_objective_id": "use-of-brackets-ao-simplify-expressions",
          "text": "Simplify expressions."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch10-b029",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": null
    },
    "content_text": "We sometimes use brackets to group terms in algebraic expressions together.\n\nAs you know, $2x$ means $2 \\times x = x + x$.\n\nIf we replace the $x$ with $(x + y)$, then in the same way:\n\n$$\n2(x + y) = 2 \\times (x + y)\n$$\n\nWe can use repeated addition to work out any multiplication, so:\n\n$$\n2 \\times (x + y) = (x + y) + (x + y)\n$$\n\nWe need to remove the brackets before we can collect the like terms and simplify the expression:\n\n$$\n(x + y) + (x + y)=x + y + x + y\n$$\n\nTherefore:\n\n$$\n\\begin{align}\n&\\phantom{000}2 \\times (x + y) \\\\\n&= (x + y) + (x + y) \\\\\n&= x + y + x + y \\\\\n&= x + x + y + y \\\\\n&= 2x + 2y\n\\end{align}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b030",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Worked example 10.7: Removing brackets using repeated addition"
    },
    "content_text": "Source math retained:\n4m = 4 \\times m\nm\n(a + b)\n4(a + b) = 4 \\times (a + b)\n\\begin{align}\n &\\phantom{000}4 \\times (a + b) \\\\\n &= (a+b) + (a+b) + (a+b) + (a+b) \\\\\n \\end{align}\n\\begin{align}\n &\\phantom{000}4 \\times (a + b) \\\\\n &= (a+b) + (a+b) + (a+b) + (a+b) \\\\\n &= a + b + a + b + a + b + a + b \\\\\n \\end{align}\n\\begin{align}\n &\\phantom{000}4 \\times (a + b) \\\\\n &= (a+b) + (a+b) + (a+b) + (a+b) \\\\\n &= a + b + a + b + a + b + a + b \\\\\n &= a + a + a + a + b + b + b + b \\\\\n &= 4a + 4b\n \\end{align}",
    "prompt_text": "$4m = 4 \\times m$. Replace the $m$ with $(a + b)$. Then remove the brackets and simplify the expression.",
    "answer_text": "Step 1: Replace the $m$ with $(a + b)$.\n\n$$\n4(a + b) = 4 \\times (a + b)\n$$\n\nStep 2: Use repeated addition to work out this multiplication.\n\n$$\n\\begin{align}\n&\\phantom{000}4 \\times (a + b) \\\\\n&= (a+b) + (a+b) + (a+b) + (a+b)\n\\end{align}\n$$\n\nStep 3: Remove the brackets.\n\n$$\n\\begin{align}\n&\\phantom{000}4 \\times (a + b) \\\\\n&= (a+b) + (a+b) + (a+b) + (a+b) \\\\\n&= a + b + a + b + a + b + a + b\n\\end{align}\n$$\n\nStep 4: Collect the like terms and simplify.\n\n$$\n\\begin{align}\n&\\phantom{000}4 \\times (a + b) \\\\\n&= (a+b) + (a+b) + (a+b) + (a+b) \\\\\n&= a + b + a + b + a + b + a + b \\\\\n&= a + a + a + a + b + b + b + b \\\\\n&= 4a + 4b\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b031",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Exercise 10.6: Remove brackets and simplify"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.6: Remove brackets and simplify\n\nRemove the brackets using repeated addition and then simplify.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b031-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Exercise 10.6: Remove brackets and simplify"
    },
    "content_text": "Source math retained:\n2(h +m)\n\\begin{align}\n &= 2 \\times (h+m) \\\\\n &=(h + m) + (h + m) \\\\\n &= h+m+h+m \\\\\n &= h + h + m + m \\\\\n &=2h + 2m\n \\end{align}",
    "prompt_text": "### Exercise 10.6: Remove brackets and simplify\n\n1. $$\n2(h +m)\n$$",
    "answer_text": "$$\n\\begin{align}\n&= 2 \\times (h+m) \\\\\n&=(h + m) + (h + m) \\\\\n&= h+m+h+m \\\\\n&= h + h + m + m \\\\\n&=2h + 2m\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b031-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Exercise 10.6: Remove brackets and simplify"
    },
    "content_text": "Source math retained:\n3(p +k)\n\\begin{align}\n &= 3 \\times (p+k) \\\\\n &=(p + k) + (p + k) + (p + k) \\\\\n &=p+k+p+k+p+k \\\\\n &= p + p + p  + k + k + k \\\\\n &=3p + 3k\n \\end{align}",
    "prompt_text": "### Exercise 10.6: Remove brackets and simplify\n\n2. $$\n3(p +k)\n$$",
    "answer_text": "$$\n\\begin{align}\n&= 3 \\times (p+k) \\\\\n&=(p + k) + (p + k) + (p + k) \\\\\n&=p+k+p+k+p+k \\\\\n&= p + p + p  + k + k + k \\\\\n&=3p + 3k\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b031-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Exercise 10.6: Remove brackets and simplify"
    },
    "content_text": "Source math retained:\n2(a + 2)\n\\begin{align}\n &= 2 \\times (a+2) \\\\\n &=(a + 2) + (a + 2) \\\\\n &=a+2+a+2 \\\\\n &= a + a + 2+ 2 \\\\\n &=2a + 4\n \\end{align}",
    "prompt_text": "### Exercise 10.6: Remove brackets and simplify\n\n3. $$\n2(a + 2)\n$$",
    "answer_text": "$$\n\\begin{align}\n&= 2 \\times (a+2) \\\\\n&=(a + 2) + (a + 2) \\\\\n&=a+2+a+2 \\\\\n&= a + a + 2+ 2 \\\\\n&=2a + 4\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b031-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Exercise 10.6: Remove brackets and simplify"
    },
    "content_text": "Source math retained:\n3(4x +3y)\n\\begin{align}\n &= 3 \\times (4x+3y) \\\\\n &=(4x + 3y) + (4x + 3y) + (4x + 3y) \\\\\n &=4x+3y+4x+3y+4x+3y \\\\\n &= 4x + 4x + 4x + 3y + 3y + 3y \\\\\n &=12x + 9y\n \\end{align}",
    "prompt_text": "### Exercise 10.6: Remove brackets and simplify\n\n4. $$\n3(4x +3y)\n$$",
    "answer_text": "$$\n\\begin{align}\n&= 3 \\times (4x+3y) \\\\\n&=(4x + 3y) + (4x + 3y) + (4x + 3y) \\\\\n&=4x+3y+4x+3y+4x+3y \\\\\n&= 4x + 4x + 4x + 3y + 3y + 3y \\\\\n&=12x + 9y\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b031-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Exercise 10.6: Remove brackets and simplify"
    },
    "content_text": "Source math retained:\n2(10a - 6b + c)\n\\begin{align}\n &= 2 \\times (10a - 6b + c) \\\\\n &=(10a - 6b + c) + (10a - 6b + c) \\\\\n &=10a - 6b + c + 10a - 6b + c \\\\\n &= 10a + 10a - 6b - 6b + c + c \\\\\n &=20a - 12b + 2c\n \\end{align}",
    "prompt_text": "### Exercise 10.6: Remove brackets and simplify\n\n5. $$\n2(10a - 6b + c)\n$$",
    "answer_text": "$$\n\\begin{align}\n&= 2 \\times (10a - 6b + c) \\\\\n&=(10a - 6b + c) + (10a - 6b + c) \\\\\n&=10a - 6b + c + 10a - 6b + c \\\\\n&= 10a + 10a - 6b - 6b + c + c \\\\\n&=20a - 12b + 2c\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b032",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Negative signs before brackets"
    },
    "content_text": "Up to now we only worked with brackets that have a positive sign in front of them. When there is a negative sign before a bracket, it affects all the terms inside the bracket.\n\nLook at this example:\n\n$$\n10-(2+3)\n$$\n\nWe can simplify it as follows:\n\n$$\n\\begin{align}\n&\\phantom{000}10-(2+3) \\\\\n&=10-5 \\\\\n&=5\n\\end{align}\n$$\n\nThis is the same as:\n\n$$\n\\begin{align}\n&\\phantom{000}10-(2+3) \\\\\n&=10-2-3 \\\\\n&=8-3 \\\\\n&=5\n\\end{align}\n$$\n\nIt is NOT the same as:\n\n$$\n10-(2+3) \\neq 10-2+3 = 11\n$$\n\nSo, if we remove a bracket with a negative sign in front of it, we change the signs of all the terms inside the bracket. Here are some examples:\n\n$$\n5a-(2b+c)=5a-2b-c\n$$\n\n$$\n4x-(-y+2z)=4x+y-2z\n$$\n\n$$\n-(q-2r)+s=-q+2r+s\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b033",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Worked example 10.8: Removing brackets with negative signs in front"
    },
    "content_text": "",
    "prompt_text": "Remove the brackets and then simplify the following expression:\n\n$$\n2(4m+n)-(5m+3n)\n$$",
    "answer_text": "Step 1: Use repeated addition to work out multiplication of brackets.\n\n$$\n\\begin{align}\n&\\phantom{000}2(4m + n)-(5m+3n) \\\\\n&= (4m+n) + (4m+n) - (5m+3n) \\\\\n\\end{align}\n$$\n\nStep 2: Remove the brackets. If there is a negative sign in front of a bracket, change the signs of all the terms inside the bracket.\n\n$$\n\\begin{align}\n&\\phantom{000}2(4m + n)-(5m+3n) \\\\\n&= (4m+n) + (4m+n) - (5m+3n) \\\\\n&=4m+n+4m+n-5m-3n \\\\\n\\end{align}\n$$\n\nStep 3: Collect the like terms and simplify.\n\n$$\n\\begin{align}\n&\\phantom{000}2(4m + n)-(5m+3n) \\\\\n&= (4m+n) + (4m+n) - (5m+3n) \\\\\n&=4m+n+4m+n-5m-3n \\\\\n&=4m+4m-5m+n+n-3n \\\\\n&=3m-n\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b034",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Exercise 10.7: Remove brackets with negative signs and simplify"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.7: Remove brackets with negative signs and simplify\n\nRemove the brackets and then simplify.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b034-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Exercise 10.7: Remove brackets with negative signs and simplify"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.7: Remove brackets with negative signs and simplify\n\nRemove the brackets and then simplify.\n\n1. $$\n3k-(2p +k)\n$$",
    "answer_text": "$$\n\\begin{align}\n&= 3k-2p-k \\\\\n&=3k-k-2p \\\\\n&=2k-2p\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b034-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Exercise 10.7: Remove brackets with negative signs and simplify"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.7: Remove brackets with negative signs and simplify\n\nRemove the brackets and then simplify.\n\n2. $$\n2h +m-(m+2h)-m\n$$",
    "answer_text": "$$\n\\begin{align}\n&= 2h +m-m-2h-m \\\\\n&=2h-2h+m-m-m \\\\\n&=0-m \\\\\n&=-m\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b034-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Exercise 10.7: Remove brackets with negative signs and simplify"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.7: Remove brackets with negative signs and simplify\n\nRemove the brackets and then simplify.\n\n3. $$\n-(4x +3y)+(2x-y)\n$$",
    "answer_text": "$$\n\\begin{align}\n&=-4x - 3y + 2x -y \\\\\n&=-4x+2x-3y-y \\\\\n&=-2x-4y\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b034-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Exercise 10.7: Remove brackets with negative signs and simplify"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.7: Remove brackets with negative signs and simplify\n\nRemove the brackets and then simplify.\n\n4. $$\n3(a + 2)-(4a+2)\n$$",
    "answer_text": "$$\n\\begin{align}\n&=(a + 2) + (a + 2) +(a+2) -(4a+2) \\\\\n&=a+2+a+2+a+2-4a-2 \\\\\n&=a + a + a-4a +2+ 2+2-2 \\\\\n&=-a + 4\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b034-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Exercise 10.7: Remove brackets with negative signs and simplify"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.7: Remove brackets with negative signs and simplify\n\nRemove the brackets and then simplify.\n\n5. $$\n2(10a - 6b + c)-(3c-2b-a)-(b+c)\n$$",
    "answer_text": "$$\n\\begin{align}\n&=(10a - 6b + c) + (10a - 6b + c) -(3c-2b-a)-(b+c) \\\\\n&=10a - 6b + c + 10a - 6b + c -3c+2b+a-b-c \\\\\n&=10a + 10a +a - 6b - 6b +2b -b + c + c -3c-c \\\\\n&=21a - 10b - 2c\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b035",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Negative signs before brackets"
    },
    "content_text": "When we change the signs of the terms inside a bracket that has a negative sign in front of it, we actually multiply each term by $-1$. You will learn more about this next year.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b036",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": null
    },
    "content_text": "When we have an expression with brackets, we know we need to multiply. When we do the multiplication, we say that we **expand** the expression.\n\nFrom the examples and the exercises above, can you see a shorter way than repeated addition to multiply the expressions? The simpler way is to multiply the coefficient of the bracket by each of the terms that is inside the bracket.\n\nWhen we do this, we are applying the **distributive law**. This law states that:\n\n$$\n4 \\times (3+2) = 4 \\times 3 + 4 \\times 2\n$$\n\nIn other words, 4 groups of $(3 + 2)$ is the same as 4 groups of 3 plus 4 groups of 2. So the $4 \\times$ can be \"distributed\" across the $(3 + 2)$, to get:\n\n$$\n4 =\\times= 3 + 4 =\\times= 2\n$$\n\nBy now you know that $2(a + b) = 2a + 2b$.\n\nNote that the bracket is seen as one \"package\" that can be replaced by one variable. Therefore, the expression $2(a + b)$ has one term, but the expression $2a + 2b$ has two terms.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b037",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": null
    },
    "content_text": "**expand** To expand an algebraic expression is to multiply what is outside the brackets (the coefficient of the bracket) by each of the terms that is inside the bracket.\n\n**distributive law** The distributive law states that the multiplying factor (the coefficient) can be distributed across each of the terms inside a bracket, so $a x (b + c) = a x b + a x c$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b038",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Worked example 10.9: Multiplying the coefficient of a bracket by two terms inside"
    },
    "content_text": "",
    "prompt_text": "Expand this expression:\n\n$$\n3(2a + b)\n$$",
    "answer_text": "Step 1: Multiply the 3 by the first term in the bracket, which is $2a$.\n\nRemember that $2a$ means $2\\times a$.\n\n$$\n3 \\times 2 \\times a = 6 \\times a = 6a\n$$\n\nSo the first term is $6a$.\n\nStep 2: Multiply the 3 by the second term in the bracket, which is $b$.\n\n$$\n3 \\times b = 3b\n$$\n\nThe second term is $3b$.\n\nStep 3: Write the new terms of the expression with the correct operator, which in this case is $+$.\n\n$$\n6a + 3b\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b039",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Worked example 10.10: Multiplying the coefficient of a bracket by three terms inside"
    },
    "content_text": "",
    "prompt_text": "Expand the expression $2(a + 5b - 3c)$.",
    "answer_text": "Step 1: Multiply the 2 by the first term in the bracket.\n\n$$\n2 \\times a = 2a\n$$\n\nStep 2: Multiply the 2 by the second term in the bracket.\n\n$$\n2 \\times 5b = 10b\n$$\n\nStep 3: Multiply the 2 by the third term in the bracket.\n\n$$\n2 \\times 3c = 6c\n$$\n\nStep 4: Write the new terms of the expression with the correct operation signs.\n\n$$\n2a + 10b -6c\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b040",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": null
    },
    "content_text": "When you expand, you do not need to write all the steps separately as shown in the worked examples above. You can go directly to the answer by writing each new term as you work it out. So your answer could look like this: $2(a + 5b - 3c) = 2a + 10b -6c$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b041",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.8: Use the distributive law to expand and simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.8: Use the distributive law to expand and simplify expressions\n\nUse the distributive law to expand the brackets and then simplify the expressions.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b041-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.8: Use the distributive law to expand and simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.8: Use the distributive law to expand and simplify expressions\n\nUse the distributive law to expand the brackets and then simplify the expressions.\n\n1. $$\n3(2 + a - 4x)\n$$",
    "answer_text": "$$\n=6+3a-12x\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b041-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.8: Use the distributive law to expand and simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.8: Use the distributive law to expand and simplify expressions\n\nUse the distributive law to expand the brackets and then simplify the expressions.\n\n2. $$\n5(2n - 16 - m)+4m\n$$",
    "answer_text": "$$\n\\begin{align}\n&=10n-80-5m+4m \\\\\n&=10n-80-m\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b041-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.8: Use the distributive law to expand and simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.8: Use the distributive law to expand and simplify expressions\n\nUse the distributive law to expand the brackets and then simplify the expressions.\n\n3. $$\n2(3x - 3y + 3)+3x-3y+3\n$$",
    "answer_text": "$$\n\\begin{align}\n&=6x-6y+6+3x-3y+3 \\\\\n&=6x+3x-6y-3y+6+3 \\\\\n&=9x-9y+9\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b041-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.8: Use the distributive law to expand and simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.8: Use the distributive law to expand and simplify expressions\n\nUse the distributive law to expand the brackets and then simplify the expressions.\n\n4. $$\n5(3x-4y+z)+3(x+y-2z)\n$$",
    "answer_text": "$$\n\\begin{align}\n&=15x-20y+5z+3x+3y-6z \\\\\n&=15x+3x-20y+3y+5z-6z \\\\\n&=18x-17y-z\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b041-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.8: Use the distributive law to expand and simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.8: Use the distributive law to expand and simplify expressions\n\nUse the distributive law to expand the brackets and then simplify the expressions.\n\n5. $$\n3(12a + 11b + 11c) -(2a - b + c)\n$$",
    "answer_text": "$$\n\\begin{align}\n&=36a+33b+33c-2a+b-c \\\\\n&=36a-2a+33b+b+33c-c \\\\\n&=34a+34b+32c\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b042",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Order of operations"
    },
    "content_text": "In Chapter 9 you were reminded of the correct order of operations that you learnt last year:\n\n1. **B**rackets\n2. **O**f\n3. **D**ivide\n4. **M**ultiply\n5. **A**dd\n6. **S**ubtract",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b043",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Worked example 10.11: Following the correct order of operations"
    },
    "content_text": "",
    "prompt_text": "Simplify the expression $2(3x+5x+1)+4\\times3x$.",
    "answer_text": "Step 1: Simplify the terms inside the bracket first.\n\n$$\n2(8x+1)+4\\times3x\n$$\n\nStep 2: There is no \"of\" or division in the expression, so do multiplication next.\n\nUse the distributive law to multiply the bracket by its coefficient.\n\nRemember that $4\\times3x$ means $4\\times3\\times x$.\n\n$$\n16x+2+12x\n$$\n\nStep 3: Collect the like terms and simplify.\n\n$$\n\\begin{align}\n& 16x+2+12x \\\\\n=& 16x+12x+2 \\\\\n=& 28x+2\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b044",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Worked example 10.12: Following the correct order of operations"
    },
    "content_text": "",
    "prompt_text": "Simplify the expression $(2y+6y)\\div(2\\times2) \\times 10-5\\times2y+2y$.",
    "answer_text": "Step 1: Simplify the terms inside the brackets first.\n\n$$\n8y\\div 4 \\times 10-5\\times2y+2y\n$$\n\nStep 2: There is no \"of\" in the expression, so do division next.\n\nWhen we multiply a term that has a variable by a number, we simply multiply the coefficient of the term by the number. For example $6x \\times 2=12x$. In the same way, when we divide a term that has a variable by a number, we simply divide the coefficient of the term by the number. For example $6x\\div 2=3x$.\n\n$$\n2y \\times 10-5\\times2y+2y\n$$\n\nStep 3: Multiplication comes after division.\n\n$$\n20y-10y+2y\n$$\n\nStep 4: Addition comes after multiplication.\n\n$$\n20y+2y-10y=22y-10y\n$$\n\nStep 5: Do subtraction last.\n\n$$\n12y\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b045",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.9: Follow the correct order of operations to simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.9: Follow the correct order of operations to simplify expressions\n\nSimplify the expressions.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b045-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.9: Follow the correct order of operations to simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.9: Follow the correct order of operations to simplify expressions\n\nSimplify the expressions.\n\n1. $$\n5y-(4y-3y)\n$$",
    "answer_text": "$$\n\\begin{align}\n&=5y-y \\\\\n&=4y\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b045-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.9: Follow the correct order of operations to simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.9: Follow the correct order of operations to simplify expressions\n\nSimplify the expressions.\n\n2. $$\n4x(7 - 2)-(x + 2)\n$$",
    "answer_text": "$$\n\\begin{align}\n&=4x(5)-x-2 \\\\\n&=20x-x-2 \\\\\n&=19x-2\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b045-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.9: Follow the correct order of operations to simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.9: Follow the correct order of operations to simplify expressions\n\nSimplify the expressions.\n\n3. $$\nx(2+3\\times4)-(x+2x)\n$$",
    "answer_text": "$$\n\\begin{align}\n&=x(2+12)-x-2x \\\\\n&=x(14)-x-2x \\\\\n&=14x-x-2x \\\\\n&=11x\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b045-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.9: Follow the correct order of operations to simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.9: Follow the correct order of operations to simplify expressions\n\nSimplify the expressions.\n\n4. $$\n4x\\times 2+3x \\times 9 \\div 3\n$$",
    "answer_text": "$$\n\\begin{align}\n&=4x\\times 2+3x \\times 3 \\\\\n&=8x+9x \\\\\n&=17x \\\\\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b045-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.9: Follow the correct order of operations to simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.9: Follow the correct order of operations to simplify expressions\n\nSimplify the expressions.\n\n5. $$\n2(x+y)-(2x+y-3x)\n$$",
    "answer_text": "$$\n\\begin{align}\n&=2(x+y)-(2x-3x+y) \\\\\n&=2(x+y)-(x+y) \\\\\n&=2x+2y-x-y \\\\\n&=2x-x+2y-y \\\\\n&=x+y\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b045-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.9: Follow the correct order of operations to simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.9: Follow the correct order of operations to simplify expressions\n\nSimplify the expressions.\n\n6. $$\n5y-(4y-4)+2y\\times 3\n$$",
    "answer_text": "$$\n\\begin{align}\n&=5y-(4y-4)+6y \\\\\n&=5y-4y+4+6y \\\\\n&=5y-4y+6y+4 \\\\\n&=11y-4y+4 \\\\\n&=7y+4\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b045-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.9: Follow the correct order of operations to simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.9: Follow the correct order of operations to simplify expressions\n\nSimplify the expressions.\n\n7. $$\n-(p+q)-p+q+2(p-q)\n$$",
    "answer_text": "$$\n\\begin{align}\n&=-p-q-p+q+2p-2q \\\\\n&=-p-p+2p-q+q-2q \\\\\n&=0-2q \\\\\n&=-2q\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b045-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.9: Follow the correct order of operations to simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.9: Follow the correct order of operations to simplify expressions\n\nSimplify the expressions.\n\n8. $$\n-3m(-5+2+3)+2m\\times3\n$$",
    "answer_text": "$$\n\\begin{align}\n&=-3m(-5+5)+2m\\times3 \\\\\n&=-3m(0)+6m \\\\\n&=0+6m \\\\\n&=6m\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b045-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.9: Follow the correct order of operations to simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.9: Follow the correct order of operations to simplify expressions\n\nSimplify the expressions.\n\n9. $$\n8x \\div 2+4\\times 2x+2\n$$",
    "answer_text": "$$\n\\begin{align}\n&=4x+8x+2 \\\\\n&=12x+2\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b045-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.9: Follow the correct order of operations to simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.9: Follow the correct order of operations to simplify expressions\n\nSimplify the expressions.\n\n10. $$\n3(-2a + b + c + 4a - 2b + c)-(a - b - c)\n$$",
    "answer_text": "$$\n\\begin{align}\n&=3(-2a+4a+b-2b+c+c)-(a-b-c) \\\\\n&=3(2a-b+2c)-(a-b-c) \\\\\n&=6a-3b+6c-a+b+c \\\\\n&=6a-a-3b+b+6c+c \\\\\n&=5a-2b+7c\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
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
  "subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets",
  "subtopic_title": "Use of brackets",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets-po01",
        "source_performance_objective_index": 1,
        "text": "Insert/remove brackets and simplify expressions"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "use-of-brackets-ao-insert-brackets",
          "text": "Insert brackets in expressions."
        },
        {
          "atomic_objective_id": "use-of-brackets-ao-remove-brackets",
          "text": "Remove brackets from expressions."
        },
        {
          "atomic_objective_id": "use-of-brackets-ao-simplify-expressions",
          "text": "Simplify expressions."
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
    "record_id": "ch10-b029",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": null
    },
    "content_text": "We sometimes use brackets to group terms in algebraic expressions together.\n\nAs you know, $2x$ means $2 \\times x = x + x$.\n\nIf we replace the $x$ with $(x + y)$, then in the same way:\n\n$$\n2(x + y) = 2 \\times (x + y)\n$$\n\nWe can use repeated addition to work out any multiplication, so:\n\n$$\n2 \\times (x + y) = (x + y) + (x + y)\n$$\n\nWe need to remove the brackets before we can collect the like terms and simplify the expression:\n\n$$\n(x + y) + (x + y)=x + y + x + y\n$$\n\nTherefore:\n\n$$\n\\begin{align}\n&\\phantom{000}2 \\times (x + y) \\\\\n&= (x + y) + (x + y) \\\\\n&= x + y + x + y \\\\\n&= x + x + y + y \\\\\n&= 2x + 2y\n\\end{align}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b030",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Worked example 10.7: Removing brackets using repeated addition"
    },
    "content_text": "Source math retained:\n4m = 4 \\times m\nm\n(a + b)\n4(a + b) = 4 \\times (a + b)\n\\begin{align}\n &\\phantom{000}4 \\times (a + b) \\\\\n &= (a+b) + (a+b) + (a+b) + (a+b) \\\\\n \\end{align}\n\\begin{align}\n &\\phantom{000}4 \\times (a + b) \\\\\n &= (a+b) + (a+b) + (a+b) + (a+b) \\\\\n &= a + b + a + b + a + b + a + b \\\\\n \\end{align}\n\\begin{align}\n &\\phantom{000}4 \\times (a + b) \\\\\n &= (a+b) + (a+b) + (a+b) + (a+b) \\\\\n &= a + b + a + b + a + b + a + b \\\\\n &= a + a + a + a + b + b + b + b \\\\\n &= 4a + 4b\n \\end{align}",
    "prompt_text": "$4m = 4 \\times m$. Replace the $m$ with $(a + b)$. Then remove the brackets and simplify the expression.",
    "answer_text": "Step 1: Replace the $m$ with $(a + b)$.\n\n$$\n4(a + b) = 4 \\times (a + b)\n$$\n\nStep 2: Use repeated addition to work out this multiplication.\n\n$$\n\\begin{align}\n&\\phantom{000}4 \\times (a + b) \\\\\n&= (a+b) + (a+b) + (a+b) + (a+b)\n\\end{align}\n$$\n\nStep 3: Remove the brackets.\n\n$$\n\\begin{align}\n&\\phantom{000}4 \\times (a + b) \\\\\n&= (a+b) + (a+b) + (a+b) + (a+b) \\\\\n&= a + b + a + b + a + b + a + b\n\\end{align}\n$$\n\nStep 4: Collect the like terms and simplify.\n\n$$\n\\begin{align}\n&\\phantom{000}4 \\times (a + b) \\\\\n&= (a+b) + (a+b) + (a+b) + (a+b) \\\\\n&= a + b + a + b + a + b + a + b \\\\\n&= a + a + a + a + b + b + b + b \\\\\n&= 4a + 4b\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b031",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Exercise 10.6: Remove brackets and simplify"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.6: Remove brackets and simplify\n\nRemove the brackets using repeated addition and then simplify.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b031-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Exercise 10.6: Remove brackets and simplify"
    },
    "content_text": "Source math retained:\n2(h +m)\n\\begin{align}\n &= 2 \\times (h+m) \\\\\n &=(h + m) + (h + m) \\\\\n &= h+m+h+m \\\\\n &= h + h + m + m \\\\\n &=2h + 2m\n \\end{align}",
    "prompt_text": "### Exercise 10.6: Remove brackets and simplify\n\n1. $$\n2(h +m)\n$$",
    "answer_text": "$$\n\\begin{align}\n&= 2 \\times (h+m) \\\\\n&=(h + m) + (h + m) \\\\\n&= h+m+h+m \\\\\n&= h + h + m + m \\\\\n&=2h + 2m\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b031-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Exercise 10.6: Remove brackets and simplify"
    },
    "content_text": "Source math retained:\n3(p +k)\n\\begin{align}\n &= 3 \\times (p+k) \\\\\n &=(p + k) + (p + k) + (p + k) \\\\\n &=p+k+p+k+p+k \\\\\n &= p + p + p  + k + k + k \\\\\n &=3p + 3k\n \\end{align}",
    "prompt_text": "### Exercise 10.6: Remove brackets and simplify\n\n2. $$\n3(p +k)\n$$",
    "answer_text": "$$\n\\begin{align}\n&= 3 \\times (p+k) \\\\\n&=(p + k) + (p + k) + (p + k) \\\\\n&=p+k+p+k+p+k \\\\\n&= p + p + p  + k + k + k \\\\\n&=3p + 3k\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b031-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Exercise 10.6: Remove brackets and simplify"
    },
    "content_text": "Source math retained:\n2(a + 2)\n\\begin{align}\n &= 2 \\times (a+2) \\\\\n &=(a + 2) + (a + 2) \\\\\n &=a+2+a+2 \\\\\n &= a + a + 2+ 2 \\\\\n &=2a + 4\n \\end{align}",
    "prompt_text": "### Exercise 10.6: Remove brackets and simplify\n\n3. $$\n2(a + 2)\n$$",
    "answer_text": "$$\n\\begin{align}\n&= 2 \\times (a+2) \\\\\n&=(a + 2) + (a + 2) \\\\\n&=a+2+a+2 \\\\\n&= a + a + 2+ 2 \\\\\n&=2a + 4\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b031-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Exercise 10.6: Remove brackets and simplify"
    },
    "content_text": "Source math retained:\n3(4x +3y)\n\\begin{align}\n &= 3 \\times (4x+3y) \\\\\n &=(4x + 3y) + (4x + 3y) + (4x + 3y) \\\\\n &=4x+3y+4x+3y+4x+3y \\\\\n &= 4x + 4x + 4x + 3y + 3y + 3y \\\\\n &=12x + 9y\n \\end{align}",
    "prompt_text": "### Exercise 10.6: Remove brackets and simplify\n\n4. $$\n3(4x +3y)\n$$",
    "answer_text": "$$\n\\begin{align}\n&= 3 \\times (4x+3y) \\\\\n&=(4x + 3y) + (4x + 3y) + (4x + 3y) \\\\\n&=4x+3y+4x+3y+4x+3y \\\\\n&= 4x + 4x + 4x + 3y + 3y + 3y \\\\\n&=12x + 9y\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b031-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Exercise 10.6: Remove brackets and simplify"
    },
    "content_text": "Source math retained:\n2(10a - 6b + c)\n\\begin{align}\n &= 2 \\times (10a - 6b + c) \\\\\n &=(10a - 6b + c) + (10a - 6b + c) \\\\\n &=10a - 6b + c + 10a - 6b + c \\\\\n &= 10a + 10a - 6b - 6b + c + c \\\\\n &=20a - 12b + 2c\n \\end{align}",
    "prompt_text": "### Exercise 10.6: Remove brackets and simplify\n\n5. $$\n2(10a - 6b + c)\n$$",
    "answer_text": "$$\n\\begin{align}\n&= 2 \\times (10a - 6b + c) \\\\\n&=(10a - 6b + c) + (10a - 6b + c) \\\\\n&=10a - 6b + c + 10a - 6b + c \\\\\n&= 10a + 10a - 6b - 6b + c + c \\\\\n&=20a - 12b + 2c\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b032",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Negative signs before brackets"
    },
    "content_text": "Up to now we only worked with brackets that have a positive sign in front of them. When there is a negative sign before a bracket, it affects all the terms inside the bracket.\n\nLook at this example:\n\n$$\n10-(2+3)\n$$\n\nWe can simplify it as follows:\n\n$$\n\\begin{align}\n&\\phantom{000}10-(2+3) \\\\\n&=10-5 \\\\\n&=5\n\\end{align}\n$$\n\nThis is the same as:\n\n$$\n\\begin{align}\n&\\phantom{000}10-(2+3) \\\\\n&=10-2-3 \\\\\n&=8-3 \\\\\n&=5\n\\end{align}\n$$\n\nIt is NOT the same as:\n\n$$\n10-(2+3) \\neq 10-2+3 = 11\n$$\n\nSo, if we remove a bracket with a negative sign in front of it, we change the signs of all the terms inside the bracket. Here are some examples:\n\n$$\n5a-(2b+c)=5a-2b-c\n$$\n\n$$\n4x-(-y+2z)=4x+y-2z\n$$\n\n$$\n-(q-2r)+s=-q+2r+s\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b033",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Worked example 10.8: Removing brackets with negative signs in front"
    },
    "content_text": "",
    "prompt_text": "Remove the brackets and then simplify the following expression:\n\n$$\n2(4m+n)-(5m+3n)\n$$",
    "answer_text": "Step 1: Use repeated addition to work out multiplication of brackets.\n\n$$\n\\begin{align}\n&\\phantom{000}2(4m + n)-(5m+3n) \\\\\n&= (4m+n) + (4m+n) - (5m+3n) \\\\\n\\end{align}\n$$\n\nStep 2: Remove the brackets. If there is a negative sign in front of a bracket, change the signs of all the terms inside the bracket.\n\n$$\n\\begin{align}\n&\\phantom{000}2(4m + n)-(5m+3n) \\\\\n&= (4m+n) + (4m+n) - (5m+3n) \\\\\n&=4m+n+4m+n-5m-3n \\\\\n\\end{align}\n$$\n\nStep 3: Collect the like terms and simplify.\n\n$$\n\\begin{align}\n&\\phantom{000}2(4m + n)-(5m+3n) \\\\\n&= (4m+n) + (4m+n) - (5m+3n) \\\\\n&=4m+n+4m+n-5m-3n \\\\\n&=4m+4m-5m+n+n-3n \\\\\n&=3m-n\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b034",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Exercise 10.7: Remove brackets with negative signs and simplify"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.7: Remove brackets with negative signs and simplify\n\nRemove the brackets and then simplify.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b034-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Exercise 10.7: Remove brackets with negative signs and simplify"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.7: Remove brackets with negative signs and simplify\n\nRemove the brackets and then simplify.\n\n1. $$\n3k-(2p +k)\n$$",
    "answer_text": "$$\n\\begin{align}\n&= 3k-2p-k \\\\\n&=3k-k-2p \\\\\n&=2k-2p\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b034-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Exercise 10.7: Remove brackets with negative signs and simplify"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.7: Remove brackets with negative signs and simplify\n\nRemove the brackets and then simplify.\n\n2. $$\n2h +m-(m+2h)-m\n$$",
    "answer_text": "$$\n\\begin{align}\n&= 2h +m-m-2h-m \\\\\n&=2h-2h+m-m-m \\\\\n&=0-m \\\\\n&=-m\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b034-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Exercise 10.7: Remove brackets with negative signs and simplify"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.7: Remove brackets with negative signs and simplify\n\nRemove the brackets and then simplify.\n\n3. $$\n-(4x +3y)+(2x-y)\n$$",
    "answer_text": "$$\n\\begin{align}\n&=-4x - 3y + 2x -y \\\\\n&=-4x+2x-3y-y \\\\\n&=-2x-4y\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b034-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Exercise 10.7: Remove brackets with negative signs and simplify"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.7: Remove brackets with negative signs and simplify\n\nRemove the brackets and then simplify.\n\n4. $$\n3(a + 2)-(4a+2)\n$$",
    "answer_text": "$$\n\\begin{align}\n&=(a + 2) + (a + 2) +(a+2) -(4a+2) \\\\\n&=a+2+a+2+a+2-4a-2 \\\\\n&=a + a + a-4a +2+ 2+2-2 \\\\\n&=-a + 4\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b034-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Exercise 10.7: Remove brackets with negative signs and simplify"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.7: Remove brackets with negative signs and simplify\n\nRemove the brackets and then simplify.\n\n5. $$\n2(10a - 6b + c)-(3c-2b-a)-(b+c)\n$$",
    "answer_text": "$$\n\\begin{align}\n&=(10a - 6b + c) + (10a - 6b + c) -(3c-2b-a)-(b+c) \\\\\n&=10a - 6b + c + 10a - 6b + c -3c+2b+a-b-c \\\\\n&=10a + 10a +a - 6b - 6b +2b -b + c + c -3c-c \\\\\n&=21a - 10b - 2c\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b035",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.4 Working with brackets in algebraic expressions",
      "h3": "Negative signs before brackets"
    },
    "content_text": "When we change the signs of the terms inside a bracket that has a negative sign in front of it, we actually multiply each term by $-1$. You will learn more about this next year.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b036",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": null
    },
    "content_text": "When we have an expression with brackets, we know we need to multiply. When we do the multiplication, we say that we **expand** the expression.\n\nFrom the examples and the exercises above, can you see a shorter way than repeated addition to multiply the expressions? The simpler way is to multiply the coefficient of the bracket by each of the terms that is inside the bracket.\n\nWhen we do this, we are applying the **distributive law**. This law states that:\n\n$$\n4 \\times (3+2) = 4 \\times 3 + 4 \\times 2\n$$\n\nIn other words, 4 groups of $(3 + 2)$ is the same as 4 groups of 3 plus 4 groups of 2. So the $4 \\times$ can be \"distributed\" across the $(3 + 2)$, to get:\n\n$$\n4 =\\times= 3 + 4 =\\times= 2\n$$\n\nBy now you know that $2(a + b) = 2a + 2b$.\n\nNote that the bracket is seen as one \"package\" that can be replaced by one variable. Therefore, the expression $2(a + b)$ has one term, but the expression $2a + 2b$ has two terms.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b037",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": null
    },
    "content_text": "**expand** To expand an algebraic expression is to multiply what is outside the brackets (the coefficient of the bracket) by each of the terms that is inside the bracket.\n\n**distributive law** The distributive law states that the multiplying factor (the coefficient) can be distributed across each of the terms inside a bracket, so $a x (b + c) = a x b + a x c$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b038",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Worked example 10.9: Multiplying the coefficient of a bracket by two terms inside"
    },
    "content_text": "",
    "prompt_text": "Expand this expression:\n\n$$\n3(2a + b)\n$$",
    "answer_text": "Step 1: Multiply the 3 by the first term in the bracket, which is $2a$.\n\nRemember that $2a$ means $2\\times a$.\n\n$$\n3 \\times 2 \\times a = 6 \\times a = 6a\n$$\n\nSo the first term is $6a$.\n\nStep 2: Multiply the 3 by the second term in the bracket, which is $b$.\n\n$$\n3 \\times b = 3b\n$$\n\nThe second term is $3b$.\n\nStep 3: Write the new terms of the expression with the correct operator, which in this case is $+$.\n\n$$\n6a + 3b\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b039",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Worked example 10.10: Multiplying the coefficient of a bracket by three terms inside"
    },
    "content_text": "",
    "prompt_text": "Expand the expression $2(a + 5b - 3c)$.",
    "answer_text": "Step 1: Multiply the 2 by the first term in the bracket.\n\n$$\n2 \\times a = 2a\n$$\n\nStep 2: Multiply the 2 by the second term in the bracket.\n\n$$\n2 \\times 5b = 10b\n$$\n\nStep 3: Multiply the 2 by the third term in the bracket.\n\n$$\n2 \\times 3c = 6c\n$$\n\nStep 4: Write the new terms of the expression with the correct operation signs.\n\n$$\n2a + 10b -6c\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b040",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": null
    },
    "content_text": "When you expand, you do not need to write all the steps separately as shown in the worked examples above. You can go directly to the answer by writing each new term as you work it out. So your answer could look like this: $2(a + 5b - 3c) = 2a + 10b -6c$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b041",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.8: Use the distributive law to expand and simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.8: Use the distributive law to expand and simplify expressions\n\nUse the distributive law to expand the brackets and then simplify the expressions.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b041-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.8: Use the distributive law to expand and simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.8: Use the distributive law to expand and simplify expressions\n\nUse the distributive law to expand the brackets and then simplify the expressions.\n\n1. $$\n3(2 + a - 4x)\n$$",
    "answer_text": "$$\n=6+3a-12x\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b041-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.8: Use the distributive law to expand and simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.8: Use the distributive law to expand and simplify expressions\n\nUse the distributive law to expand the brackets and then simplify the expressions.\n\n2. $$\n5(2n - 16 - m)+4m\n$$",
    "answer_text": "$$\n\\begin{align}\n&=10n-80-5m+4m \\\\\n&=10n-80-m\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b041-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.8: Use the distributive law to expand and simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.8: Use the distributive law to expand and simplify expressions\n\nUse the distributive law to expand the brackets and then simplify the expressions.\n\n3. $$\n2(3x - 3y + 3)+3x-3y+3\n$$",
    "answer_text": "$$\n\\begin{align}\n&=6x-6y+6+3x-3y+3 \\\\\n&=6x+3x-6y-3y+6+3 \\\\\n&=9x-9y+9\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b041-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.8: Use the distributive law to expand and simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.8: Use the distributive law to expand and simplify expressions\n\nUse the distributive law to expand the brackets and then simplify the expressions.\n\n4. $$\n5(3x-4y+z)+3(x+y-2z)\n$$",
    "answer_text": "$$\n\\begin{align}\n&=15x-20y+5z+3x+3y-6z \\\\\n&=15x+3x-20y+3y+5z-6z \\\\\n&=18x-17y-z\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b041-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.8: Use the distributive law to expand and simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.8: Use the distributive law to expand and simplify expressions\n\nUse the distributive law to expand the brackets and then simplify the expressions.\n\n5. $$\n3(12a + 11b + 11c) -(2a - b + c)\n$$",
    "answer_text": "$$\n\\begin{align}\n&=36a+33b+33c-2a+b-c \\\\\n&=36a-2a+33b+b+33c-c \\\\\n&=34a+34b+32c\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b042",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Order of operations"
    },
    "content_text": "In Chapter 9 you were reminded of the correct order of operations that you learnt last year:\n\n1. **B**rackets\n2. **O**f\n3. **D**ivide\n4. **M**ultiply\n5. **A**dd\n6. **S**ubtract",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b043",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Worked example 10.11: Following the correct order of operations"
    },
    "content_text": "",
    "prompt_text": "Simplify the expression $2(3x+5x+1)+4\\times3x$.",
    "answer_text": "Step 1: Simplify the terms inside the bracket first.\n\n$$\n2(8x+1)+4\\times3x\n$$\n\nStep 2: There is no \"of\" or division in the expression, so do multiplication next.\n\nUse the distributive law to multiply the bracket by its coefficient.\n\nRemember that $4\\times3x$ means $4\\times3\\times x$.\n\n$$\n16x+2+12x\n$$\n\nStep 3: Collect the like terms and simplify.\n\n$$\n\\begin{align}\n& 16x+2+12x \\\\\n=& 16x+12x+2 \\\\\n=& 28x+2\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b044",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Worked example 10.12: Following the correct order of operations"
    },
    "content_text": "",
    "prompt_text": "Simplify the expression $(2y+6y)\\div(2\\times2) \\times 10-5\\times2y+2y$.",
    "answer_text": "Step 1: Simplify the terms inside the brackets first.\n\n$$\n8y\\div 4 \\times 10-5\\times2y+2y\n$$\n\nStep 2: There is no \"of\" in the expression, so do division next.\n\nWhen we multiply a term that has a variable by a number, we simply multiply the coefficient of the term by the number. For example $6x \\times 2=12x$. In the same way, when we divide a term that has a variable by a number, we simply divide the coefficient of the term by the number. For example $6x\\div 2=3x$.\n\n$$\n2y \\times 10-5\\times2y+2y\n$$\n\nStep 3: Multiplication comes after division.\n\n$$\n20y-10y+2y\n$$\n\nStep 4: Addition comes after multiplication.\n\n$$\n20y+2y-10y=22y-10y\n$$\n\nStep 5: Do subtraction last.\n\n$$\n12y\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b045",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.9: Follow the correct order of operations to simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.9: Follow the correct order of operations to simplify expressions\n\nSimplify the expressions.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b045-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.9: Follow the correct order of operations to simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.9: Follow the correct order of operations to simplify expressions\n\nSimplify the expressions.\n\n1. $$\n5y-(4y-3y)\n$$",
    "answer_text": "$$\n\\begin{align}\n&=5y-y \\\\\n&=4y\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b045-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.9: Follow the correct order of operations to simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.9: Follow the correct order of operations to simplify expressions\n\nSimplify the expressions.\n\n2. $$\n4x(7 - 2)-(x + 2)\n$$",
    "answer_text": "$$\n\\begin{align}\n&=4x(5)-x-2 \\\\\n&=20x-x-2 \\\\\n&=19x-2\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b045-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.9: Follow the correct order of operations to simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.9: Follow the correct order of operations to simplify expressions\n\nSimplify the expressions.\n\n3. $$\nx(2+3\\times4)-(x+2x)\n$$",
    "answer_text": "$$\n\\begin{align}\n&=x(2+12)-x-2x \\\\\n&=x(14)-x-2x \\\\\n&=14x-x-2x \\\\\n&=11x\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b045-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.9: Follow the correct order of operations to simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.9: Follow the correct order of operations to simplify expressions\n\nSimplify the expressions.\n\n4. $$\n4x\\times 2+3x \\times 9 \\div 3\n$$",
    "answer_text": "$$\n\\begin{align}\n&=4x\\times 2+3x \\times 3 \\\\\n&=8x+9x \\\\\n&=17x \\\\\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b045-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.9: Follow the correct order of operations to simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.9: Follow the correct order of operations to simplify expressions\n\nSimplify the expressions.\n\n5. $$\n2(x+y)-(2x+y-3x)\n$$",
    "answer_text": "$$\n\\begin{align}\n&=2(x+y)-(2x-3x+y) \\\\\n&=2(x+y)-(x+y) \\\\\n&=2x+2y-x-y \\\\\n&=2x-x+2y-y \\\\\n&=x+y\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b045-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.9: Follow the correct order of operations to simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.9: Follow the correct order of operations to simplify expressions\n\nSimplify the expressions.\n\n6. $$\n5y-(4y-4)+2y\\times 3\n$$",
    "answer_text": "$$\n\\begin{align}\n&=5y-(4y-4)+6y \\\\\n&=5y-4y+4+6y \\\\\n&=5y-4y+6y+4 \\\\\n&=11y-4y+4 \\\\\n&=7y+4\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b045-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.9: Follow the correct order of operations to simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.9: Follow the correct order of operations to simplify expressions\n\nSimplify the expressions.\n\n7. $$\n-(p+q)-p+q+2(p-q)\n$$",
    "answer_text": "$$\n\\begin{align}\n&=-p-q-p+q+2p-2q \\\\\n&=-p-p+2p-q+q-2q \\\\\n&=0-2q \\\\\n&=-2q\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b045-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.9: Follow the correct order of operations to simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.9: Follow the correct order of operations to simplify expressions\n\nSimplify the expressions.\n\n8. $$\n-3m(-5+2+3)+2m\\times3\n$$",
    "answer_text": "$$\n\\begin{align}\n&=-3m(-5+5)+2m\\times3 \\\\\n&=-3m(0)+6m \\\\\n&=0+6m \\\\\n&=6m\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b045-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.9: Follow the correct order of operations to simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.9: Follow the correct order of operations to simplify expressions\n\nSimplify the expressions.\n\n9. $$\n8x \\div 2+4\\times 2x+2\n$$",
    "answer_text": "$$\n\\begin{align}\n&=4x+8x+2 \\\\\n&=12x+2\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
  {
    "record_id": "ch10-b045-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 10: Simplifying algebraic expressions",
      "h2": "10.5 Working with brackets using the distributive law",
      "h3": "Exercise 10.9: Follow the correct order of operations to simplify expressions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 10.9: Follow the correct order of operations to simplify expressions\n\nSimplify the expressions.\n\n10. $$\n3(-2a + b + c + 4a - 2b + c)-(a - b - c)\n$$",
    "answer_text": "$$\n\\begin{align}\n&=3(-2a+4a+b-2b+c+c)-(a-b-c) \\\\\n&=3(2a-b+2c)-(a-b-c) \\\\\n&=6a-3b+6c-a+b+c \\\\\n&=6a-a-3b+b+6c+c \\\\\n&=5a-2b+7c\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-simplification-of-algebraic-expressions-use-of-brackets"
  },
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
