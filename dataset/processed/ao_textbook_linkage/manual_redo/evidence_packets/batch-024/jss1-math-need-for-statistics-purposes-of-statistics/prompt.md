# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-5",
  "topic_key": "jss1-math-need-for-statistics",
  "topic": "Need for Statistics",
  "subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics",
  "subtopic_title": "Purposes of statistics",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-need-for-statistics-purposes-of-statistics-po01",
        "source_performance_objective_index": 1,
        "text": "List purposes of statistics"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "purposes-of-statistics-ao-list-purposes",
          "text": "List purposes of statistics."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch16-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": null
    },
    "content_text": "Statistics keeps us informed about what is happening in the world around us. Some examples of how statistics are useful are listed below.\n\n- Weather information is given in newspapers, on the radio, on television and on the internet. Scientists use statistics to compare previous weather with the current weather, and then predict future weather in a particular area.\n- Statistics play an important part in financial businesses. Traders and people in business use statistics to decide how they should invest and make money.\n- Statistics play an important role in the development of new medicines. New medicines have to be tested and results have to be recorded to see whether the medicines help in the way they are supposed to and whether they have bad side-effects.\n- News reporters make predictions of election winners based on statistics collected about how people are going to vote.\n- Statistical concepts are used in quality testing in factories and manufacturers. Companies test samples of products and use the statistical results to estimate whether all the products are likely to work correctly.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b002",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Statistical data"
    },
    "content_text": "The first step in doing statistical work is to decide what it is you want to find out about. The next thing you do is plan how you are going to gather enough information so you can find out what you want to know. The information used in statistics is called **data**.\n\nOnce your planning is complete, you begin to gather the information, which in statistics is called **collecting data**.\n\nExamples of data that you could collect about yourself, your friends or your family are:\n\n- where different people live\n- what different people eat for breakfast\n- people's favourite fruit\n- people's ages, heights or masses\n- the number of siblings that people have\n- which size shoe people wear\n\nOnce you have collected the data, you can put it in a table so it is easier to read and understand. Having the data organised in a table makes it easier to see what the data tells you and to answer questions about the data. This is called **analysing data**.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b003",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Statistical data"
    },
    "content_text": "If data is collected from a number of people, we say that we have surveyed the people. We \"do a survey\" to collect information from the people, such as where all the students in a school live.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b004",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Statistical data"
    },
    "content_text": "**data** Data is information in the form of facts, such as numbers, measurements or observations.\n\n**collecting data** Collecting data is gathering together and recording the information needed.\n\n**analysing data** Analysing data is making sense of the data to see what it tells you.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b005",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Worked example 16.1: Analysing data given in a table"
    },
    "content_text": "",
    "prompt_text": "A researcher wanted to compare the numbers of female and male teachers at different schools. She did a survey to find out the number of male and female teachers there were in six different schools. She recorded the results in this table.\n\n|  | School A | School B | School C | School D | School E | School F |\n| --- | ---: | ---: | ---: | ---: | ---: | ---: |\n| **Male teachers** | 18 | 8 | 9 | 3 | 9 | 5 |\n| **Female teachers** | 11 | 2 | 10 | 4 | 15 | 6 |\n\nUse the table to answer the following questions.\n\n1. How many teachers were there at School A?\n2. How many teachers were there at School D?\n3. Which school had the most male teachers?\n4. Which school had the most female teachers?\n5. Arrange the schools in order of most teachers to fewest teachers.",
    "answer_text": "Step 1: Find the column headed **School A**. Add together the number of male teachers and the number of female teachers.\n\nNumber of teachers at School A = $\\text{18 + 11 = 29}$\n\nAnswer: 29\n\nStep 2: Find the column headed **School D**. Add together the number of male teachers and the number of female teachers.\n\nNumber of teachers at School D = $\\text{3 + 4 = 7}$\n\nAnswer: 7\n\nStep 3: Look along the row marked **Male teachers** and find the column with the largest number in it.\n\nThere are 18 male teachers at School A, which is more than the number of male teachers at any other school.\n\nAnswer: School A\n\nStep 4: Look along the row marked **Female teachers** and find the column with the largest number in it.\n\nThere are 15 female teachers at School E, which is more than the number of female teachers at any other school.\n\nAnswer: School E\n\nStep 5: Add up the number of male teachers and female teachers at each school. Then arrange the schools in order from most to fewest teachers.\n\nSchool A = $\\text{18 + 11 = 29}$ teachers  \nSchool B = $\\text{8 + 2 = 10}$ teachers  \nSchool C = $\\text{9 + 10 = 19}$ teachers  \nSchool D = $\\text{3 + 4 = 7}$ teachers  \nSchool E = $\\text{9 + 15 = 24}$ teachers  \nSchool F = $\\text{5 + 6 = 11}$ teachers\n\nNumber of teachers from largest to smallest: 29; 24; 19; 11; 10; 7\n\nAnswer: School A; School E; School C; School F; School B; School D",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b006",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.1: Analyse data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.1: Analyse data given in a table",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b006-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.1: Analyse data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.1: Analyse data given in a table\n\nYou surveyed the students in your class at school to find out whether they preferred fruit juice, lemonade, orange fizz or cola.\n\nThe table shows the results of your survey.\n\n| Drink | Students |\n| --- | ---: |\n| fruit juice | 12 |\n| lemonade | 10 |\n| orange fizz | 11 |\n| cola | 7 |\n\n1. How many students took part in the survey?",
    "answer_text": "Number of students who took part in the survey = $\\text{12 + 10 + 11 + 7 = 40}$",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b006-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.1: Analyse data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.1: Analyse data given in a table\n\nYou surveyed the students in your class at school to find out whether they preferred fruit juice, lemonade, orange fizz or cola.\n\nThe table shows the results of your survey.\n\n| Drink | Students |\n| --- | ---: |\n| fruit juice | 12 |\n| lemonade | 10 |\n| orange fizz | 11 |\n| cola | 7 |\n\n2. Which drink was preferred by the largest number of students in your class?",
    "answer_text": "The largest number in the second column = 12\n\nFruit juice was preferred by the largest number of students.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b006-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.1: Analyse data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.1: Analyse data given in a table\n\nYou surveyed the students in your class at school to find out whether they preferred fruit juice, lemonade, orange fizz or cola.\n\nThe table shows the results of your survey.\n\n| Drink | Students |\n| --- | ---: |\n| fruit juice | 12 |\n| lemonade | 10 |\n| orange fizz | 11 |\n| cola | 7 |\n\n3. Which drink was preferred by the smallest number of students in your class?",
    "answer_text": "The smallest number in the second column = 7.\n\nThe smallest number of students preferred cola.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b006-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.1: Analyse data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.1: Analyse data given in a table\n\nYou surveyed the students in your class at school to find out whether they preferred fruit juice, lemonade, orange fizz or cola.\n\nThe table shows the results of your survey.\n\n| Drink | Students |\n| --- | ---: |\n| fruit juice | 12 |\n| lemonade | 10 |\n| orange fizz | 11 |\n| cola | 7 |\n\n4. Arrange the drinks in rank order. Rank order means from the one preferred by the largest number to the one preferred by the smallest number.",
    "answer_text": "Numbers from biggest to smallest: $\\text{12; 11; 10; 7}$.\n\nThe drinks in rank order are fruit juice; orange fizz; lemonade; cola.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b006-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.1: Analyse data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.1: Analyse data given in a table\n\nThe students in your class were surveyed to find out what size shoe they wear.\n\nThe results were organised into the following table.\n\n| Shoe size | Total number |\n| ---: | ---: |\n| 4 | 7 |\n| 5 | 9 |\n| 6 | 5 |\n| 7 | 11 |\n| 8 | 3 |\n| 9 | 1 |\n\n5. Which shoe size is worn by the most students in your class?",
    "answer_text": "The largest number in the second column for total number is 11 students.\n\nA size 7 shoe is worn by the most students.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b006-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.1: Analyse data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.1: Analyse data given in a table\n\nThe students in your class were surveyed to find out what size shoe they wear.\n\nThe results were organised into the following table.\n\n| Shoe size | Total number |\n| ---: | ---: |\n| 4 | 7 |\n| 5 | 9 |\n| 6 | 5 |\n| 7 | 11 |\n| 8 | 3 |\n| 9 | 1 |\n\n6. Which shoe size is worn by the fewest students in your class?",
    "answer_text": "The smallest number in the second column is 1 student.\n\nA size 9 shoe is worn by the fewest students.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b006-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.1: Analyse data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.1: Analyse data given in a table\n\nThe students in your class were surveyed to find out what size shoe they wear.\n\nThe results were organised into the following table.\n\n| Shoe size | Total number |\n| ---: | ---: |\n| 4 | 7 |\n| 5 | 9 |\n| 6 | 5 |\n| 7 | 11 |\n| 8 | 3 |\n| 9 | 1 |\n\n7. How many students took part in the survey?",
    "answer_text": "Number of students that took part in the survey = $\\text{7 + 9 + 5 + 11 + 3 + 1 = 36}$",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b006-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.1: Analyse data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.1: Analyse data given in a table\n\nThe students in your class were surveyed to find out what size shoe they wear.\n\nThe results were organised into the following table.\n\n| Shoe size | Total number |\n| ---: | ---: |\n| 4 | 7 |\n| 5 | 9 |\n| 6 | 5 |\n| 7 | 11 |\n| 8 | 3 |\n| 9 | 1 |\n\n8. Arrange the shoe sizes in rank order (from the shoe size worn by the most students to the shoe size worn by the fewest students).",
    "answer_text": "Number of students wearing each size in rank order: $\\text{11; 9; 7; 5; 3; 1}$.\n\nThe shoe sizes in rank order: size 7; size 5; size 4; size 6; size 8; size 9.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b007",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Sources of statistical information"
    },
    "content_text": "One source of statistical information would be the results of a survey. A second source of statistical information is the newspaper and another source of statistical information is the internet.\n\n- Information about the ages of people in Nigeria can be sourced from the Nigerian National Bureau of Statistics website at https://www.nigerianstat.gov.ng/.\n- Information about the top eight causes of death in Nigeria can be sourced from the Nigerian Centre for Disease Control and Prevention website at https://www.ncdc.gov.ng/.\n- Information about voter education and who is allowed to vote in the next elections can be sourced from the Independent National Election Commission website at https://www.inecnigeria.org/voter-education/.\n- Information about customer rights in a bank can be sourced from the Central Bank of Nigeria website at https://www.cbn.gov.ng/Supervision/cpdconedu.asp.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b008",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Worked example 16.2: Analysing statistical data about age groups"
    },
    "content_text": "",
    "prompt_text": "Erioluwa found the following information about the Nigerian population on the Nigerian National Bureau of Statistics website. The table gives statistics about the percentage of the Nigerian population in the given five age groups in 2012 and 2018.\n\n| Year | 0 to 14 years | 15 to 24 years | 25 to 54 years | 55 to 64 years | 65 years and older |\n| ---: | ---: | ---: | ---: | ---: | ---: |\n| 2012 | 43.8% | 19.3% | 30.1% | 3.8% | 3% |\n| 2018 | 42.5% | 19.8% | 30.4% | 4.0% | 3.3% |\n\nUse the table to answer the following questions.\n\n1. Arrange the age groups in 2012 in ascending order (from smallest to largest).\n2. Arrange the age groups in 2018 in ascending order. Comment on any differences in the rankings.\n3. In 2012 the population of Nigeria was approximately 166.2 million. How many Nigerians fell into the 0 to 14 year age group?\n4. In 2018 the population of Nigeria was approximately 200.96 million. How many Nigerians fell into the 0 to 14 age group? Comment on any differences in the figures.",
    "answer_text": "Step 1: Arrange the 2012 percentages in ascending order and then use the percentages to arrange the age groups in ascending order.\n\nPercentages in ascending order in 2012: 3%; 3.8%; 19.3%; 30.1%; 43,8%\n\nAnswer: 65 years and older; 55 to 64 years; 15 to 24 years; 25 to 54 years; 0 to 14 years.\n\nStep 2: Arrange the 2018 percentages in ascending order and then use the percentages to arrange the age groups in ascending order.\n\nPercentages in ascending order in 2018: 3.3%; 4.0%; 19.8%; 30.4%; 42.5%\n\nAnswer: 65 years and older; 55 to 64 years; 15 to 24 years; 25 to 54 years; 0 to 14 years.\n\nThe percentages of the population in each age group have changed slightly over the six years, but the order of the age groups has not changed.\n\nStep 3: Find the percentage of Nigerians that fell into the 0 to 14 year age group in 2012, and then find that percentage of 166.2 million Nigerians.\n\nPercentage of the population in 2012 that fell into the 0 to 14 age group = 43.8%\n\nAnswer: Number of Nigerians that fell into the 0 to 14 age group in 2012 = 43.8% $\\times$ 166.2 million = 72.7956 million\n\nStep 4: Find the percentage of Nigerians that fell into the 0 to 14 year age group in 2018 and then find that percentage of 200.96 million Nigerians.\n\nPercentage of the population in 2018 that fell into the 0 to 14 age group = 42.5%\n\nAnswer: Number of Nigerians that fell into the 0 to 14 age group in 2018 = 42.5% $\\times$ 200.96 million = 85.408 million\n\nAlthough the percentage of the Nigerian population that fell in the 0 to 14 age group decreased from 2012 to 2018, the actual number of Nigerians in this age group increased from 72.7956 million to 85.408 million.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b009",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.2: Analyse statistical data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.2: Analyse statistical data given in a table",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b009-i01a",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.2: Analyse statistical data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.2: Analyse statistical data given in a table\n\n1. Chidi sourced information about the top eight causes of death in Nigeria from a survey published by the Centre for Disease Control and Prevention in 2013. The following table shows the results.\n\n| Reason for death | Percentage of total number of deaths in 2012 |\n| --- | ---: |\n| Malaria | 20% |\n| Chest infections | 19% |\n| HIV and Aids | 9% |\n| Diarrhoea | 5% |\n| Road accidents | 5% |\n| Malnutrition | 4% |\n| Cancer | 3% |\n| TB | 2% |\n\nUse the table to answer the following questions.\n\n1a. What percentage of deaths in 2012 were due to road accidents?",
    "answer_text": "Percentage of deaths in 2012 due to road accidents = 5%",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b009-i01b",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.2: Analyse statistical data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.2: Analyse statistical data given in a table\n\n1. Chidi sourced information about the top eight causes of death in Nigeria from a survey published by the Centre for Disease Control and Prevention in 2013. The following table shows the results.\n\n| Reason for death | Percentage of total number of deaths in 2012 |\n| --- | ---: |\n| Malaria | 20% |\n| Chest infections | 19% |\n| HIV and Aids | 9% |\n| Diarrhoea | 5% |\n| Road accidents | 5% |\n| Malnutrition | 4% |\n| Cancer | 3% |\n| TB | 2% |\n\nUse the table to answer the following questions.\n\n1b. In 2012, what was the difference in the percentage of deaths that were caused by chest infections and by cancer?",
    "answer_text": "Difference between the percentage of deaths in 2012 caused by chest infections and cancer = 19% $-$ 3% $=$ 13%",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b009-i01c",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.2: Analyse statistical data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.2: Analyse statistical data given in a table\n\n1. Chidi sourced information about the top eight causes of death in Nigeria from a survey published by the Centre for Disease Control and Prevention in 2013. The following table shows the results.\n\n| Reason for death | Percentage of total number of deaths in 2012 |\n| --- | ---: |\n| Malaria | 20% |\n| Chest infections | 19% |\n| HIV and Aids | 9% |\n| Diarrhoea | 5% |\n| Road accidents | 5% |\n| Malnutrition | 4% |\n| Cancer | 3% |\n| TB | 2% |\n\nUse the table to answer the following questions.\n\n1c. Approximately 2,500,000 Nigerians died during 2012. How many of these Nigerians died from malaria?",
    "answer_text": "Number of people who died from malaria in 2012 = 20% of 2,500,000 = 500,000",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b009-i02a",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.2: Analyse statistical data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.2: Analyse statistical data given in a table\n\n2. Abiodun wanted to know how the Lion, Leopard and Elephant Football teams were doing in the Nigerian Football League. He found the following table of results in the newspaper:\n\n| Team | Matches played | Won | Drawn | Lost | Goals for | Goals against | Points |\n| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n| Lions | 22 | 12 | 4 | 6 | 23 | 18 | 40 |\n| Leopards | 22 | 8 | 11 | 3 | 22 | 18 | 35 |\n| Elephants | 22 | 8 | 9 | 5 | 22 | 13 | 33 |\n\nThe points are calculated as follows:\n\nWin: 3 points  \nDraw: 1 point  \nLoss: 0 points\n\nUse the table to answer the following questions.\n\n2a. Which team won the most games?",
    "answer_text": "The Lions team won 12 of 22 games, so it won the most games.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b009-i02b",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.2: Analyse statistical data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.2: Analyse statistical data given in a table\n\n2. Abiodun wanted to know how the Lion, Leopard and Elephant Football teams were doing in the Nigerian Football League. He found the following table of results in the newspaper:\n\n| Team | Matches played | Won | Drawn | Lost | Goals for | Goals against | Points |\n| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n| Lions | 22 | 12 | 4 | 6 | 23 | 18 | 40 |\n| Leopards | 22 | 8 | 11 | 3 | 22 | 18 | 35 |\n| Elephants | 22 | 8 | 9 | 5 | 22 | 13 | 33 |\n\nThe points are calculated as follows:\n\nWin: 3 points  \nDraw: 1 point  \nLoss: 0 points\n\nUse the table to answer the following questions.\n\n2b. Which team drew more games?",
    "answer_text": "The Leopards team drew 11 of 22 games, so it drew the most games.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b009-i02c",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.2: Analyse statistical data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.2: Analyse statistical data given in a table\n\n2. Abiodun wanted to know how the Lion, Leopard and Elephant Football teams were doing in the Nigerian Football League. He found the following table of results in the newspaper:\n\n| Team | Matches played | Won | Drawn | Lost | Goals for | Goals against | Points |\n| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n| Lions | 22 | 12 | 4 | 6 | 23 | 18 | 40 |\n| Leopards | 22 | 8 | 11 | 3 | 22 | 18 | 35 |\n| Elephants | 22 | 8 | 9 | 5 | 22 | 13 | 33 |\n\nThe points are calculated as follows:\n\nWin: 3 points  \nDraw: 1 point  \nLoss: 0 points\n\nUse the table to answer the following questions.\n\n2c. Which team lost the most games?",
    "answer_text": "The Lions lost 6 of 22 games, so it lost the most games.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b009-i02d",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.2: Analyse statistical data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.2: Analyse statistical data given in a table\n\n2. Abiodun wanted to know how the Lion, Leopard and Elephant Football teams were doing in the Nigerian Football League. He found the following table of results in the newspaper:\n\n| Team | Matches played | Won | Drawn | Lost | Goals for | Goals against | Points |\n| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n| Lions | 22 | 12 | 4 | 6 | 23 | 18 | 40 |\n| Leopards | 22 | 8 | 11 | 3 | 22 | 18 | 35 |\n| Elephants | 22 | 8 | 9 | 5 | 22 | 13 | 33 |\n\nThe points are calculated as follows:\n\nWin: 3 points  \nDraw: 1 point  \nLoss: 0 points\n\nUse the table to answer the following questions.\n\n2d. Which team won the League?",
    "answer_text": "The Lions team had the most points, so it won the League.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b009-i02e",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.2: Analyse statistical data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.2: Analyse statistical data given in a table\n\n2. Abiodun wanted to know how the Lion, Leopard and Elephant Football teams were doing in the Nigerian Football League. He found the following table of results in the newspaper:\n\n| Team | Matches played | Won | Drawn | Lost | Goals for | Goals against | Points |\n| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n| Lions | 22 | 12 | 4 | 6 | 23 | 18 | 40 |\n| Leopards | 22 | 8 | 11 | 3 | 22 | 18 | 35 |\n| Elephants | 22 | 8 | 9 | 5 | 22 | 13 | 33 |\n\nThe points are calculated as follows:\n\nWin: 3 points  \nDraw: 1 point  \nLoss: 0 points\n\nUse the table to answer the following questions.\n\n2e. For each team, do the won, drawn and lost games add up to the matches played?",
    "answer_text": "Lions: 12 $+$ 4 + 6 $=$ 22\n\nLeopards: 8 $+$ 11 + 3 $=$ 22\n\nElephants: 8 $+$ 9 + 5 $=$ 22\n\nYes, the won, drawn and lost games for each team add up to 22, which is the number of games played.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b009-i02f",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.2: Analyse statistical data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.2: Analyse statistical data given in a table\n\n2. Abiodun wanted to know how the Lion, Leopard and Elephant Football teams were doing in the Nigerian Football League. He found the following table of results in the newspaper:\n\n| Team | Matches played | Won | Drawn | Lost | Goals for | Goals against | Points |\n| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n| Lions | 22 | 12 | 4 | 6 | 23 | 18 | 40 |\n| Leopards | 22 | 8 | 11 | 3 | 22 | 18 | 35 |\n| Elephants | 22 | 8 | 9 | 5 | 22 | 13 | 33 |\n\nThe points are calculated as follows:\n\nWin: 3 points  \nDraw: 1 point  \nLoss: 0 points\n\nUse the table to answer the following questions.\n\n2f. Show how the Elephants points were calculated.",
    "answer_text": "Elephants points = ($\\text{8}\\times{3}$) + ($\\text{9}\\times{1}$) + ($\\text{5}\\times{0}$) = $\\text{24 + 9 + 0 = 33}$",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b009-i02g",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.2: Analyse statistical data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.2: Analyse statistical data given in a table\n\n2. Abiodun wanted to know how the Lion, Leopard and Elephant Football teams were doing in the Nigerian Football League. He found the following table of results in the newspaper:\n\n| Team | Matches played | Won | Drawn | Lost | Goals for | Goals against | Points |\n| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n| Lions | 22 | 12 | 4 | 6 | 23 | 18 | 40 |\n| Leopards | 22 | 8 | 11 | 3 | 22 | 18 | 35 |\n| Elephants | 22 | 8 | 9 | 5 | 22 | 13 | 33 |\n\nThe points are calculated as follows:\n\nWin: 3 points  \nDraw: 1 point  \nLoss: 0 points\n\nUse the table to answer the following questions.\n\n2g. For every game the Lions lost, how many did the team win?",
    "answer_text": "The ratio of the number of games lost to the number of games won = $6 : 12 = 1 : 2$.\n\nFor every game the Lions team lost, it won two games.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b014",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Using statistics for predictions"
    },
    "content_text": "We can use statistics to help us with the planning of a project or a task. It can help us with financial decisions or with buying the correct stock for a business.\n\nWriting statistics in a table often helps when it comes to making predictions.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b015",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Worked example 16.4: Using a table to predict and plan"
    },
    "content_text": "",
    "prompt_text": "Adija sells Agege bread in large loaves and small loaves from her stall. Every day, she buys 24 large loaves and 24 small loaves from the bakery.\n\nAdija finds that she has several loaves of bread each day that she has not sold.\n\nShe decides to record the numbers of large loaves and small loaves that she sells every day for a week. She wants to use this table to guide her as to how many of each size loaf she should buy in future.\n\n| Size | Mon | Tues | Wed | Thurs | Fri | Sat | Sun |\n| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n| Large | 20 | 18 | 19 | 16 | 19 | 18 | 20 |\n| Small | 24 | 21 | 22 | 24 | 20 | 20 | 24 |\n\nUse the table to answer the following questions.\n\n1. How many large loaves did Adija sell altogether in that week?\n2. How many small loaves did Adija sell altogether in that week?\n3. During that week, did Adija sell more large loaves or small loaves?\n4. During that week, what was the maximum number of large loaves sold on one day?\n5. During that week, what was the maximum number of small loaves sold on one day?\n6. Of which size loaf should Adija buy fewer?",
    "answer_text": "Step 1: Add the number of large loaves sold.\n\nNumber of large loaves sold = 20 + 18 + 19 + 16 + 19 + 18 + 20 = 130\n\nStep 2: Add the number of small loaves sold.\n\nNumber of small loaves sold = 24 + 21 + 22 + 24 + 20 + 20 + 24 = 155\n\nStep 3: Compare the number of large loaves sold and the number of small loaves sold, and say which total is greater.\n\nAdija sold more small loaves than large loaves.\n\nStep 4: Look along the row showing large loaves and give the maximum number sold on a day.\n\nMaximum number of large loaves sold on a day = 20\n\nStep 5: Look along the row showing small loaves and give the maximum number sold on a day.\n\nMaximum number of small loaves sold on a day = 24\n\nStep 6: Compare the maximum number of large loaves sold and the maximum number of small loaves sold, and say which one Adija should buy fewer of.\n\nAdija should buy fewer large loaves.\n\nFrom the answers to the questions, we can see that the bread seller's statistical record of her sales helped her plan the number of loaves of bread to buy. This will help her not to spend money on loaves she does not sell, so it will help her to maximise the amount of money she makes from selling bread.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b016",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Exercise 16.4: Use statistics given in a table to predict and plan"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.4: Use statistics given in a table to predict and plan",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b016-i01a",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Exercise 16.4: Use statistics given in a table to predict and plan"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.4: Use statistics given in a table to predict and plan\n\n1. A stationery shop kept a record of the number of exercise books it sold in a week, as well as the total profit it made on the sale of these exercise books.\n\n| Exercise book size | Numbers sold | Profit made on the sale of each book (in ₦) |\n| ---: | ---: | ---: |\n| 60 pages | 100 | 5 |\n| 90 pages | 20 | 7 |\n| 120 pages | 40 | 9 |\n\nUse the table to answer the following questions.\n\n1a. Rank the size of the exercise books in order of the numbers sold.",
    "answer_text": "Ranked in numbers sold: 100; 40; 20\n\nSize of exercise books ranked in numbers sold: 60 pages; 120 pages; 90 pages.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b016-i01b",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Exercise 16.4: Use statistics given in a table to predict and plan"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.4: Use statistics given in a table to predict and plan\n\n1. A stationery shop kept a record of the number of exercise books it sold in a week, as well as the total profit it made on the sale of these exercise books.\n\n| Exercise book size | Numbers sold | Profit made on the sale of each book (in ₦) |\n| ---: | ---: | ---: |\n| 60 pages | 100 | 5 |\n| 90 pages | 20 | 7 |\n| 120 pages | 40 | 9 |\n\nUse the table to answer the following questions.\n\n1b. What is the total profit made on the sale of 60-page exercise books?",
    "answer_text": "Total profit made on the sale of 60-page exercise books = $\\text{100}\\times{₦5} = \\text{₦500}$",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b016-i01c",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Exercise 16.4: Use statistics given in a table to predict and plan"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.4: Use statistics given in a table to predict and plan\n\n1. A stationery shop kept a record of the number of exercise books it sold in a week, as well as the total profit it made on the sale of these exercise books.\n\n| Exercise book size | Numbers sold | Profit made on the sale of each book (in ₦) |\n| ---: | ---: | ---: |\n| 60 pages | 100 | 5 |\n| 90 pages | 20 | 7 |\n| 120 pages | 40 | 9 |\n\nUse the table to answer the following questions.\n\n1c. What is the total profit made on the sale of 90-page exercise books?",
    "answer_text": "Total profit made on the sale of 90-page exercise books = $\\text{20}\\times{₦7} = \\text{₦140}$",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b016-i01d",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Exercise 16.4: Use statistics given in a table to predict and plan"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.4: Use statistics given in a table to predict and plan\n\n1. A stationery shop kept a record of the number of exercise books it sold in a week, as well as the total profit it made on the sale of these exercise books.\n\n| Exercise book size | Numbers sold | Profit made on the sale of each book (in ₦) |\n| ---: | ---: | ---: |\n| 60 pages | 100 | 5 |\n| 90 pages | 20 | 7 |\n| 120 pages | 40 | 9 |\n\nUse the table to answer the following questions.\n\n1d. What is the total profit made on the sale of 120-page exercise books?",
    "answer_text": "Total profit made on the sale of 120-page exercise books = $\\text{40}\\times{₦9} = \\text{₦360}$",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b016-i01e",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Exercise 16.4: Use statistics given in a table to predict and plan"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.4: Use statistics given in a table to predict and plan\n\n1. A stationery shop kept a record of the number of exercise books it sold in a week, as well as the total profit it made on the sale of these exercise books.\n\n| Exercise book size | Numbers sold | Profit made on the sale of each book (in ₦) |\n| ---: | ---: | ---: |\n| 60 pages | 100 | 5 |\n| 90 pages | 20 | 7 |\n| 120 pages | 40 | 9 |\n\nUse the table to answer the following questions.\n\n1e. On which size exercise book did the stationery shop make the biggest profit?",
    "answer_text": "The stationery shop made the biggest profit on the 60-page exercise books.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b016-i01f",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Exercise 16.4: Use statistics given in a table to predict and plan"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.4: Use statistics given in a table to predict and plan\n\n1. A stationery shop kept a record of the number of exercise books it sold in a week, as well as the total profit it made on the sale of these exercise books.\n\n| Exercise book size | Numbers sold | Profit made on the sale of each book (in ₦) |\n| ---: | ---: | ---: |\n| 60 pages | 100 | 5 |\n| 90 pages | 20 | 7 |\n| 120 pages | 40 | 9 |\n\nUse the table to answer the following questions.\n\n1f. If the stationery shop had to stop stocking one of the exercise books, which one should it stop stocking?",
    "answer_text": "The stationery shop makes the smallest profit on the 90-page exercise books, as it sells the fewest of them. So it should stop stocking the 90-page exercise book.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b016-i02a",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Exercise 16.4: Use statistics given in a table to predict and plan"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.4: Use statistics given in a table to predict and plan\n\n2. This table shows some of the items sold in the local shop on a particular day, the number of each item sold that day, the price per item and the total amount earned by the item.\n\n| Items sold | Number sold | Price/item in ₦ | Amount earned in ₦ |\n| --- | ---: | ---: | --- |\n| 1 litre milk | 12 | 820 | $\\text{12}\\times{820}={9,840}$ |\n| 1 kg rice | 20 | 700 | $\\text{20}\\times{700}={14,000}$ |\n| 12 eggs | 15 | 600 | $\\text{15}\\times{600}={9,000}$ |\n| 1 kg bananas | 22 | 500 | $\\text{22}\\times{500}={11,000}$ |\n| 500 g cheese | 9 | 600 | $\\text{9}\\times{600}={5,400}$ |\n\n2a. Arrange the items in descending order, from the largest number sold to smallest number sold.",
    "answer_text": "Numbers sold in descending order: 22; 20; 15; 12; 9\n\nItems sold in descending order: bananas; rice; eggs; milk; cheese",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b016-i02b",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Exercise 16.4: Use statistics given in a table to predict and plan"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.4: Use statistics given in a table to predict and plan\n\n2. This table shows some of the items sold in the local shop on a particular day, the number of each item sold that day, the price per item and the total amount earned by the item.\n\n| Items sold | Number sold | Price/item in ₦ | Amount earned in ₦ |\n| --- | ---: | ---: | --- |\n| 1 litre milk | 12 | 820 | $\\text{12}\\times{820}={9,840}$ |\n| 1 kg rice | 20 | 700 | $\\text{20}\\times{700}={14,000}$ |\n| 12 eggs | 15 | 600 | $\\text{15}\\times{600}={9,000}$ |\n| 1 kg bananas | 22 | 500 | $\\text{22}\\times{500}={11,000}$ |\n| 500 g cheese | 9 | 600 | $\\text{9}\\times{600}={5,400}$ |\n\n2b. From which item sold did the shop keeper earn the most money?",
    "answer_text": "The shop keeper earned the most money from rice.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b016-i02c",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Exercise 16.4: Use statistics given in a table to predict and plan"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.4: Use statistics given in a table to predict and plan\n\n2. This table shows some of the items sold in the local shop on a particular day, the number of each item sold that day, the price per item and the total amount earned by the item.\n\n| Items sold | Number sold | Price/item in ₦ | Amount earned in ₦ |\n| --- | ---: | ---: | --- |\n| 1 litre milk | 12 | 820 | $\\text{12}\\times{820}={9,840}$ |\n| 1 kg rice | 20 | 700 | $\\text{20}\\times{700}={14,000}$ |\n| 12 eggs | 15 | 600 | $\\text{15}\\times{600}={9,000}$ |\n| 1 kg bananas | 22 | 500 | $\\text{22}\\times{500}={11,000}$ |\n| 500 g cheese | 9 | 600 | $\\text{9}\\times{600}={5,400}$ |\n\n2c. From which item sold did the shop keeper earn the least money?",
    "answer_text": "The shop keeper earned the least money from cheese.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b016-i02d",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Exercise 16.4: Use statistics given in a table to predict and plan"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.4: Use statistics given in a table to predict and plan\n\n2. This table shows some of the items sold in the local shop on a particular day, the number of each item sold that day, the price per item and the total amount earned by the item.\n\n| Items sold | Number sold | Price/item in ₦ | Amount earned in ₦ |\n| --- | ---: | ---: | --- |\n| 1 litre milk | 12 | 820 | $\\text{12}\\times{820}={9,840}$ |\n| 1 kg rice | 20 | 700 | $\\text{20}\\times{700}={14,000}$ |\n| 12 eggs | 15 | 600 | $\\text{15}\\times{600}={9,000}$ |\n| 1 kg bananas | 22 | 500 | $\\text{22}\\times{500}={11,000}$ |\n| 500 g cheese | 9 | 600 | $\\text{9}\\times{600}={5,400}$ |\n\n2d. The shop keeper decides to stop selling one of the items that she has been selling. Which item should she stop selling?",
    "answer_text": "The shopkeeper sells the fewest items of cheese and earns the least money from selling the cheese, so she should probably decide to stop selling cheese.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b017",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.4 Summary",
      "h3": null
    },
    "content_text": "- Statistics keeps us informed about what is happening in the world around us.\n- Statistics can be given in table form. We can analyse these statistics in order to draw conclusions about the information given.\n- Governments use statistics to make decisions about planning and where to spend their money best.\n- Probability involves the study of the laws of chance.\n- We can use the probability scale to give word descriptions or decimals that describe the probability of something occurring.\n- We can use statistics to help us with the planning of a project or or a task. It can help us with financial decisions or with buying the correct stock for a business.\n- Writing statistics in a table often helps when it comes to making predictions.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
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
  "topic_key": "jss1-math-need-for-statistics",
  "topic": "Need for Statistics",
  "subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics",
  "subtopic_title": "Purposes of statistics",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-need-for-statistics-purposes-of-statistics-po01",
        "source_performance_objective_index": 1,
        "text": "List purposes of statistics"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "purposes-of-statistics-ao-list-purposes",
          "text": "List purposes of statistics."
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
    "record_id": "ch16-b001",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": null
    },
    "content_text": "Statistics keeps us informed about what is happening in the world around us. Some examples of how statistics are useful are listed below.\n\n- Weather information is given in newspapers, on the radio, on television and on the internet. Scientists use statistics to compare previous weather with the current weather, and then predict future weather in a particular area.\n- Statistics play an important part in financial businesses. Traders and people in business use statistics to decide how they should invest and make money.\n- Statistics play an important role in the development of new medicines. New medicines have to be tested and results have to be recorded to see whether the medicines help in the way they are supposed to and whether they have bad side-effects.\n- News reporters make predictions of election winners based on statistics collected about how people are going to vote.\n- Statistical concepts are used in quality testing in factories and manufacturers. Companies test samples of products and use the statistical results to estimate whether all the products are likely to work correctly.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b002",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Statistical data"
    },
    "content_text": "The first step in doing statistical work is to decide what it is you want to find out about. The next thing you do is plan how you are going to gather enough information so you can find out what you want to know. The information used in statistics is called **data**.\n\nOnce your planning is complete, you begin to gather the information, which in statistics is called **collecting data**.\n\nExamples of data that you could collect about yourself, your friends or your family are:\n\n- where different people live\n- what different people eat for breakfast\n- people's favourite fruit\n- people's ages, heights or masses\n- the number of siblings that people have\n- which size shoe people wear\n\nOnce you have collected the data, you can put it in a table so it is easier to read and understand. Having the data organised in a table makes it easier to see what the data tells you and to answer questions about the data. This is called **analysing data**.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b003",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Statistical data"
    },
    "content_text": "If data is collected from a number of people, we say that we have surveyed the people. We \"do a survey\" to collect information from the people, such as where all the students in a school live.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b004",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Statistical data"
    },
    "content_text": "**data** Data is information in the form of facts, such as numbers, measurements or observations.\n\n**collecting data** Collecting data is gathering together and recording the information needed.\n\n**analysing data** Analysing data is making sense of the data to see what it tells you.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b005",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Worked example 16.1: Analysing data given in a table"
    },
    "content_text": "",
    "prompt_text": "A researcher wanted to compare the numbers of female and male teachers at different schools. She did a survey to find out the number of male and female teachers there were in six different schools. She recorded the results in this table.\n\n|  | School A | School B | School C | School D | School E | School F |\n| --- | ---: | ---: | ---: | ---: | ---: | ---: |\n| **Male teachers** | 18 | 8 | 9 | 3 | 9 | 5 |\n| **Female teachers** | 11 | 2 | 10 | 4 | 15 | 6 |\n\nUse the table to answer the following questions.\n\n1. How many teachers were there at School A?\n2. How many teachers were there at School D?\n3. Which school had the most male teachers?\n4. Which school had the most female teachers?\n5. Arrange the schools in order of most teachers to fewest teachers.",
    "answer_text": "Step 1: Find the column headed **School A**. Add together the number of male teachers and the number of female teachers.\n\nNumber of teachers at School A = $\\text{18 + 11 = 29}$\n\nAnswer: 29\n\nStep 2: Find the column headed **School D**. Add together the number of male teachers and the number of female teachers.\n\nNumber of teachers at School D = $\\text{3 + 4 = 7}$\n\nAnswer: 7\n\nStep 3: Look along the row marked **Male teachers** and find the column with the largest number in it.\n\nThere are 18 male teachers at School A, which is more than the number of male teachers at any other school.\n\nAnswer: School A\n\nStep 4: Look along the row marked **Female teachers** and find the column with the largest number in it.\n\nThere are 15 female teachers at School E, which is more than the number of female teachers at any other school.\n\nAnswer: School E\n\nStep 5: Add up the number of male teachers and female teachers at each school. Then arrange the schools in order from most to fewest teachers.\n\nSchool A = $\\text{18 + 11 = 29}$ teachers  \nSchool B = $\\text{8 + 2 = 10}$ teachers  \nSchool C = $\\text{9 + 10 = 19}$ teachers  \nSchool D = $\\text{3 + 4 = 7}$ teachers  \nSchool E = $\\text{9 + 15 = 24}$ teachers  \nSchool F = $\\text{5 + 6 = 11}$ teachers\n\nNumber of teachers from largest to smallest: 29; 24; 19; 11; 10; 7\n\nAnswer: School A; School E; School C; School F; School B; School D",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b006",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.1: Analyse data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.1: Analyse data given in a table",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b006-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.1: Analyse data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.1: Analyse data given in a table\n\nYou surveyed the students in your class at school to find out whether they preferred fruit juice, lemonade, orange fizz or cola.\n\nThe table shows the results of your survey.\n\n| Drink | Students |\n| --- | ---: |\n| fruit juice | 12 |\n| lemonade | 10 |\n| orange fizz | 11 |\n| cola | 7 |\n\n1. How many students took part in the survey?",
    "answer_text": "Number of students who took part in the survey = $\\text{12 + 10 + 11 + 7 = 40}$",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b006-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.1: Analyse data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.1: Analyse data given in a table\n\nYou surveyed the students in your class at school to find out whether they preferred fruit juice, lemonade, orange fizz or cola.\n\nThe table shows the results of your survey.\n\n| Drink | Students |\n| --- | ---: |\n| fruit juice | 12 |\n| lemonade | 10 |\n| orange fizz | 11 |\n| cola | 7 |\n\n2. Which drink was preferred by the largest number of students in your class?",
    "answer_text": "The largest number in the second column = 12\n\nFruit juice was preferred by the largest number of students.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b006-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.1: Analyse data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.1: Analyse data given in a table\n\nYou surveyed the students in your class at school to find out whether they preferred fruit juice, lemonade, orange fizz or cola.\n\nThe table shows the results of your survey.\n\n| Drink | Students |\n| --- | ---: |\n| fruit juice | 12 |\n| lemonade | 10 |\n| orange fizz | 11 |\n| cola | 7 |\n\n3. Which drink was preferred by the smallest number of students in your class?",
    "answer_text": "The smallest number in the second column = 7.\n\nThe smallest number of students preferred cola.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b006-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.1: Analyse data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.1: Analyse data given in a table\n\nYou surveyed the students in your class at school to find out whether they preferred fruit juice, lemonade, orange fizz or cola.\n\nThe table shows the results of your survey.\n\n| Drink | Students |\n| --- | ---: |\n| fruit juice | 12 |\n| lemonade | 10 |\n| orange fizz | 11 |\n| cola | 7 |\n\n4. Arrange the drinks in rank order. Rank order means from the one preferred by the largest number to the one preferred by the smallest number.",
    "answer_text": "Numbers from biggest to smallest: $\\text{12; 11; 10; 7}$.\n\nThe drinks in rank order are fruit juice; orange fizz; lemonade; cola.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b006-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.1: Analyse data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.1: Analyse data given in a table\n\nThe students in your class were surveyed to find out what size shoe they wear.\n\nThe results were organised into the following table.\n\n| Shoe size | Total number |\n| ---: | ---: |\n| 4 | 7 |\n| 5 | 9 |\n| 6 | 5 |\n| 7 | 11 |\n| 8 | 3 |\n| 9 | 1 |\n\n5. Which shoe size is worn by the most students in your class?",
    "answer_text": "The largest number in the second column for total number is 11 students.\n\nA size 7 shoe is worn by the most students.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b006-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.1: Analyse data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.1: Analyse data given in a table\n\nThe students in your class were surveyed to find out what size shoe they wear.\n\nThe results were organised into the following table.\n\n| Shoe size | Total number |\n| ---: | ---: |\n| 4 | 7 |\n| 5 | 9 |\n| 6 | 5 |\n| 7 | 11 |\n| 8 | 3 |\n| 9 | 1 |\n\n6. Which shoe size is worn by the fewest students in your class?",
    "answer_text": "The smallest number in the second column is 1 student.\n\nA size 9 shoe is worn by the fewest students.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b006-i07",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.1: Analyse data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.1: Analyse data given in a table\n\nThe students in your class were surveyed to find out what size shoe they wear.\n\nThe results were organised into the following table.\n\n| Shoe size | Total number |\n| ---: | ---: |\n| 4 | 7 |\n| 5 | 9 |\n| 6 | 5 |\n| 7 | 11 |\n| 8 | 3 |\n| 9 | 1 |\n\n7. How many students took part in the survey?",
    "answer_text": "Number of students that took part in the survey = $\\text{7 + 9 + 5 + 11 + 3 + 1 = 36}$",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b006-i08",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.1: Analyse data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.1: Analyse data given in a table\n\nThe students in your class were surveyed to find out what size shoe they wear.\n\nThe results were organised into the following table.\n\n| Shoe size | Total number |\n| ---: | ---: |\n| 4 | 7 |\n| 5 | 9 |\n| 6 | 5 |\n| 7 | 11 |\n| 8 | 3 |\n| 9 | 1 |\n\n8. Arrange the shoe sizes in rank order (from the shoe size worn by the most students to the shoe size worn by the fewest students).",
    "answer_text": "Number of students wearing each size in rank order: $\\text{11; 9; 7; 5; 3; 1}$.\n\nThe shoe sizes in rank order: size 7; size 5; size 4; size 6; size 8; size 9.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b007",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Sources of statistical information"
    },
    "content_text": "One source of statistical information would be the results of a survey. A second source of statistical information is the newspaper and another source of statistical information is the internet.\n\n- Information about the ages of people in Nigeria can be sourced from the Nigerian National Bureau of Statistics website at https://www.nigerianstat.gov.ng/.\n- Information about the top eight causes of death in Nigeria can be sourced from the Nigerian Centre for Disease Control and Prevention website at https://www.ncdc.gov.ng/.\n- Information about voter education and who is allowed to vote in the next elections can be sourced from the Independent National Election Commission website at https://www.inecnigeria.org/voter-education/.\n- Information about customer rights in a bank can be sourced from the Central Bank of Nigeria website at https://www.cbn.gov.ng/Supervision/cpdconedu.asp.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b008",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Worked example 16.2: Analysing statistical data about age groups"
    },
    "content_text": "",
    "prompt_text": "Erioluwa found the following information about the Nigerian population on the Nigerian National Bureau of Statistics website. The table gives statistics about the percentage of the Nigerian population in the given five age groups in 2012 and 2018.\n\n| Year | 0 to 14 years | 15 to 24 years | 25 to 54 years | 55 to 64 years | 65 years and older |\n| ---: | ---: | ---: | ---: | ---: | ---: |\n| 2012 | 43.8% | 19.3% | 30.1% | 3.8% | 3% |\n| 2018 | 42.5% | 19.8% | 30.4% | 4.0% | 3.3% |\n\nUse the table to answer the following questions.\n\n1. Arrange the age groups in 2012 in ascending order (from smallest to largest).\n2. Arrange the age groups in 2018 in ascending order. Comment on any differences in the rankings.\n3. In 2012 the population of Nigeria was approximately 166.2 million. How many Nigerians fell into the 0 to 14 year age group?\n4. In 2018 the population of Nigeria was approximately 200.96 million. How many Nigerians fell into the 0 to 14 age group? Comment on any differences in the figures.",
    "answer_text": "Step 1: Arrange the 2012 percentages in ascending order and then use the percentages to arrange the age groups in ascending order.\n\nPercentages in ascending order in 2012: 3%; 3.8%; 19.3%; 30.1%; 43,8%\n\nAnswer: 65 years and older; 55 to 64 years; 15 to 24 years; 25 to 54 years; 0 to 14 years.\n\nStep 2: Arrange the 2018 percentages in ascending order and then use the percentages to arrange the age groups in ascending order.\n\nPercentages in ascending order in 2018: 3.3%; 4.0%; 19.8%; 30.4%; 42.5%\n\nAnswer: 65 years and older; 55 to 64 years; 15 to 24 years; 25 to 54 years; 0 to 14 years.\n\nThe percentages of the population in each age group have changed slightly over the six years, but the order of the age groups has not changed.\n\nStep 3: Find the percentage of Nigerians that fell into the 0 to 14 year age group in 2012, and then find that percentage of 166.2 million Nigerians.\n\nPercentage of the population in 2012 that fell into the 0 to 14 age group = 43.8%\n\nAnswer: Number of Nigerians that fell into the 0 to 14 age group in 2012 = 43.8% $\\times$ 166.2 million = 72.7956 million\n\nStep 4: Find the percentage of Nigerians that fell into the 0 to 14 year age group in 2018 and then find that percentage of 200.96 million Nigerians.\n\nPercentage of the population in 2018 that fell into the 0 to 14 age group = 42.5%\n\nAnswer: Number of Nigerians that fell into the 0 to 14 age group in 2018 = 42.5% $\\times$ 200.96 million = 85.408 million\n\nAlthough the percentage of the Nigerian population that fell in the 0 to 14 age group decreased from 2012 to 2018, the actual number of Nigerians in this age group increased from 72.7956 million to 85.408 million.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b009",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.2: Analyse statistical data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.2: Analyse statistical data given in a table",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b009-i01a",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.2: Analyse statistical data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.2: Analyse statistical data given in a table\n\n1. Chidi sourced information about the top eight causes of death in Nigeria from a survey published by the Centre for Disease Control and Prevention in 2013. The following table shows the results.\n\n| Reason for death | Percentage of total number of deaths in 2012 |\n| --- | ---: |\n| Malaria | 20% |\n| Chest infections | 19% |\n| HIV and Aids | 9% |\n| Diarrhoea | 5% |\n| Road accidents | 5% |\n| Malnutrition | 4% |\n| Cancer | 3% |\n| TB | 2% |\n\nUse the table to answer the following questions.\n\n1a. What percentage of deaths in 2012 were due to road accidents?",
    "answer_text": "Percentage of deaths in 2012 due to road accidents = 5%",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b009-i01b",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.2: Analyse statistical data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.2: Analyse statistical data given in a table\n\n1. Chidi sourced information about the top eight causes of death in Nigeria from a survey published by the Centre for Disease Control and Prevention in 2013. The following table shows the results.\n\n| Reason for death | Percentage of total number of deaths in 2012 |\n| --- | ---: |\n| Malaria | 20% |\n| Chest infections | 19% |\n| HIV and Aids | 9% |\n| Diarrhoea | 5% |\n| Road accidents | 5% |\n| Malnutrition | 4% |\n| Cancer | 3% |\n| TB | 2% |\n\nUse the table to answer the following questions.\n\n1b. In 2012, what was the difference in the percentage of deaths that were caused by chest infections and by cancer?",
    "answer_text": "Difference between the percentage of deaths in 2012 caused by chest infections and cancer = 19% $-$ 3% $=$ 13%",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b009-i01c",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.2: Analyse statistical data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.2: Analyse statistical data given in a table\n\n1. Chidi sourced information about the top eight causes of death in Nigeria from a survey published by the Centre for Disease Control and Prevention in 2013. The following table shows the results.\n\n| Reason for death | Percentage of total number of deaths in 2012 |\n| --- | ---: |\n| Malaria | 20% |\n| Chest infections | 19% |\n| HIV and Aids | 9% |\n| Diarrhoea | 5% |\n| Road accidents | 5% |\n| Malnutrition | 4% |\n| Cancer | 3% |\n| TB | 2% |\n\nUse the table to answer the following questions.\n\n1c. Approximately 2,500,000 Nigerians died during 2012. How many of these Nigerians died from malaria?",
    "answer_text": "Number of people who died from malaria in 2012 = 20% of 2,500,000 = 500,000",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b009-i02a",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.2: Analyse statistical data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.2: Analyse statistical data given in a table\n\n2. Abiodun wanted to know how the Lion, Leopard and Elephant Football teams were doing in the Nigerian Football League. He found the following table of results in the newspaper:\n\n| Team | Matches played | Won | Drawn | Lost | Goals for | Goals against | Points |\n| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n| Lions | 22 | 12 | 4 | 6 | 23 | 18 | 40 |\n| Leopards | 22 | 8 | 11 | 3 | 22 | 18 | 35 |\n| Elephants | 22 | 8 | 9 | 5 | 22 | 13 | 33 |\n\nThe points are calculated as follows:\n\nWin: 3 points  \nDraw: 1 point  \nLoss: 0 points\n\nUse the table to answer the following questions.\n\n2a. Which team won the most games?",
    "answer_text": "The Lions team won 12 of 22 games, so it won the most games.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b009-i02b",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.2: Analyse statistical data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.2: Analyse statistical data given in a table\n\n2. Abiodun wanted to know how the Lion, Leopard and Elephant Football teams were doing in the Nigerian Football League. He found the following table of results in the newspaper:\n\n| Team | Matches played | Won | Drawn | Lost | Goals for | Goals against | Points |\n| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n| Lions | 22 | 12 | 4 | 6 | 23 | 18 | 40 |\n| Leopards | 22 | 8 | 11 | 3 | 22 | 18 | 35 |\n| Elephants | 22 | 8 | 9 | 5 | 22 | 13 | 33 |\n\nThe points are calculated as follows:\n\nWin: 3 points  \nDraw: 1 point  \nLoss: 0 points\n\nUse the table to answer the following questions.\n\n2b. Which team drew more games?",
    "answer_text": "The Leopards team drew 11 of 22 games, so it drew the most games.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b009-i02c",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.2: Analyse statistical data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.2: Analyse statistical data given in a table\n\n2. Abiodun wanted to know how the Lion, Leopard and Elephant Football teams were doing in the Nigerian Football League. He found the following table of results in the newspaper:\n\n| Team | Matches played | Won | Drawn | Lost | Goals for | Goals against | Points |\n| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n| Lions | 22 | 12 | 4 | 6 | 23 | 18 | 40 |\n| Leopards | 22 | 8 | 11 | 3 | 22 | 18 | 35 |\n| Elephants | 22 | 8 | 9 | 5 | 22 | 13 | 33 |\n\nThe points are calculated as follows:\n\nWin: 3 points  \nDraw: 1 point  \nLoss: 0 points\n\nUse the table to answer the following questions.\n\n2c. Which team lost the most games?",
    "answer_text": "The Lions lost 6 of 22 games, so it lost the most games.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b009-i02d",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.2: Analyse statistical data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.2: Analyse statistical data given in a table\n\n2. Abiodun wanted to know how the Lion, Leopard and Elephant Football teams were doing in the Nigerian Football League. He found the following table of results in the newspaper:\n\n| Team | Matches played | Won | Drawn | Lost | Goals for | Goals against | Points |\n| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n| Lions | 22 | 12 | 4 | 6 | 23 | 18 | 40 |\n| Leopards | 22 | 8 | 11 | 3 | 22 | 18 | 35 |\n| Elephants | 22 | 8 | 9 | 5 | 22 | 13 | 33 |\n\nThe points are calculated as follows:\n\nWin: 3 points  \nDraw: 1 point  \nLoss: 0 points\n\nUse the table to answer the following questions.\n\n2d. Which team won the League?",
    "answer_text": "The Lions team had the most points, so it won the League.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b009-i02e",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.2: Analyse statistical data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.2: Analyse statistical data given in a table\n\n2. Abiodun wanted to know how the Lion, Leopard and Elephant Football teams were doing in the Nigerian Football League. He found the following table of results in the newspaper:\n\n| Team | Matches played | Won | Drawn | Lost | Goals for | Goals against | Points |\n| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n| Lions | 22 | 12 | 4 | 6 | 23 | 18 | 40 |\n| Leopards | 22 | 8 | 11 | 3 | 22 | 18 | 35 |\n| Elephants | 22 | 8 | 9 | 5 | 22 | 13 | 33 |\n\nThe points are calculated as follows:\n\nWin: 3 points  \nDraw: 1 point  \nLoss: 0 points\n\nUse the table to answer the following questions.\n\n2e. For each team, do the won, drawn and lost games add up to the matches played?",
    "answer_text": "Lions: 12 $+$ 4 + 6 $=$ 22\n\nLeopards: 8 $+$ 11 + 3 $=$ 22\n\nElephants: 8 $+$ 9 + 5 $=$ 22\n\nYes, the won, drawn and lost games for each team add up to 22, which is the number of games played.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b009-i02f",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.2: Analyse statistical data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.2: Analyse statistical data given in a table\n\n2. Abiodun wanted to know how the Lion, Leopard and Elephant Football teams were doing in the Nigerian Football League. He found the following table of results in the newspaper:\n\n| Team | Matches played | Won | Drawn | Lost | Goals for | Goals against | Points |\n| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n| Lions | 22 | 12 | 4 | 6 | 23 | 18 | 40 |\n| Leopards | 22 | 8 | 11 | 3 | 22 | 18 | 35 |\n| Elephants | 22 | 8 | 9 | 5 | 22 | 13 | 33 |\n\nThe points are calculated as follows:\n\nWin: 3 points  \nDraw: 1 point  \nLoss: 0 points\n\nUse the table to answer the following questions.\n\n2f. Show how the Elephants points were calculated.",
    "answer_text": "Elephants points = ($\\text{8}\\times{3}$) + ($\\text{9}\\times{1}$) + ($\\text{5}\\times{0}$) = $\\text{24 + 9 + 0 = 33}$",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b009-i02g",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.1 The purposes of statistics",
      "h3": "Exercise 16.2: Analyse statistical data given in a table"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.2: Analyse statistical data given in a table\n\n2. Abiodun wanted to know how the Lion, Leopard and Elephant Football teams were doing in the Nigerian Football League. He found the following table of results in the newspaper:\n\n| Team | Matches played | Won | Drawn | Lost | Goals for | Goals against | Points |\n| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n| Lions | 22 | 12 | 4 | 6 | 23 | 18 | 40 |\n| Leopards | 22 | 8 | 11 | 3 | 22 | 18 | 35 |\n| Elephants | 22 | 8 | 9 | 5 | 22 | 13 | 33 |\n\nThe points are calculated as follows:\n\nWin: 3 points  \nDraw: 1 point  \nLoss: 0 points\n\nUse the table to answer the following questions.\n\n2g. For every game the Lions lost, how many did the team win?",
    "answer_text": "The ratio of the number of games lost to the number of games won = $6 : 12 = 1 : 2$.\n\nFor every game the Lions team lost, it won two games.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
  },
  {
    "record_id": "ch16-b014",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Using statistics for predictions"
    },
    "content_text": "We can use statistics to help us with the planning of a project or a task. It can help us with financial decisions or with buying the correct stock for a business.\n\nWriting statistics in a table often helps when it comes to making predictions.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b015",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Worked example 16.4: Using a table to predict and plan"
    },
    "content_text": "",
    "prompt_text": "Adija sells Agege bread in large loaves and small loaves from her stall. Every day, she buys 24 large loaves and 24 small loaves from the bakery.\n\nAdija finds that she has several loaves of bread each day that she has not sold.\n\nShe decides to record the numbers of large loaves and small loaves that she sells every day for a week. She wants to use this table to guide her as to how many of each size loaf she should buy in future.\n\n| Size | Mon | Tues | Wed | Thurs | Fri | Sat | Sun |\n| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n| Large | 20 | 18 | 19 | 16 | 19 | 18 | 20 |\n| Small | 24 | 21 | 22 | 24 | 20 | 20 | 24 |\n\nUse the table to answer the following questions.\n\n1. How many large loaves did Adija sell altogether in that week?\n2. How many small loaves did Adija sell altogether in that week?\n3. During that week, did Adija sell more large loaves or small loaves?\n4. During that week, what was the maximum number of large loaves sold on one day?\n5. During that week, what was the maximum number of small loaves sold on one day?\n6. Of which size loaf should Adija buy fewer?",
    "answer_text": "Step 1: Add the number of large loaves sold.\n\nNumber of large loaves sold = 20 + 18 + 19 + 16 + 19 + 18 + 20 = 130\n\nStep 2: Add the number of small loaves sold.\n\nNumber of small loaves sold = 24 + 21 + 22 + 24 + 20 + 20 + 24 = 155\n\nStep 3: Compare the number of large loaves sold and the number of small loaves sold, and say which total is greater.\n\nAdija sold more small loaves than large loaves.\n\nStep 4: Look along the row showing large loaves and give the maximum number sold on a day.\n\nMaximum number of large loaves sold on a day = 20\n\nStep 5: Look along the row showing small loaves and give the maximum number sold on a day.\n\nMaximum number of small loaves sold on a day = 24\n\nStep 6: Compare the maximum number of large loaves sold and the maximum number of small loaves sold, and say which one Adija should buy fewer of.\n\nAdija should buy fewer large loaves.\n\nFrom the answers to the questions, we can see that the bread seller's statistical record of her sales helped her plan the number of loaves of bread to buy. This will help her not to spend money on loaves she does not sell, so it will help her to maximise the amount of money she makes from selling bread.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b016",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Exercise 16.4: Use statistics given in a table to predict and plan"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.4: Use statistics given in a table to predict and plan",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b016-i01a",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Exercise 16.4: Use statistics given in a table to predict and plan"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.4: Use statistics given in a table to predict and plan\n\n1. A stationery shop kept a record of the number of exercise books it sold in a week, as well as the total profit it made on the sale of these exercise books.\n\n| Exercise book size | Numbers sold | Profit made on the sale of each book (in ₦) |\n| ---: | ---: | ---: |\n| 60 pages | 100 | 5 |\n| 90 pages | 20 | 7 |\n| 120 pages | 40 | 9 |\n\nUse the table to answer the following questions.\n\n1a. Rank the size of the exercise books in order of the numbers sold.",
    "answer_text": "Ranked in numbers sold: 100; 40; 20\n\nSize of exercise books ranked in numbers sold: 60 pages; 120 pages; 90 pages.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b016-i01b",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Exercise 16.4: Use statistics given in a table to predict and plan"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.4: Use statistics given in a table to predict and plan\n\n1. A stationery shop kept a record of the number of exercise books it sold in a week, as well as the total profit it made on the sale of these exercise books.\n\n| Exercise book size | Numbers sold | Profit made on the sale of each book (in ₦) |\n| ---: | ---: | ---: |\n| 60 pages | 100 | 5 |\n| 90 pages | 20 | 7 |\n| 120 pages | 40 | 9 |\n\nUse the table to answer the following questions.\n\n1b. What is the total profit made on the sale of 60-page exercise books?",
    "answer_text": "Total profit made on the sale of 60-page exercise books = $\\text{100}\\times{₦5} = \\text{₦500}$",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b016-i01c",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Exercise 16.4: Use statistics given in a table to predict and plan"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.4: Use statistics given in a table to predict and plan\n\n1. A stationery shop kept a record of the number of exercise books it sold in a week, as well as the total profit it made on the sale of these exercise books.\n\n| Exercise book size | Numbers sold | Profit made on the sale of each book (in ₦) |\n| ---: | ---: | ---: |\n| 60 pages | 100 | 5 |\n| 90 pages | 20 | 7 |\n| 120 pages | 40 | 9 |\n\nUse the table to answer the following questions.\n\n1c. What is the total profit made on the sale of 90-page exercise books?",
    "answer_text": "Total profit made on the sale of 90-page exercise books = $\\text{20}\\times{₦7} = \\text{₦140}$",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b016-i01d",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Exercise 16.4: Use statistics given in a table to predict and plan"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.4: Use statistics given in a table to predict and plan\n\n1. A stationery shop kept a record of the number of exercise books it sold in a week, as well as the total profit it made on the sale of these exercise books.\n\n| Exercise book size | Numbers sold | Profit made on the sale of each book (in ₦) |\n| ---: | ---: | ---: |\n| 60 pages | 100 | 5 |\n| 90 pages | 20 | 7 |\n| 120 pages | 40 | 9 |\n\nUse the table to answer the following questions.\n\n1d. What is the total profit made on the sale of 120-page exercise books?",
    "answer_text": "Total profit made on the sale of 120-page exercise books = $\\text{40}\\times{₦9} = \\text{₦360}$",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b016-i01e",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Exercise 16.4: Use statistics given in a table to predict and plan"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.4: Use statistics given in a table to predict and plan\n\n1. A stationery shop kept a record of the number of exercise books it sold in a week, as well as the total profit it made on the sale of these exercise books.\n\n| Exercise book size | Numbers sold | Profit made on the sale of each book (in ₦) |\n| ---: | ---: | ---: |\n| 60 pages | 100 | 5 |\n| 90 pages | 20 | 7 |\n| 120 pages | 40 | 9 |\n\nUse the table to answer the following questions.\n\n1e. On which size exercise book did the stationery shop make the biggest profit?",
    "answer_text": "The stationery shop made the biggest profit on the 60-page exercise books.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b016-i01f",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Exercise 16.4: Use statistics given in a table to predict and plan"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.4: Use statistics given in a table to predict and plan\n\n1. A stationery shop kept a record of the number of exercise books it sold in a week, as well as the total profit it made on the sale of these exercise books.\n\n| Exercise book size | Numbers sold | Profit made on the sale of each book (in ₦) |\n| ---: | ---: | ---: |\n| 60 pages | 100 | 5 |\n| 90 pages | 20 | 7 |\n| 120 pages | 40 | 9 |\n\nUse the table to answer the following questions.\n\n1f. If the stationery shop had to stop stocking one of the exercise books, which one should it stop stocking?",
    "answer_text": "The stationery shop makes the smallest profit on the 90-page exercise books, as it sells the fewest of them. So it should stop stocking the 90-page exercise book.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b016-i02a",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Exercise 16.4: Use statistics given in a table to predict and plan"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.4: Use statistics given in a table to predict and plan\n\n2. This table shows some of the items sold in the local shop on a particular day, the number of each item sold that day, the price per item and the total amount earned by the item.\n\n| Items sold | Number sold | Price/item in ₦ | Amount earned in ₦ |\n| --- | ---: | ---: | --- |\n| 1 litre milk | 12 | 820 | $\\text{12}\\times{820}={9,840}$ |\n| 1 kg rice | 20 | 700 | $\\text{20}\\times{700}={14,000}$ |\n| 12 eggs | 15 | 600 | $\\text{15}\\times{600}={9,000}$ |\n| 1 kg bananas | 22 | 500 | $\\text{22}\\times{500}={11,000}$ |\n| 500 g cheese | 9 | 600 | $\\text{9}\\times{600}={5,400}$ |\n\n2a. Arrange the items in descending order, from the largest number sold to smallest number sold.",
    "answer_text": "Numbers sold in descending order: 22; 20; 15; 12; 9\n\nItems sold in descending order: bananas; rice; eggs; milk; cheese",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b016-i02b",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Exercise 16.4: Use statistics given in a table to predict and plan"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.4: Use statistics given in a table to predict and plan\n\n2. This table shows some of the items sold in the local shop on a particular day, the number of each item sold that day, the price per item and the total amount earned by the item.\n\n| Items sold | Number sold | Price/item in ₦ | Amount earned in ₦ |\n| --- | ---: | ---: | --- |\n| 1 litre milk | 12 | 820 | $\\text{12}\\times{820}={9,840}$ |\n| 1 kg rice | 20 | 700 | $\\text{20}\\times{700}={14,000}$ |\n| 12 eggs | 15 | 600 | $\\text{15}\\times{600}={9,000}$ |\n| 1 kg bananas | 22 | 500 | $\\text{22}\\times{500}={11,000}$ |\n| 500 g cheese | 9 | 600 | $\\text{9}\\times{600}={5,400}$ |\n\n2b. From which item sold did the shop keeper earn the most money?",
    "answer_text": "The shop keeper earned the most money from rice.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b016-i02c",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Exercise 16.4: Use statistics given in a table to predict and plan"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.4: Use statistics given in a table to predict and plan\n\n2. This table shows some of the items sold in the local shop on a particular day, the number of each item sold that day, the price per item and the total amount earned by the item.\n\n| Items sold | Number sold | Price/item in ₦ | Amount earned in ₦ |\n| --- | ---: | ---: | --- |\n| 1 litre milk | 12 | 820 | $\\text{12}\\times{820}={9,840}$ |\n| 1 kg rice | 20 | 700 | $\\text{20}\\times{700}={14,000}$ |\n| 12 eggs | 15 | 600 | $\\text{15}\\times{600}={9,000}$ |\n| 1 kg bananas | 22 | 500 | $\\text{22}\\times{500}={11,000}$ |\n| 500 g cheese | 9 | 600 | $\\text{9}\\times{600}={5,400}$ |\n\n2c. From which item sold did the shop keeper earn the least money?",
    "answer_text": "The shop keeper earned the least money from cheese.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b016-i02d",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.3 Practical applications",
      "h3": "Exercise 16.4: Use statistics given in a table to predict and plan"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.4: Use statistics given in a table to predict and plan\n\n2. This table shows some of the items sold in the local shop on a particular day, the number of each item sold that day, the price per item and the total amount earned by the item.\n\n| Items sold | Number sold | Price/item in ₦ | Amount earned in ₦ |\n| --- | ---: | ---: | --- |\n| 1 litre milk | 12 | 820 | $\\text{12}\\times{820}={9,840}$ |\n| 1 kg rice | 20 | 700 | $\\text{20}\\times{700}={14,000}$ |\n| 12 eggs | 15 | 600 | $\\text{15}\\times{600}={9,000}$ |\n| 1 kg bananas | 22 | 500 | $\\text{22}\\times{500}={11,000}$ |\n| 500 g cheese | 9 | 600 | $\\text{9}\\times{600}={5,400}$ |\n\n2d. The shop keeper decides to stop selling one of the items that she has been selling. Which item should she stop selling?",
    "answer_text": "The shopkeeper sells the fewest items of cheese and earns the least money from selling the cheese, so she should probably decide to stop selling cheese.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b017",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.4 Summary",
      "h3": null
    },
    "content_text": "- Statistics keeps us informed about what is happening in the world around us.\n- Statistics can be given in table form. We can analyse these statistics in order to draw conclusions about the information given.\n- Governments use statistics to make decisions about planning and where to spend their money best.\n- Probability involves the study of the laws of chance.\n- We can use the probability scale to give word descriptions or decimals that describe the probability of something occurring.\n- We can use statistics to help us with the planning of a project or or a task. It can help us with financial decisions or with buying the correct stock for a business.\n- Writing statistics in a table often helps when it comes to making predictions.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-purposes-of-statistics"
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
