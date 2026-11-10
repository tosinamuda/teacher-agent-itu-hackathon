# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-5",
  "topic_key": "jss1-math-data-presentation",
  "topic": "Data Presentation",
  "subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data",
  "subtopic_title": "Graphical presentation of data",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-data-presentation-graphical-presentation-of-data-po01",
        "source_performance_objective_index": 1,
        "text": "Present data using bar charts, pie charts and histograms"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "graphical-presentation-of-data-ao-present-using-bar-charts",
          "text": "Present data using bar charts."
        },
        {
          "atomic_objective_id": "graphical-presentation-of-data-ao-present-using-pie-charts",
          "text": "Present data using pie charts."
        },
        {
          "atomic_objective_id": "graphical-presentation-of-data-ao-present-using-histograms",
          "text": "Present data using histograms."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-data-presentation-graphical-presentation-of-data-po02",
        "source_performance_objective_index": 2,
        "text": "Read and interpret information from bar charts, pie charts and histograms"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "graphical-presentation-of-data-ao-read-bar-charts",
          "text": "Read information from bar charts."
        },
        {
          "atomic_objective_id": "graphical-presentation-of-data-ao-interpret-bar-charts",
          "text": "Interpret information from bar charts."
        },
        {
          "atomic_objective_id": "graphical-presentation-of-data-ao-read-pie-charts",
          "text": "Read information from pie charts."
        },
        {
          "atomic_objective_id": "graphical-presentation-of-data-ao-interpret-pie-charts",
          "text": "Interpret information from pie charts."
        },
        {
          "atomic_objective_id": "graphical-presentation-of-data-ao-read-histograms",
          "text": "Read information from histograms."
        },
        {
          "atomic_objective_id": "graphical-presentation-of-data-ao-interpret-histograms",
          "text": "Interpret information from histograms."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch17-b034",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": null
    },
    "content_text": "So far we have collected the data, then organised the data, and summarised the data. Now we need to find ways to present the data, so that we can share the results of our research with other people.\n\nThere are many ways of presenting data to show results, including written reports, tables and graphs. Graphs are useful as they give a picture of the results that is easy to understand. We will use bar graphs.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b035",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": null
    },
    "content_text": "presenting data Presenting data is finding a way to show results so they can be shared with other people.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b036",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Using bar graphs to present data"
    },
    "content_text": "Bar graphs are used to display data that has been collected and organised in categories. An example of categories is the cars of different colours that we looked at earlier in this chapter.\n\nA bar graph is a chart that uses either horizontal or vertical bars to show how categories compare with each other. The length of each bar shows the value that the bar represents.\n\nFor example, every month for five months, the manager of a new shop keeps count of how many customers visit the shop. The manager created this bar graph to show the results.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-g10-math-lit-12-gd-0030.png\n\n- The categories (the months) are shown along the horizontal axis.\n- The frequency (the number of customers) is shown along the vertical axis.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b037",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Using bar graphs to present data"
    },
    "content_text": "It is important to use an appropriate interval on the graph to show the frequency.\n\nThis bar graph uses an interval of 100 along the vertical axis. If the largest frequency was only 15, an interval of 100 is not appropriate. Using an interval of 1 would not be appropriate if the maximum frequency was 500, as this would make a graph very large and hard to read.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b038",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Worked example 17.10: Reading information from bar graphs"
    },
    "content_text": "",
    "prompt_text": "The school tuckshop staff keeps a record of how many hot dogs, sandwiches, salads and burgers they sell on one day. They draw a bar graph to represent the data.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-g10-math-lit-12-gd-0032.png\n\nDraw up a frequency table and complete it by reading the information off the bar graph.",
    "answer_text": "Step 1: The categories are the types of food sold. Put the categories you see on the bar graph into the first column of the frequency table.\n\n| Categories | Frequency |\n| --- | --- |\n| Hot dogs |  |\n| Sandwiches |  |\n| Salads |  |\n| Burgers |  |\n\nStep 2: Read the frequencies off the graph, and write them next to the correct category in the table.\n\n| Categories | Frequency |\n| --- | --- |\n| Hot dogs | 15 |\n| Sandwiches | 35 |\n| Salads | 10 |\n| Burgers | 12 |",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b039",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Exercise 17.8: Read information off bar graphs"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.8: Read information off bar graphs",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b039-i01a",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Exercise 17.8: Read information off bar graphs"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.8: Read information off bar graphs\n\n1a. School A started a recycling project. The bar chart below shows the number of kilograms of each category School A recycled last week.\n\nSchool A's recycling\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_007.png\n\nOf which item did the school collect the most, in kilograms?",
    "answer_text": "Find the category for which the school collected the most by finding the highest bar on the bar graph.\n\nFrom the graph, we can see that more kilograms of plastic were collected than any other category. This is represented by the highest bar, which is 14 kg.\n\nAnswer: In kilograms, the item collected the most was plastic.",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b039-i01b",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Exercise 17.8: Read information off bar graphs"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.8: Read information off bar graphs\n\n1b. School A started a recycling project. The bar chart below shows the number of kilograms of each category School A recycled last week.\n\nSchool A's recycling\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_007.png\n\nFor which item did the school collect 7 kg?",
    "answer_text": "To find the answer to the second question, you need to focus on the vertical axis, which shows the frequency of items in kilograms.\n\nThis means that you need to find 7 on the vertical axis.\n\nFollow a horizontal line across (you can use a ruler) until you reach the bar that corresponds with that value, which is textiles.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-1_023.png\n\nAnswer: The school collected 7 kg of textiles.",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b039-i01c",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Exercise 17.8: Read information off bar graphs"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.8: Read information off bar graphs\n\n1c. School A started a recycling project. The bar chart below shows the number of kilograms of each category School A recycled last week.\n\nSchool A's recycling\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_007.png\n\nOf which item did the school collect the least, in kilograms?",
    "answer_text": "Find the category with the shortest bar.\n\nWe see that the shortest bar has a measurement of 2 kg, and it is for the category of paper.\n\nAnswer: In kilograms, the item collected the least was paper.",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b039-i02a",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Exercise 17.8: Read information off bar graphs"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.8: Read information off bar graphs\n\n2a. School B also started a recycling project. The bar chart below shows the number of kilograms of each category School B recycled last week.\n\nSchool B's recycling\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_020.png\n\nOf which item did the school collect the most, in kilograms?",
    "answer_text": "The tallest bar is 14 kg for electronics.\n\nAnswer: In kilograms, the item collected the most was electronics.",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b039-i02b",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Exercise 17.8: Read information off bar graphs"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.8: Read information off bar graphs\n\n2b. School B also started a recycling project. The bar chart below shows the number of kilograms of each category School B recycled last week.\n\nSchool B's recycling\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_020.png\n\nFor which item did the school collect 13 kg?",
    "answer_text": "The bar that corresponds with 13 kg is garden waste.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-1_015.png\n\nAnswer: The school collected 13 kg of garden waste.",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b039-i02c",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Exercise 17.8: Read information off bar graphs"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.8: Read information off bar graphs\n\n2c. School B also started a recycling project. The bar chart below shows the number of kilograms of each category School B recycled last week.\n\nSchool B's recycling\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_020.png\n\nOf which item did the school collect the least, in kilograms?",
    "answer_text": "The shortest bar has a measurement of 3 kg, and corresponds with plastic.\n\nAnswer: In kilograms, the item collected the least was plastic.",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b039-i03a",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Exercise 17.8: Read information off bar graphs"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.8: Read information off bar graphs\n\n3a. School C also started a recycling project. The bar chart below shows the number of kilograms of each item School C recycled last week.\n\nSchool C's recycling\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_018.png\n\nOf which item did the school collect the most, in kilograms?",
    "answer_text": "The tallest bar is 15 kg for electronics.\n\nAnswer: In kilograms, the item collected the most was electronics.",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b039-i03b",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Exercise 17.8: Read information off bar graphs"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.8: Read information off bar graphs\n\n3b. School C also started a recycling project. The bar chart below shows the number of kilograms of each item School C recycled last week.\n\nSchool C's recycling\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_018.png\n\nWhich item did the school collect 1 kg of?",
    "answer_text": "Find the value of 1 on the vertical axis, and the bar that corresponds with that value.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-1_021.png\n\nThe school collected 1 kg of textiles.",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b039-i03c",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Exercise 17.8: Read information off bar graphs"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.8: Read information off bar graphs\n\n3c. School C also started a recycling project. The bar chart below shows the number of kilograms of each item School C recycled last week.\n\nSchool C's recycling\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_018.png\n\nOf which item did the school collect the least, in kilograms?",
    "answer_text": "In kilograms, the item collected the least was textiles.",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
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
  "subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data",
  "subtopic_title": "Graphical presentation of data",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-data-presentation-graphical-presentation-of-data-po01",
        "source_performance_objective_index": 1,
        "text": "Present data using bar charts, pie charts and histograms"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "graphical-presentation-of-data-ao-present-using-bar-charts",
          "text": "Present data using bar charts."
        },
        {
          "atomic_objective_id": "graphical-presentation-of-data-ao-present-using-pie-charts",
          "text": "Present data using pie charts."
        },
        {
          "atomic_objective_id": "graphical-presentation-of-data-ao-present-using-histograms",
          "text": "Present data using histograms."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-data-presentation-graphical-presentation-of-data-po02",
        "source_performance_objective_index": 2,
        "text": "Read and interpret information from bar charts, pie charts and histograms"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "graphical-presentation-of-data-ao-read-bar-charts",
          "text": "Read information from bar charts."
        },
        {
          "atomic_objective_id": "graphical-presentation-of-data-ao-interpret-bar-charts",
          "text": "Interpret information from bar charts."
        },
        {
          "atomic_objective_id": "graphical-presentation-of-data-ao-read-pie-charts",
          "text": "Read information from pie charts."
        },
        {
          "atomic_objective_id": "graphical-presentation-of-data-ao-interpret-pie-charts",
          "text": "Interpret information from pie charts."
        },
        {
          "atomic_objective_id": "graphical-presentation-of-data-ao-read-histograms",
          "text": "Read information from histograms."
        },
        {
          "atomic_objective_id": "graphical-presentation-of-data-ao-interpret-histograms",
          "text": "Interpret information from histograms."
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
    "record_id": "ch17-b034",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": null
    },
    "content_text": "So far we have collected the data, then organised the data, and summarised the data. Now we need to find ways to present the data, so that we can share the results of our research with other people.\n\nThere are many ways of presenting data to show results, including written reports, tables and graphs. Graphs are useful as they give a picture of the results that is easy to understand. We will use bar graphs.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b035",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": null
    },
    "content_text": "presenting data Presenting data is finding a way to show results so they can be shared with other people.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b036",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Using bar graphs to present data"
    },
    "content_text": "Bar graphs are used to display data that has been collected and organised in categories. An example of categories is the cars of different colours that we looked at earlier in this chapter.\n\nA bar graph is a chart that uses either horizontal or vertical bars to show how categories compare with each other. The length of each bar shows the value that the bar represents.\n\nFor example, every month for five months, the manager of a new shop keeps count of how many customers visit the shop. The manager created this bar graph to show the results.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-g10-math-lit-12-gd-0030.png\n\n- The categories (the months) are shown along the horizontal axis.\n- The frequency (the number of customers) is shown along the vertical axis.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b037",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Using bar graphs to present data"
    },
    "content_text": "It is important to use an appropriate interval on the graph to show the frequency.\n\nThis bar graph uses an interval of 100 along the vertical axis. If the largest frequency was only 15, an interval of 100 is not appropriate. Using an interval of 1 would not be appropriate if the maximum frequency was 500, as this would make a graph very large and hard to read.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b038",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Worked example 17.10: Reading information from bar graphs"
    },
    "content_text": "",
    "prompt_text": "The school tuckshop staff keeps a record of how many hot dogs, sandwiches, salads and burgers they sell on one day. They draw a bar graph to represent the data.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-g10-math-lit-12-gd-0032.png\n\nDraw up a frequency table and complete it by reading the information off the bar graph.",
    "answer_text": "Step 1: The categories are the types of food sold. Put the categories you see on the bar graph into the first column of the frequency table.\n\n| Categories | Frequency |\n| --- | --- |\n| Hot dogs |  |\n| Sandwiches |  |\n| Salads |  |\n| Burgers |  |\n\nStep 2: Read the frequencies off the graph, and write them next to the correct category in the table.\n\n| Categories | Frequency |\n| --- | --- |\n| Hot dogs | 15 |\n| Sandwiches | 35 |\n| Salads | 10 |\n| Burgers | 12 |",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b039",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Exercise 17.8: Read information off bar graphs"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.8: Read information off bar graphs",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b039-i01a",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Exercise 17.8: Read information off bar graphs"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.8: Read information off bar graphs\n\n1a. School A started a recycling project. The bar chart below shows the number of kilograms of each category School A recycled last week.\n\nSchool A's recycling\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_007.png\n\nOf which item did the school collect the most, in kilograms?",
    "answer_text": "Find the category for which the school collected the most by finding the highest bar on the bar graph.\n\nFrom the graph, we can see that more kilograms of plastic were collected than any other category. This is represented by the highest bar, which is 14 kg.\n\nAnswer: In kilograms, the item collected the most was plastic.",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b039-i01b",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Exercise 17.8: Read information off bar graphs"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.8: Read information off bar graphs\n\n1b. School A started a recycling project. The bar chart below shows the number of kilograms of each category School A recycled last week.\n\nSchool A's recycling\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_007.png\n\nFor which item did the school collect 7 kg?",
    "answer_text": "To find the answer to the second question, you need to focus on the vertical axis, which shows the frequency of items in kilograms.\n\nThis means that you need to find 7 on the vertical axis.\n\nFollow a horizontal line across (you can use a ruler) until you reach the bar that corresponds with that value, which is textiles.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-1_023.png\n\nAnswer: The school collected 7 kg of textiles.",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b039-i01c",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Exercise 17.8: Read information off bar graphs"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.8: Read information off bar graphs\n\n1c. School A started a recycling project. The bar chart below shows the number of kilograms of each category School A recycled last week.\n\nSchool A's recycling\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_007.png\n\nOf which item did the school collect the least, in kilograms?",
    "answer_text": "Find the category with the shortest bar.\n\nWe see that the shortest bar has a measurement of 2 kg, and it is for the category of paper.\n\nAnswer: In kilograms, the item collected the least was paper.",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b039-i02a",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Exercise 17.8: Read information off bar graphs"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.8: Read information off bar graphs\n\n2a. School B also started a recycling project. The bar chart below shows the number of kilograms of each category School B recycled last week.\n\nSchool B's recycling\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_020.png\n\nOf which item did the school collect the most, in kilograms?",
    "answer_text": "The tallest bar is 14 kg for electronics.\n\nAnswer: In kilograms, the item collected the most was electronics.",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b039-i02b",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Exercise 17.8: Read information off bar graphs"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.8: Read information off bar graphs\n\n2b. School B also started a recycling project. The bar chart below shows the number of kilograms of each category School B recycled last week.\n\nSchool B's recycling\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_020.png\n\nFor which item did the school collect 13 kg?",
    "answer_text": "The bar that corresponds with 13 kg is garden waste.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-1_015.png\n\nAnswer: The school collected 13 kg of garden waste.",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b039-i02c",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Exercise 17.8: Read information off bar graphs"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.8: Read information off bar graphs\n\n2c. School B also started a recycling project. The bar chart below shows the number of kilograms of each category School B recycled last week.\n\nSchool B's recycling\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_020.png\n\nOf which item did the school collect the least, in kilograms?",
    "answer_text": "The shortest bar has a measurement of 3 kg, and corresponds with plastic.\n\nAnswer: In kilograms, the item collected the least was plastic.",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b039-i03a",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Exercise 17.8: Read information off bar graphs"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.8: Read information off bar graphs\n\n3a. School C also started a recycling project. The bar chart below shows the number of kilograms of each item School C recycled last week.\n\nSchool C's recycling\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_018.png\n\nOf which item did the school collect the most, in kilograms?",
    "answer_text": "The tallest bar is 15 kg for electronics.\n\nAnswer: In kilograms, the item collected the most was electronics.",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b039-i03b",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Exercise 17.8: Read information off bar graphs"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.8: Read information off bar graphs\n\n3b. School C also started a recycling project. The bar chart below shows the number of kilograms of each item School C recycled last week.\n\nSchool C's recycling\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_018.png\n\nWhich item did the school collect 1 kg of?",
    "answer_text": "Find the value of 1 on the vertical axis, and the bar that corresponds with that value.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-1_021.png\n\nThe school collected 1 kg of textiles.",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
  },
  {
    "record_id": "ch17-b039-i03c",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.3 Presenting data",
      "h3": "Exercise 17.8: Read information off bar graphs"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.8: Read information off bar graphs\n\n3c. School C also started a recycling project. The bar chart below shows the number of kilograms of each item School C recycled last week.\n\nSchool C's recycling\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_018.png\n\nOf which item did the school collect the least, in kilograms?",
    "answer_text": "In kilograms, the item collected the least was textiles.",
    "primary_subtopic_id": "jss1-math-data-presentation-graphical-presentation-of-data"
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
