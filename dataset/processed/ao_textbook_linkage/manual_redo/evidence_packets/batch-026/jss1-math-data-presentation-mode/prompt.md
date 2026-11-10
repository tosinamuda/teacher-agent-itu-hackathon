# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-5",
  "topic_key": "jss1-math-data-presentation",
  "topic": "Data Presentation",
  "subtopic_id": "jss1-math-data-presentation-mode",
  "subtopic_title": "Mode",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-data-presentation-mode-po01",
        "source_performance_objective_index": 1,
        "text": "Determine the mode of a given set of data"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "mode-ao-determine-mode",
          "text": "Determine the mode of a given set of data."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch17-b018",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": null
    },
    "content_text": "After we have collected and organised data, we need to summarise it. **Summarising data** allows us to see at a glance what important things the data has told us.\n\nWhen we summarise data, we use different methods to sum up what the whole set of data has told us. These methods give us numbers that are called the mean, the mode and the median.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-presentation-mean"
  },
  {
    "record_id": "ch17-b019",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": null
    },
    "content_text": "**summarising data** Summarising data is using the mean, the mode and the median to sum up what the whole set of data has told us.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-presentation-mean"
  },
  {
    "record_id": "ch17-b023",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": "The mode"
    },
    "content_text": "The mode is the data item that occurs most often in a set of data. No calculation is needed to find the mode. You may have to sort the data, and then count to find the value that appears most often.\n\nFor example, if you have the data set $\\text{2; 5; 7; 7; 7; 10; 12; 12; 15}$, the mode is 7, because 7 occurs three times.\n\nAs you can see, 12 is also repeated, but it is only repeated twice. If 12 were also repeated three times, you would have two modes for this data set: 7 and 12.\n\nIf no number is repeated, then there is no mode for this data set.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-presentation-mode"
  },
  {
    "record_id": "ch17-b024",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": "Worked example 17.5: Finding the mode"
    },
    "content_text": "",
    "prompt_text": "Find the mode of this data set: $\\text{10; 7; 7; 6; 9; 5}$.",
    "answer_text": "Step 1: First sort the data, writing the values in order from smallest to largest.\n\n$$\n\\text{5; 6; 7; 7; 9; 10}\n$$\n\nStep 2: Identify the mode, which is the value that appears the most often.\n\nThe number 7 appears twice.\n\nThe mode is 7.",
    "primary_subtopic_id": "jss1-math-data-presentation-mode"
  },
  {
    "record_id": "ch17-b025",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": "Worked example 17.6: Finding the mode when there is more than one mode"
    },
    "content_text": "",
    "prompt_text": "Find the mode of the data set $\\text{10; 8; 8; 9; 7; 9; 10; 11; 6; 11}$.",
    "answer_text": "Step 1: First sort the data by writing the values in order from smallest to largest.\n\n$$\n\\text{6; 7; 8; 8; 9; 9; 10; 11; 11}\n$$\n\nStep 2: Identify the mode.\n\nThe numbers 8, 9 and 11 all appear twice.\n\nThe modes are 8; 9 and 11.\n\nIf there are two or more modes, give all of the mode values separated by a semi-colon (;) and \"and\".",
    "primary_subtopic_id": "jss1-math-data-presentation-mode"
  },
  {
    "record_id": "ch17-b026",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": "Exercise 17.5: Find the mode of a data set"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.5: Find the mode of a data set",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-presentation-mode"
  },
  {
    "record_id": "ch17-b026-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": "Exercise 17.5: Find the mode of a data set"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.5: Find the mode of a data set\n\n1. Find the mode of the following set of data:\n\n$$\n\\text{1; 2; 3; 4; 5; 1; 2; 3; 4; 1; 2; 3; 1; 2; 1}\n$$",
    "answer_text": "First sort the data from smallest to largest:\n\n$$\n\\text {1; 1; 1; 1; 1; 2; 2; 2; 2; 3; 3; 3; 4; 4; 5}\n$$\n\nMany numbers appear more than once, but 1 appears five times.\n\nThe mode is 1.",
    "primary_subtopic_id": "jss1-math-data-presentation-mode"
  },
  {
    "record_id": "ch17-b026-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": "Exercise 17.5: Find the mode of a data set"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.5: Find the mode of a data set\n\n2. Find the mode of the following set of data:\n\n$$\n\\text{5; 5; 6; 8; 9; 9; 11; 11}\n$$",
    "answer_text": "The data is already sorted into ascending order.\n\n5, 9 and 11 all appear twice.\n\nThe modes are 5; 9 and 11.",
    "primary_subtopic_id": "jss1-math-data-presentation-mode"
  },
  {
    "record_id": "ch17-b026-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": "Exercise 17.5: Find the mode of a data set"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.5: Find the mode of a data set\n\n3. Find the mode of the following set of measurements:\n\n$$\n\\text{ 4 m; 7 m; 6 m; 11 m; 8 m; 5 m; 9 m; 6 m; 11 m}\n$$",
    "answer_text": "Sorted data:\n\n$$\n\\text{4 m; 5 m; 6 m; 6 m; 7 m; 8 m; 9 m; 11 m; 11 m}\n$$\n\nThe modes are 6 m and 11 m.",
    "primary_subtopic_id": "jss1-math-data-presentation-mode"
  },
  {
    "record_id": "ch17-b026-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": "Exercise 17.5: Find the mode of a data set"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.5: Find the mode of a data set\n\n4. Funeka decides to record the colours of everyone's schoolbags as they arrive at school. She makes a tally list to record the colours. Later, she uses the tallies to draw up this frequency table:\n\n| Colour of schoolbags | Frequency |\n| --- | --- |\n| Blue | 27 |\n| Red | 16 |\n| White | 43 |\n| Black | 7 |\n| Green | 16 |\n\nWhat colour is the mode?",
    "answer_text": "The mode is the data item that appears the most often, so the mode will be the colour with the highest frequency.\n\nThe mode of this data set is white.",
    "primary_subtopic_id": "jss1-math-data-presentation-mode"
  },
  {
    "record_id": "ch17-b032",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": "Worked example 17.9: Finding mean, median and mode for one data set"
    },
    "content_text": "",
    "prompt_text": "Find the mean, median and mode for the data set $\\text{5; 11; 9; 9; 10; 8; 9; 10; 6}$.\n\n- If necessary, round your answer to two decimal places.\n- If there are two or more modes, give all of the mode values, separated by \"and\" and/or a semi-colon (;).",
    "answer_text": "Step 1: Find the mean of the data set by adding up all the values in the data set and dividing by the number of data values.\n\n$$\n\\text{The mean} = \\dfrac{\\text{the sum of the data values}}{\\text{the number of data values}} = \\dfrac{\\text{5 + 11 + 9 + 9 + 10 + 8 + 9 + 10 + 6}}{\\text{9}} = \\dfrac{\\text{77}}{\\text{9}} = \\text{8.56}\n$$\n\nStep 2: Find the mode by arranging the data in ascending order, and then finding the value or values that appear the most.\n\nArranging the data in order we get $\\text{5; 6; 8; 9; 9; 9; 10; 10; 11}$.\n\nThe mode is 9 as it appears three times.\n\nStep 3: Find the median by finding the middle value in the data set.\n\nWe have 9 values: $\\text{5; 6; 8; 9; 9; 9; 10; 10; 11}$, so the median is the fifth value, which is a 9.\n\nAnswer: The mean is 8.56, the mode is 9, and the median is 9.",
    "primary_subtopic_id": "jss1-math-data-presentation-mean"
  },
  {
    "record_id": "ch17-b033",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": "Exercise 17.7: Find the mean, median and mode of a data set"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.7: Find the mean, median and mode of a data set\n\nIf necessary, round your answer to two decimal places.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-presentation-mean"
  },
  {
    "record_id": "ch17-b033-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": "Exercise 17.7: Find the mean, median and mode of a data set"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.7: Find the mean, median and mode of a data set\n\nIf necessary, round your answer to two decimal places.\n\n1. Find the mean, median and mode for the following set of data: $\\text{11; 7; 9; 5; 7; 8; 7}$.",
    "answer_text": "$$\n\\text{Mean} = \\dfrac{\\text{the sum of the data values}}{\\text{the number of data values}} = \\dfrac{\\text{11 + 7 + 9 + 5 + 7 + 8  + 7}}{\\text{7}} = \\dfrac{\\text{54}}{\\text{7}} = \\text{7.71}\n$$\n\nAscending order: $\\text{5 ; 7 ; 7 ; 7 ; 8 ; 9 ; 11}$\n\n7 is the mode as it appears three times.\n\nThe median (middle value) is 7.\n\nAnswer: The mean is 7.71, the mode is 7 and the median is 7.",
    "primary_subtopic_id": "jss1-math-data-presentation-mean"
  },
  {
    "record_id": "ch17-b033-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": "Exercise 17.7: Find the mean, median and mode of a data set"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.7: Find the mean, median and mode of a data set\n\nIf necessary, round your answer to two decimal places.\n\n2. Find the mean, median and mode for the data set $\\text{9; 6; 5; 9; 6; 10; 11; 8}$.",
    "answer_text": "$$\n\\text{Mean} = \\dfrac{\\text{9 + 6 + 5 + 9 + 6 + 10 + 11 + 8}}{\\text{7}} = \\dfrac{\\text{64}}{\\text{8}} = \\text{8}\n$$\n\nAscending order: $\\text{5 ; 6 ; 6 ; 8 ; 9 ; 9 ; 10 ; 11}$\n\nThe modes are 6 and 9.\n\nThe median is $=\\frac{\\text{8} + \\text{9}}{\\text{2}} = \\text{8.5}$.\n\nAnswer: The mean is 8, the modes are 6 and 9, and the median is 8.5.",
    "primary_subtopic_id": "jss1-math-data-presentation-mean"
  },
  {
    "record_id": "ch17-b040",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.4 Summary",
      "h3": null
    },
    "content_text": "- Collecting, organising and presenting data forms part of the data handling cycle.\n- Data can be collected using observations, interviews, questionnaires and existing databases.\n- The method chosen for collecting the data depends on the type of research being done.\n- Organising data is bringing it together in a systematic way that makes it easier to read.\n- Data can be organised using tallies and frequency tables.\n- Tallies are a way of counting by drawing a short vertical line to record each item as you count it. For every fifth mark, you draw a diagonal line through the first four lines.\n- The frequency is how many times an event occurred.\n- A frequency table shows the list of different categories, together with the number of times each category occurs.\n- We summarise data by finding one or two numbers that sum up the whole set of data, using the mean, median and mode.\n  - The mean gives the average, and is calculated by adding all the values together and dividing by the number of values in the data set.\n  - The mode is the data item (or items) that occurs most often in a set of data.\n  - The median is the middle value in a set of data values.\n- Presenting data is finding a way to show results so they can be shared with other people.\n- Bar graphs are used to present data that is compared in categories.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
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
  "theme_key": "jss1-theme-5",
  "topic_key": "jss1-math-data-presentation",
  "topic": "Data Presentation",
  "subtopic_id": "jss1-math-data-presentation-mode",
  "subtopic_title": "Mode",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-data-presentation-mode-po01",
        "source_performance_objective_index": 1,
        "text": "Determine the mode of a given set of data"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "mode-ao-determine-mode",
          "text": "Determine the mode of a given set of data."
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
    "record_id": "ch17-b018",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": null
    },
    "content_text": "After we have collected and organised data, we need to summarise it. **Summarising data** allows us to see at a glance what important things the data has told us.\n\nWhen we summarise data, we use different methods to sum up what the whole set of data has told us. These methods give us numbers that are called the mean, the mode and the median.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-presentation-mean"
  },
  {
    "record_id": "ch17-b019",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": null
    },
    "content_text": "**summarising data** Summarising data is using the mean, the mode and the median to sum up what the whole set of data has told us.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-presentation-mean"
  },
  {
    "record_id": "ch17-b023",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": "The mode"
    },
    "content_text": "The mode is the data item that occurs most often in a set of data. No calculation is needed to find the mode. You may have to sort the data, and then count to find the value that appears most often.\n\nFor example, if you have the data set $\\text{2; 5; 7; 7; 7; 10; 12; 12; 15}$, the mode is 7, because 7 occurs three times.\n\nAs you can see, 12 is also repeated, but it is only repeated twice. If 12 were also repeated three times, you would have two modes for this data set: 7 and 12.\n\nIf no number is repeated, then there is no mode for this data set.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-presentation-mode"
  },
  {
    "record_id": "ch17-b024",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": "Worked example 17.5: Finding the mode"
    },
    "content_text": "",
    "prompt_text": "Find the mode of this data set: $\\text{10; 7; 7; 6; 9; 5}$.",
    "answer_text": "Step 1: First sort the data, writing the values in order from smallest to largest.\n\n$$\n\\text{5; 6; 7; 7; 9; 10}\n$$\n\nStep 2: Identify the mode, which is the value that appears the most often.\n\nThe number 7 appears twice.\n\nThe mode is 7.",
    "primary_subtopic_id": "jss1-math-data-presentation-mode"
  },
  {
    "record_id": "ch17-b025",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": "Worked example 17.6: Finding the mode when there is more than one mode"
    },
    "content_text": "",
    "prompt_text": "Find the mode of the data set $\\text{10; 8; 8; 9; 7; 9; 10; 11; 6; 11}$.",
    "answer_text": "Step 1: First sort the data by writing the values in order from smallest to largest.\n\n$$\n\\text{6; 7; 8; 8; 9; 9; 10; 11; 11}\n$$\n\nStep 2: Identify the mode.\n\nThe numbers 8, 9 and 11 all appear twice.\n\nThe modes are 8; 9 and 11.\n\nIf there are two or more modes, give all of the mode values separated by a semi-colon (;) and \"and\".",
    "primary_subtopic_id": "jss1-math-data-presentation-mode"
  },
  {
    "record_id": "ch17-b026",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": "Exercise 17.5: Find the mode of a data set"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.5: Find the mode of a data set",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-presentation-mode"
  },
  {
    "record_id": "ch17-b026-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": "Exercise 17.5: Find the mode of a data set"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.5: Find the mode of a data set\n\n1. Find the mode of the following set of data:\n\n$$\n\\text{1; 2; 3; 4; 5; 1; 2; 3; 4; 1; 2; 3; 1; 2; 1}\n$$",
    "answer_text": "First sort the data from smallest to largest:\n\n$$\n\\text {1; 1; 1; 1; 1; 2; 2; 2; 2; 3; 3; 3; 4; 4; 5}\n$$\n\nMany numbers appear more than once, but 1 appears five times.\n\nThe mode is 1.",
    "primary_subtopic_id": "jss1-math-data-presentation-mode"
  },
  {
    "record_id": "ch17-b026-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": "Exercise 17.5: Find the mode of a data set"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.5: Find the mode of a data set\n\n2. Find the mode of the following set of data:\n\n$$\n\\text{5; 5; 6; 8; 9; 9; 11; 11}\n$$",
    "answer_text": "The data is already sorted into ascending order.\n\n5, 9 and 11 all appear twice.\n\nThe modes are 5; 9 and 11.",
    "primary_subtopic_id": "jss1-math-data-presentation-mode"
  },
  {
    "record_id": "ch17-b026-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": "Exercise 17.5: Find the mode of a data set"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.5: Find the mode of a data set\n\n3. Find the mode of the following set of measurements:\n\n$$\n\\text{ 4 m; 7 m; 6 m; 11 m; 8 m; 5 m; 9 m; 6 m; 11 m}\n$$",
    "answer_text": "Sorted data:\n\n$$\n\\text{4 m; 5 m; 6 m; 6 m; 7 m; 8 m; 9 m; 11 m; 11 m}\n$$\n\nThe modes are 6 m and 11 m.",
    "primary_subtopic_id": "jss1-math-data-presentation-mode"
  },
  {
    "record_id": "ch17-b026-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": "Exercise 17.5: Find the mode of a data set"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.5: Find the mode of a data set\n\n4. Funeka decides to record the colours of everyone's schoolbags as they arrive at school. She makes a tally list to record the colours. Later, she uses the tallies to draw up this frequency table:\n\n| Colour of schoolbags | Frequency |\n| --- | --- |\n| Blue | 27 |\n| Red | 16 |\n| White | 43 |\n| Black | 7 |\n| Green | 16 |\n\nWhat colour is the mode?",
    "answer_text": "The mode is the data item that appears the most often, so the mode will be the colour with the highest frequency.\n\nThe mode of this data set is white.",
    "primary_subtopic_id": "jss1-math-data-presentation-mode"
  },
  {
    "record_id": "ch17-b032",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": "Worked example 17.9: Finding mean, median and mode for one data set"
    },
    "content_text": "",
    "prompt_text": "Find the mean, median and mode for the data set $\\text{5; 11; 9; 9; 10; 8; 9; 10; 6}$.\n\n- If necessary, round your answer to two decimal places.\n- If there are two or more modes, give all of the mode values, separated by \"and\" and/or a semi-colon (;).",
    "answer_text": "Step 1: Find the mean of the data set by adding up all the values in the data set and dividing by the number of data values.\n\n$$\n\\text{The mean} = \\dfrac{\\text{the sum of the data values}}{\\text{the number of data values}} = \\dfrac{\\text{5 + 11 + 9 + 9 + 10 + 8 + 9 + 10 + 6}}{\\text{9}} = \\dfrac{\\text{77}}{\\text{9}} = \\text{8.56}\n$$\n\nStep 2: Find the mode by arranging the data in ascending order, and then finding the value or values that appear the most.\n\nArranging the data in order we get $\\text{5; 6; 8; 9; 9; 9; 10; 10; 11}$.\n\nThe mode is 9 as it appears three times.\n\nStep 3: Find the median by finding the middle value in the data set.\n\nWe have 9 values: $\\text{5; 6; 8; 9; 9; 9; 10; 10; 11}$, so the median is the fifth value, which is a 9.\n\nAnswer: The mean is 8.56, the mode is 9, and the median is 9.",
    "primary_subtopic_id": "jss1-math-data-presentation-mean"
  },
  {
    "record_id": "ch17-b033",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": "Exercise 17.7: Find the mean, median and mode of a data set"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.7: Find the mean, median and mode of a data set\n\nIf necessary, round your answer to two decimal places.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-presentation-mean"
  },
  {
    "record_id": "ch17-b033-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": "Exercise 17.7: Find the mean, median and mode of a data set"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.7: Find the mean, median and mode of a data set\n\nIf necessary, round your answer to two decimal places.\n\n1. Find the mean, median and mode for the following set of data: $\\text{11; 7; 9; 5; 7; 8; 7}$.",
    "answer_text": "$$\n\\text{Mean} = \\dfrac{\\text{the sum of the data values}}{\\text{the number of data values}} = \\dfrac{\\text{11 + 7 + 9 + 5 + 7 + 8  + 7}}{\\text{7}} = \\dfrac{\\text{54}}{\\text{7}} = \\text{7.71}\n$$\n\nAscending order: $\\text{5 ; 7 ; 7 ; 7 ; 8 ; 9 ; 11}$\n\n7 is the mode as it appears three times.\n\nThe median (middle value) is 7.\n\nAnswer: The mean is 7.71, the mode is 7 and the median is 7.",
    "primary_subtopic_id": "jss1-math-data-presentation-mean"
  },
  {
    "record_id": "ch17-b033-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.2 Summarising data",
      "h3": "Exercise 17.7: Find the mean, median and mode of a data set"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.7: Find the mean, median and mode of a data set\n\nIf necessary, round your answer to two decimal places.\n\n2. Find the mean, median and mode for the data set $\\text{9; 6; 5; 9; 6; 10; 11; 8}$.",
    "answer_text": "$$\n\\text{Mean} = \\dfrac{\\text{9 + 6 + 5 + 9 + 6 + 10 + 11 + 8}}{\\text{7}} = \\dfrac{\\text{64}}{\\text{8}} = \\text{8}\n$$\n\nAscending order: $\\text{5 ; 6 ; 6 ; 8 ; 9 ; 9 ; 10 ; 11}$\n\nThe modes are 6 and 9.\n\nThe median is $=\\frac{\\text{8} + \\text{9}}{\\text{2}} = \\text{8.5}$.\n\nAnswer: The mean is 8, the modes are 6 and 9, and the median is 8.5.",
    "primary_subtopic_id": "jss1-math-data-presentation-mean"
  },
  {
    "record_id": "ch17-b040",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.4 Summary",
      "h3": null
    },
    "content_text": "- Collecting, organising and presenting data forms part of the data handling cycle.\n- Data can be collected using observations, interviews, questionnaires and existing databases.\n- The method chosen for collecting the data depends on the type of research being done.\n- Organising data is bringing it together in a systematic way that makes it easier to read.\n- Data can be organised using tallies and frequency tables.\n- Tallies are a way of counting by drawing a short vertical line to record each item as you count it. For every fifth mark, you draw a diagonal line through the first four lines.\n- The frequency is how many times an event occurred.\n- A frequency table shows the list of different categories, together with the number of times each category occurs.\n- We summarise data by finding one or two numbers that sum up the whole set of data, using the mean, median and mode.\n  - The mean gives the average, and is calculated by adding all the values together and dividing by the number of values in the data set.\n  - The mode is the data item (or items) that occurs most often in a set of data.\n  - The median is the middle value in a set of data values.\n- Presenting data is finding a way to show results so they can be shared with other people.\n- Bar graphs are used to present data that is compared in categories.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
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
