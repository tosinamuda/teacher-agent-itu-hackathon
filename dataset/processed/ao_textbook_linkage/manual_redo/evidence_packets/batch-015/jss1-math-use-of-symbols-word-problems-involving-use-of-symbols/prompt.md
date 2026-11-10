# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-3",
  "topic_key": "jss1-math-use-of-symbols",
  "topic": "Use of Symbols",
  "subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols",
  "subtopic_title": "Word problems involving use of symbols",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols-po01",
        "source_performance_objective_index": 1,
        "text": "Solve word problems involving use of symbols"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "word-problems-use-of-symbols-ao-solve-problems",
          "text": "Solve word problems involving use of symbols."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch09-b027",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": null
    },
    "content_text": "We can use open sentences with variables to set out and solve problems that are described in words. Remember that we can translate the following words into mathematical operations:\n\n| English | Mathematical symbol |\n| --- | --- |\n| sum of | + |\n| difference | $-$ |\n| product | $\\times$ |\n| quotient | $\\div$ |\n\nWhen you need to solve a problem that is described in words, follow these steps:\n\n1. **Understand the problem:** Read the question carefully a few times. Identify the information you have. Make sure you know what is asked. It may help to draw a picture.\n2. **Make a plan:** Write a number sentence that you can use to solve the problem.\n3. **Carry out the plan:** Solve the number sentence.\n4. **Look back:** Make sure that your answer is what you were asked to calculate. Check that your answer makes sense.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b028",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Worked example 9.7: Solving a problem using open sentences"
    },
    "content_text": "Usman is 1.8 m tall and his sister Jummai is y m tall. The difference in their heights is 0.4 m. How tall is Jummai if she is shorter than Usman?",
    "prompt_text": "There are 32 students in one JSS1 class. If 20 of the students are boys, how many girls are there in this class?",
    "answer_text": "Step 1: Understand the problem.\n\n- total students: 32\n- boys: 20\n- girls: asked\n\nStep 2: Devise a plan.\n\n$$\n\\begin{align}\n \\text{total students} &= \\text{girls} + \\text{boys}\\newline\n 32 &= g + 20\n\\end{align}\n$$\n\nStep 3: Carry out the plan.\n\n$$\n\\begin{align}\n 32 &= g + 20  \\\\\n 32 - 20 &= g + 20 - 20 \\\\\n 12 &= g \\\\\n g &= 12\n\\end{align}\n$$\n\nStep 4: Look back.\n\n$$12+20=32$$\n\nThe answer is correct. There are 12 girls in the class.",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b029",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Worked example 9.8: Solving a problem using open sentences"
    },
    "content_text": "",
    "prompt_text": "For six days of the week, Ndidi spends the same amount of time each day practising the violin. On the last day of the week, she practises only 30 minutes. Her total practice time for the week is 300 minutes. For how many minutes does Ndidi practise the violin each day of the first six weekdays?",
    "answer_text": "Step 1: Understand the problem.\n\n- total time: 300 minutes\n- last day: 30 minutes\n- six days: equal minutes\n\nStep 2: Devise a plan.\n\n$$\n\\begin{align}\n \\text{total time} &= 6 \\times \\text{asked} + 30\\newline\n 300 &= 6 \\times x + 30\n\\end{align}\n$$\n\nStep 3: Carry out the plan.\n\n$$\n\\begin{align}\n 300 &= (6 \\times x) + 30  \\\\\n 300 - 30 &= (6 \\times x) + 30 - 30 \\\\\n 270 &= 6 \\times x \\\\\n 270 \\div 6 &= 6 \\div 6 \\times x \\\\\n 45 &= x \\\\\n x &= 45\n\\end{align}\n$$\n\nStep 4: Look back.\n\n$$45 \\text{ minutes} \\times 6 \\text{ days} = 270 \\text{ minutes}$$\n$$270 \\text{ minutes} + 30 \\text{ minutes} = 300 \\text{ minutes}$$\n\nThe answer is correct. She practises for 45 minutes per day for the first six days of the week.",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b030",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Exercise 9.6: Use open sentences to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.6: Use open sentences to solve problems",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b030-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Exercise 9.6: Use open sentences to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.6: Use open sentences to solve problems\n\n1. Two numbers add up to 28. One of the numbers is 10. What is the other number?",
    "answer_text": "$$\n\\begin{align}\nx + 10 &= 28 \\\\\nx &= 28 - 10 \\\\\nx &= 18\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b030-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Exercise 9.6: Use open sentences to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.6: Use open sentences to solve problems\n\n2. The product of two numbers is 840. One of the numbers is 12. What is the other number?",
    "answer_text": "$$\n\\begin{align}\nx \\times 12 &= 240 \\\\\nx &= 240 \\div 12 \\\\\nx &= 20\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b030-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Exercise 9.6: Use open sentences to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.6: Use open sentences to solve problems\n\n3. 1,025 divided by a certain number gives a quotient (answer after dividing) of 25. What is the other number?",
    "answer_text": "$$\n\\begin{align}\n1,025 \\div x &= 25 \\\\\n1,025 &= 25 \\times x \\\\\n1,025 \\div 25 &= x \\\\\nx &= 41\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b030-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Exercise 9.6: Use open sentences to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.6: Use open sentences to solve problems\n\n4. The difference between two numbers is 17. If the larger number is 67, what is the smaller number?",
    "answer_text": "$$\n\\begin{align}\n67 - x &= 17 \\\\\n67 - 17 &= x \\\\\nx &= 50\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b030-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Exercise 9.6: Use open sentences to solve problems"
    },
    "content_text": "Usman is 1.8 m tall and his sister Jummai is y m tall. The difference in their heights is 0.4 m. How tall is Jummai if she is shorter than Usman?",
    "prompt_text": "### Exercise 9.6: Use open sentences to solve problems\n\n5. Usman is 1.8 m tall and his sister Jummai is $y$ m tall. The difference in their heights is 0.4 m. How tall is Jummai if she is shorter than Usman?",
    "answer_text": "$$\n\\begin{align}\n1.8 - y &= 0.4 \\\\\n1.8 &= 0.4 + y \\\\\n1.8 - 0.4 &= y \\\\\ny &= 1.4\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b030-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Exercise 9.6: Use open sentences to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.6: Use open sentences to solve problems\n\n6. A farmer has 24 rows of apple trees in his apple orchard. Each row has the same number of apple trees. If he has a total of 480 apple trees, how many trees are there in each row?",
    "answer_text": "$$\n\\begin{align}\n24 \\times t &= 480 \\\\\nt &= 480 \\div 24 \\\\\nt &= 20\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b030-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Exercise 9.6: Use open sentences to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.6: Use open sentences to solve problems\n\n7. The sum of three numbers is 208. One of the numbers is 88 and the other number is half of 88. What is the third number?",
    "answer_text": "$$\n\\begin{align}\n88 + 44 + x &= 208 \\\\\nx &= 208 - 132 \\\\\nx &= 76\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b030-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Exercise 9.6: Use open sentences to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.6: Use open sentences to solve problems\n\n8. Two sisters add their ages and see that they are 100 years old together. The younger sister is 45. How old is her older sister?",
    "answer_text": "$$\n\\begin{align}\n45 + x &= 100 \\\\\nx &= 100 - 45 \\\\\nx &= 55\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b030-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Exercise 9.6: Use open sentences to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.6: Use open sentences to solve problems\n\n9. A mother has 4 children. She wants to divide 35 sweets equally among them. If every child receives 8 sweets, how many are left over?",
    "answer_text": "$$\n\\begin{align}\n 4 \\times 8 + x &= 35  \\\\\n 32 + x &= 35 \\\\\n 32 - 32 + x &= 35 - 32 \\\\\n x &= 3\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b030-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Exercise 9.6: Use open sentences to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.6: Use open sentences to solve problems\n\n10. There are 126 plates of food available at a party. There are 38 guests at the party and they each receive the same amount of food. The family who hosts the party gets 12 plates of food. How many plates of food does each guest get?",
    "answer_text": "$$\n\\begin{align}\n38 \\times x + 12 &= 126  \\\\\n(38 \\times x) + 12 - 12 &= 126 - 12 \\\\\n38 \\times x &= 114 \\\\\n38 \\div 38 \\times x &= 114 \\div 38 \\\\\nx &= 3\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b031",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.4 Summary",
      "h3": null
    },
    "content_text": "- A closed number sentence is always true or always false.\n- In an open number sentence, there is some information missing that we need to find.\n- An open number sentence can use picture symbols or variables to show which information is missing.\n- The value of a variable can vary.\n- Finding the missing information, or finding the value of the variable, is called solving an open sentence.\n- We can solve an open sentence using mental maths or using the inverse operation.\n- We can use open sentences to solve problems described in words.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
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
  "topic_key": "jss1-math-use-of-symbols",
  "topic": "Use of Symbols",
  "subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols",
  "subtopic_title": "Word problems involving use of symbols",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols-po01",
        "source_performance_objective_index": 1,
        "text": "Solve word problems involving use of symbols"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "word-problems-use-of-symbols-ao-solve-problems",
          "text": "Solve word problems involving use of symbols."
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
    "record_id": "ch09-b027",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": null
    },
    "content_text": "We can use open sentences with variables to set out and solve problems that are described in words. Remember that we can translate the following words into mathematical operations:\n\n| English | Mathematical symbol |\n| --- | --- |\n| sum of | + |\n| difference | $-$ |\n| product | $\\times$ |\n| quotient | $\\div$ |\n\nWhen you need to solve a problem that is described in words, follow these steps:\n\n1. **Understand the problem:** Read the question carefully a few times. Identify the information you have. Make sure you know what is asked. It may help to draw a picture.\n2. **Make a plan:** Write a number sentence that you can use to solve the problem.\n3. **Carry out the plan:** Solve the number sentence.\n4. **Look back:** Make sure that your answer is what you were asked to calculate. Check that your answer makes sense.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b028",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Worked example 9.7: Solving a problem using open sentences"
    },
    "content_text": "Usman is 1.8 m tall and his sister Jummai is y m tall. The difference in their heights is 0.4 m. How tall is Jummai if she is shorter than Usman?",
    "prompt_text": "There are 32 students in one JSS1 class. If 20 of the students are boys, how many girls are there in this class?",
    "answer_text": "Step 1: Understand the problem.\n\n- total students: 32\n- boys: 20\n- girls: asked\n\nStep 2: Devise a plan.\n\n$$\n\\begin{align}\n \\text{total students} &= \\text{girls} + \\text{boys}\\newline\n 32 &= g + 20\n\\end{align}\n$$\n\nStep 3: Carry out the plan.\n\n$$\n\\begin{align}\n 32 &= g + 20  \\\\\n 32 - 20 &= g + 20 - 20 \\\\\n 12 &= g \\\\\n g &= 12\n\\end{align}\n$$\n\nStep 4: Look back.\n\n$$12+20=32$$\n\nThe answer is correct. There are 12 girls in the class.",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b029",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Worked example 9.8: Solving a problem using open sentences"
    },
    "content_text": "",
    "prompt_text": "For six days of the week, Ndidi spends the same amount of time each day practising the violin. On the last day of the week, she practises only 30 minutes. Her total practice time for the week is 300 minutes. For how many minutes does Ndidi practise the violin each day of the first six weekdays?",
    "answer_text": "Step 1: Understand the problem.\n\n- total time: 300 minutes\n- last day: 30 minutes\n- six days: equal minutes\n\nStep 2: Devise a plan.\n\n$$\n\\begin{align}\n \\text{total time} &= 6 \\times \\text{asked} + 30\\newline\n 300 &= 6 \\times x + 30\n\\end{align}\n$$\n\nStep 3: Carry out the plan.\n\n$$\n\\begin{align}\n 300 &= (6 \\times x) + 30  \\\\\n 300 - 30 &= (6 \\times x) + 30 - 30 \\\\\n 270 &= 6 \\times x \\\\\n 270 \\div 6 &= 6 \\div 6 \\times x \\\\\n 45 &= x \\\\\n x &= 45\n\\end{align}\n$$\n\nStep 4: Look back.\n\n$$45 \\text{ minutes} \\times 6 \\text{ days} = 270 \\text{ minutes}$$\n$$270 \\text{ minutes} + 30 \\text{ minutes} = 300 \\text{ minutes}$$\n\nThe answer is correct. She practises for 45 minutes per day for the first six days of the week.",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b030",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Exercise 9.6: Use open sentences to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.6: Use open sentences to solve problems",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b030-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Exercise 9.6: Use open sentences to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.6: Use open sentences to solve problems\n\n1. Two numbers add up to 28. One of the numbers is 10. What is the other number?",
    "answer_text": "$$\n\\begin{align}\nx + 10 &= 28 \\\\\nx &= 28 - 10 \\\\\nx &= 18\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b030-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Exercise 9.6: Use open sentences to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.6: Use open sentences to solve problems\n\n2. The product of two numbers is 840. One of the numbers is 12. What is the other number?",
    "answer_text": "$$\n\\begin{align}\nx \\times 12 &= 240 \\\\\nx &= 240 \\div 12 \\\\\nx &= 20\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b030-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Exercise 9.6: Use open sentences to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.6: Use open sentences to solve problems\n\n3. 1,025 divided by a certain number gives a quotient (answer after dividing) of 25. What is the other number?",
    "answer_text": "$$\n\\begin{align}\n1,025 \\div x &= 25 \\\\\n1,025 &= 25 \\times x \\\\\n1,025 \\div 25 &= x \\\\\nx &= 41\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b030-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Exercise 9.6: Use open sentences to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.6: Use open sentences to solve problems\n\n4. The difference between two numbers is 17. If the larger number is 67, what is the smaller number?",
    "answer_text": "$$\n\\begin{align}\n67 - x &= 17 \\\\\n67 - 17 &= x \\\\\nx &= 50\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b030-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Exercise 9.6: Use open sentences to solve problems"
    },
    "content_text": "Usman is 1.8 m tall and his sister Jummai is y m tall. The difference in their heights is 0.4 m. How tall is Jummai if she is shorter than Usman?",
    "prompt_text": "### Exercise 9.6: Use open sentences to solve problems\n\n5. Usman is 1.8 m tall and his sister Jummai is $y$ m tall. The difference in their heights is 0.4 m. How tall is Jummai if she is shorter than Usman?",
    "answer_text": "$$\n\\begin{align}\n1.8 - y &= 0.4 \\\\\n1.8 &= 0.4 + y \\\\\n1.8 - 0.4 &= y \\\\\ny &= 1.4\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b030-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Exercise 9.6: Use open sentences to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.6: Use open sentences to solve problems\n\n6. A farmer has 24 rows of apple trees in his apple orchard. Each row has the same number of apple trees. If he has a total of 480 apple trees, how many trees are there in each row?",
    "answer_text": "$$\n\\begin{align}\n24 \\times t &= 480 \\\\\nt &= 480 \\div 24 \\\\\nt &= 20\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b030-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Exercise 9.6: Use open sentences to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.6: Use open sentences to solve problems\n\n7. The sum of three numbers is 208. One of the numbers is 88 and the other number is half of 88. What is the third number?",
    "answer_text": "$$\n\\begin{align}\n88 + 44 + x &= 208 \\\\\nx &= 208 - 132 \\\\\nx &= 76\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b030-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Exercise 9.6: Use open sentences to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.6: Use open sentences to solve problems\n\n8. Two sisters add their ages and see that they are 100 years old together. The younger sister is 45. How old is her older sister?",
    "answer_text": "$$\n\\begin{align}\n45 + x &= 100 \\\\\nx &= 100 - 45 \\\\\nx &= 55\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b030-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Exercise 9.6: Use open sentences to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.6: Use open sentences to solve problems\n\n9. A mother has 4 children. She wants to divide 35 sweets equally among them. If every child receives 8 sweets, how many are left over?",
    "answer_text": "$$\n\\begin{align}\n 4 \\times 8 + x &= 35  \\\\\n 32 + x &= 35 \\\\\n 32 - 32 + x &= 35 - 32 \\\\\n x &= 3\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b030-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Exercise 9.6: Use open sentences to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.6: Use open sentences to solve problems\n\n10. There are 126 plates of food available at a party. There are 38 guests at the party and they each receive the same amount of food. The family who hosts the party gets 12 plates of food. How many plates of food does each guest get?",
    "answer_text": "$$\n\\begin{align}\n38 \\times x + 12 &= 126  \\\\\n(38 \\times x) + 12 - 12 &= 126 - 12 \\\\\n38 \\times x &= 114 \\\\\n38 \\div 38 \\times x &= 114 \\div 38 \\\\\nx &= 3\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-word-problems-involving-use-of-symbols"
  },
  {
    "record_id": "ch09-b031",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.4 Summary",
      "h3": null
    },
    "content_text": "- A closed number sentence is always true or always false.\n- In an open number sentence, there is some information missing that we need to find.\n- An open number sentence can use picture symbols or variables to show which information is missing.\n- The value of a variable can vary.\n- Finding the missing information, or finding the value of the variable, is called solving an open sentence.\n- We can solve an open sentence using mental maths or using the inverse operation.\n- We can use open sentences to solve problems described in words.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
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
