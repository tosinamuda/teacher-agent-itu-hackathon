# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-2",
  "topic_key": "jss1-math-addition-and-subtraction",
  "topic": "Addition and Subtraction",
  "subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers",
  "subtopic_title": "Addition and subtraction of positive and negative integers",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers-po01",
        "source_performance_objective_index": 1,
        "text": "Add and subtract positive and negative integers on a number line"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "positive-and-negative-integers-ao-add-on-number-line",
          "text": "Add positive and negative integers on a number line."
        },
        {
          "atomic_objective_id": "positive-and-negative-integers-ao-subtract-on-number-line",
          "text": "Subtract positive and negative integers on a number line."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch05-b007",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.3 The number line",
      "h3": null
    },
    "content_text": "The set of integers is made up of all the positive and negative whole numbers, including zero. We may represent integers on a number line. This is a straight line, divided into equal segments, that shows the position of the numbers.\n\nNumbers to the right of zero are called positive numbers. We represent them with or without a plus sign in front. For example, the positive number five may be written as +5 or just 5. Numbers to the left of zero are called negative numbers. We always represent them with a minus sign in front. For example, the negative number three is written as -3. The number zero is neither positive nor negative.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-use-of-number-line"
  },
  {
    "record_id": "ch05-b008",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.3 The number line",
      "h3": null
    },
    "content_text": "**integers** Integers are positive and negative whole numbers, including zero.\n\n**number line** A number line is a straight line divided into equal segments, that shows the position of numbers.\n\n**positive numbers** Positive numbers are numbers that are larger than zero. They lie to the right of zero on a number line.\n\n**negative numbers** Negative numbers are numbers that are smaller than zero. They lie to the left of zero on a number line.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-use-of-number-line"
  },
  {
    "record_id": "ch05-b009",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.3 The number line",
      "h3": null
    },
    "content_text": "We draw a number line with arrowheads at both ends to show that the line can carry on in both directions forever. Here is an example of a number line:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-001.png)",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-use-of-number-line"
  },
  {
    "record_id": "ch05-b010",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.3 The number line",
      "h3": null
    },
    "content_text": "A number line can also be drawn vertically. Then the positive numbers lie above zero and the negative numbers lie below zero.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-use-of-number-line"
  },
  {
    "record_id": "ch05-b011",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "Comparing integers on the number line",
      "h3": null
    },
    "content_text": "Positive and negative numbers are sometimes called **directed numbers**. This is because the sign of the number (positive or negative) tells us in which direction from zero they appear on the number line.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-use-of-number-line"
  },
  {
    "record_id": "ch05-b012",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "Comparing integers on the number line",
      "h3": null
    },
    "content_text": "**directed numbers** Directed numbers are positive and negative numbers. The sign of a directed number tells us in which direction from zero it lies on the number line.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-use-of-number-line"
  },
  {
    "record_id": "ch05-b013",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "Comparing integers on the number line",
      "h3": null
    },
    "content_text": "The further to the right a number lies on the number line, the larger it is. The further to the left a number lies on the number line, the smaller it is. We use the symbols < and > to show the relationship between two numbers:\n\n- The symbol < means \"smaller than\".\n- The symbol > means \"greater than\".\n\nLook at the number line above again. The number 2 lies to the left of the number 6 on the number line. We may write this in two ways:\n\n- 2<6, which means two is smaller than six\n- 6&amp;gt;2, which means six is greater than two",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-use-of-number-line"
  },
  {
    "record_id": "ch05-b014",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "Comparing integers on the number line",
      "h3": null
    },
    "content_text": "To help you choose the correct symbol, remember that the symbol must \"open up\" towards the larger number. The \"closed\" and smaller end points to the smaller number. This crocodile may also help you remember which symbol to use. It always wants to eat the larger number, and it turns away from the smaller number.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-002.png)",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-use-of-number-line"
  },
  {
    "record_id": "ch05-b015",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "Comparing integers on the number line",
      "h3": "Exercise 5.3: Compare integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.3: Compare integers",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-use-of-number-line"
  },
  {
    "record_id": "ch05-b015-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "Comparing integers on the number line",
      "h3": "Exercise 5.3: Compare integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.3: Compare integers\n\n1. Draw a number line showing all the integers from -10 to 10.",
    "answer_text": "![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-003.png)",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-use-of-number-line"
  },
  {
    "record_id": "ch05-b015-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "Comparing integers on the number line",
      "h3": "Exercise 5.3: Compare integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.3: Compare integers\n\n2. Place the correct symbol between each pair of numbers. Use your number line to help you.\n\na. 1 \\square 7\nb. 9 \\square 6\nc. 4 \\square 0\nd. -4 \\square 0\ne. 1 \\square -2\nf. -6 \\square 1\ng. -3 \\square -2\nh. -3 \\square -7\ni. -8 \\square -5\nj. 1 \\square -1",
    "answer_text": "a. 1<7\nb. 9&amp;gt;6\nc. 4&amp;gt;0\nd. -4<0\ne. 1&amp;gt;-2\nf. -6<1\ng. -3<-2\nh. -3&amp;gt;-7\ni. -8<-5\nj. 1&amp;gt;-1",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-use-of-number-line"
  },
  {
    "record_id": "ch05-b015-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "Comparing integers on the number line",
      "h3": "Exercise 5.3: Compare integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.3: Compare integers\n\n3. Arrange the following lists of numbers as required, using the correct symbol. Use your number line to help you.\n\na. Arrange from the smallest to the largest: 1;-5;-3; 2;-1\nb. Arrange from the largest to the smallest: -9; 6; 3;-6; 0",
    "answer_text": "a. -5<-3<-1<1<2\nb. 6&amp;gt;3&amp;gt;0&amp;gt;-6&amp;gt;-9",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-use-of-number-line"
  },
  {
    "record_id": "ch05-b016",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Adding integers"
    },
    "content_text": "We may use a number line to count. When we count to the right, we count in the positive direction. This is because the numbers become larger as we move to the right on a number line. When we count to the left, we count in the negative direction. This is because the numbers become smaller as we move to the left on a number line.\n\nWhen we add one integer to another, we may see it as units that are added along the number line. Examples of how we may interpret addition are:\n\n- $5+2$: from the number 5, count 2 units in the positive direction (to the right)\n- $-7+3$: from the number -7, count 3 units in the positive direction (to the right)\n- $1+(-4)$: from the number 1, count 4 units in the negative direction (to the left)\n- $-6+(-3)$: from the number -6, count 3 units in the negative direction (to the left)",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b017",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Adding integers"
    },
    "content_text": "Integers may be added in any order. For example, $-1+3$ and $3+(-1)$ give the same answer.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b018",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Worked example 5.3: Adding integers using the number line"
    },
    "content_text": "",
    "prompt_text": "Use a number line to determine the following: $-5+10$.\n\nStep 1: Draw a number line and find the first number on the line.\n\nThe first number is -5.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-004.png)\n\nStep 2: Determine how many units you must count, and in which direction.\n\nThe number 10 indicates that you must count 10 units in the positive direction, that is, to the right.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-005.png)\n\nA positive number does not always have a plus sign in front. When we write 10, it represents +10.\n\nStep 3: The answer is the number where you end up.\n\n$$\n-5+10=5\n$$\n\nUse a number line to determine the following: $-4+(-6)$.\n\nStep 1: Draw a number line and find the first number on the line.\n\nThe first number is -4.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-006.png)\n\nStep 2: Determine how many units you must count, and in which direction.\n\nThe number -6 indicates that you must count 6 units in the negative direction, that is, to the left.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-007.png)\n\nStep 3: The answer is the number where you end up.\n\n$$\n-4+(-6)=-10\n$$",
    "answer_text": "[{'asset_type': 'image', 'ordinal': 1, 'src': 'https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-004.png'}, {'asset_type': 'image', 'ordinal': 2, 'src': 'https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-005.png'}, {'asset_type': 'image', 'ordinal': 3, 'src': 'https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-006.png'}, {'asset_type': 'image', 'ordinal': 4, 'src': 'https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-007.png'}]",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b019",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.4: Use a number line to add integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.4: Use a number line to add integers\n\nUse number lines to add the following pairs of integers.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b019-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.4: Use a number line to add integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.4: Use a number line to add integers\n\n1. $1+6$",
    "answer_text": "![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-008.png)\n\n$$\n\\therefore 1+6=7\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b019-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.4: Use a number line to add integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.4: Use a number line to add integers\n\n2. $-6+7$",
    "answer_text": "![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-009.png)\n\n$$\n\\therefore -6+7=1\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b019-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.4: Use a number line to add integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.4: Use a number line to add integers\n\n3. $4+(-9)$",
    "answer_text": "![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-010.png)\n\n$$\n\\therefore 4+(-9)=-5\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b019-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.4: Use a number line to add integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.4: Use a number line to add integers\n\n4. $-2+(-6)$",
    "answer_text": "![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-011.png)\n\n$$\n\\therefore -2+(-6)=-8\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b020",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Subtracting integers"
    },
    "content_text": "There are different ways to think about subtraction. One way is to see it as another form of addition. Subtracting a number is the same as adding the \"opposite\" of the number. A number and its \"opposite\" are equal distances from zero, but on opposite sides. For example, -7 is the \"opposite\" number of 7, and 5 is the \"opposite\" number of -5.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b021",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Subtracting integers"
    },
    "content_text": "The \"opposite\" of a number referred to above has a special name. It is called the additive inverse of the number. When you add a number and its additive inverse, the answer is zero.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b022",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Subtracting integers"
    },
    "content_text": "The subtraction $6-4$ is the same as $6+(-4)$. Similarly, the subtraction $5-(-1)$ is the same as $5+(+1)$. After writing a subtraction as an addition, you may use the method shown in Worked example 5.3 to add the two numbers.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b023",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.5: Write subtraction as addition"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.5: Write subtraction as addition\n\nWrite each subtraction as an addition.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b023-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.5: Write subtraction as addition"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.5: Write subtraction as addition\n\n1. $1-6$",
    "answer_text": "$$\n\\require{enclose}1\\,\\enclose{circle}[mathcolor=\"red\"]{-}\\,6=1\\,\\enclose{circle}[mathcolor=\"red\"]{+}(-6)\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b023-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.5: Write subtraction as addition"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.5: Write subtraction as addition\n\n2. $-6-7$",
    "answer_text": "$$\n\\require{enclose}-6\\,\\enclose{circle}[mathcolor=\"red\"]{-}\\,7=-6\\,\\enclose{circle}[mathcolor=\"red\"]{+}(-7)\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b023-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.5: Write subtraction as addition"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.5: Write subtraction as addition\n\n3. $5-(-2)$",
    "answer_text": "$$\n\\require{enclose}5\\,\\enclose{circle}[mathcolor=\"red\"]{-}(-2)=5\\,\\enclose{circle}[mathcolor=\"red\"]{+}\\,2\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b023-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.5: Write subtraction as addition"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.5: Write subtraction as addition\n\n4. $-8-(-4)$",
    "answer_text": "$$\n\\require{enclose}-8\\,\\enclose{circle}[mathcolor=\"red\"]{-}(-4)=-8\\,\\enclose{circle}[mathcolor=\"red\"]{+}\\,4\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b024",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Subtracting integers"
    },
    "content_text": "Another way is to see subtraction as the difference between two numbers. For example, if you have 7 sweets and you eat 4 sweets, you have $7-4=3$ left. The number of sweets you have left is the difference between the sweets you had at the start and the sweets you ate. On a number line, the difference between the numbers 7 and 4 is 3 units.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-012.png)\n\nThe number 7 lies 3 units to the positive side of the number 4. Therefore, $7-4=+3$. At the same time, the number 4 lies 3 units to the negative side of the number 7. Therefore, $4-7=-3$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b025",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Subtracting integers"
    },
    "content_text": "Integers cannot be subtracted in any order. For example, $3-1$ and $1-3$ do not give the same answer.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b026",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Worked example 5.4: Subtracting integers using the number line"
    },
    "content_text": "",
    "prompt_text": "Use a number line to determine the following: $-5-3$\n\nUse a number line to determine the following: $-4-(-6)$",
    "answer_text": "Question 1\n\nStep 1: Identify the two integers that must be subtracted.\n\n$$\n\\require{enclose}-5\\, \\enclose{circle}[mathcolor=\"red\"]{-}\\,3\n$$\n\nThe numbers are $-5$ and 3.\n\nStep 2: Draw a number line and show the two numbers on the line.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-013.png)\n\nStep 3: Determine the difference between the two numbers.\n\nThe difference between $-5$ and 3 is 8 units.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-014.png)\n\nStep 4: Determine whether the number you are subtracting from lies to the positive or the negative side of the number that is being subtracted.\n\n$-5$ lies to the negative side of 3.\n\nStep 5: Use the information from Step 4 to decide whether the answer is positive or negative.\n\n$$\n-5-3=-8\n$$\n\nQuestion 2\n\nStep 1: Identify the two integers that must be subtracted.\n\n$$\n\\require{enclose}-4\\, \\enclose{circle}[mathcolor=\"red\"]{-}(-6)\n$$\n\nThe numbers are $-4$ and $-6$.\n\nStep 2: Draw a number line and show the two numbers on the line.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-015.png)\n\nStep 3: Determine the difference between the two numbers.\n\nThe difference between $-4$ and $-6$ is 2 units.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-016.png)\n\nStep 4: Determine whether the number you are subtracting from lies to the positive or the negative side of the number that is being subtracted.\n\n$-4$ lies to the positive side of $-6$.\n\nStep 5: Use the information from Step 4 to decide whether the answer is positive or negative.\n\n$$\n-4-(-6)=2\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b027",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.6: Use a number line to subtract integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.6: Use a number line to subtract integers\n\nFor each pair, use a number line to subtract the second integer from the first one.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b027-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.6: Use a number line to subtract integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.6: Use a number line to subtract integers\n\n1. $2-5$",
    "answer_text": "$$\n\\require{enclose}2\\,\\enclose{circle}[mathcolor=\"red\"]{-}\\,5\n$$\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-017.png)\n\n2 lies to the negative side of 5.\n\n$$\n\\therefore 2-5=-3\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b027-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.6: Use a number line to subtract integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.6: Use a number line to subtract integers\n\n2. $-1-3$",
    "answer_text": "$$\n\\require{enclose}-1\\,\\enclose{circle}[mathcolor=\"red\"]{-}\\,3\n$$\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-018.png)\n\n$-1$ lies to the negative side of 3.\n\n$$\n\\therefore -1-3=-4\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b027-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.6: Use a number line to subtract integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.6: Use a number line to subtract integers\n\n3. $5-(-6)$",
    "answer_text": "$$\n\\require{enclose}5\\,\\enclose{circle}[mathcolor=\"red\"]{-}(-6)\n$$\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-019.png)\n\n5 lies to the positive side of $-6$.\n\n$$\n\\therefore 5-(-6)=11\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b027-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.6: Use a number line to subtract integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.6: Use a number line to subtract integers\n\n4. $-2-(-7)$",
    "answer_text": "$$\n\\require{enclose}-2\\,\\enclose{circle}[mathcolor=\"red\"]{-}(-7)\n$$\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-020.png)\n\n$-2$ lies to the positive side of $-7$.\n\n$$\n\\therefore -2-(-7)=5\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b028",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Worked example 5.5: Comparing different methods of subtracting integers"
    },
    "content_text": "",
    "prompt_text": "Determine the following: $-4-3$",
    "answer_text": "Identify the two integers that must be subtracted.\n\n$$\n\\require{enclose}-4\\,\\enclose{circle}[mathcolor=\"red\"]{-}\\,3\n$$\n\nThe number 3 must be subtracted from the number $-4$.\n\nMethod 1: Regard subtraction as another form of addition.\n\n$$\n\\require{enclose}-4\\,\\enclose{circle}[mathcolor=\"red\"]{-}\\,3=-4\\,\\enclose{circle}[mathcolor=\"red\"]{+}(-3)\n$$\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-021.png)\n\n$$\n\\therefore -4+(-3)=-7\n$$\n\nMethod 2: Regard subtraction as the difference between two numbers.\n\n$$\n\\require{enclose}-4\\,\\enclose{circle}[mathcolor=\"red\"]{-}\\,3\n$$\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-022.png)\n\n$-4$ lies to the negative side of 3.\n\n$$\n\\therefore -4-3=-7\n$$\n\nThe two methods give the same answer.",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b029",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.5 Practical applications",
      "h3": "Thermometers"
    },
    "content_text": "A thermometer is an instrument we use to measure temperature. Most thermometers we use in everyday life measure the temperature in degrees Celsius $(^\\circ \\text C)$. The freezing point of water, $0 ^\\circ \\text C$, is shown somewhere in the middle of the thermometer. Temperatures above $0 ^\\circ \\text C$ are positive and temperatures below $0 ^\\circ \\text C$ are negative. The average body temperature of a healthy human is $37 ^\\circ \\text C$, as shown on the thermometer below. The typical temperature of the freezing compartment of a refrigerator is $-18 ^\\circ \\text C$.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-023.png)",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-everyday-application-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b030",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.5 Practical applications",
      "h3": "Banking"
    },
    "content_text": "Banks allow people to borrow money from them. When you put money into your bank account, you have a positive bank balance. When you draw money from your bank account, it is subtracted from your balance. If you withdraw more money than you have in your bank account, your bank account goes into an overdraft. Your bank balance becomes negative. Part of a bank statement is shown below.\n\n$$\n\\begin{array}{|l l r|}\n\\hline\n\\ggg \\triangleright\\triangleright\\triangleright & \\textbf{BESTBANK NIGERIA}\\\\\n\\hline\n \\text{2019/10/01} & \\text{Balance brought forward} &  ₦120,512.45 \\\\\n \\text{2019/10/05} & \\text{Deposit} &  ₦13,000.00 \\\\\n \\text{2019/10/12} & \\text{Withdrawal} &  -\\,₦4,000.00 \\\\\n \\text{2019/10/15} & \\text{Credit card transaction} &  -\\,₦52,514.05 \\\\\n \\text{2019/10/18} & \\text{Refund} &  ₦500.00 \\\\\n \\text{2019/10/22} & \\text{Credit card transaction} &  -\\,₦7,223.40 \\\\\n \\text{2019/10/25} & \\text{Withdrawal} &  -\\,₦80,100.00 \\\\\n \\hline\n \\text{2019/10/31} & \\text{Balance carried over} &  -\\,₦9,825.00 \\\\\n \\hline\n \\end{array}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-everyday-application-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b031",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.5 Practical applications",
      "h3": "Movement along the same straight line"
    },
    "content_text": "When we move along the same straight line, we may use positive and negative numbers to determine our position relative to a starting point. The diagram shows part of a school yard.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-05-0_011.png)\n\nSuppose you walk from the swimming pool 100 m to the right and then 20 m to the left. If distances to the right are taken as positive and distances to the left are taken as negative, you end up $100\\space \\text m + (-20\\space \\text m)=80\\space\\text m$ to the right of the swimming pool.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-everyday-application-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b032",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.5 Practical applications",
      "h3": "Exercise 5.7: Use positive and negative numbers to solve problems."
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.7: Use positive and negative numbers to solve problems.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-everyday-application-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b032-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.5 Practical applications",
      "h3": "Exercise 5.7: Use positive and negative numbers to solve problems."
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.7: Use positive and negative numbers to solve problems.\n\n1. Food is taken out of the freezing compartment of a refrigerator. Its temperature changes from -10\\space ^\\circ \\text C to 7\\space ^\\circ \\text C. Calculate by how much the temperature of the food increased.\n\nHint: To calculate the change in a quantity, use the following principle: \\text{change}=\\text{final value}-\\text{initial value}",
    "answer_text": "7\\space ^\\circ \\text C - (-10\\space ^\\circ \\text C)\n\n\\require{enclose}\n$$\n\\begin{array}{r l}\n7\\,\\enclose{circle}[mathcolor=\"red\"]{-}(-10)&=7\\,\\enclose{circle}[mathcolor=\"red\"]{+}(+10)\\newline\n&=17\\space ^\\circ \\text C\n\\end{array}\n$$\nThe temperature of the food increased by 17\\space ^\\circ \\text C.",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-everyday-application-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b032-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.5 Practical applications",
      "h3": "Exercise 5.7: Use positive and negative numbers to solve problems."
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.7: Use positive and negative numbers to solve problems.\n\n2. A piece of meat is at a room temperature of 25\\space ^\\circ \\text C. It is placed in a freezer. The temperature of the meat drops by 40\\space ^\\circ \\text C. Calculate the new temperature of the meat.",
    "answer_text": "If the temperature dropped, we must count 40 units in the negative direction: 25\\space ^\\circ \\text C +(- 40\\space ^\\circ \\text C)\n\nStart at the number +25.\n\nCount 25 units in the negative direction. Now you are at zero.\n\nCount another 40-25=15 units in the negative direction. Now you are at -15.\n\nThe new temperature is -15\\space ^\\circ \\text C.",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-everyday-application-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b032-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.5 Practical applications",
      "h3": "Exercise 5.7: Use positive and negative numbers to solve problems."
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.7: Use positive and negative numbers to solve problems.\n\n3. Scientists have worked out that the average temperature on the surface of the Earth is 14\\space ^\\circ \\text C, and that the average temperature on the surface of Mars is -63\\space ^\\circ \\text C. Calculate how much warmer than Mars the Earth is.",
    "answer_text": "If we want to know the difference between the temperature of the Earth and of Mars, we must subtract the temperature of Mars: 14\\space ^\\circ \\text C -(- 63\\space ^\\circ \\text C)\n\n\\require{enclose}\n$$\n\\begin{array}{r l}\n14\\,\\enclose{circle}[mathcolor=\"red\"]{-}(-63)&=14\\,\\enclose{circle}[mathcolor=\"red\"]{+}(+63)\\newline\n&=77\\space ^\\circ \\text C\n\\end{array}\n$$\nThe Earth is 77\\space ^\\circ \\text C warmer than Mars.",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-everyday-application-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b032-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.5 Practical applications",
      "h3": "Exercise 5.7: Use positive and negative numbers to solve problems."
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.7: Use positive and negative numbers to solve problems.\n\n4. Chioma and Ndidi are sisters. At the start of the school holidays, Chioma owes Ndidi ₦50. Ndidi has another ₦25 that she saved during the term. Both girls earn pocket money during the holidays. They each receive ₦750 in total. Chioma repays her debt to Ndidi. Calculate how much money each of them have at the end of the holidays.",
    "answer_text": "$$\n\\begin{array}{|l r r|}\n \\hline\n  & \\text{Chioma} &  \\text{Ndidi} \\newline\n  \\hline\n   \\text{Start} & ₦0 &  ₦25 \\newline\n   \\text{Earnings} & ₦750 &  ₦750 \\newline\n   \\text{Debt} & -\\,₦50 &  ₦50 \\newline\n   \\hline\n   \\text{Balance} & ₦700 &  ₦825 \\newline\n   \\hline\n   \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-everyday-application-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b032-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.5 Practical applications",
      "h3": "Exercise 5.7: Use positive and negative numbers to solve problems."
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.7: Use positive and negative numbers to solve problems.\n\n5. A man owes the bank ₦5,500. He deposits ₦6,000, but later withdraws ₦800. Calculate his new bank balance.",
    "answer_text": "$$\n\\begin{array}{|l r|}\n \\hline\n   \\text{Start} &  -\\,₦5,500 \\newline\n   \\text{Deposit} &  ₦6,000 \\newline\n   \\text{Debt} &  -\\,₦800 \\newline\n   \\hline\n   \\text{Balance} &  -\\,₦300 \\newline\n   \\hline\n   \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-everyday-application-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b032-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.5 Practical applications",
      "h3": "Exercise 5.7: Use positive and negative numbers to solve problems."
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.7: Use positive and negative numbers to solve problems.\n\n6. Oladapo walks east from his house to school. After walking for 750 m, he realizes that he forgot a book at home. He turns around and walks back. His cell phone rings when he is 200 m from the point where he turned around. Calculate how far from his house Oladapo is when his phone rings.",
    "answer_text": "If east is taken as positive: 750\\space \\text m+(-200\\space \\text m)=550\\space\\text m\n\nHe is 550 m to the east of his house.",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-everyday-application-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b032-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.5 Practical applications",
      "h3": "Exercise 5.7: Use positive and negative numbers to solve problems."
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.7: Use positive and negative numbers to solve problems.\n\n7. A girl sits in a tree. She throws a ball straight up into the air. It reaches a height of 1 m above the girl's hand and then falls back. The ball falls straight downwards for 3 m, past the tree, and lands on the ground. Calculate the distance between the girl's hand and the ground.\n\nA bird flies straight north. After 50 m it turns around. It flies straight south for 90 m. It turns around again and flies straight north for 10 m. Determine where it is in relation to its original position.",
    "answer_text": "If upwards is taken as positive: 1\\space \\text m+(-3\\space \\text m)=-2\\space\\text m\n\nThe ground is 2 m below the girl's hand.\n\nIf north is taken as positive: 50\\space \\text m+(-90\\space \\text m)+(10\\space \\text m)=-30\\space\\text m\n\nThe bird is 30 m south of its original position.",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-everyday-application-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b033",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.6 Summary",
      "h3": null
    },
    "content_text": "- The place value of a digit tells us what the value of that digit is, based on its position in a number.\n- When we add or subtract large numbers, we line up the units, tens, hundreds and thousands of the numbers.\n- A number line is a straight line, divided into equal segments, that shows the positions of numbers.\n- Positive numbers are larger than zero and lie to the right of zero on a number line.\n- Negative numbers are smaller than zero and lie to the left of zero on a number line.\n- Zero is neither positive nor negative.\n- The symbol < means \"smaller than\", and 3<5 means three is smaller than five. The symbol > means \"greater than\", and 5>3 means five is greater than three.\n- When we add one integer to another, we may see it as units that are added along the number line. When we add positive numbers, we count to the right on a number line. When we add negative numbers, we count to the left on a number line.\n- Subtracting a number is the same as adding the \"opposite\" of the number. For example, $2-7$ is the same as $2+(-7)$.\n- Subtraction may also be seen as the difference between two numbers. For example, there are 5 units between the numbers 2 and 7. If the number which is subtracted from lies to the negative side of the number that is subtracted, the difference is negative: $2-7=-5$. If the number which is subtracted from lies to the positive side of the number that is subtracted, the difference is positive: $7-2=5$.\n- A thermometer is an instrument used to measure temperature. Temperatures above $0\\space ^\\circ\\text C$ are positive. Temperatures below $0\\space ^\\circ\\text C$ are negative.\n- A positive bank balance means you have money in the bank. A negative bank balance means you owe the bank money.\n- For movement along a straight line, we take one direction as positive. The opposite direction is negative.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
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
  "topic_key": "jss1-math-addition-and-subtraction",
  "topic": "Addition and Subtraction",
  "subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers",
  "subtopic_title": "Addition and subtraction of positive and negative integers",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers-po01",
        "source_performance_objective_index": 1,
        "text": "Add and subtract positive and negative integers on a number line"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "positive-and-negative-integers-ao-add-on-number-line",
          "text": "Add positive and negative integers on a number line."
        },
        {
          "atomic_objective_id": "positive-and-negative-integers-ao-subtract-on-number-line",
          "text": "Subtract positive and negative integers on a number line."
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
    "record_id": "ch05-b007",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.3 The number line",
      "h3": null
    },
    "content_text": "The set of integers is made up of all the positive and negative whole numbers, including zero. We may represent integers on a number line. This is a straight line, divided into equal segments, that shows the position of the numbers.\n\nNumbers to the right of zero are called positive numbers. We represent them with or without a plus sign in front. For example, the positive number five may be written as +5 or just 5. Numbers to the left of zero are called negative numbers. We always represent them with a minus sign in front. For example, the negative number three is written as -3. The number zero is neither positive nor negative.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-use-of-number-line"
  },
  {
    "record_id": "ch05-b008",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.3 The number line",
      "h3": null
    },
    "content_text": "**integers** Integers are positive and negative whole numbers, including zero.\n\n**number line** A number line is a straight line divided into equal segments, that shows the position of numbers.\n\n**positive numbers** Positive numbers are numbers that are larger than zero. They lie to the right of zero on a number line.\n\n**negative numbers** Negative numbers are numbers that are smaller than zero. They lie to the left of zero on a number line.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-use-of-number-line"
  },
  {
    "record_id": "ch05-b009",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.3 The number line",
      "h3": null
    },
    "content_text": "We draw a number line with arrowheads at both ends to show that the line can carry on in both directions forever. Here is an example of a number line:\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-001.png)",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-use-of-number-line"
  },
  {
    "record_id": "ch05-b010",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.3 The number line",
      "h3": null
    },
    "content_text": "A number line can also be drawn vertically. Then the positive numbers lie above zero and the negative numbers lie below zero.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-use-of-number-line"
  },
  {
    "record_id": "ch05-b011",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "Comparing integers on the number line",
      "h3": null
    },
    "content_text": "Positive and negative numbers are sometimes called **directed numbers**. This is because the sign of the number (positive or negative) tells us in which direction from zero they appear on the number line.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-use-of-number-line"
  },
  {
    "record_id": "ch05-b012",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "Comparing integers on the number line",
      "h3": null
    },
    "content_text": "**directed numbers** Directed numbers are positive and negative numbers. The sign of a directed number tells us in which direction from zero it lies on the number line.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-use-of-number-line"
  },
  {
    "record_id": "ch05-b013",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "Comparing integers on the number line",
      "h3": null
    },
    "content_text": "The further to the right a number lies on the number line, the larger it is. The further to the left a number lies on the number line, the smaller it is. We use the symbols < and > to show the relationship between two numbers:\n\n- The symbol < means \"smaller than\".\n- The symbol > means \"greater than\".\n\nLook at the number line above again. The number 2 lies to the left of the number 6 on the number line. We may write this in two ways:\n\n- 2<6, which means two is smaller than six\n- 6&amp;gt;2, which means six is greater than two",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-use-of-number-line"
  },
  {
    "record_id": "ch05-b014",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "Comparing integers on the number line",
      "h3": null
    },
    "content_text": "To help you choose the correct symbol, remember that the symbol must \"open up\" towards the larger number. The \"closed\" and smaller end points to the smaller number. This crocodile may also help you remember which symbol to use. It always wants to eat the larger number, and it turns away from the smaller number.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-002.png)",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-use-of-number-line"
  },
  {
    "record_id": "ch05-b015",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "Comparing integers on the number line",
      "h3": "Exercise 5.3: Compare integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.3: Compare integers",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-use-of-number-line"
  },
  {
    "record_id": "ch05-b015-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "Comparing integers on the number line",
      "h3": "Exercise 5.3: Compare integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.3: Compare integers\n\n1. Draw a number line showing all the integers from -10 to 10.",
    "answer_text": "![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-003.png)",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-use-of-number-line"
  },
  {
    "record_id": "ch05-b015-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "Comparing integers on the number line",
      "h3": "Exercise 5.3: Compare integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.3: Compare integers\n\n2. Place the correct symbol between each pair of numbers. Use your number line to help you.\n\na. 1 \\square 7\nb. 9 \\square 6\nc. 4 \\square 0\nd. -4 \\square 0\ne. 1 \\square -2\nf. -6 \\square 1\ng. -3 \\square -2\nh. -3 \\square -7\ni. -8 \\square -5\nj. 1 \\square -1",
    "answer_text": "a. 1<7\nb. 9&amp;gt;6\nc. 4&amp;gt;0\nd. -4<0\ne. 1&amp;gt;-2\nf. -6<1\ng. -3<-2\nh. -3&amp;gt;-7\ni. -8<-5\nj. 1&amp;gt;-1",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-use-of-number-line"
  },
  {
    "record_id": "ch05-b015-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "Comparing integers on the number line",
      "h3": "Exercise 5.3: Compare integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.3: Compare integers\n\n3. Arrange the following lists of numbers as required, using the correct symbol. Use your number line to help you.\n\na. Arrange from the smallest to the largest: 1;-5;-3; 2;-1\nb. Arrange from the largest to the smallest: -9; 6; 3;-6; 0",
    "answer_text": "a. -5<-3<-1<1<2\nb. 6&amp;gt;3&amp;gt;0&amp;gt;-6&amp;gt;-9",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-use-of-number-line"
  },
  {
    "record_id": "ch05-b016",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Adding integers"
    },
    "content_text": "We may use a number line to count. When we count to the right, we count in the positive direction. This is because the numbers become larger as we move to the right on a number line. When we count to the left, we count in the negative direction. This is because the numbers become smaller as we move to the left on a number line.\n\nWhen we add one integer to another, we may see it as units that are added along the number line. Examples of how we may interpret addition are:\n\n- $5+2$: from the number 5, count 2 units in the positive direction (to the right)\n- $-7+3$: from the number -7, count 3 units in the positive direction (to the right)\n- $1+(-4)$: from the number 1, count 4 units in the negative direction (to the left)\n- $-6+(-3)$: from the number -6, count 3 units in the negative direction (to the left)",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b017",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Adding integers"
    },
    "content_text": "Integers may be added in any order. For example, $-1+3$ and $3+(-1)$ give the same answer.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b018",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Worked example 5.3: Adding integers using the number line"
    },
    "content_text": "",
    "prompt_text": "Use a number line to determine the following: $-5+10$.\n\nStep 1: Draw a number line and find the first number on the line.\n\nThe first number is -5.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-004.png)\n\nStep 2: Determine how many units you must count, and in which direction.\n\nThe number 10 indicates that you must count 10 units in the positive direction, that is, to the right.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-005.png)\n\nA positive number does not always have a plus sign in front. When we write 10, it represents +10.\n\nStep 3: The answer is the number where you end up.\n\n$$\n-5+10=5\n$$\n\nUse a number line to determine the following: $-4+(-6)$.\n\nStep 1: Draw a number line and find the first number on the line.\n\nThe first number is -4.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-006.png)\n\nStep 2: Determine how many units you must count, and in which direction.\n\nThe number -6 indicates that you must count 6 units in the negative direction, that is, to the left.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-007.png)\n\nStep 3: The answer is the number where you end up.\n\n$$\n-4+(-6)=-10\n$$",
    "answer_text": "[{'asset_type': 'image', 'ordinal': 1, 'src': 'https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-004.png'}, {'asset_type': 'image', 'ordinal': 2, 'src': 'https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-005.png'}, {'asset_type': 'image', 'ordinal': 3, 'src': 'https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-006.png'}, {'asset_type': 'image', 'ordinal': 4, 'src': 'https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-007.png'}]",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b019",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.4: Use a number line to add integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.4: Use a number line to add integers\n\nUse number lines to add the following pairs of integers.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b019-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.4: Use a number line to add integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.4: Use a number line to add integers\n\n1. $1+6$",
    "answer_text": "![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-008.png)\n\n$$\n\\therefore 1+6=7\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b019-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.4: Use a number line to add integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.4: Use a number line to add integers\n\n2. $-6+7$",
    "answer_text": "![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-009.png)\n\n$$\n\\therefore -6+7=1\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b019-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.4: Use a number line to add integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.4: Use a number line to add integers\n\n3. $4+(-9)$",
    "answer_text": "![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-010.png)\n\n$$\n\\therefore 4+(-9)=-5\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b019-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.4: Use a number line to add integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.4: Use a number line to add integers\n\n4. $-2+(-6)$",
    "answer_text": "![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-011.png)\n\n$$\n\\therefore -2+(-6)=-8\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b020",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Subtracting integers"
    },
    "content_text": "There are different ways to think about subtraction. One way is to see it as another form of addition. Subtracting a number is the same as adding the \"opposite\" of the number. A number and its \"opposite\" are equal distances from zero, but on opposite sides. For example, -7 is the \"opposite\" number of 7, and 5 is the \"opposite\" number of -5.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b021",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Subtracting integers"
    },
    "content_text": "The \"opposite\" of a number referred to above has a special name. It is called the additive inverse of the number. When you add a number and its additive inverse, the answer is zero.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b022",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Subtracting integers"
    },
    "content_text": "The subtraction $6-4$ is the same as $6+(-4)$. Similarly, the subtraction $5-(-1)$ is the same as $5+(+1)$. After writing a subtraction as an addition, you may use the method shown in Worked example 5.3 to add the two numbers.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b023",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.5: Write subtraction as addition"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.5: Write subtraction as addition\n\nWrite each subtraction as an addition.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b023-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.5: Write subtraction as addition"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.5: Write subtraction as addition\n\n1. $1-6$",
    "answer_text": "$$\n\\require{enclose}1\\,\\enclose{circle}[mathcolor=\"red\"]{-}\\,6=1\\,\\enclose{circle}[mathcolor=\"red\"]{+}(-6)\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b023-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.5: Write subtraction as addition"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.5: Write subtraction as addition\n\n2. $-6-7$",
    "answer_text": "$$\n\\require{enclose}-6\\,\\enclose{circle}[mathcolor=\"red\"]{-}\\,7=-6\\,\\enclose{circle}[mathcolor=\"red\"]{+}(-7)\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b023-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.5: Write subtraction as addition"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.5: Write subtraction as addition\n\n3. $5-(-2)$",
    "answer_text": "$$\n\\require{enclose}5\\,\\enclose{circle}[mathcolor=\"red\"]{-}(-2)=5\\,\\enclose{circle}[mathcolor=\"red\"]{+}\\,2\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b023-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.5: Write subtraction as addition"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.5: Write subtraction as addition\n\n4. $-8-(-4)$",
    "answer_text": "$$\n\\require{enclose}-8\\,\\enclose{circle}[mathcolor=\"red\"]{-}(-4)=-8\\,\\enclose{circle}[mathcolor=\"red\"]{+}\\,4\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b024",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Subtracting integers"
    },
    "content_text": "Another way is to see subtraction as the difference between two numbers. For example, if you have 7 sweets and you eat 4 sweets, you have $7-4=3$ left. The number of sweets you have left is the difference between the sweets you had at the start and the sweets you ate. On a number line, the difference between the numbers 7 and 4 is 3 units.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-012.png)\n\nThe number 7 lies 3 units to the positive side of the number 4. Therefore, $7-4=+3$. At the same time, the number 4 lies 3 units to the negative side of the number 7. Therefore, $4-7=-3$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b025",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Subtracting integers"
    },
    "content_text": "Integers cannot be subtracted in any order. For example, $3-1$ and $1-3$ do not give the same answer.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b026",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Worked example 5.4: Subtracting integers using the number line"
    },
    "content_text": "",
    "prompt_text": "Use a number line to determine the following: $-5-3$\n\nUse a number line to determine the following: $-4-(-6)$",
    "answer_text": "Question 1\n\nStep 1: Identify the two integers that must be subtracted.\n\n$$\n\\require{enclose}-5\\, \\enclose{circle}[mathcolor=\"red\"]{-}\\,3\n$$\n\nThe numbers are $-5$ and 3.\n\nStep 2: Draw a number line and show the two numbers on the line.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-013.png)\n\nStep 3: Determine the difference between the two numbers.\n\nThe difference between $-5$ and 3 is 8 units.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-014.png)\n\nStep 4: Determine whether the number you are subtracting from lies to the positive or the negative side of the number that is being subtracted.\n\n$-5$ lies to the negative side of 3.\n\nStep 5: Use the information from Step 4 to decide whether the answer is positive or negative.\n\n$$\n-5-3=-8\n$$\n\nQuestion 2\n\nStep 1: Identify the two integers that must be subtracted.\n\n$$\n\\require{enclose}-4\\, \\enclose{circle}[mathcolor=\"red\"]{-}(-6)\n$$\n\nThe numbers are $-4$ and $-6$.\n\nStep 2: Draw a number line and show the two numbers on the line.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-015.png)\n\nStep 3: Determine the difference between the two numbers.\n\nThe difference between $-4$ and $-6$ is 2 units.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-016.png)\n\nStep 4: Determine whether the number you are subtracting from lies to the positive or the negative side of the number that is being subtracted.\n\n$-4$ lies to the positive side of $-6$.\n\nStep 5: Use the information from Step 4 to decide whether the answer is positive or negative.\n\n$$\n-4-(-6)=2\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b027",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.6: Use a number line to subtract integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.6: Use a number line to subtract integers\n\nFor each pair, use a number line to subtract the second integer from the first one.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b027-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.6: Use a number line to subtract integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.6: Use a number line to subtract integers\n\n1. $2-5$",
    "answer_text": "$$\n\\require{enclose}2\\,\\enclose{circle}[mathcolor=\"red\"]{-}\\,5\n$$\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-017.png)\n\n2 lies to the negative side of 5.\n\n$$\n\\therefore 2-5=-3\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b027-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.6: Use a number line to subtract integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.6: Use a number line to subtract integers\n\n2. $-1-3$",
    "answer_text": "$$\n\\require{enclose}-1\\,\\enclose{circle}[mathcolor=\"red\"]{-}\\,3\n$$\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-018.png)\n\n$-1$ lies to the negative side of 3.\n\n$$\n\\therefore -1-3=-4\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b027-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.6: Use a number line to subtract integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.6: Use a number line to subtract integers\n\n3. $5-(-6)$",
    "answer_text": "$$\n\\require{enclose}5\\,\\enclose{circle}[mathcolor=\"red\"]{-}(-6)\n$$\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-019.png)\n\n5 lies to the positive side of $-6$.\n\n$$\n\\therefore 5-(-6)=11\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b027-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Exercise 5.6: Use a number line to subtract integers"
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.6: Use a number line to subtract integers\n\n4. $-2-(-7)$",
    "answer_text": "$$\n\\require{enclose}-2\\,\\enclose{circle}[mathcolor=\"red\"]{-}(-7)\n$$\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-020.png)\n\n$-2$ lies to the positive side of $-7$.\n\n$$\n\\therefore -2-(-7)=5\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b028",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.4 Addition and subtraction using the number line",
      "h3": "Worked example 5.5: Comparing different methods of subtracting integers"
    },
    "content_text": "",
    "prompt_text": "Determine the following: $-4-3$",
    "answer_text": "Identify the two integers that must be subtracted.\n\n$$\n\\require{enclose}-4\\,\\enclose{circle}[mathcolor=\"red\"]{-}\\,3\n$$\n\nThe number 3 must be subtracted from the number $-4$.\n\nMethod 1: Regard subtraction as another form of addition.\n\n$$\n\\require{enclose}-4\\,\\enclose{circle}[mathcolor=\"red\"]{-}\\,3=-4\\,\\enclose{circle}[mathcolor=\"red\"]{+}(-3)\n$$\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-021.png)\n\n$$\n\\therefore -4+(-3)=-7\n$$\n\nMethod 2: Regard subtraction as the difference between two numbers.\n\n$$\n\\require{enclose}-4\\,\\enclose{circle}[mathcolor=\"red\"]{-}\\,3\n$$\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-022.png)\n\n$-4$ lies to the negative side of 3.\n\n$$\n\\therefore -4-3=-7\n$$\n\nThe two methods give the same answer.",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b029",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.5 Practical applications",
      "h3": "Thermometers"
    },
    "content_text": "A thermometer is an instrument we use to measure temperature. Most thermometers we use in everyday life measure the temperature in degrees Celsius $(^\\circ \\text C)$. The freezing point of water, $0 ^\\circ \\text C$, is shown somewhere in the middle of the thermometer. Temperatures above $0 ^\\circ \\text C$ are positive and temperatures below $0 ^\\circ \\text C$ are negative. The average body temperature of a healthy human is $37 ^\\circ \\text C$, as shown on the thermometer below. The typical temperature of the freezing compartment of a refrigerator is $-18 ^\\circ \\text C$.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-05-023.png)",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-everyday-application-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b030",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.5 Practical applications",
      "h3": "Banking"
    },
    "content_text": "Banks allow people to borrow money from them. When you put money into your bank account, you have a positive bank balance. When you draw money from your bank account, it is subtracted from your balance. If you withdraw more money than you have in your bank account, your bank account goes into an overdraft. Your bank balance becomes negative. Part of a bank statement is shown below.\n\n$$\n\\begin{array}{|l l r|}\n\\hline\n\\ggg \\triangleright\\triangleright\\triangleright & \\textbf{BESTBANK NIGERIA}\\\\\n\\hline\n \\text{2019/10/01} & \\text{Balance brought forward} &  ₦120,512.45 \\\\\n \\text{2019/10/05} & \\text{Deposit} &  ₦13,000.00 \\\\\n \\text{2019/10/12} & \\text{Withdrawal} &  -\\,₦4,000.00 \\\\\n \\text{2019/10/15} & \\text{Credit card transaction} &  -\\,₦52,514.05 \\\\\n \\text{2019/10/18} & \\text{Refund} &  ₦500.00 \\\\\n \\text{2019/10/22} & \\text{Credit card transaction} &  -\\,₦7,223.40 \\\\\n \\text{2019/10/25} & \\text{Withdrawal} &  -\\,₦80,100.00 \\\\\n \\hline\n \\text{2019/10/31} & \\text{Balance carried over} &  -\\,₦9,825.00 \\\\\n \\hline\n \\end{array}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-everyday-application-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b031",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.5 Practical applications",
      "h3": "Movement along the same straight line"
    },
    "content_text": "When we move along the same straight line, we may use positive and negative numbers to determine our position relative to a starting point. The diagram shows part of a school yard.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-05-0_011.png)\n\nSuppose you walk from the swimming pool 100 m to the right and then 20 m to the left. If distances to the right are taken as positive and distances to the left are taken as negative, you end up $100\\space \\text m + (-20\\space \\text m)=80\\space\\text m$ to the right of the swimming pool.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-everyday-application-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b032",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.5 Practical applications",
      "h3": "Exercise 5.7: Use positive and negative numbers to solve problems."
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.7: Use positive and negative numbers to solve problems.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-everyday-application-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b032-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.5 Practical applications",
      "h3": "Exercise 5.7: Use positive and negative numbers to solve problems."
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.7: Use positive and negative numbers to solve problems.\n\n1. Food is taken out of the freezing compartment of a refrigerator. Its temperature changes from -10\\space ^\\circ \\text C to 7\\space ^\\circ \\text C. Calculate by how much the temperature of the food increased.\n\nHint: To calculate the change in a quantity, use the following principle: \\text{change}=\\text{final value}-\\text{initial value}",
    "answer_text": "7\\space ^\\circ \\text C - (-10\\space ^\\circ \\text C)\n\n\\require{enclose}\n$$\n\\begin{array}{r l}\n7\\,\\enclose{circle}[mathcolor=\"red\"]{-}(-10)&=7\\,\\enclose{circle}[mathcolor=\"red\"]{+}(+10)\\newline\n&=17\\space ^\\circ \\text C\n\\end{array}\n$$\nThe temperature of the food increased by 17\\space ^\\circ \\text C.",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-everyday-application-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b032-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.5 Practical applications",
      "h3": "Exercise 5.7: Use positive and negative numbers to solve problems."
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.7: Use positive and negative numbers to solve problems.\n\n2. A piece of meat is at a room temperature of 25\\space ^\\circ \\text C. It is placed in a freezer. The temperature of the meat drops by 40\\space ^\\circ \\text C. Calculate the new temperature of the meat.",
    "answer_text": "If the temperature dropped, we must count 40 units in the negative direction: 25\\space ^\\circ \\text C +(- 40\\space ^\\circ \\text C)\n\nStart at the number +25.\n\nCount 25 units in the negative direction. Now you are at zero.\n\nCount another 40-25=15 units in the negative direction. Now you are at -15.\n\nThe new temperature is -15\\space ^\\circ \\text C.",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-everyday-application-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b032-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.5 Practical applications",
      "h3": "Exercise 5.7: Use positive and negative numbers to solve problems."
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.7: Use positive and negative numbers to solve problems.\n\n3. Scientists have worked out that the average temperature on the surface of the Earth is 14\\space ^\\circ \\text C, and that the average temperature on the surface of Mars is -63\\space ^\\circ \\text C. Calculate how much warmer than Mars the Earth is.",
    "answer_text": "If we want to know the difference between the temperature of the Earth and of Mars, we must subtract the temperature of Mars: 14\\space ^\\circ \\text C -(- 63\\space ^\\circ \\text C)\n\n\\require{enclose}\n$$\n\\begin{array}{r l}\n14\\,\\enclose{circle}[mathcolor=\"red\"]{-}(-63)&=14\\,\\enclose{circle}[mathcolor=\"red\"]{+}(+63)\\newline\n&=77\\space ^\\circ \\text C\n\\end{array}\n$$\nThe Earth is 77\\space ^\\circ \\text C warmer than Mars.",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-everyday-application-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b032-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.5 Practical applications",
      "h3": "Exercise 5.7: Use positive and negative numbers to solve problems."
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.7: Use positive and negative numbers to solve problems.\n\n4. Chioma and Ndidi are sisters. At the start of the school holidays, Chioma owes Ndidi ₦50. Ndidi has another ₦25 that she saved during the term. Both girls earn pocket money during the holidays. They each receive ₦750 in total. Chioma repays her debt to Ndidi. Calculate how much money each of them have at the end of the holidays.",
    "answer_text": "$$\n\\begin{array}{|l r r|}\n \\hline\n  & \\text{Chioma} &  \\text{Ndidi} \\newline\n  \\hline\n   \\text{Start} & ₦0 &  ₦25 \\newline\n   \\text{Earnings} & ₦750 &  ₦750 \\newline\n   \\text{Debt} & -\\,₦50 &  ₦50 \\newline\n   \\hline\n   \\text{Balance} & ₦700 &  ₦825 \\newline\n   \\hline\n   \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-everyday-application-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b032-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.5 Practical applications",
      "h3": "Exercise 5.7: Use positive and negative numbers to solve problems."
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.7: Use positive and negative numbers to solve problems.\n\n5. A man owes the bank ₦5,500. He deposits ₦6,000, but later withdraws ₦800. Calculate his new bank balance.",
    "answer_text": "$$\n\\begin{array}{|l r|}\n \\hline\n   \\text{Start} &  -\\,₦5,500 \\newline\n   \\text{Deposit} &  ₦6,000 \\newline\n   \\text{Debt} &  -\\,₦800 \\newline\n   \\hline\n   \\text{Balance} &  -\\,₦300 \\newline\n   \\hline\n   \\end{array}\n$$",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-everyday-application-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b032-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.5 Practical applications",
      "h3": "Exercise 5.7: Use positive and negative numbers to solve problems."
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.7: Use positive and negative numbers to solve problems.\n\n6. Oladapo walks east from his house to school. After walking for 750 m, he realizes that he forgot a book at home. He turns around and walks back. His cell phone rings when he is 200 m from the point where he turned around. Calculate how far from his house Oladapo is when his phone rings.",
    "answer_text": "If east is taken as positive: 750\\space \\text m+(-200\\space \\text m)=550\\space\\text m\n\nHe is 550 m to the east of his house.",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-everyday-application-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b032-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.5 Practical applications",
      "h3": "Exercise 5.7: Use positive and negative numbers to solve problems."
    },
    "content_text": "",
    "prompt_text": "### Exercise 5.7: Use positive and negative numbers to solve problems.\n\n7. A girl sits in a tree. She throws a ball straight up into the air. It reaches a height of 1 m above the girl's hand and then falls back. The ball falls straight downwards for 3 m, past the tree, and lands on the ground. Calculate the distance between the girl's hand and the ground.\n\nA bird flies straight north. After 50 m it turns around. It flies straight south for 90 m. It turns around again and flies straight north for 10 m. Determine where it is in relation to its original position.",
    "answer_text": "If upwards is taken as positive: 1\\space \\text m+(-3\\space \\text m)=-2\\space\\text m\n\nThe ground is 2 m below the girl's hand.\n\nIf north is taken as positive: 50\\space \\text m+(-90\\space \\text m)+(10\\space \\text m)=-30\\space\\text m\n\nThe bird is 30 m south of its original position.",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-everyday-application-of-positive-and-negative-integers"
  },
  {
    "record_id": "ch05-b033",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 5: Addition and subtraction of integers",
      "h2": "5.6 Summary",
      "h3": null
    },
    "content_text": "- The place value of a digit tells us what the value of that digit is, based on its position in a number.\n- When we add or subtract large numbers, we line up the units, tens, hundreds and thousands of the numbers.\n- A number line is a straight line, divided into equal segments, that shows the positions of numbers.\n- Positive numbers are larger than zero and lie to the right of zero on a number line.\n- Negative numbers are smaller than zero and lie to the left of zero on a number line.\n- Zero is neither positive nor negative.\n- The symbol < means \"smaller than\", and 3<5 means three is smaller than five. The symbol > means \"greater than\", and 5>3 means five is greater than three.\n- When we add one integer to another, we may see it as units that are added along the number line. When we add positive numbers, we count to the right on a number line. When we add negative numbers, we count to the left on a number line.\n- Subtracting a number is the same as adding the \"opposite\" of the number. For example, $2-7$ is the same as $2+(-7)$.\n- Subtraction may also be seen as the difference between two numbers. For example, there are 5 units between the numbers 2 and 7. If the number which is subtracted from lies to the negative side of the number that is subtracted, the difference is negative: $2-7=-5$. If the number which is subtracted from lies to the positive side of the number that is subtracted, the difference is positive: $7-2=5$.\n- A thermometer is an instrument used to measure temperature. Temperatures above $0\\space ^\\circ\\text C$ are positive. Temperatures below $0\\space ^\\circ\\text C$ are negative.\n- A positive bank balance means you have money in the bank. A negative bank balance means you owe the bank money.\n- For movement along a straight line, we take one direction as positive. The opposite direction is negative.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers"
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
