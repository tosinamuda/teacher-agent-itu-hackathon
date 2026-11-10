# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-5",
  "topic_key": "jss1-math-need-for-statistics",
  "topic": "Need for Statistics",
  "subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes",
  "subtopic_title": "Need for collecting data for planning purposes",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes-po01",
        "source_performance_objective_index": 1,
        "text": "Recognise the usefulness of statistics for planning purposes"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "need-for-collecting-data-for-planning-purposes-ao-recognise-usefulness-for-planning",
          "text": "Recognise the usefulness of statistics for planning purposes."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes-po02",
        "source_performance_objective_index": 2,
        "text": "Apply the occurrence of chance events / application of probabilities in everyday life"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "need-for-collecting-data-for-planning-purposes-ao-apply-chance-events-and-probabilities",
          "text": "Apply the occurrence of chance events / application of probabilities in everyday life."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes-po03",
        "source_performance_objective_index": 3,
        "text": "Recognise the usefulness of statistics for prediction purposes"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "need-for-collecting-data-for-planning-purposes-ao-recognise-usefulness-for-prediction",
          "text": "Recognise the usefulness of statistics for prediction purposes."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch16-b010",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.2 Introduction to probability",
      "h3": null
    },
    "content_text": "Probability is the study of the laws of chance. It is about how probable or how likely it is that something will happen.\n\nWe often use the word \"chance\" when we are talking about probability, for example, \"I have no chance of winning the prize!\"\n\nExamples of other statements that try to predict how likely an event will happen are:\n\n- \"I am sure it will never happen.\"\n- \"It might hail today.\"\n- \"She is unlikely to visit tomorrow.\"",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b011",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.2 Introduction to probability",
      "h3": "The probability scale"
    },
    "content_text": "To describe the probability that something will happen, we can use a probability scale.\n\nThe probability scale is a line that starts with impossible events at the left-hand end and ends with certain events at the right-hand end.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss2-15-1_016.png\n\nAll probabilities must fall somewhere on this line.\n\n- An event that is described as *impossible* is one that we know will never happen, such as having 8 days in one week. An event that is impossible is given a probability of 0.\n- An event is described as *certain* if we know that it will definitely happen, such as having a Monday in a week. An event that is certain is given a probability of 1.\n- Between the two ends of the line are word descriptions and decimals, such as very unlikely (a probability of 0.2), unlikely (a probability of 0.4), 50% chance, which means an equal chance that two things will happen (a probability of 0.5), likely (a probability of 0.6), and very likely (a probability of 0.8).",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b012",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.2 Introduction to probability",
      "h3": "Worked example 16.3: Using the probability scale to describe probability"
    },
    "content_text": "",
    "prompt_text": "Use the probability scale to find a word description for each of the events listed below.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss2-15-1_016.png\n\n1. What are the chances of someone winning the lottery if he buys a ticket every week for two months?\n2. How likely is it that the sun will rise tomorrow morning?\n3. What are the chances of a pregnant woman having a female child or a male child?",
    "answer_text": "Step 1: The chance of winning the lottery is extremely small, no matter how often one buys tickets. Choose a word description from the scale that describes this.\n\nIt is *highly unlikely* that this person will win the lottery.\n\nStep 2: The sun will definitely rise tomorrow morning. Choose the best word from the scale that describes this.\n\nIt is *certain* that the sun will rise tomorrow morning.\n\nStep 3: Choose a word description from the scale that describes this.\n\nThere is a *50% chance* (or you could say an *equal chance*) of a pregnant woman having a female or a male child.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b013",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.2 Introduction to probability",
      "h3": "Exercise 16.3: Use the probability scale to describe probability"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.3: Use the probability scale to describe probability\n\nUse the probability scale to give each of these events a word description from the scale.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss2-15-1_016.png",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b013-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.2 Introduction to probability",
      "h3": "Exercise 16.3: Use the probability scale to describe probability"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.3: Use the probability scale to describe probability\n\nUse the probability scale to give each of these events a word description from the scale.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss2-15-1_016.png\n\n1. The player will throw a number smaller than 7 on an ordinary die.",
    "answer_text": "It is certain that the player will throw a number smaller than 7 on an ordinary die.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b013-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.2 Introduction to probability",
      "h3": "Exercise 16.3: Use the probability scale to describe probability"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.3: Use the probability scale to describe probability\n\nUse the probability scale to give each of these events a word description from the scale.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss2-15-1_016.png\n\n2. It will rain tomorrow in the Sahara Desert.",
    "answer_text": "It is very unlikely that it will rain tomorrow in the Sahara Desert.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b013-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.2 Introduction to probability",
      "h3": "Exercise 16.3: Use the probability scale to describe probability"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.3: Use the probability scale to describe probability\n\nUse the probability scale to give each of these events a word description from the scale.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss2-15-1_016.png\n\n3. I am 2 years old and I own a motor car.",
    "answer_text": "It is very unlikely that someone will be 2 years old and will own a motor car.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b013-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.2 Introduction to probability",
      "h3": "Exercise 16.3: Use the probability scale to describe probability"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.3: Use the probability scale to describe probability\n\nUse the probability scale to give each of these events a word description from the scale.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss2-15-1_016.png\n\n4. When I toss a coin, it will land on heads.",
    "answer_text": "There is a 50% chance that the coin will land on heads. It is just as likely to land on tails.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b013-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.2 Introduction to probability",
      "h3": "Exercise 16.3: Use the probability scale to describe probability"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.3: Use the probability scale to describe probability\n\nUse the probability scale to give each of these events a word description from the scale.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss2-15-1_016.png\n\n5. The day after Tuesday is Wednesday.",
    "answer_text": "It is certain that the day after Tuesday is Wednesday.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b013-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.2 Introduction to probability",
      "h3": "Exercise 16.3: Use the probability scale to describe probability"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.3: Use the probability scale to describe probability\n\nUse the probability scale to give each of these events a word description from the scale.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss2-15-1_016.png\n\n6. In a particular calendar year, June always comes before March.",
    "answer_text": "It is impossible that June will come before March in a particular calendar year.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
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
  "subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes",
  "subtopic_title": "Need for collecting data for planning purposes",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes-po01",
        "source_performance_objective_index": 1,
        "text": "Recognise the usefulness of statistics for planning purposes"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "need-for-collecting-data-for-planning-purposes-ao-recognise-usefulness-for-planning",
          "text": "Recognise the usefulness of statistics for planning purposes."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes-po02",
        "source_performance_objective_index": 2,
        "text": "Apply the occurrence of chance events / application of probabilities in everyday life"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "need-for-collecting-data-for-planning-purposes-ao-apply-chance-events-and-probabilities",
          "text": "Apply the occurrence of chance events / application of probabilities in everyday life."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes-po03",
        "source_performance_objective_index": 3,
        "text": "Recognise the usefulness of statistics for prediction purposes"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "need-for-collecting-data-for-planning-purposes-ao-recognise-usefulness-for-prediction",
          "text": "Recognise the usefulness of statistics for prediction purposes."
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
    "record_id": "ch16-b010",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.2 Introduction to probability",
      "h3": null
    },
    "content_text": "Probability is the study of the laws of chance. It is about how probable or how likely it is that something will happen.\n\nWe often use the word \"chance\" when we are talking about probability, for example, \"I have no chance of winning the prize!\"\n\nExamples of other statements that try to predict how likely an event will happen are:\n\n- \"I am sure it will never happen.\"\n- \"It might hail today.\"\n- \"She is unlikely to visit tomorrow.\"",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b011",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.2 Introduction to probability",
      "h3": "The probability scale"
    },
    "content_text": "To describe the probability that something will happen, we can use a probability scale.\n\nThe probability scale is a line that starts with impossible events at the left-hand end and ends with certain events at the right-hand end.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss2-15-1_016.png\n\nAll probabilities must fall somewhere on this line.\n\n- An event that is described as *impossible* is one that we know will never happen, such as having 8 days in one week. An event that is impossible is given a probability of 0.\n- An event is described as *certain* if we know that it will definitely happen, such as having a Monday in a week. An event that is certain is given a probability of 1.\n- Between the two ends of the line are word descriptions and decimals, such as very unlikely (a probability of 0.2), unlikely (a probability of 0.4), 50% chance, which means an equal chance that two things will happen (a probability of 0.5), likely (a probability of 0.6), and very likely (a probability of 0.8).",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b012",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.2 Introduction to probability",
      "h3": "Worked example 16.3: Using the probability scale to describe probability"
    },
    "content_text": "",
    "prompt_text": "Use the probability scale to find a word description for each of the events listed below.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss2-15-1_016.png\n\n1. What are the chances of someone winning the lottery if he buys a ticket every week for two months?\n2. How likely is it that the sun will rise tomorrow morning?\n3. What are the chances of a pregnant woman having a female child or a male child?",
    "answer_text": "Step 1: The chance of winning the lottery is extremely small, no matter how often one buys tickets. Choose a word description from the scale that describes this.\n\nIt is *highly unlikely* that this person will win the lottery.\n\nStep 2: The sun will definitely rise tomorrow morning. Choose the best word from the scale that describes this.\n\nIt is *certain* that the sun will rise tomorrow morning.\n\nStep 3: Choose a word description from the scale that describes this.\n\nThere is a *50% chance* (or you could say an *equal chance*) of a pregnant woman having a female or a male child.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b013",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.2 Introduction to probability",
      "h3": "Exercise 16.3: Use the probability scale to describe probability"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.3: Use the probability scale to describe probability\n\nUse the probability scale to give each of these events a word description from the scale.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss2-15-1_016.png",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b013-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.2 Introduction to probability",
      "h3": "Exercise 16.3: Use the probability scale to describe probability"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.3: Use the probability scale to describe probability\n\nUse the probability scale to give each of these events a word description from the scale.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss2-15-1_016.png\n\n1. The player will throw a number smaller than 7 on an ordinary die.",
    "answer_text": "It is certain that the player will throw a number smaller than 7 on an ordinary die.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b013-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.2 Introduction to probability",
      "h3": "Exercise 16.3: Use the probability scale to describe probability"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.3: Use the probability scale to describe probability\n\nUse the probability scale to give each of these events a word description from the scale.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss2-15-1_016.png\n\n2. It will rain tomorrow in the Sahara Desert.",
    "answer_text": "It is very unlikely that it will rain tomorrow in the Sahara Desert.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b013-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.2 Introduction to probability",
      "h3": "Exercise 16.3: Use the probability scale to describe probability"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.3: Use the probability scale to describe probability\n\nUse the probability scale to give each of these events a word description from the scale.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss2-15-1_016.png\n\n3. I am 2 years old and I own a motor car.",
    "answer_text": "It is very unlikely that someone will be 2 years old and will own a motor car.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b013-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.2 Introduction to probability",
      "h3": "Exercise 16.3: Use the probability scale to describe probability"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.3: Use the probability scale to describe probability\n\nUse the probability scale to give each of these events a word description from the scale.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss2-15-1_016.png\n\n4. When I toss a coin, it will land on heads.",
    "answer_text": "There is a 50% chance that the coin will land on heads. It is just as likely to land on tails.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b013-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.2 Introduction to probability",
      "h3": "Exercise 16.3: Use the probability scale to describe probability"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.3: Use the probability scale to describe probability\n\nUse the probability scale to give each of these events a word description from the scale.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss2-15-1_016.png\n\n5. The day after Tuesday is Wednesday.",
    "answer_text": "It is certain that the day after Tuesday is Wednesday.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
  },
  {
    "record_id": "ch16-b013-i06",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 16: Need for statistics",
      "h2": "16.2 Introduction to probability",
      "h3": "Exercise 16.3: Use the probability scale to describe probability"
    },
    "content_text": "",
    "prompt_text": "### Exercise 16.3: Use the probability scale to describe probability\n\nUse the probability scale to give each of these events a word description from the scale.\n\nSource image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss2-15-1_016.png\n\n6. In a particular calendar year, June always comes before March.",
    "answer_text": "It is impossible that June will come before March in a particular calendar year.",
    "primary_subtopic_id": "jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes"
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
