# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-5",
  "topic_key": "jss1-math-data-collection",
  "topic": "Data Collection",
  "subtopic_id": "jss1-math-data-collection-collect-data-in-the-class",
  "subtopic_title": "Collect data in the class",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-data-collection-collect-data-in-the-class-po01",
        "source_performance_objective_index": 1,
        "text": "Collect data in the class"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "collect-data-in-the-class-ao-collect-data",
          "text": "Collect data in the class."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch17-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": null
    },
    "content_text": "You have learnt that statistics is useful as it allows us to interpret what has happened in the past, so that we can predict what is likely to happen in the future, and plan for it. A vital part of working with statistics is gathering the information, recording it, and then presenting it so that it can be understood easily and used by other people. This is called **data handling**.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b002",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": null
    },
    "content_text": "**data handling** Data handling is gathering and recording information, and then presenting it in a way that can be understood easily and used by other people.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b003",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "The data handling cycle"
    },
    "content_text": "The process of data handling is summarised in the diagram below.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-g10-math-lit-12-gd-0001.png)\n\nWe show the process of data handling as a cycle, because once we have summarised, represented and analysed the results, we may have new questions that we need to research. Then we will need to start the cycle again.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b004",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Different ways of collecting data"
    },
    "content_text": "The first step in any statistical process is **data collection**, which is gathering the facts and figures (the data).\n\nWhat we are researching affects the way we collect the data. Four methods of collecting data are shown in the diagram.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-g10-math-lit-12-gd-0003.png)\n\n1. **Observation and measurement**: Collecting data using observation or measurement involves looking at something that actually happens, and then measuring and recording it. An example of observation is counting the number of cars passing the gate of your school every hour. An example of measurement is measuring the masses of all the students in your class.\n2. **Interview**: An interview usually takes place between two people. One of the people is called *the interviewer* and the other is *the interviewee* or *respondent*. We use interviews when we can talk to the respondents directly. For example, we could interview people leaving a shop to find out whether they were happy with the way they were treated by the people working in the shop. Job and parent-teacher interviews are examples interviews that are also for collecting data, but this data is used in a way that is different from statistical use.\n3. **Questionnaire**: A questionnaire is a set of questions given to many people to complete. A questionnaire is useful for getting information from many people, as it can be handed out and then collected later, and does not need an interviewer. It is the best method of collecting data when you want to ask a large group of people what they think about a specific issue. A questionnaire should have a short explanation of what your research is about. A very special kind of questionnaire is used for a national population census, which last took place in 2012 in Nigeria.\n4. **Database**: A database is an organised collection of data that someone else has already organised and presented. Databases can be stored on a computer or on the internet, or presented in publications such as books, newspapers and magazines.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b005",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Different ways of collecting data"
    },
    "content_text": "**data collection** Data collection is gathering the facts and figures needed for the research.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b006",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Worked example 17.1: Choosing the best way to collect data"
    },
    "content_text": "",
    "prompt_text": "Amaka wants to answer the following question: Is my baby crying too much? Consider which of the following would be the best method for her to use.\n\n- Should Amaka interview people one-on-one to find out the answer to her question?\n- Should Amaka use a questionnaire to give to groups of people to find the answer to her question?\n- Should Amaka observe her baby to find the answer to her question?",
    "answer_text": "Step 1: Decide whether Amaka should interview people one-on-one to find out the answer to her question.\n\nAn interview is a formal or informal conversation with another person. Another person might have an opinion, but will not be able to give a definite answer.\n\nAnswer: Interviews would not be the best method.\n\nStep 2: Decide whether Amaka should give a questionnaire to a group of people to find the answer to her question.\n\nA questionnaire has a set of clear questions, usually with a choice of answers, that is given to many people. A group of people outside the home would not be able to answer Amaka's question.\n\nAnswer: A questionnaire would not be the best method.\n\nStep 3: Decide whether Amaka should observe her baby to find the answer to her question.\n\nObservation is the best method of collecting data when you need information about the behaviour of people.\n\nAnswer: The question about Amaka's baby is better answered by watching its behaviour. So she should observe her baby and then make an informed judgement about whether it is crying too much.",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b007",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Exercise 17.1: Choose the best way to collect data"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.1: Choose the best way to collect data",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b007-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Exercise 17.1: Choose the best way to collect data"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.1: Choose the best way to collect data\n\n1. Babangida wants to find out her classmates' favourite television programme.\n\nWhat one of the following should Babangida do?\n\n- Look up the answer in the newspaper.\n- Observe everyone in her class when they are watching television.\n- Draw up a questionnaire asking which of the given ten television programmes was their favourite and hand it out to her classmates to complete.",
    "answer_text": "Babangida won't find out about the favourite television programme of her classmates in a newspaper.\n\nObserving all her classmates when they watch television will be too time consuming, and won't necessarily tell her which programme is their favourite.\n\nAnswer: Babangida should draw up a questionnaire and then give it to her classmates to complete.",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b007-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Exercise 17.1: Choose the best way to collect data"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.1: Choose the best way to collect data\n\n2. Adanna wants to know how the price of cooking oil has increased over the last ten years.\n\nWhich one of the following should Adanna do?\n\n- Go to the Nigerian National Bureau of Statistics website and use the database that they have there which gives the price of cooking oil over the last ten years.\n- Interview everyone entering a supermarket one Saturday morning and asking them what they remember about the cost of cooking oil over the last ten years.\n- Draw up a questionnaire to hand out to all the students in her school asking them to ask their parents what they remember about the cost of cooking oil over the last ten years.",
    "answer_text": "Answer: Adanna should go to the Nigerian National Bureau of Statistics website to find the information that she wants.\n\nPeople won't remember facts like the price of cooking oil ten years ago, so interviewing everyone entering the supermarket won't give Adanna the information she wants, nor will giving students at school a questionnaire.",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b008",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Organising data"
    },
    "content_text": "After data has been collected, the next step is **organising the data**, by bringing it together in a systematic way that makes it easier to read. We can organise data by using tallies and frequency tables.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b009",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Organising data"
    },
    "content_text": "**organising data** Organising data is bringing it together in a systematic way that makes it easier to read.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b010",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Tallies"
    },
    "content_text": "Tallies are a way of counting by drawing a short vertical line to record each item as you count it. To make reading the tally marks easier, for every fifth mark, you draw a diagonal line through the first four lines. Then leave a space before starting on the next group of four tally marks.\n\nThe table below shows the tally marks for a few numbers:\n\n| Number | Tally image |\n| --- | --- |\n| 3 | Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-1_020.png |\n| 4 | Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-2.png |\n| 5 | Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-3_004.png |\n| 8 | Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-4_003.png |\n| 10 | Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_016.png |\n| 12 | Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_028.png |\n\nThe advantage of using tallies is that you can keep a running total while you are counting, and tally tables are easy to read because you can count in fives.\n\nHere is an example of a tally table showing the numbers of cars of different colours that have been counted. Each car that is counted is shown by one tally mark.\n\n| Car colour | Tally image |\n| --- | --- |\n| Red | Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-17-002.png |\n| Green | Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-1_020.png |\n| Blue | Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-2.png |\n| Yellow | Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-17-001.png |\n\nFrom these tallies, we can see that 7 red cars, 3 green cars, 4 blue cars and 2 yellow cars were counted.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b011",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Frequency tables"
    },
    "content_text": "When we have finished counting, and add up all the tally marks, the totals tell us how many times the event occurred, which is called the **frequency**. So the frequency of red cars was 7, of green cars was 3, of blue cars was 4, and of yellow cars was 2.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b012",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Frequency tables"
    },
    "content_text": "**frequency** The frequency is how many times the event occurred.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b013",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Frequency tables"
    },
    "content_text": "A frequency table shows the list of different categories, together with the number of times each item occurs. This frequency table shows the number of differently coloured cars.\n\n| Car colours | Frequency |\n| --- | ---: |\n| Red | 7 |\n| Green | 3 |\n| Blue | 4 |\n| Yellow | 2 |\n\n- In the first column of a frequency table we list the categories. In this example the categories are the car colours: red, green, blue and yellow.\n- In the second column we record the frequency, which is the number of times each category occurs. The frequency is the same as the number of marks in the tally table.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b014",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Worked example 17.2: Counting tally marks"
    },
    "content_text": "",
    "prompt_text": "Amina counted the number of students who belonged to the chess club, and used tally marks to show this data.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_017.png\n\nHow many students belong to the chess club?",
    "answer_text": "Step 1: Count up the tally marks.\n\nThere are 4 $\\times$ 5 = 20 tally marks.\n\nStep 2: Write your answer in a full sentence.\n\nAnswer: 20 students belong to the chess club.",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b015",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Exercise 17.2: Count tally marks"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.2: Count tally marks",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b015-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Exercise 17.2: Count tally marks"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.2: Count tally marks\n\n1. Oladapo counted the number of students who have pets at home, and used tally marks to show this data.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_014.png\n\nHow many students have pets at home?",
    "answer_text": "Count up the tally marks.\n\nThe number of students who have pets at home = ($\\text{2}\\times {5}$) + $\\text{3}$ = $\\text{13}$.\n\nAnswer: 13 students have pets at home.",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b015-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Exercise 17.2: Count tally marks"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.2: Count tally marks\n\n2. Adebisi counted the number of girls playing tennis, and used tally marks to show this data.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_016.png\n\nHow many girls are playing tennis?",
    "answer_text": "10 girls are playing tennis.",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b016",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Worked example 17.3: Drawing up a frequency table"
    },
    "content_text": "The frequency is the number of times each number was thrown.",
    "prompt_text": "15 students each had one chance to throw a die, and they recorded the number the die landed on each time.\n\nThe list of numbers is $\\text{5 ; 1 ; 5 ; 1 ; 1 ; 2 ; 3 ; 5 ; 6 ; 4 ; 2 ; 4 ; 2 ; 5 ; 5}$.\n\nWork out how many of each number was thrown, and create a frequency table to show your results.",
    "answer_text": "Step 1: Arrange the numbers in ascending order to help you count. Cross out each number once you have counted it.\n\n$$\n\\text{1 ; 1 ; 1 ; 2 ; 2 ; 2 ; 3 ; 4 ; 4 ; 5 ; 5 ; 5 ; 5 ; 5 ; 6}\n$$\n\nStep 2: Count the number of times each number was thrown, and write the total for each number in a frequency table.\n\n| Score | Frequency |\n| --- | ---: |\n| 1 | 3 |\n| 2 | 3 |\n| 3 | 1 |\n| 4 | 2 |\n| 5 | 5 |\n| 6 | 1 |",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b017",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Exercise 17.3: Draw up frequency tables"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.3: Draw up frequency tables",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b017-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Exercise 17.3: Draw up frequency tables"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.3: Draw up frequency tables\n\n1. 15 students each had one chance to throw a die. The number the die landed on was recorded.\n\nThe numbers were $\\text{5 ; 1 ; 3 ; 3 ; 4 ; 5 ; 3 ; 1 ; 1 ; 3 ; 6 ; 3 ; 3 ; 6 ; 4}$.\n\nWork out how many of each number was thrown, and create a frequency table to show your results.",
    "answer_text": "Arrange your data in order to help you count. Cross out each number once you have counted it.\n\n$$\n\\text{1 ; 1 ; 1 ; 3 ; 3 ; 3 ; 3 ; 3 ; 3 ; 4 ; 4 ; 5 ; 5 ; 6 ; 6}\n$$\n\n| Score | Frequency |\n| --- | ---: |\n| 1 | 3 |\n| 2 | 0 |\n| 3 | 6 |\n| 4 | 2 |\n| 5 | 2 |\n| 6 | 2 |",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b017-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Exercise 17.3: Draw up frequency tables"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.3: Draw up frequency tables\n\n2. The marks out of 10 for a maths quiz are listed below. There were 20 students who took part in the quiz.\n\nThe marks were $\\text{5 ; 7 ; 5 ; 7 ; 6 ; 7 ; 7 ; 5 ; 8 ; 8 ; 5 ; 5 ; 8 ; 10 ; 6 ; 5 ; 5 ; 10 ; 7 ; 6}$.\n\nWork out how many students got each mark, and use the frequency table given below to show your results.\n\n| Score | Frequency |\n| --- | ---: |\n| 5 |  |\n| 6 |  |\n| 7 |  |\n| 8 |  |\n| 9 |  |\n| 10 |  |",
    "answer_text": "Arrange your data in order. Cross out a number once you have counted it.\n\n$$\n\\text{5 ; 5 ; 5 ; 5 ; 5 ; 5 ; 5 ; 6 ; 6 ; 6 ; 7 ; 7 ; 7 ; 7 ; 7 ; 8 ; 8 ; 8 ; 10; 10}\n$$\n\nCount the number of times each mark appears and write the totals in the frequency column.\n\n| Score | Frequency |\n| --- | ---: |\n| 5 | 7 |\n| 6 | 3 |\n| 7 | 5 |\n| 8 | 3 |\n| 9 | 0 |\n| 10 | 2 |",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
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
  "topic_key": "jss1-math-data-collection",
  "topic": "Data Collection",
  "subtopic_id": "jss1-math-data-collection-collect-data-in-the-class",
  "subtopic_title": "Collect data in the class",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-data-collection-collect-data-in-the-class-po01",
        "source_performance_objective_index": 1,
        "text": "Collect data in the class"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "collect-data-in-the-class-ao-collect-data",
          "text": "Collect data in the class."
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
    "record_id": "ch17-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": null
    },
    "content_text": "You have learnt that statistics is useful as it allows us to interpret what has happened in the past, so that we can predict what is likely to happen in the future, and plan for it. A vital part of working with statistics is gathering the information, recording it, and then presenting it so that it can be understood easily and used by other people. This is called **data handling**.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b002",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": null
    },
    "content_text": "**data handling** Data handling is gathering and recording information, and then presenting it in a way that can be understood easily and used by other people.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b003",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "The data handling cycle"
    },
    "content_text": "The process of data handling is summarised in the diagram below.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-g10-math-lit-12-gd-0001.png)\n\nWe show the process of data handling as a cycle, because once we have summarised, represented and analysed the results, we may have new questions that we need to research. Then we will need to start the cycle again.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b004",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Different ways of collecting data"
    },
    "content_text": "The first step in any statistical process is **data collection**, which is gathering the facts and figures (the data).\n\nWhat we are researching affects the way we collect the data. Four methods of collecting data are shown in the diagram.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-g10-math-lit-12-gd-0003.png)\n\n1. **Observation and measurement**: Collecting data using observation or measurement involves looking at something that actually happens, and then measuring and recording it. An example of observation is counting the number of cars passing the gate of your school every hour. An example of measurement is measuring the masses of all the students in your class.\n2. **Interview**: An interview usually takes place between two people. One of the people is called *the interviewer* and the other is *the interviewee* or *respondent*. We use interviews when we can talk to the respondents directly. For example, we could interview people leaving a shop to find out whether they were happy with the way they were treated by the people working in the shop. Job and parent-teacher interviews are examples interviews that are also for collecting data, but this data is used in a way that is different from statistical use.\n3. **Questionnaire**: A questionnaire is a set of questions given to many people to complete. A questionnaire is useful for getting information from many people, as it can be handed out and then collected later, and does not need an interviewer. It is the best method of collecting data when you want to ask a large group of people what they think about a specific issue. A questionnaire should have a short explanation of what your research is about. A very special kind of questionnaire is used for a national population census, which last took place in 2012 in Nigeria.\n4. **Database**: A database is an organised collection of data that someone else has already organised and presented. Databases can be stored on a computer or on the internet, or presented in publications such as books, newspapers and magazines.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b005",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Different ways of collecting data"
    },
    "content_text": "**data collection** Data collection is gathering the facts and figures needed for the research.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b006",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Worked example 17.1: Choosing the best way to collect data"
    },
    "content_text": "",
    "prompt_text": "Amaka wants to answer the following question: Is my baby crying too much? Consider which of the following would be the best method for her to use.\n\n- Should Amaka interview people one-on-one to find out the answer to her question?\n- Should Amaka use a questionnaire to give to groups of people to find the answer to her question?\n- Should Amaka observe her baby to find the answer to her question?",
    "answer_text": "Step 1: Decide whether Amaka should interview people one-on-one to find out the answer to her question.\n\nAn interview is a formal or informal conversation with another person. Another person might have an opinion, but will not be able to give a definite answer.\n\nAnswer: Interviews would not be the best method.\n\nStep 2: Decide whether Amaka should give a questionnaire to a group of people to find the answer to her question.\n\nA questionnaire has a set of clear questions, usually with a choice of answers, that is given to many people. A group of people outside the home would not be able to answer Amaka's question.\n\nAnswer: A questionnaire would not be the best method.\n\nStep 3: Decide whether Amaka should observe her baby to find the answer to her question.\n\nObservation is the best method of collecting data when you need information about the behaviour of people.\n\nAnswer: The question about Amaka's baby is better answered by watching its behaviour. So she should observe her baby and then make an informed judgement about whether it is crying too much.",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b007",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Exercise 17.1: Choose the best way to collect data"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.1: Choose the best way to collect data",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b007-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Exercise 17.1: Choose the best way to collect data"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.1: Choose the best way to collect data\n\n1. Babangida wants to find out her classmates' favourite television programme.\n\nWhat one of the following should Babangida do?\n\n- Look up the answer in the newspaper.\n- Observe everyone in her class when they are watching television.\n- Draw up a questionnaire asking which of the given ten television programmes was their favourite and hand it out to her classmates to complete.",
    "answer_text": "Babangida won't find out about the favourite television programme of her classmates in a newspaper.\n\nObserving all her classmates when they watch television will be too time consuming, and won't necessarily tell her which programme is their favourite.\n\nAnswer: Babangida should draw up a questionnaire and then give it to her classmates to complete.",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b007-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Exercise 17.1: Choose the best way to collect data"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.1: Choose the best way to collect data\n\n2. Adanna wants to know how the price of cooking oil has increased over the last ten years.\n\nWhich one of the following should Adanna do?\n\n- Go to the Nigerian National Bureau of Statistics website and use the database that they have there which gives the price of cooking oil over the last ten years.\n- Interview everyone entering a supermarket one Saturday morning and asking them what they remember about the cost of cooking oil over the last ten years.\n- Draw up a questionnaire to hand out to all the students in her school asking them to ask their parents what they remember about the cost of cooking oil over the last ten years.",
    "answer_text": "Answer: Adanna should go to the Nigerian National Bureau of Statistics website to find the information that she wants.\n\nPeople won't remember facts like the price of cooking oil ten years ago, so interviewing everyone entering the supermarket won't give Adanna the information she wants, nor will giving students at school a questionnaire.",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b008",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Organising data"
    },
    "content_text": "After data has been collected, the next step is **organising the data**, by bringing it together in a systematic way that makes it easier to read. We can organise data by using tallies and frequency tables.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b009",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Organising data"
    },
    "content_text": "**organising data** Organising data is bringing it together in a systematic way that makes it easier to read.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b010",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Tallies"
    },
    "content_text": "Tallies are a way of counting by drawing a short vertical line to record each item as you count it. To make reading the tally marks easier, for every fifth mark, you draw a diagonal line through the first four lines. Then leave a space before starting on the next group of four tally marks.\n\nThe table below shows the tally marks for a few numbers:\n\n| Number | Tally image |\n| --- | --- |\n| 3 | Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-1_020.png |\n| 4 | Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-2.png |\n| 5 | Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-3_004.png |\n| 8 | Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-4_003.png |\n| 10 | Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_016.png |\n| 12 | Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_028.png |\n\nThe advantage of using tallies is that you can keep a running total while you are counting, and tally tables are easy to read because you can count in fives.\n\nHere is an example of a tally table showing the numbers of cars of different colours that have been counted. Each car that is counted is shown by one tally mark.\n\n| Car colour | Tally image |\n| --- | --- |\n| Red | Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-17-002.png |\n| Green | Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-1_020.png |\n| Blue | Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-2.png |\n| Yellow | Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-17-001.png |\n\nFrom these tallies, we can see that 7 red cars, 3 green cars, 4 blue cars and 2 yellow cars were counted.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b011",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Frequency tables"
    },
    "content_text": "When we have finished counting, and add up all the tally marks, the totals tell us how many times the event occurred, which is called the **frequency**. So the frequency of red cars was 7, of green cars was 3, of blue cars was 4, and of yellow cars was 2.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b012",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Frequency tables"
    },
    "content_text": "**frequency** The frequency is how many times the event occurred.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b013",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Frequency tables"
    },
    "content_text": "A frequency table shows the list of different categories, together with the number of times each item occurs. This frequency table shows the number of differently coloured cars.\n\n| Car colours | Frequency |\n| --- | ---: |\n| Red | 7 |\n| Green | 3 |\n| Blue | 4 |\n| Yellow | 2 |\n\n- In the first column of a frequency table we list the categories. In this example the categories are the car colours: red, green, blue and yellow.\n- In the second column we record the frequency, which is the number of times each category occurs. The frequency is the same as the number of marks in the tally table.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b014",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Worked example 17.2: Counting tally marks"
    },
    "content_text": "",
    "prompt_text": "Amina counted the number of students who belonged to the chess club, and used tally marks to show this data.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_017.png\n\nHow many students belong to the chess club?",
    "answer_text": "Step 1: Count up the tally marks.\n\nThere are 4 $\\times$ 5 = 20 tally marks.\n\nStep 2: Write your answer in a full sentence.\n\nAnswer: 20 students belong to the chess club.",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b015",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Exercise 17.2: Count tally marks"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.2: Count tally marks",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b015-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Exercise 17.2: Count tally marks"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.2: Count tally marks\n\n1. Oladapo counted the number of students who have pets at home, and used tally marks to show this data.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_014.png\n\nHow many students have pets at home?",
    "answer_text": "Count up the tally marks.\n\nThe number of students who have pets at home = ($\\text{2}\\times {5}$) + $\\text{3}$ = $\\text{13}$.\n\nAnswer: 13 students have pets at home.",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b015-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Exercise 17.2: Count tally marks"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.2: Count tally marks\n\n2. Adebisi counted the number of girls playing tennis, and used tally marks to show this data.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-17-0_016.png\n\nHow many girls are playing tennis?",
    "answer_text": "10 girls are playing tennis.",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b016",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Worked example 17.3: Drawing up a frequency table"
    },
    "content_text": "The frequency is the number of times each number was thrown.",
    "prompt_text": "15 students each had one chance to throw a die, and they recorded the number the die landed on each time.\n\nThe list of numbers is $\\text{5 ; 1 ; 5 ; 1 ; 1 ; 2 ; 3 ; 5 ; 6 ; 4 ; 2 ; 4 ; 2 ; 5 ; 5}$.\n\nWork out how many of each number was thrown, and create a frequency table to show your results.",
    "answer_text": "Step 1: Arrange the numbers in ascending order to help you count. Cross out each number once you have counted it.\n\n$$\n\\text{1 ; 1 ; 1 ; 2 ; 2 ; 2 ; 3 ; 4 ; 4 ; 5 ; 5 ; 5 ; 5 ; 5 ; 6}\n$$\n\nStep 2: Count the number of times each number was thrown, and write the total for each number in a frequency table.\n\n| Score | Frequency |\n| --- | ---: |\n| 1 | 3 |\n| 2 | 3 |\n| 3 | 1 |\n| 4 | 2 |\n| 5 | 5 |\n| 6 | 1 |",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b017",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Exercise 17.3: Draw up frequency tables"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.3: Draw up frequency tables",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b017-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Exercise 17.3: Draw up frequency tables"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.3: Draw up frequency tables\n\n1. 15 students each had one chance to throw a die. The number the die landed on was recorded.\n\nThe numbers were $\\text{5 ; 1 ; 3 ; 3 ; 4 ; 5 ; 3 ; 1 ; 1 ; 3 ; 6 ; 3 ; 3 ; 6 ; 4}$.\n\nWork out how many of each number was thrown, and create a frequency table to show your results.",
    "answer_text": "Arrange your data in order to help you count. Cross out each number once you have counted it.\n\n$$\n\\text{1 ; 1 ; 1 ; 3 ; 3 ; 3 ; 3 ; 3 ; 3 ; 4 ; 4 ; 5 ; 5 ; 6 ; 6}\n$$\n\n| Score | Frequency |\n| --- | ---: |\n| 1 | 3 |\n| 2 | 0 |\n| 3 | 6 |\n| 4 | 2 |\n| 5 | 2 |\n| 6 | 2 |",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
  },
  {
    "record_id": "ch17-b017-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 17: Data collection and presentation",
      "h2": "17.1 Collecting and organising data",
      "h3": "Exercise 17.3: Draw up frequency tables"
    },
    "content_text": "",
    "prompt_text": "### Exercise 17.3: Draw up frequency tables\n\n2. The marks out of 10 for a maths quiz are listed below. There were 20 students who took part in the quiz.\n\nThe marks were $\\text{5 ; 7 ; 5 ; 7 ; 6 ; 7 ; 7 ; 5 ; 8 ; 8 ; 5 ; 5 ; 8 ; 10 ; 6 ; 5 ; 5 ; 10 ; 7 ; 6}$.\n\nWork out how many students got each mark, and use the frequency table given below to show your results.\n\n| Score | Frequency |\n| --- | ---: |\n| 5 |  |\n| 6 |  |\n| 7 |  |\n| 8 |  |\n| 9 |  |\n| 10 |  |",
    "answer_text": "Arrange your data in order. Cross out a number once you have counted it.\n\n$$\n\\text{5 ; 5 ; 5 ; 5 ; 5 ; 5 ; 5 ; 6 ; 6 ; 6 ; 7 ; 7 ; 7 ; 7 ; 7 ; 8 ; 8 ; 8 ; 10; 10}\n$$\n\nCount the number of times each mark appears and write the totals in the frequency column.\n\n| Score | Frequency |\n| --- | ---: |\n| 5 | 7 |\n| 6 | 3 |\n| 7 | 5 |\n| 8 | 3 |\n| 9 | 0 |\n| 10 | 2 |",
    "primary_subtopic_id": "jss1-math-data-collection-collect-data-in-the-class"
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
