# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-3",
  "topic_key": "jss1-math-use-of-symbols",
  "topic": "Use of Symbols",
  "subtopic_id": "jss1-math-use-of-symbols-open-sentences",
  "subtopic_title": "Open sentences",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-use-of-symbols-open-sentences-po01",
        "source_performance_objective_index": 1,
        "text": "Solve problems expressed in open sentences"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "open-sentences-ao-solve-problems",
          "text": "Solve problems expressed in open sentences."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-use-of-symbols-open-sentences-po02",
        "source_performance_objective_index": 2,
        "text": "Identify the relationship between addition and subtraction; multiplication and division"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "open-sentences-ao-identify-relationship-addition-and-subtraction",
          "text": "Identify the relationship between addition and subtraction."
        },
        {
          "atomic_objective_id": "open-sentences-ao-identify-relationship-multiplication-and-division",
          "text": "Identify the relationship between multiplication and division."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch09-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Closed number sentences",
      "h3": "Closed number sentences"
    },
    "content_text": "A number sentence is a group of numbers and mathematical symbols (such as +, -, or =) that gives information about the numbers. Here is an example of a number sentence: 3 + 4 = 7. This is called a closed number sentence, because all the information is given in the sentence. This closed number sentence is always true. Here is an example of a closed number sentence that is false: 5 + 8 = 2.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b002",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Closed number sentences",
      "h3": "Closed number sentences"
    },
    "content_text": "closed number sentence\nA closed number sentence gives all the information about the numbers, and it is always true or always false.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b003",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Closed number sentences",
      "h3": "Closed number sentences"
    },
    "content_text": "Here are some more examples of closed number sentences: 9 \\div 3 = 3 (true), 7\\times 12 = 84 (true), 4 \\times 8 = 8 + 8 + 8 + 8 + 8 (false).",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b004",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Closed number sentences",
      "h3": "Exercise 9.1: Decide whether closed sentences are true or false"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.1: Decide whether closed sentences are true or false\n\nState whether the closed sentence is always true or false.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b004-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Closed number sentences",
      "h3": "Exercise 9.1: Decide whether closed sentences are true or false"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.1: Decide whether closed sentences are true or false\n\n1. 4\\times 10 = 40",
    "answer_text": "True",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b004-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Closed number sentences",
      "h3": "Exercise 9.1: Decide whether closed sentences are true or false"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.1: Decide whether closed sentences are true or false\n\n2. 102\\div 2 = 12",
    "answer_text": "False",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b004-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Closed number sentences",
      "h3": "Exercise 9.1: Decide whether closed sentences are true or false"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.1: Decide whether closed sentences are true or false\n\n3. 30 + 30 + 30 = 3\\times 30",
    "answer_text": "True",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b004-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Closed number sentences",
      "h3": "Exercise 9.1: Decide whether closed sentences are true or false"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.1: Decide whether closed sentences are true or false\n\n4. 9\\div 18 = 2",
    "answer_text": "False",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b004-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Closed number sentences",
      "h3": "Exercise 9.1: Decide whether closed sentences are true or false"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.1: Decide whether closed sentences are true or false\n\n5. 9\\div 18 = \\frac{1}{2}",
    "answer_text": "True",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b005",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Open number sentences",
      "h3": "Open number sentences"
    },
    "content_text": "Here is another example of a number sentence: \\square + 3 = 7. This is called an open number sentence, because not all the information is given in the sentence. We do not know if this sentence is true or false because we do not know what is in the box.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b006",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Open number sentences",
      "h3": "Open number sentences"
    },
    "content_text": "open number sentence\nAn open number sentence does not give all the information about the numbers, but has information missing that we must find.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b007",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Worked example 9.1: Finding missing information in an open sentence"
    },
    "content_text": "",
    "prompt_text": "Find the value of the square in this open number sentence:\n\n$$\n\\square + 3 = 7\n$$",
    "answer_text": "Step 1: Ask yourself the question, \"What do I need to add to 3 to get 7?\"\n\nUsing your knowledge and mental maths, you will find that you need to add 4 to 3 to get 7.\n\nStep 2: Write down the value of the square.\n\n$$\n\\square = 4\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b008",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.2: Find missing information in open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.2: Find missing information in open sentences\n\nFor each open number sentence, find the number that makes the sentence true.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b008-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.2: Find missing information in open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.2: Find missing information in open sentences\n\n1. $$17 - 9 = \\square$$",
    "answer_text": "8",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b008-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.2: Find missing information in open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.2: Find missing information in open sentences\n\n2. $$3 + 9 = \\square$$",
    "answer_text": "12",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b008-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.2: Find missing information in open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.2: Find missing information in open sentences\n\n3. $$2\\times 12 = \\square$$",
    "answer_text": "24",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b008-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.2: Find missing information in open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.2: Find missing information in open sentences\n\n4. $$9-\\square= 2$$",
    "answer_text": "7",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b008-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.2: Find missing information in open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.2: Find missing information in open sentences\n\n5. $$\\bigcirc=\\frac{1}{2}+ \\frac{1}{2}$$",
    "answer_text": "1",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b008-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.2: Find missing information in open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.2: Find missing information in open sentences\n\n6. $$10\\times\\square = 100$$",
    "answer_text": "10",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b008-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.2: Find missing information in open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.2: Find missing information in open sentences\n\n7. $$63\\div9=\\square$$",
    "answer_text": "7",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b008-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.2: Find missing information in open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.2: Find missing information in open sentences\n\n8. $$30 + 30 + \\bigcirc = 3\\times 30$$",
    "answer_text": "30",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b008-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.2: Find missing information in open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.2: Find missing information in open sentences\n\n9. $$\\square\\times6=30$$",
    "answer_text": "5",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b008-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.2: Find missing information in open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.2: Find missing information in open sentences\n\n10. $$5 + \\bigcirc + 18 = 30$$",
    "answer_text": "7",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b009",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Variables in open sentences"
    },
    "content_text": "So far we have worked with open sentences that contain a symbol such as a $\\square$ or a $\\bigcirc$. Instead of pictures like these, in mathematics it works better to use letters to represent missing information. These letters are called **variables**, because their value can vary.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b010",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Variables in open sentences"
    },
    "content_text": "**variable** A variable is a symbol for a number we do not know yet. It is usually a letter such as $x$ or $y$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b011",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Variables in open sentences"
    },
    "content_text": "If we have an expression, such as $x+5$, we cannot know the value of the $x$ unless it is given. If we give the $x$ different values, then we can make number sentences that are true.\n\nIf $x$ = 1, then $x+5 = 1 + 5 = 6$\n\nIf $x$ = 3, then $x+5 = 3 + 5 = 8$\n\nIf $x$ = 0, then $x+5 = 0 + 5 = 0$\n\nThe value of the $x$ can vary, and that is why it is called a variable.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b012",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.3: Find the value of the expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.3: Find the value of the expression\n\nFind the value of the following expressions if $x=3$.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b012-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.3: Find the value of the expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.3: Find the value of the expression\n\n1. $$17 - x$$",
    "answer_text": "14",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b012-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.3: Find the value of the expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.3: Find the value of the expression\n\n2. $$3 + x$$",
    "answer_text": "6",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b012-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.3: Find the value of the expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.3: Find the value of the expression\n\n3. $$2\\times x\\times 0$$",
    "answer_text": "0",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b012-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.3: Find the value of the expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.3: Find the value of the expression\n\n4. $$9-x+2$$",
    "answer_text": "8",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b012-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.3: Find the value of the expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.3: Find the value of the expression\n\n5. $$\\frac{1}{x}+ \\frac{1}{x}$$",
    "answer_text": "\\frac{2}{3}",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b012-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.3: Find the value of the expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.3: Find the value of the expression\n\n6. $$10\\times x$$",
    "answer_text": "30",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b012-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.3: Find the value of the expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.3: Find the value of the expression\n\n7. $$60\\div x$$",
    "answer_text": "20",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b012-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.3: Find the value of the expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.3: Find the value of the expression\n\n8. $$30 + 30 + x$$",
    "answer_text": "63",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b012-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.3: Find the value of the expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.3: Find the value of the expression\n\n9. $$x\\times6$$",
    "answer_text": "18",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b012-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.3: Find the value of the expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.3: Find the value of the expression\n\n10. $$5 + x + 18$$",
    "answer_text": "26",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b013",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences that have variables",
      "h3": null
    },
    "content_text": "Variables and open sentences form part of a section of mathematics we call algebra. To show that there is information that we must find, an open sentence can use a picture symbol (such as a box or a circle) or a variable (a letter representing any number).\n\nHere are some examples of open sentences using variables:\n\n$$\n3 + x = 5\n$$\n$$\np - 4 = -3\n$$\n$$\nn - 17 = 20\n$$\n$$\n3 \\times y = 15\n$$\n$$\nb \\div 20 = 5\n$$\n\nIn these open sentences, we can find the correct value for the unknown variable that will make the sentence true. This is called solving the open sentence.\n\nIf the sentence that you need to be solve is straightforward, one option is to use mental maths to solve it.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b014",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences that have variables",
      "h3": "Worked example 9.2: Finding the value of a variable using mental maths"
    },
    "content_text": "",
    "prompt_text": "Find the value of $x$ in this open number sentence:\n\n$$\nx + 7 = 9\n$$",
    "answer_text": "Step 1: You need to find the value of $x$ that will make the statement true. To do this, you can ask yourself the question, \"What number added to 7 will give me 9?\"\n\nUsing your knowledge and mental maths, you will find that you need to add 2 to 7 to get 9.\n\nStep 2: This means that the value of $x$ is 2, so write your answer:\n\n$$\nx=2\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b015",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences that have variables",
      "h3": "Using inverse operations to solve open sentences"
    },
    "content_text": "Another way to find the value of $x$ in $x + 7 = 9$, is to use the **inverse operation** of addition. The inverse operation of addition is subtraction. In Chapter 5 you learnt that subtraction may be seen as another form of addition. For example, $6-4$ is the same as $6+(-4)$. The numbers $4$ and $-4$ are called additive inverses. When we add them, the answer is zero: $4+(-4)=0$.\n\nThe inverse operation of multiplication is division. In Chapter 6 you learnt that dividing by a fraction is the same as multiplying by the reciprocal of the fraction. For example, $4\\div\\frac{2}{3}$ is the same as $4\\times\\frac{3}{2}$. A fraction and its reciprocal are called multiplicative inverses. When we multiply them, the answer is 1: $\\frac{2}{3}\\times\\frac{3}{2}=1$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b016",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences that have variables",
      "h3": "Using inverse operations to solve open sentences"
    },
    "content_text": "**inverse operation**\nAn inverse operation does the opposite of another operation. Addition and subtraction are inverse operations, and multiplication and division are inverse operations.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b017",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences that have variables",
      "h3": "Using inverse operations to solve open sentences"
    },
    "content_text": "This closed number sentence is true:\n\n$$\n2 + 7 = 9\n$$\n\nWe know that this closed number sentence is also true:\n\n$$\n2 = 9 - 7\n$$\n\nNotice that we get from the first number sentence to the second number sentence using the inverse operation of addition, which is subtraction:\n\n$$\n\\begin{align}\n2 + 7 &= 9 \\\\\n2 + 7\\, \\color{red}{-\\;7} &= 9\\space \\color{red}{-\\;7} \\\\\n2 + 0 &= 9 - 7 \\\\\n2 &= 9 - 7\n\\end{align}\n$$\n\nHere is an example of a closed number sentence using multiplication:\n\n$$\n2 \\times 3 = 6\n$$\n\nWe know that this closed number sentence is also true:\n\n$$\n2 = 6 \\div 3\n$$\n\nNotice that we get from the first number sentence to the second number sentence using the inverse operation of multiplication, which is division:\n\n$$\n\\begin{align}\n2 \\times 3 &= 6 \\\\\n2 \\times 3\\; \\color{red}{\\div\\;3} &= 6\\space \\color{red}{\\div\\;3} \\\\\n2 \\times 1 &= 6 \\div 3 \\\\\n2 &= 6 \\div 3\n\\end{align}\n$$\n\nWe may use inverse operations to find the value of a variable in an open number sentence. We aim to write the number sentence in this format:\n\n$$\nvariable=\\text{value}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b018",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences that have variables",
      "h3": "Worked example 9.3: Solving an open sentence using the inverse of addition"
    },
    "content_text": "",
    "prompt_text": "Find the value of $x$ in this open sentence:\n\n$$\nx + 12 = 29\n$$",
    "answer_text": "Step 1: Use an inverse operation for any number that is added to or subtracted from the variable.\n\n$$\nx + 12 - 12 = 29 - 12\n$$\n\nStep 2: Simplify the sentence from Step 1 until you get to the format $\\boldsymbol{variable}=\\textbf{ value}$.\n\n$$\n\\begin{align}\nx + 12 - 12 &= 29 - 12 \\\\\nx  + 0 &= 17 \\\\\nx &= 17\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b019",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences that have variables",
      "h3": "Worked example 9.4: Solving an open sentence using the inverse of multiplication"
    },
    "content_text": "",
    "prompt_text": "Find the value of $y$ in this open sentence:\n\n$$\ny \\times 3 = 27\n$$",
    "answer_text": "Step 1: Use an inverse operation for any number that the variable is multiplied or divided by.\n\n$$\ny \\times 3 \\div 3 = 27 \\div 3\n$$\n\nStep 2: Simplify the number sentence from Step 1 until you get to the format $\\boldsymbol{variable}=\\textbf{ value}$.\n\n$$\n\\begin{align}\ny \\times 3 \\div 3 &= 27 \\div 3 \\\\\ny \\times 1 &= 9 \\\\\ny &= 9\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b020",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences that have variables",
      "h3": "Using inverse operations to solve open sentences"
    },
    "content_text": "Note that an open sentence is not regarded as solved when the variable is negative, for example $-x=5$. The variable must be positive in your final answer, for example $x=-5$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b021",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences that have variables",
      "h3": "Using inverse operations to solve open sentences"
    },
    "content_text": "The format $variable=\\text{value}$ may be swapped around. Therefore, $x=7$ and $7=x$ has the same meaning.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b022",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences that have variables",
      "h3": "Worked example 9.5: Solving an open sentence using the inverse operation on the variable"
    },
    "content_text": "",
    "prompt_text": "Find the value of $x$:\n\n$$\n18 -  x = 14\n$$",
    "answer_text": "Step 1: Use an inverse operation to get a positive variable.\n\n$$\n18 -x + x= 14 + x\n$$\n\nStep 2: Simplify the number sentence from Step 1 until it has only one positive variable.\n\n$$\n\\begin{align}\n 18 -x + x &= 14 + x \\\\\n 18 + 0 &= 14 + x \\\\\n 18 &= 14 + x\n \\end{align}\n$$\n\nStep 3: Use an inverse operation for the number that is added to or subtracted from the variable.\n\n$$\n18 - 14 = 14 - 14 + x\n$$\n\nStep 4: Simplify the number sentence from Step 1 until you get to the format $\\boldsymbol{variable}=\\textbf{ value}$.\n\n$$\n\\begin{align}\n18 - 14 &= 14 -14 + x \\\\\n4 &= 0 + x \\\\\n4 &= x \\\\\nx &= 4\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b023",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.4: Solve open sentences"
    },
    "content_text": "Usman is 1.8 m tall and his sister Jummai is y m tall. The difference in their heights is 0.4 m. How tall is Jummai if she is shorter than Usman?",
    "prompt_text": "### Exercise 9.4: Solve open sentences\n\nFind the value of the variable in the following open sentences:",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b023-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.4: Solve open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.4: Solve open sentences\n\n1. y + 7 = 30",
    "answer_text": "$$\n\\begin{align}\n y + 7 - 7 &= 30 - 7 \\\\\n y &= 23\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b023-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.4: Solve open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.4: Solve open sentences\n\n2. 3 + x = 15",
    "answer_text": "$$\n\\begin{align}\n 3 - 3 + x &= 15 - 3 \\\\\n x &= 12\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b023-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.4: Solve open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.4: Solve open sentences\n\n3. z - 8 = 20",
    "answer_text": "$$\n\\begin{align}\n z - 8 + 8 &= 20 + 8 \\\\\n z &= 28\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b023-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.4: Solve open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.4: Solve open sentences\n\n4. q  - 4 = -5",
    "answer_text": "$$\n\\begin{align}\n q - 4 + 4 &= -5 + 4 \\\\\n q &= -1\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b023-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.4: Solve open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.4: Solve open sentences\n\n5. 17 - n = 20",
    "answer_text": "$$\n\\begin{align}\n 17 - n + n &= 20 + n \\\\\n 17 &= 20 + n  \\\\\n 17 - 20 &= 20 - 20 + n \\\\\n 3 &= n \\\\\n n &= 3\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b023-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.4: Solve open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.4: Solve open sentences\n\n6. 15 - p = -5",
    "answer_text": "$$\n\\begin{align}\n 15 - p + p &= -5 + p \\\\\n 15 &= -5 + p  \\\\\n 15 + 5 &= -5 + 5 + p \\\\\n 20 &= p \\\\\n p &= 20\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b023-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.4: Solve open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.4: Solve open sentences\n\n7. x \\times 8 = 48",
    "answer_text": "$$\n\\begin{align}\n x \\times 8 \\div 8 &= 48 \\div 8 \\\\\n x &= 6  \\\\\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b023-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.4: Solve open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.4: Solve open sentences\n\n8. 3 \\times y = 15",
    "answer_text": "$$\n\\begin{align}\n 3 \\div 3 \\times y &= 15 \\div 3 \\\\\n y &= 5  \\\\\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b023-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.4: Solve open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.4: Solve open sentences\n\n9. c\\div 20 = 5",
    "answer_text": "$$\n\\begin{align}\n c \\div 20 \\times 20 &= 5 \\times 20 \\\\\n c &= 100  \\\\\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b023-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.4: Solve open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.4: Solve open sentences\n\n10. 40 \\div x = 8",
    "answer_text": "$$\n\\begin{align}\n40 \\div x \\times x &= 8 \\times x \\\\\n40 &= 8 \\times x  \\\\\n40 \\div 8 &= 8 \\div 8 \\times x \\\\\n5 &= x \\\\\nx &= 5\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b024",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": null
    },
    "content_text": "Open number sentences may have more than one operation, for example $4-2+x=10$. To solve number sentences like these, you must remember the correct order of operations that you learnt last year:\n\n1. **B**rackets\n2. **O**f\n3. **D**ivide\n4. **M**ultiply\n5. **A**dd\n6. **S**ubtract",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b025",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Worked example 9.7: Solving a problem using open sentences"
    },
    "content_text": "",
    "prompt_text": "Find the value of x:",
    "answer_text": "$$\nx \\div 2 + 3 = 8\n$$\n\nStep 1: Decide which inverse operation to do first.\n\nAccording to the order BODMAS, you must calculate $x \\div 2$ before $2+3$.\nThis means $x \\div 2$ must \"stay together\". You may insert brackets to help you.\nWe must use the inverse of addition first.\n\n$$\n(x \\div 2) +3 - 3 = 8 - 3\n$$\n\nStep 2: Simplify the number sentence from Step 1 until you have only one operation.\n\n$$\n\\begin{align}\n (x \\div 2) +3 - 3 &= 8 - 3 \\\\\n x \\div 2 &= 5\n\\end{align}\n$$\n\nStep 3: Use an inverse operation and simplify to get to the format $\\boldsymbol{variable}=\\textbf{ value}$.\n\n$$\n\\begin{align}\n x \\div 2 &= 5 \\\\\n x \\div 2 \\times 2 &= 5 \\times 2 \\\\\n x &= 10\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\nFind the value of the variable in the following open sentences:",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n1. 3 + x - 4 = 20",
    "answer_text": "$$\n\\begin{align}\n x - 1 &= 20 \\\\\n x - 1 + 1 &= 20 + 1 \\\\\n x &= 21\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n2. q \\times 3 + 5 = 29",
    "answer_text": "$$\n\\begin{align}\n (q \\times 3) + 5 - 5 &= 29 - 5 \\\\\n q \\times 3 &= 24 \\\\\n q \\times 3 \\div 3 &= 24 \\div 3 \\\\\n q &= 8\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n3. t + 10 \\div 2 = 12",
    "answer_text": "$$\n\\begin{align}\n t + (10 \\div 2) &= 12 \\\\\n t + 5 &= 12 \\\\\n t + 5 - 5 &= 12 - 5 \\\\\n t &= 7\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n4. 5 - x + 2 = 12",
    "answer_text": "$$\n\\begin{align}\n 5 + 2 - x &= 12 \\\\\n 7 - x &= 12 \\\\\n 7 - x + x &= 12 + x \\\\\n 7 &= 12 + x \\\\\n 7 - 12 &= 12 - 12 + x \\\\\n -5 &= x \\\\\n x &= -5\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n5. y \\times 5 - 7 = 13",
    "answer_text": "$$\n\\begin{align}\n (y \\times 5) - 7 &= 13 \\\\\n (y \\times 5) - 7 + 7 &= 13 + 7 \\\\\n y \\times 5 &= 20 \\\\\n y \\times 5 \\div 5 &= 20 \\div 5 \\\\\n y &= 4\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n6. p \\div 2 - 5 = 25",
    "answer_text": "$$\n\\begin{align}\n (p \\div 2) - 5 &= 25 \\\\\n (p \\div 2) - 5 + 5 &= 25 + 5 \\\\\n p \\div 2 &= 30 \\\\\n p \\div 2 \\times 2 &= 30 \\times 2 \\\\\n p &= 60\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n7. 5 \\times -2 = 6 + v",
    "answer_text": "$$\n\\begin{align}\n -10 &= 6 + v \\\\\n -10 - 6 &= 6 - 6 + v \\\\\n -16 &= v \\\\\n v &= -16\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n8. 2 \\times -6 = 24 \\div r",
    "answer_text": "$$\n\\begin{align}\n -12 &= 24 \\div r  \\\\\n -12 \\times r &= 24 \\div r \\times r \\\\\n -12 \\div -12 \\times r &= 24 \\div -12 \\\\\n r &= -2\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
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
  "subtopic_id": "jss1-math-use-of-symbols-open-sentences",
  "subtopic_title": "Open sentences",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-use-of-symbols-open-sentences-po01",
        "source_performance_objective_index": 1,
        "text": "Solve problems expressed in open sentences"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "open-sentences-ao-solve-problems",
          "text": "Solve problems expressed in open sentences."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-use-of-symbols-open-sentences-po02",
        "source_performance_objective_index": 2,
        "text": "Identify the relationship between addition and subtraction; multiplication and division"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "open-sentences-ao-identify-relationship-addition-and-subtraction",
          "text": "Identify the relationship between addition and subtraction."
        },
        {
          "atomic_objective_id": "open-sentences-ao-identify-relationship-multiplication-and-division",
          "text": "Identify the relationship between multiplication and division."
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
    "record_id": "ch09-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Closed number sentences",
      "h3": "Closed number sentences"
    },
    "content_text": "A number sentence is a group of numbers and mathematical symbols (such as +, -, or =) that gives information about the numbers. Here is an example of a number sentence: 3 + 4 = 7. This is called a closed number sentence, because all the information is given in the sentence. This closed number sentence is always true. Here is an example of a closed number sentence that is false: 5 + 8 = 2.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b002",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Closed number sentences",
      "h3": "Closed number sentences"
    },
    "content_text": "closed number sentence\nA closed number sentence gives all the information about the numbers, and it is always true or always false.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b003",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Closed number sentences",
      "h3": "Closed number sentences"
    },
    "content_text": "Here are some more examples of closed number sentences: 9 \\div 3 = 3 (true), 7\\times 12 = 84 (true), 4 \\times 8 = 8 + 8 + 8 + 8 + 8 (false).",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b004",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Closed number sentences",
      "h3": "Exercise 9.1: Decide whether closed sentences are true or false"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.1: Decide whether closed sentences are true or false\n\nState whether the closed sentence is always true or false.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b004-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Closed number sentences",
      "h3": "Exercise 9.1: Decide whether closed sentences are true or false"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.1: Decide whether closed sentences are true or false\n\n1. 4\\times 10 = 40",
    "answer_text": "True",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b004-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Closed number sentences",
      "h3": "Exercise 9.1: Decide whether closed sentences are true or false"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.1: Decide whether closed sentences are true or false\n\n2. 102\\div 2 = 12",
    "answer_text": "False",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b004-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Closed number sentences",
      "h3": "Exercise 9.1: Decide whether closed sentences are true or false"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.1: Decide whether closed sentences are true or false\n\n3. 30 + 30 + 30 = 3\\times 30",
    "answer_text": "True",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b004-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Closed number sentences",
      "h3": "Exercise 9.1: Decide whether closed sentences are true or false"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.1: Decide whether closed sentences are true or false\n\n4. 9\\div 18 = 2",
    "answer_text": "False",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b004-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Closed number sentences",
      "h3": "Exercise 9.1: Decide whether closed sentences are true or false"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.1: Decide whether closed sentences are true or false\n\n5. 9\\div 18 = \\frac{1}{2}",
    "answer_text": "True",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b005",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Open number sentences",
      "h3": "Open number sentences"
    },
    "content_text": "Here is another example of a number sentence: \\square + 3 = 7. This is called an open number sentence, because not all the information is given in the sentence. We do not know if this sentence is true or false because we do not know what is in the box.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b006",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Open number sentences",
      "h3": "Open number sentences"
    },
    "content_text": "open number sentence\nAn open number sentence does not give all the information about the numbers, but has information missing that we must find.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b007",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Worked example 9.1: Finding missing information in an open sentence"
    },
    "content_text": "",
    "prompt_text": "Find the value of the square in this open number sentence:\n\n$$\n\\square + 3 = 7\n$$",
    "answer_text": "Step 1: Ask yourself the question, \"What do I need to add to 3 to get 7?\"\n\nUsing your knowledge and mental maths, you will find that you need to add 4 to 3 to get 7.\n\nStep 2: Write down the value of the square.\n\n$$\n\\square = 4\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b008",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.2: Find missing information in open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.2: Find missing information in open sentences\n\nFor each open number sentence, find the number that makes the sentence true.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b008-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.2: Find missing information in open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.2: Find missing information in open sentences\n\n1. $$17 - 9 = \\square$$",
    "answer_text": "8",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b008-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.2: Find missing information in open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.2: Find missing information in open sentences\n\n2. $$3 + 9 = \\square$$",
    "answer_text": "12",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b008-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.2: Find missing information in open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.2: Find missing information in open sentences\n\n3. $$2\\times 12 = \\square$$",
    "answer_text": "24",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b008-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.2: Find missing information in open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.2: Find missing information in open sentences\n\n4. $$9-\\square= 2$$",
    "answer_text": "7",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b008-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.2: Find missing information in open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.2: Find missing information in open sentences\n\n5. $$\\bigcirc=\\frac{1}{2}+ \\frac{1}{2}$$",
    "answer_text": "1",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b008-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.2: Find missing information in open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.2: Find missing information in open sentences\n\n6. $$10\\times\\square = 100$$",
    "answer_text": "10",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b008-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.2: Find missing information in open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.2: Find missing information in open sentences\n\n7. $$63\\div9=\\square$$",
    "answer_text": "7",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b008-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.2: Find missing information in open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.2: Find missing information in open sentences\n\n8. $$30 + 30 + \\bigcirc = 3\\times 30$$",
    "answer_text": "30",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b008-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.2: Find missing information in open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.2: Find missing information in open sentences\n\n9. $$\\square\\times6=30$$",
    "answer_text": "5",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b008-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.2: Find missing information in open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.2: Find missing information in open sentences\n\n10. $$5 + \\bigcirc + 18 = 30$$",
    "answer_text": "7",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b009",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Variables in open sentences"
    },
    "content_text": "So far we have worked with open sentences that contain a symbol such as a $\\square$ or a $\\bigcirc$. Instead of pictures like these, in mathematics it works better to use letters to represent missing information. These letters are called **variables**, because their value can vary.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b010",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Variables in open sentences"
    },
    "content_text": "**variable** A variable is a symbol for a number we do not know yet. It is usually a letter such as $x$ or $y$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b011",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Variables in open sentences"
    },
    "content_text": "If we have an expression, such as $x+5$, we cannot know the value of the $x$ unless it is given. If we give the $x$ different values, then we can make number sentences that are true.\n\nIf $x$ = 1, then $x+5 = 1 + 5 = 6$\n\nIf $x$ = 3, then $x+5 = 3 + 5 = 8$\n\nIf $x$ = 0, then $x+5 = 0 + 5 = 0$\n\nThe value of the $x$ can vary, and that is why it is called a variable.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b012",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.3: Find the value of the expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.3: Find the value of the expression\n\nFind the value of the following expressions if $x=3$.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b012-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.3: Find the value of the expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.3: Find the value of the expression\n\n1. $$17 - x$$",
    "answer_text": "14",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b012-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.3: Find the value of the expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.3: Find the value of the expression\n\n2. $$3 + x$$",
    "answer_text": "6",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b012-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.3: Find the value of the expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.3: Find the value of the expression\n\n3. $$2\\times x\\times 0$$",
    "answer_text": "0",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b012-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.3: Find the value of the expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.3: Find the value of the expression\n\n4. $$9-x+2$$",
    "answer_text": "8",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b012-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.3: Find the value of the expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.3: Find the value of the expression\n\n5. $$\\frac{1}{x}+ \\frac{1}{x}$$",
    "answer_text": "\\frac{2}{3}",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b012-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.3: Find the value of the expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.3: Find the value of the expression\n\n6. $$10\\times x$$",
    "answer_text": "30",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b012-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.3: Find the value of the expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.3: Find the value of the expression\n\n7. $$60\\div x$$",
    "answer_text": "20",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b012-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.3: Find the value of the expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.3: Find the value of the expression\n\n8. $$30 + 30 + x$$",
    "answer_text": "63",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b012-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.3: Find the value of the expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.3: Find the value of the expression\n\n9. $$x\\times6$$",
    "answer_text": "18",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b012-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.1 Finding missing information in open sentences",
      "h3": "Exercise 9.3: Find the value of the expression"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.3: Find the value of the expression\n\n10. $$5 + x + 18$$",
    "answer_text": "26",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b013",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences that have variables",
      "h3": null
    },
    "content_text": "Variables and open sentences form part of a section of mathematics we call algebra. To show that there is information that we must find, an open sentence can use a picture symbol (such as a box or a circle) or a variable (a letter representing any number).\n\nHere are some examples of open sentences using variables:\n\n$$\n3 + x = 5\n$$\n$$\np - 4 = -3\n$$\n$$\nn - 17 = 20\n$$\n$$\n3 \\times y = 15\n$$\n$$\nb \\div 20 = 5\n$$\n\nIn these open sentences, we can find the correct value for the unknown variable that will make the sentence true. This is called solving the open sentence.\n\nIf the sentence that you need to be solve is straightforward, one option is to use mental maths to solve it.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b014",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences that have variables",
      "h3": "Worked example 9.2: Finding the value of a variable using mental maths"
    },
    "content_text": "",
    "prompt_text": "Find the value of $x$ in this open number sentence:\n\n$$\nx + 7 = 9\n$$",
    "answer_text": "Step 1: You need to find the value of $x$ that will make the statement true. To do this, you can ask yourself the question, \"What number added to 7 will give me 9?\"\n\nUsing your knowledge and mental maths, you will find that you need to add 2 to 7 to get 9.\n\nStep 2: This means that the value of $x$ is 2, so write your answer:\n\n$$\nx=2\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences"
  },
  {
    "record_id": "ch09-b015",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences that have variables",
      "h3": "Using inverse operations to solve open sentences"
    },
    "content_text": "Another way to find the value of $x$ in $x + 7 = 9$, is to use the **inverse operation** of addition. The inverse operation of addition is subtraction. In Chapter 5 you learnt that subtraction may be seen as another form of addition. For example, $6-4$ is the same as $6+(-4)$. The numbers $4$ and $-4$ are called additive inverses. When we add them, the answer is zero: $4+(-4)=0$.\n\nThe inverse operation of multiplication is division. In Chapter 6 you learnt that dividing by a fraction is the same as multiplying by the reciprocal of the fraction. For example, $4\\div\\frac{2}{3}$ is the same as $4\\times\\frac{3}{2}$. A fraction and its reciprocal are called multiplicative inverses. When we multiply them, the answer is 1: $\\frac{2}{3}\\times\\frac{3}{2}=1$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b016",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences that have variables",
      "h3": "Using inverse operations to solve open sentences"
    },
    "content_text": "**inverse operation**\nAn inverse operation does the opposite of another operation. Addition and subtraction are inverse operations, and multiplication and division are inverse operations.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b017",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences that have variables",
      "h3": "Using inverse operations to solve open sentences"
    },
    "content_text": "This closed number sentence is true:\n\n$$\n2 + 7 = 9\n$$\n\nWe know that this closed number sentence is also true:\n\n$$\n2 = 9 - 7\n$$\n\nNotice that we get from the first number sentence to the second number sentence using the inverse operation of addition, which is subtraction:\n\n$$\n\\begin{align}\n2 + 7 &= 9 \\\\\n2 + 7\\, \\color{red}{-\\;7} &= 9\\space \\color{red}{-\\;7} \\\\\n2 + 0 &= 9 - 7 \\\\\n2 &= 9 - 7\n\\end{align}\n$$\n\nHere is an example of a closed number sentence using multiplication:\n\n$$\n2 \\times 3 = 6\n$$\n\nWe know that this closed number sentence is also true:\n\n$$\n2 = 6 \\div 3\n$$\n\nNotice that we get from the first number sentence to the second number sentence using the inverse operation of multiplication, which is division:\n\n$$\n\\begin{align}\n2 \\times 3 &= 6 \\\\\n2 \\times 3\\; \\color{red}{\\div\\;3} &= 6\\space \\color{red}{\\div\\;3} \\\\\n2 \\times 1 &= 6 \\div 3 \\\\\n2 &= 6 \\div 3\n\\end{align}\n$$\n\nWe may use inverse operations to find the value of a variable in an open number sentence. We aim to write the number sentence in this format:\n\n$$\nvariable=\\text{value}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b018",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences that have variables",
      "h3": "Worked example 9.3: Solving an open sentence using the inverse of addition"
    },
    "content_text": "",
    "prompt_text": "Find the value of $x$ in this open sentence:\n\n$$\nx + 12 = 29\n$$",
    "answer_text": "Step 1: Use an inverse operation for any number that is added to or subtracted from the variable.\n\n$$\nx + 12 - 12 = 29 - 12\n$$\n\nStep 2: Simplify the sentence from Step 1 until you get to the format $\\boldsymbol{variable}=\\textbf{ value}$.\n\n$$\n\\begin{align}\nx + 12 - 12 &= 29 - 12 \\\\\nx  + 0 &= 17 \\\\\nx &= 17\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b019",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences that have variables",
      "h3": "Worked example 9.4: Solving an open sentence using the inverse of multiplication"
    },
    "content_text": "",
    "prompt_text": "Find the value of $y$ in this open sentence:\n\n$$\ny \\times 3 = 27\n$$",
    "answer_text": "Step 1: Use an inverse operation for any number that the variable is multiplied or divided by.\n\n$$\ny \\times 3 \\div 3 = 27 \\div 3\n$$\n\nStep 2: Simplify the number sentence from Step 1 until you get to the format $\\boldsymbol{variable}=\\textbf{ value}$.\n\n$$\n\\begin{align}\ny \\times 3 \\div 3 &= 27 \\div 3 \\\\\ny \\times 1 &= 9 \\\\\ny &= 9\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b020",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences that have variables",
      "h3": "Using inverse operations to solve open sentences"
    },
    "content_text": "Note that an open sentence is not regarded as solved when the variable is negative, for example $-x=5$. The variable must be positive in your final answer, for example $x=-5$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b021",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences that have variables",
      "h3": "Using inverse operations to solve open sentences"
    },
    "content_text": "The format $variable=\\text{value}$ may be swapped around. Therefore, $x=7$ and $7=x$ has the same meaning.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b022",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences that have variables",
      "h3": "Worked example 9.5: Solving an open sentence using the inverse operation on the variable"
    },
    "content_text": "",
    "prompt_text": "Find the value of $x$:\n\n$$\n18 -  x = 14\n$$",
    "answer_text": "Step 1: Use an inverse operation to get a positive variable.\n\n$$\n18 -x + x= 14 + x\n$$\n\nStep 2: Simplify the number sentence from Step 1 until it has only one positive variable.\n\n$$\n\\begin{align}\n 18 -x + x &= 14 + x \\\\\n 18 + 0 &= 14 + x \\\\\n 18 &= 14 + x\n \\end{align}\n$$\n\nStep 3: Use an inverse operation for the number that is added to or subtracted from the variable.\n\n$$\n18 - 14 = 14 - 14 + x\n$$\n\nStep 4: Simplify the number sentence from Step 1 until you get to the format $\\boldsymbol{variable}=\\textbf{ value}$.\n\n$$\n\\begin{align}\n18 - 14 &= 14 -14 + x \\\\\n4 &= 0 + x \\\\\n4 &= x \\\\\nx &= 4\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b023",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.4: Solve open sentences"
    },
    "content_text": "Usman is 1.8 m tall and his sister Jummai is y m tall. The difference in their heights is 0.4 m. How tall is Jummai if she is shorter than Usman?",
    "prompt_text": "### Exercise 9.4: Solve open sentences\n\nFind the value of the variable in the following open sentences:",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b023-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.4: Solve open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.4: Solve open sentences\n\n1. y + 7 = 30",
    "answer_text": "$$\n\\begin{align}\n y + 7 - 7 &= 30 - 7 \\\\\n y &= 23\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b023-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.4: Solve open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.4: Solve open sentences\n\n2. 3 + x = 15",
    "answer_text": "$$\n\\begin{align}\n 3 - 3 + x &= 15 - 3 \\\\\n x &= 12\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b023-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.4: Solve open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.4: Solve open sentences\n\n3. z - 8 = 20",
    "answer_text": "$$\n\\begin{align}\n z - 8 + 8 &= 20 + 8 \\\\\n z &= 28\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b023-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.4: Solve open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.4: Solve open sentences\n\n4. q  - 4 = -5",
    "answer_text": "$$\n\\begin{align}\n q - 4 + 4 &= -5 + 4 \\\\\n q &= -1\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b023-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.4: Solve open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.4: Solve open sentences\n\n5. 17 - n = 20",
    "answer_text": "$$\n\\begin{align}\n 17 - n + n &= 20 + n \\\\\n 17 &= 20 + n  \\\\\n 17 - 20 &= 20 - 20 + n \\\\\n 3 &= n \\\\\n n &= 3\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b023-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.4: Solve open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.4: Solve open sentences\n\n6. 15 - p = -5",
    "answer_text": "$$\n\\begin{align}\n 15 - p + p &= -5 + p \\\\\n 15 &= -5 + p  \\\\\n 15 + 5 &= -5 + 5 + p \\\\\n 20 &= p \\\\\n p &= 20\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b023-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.4: Solve open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.4: Solve open sentences\n\n7. x \\times 8 = 48",
    "answer_text": "$$\n\\begin{align}\n x \\times 8 \\div 8 &= 48 \\div 8 \\\\\n x &= 6  \\\\\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b023-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.4: Solve open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.4: Solve open sentences\n\n8. 3 \\times y = 15",
    "answer_text": "$$\n\\begin{align}\n 3 \\div 3 \\times y &= 15 \\div 3 \\\\\n y &= 5  \\\\\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b023-i09",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.4: Solve open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.4: Solve open sentences\n\n9. c\\div 20 = 5",
    "answer_text": "$$\n\\begin{align}\n c \\div 20 \\times 20 &= 5 \\times 20 \\\\\n c &= 100  \\\\\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b023-i10",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.4: Solve open sentences"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.4: Solve open sentences\n\n10. 40 \\div x = 8",
    "answer_text": "$$\n\\begin{align}\n40 \\div x \\times x &= 8 \\times x \\\\\n40 &= 8 \\times x  \\\\\n40 \\div 8 &= 8 \\div 8 \\times x \\\\\n5 &= x \\\\\nx &= 5\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-open-sentences"
  },
  {
    "record_id": "ch09-b024",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": null
    },
    "content_text": "Open number sentences may have more than one operation, for example $4-2+x=10$. To solve number sentences like these, you must remember the correct order of operations that you learnt last year:\n\n1. **B**rackets\n2. **O**f\n3. **D**ivide\n4. **M**ultiply\n5. **A**dd\n6. **S**ubtract",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b025",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.3 Using open sentences to solve problems",
      "h3": "Worked example 9.7: Solving a problem using open sentences"
    },
    "content_text": "",
    "prompt_text": "Find the value of x:",
    "answer_text": "$$\nx \\div 2 + 3 = 8\n$$\n\nStep 1: Decide which inverse operation to do first.\n\nAccording to the order BODMAS, you must calculate $x \\div 2$ before $2+3$.\nThis means $x \\div 2$ must \"stay together\". You may insert brackets to help you.\nWe must use the inverse of addition first.\n\n$$\n(x \\div 2) +3 - 3 = 8 - 3\n$$\n\nStep 2: Simplify the number sentence from Step 1 until you have only one operation.\n\n$$\n\\begin{align}\n (x \\div 2) +3 - 3 &= 8 - 3 \\\\\n x \\div 2 &= 5\n\\end{align}\n$$\n\nStep 3: Use an inverse operation and simplify to get to the format $\\boldsymbol{variable}=\\textbf{ value}$.\n\n$$\n\\begin{align}\n x \\div 2 &= 5 \\\\\n x \\div 2 \\times 2 &= 5 \\times 2 \\\\\n x &= 10\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\nFind the value of the variable in the following open sentences:",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n1. 3 + x - 4 = 20",
    "answer_text": "$$\n\\begin{align}\n x - 1 &= 20 \\\\\n x - 1 + 1 &= 20 + 1 \\\\\n x &= 21\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n2. q \\times 3 + 5 = 29",
    "answer_text": "$$\n\\begin{align}\n (q \\times 3) + 5 - 5 &= 29 - 5 \\\\\n q \\times 3 &= 24 \\\\\n q \\times 3 \\div 3 &= 24 \\div 3 \\\\\n q &= 8\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n3. t + 10 \\div 2 = 12",
    "answer_text": "$$\n\\begin{align}\n t + (10 \\div 2) &= 12 \\\\\n t + 5 &= 12 \\\\\n t + 5 - 5 &= 12 - 5 \\\\\n t &= 7\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n4. 5 - x + 2 = 12",
    "answer_text": "$$\n\\begin{align}\n 5 + 2 - x &= 12 \\\\\n 7 - x &= 12 \\\\\n 7 - x + x &= 12 + x \\\\\n 7 &= 12 + x \\\\\n 7 - 12 &= 12 - 12 + x \\\\\n -5 &= x \\\\\n x &= -5\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n5. y \\times 5 - 7 = 13",
    "answer_text": "$$\n\\begin{align}\n (y \\times 5) - 7 &= 13 \\\\\n (y \\times 5) - 7 + 7 &= 13 + 7 \\\\\n y \\times 5 &= 20 \\\\\n y \\times 5 \\div 5 &= 20 \\div 5 \\\\\n y &= 4\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n6. p \\div 2 - 5 = 25",
    "answer_text": "$$\n\\begin{align}\n (p \\div 2) - 5 &= 25 \\\\\n (p \\div 2) - 5 + 5 &= 25 + 5 \\\\\n p \\div 2 &= 30 \\\\\n p \\div 2 \\times 2 &= 30 \\times 2 \\\\\n p &= 60\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n7. 5 \\times -2 = 6 + v",
    "answer_text": "$$\n\\begin{align}\n -10 &= 6 + v \\\\\n -10 - 6 &= 6 - 6 + v \\\\\n -16 &= v \\\\\n v &= -16\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
  {
    "record_id": "ch09-b026-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 9: Using symbols",
      "h2": "9.2 Solving open sentences",
      "h3": "Exercise 9.5: Solve open sentences with two operations"
    },
    "content_text": "",
    "prompt_text": "### Exercise 9.5: Solve open sentences with two operations\n\n8. 2 \\times -6 = 24 \\div r",
    "answer_text": "$$\n\\begin{align}\n -12 &= 24 \\div r  \\\\\n -12 \\times r &= 24 \\div r \\times r \\\\\n -12 \\div -12 \\times r &= 24 \\div -12 \\\\\n r &= -2\n\\end{align}\n$$",
    "primary_subtopic_id": "jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations"
  },
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
