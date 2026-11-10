# Manual AO-to-textbook linkage — per-row review audit

This document records the per-row manual inspection that produced the review
categorization stored in each linkage row. For every JSS1 Mathematics
curriculum subtopic, it lists:

- the source curriculum objective(s),
- each atomic objective (with bloom verb and level),
- every linked textbook record — its `record_type`, `heading_path`, the
  current placement of the record (shared_foundation, excluded, review_items,
  or attached to an AO with a role), and an evidence quote from the record's
  `content_text` or `prompt_text`,
- the row-level manually authored `review_categories` with their reasons,
- per-atomic-objective `evidence_classification`, AO-level
  `review_categories`, linked record ids with their roles, and the assessment
  status.

Category values come strictly from the manual data stored in each linkage
row JSON file; this document only renders that manual data alongside the
textbook evidence that informed it.

The allowed review categories are:

- `ambiguous_record_scope` — record may support more than one AO, or
  scope/direction is unclear.
- `ao_no_evidence` — an AO has no direct textbook record support.
- `no_reused_assessment` — AO has instruction/practice evidence but no
  reusable `exercise_item` assessment.
- `corpus_gap` — no linked textbook records exist for the subtopic.
- `curriculum_textbook_mismatch` — curriculum AO asks for something the
  textbook section does not cover.
- `prerequisite_only_evidence` — textbook content supports
  prerequisite/foundation knowledge only, not the AO itself.

AO `evidence_classification` is one of `direct`, `prerequisite_only`, or
`none`.

---

## `jss1-math-whole-numbers-millions-and-billions`

**Title:** Millions and billions  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-whole-numbers-millions-and-billions-po01`: Count and write in millions and billions

### Atomic objectives
- `millions-and-billions-ao-count-millions` [count/remember]: Count in millions.
- `millions-and-billions-ao-count-billions` [count/remember]: Count in billions.
- `millions-and-billions-ao-write-millions` [write/remember]: Write in millions.
- `millions-and-billions-ao-write-billions` [write/remember]: Write in billions.

### Linked textbook records (72 total) — inspected
- `ch01-b001` [exposition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small
  - evidence quote: "Last year you learnt how to write and read numbers up to one million. You also counted in millions. In this chapter, you will revise some of last year's work. You will also learn to read, write and count in even larger…"
- `ch01-b002` [exposition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.1 The base ten number system
  - evidence quote: "The most common number system used for everyday counting is the **base ten number system**. It is also called the decimal number system. The number 10 is the base of this number system.  When we count using the base ten…"
- `ch01-b003` [definition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.1 The base ten number system
  - evidence quote: "**base ten number system** The base ten number system is a number system that counts in groups of 10, and uses uses the digits 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 to represent any other number. It is also called the decimal nu…"
- `ch01-b004` [exposition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.1 The base ten number system
  - evidence quote: "In the base ten number system, we go to a new group each time we reach the number 10. The numbers 1 to 9 are called **units**. Zero is used as a placeholder. The number after 9 is 10, which means that we have 1 group of…"
- `ch01-b005` [definition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.1 The base ten number system
  - evidence quote: "**units** Units are the numbers 1; 2; 3; 4; 5; 6; 7; 8; 9 in the base ten number system.  **tens** Tens are the numbers 10; 20; 30; 40; 50; 60; 70; 80; 90 in the base ten number system.  **hundreds** Hundreds are the nu…"
- `ch01-b006` [exposition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.1 The base ten number system > Grouping digits
  - evidence quote: "You may have noticed that we write a thousand as 1,000 rather than 1000. Similarly, we write ten thousand as 10,000 rather than 10000. We use a comma to group the digits. Grouping digits makes it easier to read large nu…"
- `ch01-b007` [exercise_block] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.1 The base ten number system > Exercise 1.1: Group the digits in large numbers
  - evidence quote: "### Exercise 1.1: Group the digits in large numbers  Rewrite each of the following numbers with the digits correctly grouped."
- `ch01-b007-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.1 The base ten number system > Exercise 1.1: Group the digits in large numbers
  - evidence quote: "### Exercise 1.1: Group the digits in large numbers  Rewrite each of the following numbers with the digits correctly grouped.  1. 25618.231"
- `ch01-b007-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.1 The base ten number system > Exercise 1.1: Group the digits in large numbers
  - evidence quote: "### Exercise 1.1: Group the digits in large numbers  Rewrite each of the following numbers with the digits correctly grouped.  2. 100985.0021"
- `ch01-b007-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.1 The base ten number system > Exercise 1.1: Group the digits in large numbers
  - evidence quote: "### Exercise 1.1: Group the digits in large numbers  Rewrite each of the following numbers with the digits correctly grouped.  3. 201050.11"
- `ch01-b007-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.1 The base ten number system > Exercise 1.1: Group the digits in large numbers
  - evidence quote: "### Exercise 1.1: Group the digits in large numbers  Rewrite each of the following numbers with the digits correctly grouped.  4. 5555.55"
- `ch01-b007-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.1 The base ten number system > Exercise 1.1: Group the digits in large numbers
  - evidence quote: "### Exercise 1.1: Group the digits in large numbers  Rewrite each of the following numbers with the digits correctly grouped.  5. 121212.1212"
- `ch01-b008` [note] — placed in **AO:millions-and-billions-ao-write-millions (foundation)**
  - heading: Chapter 1: Numbers big and small > 1.1 The base ten number system > Grouping digits
  - evidence quote: "In some countries, people use spaces instead of commas to group digits. For example, they write the number 504,816 as 504 816. In some countries, they also use a decimal comma instead of a decimal point. For example, th…"
- `ch01-b009` [exposition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Place value in numbers larger than zero
  - evidence quote: "Each digit in a number tells you the specific value of that digit. The **place value** of a digit tells us what the value of that digit is, based on that number's position (place) in the number."
- `ch01-b010` [definition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Place value in numbers larger than zero
  - evidence quote: "**place value** Place value is the value of a digit according to its position in a number."
- `ch01-b011` [worked_example] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Worked example 1.1: Finding the place value of a digit
  - evidence quote: "Give the place value of each digit in the number 52,143."
- `ch01-b012` [exercise_block] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Exercise 1.2: Find the place value of a number
  - evidence quote: "### Exercise 1.2: Find the place value of a number  Use place value tables to determine the place value of the number 6 in each number."
- `ch01-b012-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Exercise 1.2: Find the place value of a number
  - evidence quote: "### Exercise 1.2: Find the place value of a number  Use place value tables to determine the place value of the number 6 in each number.  1. 164"
- `ch01-b012-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Exercise 1.2: Find the place value of a number
  - evidence quote: "### Exercise 1.2: Find the place value of a number  Use place value tables to determine the place value of the number 6 in each number.  2. 1,026"
- `ch01-b012-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Exercise 1.2: Find the place value of a number
  - evidence quote: "### Exercise 1.2: Find the place value of a number  Use place value tables to determine the place value of the number 6 in each number.  3. 68,417"
- `ch01-b012-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Exercise 1.2: Find the place value of a number
  - evidence quote: "### Exercise 1.2: Find the place value of a number  Use place value tables to determine the place value of the number 6 in each number.  4. 13,650"
- `ch01-b012-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Exercise 1.2: Find the place value of a number
  - evidence quote: "### Exercise 1.2: Find the place value of a number  Use place value tables to determine the place value of the number 6 in each number.  5. 26,009"
- `ch01-b022` [exposition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.3 Powers of ten
  - evidence quote: "In the base ten number system, we can use powers of ten to write big numbers, so that they are easier to read and work with. For example, the number 100 is equal to $10\times 10$. This can be written as $10^2$. Here the…"
- `ch01-b023` [note] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.3 Powers of ten
  - evidence quote: "You will learn more about writing numbers in index form in Chapter 2."
- `ch01-b024` [exposition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.3 Powers of ten
  - evidence quote: "The table lists the powers of ten for numbers you have already worked with.  $$ \begin{array}{|l|l|l|}   \hline     \textbf{Name} & \textbf{Number} & \textbf{Powers of ten}  \\     \hline      \text{Ten} & 10 & 10=10^1…"
- `ch01-b029` [exposition] — placed in **AO:millions-and-billions-ao-count-millions (foundation)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Counting up to one million
  - evidence quote: "The number 1,000,000 is named one million. We may write one million as follows: $1,000,000=10\times10\times10\times10\times10\times10=10^6$  Try to imagine how large one million is:  - If you stay awake for 1,000,000 se…"
- `ch01-b030` [exercise_block] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.5: Count to one million in hundred thousands and in ten thousands
  - evidence quote: "### Exercise 1.5: Count to one million in hundred thousands and in ten thousands"
- `ch01-b030-i01` [exercise_item] — placed in **AO:millions-and-billions-ao-count-millions (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.5: Count to one million in hundred thousands and in ten thousands
  - evidence quote: "### Exercise 1.5: Count to one million in hundred thousands and in ten thousands  1. Count aloud from zero to one million in hundred thousands. Then write down the numbers and their names."
- `ch01-b030-i02` [exercise_item] — placed in **AO:millions-and-billions-ao-count-millions (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.5: Count to one million in hundred thousands and in ten thousands
  - evidence quote: "### Exercise 1.5: Count to one million in hundred thousands and in ten thousands  2. Count aloud from nine hundred thousand to one million in ten thousands. Then write down the numbers and their names."
- `ch01-b031` [exposition] — placed in **AO:millions-and-billions-ao-count-millions (instruction)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Counting up to one million
  - evidence quote: "The following counting chart shows you how to count from 990,000 to 1,000,000 in hundreds and in thousands.  ![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-01-005.png)"
- `ch01-b032` [exercise_block] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.6: Count to one million in thousands and in hundreds
  - evidence quote: "### Exercise 1.6: Count to one million in thousands and in hundreds"
- `ch01-b032-i01` [exercise_item] — placed in **AO:millions-and-billions-ao-count-millions (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.6: Count to one million in thousands and in hundreds
  - evidence quote: "### Exercise 1.6: Count to one million in thousands and in hundreds  1. Count aloud from nine hundred and ninety thousand to one million in thousands. Then write down the numbers and their names."
- `ch01-b032-i02` [exercise_item] — placed in **AO:millions-and-billions-ao-count-millions (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.6: Count to one million in thousands and in hundreds
  - evidence quote: "### Exercise 1.6: Count to one million in thousands and in hundreds  2. Count aloud from nine hundred and ninety eight thousand five hundred to one million in hundreds. Then write down the numbers and their names."
- `ch01-b033` [exposition] — placed in **AO:millions-and-billions-ao-count-millions (instruction)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Counting up to one million
  - evidence quote: "This counting chart shows you how to count from 999,900 to 1,000,000 in units and in tens.  ![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-01-006.png)"
- `ch01-b034` [exercise_block] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.7: Count to one million in tens and in units
  - evidence quote: "### Exercise 1.7: Count to one million in tens and in units"
- `ch01-b034-i01` [exercise_item] — placed in **AO:millions-and-billions-ao-count-millions (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.7: Count to one million in tens and in units
  - evidence quote: "### Exercise 1.7: Count to one million in tens and in units  1. Count aloud from nine hundred and ninety nine thousand nine hundred to one million in tens. Then write down the numbers and their names."
- `ch01-b034-i02` [exercise_item] — placed in **AO:millions-and-billions-ao-count-millions (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.7: Count to one million in tens and in units
  - evidence quote: "### Exercise 1.7: Count to one million in tens and in units  2. Count aloud from nine hundred and ninety nine thousand nine hundred and eighty five to one million in units. Then write down the numbers and their names."
- `ch01-b035` [exposition] — placed in **AO:millions-and-billions-ao-count-billions (instruction)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Counting up to one billion
  - evidence quote: "The table in the previous section listed the names of large numbers made up of groups of ten. This table shows how to write numbers as powers of ten.  $$ \begin{array}{|l|l|l|}   \hline     \textbf{Name} & \textbf{Numbe…"
- `ch01-b036` [worked_example] — placed in **AO:millions-and-billions-ao-count-millions (worked_example)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Worked example 1.4: Counting with large numbers
  - evidence quote: "Count in thousands from five hundred and sixty one million seven hundred and twenty one thousand to five hundred and sixty one million seven hundred and thirty two thousand. Write down the numbers and their names."
- `ch01-b037` [exercise_block] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.8: Count with large numbers
  - evidence quote: "### Exercise 1.8: Count with large numbers"
- `ch01-b037-i01` [exercise_item] — placed in **AO:millions-and-billions-ao-count-millions (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.8: Count with large numbers
  - evidence quote: "### Exercise 1.8: Count with large numbers  1. Count in millions from two hundred and sixteen million one hundred and fifty four thousand one hundred to two hundred and twenty one million one hundred and fifty four thou…"
- `ch01-b037-i02` [exercise_item] — placed in **AO:millions-and-billions-ao-count-millions (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.8: Count with large numbers
  - evidence quote: "### Exercise 1.8: Count with large numbers  2. Count in hundred thousands from nine million eight hundred and ninety six thousand five hundred to ten million three hundred and ninety six thousand five hundred. Write dow…"
- `ch01-b037-i03` [exercise_item] — placed in **AO:millions-and-billions-ao-count-millions (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.8: Count with large numbers
  - evidence quote: "### Exercise 1.8: Count with large numbers  3. Count in hundreds from nine hundred and ninety nine million nine hundred and eighty nine thousand seven hundred to nine hundred and ninety nine million nine hundred and nin…"
- `ch01-b038` [exposition] — placed in **AO:millions-and-billions-ao-write-millions (instruction)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Counting in millions and billions
  - evidence quote: "In everyday life, we commonly use a mixture of digits and words to express (read and write) large numbers. For example, most people will find it easier to read 25 billion than 25,000,000,000.  To help us interpret a mix…"
- `ch01-b039` [worked_example] — placed in **AO:millions-and-billions-ao-write-billions (worked_example)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Worked example 1.5: Writing a mixture of digits and words in digits only
  - evidence quote: "Express 0.15 billion in digits only. Write out the full name of the answer."
- `ch01-b040` [exercise_block] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.9: Express a mixture of digits and words in digits only
  - evidence quote: "### Exercise 1.9: Express a mixture of digits and words in digits only"
- `ch01-b040-i01` [exercise_item] — placed in **AO:millions-and-billions-ao-write-millions (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.9: Express a mixture of digits and words in digits only
  - evidence quote: "### Exercise 1.9: Express a mixture of digits and words in digits only  1. Express 0.835 million in digits only, and write out its full name."
- `ch01-b040-i02` [exercise_item] — placed in **AO:millions-and-billions-ao-write-billions (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.9: Express a mixture of digits and words in digits only
  - evidence quote: "### Exercise 1.9: Express a mixture of digits and words in digits only  2. Express 3.45 billion in digits only, and write out its full name."
- `ch01-b040-i03` [exercise_item] — placed in **AO:millions-and-billions-ao-write-millions (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.9: Express a mixture of digits and words in digits only
  - evidence quote: "### Exercise 1.9: Express a mixture of digits and words in digits only  3. Express 20.05 million in digits only, and write out its full name."
- `ch01-b040-i04` [exercise_item] — placed in **AO:millions-and-billions-ao-write-millions (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.9: Express a mixture of digits and words in digits only
  - evidence quote: "### Exercise 1.9: Express a mixture of digits and words in digits only  4. Express 175.5 million in digits only, and write out its full name."
- `ch01-b040-i05` [exercise_item] — placed in **AO:millions-and-billions-ao-write-millions (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.9: Express a mixture of digits and words in digits only
  - evidence quote: "### Exercise 1.9: Express a mixture of digits and words in digits only  5. Express 202.25 million in digits only, and write out its full name."
- `ch01-b041` [exercise_block] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.10: Count in millions and billions
  - evidence quote: "### Exercise 1.10: Count in millions and billions"
- `ch01-b041-i01` [exercise_item] — placed in **AO:millions-and-billions-ao-count-millions (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.10: Count in millions and billions
  - evidence quote: "### Exercise 1.10: Count in millions and billions  1. Count in millions from 1.5 million to 5.5 million. Write down the numbers as digits only and include their full names."
- `ch01-b041-i02` [exercise_item] — placed in **AO:millions-and-billions-ao-count-billions (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.10: Count in millions and billions
  - evidence quote: "### Exercise 1.10: Count in millions and billions  2. Count in 0.5 billions from 10.5 billion to 12 billion. Write down the numbers as digits only and include their full names."
- `ch01-b041-i03` [exercise_item] — placed in **AO:millions-and-billions-ao-count-billions (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.10: Count in millions and billions
  - evidence quote: "### Exercise 1.10: Count in millions and billions  3. Count in 0.25 billions from 25 billion to 26.5 billion. Write down the numbers as digits only and include their full names."
- `ch01-b041-i04` [exercise_item] — placed in **AO:millions-and-billions-ao-count-millions (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.10: Count in millions and billions
  - evidence quote: "### Exercise 1.10: Count in millions and billions  4. Count in 3 millions from 900 million to 912 million. Write down the numbers as digits only and include their full names."
- `ch01-b041-i05` [exercise_item] — placed in **AO:millions-and-billions-ao-count-millions (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.10: Count in millions and billions
  - evidence quote: "### Exercise 1.10: Count in millions and billions  5. Count in 2 millions from 990 million to 1,000 million. Write down the numbers as digits only and include their full names."
- `ch01-b042` [exposition] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Counting in trillions
  - evidence quote: "Our table with powers of ten can be expanded further, to include even larger numbers.  $$ \begin{array}{|l|l|l|}   \hline     \textbf{Name} & \textbf{Number} & \textbf{Powers of ten}  \\     \hline      \text{Ten} & 10…"
- `ch01-b043` [worked_example] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Worked example 1.6: Comparing large numbers
  - evidence quote: "Arrange the following numbers from the smallest to the largest: 50.5 billion; 0.055 trillion; 500.5 million"
- `ch01-b044` [exercise_block] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.11: Compare large numbers
  - evidence quote: "### Exercise 1.11: Compare large numbers"
- `ch01-b044-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.11: Compare large numbers
  - evidence quote: "### Exercise 1.11: Compare large numbers  1. Which number is larger, 0.08 trillion or 800 billion?"
- `ch01-b044-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.11: Compare large numbers
  - evidence quote: "### Exercise 1.11: Compare large numbers  2. Which number is smaller, 120 billion or 1.2 trillion?"
- `ch01-b044-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.11: Compare large numbers
  - evidence quote: "### Exercise 1.11: Compare large numbers  3. Arrange the following numbers from the largest to the smallest: 3,600 million; 3 billion; 0.36 trillion."
- `ch01-b046` [exposition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.6 Using large numbers in everyday life
  - evidence quote: "In your daily life, you may come across large numbers in newspapers, on television shows and in some of your other school subjects.  Whenever you get stuck with a large number, write the number in a place value table to…"
- `ch01-b047` [exercise_block] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.6 Using large numbers in everyday life > Exercise 1.13: Use large numbers to solve problems
  - evidence quote: "### Exercise 1.13: Use large numbers to solve problems"
- `ch01-b047-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.6 Using large numbers in everyday life > Exercise 1.13: Use large numbers to solve problems
  - evidence quote: "### Exercise 1.13: Use large numbers to solve problems  1. Scientists estimate that the average child has $10^5$ hairs on her head.  a. Write out the full number in digits.  b. Give the name of this number."
- `ch01-b047-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.6 Using large numbers in everyday life > Exercise 1.13: Use large numbers to solve problems
  - evidence quote: "### Exercise 1.13: Use large numbers to solve problems  2. During May 2019, Nigeria's population was recorded as 200,233,151.  a. Write the number in words.  b. It is estimated that the population will almost double by…"
- `ch01-b047-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.6 Using large numbers in everyday life > Exercise 1.13: Use large numbers to solve problems
  - evidence quote: "### Exercise 1.13: Use large numbers to solve problems  3. In 2018, the Federal Government of Nigeria estimated a total revenue of ₦6,607,000,000,000.  a. Write the number as a mixture of digits and words, so that it wi…"
- `ch01-b047-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.6 Using large numbers in everyday life > Exercise 1.13: Use large numbers to solve problems
  - evidence quote: "### Exercise 1.13: Use large numbers to solve problems  4. The side length of a cube is 1 m.  a. Convert the side length to centimetres. Then determine the volume of the cube in cubic centimetres. Write the answer in wo…"
- `ch01-b047-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.6 Using large numbers in everyday life > Exercise 1.13: Use large numbers to solve problems
  - evidence quote: "### Exercise 1.13: Use large numbers to solve problems  5. There are 31,536,000 seconds in one year.  a. Calculate the number of seconds in ten years. Write the answer in words.  b. Determine whether your previous answe…"
- `ch01-b047-i06` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.6 Using large numbers in everyday life > Exercise 1.13: Use large numbers to solve problems
  - evidence quote: "### Exercise 1.13: Use large numbers to solve problems  6. In 2018, the Federal Government of Nigeria estimated the following budget allocations to three of their ministries: ₦435.01 billion to Education, ₦444.43 billio…"
- `ch01-b048` [summary] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.7 Summary
  - evidence quote: "- In the base ten number system, we use the digits 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 to represent any other number. - The numbers 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 are called units in the base ten number system. - The numbers 10;…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: 22 linked records (place-value tasks, compare-and-order tasks, trillions extension, applied problem-solving items in ch01-b007-i*, b011, b012-i*, b042, b043, b044-i*, b047-i*) describe sub-skills outside the count/write AOs and are parked in review_items.
- **no_reused_assessment**: Each of the four AOs (count-millions, count-billions, write-millions, write-billions) has record_links but no AO-aligned exercise_item reused as assessment.

### Per-atomic-objective evidence classification
- `millions-and-billions-ao-count-millions` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch01-b029(foundation), ch01-b030-i01(exercise), ch01-b030-i02(exercise), ch01-b031(instruction), ch01-b032-i01(exercise), ch01-b032-i02(exercise), ch01-b033(instruction), ch01-b034-i01(exercise), ch01-b034-i02(exercise), ch01-b036(worked_example), ch01-b037-i01(exercise), ch01-b037-i02(exercise), ch01-b037-i03(exercise), ch01-b041-i01(exercise), ch01-b041-i04(exercise), ch01-b041-i05(exercise)
  - assessment: _(none anchored)_
- `millions-and-billions-ao-count-billions` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch01-b035(instruction), ch01-b041-i02(exercise), ch01-b041-i03(exercise)
  - assessment: _(none anchored)_
- `millions-and-billions-ao-write-millions` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch01-b008(foundation), ch01-b038(instruction), ch01-b040-i01(exercise), ch01-b040-i03(exercise), ch01-b040-i04(exercise), ch01-b040-i05(exercise)
  - assessment: _(none anchored)_
- `millions-and-billions-ao-write-billions` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch01-b039(worked_example), ch01-b040-i02(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All review_items were inspected. Candidate proposals were added for digit grouping, whole-number place value, comparing/ordering large numbers, and solving large-number word problems because those records teach measurable skills outside the current count/write millions-and-billions AOs. The trillions extension record is not proposed as new here because the curriculum already has a separate Trillions subtopic.

### Candidate atomic objective proposals
- `millions-and-billions-candidate-ao-group-digits-large-numbers` [prerequisite; candidate_for_expert_review]
  - proposed objective: Group digits correctly in large numbers.
  - source records: ch01-b007-i01, ch01-b007-i02, ch01-b007-i03, ch01-b007-i04, ch01-b007-i05
  - closest existing AOs: millions-and-billions-ao-write-millions, millions-and-billions-ao-write-billions
  - candidate evidence quote: "Rewrite each of the following numbers with the digits correctly grouped."
  - rationale: Digit grouping is a prerequisite notation skill for reading and writing large numbers, but it is not the same objective as counting or writing specifically in millions and billions.
- `millions-and-billions-candidate-ao-determine-whole-number-place-values` [prerequisite; candidate_for_expert_review]
  - proposed objective: Determine the place values of digits in whole numbers.
  - source records: ch01-b011, ch01-b012-i01, ch01-b012-i02, ch01-b012-i03, ch01-b012-i04, ch01-b012-i05
  - closest existing AOs: millions-and-billions-ao-write-millions, millions-and-billions-ao-write-billions
  - candidate evidence quote: "Give the place value of each digit in the number 52,143."
  - rationale: The records ask learners to identify place values of digits. That supports large-number writing, but it is a distinct measurable skill.
- `millions-and-billions-candidate-ao-compare-and-order-large-numbers` [extension_or_enrichment; candidate_for_expert_review]
  - proposed objective: Compare and order large numbers.
  - source records: ch01-b043, ch01-b044-i01, ch01-b044-i02, ch01-b044-i03
  - closest existing AOs: millions-and-billions-ao-count-millions, millions-and-billions-ao-count-billions
  - candidate evidence quote: "Arrange the following numbers from the smallest to the largest"
  - rationale: The comparison and ordering records require relative-size reasoning with large numbers, not counting or writing them.
- `millions-and-billions-candidate-ao-use-large-numbers-to-solve-problems` [extension_or_enrichment; candidate_for_expert_review]
  - proposed objective: Use large numbers to solve real-world problems.
  - source records: ch01-b047-i01, ch01-b047-i02, ch01-b047-i03, ch01-b047-i04, ch01-b047-i05, ch01-b047-i06
  - closest existing AOs: millions-and-billions-ao-count-millions, millions-and-billions-ao-write-millions, millions-and-billions-ao-write-billions
  - candidate evidence quote: "Use large numbers to solve problems"
  - rationale: The word-problem records apply large numbers in contexts such as population, budgets, measurements, and time. That is broader than the row AOs.

---

## `jss1-math-whole-numbers-trillions`

**Title:** Trillions  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, ao_no_evidence, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-whole-numbers-trillions-po01`: Count and write in trillions
- `jss1-math-whole-numbers-trillions-po02`: Apply the counting, writing, and reading of large numbers in everyday life

### Atomic objectives
- `trillions-ao-count-trillions` [count/remember]: Count in trillions.
- `trillions-ao-write-trillions` [write/remember]: Write in trillions.
- `everyday-life-ao-apply-counting-large-numbers` [apply/apply]: Apply counting of large numbers in everyday life.
- `everyday-life-ao-apply-writing-large-numbers` [apply/apply]: Apply writing of large numbers in everyday life.
- `everyday-life-ao-apply-reading-large-numbers` [apply/apply]: Apply reading of large numbers in everyday life.

### Linked textbook records (43 total) — inspected
- `ch01-b001` [exposition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small
  - evidence quote: "Last year you learnt how to write and read numbers up to one million. You also counted in millions. In this chapter, you will revise some of last year's work. You will also learn to read, write and count in even larger…"
- `ch01-b002` [exposition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.1 The base ten number system
  - evidence quote: "The most common number system used for everyday counting is the **base ten number system**. It is also called the decimal number system. The number 10 is the base of this number system.  When we count using the base ten…"
- `ch01-b003` [definition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.1 The base ten number system
  - evidence quote: "**base ten number system** The base ten number system is a number system that counts in groups of 10, and uses uses the digits 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 to represent any other number. It is also called the decimal nu…"
- `ch01-b004` [exposition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.1 The base ten number system
  - evidence quote: "In the base ten number system, we go to a new group each time we reach the number 10. The numbers 1 to 9 are called **units**. Zero is used as a placeholder. The number after 9 is 10, which means that we have 1 group of…"
- `ch01-b005` [definition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.1 The base ten number system
  - evidence quote: "**units** Units are the numbers 1; 2; 3; 4; 5; 6; 7; 8; 9 in the base ten number system.  **tens** Tens are the numbers 10; 20; 30; 40; 50; 60; 70; 80; 90 in the base ten number system.  **hundreds** Hundreds are the nu…"
- `ch01-b006` [exposition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.1 The base ten number system > Grouping digits
  - evidence quote: "You may have noticed that we write a thousand as 1,000 rather than 1000. Similarly, we write ten thousand as 10,000 rather than 10000. We use a comma to group the digits. Grouping digits makes it easier to read large nu…"
- `ch01-b007` [exercise_block] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.1 The base ten number system > Exercise 1.1: Group the digits in large numbers
  - evidence quote: "### Exercise 1.1: Group the digits in large numbers  Rewrite each of the following numbers with the digits correctly grouped."
- `ch01-b007-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.1 The base ten number system > Exercise 1.1: Group the digits in large numbers
  - evidence quote: "### Exercise 1.1: Group the digits in large numbers  Rewrite each of the following numbers with the digits correctly grouped.  1. 25618.231"
- `ch01-b007-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.1 The base ten number system > Exercise 1.1: Group the digits in large numbers
  - evidence quote: "### Exercise 1.1: Group the digits in large numbers  Rewrite each of the following numbers with the digits correctly grouped.  2. 100985.0021"
- `ch01-b007-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.1 The base ten number system > Exercise 1.1: Group the digits in large numbers
  - evidence quote: "### Exercise 1.1: Group the digits in large numbers  Rewrite each of the following numbers with the digits correctly grouped.  3. 201050.11"
- `ch01-b007-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.1 The base ten number system > Exercise 1.1: Group the digits in large numbers
  - evidence quote: "### Exercise 1.1: Group the digits in large numbers  Rewrite each of the following numbers with the digits correctly grouped.  4. 5555.55"
- `ch01-b007-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.1 The base ten number system > Exercise 1.1: Group the digits in large numbers
  - evidence quote: "### Exercise 1.1: Group the digits in large numbers  Rewrite each of the following numbers with the digits correctly grouped.  5. 121212.1212"
- `ch01-b008` [note] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.1 The base ten number system > Grouping digits
  - evidence quote: "In some countries, people use spaces instead of commas to group digits. For example, they write the number 504,816 as 504 816. In some countries, they also use a decimal comma instead of a decimal point. For example, th…"
- `ch01-b009` [exposition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Place value in numbers larger than zero
  - evidence quote: "Each digit in a number tells you the specific value of that digit. The **place value** of a digit tells us what the value of that digit is, based on that number's position (place) in the number."
- `ch01-b010` [definition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Place value in numbers larger than zero
  - evidence quote: "**place value** Place value is the value of a digit according to its position in a number."
- `ch01-b011` [worked_example] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Worked example 1.1: Finding the place value of a digit
  - evidence quote: "Give the place value of each digit in the number 52,143."
- `ch01-b012` [exercise_block] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Exercise 1.2: Find the place value of a number
  - evidence quote: "### Exercise 1.2: Find the place value of a number  Use place value tables to determine the place value of the number 6 in each number."
- `ch01-b012-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Exercise 1.2: Find the place value of a number
  - evidence quote: "### Exercise 1.2: Find the place value of a number  Use place value tables to determine the place value of the number 6 in each number.  1. 164"
- `ch01-b012-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Exercise 1.2: Find the place value of a number
  - evidence quote: "### Exercise 1.2: Find the place value of a number  Use place value tables to determine the place value of the number 6 in each number.  2. 1,026"
- `ch01-b012-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Exercise 1.2: Find the place value of a number
  - evidence quote: "### Exercise 1.2: Find the place value of a number  Use place value tables to determine the place value of the number 6 in each number.  3. 68,417"
- `ch01-b012-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Exercise 1.2: Find the place value of a number
  - evidence quote: "### Exercise 1.2: Find the place value of a number  Use place value tables to determine the place value of the number 6 in each number.  4. 13,650"
- `ch01-b012-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Exercise 1.2: Find the place value of a number
  - evidence quote: "### Exercise 1.2: Find the place value of a number  Use place value tables to determine the place value of the number 6 in each number.  5. 26,009"
- `ch01-b042` [exposition] — placed in **AO:trillions-ao-count-trillions (instruction)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Counting in trillions
  - evidence quote: "Our table with powers of ten can be expanded further, to include even larger numbers.  $$ \begin{array}{|l|l|l|}   \hline     \textbf{Name} & \textbf{Number} & \textbf{Powers of ten}  \\     \hline      \text{Ten} & 10…"
- `ch01-b043` [worked_example] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Worked example 1.6: Comparing large numbers
  - evidence quote: "Arrange the following numbers from the smallest to the largest: 50.5 billion; 0.055 trillion; 500.5 million"
- `ch01-b044` [exercise_block] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.11: Compare large numbers
  - evidence quote: "### Exercise 1.11: Compare large numbers"
- `ch01-b044-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.11: Compare large numbers
  - evidence quote: "### Exercise 1.11: Compare large numbers  1. Which number is larger, 0.08 trillion or 800 billion?"
- `ch01-b044-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.11: Compare large numbers
  - evidence quote: "### Exercise 1.11: Compare large numbers  2. Which number is smaller, 120 billion or 1.2 trillion?"
- `ch01-b044-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.11: Compare large numbers
  - evidence quote: "### Exercise 1.11: Compare large numbers  3. Arrange the following numbers from the largest to the smallest: 3,600 million; 3 billion; 0.36 trillion."
- `ch01-b045` [exercise_block] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.12: Count in trillions
  - evidence quote: "### Exercise 1.12: Count in trillions"
- `ch01-b045-i01` [exercise_item] — placed in **AO:trillions-ao-count-trillions (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.12: Count in trillions
  - evidence quote: "### Exercise 1.12: Count in trillions  1. Count in trillions from 3.5 trillion to 6.5 trillion. Write down the numbers as digits only and include their full names."
- `ch01-b045-i02` [exercise_item] — placed in **AO:trillions-ao-count-trillions (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.12: Count in trillions
  - evidence quote: "### Exercise 1.12: Count in trillions  2. Count in 0.5 trillions from 37.5 trillion to 40.5 trillion. Write down the numbers as digits only and include their full names."
- `ch01-b045-i03` [exercise_item] — placed in **AO:trillions-ao-count-trillions (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.12: Count in trillions
  - evidence quote: "### Exercise 1.12: Count in trillions  3. Count in 0.25 trillions from 9 trillion to 10.5 trillion. Write down the numbers as digits only and include their full names."
- `ch01-b045-i04` [exercise_item] — placed in **AO:trillions-ao-count-trillions (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.12: Count in trillions
  - evidence quote: "### Exercise 1.12: Count in trillions  4. Count in 3 trillions from 987 trillion to 999 trillion. Write down the numbers as digits only and include their full names."
- `ch01-b045-i05` [exercise_item] — placed in **AO:trillions-ao-count-trillions (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.12: Count in trillions
  - evidence quote: "### Exercise 1.12: Count in trillions  5. Count in 4 trillions from 892 trillion to 908 trillion. Write down the numbers as digits only and include their full names."
- `ch01-b046` [exposition] — placed in **AO:everyday-life-ao-apply-counting-large-numbers (instruction)**
  - heading: Chapter 1: Numbers big and small > 1.6 Using large numbers in everyday life
  - evidence quote: "In your daily life, you may come across large numbers in newspapers, on television shows and in some of your other school subjects.  Whenever you get stuck with a large number, write the number in a place value table to…"
- `ch01-b047` [exercise_block] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.6 Using large numbers in everyday life > Exercise 1.13: Use large numbers to solve problems
  - evidence quote: "### Exercise 1.13: Use large numbers to solve problems"
- `ch01-b047-i01` [exercise_item] — placed in **AO:everyday-life-ao-apply-writing-large-numbers (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.6 Using large numbers in everyday life > Exercise 1.13: Use large numbers to solve problems
  - evidence quote: "### Exercise 1.13: Use large numbers to solve problems  1. Scientists estimate that the average child has $10^5$ hairs on her head.  a. Write out the full number in digits.  b. Give the name of this number."
- `ch01-b047-i02` [exercise_item] — placed in **AO:everyday-life-ao-apply-writing-large-numbers (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.6 Using large numbers in everyday life > Exercise 1.13: Use large numbers to solve problems
  - evidence quote: "### Exercise 1.13: Use large numbers to solve problems  2. During May 2019, Nigeria's population was recorded as 200,233,151.  a. Write the number in words.  b. It is estimated that the population will almost double by…"
- `ch01-b047-i03` [exercise_item] — placed in **AO:everyday-life-ao-apply-writing-large-numbers (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.6 Using large numbers in everyday life > Exercise 1.13: Use large numbers to solve problems
  - evidence quote: "### Exercise 1.13: Use large numbers to solve problems  3. In 2018, the Federal Government of Nigeria estimated a total revenue of ₦6,607,000,000,000.  a. Write the number as a mixture of digits and words, so that it wi…"
- `ch01-b047-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.6 Using large numbers in everyday life > Exercise 1.13: Use large numbers to solve problems
  - evidence quote: "### Exercise 1.13: Use large numbers to solve problems  4. The side length of a cube is 1 m.  a. Convert the side length to centimetres. Then determine the volume of the cube in cubic centimetres. Write the answer in wo…"
- `ch01-b047-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.6 Using large numbers in everyday life > Exercise 1.13: Use large numbers to solve problems
  - evidence quote: "### Exercise 1.13: Use large numbers to solve problems  5. There are 31,536,000 seconds in one year.  a. Calculate the number of seconds in ten years. Write the answer in words.  b. Determine whether your previous answe…"
- `ch01-b047-i06` [exercise_item] — placed in **AO:everyday-life-ao-apply-reading-large-numbers (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.6 Using large numbers in everyday life > Exercise 1.13: Use large numbers to solve problems
  - evidence quote: "### Exercise 1.13: Use large numbers to solve problems  6. In 2018, the Federal Government of Nigeria estimated the following budget allocations to three of their ministries: ₦435.01 billion to Education, ₦444.43 billio…"
- `ch01-b048` [summary] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.7 Summary
  - evidence quote: "- In the base ten number system, we use the digits 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 to represent any other number. - The numbers 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 are called units in the base ten number system. - The numbers 10;…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: 17 records (digit-grouping items at non-trillion magnitudes, place-value worked example/items, comparison/ordering, unit conversion, calculation) are parked in review_items.
- **ao_no_evidence**: trillions-ao-write-trillions has zero record_links; counting exercises (ch01-b045-i*) are heading-tagged as 'count in trillions' and were assigned to the count AO, leaving the write AO unsupported in the linked corpus.
- **no_reused_assessment**: None of the five AOs has an AO-aligned reused exercise_item assessment.

### Per-atomic-objective evidence classification
- `trillions-ao-count-trillions` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch01-b042(instruction), ch01-b045-i01(exercise), ch01-b045-i02(exercise), ch01-b045-i03(exercise), ch01-b045-i04(exercise), ch01-b045-i05(exercise)
  - assessment: _(none anchored)_
- `trillions-ao-write-trillions` → evidence: **none** · categories: ao_no_evidence
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `everyday-life-ao-apply-counting-large-numbers` → evidence: **prerequisite_only** · categories: prerequisite_only_evidence, no_reused_assessment
  - linked records: ch01-b046(instruction)
  - assessment: _(none anchored)_
- `everyday-life-ao-apply-writing-large-numbers` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch01-b047-i01(exercise), ch01-b047-i02(exercise), ch01-b047-i03(exercise)
  - assessment: _(none anchored)_
- `everyday-life-ao-apply-reading-large-numbers` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch01-b047-i06(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All review_items were inspected. Candidate proposals were added for digit grouping, place-value identification, comparing/ordering large numbers, and real-world large-number calculations because these records are measurable textbook skills outside the row AOs for counting/writing/reading/applying trillions.

### Candidate atomic objective proposals
- `trillions-candidate-ao-group-digits-large-numbers` [prerequisite; candidate_for_expert_review]
  - proposed objective: Group digits correctly in large numbers.
  - source records: ch01-b007-i01, ch01-b007-i02, ch01-b007-i03, ch01-b007-i04, ch01-b007-i05
  - closest existing AOs: trillions-ao-write-trillions
  - candidate evidence quote: "Rewrite each of the following numbers with the digits correctly grouped."
  - rationale: Digit grouping is necessary notation for large numbers, but the sampled records are below trillion magnitude and do not directly satisfy writing in trillions.
- `trillions-candidate-ao-determine-whole-number-place-values` [prerequisite; candidate_for_expert_review]
  - proposed objective: Determine the place values of digits in whole numbers.
  - source records: ch01-b011, ch01-b012-i01, ch01-b012-i02, ch01-b012-i03, ch01-b012-i04, ch01-b012-i05
  - closest existing AOs: trillions-ao-write-trillions
  - candidate evidence quote: "Give the place value of each digit in the number 52,143."
  - rationale: Place-value identification is foundational to trillion notation but is not the current count/write/read/apply trillions skill.
- `trillions-candidate-ao-compare-and-order-large-numbers` [extension_or_enrichment; candidate_for_expert_review]
  - proposed objective: Compare and order large numbers.
  - source records: ch01-b043, ch01-b044-i01, ch01-b044-i02, ch01-b044-i03
  - closest existing AOs: everyday-life-ao-apply-counting-large-numbers, everyday-life-ao-apply-reading-large-numbers
  - candidate evidence quote: "Arrange the following numbers from the smallest to the largest"
  - rationale: The records ask learners to compare and order million/billion/trillion quantities, which is a measurable skill not stated by the current AOs.
- `trillions-candidate-ao-solve-large-number-calculation-problems` [extension_or_enrichment; candidate_for_expert_review]
  - proposed objective: Solve real-world calculation problems involving large numbers.
  - source records: ch01-b047-i04, ch01-b047-i05
  - closest existing AOs: everyday-life-ao-apply-counting-large-numbers, everyday-life-ao-apply-writing-large-numbers
  - candidate evidence quote: "There are 31,536,000 seconds in one year."
  - rationale: These records require multi-step calculations with large numbers rather than only reading, writing, or counting them.

---

## `jss1-math-whole-numbers-quantitative-reasoning`

**Title:** Quantitative reasoning  
**Status:** `mapped`  
**Row review categories:** _(none — mapped or no-records baseline)_

### Curriculum objectives (source)
- `jss1-math-whole-numbers-quantitative-reasoning-po01`: Solve problems in quantitative aptitude reasoning using large numbers

### Atomic objectives
- `quantitative-reasoning-ao-solve-large-number-problems` [solve/apply]: Solve problems in quantitative aptitude reasoning using large numbers.

### Linked textbook records (13 total) — inspected
- `ch01-b043` [worked_example] — placed in **AO:quantitative-reasoning-ao-solve-large-number-problems (worked_example)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Worked example 1.6: Comparing large numbers
  - evidence quote: "Arrange the following numbers from the smallest to the largest: 50.5 billion; 0.055 trillion; 500.5 million"
- `ch01-b044` [exercise_block] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.11: Compare large numbers
  - evidence quote: "### Exercise 1.11: Compare large numbers"
- `ch01-b044-i01` [exercise_item] — placed in **AO:quantitative-reasoning-ao-solve-large-number-problems (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.11: Compare large numbers
  - evidence quote: "### Exercise 1.11: Compare large numbers  1. Which number is larger, 0.08 trillion or 800 billion?"
- `ch01-b044-i02` [exercise_item] — placed in **AO:quantitative-reasoning-ao-solve-large-number-problems (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.11: Compare large numbers
  - evidence quote: "### Exercise 1.11: Compare large numbers  2. Which number is smaller, 120 billion or 1.2 trillion?"
- `ch01-b044-i03` [exercise_item] — placed in **AO:quantitative-reasoning-ao-solve-large-number-problems (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.5 Counting in big numbers > Exercise 1.11: Compare large numbers
  - evidence quote: "### Exercise 1.11: Compare large numbers  3. Arrange the following numbers from the largest to the smallest: 3,600 million; 3 billion; 0.36 trillion."
- `ch01-b047` [exercise_block] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.6 Using large numbers in everyday life > Exercise 1.13: Use large numbers to solve problems
  - evidence quote: "### Exercise 1.13: Use large numbers to solve problems"
- `ch01-b047-i01` [exercise_item] — placed in **AO:quantitative-reasoning-ao-solve-large-number-problems (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.6 Using large numbers in everyday life > Exercise 1.13: Use large numbers to solve problems
  - evidence quote: "### Exercise 1.13: Use large numbers to solve problems  1. Scientists estimate that the average child has $10^5$ hairs on her head.  a. Write out the full number in digits.  b. Give the name of this number."
- `ch01-b047-i02` [exercise_item] — placed in **AO:quantitative-reasoning-ao-solve-large-number-problems (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.6 Using large numbers in everyday life > Exercise 1.13: Use large numbers to solve problems
  - evidence quote: "### Exercise 1.13: Use large numbers to solve problems  2. During May 2019, Nigeria's population was recorded as 200,233,151.  a. Write the number in words.  b. It is estimated that the population will almost double by…"
- `ch01-b047-i03` [exercise_item] — placed in **AO:quantitative-reasoning-ao-solve-large-number-problems (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.6 Using large numbers in everyday life > Exercise 1.13: Use large numbers to solve problems
  - evidence quote: "### Exercise 1.13: Use large numbers to solve problems  3. In 2018, the Federal Government of Nigeria estimated a total revenue of ₦6,607,000,000,000.  a. Write the number as a mixture of digits and words, so that it wi…"
- `ch01-b047-i04` [exercise_item] — placed in **AO:quantitative-reasoning-ao-solve-large-number-problems (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.6 Using large numbers in everyday life > Exercise 1.13: Use large numbers to solve problems
  - evidence quote: "### Exercise 1.13: Use large numbers to solve problems  4. The side length of a cube is 1 m.  a. Convert the side length to centimetres. Then determine the volume of the cube in cubic centimetres. Write the answer in wo…"
- `ch01-b047-i05` [exercise_item] — placed in **AO:quantitative-reasoning-ao-solve-large-number-problems (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.6 Using large numbers in everyday life > Exercise 1.13: Use large numbers to solve problems
  - evidence quote: "### Exercise 1.13: Use large numbers to solve problems  5. There are 31,536,000 seconds in one year.  a. Calculate the number of seconds in ten years. Write the answer in words.  b. Determine whether your previous answe…"
- `ch01-b047-i06` [exercise_item] — placed in **AO:quantitative-reasoning-ao-solve-large-number-problems (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.6 Using large numbers in everyday life > Exercise 1.13: Use large numbers to solve problems
  - evidence quote: "### Exercise 1.13: Use large numbers to solve problems  6. In 2018, the Federal Government of Nigeria estimated the following budget allocations to three of their ministries: ₦435.01 billion to Education, ₦444.43 billio…"
- `ch01-b048` [summary] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.7 Summary
  - evidence quote: "- In the base ten number system, we use the digits 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 to represent any other number. - The numbers 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 are called units in the base ten number system. - The numbers 10;…"

### Row-level review categories and manually authored reasons
_None — all AOs have direct evidence and a reused assessment._

### Per-atomic-objective evidence classification
- `quantitative-reasoning-ao-solve-large-number-problems` → evidence: **direct** · categories: —
  - linked records: ch01-b043(worked_example), ch01-b044-i01(exercise), ch01-b044-i02(exercise), ch01-b044-i03(exercise), ch01-b047-i01(exercise), ch01-b047-i02(exercise), ch01-b047-i03(exercise), ch01-b047-i04(exercise), ch01-b047-i05(exercise), ch01-b047-i06(exercise)
  - assessment: reused from `ch01-b044-i03`

---

## `jss1-math-lcm-lcm-of-whole-numbers`

**Title:** LCM of whole numbers  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-lcm-lcm-of-whole-numbers-po01`: Identify common multiples of two or more whole numbers
- `jss1-math-lcm-lcm-of-whole-numbers-po02`: Find the LCM of whole numbers

### Atomic objectives
- `lcm-whole-numbers-ao-identify-common-multiples` [identify/remember]: Identify common multiples of two or more whole numbers.
- `lcm-whole-numbers-ao-find-lcm` [find/apply]: Find the LCM of whole numbers.

### Linked textbook records (40 total) — inspected
- `ch02-b026` [exposition] — placed in **shared_foundation**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Multiples
  - evidence quote: "Natural numbers are the numbers we use for counting. They include all the positive whole numbers from 1 onwards: $1; 2; 3; 4; 5; \ldots$. The multiples of a given number are the numbers you get when you multiply the giv…"
- `ch02-b027` [definition] — placed in **shared_foundation**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Multiples
  - evidence quote: "**multiple** A multiple is a whole number into which a smaller number divides without a remainder."
- `ch02-b028` [exercise_block] — placed in **excluded**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Exercise 2.7: Find multiples
  - evidence quote: "### Exercise 2.7: Find multiples  Write down the first five multiples of the following numbers."
- `ch02-b028-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Exercise 2.7: Find multiples
  - evidence quote: "### Exercise 2.7: Find multiples  1. 8"
- `ch02-b028-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Exercise 2.7: Find multiples
  - evidence quote: "### Exercise 2.7: Find multiples  2. 13"
- `ch02-b028-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Exercise 2.7: Find multiples
  - evidence quote: "### Exercise 2.7: Find multiples  3. 21"
- `ch02-b029` [exposition] — placed in **AO:lcm-whole-numbers-ao-identify-common-multiples (instruction)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Common multiples
  - evidence quote: "A multiple is a number that can be divided by another number without a remainder. Two numbers have a **common multiple** if the same number is a multiple of both those numbers. For example, the number 12 is a common mul…"
- `ch02-b030` [definition] — placed in **AO:lcm-whole-numbers-ao-identify-common-multiples (foundation)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Common multiples
  - evidence quote: "**common multiple** A common multiple is a multiple of two or more numbers."
- `ch02-b031` [worked_example] — placed in **AO:lcm-whole-numbers-ao-identify-common-multiples (worked_example)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Worked example 2.7: Common multiples
  - evidence quote: "Find three common multiples of 5 and 6."
- `ch02-b032` [exercise_block] — placed in **excluded**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Exercise 2.8: Find common multiples
  - evidence quote: "### Exercise 2.8: Find common multiples  Find two common multiples of the following sets of numbers:"
- `ch02-b032-i01` [exercise_item] — placed in **AO:lcm-whole-numbers-ao-identify-common-multiples (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Exercise 2.8: Find common multiples
  - evidence quote: "### Exercise 2.8: Find common multiples  1. 12 and 15"
- `ch02-b032-i02` [exercise_item] — placed in **AO:lcm-whole-numbers-ao-identify-common-multiples (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Exercise 2.8: Find common multiples
  - evidence quote: "### Exercise 2.8: Find common multiples  2. 5, 10 and 15"
- `ch02-b032-i03` [exercise_item] — placed in **AO:lcm-whole-numbers-ao-identify-common-multiples (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Exercise 2.8: Find common multiples
  - evidence quote: "### Exercise 2.8: Find common multiples  3. 2, 4 and 6"
- `ch02-b033` [exposition] — placed in **AO:lcm-whole-numbers-ao-find-lcm (instruction)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Common multiples
  - evidence quote: "The lowest common multiple (LCM) of two numbers is the smallest number that is a multiple of both. For example, the first three common multiples of the numbers 4 and 6 are 12, 24 and 36. The number 12 is the smallest of…"
- `ch02-b034` [definition] — placed in **AO:lcm-whole-numbers-ao-find-lcm (foundation)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Common multiples
  - evidence quote: "lowest common multiple (LCM)  The lowest common multiple is the smallest whole number into which two or more numbers divide without a remainder."
- `ch02-b035` [exercise_block] — placed in **excluded**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Exercise 2.9: Find the LCM
  - evidence quote: "### Exercise 2.9: Find the LCM  In Exercise 2.8, you determined two common multiples of the following sets of numbers. Now identify the LCM in each case."
- `ch02-b035-i01` [exercise_item] — placed in **AO:lcm-whole-numbers-ao-find-lcm (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Exercise 2.9: Find the LCM
  - evidence quote: "### Exercise 2.9: Find the LCM  In Exercise 2.8, you determined two common multiples of the following sets of numbers. Now identify the LCM in each case.  1. 12 and 15"
- `ch02-b035-i02` [exercise_item] — placed in **AO:lcm-whole-numbers-ao-find-lcm (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Exercise 2.9: Find the LCM
  - evidence quote: "### Exercise 2.9: Find the LCM  In Exercise 2.8, you determined two common multiples of the following sets of numbers. Now identify the LCM in each case.  2. 5, 10 and 15"
- `ch02-b035-i03` [exercise_item] — placed in **AO:lcm-whole-numbers-ao-find-lcm (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Exercise 2.9: Find the LCM
  - evidence quote: "### Exercise 2.9: Find the LCM  In Exercise 2.8, you determined two common multiples of the following sets of numbers. Now identify the LCM in each case.  3. 2, 4 and 6"
- `ch02-b036` [worked_example] — placed in **AO:lcm-whole-numbers-ao-find-lcm (worked_example)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Worked example 2.8: LCM using prime factors
  - evidence quote: "Find the LCM of 12 and 18."
- `ch02-b037` [worked_example] — placed in **AO:lcm-whole-numbers-ao-find-lcm (worked_example)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Worked example 2.9: LCM using prime factors in index form
  - evidence quote: "Find the LCM of 60 and 45."
- `ch02-b038` [exercise_block] — placed in **excluded**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Exercise 2.10: Use different methods to find the LCM
  - evidence quote: "### Exercise 2.10: Use different methods to find the LCM"
- `ch02-b038-i01` [exercise_item] — placed in **AO:lcm-whole-numbers-ao-find-lcm (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Exercise 2.10: Use different methods to find the LCM
  - evidence quote: "### Exercise 2.10: Use different methods to find the LCM  1. For the following sets of numbers, use lists of multiples to find the LCM.  6 and 21 4 and 11 7 and 9 2, 3 and 5 6, 10 and 12"
- `ch02-b038-i02` [exercise_item] — placed in **AO:lcm-whole-numbers-ao-find-lcm (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Exercise 2.10: Use different methods to find the LCM
  - evidence quote: "### Exercise 2.10: Use different methods to find the LCM  2. For the following sets of numbers, express each number as a product of prime factors and then find the LCM.  9 and 12 20 and 50 24 and 40 6, 8 and 12 10, 16 a…"
- `ch02-b038-i03` [exercise_item] — placed in **AO:lcm-whole-numbers-ao-find-lcm (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.2 Lowest common multiple > Exercise 2.10: Use different methods to find the LCM
  - evidence quote: "### Exercise 2.10: Use different methods to find the LCM  3. For the following sets of numbers, express each number as a product of prime factors in index form and then find the LCM.  12 and 27 20 and 25 24 and 28 9, 12…"
- `ch02-b039` [exposition] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.3 Compare HCF and LCM
  - evidence quote: "Be careful to not confuse HCF and LCM. The differences are listed in the table.  | HCF (highest common factor) | LCM (lowest common multiple) | | --- | --- | | A factor of two or more numbers | A multiple of two of more…"
- `ch02-b040` [worked_example] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.3 Compare HCF and LCM > Worked example 2.10: HCF and LCM
  - evidence quote: "Find the HCF and the LCM of 24 and 32."
- `ch02-b041` [exercise_block] — placed in **excluded**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.10: Determine HCF and LCM
  - evidence quote: "### Exercise 2.10: Determine HCF and LCM  The prime factorisation of three numbers are as follows:  $2^2 \times 3 \times 5$ $2^3 \times 3 \times 5$ $2^2 \times 3^2 \times 5$"
- `ch02-b041-i01` [exercise_item] — placed in **AO:lcm-whole-numbers-ao-find-lcm (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.10: Determine HCF and LCM
  - evidence quote: "### Exercise 2.10: Determine HCF and LCM  1. Determine the LCM of the three numbers."
- `ch02-b041-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.10: Determine HCF and LCM
  - evidence quote: "### Exercise 2.10: Determine HCF and LCM  2. Determine the HCF of the three numbers."
- `ch02-b041-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.10: Determine HCF and LCM
  - evidence quote: "### Exercise 2.10: Determine HCF and LCM  3. Apart from the HCF, identify another common factor for the three numbers."
- `ch02-b041-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.10: Determine HCF and LCM
  - evidence quote: "### Exercise 2.10: Determine HCF and LCM  4. Calculate the three original numbers."
- `ch02-b042` [exposition] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > 2.4 Practical applications
  - evidence quote: "You can use your knowledge of factors and multiples to solve problems. Here are some hints:  - Decide whether the problem is about factors or multiples. Factors divide into a given number. Multiples are the products of…"
- `ch02-b043` [exercise_block] — placed in **excluded**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.11: Use factors and multiples to solve problems
  - evidence quote: "### Exercise 2.11: Use factors and multiples to solve problems"
- `ch02-b043-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.11: Use factors and multiples to solve problems
  - evidence quote: "### Exercise 2.11: Use factors and multiples to solve problems  1. Chinasa is a student. This year, her age is a multiple of 6. Next year, her age will be a multiple of 5. If Chinasa is younger than 40, how old will she…"
- `ch02-b043-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.11: Use factors and multiples to solve problems
  - evidence quote: "### Exercise 2.11: Use factors and multiples to solve problems  2. Zahrah decides to sell sweets for extra pocket money. She buys a bag of chocolate bars and a bag of toffees. At home, she opens the bags and discovers t…"
- `ch02-b043-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.11: Use factors and multiples to solve problems
  - evidence quote: "### Exercise 2.11: Use factors and multiples to solve problems  3. It is school holidays. Suleiman, Umar and Faruq want to earn some pocket money. They decide to wash cars on the days that they do not have chores to do…"
- `ch02-b043-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.11: Use factors and multiples to solve problems
  - evidence quote: "### Exercise 2.11: Use factors and multiples to solve problems  4. Chika's family has a few dogs and a few chickens. They have a total of 8 animals. The animals have 22 legs altogether. How many dogs and how many chicke…"
- `ch02-b043-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.11: Use factors and multiples to solve problems
  - evidence quote: "### Exercise 2.11: Use factors and multiples to solve problems  5. A class of 26 boys and 39 girls must be divided into small groups for an activity.  a. If the teacher wants equal numbers of boys and girls in each grou…"
- `ch02-b044` [summary] — placed in **excluded**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Summary > 2.4 Summary
  - evidence quote: "- A factor is a whole number that divides into a larger number without a remainder. For example, 4 is a factor of 24. - A prime factor is a factor that is also a prime number. For example, 3 is a prime factor of 24, but…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: 14 records (find-multiples items at the single-number level, mixed HCF/LCM exposition and worked example, individual HCF/factor exercises, applied factor/multiple word problems) are parked in review_items.
- **no_reused_assessment**: Both AOs have record_links but neither has an AO-aligned reused exercise_item assessment.

### Per-atomic-objective evidence classification
- `lcm-whole-numbers-ao-identify-common-multiples` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch02-b029(instruction), ch02-b030(foundation), ch02-b031(worked_example), ch02-b032-i01(exercise), ch02-b032-i02(exercise), ch02-b032-i03(exercise)
  - assessment: _(none anchored)_
- `lcm-whole-numbers-ao-find-lcm` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch02-b033(instruction), ch02-b034(foundation), ch02-b035-i01(exercise), ch02-b035-i02(exercise), ch02-b035-i03(exercise), ch02-b036(worked_example), ch02-b037(worked_example), ch02-b038-i01(exercise), ch02-b038-i02(exercise), ch02-b038-i03(exercise), ch02-b041-i01(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All review_items were inspected. Candidate proposals were added for finding multiples of one number and for factor/multiple word problems. HCF-only records were not proposed here because HCF already has its own curriculum subtopic.

### Candidate atomic objective proposals
- `lcm-whole-numbers-candidate-ao-find-multiples-of-one-number` [prerequisite; candidate_for_expert_review]
  - proposed objective: Find multiples of a given whole number.
  - source records: ch02-b028-i01, ch02-b028-i02, ch02-b028-i03
  - closest existing AOs: lcm-whole-numbers-ao-identify-common-multiples, lcm-whole-numbers-ao-find-lcm
  - candidate evidence quote: "Find multiples"
  - rationale: Finding multiples of one number is prerequisite to common multiples and LCM, but it is a distinct measurable step.
- `lcm-whole-numbers-candidate-ao-solve-factor-multiple-word-problems` [extension_or_enrichment; candidate_for_expert_review]
  - proposed objective: Solve word problems involving factors and multiples.
  - source records: ch02-b042, ch02-b043-i01, ch02-b043-i02, ch02-b043-i03, ch02-b043-i04, ch02-b043-i05
  - closest existing AOs: lcm-whole-numbers-ao-find-lcm
  - candidate evidence quote: "You can use your knowledge of factors and multiples to solve problems."
  - rationale: The word problems require selecting and applying factor/multiple reasoning in context, broader than identifying common multiples or finding LCM procedurally.

---

## `jss1-math-hcf-hcf-of-whole-numbers`

**Title:** HCF of whole numbers  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-hcf-hcf-of-whole-numbers-po01`: Identify common factors of whole numbers
- `jss1-math-hcf-hcf-of-whole-numbers-po02`: Find the HCF of whole numbers

### Atomic objectives
- `hcf-whole-numbers-ao-identify-common-factors` [identify/remember]: Identify common factors of whole numbers.
- `hcf-whole-numbers-ao-find-hcf` [find/apply]: Find the HCF of whole numbers.

### Linked textbook records (34 total) — inspected
- `ch02-b016` [exposition] — placed in **shared_foundation**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Common factors
  - evidence quote: "Two numbers have a common factor if the same number is a factor of both numbers. For example, the number 2 divides into both 10 and 12 without a remainder. Therefore, 2 is a common factor of 10 and 12."
- `ch02-b017` [definition] — placed in **shared_foundation**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Common factors
  - evidence quote: "common factor  A common factor is a factor of two or more numbers."
- `ch02-b018` [worked_example] — placed in **AO:hcf-whole-numbers-ao-identify-common-factors (worked_example)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Worked example 2.4: Common factors
  - evidence quote: "Find the common factors of 12 and 18."
- `ch02-b019` [exercise_block] — placed in **excluded**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.4: Find common factors
  - evidence quote: "### Exercise 2.4: Find common factors  Find the common factors of the following sets of numbers:"
- `ch02-b019-i01` [exercise_item] — placed in **AO:hcf-whole-numbers-ao-identify-common-factors (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.4: Find common factors
  - evidence quote: "### Exercise 2.4: Find common factors  Find the common factors of the following sets of numbers:  1. 15 and 27"
- `ch02-b019-i02` [exercise_item] — placed in **AO:hcf-whole-numbers-ao-identify-common-factors (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.4: Find common factors
  - evidence quote: "### Exercise 2.4: Find common factors  Find the common factors of the following sets of numbers:  2. 30 and 45"
- `ch02-b019-i03` [exercise_item] — placed in **AO:hcf-whole-numbers-ao-identify-common-factors (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.4: Find common factors
  - evidence quote: "### Exercise 2.4: Find common factors  Find the common factors of the following sets of numbers:  3. 10, 20 and 30"
- `ch02-b020` [exposition] — placed in **AO:hcf-whole-numbers-ao-find-hcf (instruction)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Common factors
  - evidence quote: "The highest common factor (HCF) of two numbers is the largest number that is a factor of both. For example, the common factors of 12 and 16 are 1, 2 and 4. The number 4 is the largest number on the list, so it is the hi…"
- `ch02-b021` [definition] — placed in **AO:hcf-whole-numbers-ao-find-hcf (foundation)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Common factors
  - evidence quote: "highest common factor (HCF)  The highest common factor is the largest whole number that divides into two or more numbers without a remainder."
- `ch02-b022` [exercise_block] — placed in **excluded**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.5: Find the HCF
  - evidence quote: "### Exercise 2.5: Find the HCF  In Exercise 2.4, you determined the common factors of the following sets of numbers. Now identify the HCF in each case."
- `ch02-b022-i01` [exercise_item] — placed in **AO:hcf-whole-numbers-ao-find-hcf (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.5: Find the HCF
  - evidence quote: "### Exercise 2.5: Find the HCF  In Exercise 2.4, you determined the common factors of the following sets of numbers. Now identify the HCF in each case.  1. 15 and 27"
- `ch02-b022-i02` [exercise_item] — placed in **AO:hcf-whole-numbers-ao-find-hcf (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.5: Find the HCF
  - evidence quote: "### Exercise 2.5: Find the HCF  In Exercise 2.4, you determined the common factors of the following sets of numbers. Now identify the HCF in each case.  2. 30 and 45"
- `ch02-b022-i03` [exercise_item] — placed in **AO:hcf-whole-numbers-ao-find-hcf (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.5: Find the HCF
  - evidence quote: "### Exercise 2.5: Find the HCF  In Exercise 2.4, you determined the common factors of the following sets of numbers. Now identify the HCF in each case.  3. 10, 20 and 30"
- `ch02-b023` [worked_example] — placed in **AO:hcf-whole-numbers-ao-find-hcf (worked_example)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Worked example 2.5: HCF using prime factors
  - evidence quote: "Find the HCF of 60 and 80."
- `ch02-b024` [worked_example] — placed in **AO:hcf-whole-numbers-ao-find-hcf (worked_example)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Worked example 2.6: HCF using prime factors in index form
  - evidence quote: "Find the HCF of 90 and 108."
- `ch02-b025` [exercise_block] — placed in **excluded**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.6: Use different methods to find the HCF
  - evidence quote: "### Exercise 2.6: Use different methods to find the HCF  For the following sets of numbers, find all the factors of each number and then find the HCF."
- `ch02-b025-i01` [exercise_item] — placed in **AO:hcf-whole-numbers-ao-find-hcf (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.6: Use different methods to find the HCF
  - evidence quote: "### Exercise 2.6: Use different methods to find the HCF  1. For the following sets of numbers, find all the factors of each number and then find the HCF.     1. 15 and 80    2. 40 and 64    3. 50 and 70    4. 18, 24 and…"
- `ch02-b025-i02` [exercise_item] — placed in **AO:hcf-whole-numbers-ao-find-hcf (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.6: Use different methods to find the HCF
  - evidence quote: "### Exercise 2.6: Use different methods to find the HCF  2. For the following sets of numbers, express each number as a product of prime factors and then find the HCF.     1. 39 and 169    2. 45 and 63    3. 144 and 216…"
- `ch02-b025-i03` [exercise_item] — placed in **AO:hcf-whole-numbers-ao-find-hcf (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.6: Use different methods to find the HCF
  - evidence quote: "### Exercise 2.6: Use different methods to find the HCF  3. For the following sets of numbers, express each number as a product of prime factors in index form and then find the HCF.     1. 36 and 120    2. 125 and 300…"
- `ch02-b039` [exposition] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.3 Compare HCF and LCM
  - evidence quote: "Be careful to not confuse HCF and LCM. The differences are listed in the table.  | HCF (highest common factor) | LCM (lowest common multiple) | | --- | --- | | A factor of two or more numbers | A multiple of two of more…"
- `ch02-b040` [worked_example] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.3 Compare HCF and LCM > Worked example 2.10: HCF and LCM
  - evidence quote: "Find the HCF and the LCM of 24 and 32."
- `ch02-b041` [exercise_block] — placed in **excluded**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.10: Determine HCF and LCM
  - evidence quote: "### Exercise 2.10: Determine HCF and LCM  The prime factorisation of three numbers are as follows:  $2^2 \times 3 \times 5$ $2^3 \times 3 \times 5$ $2^2 \times 3^2 \times 5$"
- `ch02-b041-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.10: Determine HCF and LCM
  - evidence quote: "### Exercise 2.10: Determine HCF and LCM  1. Determine the LCM of the three numbers."
- `ch02-b041-i02` [exercise_item] — placed in **AO:hcf-whole-numbers-ao-find-hcf (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.10: Determine HCF and LCM
  - evidence quote: "### Exercise 2.10: Determine HCF and LCM  2. Determine the HCF of the three numbers."
- `ch02-b041-i03` [exercise_item] — placed in **AO:hcf-whole-numbers-ao-identify-common-factors (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.10: Determine HCF and LCM
  - evidence quote: "### Exercise 2.10: Determine HCF and LCM  3. Apart from the HCF, identify another common factor for the three numbers."
- `ch02-b041-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.10: Determine HCF and LCM
  - evidence quote: "### Exercise 2.10: Determine HCF and LCM  4. Calculate the three original numbers."
- `ch02-b042` [exposition] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > 2.4 Practical applications
  - evidence quote: "You can use your knowledge of factors and multiples to solve problems. Here are some hints:  - Decide whether the problem is about factors or multiples. Factors divide into a given number. Multiples are the products of…"
- `ch02-b043` [exercise_block] — placed in **excluded**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.11: Use factors and multiples to solve problems
  - evidence quote: "### Exercise 2.11: Use factors and multiples to solve problems"
- `ch02-b043-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.11: Use factors and multiples to solve problems
  - evidence quote: "### Exercise 2.11: Use factors and multiples to solve problems  1. Chinasa is a student. This year, her age is a multiple of 6. Next year, her age will be a multiple of 5. If Chinasa is younger than 40, how old will she…"
- `ch02-b043-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.11: Use factors and multiples to solve problems
  - evidence quote: "### Exercise 2.11: Use factors and multiples to solve problems  2. Zahrah decides to sell sweets for extra pocket money. She buys a bag of chocolate bars and a bag of toffees. At home, she opens the bags and discovers t…"
- `ch02-b043-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.11: Use factors and multiples to solve problems
  - evidence quote: "### Exercise 2.11: Use factors and multiples to solve problems  3. It is school holidays. Suleiman, Umar and Faruq want to earn some pocket money. They decide to wash cars on the days that they do not have chores to do…"
- `ch02-b043-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.11: Use factors and multiples to solve problems
  - evidence quote: "### Exercise 2.11: Use factors and multiples to solve problems  4. Chika's family has a few dogs and a few chickens. They have a total of 8 animals. The animals have 22 legs altogether. How many dogs and how many chicke…"
- `ch02-b043-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.11: Use factors and multiples to solve problems
  - evidence quote: "### Exercise 2.11: Use factors and multiples to solve problems  5. A class of 26 boys and 39 girls must be divided into small groups for an activity.  a. If the teacher wants equal numbers of boys and girls in each grou…"
- `ch02-b044` [summary] — placed in **excluded**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Summary > 2.4 Summary
  - evidence quote: "- A factor is a whole number that divides into a larger number without a remainder. For example, 4 is a factor of 24. - A prime factor is a factor that is also a prime number. For example, 3 is a prime factor of 24, but…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: 10 records (HCF/LCM comparison, mixed HCF+LCM worked example, individual LCM exercise, original-numbers reconstruction, practical applications and applied word problems) are parked in review_items.
- **no_reused_assessment**: Neither AO has an AO-aligned reused exercise_item assessment.

### Per-atomic-objective evidence classification
- `hcf-whole-numbers-ao-identify-common-factors` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch02-b018(worked_example), ch02-b019-i01(exercise), ch02-b019-i02(exercise), ch02-b019-i03(exercise), ch02-b041-i03(exercise)
  - assessment: _(none anchored)_
- `hcf-whole-numbers-ao-find-hcf` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch02-b020(instruction), ch02-b021(foundation), ch02-b022-i01(exercise), ch02-b022-i02(exercise), ch02-b022-i03(exercise), ch02-b023(worked_example), ch02-b024(worked_example), ch02-b025-i01(exercise), ch02-b025-i02(exercise), ch02-b025-i03(exercise), ch02-b041-i02(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All review_items were inspected. Candidate proposal added for applied factor/multiple word problems. LCM-only records were not proposed as new HCF AOs because LCM already has its own curriculum subtopic.

### Candidate atomic objective proposals
- `hcf-whole-numbers-candidate-ao-solve-factor-multiple-word-problems` [extension_or_enrichment; candidate_for_expert_review]
  - proposed objective: Solve word problems involving factors and multiples.
  - source records: ch02-b042, ch02-b043-i01, ch02-b043-i02, ch02-b043-i03, ch02-b043-i04, ch02-b043-i05
  - closest existing AOs: hcf-whole-numbers-ao-find-hcf
  - candidate evidence quote: "You can use your knowledge of factors and multiples to solve problems."
  - rationale: The word problems require applied reasoning with factors and multiples rather than only identifying common factors or finding HCF procedurally.

---

## `jss1-math-hcf-lcm-and-hcf-of-given-whole-numbers`

**Title:** LCM and HCF of given whole numbers  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-hcf-lcm-and-hcf-of-given-whole-numbers-po01`: Identify the difference between LCM and HCF

### Atomic objectives
- `lcm-and-hcf-ao-identify-difference` [identify/remember]: Identify the difference between LCM and HCF.

### Linked textbook records (8 total) — inspected
- `ch02-b039` [exposition] — placed in **AO:lcm-and-hcf-ao-identify-difference (instruction)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.3 Compare HCF and LCM
  - evidence quote: "Be careful to not confuse HCF and LCM. The differences are listed in the table.  | HCF (highest common factor) | LCM (lowest common multiple) | | --- | --- | | A factor of two or more numbers | A multiple of two of more…"
- `ch02-b040` [worked_example] — placed in **AO:lcm-and-hcf-ao-identify-difference (worked_example)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.3 Compare HCF and LCM > Worked example 2.10: HCF and LCM
  - evidence quote: "Find the HCF and the LCM of 24 and 32."
- `ch02-b041` [exercise_block] — placed in **excluded**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.10: Determine HCF and LCM
  - evidence quote: "### Exercise 2.10: Determine HCF and LCM  The prime factorisation of three numbers are as follows:  $2^2 \times 3 \times 5$ $2^3 \times 3 \times 5$ $2^2 \times 3^2 \times 5$"
- `ch02-b041-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.10: Determine HCF and LCM
  - evidence quote: "### Exercise 2.10: Determine HCF and LCM  1. Determine the LCM of the three numbers."
- `ch02-b041-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.10: Determine HCF and LCM
  - evidence quote: "### Exercise 2.10: Determine HCF and LCM  2. Determine the HCF of the three numbers."
- `ch02-b041-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.10: Determine HCF and LCM
  - evidence quote: "### Exercise 2.10: Determine HCF and LCM  3. Apart from the HCF, identify another common factor for the three numbers."
- `ch02-b041-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.10: Determine HCF and LCM
  - evidence quote: "### Exercise 2.10: Determine HCF and LCM  4. Calculate the three original numbers."
- `ch02-b044` [summary] — placed in **excluded**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Summary > 2.4 Summary
  - evidence quote: "- A factor is a whole number that divides into a larger number without a remainder. For example, 4 is a factor of 24. - A prime factor is a factor that is also a prime number. For example, 3 is a prime factor of 24, but…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: Four ch02-b041 items each compute a single quantity (LCM only, HCF only, another common factor, or reconstruct numbers) and do not directly demonstrate the difference between LCM and HCF.
- **no_reused_assessment**: The single AO has instruction (ch02-b039) and a worked example (ch02-b040) but no exercise_item directly testing the difference between LCM and HCF.

### Per-atomic-objective evidence classification
- `lcm-and-hcf-ao-identify-difference` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch02-b039(instruction), ch02-b040(worked_example)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All review_items were inspected. Candidate proposal added because the row AO only asks students to identify the difference between LCM and HCF, while the exercise records ask them to determine LCM/HCF quantities.

### Candidate atomic objective proposals
- `lcm-and-hcf-candidate-ao-determine-lcm-and-hcf` [missing_direct_objective; candidate_for_expert_review]
  - proposed objective: Determine the LCM and HCF of given whole numbers.
  - source records: ch02-b040, ch02-b041-i01, ch02-b041-i02
  - closest existing AOs: lcm-and-hcf-ao-identify-difference
  - candidate evidence quote: "Determine the LCM of the three numbers."
  - rationale: The records require computing LCM and HCF, which is a measurable objective distinct from explaining the difference between them.

---

## `jss1-math-hcf-quantitative-reasoning`

**Title:** Quantitative reasoning  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-hcf-quantitative-reasoning-po01`: Solve problems on quantitative aptitude involving LCM and HCF of whole numbers

### Atomic objectives
- `hcf-quantitative-reasoning-ao-solve-problems-lcm` [solve/apply]: Solve problems on quantitative aptitude involving LCM of whole numbers.
- `hcf-quantitative-reasoning-ao-solve-problems-hcf` [solve/apply]: Solve problems on quantitative aptitude involving HCF of whole numbers.

### Linked textbook records (7 total) — inspected
- `ch02-b042` [exposition] — placed in **shared_foundation**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > 2.4 Practical applications
  - evidence quote: "You can use your knowledge of factors and multiples to solve problems. Here are some hints:  - Decide whether the problem is about factors or multiples. Factors divide into a given number. Multiples are the products of…"
- `ch02-b043` [exercise_block] — placed in **excluded**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.11: Use factors and multiples to solve problems
  - evidence quote: "### Exercise 2.11: Use factors and multiples to solve problems"
- `ch02-b043-i01` [exercise_item] — placed in **AO:hcf-quantitative-reasoning-ao-solve-problems-lcm (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.11: Use factors and multiples to solve problems
  - evidence quote: "### Exercise 2.11: Use factors and multiples to solve problems  1. Chinasa is a student. This year, her age is a multiple of 6. Next year, her age will be a multiple of 5. If Chinasa is younger than 40, how old will she…"
- `ch02-b043-i02` [exercise_item] — placed in **AO:hcf-quantitative-reasoning-ao-solve-problems-hcf (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.11: Use factors and multiples to solve problems
  - evidence quote: "### Exercise 2.11: Use factors and multiples to solve problems  2. Zahrah decides to sell sweets for extra pocket money. She buys a bag of chocolate bars and a bag of toffees. At home, she opens the bags and discovers t…"
- `ch02-b043-i03` [exercise_item] — placed in **AO:hcf-quantitative-reasoning-ao-solve-problems-lcm (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.11: Use factors and multiples to solve problems
  - evidence quote: "### Exercise 2.11: Use factors and multiples to solve problems  3. It is school holidays. Suleiman, Umar and Faruq want to earn some pocket money. They decide to wash cars on the days that they do not have chores to do…"
- `ch02-b043-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.11: Use factors and multiples to solve problems
  - evidence quote: "### Exercise 2.11: Use factors and multiples to solve problems  4. Chika's family has a few dogs and a few chickens. They have a total of 8 animals. The animals have 22 legs altogether. How many dogs and how many chicke…"
- `ch02-b043-i05` [exercise_item] — placed in **AO:hcf-quantitative-reasoning-ao-solve-problems-hcf (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.4 Lowest common multiple > Exercise 2.11: Use factors and multiples to solve problems
  - evidence quote: "### Exercise 2.11: Use factors and multiples to solve problems  5. A class of 26 boys and 39 girls must be divided into small groups for an activity.  a. If the teacher wants equal numbers of boys and girls in each grou…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch02-b043-i04 is a systematic-listing word problem (animals/legs) whose solution does not invoke LCM or HCF.
- **no_reused_assessment**: Both AOs have direct exercises but no AO-aligned reused assessment was selected.

### Per-atomic-objective evidence classification
- `hcf-quantitative-reasoning-ao-solve-problems-lcm` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch02-b043-i01(exercise), ch02-b043-i03(exercise)
  - assessment: _(none anchored)_
- `hcf-quantitative-reasoning-ao-solve-problems-hcf` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch02-b043-i02(exercise), ch02-b043-i05(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All review_items were inspected. Candidate proposal added for the animal-leg systematic listing problem because its solution does not use LCM or HCF despite being linked to the HCF/LCM QR row.

### Candidate atomic objective proposals
- `hcf-quantitative-reasoning-candidate-ao-solve-systematic-listing-problems` [extension_or_enrichment; candidate_for_expert_review]
  - proposed objective: Solve word problems using systematic listing.
  - source records: ch02-b043-i04
  - closest existing AOs: hcf-quantitative-reasoning-ao-solve-problems-lcm, hcf-quantitative-reasoning-ao-solve-problems-hcf
  - candidate evidence quote: "They have a total of 8 animals."
  - rationale: The record is a constraint/listing problem about animals and legs; it is measurable but not an LCM/HCF quantitative aptitude problem.

---

## `jss1-math-counting-in-base-2-counting-in-groups-of-twos`

**Title:** Counting in groups of twos  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment, curriculum_textbook_mismatch

### Curriculum objectives (source)
- `jss1-math-counting-in-base-2-counting-in-groups-of-twos-po01`: Count in groups of twos

### Atomic objectives
- `counting-in-base-2-ao-count-groups-of-twos` [count/remember]: Count in groups of twos.

### Linked textbook records (33 total) — inspected
- `ch03-b001` [exposition] — placed in **AO:counting-in-base-2-ao-count-groups-of-twos (foundation)**
  - heading: Chapter 3: Binary numbers
  - evidence quote: "In Chapter 1 you learnt that we use the base ten number system for everyday counting. When we count using the base ten number system, we put objects in groups of ten. We use the numbers 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 as d…"
- `ch03-b002` [exposition] — placed in **AO:counting-in-base-2-ao-count-groups-of-twos (instruction)**
  - heading: Chapter 3: Binary numbers > 3.1 The base two number system
  - evidence quote: "In this chapter you will learn about the base two number system. The base two number system is used in computers and other devices that also use computing functions. It is therefore a very important number system.  When…"
- `ch03-b003` [definition] — placed in **AO:counting-in-base-2-ao-count-groups-of-twos (foundation)**
  - heading: Chapter 3: Binary numbers > 3.1 The base two number system
  - evidence quote: "**base ten number system** The base ten number system is a number system that counts in groups of 10, and uses the digits 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 to represent any number. It is also called the decimal number system…"
- `ch03-b004` [exposition] — placed in **AO:counting-in-base-2-ao-count-groups-of-twos (instruction)**
  - heading: Chapter 3: Binary numbers > 3.1 The base two number system > Counting in the base two number system
  - evidence quote: "In the base two number system, we go to a new group each time we reach a number that is a power of 2. We therefore count as follows:  $$ \begin{array}{l l} \circledast & 1 \text{ unit} \\ \color{green}{\circledast \, \c…"
- `ch03-b013` [exposition] — placed in **AO:counting-in-base-2-ao-count-groups-of-twos (instruction)**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers
  - evidence quote: "We can use a place value table to write the numbers 1 to 16 in the decimal number system as binary numbers:  $$ \begin{array}{|c|c|c|c|c||c|c|}  \hline  \text{sixteens} & \text{eights} & \text{fours} & \text{twos} & \te…"
- `ch03-b014` [exposition] — placed in **AO:counting-in-base-2-ao-count-groups-of-twos (foundation)**
  - heading: Chapter 3: Binary numbers > Notation of decimal and binary numbers
  - evidence quote: "When we work with decimal and binary numbers together, we need a way to identify whether a number is a decimal  number or a binary number. For example, the digits 100 represent one hundred objects in the base ten number…"
- `ch03-b015` [worked_example] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Worked example 3.2: Converting binary numbers to decimal numbers
  - evidence quote: "Write  $11010_\text{two}$ as a base ten number."
- `ch03-b016` [exercise_block] — placed in **excluded**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.2: Convert binary numbers to base ten numbers
  - evidence quote: "### Exercise 3.2: Convert binary numbers to base ten numbers  Convert each of the following binary numbers to base ten numbers."
- `ch03-b016-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.2: Convert binary numbers to base ten numbers
  - evidence quote: "### Exercise 3.2: Convert binary numbers to base ten numbers  1. $101_\text{two}$"
- `ch03-b016-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.2: Convert binary numbers to base ten numbers
  - evidence quote: "### Exercise 3.2: Convert binary numbers to base ten numbers  2. $1001_\text{two}$"
- `ch03-b016-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.2: Convert binary numbers to base ten numbers
  - evidence quote: "### Exercise 3.2: Convert binary numbers to base ten numbers  3. $1111_\text{two}$"
- `ch03-b016-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.2: Convert binary numbers to base ten numbers
  - evidence quote: "### Exercise 3.2: Convert binary numbers to base ten numbers  4. $10011_\text{two}$"
- `ch03-b016-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.2: Convert binary numbers to base ten numbers
  - evidence quote: "### Exercise 3.2: Convert binary numbers to base ten numbers  5. $11000_\text{two}$"
- `ch03-b016-i06` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.2: Convert binary numbers to base ten numbers
  - evidence quote: "### Exercise 3.2: Convert binary numbers to base ten numbers  6. $11110_\text{two}$"
- `ch03-b016-i07` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.2: Convert binary numbers to base ten numbers
  - evidence quote: "### Exercise 3.2: Convert binary numbers to base ten numbers  7. $101001_\text{two}$"
- `ch03-b016-i08` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.2: Convert binary numbers to base ten numbers
  - evidence quote: "### Exercise 3.2: Convert binary numbers to base ten numbers  8. $111010_\text{two}$"
- `ch03-b016-i09` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.2: Convert binary numbers to base ten numbers
  - evidence quote: "### Exercise 3.2: Convert binary numbers to base ten numbers  9. $1000111_\text{two}$"
- `ch03-b016-i10` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.2: Convert binary numbers to base ten numbers
  - evidence quote: "### Exercise 3.2: Convert binary numbers to base ten numbers  10. $1010011_\text{two}$"
- `ch03-b017` [worked_example] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Worked example 3.3: Converting decimal numbers to binary numbers
  - evidence quote: "Write  $23_\text{ten}$ as a base two number."
- `ch03-b017-note` [note] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Worked example 3.3: Converting decimal numbers to binary numbers
  - evidence quote: "If you do not feel comfortable with the method explained here, you can write the decimal number as  the sum of powers of 2 and then use a place value table. This is shown in Worked example 3.2."
- `ch03-b018` [exercise_block] — placed in **excluded**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.3: Convert decimal numbers to base two numbers
  - evidence quote: "### Exercise 3.3: Convert decimal numbers to base two numbers  Convert each of the following decimal numbers to base two numbers."
- `ch03-b018-hint` [hint] — placed in **excluded**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.3: Convert decimal numbers to base two numbers
  - evidence quote: "Remember that when you write the remainders, you start from the bottom one and go up to the top one."
- `ch03-b018-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.3: Convert decimal numbers to base two numbers
  - evidence quote: "### Exercise 3.3: Convert decimal numbers to base two numbers  1. $7_\text{ten}$"
- `ch03-b018-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.3: Convert decimal numbers to base two numbers
  - evidence quote: "### Exercise 3.3: Convert decimal numbers to base two numbers  2. $11_\text{ten}$"
- `ch03-b018-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.3: Convert decimal numbers to base two numbers
  - evidence quote: "### Exercise 3.3: Convert decimal numbers to base two numbers  3. $13_\text{ten}$"
- `ch03-b018-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.3: Convert decimal numbers to base two numbers
  - evidence quote: "### Exercise 3.3: Convert decimal numbers to base two numbers  4. $20_\text{ten}$"
- `ch03-b018-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.3: Convert decimal numbers to base two numbers
  - evidence quote: "### Exercise 3.3: Convert decimal numbers to base two numbers  5. $29_\text{ten}$"
- `ch03-b018-i06` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.3: Convert decimal numbers to base two numbers
  - evidence quote: "### Exercise 3.3: Convert decimal numbers to base two numbers  6. $36_\text{ten}$"
- `ch03-b018-i07` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.3: Convert decimal numbers to base two numbers
  - evidence quote: "### Exercise 3.3: Convert decimal numbers to base two numbers  7. $44_\text{ten}$"
- `ch03-b018-i08` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.3: Convert decimal numbers to base two numbers
  - evidence quote: "### Exercise 3.3: Convert decimal numbers to base two numbers  8. $65_\text{ten}$"
- `ch03-b018-i09` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.3: Convert decimal numbers to base two numbers
  - evidence quote: "### Exercise 3.3: Convert decimal numbers to base two numbers  9. $78_\text{ten}$"
- `ch03-b018-i10` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.3: Convert decimal numbers to base two numbers
  - evidence quote: "### Exercise 3.3: Convert decimal numbers to base two numbers  10. $97_\text{ten}$"
- `ch03-b019` [summary] — placed in **excluded**
  - heading: Chapter 3: Binary numbers > 3.5 Summary
  - evidence quote: "- The base two number system is a number system that counts in groups of 2, and uses only the digits 0 and 1 to  represent any number.   - In the base ten number system we work with powers of 10. In the base two number…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: 23 records (binary-to-decimal and decimal-to-binary conversion worked examples and exercises, plus an alternative-method note) are parked in review_items because the subtopic AO is counting in twos, not conversion.
- **no_reused_assessment**: The AO has instructional record_links but no exercise_item directly testing counting in groups of twos.
- **curriculum_textbook_mismatch**: The textbook's chapter 3 binary records emphasise conversion (binary↔decimal), while the AO asks specifically about counting in groups of twos.

### Per-atomic-objective evidence classification
- `counting-in-base-2-ao-count-groups-of-twos` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch03-b001(foundation), ch03-b002(instruction), ch03-b003(foundation), ch03-b004(instruction), ch03-b013(instruction), ch03-b014(foundation)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All review_items were inspected. Candidate proposals were added for both binary-to-base-ten and base-ten-to-binary conversion because the linked textbook section teaches conversion skills beyond counting in groups of twos.

### Candidate atomic objective proposals
- `counting-in-base-2-candidate-ao-convert-binary-to-base-ten` [curriculum_textbook_mismatch; candidate_for_expert_review]
  - proposed objective: Convert binary numbers to base ten numbers.
  - source records: ch03-b015, ch03-b016-i01, ch03-b016-i02, ch03-b016-i03, ch03-b016-i04, ch03-b016-i05, ch03-b016-i06, ch03-b016-i07, ch03-b016-i08, ch03-b016-i09, ch03-b016-i10
  - closest existing AOs: counting-in-base-2-ao-count-groups-of-twos
  - candidate evidence quote: "$11010_\text{two}$ as a base ten number."
  - rationale: These records require converting binary notation into base ten values. That is distinct from counting in groups of twos.
- `counting-in-base-2-candidate-ao-convert-base-ten-to-binary` [curriculum_textbook_mismatch; candidate_for_expert_review]
  - proposed objective: Convert base ten numbers to binary numbers.
  - source records: ch03-b017, ch03-b017-note, ch03-b018-i01, ch03-b018-i02, ch03-b018-i03, ch03-b018-i04, ch03-b018-i05, ch03-b018-i06, ch03-b018-i07, ch03-b018-i08, ch03-b018-i09, ch03-b018-i10
  - closest existing AOs: counting-in-base-2-ao-count-groups-of-twos
  - candidate evidence quote: "$23_\text{ten}$ as a base two number."
  - rationale: These records teach decimal-to-binary conversion, another measurable conversion skill absent from the count-in-groups-of-twos AO.

---

## `jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2`

**Title:** Converting numbers 1-10 to base 2  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-conversion-of-base-10-numerals-to-binary-numbers-converting-numbers-110-to-base-2-po01`: Convert base 10 numerals to binary numbers

### Atomic objectives
- `base-10-to-binary-ao-convert-base-10-to-binary` [convert/apply]: Convert base 10 numerals to binary numbers.

### Linked textbook records (48 total) — inspected
- `ch03-b001` [exposition] — placed in **shared_foundation**
  - heading: Chapter 3: Binary numbers
  - evidence quote: "In Chapter 1 you learnt that we use the base ten number system for everyday counting. When we count using the base ten number system, we put objects in groups of ten. We use the numbers 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 as d…"
- `ch03-b002` [exposition] — placed in **shared_foundation**
  - heading: Chapter 3: Binary numbers > 3.1 The base two number system
  - evidence quote: "In this chapter you will learn about the base two number system. The base two number system is used in computers and other devices that also use computing functions. It is therefore a very important number system.  When…"
- `ch03-b003` [definition] — placed in **shared_foundation**
  - heading: Chapter 3: Binary numbers > 3.1 The base two number system
  - evidence quote: "**base ten number system** The base ten number system is a number system that counts in groups of 10, and uses the digits 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 to represent any number. It is also called the decimal number system…"
- `ch03-b004` [exposition] — placed in **shared_foundation**
  - heading: Chapter 3: Binary numbers > 3.1 The base two number system > Counting in the base two number system
  - evidence quote: "In the base two number system, we go to a new group each time we reach a number that is a power of 2. We therefore count as follows:  $$ \begin{array}{l l} \circledast & 1 \text{ unit} \\ \color{green}{\circledast \, \c…"
- `ch03-b005` [exposition] — placed in **shared_foundation**
  - heading: Chapter 3: Binary numbers > 3.2 Powers of 2
  - evidence quote: "In the base ten number system we work with powers of 10. In the base two number system, we work with powers of 2.  The first ten powers of 2 are:  $$ \begin{array}{|l|r|l|} \hline \textbf{Name} & \textbf{Number} & \text…"
- `ch03-b006` [note] — placed in **shared_foundation**
  - heading: Chapter 3: Binary numbers > 3.2 Powers of 2
  - evidence quote: "Remember that any number to the power of zero is equal to one. Therefore, 2^0=1."
- `ch03-b007` [exposition] — placed in **AO:base-10-to-binary-ao-convert-base-10-to-binary (instruction)**
  - heading: Chapter 3: Binary numbers > 3.2 Powers of 2
  - evidence quote: "To work with binary numbers, you need to be able to write a decimal number as the sum of powers of 2.  Remember that a decimal number is a number that uses the base ten number system. Decimal numbers are the numbers we…"
- `ch03-b008` [worked_example] — placed in **AO:base-10-to-binary-ao-convert-base-10-to-binary (worked_example)**
  - heading: Chapter 3: Binary numbers > 3.2 Powers of 2 > Worked example 3.1: Writing a decimal number as the sum of powers of 2
  - evidence quote: "Write the number 53 as the sum of powers of 2. Then write the number in this base two place value table."
- `ch03-b009` [exposition] — placed in **shared_foundation**
  - heading: Chapter 3: Binary numbers > 3.2 Powers of 2
  - evidence quote: "Here is a table with the powers of 2. You can refer back to it as you answer the questions that follow.  $$ \begin{array}{|c|} \hline 2^0=1 \ \hline 2^1=2 \ \hline 2^2=4 \ \hline 2^3=8 \ \hline 2^4=16 \hline 2^5=32 \ \h…"
- `ch03-b010` [exercise_block] — placed in **excluded**
  - heading: Chapter 3: Binary numbers > 3.2 Powers of 2 > Exercise 3.1: Write decimal numbers as the sum of powers of 2
  - evidence quote: "### Exercise 3.1: Write decimal numbers as the sum of powers of 2  Write each decimal number as the sum of powers of 2. Then write the number in a base two place value table."
- `ch03-b010-i01` [exercise_item] — placed in **AO:base-10-to-binary-ao-convert-base-10-to-binary (exercise)**
  - heading: Chapter 3: Binary numbers > 3.2 Powers of 2 > Exercise 3.1: Write decimal numbers as the sum of powers of 2
  - evidence quote: "### Exercise 3.1: Write decimal numbers as the sum of powers of 2  1. 39"
- `ch03-b010-i02` [exercise_item] — placed in **AO:base-10-to-binary-ao-convert-base-10-to-binary (exercise)**
  - heading: Chapter 3: Binary numbers > 3.2 Powers of 2 > Exercise 3.1: Write decimal numbers as the sum of powers of 2
  - evidence quote: "### Exercise 3.1: Write decimal numbers as the sum of powers of 2  2. 75"
- `ch03-b010-i03` [exercise_item] — placed in **AO:base-10-to-binary-ao-convert-base-10-to-binary (exercise)**
  - heading: Chapter 3: Binary numbers > 3.2 Powers of 2 > Exercise 3.1: Write decimal numbers as the sum of powers of 2
  - evidence quote: "### Exercise 3.1: Write decimal numbers as the sum of powers of 2  3. 120"
- `ch03-b010-i04` [exercise_item] — placed in **AO:base-10-to-binary-ao-convert-base-10-to-binary (exercise)**
  - heading: Chapter 3: Binary numbers > 3.2 Powers of 2 > Exercise 3.1: Write decimal numbers as the sum of powers of 2
  - evidence quote: "### Exercise 3.1: Write decimal numbers as the sum of powers of 2  4. 228"
- `ch03-b010-i05` [exercise_item] — placed in **AO:base-10-to-binary-ao-convert-base-10-to-binary (exercise)**
  - heading: Chapter 3: Binary numbers > 3.2 Powers of 2 > Exercise 3.1: Write decimal numbers as the sum of powers of 2
  - evidence quote: "### Exercise 3.1: Write decimal numbers as the sum of powers of 2  5. 277"
- `ch03-b011` [exposition] — placed in **shared_foundation**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers
  - evidence quote: "The numbers in the base two number system are called binary numbers."
- `ch03-b012` [definition] — placed in **shared_foundation**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers
  - evidence quote: "binary numbers  The numbers in the base two number system are called binary numbers. They are all represented by combinations of the digits 0 and 1."
- `ch03-b013` [exposition] — placed in **shared_foundation**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers
  - evidence quote: "We can use a place value table to write the numbers 1 to 16 in the decimal number system as binary numbers:  $$ \begin{array}{|c|c|c|c|c||c|c|}  \hline  \text{sixteens} & \text{eights} & \text{fours} & \text{twos} & \te…"
- `ch03-b014` [exposition] — placed in **shared_foundation**
  - heading: Chapter 3: Binary numbers > Notation of decimal and binary numbers
  - evidence quote: "When we work with decimal and binary numbers together, we need a way to identify whether a number is a decimal  number or a binary number. For example, the digits 100 represent one hundred objects in the base ten number…"
- `ch03-b015` [worked_example] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Worked example 3.2: Converting binary numbers to decimal numbers
  - evidence quote: "Write  $11010_\text{two}$ as a base ten number."
- `ch03-b016` [exercise_block] — placed in **excluded**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.2: Convert binary numbers to base ten numbers
  - evidence quote: "### Exercise 3.2: Convert binary numbers to base ten numbers  Convert each of the following binary numbers to base ten numbers."
- `ch03-b016-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.2: Convert binary numbers to base ten numbers
  - evidence quote: "### Exercise 3.2: Convert binary numbers to base ten numbers  1. $101_\text{two}$"
- `ch03-b016-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.2: Convert binary numbers to base ten numbers
  - evidence quote: "### Exercise 3.2: Convert binary numbers to base ten numbers  2. $1001_\text{two}$"
- `ch03-b016-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.2: Convert binary numbers to base ten numbers
  - evidence quote: "### Exercise 3.2: Convert binary numbers to base ten numbers  3. $1111_\text{two}$"
- `ch03-b016-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.2: Convert binary numbers to base ten numbers
  - evidence quote: "### Exercise 3.2: Convert binary numbers to base ten numbers  4. $10011_\text{two}$"
- `ch03-b016-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.2: Convert binary numbers to base ten numbers
  - evidence quote: "### Exercise 3.2: Convert binary numbers to base ten numbers  5. $11000_\text{two}$"
- `ch03-b016-i06` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.2: Convert binary numbers to base ten numbers
  - evidence quote: "### Exercise 3.2: Convert binary numbers to base ten numbers  6. $11110_\text{two}$"
- `ch03-b016-i07` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.2: Convert binary numbers to base ten numbers
  - evidence quote: "### Exercise 3.2: Convert binary numbers to base ten numbers  7. $101001_\text{two}$"
- `ch03-b016-i08` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.2: Convert binary numbers to base ten numbers
  - evidence quote: "### Exercise 3.2: Convert binary numbers to base ten numbers  8. $111010_\text{two}$"
- `ch03-b016-i09` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.2: Convert binary numbers to base ten numbers
  - evidence quote: "### Exercise 3.2: Convert binary numbers to base ten numbers  9. $1000111_\text{two}$"
- `ch03-b016-i10` [exercise_item] — placed in **review_items**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.2: Convert binary numbers to base ten numbers
  - evidence quote: "### Exercise 3.2: Convert binary numbers to base ten numbers  10. $1010011_\text{two}$"
- `ch03-b017` [worked_example] — placed in **AO:base-10-to-binary-ao-convert-base-10-to-binary (worked_example)**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Worked example 3.3: Converting decimal numbers to binary numbers
  - evidence quote: "Write  $23_\text{ten}$ as a base two number."
- `ch03-b017-note` [note] — placed in **AO:base-10-to-binary-ao-convert-base-10-to-binary (instruction)**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Worked example 3.3: Converting decimal numbers to binary numbers
  - evidence quote: "If you do not feel comfortable with the method explained here, you can write the decimal number as  the sum of powers of 2 and then use a place value table. This is shown in Worked example 3.2."
- `ch03-b018` [exercise_block] — placed in **excluded**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.3: Convert decimal numbers to base two numbers
  - evidence quote: "### Exercise 3.3: Convert decimal numbers to base two numbers  Convert each of the following decimal numbers to base two numbers."
- `ch03-b018-hint` [hint] — placed in **excluded**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.3: Convert decimal numbers to base two numbers
  - evidence quote: "Remember that when you write the remainders, you start from the bottom one and go up to the top one."
- `ch03-b018-i01` [exercise_item] — placed in **AO:base-10-to-binary-ao-convert-base-10-to-binary (exercise)**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.3: Convert decimal numbers to base two numbers
  - evidence quote: "### Exercise 3.3: Convert decimal numbers to base two numbers  1. $7_\text{ten}$"
- `ch03-b018-i02` [exercise_item] — placed in **AO:base-10-to-binary-ao-convert-base-10-to-binary (exercise)**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.3: Convert decimal numbers to base two numbers
  - evidence quote: "### Exercise 3.3: Convert decimal numbers to base two numbers  2. $11_\text{ten}$"
- `ch03-b018-i03` [exercise_item] — placed in **AO:base-10-to-binary-ao-convert-base-10-to-binary (exercise)**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.3: Convert decimal numbers to base two numbers
  - evidence quote: "### Exercise 3.3: Convert decimal numbers to base two numbers  3. $13_\text{ten}$"
- `ch03-b018-i04` [exercise_item] — placed in **AO:base-10-to-binary-ao-convert-base-10-to-binary (exercise)**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.3: Convert decimal numbers to base two numbers
  - evidence quote: "### Exercise 3.3: Convert decimal numbers to base two numbers  4. $20_\text{ten}$"
- `ch03-b018-i05` [exercise_item] — placed in **AO:base-10-to-binary-ao-convert-base-10-to-binary (exercise)**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.3: Convert decimal numbers to base two numbers
  - evidence quote: "### Exercise 3.3: Convert decimal numbers to base two numbers  5. $29_\text{ten}$"
- `ch03-b018-i06` [exercise_item] — placed in **AO:base-10-to-binary-ao-convert-base-10-to-binary (exercise)**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.3: Convert decimal numbers to base two numbers
  - evidence quote: "### Exercise 3.3: Convert decimal numbers to base two numbers  6. $36_\text{ten}$"
- `ch03-b018-i07` [exercise_item] — placed in **AO:base-10-to-binary-ao-convert-base-10-to-binary (exercise)**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.3: Convert decimal numbers to base two numbers
  - evidence quote: "### Exercise 3.3: Convert decimal numbers to base two numbers  7. $44_\text{ten}$"
- `ch03-b018-i08` [exercise_item] — placed in **AO:base-10-to-binary-ao-convert-base-10-to-binary (exercise)**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.3: Convert decimal numbers to base two numbers
  - evidence quote: "### Exercise 3.3: Convert decimal numbers to base two numbers  8. $65_\text{ten}$"
- `ch03-b018-i09` [exercise_item] — placed in **AO:base-10-to-binary-ao-convert-base-10-to-binary (exercise)**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.3: Convert decimal numbers to base two numbers
  - evidence quote: "### Exercise 3.3: Convert decimal numbers to base two numbers  9. $78_\text{ten}$"
- `ch03-b018-i10` [exercise_item] — placed in **AO:base-10-to-binary-ao-convert-base-10-to-binary (exercise)**
  - heading: Chapter 3: Binary numbers > 3.3 Binary numbers > Exercise 3.3: Convert decimal numbers to base two numbers
  - evidence quote: "### Exercise 3.3: Convert decimal numbers to base two numbers  10. $97_\text{ten}$"
- `ch03-b019` [summary] — placed in **excluded**
  - heading: Chapter 3: Binary numbers > 3.5 Summary
  - evidence quote: "- The base two number system is a number system that counts in groups of 2, and uses only the digits 0 and 1 to  represent any number.   - In the base ten number system we work with powers of 10. In the base two number…"
- `ch08-b001` [exposition] — placed in **shared_foundation**
  - heading: Chapter 8: Operations with binary numbers
  - evidence quote: "In Chapter 3 you learnt about the base two number system. The base two or binary number system counts in groups of 2, and uses only the digits 0 and 1 to represent any number. The numbers in the base two number system a…"
- `ch08-b023` [summary] — placed in **excluded**
  - heading: Chapter 8: Operations with binary numbers > 8.4 Summary
  - evidence quote: "From Chapter 3 you know that: - 2_\text{ten}=10_\text{two} - 3_\text{ten}=11_\text{two}  Use the following basic rules when adding binary numbers: - 0+0=0 - 0+1=1 - 1+0=1 - 1+1=10 - 1+1+1=11  Use the following basic rul…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: 11 records cover the reverse direction (binary→decimal conversion: ch03-b015 worked example and ch03-b016-i01..i10 exercises) and are parked in review_items.
- **no_reused_assessment**: The AO has direct worked examples and exercises but no reused assessment was anchored.

### Per-atomic-objective evidence classification
- `base-10-to-binary-ao-convert-base-10-to-binary` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch03-b007(instruction), ch03-b008(worked_example), ch03-b010-i01(exercise), ch03-b010-i02(exercise), ch03-b010-i03(exercise), ch03-b010-i04(exercise), ch03-b010-i05(exercise), ch03-b017(worked_example), ch03-b017-note(instruction), ch03-b018-i01(exercise), ch03-b018-i02(exercise), ch03-b018-i03(exercise), ch03-b018-i04(exercise), ch03-b018-i05(exercise), ch03-b018-i06(exercise), ch03-b018-i07(exercise), ch03-b018-i08(exercise), ch03-b018-i09(exercise), ch03-b018-i10(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All review_items were inspected. Candidate proposal added for the reverse conversion direction, binary to base ten, because the current AO covers only base-ten-to-binary conversion.

### Candidate atomic objective proposals
- `base-10-to-binary-candidate-ao-convert-binary-to-base-ten` [curriculum_textbook_mismatch; candidate_for_expert_review]
  - proposed objective: Convert binary numbers to base ten numbers.
  - source records: ch03-b015, ch03-b016-i01, ch03-b016-i02, ch03-b016-i03, ch03-b016-i04, ch03-b016-i05, ch03-b016-i06, ch03-b016-i07, ch03-b016-i08, ch03-b016-i09, ch03-b016-i10
  - closest existing AOs: base-10-to-binary-ao-convert-base-10-to-binary
  - candidate evidence quote: "$11010_\text{two}$ as a base ten number."
  - rationale: The records ask for binary-to-base-ten conversion, the reverse of the current row AO.

---

## `jss1-math-fractions-meaning-of-fraction`

**Title:** Meaning of fraction  
**Status:** `needs_review`  
**Row review categories:** no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-fractions-meaning-of-fraction-po01`: Explain the meaning of a fraction
- `jss1-math-fractions-meaning-of-fraction-po02`: Identify parts of a fraction (numerator and denominator)

### Atomic objectives
- `meaning-of-fraction-ao-explain-meaning` [explain/understand]: Explain the meaning of a fraction.
- `meaning-of-fraction-ao-identify-numerator` [identify/remember]: Identify the numerator of a fraction.
- `meaning-of-fraction-ao-identify-denominator` [identify/remember]: Identify the denominator of a fraction.

### Linked textbook records (5 total) — inspected
- `ch01-b013` [exposition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Place value in decimal fractions
  - evidence quote: "A fraction means a part of a whole. One way to write a fraction is to write one whole number on top of another whole number with a dividing line between them. For example, $\frac{2}{10}$ means two parts of a whole that…"
- `ch04-b001` [exposition] — placed in **shared_foundation**
  - heading: Chapter 4: Equivalent fractions > 4.1 Types of fractions
  - evidence quote: "A fraction is part of a whole. There are different ways to write fractions. One way is to write the fraction as one whole number on top of another whole number with a dividing line between, as $\frac{\text{numerator}}{\…"
- `ch04-b002` [definition] — placed in **shared_foundation**
  - heading: Chapter 4: Equivalent fractions > 4.1 Types of fractions > 4.1 Types of fractions
  - evidence quote: "**fraction** A fraction is a part of a whole.  **denominator** The denominator is the number written below the line in a fraction; it represents all the parts of a whole.  **numerator** The numerator is the number writt…"
- `ch04-b003` [exposition] — placed in **AO:meaning-of-fraction-ao-explain-meaning (instruction)**
  - heading: Chapter 4: Equivalent fractions > 4.1 Types of fractions > 4.1 Types of fractions
  - evidence quote: "For example, if you cut a cake into seven pieces, you can say that the whole cake is made up of $\frac{7}{7}$.  ![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-001.png…"
- `ch04-b058` [summary] — placed in **excluded**
  - heading: Chapter 4: Equivalent fractions > 4.7 Summary
  - evidence quote: "- A common fraction is written as $\frac{\text{numerator}}{\text{denominator}}$. - A proper fraction is smaller than 1, for example $\frac{2}{7}$. - A mixed number consists of a whole number and a proper fraction, for e…"

### Row-level review categories and manually authored reasons
- **no_reused_assessment**: All three AOs are directly supported by shared_foundation records ch04-b001 (general meaning), ch04-b002 (definitions of numerator and denominator), and ch01-b013 (fraction as part of a whole), plus ch04-b003 (cake example) attached to explain-meaning. However the linked corpus has no exercise_item that asks the student to identify a numerator or denominator, or to explain the meaning, so no AO-aligned reused assessment is available.

### Per-atomic-objective evidence classification
- `meaning-of-fraction-ao-explain-meaning` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch04-b003(instruction)
  - assessment: _(none anchored)_
- `meaning-of-fraction-ao-identify-numerator` → evidence: **direct** · categories: no_reused_assessment
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `meaning-of-fraction-ao-identify-denominator` → evidence: **direct** · categories: no_reused_assessment
  - linked records: _(none)_
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-fractions-types-of-fractions`

**Title:** Types of fractions (proper and improper fractions)  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-fractions-types-of-fractions-po01`: Distinguish between proper and improper fractions
- `jss1-math-fractions-types-of-fractions-po02`: Classify given fractions as proper or improper

### Atomic objectives
- `types-of-fractions-ao-distinguish-proper-and-improper` [distinguish/understand]: Distinguish between proper and improper fractions.
- `types-of-fractions-ao-classify-proper-or-improper` [classify/understand]: Classify given fractions as proper or improper.

### Linked textbook records (13 total) — inspected
- `ch04-b004` [definition] — placed in **shared_foundation**
  - heading: Chapter 4: Equivalent fractions > 4.1 Types of fractions > 4.1 Types of fractions
  - evidence quote: "**proper fraction** A proper fraction is a fraction that is smaller than 1, so the numerator is smaller than the denominator."
- `ch04-b005` [exercise_block] — placed in **excluded**
  - heading: Chapter 4: Equivalent fractions > 4.1 Types of fractions > Exercise 4.1: Write proper fractions from diagrams
  - evidence quote: "### Exercise 4.1: Write proper fractions from diagrams  For each diagram, express the shaded part as a proper fraction."
- `ch04-b005-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 4: Equivalent fractions > 4.1 Types of fractions > Exercise 4.1: Write proper fractions from diagrams
  - evidence quote: "### Exercise 4.1: Write proper fractions from diagrams  For each diagram, express the shaded part as a proper fraction.  1. ![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss…"
- `ch04-b005-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 4: Equivalent fractions > 4.1 Types of fractions > Exercise 4.1: Write proper fractions from diagrams
  - evidence quote: "### Exercise 4.1: Write proper fractions from diagrams  For each diagram, express the shaded part as a proper fraction.  2. ![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss…"
- `ch04-b005-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 4: Equivalent fractions > 4.1 Types of fractions > Exercise 4.1: Write proper fractions from diagrams
  - evidence quote: "### Exercise 4.1: Write proper fractions from diagrams  For each diagram, express the shaded part as a proper fraction.  3. ![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss…"
- `ch04-b005-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 4: Equivalent fractions > 4.1 Types of fractions > Exercise 4.1: Write proper fractions from diagrams
  - evidence quote: "### Exercise 4.1: Write proper fractions from diagrams  For each diagram, express the shaded part as a proper fraction.  4. ![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss…"
- `ch04-b005-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 4: Equivalent fractions > 4.1 Types of fractions > Exercise 4.1: Write proper fractions from diagrams
  - evidence quote: "### Exercise 4.1: Write proper fractions from diagrams  For each diagram, express the shaded part as a proper fraction.  5. ![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss…"
- `ch04-b005-i06` [exercise_item] — placed in **review_items**
  - heading: Chapter 4: Equivalent fractions > 4.1 Types of fractions > Exercise 4.1: Write proper fractions from diagrams
  - evidence quote: "### Exercise 4.1: Write proper fractions from diagrams  For each diagram, express the shaded part as a proper fraction.  6. ![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss…"
- `ch04-b005-i07` [exercise_item] — placed in **review_items**
  - heading: Chapter 4: Equivalent fractions > 4.1 Types of fractions > Exercise 4.1: Write proper fractions from diagrams
  - evidence quote: "### Exercise 4.1: Write proper fractions from diagrams  For each diagram, express the shaded part as a proper fraction.  7. ![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss…"
- `ch04-b005-i08` [exercise_item] — placed in **review_items**
  - heading: Chapter 4: Equivalent fractions > 4.1 Types of fractions > Exercise 4.1: Write proper fractions from diagrams
  - evidence quote: "### Exercise 4.1: Write proper fractions from diagrams  For each diagram, express the shaded part as a proper fraction.  8. ![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss…"
- `ch04-b008` [exposition] — placed in **shared_foundation**
  - heading: Chapter 4: Equivalent fractions > 4.1 Types of fractions > 4.1 Types of fractions
  - evidence quote: "A mixed number may be expressed as an **improper fraction**. An improper fraction is larger than 1. Its numerator is larger than its denominator. Suppose we cut the two whole apples shown above into halves as well. We w…"
- `ch04-b009` [definition] — placed in **shared_foundation**
  - heading: Chapter 4: Equivalent fractions > 4.1 Types of fractions > 4.1 Types of fractions
  - evidence quote: "**improper fraction** An improper fraction is a fraction that is larger than 1, so the numerator is larger than the denominator."
- `ch04-b058` [summary] — placed in **excluded**
  - heading: Chapter 4: Equivalent fractions > 4.7 Summary
  - evidence quote: "- A common fraction is written as $\frac{\text{numerator}}{\text{denominator}}$. - A proper fraction is smaller than 1, for example $\frac{2}{7}$. - A mixed number consists of a whole number and a proper fraction, for e…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch04-b005-i01..i08 ask the student to express a shaded diagram region as a proper fraction (the items are pre-labelled as proper). They produce a fraction rather than distinguish or classify proper vs improper, so the AO match is uncertain.
- **no_reused_assessment**: Both AOs are directly grounded by the shared_foundation definitions (ch04-b004 proper, ch04-b009 improper) and the contrasting exposition ch04-b008, but the linked corpus has no exercise_item that asks the student to distinguish or classify proper vs improper, so no AO-aligned reused assessment is available.

### Per-atomic-objective evidence classification
- `types-of-fractions-ao-distinguish-proper-and-improper` → evidence: **direct** · categories: no_reused_assessment
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `types-of-fractions-ao-classify-proper-or-improper` → evidence: **direct** · categories: no_reused_assessment
  - linked records: _(none)_
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All review_items were inspected. Candidate proposal added because the diagram records ask learners to write proper fractions from shaded regions, not to distinguish or classify proper versus improper fractions.

### Candidate atomic objective proposals
- `types-of-fractions-candidate-ao-write-proper-fractions-from-diagrams` [missing_direct_objective; candidate_for_expert_review]
  - proposed objective: Write proper fractions from diagrams.
  - source records: ch04-b005-i01, ch04-b005-i02, ch04-b005-i03, ch04-b005-i04, ch04-b005-i05, ch04-b005-i06, ch04-b005-i07, ch04-b005-i08
  - closest existing AOs: types-of-fractions-ao-distinguish-proper-and-improper, types-of-fractions-ao-classify-proper-or-improper
  - candidate evidence quote: "express the shaded part as a proper fraction."
  - rationale: The records require producing fractions from diagrams. That is measurable and related, but not the same as classifying fraction types.

---

## `jss1-math-fractions-mixed-fractions`

**Title:** Mixed fractions  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-fractions-mixed-fractions-po01`: Convert improper fractions to mixed fractions and vice versa

### Atomic objectives
- `mixed-fractions-ao-convert-improper-to-mixed` [convert/apply]: Convert improper fractions to mixed fractions.
- `mixed-fractions-ao-convert-mixed-to-improper` [convert/apply]: Convert mixed fractions to improper fractions.

### Linked textbook records (22 total) — inspected
- `ch04-b006` [exposition] — placed in **shared_foundation**
  - heading: Chapter 4: Equivalent fractions > 4.1 Types of fractions > 4.1 Types of fractions
  - evidence quote: "A **mixed number** is made up of a whole number and a proper fraction. For example, $2\frac{1}{2}$ apples mean you have two whole apples and one half of another apple.  ![](https://electricbookworks.github.io/siyavula-o…"
- `ch04-b007` [definition] — placed in **shared_foundation**
  - heading: Chapter 4: Equivalent fractions > 4.1 Types of fractions > 4.1 Types of fractions
  - evidence quote: "**mixed number** A mixed number is a number that is made up of a whole number and a proper fraction."
- `ch04-b008` [exposition] — placed in **shared_foundation**
  - heading: Chapter 4: Equivalent fractions > 4.1 Types of fractions > 4.1 Types of fractions
  - evidence quote: "A mixed number may be expressed as an **improper fraction**. An improper fraction is larger than 1. Its numerator is larger than its denominator. Suppose we cut the two whole apples shown above into halves as well. We w…"
- `ch04-b009` [definition] — placed in **shared_foundation**
  - heading: Chapter 4: Equivalent fractions > 4.1 Types of fractions > 4.1 Types of fractions
  - evidence quote: "**improper fraction** An improper fraction is a fraction that is larger than 1, so the numerator is larger than the denominator."
- `ch04-b010` [worked_example] — placed in **AO:mixed-fractions-ao-convert-mixed-to-improper (worked_example)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions > Worked example 4.1: Expressing mixed numbers as improper fractions
  - evidence quote: "Write $5\frac{3}{4}$ as an improper fraction."
- `ch04-b011` [worked_example] — placed in **AO:mixed-fractions-ao-convert-improper-to-mixed (worked_example)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions > Worked example 4.2: Expressing improper fractions as mixed numbers
  - evidence quote: "Write $\frac{26}{3}$ as a mixed number."
- `ch04-b012` [exercise_block] — placed in **excluded**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions > Exercise 4.2: Convert between mixed numbers and improper fractions
  - evidence quote: "### Exercise 4.2: Convert between mixed numbers and improper fractions"
- `ch04-b012-i01` [exercise_item] — placed in **AO:mixed-fractions-ao-convert-mixed-to-improper (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions > Exercise 4.2: Convert between mixed numbers and improper fractions
  - evidence quote: "### Exercise 4.2: Convert between mixed numbers and improper fractions  1. Express the following mixed numbers as improper fractions.     1. $6\frac{3}{7}$    2. $2\frac{5}{11}$    3. $13\frac{2}{3}$"
- `ch04-b012-i02` [exercise_item] — placed in **AO:mixed-fractions-ao-convert-improper-to-mixed (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions > Exercise 4.2: Convert between mixed numbers and improper fractions
  - evidence quote: "### Exercise 4.2: Convert between mixed numbers and improper fractions  2. Express the following improper fractions as mixed numbers.     1. $\frac{30}{7}$    2. $\frac{112}{9}$    3. $\frac{85}{11}$"
- `ch04-b013` [note] — placed in **AO:mixed-fractions-ao-convert-mixed-to-improper (instruction)**
  - heading: Chapter 4: Equivalent fractions > 4.1 Types of fractions
  - evidence quote: "Once you understand how to express a mixed number as an improper fraction, you may use this short method. Example: 3\frac{3}{5}. Denominator: \frac{\phantom{00}}{5}. Numerator: (5\times3)+3=18. Answer: \frac{18}{5}."
- `ch04-b057-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 4: Equivalent fractions > 4.6 Practical applications > Exercise 4.12: Use equivalent fractions to solve problems
  - evidence quote: "### Exercise 4.12: Use equivalent fractions to solve problems  2. After a birthday party, $2\frac{2}{5}$ cakes are left over. If the leftover cake is cut into equal pieces, how many people could get one piece each?"
- `ch04-b058` [summary] — placed in **excluded**
  - heading: Chapter 4: Equivalent fractions > 4.7 Summary
  - evidence quote: "- A common fraction is written as $\frac{\text{numerator}}{\text{denominator}}$. - A proper fraction is smaller than 1, for example $\frac{2}{7}$. - A mixed number consists of a whole number and a proper fraction, for e…"
- `ch06-b048` [note] — placed in **excluded**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Multiplying and dividing mixed numbers
  - evidence quote: "If necessary, go back to Chapter 4 and revise how to convert mixed numbers to improper fractions."
- `ch06-b050` [worked_example] — placed in **review_items**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Worked example 6.16: Dividing mixed numbers
  - evidence quote: "Calculate:  $$2\frac{5}{8}\div3\frac{3}{4}$$"
- `ch06-b051` [note] — placed in **excluded**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Simplifying before multiplying
  - evidence quote: "If necessary, go back to Chapter 4 and revise how to convert improper fractions to mixed numbers."
- `ch06-b052` [exercise_block] — placed in **excluded**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Exercise 6.9: Multiply and divide mixed numbers
  - evidence quote: "### Exercise 6.9: Multiply and divide mixed numbers"
- `ch06-b052-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Exercise 6.9: Multiply and divide mixed numbers
  - evidence quote: "### Exercise 6.9: Multiply and divide mixed numbers  1. $5\frac{1}{3}\times2\frac{3}{4}$"
- `ch06-b052-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Exercise 6.9: Multiply and divide mixed numbers
  - evidence quote: "### Exercise 6.9: Multiply and divide mixed numbers  2. $3\frac{3}{5}\times1\frac{6}{9}$"
- `ch06-b052-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Exercise 6.9: Multiply and divide mixed numbers
  - evidence quote: "### Exercise 6.9: Multiply and divide mixed numbers  3. $7\frac{1}{8}\div4\frac{3}{4}$"
- `ch06-b052-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Exercise 6.9: Multiply and divide mixed numbers
  - evidence quote: "### Exercise 6.9: Multiply and divide mixed numbers  4. $4\frac{1}{6}\div3\frac{8}{9}$"
- `ch06-b052-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Exercise 6.9: Multiply and divide mixed numbers
  - evidence quote: "### Exercise 6.9: Multiply and divide mixed numbers  5. $6\frac{3}{10}\div1\frac{4}{5}$"
- `ch06-b054-i10` [exercise_item] — placed in **review_items**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications > Exercise 6.10: Use operations with fractions to solve problems
  - evidence quote: "### Exercise 6.10: Use operations with fractions to solve problems  10. A bag of garri has a mass of $10\frac{5}{6}$ kg. How many small packets, each with a mass of $2\frac{1}{2}$ kg, can be made up from the bag?"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: Eight records (ch04-b057-i02 applied word problem, ch06-b050 division worked example, ch06-b052-i01..i05 mult/div mixed-number items, ch06-b054-i10 applied word problem) describe operations beyond conversion between mixed and improper.
- **no_reused_assessment**: Both conversion AOs have a worked example and one direct exercise each but no reused assessment was anchored.

### Per-atomic-objective evidence classification
- `mixed-fractions-ao-convert-improper-to-mixed` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch04-b011(worked_example), ch04-b012-i02(exercise)
  - assessment: _(none anchored)_
- `mixed-fractions-ao-convert-mixed-to-improper` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch04-b010(worked_example), ch04-b012-i01(exercise), ch04-b013(instruction)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All review_items were inspected. Candidate proposal added for mixed-number multiplication/division records. Equivalent-fraction word-problem records were not proposed here because they belong to the equivalent-fractions subtopic.

### Candidate atomic objective proposals
- `mixed-fractions-candidate-ao-multiply-and-divide-mixed-numbers` [extension_or_enrichment; candidate_for_expert_review]
  - proposed objective: Multiply and divide mixed numbers.
  - source records: ch06-b050, ch06-b052-i01, ch06-b052-i02, ch06-b052-i03, ch06-b052-i04, ch06-b052-i05
  - closest existing AOs: mixed-fractions-ao-convert-improper-to-mixed, mixed-fractions-ao-convert-mixed-to-improper
  - candidate evidence quote: "Calculate:"
  - rationale: The records use mixed-number conversion as part of multiplication/division, but the primary skill is operating on mixed numbers rather than converting between forms.

---

## `jss1-math-fractions-equivalent-fractions`

**Title:** Equivalent fractions  
**Status:** `needs_review`  
**Row review categories:** prerequisite_only_evidence, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-fractions-equivalent-fractions-po01`: Identify equivalent fractions
- `jss1-math-fractions-equivalent-fractions-po02`: Find the equivalence of any given fraction using a formula
- `jss1-math-fractions-equivalent-fractions-po03`: Apply equivalent fractions in sharing commodities

### Atomic objectives
- `equivalent-fractions-ao-identify-equivalent-fractions` [identify/remember]: Identify equivalent fractions.
- `equivalent-fractions-ao-find-equivalence-using-formula` [find/apply]: Find the equivalence of any given fraction using a formula.
- `equivalent-fractions-ao-apply-in-sharing-commodities` [apply/apply]: Apply equivalent fractions in sharing commodities.

### Linked textbook records (29 total) — inspected
- `ch04-b014` [exposition] — placed in **shared_foundation**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions
  - evidence quote: "Fractions that represent the same part of a whole in different ways are called equivalent fractions. Look at the three diagrams below. The fraction of the rectangle that is shaded is given next to each diagram.  All thr…"
- `ch04-b015` [definition] — placed in **shared_foundation**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions
  - evidence quote: "equivalent fractions  Equivalent fractions are fractions that have different numerators and denominators, but they represent the same part of a whole, and they have the same value."
- `ch04-b016` [exposition] — placed in **AO:equivalent-fractions-ao-find-equivalence-using-formula (instruction)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions
  - evidence quote: "We find equivalent fractions by multiplying or dividing the numerator and the denominator by the same whole number."
- `ch04-b017` [worked_example] — placed in **AO:equivalent-fractions-ao-find-equivalence-using-formula (worked_example)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions > Worked example 4.3: Working out equivalent fractions
  - evidence quote: "Find the missing numbers in these equivalent fractions:  $$ \frac{3}{4}=\frac{\square}{16}=\frac{6}{\square}=\frac{15}{\square} $$"
- `ch04-b018` [exposition] — placed in **AO:equivalent-fractions-ao-find-equivalence-using-formula (foundation)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions > Find equivalent fractions
  - evidence quote: "Improper fractions can also have equivalent fractions. Earlier on in this chapter, we showed that $2\frac{1}{2}$ apples is equal to $\frac{5}{2}$ apples. The improper fraction $\frac{5}{2}$ tells us that we are dealing…"
- `ch04-b019` [exercise_block] — placed in **excluded**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions > Exercise 4.3: Determine equivalent fractions
  - evidence quote: "### Exercise 4.3: Determine equivalent fractions  Find the missing numbers in each list of equivalent fractions."
- `ch04-b019-i01` [exercise_item] — placed in **AO:equivalent-fractions-ao-find-equivalence-using-formula (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions > Exercise 4.3: Determine equivalent fractions
  - evidence quote: "### Exercise 4.3: Determine equivalent fractions  Find the missing numbers in each list of equivalent fractions.  1. $$ \frac{3}{7}=\frac{\square}{42}=\frac{9}{\square}=\frac{6}{\square} $$"
- `ch04-b019-i02` [exercise_item] — placed in **AO:equivalent-fractions-ao-find-equivalence-using-formula (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions > Exercise 4.3: Determine equivalent fractions
  - evidence quote: "### Exercise 4.3: Determine equivalent fractions  Find the missing numbers in each list of equivalent fractions.  2. $$ \frac{2}{5}=\frac{\square}{15}=\frac{8}{\square}=\frac{\square}{250} $$"
- `ch04-b019-i03` [exercise_item] — placed in **AO:equivalent-fractions-ao-find-equivalence-using-formula (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions > Exercise 4.3: Determine equivalent fractions
  - evidence quote: "### Exercise 4.3: Determine equivalent fractions  Find the missing numbers in each list of equivalent fractions.  3. $$ \frac{\square}{6}=\frac{5}{30}=\frac{15}{\square}=\frac{\square}{12} $$"
- `ch04-b019-i04` [exercise_item] — placed in **AO:equivalent-fractions-ao-find-equivalence-using-formula (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions > Exercise 4.3: Determine equivalent fractions
  - evidence quote: "### Exercise 4.3: Determine equivalent fractions  Find the missing numbers in each list of equivalent fractions.  4. $$ \frac{8}{3}=\frac{\square}{6}=\frac{\square}{24}=\frac{24}{\square} $$"
- `ch04-b019-i05` [exercise_item] — placed in **AO:equivalent-fractions-ao-find-equivalence-using-formula (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions > Exercise 4.3: Determine equivalent fractions
  - evidence quote: "### Exercise 4.3: Determine equivalent fractions  Find the missing numbers in each list of equivalent fractions.  5. $$ \frac{24}{27}=\frac{8}{\square}=\frac{64}{\square}=\frac{40}{\square} $$"
- `ch04-b020` [exposition] — placed in **AO:equivalent-fractions-ao-identify-equivalent-fractions (instruction)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions > Simplify equivalent fractions
  - evidence quote: "A fraction is in its **simplest form** when the numerator and the denominator have no common factor. For example, $\frac{1}{2}$ is the simplest form of the fractions $\frac{2}{4}$ and $\frac{4}{8}$. These fractions are…"
- `ch04-b021` [definition] — placed in **AO:equivalent-fractions-ao-identify-equivalent-fractions (foundation)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions > Simplify equivalent fractions
  - evidence quote: "**simplest form** A fraction is in its simplest form when the numerator and denominator have no common factor."
- `ch04-b022` [worked_example] — placed in **AO:equivalent-fractions-ao-identify-equivalent-fractions (worked_example)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions > Worked example 4.4: Finding the simplest form of a fraction
  - evidence quote: "Find the simplest form of the fraction $\frac{40}{60}$."
- `ch04-b023` [exercise_block] — placed in **excluded**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions > Exercise 4.4: Simplify fractions
  - evidence quote: "### Exercise 4.4: Simplify fractions  Find the simplest form of each of the following fractions, using the method of your choice."
- `ch04-b023-i01` [exercise_item] — placed in **AO:equivalent-fractions-ao-identify-equivalent-fractions (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions > Exercise 4.4: Simplify fractions
  - evidence quote: "### Exercise 4.4: Simplify fractions  Find the simplest form of each of the following fractions, using the method of your choice.  1. $$ \frac{39}{78} $$"
- `ch04-b023-i02` [exercise_item] — placed in **AO:equivalent-fractions-ao-identify-equivalent-fractions (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions > Exercise 4.4: Simplify fractions
  - evidence quote: "### Exercise 4.4: Simplify fractions  Find the simplest form of each of the following fractions, using the method of your choice.  2. $$ \frac{12}{108} $$"
- `ch04-b023-i03` [exercise_item] — placed in **AO:equivalent-fractions-ao-identify-equivalent-fractions (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions > Exercise 4.4: Simplify fractions
  - evidence quote: "### Exercise 4.4: Simplify fractions  Find the simplest form of each of the following fractions, using the method of your choice.  3. $$ \frac{16}{64} $$"
- `ch04-b023-i04` [exercise_item] — placed in **AO:equivalent-fractions-ao-identify-equivalent-fractions (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions > Exercise 4.4: Simplify fractions
  - evidence quote: "### Exercise 4.4: Simplify fractions  Find the simplest form of each of the following fractions, using the method of your choice.  4. $$ \frac{45}{75} $$"
- `ch04-b023-i05` [exercise_item] — placed in **AO:equivalent-fractions-ao-identify-equivalent-fractions (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions > Exercise 4.4: Simplify fractions
  - evidence quote: "### Exercise 4.4: Simplify fractions  Find the simplest form of each of the following fractions, using the method of your choice.  5. $$ \frac{250}{150} $$"
- `ch04-b024` [exposition] — placed in **AO:equivalent-fractions-ao-identify-equivalent-fractions (instruction)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions > Identify equivalent fractions
  - evidence quote: "Fractions that are equivalent have the same simplest form. Look at the two diagrams below. The fraction of the rectangle that is shaded is given next to each diagram.  ![](https://electricbookworks.github.io/siyavula-op…"
- `ch04-b025` [note] — placed in **AO:equivalent-fractions-ao-identify-equivalent-fractions (foundation)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Equivalent fractions > Identify equivalent fractions
  - evidence quote: "Remember that equivalent fractions have the same simplest form."
- `ch04-b026` [exercise_block] — placed in **excluded**
  - heading: Chapter 4: Equivalent fractions > 4.2 Comparing fractions > Exercise 4.5: Determine whether fractions are equivalent or not
  - evidence quote: "### Exercise 4.5: Determine whether fractions are equivalent or not  For each of the following pairs of fractions, determine whether they are equivalent or not."
- `ch04-b026-i01` [exercise_item] — placed in **AO:equivalent-fractions-ao-identify-equivalent-fractions (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Comparing fractions > Exercise 4.5: Determine whether fractions are equivalent or not
  - evidence quote: "### Exercise 4.5: Determine whether fractions are equivalent or not  1. $\frac{15}{18}$ and $\frac{20}{24}$"
- `ch04-b026-i02` [exercise_item] — placed in **AO:equivalent-fractions-ao-identify-equivalent-fractions (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Comparing fractions > Exercise 4.5: Determine whether fractions are equivalent or not
  - evidence quote: "### Exercise 4.5: Determine whether fractions are equivalent or not  2. $\frac{14}{70}$ and $\frac{21}{105}$"
- `ch04-b026-i03` [exercise_item] — placed in **AO:equivalent-fractions-ao-identify-equivalent-fractions (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Comparing fractions > Exercise 4.5: Determine whether fractions are equivalent or not
  - evidence quote: "### Exercise 4.5: Determine whether fractions are equivalent or not  3. $\frac{16}{48}$ and $\frac{18}{72}$"
- `ch04-b026-i04` [exercise_item] — placed in **AO:equivalent-fractions-ao-identify-equivalent-fractions (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Comparing fractions > Exercise 4.5: Determine whether fractions are equivalent or not
  - evidence quote: "### Exercise 4.5: Determine whether fractions are equivalent or not  4. $\frac{36}{24}$ and $\frac{24}{16}$"
- `ch04-b026-i05` [exercise_item] — placed in **AO:equivalent-fractions-ao-identify-equivalent-fractions (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.2 Comparing fractions > Exercise 4.5: Determine whether fractions are equivalent or not
  - evidence quote: "### Exercise 4.5: Determine whether fractions are equivalent or not  5. $\frac{8}{10}$ and $\frac{18}{20}$"
- `ch04-b058` [summary] — placed in **excluded**
  - heading: Chapter 4: Equivalent fractions > 4.7 Summary
  - evidence quote: "- A common fraction is written as $\frac{\text{numerator}}{\text{denominator}}$. - A proper fraction is smaller than 1, for example $\frac{2}{7}$. - A mixed number consists of a whole number and a proper fraction, for e…"

### Row-level review categories and manually authored reasons
- **prerequisite_only_evidence**: The apply-in-sharing-commodities AO has only the shared_foundation equivalent-fraction definitions (ch04-b014 exposition, ch04-b015 definition); no record teaches applying equivalent fractions to sharing commodities. The foundation knowledge is prerequisite, not direct AO support.
- **no_reused_assessment**: identify-equivalent-fractions and find-equivalence-using-formula AOs have direct exercises (ch04-b026-i01..i05 and ch04-b019-i01..i05) but no AO-aligned reused exercise_item assessment was selected. apply-in-sharing-commodities has no exercise at all.

### Per-atomic-objective evidence classification
- `equivalent-fractions-ao-identify-equivalent-fractions` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch04-b020(instruction), ch04-b021(foundation), ch04-b022(worked_example), ch04-b023-i01(exercise), ch04-b023-i02(exercise), ch04-b023-i03(exercise), ch04-b023-i04(exercise), ch04-b023-i05(exercise), ch04-b024(instruction), ch04-b025(foundation), ch04-b026-i01(exercise), ch04-b026-i02(exercise), ch04-b026-i03(exercise), ch04-b026-i04(exercise), ch04-b026-i05(exercise)
  - assessment: _(none anchored)_
- `equivalent-fractions-ao-find-equivalence-using-formula` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch04-b016(instruction), ch04-b017(worked_example), ch04-b018(foundation), ch04-b019-i01(exercise), ch04-b019-i02(exercise), ch04-b019-i03(exercise), ch04-b019-i04(exercise), ch04-b019-i05(exercise)
  - assessment: _(none anchored)_
- `equivalent-fractions-ao-apply-in-sharing-commodities` → evidence: **prerequisite_only** · categories: prerequisite_only_evidence
  - linked records: _(none)_
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-fractions-quantitative-aptitude-reasoning`

**Title:** Quantitative aptitude reasoning  
**Status:** `mapped`  
**Row review categories:** _(none — mapped or no-records baseline)_

### Curriculum objectives (source)
- `jss1-math-fractions-quantitative-aptitude-reasoning-po01`: Solve problems in quantitative aptitude

### Atomic objectives
- `fractions-quantitative-reasoning-ao-solve-problems` [solve/apply]: Solve problems in quantitative aptitude.

### Linked textbook records (12 total) — inspected
- `ch04-b056` [exposition] — placed in **AO:fractions-quantitative-reasoning-ao-solve-problems (instruction)**
  - heading: Chapter 4: Equivalent fractions > 4.6 Practical applications
  - evidence quote: "Fractions are very useful in everyday life. We use equivalent fractions to compare different fractions and to convert one type of fraction to another."
- `ch04-b057` [exercise_block] — placed in **excluded**
  - heading: Chapter 4: Equivalent fractions > 4.6 Practical applications > Exercise 4.12: Use equivalent fractions to solve problems
  - evidence quote: "### Exercise 4.12: Use equivalent fractions to solve problems"
- `ch04-b057-i01` [exercise_item] — placed in **AO:fractions-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.6 Practical applications > Exercise 4.12: Use equivalent fractions to solve problems
  - evidence quote: "### Exercise 4.12: Use equivalent fractions to solve problems  1. A teacher has 25 learners in her class. At break time, she decides to give each of them one quarter of an orange to eat. How many oranges does she need?"
- `ch04-b057-i02` [exercise_item] — placed in **AO:fractions-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.6 Practical applications > Exercise 4.12: Use equivalent fractions to solve problems
  - evidence quote: "### Exercise 4.12: Use equivalent fractions to solve problems  2. After a birthday party, $2\frac{2}{5}$ cakes are left over. If the leftover cake is cut into equal pieces, how many people could get one piece each?"
- `ch04-b057-i03` [exercise_item] — placed in **AO:fractions-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.6 Practical applications > Exercise 4.12: Use equivalent fractions to solve problems
  - evidence quote: "### Exercise 4.12: Use equivalent fractions to solve problems  3. The floor of a room is tiled with 64 identical tiles. A carpet is put in the centre of the room. The carpet covers $\frac{3}{8}$ of the tiled surface. Ho…"
- `ch04-b057-i04` [exercise_item] — placed in **AO:fractions-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.6 Practical applications > Exercise 4.12: Use equivalent fractions to solve problems
  - evidence quote: "### Exercise 4.12: Use equivalent fractions to solve problems  4. A bag with 72 sweets is divided between Musa, Umar and Isa. Musa gets 27 sweets, Umar gets 12 sweets, and Isa gets the rest of the sweets. Determine whic…"
- `ch04-b057-i05` [exercise_item] — placed in **AO:fractions-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.6 Practical applications > Exercise 4.12: Use equivalent fractions to solve problems
  - evidence quote: "### Exercise 4.12: Use equivalent fractions to solve problems  5. Atinuke and Eniola buy a bag of rice. Atinuke gets $\frac{3}{7}$ of the bag, Eniola gets $\frac{5}{9}$ of the bag and a little bit is left over. Who rece…"
- `ch04-b057-i06` [exercise_item] — placed in **AO:fractions-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.6 Practical applications > Exercise 4.12: Use equivalent fractions to solve problems
  - evidence quote: "### Exercise 4.12: Use equivalent fractions to solve problems  6. A wall with a surface area of 1 m^2 is painted. The painter knocks over the can of paint and some of the paint cannot be recovered. She is only able to p…"
- `ch04-b057-i07` [exercise_item] — placed in **AO:fractions-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.6 Practical applications > Exercise 4.12: Use equivalent fractions to solve problems
  - evidence quote: "### Exercise 4.12: Use equivalent fractions to solve problems  7. Amadi has to walk 1 km to school. After walking $\frac{5}{8}$ of the way, he realises that he forgot a book at home and he turns around. Determine the di…"
- `ch04-b057-i08` [exercise_item] — placed in **AO:fractions-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.6 Practical applications > Exercise 4.12: Use equivalent fractions to solve problems
  - evidence quote: "### Exercise 4.12: Use equivalent fractions to solve problems  8. Jummai got 88% for a class test. The test was for 25 marks. Calculate Jummai's mark out of 25."
- `ch04-b057-i09` [exercise_item] — placed in **AO:fractions-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.6 Practical applications > Exercise 4.12: Use equivalent fractions to solve problems
  - evidence quote: "### Exercise 4.12: Use equivalent fractions to solve problems  9. There are 30 students in a class. If 21 students are girls, what percentage of the class is female?"
- `ch04-b057-i10` [exercise_item] — placed in **AO:fractions-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.6 Practical applications > Exercise 4.12: Use equivalent fractions to solve problems
  - evidence quote: "### Exercise 4.12: Use equivalent fractions to solve problems  10. A children's clothing store advertises a 15% discount on a dress of ₦3,000. Calculate the value of the discount."

### Row-level review categories and manually authored reasons
_None — all AOs have direct evidence and a reused assessment._

### Per-atomic-objective evidence classification
- `fractions-quantitative-reasoning-ao-solve-problems` → evidence: **direct** · categories: —
  - linked records: ch04-b056(instruction), ch04-b057-i01(exercise), ch04-b057-i02(exercise), ch04-b057-i03(exercise), ch04-b057-i04(exercise), ch04-b057-i05(exercise), ch04-b057-i06(exercise), ch04-b057-i07(exercise), ch04-b057-i08(exercise), ch04-b057-i09(exercise), ch04-b057-i10(exercise)
  - assessment: reused from `ch04-b057-i03`

---

## `jss1-math-fractions-ordering-of-fractions`

**Title:** Ordering of fractions  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-fractions-ordering-of-fractions-po01`: Arrange fractions in ascending/descending order

### Atomic objectives
- `ordering-of-fractions-ao-arrange-ascending` [arrange/apply]: Arrange fractions in ascending order.
- `ordering-of-fractions-ao-arrange-descending` [arrange/apply]: Arrange fractions in descending order.

### Linked textbook records (12 total) — inspected
- `ch04-b027` [exposition] — placed in **shared_foundation**
  - heading: Chapter 4: Equivalent fractions > 4.3 Comparing fractions
  - evidence quote: "It may be difficult to compare fractions that do not have the same denominator. Look at the two diagrams below. The fraction of the circle that is shaded is given below each diagram.  ![](https://electricbookworks.githu…"
- `ch04-b028` [definition] — placed in **shared_foundation**
  - heading: Chapter 4: Equivalent fractions > 4.3 Comparing fractions
  - evidence quote: "lowest common denominator (LCD)  The LCD is the smallest whole number into which the denominators of two or more fractions can divide without a remainder."
- `ch04-b029` [note] — placed in **excluded**
  - heading: Chapter 4: Equivalent fractions > 4.3 Comparing fractions
  - evidence quote: "If necessary, go back to Chapter 2 to see how to find the LCM of two or more numbers."
- `ch04-b030` [exposition] — placed in **shared_foundation**
  - heading: Chapter 4: Equivalent fractions > 4.3 Comparing fractions
  - evidence quote: "If we express more than two fractions using the same denominator, this allows us to order the fractions in ascending order or descending order. Fractions that are arranged in ascending order start with the smallest frac…"
- `ch04-b031` [definition] — placed in **shared_foundation**
  - heading: Chapter 4: Equivalent fractions > 4.3 Comparing fractions
  - evidence quote: "ascending order  When numbers of any kind are arranged in ascending order, they are arranged from the smallest to the largest.  descending order  When numbers of any kind are arranged in descending order, they are arran…"
- `ch04-b032` [worked_example] — placed in **AO:ordering-of-fractions-ao-arrange-ascending (worked_example)**
  - heading: Chapter 4: Equivalent fractions > 4.3 Comparing fractions > Worked example 4.5: Ordering fractions
  - evidence quote: "Arrange the following fractions in ascending order:  $$ \frac{5}{6};\space\frac{7}{8};\space\frac{3}{4} $$"
- `ch04-b033` [exercise_block] — placed in **excluded**
  - heading: Chapter 4: Equivalent fractions > 4.3 Comparing fractions > Exercise 4.6: Order and compare fractions
  - evidence quote: "### Exercise 4.6: Order and compare fractions"
- `ch04-b033-i01` [exercise_item] — placed in **AO:ordering-of-fractions-ao-arrange-ascending (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.3 Comparing fractions > Exercise 4.6: Order and compare fractions
  - evidence quote: "### Exercise 4.6: Order and compare fractions  1. Arrange the following fractions in ascending order: $\frac{8}{9};\space\frac{11}{12};\space\frac{5}{6}$"
- `ch04-b033-i02` [exercise_item] — placed in **AO:ordering-of-fractions-ao-arrange-descending (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.3 Comparing fractions > Exercise 4.6: Order and compare fractions
  - evidence quote: "### Exercise 4.6: Order and compare fractions  2. Arrange the following fractions in descending order: $\frac{5}{8};\space\frac{8}{14};\space\frac{18}{28}$"
- `ch04-b033-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 4: Equivalent fractions > 4.3 Comparing fractions > Exercise 4.6: Order and compare fractions
  - evidence quote: "### Exercise 4.6: Order and compare fractions  3. Look at this list of fractions: $\frac{13}{4};\space\frac{8}{28};\space\frac{17}{6};\space\frac{15}{35};\space\frac{9}{21}$. From the list, identify:  a. two fractions t…"
- `ch04-b057-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 4: Equivalent fractions > 4.6 Practical applications > Exercise 4.12: Use equivalent fractions to solve problems
  - evidence quote: "### Exercise 4.12: Use equivalent fractions to solve problems  5. Atinuke and Eniola buy a bag of rice. Atinuke gets $\frac{3}{7}$ of the bag, Eniola gets $\frac{5}{9}$ of the bag and a little bit is left over. Who rece…"
- `ch04-b058` [summary] — placed in **excluded**
  - heading: Chapter 4: Equivalent fractions > 4.7 Summary
  - evidence quote: "- A common fraction is written as $\frac{\text{numerator}}{\text{denominator}}$. - A proper fraction is smaller than 1, for example $\frac{2}{7}$. - A mixed number consists of a whole number and a proper fraction, for e…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch04-b033-i03 asks the student to identify equivalent/highest/lowest fractions from a list (an identification task, not ordering); ch04-b057-i05 is an applied word problem belonging to the QR subtopic.
- **no_reused_assessment**: Ascending and descending AOs each have a single direct exercise but neither has a reused assessment.

### Per-atomic-objective evidence classification
- `ordering-of-fractions-ao-arrange-ascending` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch04-b032(worked_example), ch04-b033-i01(exercise)
  - assessment: _(none anchored)_
- `ordering-of-fractions-ao-arrange-descending` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch04-b033-i02(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All review_items were inspected. Candidate proposal added for identifying equivalent/highest/lowest fractions from a list; the applied sharing record belongs to the equivalent-fractions problem-solving scope and was not proposed here.

### Candidate atomic objective proposals
- `ordering-of-fractions-candidate-ao-identify-highest-lowest-equivalent-fractions` [extension_or_enrichment; candidate_for_expert_review]
  - proposed objective: Identify equivalent, highest, and lowest fractions from a list.
  - source records: ch04-b033-i03
  - closest existing AOs: ordering-of-fractions-ao-arrange-ascending, ordering-of-fractions-ao-arrange-descending
  - candidate evidence quote: "From the list, identify:"
  - rationale: The item asks for selected comparisons from a list rather than arranging all fractions in ascending or descending order.

---

## `jss1-math-fractions-conversion-of-fractions-to-decimals-and-vice-versa`

**Title:** Conversion of fractions to decimals and vice versa  
**Status:** `mapped`  
**Row review categories:** _(none — mapped or no-records baseline)_

### Curriculum objectives (source)
- `jss1-math-fractions-conversion-of-fractions-to-decimals-and-vice-versa-po01`: Convert fractions to decimals and decimal to fraction

### Atomic objectives
- `fractions-to-decimals-ao-convert-fractions-to-decimals` [convert/apply]: Convert fractions to decimals.
- `fractions-to-decimals-ao-convert-decimals-to-fractions` [convert/apply]: Convert decimals to fractions.

### Linked textbook records (32 total) — inspected
- `ch01-b013` [exposition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Place value in decimal fractions
  - evidence quote: "A fraction means a part of a whole. One way to write a fraction is to write one whole number on top of another whole number with a dividing line between them. For example, $\frac{2}{10}$ means two parts of a whole that…"
- `ch01-b014` [definition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Place value in decimal fractions
  - evidence quote: "**decimal fraction** A decimal fraction is a fraction in which the digits of the numerator are written after a decimal point."
- `ch01-b015` [exposition] — placed in **AO:fractions-to-decimals-ao-convert-fractions-to-decimals (foundation)**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Place value in decimal fractions
  - evidence quote: "To write a fraction as a decimal fraction, the denominator has to be in a grouping of 10, so it needs to be 10; 100; 1,000; or 10,000, and so on. This is because decimal fractions use the base ten number system."
- `ch01-b016` [note] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Place value in decimal fractions
  - evidence quote: "You will learn more about fractions in Chapter 4. You will also learn how to change a fraction so that its denominator is in a grouping of 10."
- `ch01-b017` [exposition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Place value in decimal fractions
  - evidence quote: "For decimal fractions, the place values we work with are $\frac{1}{10}, \frac{1}{100}, \frac{1}{1,000}$ and $\frac{1}{10,000}$. They are called **tenths**, **hundredths**, **thousandths** and **ten thousandths**.  These…"
- `ch01-b018` [definition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Place value in decimal fractions
  - evidence quote: "**tenths** Tenths are the decimal fractions 0.1; 0.2; 0.3; 0.4; 0.5; 0.6; 0.7; 0.8; 0.9 in the base ten number system.  **hundredths** Hundredths are the decimal fractions 0.01; 0.02; 0.03; 0.04; 0.05; 0.06; 0.07; 0.08;…"
- `ch01-b020` [note] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Place value in decimal fractions
  - evidence quote: "As you can see, we do not give the place value of the zeroes in a number, because 0 multiplied by anything equals 0. So the place value of any 0 will always be 0. The zeroes have to be included in a number to show the p…"
- `ch01-b022` [exposition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.3 Powers of ten
  - evidence quote: "In the base ten number system, we can use powers of ten to write big numbers, so that they are easier to read and work with. For example, the number 100 is equal to $10\times 10$. This can be written as $10^2$. Here the…"
- `ch01-b023` [note] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.3 Powers of ten
  - evidence quote: "You will learn more about writing numbers in index form in Chapter 2."
- `ch01-b024` [exposition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.3 Powers of ten
  - evidence quote: "The table lists the powers of ten for numbers you have already worked with.  $$ \begin{array}{|l|l|l|}   \hline     \textbf{Name} & \textbf{Number} & \textbf{Powers of ten}  \\     \hline      \text{Ten} & 10 & 10=10^1…"
- `ch04-b034` [exposition] — placed in **shared_foundation**
  - heading: Chapter 4: Equivalent fractions > 4.4 Decimal fractions
  - evidence quote: "Instead of writing a fraction as a common fraction, we can also write it as a **decimal fraction**. We use **decimal notation** to write decimal fractions. In this notation, the numerator is written after a decimal poin…"
- `ch04-b035` [definition] — placed in **shared_foundation**
  - heading: Chapter 4: Equivalent fractions > 4.4 Decimal fractions
  - evidence quote: "**decimal fraction** A decimal fraction is a fraction that is written in decimal notation, with the whole number before the decimal point and the fraction after it.  **decimal notation** Decimal notation is a way of wri…"
- `ch04-b036` [exposition] — placed in **shared_foundation**
  - heading: Chapter 4: Equivalent fractions > 4.4 Decimal fractions
  - evidence quote: "In decimal notation, the number of digits after the decimal point shows us which power of ten is the fraction's denominator. You learnt about these decimal fractions in Chapter 1:  $$ \begin{array}{|l|l|l|l|}   \hline…"
- `ch04-b037` [note] — placed in **shared_foundation**
  - heading: Chapter 4: Equivalent fractions > 4.4 Decimal fractions
  - evidence quote: "You do not need to write zeros at the end of decimal fractions. For example, we write 0.5 rather than 0.50 or 0.500. This is because $\frac{5}{10}=\frac{50}{100}=\frac{500}{1,000}$."
- `ch04-b038` [exposition] — placed in **shared_foundation**
  - heading: Chapter 4: Equivalent fractions > 4.4 Decimal fractions > Converting decimal fractions to common fractions
  - evidence quote: "The fraction 0.5 and the fraction $\frac{1}{2}$ represent exactly the same part of a whole, namely a half. The fractions $\frac{5}{10}$ and $\frac{1}{2}$ are equivalent fractions. A decimal fraction and a common fractio…"
- `ch04-b039` [worked_example] — placed in **AO:fractions-to-decimals-ao-convert-decimals-to-fractions (worked_example)**
  - heading: Chapter 4: Equivalent fractions > 4.4 Decimal fractions > Worked example 4.6: Converting decimal fractions to common fractions
  - evidence quote: "Write 4.08 as a common fraction."
- `ch04-b040` [exercise_block] — placed in **excluded**
  - heading: Chapter 4: Equivalent fractions > 4.4 Decimal fractions > Exercise 4.7: Convert decimal fractions to common fractions
  - evidence quote: "### Exercise 4.7: Convert decimal fractions to common fractions  Convert the following decimal fractions to common fractions."
- `ch04-b040-i01` [exercise_item] — placed in **AO:fractions-to-decimals-ao-convert-decimals-to-fractions (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.4 Decimal fractions > Exercise 4.7: Convert decimal fractions to common fractions
  - evidence quote: "### Exercise 4.7: Convert decimal fractions to common fractions  Convert the following decimal fractions to common fractions.  1. 1.05"
- `ch04-b040-i02` [exercise_item] — placed in **AO:fractions-to-decimals-ao-convert-decimals-to-fractions (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.4 Decimal fractions > Exercise 4.7: Convert decimal fractions to common fractions
  - evidence quote: "### Exercise 4.7: Convert decimal fractions to common fractions  Convert the following decimal fractions to common fractions.  2. 0.128"
- `ch04-b040-i03` [exercise_item] — placed in **AO:fractions-to-decimals-ao-convert-decimals-to-fractions (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.4 Decimal fractions > Exercise 4.7: Convert decimal fractions to common fractions
  - evidence quote: "### Exercise 4.7: Convert decimal fractions to common fractions  Convert the following decimal fractions to common fractions.  3. 0.0275"
- `ch04-b041` [exposition] — placed in **AO:fractions-to-decimals-ao-convert-fractions-to-decimals (instruction)**
  - heading: Chapter 4: Equivalent fractions > 4.4 Decimal fractions > Converting common fractions to decimal fractions
  - evidence quote: "When a common fraction has a denominator that is a power of ten, it is easy to convert it to a decimal fraction. You dealt with the place values of decimal fractions in Chapter 1.  $$ \begin{array}{|c|c|c|c|c|c|}   \hli…"
- `ch04-b042` [exercise_block] — placed in **excluded**
  - heading: Chapter 4: Equivalent fractions > 4.4 Decimal fractions > Exercise 4.8: Convert common fractions with denominators that are powers of ten to decimal fractions
  - evidence quote: "### Exercise 4.8: Convert common fractions with denominators that are powers of ten to decimal fractions  Convert the following common fractions to decimal fractions."
- `ch04-b042-i01` [exercise_item] — placed in **AO:fractions-to-decimals-ao-convert-fractions-to-decimals (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.4 Decimal fractions > Exercise 4.8: Convert common fractions with denominators that are powers of ten to decimal fractions
  - evidence quote: "### Exercise 4.8: Convert common fractions with denominators that are powers of ten to decimal fractions  1. $\frac{506}{1,000}$"
- `ch04-b042-i02` [exercise_item] — placed in **AO:fractions-to-decimals-ao-convert-fractions-to-decimals (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.4 Decimal fractions > Exercise 4.8: Convert common fractions with denominators that are powers of ten to decimal fractions
  - evidence quote: "### Exercise 4.8: Convert common fractions with denominators that are powers of ten to decimal fractions  2. $\frac{29}{10,000}$"
- `ch04-b042-i03` [exercise_item] — placed in **AO:fractions-to-decimals-ao-convert-fractions-to-decimals (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.4 Decimal fractions > Exercise 4.8: Convert common fractions with denominators that are powers of ten to decimal fractions
  - evidence quote: "### Exercise 4.8: Convert common fractions with denominators that are powers of ten to decimal fractions  3. $\frac{720}{100}$"
- `ch04-b043` [exposition] — placed in **AO:fractions-to-decimals-ao-convert-fractions-to-decimals (instruction)**
  - heading: Chapter 4: Equivalent fractions > 4.4 Decimal fractions > Converting common fractions to decimal fractions
  - evidence quote: "When the denominator of a common fraction is not a power of ten, we use division to convert the common fraction to a decimal fraction."
- `ch04-b044` [worked_example] — placed in **AO:fractions-to-decimals-ao-convert-fractions-to-decimals (worked_example)**
  - heading: Chapter 4: Equivalent fractions > 4.4 Decimal fractions > Worked example 4.7: Converting common fractions to decimal fractions
  - evidence quote: "Write  $\frac{5}{6}$ as a decimal fraction."
- `ch04-b045` [exercise_block] — placed in **excluded**
  - heading: Chapter 4: Equivalent fractions > 4.4 Decimal fractions > Exercise 4.9: Convert common fractions to decimal fractions
  - evidence quote: "### Exercise 4.9: Convert common fractions to decimal fractions  Convert the following common fractions to decimal fractions."
- `ch04-b045-i01` [exercise_item] — placed in **AO:fractions-to-decimals-ao-convert-fractions-to-decimals (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.4 Decimal fractions > Exercise 4.9: Convert common fractions to decimal fractions
  - evidence quote: "### Exercise 4.9: Convert common fractions to decimal fractions  1. $\frac{3}{8}$"
- `ch04-b045-i02` [exercise_item] — placed in **AO:fractions-to-decimals-ao-convert-fractions-to-decimals (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.4 Decimal fractions > Exercise 4.9: Convert common fractions to decimal fractions
  - evidence quote: "### Exercise 4.9: Convert common fractions to decimal fractions  2. $\frac{23}{4}$"
- `ch04-b045-i03` [exercise_item] — placed in **AO:fractions-to-decimals-ao-convert-fractions-to-decimals (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.4 Decimal fractions > Exercise 4.9: Convert common fractions to decimal fractions
  - evidence quote: "### Exercise 4.9: Convert common fractions to decimal fractions  3. $\frac{9}{40}$"
- `ch04-b058` [summary] — placed in **excluded**
  - heading: Chapter 4: Equivalent fractions > 4.7 Summary
  - evidence quote: "- A common fraction is written as $\frac{\text{numerator}}{\text{denominator}}$. - A proper fraction is smaller than 1, for example $\frac{2}{7}$. - A mixed number consists of a whole number and a proper fraction, for e…"

### Row-level review categories and manually authored reasons
_None — all AOs have direct evidence and a reused assessment._

### Per-atomic-objective evidence classification
- `fractions-to-decimals-ao-convert-fractions-to-decimals` → evidence: **direct** · categories: —
  - linked records: ch01-b015(foundation), ch04-b041(instruction), ch04-b042-i01(exercise), ch04-b042-i02(exercise), ch04-b042-i03(exercise), ch04-b043(instruction), ch04-b044(worked_example), ch04-b045-i01(exercise), ch04-b045-i02(exercise), ch04-b045-i03(exercise)
  - assessment: reused from `ch04-b045-i01`
- `fractions-to-decimals-ao-convert-decimals-to-fractions` → evidence: **direct** · categories: —
  - linked records: ch04-b039(worked_example), ch04-b040-i01(exercise), ch04-b040-i02(exercise), ch04-b040-i03(exercise)
  - assessment: reused from `ch04-b040-i03`

---

## `jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa`

**Title:** Conversion of fractions to percentages and vice versa  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-fractions-conversion-of-fractions-to-percentages-and-vice-versa-po01`: Convert fractions to percentages and percentages to fractions

### Atomic objectives
- `fractions-to-percentages-ao-convert-fractions-to-percentages` [convert/apply]: Convert fractions to percentages.
- `fractions-to-percentages-ao-convert-percentages-to-fractions` [convert/apply]: Convert percentages to fractions.

### Linked textbook records (21 total) — inspected
- `ch04-b046` [exposition] — placed in **shared_foundation**
  - heading: Chapter 4: Equivalent fractions > 4.5 Percentages
  - evidence quote: "As well as writing a fraction as a common fraction or a decimal fraction, we may also express a fraction as a **percentage**. A percentage is a fraction in which the denominator is always 100. Only the numerator is writ…"
- `ch04-b047` [definition] — placed in **shared_foundation**
  - heading: Chapter 4: Equivalent fractions > 4.5 Percentages
  - evidence quote: "**percentage** A percentage is a fraction in which the denominator is 100 and where only the numerator is written down, followed by a percentage symbol."
- `ch04-b048` [exposition] — placed in **shared_foundation**
  - heading: Chapter 4: Equivalent fractions > 4.5 Percentages
  - evidence quote: "This figure is divided into 100 parts. There are 22 blocks that are shaded. The common fraction $\frac{22}{100}$ tells you what part is shaded. To express this as a percentage, we write only the numerator, followed by a…"
- `ch04-b049` [note] — placed in **shared_foundation**
  - heading: Chapter 4: Equivalent fractions > 4.5 Percentages
  - evidence quote: "If we shade all the blocks in the figure, the shaded fraction will be $\frac{100}{100}=1$. One full whole is therefore 100%."
- `ch04-b050` [exposition] — placed in **AO:fractions-to-percentages-ao-convert-percentages-to-fractions (instruction)**
  - heading: Chapter 4: Equivalent fractions > 4.5 Percentages > Converting percentages to common fractions
  - evidence quote: "It is easy to convert percentages to common fractions. We simply use the form $\frac{\text{numerator}}{\text{denominator}}$. We know that the denominator is always 100, so we have $\frac{\text{numerator}}{100}$. The num…"
- `ch04-b051` [exercise_block] — placed in **excluded**
  - heading: Chapter 4: Equivalent fractions > 4.5 Percentages > Exercise 4.10: Convert percentages to common fractions
  - evidence quote: "### Exercise 4.10: Convert percentages to common fractions  Convert the following percentages to common fractions."
- `ch04-b051-i01` [exercise_item] — placed in **AO:fractions-to-percentages-ao-convert-percentages-to-fractions (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.5 Percentages > Exercise 4.10: Convert percentages to common fractions
  - evidence quote: "### Exercise 4.10: Convert percentages to common fractions  1. 55%"
- `ch04-b051-i02` [exercise_item] — placed in **AO:fractions-to-percentages-ao-convert-percentages-to-fractions (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.5 Percentages > Exercise 4.10: Convert percentages to common fractions
  - evidence quote: "### Exercise 4.10: Convert percentages to common fractions  2. 80%"
- `ch04-b051-i03` [exercise_item] — placed in **AO:fractions-to-percentages-ao-convert-percentages-to-fractions (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.5 Percentages > Exercise 4.10: Convert percentages to common fractions
  - evidence quote: "### Exercise 4.10: Convert percentages to common fractions  3. 4%"
- `ch04-b052` [exposition] — placed in **AO:fractions-to-percentages-ao-convert-fractions-to-percentages (instruction)**
  - heading: Chapter 4: Equivalent fractions > 4.5 Percentages > Converting common fractions to percentages
  - evidence quote: "To express a common fraction as a percentage, we need to know how many parts out of 100 we are dealing with. Consider the fraction $\frac{2}{5}$. It shows that we are dealing with 2 parts of a whole that is divided into…"
- `ch04-b053` [worked_example] — placed in **AO:fractions-to-percentages-ao-convert-fractions-to-percentages (worked_example)**
  - heading: Chapter 4: Equivalent fractions > 4.5 Percentages > Worked example 4.8: Converting common fractions to percentages
  - evidence quote: "Write $\frac{7}{8}$ as a percentage.  Step 1: Find the LCM of 100 and the denominator.  $8=2^3$ $100=2^2\times 5^2$ $\therefore \text{LCM}=2^3\times5^2=8\times25=200$  Step 2: Find the equivalent fraction in which the d…"
- `ch04-b054` [note] — placed in **AO:fractions-to-percentages-ao-convert-fractions-to-percentages (instruction)**
  - heading: Chapter 4: Equivalent fractions > 4.5 Percentages > Converting common fractions to percentages
  - evidence quote: "There are other ways to convert common fractions to percentages. You will learn more about this in Chapter 6."
- `ch04-b055` [exercise_block] — placed in **excluded**
  - heading: Chapter 4: Equivalent fractions > 4.5 Percentages > Exercise 4.11: Convert common fractions to percentages
  - evidence quote: "### Exercise 4.11: Convert common fractions to percentages"
- `ch04-b055-i01` [exercise_item] — placed in **AO:fractions-to-percentages-ao-convert-fractions-to-percentages (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.5 Percentages > Exercise 4.11: Convert common fractions to percentages
  - evidence quote: "### Exercise 4.11: Convert common fractions to percentages  1. $\frac{3}{5}$  $$ \frac{5}{5} $$  $$ 100=2^2\times 5^2 $$  $$ \therefore \text{LCM}=2^2\times5^2=4\times25=100 $$  $$ \frac{3\times20}{5\times20}=\frac{60}{…"
- `ch04-b055-i02` [exercise_item] — placed in **AO:fractions-to-percentages-ao-convert-fractions-to-percentages (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.5 Percentages > Exercise 4.11: Convert common fractions to percentages
  - evidence quote: "### Exercise 4.11: Convert common fractions to percentages  2. $\frac{13}{25}$"
- `ch04-b055-i03` [exercise_item] — placed in **AO:fractions-to-percentages-ao-convert-fractions-to-percentages (exercise)**
  - heading: Chapter 4: Equivalent fractions > 4.5 Percentages > Exercise 4.11: Convert common fractions to percentages
  - evidence quote: "### Exercise 4.11: Convert common fractions to percentages  3. $\frac{1}{6}$  $$ 6=2\times3 $$  $$ 100=2^2\times 5^2 $$  $$ \therefore \text{LCM}=3\times2^2\times5^2=3\times4\times25=300 $$  $$ \frac{1\times50}{6\times5…"
- `ch04-b057-i08` [exercise_item] — placed in **review_items**
  - heading: Chapter 4: Equivalent fractions > 4.6 Practical applications > Exercise 4.12: Use equivalent fractions to solve problems
  - evidence quote: "### Exercise 4.12: Use equivalent fractions to solve problems  8. Jummai got 88% for a class test. The test was for 25 marks. Calculate Jummai's mark out of 25."
- `ch04-b057-i09` [exercise_item] — placed in **review_items**
  - heading: Chapter 4: Equivalent fractions > 4.6 Practical applications > Exercise 4.12: Use equivalent fractions to solve problems
  - evidence quote: "### Exercise 4.12: Use equivalent fractions to solve problems  9. There are 30 students in a class. If 21 students are girls, what percentage of the class is female?"
- `ch04-b057-i10` [exercise_item] — placed in **review_items**
  - heading: Chapter 4: Equivalent fractions > 4.6 Practical applications > Exercise 4.12: Use equivalent fractions to solve problems
  - evidence quote: "### Exercise 4.12: Use equivalent fractions to solve problems  10. A children's clothing store advertises a 15% discount on a dress of ₦3,000. Calculate the value of the discount."
- `ch04-b058` [summary] — placed in **excluded**
  - heading: Chapter 4: Equivalent fractions > 4.7 Summary
  - evidence quote: "- A common fraction is written as $\frac{\text{numerator}}{\text{denominator}}$. - A proper fraction is smaller than 1, for example $\frac{2}{7}$. - A mixed number consists of a whole number and a proper fraction, for e…"
- `ch06-b054-i09` [exercise_item] — placed in **review_items**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications > Exercise 6.10: Use operations with fractions to solve problems
  - evidence quote: "### Exercise 6.10: Use operations with fractions to solve problems  9. A clothing store offers a discount of 15% on a pair of shoes that originally cost ₦1,500. Calculate the new, discount price."

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch04-b057-i08/i09/i10 are applied equivalent-fraction word problems where conversion to/from a percentage is incidental, and ch06-b054-i09 is a Chapter-6 applied operations item.
- **no_reused_assessment**: Both conversion AOs have direct exercises but no reused exercise_item assessment was selected.

### Per-atomic-objective evidence classification
- `fractions-to-percentages-ao-convert-fractions-to-percentages` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch04-b052(instruction), ch04-b053(worked_example), ch04-b054(instruction), ch04-b055-i01(exercise), ch04-b055-i02(exercise), ch04-b055-i03(exercise)
  - assessment: _(none anchored)_
- `fractions-to-percentages-ao-convert-percentages-to-fractions` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch04-b050(instruction), ch04-b051-i01(exercise), ch04-b051-i02(exercise), ch04-b051-i03(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All review_items were inspected. Candidate proposal added for applied percentage/fraction word problems because these records go beyond direct conversion in either direction.

### Candidate atomic objective proposals
- `fractions-percentages-candidate-ao-solve-fraction-percentage-word-problems` [extension_or_enrichment; candidate_for_expert_review]
  - proposed objective: Solve word problems involving fractions and percentages.
  - source records: ch04-b057-i08, ch04-b057-i09, ch04-b057-i10, ch06-b054-i09
  - closest existing AOs: fractions-to-percentages-ao-convert-fractions-to-percentages, fractions-to-percentages-ao-convert-percentages-to-fractions
  - candidate evidence quote: "Jummai got 88% for a class test."
  - rationale: The records require applying percentage/fraction conversion in contexts, not simply converting isolated fractions and percentages.

---

## `jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values`

**Title:** Addition and subtraction of numbers and place values  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values-po01`: Add and subtract correctly
- `jss1-math-addition-and-subtraction-addition-and-subtraction-of-numbers-and-place-values-po02`: State place value of digits

### Atomic objectives
- `addition-and-subtraction-ao-add-correctly` [add/apply]: Add numbers correctly.
- `addition-and-subtraction-ao-subtract-correctly` [subtract/apply]: Subtract numbers correctly.
- `addition-and-subtraction-ao-state-place-value-of-digits` [state/remember]: State place value of digits.

### Linked textbook records (26 total) — inspected
- `ch01-b019` [worked_example] — placed in **AO:addition-and-subtraction-ao-state-place-value-of-digits (worked_example)**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Worked example 1.2: Finding place value in decimal numbers
  - evidence quote: "Write down the place values of all the non-zero digits in the following number: 73,025.048"
- `ch01-b021` [exercise_block] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Exercise 1.3: Determine place value in numbers with decimal fractions
  - evidence quote: "### Exercise 1.3: Determine place value in numbers with decimal fractions  Write down the place value of the given digit in each case."
- `ch01-b021-i01` [exercise_item] — placed in **AO:addition-and-subtraction-ao-state-place-value-of-digits (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Exercise 1.3: Determine place value in numbers with decimal fractions
  - evidence quote: "### Exercise 1.3: Determine place value in numbers with decimal fractions  Write down the place value of the given digit in each case.  1. Give the values of the digits 5 and 8 in the number 5,023.08"
- `ch01-b021-i02` [exercise_item] — placed in **AO:addition-and-subtraction-ao-state-place-value-of-digits (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Exercise 1.3: Determine place value in numbers with decimal fractions
  - evidence quote: "### Exercise 1.3: Determine place value in numbers with decimal fractions  Write down the place value of the given digit in each case.  2. Give the values of the digits 1 and 4 in the number 75.1804"
- `ch01-b021-i03` [exercise_item] — placed in **AO:addition-and-subtraction-ao-state-place-value-of-digits (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Exercise 1.3: Determine place value in numbers with decimal fractions
  - evidence quote: "### Exercise 1.3: Determine place value in numbers with decimal fractions  Write down the place value of the given digit in each case.  3. Give the values of the digits 9 and 7 in the number 70,546.009"
- `ch01-b021-i04` [exercise_item] — placed in **AO:addition-and-subtraction-ao-state-place-value-of-digits (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Exercise 1.3: Determine place value in numbers with decimal fractions
  - evidence quote: "### Exercise 1.3: Determine place value in numbers with decimal fractions  Write down the place value of the given digit in each case.  4. Give the two values of the digit 5 in the number 10,503.54"
- `ch01-b021-i05` [exercise_item] — placed in **AO:addition-and-subtraction-ao-state-place-value-of-digits (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Exercise 1.3: Determine place value in numbers with decimal fractions
  - evidence quote: "### Exercise 1.3: Determine place value in numbers with decimal fractions  Write down the place value of the given digit in each case.  5. Give the three values of the digit 9 in the number 99,148.319"
- `ch01-b025` [exposition] — placed in **AO:addition-and-subtraction-ao-add-correctly (instruction)**
  - heading: Chapter 1: Numbers big and small > 1.4 How to add in groups of ten using place value
  - evidence quote: "In the base ten number system, we can have a maximum of 9 digits for one place value. For example, the number 90 means 9 groups of 10, so we have a 9 in the tens place value. We may write it as 9 x 10 = 90. If we add an…"
- `ch01-b026` [exposition] — placed in **AO:addition-and-subtraction-ao-add-correctly (instruction)**
  - heading: Chapter 1: Numbers big and small > 1.4 How to add in groups of ten using place value > Beyond the digit 9
  - evidence quote: "Whenever we reach the digit 9 in any column of a place value table, and then want to add one more group:  - the digit 9 becomes 0 - the digit in the column to the left must increase by 1."
- `ch01-b027` [worked_example] — placed in **AO:addition-and-subtraction-ao-add-correctly (worked_example)**
  - heading: Chapter 1: Numbers big and small > 1.4 How to add in groups of ten using place value > Worked example 1.3: Dealing with the digit 9
  - evidence quote: "Add 10,000 to the number 591,432."
- `ch01-b028` [exercise_block] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.4 How to add in groups of ten using place value > Exercise 1.4: Do addition with numbers that have the digit 9
  - evidence quote: "### Exercise 1.4: Do addition with numbers that have the digit 9"
- `ch01-b028-i01` [exercise_item] — placed in **AO:addition-and-subtraction-ao-add-correctly (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.4 How to add in groups of ten using place value > Exercise 1.4: Do addition with numbers that have the digit 9
  - evidence quote: "### Exercise 1.4: Do addition with numbers that have the digit 9  1. Add 1,000 to the number 89,015."
- `ch01-b028-i02` [exercise_item] — placed in **AO:addition-and-subtraction-ao-add-correctly (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.4 How to add in groups of ten using place value > Exercise 1.4: Do addition with numbers that have the digit 9
  - evidence quote: "### Exercise 1.4: Do addition with numbers that have the digit 9  2. Add 100 to the number 9,938."
- `ch01-b028-i03` [exercise_item] — placed in **AO:addition-and-subtraction-ao-add-correctly (exercise)**
  - heading: Chapter 1: Numbers big and small > 1.4 How to add in groups of ten using place value > Exercise 1.4: Do addition with numbers that have the digit 9
  - evidence quote: "### Exercise 1.4: Do addition with numbers that have the digit 9  3. Add 10 to the number 7,992."
- `ch05-b001` [exposition] — placed in **shared_foundation**
  - heading: Chapter 5: Addition and subtraction of integers > 5.1 Revise place values
  - evidence quote: "In Chapter 1 you learnt that the place value of a digit tells us what the value of that digit is, based on its position in a number. You used place value tables to determine the place value of specific digits in a numbe…"
- `ch05-b002` [exercise_block] — placed in **excluded**
  - heading: Chapter 5: Addition and subtraction of integers > 5.1 Revise place values > Exercise 5.1: Determine place values
  - evidence quote: "### Exercise 5.1: Determine place values"
- `ch05-b002-i01` [exercise_item] — placed in **AO:addition-and-subtraction-ao-state-place-value-of-digits (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.1 Revise place values > Exercise 5.1: Determine place values
  - evidence quote: "### Exercise 5.1: Determine place values  1. Determine the place value of the digit 8 in each of the following numbers.  1. 987 2. 2,804 3. 168,417 4. 3,806,640 5. 26,008"
- `ch05-b002-i02` [exercise_item] — placed in **AO:addition-and-subtraction-ao-state-place-value-of-digits (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.1 Revise place values > Exercise 5.1: Determine place values
  - evidence quote: "### Exercise 5.1: Determine place values  2. Determine the two place values of the digit 3 in each of the following numbers.  1. 363 2. 3,031 3. 32,358 4. 331,047 5. 3,158,325"
- `ch05-b003` [exposition] — placed in **shared_foundation**
  - heading: Chapter 5: Addition and subtraction of integers > 5.2 Addition and subtraction of large numbers
  - evidence quote: "It is important to be aware of place values when we add or subtract large numbers. For example, we cannot subtract hundreds from units, or thousands from tens."
- `ch05-b004` [worked_example] — placed in **AO:addition-and-subtraction-ao-add-correctly (worked_example)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.2 Addition and subtraction of large numbers > Worked example 5.1: Adding whole numbers
  - evidence quote: "Find the total of $403+628+1,023+49$."
- `ch05-b005` [worked_example] — placed in **AO:addition-and-subtraction-ao-subtract-correctly (worked_example)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.2 Addition and subtraction of large numbers > Worked example 5.2: Subtracting whole numbers
  - evidence quote: "Subtract 178 from 4,032."
- `ch05-b006` [exercise_block] — placed in **excluded**
  - heading: Chapter 5: Addition and subtraction of integers > 5.2 Addition and subtraction of large numbers > Exercise 5.2: Add and subtract whole numbers
  - evidence quote: "### Exercise 5.2: Add and subtract whole numbers"
- `ch05-b006-i01` [exercise_item] — placed in **AO:addition-and-subtraction-ao-add-correctly (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.2 Addition and subtraction of large numbers > Exercise 5.2: Add and subtract whole numbers
  - evidence quote: "### Exercise 5.2: Add and subtract whole numbers  1. Add the following numbers.  1. $9,000+800+70+6$ 2. $5,050+55+5+500$ 3. $2,804+1,999+3,333$ 4. $42+1,005+936+41$ 5. $909+9,090+9,009+9$"
- `ch05-b006-i02` [exercise_item] — placed in **AO:addition-and-subtraction-ao-subtract-correctly (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.2 Addition and subtraction of large numbers > Exercise 5.2: Add and subtract whole numbers
  - evidence quote: "### Exercise 5.2: Add and subtract whole numbers  2. Subtract the following numbers.  1. $8,642-2,468$ 2. $1,723-958$ 3. $7,777-888$ 4. $10,000-8,734$ 5. $50,000-599$"
- `ch05-b006-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 5: Addition and subtraction of integers > 5.2 Addition and subtraction of large numbers > Exercise 5.2: Add and subtract whole numbers
  - evidence quote: "### Exercise 5.2: Add and subtract whole numbers  3. Determine the difference in the two place values of 5 in the following numbers.  To determine the difference between two numbers, subtract the smaller number from the…"
- `ch05-b033` [summary] — placed in **excluded**
  - heading: Chapter 5: Addition and subtraction of integers > 5.6 Summary
  - evidence quote: "- The place value of a digit tells us what the value of that digit is, based on its position in a number. - When we add or subtract large numbers, we line up the units, tens, hundreds and thousands of the numbers. - A n…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch05-b006-i03 asks for the difference between the two place values of digit 5 in two numbers, combining place-value identification with subtraction and not cleanly fitting a single AO.
- **no_reused_assessment**: Each of the three AOs has direct evidence but no reused exercise_item assessment was selected.

### Per-atomic-objective evidence classification
- `addition-and-subtraction-ao-add-correctly` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch01-b025(instruction), ch01-b026(instruction), ch01-b027(worked_example), ch01-b028-i01(exercise), ch01-b028-i02(exercise), ch01-b028-i03(exercise), ch05-b004(worked_example), ch05-b006-i01(exercise)
  - assessment: _(none anchored)_
- `addition-and-subtraction-ao-subtract-correctly` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch05-b005(worked_example), ch05-b006-i02(exercise)
  - assessment: _(none anchored)_
- `addition-and-subtraction-ao-state-place-value-of-digits` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch01-b019(worked_example), ch01-b021-i01(exercise), ch01-b021-i02(exercise), ch01-b021-i03(exercise), ch01-b021-i04(exercise), ch01-b021-i05(exercise), ch05-b002-i01(exercise), ch05-b002-i02(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-addition-and-subtraction-use-of-number-line`

**Title:** Use of number line  
**Status:** `mapped`  
**Row review categories:** _(none — mapped or no-records baseline)_

### Curriculum objectives (source)
- `jss1-math-addition-and-subtraction-use-of-number-line-po01`: Draw and use a number line

### Atomic objectives
- `use-of-number-line-ao-draw-number-line` [draw/apply]: Draw a number line.
- `use-of-number-line-ao-use-number-line` [use/apply]: Use a number line.

### Linked textbook records (30 total) — inspected
- `ch05-b007` [exposition] — placed in **shared_foundation**
  - heading: Chapter 5: Addition and subtraction of integers > 5.3 The number line
  - evidence quote: "The set of integers is made up of all the positive and negative whole numbers, including zero. We may represent integers on a number line. This is a straight line, divided into equal segments, that shows the position of…"
- `ch05-b008` [definition] — placed in **shared_foundation**
  - heading: Chapter 5: Addition and subtraction of integers > 5.3 The number line
  - evidence quote: "**integers** Integers are positive and negative whole numbers, including zero.  **number line** A number line is a straight line divided into equal segments, that shows the position of numbers.  **positive numbers** Pos…"
- `ch05-b009` [exposition] — placed in **AO:use-of-number-line-ao-draw-number-line (instruction)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.3 The number line
  - evidence quote: "We draw a number line with arrowheads at both ends to show that the line can carry on in both directions forever. Here is an example of a number line:  ![](https://electricbookworks.github.io/siyavula-open-textbooks-ima…"
- `ch05-b010` [note] — placed in **shared_foundation**
  - heading: Chapter 5: Addition and subtraction of integers > 5.3 The number line
  - evidence quote: "A number line can also be drawn vertically. Then the positive numbers lie above zero and the negative numbers lie below zero."
- `ch05-b011` [exposition] — placed in **AO:use-of-number-line-ao-use-number-line (instruction)**
  - heading: Chapter 5: Addition and subtraction of integers > Comparing integers on the number line
  - evidence quote: "Positive and negative numbers are sometimes called **directed numbers**. This is because the sign of the number (positive or negative) tells us in which direction from zero they appear on the number line."
- `ch05-b012` [definition] — placed in **AO:use-of-number-line-ao-use-number-line (foundation)**
  - heading: Chapter 5: Addition and subtraction of integers > Comparing integers on the number line
  - evidence quote: "**directed numbers** Directed numbers are positive and negative numbers. The sign of a directed number tells us in which direction from zero it lies on the number line."
- `ch05-b013` [exposition] — placed in **AO:use-of-number-line-ao-use-number-line (instruction)**
  - heading: Chapter 5: Addition and subtraction of integers > Comparing integers on the number line
  - evidence quote: "The further to the right a number lies on the number line, the larger it is. The further to the left a number lies on the number line, the smaller it is. We use the symbols < and > to show the relationship between two n…"
- `ch05-b014` [note] — placed in **AO:use-of-number-line-ao-use-number-line (instruction)**
  - heading: Chapter 5: Addition and subtraction of integers > Comparing integers on the number line
  - evidence quote: "To help you choose the correct symbol, remember that the symbol must "open up" towards the larger number. The "closed" and smaller end points to the smaller number. This crocodile may also help you remember which symbol…"
- `ch05-b015` [exercise_block] — placed in **excluded**
  - heading: Chapter 5: Addition and subtraction of integers > Comparing integers on the number line > Exercise 5.3: Compare integers
  - evidence quote: "### Exercise 5.3: Compare integers"
- `ch05-b015-i01` [exercise_item] — placed in **AO:use-of-number-line-ao-draw-number-line (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > Comparing integers on the number line > Exercise 5.3: Compare integers
  - evidence quote: "### Exercise 5.3: Compare integers  1. Draw a number line showing all the integers from -10 to 10."
- `ch05-b015-i02` [exercise_item] — placed in **AO:use-of-number-line-ao-use-number-line (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > Comparing integers on the number line > Exercise 5.3: Compare integers
  - evidence quote: "### Exercise 5.3: Compare integers  2. Place the correct symbol between each pair of numbers. Use your number line to help you.  a. 1 \square 7 b. 9 \square 6 c. 4 \square 0 d. -4 \square 0 e. 1 \square -2 f. -6 \square…"
- `ch05-b015-i03` [exercise_item] — placed in **AO:use-of-number-line-ao-use-number-line (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > Comparing integers on the number line > Exercise 5.3: Compare integers
  - evidence quote: "### Exercise 5.3: Compare integers  3. Arrange the following lists of numbers as required, using the correct symbol. Use your number line to help you.  a. Arrange from the smallest to the largest: 1;-5;-3; 2;-1 b. Arran…"
- `ch05-b016` [exposition] — placed in **AO:use-of-number-line-ao-use-number-line (instruction)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Adding integers
  - evidence quote: "We may use a number line to count. When we count to the right, we count in the positive direction. This is because the numbers become larger as we move to the right on a number line. When we count to the left, we count…"
- `ch05-b017` [note] — placed in **AO:use-of-number-line-ao-use-number-line (foundation)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Adding integers
  - evidence quote: "Integers may be added in any order. For example, $-1+3$ and $3+(-1)$ give the same answer."
- `ch05-b018` [worked_example] — placed in **AO:use-of-number-line-ao-use-number-line (worked_example)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Worked example 5.3: Adding integers using the number line
  - evidence quote: "Use a number line to determine the following: $-5+10$.  Step 1: Draw a number line and find the first number on the line.  The first number is -5.  ![](https://electricbookworks.github.io/siyavula-open-textbooks-images/…"
- `ch05-b019` [exercise_block] — placed in **excluded**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.4: Use a number line to add integers
  - evidence quote: "### Exercise 5.4: Use a number line to add integers  Use number lines to add the following pairs of integers."
- `ch05-b019-i01` [exercise_item] — placed in **AO:use-of-number-line-ao-use-number-line (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.4: Use a number line to add integers
  - evidence quote: "### Exercise 5.4: Use a number line to add integers  1. $1+6$"
- `ch05-b019-i02` [exercise_item] — placed in **AO:use-of-number-line-ao-use-number-line (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.4: Use a number line to add integers
  - evidence quote: "### Exercise 5.4: Use a number line to add integers  2. $-6+7$"
- `ch05-b019-i03` [exercise_item] — placed in **AO:use-of-number-line-ao-use-number-line (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.4: Use a number line to add integers
  - evidence quote: "### Exercise 5.4: Use a number line to add integers  3. $4+(-9)$"
- `ch05-b019-i04` [exercise_item] — placed in **AO:use-of-number-line-ao-use-number-line (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.4: Use a number line to add integers
  - evidence quote: "### Exercise 5.4: Use a number line to add integers  4. $-2+(-6)$"
- `ch05-b024` [exposition] — placed in **AO:use-of-number-line-ao-use-number-line (instruction)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Subtracting integers
  - evidence quote: "Another way is to see subtraction as the difference between two numbers. For example, if you have 7 sweets and you eat 4 sweets, you have $7-4=3$ left. The number of sweets you have left is the difference between the sw…"
- `ch05-b025` [note] — placed in **AO:use-of-number-line-ao-use-number-line (foundation)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Subtracting integers
  - evidence quote: "Integers cannot be subtracted in any order. For example, $3-1$ and $1-3$ do not give the same answer."
- `ch05-b026` [worked_example] — placed in **AO:use-of-number-line-ao-use-number-line (worked_example)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Worked example 5.4: Subtracting integers using the number line
  - evidence quote: "Use a number line to determine the following: $-5-3$  Use a number line to determine the following: $-4-(-6)$"
- `ch05-b027` [exercise_block] — placed in **excluded**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.6: Use a number line to subtract integers
  - evidence quote: "### Exercise 5.6: Use a number line to subtract integers  For each pair, use a number line to subtract the second integer from the first one."
- `ch05-b027-i01` [exercise_item] — placed in **AO:use-of-number-line-ao-use-number-line (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.6: Use a number line to subtract integers
  - evidence quote: "### Exercise 5.6: Use a number line to subtract integers  1. $2-5$"
- `ch05-b027-i02` [exercise_item] — placed in **AO:use-of-number-line-ao-use-number-line (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.6: Use a number line to subtract integers
  - evidence quote: "### Exercise 5.6: Use a number line to subtract integers  2. $-1-3$"
- `ch05-b027-i03` [exercise_item] — placed in **AO:use-of-number-line-ao-use-number-line (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.6: Use a number line to subtract integers
  - evidence quote: "### Exercise 5.6: Use a number line to subtract integers  3. $5-(-6)$"
- `ch05-b027-i04` [exercise_item] — placed in **AO:use-of-number-line-ao-use-number-line (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.6: Use a number line to subtract integers
  - evidence quote: "### Exercise 5.6: Use a number line to subtract integers  4. $-2-(-7)$"
- `ch05-b028` [worked_example] — placed in **AO:use-of-number-line-ao-use-number-line (worked_example)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Worked example 5.5: Comparing different methods of subtracting integers
  - evidence quote: "Determine the following: $-4-3$"
- `ch05-b033` [summary] — placed in **excluded**
  - heading: Chapter 5: Addition and subtraction of integers > 5.6 Summary
  - evidence quote: "- The place value of a digit tells us what the value of that digit is, based on its position in a number. - When we add or subtract large numbers, we line up the units, tens, hundreds and thousands of the numbers. - A n…"

### Row-level review categories and manually authored reasons
_None — all AOs have direct evidence and a reused assessment._

### Per-atomic-objective evidence classification
- `use-of-number-line-ao-draw-number-line` → evidence: **direct** · categories: —
  - linked records: ch05-b009(instruction), ch05-b015-i01(exercise)
  - assessment: reused from `ch05-b015-i01`
- `use-of-number-line-ao-use-number-line` → evidence: **direct** · categories: —
  - linked records: ch05-b011(instruction), ch05-b012(foundation), ch05-b013(instruction), ch05-b014(instruction), ch05-b015-i02(exercise), ch05-b015-i03(exercise), ch05-b016(instruction), ch05-b017(foundation), ch05-b018(worked_example), ch05-b019-i01(exercise), ch05-b019-i02(exercise), ch05-b019-i03(exercise), ch05-b019-i04(exercise), ch05-b024(instruction), ch05-b025(foundation), ch05-b026(worked_example), ch05-b027-i01(exercise), ch05-b027-i02(exercise), ch05-b027-i03(exercise), ch05-b027-i04(exercise), ch05-b028(worked_example)
  - assessment: reused from `ch05-b019-i01`

---

## `jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers`

**Title:** Addition and subtraction of positive and negative integers  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-addition-and-subtraction-addition-and-subtraction-of-positive-and-negative-integers-po01`: Add and subtract positive and negative integers on a number line

### Atomic objectives
- `positive-and-negative-integers-ao-add-on-number-line` [add/apply]: Add positive and negative integers on a number line.
- `positive-and-negative-integers-ao-subtract-on-number-line` [subtract/apply]: Subtract positive and negative integers on a number line.

### Linked textbook records (49 total) — inspected
- `ch05-b007` [exposition] — placed in **shared_foundation**
  - heading: Chapter 5: Addition and subtraction of integers > 5.3 The number line
  - evidence quote: "The set of integers is made up of all the positive and negative whole numbers, including zero. We may represent integers on a number line. This is a straight line, divided into equal segments, that shows the position of…"
- `ch05-b008` [definition] — placed in **shared_foundation**
  - heading: Chapter 5: Addition and subtraction of integers > 5.3 The number line
  - evidence quote: "**integers** Integers are positive and negative whole numbers, including zero.  **number line** A number line is a straight line divided into equal segments, that shows the position of numbers.  **positive numbers** Pos…"
- `ch05-b009` [exposition] — placed in **shared_foundation**
  - heading: Chapter 5: Addition and subtraction of integers > 5.3 The number line
  - evidence quote: "We draw a number line with arrowheads at both ends to show that the line can carry on in both directions forever. Here is an example of a number line:  ![](https://electricbookworks.github.io/siyavula-open-textbooks-ima…"
- `ch05-b010` [note] — placed in **shared_foundation**
  - heading: Chapter 5: Addition and subtraction of integers > 5.3 The number line
  - evidence quote: "A number line can also be drawn vertically. Then the positive numbers lie above zero and the negative numbers lie below zero."
- `ch05-b011` [exposition] — placed in **shared_foundation**
  - heading: Chapter 5: Addition and subtraction of integers > Comparing integers on the number line
  - evidence quote: "Positive and negative numbers are sometimes called **directed numbers**. This is because the sign of the number (positive or negative) tells us in which direction from zero they appear on the number line."
- `ch05-b012` [definition] — placed in **shared_foundation**
  - heading: Chapter 5: Addition and subtraction of integers > Comparing integers on the number line
  - evidence quote: "**directed numbers** Directed numbers are positive and negative numbers. The sign of a directed number tells us in which direction from zero it lies on the number line."
- `ch05-b013` [exposition] — placed in **shared_foundation**
  - heading: Chapter 5: Addition and subtraction of integers > Comparing integers on the number line
  - evidence quote: "The further to the right a number lies on the number line, the larger it is. The further to the left a number lies on the number line, the smaller it is. We use the symbols < and > to show the relationship between two n…"
- `ch05-b014` [note] — placed in **shared_foundation**
  - heading: Chapter 5: Addition and subtraction of integers > Comparing integers on the number line
  - evidence quote: "To help you choose the correct symbol, remember that the symbol must "open up" towards the larger number. The "closed" and smaller end points to the smaller number. This crocodile may also help you remember which symbol…"
- `ch05-b015` [exercise_block] — placed in **excluded**
  - heading: Chapter 5: Addition and subtraction of integers > Comparing integers on the number line > Exercise 5.3: Compare integers
  - evidence quote: "### Exercise 5.3: Compare integers"
- `ch05-b015-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 5: Addition and subtraction of integers > Comparing integers on the number line > Exercise 5.3: Compare integers
  - evidence quote: "### Exercise 5.3: Compare integers  1. Draw a number line showing all the integers from -10 to 10."
- `ch05-b015-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 5: Addition and subtraction of integers > Comparing integers on the number line > Exercise 5.3: Compare integers
  - evidence quote: "### Exercise 5.3: Compare integers  2. Place the correct symbol between each pair of numbers. Use your number line to help you.  a. 1 \square 7 b. 9 \square 6 c. 4 \square 0 d. -4 \square 0 e. 1 \square -2 f. -6 \square…"
- `ch05-b015-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 5: Addition and subtraction of integers > Comparing integers on the number line > Exercise 5.3: Compare integers
  - evidence quote: "### Exercise 5.3: Compare integers  3. Arrange the following lists of numbers as required, using the correct symbol. Use your number line to help you.  a. Arrange from the smallest to the largest: 1;-5;-3; 2;-1 b. Arran…"
- `ch05-b016` [exposition] — placed in **AO:positive-and-negative-integers-ao-add-on-number-line (instruction)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Adding integers
  - evidence quote: "We may use a number line to count. When we count to the right, we count in the positive direction. This is because the numbers become larger as we move to the right on a number line. When we count to the left, we count…"
- `ch05-b017` [note] — placed in **shared_foundation**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Adding integers
  - evidence quote: "Integers may be added in any order. For example, $-1+3$ and $3+(-1)$ give the same answer."
- `ch05-b018` [worked_example] — placed in **AO:positive-and-negative-integers-ao-add-on-number-line (worked_example)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Worked example 5.3: Adding integers using the number line
  - evidence quote: "Use a number line to determine the following: $-5+10$.  Step 1: Draw a number line and find the first number on the line.  The first number is -5.  ![](https://electricbookworks.github.io/siyavula-open-textbooks-images/…"
- `ch05-b019` [exercise_block] — placed in **excluded**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.4: Use a number line to add integers
  - evidence quote: "### Exercise 5.4: Use a number line to add integers  Use number lines to add the following pairs of integers."
- `ch05-b019-i01` [exercise_item] — placed in **AO:positive-and-negative-integers-ao-add-on-number-line (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.4: Use a number line to add integers
  - evidence quote: "### Exercise 5.4: Use a number line to add integers  1. $1+6$"
- `ch05-b019-i02` [exercise_item] — placed in **AO:positive-and-negative-integers-ao-add-on-number-line (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.4: Use a number line to add integers
  - evidence quote: "### Exercise 5.4: Use a number line to add integers  2. $-6+7$"
- `ch05-b019-i03` [exercise_item] — placed in **AO:positive-and-negative-integers-ao-add-on-number-line (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.4: Use a number line to add integers
  - evidence quote: "### Exercise 5.4: Use a number line to add integers  3. $4+(-9)$"
- `ch05-b019-i04` [exercise_item] — placed in **AO:positive-and-negative-integers-ao-add-on-number-line (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.4: Use a number line to add integers
  - evidence quote: "### Exercise 5.4: Use a number line to add integers  4. $-2+(-6)$"
- `ch05-b020` [exposition] — placed in **AO:positive-and-negative-integers-ao-subtract-on-number-line (instruction)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Subtracting integers
  - evidence quote: "There are different ways to think about subtraction. One way is to see it as another form of addition. Subtracting a number is the same as adding the "opposite" of the number. A number and its "opposite" are equal dista…"
- `ch05-b021` [note] — placed in **shared_foundation**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Subtracting integers
  - evidence quote: "The "opposite" of a number referred to above has a special name. It is called the additive inverse of the number. When you add a number and its additive inverse, the answer is zero."
- `ch05-b022` [exposition] — placed in **AO:positive-and-negative-integers-ao-subtract-on-number-line (instruction)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Subtracting integers
  - evidence quote: "The subtraction $6-4$ is the same as $6+(-4)$. Similarly, the subtraction $5-(-1)$ is the same as $5+(+1)$. After writing a subtraction as an addition, you may use the method shown in Worked example 5.3 to add the two n…"
- `ch05-b023` [exercise_block] — placed in **excluded**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.5: Write subtraction as addition
  - evidence quote: "### Exercise 5.5: Write subtraction as addition  Write each subtraction as an addition."
- `ch05-b023-i01` [exercise_item] — placed in **AO:positive-and-negative-integers-ao-subtract-on-number-line (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.5: Write subtraction as addition
  - evidence quote: "### Exercise 5.5: Write subtraction as addition  1. $1-6$"
- `ch05-b023-i02` [exercise_item] — placed in **AO:positive-and-negative-integers-ao-subtract-on-number-line (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.5: Write subtraction as addition
  - evidence quote: "### Exercise 5.5: Write subtraction as addition  2. $-6-7$"
- `ch05-b023-i03` [exercise_item] — placed in **AO:positive-and-negative-integers-ao-subtract-on-number-line (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.5: Write subtraction as addition
  - evidence quote: "### Exercise 5.5: Write subtraction as addition  3. $5-(-2)$"
- `ch05-b023-i04` [exercise_item] — placed in **AO:positive-and-negative-integers-ao-subtract-on-number-line (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.5: Write subtraction as addition
  - evidence quote: "### Exercise 5.5: Write subtraction as addition  4. $-8-(-4)$"
- `ch05-b024` [exposition] — placed in **AO:positive-and-negative-integers-ao-subtract-on-number-line (instruction)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Subtracting integers
  - evidence quote: "Another way is to see subtraction as the difference between two numbers. For example, if you have 7 sweets and you eat 4 sweets, you have $7-4=3$ left. The number of sweets you have left is the difference between the sw…"
- `ch05-b025` [note] — placed in **shared_foundation**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Subtracting integers
  - evidence quote: "Integers cannot be subtracted in any order. For example, $3-1$ and $1-3$ do not give the same answer."
- `ch05-b026` [worked_example] — placed in **AO:positive-and-negative-integers-ao-subtract-on-number-line (worked_example)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Worked example 5.4: Subtracting integers using the number line
  - evidence quote: "Use a number line to determine the following: $-5-3$  Use a number line to determine the following: $-4-(-6)$"
- `ch05-b027` [exercise_block] — placed in **excluded**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.6: Use a number line to subtract integers
  - evidence quote: "### Exercise 5.6: Use a number line to subtract integers  For each pair, use a number line to subtract the second integer from the first one."
- `ch05-b027-i01` [exercise_item] — placed in **AO:positive-and-negative-integers-ao-subtract-on-number-line (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.6: Use a number line to subtract integers
  - evidence quote: "### Exercise 5.6: Use a number line to subtract integers  1. $2-5$"
- `ch05-b027-i02` [exercise_item] — placed in **AO:positive-and-negative-integers-ao-subtract-on-number-line (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.6: Use a number line to subtract integers
  - evidence quote: "### Exercise 5.6: Use a number line to subtract integers  2. $-1-3$"
- `ch05-b027-i03` [exercise_item] — placed in **AO:positive-and-negative-integers-ao-subtract-on-number-line (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.6: Use a number line to subtract integers
  - evidence quote: "### Exercise 5.6: Use a number line to subtract integers  3. $5-(-6)$"
- `ch05-b027-i04` [exercise_item] — placed in **AO:positive-and-negative-integers-ao-subtract-on-number-line (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Exercise 5.6: Use a number line to subtract integers
  - evidence quote: "### Exercise 5.6: Use a number line to subtract integers  4. $-2-(-7)$"
- `ch05-b028` [worked_example] — placed in **AO:positive-and-negative-integers-ao-subtract-on-number-line (worked_example)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.4 Addition and subtraction using the number line > Worked example 5.5: Comparing different methods of subtracting integers
  - evidence quote: "Determine the following: $-4-3$"
- `ch05-b029` [exposition] — placed in **shared_foundation**
  - heading: Chapter 5: Addition and subtraction of integers > 5.5 Practical applications > Thermometers
  - evidence quote: "A thermometer is an instrument we use to measure temperature. Most thermometers we use in everyday life measure the temperature in degrees Celsius $(^\circ \text C)$. The freezing point of water, $0 ^\circ \text C$, is…"
- `ch05-b030` [exposition] — placed in **shared_foundation**
  - heading: Chapter 5: Addition and subtraction of integers > 5.5 Practical applications > Banking
  - evidence quote: "Banks allow people to borrow money from them. When you put money into your bank account, you have a positive bank balance. When you draw money from your bank account, it is subtracted from your balance. If you withdraw…"
- `ch05-b031` [exposition] — placed in **shared_foundation**
  - heading: Chapter 5: Addition and subtraction of integers > 5.5 Practical applications > Movement along the same straight line
  - evidence quote: "When we move along the same straight line, we may use positive and negative numbers to determine our position relative to a starting point. The diagram shows part of a school yard.  ![](https://electricbookworks.github.…"
- `ch05-b032` [exercise_block] — placed in **excluded**
  - heading: Chapter 5: Addition and subtraction of integers > 5.5 Practical applications > Exercise 5.7: Use positive and negative numbers to solve problems.
  - evidence quote: "### Exercise 5.7: Use positive and negative numbers to solve problems."
- `ch05-b032-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 5: Addition and subtraction of integers > 5.5 Practical applications > Exercise 5.7: Use positive and negative numbers to solve problems.
  - evidence quote: "### Exercise 5.7: Use positive and negative numbers to solve problems.  1. Food is taken out of the freezing compartment of a refrigerator. Its temperature changes from -10\space ^\circ \text C to 7\space ^\circ \text C…"
- `ch05-b032-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 5: Addition and subtraction of integers > 5.5 Practical applications > Exercise 5.7: Use positive and negative numbers to solve problems.
  - evidence quote: "### Exercise 5.7: Use positive and negative numbers to solve problems.  2. A piece of meat is at a room temperature of 25\space ^\circ \text C. It is placed in a freezer. The temperature of the meat drops by 40\space ^\…"
- `ch05-b032-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 5: Addition and subtraction of integers > 5.5 Practical applications > Exercise 5.7: Use positive and negative numbers to solve problems.
  - evidence quote: "### Exercise 5.7: Use positive and negative numbers to solve problems.  3. Scientists have worked out that the average temperature on the surface of the Earth is 14\space ^\circ \text C, and that the average temperature…"
- `ch05-b032-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 5: Addition and subtraction of integers > 5.5 Practical applications > Exercise 5.7: Use positive and negative numbers to solve problems.
  - evidence quote: "### Exercise 5.7: Use positive and negative numbers to solve problems.  4. Chioma and Ndidi are sisters. At the start of the school holidays, Chioma owes Ndidi ₦50. Ndidi has another ₦25 that she saved during the term.…"
- `ch05-b032-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 5: Addition and subtraction of integers > 5.5 Practical applications > Exercise 5.7: Use positive and negative numbers to solve problems.
  - evidence quote: "### Exercise 5.7: Use positive and negative numbers to solve problems.  5. A man owes the bank ₦5,500. He deposits ₦6,000, but later withdraws ₦800. Calculate his new bank balance."
- `ch05-b032-i06` [exercise_item] — placed in **review_items**
  - heading: Chapter 5: Addition and subtraction of integers > 5.5 Practical applications > Exercise 5.7: Use positive and negative numbers to solve problems.
  - evidence quote: "### Exercise 5.7: Use positive and negative numbers to solve problems.  6. Oladapo walks east from his house to school. After walking for 750 m, he realizes that he forgot a book at home. He turns around and walks back.…"
- `ch05-b032-i07` [exercise_item] — placed in **review_items**
  - heading: Chapter 5: Addition and subtraction of integers > 5.5 Practical applications > Exercise 5.7: Use positive and negative numbers to solve problems.
  - evidence quote: "### Exercise 5.7: Use positive and negative numbers to solve problems.  7. A girl sits in a tree. She throws a ball straight up into the air. It reaches a height of 1 m above the girl's hand and then falls back. The bal…"
- `ch05-b033` [summary] — placed in **excluded**
  - heading: Chapter 5: Addition and subtraction of integers > 5.6 Summary
  - evidence quote: "- The place value of a digit tells us what the value of that digit is, based on its position in a number. - When we add or subtract large numbers, we line up the units, tens, hundreds and thousands of the numbers. - A n…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch05-b015-i01..i03 are compare/order integer exercises (Exercise 5.3) and ch05-b032-i01..i07 are applied word problems (Exercise 5.7) that live outside the add/subtract-on-number-line AOs.
- **no_reused_assessment**: Both AOs have direct evidence but no reused exercise_item assessment was selected.

### Per-atomic-objective evidence classification
- `positive-and-negative-integers-ao-add-on-number-line` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch05-b016(instruction), ch05-b018(worked_example), ch05-b019-i01(exercise), ch05-b019-i02(exercise), ch05-b019-i03(exercise), ch05-b019-i04(exercise)
  - assessment: _(none anchored)_
- `positive-and-negative-integers-ao-subtract-on-number-line` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch05-b020(instruction), ch05-b022(instruction), ch05-b023-i01(exercise), ch05-b023-i02(exercise), ch05-b023-i03(exercise), ch05-b023-i04(exercise), ch05-b024(instruction), ch05-b026(worked_example), ch05-b027-i01(exercise), ch05-b027-i02(exercise), ch05-b027-i03(exercise), ch05-b027-i04(exercise), ch05-b028(worked_example)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All review_items were inspected. Candidate proposals were added for integer comparison and real-world positive/negative integer problem solving because those records are not add/subtract-on-number-line tasks.

### Candidate atomic objective proposals
- `positive-negative-integers-candidate-ao-compare-integers` [prerequisite; candidate_for_expert_review]
  - proposed objective: Compare integers on a number line.
  - source records: ch05-b015-i01, ch05-b015-i02, ch05-b015-i03
  - closest existing AOs: positive-and-negative-integers-ao-add-on-number-line, positive-and-negative-integers-ao-subtract-on-number-line
  - candidate evidence quote: "Draw a number line showing all the integers from -10 to 10."
  - rationale: The records establish integer order and comparison, which is prerequisite to operations on a number line but not the same operation skill.
- `positive-negative-integers-candidate-ao-use-integers-to-solve-problems` [extension_or_enrichment; candidate_for_expert_review]
  - proposed objective: Use positive and negative integers to solve real-world problems.
  - source records: ch05-b032-i01, ch05-b032-i02, ch05-b032-i03, ch05-b032-i04, ch05-b032-i05, ch05-b032-i06, ch05-b032-i07
  - closest existing AOs: positive-and-negative-integers-ao-add-on-number-line, positive-and-negative-integers-ao-subtract-on-number-line
  - candidate evidence quote: "Use positive and negative numbers to solve problems"
  - rationale: The records apply positive and negative numbers in temperature, height, and money contexts rather than asking for number-line addition/subtraction.

---

## `jss1-math-addition-and-subtraction-everyday-application-of-positive-and-negative-integers`

**Title:** Everyday application of positive and negative integers  
**Status:** `mapped`  
**Row review categories:** _(none — mapped or no-records baseline)_

### Curriculum objectives (source)
- `jss1-math-addition-and-subtraction-everyday-application-of-positive-and-negative-integers-po01`: Interpret positive and negative numbers in everyday activities

### Atomic objectives
- `everyday-application-positive-and-negative-integers-ao-interpret-numbers` [interpret/understand]: Interpret positive and negative numbers in everyday activities.

### Linked textbook records (12 total) — inspected
- `ch05-b029` [exposition] — placed in **AO:everyday-application-positive-and-negative-integers-ao-interpret-numbers (instruction)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.5 Practical applications > Thermometers
  - evidence quote: "A thermometer is an instrument we use to measure temperature. Most thermometers we use in everyday life measure the temperature in degrees Celsius $(^\circ \text C)$. The freezing point of water, $0 ^\circ \text C$, is…"
- `ch05-b030` [exposition] — placed in **AO:everyday-application-positive-and-negative-integers-ao-interpret-numbers (instruction)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.5 Practical applications > Banking
  - evidence quote: "Banks allow people to borrow money from them. When you put money into your bank account, you have a positive bank balance. When you draw money from your bank account, it is subtracted from your balance. If you withdraw…"
- `ch05-b031` [exposition] — placed in **AO:everyday-application-positive-and-negative-integers-ao-interpret-numbers (instruction)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.5 Practical applications > Movement along the same straight line
  - evidence quote: "When we move along the same straight line, we may use positive and negative numbers to determine our position relative to a starting point. The diagram shows part of a school yard.  ![](https://electricbookworks.github.…"
- `ch05-b032` [exercise_block] — placed in **excluded**
  - heading: Chapter 5: Addition and subtraction of integers > 5.5 Practical applications > Exercise 5.7: Use positive and negative numbers to solve problems.
  - evidence quote: "### Exercise 5.7: Use positive and negative numbers to solve problems."
- `ch05-b032-i01` [exercise_item] — placed in **AO:everyday-application-positive-and-negative-integers-ao-interpret-numbers (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.5 Practical applications > Exercise 5.7: Use positive and negative numbers to solve problems.
  - evidence quote: "### Exercise 5.7: Use positive and negative numbers to solve problems.  1. Food is taken out of the freezing compartment of a refrigerator. Its temperature changes from -10\space ^\circ \text C to 7\space ^\circ \text C…"
- `ch05-b032-i02` [exercise_item] — placed in **AO:everyday-application-positive-and-negative-integers-ao-interpret-numbers (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.5 Practical applications > Exercise 5.7: Use positive and negative numbers to solve problems.
  - evidence quote: "### Exercise 5.7: Use positive and negative numbers to solve problems.  2. A piece of meat is at a room temperature of 25\space ^\circ \text C. It is placed in a freezer. The temperature of the meat drops by 40\space ^\…"
- `ch05-b032-i03` [exercise_item] — placed in **AO:everyday-application-positive-and-negative-integers-ao-interpret-numbers (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.5 Practical applications > Exercise 5.7: Use positive and negative numbers to solve problems.
  - evidence quote: "### Exercise 5.7: Use positive and negative numbers to solve problems.  3. Scientists have worked out that the average temperature on the surface of the Earth is 14\space ^\circ \text C, and that the average temperature…"
- `ch05-b032-i04` [exercise_item] — placed in **AO:everyday-application-positive-and-negative-integers-ao-interpret-numbers (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.5 Practical applications > Exercise 5.7: Use positive and negative numbers to solve problems.
  - evidence quote: "### Exercise 5.7: Use positive and negative numbers to solve problems.  4. Chioma and Ndidi are sisters. At the start of the school holidays, Chioma owes Ndidi ₦50. Ndidi has another ₦25 that she saved during the term.…"
- `ch05-b032-i05` [exercise_item] — placed in **AO:everyday-application-positive-and-negative-integers-ao-interpret-numbers (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.5 Practical applications > Exercise 5.7: Use positive and negative numbers to solve problems.
  - evidence quote: "### Exercise 5.7: Use positive and negative numbers to solve problems.  5. A man owes the bank ₦5,500. He deposits ₦6,000, but later withdraws ₦800. Calculate his new bank balance."
- `ch05-b032-i06` [exercise_item] — placed in **AO:everyday-application-positive-and-negative-integers-ao-interpret-numbers (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.5 Practical applications > Exercise 5.7: Use positive and negative numbers to solve problems.
  - evidence quote: "### Exercise 5.7: Use positive and negative numbers to solve problems.  6. Oladapo walks east from his house to school. After walking for 750 m, he realizes that he forgot a book at home. He turns around and walks back.…"
- `ch05-b032-i07` [exercise_item] — placed in **AO:everyday-application-positive-and-negative-integers-ao-interpret-numbers (exercise)**
  - heading: Chapter 5: Addition and subtraction of integers > 5.5 Practical applications > Exercise 5.7: Use positive and negative numbers to solve problems.
  - evidence quote: "### Exercise 5.7: Use positive and negative numbers to solve problems.  7. A girl sits in a tree. She throws a ball straight up into the air. It reaches a height of 1 m above the girl's hand and then falls back. The bal…"
- `ch05-b033` [summary] — placed in **excluded**
  - heading: Chapter 5: Addition and subtraction of integers > 5.6 Summary
  - evidence quote: "- The place value of a digit tells us what the value of that digit is, based on its position in a number. - When we add or subtract large numbers, we line up the units, tens, hundreds and thousands of the numbers. - A n…"

### Row-level review categories and manually authored reasons
_None — all AOs have direct evidence and a reused assessment._

### Per-atomic-objective evidence classification
- `everyday-application-positive-and-negative-integers-ao-interpret-numbers` → evidence: **direct** · categories: —
  - linked records: ch05-b029(instruction), ch05-b030(instruction), ch05-b031(instruction), ch05-b032-i01(exercise), ch05-b032-i02(exercise), ch05-b032-i03(exercise), ch05-b032-i04(exercise), ch05-b032-i05(exercise), ch05-b032-i06(exercise), ch05-b032-i07(exercise)
  - assessment: reused from `ch05-b032-i03`

---

## `jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions`

**Title:** Addition and subtraction of fractions  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-addition-and-subtraction-of-fractions-addition-and-subtraction-of-fractions-po01`: Solve problems on addition and subtraction of fractions

### Atomic objectives
- `addition-and-subtraction-of-fractions-ao-solve-addition-problems` [solve/apply]: Solve problems on addition of fractions.
- `addition-and-subtraction-of-fractions-ao-solve-subtraction-problems` [solve/apply]: Solve problems on subtraction of fractions.

### Linked textbook records (41 total) — inspected
- `ch06-b001` [exposition] — placed in **shared_foundation**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions
  - evidence quote: "In Chapter 4, you learnt that a common fraction is written as two whole numbers, one on top of the other: $\frac{\text{numerator}}{\text{denominator}}$.  - The denominator represents all the parts of a whole. For exampl…"
- `ch06-b002` [exposition] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-addition-problems (instruction)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Adding fractions with the same denominator
  - evidence quote: "Usman and Adamu are at a birthday party. There is a cake that is cut into 4 pieces:  ![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-06-001.png)  Suppose Usman gets $\fra…"
- `ch06-b003` [note] — placed in **shared_foundation**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Adding fractions with the same denominator
  - evidence quote: "Remember that the denominator of a fraction tells us into how many parts a whole is divided. In this case, one whole cake is divided into 4 pieces. Together, the boys have 2 of those pieces."
- `ch06-b004` [exposition] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-addition-problems (instruction)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Adding fractions with the same denominator
  - evidence quote: "In Chapter 4, you learnt how to write a fraction in its simplest form. This is when the numerator and denominator have no common factor.  The simplest form of $\frac{2}{4}$ is $\frac{1}{2}$.  ![](https://electricbookwor…"
- `ch06-b005` [exposition] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-subtraction-problems (instruction)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Subtracting fractions with the same denominator
  - evidence quote: "Suppose another cake arrives at the birthday party that Usman and Adamu are attending. This cake is also cut into 4 pieces. Someone immediately takes a piece, so that only 3 of the 4 pieces are left. The cake may now be…"
- `ch06-b006` [worked_example] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-addition-problems (worked_example)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Worked example 6.1: Adding fractions with the same denominator
  - evidence quote: "Calculate:  $\frac{7}{10}+\frac{1}{10}$"
- `ch06-b007` [worked_example] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-subtraction-problems (worked_example)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Worked example 6.2: Subtracting fractions with the same denominator
  - evidence quote: "Calculate:  $$ \frac{7}{9}-\frac{3}{9} $$"
- `ch06-b008` [exercise_block] — placed in **excluded**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Exercise 6.1: Add and subtract fractions that have the same denominators
  - evidence quote: "### Exercise 6.1: Add and subtract fractions that have the same denominators  Calculate each of the following."
- `ch06-b008-i01` [exercise_item] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-addition-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Exercise 6.1: Add and subtract fractions that have the same denominators
  - evidence quote: "### Exercise 6.1: Add and subtract fractions that have the same denominators  Calculate each of the following.  1. \frac{3}{11}+\frac{5}{11}"
- `ch06-b008-i02` [exercise_item] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-addition-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Exercise 6.1: Add and subtract fractions that have the same denominators
  - evidence quote: "### Exercise 6.1: Add and subtract fractions that have the same denominators  Calculate each of the following.  2. \frac{7}{12}+\frac{3}{12}"
- `ch06-b008-i03` [exercise_item] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-addition-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Exercise 6.1: Add and subtract fractions that have the same denominators
  - evidence quote: "### Exercise 6.1: Add and subtract fractions that have the same denominators  Calculate each of the following.  3. \frac{11}{36}+\frac{13}{36}"
- `ch06-b008-i04` [exercise_item] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-subtraction-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Exercise 6.1: Add and subtract fractions that have the same denominators
  - evidence quote: "### Exercise 6.1: Add and subtract fractions that have the same denominators  Calculate each of the following.  4. \frac{15}{17}-\frac{9}{17}"
- `ch06-b008-i05` [exercise_item] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-subtraction-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Exercise 6.1: Add and subtract fractions that have the same denominators
  - evidence quote: "### Exercise 6.1: Add and subtract fractions that have the same denominators  Calculate each of the following.  5. \frac{19}{20}-\frac{7}{20}"
- `ch06-b008-i06` [exercise_item] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-subtraction-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Exercise 6.1: Add and subtract fractions that have the same denominators
  - evidence quote: "### Exercise 6.1: Add and subtract fractions that have the same denominators  Calculate each of the following.  6. \frac{41}{48}-\frac{5}{48}"
- `ch06-b009` [exposition] — placed in **shared_foundation**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Adding and subtracting fractions with different denominators
  - evidence quote: "Suppose we want to determine the following:  $$ \frac{2}{3}+\frac{1}{2} $$  $$ \frac{2}{3}-\frac{1}{2} $$  \frac{2}{3} of a cake may be represented as:  \frac{1}{2} of a cake may be represented as:  We can divide one ca…"
- `ch06-b010` [note] — placed in **excluded**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Adding and subtracting fractions with different denominators
  - evidence quote: "If necessary, go back to Chapter 4 for information about the lowest common denominator (LCD) of two or more fractions. Revise how find equivalent fractions that all have the LCD as their denominator."
- `ch06-b011` [worked_example] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-addition-problems (worked_example)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Worked example 6.3: Adding fractions with different denominators
  - evidence quote: "Calculate:  $$ \frac{2}{3}+\frac{1}{2} $$"
- `ch06-b012` [worked_example] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-subtraction-problems (worked_example)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Worked example 6.4: Subtracting fractions with different denominators
  - evidence quote: "Calculate:  $$ \frac{2}{3}-\frac{1}{2} $$"
- `ch06-b013` [note] — placed in **shared_foundation**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Adding and subtracting fractions with different denominators
  - evidence quote: "As you get used to adding and subtracting fractions, it will no longer be necessary to draw diagrams. Just be sure to always write out the calculation in full."
- `ch06-b014` [exercise_block] — placed in **excluded**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Exercise 6.2: Add and subtract fractions that have different denominators
  - evidence quote: "### Exercise 6.2: Add and subtract fractions that have different denominators  Calculate each of the following."
- `ch06-b014-i01` [exercise_item] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-addition-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Exercise 6.2: Add and subtract fractions that have different denominators
  - evidence quote: "### Exercise 6.2: Add and subtract fractions that have different denominators  Calculate each of the following.  1. \frac{3}{4}+\frac{1}{8}"
- `ch06-b014-i02` [exercise_item] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-addition-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Exercise 6.2: Add and subtract fractions that have different denominators
  - evidence quote: "### Exercise 6.2: Add and subtract fractions that have different denominators  Calculate each of the following.  2. \frac{2}{3}+\frac{2}{7}"
- `ch06-b014-i03` [exercise_item] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-addition-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Exercise 6.2: Add and subtract fractions that have different denominators
  - evidence quote: "### Exercise 6.2: Add and subtract fractions that have different denominators  Calculate each of the following.  3. \frac{11}{30}+\frac{4}{12}"
- `ch06-b014-i04` [exercise_item] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-addition-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Exercise 6.2: Add and subtract fractions that have different denominators
  - evidence quote: "### Exercise 6.2: Add and subtract fractions that have different denominators  Calculate each of the following.  4. \frac{10}{15}+\frac{8}{20}"
- `ch06-b014-i05` [exercise_item] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-addition-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Exercise 6.2: Add and subtract fractions that have different denominators
  - evidence quote: "### Exercise 6.2: Add and subtract fractions that have different denominators  Calculate each of the following.  5. \frac{1}{8}+\frac{5}{6}+\frac{5}{10}"
- `ch06-b014-i06` [exercise_item] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-subtraction-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Exercise 6.2: Add and subtract fractions that have different denominators
  - evidence quote: "### Exercise 6.2: Add and subtract fractions that have different denominators  Calculate each of the following.  6. \frac{11}{15}-\frac{3}{5}"
- `ch06-b014-i07` [exercise_item] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-subtraction-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Exercise 6.2: Add and subtract fractions that have different denominators
  - evidence quote: "### Exercise 6.2: Add and subtract fractions that have different denominators  Calculate each of the following.  7. \frac{5}{6}-\frac{2}{5}"
- `ch06-b014-i08` [exercise_item] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-subtraction-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Exercise 6.2: Add and subtract fractions that have different denominators
  - evidence quote: "### Exercise 6.2: Add and subtract fractions that have different denominators  Calculate each of the following.  8. \frac{9}{12}-\frac{3}{15}"
- `ch06-b014-i09` [exercise_item] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-subtraction-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Exercise 6.2: Add and subtract fractions that have different denominators
  - evidence quote: "### Exercise 6.2: Add and subtract fractions that have different denominators  Calculate each of the following.  9. \frac{23}{24}-\frac{12}{18}"
- `ch06-b014-i10` [exercise_item] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-subtraction-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Exercise 6.2: Add and subtract fractions that have different denominators
  - evidence quote: "### Exercise 6.2: Add and subtract fractions that have different denominators  Calculate each of the following.  10. \frac{9}{10}-\frac{1}{6}-\frac{2}{15}"
- `ch06-b015` [exposition] — placed in **shared_foundation**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Adding and subtracting mixed numbers
  - evidence quote: "Remember that a mixed number is made up of a whole number and a proper fraction. There are various methods that may be used to add and subtract mixed numbers. It is recommended that you first convert all mixed numbers t…"
- `ch06-b016` [note] — placed in **excluded**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Adding and subtracting mixed numbers
  - evidence quote: "If necessary, go back to Chapter 4 and revise how to convert mixed numbers to improper fractions."
- `ch06-b017` [worked_example] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-addition-problems (worked_example)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Worked example 6.5: Adding mixed numbers
  - evidence quote: "Calculate:  $$ 2\frac{4}{5}+1\frac{2}{3} $$"
- `ch06-b018` [exercise_block] — placed in **excluded**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Exercise 6.3: Add and subtract mixed numbers
  - evidence quote: "### Exercise 6.3: Add and subtract mixed numbers  Calculate each of the following."
- `ch06-b018-i01` [exercise_item] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-addition-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Exercise 6.3: Add and subtract mixed numbers
  - evidence quote: "### Exercise 6.3: Add and subtract mixed numbers  1. $2\frac{1}{6}+1\frac{3}{8}$"
- `ch06-b018-i02` [exercise_item] — placed in **AO:addition-and-subtraction-of-fractions-ao-solve-subtraction-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Exercise 6.3: Add and subtract mixed numbers
  - evidence quote: "### Exercise 6.3: Add and subtract mixed numbers  2. $2\frac{5}{12}-1\frac{3}{28}$"
- `ch06-b018-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 6: Operations with fractions > 6.1 Addition and subtraction of fractions > Exercise 6.3: Add and subtract mixed numbers
  - evidence quote: "### Exercise 6.3: Add and subtract mixed numbers  3. $1\frac{7}{8}+2\frac{3}{10}-3\frac{1}{20}$"
- `ch06-b054-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications > Exercise 6.10: Use operations with fractions to solve problems
  - evidence quote: "### Exercise 6.10: Use operations with fractions to solve problems  1. Chijindum spends $\frac{1}{4}$ of his pocket money on clothes and $\frac{3}{10}$ on sweets. What fraction of his pocket money did he spend altogethe…"
- `ch06-b054-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications > Exercise 6.10: Use operations with fractions to solve problems
  - evidence quote: "### Exercise 6.10: Use operations with fractions to solve problems  5. Talatu decides to share a packet of sweets with her siblings. She gives $\frac{1}{4}$ of the packet to her sister and $\frac{3}{8}$ to her brother.…"
- `ch06-b054-i08` [exercise_item] — placed in **review_items**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications > Exercise 6.10: Use operations with fractions to solve problems
  - evidence quote: "### Exercise 6.10: Use operations with fractions to solve problems  8. Habib goes home after school. He spends a $\frac{1}{5}$ hour having lunch, then watches television for $1\frac{2}{3}$ hours, and then does his homew…"
- `ch06-b055` [summary] — placed in **excluded**
  - heading: Chapter 6: Operations with fractions > 6.6 Summary
  - evidence quote: "- To add or subtract fractions with the same denominator:   - Write down the denominator.   - Then add or subtract the numerators. - To add or subtract fractions with different denominators:   - Find the LCD.   - Find e…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch06-b018-i03 combines addition and subtraction in one expression; ch06-b054-i01/i05/i08 are applied word problems that belong to the word-problems subtopic.
- **no_reused_assessment**: Both AOs have direct exercises but no reused assessment was selected.

### Per-atomic-objective evidence classification
- `addition-and-subtraction-of-fractions-ao-solve-addition-problems` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch06-b002(instruction), ch06-b004(instruction), ch06-b006(worked_example), ch06-b008-i01(exercise), ch06-b008-i02(exercise), ch06-b008-i03(exercise), ch06-b011(worked_example), ch06-b014-i01(exercise), ch06-b014-i02(exercise), ch06-b014-i03(exercise), ch06-b014-i04(exercise), ch06-b014-i05(exercise), ch06-b017(worked_example), ch06-b018-i01(exercise)
  - assessment: _(none anchored)_
- `addition-and-subtraction-of-fractions-ao-solve-subtraction-problems` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch06-b005(instruction), ch06-b007(worked_example), ch06-b008-i04(exercise), ch06-b008-i05(exercise), ch06-b008-i06(exercise), ch06-b012(worked_example), ch06-b014-i06(exercise), ch06-b014-i07(exercise), ch06-b014-i08(exercise), ch06-b014-i09(exercise), ch06-b014-i10(exercise), ch06-b018-i02(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-addition-and-subtraction-of-fractions-word-problems-on-addition-and-subtraction-of-fractions`

**Title:** Word problems on addition and subtraction of fractions  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-addition-and-subtraction-of-fractions-word-problems-on-addition-and-subtraction-of-fractions-po01`: Solve word problems on addition and subtraction of fractions

### Atomic objectives
- `word-problems-addition-and-subtraction-of-fractions-ao-solve-addition-word-problems` [solve/apply]: Solve word problems on addition of fractions.
- `word-problems-addition-and-subtraction-of-fractions-ao-solve-subtraction-word-problems` [solve/apply]: Solve word problems on subtraction of fractions.

### Linked textbook records (6 total) — inspected
- `ch06-b053` [exposition] — placed in **shared_foundation**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications
  - evidence quote: "You can use your knowledge of fractions to solve problems. Here are some hints:  - Remember that the denominator of a fraction tells us how many parts a whole is divided into. The numerator tells us how many of those pa…"
- `ch06-b054` [exercise_block] — placed in **excluded**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications > Exercise 6.10: Use operations with fractions to solve problems
  - evidence quote: "### Exercise 6.10: Use operations with fractions to solve problems"
- `ch06-b054-i01` [exercise_item] — placed in **AO:word-problems-addition-and-subtraction-of-fractions-ao-solve-addition-word-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications > Exercise 6.10: Use operations with fractions to solve problems
  - evidence quote: "### Exercise 6.10: Use operations with fractions to solve problems  1. Chijindum spends $\frac{1}{4}$ of his pocket money on clothes and $\frac{3}{10}$ on sweets. What fraction of his pocket money did he spend altogethe…"
- `ch06-b054-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications > Exercise 6.10: Use operations with fractions to solve problems
  - evidence quote: "### Exercise 6.10: Use operations with fractions to solve problems  4. Only $\frac{9}{10}$ of the Mathematics class came to school on Friday. At the start of the lesson, the principal called $\frac{1}{6}$ of the class t…"
- `ch06-b054-i05` [exercise_item] — placed in **AO:word-problems-addition-and-subtraction-of-fractions-ao-solve-subtraction-word-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications > Exercise 6.10: Use operations with fractions to solve problems
  - evidence quote: "### Exercise 6.10: Use operations with fractions to solve problems  5. Talatu decides to share a packet of sweets with her siblings. She gives $\frac{1}{4}$ of the packet to her sister and $\frac{3}{8}$ to her brother.…"
- `ch06-b054-i08` [exercise_item] — placed in **AO:word-problems-addition-and-subtraction-of-fractions-ao-solve-addition-word-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications > Exercise 6.10: Use operations with fractions to solve problems
  - evidence quote: "### Exercise 6.10: Use operations with fractions to solve problems  8. Habib goes home after school. He spends a $\frac{1}{5}$ hour having lunch, then watches television for $1\frac{2}{3}$ hours, and then does his homew…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch06-b054-i04 word problem's direction (addition, subtraction, or fraction-of-fraction) is not unambiguous and was parked for expert review.
- **no_reused_assessment**: Each AO has direct word-problem exercises but no reused exercise_item assessment was selected.

### Per-atomic-objective evidence classification
- `word-problems-addition-and-subtraction-of-fractions-ao-solve-addition-word-problems` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch06-b054-i01(exercise), ch06-b054-i08(exercise)
  - assessment: _(none anchored)_
- `word-problems-addition-and-subtraction-of-fractions-ao-solve-subtraction-word-problems` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch06-b054-i05(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions`

**Title:** Multiplication of fractions  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-multiplications-and-divisions-of-fractions-multiplication-of-fractions-po01`: Solve problems on multiplication of fractions

### Atomic objectives
- `multiplication-of-fractions-ao-solve-problems` [solve/apply]: Solve problems on multiplication of fractions.

### Linked textbook records (26 total) — inspected
- `ch06-b019` [exposition] — placed in **AO:multiplication-of-fractions-ao-solve-problems (instruction)**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Multiplication: whole number x fraction
  - evidence quote: "You might remember from previous years that multiplication is a form of addition. For example, $5 \times \triangle$ means $\triangle + \triangle + \triangle + \triangle + \triangle$.  In the same way, $5\times\frac{1}{4…"
- `ch06-b020` [worked_example] — placed in **AO:multiplication-of-fractions-ao-solve-problems (worked_example)**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Worked example 6.6: Multiplying: whole number x fraction
  - evidence quote: "Calculate:  $$ 5\times\frac{1}{4} $$"
- `ch06-b021` [exposition] — placed in **AO:multiplication-of-fractions-ao-solve-problems (instruction)**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Multiplication: fraction x whole number
  - evidence quote: "By now you know that $\frac{2}{5}$ of a cake may be represented as follows:  ![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web//ebw-jss1-06-021.png)  Suppose Azubuike ate $\frac{2}{…"
- `ch06-b022` [worked_example] — placed in **AO:multiplication-of-fractions-ao-solve-problems (worked_example)**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Worked example 6.7: Multiplying: fraction x whole number
  - evidence quote: "Calculate:  $$ \frac{2}{5}\times3 $$"
- `ch06-b023` [exercise_block] — placed in **excluded**
  - heading: Chapter 6: Operations with fractions > 6.4 Multiplying fractions and whole numbers > Exercise 6.4: Multiply fractions and whole numbers
  - evidence quote: "### Exercise 6.4: Multiply fractions and whole numbers  Calculate each of the following."
- `ch06-b023-i01` [exercise_item] — placed in **AO:multiplication-of-fractions-ao-solve-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.4 Multiplying fractions and whole numbers > Exercise 6.4: Multiply fractions and whole numbers
  - evidence quote: "### Exercise 6.4: Multiply fractions and whole numbers  Calculate each of the following.  1. $$ 4\times\frac{6}{9} $$"
- `ch06-b023-i02` [exercise_item] — placed in **AO:multiplication-of-fractions-ao-solve-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.4 Multiplying fractions and whole numbers > Exercise 6.4: Multiply fractions and whole numbers
  - evidence quote: "### Exercise 6.4: Multiply fractions and whole numbers  Calculate each of the following.  2. $$ 6\times\frac{3}{10} $$"
- `ch06-b023-i03` [exercise_item] — placed in **AO:multiplication-of-fractions-ao-solve-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.4 Multiplying fractions and whole numbers > Exercise 6.4: Multiply fractions and whole numbers
  - evidence quote: "### Exercise 6.4: Multiply fractions and whole numbers  Calculate each of the following.  3. $$ \frac{3}{8}\times5 $$"
- `ch06-b023-i04` [exercise_item] — placed in **AO:multiplication-of-fractions-ao-solve-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.4 Multiplying fractions and whole numbers > Exercise 6.4: Multiply fractions and whole numbers
  - evidence quote: "### Exercise 6.4: Multiply fractions and whole numbers  Calculate each of the following.  4. $$ \frac{9}{14}\times4 $$"
- `ch06-b024` [note] — placed in **AO:multiplication-of-fractions-ao-solve-problems (instruction)**
  - heading: Chapter 6: Operations with fractions > 6.4 Multiplying fractions and whole numbers > Multiplication: fraction x whole number
  - evidence quote: "Once you understand how to multiply whole numbers and fractions, you may use this short method.  Example: $\frac{2}{7}\times6$  Denominator (stays the same): $\frac{\phantom{00}}{7}$  Numerator: $2\times6=12$  Calculati…"
- `ch06-b025` [exposition] — placed in **AO:multiplication-of-fractions-ao-solve-problems (instruction)**
  - heading: Chapter 6: Operations with fractions > 6.4 Multiplying fractions and whole numbers > Multiplication: fraction x fraction
  - evidence quote: "When we write $\frac{2}{3}\times\frac{3}{4}$, it means two thirds, $\frac{2}{3}$, of three quarters, $\frac{3}{4}$.  By now you know that $\frac{3}{4}$ of a cake may be represented as follows:  ![](https://electricbookw…"
- `ch06-b026` [worked_example] — placed in **AO:multiplication-of-fractions-ao-solve-problems (worked_example)**
  - heading: Chapter 6: Operations with fractions > 6.4 Multiplying fractions and whole numbers > Worked example 6.8: Multiplying using a diagram: fraction x fraction
  - evidence quote: "Calculate:  $$ \frac{2}{3}\times\frac{3}{4} $$"
- `ch06-b027` [exposition] — placed in **AO:multiplication-of-fractions-ao-solve-problems (instruction)**
  - heading: Chapter 6: Operations with fractions > 6.4 Multiplying fractions and whole numbers > Multiplication: fraction x fraction
  - evidence quote: "See whether you notice a pattern when we write the first two lines of the calculation in Step 6 of the previous worked example as follows:  $$ \frac{2}{3}\times\frac{3}{4}=\frac{6}{12} $$  When we multiply two fractions…"
- `ch06-b028` [worked_example] — placed in **AO:multiplication-of-fractions-ao-solve-problems (worked_example)**
  - heading: Chapter 6: Operations with fractions > 6.4 Multiplying fractions and whole numbers > Worked example 6.9: Calculating fraction x fraction directly
  - evidence quote: "Calculate:  $$ \frac{5}{6}\times\frac{3}{8} $$"
- `ch06-b029` [exercise_block] — placed in **excluded**
  - heading: Chapter 6: Operations with fractions > 6.4 Multiplying fractions and whole numbers > Exercise 6.5: Multiply fractions with fractions
  - evidence quote: "### Exercise 6.5: Multiply fractions with fractions"
- `ch06-b029-i01` [exercise_item] — placed in **AO:multiplication-of-fractions-ao-solve-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.4 Multiplying fractions and whole numbers > Exercise 6.5: Multiply fractions with fractions
  - evidence quote: "### Exercise 6.5: Multiply fractions with fractions  1. Use a diagram to determine $\frac{1}{2}\times\frac{2}{5}$."
- `ch06-b029-i02` [exercise_item] — placed in **AO:multiplication-of-fractions-ao-solve-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.4 Multiplying fractions and whole numbers > Exercise 6.5: Multiply fractions with fractions
  - evidence quote: "### Exercise 6.5: Multiply fractions with fractions  2. Calculate each of the following directly.  a. $$ \frac{4}{9}\times\frac{3}{5} $$  b. $$ \frac{6}{7}\times\frac{9}{10} $$  c. $$ \frac{11}{12}\times\frac{4}{5} $$"
- `ch06-b047` [exposition] — placed in **AO:multiplication-of-fractions-ao-solve-problems (instruction)**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Multiplying and dividing mixed numbers
  - evidence quote: "There are various methods that may be used to multiply and divide mixed numbers. It is recommended that you first convert all mixed numbers to improper fractions before you multiply or divide."
- `ch06-b048` [note] — placed in **excluded**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Multiplying and dividing mixed numbers
  - evidence quote: "If necessary, go back to Chapter 4 and revise how to convert mixed numbers to improper fractions."
- `ch06-b049` [exposition] — placed in **AO:multiplication-of-fractions-ao-solve-problems (instruction)**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Simplifying before multiplying
  - evidence quote: "Improper fractions sometimes involve large numbers that are not so easy to multiply. To make things easier, you should try to simplify the numerators and denominators before you multiply them.  Note that the order in wh…"
- `ch06-b052` [exercise_block] — placed in **excluded**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Exercise 6.9: Multiply and divide mixed numbers
  - evidence quote: "### Exercise 6.9: Multiply and divide mixed numbers"
- `ch06-b052-i01` [exercise_item] — placed in **AO:multiplication-of-fractions-ao-solve-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Exercise 6.9: Multiply and divide mixed numbers
  - evidence quote: "### Exercise 6.9: Multiply and divide mixed numbers  1. $5\frac{1}{3}\times2\frac{3}{4}$"
- `ch06-b052-i02` [exercise_item] — placed in **AO:multiplication-of-fractions-ao-solve-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Exercise 6.9: Multiply and divide mixed numbers
  - evidence quote: "### Exercise 6.9: Multiply and divide mixed numbers  2. $3\frac{3}{5}\times1\frac{6}{9}$"
- `ch06-b054-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications > Exercise 6.10: Use operations with fractions to solve problems
  - evidence quote: "### Exercise 6.10: Use operations with fractions to solve problems  2. It takes Adanna $\frac{5}{8}$ of an hour to walk to school. How long will it take her to walk to school, back home and back to school again?"
- `ch06-b054-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications > Exercise 6.10: Use operations with fractions to solve problems
  - evidence quote: "### Exercise 6.10: Use operations with fractions to solve problems  3. In a certain class, $\frac{5}{8}$ of the class are girls and $\frac{9}{10}$ of the girls take Mathematics. Calculate the fraction of the class that…"
- `ch06-b055` [summary] — placed in **excluded**
  - heading: Chapter 6: Operations with fractions > 6.6 Summary
  - evidence quote: "- To add or subtract fractions with the same denominator:   - Write down the denominator.   - Then add or subtract the numerators. - To add or subtract fractions with different denominators:   - Find the LCD.   - Find e…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch06-b054-i02 and ch06-b054-i03 are applied multiplication word problems that belong to the word-problems subtopic.
- **no_reused_assessment**: The AO has direct worked examples and exercises but no reused assessment was selected.

### Per-atomic-objective evidence classification
- `multiplication-of-fractions-ao-solve-problems` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch06-b019(instruction), ch06-b020(worked_example), ch06-b021(instruction), ch06-b022(worked_example), ch06-b023-i01(exercise), ch06-b023-i02(exercise), ch06-b023-i03(exercise), ch06-b023-i04(exercise), ch06-b024(instruction), ch06-b025(instruction), ch06-b026(worked_example), ch06-b027(instruction), ch06-b028(worked_example), ch06-b029-i01(exercise), ch06-b029-i02(exercise), ch06-b047(instruction), ch06-b049(instruction), ch06-b052-i01(exercise), ch06-b052-i02(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions`

**Title:** Division of fractions  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-multiplications-and-divisions-of-fractions-division-of-fractions-po01`: Solve problems on division of fractions

### Atomic objectives
- `division-of-fractions-ao-solve-problems` [solve/apply]: Solve problems on division of fractions.

### Linked textbook records (39 total) — inspected
- `ch06-b030` [exposition] — placed in **AO:division-of-fractions-ao-solve-problems (instruction)**
  - heading: Chapter 6: Operations with fractions > 6.5 Dividing by a fraction > Division: whole number ÷ fraction
  - evidence quote: "Suppose there are 4 cakes available for Oluchi's birthday party. The cakes are quite small, so she wants each person to have $\frac{2}{3}$ of a cake. How will Oluchi know how many people will get cake?  Oluchi must calc…"
- `ch06-b031` [worked_example] — placed in **AO:division-of-fractions-ao-solve-problems (worked_example)**
  - heading: Chapter 6: Operations with fractions > 6.4 Dividing fractions > Worked example 6.10: Dividing using diagrams: whole number ÷ fraction
  - evidence quote: "Calculate:  $$ 4\div\frac{2}{3} $$"
- `ch06-b032` [exposition] — placed in **AO:division-of-fractions-ao-solve-problems (instruction)**
  - heading: Chapter 6: Operations with fractions > 6.4 Dividing fractions > Reciprocals of fractions
  - evidence quote: "Division may be seen as another form of multiplication. Dividing by a fraction is the same as multiplying by the "opposite" of the fraction. The "opposite" of a fraction is called its **reciprocal**. The reciprocal is t…"
- `ch06-b033` [definition] — placed in **AO:division-of-fractions-ao-solve-problems (foundation)**
  - heading: Chapter 6: Operations with fractions > 6.4 Dividing fractions > Reciprocals of fractions
  - evidence quote: "**reciprocal** The "opposite" of a fraction, which we get by swapping the numerator and denominator."
- `ch06-b034` [exposition] — placed in **AO:division-of-fractions-ao-solve-problems (foundation)**
  - heading: Chapter 6: Operations with fractions > 6.4 Dividing fractions > Reciprocals of fractions
  - evidence quote: "Whole numbers also have reciprocals. We may write any whole number as an improper fraction with the denominator 1. For example, $5=\frac{5}{1}$ and $13=\frac{13}{1}$. Now we get the reciprocal by swapping the numerator…"
- `ch06-b035` [note] — placed in **AO:division-of-fractions-ao-solve-problems (foundation)**
  - heading: Chapter 6: Operations with fractions > 6.4 Dividing fractions > Reciprocals of fractions
  - evidence quote: "The reciprocal of a fraction is also called its multiplicative inverse. When you multiply a fraction and its multiplicative inverse, the answer is 1."
- `ch06-b036` [exposition] — placed in **AO:division-of-fractions-ao-solve-problems (instruction)**
  - heading: Chapter 6: Operations with fractions > 6.4 Dividing fractions > Reciprocals of fractions
  - evidence quote: "We may use reciprocals in division that involves fractions."
- `ch06-b037` [worked_example] — placed in **AO:division-of-fractions-ao-solve-problems (worked_example)**
  - heading: Chapter 6: Operations with fractions > 6.4 Dividing fractions > Worked example 6.11: Using a reciprocal to divide: whole number ÷ fraction
  - evidence quote: "Calculate:  $$ 4\div\frac{2}{3} $$"
- `ch06-b038` [exercise_block] — placed in **excluded**
  - heading: Chapter 6: Operations with fractions > 6.4 Dividing fractions > Exercise 6.6: Divide whole numbers by fractions
  - evidence quote: "### Exercise 6.6: Divide whole numbers by fractions  Calculate each of the following."
- `ch06-b038-i01` [exercise_item] — placed in **AO:division-of-fractions-ao-solve-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.4 Dividing fractions > Exercise 6.6: Divide whole numbers by fractions
  - evidence quote: "### Exercise 6.6: Divide whole numbers by fractions  1.  $$ 2\div\frac{1}{6} $$"
- `ch06-b038-i02` [exercise_item] — placed in **AO:division-of-fractions-ao-solve-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.4 Dividing fractions > Exercise 6.6: Divide whole numbers by fractions
  - evidence quote: "### Exercise 6.6: Divide whole numbers by fractions  2.  $$ 7\div\frac{4}{5} $$"
- `ch06-b038-i03` [exercise_item] — placed in **AO:division-of-fractions-ao-solve-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.4 Dividing fractions > Exercise 6.6: Divide whole numbers by fractions
  - evidence quote: "### Exercise 6.6: Divide whole numbers by fractions  3.  $$ 8\div\frac{3}{4} $$"
- `ch06-b039` [exposition] — placed in **AO:division-of-fractions-ao-solve-problems (instruction)**
  - heading: Chapter 6: Operations with fractions > 6.7 Division of fractions > Division: fraction ÷ whole number
  - evidence quote: "At Ifetayo's birthday party, there is only $\frac{3}{4}$ of one cake left. Ifetayo wants to share this equally between her two best friends, so that they can take it home.  The cake that is left may be represented as fo…"
- `ch06-b040` [worked_example] — placed in **AO:division-of-fractions-ao-solve-problems (worked_example)**
  - heading: Chapter 6: Operations with fractions > 6.7 Division of fractions > Worked example 6.12: Dividing using a diagram: fraction ÷ whole number
  - evidence quote: "Calculate: $$ \frac{3}{4}\div2 $$"
- `ch06-b041` [worked_example] — placed in **AO:division-of-fractions-ao-solve-problems (worked_example)**
  - heading: Chapter 6: Operations with fractions > 6.7 Division of fractions > Worked example 6.13: Using a reciprocal to divide: fraction ÷ whole number
  - evidence quote: "Calculate: $$ \frac{3}{4}\div2 $$"
- `ch06-b042` [exercise_block] — placed in **excluded**
  - heading: Chapter 6: Operations with fractions > 6.7 Division of fractions > Exercise 6.7: Divide fractions by whole numbers
  - evidence quote: "### Exercise 6.7: Divide fractions by whole numbers  Calculate each of the following."
- `ch06-b042-i01` [exercise_item] — placed in **AO:division-of-fractions-ao-solve-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.7 Division of fractions > Exercise 6.7: Divide fractions by whole numbers
  - evidence quote: "### Exercise 6.7: Divide fractions by whole numbers  Calculate each of the following.  1. $$ \frac{4}{5}\div6 $$"
- `ch06-b042-i02` [exercise_item] — placed in **AO:division-of-fractions-ao-solve-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.7 Division of fractions > Exercise 6.7: Divide fractions by whole numbers
  - evidence quote: "### Exercise 6.7: Divide fractions by whole numbers  Calculate each of the following.  2. $$ \frac{6}{15}\div4 $$"
- `ch06-b042-i03` [exercise_item] — placed in **AO:division-of-fractions-ao-solve-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.7 Division of fractions > Exercise 6.7: Divide fractions by whole numbers
  - evidence quote: "### Exercise 6.7: Divide fractions by whole numbers  Calculate each of the following.  3. $$ \frac{8}{9}\div 10 $$"
- `ch06-b043` [exposition] — placed in **AO:division-of-fractions-ao-solve-problems (instruction)**
  - heading: Chapter 6: Operations with fractions > 6.7 Division of fractions > Division: fraction ÷ fraction
  - evidence quote: "Remember that there was only $\frac{3}{4}$ of one cake left at Ifetayo's birthday party. Suppose, instead of dividing this between her two best friends, she rather decides to give $\frac{1}{8}$ of the cake to as many pe…"
- `ch06-b044` [worked_example] — placed in **AO:division-of-fractions-ao-solve-problems (worked_example)**
  - heading: Chapter 6: Operations with fractions > 6.7 Division of fractions > Worked example 6.14: Using a diagram to divide: fraction ÷ fraction
  - evidence quote: "Calculate: $$ \frac{3}{4}\div\frac{1}{8} $$"
- `ch06-b045` [worked_example] — placed in **AO:division-of-fractions-ao-solve-problems (worked_example)**
  - heading: Chapter 6: Operations with fractions > 6.7 Division of fractions > Worked example 6.15: Using a reciprocal to divide: fraction ÷ fraction
  - evidence quote: "Calculate: $$ \frac{3}{4}\div\frac{1}{8} $$"
- `ch06-b046` [exercise_block] — placed in **excluded**
  - heading: Chapter 6: Operations with fractions > 6.7 Division of fractions > Exercise 6.8: Divide fractions by fractions
  - evidence quote: "### Exercise 6.8: Divide fractions by fractions  Calculate each of the following."
- `ch06-b046-i01` [exercise_item] — placed in **AO:division-of-fractions-ao-solve-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.7 Division of fractions > Exercise 6.8: Divide fractions by fractions
  - evidence quote: "### Exercise 6.8: Divide fractions by fractions  Calculate each of the following.  1. $$ \frac{3}{7}\div\frac{1}{2} $$"
- `ch06-b046-i02` [exercise_item] — placed in **AO:division-of-fractions-ao-solve-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.7 Division of fractions > Exercise 6.8: Divide fractions by fractions
  - evidence quote: "### Exercise 6.8: Divide fractions by fractions  Calculate each of the following.  2. $$ \frac{10}{13}\div\frac{3}{4} $$"
- `ch06-b046-i03` [exercise_item] — placed in **AO:division-of-fractions-ao-solve-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.7 Division of fractions > Exercise 6.8: Divide fractions by fractions
  - evidence quote: "### Exercise 6.8: Divide fractions by fractions  Calculate each of the following.  3. $$ \frac{12}{15}\div\frac{3}{5} $$"
- `ch06-b047` [exposition] — placed in **AO:division-of-fractions-ao-solve-problems (instruction)**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Multiplying and dividing mixed numbers
  - evidence quote: "There are various methods that may be used to multiply and divide mixed numbers. It is recommended that you first convert all mixed numbers to improper fractions before you multiply or divide."
- `ch06-b048` [note] — placed in **excluded**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Multiplying and dividing mixed numbers
  - evidence quote: "If necessary, go back to Chapter 4 and revise how to convert mixed numbers to improper fractions."
- `ch06-b049` [exposition] — placed in **AO:division-of-fractions-ao-solve-problems (instruction)**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Simplifying before multiplying
  - evidence quote: "Improper fractions sometimes involve large numbers that are not so easy to multiply. To make things easier, you should try to simplify the numerators and denominators before you multiply them.  Note that the order in wh…"
- `ch06-b050` [worked_example] — placed in **AO:division-of-fractions-ao-solve-problems (worked_example)**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Worked example 6.16: Dividing mixed numbers
  - evidence quote: "Calculate:  $$2\frac{5}{8}\div3\frac{3}{4}$$"
- `ch06-b051` [note] — placed in **excluded**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Simplifying before multiplying
  - evidence quote: "If necessary, go back to Chapter 4 and revise how to convert improper fractions to mixed numbers."
- `ch06-b052` [exercise_block] — placed in **excluded**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Exercise 6.9: Multiply and divide mixed numbers
  - evidence quote: "### Exercise 6.9: Multiply and divide mixed numbers"
- `ch06-b052-i03` [exercise_item] — placed in **AO:division-of-fractions-ao-solve-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Exercise 6.9: Multiply and divide mixed numbers
  - evidence quote: "### Exercise 6.9: Multiply and divide mixed numbers  3. $7\frac{1}{8}\div4\frac{3}{4}$"
- `ch06-b052-i04` [exercise_item] — placed in **AO:division-of-fractions-ao-solve-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Exercise 6.9: Multiply and divide mixed numbers
  - evidence quote: "### Exercise 6.9: Multiply and divide mixed numbers  4. $4\frac{1}{6}\div3\frac{8}{9}$"
- `ch06-b052-i05` [exercise_item] — placed in **AO:division-of-fractions-ao-solve-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.2 Multiplication and division of fractions > Exercise 6.9: Multiply and divide mixed numbers
  - evidence quote: "### Exercise 6.9: Multiply and divide mixed numbers  5. $6\frac{3}{10}\div1\frac{4}{5}$"
- `ch06-b054-i06` [exercise_item] — placed in **review_items**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications > Exercise 6.10: Use operations with fractions to solve problems
  - evidence quote: "### Exercise 6.10: Use operations with fractions to solve problems  6. A local store owner buys rice in bags of 50 kg. He then makes up smaller bags to sell. If a small bag is $\frac{6}{15}$ kg, how many small bags can…"
- `ch06-b054-i07` [exercise_item] — placed in **review_items**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications > Exercise 6.10: Use operations with fractions to solve problems
  - evidence quote: "### Exercise 6.10: Use operations with fractions to solve problems  7. There is $\frac{14}{16}$ litre of vegetable oil left in a bottle. A baker must measure this out in cups of $\frac{1}{4}$ litre each. How many cups w…"
- `ch06-b054-i10` [exercise_item] — placed in **review_items**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications > Exercise 6.10: Use operations with fractions to solve problems
  - evidence quote: "### Exercise 6.10: Use operations with fractions to solve problems  10. A bag of garri has a mass of $10\frac{5}{6}$ kg. How many small packets, each with a mass of $2\frac{1}{2}$ kg, can be made up from the bag?"
- `ch06-b055` [summary] — placed in **excluded**
  - heading: Chapter 6: Operations with fractions > 6.6 Summary
  - evidence quote: "- To add or subtract fractions with the same denominator:   - Write down the denominator.   - Then add or subtract the numerators. - To add or subtract fractions with different denominators:   - Find the LCD.   - Find e…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch06-b054-i06/i07/i10 are applied division word problems that belong to the word-problems subtopic.
- **no_reused_assessment**: The AO has direct worked examples and exercises but no reused assessment was selected.

### Per-atomic-objective evidence classification
- `division-of-fractions-ao-solve-problems` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch06-b030(instruction), ch06-b031(worked_example), ch06-b032(instruction), ch06-b033(foundation), ch06-b034(foundation), ch06-b035(foundation), ch06-b036(instruction), ch06-b037(worked_example), ch06-b038-i01(exercise), ch06-b038-i02(exercise), ch06-b038-i03(exercise), ch06-b039(instruction), ch06-b040(worked_example), ch06-b041(worked_example), ch06-b042-i01(exercise), ch06-b042-i02(exercise), ch06-b042-i03(exercise), ch06-b043(instruction), ch06-b044(worked_example), ch06-b045(worked_example), ch06-b046-i01(exercise), ch06-b046-i02(exercise), ch06-b046-i03(exercise), ch06-b047(instruction), ch06-b049(instruction), ch06-b050(worked_example), ch06-b052-i03(exercise), ch06-b052-i04(exercise), ch06-b052-i05(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-multiplications-and-divisions-of-fractions-word-problems-involving-multiplication-and-division-of-fractions`

**Title:** Word problems involving multiplication and division of fractions  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-multiplications-and-divisions-of-fractions-word-problems-involving-multiplication-and-division-of-fractions-po01`: Solve word problems involving multiplication and division of fractions

### Atomic objectives
- `word-problems-multiplication-and-division-of-fractions-ao-solve-multiplication-word-problems` [solve/apply]: Solve word problems involving multiplication of fractions.
- `word-problems-multiplication-and-division-of-fractions-ao-solve-division-word-problems` [solve/apply]: Solve word problems involving division of fractions.

### Linked textbook records (10 total) — inspected
- `ch06-b030` [exposition] — placed in **AO:word-problems-multiplication-and-division-of-fractions-ao-solve-division-word-problems (instruction)**
  - heading: Chapter 6: Operations with fractions > 6.5 Dividing by a fraction > Division: whole number ÷ fraction
  - evidence quote: "Suppose there are 4 cakes available for Oluchi's birthday party. The cakes are quite small, so she wants each person to have $\frac{2}{3}$ of a cake. How will Oluchi know how many people will get cake?  Oluchi must calc…"
- `ch06-b053` [exposition] — placed in **shared_foundation**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications
  - evidence quote: "You can use your knowledge of fractions to solve problems. Here are some hints:  - Remember that the denominator of a fraction tells us how many parts a whole is divided into. The numerator tells us how many of those pa…"
- `ch06-b054` [exercise_block] — placed in **excluded**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications > Exercise 6.10: Use operations with fractions to solve problems
  - evidence quote: "### Exercise 6.10: Use operations with fractions to solve problems"
- `ch06-b054-i02` [exercise_item] — placed in **AO:word-problems-multiplication-and-division-of-fractions-ao-solve-multiplication-word-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications > Exercise 6.10: Use operations with fractions to solve problems
  - evidence quote: "### Exercise 6.10: Use operations with fractions to solve problems  2. It takes Adanna $\frac{5}{8}$ of an hour to walk to school. How long will it take her to walk to school, back home and back to school again?"
- `ch06-b054-i03` [exercise_item] — placed in **AO:word-problems-multiplication-and-division-of-fractions-ao-solve-multiplication-word-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications > Exercise 6.10: Use operations with fractions to solve problems
  - evidence quote: "### Exercise 6.10: Use operations with fractions to solve problems  3. In a certain class, $\frac{5}{8}$ of the class are girls and $\frac{9}{10}$ of the girls take Mathematics. Calculate the fraction of the class that…"
- `ch06-b054-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications > Exercise 6.10: Use operations with fractions to solve problems
  - evidence quote: "### Exercise 6.10: Use operations with fractions to solve problems  4. Only $\frac{9}{10}$ of the Mathematics class came to school on Friday. At the start of the lesson, the principal called $\frac{1}{6}$ of the class t…"
- `ch06-b054-i06` [exercise_item] — placed in **AO:word-problems-multiplication-and-division-of-fractions-ao-solve-division-word-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications > Exercise 6.10: Use operations with fractions to solve problems
  - evidence quote: "### Exercise 6.10: Use operations with fractions to solve problems  6. A local store owner buys rice in bags of 50 kg. He then makes up smaller bags to sell. If a small bag is $\frac{6}{15}$ kg, how many small bags can…"
- `ch06-b054-i07` [exercise_item] — placed in **AO:word-problems-multiplication-and-division-of-fractions-ao-solve-division-word-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications > Exercise 6.10: Use operations with fractions to solve problems
  - evidence quote: "### Exercise 6.10: Use operations with fractions to solve problems  7. There is $\frac{14}{16}$ litre of vegetable oil left in a bottle. A baker must measure this out in cups of $\frac{1}{4}$ litre each. How many cups w…"
- `ch06-b054-i09` [exercise_item] — placed in **AO:word-problems-multiplication-and-division-of-fractions-ao-solve-multiplication-word-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications > Exercise 6.10: Use operations with fractions to solve problems
  - evidence quote: "### Exercise 6.10: Use operations with fractions to solve problems  9. A clothing store offers a discount of 15% on a pair of shoes that originally cost ₦1,500. Calculate the new, discount price."
- `ch06-b054-i10` [exercise_item] — placed in **AO:word-problems-multiplication-and-division-of-fractions-ao-solve-division-word-problems (exercise)**
  - heading: Chapter 6: Operations with fractions > 6.3 Practical applications > Exercise 6.10: Use operations with fractions to solve problems
  - evidence quote: "### Exercise 6.10: Use operations with fractions to solve problems  10. A bag of garri has a mass of $10\frac{5}{6}$ kg. How many small packets, each with a mass of $2\frac{1}{2}$ kg, can be made up from the bag?"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch06-b054-i04 is a subtraction-of-fractions word problem and does not fit either the multiplication or division AO of this subtopic.
- **no_reused_assessment**: Both AOs have direct word-problem exercises but no reused assessment was selected.

### Per-atomic-objective evidence classification
- `word-problems-multiplication-and-division-of-fractions-ao-solve-multiplication-word-problems` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch06-b054-i02(exercise), ch06-b054-i03(exercise), ch06-b054-i09(exercise)
  - assessment: _(none anchored)_
- `word-problems-multiplication-and-division-of-fractions-ao-solve-division-word-problems` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch06-b030(instruction), ch06-b054-i06(exercise), ch06-b054-i07(exercise), ch06-b054-i10(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors`

**Title:** Prime numbers and factors  
**Status:** `needs_review`  
**Row review categories:** no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors-po01`: Identify prime numbers
- `jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors-po02`: Find the factors of a given whole number
- `jss1-math-multiplications-and-divisions-of-fractions-prime-numbers-and-factors-po03`: Express a number as a product of its prime factors

### Atomic objectives
- `prime-numbers-and-factors-ao-identify-prime-numbers` [identify/remember]: Identify prime numbers.
- `prime-numbers-and-factors-ao-find-factors` [find/apply]: Find the factors of a given whole number.
- `prime-numbers-and-factors-ao-express-prime-factors` [express/apply]: Express a number as a product of its prime factors.

### Linked textbook records (28 total) — inspected
- `ch02-b001` [exposition] — placed in **AO:prime-numbers-and-factors-ao-find-factors (instruction)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Factors
  - evidence quote: "A factor is any of the two or more whole numbers we multiply to get a product. For example: $6 \times 2 = 12$. The numbers 6 and 2 are factors of 12.  A factor is also described as a whole number that divides into a lar…"
- `ch02-b002` [definition] — placed in **shared_foundation**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Factors
  - evidence quote: "factor  A factor is a whole number that divides into a larger number without a remainder."
- `ch02-b003` [worked_example] — placed in **AO:prime-numbers-and-factors-ao-find-factors (worked_example)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Worked example 2.1: Factors
  - evidence quote: "Find all the factors of the number 60."
- `ch02-b004` [exercise_block] — placed in **excluded**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.1: Find factors
  - evidence quote: "### Exercise 2.1: Find factors  Find all the factors of the following numbers:"
- `ch02-b004-i01` [exercise_item] — placed in **AO:prime-numbers-and-factors-ao-find-factors (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.1: Find factors
  - evidence quote: "### Exercise 2.1: Find factors  1. 54"
- `ch02-b004-i02` [exercise_item] — placed in **AO:prime-numbers-and-factors-ao-find-factors (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.1: Find factors
  - evidence quote: "### Exercise 2.1: Find factors  2. 39"
- `ch02-b004-i03` [exercise_item] — placed in **AO:prime-numbers-and-factors-ao-find-factors (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.1: Find factors
  - evidence quote: "### Exercise 2.1: Find factors  3. 45"
- `ch02-b005` [exposition] — placed in **AO:prime-numbers-and-factors-ao-identify-prime-numbers (instruction)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Prime factors
  - evidence quote: "The number 3 has only two factors: 1 and 3. Similarly, the number 11 has only two factors: 1 and 11. These are examples of prime numbers."
- `ch02-b006` [definition] — placed in **AO:prime-numbers-and-factors-ao-identify-prime-numbers (foundation)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Prime factors
  - evidence quote: "prime number  A prime number is a number that has only two factors: 1 and the number itself."
- `ch02-b007` [exposition] — placed in **AO:prime-numbers-and-factors-ao-identify-prime-numbers (foundation)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Prime factors
  - evidence quote: "The prime numbers between 1 and 100 are highlighted in the grid below.  ![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-02-001.png)  prime factors These are the factors o…"
- `ch02-b008` [definition] — placed in **AO:prime-numbers-and-factors-ao-identify-prime-numbers (foundation)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Prime factors
  - evidence quote: "prime factor  A prime factor is a factor that is also a prime number."
- `ch02-b009` [worked_example] — placed in **AO:prime-numbers-and-factors-ao-express-prime-factors (worked_example)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Worked example 2.2: Prime factors
  - evidence quote: "Find the prime factors of 80."
- `ch02-b010` [exercise_block] — placed in **excluded**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.2: Express numbers as products of prime factors
  - evidence quote: "### Exercise 2.2: Express numbers as products of prime factors  Express the following numbers as products of prime factors:"
- `ch02-b010-i01` [exercise_item] — placed in **AO:prime-numbers-and-factors-ao-express-prime-factors (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.2: Express numbers as products of prime factors
  - evidence quote: "### Exercise 2.2: Express numbers as products of prime factors  Express the following numbers as products of prime factors:  1. 30"
- `ch02-b010-i02` [exercise_item] — placed in **AO:prime-numbers-and-factors-ao-express-prime-factors (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.2: Express numbers as products of prime factors
  - evidence quote: "### Exercise 2.2: Express numbers as products of prime factors  Express the following numbers as products of prime factors:  2. 140"
- `ch02-b010-i03` [exercise_item] — placed in **AO:prime-numbers-and-factors-ao-express-prime-factors (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.2: Express numbers as products of prime factors
  - evidence quote: "### Exercise 2.2: Express numbers as products of prime factors  Express the following numbers as products of prime factors:  3. 195"
- `ch02-b010-i04` [exercise_item] — placed in **AO:prime-numbers-and-factors-ao-express-prime-factors (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.2: Express numbers as products of prime factors
  - evidence quote: "### Exercise 2.2: Express numbers as products of prime factors  Express the following numbers as products of prime factors:  4. 252"
- `ch02-b010-i05` [exercise_item] — placed in **AO:prime-numbers-and-factors-ao-express-prime-factors (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.2: Express numbers as products of prime factors
  - evidence quote: "### Exercise 2.2: Express numbers as products of prime factors  Express the following numbers as products of prime factors:  5. 297"
- `ch02-b011` [exposition] — placed in **AO:prime-numbers-and-factors-ao-express-prime-factors (instruction)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Index form
  - evidence quote: "Finding and writing down the prime factors of large numbers can become confusing. To make the process easier, we may use continued division and write the prime factors in index form. The index or power of a number tells…"
- `ch02-b012` [definition] — placed in **AO:prime-numbers-and-factors-ao-express-prime-factors (foundation)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Index form
  - evidence quote: "index form Index form tells you how many times to use the same number in a multiplication by writing a superscript next to the number, for example $3^2$ means multiply 3 by 3."
- `ch02-b013` [note] — placed in **AO:prime-numbers-and-factors-ao-express-prime-factors (foundation)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Index form
  - evidence quote: "An index of 1 means a number is not multiplied by itself. Therefore, $2$ and $2^1$ have the same meaning."
- `ch02-b014` [worked_example] — placed in **AO:prime-numbers-and-factors-ao-express-prime-factors (worked_example)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Worked example 2.3: Prime factors in index form
  - evidence quote: "Find the prime factors of 180 and write them in index form."
- `ch02-b015` [exercise_block] — placed in **excluded**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.3: Express numbers as products of prime factors in index form
  - evidence quote: "### Exercise 2.3: Express numbers as products of prime factors in index form  Express the following numbers as prime factors in index form:"
- `ch02-b015-i01` [exercise_item] — placed in **AO:prime-numbers-and-factors-ao-express-prime-factors (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.3: Express numbers as products of prime factors in index form
  - evidence quote: "### Exercise 2.3: Express numbers as products of prime factors in index form  Express the following numbers as prime factors in index form:  1. 60"
- `ch02-b015-i02` [exercise_item] — placed in **AO:prime-numbers-and-factors-ao-express-prime-factors (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.3: Express numbers as products of prime factors in index form
  - evidence quote: "### Exercise 2.3: Express numbers as products of prime factors in index form  Express the following numbers as prime factors in index form:  2. 144"
- `ch02-b015-i03` [exercise_item] — placed in **AO:prime-numbers-and-factors-ao-express-prime-factors (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.3: Express numbers as products of prime factors in index form
  - evidence quote: "### Exercise 2.3: Express numbers as products of prime factors in index form  Express the following numbers as prime factors in index form:  3. 198"
- `ch02-b015-i04` [exercise_item] — placed in **AO:prime-numbers-and-factors-ao-express-prime-factors (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.3: Express numbers as products of prime factors in index form
  - evidence quote: "### Exercise 2.3: Express numbers as products of prime factors in index form  Express the following numbers as prime factors in index form:  4. 300"
- `ch02-b015-i05` [exercise_item] — placed in **AO:prime-numbers-and-factors-ao-express-prime-factors (exercise)**
  - heading: Chapter 2: Highest common factor and lowest common multiple > 2.1 Highest common factor > Exercise 2.3: Express numbers as products of prime factors in index form
  - evidence quote: "### Exercise 2.3: Express numbers as products of prime factors in index form  Express the following numbers as prime factors in index form:  5. 3 375"

### Row-level review categories and manually authored reasons
- **no_reused_assessment**: identify-prime-numbers AO has direct instruction (ch02-b005, b006, b007, b008) but no exercise_item is linked, so no reused assessment is possible. find-factors and express-prime-factors AOs have exercises but no reused assessment was anchored either.

### Per-atomic-objective evidence classification
- `prime-numbers-and-factors-ao-identify-prime-numbers` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch02-b005(instruction), ch02-b006(foundation), ch02-b007(foundation), ch02-b008(foundation)
  - assessment: _(none anchored)_
- `prime-numbers-and-factors-ao-find-factors` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch02-b001(instruction), ch02-b003(worked_example), ch02-b004-i01(exercise), ch02-b004-i02(exercise), ch02-b004-i03(exercise)
  - assessment: _(none anchored)_
- `prime-numbers-and-factors-ao-express-prime-factors` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch02-b009(worked_example), ch02-b010-i01(exercise), ch02-b010-i02(exercise), ch02-b010-i03(exercise), ch02-b010-i04(exercise), ch02-b010-i05(exercise), ch02-b011(instruction), ch02-b012(foundation), ch02-b013(foundation), ch02-b014(worked_example), ch02-b015-i01(exercise), ch02-b015-i02(exercise), ch02-b015-i03(exercise), ch02-b015-i04(exercise), ch02-b015-i05(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-estimation-estimation-of-dimensions-and-distances`

**Title:** Estimation of dimensions and distances  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, ao_no_evidence, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-estimation-estimation-of-dimensions-and-distances-po01`: Estimate the dimensions and distances within the school

### Atomic objectives
- `estimation-of-dimensions-and-distances-ao-estimate-dimensions` [estimate/apply]: Estimate the dimensions within the school.
- `estimation-of-dimensions-and-distances-ao-estimate-distances` [estimate/apply]: Estimate the distances within the school.

### Linked textbook records (27 total) — inspected
- `ch07-b001` [exposition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation
  - evidence quote: "**Estimation** is the process of making a guess about the size or cost of something, without doing the actual measurement or calculation. Estimations are sometimes needed because we do not have all the facts, or because…"
- `ch07-b002` [definition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation
  - evidence quote: "**estimation** Estimation is the process of making a guess without doing the actual measurement or calculation."
- `ch07-b003` [exposition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Estimating distances and dimensions
  - evidence quote: "A **distance** can be described as the length of the space between two points. An example of a distance is the length of the path between the door of the classroom and the door to the principal's office.  The **dimensio…"
- `ch07-b004` [definition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Estimating distances and dimensions
  - evidence quote: "**distance** Distance is the length of the space between two points.  **dimensions** The dimensions of an object are the measurable lengths that we use to determine the size of the object, such as its length, breadth an…"
- `ch07-b005` [exposition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Estimating distances and dimensions
  - evidence quote: "When we estimate distances and dimensions, it is important to use the correct unit of measurement. The **SI unit** for length is the metre. A length of one metre (1 m) is more or less equal to:  - the height of a 6-year…"
- `ch07-b006` [definition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Estimating distances and dimensions
  - evidence quote: "**SI unit** An SI unit is a basic unit of measurement that forms part of the International System of Units."
- `ch07-b007` [worked_example] — placed in **AO:estimation-of-dimensions-and-distances-ao-estimate-dimensions (worked_example)**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Worked example 7.1: Evaluating an estimation of a dimension
  - evidence quote: "Adebankole is 14 years old. He estimated his own height as 160 cm. Evaluate his estimation."
- `ch07-b008` [exercise_block] — placed in **excluded**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.1: Estimate distances and dimensions in your classroom
  - evidence quote: "### Exercise 7.1: Estimate distances and dimensions in your classroom  Estimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measu…"
- `ch07-b008-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.1: Estimate distances and dimensions in your classroom
  - evidence quote: "### Exercise 7.1: Estimate distances and dimensions in your classroom  Estimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measu…"
- `ch07-b008-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.1: Estimate distances and dimensions in your classroom
  - evidence quote: "### Exercise 7.1: Estimate distances and dimensions in your classroom  Estimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measu…"
- `ch07-b008-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.1: Estimate distances and dimensions in your classroom
  - evidence quote: "### Exercise 7.1: Estimate distances and dimensions in your classroom  Estimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measu…"
- `ch07-b008-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.1: Estimate distances and dimensions in your classroom
  - evidence quote: "### Exercise 7.1: Estimate distances and dimensions in your classroom  Estimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measu…"
- `ch07-b008-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.1: Estimate distances and dimensions in your classroom
  - evidence quote: "### Exercise 7.1: Estimate distances and dimensions in your classroom  Estimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measu…"
- `ch07-b008-i06` [exercise_item] — placed in **review_items**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.1: Estimate distances and dimensions in your classroom
  - evidence quote: "### Exercise 7.1: Estimate distances and dimensions in your classroom  Estimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measu…"
- `ch07-b008-i07` [exercise_item] — placed in **review_items**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.1: Estimate distances and dimensions in your classroom
  - evidence quote: "### Exercise 7.1: Estimate distances and dimensions in your classroom  Estimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measu…"
- `ch07-b008-i08` [exercise_item] — placed in **review_items**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.1: Estimate distances and dimensions in your classroom
  - evidence quote: "### Exercise 7.1: Estimate distances and dimensions in your classroom  Estimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measu…"
- `ch07-b008-i09` [exercise_item] — placed in **review_items**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.1: Estimate distances and dimensions in your classroom
  - evidence quote: "### Exercise 7.1: Estimate distances and dimensions in your classroom  Estimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measu…"
- `ch07-b008-i10` [exercise_item] — placed in **review_items**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.1: Estimate distances and dimensions in your classroom
  - evidence quote: "### Exercise 7.1: Estimate distances and dimensions in your classroom  Estimate the following distances and dimensions. Include an appropriate unit of measurement in each case. Then use a ruler, metre rule or tape measu…"
- `ch07-b009` [exercise_block] — placed in **excluded**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.2: Estimate everyday distances and dimensions
  - evidence quote: "### Exercise 7.2: Estimate everyday distances and dimensions  Estimate the following distances and dimensions by deciding which one of the options a) to d) is the most correct."
- `ch07-b009-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.2: Estimate everyday distances and dimensions
  - evidence quote: "### Exercise 7.2: Estimate everyday distances and dimensions  Estimate the following distances and dimensions by deciding which one of the options a) to d) is the most correct.  1. Diameter of a 50 kobo coin a) 5 mm b)…"
- `ch07-b009-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.2: Estimate everyday distances and dimensions
  - evidence quote: "### Exercise 7.2: Estimate everyday distances and dimensions  Estimate the following distances and dimensions by deciding which one of the options a) to d) is the most correct.  2. Length of a ₦10 note a) 20 mm b) 1.5 c…"
- `ch07-b009-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.2: Estimate everyday distances and dimensions
  - evidence quote: "### Exercise 7.2: Estimate everyday distances and dimensions  Estimate the following distances and dimensions by deciding which one of the options a) to d) is the most correct.  3. Height of a standard door a) 450 mm b)…"
- `ch07-b009-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.2: Estimate everyday distances and dimensions
  - evidence quote: "### Exercise 7.2: Estimate everyday distances and dimensions  Estimate the following distances and dimensions by deciding which one of the options a) to d) is the most correct.  4. Maximum length of a standard football…"
- `ch07-b009-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.2: Estimate everyday distances and dimensions
  - evidence quote: "### Exercise 7.2: Estimate everyday distances and dimensions  Estimate the following distances and dimensions by deciding which one of the options a) to d) is the most correct.  5. Shortest driving distance from Murtala…"
- `ch07-b038-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.9: Evaluate test answers
  - evidence quote: "### Exercise 7.9: Evaluate test answers  3. The width of the classroom is 90 m."
- `ch07-b041-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.10: Use estimation and approximation to solve problems
  - evidence quote: "### Exercise 7.10: Use estimation and approximation to solve problems  3. A student's steps are 60 cm long. He takes 8,315 steps from his front door to the school gate. Approximately how far does he live from the school?"
- `ch07-b042` [summary] — placed in **excluded**
  - heading: Chapter 7: Estimation and approximation > 7.4 Summary
  - evidence quote: "- Estimation is the process of making a guess about the size or cost of something, without doing the actual measurement or calculation. - Distance is the length of the space between two points. - The dimensions of an ob…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch07-b008-i01..i10 and ch07-b009-i01..i05 (Exercises 7.1 and 7.2) ask for estimates that may target dimension or distance depending on the object; direction is not unambiguous.
- **ao_no_evidence**: estimate-distances AO has zero record_links: ch07-b007 worked example evaluates an estimation of a dimension (height), and the dimension/distance items were not individually assigned.
- **no_reused_assessment**: estimate-dimensions AO has a worked example but no reused exercise_item assessment.

### Per-atomic-objective evidence classification
- `estimation-of-dimensions-and-distances-ao-estimate-dimensions` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch07-b007(worked_example)
  - assessment: _(none anchored)_
- `estimation-of-dimensions-and-distances-ao-estimate-distances` → evidence: **none** · categories: ao_no_evidence
  - linked records: _(none)_
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-estimation-estimation-of-capacity-and-mass-of-objects`

**Title:** Estimation of capacity and mass of objects  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-estimation-estimation-of-capacity-and-mass-of-objects-po01`: Estimate the capacity and mass of given objects

### Atomic objectives
- `estimation-of-capacity-and-mass-of-objects-ao-estimate-capacity` [estimate/apply]: Estimate the capacity of given objects.
- `estimation-of-capacity-and-mass-of-objects-ao-estimate-mass` [estimate/apply]: Estimate the mass of given objects.

### Linked textbook records (41 total) — inspected
- `ch07-b001` [exposition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation
  - evidence quote: "**Estimation** is the process of making a guess about the size or cost of something, without doing the actual measurement or calculation. Estimations are sometimes needed because we do not have all the facts, or because…"
- `ch07-b002` [definition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation
  - evidence quote: "**estimation** Estimation is the process of making a guess without doing the actual measurement or calculation."
- `ch07-b010` [exposition] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-capacity (instruction)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Capacity
  - evidence quote: "Volume is the amount of space occupied by an object or the amount of space inside a container. The amount of liquid that a container can hold is called the capacity of the container."
- `ch07-b011` [definition] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-capacity (foundation)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Capacity
  - evidence quote: "**capacity** The amount of liquid that a container can hold is called the capacity of the container."
- `ch07-b012` [exposition] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-capacity (instruction)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Capacity
  - evidence quote: "The SI unit for capacity is the litre. A capacity of one litre (1 L) is more or less equal to:  - six cups of tea - a carton of milk - three cans of soft drink.  Other units of measurement used often are multiples of te…"
- `ch07-b013` [worked_example] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-capacity (worked_example)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Capacity > Worked example 7.2: Evaluating an estimation of capacity
  - evidence quote: "Amaka is feeling sick. The doctor gives her a bottle of medicine. She estimates that the capacity of the bottle is 250 cl. Evaluate her estimation."
- `ch07-b014` [exercise_block] — placed in **excluded**
  - heading: Chapter 7: Estimation and approximation > 7.2 Capacity > Exercise 7.3: Estimate capacity of containers
  - evidence quote: "### Exercise 7.3: Estimate capacity of containers  You might use the containers listed below at school or at home. Estimate the capacity of the containers. Include an appropriate unit of measurement in each case. Then u…"
- `ch07-b014-i01` [exercise_item] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-capacity (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Capacity > Exercise 7.3: Estimate capacity of containers
  - evidence quote: "### Exercise 7.3: Estimate capacity of containers  You might use the containers listed below at school or at home. Estimate the capacity of the containers. Include an appropriate unit of measurement in each case. Then u…"
- `ch07-b014-i02` [exercise_item] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-capacity (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Capacity > Exercise 7.3: Estimate capacity of containers
  - evidence quote: "### Exercise 7.3: Estimate capacity of containers  You might use the containers listed below at school or at home. Estimate the capacity of the containers. Include an appropriate unit of measurement in each case. Then u…"
- `ch07-b014-i03` [exercise_item] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-capacity (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Capacity > Exercise 7.3: Estimate capacity of containers
  - evidence quote: "### Exercise 7.3: Estimate capacity of containers  You might use the containers listed below at school or at home. Estimate the capacity of the containers. Include an appropriate unit of measurement in each case. Then u…"
- `ch07-b014-i04` [exercise_item] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-capacity (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Capacity > Exercise 7.3: Estimate capacity of containers
  - evidence quote: "### Exercise 7.3: Estimate capacity of containers  You might use the containers listed below at school or at home. Estimate the capacity of the containers. Include an appropriate unit of measurement in each case. Then u…"
- `ch07-b014-i05` [exercise_item] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-capacity (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Capacity > Exercise 7.3: Estimate capacity of containers
  - evidence quote: "### Exercise 7.3: Estimate capacity of containers  You might use the containers listed below at school or at home. Estimate the capacity of the containers. Include an appropriate unit of measurement in each case. Then u…"
- `ch07-b015` [exercise_block] — placed in **excluded**
  - heading: Chapter 7: Estimation and approximation > 7.2 Capacity > Exercise 7.4: Estimate capacity of everyday containers
  - evidence quote: "### Exercise 7.4: Estimate capacity of everyday containers  Estimate the capacity of the following containers by deciding which one of the options a) to d) is the most correct."
- `ch07-b015-i01` [exercise_item] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-capacity (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Capacity > Exercise 7.4: Estimate capacity of everyday containers
  - evidence quote: "### Exercise 7.4: Estimate capacity of everyday containers  Estimate the capacity of the following containers by deciding which one of the options a) to d) is the most correct.  1. Milk tin a) 3 cl b) 25 ml c) 300 cl d)…"
- `ch07-b015-i02` [exercise_item] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-capacity (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Capacity > Exercise 7.4: Estimate capacity of everyday containers
  - evidence quote: "### Exercise 7.4: Estimate capacity of everyday containers  Estimate the capacity of the following containers by deciding which one of the options a) to d) is the most correct.  2. Kerosene tin a) 1.5 kl b) 7 ml c) 2 L…"
- `ch07-b015-i03` [exercise_item] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-capacity (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Capacity > Exercise 7.4: Estimate capacity of everyday containers
  - evidence quote: "### Exercise 7.4: Estimate capacity of everyday containers  Estimate the capacity of the following containers by deciding which one of the options a) to d) is the most correct.  3. Water bucket a) 750 cl b) 35 cl c) 550…"
- `ch07-b015-i04` [exercise_item] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-capacity (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Capacity > Exercise 7.4: Estimate capacity of everyday containers
  - evidence quote: "### Exercise 7.4: Estimate capacity of everyday containers  Estimate the capacity of the following containers by deciding which one of the options a) to d) is the most correct.  4. Petrol tank of a small car a) 850 ml b…"
- `ch07-b015-i05` [exercise_item] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-capacity (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Capacity > Exercise 7.4: Estimate capacity of everyday containers
  - evidence quote: "### Exercise 7.4: Estimate capacity of everyday containers  Estimate the capacity of the following containers by deciding which one of the options a) to d) is the most correct.  5. Petrol tanker (large truck that transp…"
- `ch07-b016` [exposition] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-mass (instruction)**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Estimate mass
  - evidence quote: "The mass of an object is a measure of how much matter is in that object. It tells us how heavy or how light the object is."
- `ch07-b017` [definition] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-mass (foundation)**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Estimate mass
  - evidence quote: "mass  The mass of an object is a measure of how much matter is in an object."
- `ch07-b018` [exposition] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-mass (instruction)**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Estimate mass
  - evidence quote: "The SI unit for mass is the gram. A mass of one gram (1 g) is more or less equal to:  - a small paperclip - one millilitre of pure water - a quarter teaspoon of sugar.  Other units of measurement used often are multiple…"
- `ch07-b019` [worked_example] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-mass (worked_example)**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Worked example 7.3: Evaluating an estimation of mass
  - evidence quote: "Danladi's mother sends his to the corner shop to buy a cup of rice. He carries it home in a small bag. He estimates that the mass of the rice is 50 g. Evaluate his estimation."
- `ch07-b020` [exercise_block] — placed in **excluded**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.5: Estimate mass of objects
  - evidence quote: "### Exercise 7.5: Estimate mass of objects  Estimate the mass of the following objects. Include an appropriate unit of measurement in each case. Then use an electronic balance from the science laboratory or a kitchen sc…"
- `ch07-b020-i01` [exercise_item] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-mass (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.5: Estimate mass of objects
  - evidence quote: "### Exercise 7.5: Estimate mass of objects  1. Your eraser"
- `ch07-b020-i02` [exercise_item] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-mass (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.5: Estimate mass of objects
  - evidence quote: "### Exercise 7.5: Estimate mass of objects  2. One of your pens"
- `ch07-b020-i03` [exercise_item] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-mass (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.5: Estimate mass of objects
  - evidence quote: "### Exercise 7.5: Estimate mass of objects  3. Your thinnest textbook"
- `ch07-b020-i04` [exercise_item] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-mass (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.5: Estimate mass of objects
  - evidence quote: "### Exercise 7.5: Estimate mass of objects  4. Full box of chalk"
- `ch07-b020-i05` [exercise_item] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-mass (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.5: Estimate mass of objects
  - evidence quote: "### Exercise 7.5: Estimate mass of objects  5. Volleyball"
- `ch07-b021` [exercise_block] — placed in **excluded**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.6: Estimate mass of everyday objects
  - evidence quote: "### Exercise 7.6: Estimate mass of everyday objects  Estimate the mass of the following objects by deciding which one of the options a) to d) is the most correct."
- `ch07-b021-i01` [exercise_item] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-mass (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.6: Estimate mass of everyday objects
  - evidence quote: "### Exercise 7.6: Estimate mass of everyday objects  1. 50 kobo coin    a. 8 mg    b. 5.5 g    c. 250 g    d. 1.5 kg"
- `ch07-b021-i02` [exercise_item] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-mass (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.6: Estimate mass of everyday objects
  - evidence quote: "### Exercise 7.6: Estimate mass of everyday objects  2. Packet of sugar cubes    a. 475 g    b. 45 g    c. 550 mg    d. 45 kg"
- `ch07-b021-i03` [exercise_item] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-mass (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.6: Estimate mass of everyday objects
  - evidence quote: "### Exercise 7.6: Estimate mass of everyday objects  3. Basketball    a. 950 mg    b. 45 g    c. 625 g    d. 12 kg"
- `ch07-b021-i04` [exercise_item] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-mass (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.6: Estimate mass of everyday objects
  - evidence quote: "### Exercise 7.6: Estimate mass of everyday objects  4. A male teenager    a. 250 kg    b. 70 kg    c. 950 g    d. 0.5 t"
- `ch07-b021-i05` [exercise_item] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-mass (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation > Exercise 7.6: Estimate mass of everyday objects
  - evidence quote: "### Exercise 7.6: Estimate mass of everyday objects  5. An adult cow    a. 65 kg    b. 700 kg    c. 50 t    d. 850 g"
- `ch07-b038-i02` [exercise_item] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-capacity (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.9: Evaluate test answers
  - evidence quote: "### Exercise 7.9: Evaluate test answers  2. The capacity of a teaspoon is 5 L."
- `ch07-b038-i04` [exercise_item] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-mass (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.9: Evaluate test answers
  - evidence quote: "### Exercise 7.9: Evaluate test answers  4. The mass of a woman is 27 kg."
- `ch07-b038-i05` [exercise_item] — placed in **AO:estimation-of-capacity-and-mass-of-objects-ao-estimate-mass (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.9: Evaluate test answers
  - evidence quote: "### Exercise 7.9: Evaluate test answers  5. $50\text{ mg}=50,000\text{ g}$"
- `ch07-b041-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.10: Use estimation and approximation to solve problems
  - evidence quote: "### Exercise 7.10: Use estimation and approximation to solve problems  5. A soft drink bottle has a capacity of 33 cl. At the factory, the bottles are filled from a container with a capacity of 21.3 kl. Approximately ho…"
- `ch07-b041-i06` [exercise_item] — placed in **review_items**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.10: Use estimation and approximation to solve problems
  - evidence quote: "### Exercise 7.10: Use estimation and approximation to solve problems  6. A 5 L container of vegetable oil is sold at ₦2,899. Approximately how much money do you need for 31 L of vegetable oil?"
- `ch07-b041-i07` [exercise_item] — placed in **review_items**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.10: Use estimation and approximation to solve problems
  - evidence quote: "### Exercise 7.10: Use estimation and approximation to solve problems  7. A man gets 17 bowls of rice from a sack of 51.15 kg. What is the approximate mass of rice needed for 5 bowls?"
- `ch07-b042` [summary] — placed in **excluded**
  - heading: Chapter 7: Estimation and approximation > 7.4 Summary
  - evidence quote: "- Estimation is the process of making a guess about the size or cost of something, without doing the actual measurement or calculation. - Distance is the length of the space between two points. - The dimensions of an ob…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch07-b041-i05/i06/i07 are applied estimation word problems whose direction (capacity vs mass) is not unambiguous and belong to the QR-involving-estimation subtopic.
- **no_reused_assessment**: Both AOs have direct exercises (and assessments could be reused from the b014/b015/b020/b021 series) but no reused exercise_item assessment was selected here.

### Per-atomic-objective evidence classification
- `estimation-of-capacity-and-mass-of-objects-ao-estimate-capacity` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch07-b010(instruction), ch07-b011(foundation), ch07-b012(instruction), ch07-b013(worked_example), ch07-b014-i01(exercise), ch07-b014-i02(exercise), ch07-b014-i03(exercise), ch07-b014-i04(exercise), ch07-b014-i05(exercise), ch07-b015-i01(exercise), ch07-b015-i02(exercise), ch07-b015-i03(exercise), ch07-b015-i04(exercise), ch07-b015-i05(exercise), ch07-b038-i02(exercise)
  - assessment: _(none anchored)_
- `estimation-of-capacity-and-mass-of-objects-ao-estimate-mass` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch07-b016(instruction), ch07-b017(foundation), ch07-b018(instruction), ch07-b019(worked_example), ch07-b020-i01(exercise), ch07-b020-i02(exercise), ch07-b020-i03(exercise), ch07-b020-i04(exercise), ch07-b020-i05(exercise), ch07-b021-i01(exercise), ch07-b021-i02(exercise), ch07-b021-i03(exercise), ch07-b021-i04(exercise), ch07-b021-i05(exercise), ch07-b038-i04(exercise), ch07-b038-i05(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-estimation-estimation-of-other-things-eg-age-time-etc`

**Title:** Estimation of other things e.g. age, time, etc  
**Status:** `needs_review`  
**Row review categories:** prerequisite_only_evidence, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-estimation-estimation-of-other-things-eg-age-time-etc-po01`: Estimate other things in day to day activities

### Atomic objectives
- `estimation-of-other-things-ao-estimate-other-things` [estimate/apply]: Estimate other things in day to day activities.

### Linked textbook records (2 total) — inspected
- `ch07-b001` [exposition] — placed in **AO:estimation-of-other-things-ao-estimate-other-things (instruction)**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation
  - evidence quote: "**Estimation** is the process of making a guess about the size or cost of something, without doing the actual measurement or calculation. Estimations are sometimes needed because we do not have all the facts, or because…"
- `ch07-b002` [definition] — placed in **AO:estimation-of-other-things-ao-estimate-other-things (foundation)**
  - heading: Chapter 7: Estimation and approximation > 7.1 Estimation
  - evidence quote: "**estimation** Estimation is the process of making a guess without doing the actual measurement or calculation."

### Row-level review categories and manually authored reasons
- **prerequisite_only_evidence**: The two linked records (ch07-b001 estimation introduction and ch07-b002 definition of estimation) introduce estimation in general; they do not directly teach or exemplify estimating 'other things in day-to-day activities' such as age or time.
- **no_reused_assessment**: No exercise_item is linked to this subtopic, so no reused assessment is possible.

### Per-atomic-objective evidence classification
- `estimation-of-other-things-ao-estimate-other-things` → evidence: **prerequisite_only** · categories: prerequisite_only_evidence, no_reused_assessment
  - linked records: ch07-b001(instruction), ch07-b002(foundation)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-estimation-quantitative-reasoning-involving-estimation`

**Title:** Quantitative reasoning involving estimation  
**Status:** `mapped`  
**Row review categories:** _(none — mapped or no-records baseline)_

### Curriculum objectives (source)
- `jss1-math-estimation-quantitative-reasoning-involving-estimation-po01`: Solve problems on quantitative reasoning in estimation

### Atomic objectives
- `quantitative-reasoning-involving-estimation-ao-solve-problems` [solve/apply]: Solve problems on quantitative reasoning in estimation.

### Linked textbook records (2 total) — inspected
- `ch07-b038` [exercise_block] — placed in **excluded**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.9: Evaluate test answers
  - evidence quote: "### Exercise 7.9: Evaluate test answers  Each of the following is an incorrect answer that was given by a student in a test. Say what mistake the student made and give the correct answer."
- `ch07-b041-i03` [exercise_item] — placed in **AO:quantitative-reasoning-involving-estimation-ao-solve-problems (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.10: Use estimation and approximation to solve problems
  - evidence quote: "### Exercise 7.10: Use estimation and approximation to solve problems  3. A student's steps are 60 cm long. He takes 8,315 steps from his front door to the school gate. Approximately how far does he live from the school?"

### Row-level review categories and manually authored reasons
_None — all AOs have direct evidence and a reused assessment._

### Per-atomic-objective evidence classification
- `quantitative-reasoning-involving-estimation-ao-solve-problems` → evidence: **direct** · categories: —
  - linked records: ch07-b041-i03(exercise)
  - assessment: reused from `ch07-b041-i03`

---

## `jss1-math-approximation-significant-figures-and-decimal-places`

**Title:** Significant figures and decimal places  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, ao_no_evidence, no_reused_assessment, curriculum_textbook_mismatch

### Curriculum objectives (source)
- `jss1-math-approximation-significant-figures-and-decimal-places-po01`: Determine the degree of accuracy of numbers
- `jss1-math-approximation-significant-figures-and-decimal-places-po02`: Round numbers to given significant figures
- `jss1-math-approximation-significant-figures-and-decimal-places-po03`: Round numbers to given decimal places

### Atomic objectives
- `significant-figures-and-decimal-places-ao-determine-degree-of-accuracy` [determine/apply]: Determine the degree of accuracy of numbers.
- `significant-figures-and-decimal-places-ao-round-significant-figures` [round/apply]: Round numbers to given significant figures.
- `significant-figures-and-decimal-places-ao-round-decimal-places` [round/apply]: Round numbers to given decimal places.

### Linked textbook records (10 total) — inspected
- `ch01-b017` [exposition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Place value in decimal fractions
  - evidence quote: "For decimal fractions, the place values we work with are $\frac{1}{10}, \frac{1}{100}, \frac{1}{1,000}$ and $\frac{1}{10,000}$. They are called **tenths**, **hundredths**, **thousandths** and **ten thousandths**.  These…"
- `ch01-b018` [definition] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Place value in decimal fractions
  - evidence quote: "**tenths** Tenths are the decimal fractions 0.1; 0.2; 0.3; 0.4; 0.5; 0.6; 0.7; 0.8; 0.9 in the base ten number system.  **hundredths** Hundredths are the decimal fractions 0.01; 0.02; 0.03; 0.04; 0.05; 0.06; 0.07; 0.08;…"
- `ch01-b019` [worked_example] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Worked example 1.2: Finding place value in decimal numbers
  - evidence quote: "Write down the place values of all the non-zero digits in the following number: 73,025.048"
- `ch01-b020` [note] — placed in **shared_foundation**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Place value in decimal fractions
  - evidence quote: "As you can see, we do not give the place value of the zeroes in a number, because 0 multiplied by anything equals 0. So the place value of any 0 will always be 0. The zeroes have to be included in a number to show the p…"
- `ch01-b021` [exercise_block] — placed in **excluded**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Exercise 1.3: Determine place value in numbers with decimal fractions
  - evidence quote: "### Exercise 1.3: Determine place value in numbers with decimal fractions  Write down the place value of the given digit in each case."
- `ch01-b021-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Exercise 1.3: Determine place value in numbers with decimal fractions
  - evidence quote: "### Exercise 1.3: Determine place value in numbers with decimal fractions  Write down the place value of the given digit in each case.  1. Give the values of the digits 5 and 8 in the number 5,023.08"
- `ch01-b021-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Exercise 1.3: Determine place value in numbers with decimal fractions
  - evidence quote: "### Exercise 1.3: Determine place value in numbers with decimal fractions  Write down the place value of the given digit in each case.  2. Give the values of the digits 1 and 4 in the number 75.1804"
- `ch01-b021-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Exercise 1.3: Determine place value in numbers with decimal fractions
  - evidence quote: "### Exercise 1.3: Determine place value in numbers with decimal fractions  Write down the place value of the given digit in each case.  3. Give the values of the digits 9 and 7 in the number 70,546.009"
- `ch01-b021-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Exercise 1.3: Determine place value in numbers with decimal fractions
  - evidence quote: "### Exercise 1.3: Determine place value in numbers with decimal fractions  Write down the place value of the given digit in each case.  4. Give the two values of the digit 5 in the number 10,503.54"
- `ch01-b021-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 1: Numbers big and small > 1.2 Place value > Exercise 1.3: Determine place value in numbers with decimal fractions
  - evidence quote: "### Exercise 1.3: Determine place value in numbers with decimal fractions  Write down the place value of the given digit in each case.  5. Give the three values of the digit 9 in the number 99,148.319"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch01-b019 worked example and ch01-b021-i01..i05 exercises are place-value determination tasks in decimal fractions, which are prerequisite to rounding to decimal places but not the AO skill.
- **ao_no_evidence**: All three AOs (degree of accuracy, significant figures, decimal places) have zero accepted record_links; none of the linked records teaches rounding to significant figures or decimal places, or quantifies degree of accuracy.
- **no_reused_assessment**: No AO has a reused exercise_item assessment.
- **curriculum_textbook_mismatch**: The curriculum AOs ask for rounding to significant figures and decimal places, but the textbook chapter 1 records linked here only cover decimal place-value identification; the rounding-to-sig-figs/decimal-places teaching is absent from the linked corpus.

### Per-atomic-objective evidence classification
- `significant-figures-and-decimal-places-ao-determine-degree-of-accuracy` → evidence: **none** · categories: ao_no_evidence, curriculum_textbook_mismatch
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `significant-figures-and-decimal-places-ao-round-significant-figures` → evidence: **none** · categories: ao_no_evidence, curriculum_textbook_mismatch
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `significant-figures-and-decimal-places-ao-round-decimal-places` → evidence: **none** · categories: ao_no_evidence, curriculum_textbook_mismatch
  - linked records: _(none)_
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-approximation-rounding-to-nearest-tenth-hundredth-and-thousandth`

**Title:** Rounding to nearest tenth, hundredth and thousandth  
**Status:** `no_records`  
**Row review categories:** corpus_gap

### Curriculum objectives (source)
- `jss1-math-approximation-rounding-to-nearest-tenth-hundredth-and-thousandth-po01`: Round numbers to the nearest tenth, hundredth and thousandth

### Atomic objectives
- `rounding-to-nearest-tenth-hundredth-and-thousandth-ao-round-tenth` [round/apply]: Round numbers to the nearest tenth.
- `rounding-to-nearest-tenth-hundredth-and-thousandth-ao-round-hundredth` [round/apply]: Round numbers to the nearest hundredth.
- `rounding-to-nearest-tenth-hundredth-and-thousandth-ao-round-thousandth` [round/apply]: Round numbers to the nearest thousandth.

### Linked textbook records (0 total) — inspected
_No textbook records are linked to this subtopic (corpus_gap)._

### Row-level review categories and manually authored reasons
- **corpus_gap**: No textbook records are linked to this subtopic in the linked corpus.

### Per-atomic-objective evidence classification
- `rounding-to-nearest-tenth-hundredth-and-thousandth-ao-round-tenth` → evidence: **none** · categories: corpus_gap
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `rounding-to-nearest-tenth-hundredth-and-thousandth-ao-round-hundredth` → evidence: **none** · categories: corpus_gap
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `rounding-to-nearest-tenth-hundredth-and-thousandth-ao-round-thousandth` → evidence: **none** · categories: corpus_gap
  - linked records: _(none)_
  - assessment: _(none anchored)_

---

## `jss1-math-approximation-approximating-values-of-addition-and-subtraction`

**Title:** Approximating values of addition and subtraction  
**Status:** `mapped`  
**Row review categories:** _(none — mapped or no-records baseline)_

### Curriculum objectives (source)
- `jss1-math-approximation-approximating-values-of-addition-and-subtraction-po01`: Approximate answers to addition and subtraction problems to a given degree of accuracy

### Atomic objectives
- `approximating-values-of-addition-and-subtraction-ao-approximate-addition` [approximate/apply]: Approximate answers to addition problems to a given degree of accuracy.
- `approximating-values-of-addition-and-subtraction-ao-approximate-subtraction` [approximate/apply]: Approximate answers to subtraction problems to a given degree of accuracy.

### Linked textbook records (11 total) — inspected
- `ch07-b022` [exposition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off
  - evidence quote: "An approximate answer is almost correct, but not exact. Approximation is the process of using rounding to quickly determine a fairly accurate answer to a calculation. Approximation is very useful in situations where you…"
- `ch07-b023` [definition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off
  - evidence quote: "approximation  Approximation is the process of using rounding to quickly determine a fairly accurate answer to a calculation."
- `ch07-b034` [exposition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Using approximation in calculations
  - evidence quote: "The aim of using approximation in calculations is to round off numbers to values that you can work with more easily when you are using mental arithmetic. When we work with approximations, we use the symbol $\approx$ ins…"
- `ch07-b036` [exercise_block] — placed in **excluded**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Exercise 7.8: Calculate approximate values
  - evidence quote: "### Exercise 7.8: Calculate approximate values  Determine the approximate answer to each of the following."
- `ch07-b036-i01` [exercise_item] — placed in **AO:approximating-values-of-addition-and-subtraction-ao-approximate-addition (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Exercise 7.8: Calculate approximate values
  - evidence quote: "### Exercise 7.8: Calculate approximate values  1. $$38+52$$"
- `ch07-b036-i02` [exercise_item] — placed in **AO:approximating-values-of-addition-and-subtraction-ao-approximate-addition (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Exercise 7.8: Calculate approximate values
  - evidence quote: "### Exercise 7.8: Calculate approximate values  2. $$543+127$$"
- `ch07-b036-i03` [exercise_item] — placed in **AO:approximating-values-of-addition-and-subtraction-ao-approximate-subtraction (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Exercise 7.8: Calculate approximate values
  - evidence quote: "### Exercise 7.8: Calculate approximate values  3. $$69-23$$"
- `ch07-b036-i04` [exercise_item] — placed in **AO:approximating-values-of-addition-and-subtraction-ao-approximate-subtraction (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Exercise 7.8: Calculate approximate values
  - evidence quote: "### Exercise 7.8: Calculate approximate values  4. $$285-162$$"
- `ch07-b036-i05` [exercise_item] — placed in **AO:approximating-values-of-addition-and-subtraction-ao-approximate-subtraction (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Exercise 7.8: Calculate approximate values
  - evidence quote: "### Exercise 7.8: Calculate approximate values  5. $$1,403-582$$"
- `ch07-b039` [exposition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications
  - evidence quote: "Keep the following in mind when you use approximation in calculations:  - Round off to the smallest multiple of ten that will allow an easy calculation. For example, if you round off to the nearest ten, your answer will…"
- `ch07-b042` [summary] — placed in **excluded**
  - heading: Chapter 7: Estimation and approximation > 7.4 Summary
  - evidence quote: "- Estimation is the process of making a guess about the size or cost of something, without doing the actual measurement or calculation. - Distance is the length of the space between two points. - The dimensions of an ob…"

### Row-level review categories and manually authored reasons
_None — all AOs have direct evidence and a reused assessment._

### Per-atomic-objective evidence classification
- `approximating-values-of-addition-and-subtraction-ao-approximate-addition` → evidence: **direct** · categories: —
  - linked records: ch07-b036-i01(exercise), ch07-b036-i02(exercise)
  - assessment: reused from `ch07-b036-i02`
- `approximating-values-of-addition-and-subtraction-ao-approximate-subtraction` → evidence: **direct** · categories: —
  - linked records: ch07-b036-i03(exercise), ch07-b036-i04(exercise), ch07-b036-i05(exercise)
  - assessment: reused from `ch07-b036-i05`

---

## `jss1-math-approximation-approximating-results-of-multiplication-and-division`

**Title:** Approximating results of multiplication and division  
**Status:** `needs_review`  
**Row review categories:** no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-approximation-approximating-results-of-multiplication-and-division-po01`: Approximate answers to multiplication and division problems to a given degree of accuracy

### Atomic objectives
- `approximating-results-of-multiplication-and-division-ao-approximate-multiplication` [approximate/apply]: Approximate answers to multiplication problems to a given degree of accuracy.
- `approximating-results-of-multiplication-and-division-ao-approximate-division` [approximate/apply]: Approximate answers to division problems to a given degree of accuracy.

### Linked textbook records (12 total) — inspected
- `ch07-b022` [exposition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off
  - evidence quote: "An approximate answer is almost correct, but not exact. Approximation is the process of using rounding to quickly determine a fairly accurate answer to a calculation. Approximation is very useful in situations where you…"
- `ch07-b023` [definition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off
  - evidence quote: "approximation  Approximation is the process of using rounding to quickly determine a fairly accurate answer to a calculation."
- `ch07-b034` [exposition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Using approximation in calculations
  - evidence quote: "The aim of using approximation in calculations is to round off numbers to values that you can work with more easily when you are using mental arithmetic. When we work with approximations, we use the symbol $\approx$ ins…"
- `ch07-b035` [worked_example] — placed in **AO:approximating-results-of-multiplication-and-division-ao-approximate-multiplication (worked_example)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Worked example 7.7: Using approximation in calculations
  - evidence quote: "Determine the approximate value of $475\times 17$."
- `ch07-b036` [exercise_block] — placed in **excluded**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Exercise 7.8: Calculate approximate values
  - evidence quote: "### Exercise 7.8: Calculate approximate values  Determine the approximate answer to each of the following."
- `ch07-b036-i06` [exercise_item] — placed in **AO:approximating-results-of-multiplication-and-division-ao-approximate-multiplication (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Exercise 7.8: Calculate approximate values
  - evidence quote: "### Exercise 7.8: Calculate approximate values  6. $$13 \times 72$$"
- `ch07-b036-i07` [exercise_item] — placed in **AO:approximating-results-of-multiplication-and-division-ao-approximate-multiplication (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Exercise 7.8: Calculate approximate values
  - evidence quote: "### Exercise 7.8: Calculate approximate values  7. $$233 \times 36$$"
- `ch07-b036-i08` [exercise_item] — placed in **AO:approximating-results-of-multiplication-and-division-ao-approximate-multiplication (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Exercise 7.8: Calculate approximate values
  - evidence quote: "### Exercise 7.8: Calculate approximate values  8. $$7\frac{1}{5} \times 2\frac{7}{8}$$"
- `ch07-b036-i09` [exercise_item] — placed in **AO:approximating-results-of-multiplication-and-division-ao-approximate-division (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Exercise 7.8: Calculate approximate values
  - evidence quote: "### Exercise 7.8: Calculate approximate values  9. $$825 \div 41$$"
- `ch07-b036-i10` [exercise_item] — placed in **AO:approximating-results-of-multiplication-and-division-ao-approximate-division (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Exercise 7.8: Calculate approximate values
  - evidence quote: "### Exercise 7.8: Calculate approximate values  10. $$3,612 \div 123$$"
- `ch07-b039` [exposition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications
  - evidence quote: "Keep the following in mind when you use approximation in calculations:  - Round off to the smallest multiple of ten that will allow an easy calculation. For example, if you round off to the nearest ten, your answer will…"
- `ch07-b042` [summary] — placed in **excluded**
  - heading: Chapter 7: Estimation and approximation > 7.4 Summary
  - evidence quote: "- Estimation is the process of making a guess about the size or cost of something, without doing the actual measurement or calculation. - Distance is the length of the space between two points. - The dimensions of an ob…"

### Row-level review categories and manually authored reasons
- **no_reused_assessment**: Both AOs have direct exercises (multiplication: ch07-b036-i06, i07, i08; division: ch07-b036-i09, i10) but no reused exercise_item assessment was anchored.

### Per-atomic-objective evidence classification
- `approximating-results-of-multiplication-and-division-ao-approximate-multiplication` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch07-b035(worked_example), ch07-b036-i06(exercise), ch07-b036-i07(exercise), ch07-b036-i08(exercise)
  - assessment: _(none anchored)_
- `approximating-results-of-multiplication-and-division-ao-approximate-division` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch07-b036-i09(exercise), ch07-b036-i10(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000`

**Title:** Rounding off numbers to the nearest 10, 100 and 1000  
**Status:** `needs_review`  
**Row review categories:** no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-approximation-rounding-off-numbers-to-the-nearest-10-100-and-1000-po01`: Round numbers to the nearest 10, 100, and 1000

### Atomic objectives
- `rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-10` [round/apply]: Round numbers to the nearest 10.
- `rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-100` [round/apply]: Round numbers to the nearest 100.
- `rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-1000` [round/apply]: Round numbers to the nearest 1000.

### Linked textbook records (23 total) — inspected
- `ch07-b022` [exposition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off
  - evidence quote: "An approximate answer is almost correct, but not exact. Approximation is the process of using rounding to quickly determine a fairly accurate answer to a calculation. Approximation is very useful in situations where you…"
- `ch07-b023` [definition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off
  - evidence quote: "approximation  Approximation is the process of using rounding to quickly determine a fairly accurate answer to a calculation."
- `ch07-b024` [exposition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Rounding off numbers
  - evidence quote: "When we round off numbers, we make them less exact, but easier to work with. We usually round off a number to a specific multiple of 10."
- `ch07-b025` [definition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Rounding off numbers
  - evidence quote: "rounding off Rounding off is the process of making a number less exact but easier to work with, by adjusting it to a specific multiple of 10."
- `ch07-b026` [exposition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Rounding off numbers
  - evidence quote: "When we round off a number to a specific multiple of 10, we have to identify the digit that represents the multiple, and then determine whether than digit remains the same or increases by one."
- `ch07-b027` [worked_example] — placed in **AO:rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-10 (worked_example)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Worked example 7.4: Rounding off to the nearest ten
  - evidence quote: "A smartphone is advertised for ₦47,689. Round off this number to the nearest ten."
- `ch07-b028` [note] — placed in **AO:rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-10 (instruction)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Rounding off numbers
  - evidence quote: "If we round off 47,689 to the nearest ten, we actually want to know whether this number is closer to 47,680 or 47,690. The number 47,689 is 1 unit away from 47,690 and 9 units away from 47,680. That is why it is rounded…"
- `ch07-b029` [worked_example] — placed in **AO:rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-100 (worked_example)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Worked example 7.5: Rounding off to the nearest hundred
  - evidence quote: "A handbag is advertised for ₦2,950. Round off this number to the nearest hundred."
- `ch07-b030` [note] — placed in **AO:rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-100 (instruction)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Rounding off numbers
  - evidence quote: "If we round off 2,950 to the nearest hundred, we actually want to know whether this number is closer to 2,900 or 3,000. The number 2,950 is exactly halfway between 2,900 and 3,000. By convention, we round up to the high…"
- `ch07-b031` [worked_example] — placed in **AO:rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-1000 (worked_example)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Worked example 7.6: Rounding off to the nearest thousand
  - evidence quote: "On a specific day, the population of Nigeria is 201,195,431. Round off this number to the nearest thousand."
- `ch07-b032` [note] — placed in **AO:rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-1000 (instruction)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Rounding off numbers
  - evidence quote: "If we round off 201,195,431 to the nearest thousand, we actually want to know whether this number is closer to 201,195,000 or 201,196,000. The number 201,195,431 is 431 units away from 201,195,000 and 569 units away fro…"
- `ch07-b033` [exercise_block] — placed in **excluded**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Exercise 7.7: Round off numbers
  - evidence quote: "### Exercise 7.7: Round off numbers  Round off each of the following numbers to the required multiple of 10."
- `ch07-b033-i01` [exercise_item] — placed in **AO:rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-10 (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Exercise 7.7: Round off numbers
  - evidence quote: "### Exercise 7.7: Round off numbers  1. 26,548 to the nearest ten"
- `ch07-b033-i02` [exercise_item] — placed in **AO:rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-100 (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Exercise 7.7: Round off numbers
  - evidence quote: "### Exercise 7.7: Round off numbers  2. 48,849 to the nearest hundred"
- `ch07-b033-i03` [exercise_item] — placed in **AO:rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-1000 (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Exercise 7.7: Round off numbers
  - evidence quote: "### Exercise 7.7: Round off numbers  3. 37,627 to the nearest thousand"
- `ch07-b033-i04` [exercise_item] — placed in **AO:rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-1000 (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Exercise 7.7: Round off numbers
  - evidence quote: "### Exercise 7.7: Round off numbers  4. 58,503 to the nearest thousand"
- `ch07-b033-i05` [exercise_item] — placed in **AO:rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-1000 (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Exercise 7.7: Round off numbers
  - evidence quote: "### Exercise 7.7: Round off numbers  5. 29,618 to the nearest thousand"
- `ch07-b033-i06` [exercise_item] — placed in **AO:rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-1000 (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Exercise 7.7: Round off numbers
  - evidence quote: "### Exercise 7.7: Round off numbers  6. 5,319,432 to the nearest thousand"
- `ch07-b033-i07` [exercise_item] — placed in **AO:rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-1000 (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Exercise 7.7: Round off numbers
  - evidence quote: "### Exercise 7.7: Round off numbers  7. 19,553 to the nearest thousand"
- `ch07-b033-i08` [exercise_item] — placed in **AO:rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-100 (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Exercise 7.7: Round off numbers
  - evidence quote: "### Exercise 7.7: Round off numbers  8. 2,905,047 to the nearest hundred"
- `ch07-b033-i09` [exercise_item] — placed in **AO:rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-10 (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Exercise 7.7: Round off numbers
  - evidence quote: "### Exercise 7.7: Round off numbers  9. 5,095 to the nearest ten"
- `ch07-b033-i10` [exercise_item] — placed in **AO:rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-100 (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off > Exercise 7.7: Round off numbers
  - evidence quote: "### Exercise 7.7: Round off numbers  10. 512,909,050 to the nearest hundred"
- `ch07-b042` [summary] — placed in **excluded**
  - heading: Chapter 7: Estimation and approximation > 7.4 Summary
  - evidence quote: "- Estimation is the process of making a guess about the size or cost of something, without doing the actual measurement or calculation. - Distance is the length of the space between two points. - The dimensions of an ob…"

### Row-level review categories and manually authored reasons
- **no_reused_assessment**: All three rounding AOs now have direct exercises distributed per item's explicit rounding target (ch07-b033-i01 'to the nearest ten', i02 'to the nearest hundred', i03 'to the nearest thousand', etc.) but no reused exercise_item assessment was selected.

### Per-atomic-objective evidence classification
- `rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-10` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch07-b027(worked_example), ch07-b028(instruction), ch07-b033-i01(exercise), ch07-b033-i09(exercise)
  - assessment: _(none anchored)_
- `rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-100` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch07-b029(worked_example), ch07-b030(instruction), ch07-b033-i02(exercise), ch07-b033-i08(exercise), ch07-b033-i10(exercise)
  - assessment: _(none anchored)_
- `rounding-off-numbers-to-the-nearest-10-100-and-1000-ao-round-nearest-1000` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch07-b031(worked_example), ch07-b032(instruction), ch07-b033-i03(exercise), ch07-b033-i04(exercise), ch07-b033-i05(exercise), ch07-b033-i06(exercise), ch07-b033-i07(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-approximation-application-of-approximation-in-everyday-life`

**Title:** Application of approximation in everyday life  
**Status:** `mapped`  
**Row review categories:** _(none — mapped or no-records baseline)_

### Curriculum objectives (source)
- `jss1-math-approximation-application-of-approximation-in-everyday-life-po01`: Apply approximation involving basic operations in everyday life activities

### Atomic objectives
- `application-of-approximation-in-everyday-life-ao-apply-approximation` [apply/apply]: Apply approximation involving basic operations in everyday life activities.

### Linked textbook records (16 total) — inspected
- `ch07-b022` [exposition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off
  - evidence quote: "An approximate answer is almost correct, but not exact. Approximation is the process of using rounding to quickly determine a fairly accurate answer to a calculation. Approximation is very useful in situations where you…"
- `ch07-b023` [definition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off
  - evidence quote: "approximation  Approximation is the process of using rounding to quickly determine a fairly accurate answer to a calculation."
- `ch07-b037` [exposition] — placed in **AO:application-of-approximation-in-everyday-life-ao-apply-approximation (instruction)**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications
  - evidence quote: "The advantages of being able to estimate and approximate have been mentioned already. This section provides more opportunity for you to practise."
- `ch07-b038` [exercise_block] — placed in **excluded**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.9: Evaluate test answers
  - evidence quote: "### Exercise 7.9: Evaluate test answers  Each of the following is an incorrect answer that was given by a student in a test. Say what mistake the student made and give the correct answer."
- `ch07-b038-i01` [exercise_item] — placed in **AO:application-of-approximation-in-everyday-life-ao-apply-approximation (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.9: Evaluate test answers
  - evidence quote: "### Exercise 7.9: Evaluate test answers  1. The cost of 50 rulers at ₦10 each is ₦5,000."
- `ch07-b039` [exposition] — placed in **AO:application-of-approximation-in-everyday-life-ao-apply-approximation (instruction)**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications
  - evidence quote: "Keep the following in mind when you use approximation in calculations:  - Round off to the smallest multiple of ten that will allow an easy calculation. For example, if you round off to the nearest ten, your answer will…"
- `ch07-b040` [worked_example] — placed in **AO:application-of-approximation-in-everyday-life-ao-apply-approximation (worked_example)**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Worked example 7.8: Using approximation in calculations
  - evidence quote: "A shop owner has to choose the supplier from which she will order sugar cubes. One supplier offers 50 $\times$ 450 g packs of sugar cubes at ₦19,599. Another supplier offers 20 $\times$ 450 g packs of sugar cubes at ₦5,…"
- `ch07-b041` [exercise_block] — placed in **excluded**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.10: Use estimation and approximation to solve problems
  - evidence quote: "### Exercise 7.10: Use estimation and approximation to solve problems"
- `ch07-b041-i01` [exercise_item] — placed in **AO:application-of-approximation-in-everyday-life-ao-apply-approximation (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.10: Use estimation and approximation to solve problems
  - evidence quote: "### Exercise 7.10: Use estimation and approximation to solve problems  1. A litre of petrol costs ₦153. What is the approximate cost of filling up a small car with a tank of 52 L?"
- `ch07-b041-i02` [exercise_item] — placed in **AO:application-of-approximation-in-everyday-life-ao-apply-approximation (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.10: Use estimation and approximation to solve problems
  - evidence quote: "### Exercise 7.10: Use estimation and approximation to solve problems  2. A fabric shop has a special offer of ₦7,475 for 9.75 m of Ankara print. Give the approximate cost per metre."
- `ch07-b041-i04` [exercise_item] — placed in **AO:application-of-approximation-in-everyday-life-ao-apply-approximation (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.10: Use estimation and approximation to solve problems
  - evidence quote: "### Exercise 7.10: Use estimation and approximation to solve problems  4. A university student rents a flat at ₦82,250 per month. She works out that her rent for the year is going to be ₦98,700 and lets her mother know.…"
- `ch07-b041-i06` [exercise_item] — placed in **AO:application-of-approximation-in-everyday-life-ao-apply-approximation (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.10: Use estimation and approximation to solve problems
  - evidence quote: "### Exercise 7.10: Use estimation and approximation to solve problems  6. A 5 L container of vegetable oil is sold at ₦2,899. Approximately how much money do you need for 31 L of vegetable oil?"
- `ch07-b041-i08` [exercise_item] — placed in **AO:application-of-approximation-in-everyday-life-ao-apply-approximation (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.10: Use estimation and approximation to solve problems
  - evidence quote: "### Exercise 7.10: Use estimation and approximation to solve problems  8. A supermarket has special offers on milk powder. One offer is two 1 kg tins at ₦7,595. Another offer is four 400 g tins at ₦6,399. Do a quick cal…"
- `ch07-b041-i09` [exercise_item] — placed in **AO:application-of-approximation-in-everyday-life-ao-apply-approximation (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.10: Use estimation and approximation to solve problems
  - evidence quote: "### Exercise 7.10: Use estimation and approximation to solve problems  9. An internet provider charges ₦9,309 per month for an 8 Mbps line. At the end of a year, they let their customers know that there will be a price…"
- `ch07-b041-i10` [exercise_item] — placed in **AO:application-of-approximation-in-everyday-life-ao-apply-approximation (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.10: Use estimation and approximation to solve problems
  - evidence quote: "### Exercise 7.10: Use estimation and approximation to solve problems  10. A caterer has to give a quote for the food at a wedding. The mother of the bride tells her that they are expecting adult 323 guests. She thinks…"
- `ch07-b042` [summary] — placed in **excluded**
  - heading: Chapter 7: Estimation and approximation > 7.4 Summary
  - evidence quote: "- Estimation is the process of making a guess about the size or cost of something, without doing the actual measurement or calculation. - Distance is the length of the space between two points. - The dimensions of an ob…"

### Row-level review categories and manually authored reasons
_None — all AOs have direct evidence and a reused assessment._

### Per-atomic-objective evidence classification
- `application-of-approximation-in-everyday-life-ao-apply-approximation` → evidence: **direct** · categories: —
  - linked records: ch07-b037(instruction), ch07-b038-i01(exercise), ch07-b039(instruction), ch07-b040(worked_example), ch07-b041-i01(exercise), ch07-b041-i02(exercise), ch07-b041-i04(exercise), ch07-b041-i06(exercise), ch07-b041-i08(exercise), ch07-b041-i09(exercise), ch07-b041-i10(exercise)
  - assessment: reused from `ch07-b041-i02`

---

## `jss1-math-approximation-quantitative-reasoning`

**Title:** Quantitative reasoning  
**Status:** `mapped`  
**Row review categories:** _(none — mapped or no-records baseline)_

### Curriculum objectives (source)
- `jss1-math-approximation-quantitative-reasoning-po01`: Solve problems on quantitative reasoning in the above contents

### Atomic objectives
- `approximation-quantitative-reasoning-ao-solve-problems` [solve/apply]: Solve problems on quantitative reasoning in the above contents.

### Linked textbook records (12 total) — inspected
- `ch07-b022` [exposition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off
  - evidence quote: "An approximate answer is almost correct, but not exact. Approximation is the process of using rounding to quickly determine a fairly accurate answer to a calculation. Approximation is very useful in situations where you…"
- `ch07-b023` [definition] — placed in **shared_foundation**
  - heading: Chapter 7: Estimation and approximation > 7.2 Approximation and rounding off
  - evidence quote: "approximation  Approximation is the process of using rounding to quickly determine a fairly accurate answer to a calculation."
- `ch07-b037` [exposition] — placed in **AO:approximation-quantitative-reasoning-ao-solve-problems (instruction)**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications
  - evidence quote: "The advantages of being able to estimate and approximate have been mentioned already. This section provides more opportunity for you to practise."
- `ch07-b038` [exercise_block] — placed in **excluded**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.9: Evaluate test answers
  - evidence quote: "### Exercise 7.9: Evaluate test answers  Each of the following is an incorrect answer that was given by a student in a test. Say what mistake the student made and give the correct answer."
- `ch07-b038-i01` [exercise_item] — placed in **AO:approximation-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.9: Evaluate test answers
  - evidence quote: "### Exercise 7.9: Evaluate test answers  1. The cost of 50 rulers at ₦10 each is ₦5,000."
- `ch07-b040` [worked_example] — placed in **AO:approximation-quantitative-reasoning-ao-solve-problems (worked_example)**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Worked example 7.8: Using approximation in calculations
  - evidence quote: "A shop owner has to choose the supplier from which she will order sugar cubes. One supplier offers 50 $\times$ 450 g packs of sugar cubes at ₦19,599. Another supplier offers 20 $\times$ 450 g packs of sugar cubes at ₦5,…"
- `ch07-b041` [exercise_block] — placed in **excluded**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.10: Use estimation and approximation to solve problems
  - evidence quote: "### Exercise 7.10: Use estimation and approximation to solve problems"
- `ch07-b041-i05` [exercise_item] — placed in **AO:approximation-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.10: Use estimation and approximation to solve problems
  - evidence quote: "### Exercise 7.10: Use estimation and approximation to solve problems  5. A soft drink bottle has a capacity of 33 cl. At the factory, the bottles are filled from a container with a capacity of 21.3 kl. Approximately ho…"
- `ch07-b041-i07` [exercise_item] — placed in **AO:approximation-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.10: Use estimation and approximation to solve problems
  - evidence quote: "### Exercise 7.10: Use estimation and approximation to solve problems  7. A man gets 17 bowls of rice from a sack of 51.15 kg. What is the approximate mass of rice needed for 5 bowls?"
- `ch07-b041-i08` [exercise_item] — placed in **AO:approximation-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.10: Use estimation and approximation to solve problems
  - evidence quote: "### Exercise 7.10: Use estimation and approximation to solve problems  8. A supermarket has special offers on milk powder. One offer is two 1 kg tins at ₦7,595. Another offer is four 400 g tins at ₦6,399. Do a quick cal…"
- `ch07-b041-i10` [exercise_item] — placed in **AO:approximation-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 7: Estimation and approximation > 7.3 Practical applications > Exercise 7.10: Use estimation and approximation to solve problems
  - evidence quote: "### Exercise 7.10: Use estimation and approximation to solve problems  10. A caterer has to give a quote for the food at a wedding. The mother of the bride tells her that they are expecting adult 323 guests. She thinks…"
- `ch07-b042` [summary] — placed in **excluded**
  - heading: Chapter 7: Estimation and approximation > 7.4 Summary
  - evidence quote: "- Estimation is the process of making a guess about the size or cost of something, without doing the actual measurement or calculation. - Distance is the length of the space between two points. - The dimensions of an ob…"

### Row-level review categories and manually authored reasons
_None — all AOs have direct evidence and a reused assessment._

### Per-atomic-objective evidence classification
- `approximation-quantitative-reasoning-ao-solve-problems` → evidence: **direct** · categories: —
  - linked records: ch07-b037(instruction), ch07-b038-i01(exercise), ch07-b040(worked_example), ch07-b041-i05(exercise), ch07-b041-i07(exercise), ch07-b041-i08(exercise), ch07-b041-i10(exercise)
  - assessment: reused from `ch07-b041-i07`

---

## `jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers`

**Title:** Addition of two or three 3-digit binary numbers  
**Status:** `mapped`  
**Row review categories:** _(none — mapped or no-records baseline)_

### Curriculum objectives (source)
- `jss1-math-addition-of-numbers-in-base-2-numerals-addition-of-two-or-three-3-digit-binary-numbers-po01`: Add two or three 3-digit binary numbers

### Atomic objectives
- `addition-of-binary-numbers-ao-add-two-or-three-3-digit-binary-numbers` [add/apply]: Add two or three 3-digit binary numbers.

### Linked textbook records (20 total) — inspected
- `ch08-b001` [exposition] — placed in **shared_foundation**
  - heading: Chapter 8: Operations with binary numbers
  - evidence quote: "In Chapter 3 you learnt about the base two number system. The base two or binary number system counts in groups of 2, and uses only the digits 0 and 1 to represent any number. The numbers in the base two number system a…"
- `ch08-b002` [exposition] — placed in **AO:addition-of-binary-numbers-ao-add-two-or-three-3-digit-binary-numbers (instruction)**
  - heading: Chapter 8: Operations with binary numbers > 8.1 Addition
  - evidence quote: "When we add binary numbers, we follow the same principles as when we add numbers in the base ten number system."
- `ch08-b003` [worked_example] — placed in **AO:addition-of-binary-numbers-ao-add-two-or-three-3-digit-binary-numbers (foundation)**
  - heading: Chapter 8: Operations with binary numbers > 8.1 Addition > Worked example 8.1: Revision of addition in the base ten number system
  - evidence quote: "Find the total of $794+648+89$."
- `ch08-b004` [exposition] — placed in **AO:addition-of-binary-numbers-ao-add-two-or-three-3-digit-binary-numbers (instruction)**
  - heading: Chapter 8: Operations with binary numbers > 8.1 Addition
  - evidence quote: "In the base two number system, we work in groups of 2. So, instead of dividing by 10, we divide by 2."
- `ch08-b005` [worked_example] — placed in **AO:addition-of-binary-numbers-ao-add-two-or-three-3-digit-binary-numbers (worked_example)**
  - heading: Chapter 8: Operations with binary numbers > 8.1 Addition > Worked example 8.2: Addition in the base two number system (Method 1)
  - evidence quote: "Find the sum of $101_\text{two}$ and $111_\text{two}$."
- `ch08-b006` [exposition] — placed in **AO:addition-of-binary-numbers-ao-add-two-or-three-3-digit-binary-numbers (instruction)**
  - heading: Chapter 8: Operations with binary numbers > 8.1 Addition
  - evidence quote: "Another way to do addition in the base two number system is to use these basic rules:  0+0=0 0+1=1 1+0=1 1+1=10 1+1+1=11"
- `ch08-b007` [note] — placed in **AO:addition-of-binary-numbers-ao-add-two-or-three-3-digit-binary-numbers (foundation)**
  - heading: Chapter 8: Operations with binary numbers > 8.1 Addition
  - evidence quote: "Remember:  $2_\text{ten}=10_\text{two}$ $3_\text{ten}=11_\text{two}$"
- `ch08-b008` [worked_example] — placed in **AO:addition-of-binary-numbers-ao-add-two-or-three-3-digit-binary-numbers (worked_example)**
  - heading: Chapter 8: Operations with binary numbers > 8.1 Addition > Worked example 8.3: Addition in the base two number system (Method 2)
  - evidence quote: "Find the sum of $101_\text{two}$ and $111_\text{two}$."
- `ch08-b009` [exercise_block] — placed in **excluded**
  - heading: Chapter 8: Operations with binary numbers > 8.1 Addition > Exercise 8.1: Add binary numbers
  - evidence quote: "### Exercise 8.1: Add binary numbers  Calculate each of the following in the base two number system."
- `ch08-b009-i01` [exercise_item] — placed in **AO:addition-of-binary-numbers-ao-add-two-or-three-3-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.1 Addition > Exercise 8.1: Add binary numbers
  - evidence quote: "### Exercise 8.1: Add binary numbers  1. $$100+10$$"
- `ch08-b009-i02` [exercise_item] — placed in **AO:addition-of-binary-numbers-ao-add-two-or-three-3-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.1 Addition > Exercise 8.1: Add binary numbers
  - evidence quote: "### Exercise 8.1: Add binary numbers  2. $$101+11$$"
- `ch08-b009-i03` [exercise_item] — placed in **AO:addition-of-binary-numbers-ao-add-two-or-three-3-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.1 Addition > Exercise 8.1: Add binary numbers
  - evidence quote: "### Exercise 8.1: Add binary numbers  3. $$110+11$$"
- `ch08-b009-i04` [exercise_item] — placed in **AO:addition-of-binary-numbers-ao-add-two-or-three-3-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.1 Addition > Exercise 8.1: Add binary numbers
  - evidence quote: "### Exercise 8.1: Add binary numbers  4. $$111+10$$"
- `ch08-b009-i05` [exercise_item] — placed in **AO:addition-of-binary-numbers-ao-add-two-or-three-3-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.1 Addition > Exercise 8.1: Add binary numbers
  - evidence quote: "### Exercise 8.1: Add binary numbers  5. $$100+101$$"
- `ch08-b009-i06` [exercise_item] — placed in **AO:addition-of-binary-numbers-ao-add-two-or-three-3-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.1 Addition > Exercise 8.1: Add binary numbers
  - evidence quote: "### Exercise 8.1: Add binary numbers  6. $$101+110$$"
- `ch08-b009-i07` [exercise_item] — placed in **AO:addition-of-binary-numbers-ao-add-two-or-three-3-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.1 Addition > Exercise 8.1: Add binary numbers
  - evidence quote: "### Exercise 8.1: Add binary numbers  7. $$110+111$$"
- `ch08-b009-i08` [exercise_item] — placed in **AO:addition-of-binary-numbers-ao-add-two-or-three-3-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.1 Addition > Exercise 8.1: Add binary numbers
  - evidence quote: "### Exercise 8.1: Add binary numbers  8. $$111+111$$"
- `ch08-b009-i09` [exercise_item] — placed in **AO:addition-of-binary-numbers-ao-add-two-or-three-3-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.1 Addition > Exercise 8.1: Add binary numbers
  - evidence quote: "### Exercise 8.1: Add binary numbers  9. $$1010+11$$"
- `ch08-b009-i10` [exercise_item] — placed in **AO:addition-of-binary-numbers-ao-add-two-or-three-3-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.1 Addition > Exercise 8.1: Add binary numbers
  - evidence quote: "### Exercise 8.1: Add binary numbers  10. $$1111+11$$"
- `ch08-b023` [summary] — placed in **excluded**
  - heading: Chapter 8: Operations with binary numbers > 8.4 Summary
  - evidence quote: "From Chapter 3 you know that: - 2_\text{ten}=10_\text{two} - 3_\text{ten}=11_\text{two}  Use the following basic rules when adding binary numbers: - 0+0=0 - 0+1=1 - 1+0=1 - 1+1=10 - 1+1+1=11  Use the following basic rul…"

### Row-level review categories and manually authored reasons
_None — all AOs have direct evidence and a reused assessment._

### Per-atomic-objective evidence classification
- `addition-of-binary-numbers-ao-add-two-or-three-3-digit-binary-numbers` → evidence: **direct** · categories: —
  - linked records: ch08-b002(instruction), ch08-b003(foundation), ch08-b004(instruction), ch08-b005(worked_example), ch08-b006(instruction), ch08-b007(foundation), ch08-b008(worked_example), ch08-b009-i01(exercise), ch08-b009-i02(exercise), ch08-b009-i03(exercise), ch08-b009-i04(exercise), ch08-b009-i05(exercise), ch08-b009-i06(exercise), ch08-b009-i07(exercise), ch08-b009-i08(exercise), ch08-b009-i09(exercise), ch08-b009-i10(exercise)
  - assessment: reused from `ch08-b009-i03`

---

## `jss1-math-subtraction-of-numbers-in-base-2-numerals-subtraction-of-two-3-digit-binary-numbers`

**Title:** Subtraction of two 3-digit binary numbers  
**Status:** `mapped`  
**Row review categories:** _(none — mapped or no-records baseline)_

### Curriculum objectives (source)
- `jss1-math-subtraction-of-numbers-in-base-2-numerals-subtraction-of-two-3-digit-binary-numbers-po01`: Subtract two 3-digit binary numbers

### Atomic objectives
- `subtraction-of-binary-numbers-ao-subtract-two-3-digit-binary-numbers` [subtract/apply]: Subtract two 3-digit binary numbers.

### Linked textbook records (19 total) — inspected
- `ch08-b010` [exposition] — placed in **AO:subtraction-of-binary-numbers-ao-subtract-two-3-digit-binary-numbers (instruction)**
  - heading: Chapter 8: Operations with binary numbers > 8.1 Addition
  - evidence quote: "When we subtract binary numbers, we follow the same principles as when we subtract numbers in the base ten number system."
- `ch08-b011` [worked_example] — placed in **AO:subtraction-of-binary-numbers-ao-subtract-two-3-digit-binary-numbers (foundation)**
  - heading: Chapter 8: Operations with binary numbers > 8.2 Subtraction > Worked example 8.4: Revision of subtraction in the base ten number system
  - evidence quote: "Subtract 178 from 4,032."
- `ch08-b012` [exposition] — placed in **AO:subtraction-of-binary-numbers-ao-subtract-two-3-digit-binary-numbers (instruction)**
  - heading: Chapter 8: Operations with binary numbers > 8.1 Addition
  - evidence quote: "In the base two number system, we work in groups of 2. So, instead of moving groups of 10 between columns, we move groups of 2."
- `ch08-b013` [worked_example] — placed in **AO:subtraction-of-binary-numbers-ao-subtract-two-3-digit-binary-numbers (worked_example)**
  - heading: Chapter 8: Operations with binary numbers > 8.2 Subtraction > Worked example 8.5: Subtraction in the base two number system (Method 1)
  - evidence quote: "Subtract $101_\text{two}$ from $1010_\text{two}$."
- `ch08-b014` [exposition] — placed in **AO:subtraction-of-binary-numbers-ao-subtract-two-3-digit-binary-numbers (instruction)**
  - heading: Chapter 8: Operations with binary numbers > 8.2 Subtraction
  - evidence quote: "Another way to do subtraction in the base two number system is to use these basic rules:  $0-0=0$  $1-0=0$  $1-1=0$  $10-1=1$  $11-1=10$"
- `ch08-b015` [note] — placed in **AO:subtraction-of-binary-numbers-ao-subtract-two-3-digit-binary-numbers (foundation)**
  - heading: Chapter 8: Operations with binary numbers > 8.2 Subtraction
  - evidence quote: "Remember:  $2_\text{ten}=10_\text{two}$  $3_\text{ten}=11_\text{two}$"
- `ch08-b016` [worked_example] — placed in **AO:subtraction-of-binary-numbers-ao-subtract-two-3-digit-binary-numbers (worked_example)**
  - heading: Chapter 8: Operations with binary numbers > 8.2 Subtraction > Worked example 8.6: Subtraction in the base two number system (Method 2)
  - evidence quote: "Subtract $101_\text{two}$ from $1010_\text{two}$."
- `ch08-b017` [exercise_block] — placed in **excluded**
  - heading: Chapter 8: Operations with binary numbers > 8.2 Subtraction > Exercise 8.2: Subtract binary numbers
  - evidence quote: "### Exercise 8.2: Subtract binary numbers  Calculate each of the following in the base two number system."
- `ch08-b017-i01` [exercise_item] — placed in **AO:subtraction-of-binary-numbers-ao-subtract-two-3-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.2 Subtraction > Exercise 8.2: Subtract binary numbers
  - evidence quote: "### Exercise 8.2: Subtract binary numbers  1. 111-110"
- `ch08-b017-i02` [exercise_item] — placed in **AO:subtraction-of-binary-numbers-ao-subtract-two-3-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.2 Subtraction > Exercise 8.2: Subtract binary numbers
  - evidence quote: "### Exercise 8.2: Subtract binary numbers  2. 111-101"
- `ch08-b017-i03` [exercise_item] — placed in **AO:subtraction-of-binary-numbers-ao-subtract-two-3-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.2 Subtraction > Exercise 8.2: Subtract binary numbers
  - evidence quote: "### Exercise 8.2: Subtract binary numbers  3. 111-100"
- `ch08-b017-i04` [exercise_item] — placed in **AO:subtraction-of-binary-numbers-ao-subtract-two-3-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.2 Subtraction > Exercise 8.2: Subtract binary numbers
  - evidence quote: "### Exercise 8.2: Subtract binary numbers  4. 110-100"
- `ch08-b017-i05` [exercise_item] — placed in **AO:subtraction-of-binary-numbers-ao-subtract-two-3-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.2 Subtraction > Exercise 8.2: Subtract binary numbers
  - evidence quote: "### Exercise 8.2: Subtract binary numbers  5. 101-11"
- `ch08-b017-i06` [exercise_item] — placed in **AO:subtraction-of-binary-numbers-ao-subtract-two-3-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.2 Subtraction > Exercise 8.2: Subtract binary numbers
  - evidence quote: "### Exercise 8.2: Subtract binary numbers  6. 110-101"
- `ch08-b017-i07` [exercise_item] — placed in **AO:subtraction-of-binary-numbers-ao-subtract-two-3-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.2 Subtraction > Exercise 8.2: Subtract binary numbers
  - evidence quote: "### Exercise 8.2: Subtract binary numbers  7. 110-11"
- `ch08-b017-i08` [exercise_item] — placed in **AO:subtraction-of-binary-numbers-ao-subtract-two-3-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.2 Subtraction > Exercise 8.2: Subtract binary numbers
  - evidence quote: "### Exercise 8.2: Subtract binary numbers  8. 1001-10"
- `ch08-b017-i09` [exercise_item] — placed in **AO:subtraction-of-binary-numbers-ao-subtract-two-3-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.2 Subtraction > Exercise 8.2: Subtract binary numbers
  - evidence quote: "### Exercise 8.2: Subtract binary numbers  9. 1000-11"
- `ch08-b017-i10` [exercise_item] — placed in **AO:subtraction-of-binary-numbers-ao-subtract-two-3-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.2 Subtraction > Exercise 8.2: Subtract binary numbers
  - evidence quote: "### Exercise 8.2: Subtract binary numbers  10. 1000-11"
- `ch08-b023` [summary] — placed in **excluded**
  - heading: Chapter 8: Operations with binary numbers > 8.4 Summary
  - evidence quote: "From Chapter 3 you know that: - 2_\text{ten}=10_\text{two} - 3_\text{ten}=11_\text{two}  Use the following basic rules when adding binary numbers: - 0+0=0 - 0+1=1 - 1+0=1 - 1+1=10 - 1+1+1=11  Use the following basic rul…"

### Row-level review categories and manually authored reasons
_None — all AOs have direct evidence and a reused assessment._

### Per-atomic-objective evidence classification
- `subtraction-of-binary-numbers-ao-subtract-two-3-digit-binary-numbers` → evidence: **direct** · categories: —
  - linked records: ch08-b010(instruction), ch08-b011(foundation), ch08-b012(instruction), ch08-b013(worked_example), ch08-b014(instruction), ch08-b015(foundation), ch08-b016(worked_example), ch08-b017-i01(exercise), ch08-b017-i02(exercise), ch08-b017-i03(exercise), ch08-b017-i04(exercise), ch08-b017-i05(exercise), ch08-b017-i06(exercise), ch08-b017-i07(exercise), ch08-b017-i08(exercise), ch08-b017-i09(exercise), ch08-b017-i10(exercise)
  - assessment: reused from `ch08-b017-i03`

---

## `jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers`

**Title:** Multiplication of two 2-digit binary numbers  
**Status:** `mapped`  
**Row review categories:** _(none — mapped or no-records baseline)_

### Curriculum objectives (source)
- `jss1-math-multiplication-of-numbers-in-base-2-numerals-multiplication-of-two-2-digit-binary-numbers-po01`: Multiply two 2-digit binary numbers

### Atomic objectives
- `multiplication-of-binary-numbers-ao-multiply-two-2-digit-binary-numbers` [multiply/apply]: Multiply two 2-digit binary numbers.

### Linked textbook records (11 total) — inspected
- `ch08-b018` [exposition] — placed in **AO:multiplication-of-binary-numbers-ao-multiply-two-2-digit-binary-numbers (instruction)**
  - heading: Chapter 8: Operations with binary numbers > 8.3 Multiplication
  - evidence quote: "Last year you learnt how to multiply integers using long multiplication. We use the same principles when multiplying numbers in the base two number system."
- `ch08-b019` [worked_example] — placed in **AO:multiplication-of-binary-numbers-ao-multiply-two-2-digit-binary-numbers (foundation)**
  - heading: Chapter 8: Operations with binary numbers > 8.3 Multiplication > Worked example 8.7: Revision of multiplication in the base ten number system
  - evidence quote: "Multiply 32 by 14."
- `ch08-b020` [exposition] — placed in **AO:multiplication-of-binary-numbers-ao-multiply-two-2-digit-binary-numbers (instruction)**
  - heading: Chapter 8: Operations with binary numbers > 8.3 Multiplication
  - evidence quote: "Multiplication of the digits 0 and 1 work the same in the base ten and base two number systems:  $0\times0=0$  $1\times0=0$  $0\times1=0$  $1\times1=1$"
- `ch08-b021` [worked_example] — placed in **AO:multiplication-of-binary-numbers-ao-multiply-two-2-digit-binary-numbers (worked_example)**
  - heading: Chapter 8: Operations with binary numbers > 8.3 Multiplication > Worked example 8.8: Multiplication in the base two number system
  - evidence quote: "Multiply $11_\text{two}$ by $11_\text{two}$."
- `ch08-b022` [exercise_block] — placed in **excluded**
  - heading: Chapter 8: Operations with binary numbers > 8.3 Binary multiplication > Exercise 8.3: Multiply binary numbers
  - evidence quote: "### Exercise 8.3: Multiply binary numbers  Calculate each of the following in the base two number system."
- `ch08-b022-i01` [exercise_item] — placed in **AO:multiplication-of-binary-numbers-ao-multiply-two-2-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.3 Binary multiplication > Exercise 8.3: Multiply binary numbers
  - evidence quote: "### Exercise 8.3: Multiply binary numbers  1. 10 \times 10"
- `ch08-b022-i02` [exercise_item] — placed in **AO:multiplication-of-binary-numbers-ao-multiply-two-2-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.3 Binary multiplication > Exercise 8.3: Multiply binary numbers
  - evidence quote: "### Exercise 8.3: Multiply binary numbers  2. 10 \times 11"
- `ch08-b022-i03` [exercise_item] — placed in **AO:multiplication-of-binary-numbers-ao-multiply-two-2-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.3 Binary multiplication > Exercise 8.3: Multiply binary numbers
  - evidence quote: "### Exercise 8.3: Multiply binary numbers  3. 100 \times 10"
- `ch08-b022-i04` [exercise_item] — placed in **AO:multiplication-of-binary-numbers-ao-multiply-two-2-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.3 Binary multiplication > Exercise 8.3: Multiply binary numbers
  - evidence quote: "### Exercise 8.3: Multiply binary numbers  4. 110 \times 11"
- `ch08-b022-i05` [exercise_item] — placed in **AO:multiplication-of-binary-numbers-ao-multiply-two-2-digit-binary-numbers (exercise)**
  - heading: Chapter 8: Operations with binary numbers > 8.3 Binary multiplication > Exercise 8.3: Multiply binary numbers
  - evidence quote: "### Exercise 8.3: Multiply binary numbers  5. 111 \times 11"
- `ch08-b023` [summary] — placed in **excluded**
  - heading: Chapter 8: Operations with binary numbers > 8.4 Summary
  - evidence quote: "From Chapter 3 you know that: - 2_\text{ten}=10_\text{two} - 3_\text{ten}=11_\text{two}  Use the following basic rules when adding binary numbers: - 0+0=0 - 0+1=1 - 1+0=1 - 1+1=10 - 1+1+1=11  Use the following basic rul…"

### Row-level review categories and manually authored reasons
_None — all AOs have direct evidence and a reused assessment._

### Per-atomic-objective evidence classification
- `multiplication-of-binary-numbers-ao-multiply-two-2-digit-binary-numbers` → evidence: **direct** · categories: —
  - linked records: ch08-b018(instruction), ch08-b019(foundation), ch08-b020(instruction), ch08-b021(worked_example), ch08-b022-i01(exercise), ch08-b022-i02(exercise), ch08-b022-i03(exercise), ch08-b022-i04(exercise), ch08-b022-i05(exercise)
  - assessment: reused from `ch08-b022-i03`

---

## `jss1-math-use-of-symbols-open-sentences`

**Title:** Open sentences  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-use-of-symbols-open-sentences-po01`: Solve problems expressed in open sentences
- `jss1-math-use-of-symbols-open-sentences-po02`: Identify the relationship between addition and subtraction; multiplication and division

### Atomic objectives
- `open-sentences-ao-solve-problems` [solve/apply]: Solve problems expressed in open sentences.
- `open-sentences-ao-identify-relationship-addition-and-subtraction` [identify/remember]: Identify the relationship between addition and subtraction.
- `open-sentences-ao-identify-relationship-multiplication-and-division` [identify/remember]: Identify the relationship between multiplication and division.

### Linked textbook records (84 total) — inspected
- `ch09-b001` [exposition] — placed in **shared_foundation**
  - heading: Chapter 9: Using symbols > 9.1 Closed number sentences > Closed number sentences
  - evidence quote: "A number sentence is a group of numbers and mathematical symbols (such as +, -, or =) that gives information about the numbers. Here is an example of a number sentence: 3 + 4 = 7. This is called a closed number sentence…"
- `ch09-b002` [definition] — placed in **shared_foundation**
  - heading: Chapter 9: Using symbols > 9.1 Closed number sentences > Closed number sentences
  - evidence quote: "closed number sentence A closed number sentence gives all the information about the numbers, and it is always true or always false."
- `ch09-b003` [exposition] — placed in **shared_foundation**
  - heading: Chapter 9: Using symbols > 9.1 Closed number sentences > Closed number sentences
  - evidence quote: "Here are some more examples of closed number sentences: 9 \div 3 = 3 (true), 7\times 12 = 84 (true), 4 \times 8 = 8 + 8 + 8 + 8 + 8 (false)."
- `ch09-b004` [exercise_block] — placed in **excluded**
  - heading: Chapter 9: Using symbols > 9.1 Closed number sentences > Exercise 9.1: Decide whether closed sentences are true or false
  - evidence quote: "### Exercise 9.1: Decide whether closed sentences are true or false  State whether the closed sentence is always true or false."
- `ch09-b004-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.1 Closed number sentences > Exercise 9.1: Decide whether closed sentences are true or false
  - evidence quote: "### Exercise 9.1: Decide whether closed sentences are true or false  1. 4\times 10 = 40"
- `ch09-b004-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.1 Closed number sentences > Exercise 9.1: Decide whether closed sentences are true or false
  - evidence quote: "### Exercise 9.1: Decide whether closed sentences are true or false  2. 102\div 2 = 12"
- `ch09-b004-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.1 Closed number sentences > Exercise 9.1: Decide whether closed sentences are true or false
  - evidence quote: "### Exercise 9.1: Decide whether closed sentences are true or false  3. 30 + 30 + 30 = 3\times 30"
- `ch09-b004-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.1 Closed number sentences > Exercise 9.1: Decide whether closed sentences are true or false
  - evidence quote: "### Exercise 9.1: Decide whether closed sentences are true or false  4. 9\div 18 = 2"
- `ch09-b004-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.1 Closed number sentences > Exercise 9.1: Decide whether closed sentences are true or false
  - evidence quote: "### Exercise 9.1: Decide whether closed sentences are true or false  5. 9\div 18 = \frac{1}{2}"
- `ch09-b005` [exposition] — placed in **shared_foundation**
  - heading: Chapter 9: Using symbols > 9.1 Open number sentences > Open number sentences
  - evidence quote: "Here is another example of a number sentence: \square + 3 = 7. This is called an open number sentence, because not all the information is given in the sentence. We do not know if this sentence is true or false because w…"
- `ch09-b006` [definition] — placed in **shared_foundation**
  - heading: Chapter 9: Using symbols > 9.1 Open number sentences > Open number sentences
  - evidence quote: "open number sentence An open number sentence does not give all the information about the numbers, but has information missing that we must find."
- `ch09-b007` [worked_example] — placed in **AO:open-sentences-ao-solve-problems (worked_example)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Worked example 9.1: Finding missing information in an open sentence
  - evidence quote: "Find the value of the square in this open number sentence:  $$ \square + 3 = 7 $$"
- `ch09-b008` [exercise_block] — placed in **excluded**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.2: Find missing information in open sentences
  - evidence quote: "### Exercise 9.2: Find missing information in open sentences  For each open number sentence, find the number that makes the sentence true."
- `ch09-b008-i01` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.2: Find missing information in open sentences
  - evidence quote: "### Exercise 9.2: Find missing information in open sentences  1. $$17 - 9 = \square$$"
- `ch09-b008-i02` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.2: Find missing information in open sentences
  - evidence quote: "### Exercise 9.2: Find missing information in open sentences  2. $$3 + 9 = \square$$"
- `ch09-b008-i03` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.2: Find missing information in open sentences
  - evidence quote: "### Exercise 9.2: Find missing information in open sentences  3. $$2\times 12 = \square$$"
- `ch09-b008-i04` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.2: Find missing information in open sentences
  - evidence quote: "### Exercise 9.2: Find missing information in open sentences  4. $$9-\square= 2$$"
- `ch09-b008-i05` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.2: Find missing information in open sentences
  - evidence quote: "### Exercise 9.2: Find missing information in open sentences  5. $$\bigcirc=\frac{1}{2}+ \frac{1}{2}$$"
- `ch09-b008-i06` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.2: Find missing information in open sentences
  - evidence quote: "### Exercise 9.2: Find missing information in open sentences  6. $$10\times\square = 100$$"
- `ch09-b008-i07` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.2: Find missing information in open sentences
  - evidence quote: "### Exercise 9.2: Find missing information in open sentences  7. $$63\div9=\square$$"
- `ch09-b008-i08` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.2: Find missing information in open sentences
  - evidence quote: "### Exercise 9.2: Find missing information in open sentences  8. $$30 + 30 + \bigcirc = 3\times 30$$"
- `ch09-b008-i09` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.2: Find missing information in open sentences
  - evidence quote: "### Exercise 9.2: Find missing information in open sentences  9. $$\square\times6=30$$"
- `ch09-b008-i10` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.2: Find missing information in open sentences
  - evidence quote: "### Exercise 9.2: Find missing information in open sentences  10. $$5 + \bigcirc + 18 = 30$$"
- `ch09-b009` [exposition] — placed in **shared_foundation**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Variables in open sentences
  - evidence quote: "So far we have worked with open sentences that contain a symbol such as a $\square$ or a $\bigcirc$. Instead of pictures like these, in mathematics it works better to use letters to represent missing information. These…"
- `ch09-b010` [definition] — placed in **shared_foundation**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Variables in open sentences
  - evidence quote: "**variable** A variable is a symbol for a number we do not know yet. It is usually a letter such as $x$ or $y$."
- `ch09-b011` [exposition] — placed in **shared_foundation**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Variables in open sentences
  - evidence quote: "If we have an expression, such as $x+5$, we cannot know the value of the $x$ unless it is given. If we give the $x$ different values, then we can make number sentences that are true.  If $x$ = 1, then $x+5 = 1 + 5 = 6$…"
- `ch09-b012` [exercise_block] — placed in **excluded**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.3: Find the value of the expression
  - evidence quote: "### Exercise 9.3: Find the value of the expression  Find the value of the following expressions if $x=3$."
- `ch09-b012-i01` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.3: Find the value of the expression
  - evidence quote: "### Exercise 9.3: Find the value of the expression  1. $$17 - x$$"
- `ch09-b012-i02` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.3: Find the value of the expression
  - evidence quote: "### Exercise 9.3: Find the value of the expression  2. $$3 + x$$"
- `ch09-b012-i03` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.3: Find the value of the expression
  - evidence quote: "### Exercise 9.3: Find the value of the expression  3. $$2\times x\times 0$$"
- `ch09-b012-i04` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.3: Find the value of the expression
  - evidence quote: "### Exercise 9.3: Find the value of the expression  4. $$9-x+2$$"
- `ch09-b012-i05` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.3: Find the value of the expression
  - evidence quote: "### Exercise 9.3: Find the value of the expression  5. $$\frac{1}{x}+ \frac{1}{x}$$"
- `ch09-b012-i06` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.3: Find the value of the expression
  - evidence quote: "### Exercise 9.3: Find the value of the expression  6. $$10\times x$$"
- `ch09-b012-i07` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.3: Find the value of the expression
  - evidence quote: "### Exercise 9.3: Find the value of the expression  7. $$60\div x$$"
- `ch09-b012-i08` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.3: Find the value of the expression
  - evidence quote: "### Exercise 9.3: Find the value of the expression  8. $$30 + 30 + x$$"
- `ch09-b012-i09` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.3: Find the value of the expression
  - evidence quote: "### Exercise 9.3: Find the value of the expression  9. $$x\times6$$"
- `ch09-b012-i10` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.3: Find the value of the expression
  - evidence quote: "### Exercise 9.3: Find the value of the expression  10. $$5 + x + 18$$"
- `ch09-b013` [exposition] — placed in **shared_foundation**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences that have variables
  - evidence quote: "Variables and open sentences form part of a section of mathematics we call algebra. To show that there is information that we must find, an open sentence can use a picture symbol (such as a box or a circle) or a variabl…"
- `ch09-b014` [worked_example] — placed in **AO:open-sentences-ao-solve-problems (worked_example)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences that have variables > Worked example 9.2: Finding the value of a variable using mental maths
  - evidence quote: "Find the value of $x$ in this open number sentence:  $$ x + 7 = 9 $$"
- `ch09-b015` [exposition] — placed in **AO:open-sentences-ao-identify-relationship-addition-and-subtraction (instruction)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences that have variables > Using inverse operations to solve open sentences
  - evidence quote: "Another way to find the value of $x$ in $x + 7 = 9$, is to use the **inverse operation** of addition. The inverse operation of addition is subtraction. In Chapter 5 you learnt that subtraction may be seen as another for…"
- `ch09-b016` [definition] — placed in **AO:open-sentences-ao-identify-relationship-addition-and-subtraction (foundation)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences that have variables > Using inverse operations to solve open sentences
  - evidence quote: "**inverse operation** An inverse operation does the opposite of another operation. Addition and subtraction are inverse operations, and multiplication and division are inverse operations."
- `ch09-b017` [exposition] — placed in **AO:open-sentences-ao-identify-relationship-addition-and-subtraction (instruction)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences that have variables > Using inverse operations to solve open sentences
  - evidence quote: "This closed number sentence is true:  $$ 2 + 7 = 9 $$  We know that this closed number sentence is also true:  $$ 2 = 9 - 7 $$  Notice that we get from the first number sentence to the second number sentence using the i…"
- `ch09-b018` [worked_example] — placed in **AO:open-sentences-ao-identify-relationship-addition-and-subtraction (worked_example)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences that have variables > Worked example 9.3: Solving an open sentence using the inverse of addition
  - evidence quote: "Find the value of $x$ in this open sentence:  $$ x + 12 = 29 $$"
- `ch09-b019` [worked_example] — placed in **AO:open-sentences-ao-identify-relationship-multiplication-and-division (worked_example)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences that have variables > Worked example 9.4: Solving an open sentence using the inverse of multiplication
  - evidence quote: "Find the value of $y$ in this open sentence:  $$ y \times 3 = 27 $$"
- `ch09-b020` [exposition] — placed in **shared_foundation**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences that have variables > Using inverse operations to solve open sentences
  - evidence quote: "Note that an open sentence is not regarded as solved when the variable is negative, for example $-x=5$. The variable must be positive in your final answer, for example $x=-5$."
- `ch09-b021` [note] — placed in **shared_foundation**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences that have variables > Using inverse operations to solve open sentences
  - evidence quote: "The format $variable=\text{value}$ may be swapped around. Therefore, $x=7$ and $7=x$ has the same meaning."
- `ch09-b022` [worked_example] — placed in **AO:open-sentences-ao-solve-problems (worked_example)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences that have variables > Worked example 9.5: Solving an open sentence using the inverse operation on the variable
  - evidence quote: "Find the value of $x$:  $$ 18 -  x = 14 $$"
- `ch09-b023` [exercise_block] — placed in **excluded**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.4: Solve open sentences
  - evidence quote: "### Exercise 9.4: Solve open sentences  Find the value of the variable in the following open sentences:"
- `ch09-b023-i01` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.4: Solve open sentences
  - evidence quote: "### Exercise 9.4: Solve open sentences  1. y + 7 = 30"
- `ch09-b023-i02` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.4: Solve open sentences
  - evidence quote: "### Exercise 9.4: Solve open sentences  2. 3 + x = 15"
- `ch09-b023-i03` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.4: Solve open sentences
  - evidence quote: "### Exercise 9.4: Solve open sentences  3. z - 8 = 20"
- `ch09-b023-i04` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.4: Solve open sentences
  - evidence quote: "### Exercise 9.4: Solve open sentences  4. q  - 4 = -5"
- `ch09-b023-i05` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.4: Solve open sentences
  - evidence quote: "### Exercise 9.4: Solve open sentences  5. 17 - n = 20"
- `ch09-b023-i06` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.4: Solve open sentences
  - evidence quote: "### Exercise 9.4: Solve open sentences  6. 15 - p = -5"
- `ch09-b023-i07` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.4: Solve open sentences
  - evidence quote: "### Exercise 9.4: Solve open sentences  7. x \times 8 = 48"
- `ch09-b023-i08` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.4: Solve open sentences
  - evidence quote: "### Exercise 9.4: Solve open sentences  8. 3 \times y = 15"
- `ch09-b023-i09` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.4: Solve open sentences
  - evidence quote: "### Exercise 9.4: Solve open sentences  9. c\div 20 = 5"
- `ch09-b023-i10` [exercise_item] — placed in **AO:open-sentences-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.4: Solve open sentences
  - evidence quote: "### Exercise 9.4: Solve open sentences  10. 40 \div x = 8"
- `ch09-b024` [exposition] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems
  - evidence quote: "Open number sentences may have more than one operation, for example $4-2+x=10$. To solve number sentences like these, you must remember the correct order of operations that you learnt last year:  1. **B**rackets 2. **O*…"
- `ch09-b025` [worked_example] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Worked example 9.7: Solving a problem using open sentences
  - evidence quote: "Find the value of x:"
- `ch09-b026` [exercise_block] — placed in **excluded**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.5: Solve open sentences with two operations
  - evidence quote: "### Exercise 9.5: Solve open sentences with two operations  Find the value of the variable in the following open sentences:"
- `ch09-b026-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.5: Solve open sentences with two operations
  - evidence quote: "### Exercise 9.5: Solve open sentences with two operations  1. 3 + x - 4 = 20"
- `ch09-b026-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.5: Solve open sentences with two operations
  - evidence quote: "### Exercise 9.5: Solve open sentences with two operations  2. q \times 3 + 5 = 29"
- `ch09-b026-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.5: Solve open sentences with two operations
  - evidence quote: "### Exercise 9.5: Solve open sentences with two operations  3. t + 10 \div 2 = 12"
- `ch09-b026-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.5: Solve open sentences with two operations
  - evidence quote: "### Exercise 9.5: Solve open sentences with two operations  4. 5 - x + 2 = 12"
- `ch09-b026-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.5: Solve open sentences with two operations
  - evidence quote: "### Exercise 9.5: Solve open sentences with two operations  5. y \times 5 - 7 = 13"
- `ch09-b026-i06` [exercise_item] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.5: Solve open sentences with two operations
  - evidence quote: "### Exercise 9.5: Solve open sentences with two operations  6. p \div 2 - 5 = 25"
- `ch09-b026-i07` [exercise_item] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.5: Solve open sentences with two operations
  - evidence quote: "### Exercise 9.5: Solve open sentences with two operations  7. 5 \times -2 = 6 + v"
- `ch09-b026-i08` [exercise_item] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.5: Solve open sentences with two operations
  - evidence quote: "### Exercise 9.5: Solve open sentences with two operations  8. 2 \times -6 = 24 \div r"
- `ch09-b027` [exposition] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems
  - evidence quote: "We can use open sentences with variables to set out and solve problems that are described in words. Remember that we can translate the following words into mathematical operations:  | English | Mathematical symbol | | -…"
- `ch09-b028` [worked_example] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Worked example 9.7: Solving a problem using open sentences
  - evidence quote: "There are 32 students in one JSS1 class. If 20 of the students are boys, how many girls are there in this class?"
- `ch09-b029` [worked_example] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Worked example 9.8: Solving a problem using open sentences
  - evidence quote: "For six days of the week, Ndidi spends the same amount of time each day practising the violin. On the last day of the week, she practises only 30 minutes. Her total practice time for the week is 300 minutes. For how man…"
- `ch09-b030` [exercise_block] — placed in **excluded**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Exercise 9.6: Use open sentences to solve problems
  - evidence quote: "### Exercise 9.6: Use open sentences to solve problems"
- `ch09-b030-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Exercise 9.6: Use open sentences to solve problems
  - evidence quote: "### Exercise 9.6: Use open sentences to solve problems  1. Two numbers add up to 28. One of the numbers is 10. What is the other number?"
- `ch09-b030-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Exercise 9.6: Use open sentences to solve problems
  - evidence quote: "### Exercise 9.6: Use open sentences to solve problems  2. The product of two numbers is 840. One of the numbers is 12. What is the other number?"
- `ch09-b030-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Exercise 9.6: Use open sentences to solve problems
  - evidence quote: "### Exercise 9.6: Use open sentences to solve problems  3. 1,025 divided by a certain number gives a quotient (answer after dividing) of 25. What is the other number?"
- `ch09-b030-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Exercise 9.6: Use open sentences to solve problems
  - evidence quote: "### Exercise 9.6: Use open sentences to solve problems  4. The difference between two numbers is 17. If the larger number is 67, what is the smaller number?"
- `ch09-b030-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Exercise 9.6: Use open sentences to solve problems
  - evidence quote: "### Exercise 9.6: Use open sentences to solve problems  5. Usman is 1.8 m tall and his sister Jummai is $y$ m tall. The difference in their heights is 0.4 m. How tall is Jummai if she is shorter than Usman?"
- `ch09-b030-i06` [exercise_item] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Exercise 9.6: Use open sentences to solve problems
  - evidence quote: "### Exercise 9.6: Use open sentences to solve problems  6. A farmer has 24 rows of apple trees in his apple orchard. Each row has the same number of apple trees. If he has a total of 480 apple trees, how many trees are…"
- `ch09-b030-i07` [exercise_item] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Exercise 9.6: Use open sentences to solve problems
  - evidence quote: "### Exercise 9.6: Use open sentences to solve problems  7. The sum of three numbers is 208. One of the numbers is 88 and the other number is half of 88. What is the third number?"
- `ch09-b030-i08` [exercise_item] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Exercise 9.6: Use open sentences to solve problems
  - evidence quote: "### Exercise 9.6: Use open sentences to solve problems  8. Two sisters add their ages and see that they are 100 years old together. The younger sister is 45. How old is her older sister?"
- `ch09-b030-i09` [exercise_item] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Exercise 9.6: Use open sentences to solve problems
  - evidence quote: "### Exercise 9.6: Use open sentences to solve problems  9. A mother has 4 children. She wants to divide 35 sweets equally among them. If every child receives 8 sweets, how many are left over?"
- `ch09-b030-i10` [exercise_item] — placed in **review_items**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Exercise 9.6: Use open sentences to solve problems
  - evidence quote: "### Exercise 9.6: Use open sentences to solve problems  10. There are 126 plates of food available at a party. There are 38 guests at the party and they each receive the same amount of food. The family who hosts the par…"
- `ch09-b031` [summary] — placed in **excluded**
  - heading: Chapter 9: Using symbols > 9.4 Summary
  - evidence quote: "- A closed number sentence is always true or always false. - In an open number sentence, there is some information missing that we need to find. - An open number sentence can use picture symbols or variables to show whi…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: 28 records (closed-sentence true/false items, two-operation exposition and exercises, applied word-problem exposition/worked examples/exercises) belong to other subtopics in the chapter and are parked in review_items.
- **no_reused_assessment**: All three AOs have direct evidence but no reused assessment was selected.

### Per-atomic-objective evidence classification
- `open-sentences-ao-solve-problems` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch09-b007(worked_example), ch09-b008-i01(exercise), ch09-b008-i02(exercise), ch09-b008-i03(exercise), ch09-b008-i04(exercise), ch09-b008-i05(exercise), ch09-b008-i06(exercise), ch09-b008-i07(exercise), ch09-b008-i08(exercise), ch09-b008-i09(exercise), ch09-b008-i10(exercise), ch09-b012-i01(exercise), ch09-b012-i02(exercise), ch09-b012-i03(exercise), ch09-b012-i04(exercise), ch09-b012-i05(exercise), ch09-b012-i06(exercise), ch09-b012-i07(exercise), ch09-b012-i08(exercise), ch09-b012-i09(exercise), ch09-b012-i10(exercise), ch09-b014(worked_example), ch09-b022(worked_example), ch09-b023-i01(exercise), ch09-b023-i02(exercise), ch09-b023-i03(exercise), ch09-b023-i04(exercise), ch09-b023-i05(exercise), ch09-b023-i06(exercise), ch09-b023-i07(exercise), ch09-b023-i08(exercise), ch09-b023-i09(exercise), ch09-b023-i10(exercise)
  - assessment: _(none anchored)_
- `open-sentences-ao-identify-relationship-addition-and-subtraction` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch09-b015(instruction), ch09-b016(foundation), ch09-b017(instruction), ch09-b018(worked_example)
  - assessment: _(none anchored)_
- `open-sentences-ao-identify-relationship-multiplication-and-division` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch09-b019(worked_example)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All review_items were inspected. Candidate proposal added only for true/false closed sentences. The two-operation and word-problem open-sentence records are not proposed as new here because the curriculum already has separate subtopics for those skills.

### Candidate atomic objective proposals
- `open-sentences-candidate-ao-evaluate-closed-sentences` [prerequisite; candidate_for_expert_review]
  - proposed objective: Decide whether closed number sentences are true or false.
  - source records: ch09-b004-i01, ch09-b004-i02, ch09-b004-i03, ch09-b004-i04, ch09-b004-i05
  - closest existing AOs: open-sentences-ao-solve-problems, open-sentences-ao-identify-relationship-addition-and-subtraction, open-sentences-ao-identify-relationship-multiplication-and-division
  - candidate evidence quote: "Decide whether closed sentences are true or false"
  - rationale: The records ask learners to evaluate closed sentences, which is prerequisite contrast for open sentences but not solving open sentences.

---

## `jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences`

**Title:** Use of letters to represent symbols or shapes in open sentences  
**Status:** `needs_review`  
**Row review categories:** ao_no_evidence, no_reused_assessment, curriculum_textbook_mismatch

### Curriculum objectives (source)
- `jss1-math-use-of-symbols-use-of-letters-to-represent-symbols-or-shapes-in-open-sentences-po01`: Use letters to represent symbols or shapes in open sentences

### Atomic objectives
- `use-of-letters-in-open-sentences-ao-represent-symbols` [use/apply]: Use letters to represent symbols in open sentences.
- `use-of-letters-in-open-sentences-ao-represent-shapes` [use/apply]: Use letters to represent shapes in open sentences.

### Linked textbook records (36 total) — inspected
- `ch09-b009` [exposition] — placed in **shared_foundation**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Variables in open sentences
  - evidence quote: "So far we have worked with open sentences that contain a symbol such as a $\square$ or a $\bigcirc$. Instead of pictures like these, in mathematics it works better to use letters to represent missing information. These…"
- `ch09-b010` [definition] — placed in **shared_foundation**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Variables in open sentences
  - evidence quote: "**variable** A variable is a symbol for a number we do not know yet. It is usually a letter such as $x$ or $y$."
- `ch09-b011` [exposition] — placed in **shared_foundation**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Variables in open sentences
  - evidence quote: "If we have an expression, such as $x+5$, we cannot know the value of the $x$ unless it is given. If we give the $x$ different values, then we can make number sentences that are true.  If $x$ = 1, then $x+5 = 1 + 5 = 6$…"
- `ch09-b012` [exercise_block] — placed in **excluded**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.3: Find the value of the expression
  - evidence quote: "### Exercise 9.3: Find the value of the expression  Find the value of the following expressions if $x=3$."
- `ch09-b012-i01` [exercise_item] — placed in **AO:use-of-letters-in-open-sentences-ao-represent-symbols (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.3: Find the value of the expression
  - evidence quote: "### Exercise 9.3: Find the value of the expression  1. $$17 - x$$"
- `ch09-b012-i02` [exercise_item] — placed in **AO:use-of-letters-in-open-sentences-ao-represent-symbols (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.3: Find the value of the expression
  - evidence quote: "### Exercise 9.3: Find the value of the expression  2. $$3 + x$$"
- `ch09-b012-i03` [exercise_item] — placed in **AO:use-of-letters-in-open-sentences-ao-represent-symbols (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.3: Find the value of the expression
  - evidence quote: "### Exercise 9.3: Find the value of the expression  3. $$2\times x\times 0$$"
- `ch09-b012-i04` [exercise_item] — placed in **AO:use-of-letters-in-open-sentences-ao-represent-symbols (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.3: Find the value of the expression
  - evidence quote: "### Exercise 9.3: Find the value of the expression  4. $$9-x+2$$"
- `ch09-b012-i05` [exercise_item] — placed in **AO:use-of-letters-in-open-sentences-ao-represent-symbols (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.3: Find the value of the expression
  - evidence quote: "### Exercise 9.3: Find the value of the expression  5. $$\frac{1}{x}+ \frac{1}{x}$$"
- `ch09-b012-i06` [exercise_item] — placed in **AO:use-of-letters-in-open-sentences-ao-represent-symbols (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.3: Find the value of the expression
  - evidence quote: "### Exercise 9.3: Find the value of the expression  6. $$10\times x$$"
- `ch09-b012-i07` [exercise_item] — placed in **AO:use-of-letters-in-open-sentences-ao-represent-symbols (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.3: Find the value of the expression
  - evidence quote: "### Exercise 9.3: Find the value of the expression  7. $$60\div x$$"
- `ch09-b012-i08` [exercise_item] — placed in **AO:use-of-letters-in-open-sentences-ao-represent-symbols (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.3: Find the value of the expression
  - evidence quote: "### Exercise 9.3: Find the value of the expression  8. $$30 + 30 + x$$"
- `ch09-b012-i09` [exercise_item] — placed in **AO:use-of-letters-in-open-sentences-ao-represent-symbols (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.3: Find the value of the expression
  - evidence quote: "### Exercise 9.3: Find the value of the expression  9. $$x\times6$$"
- `ch09-b012-i10` [exercise_item] — placed in **AO:use-of-letters-in-open-sentences-ao-represent-symbols (exercise)**
  - heading: Chapter 9: Using symbols > 9.1 Finding missing information in open sentences > Exercise 9.3: Find the value of the expression
  - evidence quote: "### Exercise 9.3: Find the value of the expression  10. $$5 + x + 18$$"
- `ch09-b013` [exposition] — placed in **shared_foundation**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences that have variables
  - evidence quote: "Variables and open sentences form part of a section of mathematics we call algebra. To show that there is information that we must find, an open sentence can use a picture symbol (such as a box or a circle) or a variabl…"
- `ch09-b014` [worked_example] — placed in **AO:use-of-letters-in-open-sentences-ao-represent-symbols (worked_example)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences that have variables > Worked example 9.2: Finding the value of a variable using mental maths
  - evidence quote: "Find the value of $x$ in this open number sentence:  $$ x + 7 = 9 $$"
- `ch09-b015` [exposition] — placed in **shared_foundation**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences that have variables > Using inverse operations to solve open sentences
  - evidence quote: "Another way to find the value of $x$ in $x + 7 = 9$, is to use the **inverse operation** of addition. The inverse operation of addition is subtraction. In Chapter 5 you learnt that subtraction may be seen as another for…"
- `ch09-b016` [definition] — placed in **shared_foundation**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences that have variables > Using inverse operations to solve open sentences
  - evidence quote: "**inverse operation** An inverse operation does the opposite of another operation. Addition and subtraction are inverse operations, and multiplication and division are inverse operations."
- `ch09-b017` [exposition] — placed in **shared_foundation**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences that have variables > Using inverse operations to solve open sentences
  - evidence quote: "This closed number sentence is true:  $$ 2 + 7 = 9 $$  We know that this closed number sentence is also true:  $$ 2 = 9 - 7 $$  Notice that we get from the first number sentence to the second number sentence using the i…"
- `ch09-b018` [worked_example] — placed in **AO:use-of-letters-in-open-sentences-ao-represent-symbols (worked_example)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences that have variables > Worked example 9.3: Solving an open sentence using the inverse of addition
  - evidence quote: "Find the value of $x$ in this open sentence:  $$ x + 12 = 29 $$"
- `ch09-b019` [worked_example] — placed in **AO:use-of-letters-in-open-sentences-ao-represent-symbols (worked_example)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences that have variables > Worked example 9.4: Solving an open sentence using the inverse of multiplication
  - evidence quote: "Find the value of $y$ in this open sentence:  $$ y \times 3 = 27 $$"
- `ch09-b020` [exposition] — placed in **shared_foundation**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences that have variables > Using inverse operations to solve open sentences
  - evidence quote: "Note that an open sentence is not regarded as solved when the variable is negative, for example $-x=5$. The variable must be positive in your final answer, for example $x=-5$."
- `ch09-b021` [note] — placed in **shared_foundation**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences that have variables > Using inverse operations to solve open sentences
  - evidence quote: "The format $variable=\text{value}$ may be swapped around. Therefore, $x=7$ and $7=x$ has the same meaning."
- `ch09-b022` [worked_example] — placed in **AO:use-of-letters-in-open-sentences-ao-represent-symbols (worked_example)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences that have variables > Worked example 9.5: Solving an open sentence using the inverse operation on the variable
  - evidence quote: "Find the value of $x$:  $$ 18 -  x = 14 $$"
- `ch09-b023` [exercise_block] — placed in **excluded**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.4: Solve open sentences
  - evidence quote: "### Exercise 9.4: Solve open sentences  Find the value of the variable in the following open sentences:"
- `ch09-b023-i01` [exercise_item] — placed in **AO:use-of-letters-in-open-sentences-ao-represent-symbols (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.4: Solve open sentences
  - evidence quote: "### Exercise 9.4: Solve open sentences  1. y + 7 = 30"
- `ch09-b023-i02` [exercise_item] — placed in **AO:use-of-letters-in-open-sentences-ao-represent-symbols (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.4: Solve open sentences
  - evidence quote: "### Exercise 9.4: Solve open sentences  2. 3 + x = 15"
- `ch09-b023-i03` [exercise_item] — placed in **AO:use-of-letters-in-open-sentences-ao-represent-symbols (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.4: Solve open sentences
  - evidence quote: "### Exercise 9.4: Solve open sentences  3. z - 8 = 20"
- `ch09-b023-i04` [exercise_item] — placed in **AO:use-of-letters-in-open-sentences-ao-represent-symbols (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.4: Solve open sentences
  - evidence quote: "### Exercise 9.4: Solve open sentences  4. q  - 4 = -5"
- `ch09-b023-i05` [exercise_item] — placed in **AO:use-of-letters-in-open-sentences-ao-represent-symbols (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.4: Solve open sentences
  - evidence quote: "### Exercise 9.4: Solve open sentences  5. 17 - n = 20"
- `ch09-b023-i06` [exercise_item] — placed in **AO:use-of-letters-in-open-sentences-ao-represent-symbols (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.4: Solve open sentences
  - evidence quote: "### Exercise 9.4: Solve open sentences  6. 15 - p = -5"
- `ch09-b023-i07` [exercise_item] — placed in **AO:use-of-letters-in-open-sentences-ao-represent-symbols (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.4: Solve open sentences
  - evidence quote: "### Exercise 9.4: Solve open sentences  7. x \times 8 = 48"
- `ch09-b023-i08` [exercise_item] — placed in **AO:use-of-letters-in-open-sentences-ao-represent-symbols (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.4: Solve open sentences
  - evidence quote: "### Exercise 9.4: Solve open sentences  8. 3 \times y = 15"
- `ch09-b023-i09` [exercise_item] — placed in **AO:use-of-letters-in-open-sentences-ao-represent-symbols (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.4: Solve open sentences
  - evidence quote: "### Exercise 9.4: Solve open sentences  9. c\div 20 = 5"
- `ch09-b023-i10` [exercise_item] — placed in **AO:use-of-letters-in-open-sentences-ao-represent-symbols (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.4: Solve open sentences
  - evidence quote: "### Exercise 9.4: Solve open sentences  10. 40 \div x = 8"
- `ch09-b031` [summary] — placed in **excluded**
  - heading: Chapter 9: Using symbols > 9.4 Summary
  - evidence quote: "- A closed number sentence is always true or always false. - In an open number sentence, there is some information missing that we need to find. - An open number sentence can use picture symbols or variables to show whi…"

### Row-level review categories and manually authored reasons
- **ao_no_evidence**: represent-shapes AO has zero record_links: the linked records use letters to stand for unknown numbers (variables), not for geometric shapes.
- **no_reused_assessment**: represent-symbols AO has direct worked examples and exercises but no reused assessment was selected.
- **curriculum_textbook_mismatch**: The curriculum AO 'Use letters to represent shapes in open sentences' is not addressed by the chapter 9 textbook records.

### Per-atomic-objective evidence classification
- `use-of-letters-in-open-sentences-ao-represent-symbols` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch09-b014(worked_example), ch09-b018(worked_example), ch09-b019(worked_example), ch09-b022(worked_example), ch09-b012-i01(exercise), ch09-b012-i02(exercise), ch09-b012-i03(exercise), ch09-b012-i04(exercise), ch09-b012-i05(exercise), ch09-b012-i06(exercise), ch09-b012-i07(exercise), ch09-b012-i08(exercise), ch09-b012-i09(exercise), ch09-b012-i10(exercise), ch09-b023-i01(exercise), ch09-b023-i02(exercise), ch09-b023-i03(exercise), ch09-b023-i04(exercise), ch09-b023-i05(exercise), ch09-b023-i06(exercise), ch09-b023-i07(exercise), ch09-b023-i08(exercise), ch09-b023-i09(exercise), ch09-b023-i10(exercise)
  - assessment: _(none anchored)_
- `use-of-letters-in-open-sentences-ao-represent-shapes` → evidence: **none** · categories: ao_no_evidence, curriculum_textbook_mismatch
  - linked records: _(none)_
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All linked records were inspected. Candidate proposal retained for expression evaluation because the textbook asks learners to substitute variable values, a measurable applied skill beyond representing unknowns with letters.

### Candidate atomic objective proposals
- `use-of-letters-in-open-sentences-candidate-ao-find-expression-values-with-variables` [extension_or_enrichment; candidate_for_expert_review]
  - proposed objective: Find the value of algebraic expressions by substituting given values for variables.
  - source records: ch09-b011, ch09-b012-i01, ch09-b012-i02, ch09-b012-i03, ch09-b012-i04, ch09-b012-i05, ch09-b012-i06, ch09-b012-i07, ch09-b012-i08, ch09-b012-i09, ch09-b012-i10
  - closest existing AOs: use-of-letters-in-open-sentences-ao-represent-symbols
  - candidate evidence quote: "If we give the $x$ different values, then we can make number sentences that are true."
  - rationale: The records ask students to substitute a known value for a variable and evaluate expressions. That is separate from representing an unknown with a letter.

---

## `jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations`

**Title:** Solving open sentences with two arithmetic operations  
**Status:** `mapped`  
**Row review categories:** _(none — mapped or no-records baseline)_

### Curriculum objectives (source)
- `jss1-math-use-of-symbols-solving-open-sentences-with-two-arithmetic-operations-po01`: Solve open sentence problems involving two arithmetic operations

### Atomic objectives
- `solving-open-sentences-with-two-operations-ao-solve-problems` [solve/apply]: Solve open sentence problems involving two arithmetic operations.

### Linked textbook records (12 total) — inspected
- `ch09-b024` [exposition] — placed in **AO:solving-open-sentences-with-two-operations-ao-solve-problems (instruction)**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems
  - evidence quote: "Open number sentences may have more than one operation, for example $4-2+x=10$. To solve number sentences like these, you must remember the correct order of operations that you learnt last year:  1. **B**rackets 2. **O*…"
- `ch09-b025` [worked_example] — placed in **AO:solving-open-sentences-with-two-operations-ao-solve-problems (worked_example)**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Worked example 9.7: Solving a problem using open sentences
  - evidence quote: "Find the value of x:"
- `ch09-b026` [exercise_block] — placed in **excluded**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.5: Solve open sentences with two operations
  - evidence quote: "### Exercise 9.5: Solve open sentences with two operations  Find the value of the variable in the following open sentences:"
- `ch09-b026-i01` [exercise_item] — placed in **AO:solving-open-sentences-with-two-operations-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.5: Solve open sentences with two operations
  - evidence quote: "### Exercise 9.5: Solve open sentences with two operations  1. 3 + x - 4 = 20"
- `ch09-b026-i02` [exercise_item] — placed in **AO:solving-open-sentences-with-two-operations-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.5: Solve open sentences with two operations
  - evidence quote: "### Exercise 9.5: Solve open sentences with two operations  2. q \times 3 + 5 = 29"
- `ch09-b026-i03` [exercise_item] — placed in **AO:solving-open-sentences-with-two-operations-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.5: Solve open sentences with two operations
  - evidence quote: "### Exercise 9.5: Solve open sentences with two operations  3. t + 10 \div 2 = 12"
- `ch09-b026-i04` [exercise_item] — placed in **AO:solving-open-sentences-with-two-operations-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.5: Solve open sentences with two operations
  - evidence quote: "### Exercise 9.5: Solve open sentences with two operations  4. 5 - x + 2 = 12"
- `ch09-b026-i05` [exercise_item] — placed in **AO:solving-open-sentences-with-two-operations-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.5: Solve open sentences with two operations
  - evidence quote: "### Exercise 9.5: Solve open sentences with two operations  5. y \times 5 - 7 = 13"
- `ch09-b026-i06` [exercise_item] — placed in **AO:solving-open-sentences-with-two-operations-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.5: Solve open sentences with two operations
  - evidence quote: "### Exercise 9.5: Solve open sentences with two operations  6. p \div 2 - 5 = 25"
- `ch09-b026-i07` [exercise_item] — placed in **AO:solving-open-sentences-with-two-operations-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.5: Solve open sentences with two operations
  - evidence quote: "### Exercise 9.5: Solve open sentences with two operations  7. 5 \times -2 = 6 + v"
- `ch09-b026-i08` [exercise_item] — placed in **AO:solving-open-sentences-with-two-operations-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.2 Solving open sentences > Exercise 9.5: Solve open sentences with two operations
  - evidence quote: "### Exercise 9.5: Solve open sentences with two operations  8. 2 \times -6 = 24 \div r"
- `ch09-b031` [summary] — placed in **excluded**
  - heading: Chapter 9: Using symbols > 9.4 Summary
  - evidence quote: "- A closed number sentence is always true or always false. - In an open number sentence, there is some information missing that we need to find. - An open number sentence can use picture symbols or variables to show whi…"

### Row-level review categories and manually authored reasons
_None — all AOs have direct evidence and a reused assessment._

### Per-atomic-objective evidence classification
- `solving-open-sentences-with-two-operations-ao-solve-problems` → evidence: **direct** · categories: —
  - linked records: ch09-b024(instruction), ch09-b025(worked_example), ch09-b026-i01(exercise), ch09-b026-i02(exercise), ch09-b026-i03(exercise), ch09-b026-i04(exercise), ch09-b026-i05(exercise), ch09-b026-i06(exercise), ch09-b026-i07(exercise), ch09-b026-i08(exercise)
  - assessment: reused from `ch09-b026-i03`

---

## `jss1-math-use-of-symbols-word-problems-involving-use-of-symbols`

**Title:** Word problems involving use of symbols  
**Status:** `mapped`  
**Row review categories:** _(none — mapped or no-records baseline)_

### Curriculum objectives (source)
- `jss1-math-use-of-symbols-word-problems-involving-use-of-symbols-po01`: Solve word problems involving use of symbols

### Atomic objectives
- `word-problems-use-of-symbols-ao-solve-problems` [solve/apply]: Solve word problems involving use of symbols.

### Linked textbook records (15 total) — inspected
- `ch09-b027` [exposition] — placed in **AO:word-problems-use-of-symbols-ao-solve-problems (instruction)**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems
  - evidence quote: "We can use open sentences with variables to set out and solve problems that are described in words. Remember that we can translate the following words into mathematical operations:  | English | Mathematical symbol | | -…"
- `ch09-b028` [worked_example] — placed in **AO:word-problems-use-of-symbols-ao-solve-problems (worked_example)**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Worked example 9.7: Solving a problem using open sentences
  - evidence quote: "There are 32 students in one JSS1 class. If 20 of the students are boys, how many girls are there in this class?"
- `ch09-b029` [worked_example] — placed in **AO:word-problems-use-of-symbols-ao-solve-problems (worked_example)**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Worked example 9.8: Solving a problem using open sentences
  - evidence quote: "For six days of the week, Ndidi spends the same amount of time each day practising the violin. On the last day of the week, she practises only 30 minutes. Her total practice time for the week is 300 minutes. For how man…"
- `ch09-b030` [exercise_block] — placed in **excluded**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Exercise 9.6: Use open sentences to solve problems
  - evidence quote: "### Exercise 9.6: Use open sentences to solve problems"
- `ch09-b030-i01` [exercise_item] — placed in **AO:word-problems-use-of-symbols-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Exercise 9.6: Use open sentences to solve problems
  - evidence quote: "### Exercise 9.6: Use open sentences to solve problems  1. Two numbers add up to 28. One of the numbers is 10. What is the other number?"
- `ch09-b030-i02` [exercise_item] — placed in **AO:word-problems-use-of-symbols-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Exercise 9.6: Use open sentences to solve problems
  - evidence quote: "### Exercise 9.6: Use open sentences to solve problems  2. The product of two numbers is 840. One of the numbers is 12. What is the other number?"
- `ch09-b030-i03` [exercise_item] — placed in **AO:word-problems-use-of-symbols-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Exercise 9.6: Use open sentences to solve problems
  - evidence quote: "### Exercise 9.6: Use open sentences to solve problems  3. 1,025 divided by a certain number gives a quotient (answer after dividing) of 25. What is the other number?"
- `ch09-b030-i04` [exercise_item] — placed in **AO:word-problems-use-of-symbols-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Exercise 9.6: Use open sentences to solve problems
  - evidence quote: "### Exercise 9.6: Use open sentences to solve problems  4. The difference between two numbers is 17. If the larger number is 67, what is the smaller number?"
- `ch09-b030-i05` [exercise_item] — placed in **AO:word-problems-use-of-symbols-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Exercise 9.6: Use open sentences to solve problems
  - evidence quote: "### Exercise 9.6: Use open sentences to solve problems  5. Usman is 1.8 m tall and his sister Jummai is $y$ m tall. The difference in their heights is 0.4 m. How tall is Jummai if she is shorter than Usman?"
- `ch09-b030-i06` [exercise_item] — placed in **AO:word-problems-use-of-symbols-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Exercise 9.6: Use open sentences to solve problems
  - evidence quote: "### Exercise 9.6: Use open sentences to solve problems  6. A farmer has 24 rows of apple trees in his apple orchard. Each row has the same number of apple trees. If he has a total of 480 apple trees, how many trees are…"
- `ch09-b030-i07` [exercise_item] — placed in **AO:word-problems-use-of-symbols-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Exercise 9.6: Use open sentences to solve problems
  - evidence quote: "### Exercise 9.6: Use open sentences to solve problems  7. The sum of three numbers is 208. One of the numbers is 88 and the other number is half of 88. What is the third number?"
- `ch09-b030-i08` [exercise_item] — placed in **AO:word-problems-use-of-symbols-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Exercise 9.6: Use open sentences to solve problems
  - evidence quote: "### Exercise 9.6: Use open sentences to solve problems  8. Two sisters add their ages and see that they are 100 years old together. The younger sister is 45. How old is her older sister?"
- `ch09-b030-i09` [exercise_item] — placed in **AO:word-problems-use-of-symbols-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Exercise 9.6: Use open sentences to solve problems
  - evidence quote: "### Exercise 9.6: Use open sentences to solve problems  9. A mother has 4 children. She wants to divide 35 sweets equally among them. If every child receives 8 sweets, how many are left over?"
- `ch09-b030-i10` [exercise_item] — placed in **AO:word-problems-use-of-symbols-ao-solve-problems (exercise)**
  - heading: Chapter 9: Using symbols > 9.3 Using open sentences to solve problems > Exercise 9.6: Use open sentences to solve problems
  - evidence quote: "### Exercise 9.6: Use open sentences to solve problems  10. There are 126 plates of food available at a party. There are 38 guests at the party and they each receive the same amount of food. The family who hosts the par…"
- `ch09-b031` [summary] — placed in **excluded**
  - heading: Chapter 9: Using symbols > 9.4 Summary
  - evidence quote: "- A closed number sentence is always true or always false. - In an open number sentence, there is some information missing that we need to find. - An open number sentence can use picture symbols or variables to show whi…"

### Row-level review categories and manually authored reasons
_None — all AOs have direct evidence and a reused assessment._

### Per-atomic-objective evidence classification
- `word-problems-use-of-symbols-ao-solve-problems` → evidence: **direct** · categories: —
  - linked records: ch09-b027(instruction), ch09-b028(worked_example), ch09-b029(worked_example), ch09-b030-i01(exercise), ch09-b030-i02(exercise), ch09-b030-i03(exercise), ch09-b030-i04(exercise), ch09-b030-i05(exercise), ch09-b030-i06(exercise), ch09-b030-i07(exercise), ch09-b030-i08(exercise), ch09-b030-i09(exercise), ch09-b030-i10(exercise)
  - assessment: reused from `ch09-b030-i03`

---

## `jss1-math-use-of-symbols-quantitative-aptitude`

**Title:** Quantitative aptitude  
**Status:** `no_records`  
**Row review categories:** corpus_gap

### Curriculum objectives (source)
- `jss1-math-use-of-symbols-quantitative-aptitude-po01`: Solve quantitative aptitude problems on the use of symbols

### Atomic objectives
- `use-of-symbols-quantitative-aptitude-ao-solve-problems` [solve/apply]: Solve quantitative aptitude problems on the use of symbols.

### Linked textbook records (0 total) — inspected
_No textbook records are linked to this subtopic (corpus_gap)._

### Row-level review categories and manually authored reasons
- **corpus_gap**: No textbook records are linked to this subtopic in the linked corpus.

### Per-atomic-objective evidence classification
- `use-of-symbols-quantitative-aptitude-ao-solve-problems` → evidence: **none** · categories: corpus_gap
  - linked records: _(none)_
  - assessment: _(none anchored)_

---

## `jss1-math-simplification-of-algebraic-expressions-like-and-unlike-terms-in-algebraic-expressions`

**Title:** Like and unlike terms in algebraic expressions  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-simplification-of-algebraic-expressions-like-and-unlike-terms-in-algebraic-expressions-po01`: Identify and collect like terms in a given expression

### Atomic objectives
- `like-and-unlike-terms-ao-identify-like-terms` [identify/remember]: Identify like terms in a given expression.
- `like-and-unlike-terms-ao-collect-like-terms` [collect/apply]: Collect like terms in a given expression.

### Linked textbook records (72 total) — inspected
- `ch10-b001` [exposition] — placed in **shared_foundation**
  - heading: Chapter 10: Simplification of algebraic expressions
  - evidence quote: "So far we have dealt with open sentences that involve using a symbol or a variable (a letter that represents a number) and contain an equals sign. This is part of a topic in mathematics we call algebra. In this chapter…"
- `ch10-b002` [exposition] — placed in **shared_foundation**
  - heading: Chapter 10: Simplification of algebraic expressions > 10.1 Algebraic expressions and terms
  - evidence quote: "Open sentences are made up of algebraic expressions. An algebraic expression is a mathematical phrase or statement that contains numbers, symbols, variables (such as $x$ or $q$) and operators (such as $+$, $-$, $\times$…"
- `ch10-b003` [definition] — placed in **shared_foundation**
  - heading: Chapter 10: Simplification of algebraic expressions > 10.1 Algebraic expressions and terms
  - evidence quote: "**algebraic expression** An algebraic expression is a mathematical statement that contains a combination of numbers, symbols, variables and mathematical operators. It does not have an equals sign."
- `ch10-b004` [exposition] — placed in **shared_foundation**
  - heading: Chapter 10: Simplification of algebraic expressions > 10.1 Algebraic expressions and terms
  - evidence quote: "Algebraic expressions are made up of **terms** that are separated by an addition ($+$) or a subtraction (-) sign.  The algebraic expression $2x+1$ has two terms.  $-3m-7n+2$ has 3 terms.  $2a + b - 6c + 4$ has 4 terms."
- `ch10-b005` [definition] — placed in **shared_foundation**
  - heading: Chapter 10: Simplification of algebraic expressions > 10.1 Algebraic expressions and terms
  - evidence quote: "**term** A term can be a single number (positive or negative), or a variable, or one or more numbers and variables that are being multiplied together. Terms are separated by $+$ or $-$ signs."
- `ch10-b006` [exposition] — placed in **shared_foundation**
  - heading: Chapter 10: Simplification of algebraic expressions > 10.1 Algebraic expressions and terms
  - evidence quote: "Here are some examples of single terms:  $$3xyz$$  $$a$$  $$-7x^2$$  $$-20$$  $$-4\times3x$$  Here are some examples of algebraic expressions with two terms:  $$3xyz + 7$$  $$a - b$$  $$x + x$$  Here are some examples o…"
- `ch10-b007` [worked_example] — placed in **shared_foundation**
  - heading: Chapter 10: Simplification of algebraic expressions > 10.1 Algebraic expressions and terms > Worked example 10.1: Determining number of terms
  - evidence quote: "How many terms does the following algebraic expression have?  $$3x + 2y - 6$$"
- `ch10-b008` [exercise_block] — placed in **excluded**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.1 Algebraic expressions and terms > Exercise 10.1: Determine the number of terms in an algebraic expression
  - evidence quote: "### Exercise 10.1: Determine the number of terms in an algebraic expression  How many terms do each of the following algebraic expressions contain?"
- `ch10-b008-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.1 Algebraic expressions and terms > Exercise 10.1: Determine the number of terms in an algebraic expression
  - evidence quote: "### Exercise 10.1: Determine the number of terms in an algebraic expression  1. $$2x+1$$"
- `ch10-b008-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.1 Algebraic expressions and terms > Exercise 10.1: Determine the number of terms in an algebraic expression
  - evidence quote: "### Exercise 10.1: Determine the number of terms in an algebraic expression  2. $$-3+7yz+x$$"
- `ch10-b008-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.1 Algebraic expressions and terms > Exercise 10.1: Determine the number of terms in an algebraic expression
  - evidence quote: "### Exercise 10.1: Determine the number of terms in an algebraic expression  3. $$8\times p$$"
- `ch10-b008-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.1 Algebraic expressions and terms > Exercise 10.1: Determine the number of terms in an algebraic expression
  - evidence quote: "### Exercise 10.1: Determine the number of terms in an algebraic expression  4. $$3 \times 7x \times 5y \times -1$$"
- `ch10-b008-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.1 Algebraic expressions and terms > Exercise 10.1: Determine the number of terms in an algebraic expression
  - evidence quote: "### Exercise 10.1: Determine the number of terms in an algebraic expression  5. $$-1 + x - 2y^2 \times z$$"
- `ch10-b008-i06` [exercise_item] — placed in **review_items**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.1 Algebraic expressions and terms > Exercise 10.1: Determine the number of terms in an algebraic expression
  - evidence quote: "### Exercise 10.1: Determine the number of terms in an algebraic expression  6. $$2x+2x$$"
- `ch10-b008-i07` [exercise_item] — placed in **review_items**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.1 Algebraic expressions and terms > Exercise 10.1: Determine the number of terms in an algebraic expression
  - evidence quote: "### Exercise 10.1: Determine the number of terms in an algebraic expression  7. $$-3+3$$"
- `ch10-b008-i08` [exercise_item] — placed in **review_items**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.1 Algebraic expressions and terms > Exercise 10.1: Determine the number of terms in an algebraic expression
  - evidence quote: "### Exercise 10.1: Determine the number of terms in an algebraic expression  8. $$8\times p \times p$$"
- `ch10-b008-i09` [exercise_item] — placed in **review_items**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.1 Algebraic expressions and terms > Exercise 10.1: Determine the number of terms in an algebraic expression
  - evidence quote: "### Exercise 10.1: Determine the number of terms in an algebraic expression  9. $$x \times x \times x \times x$$"
- `ch10-b008-i10` [exercise_item] — placed in **review_items**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.1 Algebraic expressions and terms > Exercise 10.1: Determine the number of terms in an algebraic expression
  - evidence quote: "### Exercise 10.1: Determine the number of terms in an algebraic expression  10. $$y + y +y$$"
- `ch10-b009` [exposition] — placed in **shared_foundation**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions
  - evidence quote: "When you learnt to add or subtract objects you learnt that, for example:  - 1 apple + 1 apple + 1 apple + 1 apple can be written as 4 apples  When you started working with multiplication you learnt that, for example:  -…"
- `ch10-b010` [note] — placed in **shared_foundation**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions
  - evidence quote: "In algebra, we normally do not write the multiplication sign between a number and a variable. For example, we write $4 \times a$ as $4a$."
- `ch10-b011` [exposition] — placed in **shared_foundation**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions
  - evidence quote: "Here are a few more examples:  $$x + x + x + x + x + x + x = 7 \times x = 7x$$ $$p + p + p = 3 \times p = 3p$$ $$y + y = 2 \times y = 2y$$ $$m + m + m + m + m = 5 \times m = 5m$$"
- `ch10-b012` [worked_example] — placed in **shared_foundation**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Worked example 10.2: Writing algebraic expressions
  - evidence quote: "Write the following expression using a simpler notation:  $$ y + y + y + y + y $$"
- `ch10-b013` [exercise_block] — placed in **excluded**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.2: Simplify expressions
  - evidence quote: "### Exercise 10.2: Simplify expressions  Write the following expressions in a simpler notation:"
- `ch10-b013-i01` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.2: Simplify expressions
  - evidence quote: "### Exercise 10.2: Simplify expressions  1. $$x+x$$"
- `ch10-b013-i02` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.2: Simplify expressions
  - evidence quote: "### Exercise 10.2: Simplify expressions  2. $$3+3+3+3+3+3+3$$"
- `ch10-b013-i03` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.2: Simplify expressions
  - evidence quote: "### Exercise 10.2: Simplify expressions  3. $$8\times p$$"
- `ch10-b013-i04` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.2: Simplify expressions
  - evidence quote: "### Exercise 10.2: Simplify expressions  4. $$3 \times 7 \times y$$"
- `ch10-b013-i05` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.2: Simplify expressions
  - evidence quote: "### Exercise 10.2: Simplify expressions  5. $$x + x + x + x + x$$"
- `ch10-b013-i06` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.2: Simplify expressions
  - evidence quote: "### Exercise 10.2: Simplify expressions  6. $$2x + 2x + 2x$$"
- `ch10-b013-i07` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.2: Simplify expressions
  - evidence quote: "### Exercise 10.2: Simplify expressions  7. $$k + k + k + k + k + k$$"
- `ch10-b013-i08` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.2: Simplify expressions
  - evidence quote: "### Exercise 10.2: Simplify expressions  8. $$5 \times m$$"
- `ch10-b013-i09` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.2: Simplify expressions
  - evidence quote: "### Exercise 10.2: Simplify expressions  9. $$5x + 5x + 5x + 5x$$"
- `ch10-b013-i10` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.2: Simplify expressions
  - evidence quote: "### Exercise 10.2: Simplify expressions  10. $$(-2) + (-2) + (-2)$$"
- `ch10-b016` [exposition] — placed in **shared_foundation**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Constants and coefficients
  - evidence quote: "Here are some more examples of terms that will vary in value, depending on the value of the variable:  $$ p + p + p = 3p $$  $$ y + y = 2y $$  $$ m + m + m + m + m = 5m $$  In $3p$, the 3 is the coefficient of $p$. We k…"
- `ch10-b017` [worked_example] — placed in **AO:like-and-unlike-terms-ao-identify-like-terms (worked_example)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Worked example 10.3: Identifying the different parts of an algebraic expression
  - evidence quote: "For the algebraic expression below, write down the number of terms, the constant term, the coefficient of $x$, the coefficient of $y$ and the coefficient of $k$.  $$ 2x + y -4k -6 $$"
- `ch10-b018` [exercise_block] — placed in **excluded**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.3: Identify parts of an algebraic expression
  - evidence quote: "### Exercise 10.3: Identify parts of an algebraic expression"
- `ch10-b018-i01` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-identify-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.3: Identify parts of an algebraic expression
  - evidence quote: "### Exercise 10.3: Identify parts of an algebraic expression  1. How many terms does this expression contain?  $$ 3 	imes m + 2 $$"
- `ch10-b018-i02` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-identify-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.3: Identify parts of an algebraic expression
  - evidence quote: "### Exercise 10.3: Identify parts of an algebraic expression  2. What is the constant in this algebraic expression?  $$ -3+7yz+x $$"
- `ch10-b018-i03` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-identify-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.3: Identify parts of an algebraic expression
  - evidence quote: "### Exercise 10.3: Identify parts of an algebraic expression  3. What is the coefficient of this term?  $$ 8	imes p $$"
- `ch10-b018-i04` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-identify-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.3: Identify parts of an algebraic expression
  - evidence quote: "### Exercise 10.3: Identify parts of an algebraic expression  4. Answer the questions about this expression: $3 	imes 7x - 5y -1$.  a) How many terms does this expression have? b) What is the coefficient of $x$? c) What…"
- `ch10-b018-i05` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-identify-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.3: Identify parts of an algebraic expression
  - evidence quote: "### Exercise 10.3: Identify parts of an algebraic expression  5. Answer the questions about this expression: $10 - x - 2y + z$.  a) How many terms does this expression have? b) What is the coefficient of $x$? c) What is…"
- `ch10-b019` [exposition] — placed in **AO:like-and-unlike-terms-ao-identify-like-terms (instruction)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms
  - evidence quote: "We have seen that we can add $p + p + p$ to get $3p$.  These three terms are called **like terms** because they all contain the same variable, $p$.  We can also add $3x + 4x$. Because both terms have the variable $x$, w…"
- `ch10-b020` [definition] — placed in **AO:like-and-unlike-terms-ao-identify-like-terms (foundation)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms
  - evidence quote: "**like terms** Like terms contain the same variable or variables.  **simplify an expression** To simplify an expression is to give it in its simplest form. We do this by collecting (combining) like terms using addition…"
- `ch10-b021` [exposition] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (instruction)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms
  - evidence quote: "We can add or subtract any number of like terms.  For example:  $$ 4x + 2x + 5x + 10x = 21x $$  $$ 10x - 2x + 3x - x + 14x = 24x $$  Terms that do not have the same variables are called **unlike terms**. If we find an e…"
- `ch10-b022` [definition] — placed in **AO:like-and-unlike-terms-ao-identify-like-terms (foundation)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms
  - evidence quote: "**unlike terms** Unlike terms contain different variables."
- `ch10-b023` [exercise_block] — placed in **excluded**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.4: Add and subtract like terms
  - evidence quote: "### Exercise 10.4: Add and subtract like terms  Simplify the following expressions."
- `ch10-b023-i01` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.4: Add and subtract like terms
  - evidence quote: "### Exercise 10.4: Add and subtract like terms  1. $2h + 3h$"
- `ch10-b023-i02` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.4: Add and subtract like terms
  - evidence quote: "### Exercise 10.4: Add and subtract like terms  2. $18p - 16p$"
- `ch10-b023-i03` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.4: Add and subtract like terms
  - evidence quote: "### Exercise 10.4: Add and subtract like terms  3. $9x - 10x$"
- `ch10-b023-i04` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.4: Add and subtract like terms
  - evidence quote: "### Exercise 10.4: Add and subtract like terms  4. $13x +2y$"
- `ch10-b023-i05` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.4: Add and subtract like terms
  - evidence quote: "### Exercise 10.4: Add and subtract like terms  5. $-20b + b$"
- `ch10-b023-i06` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.4: Add and subtract like terms
  - evidence quote: "### Exercise 10.4: Add and subtract like terms  6. $28k - k + 13k$"
- `ch10-b023-i07` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.4: Add and subtract like terms
  - evidence quote: "### Exercise 10.4: Add and subtract like terms  7. $28k - 28k$"
- `ch10-b023-i08` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.4: Add and subtract like terms
  - evidence quote: "### Exercise 10.4: Add and subtract like terms  8. $-7x + 7x - 12x + 24x$"
- `ch10-b023-i09` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.4: Add and subtract like terms
  - evidence quote: "### Exercise 10.4: Add and subtract like terms  9. $11a + 11b$"
- `ch10-b023-i10` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.4: Add and subtract like terms
  - evidence quote: "### Exercise 10.4: Add and subtract like terms  10. $3x -2$"
- `ch10-b024` [exposition] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (instruction)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms
  - evidence quote: "Sometimes expressions contain both like terms and unlike terms. To simplify an expression like this, we collect the like terms. This means we rearrange the terms first to group all the like terms together. Then we add o…"
- `ch10-b025` [worked_example] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (worked_example)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Worked example 10.4: Collecting like terms to simplify an expression
  - evidence quote: "Simplify the expression $2x + 3y + 5x + 2y$ by collecting the like terms."
- `ch10-b026` [worked_example] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (worked_example)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Worked example 10.5: Collecting like terms to simplify an expression
  - evidence quote: "Simplify the expression by collecting the like terms.  $$ 8x + 13y - x - 4y $$"
- `ch10-b027` [worked_example] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (worked_example)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Worked example 10.6: Collecting like terms to simplify an expression
  - evidence quote: "Simplify the expression by collecting the like terms.  $$ -2x - 3y + 5 + 10x - 3 - 2y $$"
- `ch10-b028` [exercise_block] — placed in **excluded**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.5: Simplify by collecting like terms
  - evidence quote: "### Exercise 10.5: Simplify by collecting like terms  Simplify the following expressions by collecting like terms."
- `ch10-b028-i01` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.5: Simplify by collecting like terms
  - evidence quote: "### Exercise 10.5: Simplify by collecting like terms  1. $$ 2h + 5m + 3h + 2m + m $$"
- `ch10-b028-i02` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.5: Simplify by collecting like terms
  - evidence quote: "### Exercise 10.5: Simplify by collecting like terms  2. $$ 18p - 2x - 16p - x $$"
- `ch10-b028-i03` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.5: Simplify by collecting like terms
  - evidence quote: "### Exercise 10.5: Simplify by collecting like terms  3. $$ 9x - 3y - 2y -10x + y $$"
- `ch10-b028-i04` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.5: Simplify by collecting like terms
  - evidence quote: "### Exercise 10.5: Simplify by collecting like terms  4. $$ 13x +2y + 7y - 6x - x $$"
- `ch10-b028-i05` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.5: Simplify by collecting like terms
  - evidence quote: "### Exercise 10.5: Simplify by collecting like terms  5. $$ -2a -20b - 6a + b $$"
- `ch10-b028-i06` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.5: Simplify by collecting like terms
  - evidence quote: "### Exercise 10.5: Simplify by collecting like terms  6. $$ 2 + 8k - k + 9 $$"
- `ch10-b028-i07` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.5: Simplify by collecting like terms
  - evidence quote: "### Exercise 10.5: Simplify by collecting like terms  7. $$ 28 -4m - 16 - 28m $$"
- `ch10-b028-i08` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.5: Simplify by collecting like terms
  - evidence quote: "### Exercise 10.5: Simplify by collecting like terms  8. $$ -7x + 7y + 7x - 7y $$"
- `ch10-b028-i09` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.5: Simplify by collecting like terms
  - evidence quote: "### Exercise 10.5: Simplify by collecting like terms  9. $$ 11a + 11b + 11c - 4a - 2b + c $$"
- `ch10-b028-i10` [exercise_item] — placed in **AO:like-and-unlike-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.5: Simplify by collecting like terms
  - evidence quote: "### Exercise 10.5: Simplify by collecting like terms  10. $$ 3x -2 - 4 - 5x - 2y $$"
- `ch10-b050` [summary] — placed in **excluded**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Summary
  - evidence quote: "- An algebraic expression is a mathematical statement that contains a combination of numbers, symbols, variables and mathematical operators. It does not have an equals sign. - A term can be a single number (positive or…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch10-b008-i01..i10 (count number of terms in an expression) are prerequisite to identifying like terms but not the AO skill itself, and were parked in review_items.
- **no_reused_assessment**: Both AOs have direct evidence (worked examples and exercises) but no reused assessment was selected.

### Per-atomic-objective evidence classification
- `like-and-unlike-terms-ao-identify-like-terms` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch10-b017(worked_example), ch10-b018-i01(exercise), ch10-b018-i02(exercise), ch10-b018-i03(exercise), ch10-b018-i04(exercise), ch10-b018-i05(exercise), ch10-b019(instruction), ch10-b020(foundation), ch10-b022(foundation)
  - assessment: _(none anchored)_
- `like-and-unlike-terms-ao-collect-like-terms` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch10-b013-i01(exercise), ch10-b013-i02(exercise), ch10-b013-i03(exercise), ch10-b013-i04(exercise), ch10-b013-i05(exercise), ch10-b013-i06(exercise), ch10-b013-i07(exercise), ch10-b013-i08(exercise), ch10-b013-i09(exercise), ch10-b013-i10(exercise), ch10-b021(instruction), ch10-b023-i01(exercise), ch10-b023-i02(exercise), ch10-b023-i03(exercise), ch10-b023-i04(exercise), ch10-b023-i05(exercise), ch10-b023-i06(exercise), ch10-b023-i07(exercise), ch10-b023-i08(exercise), ch10-b023-i09(exercise), ch10-b023-i10(exercise), ch10-b024(instruction), ch10-b025(worked_example), ch10-b026(worked_example), ch10-b027(worked_example), ch10-b028-i01(exercise), ch10-b028-i02(exercise), ch10-b028-i03(exercise), ch10-b028-i04(exercise), ch10-b028-i05(exercise), ch10-b028-i06(exercise), ch10-b028-i07(exercise), ch10-b028-i08(exercise), ch10-b028-i09(exercise), ch10-b028-i10(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All review_items were inspected. Candidate proposal added for counting terms because the records teach identifying expression structure before like-term collection.

### Candidate atomic objective proposals
- `like-and-unlike-terms-candidate-ao-determine-number-of-terms` [prerequisite; candidate_for_expert_review]
  - proposed objective: Determine the number of terms in an algebraic expression.
  - source records: ch10-b008-i01, ch10-b008-i02, ch10-b008-i03, ch10-b008-i04, ch10-b008-i05, ch10-b008-i06, ch10-b008-i07, ch10-b008-i08, ch10-b008-i09, ch10-b008-i10
  - closest existing AOs: like-and-unlike-terms-ao-identify-like-terms, like-and-unlike-terms-ao-collect-like-terms
  - candidate evidence quote: "Determine the number of terms in an algebraic expression"
  - rationale: Counting terms is a prerequisite expression-structure skill but not the same as identifying like terms or collecting them.

---

## `jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions`

**Title:** Identification of coefficients of terms of algebraic expressions  
**Status:** `needs_review`  
**Row review categories:** ao_no_evidence, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions-po01`: Identify the coefficient of a given algebraic term
- `jss1-math-simplification-of-algebraic-expressions-identification-of-coefficients-of-terms-of-algebraic-expressions-po02`: Identify the positive and negative coefficients of a given algebraic term

### Atomic objectives
- `identification-of-coefficients-ao-identify-coefficient` [identify/remember]: Identify the coefficient of a given algebraic term.
- `identification-of-coefficients-ao-identify-positive-coefficient` [identify/remember]: Identify the positive coefficient of a given algebraic term.
- `identification-of-coefficients-ao-identify-negative-coefficient` [identify/remember]: Identify the negative coefficient of a given algebraic term.

### Linked textbook records (11 total) — inspected
- `ch10-b014` [exposition] — placed in **shared_foundation**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Constants and coefficients
  - evidence quote: "There are two other words you also need to know and understand when working with algebraic terms: constant and coefficient.  The following algebraic expression contains two terms:  $$-4x + 5$$  5 is called a **constant*…"
- `ch10-b015` [definition] — placed in **shared_foundation**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Constants and coefficients
  - evidence quote: "**constant** A constant is a term without a variable. A constant can have a negative value (if it has a minus sign in front of it) or a positive value (if it has a plus sign or no sign in front of it).  **coefficient**…"
- `ch10-b016` [exposition] — placed in **shared_foundation**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Constants and coefficients
  - evidence quote: "Here are some more examples of terms that will vary in value, depending on the value of the variable:  $$ p + p + p = 3p $$  $$ y + y = 2y $$  $$ m + m + m + m + m = 5m $$  In $3p$, the 3 is the coefficient of $p$. We k…"
- `ch10-b017` [worked_example] — placed in **AO:identification-of-coefficients-ao-identify-coefficient (worked_example)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Worked example 10.3: Identifying the different parts of an algebraic expression
  - evidence quote: "For the algebraic expression below, write down the number of terms, the constant term, the coefficient of $x$, the coefficient of $y$ and the coefficient of $k$.  $$ 2x + y -4k -6 $$"
- `ch10-b018` [exercise_block] — placed in **excluded**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.3: Identify parts of an algebraic expression
  - evidence quote: "### Exercise 10.3: Identify parts of an algebraic expression"
- `ch10-b018-i01` [exercise_item] — placed in **AO:identification-of-coefficients-ao-identify-coefficient (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.3: Identify parts of an algebraic expression
  - evidence quote: "### Exercise 10.3: Identify parts of an algebraic expression  1. How many terms does this expression contain?  $$ 3 	imes m + 2 $$"
- `ch10-b018-i02` [exercise_item] — placed in **AO:identification-of-coefficients-ao-identify-coefficient (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.3: Identify parts of an algebraic expression
  - evidence quote: "### Exercise 10.3: Identify parts of an algebraic expression  2. What is the constant in this algebraic expression?  $$ -3+7yz+x $$"
- `ch10-b018-i03` [exercise_item] — placed in **AO:identification-of-coefficients-ao-identify-coefficient (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.3: Identify parts of an algebraic expression
  - evidence quote: "### Exercise 10.3: Identify parts of an algebraic expression  3. What is the coefficient of this term?  $$ 8	imes p $$"
- `ch10-b018-i04` [exercise_item] — placed in **AO:identification-of-coefficients-ao-identify-coefficient (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.3: Identify parts of an algebraic expression
  - evidence quote: "### Exercise 10.3: Identify parts of an algebraic expression  4. Answer the questions about this expression: $3 	imes 7x - 5y -1$.  a) How many terms does this expression have? b) What is the coefficient of $x$? c) What…"
- `ch10-b018-i05` [exercise_item] — placed in **AO:identification-of-coefficients-ao-identify-coefficient (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.3: Identify parts of an algebraic expression
  - evidence quote: "### Exercise 10.3: Identify parts of an algebraic expression  5. Answer the questions about this expression: $10 - x - 2y + z$.  a) How many terms does this expression have? b) What is the coefficient of $x$? c) What is…"
- `ch10-b050` [summary] — placed in **excluded**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Summary
  - evidence quote: "- An algebraic expression is a mathematical statement that contains a combination of numbers, symbols, variables and mathematical operators. It does not have an equals sign. - A term can be a single number (positive or…"

### Row-level review categories and manually authored reasons
- **ao_no_evidence**: identify-positive-coefficient and identify-negative-coefficient AOs have no record_links; the linked records do not separately exercise sign-specific coefficient identification.
- **no_reused_assessment**: identify-coefficient AO has direct evidence but no reused exercise_item assessment was selected.

### Per-atomic-objective evidence classification
- `identification-of-coefficients-ao-identify-coefficient` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch10-b017(worked_example), ch10-b018-i01(exercise), ch10-b018-i02(exercise), ch10-b018-i03(exercise), ch10-b018-i04(exercise), ch10-b018-i05(exercise)
  - assessment: _(none anchored)_
- `identification-of-coefficients-ao-identify-positive-coefficient` → evidence: **none** · categories: ao_no_evidence
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `identification-of-coefficients-ao-identify-negative-coefficient` → evidence: **none** · categories: ao_no_evidence
  - linked records: _(none)_
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms`

**Title:** Basic arithmetic operations applied to algebraic expressions of similar terms  
**Status:** `mapped`  
**Row review categories:** _(none — mapped or no-records baseline)_

### Curriculum objectives (source)
- `jss1-math-simplification-of-algebraic-expressions-basic-arithmetic-operations-applied-to-algebraic-expressions-of-similar-terms-po01`: Perform basic arithmetic operations on expressions of similar terms

### Atomic objectives
- `basic-arithmetic-operations-on-similar-terms-ao-perform-operations` [perform/apply]: Perform basic arithmetic operations on expressions of similar terms.

### Linked textbook records (31 total) — inspected
- `ch10-b009` [exposition] — placed in **shared_foundation**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions
  - evidence quote: "When you learnt to add or subtract objects you learnt that, for example:  - 1 apple + 1 apple + 1 apple + 1 apple can be written as 4 apples  When you started working with multiplication you learnt that, for example:  -…"
- `ch10-b010` [note] — placed in **shared_foundation**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions
  - evidence quote: "In algebra, we normally do not write the multiplication sign between a number and a variable. For example, we write $4 \times a$ as $4a$."
- `ch10-b011` [exposition] — placed in **shared_foundation**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions
  - evidence quote: "Here are a few more examples:  $$x + x + x + x + x + x + x = 7 \times x = 7x$$ $$p + p + p = 3 \times p = 3p$$ $$y + y = 2 \times y = 2y$$ $$m + m + m + m + m = 5 \times m = 5m$$"
- `ch10-b012` [worked_example] — placed in **AO:basic-arithmetic-operations-on-similar-terms-ao-perform-operations (worked_example)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Worked example 10.2: Writing algebraic expressions
  - evidence quote: "Write the following expression using a simpler notation:  $$ y + y + y + y + y $$"
- `ch10-b013` [exercise_block] — placed in **excluded**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.2: Simplify expressions
  - evidence quote: "### Exercise 10.2: Simplify expressions  Write the following expressions in a simpler notation:"
- `ch10-b013-i01` [exercise_item] — placed in **AO:basic-arithmetic-operations-on-similar-terms-ao-perform-operations (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.2: Simplify expressions
  - evidence quote: "### Exercise 10.2: Simplify expressions  1. $$x+x$$"
- `ch10-b013-i02` [exercise_item] — placed in **AO:basic-arithmetic-operations-on-similar-terms-ao-perform-operations (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.2: Simplify expressions
  - evidence quote: "### Exercise 10.2: Simplify expressions  2. $$3+3+3+3+3+3+3$$"
- `ch10-b013-i03` [exercise_item] — placed in **AO:basic-arithmetic-operations-on-similar-terms-ao-perform-operations (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.2: Simplify expressions
  - evidence quote: "### Exercise 10.2: Simplify expressions  3. $$8\times p$$"
- `ch10-b013-i04` [exercise_item] — placed in **AO:basic-arithmetic-operations-on-similar-terms-ao-perform-operations (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.2: Simplify expressions
  - evidence quote: "### Exercise 10.2: Simplify expressions  4. $$3 \times 7 \times y$$"
- `ch10-b013-i05` [exercise_item] — placed in **AO:basic-arithmetic-operations-on-similar-terms-ao-perform-operations (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.2: Simplify expressions
  - evidence quote: "### Exercise 10.2: Simplify expressions  5. $$x + x + x + x + x$$"
- `ch10-b013-i06` [exercise_item] — placed in **AO:basic-arithmetic-operations-on-similar-terms-ao-perform-operations (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.2: Simplify expressions
  - evidence quote: "### Exercise 10.2: Simplify expressions  6. $$2x + 2x + 2x$$"
- `ch10-b013-i07` [exercise_item] — placed in **AO:basic-arithmetic-operations-on-similar-terms-ao-perform-operations (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.2: Simplify expressions
  - evidence quote: "### Exercise 10.2: Simplify expressions  7. $$k + k + k + k + k + k$$"
- `ch10-b013-i08` [exercise_item] — placed in **AO:basic-arithmetic-operations-on-similar-terms-ao-perform-operations (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.2: Simplify expressions
  - evidence quote: "### Exercise 10.2: Simplify expressions  8. $$5 \times m$$"
- `ch10-b013-i09` [exercise_item] — placed in **AO:basic-arithmetic-operations-on-similar-terms-ao-perform-operations (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.2: Simplify expressions
  - evidence quote: "### Exercise 10.2: Simplify expressions  9. $$5x + 5x + 5x + 5x$$"
- `ch10-b013-i10` [exercise_item] — placed in **AO:basic-arithmetic-operations-on-similar-terms-ao-perform-operations (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.2 Working with algebraic expressions > Exercise 10.2: Simplify expressions
  - evidence quote: "### Exercise 10.2: Simplify expressions  10. $$(-2) + (-2) + (-2)$$"
- `ch10-b019` [exposition] — placed in **shared_foundation**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms
  - evidence quote: "We have seen that we can add $p + p + p$ to get $3p$.  These three terms are called **like terms** because they all contain the same variable, $p$.  We can also add $3x + 4x$. Because both terms have the variable $x$, w…"
- `ch10-b020` [definition] — placed in **shared_foundation**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms
  - evidence quote: "**like terms** Like terms contain the same variable or variables.  **simplify an expression** To simplify an expression is to give it in its simplest form. We do this by collecting (combining) like terms using addition…"
- `ch10-b021` [exposition] — placed in **shared_foundation**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms
  - evidence quote: "We can add or subtract any number of like terms.  For example:  $$ 4x + 2x + 5x + 10x = 21x $$  $$ 10x - 2x + 3x - x + 14x = 24x $$  Terms that do not have the same variables are called **unlike terms**. If we find an e…"
- `ch10-b022` [definition] — placed in **shared_foundation**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms
  - evidence quote: "**unlike terms** Unlike terms contain different variables."
- `ch10-b023` [exercise_block] — placed in **excluded**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.4: Add and subtract like terms
  - evidence quote: "### Exercise 10.4: Add and subtract like terms  Simplify the following expressions."
- `ch10-b023-i01` [exercise_item] — placed in **AO:basic-arithmetic-operations-on-similar-terms-ao-perform-operations (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.4: Add and subtract like terms
  - evidence quote: "### Exercise 10.4: Add and subtract like terms  1. $2h + 3h$"
- `ch10-b023-i02` [exercise_item] — placed in **AO:basic-arithmetic-operations-on-similar-terms-ao-perform-operations (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.4: Add and subtract like terms
  - evidence quote: "### Exercise 10.4: Add and subtract like terms  2. $18p - 16p$"
- `ch10-b023-i03` [exercise_item] — placed in **AO:basic-arithmetic-operations-on-similar-terms-ao-perform-operations (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.4: Add and subtract like terms
  - evidence quote: "### Exercise 10.4: Add and subtract like terms  3. $9x - 10x$"
- `ch10-b023-i04` [exercise_item] — placed in **AO:basic-arithmetic-operations-on-similar-terms-ao-perform-operations (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.4: Add and subtract like terms
  - evidence quote: "### Exercise 10.4: Add and subtract like terms  4. $13x +2y$"
- `ch10-b023-i05` [exercise_item] — placed in **AO:basic-arithmetic-operations-on-similar-terms-ao-perform-operations (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.4: Add and subtract like terms
  - evidence quote: "### Exercise 10.4: Add and subtract like terms  5. $-20b + b$"
- `ch10-b023-i06` [exercise_item] — placed in **AO:basic-arithmetic-operations-on-similar-terms-ao-perform-operations (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.4: Add and subtract like terms
  - evidence quote: "### Exercise 10.4: Add and subtract like terms  6. $28k - k + 13k$"
- `ch10-b023-i07` [exercise_item] — placed in **AO:basic-arithmetic-operations-on-similar-terms-ao-perform-operations (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.4: Add and subtract like terms
  - evidence quote: "### Exercise 10.4: Add and subtract like terms  7. $28k - 28k$"
- `ch10-b023-i08` [exercise_item] — placed in **AO:basic-arithmetic-operations-on-similar-terms-ao-perform-operations (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.4: Add and subtract like terms
  - evidence quote: "### Exercise 10.4: Add and subtract like terms  8. $-7x + 7x - 12x + 24x$"
- `ch10-b023-i09` [exercise_item] — placed in **AO:basic-arithmetic-operations-on-similar-terms-ao-perform-operations (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.4: Add and subtract like terms
  - evidence quote: "### Exercise 10.4: Add and subtract like terms  9. $11a + 11b$"
- `ch10-b023-i10` [exercise_item] — placed in **AO:basic-arithmetic-operations-on-similar-terms-ao-perform-operations (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.4: Add and subtract like terms
  - evidence quote: "### Exercise 10.4: Add and subtract like terms  10. $3x -2$"
- `ch10-b050` [summary] — placed in **excluded**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Summary
  - evidence quote: "- An algebraic expression is a mathematical statement that contains a combination of numbers, symbols, variables and mathematical operators. It does not have an equals sign. - A term can be a single number (positive or…"

### Row-level review categories and manually authored reasons
_None — all AOs have direct evidence and a reused assessment._

### Per-atomic-objective evidence classification
- `basic-arithmetic-operations-on-similar-terms-ao-perform-operations` → evidence: **direct** · categories: —
  - linked records: ch10-b012(worked_example), ch10-b013-i01(exercise), ch10-b013-i02(exercise), ch10-b013-i03(exercise), ch10-b013-i04(exercise), ch10-b013-i05(exercise), ch10-b013-i06(exercise), ch10-b013-i07(exercise), ch10-b013-i08(exercise), ch10-b013-i09(exercise), ch10-b013-i10(exercise), ch10-b023-i01(exercise), ch10-b023-i02(exercise), ch10-b023-i03(exercise), ch10-b023-i04(exercise), ch10-b023-i05(exercise), ch10-b023-i06(exercise), ch10-b023-i07(exercise), ch10-b023-i08(exercise), ch10-b023-i09(exercise), ch10-b023-i10(exercise)
  - assessment: reused from `ch10-b013-i03`

---

## `jss1-math-simplification-of-algebraic-expressions-collection-and-simplification-of-like-and-unlike-terms-in-algebraic-expressions`

**Title:** Collection and simplification of like and unlike terms in algebraic expressions  
**Status:** `needs_review`  
**Row review categories:** ao_no_evidence, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-simplification-of-algebraic-expressions-collection-and-simplification-of-like-and-unlike-terms-in-algebraic-expressions-po01`: Identify and collect like terms in a given expression and simplify

### Atomic objectives
- `collection-and-simplification-of-terms-ao-identify-like-terms` [identify/remember]: Identify like terms in a given expression.
- `collection-and-simplification-of-terms-ao-collect-like-terms` [collect/apply]: Collect like terms in a given expression.
- `collection-and-simplification-of-terms-ao-simplify-expression` [simplify/apply]: Simplify a given algebraic expression.

### Linked textbook records (37 total) — inspected
- `ch10-b024` [exposition] — placed in **shared_foundation**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms
  - evidence quote: "Sometimes expressions contain both like terms and unlike terms. To simplify an expression like this, we collect the like terms. This means we rearrange the terms first to group all the like terms together. Then we add o…"
- `ch10-b025` [worked_example] — placed in **AO:collection-and-simplification-of-terms-ao-collect-like-terms (worked_example)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Worked example 10.4: Collecting like terms to simplify an expression
  - evidence quote: "Simplify the expression $2x + 3y + 5x + 2y$ by collecting the like terms."
- `ch10-b026` [worked_example] — placed in **AO:collection-and-simplification-of-terms-ao-collect-like-terms (worked_example)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Worked example 10.5: Collecting like terms to simplify an expression
  - evidence quote: "Simplify the expression by collecting the like terms.  $$ 8x + 13y - x - 4y $$"
- `ch10-b027` [worked_example] — placed in **AO:collection-and-simplification-of-terms-ao-collect-like-terms (worked_example)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Worked example 10.6: Collecting like terms to simplify an expression
  - evidence quote: "Simplify the expression by collecting the like terms.  $$ -2x - 3y + 5 + 10x - 3 - 2y $$"
- `ch10-b028` [exercise_block] — placed in **excluded**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.5: Simplify by collecting like terms
  - evidence quote: "### Exercise 10.5: Simplify by collecting like terms  Simplify the following expressions by collecting like terms."
- `ch10-b028-i01` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.5: Simplify by collecting like terms
  - evidence quote: "### Exercise 10.5: Simplify by collecting like terms  1. $$ 2h + 5m + 3h + 2m + m $$"
- `ch10-b028-i02` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.5: Simplify by collecting like terms
  - evidence quote: "### Exercise 10.5: Simplify by collecting like terms  2. $$ 18p - 2x - 16p - x $$"
- `ch10-b028-i03` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.5: Simplify by collecting like terms
  - evidence quote: "### Exercise 10.5: Simplify by collecting like terms  3. $$ 9x - 3y - 2y -10x + y $$"
- `ch10-b028-i04` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.5: Simplify by collecting like terms
  - evidence quote: "### Exercise 10.5: Simplify by collecting like terms  4. $$ 13x +2y + 7y - 6x - x $$"
- `ch10-b028-i05` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.5: Simplify by collecting like terms
  - evidence quote: "### Exercise 10.5: Simplify by collecting like terms  5. $$ -2a -20b - 6a + b $$"
- `ch10-b028-i06` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.5: Simplify by collecting like terms
  - evidence quote: "### Exercise 10.5: Simplify by collecting like terms  6. $$ 2 + 8k - k + 9 $$"
- `ch10-b028-i07` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.5: Simplify by collecting like terms
  - evidence quote: "### Exercise 10.5: Simplify by collecting like terms  7. $$ 28 -4m - 16 - 28m $$"
- `ch10-b028-i08` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.5: Simplify by collecting like terms
  - evidence quote: "### Exercise 10.5: Simplify by collecting like terms  8. $$ -7x + 7y + 7x - 7y $$"
- `ch10-b028-i09` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.5: Simplify by collecting like terms
  - evidence quote: "### Exercise 10.5: Simplify by collecting like terms  9. $$ 11a + 11b + 11c - 4a - 2b + c $$"
- `ch10-b028-i10` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-collect-like-terms (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.3 Adding and subtracting like terms > Exercise 10.5: Simplify by collecting like terms
  - evidence quote: "### Exercise 10.5: Simplify by collecting like terms  10. $$ 3x -2 - 4 - 5x - 2y $$"
- `ch10-b040` [note] — placed in **AO:collection-and-simplification-of-terms-ao-simplify-expression (instruction)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law
  - evidence quote: "When you expand, you do not need to write all the steps separately as shown in the worked examples above. You can go directly to the answer by writing each new term as you work it out. So your answer could look like thi…"
- `ch10-b041` [exercise_block] — placed in **excluded**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.8: Use the distributive law to expand and simplify expressions
  - evidence quote: "### Exercise 10.8: Use the distributive law to expand and simplify expressions  Use the distributive law to expand the brackets and then simplify the expressions."
- `ch10-b041-i01` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-simplify-expression (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.8: Use the distributive law to expand and simplify expressions
  - evidence quote: "### Exercise 10.8: Use the distributive law to expand and simplify expressions  Use the distributive law to expand the brackets and then simplify the expressions.  1. $$ 3(2 + a - 4x) $$"
- `ch10-b041-i02` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-simplify-expression (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.8: Use the distributive law to expand and simplify expressions
  - evidence quote: "### Exercise 10.8: Use the distributive law to expand and simplify expressions  Use the distributive law to expand the brackets and then simplify the expressions.  2. $$ 5(2n - 16 - m)+4m $$"
- `ch10-b041-i03` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-simplify-expression (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.8: Use the distributive law to expand and simplify expressions
  - evidence quote: "### Exercise 10.8: Use the distributive law to expand and simplify expressions  Use the distributive law to expand the brackets and then simplify the expressions.  3. $$ 2(3x - 3y + 3)+3x-3y+3 $$"
- `ch10-b041-i04` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-simplify-expression (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.8: Use the distributive law to expand and simplify expressions
  - evidence quote: "### Exercise 10.8: Use the distributive law to expand and simplify expressions  Use the distributive law to expand the brackets and then simplify the expressions.  4. $$ 5(3x-4y+z)+3(x+y-2z) $$"
- `ch10-b041-i05` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-simplify-expression (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.8: Use the distributive law to expand and simplify expressions
  - evidence quote: "### Exercise 10.8: Use the distributive law to expand and simplify expressions  Use the distributive law to expand the brackets and then simplify the expressions.  5. $$ 3(12a + 11b + 11c) -(2a - b + c) $$"
- `ch10-b042` [exposition] — placed in **AO:collection-and-simplification-of-terms-ao-simplify-expression (instruction)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Order of operations
  - evidence quote: "In Chapter 9 you were reminded of the correct order of operations that you learnt last year:  1. **B**rackets 2. **O**f 3. **D**ivide 4. **M**ultiply 5. **A**dd 6. **S**ubtract"
- `ch10-b043` [worked_example] — placed in **AO:collection-and-simplification-of-terms-ao-simplify-expression (worked_example)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Worked example 10.11: Following the correct order of operations
  - evidence quote: "Simplify the expression $2(3x+5x+1)+4\times3x$."
- `ch10-b044` [worked_example] — placed in **AO:collection-and-simplification-of-terms-ao-simplify-expression (worked_example)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Worked example 10.12: Following the correct order of operations
  - evidence quote: "Simplify the expression $(2y+6y)\div(2\times2) \times 10-5\times2y+2y$."
- `ch10-b045` [exercise_block] — placed in **excluded**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.9: Follow the correct order of operations to simplify expressions
  - evidence quote: "### Exercise 10.9: Follow the correct order of operations to simplify expressions  Simplify the expressions."
- `ch10-b045-i01` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-simplify-expression (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.9: Follow the correct order of operations to simplify expressions
  - evidence quote: "### Exercise 10.9: Follow the correct order of operations to simplify expressions  Simplify the expressions.  1. $$ 5y-(4y-3y) $$"
- `ch10-b045-i02` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-simplify-expression (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.9: Follow the correct order of operations to simplify expressions
  - evidence quote: "### Exercise 10.9: Follow the correct order of operations to simplify expressions  Simplify the expressions.  2. $$ 4x(7 - 2)-(x + 2) $$"
- `ch10-b045-i03` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-simplify-expression (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.9: Follow the correct order of operations to simplify expressions
  - evidence quote: "### Exercise 10.9: Follow the correct order of operations to simplify expressions  Simplify the expressions.  3. $$ x(2+3\times4)-(x+2x) $$"
- `ch10-b045-i04` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-simplify-expression (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.9: Follow the correct order of operations to simplify expressions
  - evidence quote: "### Exercise 10.9: Follow the correct order of operations to simplify expressions  Simplify the expressions.  4. $$ 4x\times 2+3x \times 9 \div 3 $$"
- `ch10-b045-i05` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-simplify-expression (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.9: Follow the correct order of operations to simplify expressions
  - evidence quote: "### Exercise 10.9: Follow the correct order of operations to simplify expressions  Simplify the expressions.  5. $$ 2(x+y)-(2x+y-3x) $$"
- `ch10-b045-i06` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-simplify-expression (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.9: Follow the correct order of operations to simplify expressions
  - evidence quote: "### Exercise 10.9: Follow the correct order of operations to simplify expressions  Simplify the expressions.  6. $$ 5y-(4y-4)+2y\times 3 $$"
- `ch10-b045-i07` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-simplify-expression (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.9: Follow the correct order of operations to simplify expressions
  - evidence quote: "### Exercise 10.9: Follow the correct order of operations to simplify expressions  Simplify the expressions.  7. $$ -(p+q)-p+q+2(p-q) $$"
- `ch10-b045-i08` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-simplify-expression (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.9: Follow the correct order of operations to simplify expressions
  - evidence quote: "### Exercise 10.9: Follow the correct order of operations to simplify expressions  Simplify the expressions.  8. $$ -3m(-5+2+3)+2m\times3 $$"
- `ch10-b045-i09` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-simplify-expression (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.9: Follow the correct order of operations to simplify expressions
  - evidence quote: "### Exercise 10.9: Follow the correct order of operations to simplify expressions  Simplify the expressions.  9. $$ 8x \div 2+4\times 2x+2 $$"
- `ch10-b045-i10` [exercise_item] — placed in **AO:collection-and-simplification-of-terms-ao-simplify-expression (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.9: Follow the correct order of operations to simplify expressions
  - evidence quote: "### Exercise 10.9: Follow the correct order of operations to simplify expressions  Simplify the expressions.  10. $$ 3(-2a + b + c + 4a - 2b + c)-(a - b - c) $$"
- `ch10-b050` [summary] — placed in **excluded**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Summary
  - evidence quote: "- An algebraic expression is a mathematical statement that contains a combination of numbers, symbols, variables and mathematical operators. It does not have an equals sign. - A term can be a single number (positive or…"

### Row-level review categories and manually authored reasons
- **ao_no_evidence**: identify-like-terms AO has no record_links in this subtopic; identification is covered under the like-and-unlike-terms subtopic.
- **no_reused_assessment**: The collect-like-terms and simplify-expression AOs have direct evidence but no reused assessment.

### Per-atomic-objective evidence classification
- `collection-and-simplification-of-terms-ao-identify-like-terms` → evidence: **none** · categories: ao_no_evidence
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `collection-and-simplification-of-terms-ao-collect-like-terms` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch10-b025(worked_example), ch10-b026(worked_example), ch10-b027(worked_example), ch10-b028-i01(exercise), ch10-b028-i02(exercise), ch10-b028-i03(exercise), ch10-b028-i04(exercise), ch10-b028-i05(exercise), ch10-b028-i06(exercise), ch10-b028-i07(exercise), ch10-b028-i08(exercise), ch10-b028-i09(exercise), ch10-b028-i10(exercise)
  - assessment: _(none anchored)_
- `collection-and-simplification-of-terms-ao-simplify-expression` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch10-b040(instruction), ch10-b041-i01(exercise), ch10-b041-i02(exercise), ch10-b041-i03(exercise), ch10-b041-i04(exercise), ch10-b041-i05(exercise), ch10-b042(instruction), ch10-b043(worked_example), ch10-b044(worked_example), ch10-b045-i01(exercise), ch10-b045-i02(exercise), ch10-b045-i03(exercise), ch10-b045-i04(exercise), ch10-b045-i05(exercise), ch10-b045-i06(exercise), ch10-b045-i07(exercise), ch10-b045-i08(exercise), ch10-b045-i09(exercise), ch10-b045-i10(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-simplification-of-algebraic-expressions-use-of-brackets`

**Title:** Use of brackets  
**Status:** `needs_review`  
**Row review categories:** ao_no_evidence, no_reused_assessment, curriculum_textbook_mismatch

### Curriculum objectives (source)
- `jss1-math-simplification-of-algebraic-expressions-use-of-brackets-po01`: Insert/remove brackets and simplify expressions

### Atomic objectives
- `use-of-brackets-ao-insert-brackets` [insert/apply]: Insert brackets in expressions.
- `use-of-brackets-ao-remove-brackets` [remove/apply]: Remove brackets from expressions.
- `use-of-brackets-ao-simplify-expressions` [simplify/apply]: Simplify expressions.

### Linked textbook records (47 total) — inspected
- `ch10-b029` [exposition] — placed in **shared_foundation**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.4 Working with brackets in algebraic expressions
  - evidence quote: "We sometimes use brackets to group terms in algebraic expressions together.  As you know, $2x$ means $2 \times x = x + x$.  If we replace the $x$ with $(x + y)$, then in the same way:  $$ 2(x + y) = 2 \times (x + y) $$…"
- `ch10-b030` [worked_example] — placed in **AO:use-of-brackets-ao-remove-brackets (worked_example)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.4 Working with brackets in algebraic expressions > Worked example 10.7: Removing brackets using repeated addition
  - evidence quote: "$4m = 4 \times m$. Replace the $m$ with $(a + b)$. Then remove the brackets and simplify the expression."
- `ch10-b031` [exercise_block] — placed in **excluded**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.4 Working with brackets in algebraic expressions > Exercise 10.6: Remove brackets and simplify
  - evidence quote: "### Exercise 10.6: Remove brackets and simplify  Remove the brackets using repeated addition and then simplify."
- `ch10-b031-i01` [exercise_item] — placed in **AO:use-of-brackets-ao-remove-brackets (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.4 Working with brackets in algebraic expressions > Exercise 10.6: Remove brackets and simplify
  - evidence quote: "### Exercise 10.6: Remove brackets and simplify  1. $$ 2(h +m) $$"
- `ch10-b031-i02` [exercise_item] — placed in **AO:use-of-brackets-ao-remove-brackets (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.4 Working with brackets in algebraic expressions > Exercise 10.6: Remove brackets and simplify
  - evidence quote: "### Exercise 10.6: Remove brackets and simplify  2. $$ 3(p +k) $$"
- `ch10-b031-i03` [exercise_item] — placed in **AO:use-of-brackets-ao-remove-brackets (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.4 Working with brackets in algebraic expressions > Exercise 10.6: Remove brackets and simplify
  - evidence quote: "### Exercise 10.6: Remove brackets and simplify  3. $$ 2(a + 2) $$"
- `ch10-b031-i04` [exercise_item] — placed in **AO:use-of-brackets-ao-remove-brackets (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.4 Working with brackets in algebraic expressions > Exercise 10.6: Remove brackets and simplify
  - evidence quote: "### Exercise 10.6: Remove brackets and simplify  4. $$ 3(4x +3y) $$"
- `ch10-b031-i05` [exercise_item] — placed in **AO:use-of-brackets-ao-remove-brackets (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.4 Working with brackets in algebraic expressions > Exercise 10.6: Remove brackets and simplify
  - evidence quote: "### Exercise 10.6: Remove brackets and simplify  5. $$ 2(10a - 6b + c) $$"
- `ch10-b032` [exposition] — placed in **AO:use-of-brackets-ao-remove-brackets (instruction)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.4 Working with brackets in algebraic expressions > Negative signs before brackets
  - evidence quote: "Up to now we only worked with brackets that have a positive sign in front of them. When there is a negative sign before a bracket, it affects all the terms inside the bracket.  Look at this example:  $$ 10-(2+3) $$  We…"
- `ch10-b033` [worked_example] — placed in **AO:use-of-brackets-ao-remove-brackets (worked_example)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.4 Working with brackets in algebraic expressions > Worked example 10.8: Removing brackets with negative signs in front
  - evidence quote: "Remove the brackets and then simplify the following expression:  $$ 2(4m+n)-(5m+3n) $$"
- `ch10-b034` [exercise_block] — placed in **excluded**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.4 Working with brackets in algebraic expressions > Exercise 10.7: Remove brackets with negative signs and simplify
  - evidence quote: "### Exercise 10.7: Remove brackets with negative signs and simplify  Remove the brackets and then simplify."
- `ch10-b034-i01` [exercise_item] — placed in **AO:use-of-brackets-ao-remove-brackets (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.4 Working with brackets in algebraic expressions > Exercise 10.7: Remove brackets with negative signs and simplify
  - evidence quote: "### Exercise 10.7: Remove brackets with negative signs and simplify  Remove the brackets and then simplify.  1. $$ 3k-(2p +k) $$"
- `ch10-b034-i02` [exercise_item] — placed in **AO:use-of-brackets-ao-remove-brackets (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.4 Working with brackets in algebraic expressions > Exercise 10.7: Remove brackets with negative signs and simplify
  - evidence quote: "### Exercise 10.7: Remove brackets with negative signs and simplify  Remove the brackets and then simplify.  2. $$ 2h +m-(m+2h)-m $$"
- `ch10-b034-i03` [exercise_item] — placed in **AO:use-of-brackets-ao-remove-brackets (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.4 Working with brackets in algebraic expressions > Exercise 10.7: Remove brackets with negative signs and simplify
  - evidence quote: "### Exercise 10.7: Remove brackets with negative signs and simplify  Remove the brackets and then simplify.  3. $$ -(4x +3y)+(2x-y) $$"
- `ch10-b034-i04` [exercise_item] — placed in **AO:use-of-brackets-ao-remove-brackets (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.4 Working with brackets in algebraic expressions > Exercise 10.7: Remove brackets with negative signs and simplify
  - evidence quote: "### Exercise 10.7: Remove brackets with negative signs and simplify  Remove the brackets and then simplify.  4. $$ 3(a + 2)-(4a+2) $$"
- `ch10-b034-i05` [exercise_item] — placed in **AO:use-of-brackets-ao-remove-brackets (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.4 Working with brackets in algebraic expressions > Exercise 10.7: Remove brackets with negative signs and simplify
  - evidence quote: "### Exercise 10.7: Remove brackets with negative signs and simplify  Remove the brackets and then simplify.  5. $$ 2(10a - 6b + c)-(3c-2b-a)-(b+c) $$"
- `ch10-b035` [note] — placed in **AO:use-of-brackets-ao-remove-brackets (instruction)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.4 Working with brackets in algebraic expressions > Negative signs before brackets
  - evidence quote: "When we change the signs of the terms inside a bracket that has a negative sign in front of it, we actually multiply each term by $-1$. You will learn more about this next year."
- `ch10-b036` [exposition] — placed in **AO:use-of-brackets-ao-remove-brackets (instruction)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law
  - evidence quote: "When we have an expression with brackets, we know we need to multiply. When we do the multiplication, we say that we **expand** the expression.  From the examples and the exercises above, can you see a shorter way than…"
- `ch10-b037` [definition] — placed in **AO:use-of-brackets-ao-remove-brackets (foundation)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law
  - evidence quote: "**expand** To expand an algebraic expression is to multiply what is outside the brackets (the coefficient of the bracket) by each of the terms that is inside the bracket.  **distributive law** The distributive law state…"
- `ch10-b038` [worked_example] — placed in **AO:use-of-brackets-ao-remove-brackets (worked_example)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Worked example 10.9: Multiplying the coefficient of a bracket by two terms inside
  - evidence quote: "Expand this expression:  $$ 3(2a + b) $$"
- `ch10-b039` [worked_example] — placed in **AO:use-of-brackets-ao-remove-brackets (worked_example)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Worked example 10.10: Multiplying the coefficient of a bracket by three terms inside
  - evidence quote: "Expand the expression $2(a + 5b - 3c)$."
- `ch10-b040` [note] — placed in **AO:use-of-brackets-ao-remove-brackets (instruction)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law
  - evidence quote: "When you expand, you do not need to write all the steps separately as shown in the worked examples above. You can go directly to the answer by writing each new term as you work it out. So your answer could look like thi…"
- `ch10-b041` [exercise_block] — placed in **excluded**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.8: Use the distributive law to expand and simplify expressions
  - evidence quote: "### Exercise 10.8: Use the distributive law to expand and simplify expressions  Use the distributive law to expand the brackets and then simplify the expressions."
- `ch10-b041-i01` [exercise_item] — placed in **AO:use-of-brackets-ao-remove-brackets (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.8: Use the distributive law to expand and simplify expressions
  - evidence quote: "### Exercise 10.8: Use the distributive law to expand and simplify expressions  Use the distributive law to expand the brackets and then simplify the expressions.  1. $$ 3(2 + a - 4x) $$"
- `ch10-b041-i02` [exercise_item] — placed in **AO:use-of-brackets-ao-remove-brackets (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.8: Use the distributive law to expand and simplify expressions
  - evidence quote: "### Exercise 10.8: Use the distributive law to expand and simplify expressions  Use the distributive law to expand the brackets and then simplify the expressions.  2. $$ 5(2n - 16 - m)+4m $$"
- `ch10-b041-i03` [exercise_item] — placed in **AO:use-of-brackets-ao-remove-brackets (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.8: Use the distributive law to expand and simplify expressions
  - evidence quote: "### Exercise 10.8: Use the distributive law to expand and simplify expressions  Use the distributive law to expand the brackets and then simplify the expressions.  3. $$ 2(3x - 3y + 3)+3x-3y+3 $$"
- `ch10-b041-i04` [exercise_item] — placed in **AO:use-of-brackets-ao-remove-brackets (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.8: Use the distributive law to expand and simplify expressions
  - evidence quote: "### Exercise 10.8: Use the distributive law to expand and simplify expressions  Use the distributive law to expand the brackets and then simplify the expressions.  4. $$ 5(3x-4y+z)+3(x+y-2z) $$"
- `ch10-b041-i05` [exercise_item] — placed in **AO:use-of-brackets-ao-remove-brackets (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.8: Use the distributive law to expand and simplify expressions
  - evidence quote: "### Exercise 10.8: Use the distributive law to expand and simplify expressions  Use the distributive law to expand the brackets and then simplify the expressions.  5. $$ 3(12a + 11b + 11c) -(2a - b + c) $$"
- `ch10-b042` [exposition] — placed in **AO:use-of-brackets-ao-simplify-expressions (instruction)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Order of operations
  - evidence quote: "In Chapter 9 you were reminded of the correct order of operations that you learnt last year:  1. **B**rackets 2. **O**f 3. **D**ivide 4. **M**ultiply 5. **A**dd 6. **S**ubtract"
- `ch10-b043` [worked_example] — placed in **AO:use-of-brackets-ao-simplify-expressions (worked_example)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Worked example 10.11: Following the correct order of operations
  - evidence quote: "Simplify the expression $2(3x+5x+1)+4\times3x$."
- `ch10-b044` [worked_example] — placed in **AO:use-of-brackets-ao-simplify-expressions (worked_example)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Worked example 10.12: Following the correct order of operations
  - evidence quote: "Simplify the expression $(2y+6y)\div(2\times2) \times 10-5\times2y+2y$."
- `ch10-b045` [exercise_block] — placed in **excluded**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.9: Follow the correct order of operations to simplify expressions
  - evidence quote: "### Exercise 10.9: Follow the correct order of operations to simplify expressions  Simplify the expressions."
- `ch10-b045-i01` [exercise_item] — placed in **AO:use-of-brackets-ao-simplify-expressions (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.9: Follow the correct order of operations to simplify expressions
  - evidence quote: "### Exercise 10.9: Follow the correct order of operations to simplify expressions  Simplify the expressions.  1. $$ 5y-(4y-3y) $$"
- `ch10-b045-i02` [exercise_item] — placed in **AO:use-of-brackets-ao-simplify-expressions (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.9: Follow the correct order of operations to simplify expressions
  - evidence quote: "### Exercise 10.9: Follow the correct order of operations to simplify expressions  Simplify the expressions.  2. $$ 4x(7 - 2)-(x + 2) $$"
- `ch10-b045-i03` [exercise_item] — placed in **AO:use-of-brackets-ao-simplify-expressions (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.9: Follow the correct order of operations to simplify expressions
  - evidence quote: "### Exercise 10.9: Follow the correct order of operations to simplify expressions  Simplify the expressions.  3. $$ x(2+3\times4)-(x+2x) $$"
- `ch10-b045-i04` [exercise_item] — placed in **AO:use-of-brackets-ao-simplify-expressions (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.9: Follow the correct order of operations to simplify expressions
  - evidence quote: "### Exercise 10.9: Follow the correct order of operations to simplify expressions  Simplify the expressions.  4. $$ 4x\times 2+3x \times 9 \div 3 $$"
- `ch10-b045-i05` [exercise_item] — placed in **AO:use-of-brackets-ao-simplify-expressions (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.9: Follow the correct order of operations to simplify expressions
  - evidence quote: "### Exercise 10.9: Follow the correct order of operations to simplify expressions  Simplify the expressions.  5. $$ 2(x+y)-(2x+y-3x) $$"
- `ch10-b045-i06` [exercise_item] — placed in **AO:use-of-brackets-ao-simplify-expressions (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.9: Follow the correct order of operations to simplify expressions
  - evidence quote: "### Exercise 10.9: Follow the correct order of operations to simplify expressions  Simplify the expressions.  6. $$ 5y-(4y-4)+2y\times 3 $$"
- `ch10-b045-i07` [exercise_item] — placed in **AO:use-of-brackets-ao-simplify-expressions (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.9: Follow the correct order of operations to simplify expressions
  - evidence quote: "### Exercise 10.9: Follow the correct order of operations to simplify expressions  Simplify the expressions.  7. $$ -(p+q)-p+q+2(p-q) $$"
- `ch10-b045-i08` [exercise_item] — placed in **AO:use-of-brackets-ao-simplify-expressions (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.9: Follow the correct order of operations to simplify expressions
  - evidence quote: "### Exercise 10.9: Follow the correct order of operations to simplify expressions  Simplify the expressions.  8. $$ -3m(-5+2+3)+2m\times3 $$"
- `ch10-b045-i09` [exercise_item] — placed in **AO:use-of-brackets-ao-simplify-expressions (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.9: Follow the correct order of operations to simplify expressions
  - evidence quote: "### Exercise 10.9: Follow the correct order of operations to simplify expressions  Simplify the expressions.  9. $$ 8x \div 2+4\times 2x+2 $$"
- `ch10-b045-i10` [exercise_item] — placed in **AO:use-of-brackets-ao-simplify-expressions (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.5 Working with brackets using the distributive law > Exercise 10.9: Follow the correct order of operations to simplify expressions
  - evidence quote: "### Exercise 10.9: Follow the correct order of operations to simplify expressions  Simplify the expressions.  10. $$ 3(-2a + b + c + 4a - 2b + c)-(a - b - c) $$"
- `ch10-b046` [exposition] — placed in **AO:use-of-brackets-ao-simplify-expressions (instruction)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Practical applications > Using area to show the distributive law in practice
  - evidence quote: "We can use areas to show the distributive law in practice. For example, look at the two rectangles shown below. There are two ways in which we can write the total area of the two rectangles.  **Method 1**: Calculate the…"
- `ch10-b047` [exercise_block] — placed in **excluded**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Practical applications > Exercise 10.10: Use algebraic expressions to show the distributive law in practice
  - evidence quote: "### Exercise 10.10: Use algebraic expressions to show the distributive law in practice"
- `ch10-b047-i01` [exercise_item] — placed in **AO:use-of-brackets-ao-simplify-expressions (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Practical applications > Exercise 10.10: Use algebraic expressions to show the distributive law in practice
  - evidence quote: "### Exercise 10.10: Use algebraic expressions to show the distributive law in practice  1. Write down two different expressions for the total area of the two rectangles shown below. Draw sketches to show your working, a…"
- `ch10-b047-i02` [exercise_item] — placed in **AO:use-of-brackets-ao-simplify-expressions (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Practical applications > Exercise 10.10: Use algebraic expressions to show the distributive law in practice
  - evidence quote: "### Exercise 10.10: Use algebraic expressions to show the distributive law in practice  2. Write down the total area of the rectangles given below in two different ways."
- `ch10-b050` [summary] — placed in **excluded**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Summary
  - evidence quote: "- An algebraic expression is a mathematical statement that contains a combination of numbers, symbols, variables and mathematical operators. It does not have an equals sign. - A term can be a single number (positive or…"

### Row-level review categories and manually authored reasons
- **ao_no_evidence**: insert-brackets AO has no record_links; the linked chapter 10 records cover removing brackets and simplifying, not inserting brackets into existing expressions.
- **no_reused_assessment**: remove-brackets and simplify-expressions AOs have direct evidence but no reused exercise_item assessment.
- **curriculum_textbook_mismatch**: The curriculum AO 'Insert brackets in expressions' is not addressed in the linked textbook section.

### Per-atomic-objective evidence classification
- `use-of-brackets-ao-insert-brackets` → evidence: **none** · categories: ao_no_evidence, curriculum_textbook_mismatch
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `use-of-brackets-ao-remove-brackets` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch10-b030(worked_example), ch10-b031-i01(exercise), ch10-b031-i02(exercise), ch10-b031-i03(exercise), ch10-b031-i04(exercise), ch10-b031-i05(exercise), ch10-b032(instruction), ch10-b033(worked_example), ch10-b034-i01(exercise), ch10-b034-i02(exercise), ch10-b034-i03(exercise), ch10-b034-i04(exercise), ch10-b034-i05(exercise), ch10-b035(instruction), ch10-b036(instruction), ch10-b037(foundation), ch10-b038(worked_example), ch10-b039(worked_example), ch10-b040(instruction), ch10-b041-i01(exercise), ch10-b041-i02(exercise), ch10-b041-i03(exercise), ch10-b041-i04(exercise), ch10-b041-i05(exercise)
  - assessment: _(none anchored)_
- `use-of-brackets-ao-simplify-expressions` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch10-b042(instruction), ch10-b043(worked_example), ch10-b044(worked_example), ch10-b045-i01(exercise), ch10-b045-i02(exercise), ch10-b045-i03(exercise), ch10-b045-i04(exercise), ch10-b045-i05(exercise), ch10-b045-i06(exercise), ch10-b045-i07(exercise), ch10-b045-i08(exercise), ch10-b045-i09(exercise), ch10-b045-i10(exercise), ch10-b046(instruction), ch10-b047-i01(exercise), ch10-b047-i02(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning`

**Title:** Quantitative reasoning  
**Status:** `mapped`  
**Row review categories:** _(none — mapped or no-records baseline)_

### Curriculum objectives (source)
- `jss1-math-simplification-of-algebraic-expressions-quantitative-reasoning-po01`: Solve quantitative aptitude problems on the use of brackets

### Atomic objectives
- `simplification-of-algebraic-expressions-quantitative-reasoning-ao-solve-problems` [solve/apply]: Solve quantitative aptitude problems on the use of brackets.

### Linked textbook records (17 total) — inspected
- `ch10-b046` [exposition] — placed in **AO:simplification-of-algebraic-expressions-quantitative-reasoning-ao-solve-problems (instruction)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Practical applications > Using area to show the distributive law in practice
  - evidence quote: "We can use areas to show the distributive law in practice. For example, look at the two rectangles shown below. There are two ways in which we can write the total area of the two rectangles.  **Method 1**: Calculate the…"
- `ch10-b047` [exercise_block] — placed in **excluded**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Practical applications > Exercise 10.10: Use algebraic expressions to show the distributive law in practice
  - evidence quote: "### Exercise 10.10: Use algebraic expressions to show the distributive law in practice"
- `ch10-b047-i01` [exercise_item] — placed in **AO:simplification-of-algebraic-expressions-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Practical applications > Exercise 10.10: Use algebraic expressions to show the distributive law in practice
  - evidence quote: "### Exercise 10.10: Use algebraic expressions to show the distributive law in practice  1. Write down two different expressions for the total area of the two rectangles shown below. Draw sketches to show your working, a…"
- `ch10-b047-i02` [exercise_item] — placed in **AO:simplification-of-algebraic-expressions-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Practical applications > Exercise 10.10: Use algebraic expressions to show the distributive law in practice
  - evidence quote: "### Exercise 10.10: Use algebraic expressions to show the distributive law in practice  2. Write down the total area of the rectangles given below in two different ways."
- `ch10-b048` [exposition] — placed in **AO:simplification-of-algebraic-expressions-quantitative-reasoning-ao-solve-problems (instruction)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Practical applications > Using algebraic expressions to solve everyday problems
  - evidence quote: "Algebraic expressions can be very useful when you need to solve everyday problems. It allows us to use variables as representations of numbers where the value may vary.  Suppose you get ₦500 pocket money every month and…"
- `ch10-b049` [exercise_block] — placed in **excluded**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Practical applications > Exercise 10.11: Use algebraic expressions for practical problems
  - evidence quote: "### Exercise 10.11: Use algebraic expressions for practical problems"
- `ch10-b049-i01` [exercise_item] — placed in **AO:simplification-of-algebraic-expressions-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Practical applications > Exercise 10.11: Use algebraic expressions for practical problems
  - evidence quote: "### Exercise 10.11: Use algebraic expressions for practical problems  1. A father is $x$ years old. His daughter is currently half his age. How old will his daughter be in 10 years' time?"
- `ch10-b049-i02` [exercise_item] — placed in **AO:simplification-of-algebraic-expressions-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Practical applications > Exercise 10.11: Use algebraic expressions for practical problems
  - evidence quote: "### Exercise 10.11: Use algebraic expressions for practical problems  2. A long-distance athlete covers an average distance of $x\text{ metres}$ per minute. How far does she run in $y\text{ hours}$?"
- `ch10-b049-i03` [exercise_item] — placed in **AO:simplification-of-algebraic-expressions-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Practical applications > Exercise 10.11: Use algebraic expressions for practical problems
  - evidence quote: "### Exercise 10.11: Use algebraic expressions for practical problems  3. A shop owner sells maize at $₦\,x$ per cup. She also sells rice per cup, at double the price of the maize. If she sold 50 cups of maize and 45 cup…"
- `ch10-b049-i04` [exercise_item] — placed in **AO:simplification-of-algebraic-expressions-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Practical applications > Exercise 10.11: Use algebraic expressions for practical problems
  - evidence quote: "### Exercise 10.11: Use algebraic expressions for practical problems  4. A small sachet of milk costs $₦\,x$ and a small sachet of noodles costs $₦\,20$ more. Work out the cost of 4 sachets of milk and 8 sachets of nood…"
- `ch10-b049-i05` [exercise_item] — placed in **AO:simplification-of-algebraic-expressions-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Practical applications > Exercise 10.11: Use algebraic expressions for practical problems
  - evidence quote: "### Exercise 10.11: Use algebraic expressions for practical problems  5. The length of a rectangle is 3Â cm more than its breadth. Calculate the perimeter of the rectangle."
- `ch10-b049-i06` [exercise_item] — placed in **AO:simplification-of-algebraic-expressions-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Practical applications > Exercise 10.11: Use algebraic expressions for practical problems
  - evidence quote: "### Exercise 10.11: Use algebraic expressions for practical problems  6. The sum of three consecutive numbers is $y$. If the first of the three numbers is $a$, determine $y$."
- `ch10-b049-i07` [exercise_item] — placed in **AO:simplification-of-algebraic-expressions-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Practical applications > Exercise 10.11: Use algebraic expressions for practical problems
  - evidence quote: "### Exercise 10.11: Use algebraic expressions for practical problems  7. In a Mathematics test, Safiyah scored $p$ marks. Nkechi scored 7 marks more than Safiyah. Fadekemi scored 4 marks less than Nkechi. Work out the t…"
- `ch10-b049-i08` [exercise_item] — placed in **AO:simplification-of-algebraic-expressions-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Practical applications > Exercise 10.11: Use algebraic expressions for practical problems
  - evidence quote: "### Exercise 10.11: Use algebraic expressions for practical problems  8. Abodunrin has $₦\,n$ and Ikenna has $₦\,20$ more. Abodunrin spends 500 kobo and Ikenna spends 750 kobo. Calculate how many kobos they have left al…"
- `ch10-b049-i09` [exercise_item] — placed in **AO:simplification-of-algebraic-expressions-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Practical applications > Exercise 10.11: Use algebraic expressions for practical problems
  - evidence quote: "### Exercise 10.11: Use algebraic expressions for practical problems  9. A pencil costs $₦\,x$. A ruler costs $₦\,10$ less than a pencil. A pen costs $₦\,5$ more than a ruler. The price of a small exercise book is twice…"
- `ch10-b049-i10` [exercise_item] — placed in **AO:simplification-of-algebraic-expressions-quantitative-reasoning-ao-solve-problems (exercise)**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Practical applications > Exercise 10.11: Use algebraic expressions for practical problems
  - evidence quote: "### Exercise 10.11: Use algebraic expressions for practical problems  10. Rectangle 1 has a breadth of $2x\text{ cm}$ and a length of $y\text{ cm}$. Rectangle 2 has a breadth half as long as the breadth of Rectangle 1.…"
- `ch10-b050` [summary] — placed in **excluded**
  - heading: Chapter 10: Simplifying algebraic expressions > 10.6 Summary
  - evidence quote: "- An algebraic expression is a mathematical statement that contains a combination of numbers, symbols, variables and mathematical operators. It does not have an equals sign. - A term can be a single number (positive or…"

### Row-level review categories and manually authored reasons
_None — all AOs have direct evidence and a reused assessment._

### Per-atomic-objective evidence classification
- `simplification-of-algebraic-expressions-quantitative-reasoning-ao-solve-problems` → evidence: **direct** · categories: —
  - linked records: ch10-b046(instruction), ch10-b047-i01(exercise), ch10-b047-i02(exercise), ch10-b048(instruction), ch10-b049-i01(exercise), ch10-b049-i02(exercise), ch10-b049-i03(exercise), ch10-b049-i04(exercise), ch10-b049-i05(exercise), ch10-b049-i06(exercise), ch10-b049-i07(exercise), ch10-b049-i08(exercise), ch10-b049-i09(exercise), ch10-b049-i10(exercise)
  - assessment: reused from `ch10-b049-i01`

---

## `jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa`

**Title:** Translation of word problems into equations and vice-versa  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, ao_no_evidence, no_reused_assessment, curriculum_textbook_mismatch, prerequisite_only_evidence

### Curriculum objectives (source)
- `jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa-po01`: Translate word sentences into mathematical equations
- `jss1-math-simple-equations-translation-of-word-problems-into-equations-and-vice-versa-po02`: Use mathematical equations to represent word sentences

### Atomic objectives
- `translation-of-word-problems-into-equations-ao-translate-word-sentences` [translate/apply]: Translate word sentences into mathematical equations.
- `translation-of-word-problems-into-equations-ao-use-equations-to-represent` [use/apply]: Use mathematical equations to represent word sentences.

### Linked textbook records (44 total) — inspected
- `ch11-b001` [exposition] — placed in **shared_foundation**
  - heading: Chapter 11: Simple equations
  - evidence quote: "You have learnt that an algebraic *expression* is a mathematical phrase or statement. Algebraic expressions do not have equals signs. In this chapter we will be dealing with algebraic *equations*. Algebraic equations ar…"
- `ch11-b002` [exposition] — placed in **shared_foundation**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations
  - evidence quote: "An **algebraic equation** is a mathematical sentence that contains a combination of numbers, symbols, variables and mathematical operators. It always has an equals sign."
- `ch11-b003` [definition] — placed in **shared_foundation**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations
  - evidence quote: "**algebraic equation** An algebraic equation is a mathematical sentence that contains a combination of numbers, symbols, variables and mathematical operators. It always has an equals sign."
- `ch11-b004` [exposition] — placed in **shared_foundation**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > The difference between expressions and equations
  - evidence quote: "It is important that you understand the difference between algebraic expressions and algebraic equations. The table below lists the main differences.  - An expression is a phrase. An equation is a sentence. - We simplif…"
- `ch11-b005` [exposition] — placed in **shared_foundation**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Translate word sentences into algebraic equations
  - evidence quote: "In Section 9.3 of Chapter 9 and Section 10.6 of Chapter 10 you were given some examples of ways to write word phrases as mathematical statements. Revise those sections before you go on."
- `ch11-b006` [worked_example] — placed in **AO:translation-of-word-problems-into-equations-ao-translate-word-sentences (worked_example)**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Worked example 11.1: Translating simple word sentences into algebraic equations
  - evidence quote: "If a number is multiplied by 4, the answer is 6 more than the number. Write an equation to represent this."
- `ch11-b007` [worked_example] — placed in **AO:translation-of-word-problems-into-equations-ao-translate-word-sentences (worked_example)**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Worked example 11.2: Translating more complex word sentences into algebraic equations
  - evidence quote: "A mother is twice as old as her daughter. In two years' time, their combined ages will be 52 years. Write an equation to represent this."
- `ch11-b008` [exercise_block] — placed in **excluded**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Exercise 11.1: Translate word sentences into equations
  - evidence quote: "### Exercise 11.1: Translate word sentences into equations  Write an algebraic equation for each of the following situations."
- `ch11-b008-i01` [exercise_item] — placed in **AO:translation-of-word-problems-into-equations-ao-translate-word-sentences (exercise)**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Exercise 11.1: Translate word sentences into equations
  - evidence quote: "### Exercise 11.1: Translate word sentences into equations  Write an algebraic equation for each of the following situations.  1. If we add 23 to a number, the answer is 42."
- `ch11-b008-i02` [exercise_item] — placed in **AO:translation-of-word-problems-into-equations-ao-translate-word-sentences (exercise)**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Exercise 11.1: Translate word sentences into equations
  - evidence quote: "### Exercise 11.1: Translate word sentences into equations  Write an algebraic equation for each of the following situations.  2. The difference between 75 and a number is 20."
- `ch11-b008-i03` [exercise_item] — placed in **AO:translation-of-word-problems-into-equations-ao-translate-word-sentences (exercise)**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Exercise 11.1: Translate word sentences into equations
  - evidence quote: "### Exercise 11.1: Translate word sentences into equations  Write an algebraic equation for each of the following situations.  3. A pen costs twice as much as a ruler. The cost of 5 pens and 7 rulers is $₦\,102$."
- `ch11-b008-i04` [exercise_item] — placed in **AO:translation-of-word-problems-into-equations-ao-translate-word-sentences (exercise)**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Exercise 11.1: Translate word sentences into equations
  - evidence quote: "### Exercise 11.1: Translate word sentences into equations  Write an algebraic equation for each of the following situations.  4. If we add 9 to half of a number, the answer is twice the number."
- `ch11-b008-i05` [exercise_item] — placed in **AO:translation-of-word-problems-into-equations-ao-translate-word-sentences (exercise)**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Exercise 11.1: Translate word sentences into equations
  - evidence quote: "### Exercise 11.1: Translate word sentences into equations  Write an algebraic equation for each of the following situations.  5. The sum of three consecutive numbers is 24."
- `ch11-b008-i06` [exercise_item] — placed in **AO:translation-of-word-problems-into-equations-ao-translate-word-sentences (exercise)**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Exercise 11.1: Translate word sentences into equations
  - evidence quote: "### Exercise 11.1: Translate word sentences into equations  Write an algebraic equation for each of the following situations.  6. The length of a rectangle with a perimeter of 40 cm is three times more than its breadth."
- `ch11-b008-i07` [exercise_item] — placed in **AO:translation-of-word-problems-into-equations-ao-translate-word-sentences (exercise)**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Exercise 11.1: Translate word sentences into equations
  - evidence quote: "### Exercise 11.1: Translate word sentences into equations  Write an algebraic equation for each of the following situations.  7. The combined area of two rectangles is 49 square units. The area of one rectangle is six…"
- `ch11-b008-i08` [exercise_item] — placed in **AO:translation-of-word-problems-into-equations-ao-translate-word-sentences (exercise)**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Exercise 11.1: Translate word sentences into equations
  - evidence quote: "### Exercise 11.1: Translate word sentences into equations  Write an algebraic equation for each of the following situations.  8. If the sum of a number and 6 is divided by 10, the answer is 24."
- `ch11-b008-i09` [exercise_item] — placed in **AO:translation-of-word-problems-into-equations-ao-translate-word-sentences (exercise)**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Exercise 11.1: Translate word sentences into equations
  - evidence quote: "### Exercise 11.1: Translate word sentences into equations  Write an algebraic equation for each of the following situations.  9. Danjuma has $₦\,500$. He spends a certain amount on snacks and exactly the same amount on…"
- `ch11-b008-i10` [exercise_item] — placed in **AO:translation-of-word-problems-into-equations-ao-translate-word-sentences (exercise)**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Exercise 11.1: Translate word sentences into equations
  - evidence quote: "### Exercise 11.1: Translate word sentences into equations  Write an algebraic equation for each of the following situations.  10. Ngozi goes to school. She walks for a few minutes and then runs for 180 seconds. Then sh…"
- `ch11-b009` [exposition] — placed in **review_items**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Translate algebraic equations into word sentences
  - evidence quote: "We can also translate algebraic equations into word sentences. You can make up a story if you want to, or you can just think of the variable as a number."
- `ch11-b010` [worked_example] — placed in **review_items**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Worked example 11.3: Translating algebraic equations into word sentences
  - evidence quote: "Translate the following equation into a word sentence:  $$ 3+y=10-2y $$"
- `ch11-b011` [exercise_block] — placed in **excluded**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Exercise 11.2: Translate equations into word sentences
  - evidence quote: "### Exercise 11.2: Translate equations into word sentences  Write a word sentence for each of the following algebraic equations."
- `ch11-b011-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Exercise 11.2: Translate equations into word sentences
  - evidence quote: "### Exercise 11.2: Translate equations into word sentences  Write a word sentence for each of the following algebraic equations.  1. $$ x+12=25 $$"
- `ch11-b011-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Exercise 11.2: Translate equations into word sentences
  - evidence quote: "### Exercise 11.2: Translate equations into word sentences  Write a word sentence for each of the following algebraic equations.  2. $$ 2y-8=30 $$"
- `ch11-b011-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Exercise 11.2: Translate equations into word sentences
  - evidence quote: "### Exercise 11.2: Translate equations into word sentences  Write a word sentence for each of the following algebraic equations.  3. $$ \frac{2}{3}p=12 $$"
- `ch11-b011-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Exercise 11.2: Translate equations into word sentences
  - evidence quote: "### Exercise 11.2: Translate equations into word sentences  Write a word sentence for each of the following algebraic equations.  4. $$ 120-x-3x=60 $$"
- `ch11-b011-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Exercise 11.2: Translate equations into word sentences
  - evidence quote: "### Exercise 11.2: Translate equations into word sentences  Write a word sentence for each of the following algebraic equations.  5. $$ 2c+\frac{1}{2}c=10 $$"
- `ch11-b011-i06` [exercise_item] — placed in **review_items**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Exercise 11.2: Translate equations into word sentences
  - evidence quote: "### Exercise 11.2: Translate equations into word sentences  Write a word sentence for each of the following algebraic equations.  6. $$ 62=8z-\frac{1}{4}z $$"
- `ch11-b011-i07` [exercise_item] — placed in **review_items**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Exercise 11.2: Translate equations into word sentences
  - evidence quote: "### Exercise 11.2: Translate equations into word sentences  Write a word sentence for each of the following algebraic equations.  7. $$ 2p+5p=p-10 $$"
- `ch11-b011-i08` [exercise_item] — placed in **review_items**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Exercise 11.2: Translate equations into word sentences
  - evidence quote: "### Exercise 11.2: Translate equations into word sentences  Write a word sentence for each of the following algebraic equations.  8. $$ \frac{a-10}{4}=20 $$"
- `ch11-b011-i09` [exercise_item] — placed in **review_items**
  - heading: Chapter 11: Simple equations > 11.1 Formulating equations > Exercise 11.2: Translate equations into word sentences
  - evidence quote: "### Exercise 11.2: Translate equations into word sentences  Write a word sentence for each of the following algebraic equations.  9. $$ 2x+2(2x)=30 $$"
- `ch11-b025` [exposition] — placed in **review_items**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems
  - evidence quote: "Equations are very useful when you need to solve problems that are described in words. In Chapter 9, you learnt that these steps can be used to solve a problem that is described in words:  1. **Understand the problem:**…"
- `ch11-b026` [worked_example] — placed in **review_items**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems > Worked example 11.7: Solving a problem using an equation
  - evidence quote: "The length of a rectangle with a perimeter of 120 cm is 10 cm longer than its breadth. Determine the length and the breadth of the rectangle in centimetres."
- `ch11-b027` [exercise_block] — placed in **excluded**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems > Exercise 11.5: Use equations to solve problems
  - evidence quote: "### Exercise 11.5: Use equations to solve problems"
- `ch11-b027-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems > Exercise 11.5: Use equations to solve problems
  - evidence quote: "### Exercise 11.5: Use equations to solve problems  1. Erioluwa has $₦\,82$. This is $₦\,15$ more than Ifedolapo. How much money does Ifedolapo have?"
- `ch11-b027-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems > Exercise 11.5: Use equations to solve problems
  - evidence quote: "### Exercise 11.5: Use equations to solve problems  2. Halima saved a certain amount of money. After she did some holiday work, she could add $₦\,125$ to her savings. She now has $₦\,203$. How much money did she have sa…"
- `ch11-b027-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems > Exercise 11.5: Use equations to solve problems
  - evidence quote: "### Exercise 11.5: Use equations to solve problems  3. Oluchi walks 25% of a certain distance. If he walked 55 m, how far is the full distance?"
- `ch11-b027-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems > Exercise 11.5: Use equations to solve problems
  - evidence quote: "### Exercise 11.5: Use equations to solve problems  4. The sum of three consecutive numbers is 36. Determine the three numbers."
- `ch11-b027-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems > Exercise 11.5: Use equations to solve problems
  - evidence quote: "### Exercise 11.5: Use equations to solve problems  5. In a JSS1 class of 48 students, there are twice as many boys as girls. Determine how many boys and how many girls are in the class."
- `ch11-b027-i06` [exercise_item] — placed in **review_items**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems > Exercise 11.5: Use equations to solve problems
  - evidence quote: "### Exercise 11.5: Use equations to solve problems  6. A mother is three times older than her son. Their combined age is 84 years. Determine the ages of the mother and her son."
- `ch11-b027-i07` [exercise_item] — placed in **review_items**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems > Exercise 11.5: Use equations to solve problems
  - evidence quote: "### Exercise 11.5: Use equations to solve problems  7. The difference between four times a number and the number plus 5 is 10. Determine the number."
- `ch11-b027-i08` [exercise_item] — placed in **review_items**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems > Exercise 11.5: Use equations to solve problems
  - evidence quote: "### Exercise 11.5: Use equations to solve problems  8. A pen costs $₦\,4$ more than a ruler. The price for 3 pens and 8 rulers altogether is $₦\,142$. Determine the price of a pen and the price of a ruler."
- `ch11-b027-i09` [exercise_item] — placed in **review_items**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems > Exercise 11.5: Use equations to solve problems
  - evidence quote: "### Exercise 11.5: Use equations to solve problems  9. You must cut 68 cm of rope into three pieces. The second piece must have double the length of the first piece. The third piece must be 8 cm longer than the second p…"
- `ch11-b027-i10` [exercise_item] — placed in **review_items**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems > Exercise 11.5: Use equations to solve problems
  - evidence quote: "### Exercise 11.5: Use equations to solve problems  10. Lami has twice as much money as Chinweike. Latifah has three times the amount of money that Chinweike has. Chinweike's money plus $₦\,24$ is equal to the amount of…"
- `ch11-b028` [summary] — placed in **excluded**
  - heading: Chapter 11: Simple equations > 11.4 Summary
  - evidence quote: "- An algebraic equation is a mathematical sentence that contains a combination of numbers, symbols, variables and mathematical operators. It always has an equals sign. - The main differences between algebraic expression…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: 23 records belong to other subtopics: equation-to-word translation (ch11-b009, b010, b011-i01..i09 - reverse direction) and solving with equations (ch11-b025, b026, b027-i01..i10 - belongs to solution-of-simple-equations subtopic).
- **ao_no_evidence**: use-equations-to-represent AO has zero record_links because the textbook teaches a single word-to-equation skill (ch11-b005 onwards) that satisfies both translate and use-to-represent AOs; all word-to-equation records were placed on the translate AO.
- **no_reused_assessment**: translate-word-sentences AO has direct exercises (ch11-b008-i01..i10) but no reused exercise_item assessment was selected.
- **curriculum_textbook_mismatch**: The curriculum splits a single skill into two AOs (po01 'Translate word sentences into mathematical equations' and po02 'Use mathematical equations to represent word sentences'). The textbook in ch11-b005 onwards teaches one activity that satisfies both, so the AO2 distinction is not reflected in the corpus.
- **prerequisite_only_evidence**: The use-equations-to-represent AO is only supported by shared_foundation records (ch11-b001..b005 introducing equations and the translation activity) — that grounding is prerequisite, not direct AO-specific evidence.

### Per-atomic-objective evidence classification
- `translation-of-word-problems-into-equations-ao-translate-word-sentences` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch11-b006(worked_example), ch11-b007(worked_example), ch11-b008-i01(exercise), ch11-b008-i02(exercise), ch11-b008-i03(exercise), ch11-b008-i04(exercise), ch11-b008-i05(exercise), ch11-b008-i06(exercise), ch11-b008-i07(exercise), ch11-b008-i08(exercise), ch11-b008-i09(exercise), ch11-b008-i10(exercise)
  - assessment: _(none anchored)_
- `translation-of-word-problems-into-equations-ao-use-equations-to-represent` → evidence: **prerequisite_only** · categories: ao_no_evidence, curriculum_textbook_mismatch, prerequisite_only_evidence
  - linked records: _(none)_
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All review_items were inspected. Candidate proposals were added for equation-to-word translation and for solving word problems with equations. The existing AOs cover word-to-equation representation only.

### Candidate atomic objective proposals
- `translation-word-problems-candidate-ao-translate-equations-to-word-sentences` [curriculum_textbook_mismatch; candidate_for_expert_review]
  - proposed objective: Translate algebraic equations into word sentences.
  - source records: ch11-b009, ch11-b010, ch11-b011-i01, ch11-b011-i02, ch11-b011-i03, ch11-b011-i04, ch11-b011-i05, ch11-b011-i06, ch11-b011-i07, ch11-b011-i08, ch11-b011-i09
  - closest existing AOs: translation-of-word-problems-into-equations-ao-translate-word-sentences, translation-of-word-problems-into-equations-ao-use-equations-to-represent
  - candidate evidence quote: "Translate the following equation into a word sentence:"
  - rationale: The records teach the reverse direction from equations back to words, which is not represented by the current word-to-equation AOs.
- `translation-word-problems-candidate-ao-use-equations-to-solve-word-problems` [extension_or_enrichment; candidate_for_expert_review]
  - proposed objective: Use equations to solve word problems.
  - source records: ch11-b025, ch11-b026, ch11-b027-i01, ch11-b027-i02, ch11-b027-i03, ch11-b027-i04, ch11-b027-i05, ch11-b027-i06, ch11-b027-i07, ch11-b027-i08, ch11-b027-i09, ch11-b027-i10
  - closest existing AOs: translation-of-word-problems-into-equations-ao-translate-word-sentences, translation-of-word-problems-into-equations-ao-use-equations-to-represent
  - candidate evidence quote: "Equations are very useful when you need to solve problems that are described in words."
  - rationale: These records require forming and solving equations in context, not only translating or representing the sentence.

---

## `jss1-math-simple-equations-solution-of-simple-equations`

**Title:** Solution of simple equations  
**Status:** `needs_review`  
**Row review categories:** no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-simple-equations-solution-of-simple-equations-po01`: Solve simple equations and cross-check the answers

### Atomic objectives
- `solution-of-simple-equations-ao-solve-simple-equations` [solve/apply]: Solve simple equations.
- `solution-of-simple-equations-ao-cross-check-answers` [cross-check/apply]: Cross-check the answers to simple equations.

### Linked textbook records (43 total) — inspected
- `ch11-b001` [exposition] — placed in **shared_foundation**
  - heading: Chapter 11: Simple equations
  - evidence quote: "You have learnt that an algebraic *expression* is a mathematical phrase or statement. Algebraic expressions do not have equals signs. In this chapter we will be dealing with algebraic *equations*. Algebraic equations ar…"
- `ch11-b012` [exposition] — placed in **shared_foundation**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > The solution of an equation
  - evidence quote: "You have learnt how to find the values that make open sentences true. Look at the following algebraic equation:  $$ 3+x=5 $$  It is easy to see that the only value for $x$ that will make this equation true is 2. This is…"
- `ch11-b013` [definition] — placed in **shared_foundation**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > The solution of an equation
  - evidence quote: "**solution** The solution of an equation is the value of the variable that makes the equation true.  **solve** When we solve an equation, we find the value of the variable that makes the equation true."
- `ch11-b014` [exposition] — placed in **shared_foundation**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > The solution of an equation
  - evidence quote: "To solve an equation, we must isolate the variable. If $x$ is the variable, we must get the equation in the form:  $$ x=\text{value} $$"
- `ch11-b015` [exposition] — placed in **shared_foundation**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Representing an equation as a balancing scale
  - evidence quote: "To help us solve an algebraic equation, we can show it as a balancing scale. The picture shows what a scale looks like. This scale is balanced, because nothing has been placed on it.  If we place a mass piece on one of…"
- `ch11-b016` [hint] — placed in **excluded**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Representing an equation as a balancing scale
  - evidence quote: "Go back to Chapter 9 if you need to revise inverse operations. Remember that addition and subtraction are inverse operations, and multiplication and division are inverse operations."
- `ch11-b017` [exposition] — placed in **shared_foundation**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Representing an equation as a balancing scale
  - evidence quote: "Whatever we add to the one pan, we must also add to the other pan. The scale now shows:  Remember that $-5+5=0$. Therefore, if we simplify both sides, we get the solution of the equation:  $$ x=19 $$"
- `ch11-b018` [worked_example] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (worked_example)**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Worked example 11.4: Finding the solution of an equation
  - evidence quote: "Solve the following equation:  $$ 2x+x-10=2 $$"
- `ch11-b019` [exposition] — placed in **AO:solution-of-simple-equations-ao-cross-check-answers (instruction)**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Checking the solution
  - evidence quote: "We always check the solution we worked out to make sure that it makes the equation true. An equation is true if the left-hand side is equal to (has the same value as) the right-hand side."
- `ch11-b020` [worked_example] — placed in **AO:solution-of-simple-equations-ao-cross-check-answers (worked_example)**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Worked example 11.5: Checking the solution
  - evidence quote: "In the previous worked example, the solution of the equation:  $$ 2x+x-10=2 $$  was found to be:  $$ x=4 $$  Check this solution."
- `ch11-b021` [exercise_block] — placed in **excluded**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Exercise 11.3: Solve equations and check the solutions
  - evidence quote: "### Exercise 11.3: Solve equations and check the solutions  Solve each of the following equations and check the solutions."
- `ch11-b021-i01` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Exercise 11.3: Solve equations and check the solutions
  - evidence quote: "### Exercise 11.3: Solve equations and check the solutions  Solve each of the following equations and check the solutions.  1. $$ 11x=33 $$"
- `ch11-b021-i02` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Exercise 11.3: Solve equations and check the solutions
  - evidence quote: "### Exercise 11.3: Solve equations and check the solutions  Solve each of the following equations and check the solutions.  2. $$ 18+p=6 $$"
- `ch11-b021-i03` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Exercise 11.3: Solve equations and check the solutions
  - evidence quote: "### Exercise 11.3: Solve equations and check the solutions  Solve each of the following equations and check the solutions.  3. $$ \frac{1}{4}y=5 $$"
- `ch11-b021-i04` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Exercise 11.3: Solve equations and check the solutions
  - evidence quote: "### Exercise 11.3: Solve equations and check the solutions  Solve each of the following equations and check the solutions.  4. $$ 4x+5=17 $$"
- `ch11-b021-i05` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Exercise 11.3: Solve equations and check the solutions
  - evidence quote: "### Exercise 11.3: Solve equations and check the solutions  Solve each of the following equations and check the solutions.  5. $$ 10+5a=40 $$"
- `ch11-b021-i06` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Exercise 11.3: Solve equations and check the solutions
  - evidence quote: "### Exercise 11.3: Solve equations and check the solutions  Solve each of the following equations and check the solutions.  6. $$ 13=2x-3 $$"
- `ch11-b021-i07` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Exercise 11.3: Solve equations and check the solutions
  - evidence quote: "### Exercise 11.3: Solve equations and check the solutions  Solve each of the following equations and check the solutions.  7. $$ \frac{1}{2}t+1=5 $$"
- `ch11-b021-i08` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Exercise 11.3: Solve equations and check the solutions
  - evidence quote: "### Exercise 11.3: Solve equations and check the solutions  Solve each of the following equations and check the solutions.  8. $$ 36+\frac{3}{4}y=44 $$"
- `ch11-b021-i09` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Exercise 11.3: Solve equations and check the solutions
  - evidence quote: "### Exercise 11.3: Solve equations and check the solutions  Solve each of the following equations and check the solutions.  9. $$ 1-2x+11x=19 $$"
- `ch11-b021-i10` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Exercise 11.3: Solve equations and check the solutions
  - evidence quote: "### Exercise 11.3: Solve equations and check the solutions  Solve each of the following equations and check the solutions.  10. $$ 39=21+5q-4q+2q $$"
- `ch11-b022` [exposition] — placed in **shared_foundation**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Equations with variables on both sides of the equals sign
  - evidence quote: "Consider the following equation:  $$ 18-5x=4x $$  To solve an equation, we must isolate the variable. We must get the equation in the form:  $$ x=\text{value} $$  In all the equations we have solved so far, the terms wi…"
- `ch11-b023` [worked_example] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (worked_example)**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Worked example 11.6: Solving an equation with variables on both sides
  - evidence quote: "Solve the following equation:  $$ 18-5x=4x $$"
- `ch11-b024` [exercise_block] — placed in **excluded**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Exercise 11.4: Solve equations with variables on both sides
  - evidence quote: "### Exercise 11.4: Solve equations with variables on both sides  Solve each of the following equations and check the solutions."
- `ch11-b024-i01` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Exercise 11.4: Solve equations with variables on both sides
  - evidence quote: "### Exercise 11.4: Solve equations with variables on both sides  Solve each of the following equations and check the solutions.  1. $$ 2x+9=5x $$"
- `ch11-b024-i02` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Exercise 11.4: Solve equations with variables on both sides
  - evidence quote: "### Exercise 11.4: Solve equations with variables on both sides  Solve each of the following equations and check the solutions.  2. $$ 8+4p=6p-12 $$"
- `ch11-b024-i03` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Exercise 11.4: Solve equations with variables on both sides
  - evidence quote: "### Exercise 11.4: Solve equations with variables on both sides  Solve each of the following equations and check the solutions.  3. $$ 5a+7+a=4a+13 $$"
- `ch11-b024-i04` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Exercise 11.4: Solve equations with variables on both sides
  - evidence quote: "### Exercise 11.4: Solve equations with variables on both sides  Solve each of the following equations and check the solutions.  4. $$ 6-3y=-2-2y $$"
- `ch11-b024-i05` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.2 Solving equations > Exercise 11.4: Solve equations with variables on both sides
  - evidence quote: "### Exercise 11.4: Solve equations with variables on both sides  Solve each of the following equations and check the solutions.  5. $$ 10-6t+5=5t-30+t+3t $$"
- `ch11-b025` [exposition] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (instruction)**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems
  - evidence quote: "Equations are very useful when you need to solve problems that are described in words. In Chapter 9, you learnt that these steps can be used to solve a problem that is described in words:  1. **Understand the problem:**…"
- `ch11-b026` [worked_example] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (worked_example)**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems > Worked example 11.7: Solving a problem using an equation
  - evidence quote: "The length of a rectangle with a perimeter of 120 cm is 10 cm longer than its breadth. Determine the length and the breadth of the rectangle in centimetres."
- `ch11-b027` [exercise_block] — placed in **excluded**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems > Exercise 11.5: Use equations to solve problems
  - evidence quote: "### Exercise 11.5: Use equations to solve problems"
- `ch11-b027-i01` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems > Exercise 11.5: Use equations to solve problems
  - evidence quote: "### Exercise 11.5: Use equations to solve problems  1. Erioluwa has $₦\,82$. This is $₦\,15$ more than Ifedolapo. How much money does Ifedolapo have?"
- `ch11-b027-i02` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems > Exercise 11.5: Use equations to solve problems
  - evidence quote: "### Exercise 11.5: Use equations to solve problems  2. Halima saved a certain amount of money. After she did some holiday work, she could add $₦\,125$ to her savings. She now has $₦\,203$. How much money did she have sa…"
- `ch11-b027-i03` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems > Exercise 11.5: Use equations to solve problems
  - evidence quote: "### Exercise 11.5: Use equations to solve problems  3. Oluchi walks 25% of a certain distance. If he walked 55 m, how far is the full distance?"
- `ch11-b027-i04` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems > Exercise 11.5: Use equations to solve problems
  - evidence quote: "### Exercise 11.5: Use equations to solve problems  4. The sum of three consecutive numbers is 36. Determine the three numbers."
- `ch11-b027-i05` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems > Exercise 11.5: Use equations to solve problems
  - evidence quote: "### Exercise 11.5: Use equations to solve problems  5. In a JSS1 class of 48 students, there are twice as many boys as girls. Determine how many boys and how many girls are in the class."
- `ch11-b027-i06` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems > Exercise 11.5: Use equations to solve problems
  - evidence quote: "### Exercise 11.5: Use equations to solve problems  6. A mother is three times older than her son. Their combined age is 84 years. Determine the ages of the mother and her son."
- `ch11-b027-i07` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems > Exercise 11.5: Use equations to solve problems
  - evidence quote: "### Exercise 11.5: Use equations to solve problems  7. The difference between four times a number and the number plus 5 is 10. Determine the number."
- `ch11-b027-i08` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems > Exercise 11.5: Use equations to solve problems
  - evidence quote: "### Exercise 11.5: Use equations to solve problems  8. A pen costs $₦\,4$ more than a ruler. The price for 3 pens and 8 rulers altogether is $₦\,142$. Determine the price of a pen and the price of a ruler."
- `ch11-b027-i09` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems > Exercise 11.5: Use equations to solve problems
  - evidence quote: "### Exercise 11.5: Use equations to solve problems  9. You must cut 68 cm of rope into three pieces. The second piece must have double the length of the first piece. The third piece must be 8 cm longer than the second p…"
- `ch11-b027-i10` [exercise_item] — placed in **AO:solution-of-simple-equations-ao-solve-simple-equations (exercise)**
  - heading: Chapter 11: Simple equations > 11.3 Using equations to solve problems > Exercise 11.5: Use equations to solve problems
  - evidence quote: "### Exercise 11.5: Use equations to solve problems  10. Lami has twice as much money as Chinweike. Latifah has three times the amount of money that Chinweike has. Chinweike's money plus $₦\,24$ is equal to the amount of…"
- `ch11-b028` [summary] — placed in **excluded**
  - heading: Chapter 11: Simple equations > 11.4 Summary
  - evidence quote: "- An algebraic equation is a mathematical sentence that contains a combination of numbers, symbols, variables and mathematical operators. It always has an equals sign. - The main differences between algebraic expression…"

### Row-level review categories and manually authored reasons
- **no_reused_assessment**: solve-simple-equations AO has many direct exercises but no reused assessment. cross-check-answers AO has only an instructional exposition (ch11-b019) and a worked example (ch11-b020); no exercise_item exclusively tests cross-checking, so no reused assessment is possible for that AO.

### Per-atomic-objective evidence classification
- `solution-of-simple-equations-ao-solve-simple-equations` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch11-b018(worked_example), ch11-b021-i01(exercise), ch11-b021-i02(exercise), ch11-b021-i03(exercise), ch11-b021-i04(exercise), ch11-b021-i05(exercise), ch11-b021-i06(exercise), ch11-b021-i07(exercise), ch11-b021-i08(exercise), ch11-b021-i09(exercise), ch11-b021-i10(exercise), ch11-b023(worked_example), ch11-b024-i01(exercise), ch11-b024-i02(exercise), ch11-b024-i03(exercise), ch11-b024-i04(exercise), ch11-b024-i05(exercise), ch11-b025(instruction), ch11-b026(worked_example), ch11-b027-i01(exercise), ch11-b027-i02(exercise), ch11-b027-i03(exercise), ch11-b027-i04(exercise), ch11-b027-i05(exercise), ch11-b027-i06(exercise), ch11-b027-i07(exercise), ch11-b027-i08(exercise), ch11-b027-i09(exercise), ch11-b027-i10(exercise)
  - assessment: _(none anchored)_
- `solution-of-simple-equations-ao-cross-check-answers` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch11-b019(instruction), ch11-b020(worked_example)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle`

**Title:** Similarities and differences between the following: Square, rectangle, triangle, trapezium, parallelogram and circle.  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, ao_no_evidence, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-plane-shapes-similarities-and-differences-between-the-following-square-rectangle-triangle-trapezium-parallelogram-and-circle-po01`: State the similarities and differences between the following: square, rectangle, triangle, trapezium, parallelogram and circle

### Atomic objectives
- `similarities-and-differences-between-plane-shapes-ao-state-similarities` [state/remember]: State the similarities between square, rectangle, triangle, trapezium, parallelogram and circle.
- `similarities-and-differences-between-plane-shapes-ao-state-differences` [state/remember]: State the differences between square, rectangle, triangle, trapezium, parallelogram and circle.

### Linked textbook records (23 total) — inspected
- `ch12-b001` [exposition] — placed in **shared_foundation**
  - heading: Chapter 12: Two-dimensional shapes > 12.1 Types and properties of shapes
  - evidence quote: "A two-dimensional (2D) shape has two dimensions that we can measure: we can measure the length and we can measure the breadth (sometimes called the width) of the shape. For example, a square is a 2D shape. All the sides…"
- `ch12-b002` [definition] — placed in **shared_foundation**
  - heading: Chapter 12: Two-dimensional shapes > 12.1 Types and properties of shapes
  - evidence quote: "**polygon** A polygon is a closed flat shape with three or more straight sides.  **quadrilateral** A quadrilateral is a polygon that has four sides and four angles."
- `ch12-b003` [exposition] — placed in **shared_foundation**
  - heading: Chapter 12: Two-dimensional shapes > 12.1 Types and properties of shapes > Properties of two-dimensional shapes
  - evidence quote: "The properties of these two-dimensional shapes are listed below.  **A. Square** - A square has four equal sides and four right angles. - The opposite sides of a square are parallel.  **B. Rectangle** - A rectangle has t…"
- `ch12-b004` [worked_example] — placed in **AO:similarities-and-differences-between-plane-shapes-ao-state-differences (worked_example)**
  - heading: Chapter 12: Two-dimensional shapes > 12.1 Types and properties of shapes > Worked example 12.1: Comparing two-dimensional shapes
  - evidence quote: "Look at the two shapes. State which shape is NOT a polygon, and identify and name the quadrilateral."
- `ch12-b005` [exercise_block] — placed in **excluded**
  - heading: Chapter 12: Two-dimensional shapes > 12.1 Types and properties of shapes > Exercise 12.1: Compare two-dimensional shapes
  - evidence quote: "### Exercise 12.1: Compare two-dimensional shapes"
- `ch12-b005-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 12: Two-dimensional shapes > 12.1 Types and properties of shapes > Exercise 12.1: Compare two-dimensional shapes
  - evidence quote: "### Exercise 12.1: Compare two-dimensional shapes  1. Compare a square and a rectangle. What is similar? What is different?"
- `ch12-b005-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 12: Two-dimensional shapes > 12.1 Types and properties of shapes > Exercise 12.1: Compare two-dimensional shapes
  - evidence quote: "### Exercise 12.1: Compare two-dimensional shapes  2. Compare a square and a rhombus. What is similar? What is different?"
- `ch12-b005-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 12: Two-dimensional shapes > 12.1 Types and properties of shapes > Exercise 12.1: Compare two-dimensional shapes
  - evidence quote: "### Exercise 12.1: Compare two-dimensional shapes  3. Compare a trapezium and a parallelogram. What is similar? What is different?"
- `ch12-b005-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 12: Two-dimensional shapes > 12.1 Types and properties of shapes > Exercise 12.1: Compare two-dimensional shapes
  - evidence quote: "### Exercise 12.1: Compare two-dimensional shapes  4. Compare a parallelogram and a rhombus. What is similar? What is different?"
- `ch12-b005-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 12: Two-dimensional shapes > 12.1 Types and properties of shapes > Exercise 12.1: Compare two-dimensional shapes
  - evidence quote: "### Exercise 12.1: Compare two-dimensional shapes  5. Compare a triangle and a square. What is similar? What is different?"
- `ch12-b006` [exposition] — placed in **review_items**
  - heading: Chapter 12: Two-dimensional shapes > 12.1 Types and properties of shapes > Parts and properties of a circle
  - evidence quote: "A circle is a 2D shape with a curved edge, so a circle is not a polygon. We use special names for the different parts of a circle.  - The perimeter of a circle (the length around the circle) is called its *circumference…"
- `ch12-b007` [worked_example] — placed in **review_items**
  - heading: Chapter 12: Two-dimensional shapes > 12.1 Types and properties of shapes > Worked example 12.2: Identifying parts of a circle
  - evidence quote: "In the diagram below, $O$ is the centre of the circle. $T$, $S$, and $V$ are labels for parts of the circle. Which of the labels identifies the circumference of the circle?"
- `ch12-b008` [exercise_block] — placed in **excluded**
  - heading: Chapter 12: Two-dimensional shapes > 12.1 Types and properties of shapes > Exercise 12.2: Identify parts of a circle
  - evidence quote: "### Exercise 12.2: Identify parts of a circle"
- `ch12-b008-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 12: Two-dimensional shapes > 12.1 Types and properties of shapes > Exercise 12.2: Identify parts of a circle
  - evidence quote: "### Exercise 12.2: Identify parts of a circle  1. In the diagram below, $O$ is the centre of the circle. $T$, $S$ and $V$ are labels for parts of the circle.  (a) Which of the labels identifies a diameter of the circle?"
- `ch12-b008-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 12: Two-dimensional shapes > 12.1 Types and properties of shapes > Exercise 12.2: Identify parts of a circle
  - evidence quote: "### Exercise 12.2: Identify parts of a circle  2. In the diagram below, $O$ is the centre of the circle. $T$, $S$ and $V$ are labels for parts of the circle.  (b) Which of the labels identifies a radius of the circle?"
- `ch12-b008-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 12: Two-dimensional shapes > 12.1 Types and properties of shapes > Exercise 12.2: Identify parts of a circle
  - evidence quote: "### Exercise 12.2: Identify parts of a circle  3. In the diagram below, $O$ is the centre of the circle. $T$, $S$ and $V$ are labels for parts of the circle.  (c) Which of the labels identifies the circumference of the…"
- `ch12-b008-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 12: Two-dimensional shapes > 12.1 Types and properties of shapes > Exercise 12.2: Identify parts of a circle
  - evidence quote: "### Exercise 12.2: Identify parts of a circle  4. A diagram of a circle is given. $O$ is the centre of the circle.  (a) Which part of the circle is labelled $T$?"
- `ch12-b008-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 12: Two-dimensional shapes > 12.1 Types and properties of shapes > Exercise 12.2: Identify parts of a circle
  - evidence quote: "### Exercise 12.2: Identify parts of a circle  5. A diagram of a circle is given. $O$ is the centre of the circle.  (b) Which part of the circle is labelled $S$?"
- `ch12-b008-i06` [exercise_item] — placed in **review_items**
  - heading: Chapter 12: Two-dimensional shapes > 12.1 Types and properties of shapes > Exercise 12.2: Identify parts of a circle
  - evidence quote: "### Exercise 12.2: Identify parts of a circle  6. A diagram of a circle is given. $O$ is the centre of the circle.  (c) Which part of the circle is labelled $V$?"
- `ch12-b008-i07` [exercise_item] — placed in **review_items**
  - heading: Chapter 12: Two-dimensional shapes > 12.1 Types and properties of shapes > Exercise 12.2: Identify parts of a circle
  - evidence quote: "### Exercise 12.2: Identify parts of a circle  7. Select a word from Column B that best fits the description in Column A.  a) A line segment that goes all the way across the circle and passes through the centre.  Column…"
- `ch12-b008-i08` [exercise_item] — placed in **review_items**
  - heading: Chapter 12: Two-dimensional shapes > 12.1 Types and properties of shapes > Exercise 12.2: Identify parts of a circle
  - evidence quote: "### Exercise 12.2: Identify parts of a circle  8. Select a word from Column B that best fits the description in Column A.  b) The perimeter of a circle (the length around the circle).  Column B: A: Circumference, B: Rad…"
- `ch12-b008-i09` [exercise_item] — placed in **review_items**
  - heading: Chapter 12: Two-dimensional shapes > 12.1 Types and properties of shapes > Exercise 12.2: Identify parts of a circle
  - evidence quote: "### Exercise 12.2: Identify parts of a circle  9. Select a word from Column B that best fits the description in Column A.  c) A line segment from the centre of the circle to a point on the circumference.  Column B: A: C…"
- `ch12-b072` [summary] — placed in **excluded**
  - heading: Chapter 12: Two-dimensional shapes > 12.5 Summary
  - evidence quote: "A two-dimensional (2D) shape has two dimensions that we can measure: length and breadth (or width).  A polygon is a closed flat shape with three or more straight sides. A triangle has three sides and three angles. A qua…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch12-b005-i01..i05 (compare 2D shapes) may target similarities or differences depending on the wording; ch12-b006, b007, b008-i01..i09 identify parts of a circle, which is outside the similarities/differences scope.
- **ao_no_evidence**: state-similarities AO has no record_links; the only direct comparison record (ch12-b004 worked example) asks which shape is NOT a particular shape — a differences task.
- **no_reused_assessment**: Neither AO has a reused exercise_item assessment.

### Per-atomic-objective evidence classification
- `similarities-and-differences-between-plane-shapes-ao-state-similarities` → evidence: **none** · categories: ao_no_evidence
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `similarities-and-differences-between-plane-shapes-ao-state-differences` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch12-b004(worked_example)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All review_items were inspected. Candidate proposal added for identifying parts of a circle. The compare-shapes items were not proposed because they are ambiguous instances of the existing similarities/differences AOs.

### Candidate atomic objective proposals
- `similarities-differences-plane-shapes-candidate-ao-identify-parts-of-circle` [missing_direct_objective; candidate_for_expert_review]
  - proposed objective: Identify parts of a circle.
  - source records: ch12-b006, ch12-b007, ch12-b008-i01, ch12-b008-i02, ch12-b008-i03, ch12-b008-i04, ch12-b008-i05, ch12-b008-i06, ch12-b008-i07, ch12-b008-i08, ch12-b008-i09
  - closest existing AOs: similarities-and-differences-between-plane-shapes-ao-state-similarities, similarities-and-differences-between-plane-shapes-ao-state-differences
  - candidate evidence quote: "different parts of a circle."
  - rationale: The circle records ask learners to name radius, diameter, chord, circumference, and related parts; this is not a similarities/differences comparison objective.

---

## `jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle`

**Title:** Perimeter of regular polygon, square, rectangle, triangle, trapezium, parallelogram and circle.  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-plane-shapes-perimeter-of-regular-polygon-square-rectangle-triangle-trapezium-parallelogram-and-circle-po01`: Find the perimeter of a regular polygon: square, rectangle, triangle, trapezium, parallelogram and circle

### Atomic objectives
- `perimeter-of-plane-shapes-ao-find-perimeter` [find/apply]: Find the perimeter of a regular polygon: square, rectangle, triangle, trapezium, parallelogram and circle.

### Linked textbook records (78 total) — inspected
- `ch12-b009` [exposition] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (instruction)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes
  - evidence quote: "If you trace your finger around the edge of a book or a plate, you have traced the **perimeter** of the shape with your finger. The perimeter of a football field is the white line around the entire field.  Perimeter is…"
- `ch12-b010` [definition] — placed in **shared_foundation**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes
  - evidence quote: "**perimeter** Perimeter is the distance around the outside of a shape."
- `ch12-b011` [exposition] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (instruction)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Counting steps to find perimeter
  - evidence quote: "We can use a practical method to find the perimeter of a 2D shape if the shape is drawn on a grid.  Because perimeter is the distance around the outside of a shape, to find the perimeter of a polygon, we add up the leng…"
- `ch12-b012` [worked_example] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (worked_example)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Worked example 12.3: Finding the perimeter of a square
  - evidence quote: "Determine the perimeter of the square shown in the diagram by counting the steps."
- `ch12-b013` [worked_example] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (worked_example)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Worked example 12.4: Finding the perimeter of a rectangle
  - evidence quote: "Determine the perimeter of the rectangle provided by counting the steps. The length of one side of each small square represents 1 km."
- `ch12-b014` [exercise_block] — placed in **excluded**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.3: Count steps to find perimeter
  - evidence quote: "### Exercise 12.3: Count steps to find perimeter"
- `ch12-b014-i01` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.3: Count steps to find perimeter
  - evidence quote: "### Exercise 12.3: Count steps to find perimeter  1. Find the perimeter the rectangle given below by using the grid on which it is plotted. The length of one side of each small square represents 1 km."
- `ch12-b014-i02` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.3: Count steps to find perimeter
  - evidence quote: "### Exercise 12.3: Count steps to find perimeter  2. Find the perimeter of the following shape. Begin at the dot and follow the direction shown by the arrow. The length of one side of each small square represents 1 cm."
- `ch12-b014-i03` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.3: Count steps to find perimeter
  - evidence quote: "### Exercise 12.3: Count steps to find perimeter  3. Find the perimeter of this shape. The length of one side of each small square is 1 cm."
- `ch12-b014-i04` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.3: Count steps to find perimeter
  - evidence quote: "### Exercise 12.3: Count steps to find perimeter  4. Find the perimeter of this shape. The length of one side of each small square is 1 km."
- `ch12-b014-i05` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.3: Count steps to find perimeter
  - evidence quote: "### Exercise 12.3: Count steps to find perimeter  5. Find the perimeter of this shape. The length of one side of each small square is 1 cm."
- `ch12-b014-i06` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.3: Count steps to find perimeter
  - evidence quote: "### Exercise 12.3: Count steps to find perimeter  6. Find the perimeter the shape. The length of one side of each small square is 1 m."
- `ch12-b015` [exposition] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (instruction)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Perimeter of regular polygons
  - evidence quote: "If a shape is not drawn on grid paper, it will not be possible to "walk" around the shape and count the steps to find the perimeter. Then, to find the **perimeter of a polygon**, we need to know the lengths of all the s…"
- `ch12-b016` [definition] — placed in **shared_foundation**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Perimeter of regular polygons
  - evidence quote: "**regular polygon** In a regular polygon, all the sides have the same length and all the angles are equal.  **perimeter of a polygon** The perimeter of any polygon is the sum of the lengths of all the sides."
- `ch12-b017` [exposition] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (foundation)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Units of measurement for lengths
  - evidence quote: "Perimeter is a distance, and is measured using units of length, such as mm, cm, m or km.  - Millimetres (mm) and centimetres (cm) are appropriate for measuring short lengths. They are used on your ruler. - Metres (m) ar…"
- `ch12-b018` [worked_example] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (worked_example)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Worked example 12.5: Calculating perimeter of a regular polygon
  - evidence quote: "Calculate the perimeter of the regular polygon shown in the diagram. The length of one side from $W$ to $V$ is 12 millimetres."
- `ch12-b019` [exposition] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (instruction)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Units of measurement for lengths
  - evidence quote: "As you have seen in the worked example above, we can use a formula to calculate the perimeter of a regular polygon, because all the sides have the same lengths.  $$ \text {Perimeter of regular polygon = number of sides}…"
- `ch12-b020` [exercise_block] — placed in **excluded**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.4 Calculate perimeter of regular polygons
  - evidence quote: "### Exercise 12.4 Calculate perimeter of regular polygons"
- `ch12-b020-i01` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.4 Calculate perimeter of regular polygons
  - evidence quote: "### Exercise 12.4 Calculate perimeter of regular polygons  1. Calculate the perimeter of the regular polygon below. The length of one side is 7 centimetres."
- `ch12-b020-i02` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.4 Calculate perimeter of regular polygons
  - evidence quote: "### Exercise 12.4 Calculate perimeter of regular polygons  2. Calculate the perimeter of the regular polygon below. The length of one side is 4.5 metres."
- `ch12-b020-i03` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.4 Calculate perimeter of regular polygons
  - evidence quote: "### Exercise 12.4 Calculate perimeter of regular polygons  3. Calculate the perimeter of the regular polygon below. The length of one side is 20 centimetres."
- `ch12-b020-i04` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.4 Calculate perimeter of regular polygons
  - evidence quote: "### Exercise 12.4 Calculate perimeter of regular polygons  4. Calculate the perimeter of the regular polygon below. The length of one side from $W$ to $V$ is 2.6 kilometres."
- `ch12-b020-i05` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.4 Calculate perimeter of regular polygons
  - evidence quote: "### Exercise 12.4 Calculate perimeter of regular polygons  5. Calculate the perimeter of the regular polygon below. The length of one side is 30 millimetres."
- `ch12-b021` [exposition] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (instruction)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Perimeter of irregular polygons
  - evidence quote: "All polygons are not regular polygons. It is possible to draw a polygon where each side has a different length. It is also possible to draw a polygon where some of the sides are equal in length, but others have differen…"
- `ch12-b022` [definition] — placed in **shared_foundation**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Perimeter of irregular polygons
  - evidence quote: "**irregular polygon** In an irregular polygon, all the sides are not the same length and all the angles are not equal."
- `ch12-b023` [exposition] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (instruction)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Perimeter of irregular polygons
  - evidence quote: "To determine the perimeter of an irregular polygon, we have to find the sum of the lengths of all the sides. We cannot use a formula, so we simply add the lengths of all the sides."
- `ch12-b024` [worked_example] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (worked_example)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Worked example 12.6: Calculating perimeter of an irregular triangle
  - evidence quote: "Find the perimeter of the triangle given below."
- `ch12-b025` [worked_example] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (worked_example)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Worked example 12.7: Calculating perimeter of a parallelogram
  - evidence quote: "Find the perimeter of the parallelogram given below."
- `ch12-b026` [exercise_block] — placed in **excluded**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.5: Calculate perimeter of irregular polygons
  - evidence quote: "### Exercise 12.5: Calculate perimeter of irregular polygons"
- `ch12-b026-i01` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.5: Calculate perimeter of irregular polygons
  - evidence quote: "### Exercise 12.5: Calculate perimeter of irregular polygons  1. Give the name of the irregular polygon shown in the diagram, and calculate its perimeter."
- `ch12-b026-i02` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.5: Calculate perimeter of irregular polygons
  - evidence quote: "### Exercise 12.5: Calculate perimeter of irregular polygons  2. Give the name of the irregular polygon shown in the diagram, and find its perimeter."
- `ch12-b026-i03` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.5: Calculate perimeter of irregular polygons
  - evidence quote: "### Exercise 12.5: Calculate perimeter of irregular polygons  3. Give the name of the irregular polygon shown in the diagram, and find its perimeter."
- `ch12-b026-i04` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.5: Calculate perimeter of irregular polygons
  - evidence quote: "### Exercise 12.5: Calculate perimeter of irregular polygons  4. Give the name of the irregular polygon shown in the diagram, and find its perimeter."
- `ch12-b026-i05` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.5: Calculate perimeter of irregular polygons
  - evidence quote: "### Exercise 12.5: Calculate perimeter of irregular polygons  5. Study the diagram below and calculate the perimeter of this shape by using the given lengths in cm."
- `ch12-b026-i06` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.5: Calculate perimeter of irregular polygons
  - evidence quote: "### Exercise 12.5: Calculate perimeter of irregular polygons  6. Study the diagram below and calculate the perimeter of this object by using the given lengths in m."
- `ch12-b026-i07` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.5: Calculate perimeter of irregular polygons
  - evidence quote: "### Exercise 12.5: Calculate perimeter of irregular polygons  7. The diagram below shows a view from above Ms Chidi's house and land. The property has a fence going around the outside. What is the perimeter of the prope…"
- `ch12-b027` [exposition] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (instruction)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Formulae to find the perimeter of a rectangle and a square
  - evidence quote: "It can take long to find the perimeter of a polygon by counting the steps or adding the lengths of the sides. Luckily, there are formulae that we can use for some shapes. The formulae are based on the fact that the peri…"
- `ch12-b028` [worked_example] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (worked_example)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Worked example 12.8: Using a formula to find the perimeter of a rectangle
  - evidence quote: "Find the perimeter of the rectangle given below."
- `ch12-b029` [exposition] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (instruction)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Formulae to find the perimeter of a rectangle and a square
  - evidence quote: "For any parallelogram, including a rectangle, the two lengths are the same length, and the two breadths are the same length. This means we can use the formula we reached in the worked example above to calculate the peri…"
- `ch12-b030` [worked_example] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (worked_example)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Worked example 12.9: Using a formula to find the perimeter of a square
  - evidence quote: "Find the perimeter of the square given below."
- `ch12-b031` [exposition] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (instruction)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Formulae to find the perimeter of a rectangle and a square
  - evidence quote: "The four sides of a square and of a rhombus are all equal. We can therefore use the following formula to calculate the perimeter of a square and a rhombus:  $$ \text{Perimeter of square and rhombus} = 4s $$"
- `ch12-b032` [exposition] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (instruction)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Formulae to calculate perimeter
  - evidence quote: "The table below lists the formulae for the perimeter of the two-dimensional shapes you will be working with. In a formula, we can use $P$ as a symbol for perimeter.  rectangle: ${P} = 2l + 2b$  parallelogram: ${P} = 2l…"
- `ch12-b033` [exercise_block] — placed in **excluded**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.6: Calculate perimeter using formulae
  - evidence quote: "### Exercise 12.6: Calculate perimeter using formulae"
- `ch12-b033-i01` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.6: Calculate perimeter using formulae
  - evidence quote: "### Exercise 12.6: Calculate perimeter using formulae  1. Calculate the perimeter of the rectangle given below."
- `ch12-b033-i02` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.6: Calculate perimeter using formulae
  - evidence quote: "### Exercise 12.6: Calculate perimeter using formulae  2. Calculate the perimeter of the square given below."
- `ch12-b033-i03` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.6: Calculate perimeter using formulae
  - evidence quote: "### Exercise 12.6: Calculate perimeter using formulae  3. Calculate the perimeter of the triangle given below."
- `ch12-b033-i04` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.6: Calculate perimeter using formulae
  - evidence quote: "### Exercise 12.6: Calculate perimeter using formulae  4. Calculate the perimeter of the parallelogram given below."
- `ch12-b033-i05` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.6: Calculate perimeter using formulae
  - evidence quote: "### Exercise 12.6: Calculate perimeter using formulae  5. Calculate the perimeter of the trapezium given below."
- `ch12-b033-i06` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.6: Calculate perimeter using formulae
  - evidence quote: "### Exercise 12.6: Calculate perimeter using formulae  6. Consider the following square. Determine the perimeter of the square."
- `ch12-b033-i07` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.6: Calculate perimeter using formulae
  - evidence quote: "### Exercise 12.6: Calculate perimeter using formulae  7. Consider the following rectangle. Determine the perimeter of the rectangle."
- `ch12-b033-i08` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.6: Calculate perimeter using formulae
  - evidence quote: "### Exercise 12.6: Calculate perimeter using formulae  8. Calculate the perimeter of a triangle with the following side lengths: $\frac {1}{4} \text{m}; \frac {1}{3} \text{m and} \frac {1}{2} \text{m}$."
- `ch12-b033-i09` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.6: Calculate perimeter using formulae
  - evidence quote: "### Exercise 12.6: Calculate perimeter using formulae  9. Calculate the perimeter of a rhombus with side length $\frac {3}{8}$ km."
- `ch12-b033-i10` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.6: Calculate perimeter using formulae
  - evidence quote: "### Exercise 12.6: Calculate perimeter using formulae  10. Calculate the perimeter of the trapezium given below."
- `ch12-b033-i11` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.6: Calculate perimeter using formulae
  - evidence quote: "### Exercise 12.6: Calculate perimeter using formulae  11. The diagram below shows a notebook. What is the perimeter of the notebook if all the measurements are given in centimetres?"
- `ch12-b034` [exposition] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (instruction)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Using a formula to find the circumference of a circle
  - evidence quote: "We know that the perimeter of a circle is called its circumference. The circumference of a circle is a curve, so we cannot measure it with a ruler. We can use a formula to calculate the circumference of a circle. There…"
- `ch12-b035` [definition] — placed in **shared_foundation**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Using a formula to find the circumference of a circle
  - evidence quote: "**radius** The radius of a circle is the distance from the centre to the circumference.  **diameter** The diameter of a circle is the length of a line passing through the centre of the circle, and touching the circumfer…"
- `ch12-b036` [hint] — placed in **excluded**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Using a formula to find the circumference of a circle
  - evidence quote: "The diameter of a circle is double the radius, so $d = 2 \times r$."
- `ch12-b037` [exposition] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (instruction)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Using a formula to find the circumference of a circle
  - evidence quote: "You will see that the symbol $\pi$ is used in both formulae. This name of this symbol is "pi". **$\pi$** is the ratio of the circumference of a circle to its diameter.  $$ \begin{array}{l} \pi = \frac{C}{d} \end{array}…"
- `ch12-b038` [definition] — placed in **shared_foundation**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Using a formula to find the circumference of a circle
  - evidence quote: "$\pi$ (pi) is the ratio of the circumference of a circle to its diameter. The values we use for $\pi$ are 3.14 and $\frac{22}{7}$."
- `ch12-b039` [exposition] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (instruction)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Using a formula to find the circumference of a circle
  - evidence quote: "Look at the value of $\pi$ that your calculator gives you, and compare this to the value of $\frac{22}{7}$. Are they the same number?  $\pi$ is an unending number approximately equal to $\frac{22}{7}$ or 3.14. Here are…"
- `ch12-b040` [worked_example] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (worked_example)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Worked example 12.10: Calculating circumference using diameter
  - evidence quote: "The circle below has a diameter of 8 m. What is the circumference of this circle?"
- `ch12-b041` [hint] — placed in **excluded**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Using a formula to find the circumference of a circle
  - evidence quote: "If you have a $\pi$ button on your calculator, you may use it to work out the answer. But if the question gives you a value to use, such as 3.14, use that value."
- `ch12-b042` [worked_example] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (worked_example)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Worked example 12.11: Calculating circumference using radius
  - evidence quote: "The circle below has a radius of 2 cm. What is the circumference of the circle? Use 3.14 for $\pi$."
- `ch12-b043` [exercise_block] — placed in **excluded**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.7: Calculate the circumference of a circle
  - evidence quote: "### Exercise 12.7: Calculate the circumference of a circle  Use 3.14 for $\pi$ in all your calculations."
- `ch12-b043-i01` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.7: Calculate the circumference of a circle
  - evidence quote: "### Exercise 12.7: Calculate the circumference of a circle  Use 3.14 for $\pi$ in all your calculations.  1. The circle below has a diameter of 9 cm. What is the circumference of the circle?"
- `ch12-b043-i02` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.7: Calculate the circumference of a circle
  - evidence quote: "### Exercise 12.7: Calculate the circumference of a circle  Use 3.14 for $\pi$ in all your calculations.  2. The circle below has a radius of 5 cm. What is the circumference of the circle?"
- `ch12-b043-i03` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.7: Calculate the circumference of a circle
  - evidence quote: "### Exercise 12.7: Calculate the circumference of a circle  Use 3.14 for $\pi$ in all your calculations.  3. If a circle has a diameter of 11 m, what is the circumference of the circle?"
- `ch12-b043-i04` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.7: Calculate the circumference of a circle
  - evidence quote: "### Exercise 12.7: Calculate the circumference of a circle  Use 3.14 for $\pi$ in all your calculations.  4. If a circle has a radius of 10 m, what is the circumference of the circle?"
- `ch12-b043-i05` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.7: Calculate the circumference of a circle
  - evidence quote: "### Exercise 12.7: Calculate the circumference of a circle  Use 3.14 for $\pi$ in all your calculations.  5. What is the circumference of a circle that has a diameter of 40 mm?"
- `ch12-b043-i06` [exercise_item] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.2 Perimeter of two-dimensional shapes > Exercise 12.7: Calculate the circumference of a circle
  - evidence quote: "### Exercise 12.7: Calculate the circumference of a circle  Use 3.14 for $\pi$ in all your calculations.  6. What is the circumference of a circle that has a radius of 50 mm?"
- `ch12-b069` [exposition] — placed in **AO:perimeter-of-plane-shapes-ao-find-perimeter (instruction)**
  - heading: Chapter 12: Two-dimensional shapes > 12.4 Practical applications
  - evidence quote: "In real life we often need to calculate a perimeter or area. Then it is useful to know the correct formula as well as how to use the formula."
- `ch12-b071` [exercise_block] — placed in **excluded**
  - heading: Chapter 12: Two-dimensional shapes > 12.4 Practical applications > Exercise 12.12 :Find perimeter and area in real life situations
  - evidence quote: "### Exercise 12.12: Find perimeter and area in real life situations"
- `ch12-b071-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 12: Two-dimensional shapes > 12.4 Practical applications > Exercise 12.12 :Find perimeter and area in real life situations
  - evidence quote: "### Exercise 12.12: Find perimeter and area in real life situations  1. The diagram below shows a notebook with all the measurements given in centimetres.  Find the perimeter of the notebook."
- `ch12-b071-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 12: Two-dimensional shapes > 12.4 Practical applications > Exercise 12.12 :Find perimeter and area in real life situations
  - evidence quote: "### Exercise 12.12: Find perimeter and area in real life situations  2. The diagram below shows a notebook with all the measurements given in centimetres.  Find the area of the notebook."
- `ch12-b071-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 12: Two-dimensional shapes > 12.4 Practical applications > Exercise 12.12 :Find perimeter and area in real life situations
  - evidence quote: "### Exercise 12.12: Find perimeter and area in real life situations  3. Adanna is renovating her house, and she wants to have a blind made for the window. The blind will be a flat piece of fabric that reaches to the out…"
- `ch12-b071-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 12: Two-dimensional shapes > 12.4 Practical applications > Exercise 12.12 :Find perimeter and area in real life situations
  - evidence quote: "### Exercise 12.12: Find perimeter and area in real life situations  4. Adanna is renovating her house, and she wants to have a blind made for the window. The blind will be a flat piece of fabric that reaches to the out…"
- `ch12-b071-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 12: Two-dimensional shapes > 12.4 Practical applications > Exercise 12.12 :Find perimeter and area in real life situations
  - evidence quote: "### Exercise 12.12: Find perimeter and area in real life situations  5. Talatu paints plates to sell to tourists. She paints the plates purple with a white circle in the centre.  The diagram below shows the plate. $O$ i…"
- `ch12-b072` [summary] — placed in **excluded**
  - heading: Chapter 12: Two-dimensional shapes > 12.5 Summary
  - evidence quote: "A two-dimensional (2D) shape has two dimensions that we can measure: length and breadth (or width).  A polygon is a closed flat shape with three or more straight sides. A triangle has three sides and three angles. A qua…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch12-b071-i01..i05 are real-life perimeter-and-area exercises; the area portion is outside the perimeter AO scope.
- **no_reused_assessment**: The AO has direct worked examples and exercises but no reused assessment.

### Per-atomic-objective evidence classification
- `perimeter-of-plane-shapes-ao-find-perimeter` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch12-b009(instruction), ch12-b011(instruction), ch12-b012(worked_example), ch12-b013(worked_example), ch12-b014-i01(exercise), ch12-b014-i02(exercise), ch12-b014-i03(exercise), ch12-b014-i04(exercise), ch12-b014-i05(exercise), ch12-b014-i06(exercise), ch12-b015(instruction), ch12-b017(foundation), ch12-b018(worked_example), ch12-b019(instruction), ch12-b020-i01(exercise), ch12-b020-i02(exercise), ch12-b020-i03(exercise), ch12-b020-i04(exercise), ch12-b020-i05(exercise), ch12-b021(instruction), ch12-b023(instruction), ch12-b024(worked_example), ch12-b025(worked_example), ch12-b026-i01(exercise), ch12-b026-i02(exercise), ch12-b026-i03(exercise), ch12-b026-i04(exercise), ch12-b026-i05(exercise), ch12-b026-i06(exercise), ch12-b026-i07(exercise), ch12-b027(instruction), ch12-b028(worked_example), ch12-b029(instruction), ch12-b030(worked_example), ch12-b031(instruction), ch12-b032(instruction), ch12-b033-i01(exercise), ch12-b033-i02(exercise), ch12-b033-i03(exercise), ch12-b033-i04(exercise), ch12-b033-i05(exercise), ch12-b033-i06(exercise), ch12-b033-i07(exercise), ch12-b033-i08(exercise), ch12-b033-i09(exercise), ch12-b033-i10(exercise), ch12-b033-i11(exercise), ch12-b034(instruction), ch12-b037(instruction), ch12-b039(instruction), ch12-b040(worked_example), ch12-b042(worked_example), ch12-b043-i01(exercise), ch12-b043-i02(exercise), ch12-b043-i03(exercise), ch12-b043-i04(exercise), ch12-b043-i05(exercise), ch12-b043-i06(exercise), ch12-b069(instruction)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-plane-shapes-area-of-regular-plane-shapes-such-as-squares-rectangles-parallelograms-etc`

**Title:** Area of regular plane shapes such as: Squares, rectangles, parallelograms, etc.  
**Status:** `needs_review`  
**Row review categories:** no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-plane-shapes-area-of-regular-plane-shapes-such-as-squares-rectangles-parallelograms-etc-po01`: Find the area of plane shapes such as squares, rectangles, parallelograms
- `jss1-math-plane-shapes-area-of-regular-plane-shapes-such-as-squares-rectangles-parallelograms-etc-po02`: Find the area of real life plane objects

### Atomic objectives
- `area-of-plane-shapes-ao-find-area-of-plane-shapes` [find/apply]: Find the area of plane shapes such as squares, rectangles, parallelograms.
- `area-of-plane-shapes-ao-find-area-of-real-life-objects` [find/apply]: Find the area of real life plane objects.

### Linked textbook records (60 total) — inspected
- `ch12-b044` [exposition] — placed in **shared_foundation**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes
  - evidence quote: "**Area** is the amount of flat space taken up by a shape. So we can think of area as the surface of a shape that you can cover or paint. For example, the space inside the white line painted around a football field is th…"
- `ch12-b045` [definition] — placed in **shared_foundation**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes
  - evidence quote: "**area** Area is the amount of flat space taken up by a shape."
- `ch12-b046` [exposition] — placed in **shared_foundation**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Units of measurement for area
  - evidence quote: "We measure the area of a two-dimensional shape by counting or working out how many unit squares will fit into the space. Examples of units of measurement for area are $\text{mm}^{2}$, $\text{cm}^{2}$, $\text{m}^{2}$, or…"
- `ch12-b047` [exposition] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (instruction)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Determine area by counting squares on grid
  - evidence quote: "If a diagram is drawn on a grid, you can simply count the squares to find the area of the shape. Each small square on the grid can represent a square in real life.  - One small square on the grid can represent an area o…"
- `ch12-b048` [worked_example] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (worked_example)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Worked example 12.12: Counting squares to find the area of a rectangle
  - evidence quote: "Consider the diagram of a rectangle below. Use the grid to determine the area of the rectangle. Each small square on the grid represents a square of 1 km by 1 km."
- `ch12-b049` [worked_example] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (worked_example)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Worked example 12.13: Counting squares to find the area of a square
  - evidence quote: "Determine the area of the square shown below by counting the number of smaller squares on the grid that are covered by the square. Each square on the grid represents a square of 1 cm by 1 cm."
- `ch12-b050` [exercise_block] — placed in **excluded**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.8: Counting squares to determine area
  - evidence quote: "### Exercise 12.8: Counting squares to determine area"
- `ch12-b050-i01` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.8: Counting squares to determine area
  - evidence quote: "### Exercise 12.8: Counting squares to determine area  1. Consider the diagram of a rectangle below. Determine the area of the rectangle by counting the squares on the grid. Each small square represents 1 m by 1 m."
- `ch12-b050-i02` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.8: Counting squares to determine area
  - evidence quote: "### Exercise 12.8: Counting squares to determine area  2. Determine the area of the square shown below by counting the smaller squares on the grid. Each small square represents 1 cm by 1 cm."
- `ch12-b050-i03` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.8: Counting squares to determine area
  - evidence quote: "### Exercise 12.8: Counting squares to determine area  3. Determine the area of the polygon provided. Each small square represents 1 cm by 1 cm."
- `ch12-b050-i04` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.8: Counting squares to determine area
  - evidence quote: "### Exercise 12.8: Counting squares to determine area  4. Determine the area of the polygon. Each square represents 1 m by 1 m."
- `ch12-b050-i05` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.8: Counting squares to determine area
  - evidence quote: "### Exercise 12.8: Counting squares to determine area  5. Determine the area of the triangle shown below. Each small square represents 1 cm by 1 cm."
- `ch12-b051` [exposition] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (instruction)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Using formulae to calculate area
  - evidence quote: "If a shape is not drawn on a grid, you cannot find the area of the shape by counting the squares, but there are formulae that you can use to calculate area.  You can check that the formulae are correct by comparing the…"
- `ch12-b052` [worked_example] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (worked_example)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Worked example 12.14: Comparing methods of calculating area of a rectangle
  - evidence quote: "Find the area of the rectangle provided by counting squares. Each square on the grid represents a square of 1 km by 1 km. Then work out a formula for calculating the area of a rectangle, and check the answer you get by…"
- `ch12-b053` [worked_example] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (worked_example)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Worked example 12.15: Comparing methods of calculating area of a square
  - evidence quote: "Find the area of the square provided by counting squares. Each square on the grid represents a square of 1 cm by 1 cm. Then work out a formula for calculating the area of a square, and check the answer you get by compar…"
- `ch12-b054` [exposition] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (instruction)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Formulae for the area of a two-dimensional shape
  - evidence quote: "It will help you if you memorise the formulae for area, so that you can use them easily when you need to. Understanding where the formulae come from will help you to memorise them.  - **Rectangle:** Area of a rectangle…"
- `ch12-b055` [summary] — placed in **excluded**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Summary of the area formulae
  - evidence quote: "In the formulae, we can use $A$ to stand for area.  | Shape | Area formula | | --- | --- | | rectangle | $A = l \times b$ | | square | $A = s \times s = s^{2}$ | | triangle | $A = \frac{b \times h}{2}$ | | parallelogram…"
- `ch12-b056` [exercise_block] — placed in **excluded**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.9: Identify the correct area formula
  - evidence quote: "### Exercise 12.9: Identify the correct area formula"
- `ch12-b056-i01` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.9: Identify the correct area formula
  - evidence quote: "### Exercise 12.9: Identify the correct area formula  1. For each of the shapes shown below, identify the correct formula for the area of the shape.  Choices: 1. $A = \pi \times r^{2}$ 2. $A = s^{2}$ 3. $A = \frac{b \ti…"
- `ch12-b056-i02` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.9: Identify the correct area formula
  - evidence quote: "### Exercise 12.9: Identify the correct area formula  2. Identify the correct formula for the area of the given shape.  Choices: 1. $A = \pi \times r^{2}$ 2. $A = s^{2}$ 3. $A = \frac{b \times h}{2}$ 4. $A = b \times h$…"
- `ch12-b056-i03` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.9: Identify the correct area formula
  - evidence quote: "### Exercise 12.9: Identify the correct area formula  3. Which is the correct formula for the area of the shapes provided?  Choices: 1. $A = \pi \times r^{2}$ 2. $A = b^{2}$ 3. $A = \frac{b \times h}{2}$ 4. $A = b \time…"
- `ch12-b057` [exposition] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (instruction)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Using formulae to calculate area
  - evidence quote: "It saves lots of time if you know the correct formula to use when you have to calculate the area of a shape. Then you simply write down the correct formula, substitute the given values into the formula, and do the calcu…"
- `ch12-b058` [worked_example] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (worked_example)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Worked example 12.16: Finding area of a rectangle using a formula
  - evidence quote: "Find the area of a rectangle with length 15 cm and breadth 5 cm."
- `ch12-b059` [worked_example] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (worked_example)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Worked example 12.17: Finding area of a square using a formula
  - evidence quote: "Find the area of a square with side length 7 m."
- `ch12-b060` [worked_example] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (worked_example)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Worked example 12.18: Finding area of a triangle using a formula
  - evidence quote: "Find the area of a triangle with base 12 cm and height 5 cm."
- `ch12-b061` [worked_example] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (worked_example)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Worked example 12.19: Finding area of a parallelogram using a formula
  - evidence quote: "Find the area of a parallelogram with base 20 cm and height 14 cm."
- `ch12-b062` [worked_example] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (worked_example)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Worked example 12.20: Finding area of a trapezium using a formula
  - evidence quote: "Find the area of a trapezium with height 6 cm and parallel sides 7 cm and 15 cm."
- `ch12-b063` [worked_example] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (worked_example)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Worked example 12.21: Finding area of a circle using a formula
  - evidence quote: "Find the area of a circle with radius 7 mm. Use 3.14 for $\pi$."
- `ch12-b064` [exercise_block] — placed in **excluded**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.10: Use formulae to calculate area
  - evidence quote: "### Exercise 12.10: Use formulae to calculate area"
- `ch12-b064-i01` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.10: Use formulae to calculate area
  - evidence quote: "### Exercise 12.10: Use formulae to calculate area  1. Calculate the area of rectangle PQRS with side lengths 30 mm and 20 mm."
- `ch12-b064-i02` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.10: Use formulae to calculate area
  - evidence quote: "### Exercise 12.10: Use formulae to calculate area  2. Find the area of a rectangle with length 5 m and breadth 7.25 m."
- `ch12-b064-i03` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.10: Use formulae to calculate area
  - evidence quote: "### Exercise 12.10: Use formulae to calculate area  3. Determine the area of a square with side length 90 mm."
- `ch12-b064-i04` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.10: Use formulae to calculate area
  - evidence quote: "### Exercise 12.10: Use formulae to calculate area  4. Determine the area of a square with side length 8.75 mm."
- `ch12-b064-i05` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.10: Use formulae to calculate area
  - evidence quote: "### Exercise 12.10: Use formulae to calculate area  5. Calculate the area of a triangle with base 25 mm and height 8 mm."
- `ch12-b064-i06` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.10: Use formulae to calculate area
  - evidence quote: "### Exercise 12.10: Use formulae to calculate area  6. Calculate the area of a triangle with base 10.4 m and height 5 m."
- `ch12-b064-i07` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.10: Use formulae to calculate area
  - evidence quote: "### Exercise 12.10: Use formulae to calculate area  7. Find the area of a parallelogram with base 40 m and height 18 m."
- `ch12-b064-i08` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.10: Use formulae to calculate area
  - evidence quote: "### Exercise 12.10: Use formulae to calculate area  8. Determine the area of a parallelogram with base 37.5 mm and height 20 mm."
- `ch12-b064-i09` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.10: Use formulae to calculate area
  - evidence quote: "### Exercise 12.10: Use formulae to calculate area  9. Find the area of a trapezium with height 15 cm and parallel sides 30 cm and 50 cm."
- `ch12-b064-i10` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.10: Use formulae to calculate area
  - evidence quote: "### Exercise 12.10: Use formulae to calculate area  10. Find the area of a trapezium with height 8 m and parallel sides 9.6 m and 5.4 m."
- `ch12-b064-i11` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.10: Use formulae to calculate area
  - evidence quote: "### Exercise 12.10: Use formulae to calculate area  11. The circle has a radius of 4 m. What is its area? Use 3.14 for $\pi$."
- `ch12-b064-i12` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.10: Use formulae to calculate area
  - evidence quote: "### Exercise 12.10: Use formulae to calculate area  12. The circle has a diameter of 6 km. What is its area? Use 3.14 for $\pi$."
- `ch12-b064-i13` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.10: Use formulae to calculate area
  - evidence quote: "### Exercise 12.10: Use formulae to calculate area  13. If a circle has a radius of 10 mm, what is its area? Use 3.14 for $\pi$ in your calculation, and round your answer to two decimal places."
- `ch12-b064-i14` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.10: Use formulae to calculate area
  - evidence quote: "### Exercise 12.10: Use formulae to calculate area  14. If a circle has a diameter of 40 cm, what is its area? Use 3.14 for $\pi$, and round your answer to two decimal places."
- `ch12-b065` [exposition] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (instruction)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Area of irregular shapes
  - evidence quote: "Sometimes we have to calculate the area of an irregular shape. Remember that in an irregular polygon, all the sides are not the same length and all the angles are not equal.  Often the irregular shape you are given to w…"
- `ch12-b066` [worked_example] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (worked_example)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Worked example 12.22: Finding area of irregular shape by counting squares
  - evidence quote: "Determine the area of the given shape. Each square represents a $\text{1}\ \text{cm} \times \text{1}\ \text{cm}$ area."
- `ch12-b067` [worked_example] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (worked_example)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Worked example 12.23: Finding area of irregular shape by counting squares
  - evidence quote: "Calculate the area of the shape below, using the given lengths in cm."
- `ch12-b068` [exercise_block] — placed in **excluded**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.11: Calculate the area of irregular shapes
  - evidence quote: "### Exercise 12.11: Calculate the area of irregular shapes"
- `ch12-b068-i01` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.11: Calculate the area of irregular shapes
  - evidence quote: "### Exercise 12.11: Calculate the area of irregular shapes  1. Calculate the area of the shape provided. The given lengths are in cm."
- `ch12-b068-i02` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.11: Calculate the area of irregular shapes
  - evidence quote: "### Exercise 12.11: Calculate the area of irregular shapes  2. Calculate the area of this irregular polygon, using the given lengths in m."
- `ch12-b068-i03` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.11: Calculate the area of irregular shapes
  - evidence quote: "### Exercise 12.11: Calculate the area of irregular shapes  3. In the diagram below, one of the lengths of the sides has been replaced by $z$. The other five sides have the lengths shown in the figure. All of the angles…"
- `ch12-b068-i04` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-plane-shapes (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.3 Area of two-dimensional shapes > Exercise 12.11: Calculate the area of irregular shapes
  - evidence quote: "### Exercise 12.11: Calculate the area of irregular shapes  4. In the shape below, one of the lengths of the sides has been replaced by $z$. The other five sides have the lengths shown. All of the angles are right angle…"
- `ch12-b069` [exposition] — placed in **AO:area-of-plane-shapes-ao-find-area-of-real-life-objects (instruction)**
  - heading: Chapter 12: Two-dimensional shapes > 12.4 Practical applications
  - evidence quote: "In real life we often need to calculate a perimeter or area. Then it is useful to know the correct formula as well as how to use the formula."
- `ch12-b070` [worked_example] — placed in **AO:area-of-plane-shapes-ao-find-area-of-real-life-objects (worked_example)**
  - heading: Chapter 12: Two-dimensional shapes > 12.4 Practical applications > Worked example 12.24: Finding area in a real life situation
  - evidence quote: "Atinuke is working on a new design to print on fabric. He wants a pink circle with a smaller white circle inside it. The diagram below shows the design.  $O$ is the centre of the two circles. The radius of the small cir…"
- `ch12-b071` [exercise_block] — placed in **excluded**
  - heading: Chapter 12: Two-dimensional shapes > 12.4 Practical applications > Exercise 12.12 :Find perimeter and area in real life situations
  - evidence quote: "### Exercise 12.12: Find perimeter and area in real life situations"
- `ch12-b071-i01` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-real-life-objects (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.4 Practical applications > Exercise 12.12 :Find perimeter and area in real life situations
  - evidence quote: "### Exercise 12.12: Find perimeter and area in real life situations  1. The diagram below shows a notebook with all the measurements given in centimetres.  Find the perimeter of the notebook."
- `ch12-b071-i02` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-real-life-objects (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.4 Practical applications > Exercise 12.12 :Find perimeter and area in real life situations
  - evidence quote: "### Exercise 12.12: Find perimeter and area in real life situations  2. The diagram below shows a notebook with all the measurements given in centimetres.  Find the area of the notebook."
- `ch12-b071-i03` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-real-life-objects (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.4 Practical applications > Exercise 12.12 :Find perimeter and area in real life situations
  - evidence quote: "### Exercise 12.12: Find perimeter and area in real life situations  3. Adanna is renovating her house, and she wants to have a blind made for the window. The blind will be a flat piece of fabric that reaches to the out…"
- `ch12-b071-i04` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-real-life-objects (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.4 Practical applications > Exercise 12.12 :Find perimeter and area in real life situations
  - evidence quote: "### Exercise 12.12: Find perimeter and area in real life situations  4. Adanna is renovating her house, and she wants to have a blind made for the window. The blind will be a flat piece of fabric that reaches to the out…"
- `ch12-b071-i05` [exercise_item] — placed in **AO:area-of-plane-shapes-ao-find-area-of-real-life-objects (exercise)**
  - heading: Chapter 12: Two-dimensional shapes > 12.4 Practical applications > Exercise 12.12 :Find perimeter and area in real life situations
  - evidence quote: "### Exercise 12.12: Find perimeter and area in real life situations  5. Talatu paints plates to sell to tourists. She paints the plates purple with a white circle in the centre.  The diagram below shows the plate. $O$ i…"
- `ch12-b072` [summary] — placed in **excluded**
  - heading: Chapter 12: Two-dimensional shapes > 12.5 Summary
  - evidence quote: "A two-dimensional (2D) shape has two dimensions that we can measure: length and breadth (or width).  A polygon is a closed flat shape with three or more straight sides. A triangle has three sides and three angles. A qua…"

### Row-level review categories and manually authored reasons
- **no_reused_assessment**: Both AOs (plane-shapes area and real-life-object area) have direct worked examples and exercises but no reused assessment was selected.

### Per-atomic-objective evidence classification
- `area-of-plane-shapes-ao-find-area-of-plane-shapes` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch12-b047(instruction), ch12-b048(worked_example), ch12-b049(worked_example), ch12-b050-i01(exercise), ch12-b050-i02(exercise), ch12-b050-i03(exercise), ch12-b050-i04(exercise), ch12-b050-i05(exercise), ch12-b051(instruction), ch12-b052(worked_example), ch12-b053(worked_example), ch12-b054(instruction), ch12-b056-i01(exercise), ch12-b056-i02(exercise), ch12-b056-i03(exercise), ch12-b057(instruction), ch12-b058(worked_example), ch12-b059(worked_example), ch12-b060(worked_example), ch12-b061(worked_example), ch12-b062(worked_example), ch12-b063(worked_example), ch12-b064-i01(exercise), ch12-b064-i02(exercise), ch12-b064-i03(exercise), ch12-b064-i04(exercise), ch12-b064-i05(exercise), ch12-b064-i06(exercise), ch12-b064-i07(exercise), ch12-b064-i08(exercise), ch12-b064-i09(exercise), ch12-b064-i10(exercise), ch12-b064-i11(exercise), ch12-b064-i12(exercise), ch12-b064-i13(exercise), ch12-b064-i14(exercise), ch12-b065(instruction), ch12-b066(worked_example), ch12-b067(worked_example), ch12-b068-i01(exercise), ch12-b068-i02(exercise), ch12-b068-i03(exercise), ch12-b068-i04(exercise)
  - assessment: _(none anchored)_
- `area-of-plane-shapes-ao-find-area-of-real-life-objects` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch12-b069(instruction), ch12-b070(worked_example), ch12-b071-i01(exercise), ch12-b071-i02(exercise), ch12-b071-i03(exercise), ch12-b071-i04(exercise), ch12-b071-i05(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-three-dimensional-figures-identification-of-3d-shapes`

**Title:** Identification of three-dimensional shapes  
**Status:** `needs_review`  
**Row review categories:** ao_no_evidence, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-three-dimensional-figures-identification-of-3d-shapes-po01`: Identify common three-dimensional shapes
- `jss1-math-three-dimensional-figures-identification-of-3d-shapes-po02`: Distinguish between 2D and 3D shapes

### Atomic objectives
- `identification-of-3d-shapes-ao-identify-common-shapes` [identify/remember]: Identify common three-dimensional shapes.
- `identification-of-3d-shapes-ao-distinguish-2d-and-3d` [distinguish/understand]: Distinguish between 2D and 3D shapes.

### Linked textbook records (7 total) — inspected
- `ch13-b001` [exposition] — placed in **shared_foundation**
  - heading: Chapter 13: Three-dimensional objects
  - evidence quote: "A three-dimensional (3D) object has three dimensions that we can measure: length, breadth (or width), and height.  You will remember that a two-dimensional shape has only two dimensions that we can measure, which are le…"
- `ch13-b047` [exercise_block] — placed in **excluded**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres > Exercise 13.12: Describe the properties of 3D objects
  - evidence quote: "### Exercise 13.12: Describe the properties of 3D objects"
- `ch13-b047-i01` [exercise_item] — placed in **AO:identification-of-3d-shapes-ao-identify-common-shapes (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres > Exercise 13.12: Describe the properties of 3D objects
  - evidence quote: "### Exercise 13.12: Describe the properties of 3D objects  1. Identify each of the 3D objects labelled A to F shown in the diagram."
- `ch13-b047-i02` [exercise_item] — placed in **AO:identification-of-3d-shapes-ao-identify-common-shapes (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres > Exercise 13.12: Describe the properties of 3D objects
  - evidence quote: "### Exercise 13.12: Describe the properties of 3D objects  2. Consider the following 3D objects: cube, cuboid, pyramid, cone, cylinder and sphere. Write the name of each of the 3D objects in the correct column of the ta…"
- `ch13-b047-i03` [exercise_item] — placed in **AO:identification-of-3d-shapes-ao-identify-common-shapes (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres > Exercise 13.12: Describe the properties of 3D objects
  - evidence quote: "### Exercise 13.12: Describe the properties of 3D objects  3. Select a word from Column B that best fits the description in Column A.  | Column A | Column B | | --- | --- | | a) A 3D object with no edges and no vertices…"
- `ch13-b047-i04` [exercise_item] — placed in **AO:identification-of-3d-shapes-ao-identify-common-shapes (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres > Exercise 13.12: Describe the properties of 3D objects
  - evidence quote: "### Exercise 13.12: Describe the properties of 3D objects  4. Complete the table below.  | Name of 3D object | Number of faces | Number of edges | Number or vertices | | --- | --- | --- | --- | | cube |  |  |  | | cuboi…"
- `ch13-b053` [summary] — placed in **excluded**
  - heading: Chapter 13: Three-dimensional objects > 13.7 Summary
  - evidence quote: "A three-dimensional (3D) object has three dimensions that we can measure: length, breadth (or width), and height.  We use the main parts of a 3D object to describe its properties: - A 3D object has faces. The faces can…"

### Row-level review categories and manually authored reasons
- **ao_no_evidence**: distinguish-2d-and-3d AO has no record_links; the linked records describe specific 3D objects but do not explicitly contrast them with 2D shapes.
- **no_reused_assessment**: identify-common-shapes AO has direct exercises (ch13-b047-i01..i04) but no reused assessment was selected.

### Per-atomic-objective evidence classification
- `identification-of-3d-shapes-ao-identify-common-shapes` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch13-b047-i01(exercise), ch13-b047-i02(exercise), ch13-b047-i03(exercise), ch13-b047-i04(exercise)
  - assessment: _(none anchored)_
- `identification-of-3d-shapes-ao-distinguish-2d-and-3d` → evidence: **none** · categories: ao_no_evidence
  - linked records: _(none)_
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids`

**Title:** Basic properties of cubes and cuboids.  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-three-dimensional-figures-basic-properties-of-cubes-and-cuboids-po01`: Identify the properties of cubes and cuboids

### Atomic objectives
- `basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cubes` [identify/remember]: Identify the properties of cubes.
- `basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cuboids` [identify/remember]: Identify the properties of cuboids.

### Linked textbook records (38 total) — inspected
- `ch13-b002` [exposition] — placed in **shared_foundation**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids
  - evidence quote: "One of the groups of 3D objects is called **prisms**. Examples of prisms are shown below.  A prism has certain properties:  - A prism is a type of solid (3D object) that has a **polygon** as a base. - The top face of a…"
- `ch13-b003` [definition] — placed in **shared_foundation**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids
  - evidence quote: "**prism** A prism is a solid figure with the top and bottom faces parallel to each other. The top and bottom faces are polygons and are exactly the same. The side faces of a prism are rectangles.  **polygon** A polygon…"
- `ch13-b004` [exposition] — placed in **shared_foundation**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids
  - evidence quote: "We are going to study the properties of two types of prisms, namely cubes and cuboids."
- `ch13-b005` [exposition] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cubes (instruction)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Cubes
  - evidence quote: "A cube is a 3D object that is formed by six equal squares.  There are many real-life objects in the shape of a cube. A dice is a cube. Children often play with blocks in the form of cubes. You may also have seen a box i…"
- `ch13-b006` [definition] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cubes (foundation)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Cubes
  - evidence quote: "**cube** A cube is a 3D object that is formed by six equal squares.  **face** A face is a flat surface of a 3D shape.  **base** The base is the flat surface at the bottom of a 3D object on which the object stands.  **ed…"
- `ch13-b007` [exposition] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cubes (instruction)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Cubes
  - evidence quote: "A cube is a prism, because the base and top face are squares, and a square is a polygon. The side faces of a cube are also squares, which are a special type of rectangle. The side faces are perpendicular to the base of…"
- `ch13-b008` [worked_example] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cubes (worked_example)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Worked example 13.1: Identifying the parts of a cube
  - evidence quote: "Consider the cube given below.  1. What is the shaded area labelled $A$ called? 2. What is the point labelled $B$ (in the first diagram) called? 3. What is the line labelled $CD$ called?"
- `ch13-b009` [worked_example] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cubes (worked_example)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Worked example 13.2: Describing the properties of a cube
  - evidence quote: "Consider the 3D object given below.  1. How many faces does a cube have? 2. What is the shape of the faces of a cube? 3. How many edges does a cube have? 4. How many vertices does a cube have?"
- `ch13-b010` [exercise_block] — placed in **excluded**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Exercise 13.1: Identify the parts of a cube
  - evidence quote: "### Exercise 13.1: Identify the parts of a cube  Consider the diagram of the 3D object below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-011.png]"
- `ch13-b010-i01` [exercise_item] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cubes (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Exercise 13.1: Identify the parts of a cube
  - evidence quote: "### Exercise 13.1: Identify the parts of a cube  Consider the diagram of the 3D object below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-011.png]  1.…"
- `ch13-b010-i02` [exercise_item] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cubes (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Exercise 13.1: Identify the parts of a cube
  - evidence quote: "### Exercise 13.1: Identify the parts of a cube  Consider the diagram of the 3D object below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-011.png]  2.…"
- `ch13-b010-i03` [exercise_item] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cubes (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Exercise 13.1: Identify the parts of a cube
  - evidence quote: "### Exercise 13.1: Identify the parts of a cube  Consider the diagram of the 3D object below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-011.png]  3.…"
- `ch13-b010-i04` [exercise_item] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cubes (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Exercise 13.1: Identify the parts of a cube
  - evidence quote: "### Exercise 13.1: Identify the parts of a cube  Consider the diagram of the 3D object below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-011.png]  4.…"
- `ch13-b010-i05` [exercise_item] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cubes (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Exercise 13.1: Identify the parts of a cube
  - evidence quote: "### Exercise 13.1: Identify the parts of a cube  Consider the diagram of the 3D object below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-011.png]  5.…"
- `ch13-b011` [exercise_block] — placed in **excluded**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Exercise 13.2: Describe the properties of a cube
  - evidence quote: "### Exercise 13.2: Describe the properties of a cube"
- `ch13-b011-i01` [exercise_item] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cubes (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Exercise 13.2: Describe the properties of a cube
  - evidence quote: "### Exercise 13.2: Describe the properties of a cube  1. Select a word from Column B that best fits the description in Column A. Write down only the number for the description in Column A, and the capital letter that gi…"
- `ch13-b011-i02` [exercise_item] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cubes (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Exercise 13.2: Describe the properties of a cube
  - evidence quote: "### Exercise 13.2: Describe the properties of a cube  2. Complete the table given below.  **Properties of a cube**  | Number and shape of faces | Number of edges | Number of vertices | | --- | --- | --- | |  |  |  |"
- `ch13-b012` [exposition] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cuboids (instruction)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Cuboids
  - evidence quote: "A **cuboid** is formed by three pairs of rectangles. Each pair of rectangles is opposite each other and equal in size.  There are many real life objects in the shape of a cuboid, such as those shown in the examples belo…"
- `ch13-b013` [note] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cuboids (foundation)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Cuboids
  - evidence quote: "Remember that vertices is the plural of vertex. So we refer to one vertex and eight vertices."
- `ch13-b014` [definition] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cuboids (foundation)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Cuboids
  - evidence quote: "**cuboid** A cuboid is a prism formed by three pairs of rectangles. The rectangles opposite each other are equal to each other."
- `ch13-b015` [exposition] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cuboids (instruction)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Cuboids
  - evidence quote: "A cuboid is a prism, because it has a rectangle as a base and a rectangle is a polygon. The side faces of a cuboid are rectangles that are perpendicular to the base of the cuboid."
- `ch13-b016` [worked_example] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cuboids (worked_example)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Worked example 13.3: Identifying the parts of a cuboid
  - evidence quote: "Consider the cuboid given below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-022.png]  Question 1: What is the shaded area labelled $D$ called?  Questi…"
- `ch13-b017` [worked_example] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cuboids (worked_example)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Worked example 13.4: Describing the properties of a cuboid
  - evidence quote: "Consider the 3D object given below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-013.png]  Question 1: How many faces does a cuboid have?  Question 2: W…"
- `ch13-b018` [exercise_block] — placed in **excluded**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Exercise 13.3: Describe the parts of a cuboid
  - evidence quote: "### Exercise 13.3: Describe the parts of a cuboid  Consider the diagram of 3D object below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-022.png]"
- `ch13-b018-i01` [exercise_item] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cuboids (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Exercise 13.3: Describe the parts of a cuboid
  - evidence quote: "### Exercise 13.3: Describe the parts of a cuboid  Consider the diagram of 3D object below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-022.png]  1. Wh…"
- `ch13-b018-i02` [exercise_item] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cuboids (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Exercise 13.3: Describe the parts of a cuboid
  - evidence quote: "### Exercise 13.3: Describe the parts of a cuboid  Consider the diagram of 3D object below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-022.png]  2. Wh…"
- `ch13-b018-i03` [exercise_item] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cuboids (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Exercise 13.3: Describe the parts of a cuboid
  - evidence quote: "### Exercise 13.3: Describe the parts of a cuboid  Consider the diagram of 3D object below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-022.png]  3. Wh…"
- `ch13-b018-i04` [exercise_item] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cuboids (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Exercise 13.3: Describe the parts of a cuboid
  - evidence quote: "### Exercise 13.3: Describe the parts of a cuboid  Consider the diagram of 3D object below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-022.png]  4. Na…"
- `ch13-b018-i05` [exercise_item] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cuboids (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Exercise 13.3: Describe the parts of a cuboid
  - evidence quote: "### Exercise 13.3: Describe the parts of a cuboid  Consider the diagram of 3D object below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-022.png]  5. Na…"
- `ch13-b019` [exercise_block] — placed in **excluded**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Exercise 13.4: Describe the properties of a cuboid
  - evidence quote: "### Exercise 13.4: Describe the properties of a cuboid"
- `ch13-b019-i01` [exercise_item] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cuboids (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Exercise 13.4: Describe the properties of a cuboid
  - evidence quote: "### Exercise 13.4: Describe the properties of a cuboid  1. Select a word from Column B that best fits the description in Column A. Write down only the number for the description in Column A, and the capital letter that…"
- `ch13-b019-i02` [exercise_item] — placed in **AO:basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cuboids (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.1 Cubes and cuboids > Exercise 13.4: Describe the properties of a cuboid
  - evidence quote: "### Exercise 13.4: Describe the properties of a cuboid  2. Complete the table given below.  **Properties of a cuboid**  | Number and shape of faces | Number of edges | Number of vertices |  | --- | --- | --- |  |  |  |…"
- `ch13-b047` [exercise_block] — placed in **excluded**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres > Exercise 13.12: Describe the properties of 3D objects
  - evidence quote: "### Exercise 13.12: Describe the properties of 3D objects"
- `ch13-b047-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres > Exercise 13.12: Describe the properties of 3D objects
  - evidence quote: "### Exercise 13.12: Describe the properties of 3D objects  1. Identify each of the 3D objects labelled A to F shown in the diagram."
- `ch13-b047-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres > Exercise 13.12: Describe the properties of 3D objects
  - evidence quote: "### Exercise 13.12: Describe the properties of 3D objects  2. Consider the following 3D objects: cube, cuboid, pyramid, cone, cylinder and sphere. Write the name of each of the 3D objects in the correct column of the ta…"
- `ch13-b047-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres > Exercise 13.12: Describe the properties of 3D objects
  - evidence quote: "### Exercise 13.12: Describe the properties of 3D objects  3. Select a word from Column B that best fits the description in Column A.  | Column A | Column B | | --- | --- | | a) A 3D object with no edges and no vertices…"
- `ch13-b047-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres > Exercise 13.12: Describe the properties of 3D objects
  - evidence quote: "### Exercise 13.12: Describe the properties of 3D objects  4. Complete the table below.  | Name of 3D object | Number of faces | Number of edges | Number or vertices | | --- | --- | --- | --- | | cube |  |  |  | | cuboi…"
- `ch13-b053` [summary] — placed in **excluded**
  - heading: Chapter 13: Three-dimensional objects > 13.7 Summary
  - evidence quote: "A three-dimensional (3D) object has three dimensions that we can measure: length, breadth (or width), and height.  We use the main parts of a 3D object to describe its properties: - A 3D object has faces. The faces can…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch13-b047-i01..i04 are mixed 3D-object property items that may target a cube, cuboid, pyramid, cone, cylinder, or sphere; direction is not unambiguous.
- **no_reused_assessment**: Both cube and cuboid AOs have direct exercises but no reused assessment.

### Per-atomic-objective evidence classification
- `basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cubes` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch13-b005(instruction), ch13-b006(foundation), ch13-b007(instruction), ch13-b008(worked_example), ch13-b009(worked_example), ch13-b010-i01(exercise), ch13-b010-i02(exercise), ch13-b010-i03(exercise), ch13-b010-i04(exercise), ch13-b010-i05(exercise), ch13-b011-i01(exercise), ch13-b011-i02(exercise)
  - assessment: _(none anchored)_
- `basic-properties-of-cubes-and-cuboids-ao-identify-properties-of-cuboids` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch13-b012(instruction), ch13-b013(foundation), ch13-b014(foundation), ch13-b015(instruction), ch13-b016(worked_example), ch13-b017(worked_example), ch13-b018-i01(exercise), ch13-b018-i02(exercise), ch13-b018-i03(exercise), ch13-b018-i04(exercise), ch13-b018-i05(exercise), ch13-b019-i01(exercise), ch13-b019-i02(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones`

**Title:** Basic properties of pyramids and cones.  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-three-dimensional-figures-basic-properties-of-pyramids-and-cones-po01`: Identify the properties of pyramids and cones

### Atomic objectives
- `basic-properties-of-pyramids-and-cones-ao-identify-properties-of-pyramids` [identify/remember]: Identify the properties of pyramids.
- `basic-properties-of-pyramids-and-cones-ao-identify-properties-of-cones` [identify/remember]: Identify the properties of cones.

### Linked textbook records (37 total) — inspected
- `ch13-b020` [exposition] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-pyramids (instruction)**
  - heading: Chapter 13: Three-dimensional objects > 13.2 Pyramids
  - evidence quote: "A **pyramid** is an object that has a polygon as its base and sides that **converge** (meet each other) at one single point. The sides are *not* perpendicular to the base.  There are many real life objects in the form o…"
- `ch13-b021` [definition] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-pyramids (foundation)**
  - heading: Chapter 13: Three-dimensional objects > 13.2 Pyramids
  - evidence quote: "**pyramid** A pyramid is a 3D object that has a polygon as its base. The side faces are triangles that meet each other at one single point, the apex.  **converge** To converge is to move towards each other and to meet a…"
- `ch13-b022` [note] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-pyramids (foundation)**
  - heading: Chapter 13: Three-dimensional objects > 13.2 Pyramids
  - evidence quote: "A pyramid is NOT a prism, because the side faces are not rectangles and the side faces are not perpendicular to the base."
- `ch13-b023` [worked_example] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-pyramids (worked_example)**
  - heading: Chapter 13: Three-dimensional objects > 13.2 Pyramids > Worked example 13.5: Describing the parts of a pyramid
  - evidence quote: "Consider the square-based pyramid given below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-033.png]  Question 1: What is the name of the shaded area la…"
- `ch13-b024` [exercise_block] — placed in **excluded**
  - heading: Chapter 13: Three-dimensional objects > 13.2 Pyramids > Exercise 13.5: Identify the parts of a pyramid
  - evidence quote: "### Exercise 13.5: Identify the parts of a pyramid  Consider the 3D object given below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-028.png]"
- `ch13-b024-i01` [exercise_item] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-pyramids (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.2 Pyramids > Exercise 13.5: Identify the parts of a pyramid
  - evidence quote: "### Exercise 13.5: Identify the parts of a pyramid  Consider the 3D object given below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-028.png]  1. What i…"
- `ch13-b024-i02` [exercise_item] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-pyramids (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.2 Pyramids > Exercise 13.5: Identify the parts of a pyramid
  - evidence quote: "### Exercise 13.5: Identify the parts of a pyramid  Consider the 3D object given below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-028.png]  2. How ma…"
- `ch13-b024-i03` [exercise_item] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-pyramids (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.2 Pyramids > Exercise 13.5: Identify the parts of a pyramid
  - evidence quote: "### Exercise 13.5: Identify the parts of a pyramid  Consider the 3D object given below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-028.png]  3. What a…"
- `ch13-b024-i04` [exercise_item] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-pyramids (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.2 Pyramids > Exercise 13.5: Identify the parts of a pyramid
  - evidence quote: "### Exercise 13.5: Identify the parts of a pyramid  Consider the 3D object given below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-028.png]  4. How ma…"
- `ch13-b024-i05` [exercise_item] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-pyramids (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.2 Pyramids > Exercise 13.5: Identify the parts of a pyramid
  - evidence quote: "### Exercise 13.5: Identify the parts of a pyramid  Consider the 3D object given below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-028.png]  5. How ma…"
- `ch13-b024-i06` [exercise_item] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-pyramids (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.2 Pyramids > Exercise 13.5: Identify the parts of a pyramid
  - evidence quote: "### Exercise 13.5: Identify the parts of a pyramid  Consider the 3D object given below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-028.png]  6. What i…"
- `ch13-b025` [exercise_block] — placed in **excluded**
  - heading: Chapter 13: Three-dimensional objects > 13.2 Pyramids > Exercise 13.6: Describe the properties of a pyramid
  - evidence quote: "### Exercise 13.6: Describe the properties of a pyramid"
- `ch13-b025-i01` [exercise_item] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-pyramids (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.2 Pyramids > Exercise 13.6: Describe the properties of a pyramid
  - evidence quote: "### Exercise 13.6: Describe the properties of a pyramid  1. Select a word from Column B that best fits the description in Column A.  | Column A | Column B |  | --- | --- |  | a) The base and triangles that form the flat…"
- `ch13-b025-i02` [exercise_item] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-pyramids (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.2 Pyramids > Exercise 13.6: Describe the properties of a pyramid
  - evidence quote: "### Exercise 13.6: Describe the properties of a pyramid  2. Complete the table given below.  **Properties of a square-based pyramid**  | Number and shape of faces | Number of edges | Number of vertices |  | --- | --- |…"
- `ch13-b026` [exposition] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-cones (instruction)**
  - heading: Chapter 13: Three-dimensional objects > 13.3 Cones
  - evidence quote: "A **cone** is another example of a 3D object that has an apex.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-035.png]  There are many examples of cones i…"
- `ch13-b027` [note] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-cones (foundation)**
  - heading: Chapter 13: Three-dimensional objects > 13.3 Cones
  - evidence quote: "The round ball of ice cream that you eat is a sphere. You will study the properties of a sphere later in this chapter."
- `ch13-b028` [exposition] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-cones (instruction)**
  - heading: Chapter 13: Three-dimensional objects > 13.3 Cones
  - evidence quote: "We can make a party hat in the form of a cone.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-037.png]  The roof of a house can be in the form of a cone.…"
- `ch13-b029` [note] — placed in **excluded**
  - heading: Chapter 13: Three-dimensional objects > 13.3 Cones
  - evidence quote: "The circular walls of the round houses are cylinders. You will study the properties of a cylinder later in this chapter."
- `ch13-b030` [exposition] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-cones (instruction)**
  - heading: Chapter 13: Three-dimensional objects > 13.3 Cones
  - evidence quote: "The properties of a cone are:  - A cone has two *faces*. One of the faces is flat and the other face is curved. - The *base* of a cone is a flat circle. - [Source image: https://electricbookworks.github.io/siyavula-open…"
- `ch13-b031` [definition] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-cones (foundation)**
  - heading: Chapter 13: Three-dimensional objects > 13.3 Cones
  - evidence quote: "**cone** A cone is a 3D object with a circle as its base. A cone has one curved side face that comes to a point, the apex."
- `ch13-b032` [note] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-cones (foundation)**
  - heading: Chapter 13: Three-dimensional objects > 13.3 Cones
  - evidence quote: "A cone is NOT a prism: a cone has a circle as its base, and a circle is not a polygon. A prism has a polygon as a base."
- `ch13-b033` [worked_example] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-cones (worked_example)**
  - heading: Chapter 13: Three-dimensional objects > 13.3 Cones > Worked example 13.6: Identifying the parts of a cone
  - evidence quote: "Consider the diagram of the cone given below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-13-043.png]  1. What is the name of the shaded area labelled $X$…"
- `ch13-b034` [exercise_block] — placed in **excluded**
  - heading: Chapter 13: Three-dimensional objects > 13.3 Cones > Exercise 13.7: Describe the parts of a cone
  - evidence quote: "### Exercise 13.7: Describe the parts of a cone  Consider the diagram of a cone given below. The diagram labels the base with $X$ and the apex with $Y$."
- `ch13-b034-i01` [exercise_item] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-cones (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.3 Cones > Exercise 13.7: Describe the parts of a cone
  - evidence quote: "### Exercise 13.7: Describe the parts of a cone  Consider the diagram of a cone given below. The diagram labels the base with $X$ and the apex with $Y$.  1. What is the name of the 3D object?"
- `ch13-b034-i02` [exercise_item] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-cones (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.3 Cones > Exercise 13.7: Describe the parts of a cone
  - evidence quote: "### Exercise 13.7: Describe the parts of a cone  Consider the diagram of a cone given below. The diagram labels the base with $X$ and the apex with $Y$.  2. What letter on the diagram shows the base of the object?"
- `ch13-b034-i03` [exercise_item] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-cones (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.3 Cones > Exercise 13.7: Describe the parts of a cone
  - evidence quote: "### Exercise 13.7: Describe the parts of a cone  Consider the diagram of a cone given below. The diagram labels the base with $X$ and the apex with $Y$.  3. What shape is the base of the object?"
- `ch13-b034-i04` [exercise_item] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-cones (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.3 Cones > Exercise 13.7: Describe the parts of a cone
  - evidence quote: "### Exercise 13.7: Describe the parts of a cone  Consider the diagram of a cone given below. The diagram labels the base with $X$ and the apex with $Y$.  4. What is the name of the point labelled $Y$?"
- `ch13-b034-i05` [exercise_item] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-cones (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.3 Cones > Exercise 13.7: Describe the parts of a cone
  - evidence quote: "### Exercise 13.7: Describe the parts of a cone  Consider the diagram of a cone given below. The diagram labels the base with $X$ and the apex with $Y$.  5. Why is the edge of a cone not a straight line but a curve?"
- `ch13-b035` [exercise_block] — placed in **excluded**
  - heading: Chapter 13: Three-dimensional objects > 13.3 Cones > Exercise 13.8: Describe the properties of a cone
  - evidence quote: "### Exercise 13.8: Describe the properties of a cone"
- `ch13-b035-i01` [exercise_item] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-cones (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.3 Cones > Exercise 13.8: Describe the properties of a cone
  - evidence quote: "### Exercise 13.8: Describe the properties of a cone  1. Select a word from Column B that best fits the description in Column A.  | Column A | Column B | | --- | --- | | a) The flat circle that forms part of a cone. | A…"
- `ch13-b035-i02` [exercise_item] — placed in **AO:basic-properties-of-pyramids-and-cones-ao-identify-properties-of-cones (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.3 Cones > Exercise 13.8: Describe the properties of a cone
  - evidence quote: "### Exercise 13.8: Describe the properties of a cone  2. Complete the following table.  **Properties of a cone**  | Number and shape of faces | Number of edges | Number of vertices | | --- | --- | --- | |  |  |  |"
- `ch13-b047` [exercise_block] — placed in **excluded**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres > Exercise 13.12: Describe the properties of 3D objects
  - evidence quote: "### Exercise 13.12: Describe the properties of 3D objects"
- `ch13-b047-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres > Exercise 13.12: Describe the properties of 3D objects
  - evidence quote: "### Exercise 13.12: Describe the properties of 3D objects  1. Identify each of the 3D objects labelled A to F shown in the diagram."
- `ch13-b047-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres > Exercise 13.12: Describe the properties of 3D objects
  - evidence quote: "### Exercise 13.12: Describe the properties of 3D objects  2. Consider the following 3D objects: cube, cuboid, pyramid, cone, cylinder and sphere. Write the name of each of the 3D objects in the correct column of the ta…"
- `ch13-b047-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres > Exercise 13.12: Describe the properties of 3D objects
  - evidence quote: "### Exercise 13.12: Describe the properties of 3D objects  3. Select a word from Column B that best fits the description in Column A.  | Column A | Column B | | --- | --- | | a) A 3D object with no edges and no vertices…"
- `ch13-b047-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres > Exercise 13.12: Describe the properties of 3D objects
  - evidence quote: "### Exercise 13.12: Describe the properties of 3D objects  4. Complete the table below.  | Name of 3D object | Number of faces | Number of edges | Number or vertices | | --- | --- | --- | --- | | cube |  |  |  | | cuboi…"
- `ch13-b053` [summary] — placed in **excluded**
  - heading: Chapter 13: Three-dimensional objects > 13.7 Summary
  - evidence quote: "A three-dimensional (3D) object has three dimensions that we can measure: length, breadth (or width), and height.  We use the main parts of a 3D object to describe its properties: - A 3D object has faces. The faces can…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch13-b047-i01..i04 are mixed 3D-object property items whose direction (pyramid, cone, or other shape) is not unambiguous.
- **no_reused_assessment**: Both AOs have direct exercises but no reused assessment.

### Per-atomic-objective evidence classification
- `basic-properties-of-pyramids-and-cones-ao-identify-properties-of-pyramids` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch13-b020(instruction), ch13-b021(foundation), ch13-b022(foundation), ch13-b023(worked_example), ch13-b024-i01(exercise), ch13-b024-i02(exercise), ch13-b024-i03(exercise), ch13-b024-i04(exercise), ch13-b024-i05(exercise), ch13-b024-i06(exercise), ch13-b025-i01(exercise), ch13-b025-i02(exercise)
  - assessment: _(none anchored)_
- `basic-properties-of-pyramids-and-cones-ao-identify-properties-of-cones` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch13-b026(instruction), ch13-b027(foundation), ch13-b028(instruction), ch13-b030(instruction), ch13-b031(foundation), ch13-b032(foundation), ch13-b033(worked_example), ch13-b034-i01(exercise), ch13-b034-i02(exercise), ch13-b034-i03(exercise), ch13-b034-i04(exercise), ch13-b034-i05(exercise), ch13-b035-i01(exercise), ch13-b035-i02(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-three-dimensional-figures-basic-properties-of-cylinders-and-spheres`

**Title:** Basic properties of cylinders and spheres.  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-three-dimensional-figures-basic-properties-of-cylinders-and-spheres-po01`: Identify the properties of cylinders and spheres

### Atomic objectives
- `basic-properties-of-cylinders-and-spheres-ao-identify-properties-of-cylinders` [identify/remember]: Identify the properties of cylinders.
- `basic-properties-of-cylinders-and-spheres-ao-identify-properties-of-spheres` [identify/remember]: Identify the properties of spheres.

### Linked textbook records (27 total) — inspected
- `ch13-b036` [exposition] — placed in **AO:basic-properties-of-cylinders-and-spheres-ao-identify-properties-of-cylinders (instruction)**
  - heading: Chapter 13: Three-dimensional objects > 13.4 Cylinders
  - evidence quote: "In a **cylinder**, both the top and bottom faces are circles. The top and bottom faces are joined by a curved surface that is perpendicular to the base.  There are many real life objects in the form of a cylinder. Paint…"
- `ch13-b037` [definition] — placed in **AO:basic-properties-of-cylinders-and-spheres-ao-identify-properties-of-cylinders (foundation)**
  - heading: Chapter 13: Three-dimensional objects > 13.4 Cylinders
  - evidence quote: "**cylinder** A cylinder is a 3D object with two equal circles as the base and the top face. A cylinder has one curved side face that is perpendicular to the two circles."
- `ch13-b038` [note] — placed in **AO:basic-properties-of-cylinders-and-spheres-ao-identify-properties-of-cylinders (foundation)**
  - heading: Chapter 13: Three-dimensional objects > 13.4 Cylinders
  - evidence quote: "A cylinder does not have a vertex. A cylinder is NOT a prism: a prism has a circle as its base and a circle is not a polygon."
- `ch13-b039` [worked_example] — placed in **AO:basic-properties-of-cylinders-and-spheres-ao-identify-properties-of-cylinders (worked_example)**
  - heading: Chapter 13: Three-dimensional objects > 13.4 Cylinders > Worked example 13.7: Identifying the parts of a cylinder
  - evidence quote: "Consider the diagram of a cylinder given below. The diagram labels parts $D$, $E$, and $F$.  Question 1: What part of the cylinder is shaded and labelled $D$?  Question 2: What part of the cylinder is shown by the circl…"
- `ch13-b040` [exercise_block] — placed in **excluded**
  - heading: Chapter 13: Three-dimensional objects > 13.4 Cylinders > Exercise 13.9: Identify the parts of a cylinder
  - evidence quote: "### Exercise 13.9: Identify the parts of a cylinder  Consider the 3D object shown below. The diagram labels parts $D$, $E$, and $F$ on the cylinder."
- `ch13-b040-i01` [exercise_item] — placed in **AO:basic-properties-of-cylinders-and-spheres-ao-identify-properties-of-cylinders (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.4 Cylinders > Exercise 13.9: Identify the parts of a cylinder
  - evidence quote: "### Exercise 13.9: Identify the parts of a cylinder  Consider the 3D object shown below. The diagram labels parts $D$, $E$, and $F$ on the cylinder.  1. What is the name of the 3D object?"
- `ch13-b040-i02` [exercise_item] — placed in **AO:basic-properties-of-cylinders-and-spheres-ao-identify-properties-of-cylinders (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.4 Cylinders > Exercise 13.9: Identify the parts of a cylinder
  - evidence quote: "### Exercise 13.9: Identify the parts of a cylinder  Consider the 3D object shown below. The diagram labels parts $D$, $E$, and $F$ on the cylinder.  2. What is the shaded area labelled $D$ called?"
- `ch13-b040-i03` [exercise_item] — placed in **AO:basic-properties-of-cylinders-and-spheres-ao-identify-properties-of-cylinders (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.4 Cylinders > Exercise 13.9: Identify the parts of a cylinder
  - evidence quote: "### Exercise 13.9: Identify the parts of a cylinder  Consider the 3D object shown below. The diagram labels parts $D$, $E$, and $F$ on the cylinder.  3. What is the shape of the area labelled $D$?"
- `ch13-b040-i04` [exercise_item] — placed in **AO:basic-properties-of-cylinders-and-spheres-ao-identify-properties-of-cylinders (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.4 Cylinders > Exercise 13.9: Identify the parts of a cylinder
  - evidence quote: "### Exercise 13.9: Identify the parts of a cylinder  Consider the 3D object shown below. The diagram labels parts $D$, $E$, and $F$ on the cylinder.  4. What letter on the diagram shows an edge of the cylinder?"
- `ch13-b040-i05` [exercise_item] — placed in **AO:basic-properties-of-cylinders-and-spheres-ao-identify-properties-of-cylinders (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.4 Cylinders > Exercise 13.9: Identify the parts of a cylinder
  - evidence quote: "### Exercise 13.9: Identify the parts of a cylinder  Consider the 3D object shown below. The diagram labels parts $D$, $E$, and $F$ on the cylinder.  5. Why does the letter $E$ show a curve and not a straight line?"
- `ch13-b040-i06` [exercise_item] — placed in **AO:basic-properties-of-cylinders-and-spheres-ao-identify-properties-of-cylinders (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.4 Cylinders > Exercise 13.9: Identify the parts of a cylinder
  - evidence quote: "### Exercise 13.9: Identify the parts of a cylinder  Consider the 3D object shown below. The diagram labels parts $D$, $E$, and $F$ on the cylinder.  6. What part of the cylinder is labelled $F$?"
- `ch13-b041` [exercise_block] — placed in **excluded**
  - heading: Chapter 13: Three-dimensional objects > 13.4 Cylinders > Exercise 13.10: Describe the properties of a cylinder
  - evidence quote: "### Exercise 13.10: Describe the properties of a cylinder"
- `ch13-b041-i01` [exercise_item] — placed in **AO:basic-properties-of-cylinders-and-spheres-ao-identify-properties-of-cylinders (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.4 Cylinders > Exercise 13.10: Describe the properties of a cylinder
  - evidence quote: "### Exercise 13.10: Describe the properties of a cylinder  1. Select a word from Column B that best fits the description in Column A:  | Column A | Column B | | --- | --- | | a) The flat circle at the bottom of a cylind…"
- `ch13-b041-i02` [exercise_item] — placed in **AO:basic-properties-of-cylinders-and-spheres-ao-identify-properties-of-cylinders (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.4 Cylinders > Exercise 13.10: Describe the properties of a cylinder
  - evidence quote: "### Exercise 13.10: Describe the properties of a cylinder  2. Complete the following table.  **Properties of a cylinder**  | Number and shape of faces | Number of edges | Number of vertices | | --- | --- | --- | |  |  |…"
- `ch13-b042` [exposition] — placed in **AO:basic-properties-of-cylinders-and-spheres-ao-identify-properties-of-spheres (instruction)**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres
  - evidence quote: "**Spheres** are solids that are perfectly round and look the same from any direction.  There are many real life objects in the shape of a sphere.  A football is a sphere.  Many children all over the world play with glas…"
- `ch13-b043` [definition] — placed in **AO:basic-properties-of-cylinders-and-spheres-ao-identify-properties-of-spheres (foundation)**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres
  - evidence quote: "**sphere** A sphere is a 3D object consisting of one curved face."
- `ch13-b044` [note] — placed in **AO:basic-properties-of-cylinders-and-spheres-ao-identify-properties-of-spheres (foundation)**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres
  - evidence quote: "A sphere has no edges, and no vertices. A sphere has no flat faces. This means that a sphere is not a prism, as a prism has only flat faces."
- `ch13-b045` [worked_example] — placed in **AO:basic-properties-of-cylinders-and-spheres-ao-identify-properties-of-spheres (worked_example)**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres > Worked example 13.8: Identifying the parts of a sphere
  - evidence quote: "Consider the diagram of a sphere given below.  1. How many faces does a sphere have? 2. Is the face of the sphere flat or curved? 3. State whether the following statement is true or false: A sphere has one edge and no v…"
- `ch13-b046` [exercise_block] — placed in **excluded**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres > Exercise 13.11: Identify the parts of a sphere
  - evidence quote: "### Exercise 13.11: Identify the parts of a sphere  Consider the 3D object shown below."
- `ch13-b046-i01` [exercise_item] — placed in **AO:basic-properties-of-cylinders-and-spheres-ao-identify-properties-of-spheres (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres > Exercise 13.11: Identify the parts of a sphere
  - evidence quote: "### Exercise 13.11: Identify the parts of a sphere  Consider the 3D object shown below.  1. Identify the type of 3D object."
- `ch13-b046-i02` [exercise_item] — placed in **AO:basic-properties-of-cylinders-and-spheres-ao-identify-properties-of-spheres (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres > Exercise 13.11: Identify the parts of a sphere
  - evidence quote: "### Exercise 13.11: Identify the parts of a sphere  Consider the 3D object shown below.  2. Describe the properties of the object."
- `ch13-b047` [exercise_block] — placed in **excluded**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres > Exercise 13.12: Describe the properties of 3D objects
  - evidence quote: "### Exercise 13.12: Describe the properties of 3D objects"
- `ch13-b047-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres > Exercise 13.12: Describe the properties of 3D objects
  - evidence quote: "### Exercise 13.12: Describe the properties of 3D objects  1. Identify each of the 3D objects labelled A to F shown in the diagram."
- `ch13-b047-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres > Exercise 13.12: Describe the properties of 3D objects
  - evidence quote: "### Exercise 13.12: Describe the properties of 3D objects  2. Consider the following 3D objects: cube, cuboid, pyramid, cone, cylinder and sphere. Write the name of each of the 3D objects in the correct column of the ta…"
- `ch13-b047-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres > Exercise 13.12: Describe the properties of 3D objects
  - evidence quote: "### Exercise 13.12: Describe the properties of 3D objects  3. Select a word from Column B that best fits the description in Column A.  | Column A | Column B | | --- | --- | | a) A 3D object with no edges and no vertices…"
- `ch13-b047-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 13: Three-dimensional objects > 13.5 Spheres > Exercise 13.12: Describe the properties of 3D objects
  - evidence quote: "### Exercise 13.12: Describe the properties of 3D objects  4. Complete the table below.  | Name of 3D object | Number of faces | Number of edges | Number or vertices | | --- | --- | --- | --- | | cube |  |  |  | | cuboi…"
- `ch13-b053` [summary] — placed in **excluded**
  - heading: Chapter 13: Three-dimensional objects > 13.7 Summary
  - evidence quote: "A three-dimensional (3D) object has three dimensions that we can measure: length, breadth (or width), and height.  We use the main parts of a 3D object to describe its properties: - A 3D object has faces. The faces can…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch13-b047-i01..i04 are mixed 3D-object property items whose direction (cylinder, sphere, or other shape) is not unambiguous.
- **no_reused_assessment**: Both AOs have direct exercises but no reused assessment.

### Per-atomic-objective evidence classification
- `basic-properties-of-cylinders-and-spheres-ao-identify-properties-of-cylinders` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch13-b036(instruction), ch13-b037(foundation), ch13-b038(foundation), ch13-b039(worked_example), ch13-b040-i01(exercise), ch13-b040-i02(exercise), ch13-b040-i03(exercise), ch13-b040-i04(exercise), ch13-b040-i05(exercise), ch13-b040-i06(exercise), ch13-b041-i01(exercise), ch13-b041-i02(exercise)
  - assessment: _(none anchored)_
- `basic-properties-of-cylinders-and-spheres-ao-identify-properties-of-spheres` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch13-b042(instruction), ch13-b043(foundation), ch13-b044(foundation), ch13-b045(worked_example), ch13-b046-i01(exercise), ch13-b046-i02(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids`

**Title:** Volume of cubes and cuboids  
**Status:** `needs_review`  
**Row review categories:** no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-three-dimensional-figures-volume-of-cubes-and-cuboids-po01`: Find volume of a cube and a cuboid

### Atomic objectives
- `volume-of-cubes-and-cuboids-ao-find-volume-of-cube` [find/apply]: Find volume of a cube.
- `volume-of-cubes-and-cuboids-ao-find-volume-of-cuboid` [find/apply]: Find volume of a cuboid.

### Linked textbook records (12 total) — inspected
- `ch13-b048` [exposition] — placed in **shared_foundation**
  - heading: Chapter 13: Three-dimensional objects > 13.6 Volume of cubes and cuboids
  - evidence quote: "Volume is the amount of the space that a 3D object takes up. Volume is a way of measuring the size of a whole 3D object. It is measured in cubic units.  When we measure *length*, we measure one dimension. The length of…"
- `ch13-b049` [worked_example] — placed in **AO:volume-of-cubes-and-cuboids-ao-find-volume-of-cube (worked_example)**
  - heading: Chapter 13: Three-dimensional objects > 13.6 Volume of cubes and cuboids > Worked example 13.9: Calculating the volume of a cube
  - evidence quote: "Find the volume of the following cube. The cube has side length 3 cm."
- `ch13-b050` [worked_example] — placed in **AO:volume-of-cubes-and-cuboids-ao-find-volume-of-cuboid (worked_example)**
  - heading: Chapter 13: Three-dimensional objects > 13.6 Volume of cubes and cuboids > Worked example 13.10: Calculating the volume of a cuboid
  - evidence quote: "The 3D object shown below is a cuboid. The height of the cuboid is 12 cm, the length is 13 cm, and the breadth is 6 cm. Calculate the volume of the object.  The diagram is not necessarily drawn to scale."
- `ch13-b051` [exposition] — placed in **shared_foundation**
  - heading: Chapter 13: Three-dimensional objects > 13.6 Volume of cubes and cuboids
  - evidence quote: "You may calculate the volume of a prism in one step, using these formulae.  $$ \begin{align} \text{Volume of a cuboid} &= \text{area of base} \times \text{height of cuboid}\\ &= l \times b \times h \end{align} $$  $$ \b…"
- `ch13-b052` [exercise_block] — placed in **excluded**
  - heading: Chapter 13: Three-dimensional objects > 13.6 Volume of cubes and cuboids > Exercise 13.13: Find the volume of cubes and cuboids
  - evidence quote: "### Exercise 13.13: Find the volume of cubes and cuboids"
- `ch13-b052-i01` [exercise_item] — placed in **AO:volume-of-cubes-and-cuboids-ao-find-volume-of-cube (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.6 Volume of cubes and cuboids > Exercise 13.13: Find the volume of cubes and cuboids
  - evidence quote: "### Exercise 13.13: Find the volume of cubes and cuboids  1. The picture below shows a cube. The length, width and height of the cube are 5 cm. Find the volume of the cube."
- `ch13-b052-i02` [exercise_item] — placed in **AO:volume-of-cubes-and-cuboids-ao-find-volume-of-cube (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.6 Volume of cubes and cuboids > Exercise 13.13: Find the volume of cubes and cuboids
  - evidence quote: "### Exercise 13.13: Find the volume of cubes and cuboids  2. The picture below shows a cube. The length, width and height of the cube are 30 mm. Find the volume of the cube."
- `ch13-b052-i03` [exercise_item] — placed in **AO:volume-of-cubes-and-cuboids-ao-find-volume-of-cuboid (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.6 Volume of cubes and cuboids > Exercise 13.13: Find the volume of cubes and cuboids
  - evidence quote: "### Exercise 13.13: Find the volume of cubes and cuboids  3. The prism shown below is a cuboid. The height of the cuboid is 6 metres, the length is 12 metres and the breadth is 5 metres. Find the volume of the prism."
- `ch13-b052-i04` [exercise_item] — placed in **AO:volume-of-cubes-and-cuboids-ao-find-volume-of-cuboid (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.6 Volume of cubes and cuboids > Exercise 13.13: Find the volume of cubes and cuboids
  - evidence quote: "### Exercise 13.13: Find the volume of cubes and cuboids  4. The prism shown below is a cuboid. The height of the cuboid is 8 cm; the length and breadth are 10 cm and 4 cm respectively. Determine the volume of the cuboi…"
- `ch13-b052-i05` [exercise_item] — placed in **AO:volume-of-cubes-and-cuboids-ao-find-volume-of-cube (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.6 Volume of cubes and cuboids > Exercise 13.13: Find the volume of cubes and cuboids
  - evidence quote: "### Exercise 13.13: Find the volume of cubes and cuboids  5. The picture below shows a cube. The length, width and height of the cube are 4 metres. Find the volume of the cube."
- `ch13-b052-i06` [exercise_item] — placed in **AO:volume-of-cubes-and-cuboids-ao-find-volume-of-cuboid (exercise)**
  - heading: Chapter 13: Three-dimensional objects > 13.6 Volume of cubes and cuboids > Exercise 13.13: Find the volume of cubes and cuboids
  - evidence quote: "### Exercise 13.13: Find the volume of cubes and cuboids  6. The prism below is a cuboid. The height of the cuboid is 12 mm, and the other dimensions of the cuboid are 11 mm and 8 mm. Find the volume of the cuboid."
- `ch13-b053` [summary] — placed in **excluded**
  - heading: Chapter 13: Three-dimensional objects > 13.7 Summary
  - evidence quote: "A three-dimensional (3D) object has three dimensions that we can measure: length, breadth (or width), and height.  We use the main parts of a 3D object to describe its properties: - A 3D object has faces. The faces can…"

### Row-level review categories and manually authored reasons
- **no_reused_assessment**: Both AOs (volume of cube, volume of cuboid) have direct worked examples and exercises but no reused exercise_item assessment was selected.

### Per-atomic-objective evidence classification
- `volume-of-cubes-and-cuboids-ao-find-volume-of-cube` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch13-b049(worked_example), ch13-b052-i01(exercise), ch13-b052-i02(exercise), ch13-b052-i05(exercise)
  - assessment: _(none anchored)_
- `volume-of-cubes-and-cuboids-ao-find-volume-of-cuboid` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch13-b050(worked_example), ch13-b052-i03(exercise), ch13-b052-i04(exercise), ch13-b052-i06(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-construction-construction-of-parallel-and-perpendicular-lines`

**Title:** Construction of parallel and perpendicular lines.  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-construction-construction-of-parallel-and-perpendicular-lines-po01`: Construct parallel and perpendicular lines

### Atomic objectives
- `construction-of-parallel-and-perpendicular-lines-ao-construct-parallel-lines` [construct/apply]: Construct parallel lines.
- `construction-of-parallel-and-perpendicular-lines-ao-construct-perpendicular-lines` [construct/apply]: Construct perpendicular lines.

### Linked textbook records (37 total) — inspected
- `ch14-b001` [exposition] — placed in **shared_foundation**
  - heading: Chapter 14: Constructions
  - evidence quote: "A construction in Mathematics is an accurate drawing of angles and lines. You are only allowed to use a straightedge and a pair of compasses with a pencil in it when you do constructions.  1. A straightedge  A straighte…"
- `ch14-b002` [hint] — placed in **excluded**
  - heading: Chapter 14: Constructions
  - evidence quote: "The two legs of the compass are joined at the hinge. Make sure that the metal pin at the hinge is fitted tightly so that the two legs of the compass will not open too easily. Also make sure that your pencil is sharpened…"
- `ch14-b003` [hint] — placed in **excluded**
  - heading: Chapter 14: Constructions
  - evidence quote: "Do not confuse the compass that we use in mathematical constructions with the compass that we use to find direction."
- `ch14-b004` [exposition] — placed in **shared_foundation**
  - heading: Chapter 14: Constructions
  - evidence quote: "All the constructions in this chapter are based on the properties of a circle.  In the diagram below, $BC$ is the diameter of the circle. $A$ is the centre of the circle. This means that $AB$ is a radius of the circle a…"
- `ch14-b005` [definition] — placed in **shared_foundation**
  - heading: Chapter 14: Constructions
  - evidence quote: "**arc** An arc is a part of the circumference of a circle."
- `ch14-b006` [exposition] — placed in **AO:construction-of-parallel-and-perpendicular-lines-ao-construct-perpendicular-lines (instruction)**
  - heading: Chapter 14: Constructions > 14.1 Perpendicular lines
  - evidence quote: "Lines that are perpendicular **intersect** each other at right angles (at $90^{\circ}$). When we are asked to construct a **perpendicular line**, we will be given one of the lines, as well as a point. We then have to co…"
- `ch14-b007` [definition] — placed in **AO:construction-of-parallel-and-perpendicular-lines-ao-construct-perpendicular-lines (foundation)**
  - heading: Chapter 14: Constructions > 14.1 Perpendicular lines
  - evidence quote: "**intersect** When two lines intersect, they cross each other.  **perpendicular line** A perpendicular line cuts another line at a right angle."
- `ch14-b008` [exposition] — placed in **AO:construction-of-parallel-and-perpendicular-lines-ao-construct-perpendicular-lines (instruction)**
  - heading: Chapter 14: Constructions > 14.1 Perpendicular lines
  - evidence quote: "The point that is given can be on the line, or it can be a small distance away from the line.  In the first diagram, point $P$ is *on* line $AB$. In the second diagram, point $P$ is some distance *away* from line $AB$."
- `ch14-b009` [worked_example] — placed in **AO:construction-of-parallel-and-perpendicular-lines-ao-construct-perpendicular-lines (worked_example)**
  - heading: Chapter 14: Constructions > 14.1 Perpendicular lines > Worked example 14.1: Constructing a perpendicular line from a point on the line
  - evidence quote: "You are given line $AB$ with a point $P$ on the line.  Construct line $PQ$ so that $PQ$ is perpendicular to $AB$."
- `ch14-b010` [hint] — placed in **excluded**
  - heading: Chapter 14: Constructions > 14.1 Perpendicular lines
  - evidence quote: "When copying the lines in order to do constructions, the lines only need to be more or less the same length as given in the questions, and in more or less the same direction. It is a good idea to rotate your workbook if…"
- `ch14-b011` [exercise_block] — placed in **excluded**
  - heading: Chapter 14: Constructions > 14.1 Perpendicular lines > Exercise 14.1: Construct a perpendicular line from a point on the line
  - evidence quote: "### Exercise 14.1: Construct a perpendicular line from a point on the line"
- `ch14-b011-i01` [exercise_item] — placed in **AO:construction-of-parallel-and-perpendicular-lines-ao-construct-perpendicular-lines (exercise)**
  - heading: Chapter 14: Constructions > 14.1 Perpendicular lines > Exercise 14.1: Construct a perpendicular line from a point on the line
  - evidence quote: "### Exercise 14.1: Construct a perpendicular line from a point on the line  1. Draw line $CD$ as shown below. $P$ is a point on the line. Construct $PQ$ perpendicular to line $CD$. Remember to check your work."
- `ch14-b011-i02` [exercise_item] — placed in **AO:construction-of-parallel-and-perpendicular-lines-ao-construct-perpendicular-lines (exercise)**
  - heading: Chapter 14: Constructions > 14.1 Perpendicular lines > Exercise 14.1: Construct a perpendicular line from a point on the line
  - evidence quote: "### Exercise 14.1: Construct a perpendicular line from a point on the line  2. Draw line $EF$ as shown below. $P$ is a point on the line. Construct $PQ$ perpendicular to line $EF$. Remember to check your work."
- `ch14-b011-i03` [exercise_item] — placed in **AO:construction-of-parallel-and-perpendicular-lines-ao-construct-perpendicular-lines (exercise)**
  - heading: Chapter 14: Constructions > 14.1 Perpendicular lines > Exercise 14.1: Construct a perpendicular line from a point on the line
  - evidence quote: "### Exercise 14.1: Construct a perpendicular line from a point on the line  3. Draw line $MN$ as shown below. $P$ is a point on the line. Construct $PQ$ perpendicular to line $MN$. Remember to check your work."
- `ch14-b011-i04` [exercise_item] — placed in **AO:construction-of-parallel-and-perpendicular-lines-ao-construct-perpendicular-lines (exercise)**
  - heading: Chapter 14: Constructions > 14.1 Perpendicular lines > Exercise 14.1: Construct a perpendicular line from a point on the line
  - evidence quote: "### Exercise 14.1: Construct a perpendicular line from a point on the line  4. Draw line $ST$ as shown below. $P$ is a point on the line. Construct $PQ$ perpendicular to line $ST$. Remember to check your work."
- `ch14-b012` [worked_example] — placed in **AO:construction-of-parallel-and-perpendicular-lines-ao-construct-perpendicular-lines (worked_example)**
  - heading: Chapter 14: Constructions > 14.1 Perpendicular lines > Worked example 14.2: Constructing a perpendicular line from a point away from the line
  - evidence quote: "You are given line $AB$ with a point $P$ away from the line.  Construct line $PQ$ so that $PQ$ is perpendicular to $AB$."
- `ch14-b013` [hint] — placed in **excluded**
  - heading: Chapter 14: Constructions > 14.1 Perpendicular lines
  - evidence quote: "Remember to rotate your workbook if you need to, and not to erase your construction lines. Also, always check your work."
- `ch14-b014` [exercise_block] — placed in **excluded**
  - heading: Chapter 14: Constructions > 14.1 Perpendicular lines > Exercise 14.2: Construct a perpendicular line from a point away from the line
  - evidence quote: "### Exercise 14.2: Construct a perpendicular line from a point away from the line"
- `ch14-b014-i01` [exercise_item] — placed in **AO:construction-of-parallel-and-perpendicular-lines-ao-construct-perpendicular-lines (exercise)**
  - heading: Chapter 14: Constructions > 14.1 Perpendicular lines > Exercise 14.2: Construct a perpendicular line from a point away from the line
  - evidence quote: "### Exercise 14.2: Construct a perpendicular line from a point away from the line  1. Draw line $CD$ as shown below. Point $P$ is a point away from the line.  Source image: https://electricbookworks.github.io/siyavula-o…"
- `ch14-b014-i02` [exercise_item] — placed in **AO:construction-of-parallel-and-perpendicular-lines-ao-construct-perpendicular-lines (exercise)**
  - heading: Chapter 14: Constructions > 14.1 Perpendicular lines > Exercise 14.2: Construct a perpendicular line from a point away from the line
  - evidence quote: "### Exercise 14.2: Construct a perpendicular line from a point away from the line  2. Draw line $EF$ as shown below. Point $P$ is a point away from the line.  Source image: https://electricbookworks.github.io/siyavula-o…"
- `ch14-b014-i03` [exercise_item] — placed in **AO:construction-of-parallel-and-perpendicular-lines-ao-construct-perpendicular-lines (exercise)**
  - heading: Chapter 14: Constructions > 14.1 Perpendicular lines > Exercise 14.2: Construct a perpendicular line from a point away from the line
  - evidence quote: "### Exercise 14.2: Construct a perpendicular line from a point away from the line  3. Draw line $MN$ as shown below. Point $P$ is a point away from the line.  Source image: https://electricbookworks.github.io/siyavula-o…"
- `ch14-b014-i04` [exercise_item] — placed in **AO:construction-of-parallel-and-perpendicular-lines-ao-construct-perpendicular-lines (exercise)**
  - heading: Chapter 14: Constructions > 14.1 Perpendicular lines > Exercise 14.2: Construct a perpendicular line from a point away from the line
  - evidence quote: "### Exercise 14.2: Construct a perpendicular line from a point away from the line  4. Draw line $ST$ as shown below. Point $P$ is a point away from the line.  Source image: https://electricbookworks.github.io/siyavula-o…"
- `ch14-b015` [exposition] — placed in **AO:construction-of-parallel-and-perpendicular-lines-ao-construct-parallel-lines (instruction)**
  - heading: Chapter 14: Constructions > 14.2 Parallel lines
  - evidence quote: "**Parallel lines** are lines that are always the same distance apart from each other. They never meet or cross each other. When we are asked to construct parallel lines, we will be given a line and a point. We then have…"
- `ch14-b016` [definition] — placed in **AO:construction-of-parallel-and-perpendicular-lines-ao-construct-parallel-lines (foundation)**
  - heading: Chapter 14: Constructions > 14.2 Parallel lines
  - evidence quote: "**parallel lines** Parallel lines are lines that always remain the same distance apart, and never meet or cross each other."
- `ch14-b017` [exposition] — placed in **AO:construction-of-parallel-and-perpendicular-lines-ao-construct-parallel-lines (instruction)**
  - heading: Chapter 14: Constructions > 14.2 Parallel lines
  - evidence quote: "You will learn more about parallel lines in Chapter 15, but it will be easier to construct parallel lines if you know the following:  If two parallel lines are crossed by another line, then the angles marked in the diag…"
- `ch14-b018` [worked_example] — placed in **AO:construction-of-parallel-and-perpendicular-lines-ao-construct-parallel-lines (worked_example)**
  - heading: Chapter 14: Constructions > 14.2 Parallel lines > Worked example 14.3: Constructing parallel lines
  - evidence quote: "$P$ is a point away from line $AB$.  Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-038.png  Construct line $PQ$ through point $P$ so that $PQ$ is parallel…"
- `ch14-b019` [hint] — placed in **excluded**
  - heading: Chapter 14: Constructions > 14.2 Parallel lines
  - evidence quote: "Remember, you can rotate your workbook to make it easier to work with a line that is not horizontal. Do not erase your construction lines after you have completed a construction, and always check your work by measuring…"
- `ch14-b020` [exercise_block] — placed in **excluded**
  - heading: Chapter 14: Constructions > 14.2 Parallel lines > Exercise 14.3: Construct a parallel line
  - evidence quote: "### Exercise 14.3: Construct a parallel line"
- `ch14-b020-i01` [exercise_item] — placed in **AO:construction-of-parallel-and-perpendicular-lines-ao-construct-parallel-lines (exercise)**
  - heading: Chapter 14: Constructions > 14.2 Parallel lines > Exercise 14.3: Construct a parallel line
  - evidence quote: "### Exercise 14.3: Construct a parallel line  1. Draw line $CD$ as shown below. Point $P$ is a point away from the line.  Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web…"
- `ch14-b020-i02` [exercise_item] — placed in **AO:construction-of-parallel-and-perpendicular-lines-ao-construct-parallel-lines (exercise)**
  - heading: Chapter 14: Constructions > 14.2 Parallel lines > Exercise 14.3: Construct a parallel line
  - evidence quote: "### Exercise 14.3: Construct a parallel line  2. Draw line $EF$ as shown below. Point $P$ is a point away from the line.  Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web…"
- `ch14-b020-i03` [exercise_item] — placed in **AO:construction-of-parallel-and-perpendicular-lines-ao-construct-parallel-lines (exercise)**
  - heading: Chapter 14: Constructions > 14.2 Parallel lines > Exercise 14.3: Construct a parallel line
  - evidence quote: "### Exercise 14.3: Construct a parallel line  3. Draw line $MN$ as shown below. Point $P$ is a point away from the line.  Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web…"
- `ch14-b020-i04` [exercise_item] — placed in **AO:construction-of-parallel-and-perpendicular-lines-ao-construct-parallel-lines (exercise)**
  - heading: Chapter 14: Constructions > 14.2 Parallel lines > Exercise 14.3: Construct a parallel line
  - evidence quote: "### Exercise 14.3: Construct a parallel line  4. Draw line $ST$ as shown below. Point $P$ is a point away from the line.  Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web…"
- `ch14-b036` [summary] — placed in **excluded**
  - heading: Chapter 14: Constructions > 14.6 Summary
  - evidence quote: "- A construction in Mathematics is an accurate drawing of angles and lines. - You are only allowed to use a straightedge and a pair of compasses with a pencil in it when you do a construction. - You may use a ruler if y…"
- `ch15-b061` [exposition] — placed in **review_items**
  - heading: Chapter 15: Angles > 15.4 Practical applications
  - evidence quote: "When we know about different angles and how they are formed we can apply our knowledge in real life. For example, we can use angles to describe the position of a shop, or how we want to paint decorations. Many people us…"
- `ch15-b063` [exercise_block] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.4 Practical applications > Exercise 15.11: Solve real-world problems with angles
  - evidence quote: "### Exercise 15.11: Solve real-world problems with angles"
- `ch15-b063-i03a` [exercise_item] — placed in **review_items**
  - heading: Chapter 15: Angles > 15.4 Practical applications > Exercise 15.11: Solve real-world problems with angles
  - evidence quote: "### Exercise 15.11: Solve real-world problems with angles  3a. Babatunde and his brother earn income by doing welding jobs. They use their knowledge of angles and lines often in their work. The photo below shows the rai…"
- `ch15-b063-i03b` [exercise_item] — placed in **review_items**
  - heading: Chapter 15: Angles > 15.4 Practical applications > Exercise 15.11: Solve real-world problems with angles
  - evidence quote: "### Exercise 15.11: Solve real-world problems with angles  3b. In the same rail diagram, what is the relationship between the balusters marked $AC$ and $BD$?  Source image: https://electricbookworks.github.io/siyavula-o…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch15-b061 exposition and ch15-b063-i03a/i03b items are real-world angle problems from Chapter 15 that are not parallel/perpendicular construction exercises.
- **no_reused_assessment**: Both construction AOs have direct evidence but no reused assessment was selected.

### Per-atomic-objective evidence classification
- `construction-of-parallel-and-perpendicular-lines-ao-construct-parallel-lines` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch14-b015(instruction), ch14-b016(foundation), ch14-b017(instruction), ch14-b018(worked_example), ch14-b020-i01(exercise), ch14-b020-i02(exercise), ch14-b020-i03(exercise), ch14-b020-i04(exercise)
  - assessment: _(none anchored)_
- `construction-of-parallel-and-perpendicular-lines-ao-construct-perpendicular-lines` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch14-b006(instruction), ch14-b007(foundation), ch14-b008(instruction), ch14-b009(worked_example), ch14-b011-i01(exercise), ch14-b011-i02(exercise), ch14-b011-i03(exercise), ch14-b011-i04(exercise), ch14-b012(worked_example), ch14-b014-i01(exercise), ch14-b014-i02(exercise), ch14-b014-i03(exercise), ch14-b014-i04(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All review_items were inspected. Candidate proposal added for real-world angle/line problems because those records are not construction steps for parallel or perpendicular lines.

### Candidate atomic objective proposals
- `construction-parallel-perpendicular-candidate-ao-solve-real-world-angle-line-problems` [extension_or_enrichment; candidate_for_expert_review]
  - proposed objective: Solve real-world problems involving angles and lines.
  - source records: ch15-b061, ch15-b063-i03a, ch15-b063-i03b
  - closest existing AOs: construction-of-parallel-and-perpendicular-lines-ao-construct-parallel-lines, construction-of-parallel-and-perpendicular-lines-ao-construct-perpendicular-lines
  - candidate evidence quote: "apply our knowledge in real life."
  - rationale: The records use angle/line knowledge in applied welding and direction contexts rather than teaching geometric construction.

---

## `jss1-math-construction-bisection-of-a-given-line-segment`

**Title:** Bisection of a given line segment.  
**Status:** `mapped`  
**Row review categories:** _(none — mapped or no-records baseline)_

### Curriculum objectives (source)
- `jss1-math-construction-bisection-of-a-given-line-segment-po01`: Bisect a given line segment

### Atomic objectives
- `bisection-of-a-given-line-segment-ao-bisect-line-segment` [bisect/apply]: Bisect a given line segment.

### Linked textbook records (17 total) — inspected
- `ch14-b001` [exposition] — placed in **shared_foundation**
  - heading: Chapter 14: Constructions
  - evidence quote: "A construction in Mathematics is an accurate drawing of angles and lines. You are only allowed to use a straightedge and a pair of compasses with a pencil in it when you do constructions.  1. A straightedge  A straighte…"
- `ch14-b002` [hint] — placed in **excluded**
  - heading: Chapter 14: Constructions
  - evidence quote: "The two legs of the compass are joined at the hinge. Make sure that the metal pin at the hinge is fitted tightly so that the two legs of the compass will not open too easily. Also make sure that your pencil is sharpened…"
- `ch14-b003` [hint] — placed in **excluded**
  - heading: Chapter 14: Constructions
  - evidence quote: "Do not confuse the compass that we use in mathematical constructions with the compass that we use to find direction."
- `ch14-b004` [exposition] — placed in **shared_foundation**
  - heading: Chapter 14: Constructions
  - evidence quote: "All the constructions in this chapter are based on the properties of a circle.  In the diagram below, $BC$ is the diameter of the circle. $A$ is the centre of the circle. This means that $AB$ is a radius of the circle a…"
- `ch14-b005` [definition] — placed in **shared_foundation**
  - heading: Chapter 14: Constructions
  - evidence quote: "**arc** An arc is a part of the circumference of a circle."
- `ch14-b021` [exposition] — placed in **AO:bisection-of-a-given-line-segment-ao-bisect-line-segment (instruction)**
  - heading: Chapter 14: Constructions > 14.3 Line bisector
  - evidence quote: "A line segment is part of a straight line. A line segment has a beginning and an end. When we are asked to **bisect** a line segment, we are asked to divide the line segment into two equal parts.  The **bisector** is th…"
- `ch14-b022` [definition] — placed in **AO:bisection-of-a-given-line-segment-ao-bisect-line-segment (foundation)**
  - heading: Chapter 14: Constructions > 14.3 Line bisector
  - evidence quote: "**bisect** When we bisect a line segment or an angle, we divide the line segment or the angle exactly in half.  **bisector** A bisector is the line segment that divides the given line segment into two equal parts."
- `ch14-b023` [worked_example] — placed in **AO:bisection-of-a-given-line-segment-ao-bisect-line-segment (worked_example)**
  - heading: Chapter 14: Constructions > 14.3 Line bisector > Worked example 14.4: Bisecting a line segment
  - evidence quote: "You are given line segment $AB$ as shown in the diagram below.  Source image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-049.png  Bisect $AB$ and label the…"
- `ch14-b024` [exposition] — placed in **AO:bisection-of-a-given-line-segment-ao-bisect-line-segment (instruction)**
  - heading: Chapter 14: Constructions > 14.3 Line bisector
  - evidence quote: "Take note that if you measure the angles at $R$, you will find they are $90^{\circ}$. We say that the bisector is perpendicular to the original line segment. The symbol for perpendicular is $\perp$, so we write: $PQ \pe…"
- `ch14-b025` [hint] — placed in **excluded**
  - heading: Chapter 14: Constructions > 14.3 Line bisector
  - evidence quote: "If you find it easier, you may draw two bigger arcs instead of four smaller arcs when you construct the bisector of a line segment, as shown in the diagram below."
- `ch14-b026` [exposition] — placed in **AO:bisection-of-a-given-line-segment-ao-bisect-line-segment (instruction)**
  - heading: Chapter 14: Constructions > 14.3 Line bisector
  - evidence quote: "Source image reference for drawing two bigger arcs instead of four smaller arcs when bisecting a line segment: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-053.png"
- `ch14-b027` [exercise_block] — placed in **excluded**
  - heading: Chapter 14: Constructions > 14.3 Line bisector > Exercise 14.4: Bisect a line segment
  - evidence quote: "### Exercise 14.4: Bisect a line segment"
- `ch14-b027-i01` [exercise_item] — placed in **AO:bisection-of-a-given-line-segment-ao-bisect-line-segment (exercise)**
  - heading: Chapter 14: Constructions > 14.3 Line bisector > Exercise 14.4: Bisect a line segment
  - evidence quote: "### Exercise 14.4: Bisect a line segment  1. Draw line segment $CD$ as shown below.  Source image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-054.png  Bisec…"
- `ch14-b027-i02` [exercise_item] — placed in **AO:bisection-of-a-given-line-segment-ao-bisect-line-segment (exercise)**
  - heading: Chapter 14: Constructions > 14.3 Line bisector > Exercise 14.4: Bisect a line segment
  - evidence quote: "### Exercise 14.4: Bisect a line segment  2. Draw line segment $EF$ as shown below.  Source image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-056.png  Bisec…"
- `ch14-b027-i03` [exercise_item] — placed in **AO:bisection-of-a-given-line-segment-ao-bisect-line-segment (exercise)**
  - heading: Chapter 14: Constructions > 14.3 Line bisector > Exercise 14.4: Bisect a line segment
  - evidence quote: "### Exercise 14.4: Bisect a line segment  3. Draw line segment $MN$ as shown below.  Source image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-058.png  Bisec…"
- `ch14-b027-i04` [exercise_item] — placed in **AO:bisection-of-a-given-line-segment-ao-bisect-line-segment (exercise)**
  - heading: Chapter 14: Constructions > 14.3 Line bisector > Exercise 14.4: Bisect a line segment
  - evidence quote: "### Exercise 14.4: Bisect a line segment  4. Draw line segment $ST$ as shown below.  Source image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-060.png  Bisec…"
- `ch14-b036` [summary] — placed in **excluded**
  - heading: Chapter 14: Constructions > 14.6 Summary
  - evidence quote: "- A construction in Mathematics is an accurate drawing of angles and lines. - You are only allowed to use a straightedge and a pair of compasses with a pencil in it when you do a construction. - You may use a ruler if y…"

### Row-level review categories and manually authored reasons
_None — all AOs have direct evidence and a reused assessment._

### Per-atomic-objective evidence classification
- `bisection-of-a-given-line-segment-ao-bisect-line-segment` → evidence: **direct** · categories: —
  - linked records: ch14-b021(instruction), ch14-b022(foundation), ch14-b023(worked_example), ch14-b024(instruction), ch14-b026(instruction), ch14-b027-i01(exercise), ch14-b027-i02(exercise), ch14-b027-i03(exercise), ch14-b027-i04(exercise)
  - assessment: reused from `ch14-b027-i03`

---

## `jss1-math-construction-construction-of-angles-90-and-60-degrees`

**Title:** Construction of angles 90 and 60 degrees.  
**Status:** `mapped`  
**Row review categories:** _(none — mapped or no-records baseline)_

### Curriculum objectives (source)
- `jss1-math-construction-construction-of-angles-90-and-60-degrees-po01`: Construct angles 90 and 60 degrees

### Atomic objectives
- `construction-of-angles-90-and-60-degrees-ao-construct-90-degree-angle` [construct/apply]: Construct 90 degree angles.
- `construction-of-angles-90-and-60-degrees-ao-construct-60-degree-angle` [construct/apply]: Construct 60 degree angles.

### Linked textbook records (22 total) — inspected
- `ch14-b001` [exposition] — placed in **shared_foundation**
  - heading: Chapter 14: Constructions
  - evidence quote: "A construction in Mathematics is an accurate drawing of angles and lines. You are only allowed to use a straightedge and a pair of compasses with a pencil in it when you do constructions.  1. A straightedge  A straighte…"
- `ch14-b002` [hint] — placed in **excluded**
  - heading: Chapter 14: Constructions
  - evidence quote: "The two legs of the compass are joined at the hinge. Make sure that the metal pin at the hinge is fitted tightly so that the two legs of the compass will not open too easily. Also make sure that your pencil is sharpened…"
- `ch14-b003` [hint] — placed in **excluded**
  - heading: Chapter 14: Constructions
  - evidence quote: "Do not confuse the compass that we use in mathematical constructions with the compass that we use to find direction."
- `ch14-b004` [exposition] — placed in **shared_foundation**
  - heading: Chapter 14: Constructions
  - evidence quote: "All the constructions in this chapter are based on the properties of a circle.  In the diagram below, $BC$ is the diameter of the circle. $A$ is the centre of the circle. This means that $AB$ is a radius of the circle a…"
- `ch14-b005` [definition] — placed in **shared_foundation**
  - heading: Chapter 14: Constructions
  - evidence quote: "**arc** An arc is a part of the circumference of a circle."
- `ch14-b028` [exposition] — placed in **AO:construction-of-angles-90-and-60-degrees-ao-construct-60-degree-angle (instruction)**
  - heading: Chapter 14: Constructions > 14.4 Sixty-degree angles
  - evidence quote: "Here is a fun activity for you to do: Use a compass and draw a circle. Keep the position of the legs of the compass the same for the whole activity.  Make a dot anywhere on the circumference of the circle.  Source image…"
- `ch14-b029` [worked_example] — placed in **AO:construction-of-angles-90-and-60-degrees-ao-construct-60-degree-angle (worked_example)**
  - heading: Chapter 14: Constructions > 14.4 Sixty-degree angles > Worked example 14.5: Constructing an angle of 60 degrees
  - evidence quote: "You are given a line segment $BD$ as shown below. Construct $AB$ so that $C$ is a point on $AB$ and $A\hat{B}C = 60^{\circ}$.  Source image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/i…"
- `ch14-b030` [note] — placed in **AO:construction-of-angles-90-and-60-degrees-ao-construct-60-degree-angle (instruction)**
  - heading: Chapter 14: Constructions > 14.4 Sixty-degree angles
  - evidence quote: "When you construct an angle of $60^{\circ}$ you are actually constructing a triangle with three equal sides. In an equilateral triangle all three sides have equal lengths and each of the angles are equal to $60^{\circ}$."
- `ch14-b031` [exposition] — placed in **AO:construction-of-angles-90-and-60-degrees-ao-construct-60-degree-angle (instruction)**
  - heading: Chapter 14: Constructions > 14.4 Sixty-degree angles
  - evidence quote: "Source image reference for the sixty-degree-angle construction context: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-071.png"
- `ch14-b032` [exercise_block] — placed in **excluded**
  - heading: Chapter 14: Constructions > 14.4 Sixty-degree angles > Exercise 14.5: Construct an angle of 60 degrees
  - evidence quote: "### Exercise 14.5: Construct an angle of 60 degrees"
- `ch14-b032-i01` [exercise_item] — placed in **AO:construction-of-angles-90-and-60-degrees-ao-construct-60-degree-angle (exercise)**
  - heading: Chapter 14: Constructions > 14.4 Sixty-degree angles > Exercise 14.5: Construct an angle of 60 degrees
  - evidence quote: "### Exercise 14.5: Construct an angle of 60 degrees  1. Draw line segment $CD$ as shown below.  Source image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-054…"
- `ch14-b032-i02` [exercise_item] — placed in **AO:construction-of-angles-90-and-60-degrees-ao-construct-60-degree-angle (exercise)**
  - heading: Chapter 14: Constructions > 14.4 Sixty-degree angles > Exercise 14.5: Construct an angle of 60 degrees
  - evidence quote: "### Exercise 14.5: Construct an angle of 60 degrees  2. Draw line segment $EF$ as shown below.  Source image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-056…"
- `ch14-b032-i03` [exercise_item] — placed in **AO:construction-of-angles-90-and-60-degrees-ao-construct-60-degree-angle (exercise)**
  - heading: Chapter 14: Constructions > 14.4 Sixty-degree angles > Exercise 14.5: Construct an angle of 60 degrees
  - evidence quote: "### Exercise 14.5: Construct an angle of 60 degrees  3. Draw line segment $MN$ as shown below.  Source image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-058…"
- `ch14-b032-i04` [exercise_item] — placed in **AO:construction-of-angles-90-and-60-degrees-ao-construct-60-degree-angle (exercise)**
  - heading: Chapter 14: Constructions > 14.4 Sixty-degree angles > Exercise 14.5: Construct an angle of 60 degrees
  - evidence quote: "### Exercise 14.5: Construct an angle of 60 degrees  4. Draw line segment $ST$ as shown below.  Source image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-060…"
- `ch14-b033` [exposition] — placed in **AO:construction-of-angles-90-and-60-degrees-ao-construct-90-degree-angle (instruction)**
  - heading: Chapter 14: Constructions > 14.5 Right angle
  - evidence quote: "A right angle is an angle of 90 degrees. In real life we often see right angles. For example, the corners of your workbook are right angles, the corners of a door are right angles, and the corners of most tables are rig…"
- `ch14-b034` [worked_example] — placed in **AO:construction-of-angles-90-and-60-degrees-ao-construct-90-degree-angle (worked_example)**
  - heading: Chapter 14: Constructions > 14.5 Right angle > Worked example 14.6: Constructing a right angle
  - evidence quote: "You are given a line segment $BD$ as shown below. Construct $AB$ so that $A\hat{B}C = 90^{\circ}$.  Source image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14…"
- `ch14-b035` [exercise_block] — placed in **excluded**
  - heading: Chapter 14: Constructions > 14.5 Right angle > Exercise 14.6: Construct a right angle
  - evidence quote: "### Exercise 14.6: Construct a right angle"
- `ch14-b035-i01` [exercise_item] — placed in **AO:construction-of-angles-90-and-60-degrees-ao-construct-90-degree-angle (exercise)**
  - heading: Chapter 14: Constructions > 14.5 Right angle > Exercise 14.6: Construct a right angle
  - evidence quote: "### Exercise 14.6: Construct a right angle  1. Draw line segment $CD$ as shown below.  Source image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-054.png  Con…"
- `ch14-b035-i02` [exercise_item] — placed in **AO:construction-of-angles-90-and-60-degrees-ao-construct-90-degree-angle (exercise)**
  - heading: Chapter 14: Constructions > 14.5 Right angle > Exercise 14.6: Construct a right angle
  - evidence quote: "### Exercise 14.6: Construct a right angle  2. Draw line segment $EF$ as shown below.  Source image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-056.png  Con…"
- `ch14-b035-i03` [exercise_item] — placed in **AO:construction-of-angles-90-and-60-degrees-ao-construct-90-degree-angle (exercise)**
  - heading: Chapter 14: Constructions > 14.5 Right angle > Exercise 14.6: Construct a right angle
  - evidence quote: "### Exercise 14.6: Construct a right angle  3. Draw line segment $MN$ as shown below.  Source image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-0858.png  Co…"
- `ch14-b035-i04` [exercise_item] — placed in **AO:construction-of-angles-90-and-60-degrees-ao-construct-90-degree-angle (exercise)**
  - heading: Chapter 14: Constructions > 14.5 Right angle > Exercise 14.6: Construct a right angle
  - evidence quote: "### Exercise 14.6: Construct a right angle  4. Draw line segment $ST$ as shown below.  Source image reference: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-14-060.png  Con…"
- `ch14-b036` [summary] — placed in **excluded**
  - heading: Chapter 14: Constructions > 14.6 Summary
  - evidence quote: "- A construction in Mathematics is an accurate drawing of angles and lines. - You are only allowed to use a straightedge and a pair of compasses with a pencil in it when you do a construction. - You may use a ruler if y…"

### Row-level review categories and manually authored reasons
_None — all AOs have direct evidence and a reused assessment._

### Per-atomic-objective evidence classification
- `construction-of-angles-90-and-60-degrees-ao-construct-90-degree-angle` → evidence: **direct** · categories: —
  - linked records: ch14-b033(instruction), ch14-b034(worked_example), ch14-b035-i01(exercise), ch14-b035-i02(exercise), ch14-b035-i03(exercise), ch14-b035-i04(exercise)
  - assessment: reused from `ch14-b035-i03`
- `construction-of-angles-90-and-60-degrees-ao-construct-60-degree-angle` → evidence: **direct** · categories: —
  - linked records: ch14-b028(instruction), ch14-b029(worked_example), ch14-b030(instruction), ch14-b031(instruction), ch14-b032-i01(exercise), ch14-b032-i02(exercise), ch14-b032-i03(exercise), ch14-b032-i04(exercise)
  - assessment: reused from `ch14-b032-i03`

---

## `jss1-math-angles-measurement-of-angles`

**Title:** Measurement of angles.  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope

### Curriculum objectives (source)
- `jss1-math-angles-measurement-of-angles-po01`: Measure angles

### Atomic objectives
- `measurement-of-angles-ao-measure-angles` [measure/apply]: Measure angles.

### Linked textbook records (31 total) — inspected
- `ch15-b001` [exposition] — placed in **shared_foundation**
  - heading: Chapter 15: Angles
  - evidence quote: "In this chapter you will work with **angles**. You will learn how to label and measure angles. You will also learn about the different angles that are formed on a straight line when straight lines cross each other."
- `ch15-b002` [definition] — placed in **shared_foundation**
  - heading: Chapter 15: Angles
  - evidence quote: "**angle** An angle is the amount of turn between two straight lines that have a common end point. The common end point is called the vertex of the angle.  Source image: https://electricbookworks.github.io/siyavula-open-…"
- `ch15-b003` [exposition] — placed in **shared_foundation**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles
  - evidence quote: "We measure angles in degrees. Before we can measure angles, we need to know how to label angles."
- `ch15-b004` [exposition] — placed in **review_items**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Labelling angles
  - evidence quote: "When we label an angle, we name the angle, so that we know which angle it is that we are talking about."
- `ch15-b005` [worked_example] — placed in **review_items**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Worked example 15.1: Labelling angles
  - evidence quote: "Consider the following diagram.  Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_030.png  Give the correct label for the marked angle."
- `ch15-b006` [note] — placed in **review_items**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Labelling angles
  - evidence quote: "From now on we will use only one notation. We will label the angle at point $A$ as $\hat{A}$."
- `ch15-b007` [worked_example] — placed in **review_items**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Worked example 15.2: Labelling angles
  - evidence quote: "Consider the following diagram.  Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_031.png  Give the correct label for the marked angle."
- `ch15-b008` [exposition] — placed in **review_items**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Labelling angles
  - evidence quote: "It is easy to make a mistake if you have to refer to an angle as $C\hat{A}D$ or $D\hat{A}C$. It is also time consuming, so we often use small numbers to label angles. We use these to refer more easily to a specific angl…"
- `ch15-b009` [worked_example] — placed in **review_items**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Worked example 15.3: Labelling angles
  - evidence quote: "Consider the following diagram.  Diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_061.png  Give the correct label for the marked angle."
- `ch15-b010` [exercise_block] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Exercise 15.1: Label angles
  - evidence quote: "### Exercise 15.1: Label angles"
- `ch15-b010-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Exercise 15.1: Label angles
  - evidence quote: "### Exercise 15.1: Label angles  1. Consider the following diagram. Give the correct label for the marked angle.  Diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web…"
- `ch15-b010-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Exercise 15.1: Label angles
  - evidence quote: "### Exercise 15.1: Label angles  2. Consider the following diagram. Give the correct label for the marked angle.  Diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web…"
- `ch15-b010-i03` [exercise_item] — placed in **review_items**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Exercise 15.1: Label angles
  - evidence quote: "### Exercise 15.1: Label angles  3. Consider the following diagram. Give the correct label for the marked angle.  Diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web…"
- `ch15-b010-i04` [exercise_item] — placed in **review_items**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Exercise 15.1: Label angles
  - evidence quote: "### Exercise 15.1: Label angles  4. Consider the following diagram. Give the correct label for the marked angle.  Diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web…"
- `ch15-b010-i05` [exercise_item] — placed in **review_items**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Exercise 15.1: Label angles
  - evidence quote: "### Exercise 15.1: Label angles  5. Consider the following diagram. How would you mark ${\hat{T}}_{3}$?  Diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1…"
- `ch15-b011` [exposition] — placed in **AO:measurement-of-angles-ao-measure-angles (instruction)**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Measuring angles
  - evidence quote: "We measure angles in degrees. We use a protractor to measure an angle.  Protractor image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-005.png  Take note of the followi…"
- `ch15-b012` [hint] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Measuring angles
  - evidence quote: "It is a good idea to estimate the size of an angle before you measure the angle. Then you can be sure that you are reading off the correct answer from the protractor."
- `ch15-b013` [exposition] — placed in **shared_foundation**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Types of angles
  - evidence quote: "Different types of angles have different names. The names you may need to use when working with angles are given in the table below.  | Name of angle | Size of angle | | --- | --- | | acute angle | between $0^{\circ}$ a…"
- `ch15-b014` [worked_example] — placed in **AO:measurement-of-angles-ao-measure-angles (worked_example)**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Worked example 15.4: Measuring a right angle
  - evidence quote: "Use a protractor to measure the given angle in the diagram below.  Diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-010.png"
- `ch15-b015` [worked_example] — placed in **AO:measurement-of-angles-ao-measure-angles (worked_example)**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Worked example 15.5: Measuring an acute angle
  - evidence quote: "Use a protractor to measure the marked angle shown below.  Diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-012.png"
- `ch15-b016` [worked_example] — placed in **AO:measurement-of-angles-ao-measure-angles (worked_example)**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Worked example 15.6: Measuring an obtuse angle
  - evidence quote: "Use a protractor to measure the marked angle shown below.  Diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-014.png  Use the dotted lines shown to hel…"
- `ch15-b017` [worked_example] — placed in **AO:measurement-of-angles-ao-measure-angles (worked_example)**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Worked example 15.7: Measuring a reflex angle
  - evidence quote: "Use a protractor and measure the angle shown below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-016.png]"
- `ch15-b018` [hint] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Types of angles
  - evidence quote: "Remember that reflex angles are always less than $360^{\circ}$, but more than $180^{\circ}$. A full turn or revolution is equal to $360^{\circ}$."
- `ch15-b019` [exercise_block] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Exercise 15.2: Measure angles
  - evidence quote: "### Exercise 15.2: Measure angles"
- `ch15-b019-i01` [exercise_item] — placed in **AO:measurement-of-angles-ao-measure-angles (exercise)**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Exercise 15.2: Measure angles
  - evidence quote: "### Exercise 15.2: Measure angles  1. Use a protractor and measure the angle shown below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-018.png]"
- `ch15-b019-i02` [exercise_item] — placed in **AO:measurement-of-angles-ao-measure-angles (exercise)**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Exercise 15.2: Measure angles
  - evidence quote: "### Exercise 15.2: Measure angles  2. Use a protractor and measure the angle shown below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-019.png]"
- `ch15-b019-i03` [exercise_item] — placed in **AO:measurement-of-angles-ao-measure-angles (exercise)**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Exercise 15.2: Measure angles
  - evidence quote: "### Exercise 15.2: Measure angles  3. Use a protractor and measure the angle shown below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-020.png]"
- `ch15-b019-i04` [exercise_item] — placed in **AO:measurement-of-angles-ao-measure-angles (exercise)**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Exercise 15.2: Measure angles
  - evidence quote: "### Exercise 15.2: Measure angles  4. Use a protractor and measure the angle shown below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-021.png]"
- `ch15-b019-i05` [exercise_item] — placed in **AO:measurement-of-angles-ao-measure-angles (exercise)**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Exercise 15.2: Measure angles
  - evidence quote: "### Exercise 15.2: Measure angles  5. Use a protractor and measure the angle shown below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-022.png]"
- `ch15-b019-i06` [exercise_item] — placed in **AO:measurement-of-angles-ao-measure-angles (exercise)**
  - heading: Chapter 15: Angles > 15.1 Labelling and measuring angles > Exercise 15.2: Measure angles
  - evidence quote: "### Exercise 15.2: Measure angles  6. Use a protractor and measure the angle shown below.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-023.png]"
- `ch15-b064` [summary] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.5 Summary
  - evidence quote: "An angle is the amount of turn between two straight lines that have a common end point, called the vertex of the angle.  We use a protractor to measure angles in degrees. Always estimate an angle before you measure it,…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: 11 records (ch15-b004 through ch15-b010-i01..i05 plus b006, b008) cover labelling angles, which is prerequisite to but not the same skill as measuring angles; parked in review_items.

### Per-atomic-objective evidence classification
- `measurement-of-angles-ao-measure-angles` → evidence: **direct** · categories: —
  - linked records: ch15-b011(instruction), ch15-b014(worked_example), ch15-b015(worked_example), ch15-b016(worked_example), ch15-b017(worked_example), ch15-b019-i01(exercise), ch15-b019-i02(exercise), ch15-b019-i03(exercise), ch15-b019-i04(exercise), ch15-b019-i05(exercise), ch15-b019-i06(exercise)
  - assessment: reused from `ch15-b019-i03`

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All review_items were inspected. Candidate proposal added for labelling angles because the records teach angle notation, which is prerequisite to measurement but not measuring itself.

### Candidate atomic objective proposals
- `measurement-of-angles-candidate-ao-label-angles` [prerequisite; candidate_for_expert_review]
  - proposed objective: Label angles using standard angle notation.
  - source records: ch15-b004, ch15-b005, ch15-b006, ch15-b007, ch15-b008, ch15-b009, ch15-b010-i01, ch15-b010-i02, ch15-b010-i03, ch15-b010-i04, ch15-b010-i05
  - closest existing AOs: measurement-of-angles-ao-measure-angles
  - candidate evidence quote: "When we label an angle, we name the angle"
  - rationale: The records ask learners to name or label angles. That supports measuring angles but is a separate notation skill.

---

## `jss1-math-angles-identification-and-properties-of-vertically-opposite-adjacent-alternate-and-corresponding-angles`

**Title:** Identification and properties of: vertically opposite, adjacent, alternate, and corresponding angles.  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, ao_no_evidence, prerequisite_only_evidence, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-angles-identification-and-properties-of-vertically-opposite-adjacent-alternate-and-corresponding-angles-po01`: Identify vertically opposite, adjacent, alternate and corresponding angles
- `jss1-math-angles-identification-and-properties-of-vertically-opposite-adjacent-alternate-and-corresponding-angles-po02`: State properties of angles

### Atomic objectives
- `identification-and-properties-of-special-angles-ao-identify-vertically-opposite-angles` [identify/remember]: Identify vertically opposite angles.
- `identification-and-properties-of-special-angles-ao-identify-adjacent-angles` [identify/remember]: Identify adjacent angles.
- `identification-and-properties-of-special-angles-ao-identify-alternate-angles` [identify/remember]: Identify alternate angles.
- `identification-and-properties-of-special-angles-ao-identify-corresponding-angles` [identify/remember]: Identify corresponding angles.
- `identification-and-properties-of-special-angles-ao-state-properties-of-angles` [state/remember]: State properties of angles.

### Linked textbook records (65 total) — inspected
- `ch15-b020` [exposition] — placed in **shared_foundation**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines
  - evidence quote: "You will need to be able to identify and measure angles on a straight line as well as angles formed by two intersecting lines. When you know the properties of these angles, you can use them to solve problems that involv…"
- `ch15-b029` [exposition] — placed in **shared_foundation**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Angles at intersecting lines
  - evidence quote: "When two lines cross each other, we say the two lines are **intersecting** lines."
- `ch15-b030` [definition] — placed in **shared_foundation**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Angles at intersecting lines
  - evidence quote: "**intersecting lines** Intersecting lines are lines that cross each other."
- `ch15-b031` [exposition] — placed in **shared_foundation**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Angles at intersecting lines
  - evidence quote: "The diagram shows two straight lines intersecting at a point, and forming the four angles $\hat{a}$, $\hat{b}$, $\hat{c}$ and $\hat{d}$.  Diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks…"
- `ch15-b032` [definition] — placed in **AO:identification-and-properties-of-special-angles-ao-identify-vertically-opposite-angles (foundation)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Angles at intersecting lines
  - evidence quote: "**vertically opposite angles** Vertically opposite angles are on the opposite sides of a vertex formed by two intersecting lines. Vertically opposite angles are equal to each other."
- `ch15-b033` [note] — placed in **shared_foundation**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Angles at intersecting lines
  - evidence quote: "The four angles formed by two intersecting straight lines form a revolution. All the angles around one point form a revolution. One revolution is equal to $360^{\circ}$.  [Source image: https://electricbookworks.github.…"
- `ch15-b034` [note] — placed in **shared_foundation**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Angles at intersecting lines
  - evidence quote: "We can also use Greek letters to label angles:  - We read $\alpha$ as "alpha". - We read $\beta$ as "beta". - We read $\delta$ as "delta"."
- `ch15-b035` [worked_example] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (worked_example)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Worked example 15.9: Identifying types of angles at intersecting lines
  - evidence quote: "The diagram shows line $IJ$ intersecting line $EF$. The intersecting lines create four different angles. These angles are labelled with the variables $\alpha$, $\beta$, $\delta$, and $x$.  [Source image: https://electri…"
- `ch15-b036` [exercise_block] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.4: Identify angles at intersecting lines
  - evidence quote: "### Exercise 15.4: Identify angles at intersecting lines  The diagram shows line $IJ$ intersecting line $EF$. The intersecting lines create four different angles. These angles are labelled $\alpha$, $\beta$, $\delta$, a…"
- `ch15-b036-i01` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.4: Identify angles at intersecting lines
  - evidence quote: "### Exercise 15.4: Identify angles at intersecting lines  The diagram shows line $IJ$ intersecting line $EF$. The intersecting lines create four different angles. These angles are labelled $\alpha$, $\beta$, $\delta$, a…"
- `ch15-b036-i02` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.4: Identify angles at intersecting lines
  - evidence quote: "### Exercise 15.4: Identify angles at intersecting lines  The diagram shows line $IJ$ intersecting line $EF$. The intersecting lines create four different angles. These angles are labelled $\alpha$, $\beta$, $\delta$, a…"
- `ch15-b036-i03` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.4: Identify angles at intersecting lines
  - evidence quote: "### Exercise 15.4: Identify angles at intersecting lines  The diagram shows line $IJ$ intersecting line $EF$. The intersecting lines create four different angles. These angles are labelled $\alpha$, $\beta$, $\delta$, a…"
- `ch15-b036-i04` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.4: Identify angles at intersecting lines
  - evidence quote: "### Exercise 15.4: Identify angles at intersecting lines  The diagram shows line $IJ$ intersecting line $EF$. The intersecting lines create four different angles. These angles are labelled $\alpha$, $\beta$, $\delta$, a…"
- `ch15-b036-i05` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.4: Identify angles at intersecting lines
  - evidence quote: "### Exercise 15.4: Identify angles at intersecting lines  The diagram shows line $IJ$ intersecting line $EF$. The intersecting lines create four different angles. These angles are labelled $\alpha$, $\beta$, $\delta$, a…"
- `ch15-b037` [exposition] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (instruction)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Using the properties of angles at intersecting lines in calculations
  - evidence quote: "Now that you know how to identify the different angles formed by two intersecting straight lines, you can use these angles and their properties to do calculations. These will involve working out the value of unknown ang…"
- `ch15-b038` [worked_example] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (worked_example)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Worked example 15.10: Using properties of intersecting straight lines
  - evidence quote: "In the diagram below, $EF$ and $GH$ are straight lines.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_033.png]  Determine the value of $b$, giving a…"
- `ch15-b039` [exercise_block] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.5: Calculate angles at intersecting straight lines
  - evidence quote: "### Exercise 15.5: Calculate angles at intersecting straight lines"
- `ch15-b039-i01` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.5: Calculate angles at intersecting straight lines
  - evidence quote: "### Exercise 15.5: Calculate angles at intersecting straight lines  1. In the diagram below, $TU$ and $VW$ are straight lines.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/ima…"
- `ch15-b039-i02` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.5: Calculate angles at intersecting straight lines
  - evidence quote: "### Exercise 15.5: Calculate angles at intersecting straight lines  2. In the diagram below, $PQ$ and $RS$ are straight lines.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/ima…"
- `ch15-b039-i03` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.5: Calculate angles at intersecting straight lines
  - evidence quote: "### Exercise 15.5: Calculate angles at intersecting straight lines  3. In the diagram below, $EF$ and $GH$ are straight lines.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/ima…"
- `ch15-b039-i04` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.5: Calculate angles at intersecting straight lines
  - evidence quote: "### Exercise 15.5: Calculate angles at intersecting straight lines  4. In the diagram below, $EF$ and $GH$ are straight lines.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/ima…"
- `ch15-b039-i05` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.5: Calculate angles at intersecting straight lines
  - evidence quote: "### Exercise 15.5: Calculate angles at intersecting straight lines  5. In the diagram below, $TU$ and $VW$ are straight lines.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/ima…"
- `ch15-b040` [exposition] — placed in **shared_foundation**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines
  - evidence quote: "Parallel lines are always the same distance apart. We use arrow markings to indicate parallel lines.  - The two lines that have a single arrow are parallel to each other. - The two lines that have a double arrow are par…"
- `ch15-b041` [definition] — placed in **shared_foundation**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines
  - evidence quote: "**transversal** A transversal is a line that intersects two or more parallel lines."
- `ch15-b042` [exposition] — placed in **shared_foundation**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines
  - evidence quote: "The diagram shows that the transversal $GH$ intersects the parallel lines $CD$ and $EF$.  The intersecting lines create angles. Some of these angles are labelled.  Source image: https://electricbookworks.github.io/siyav…"
- `ch15-b043` [definition] — placed in **AO:identification-and-properties-of-special-angles-ao-identify-corresponding-angles (foundation)**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines
  - evidence quote: "**corresponding angles** Corresponding angles are equal. They are in matching positions on the parallel lines and transversal, in an "F" shape.  **co-interior angles** Co-interior angles are supplementary. They are both…"
- `ch15-b044` [hint] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines
  - evidence quote: "To help you remember these angles, think of **Maths is FUN!**  If two parallel lines are cut by a transversal, then:  - **F**: corresponding angles are equal - **U**: co-interior angles are supplementary - **N**: altern…"
- `ch15-b045` [worked_example] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (worked_example)**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Worked example 15.11: Recognising pairs of angles between parallel lines
  - evidence quote: "In the diagram below, $AB \parallel CD$ and $EF$ is a transversal.  Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_005.png  What type of angle pair is s…"
- `ch15-b046` [exercise_block] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Exercise 15.6: Recognise pairs of angles between parallel lines
  - evidence quote: "### Exercise 15.6: Recognise pairs of angles between parallel lines"
- `ch15-b046-i01` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Exercise 15.6: Recognise pairs of angles between parallel lines
  - evidence quote: "### Exercise 15.6: Recognise pairs of angles between parallel lines  1. In the diagram below, $AB \parallel CD$ and $EF$ is a transversal.  Source image: https://electricbookworks.github.io/siyavula-open-textbooks-image…"
- `ch15-b046-i02` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Exercise 15.6: Recognise pairs of angles between parallel lines
  - evidence quote: "### Exercise 15.6: Recognise pairs of angles between parallel lines  2. In the diagram below, $RS \parallel TO$ and $MN$ is a transversal.  Source image: https://electricbookworks.github.io/siyavula-open-textbooks-image…"
- `ch15-b046-i03` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Exercise 15.6: Recognise pairs of angles between parallel lines
  - evidence quote: "### Exercise 15.6: Recognise pairs of angles between parallel lines  3. In the diagram below, $RS \parallel TO$ and $MN$ is a transversal.  Source image: https://electricbookworks.github.io/siyavula-open-textbooks-image…"
- `ch15-b047` [exposition] — placed in **shared_foundation**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Using the properties of angles on parallel lines in calculations
  - evidence quote: "Now that you know about corresponding angles, co-interior angles and alternate angles, you can use the properties of these angles to solve problems."
- `ch15-b048` [worked_example] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (worked_example)**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Worked example 15.12: Calculating angles between parallel lines
  - evidence quote: "In the diagram below, $FG \parallel HJ$ and $KL$ is a transversal.  Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_004.png  What is the value of $x$? Gi…"
- `ch15-b049` [hint] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Using the properties of angles on parallel lines in calculations
  - evidence quote: "For Exercise 15.7, remember the facts that you have learnt about parallel lines, and decide which one of them will be useful."
- `ch15-b050` [exercise_block] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Exercise 15.7: Calculate angles between parallel lines
  - evidence quote: "### Exercise 15.7: Calculate angles between parallel lines"
- `ch15-b050-i01` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Exercise 15.7: Calculate angles between parallel lines
  - evidence quote: "### Exercise 15.7: Calculate angles between parallel lines  1. In the diagram below, $DE \parallel FG$ and $HJ$ is a transversal. Image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/we…"
- `ch15-b050-i02` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Exercise 15.7: Calculate angles between parallel lines
  - evidence quote: "### Exercise 15.7: Calculate angles between parallel lines  2. In the diagram below, $DE \parallel FG$ and $HJ$ is a transversal. Image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/we…"
- `ch15-b050-i03` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Exercise 15.7: Calculate angles between parallel lines
  - evidence quote: "### Exercise 15.7: Calculate angles between parallel lines  3. In the diagram below, $DE \parallel FG$ and $HJ$ is a transversal. Image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/we…"
- `ch15-b050-i04` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Exercise 15.7: Calculate angles between parallel lines
  - evidence quote: "### Exercise 15.7: Calculate angles between parallel lines  4. In the diagram below, $AB \parallel CD$. Image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_021.png…"
- `ch15-b050-i05` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Exercise 15.7: Calculate angles between parallel lines
  - evidence quote: "### Exercise 15.7: Calculate angles between parallel lines  5. In the diagram below, $FG \parallel HJ$. Image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_047.png…"
- `ch15-b051` [exposition] — placed in **shared_foundation**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Parallel lines with more than one transversal
  - evidence quote: "It is possible that two parallel lines can have more than one transversal. If this is the case, it is important to identify which lines are parallel lines."
- `ch15-b052` [worked_example] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (worked_example)**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Worked example 15.13: Finding angles when there are two transversals
  - evidence quote: "In the diagram below, $RS \parallel TU$. Determine the sizes of $a$ and $b$, giving reasons for your answers.  Image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-15-0_0…"
- `ch15-b053` [hint] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Parallel lines with more than one transversal
  - evidence quote: "Identify the parallel lines and draw over them in a different colour, if you can."
- `ch15-b054` [exercise_block] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Exercise 15.8: Find angle sizes where there are two transversals
  - evidence quote: "### Exercise 15.8: Find angle sizes where there are two transversals"
- `ch15-b054-i01` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Exercise 15.8: Find angle sizes where there are two transversals
  - evidence quote: "### Exercise 15.8: Find angle sizes where there are two transversals  1. In the diagram below, $EF \parallel GH$; $JK$ is a transversal and $LM$ is a transversal. Determine the sizes of $a$ and $b$, giving reasons for y…"
- `ch15-b054-i02` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Exercise 15.8: Find angle sizes where there are two transversals
  - evidence quote: "### Exercise 15.8: Find angle sizes where there are two transversals  2. In the diagram below, $EF \parallel GH$; $JK$ is a transversal and $LM$ is a transversal. Determine the sizes of $a$ and $b$, giving reasons for y…"
- `ch15-b054-i03` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Exercise 15.8: Find angle sizes where there are two transversals
  - evidence quote: "### Exercise 15.8: Find angle sizes where there are two transversals  3. Use adjacent, corresponding, co-interior and alternate angles to calculate the sizes of all the angles labelled with variables in the diagram. Giv…"
- `ch15-b055` [exposition] — placed in **shared_foundation**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Parallel lines with more than one transversal
  - evidence quote: "When we determine the angles formed by two parallel lines and a transversal, we sometimes need more than one step to find the solution to the question. The worked example below shows how to do this."
- `ch15-b056` [worked_example] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (worked_example)**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Worked example 15.14: Solving two-step problems with parallel lines
  - evidence quote: "In the diagram below, $ML \parallel JK$ and $PQ$ is a transversal. Determine the value of $s$. Give reasons for all your statements.  Image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/image…"
- `ch15-b057` [exercise_block] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Exercise 15.9: Solve two-step problems with parallel lines
  - evidence quote: "### Exercise 15.9: Solve two-step problems with parallel lines"
- `ch15-b057-i01` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Exercise 15.9: Solve two-step problems with parallel lines
  - evidence quote: "### Exercise 15.9: Solve two-step problems with parallel lines  1. In the diagram below, $DC \parallel BA$ and $EF$ is a transversal.  Determine the value of $z$. Give a reason for each statement.  Source image: https:/…"
- `ch15-b057-i02` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Exercise 15.9: Solve two-step problems with parallel lines
  - evidence quote: "### Exercise 15.9: Solve two-step problems with parallel lines  2. In the diagram below, $AB \parallel CD$ and $EF$ is a transversal.  Determine the value of $q$. Give a reason for each statement.  Source image: https:/…"
- `ch15-b058` [exposition] — placed in **shared_foundation**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Working with more than two parallel lines
  - evidence quote: "We do not have to work with two parallel lines only. Sometimes there are more than two parallel lines in a diagram. The trick is to focus on only two parallel lines at a time, and to remember the F-U-N angles. The worke…"
- `ch15-b059` [worked_example] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (worked_example)**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Worked example 15.15: Finding two angles with three parallel lines
  - evidence quote: "In the diagram below, $PQ \parallel RS \parallel TU$. Determine the values of $x$ and $y$, giving reasons for your answers.  Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/…"
- `ch15-b060` [exercise_block] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Exercise 15.10: Find two angles with three parallel lines
  - evidence quote: "### Exercise 15.10: Find two angles with three parallel lines"
- `ch15-b060-i01` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Exercise 15.10: Find two angles with three parallel lines
  - evidence quote: "### Exercise 15.10: Find two angles with three parallel lines  1. In the diagram below, $PQ \parallel RS \parallel TU$. Determine the values of $x$ and $y$, giving reasons for your answers.  Source image: https://electr…"
- `ch15-b060-i02` [exercise_item] — placed in **AO:identification-and-properties-of-special-angles-ao-state-properties-of-angles (exercise)**
  - heading: Chapter 15: Angles > 15.3 Angles on parallel lines > Exercise 15.10: Find two angles with three parallel lines
  - evidence quote: "### Exercise 15.10: Find two angles with three parallel lines  2. In the diagram below, $PQ \parallel RS \parallel TU$. Determine the values of $x$ and $y$, giving reasons for your answers.  Source image: https://electr…"
- `ch15-b061` [exposition] — placed in **review_items**
  - heading: Chapter 15: Angles > 15.4 Practical applications
  - evidence quote: "When we know about different angles and how they are formed we can apply our knowledge in real life. For example, we can use angles to describe the position of a shop, or how we want to paint decorations. Many people us…"
- `ch15-b062` [worked_example] — placed in **review_items**
  - heading: Chapter 15: Angles > 15.4 Practical applications > Worked example 15.16: Solving real-world problems with angles
  - evidence quote: "Suleiman is not sure where to find a specific shoe shop in the nearby city. He has a discussion with his friend Musa who knows where many of the shops in the city are.  Musa: "Do you know remember where the cell phone s…"
- `ch15-b063` [exercise_block] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.4 Practical applications > Exercise 15.11: Solve real-world problems with angles
  - evidence quote: "### Exercise 15.11: Solve real-world problems with angles"
- `ch15-b063-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 15: Angles > 15.4 Practical applications > Exercise 15.11: Solve real-world problems with angles
  - evidence quote: "### Exercise 15.11: Solve real-world problems with angles  1. Tinuke wants to buy clothes and is not sure where to find a good clothing shop in her town. She asks her friend Kemi for help.  Kemi: "Do you know remember w…"
- `ch15-b063-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 15: Angles > 15.4 Practical applications > Exercise 15.11: Solve real-world problems with angles
  - evidence quote: "### Exercise 15.11: Solve real-world problems with angles  2. Adanna wants to paint "NIGERIA" in big letters on a wall. She starts out with the "N" and paints the first two lines of the letter. Adanna still needs to pai…"
- `ch15-b063-i03c` [exercise_item] — placed in **review_items**
  - heading: Chapter 15: Angles > 15.4 Practical applications > Exercise 15.11: Solve real-world problems with angles
  - evidence quote: "### Exercise 15.11: Solve real-world problems with angles  3c. In the diagram below, what should the size of the angle marked $x$ be if $P\hat{R}S$ is equal to $120^{\circ}$?  Source image: https://electricbookworks.git…"
- `ch15-b064` [summary] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.5 Summary
  - evidence quote: "An angle is the amount of turn between two straight lines that have a common end point, called the vertex of the angle.  We use a protractor to measure angles in degrees. Always estimate an angle before you measure it,…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch15-b061/b062/b063-i01/i02/i03c are practical-application records from a different subtopic.
- **ao_no_evidence**: identify-adjacent-angles and identify-alternate-angles AOs have zero record_links; the linked corpus introduces these concepts in shared foundation but never separately exercises adjacent or alternate identification.
- **prerequisite_only_evidence**: identify-vertically-opposite-angles AO has only ch15-b032 (definition) and identify-corresponding-angles AO has only ch15-b043 (definition); the definitions are foundational but no worked example or exercise directly exercises identification for those AOs.
- **no_reused_assessment**: Multiple AOs have no reused exercise_item assessment.

### Per-atomic-objective evidence classification
- `identification-and-properties-of-special-angles-ao-identify-vertically-opposite-angles` → evidence: **prerequisite_only** · categories: prerequisite_only_evidence, no_reused_assessment
  - linked records: ch15-b032(foundation)
  - assessment: _(none anchored)_
- `identification-and-properties-of-special-angles-ao-identify-adjacent-angles` → evidence: **none** · categories: ao_no_evidence
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `identification-and-properties-of-special-angles-ao-identify-alternate-angles` → evidence: **none** · categories: ao_no_evidence
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `identification-and-properties-of-special-angles-ao-identify-corresponding-angles` → evidence: **prerequisite_only** · categories: prerequisite_only_evidence, no_reused_assessment
  - linked records: ch15-b043(foundation)
  - assessment: _(none anchored)_
- `identification-and-properties-of-special-angles-ao-state-properties-of-angles` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch15-b035(worked_example), ch15-b036-i01(exercise), ch15-b036-i02(exercise), ch15-b036-i03(exercise), ch15-b036-i04(exercise), ch15-b036-i05(exercise), ch15-b037(instruction), ch15-b038(worked_example), ch15-b039-i01(exercise), ch15-b039-i02(exercise), ch15-b039-i03(exercise), ch15-b039-i04(exercise), ch15-b039-i05(exercise), ch15-b045(worked_example), ch15-b046-i01(exercise), ch15-b046-i02(exercise), ch15-b046-i03(exercise), ch15-b048(worked_example), ch15-b050-i01(exercise), ch15-b050-i02(exercise), ch15-b050-i03(exercise), ch15-b050-i04(exercise), ch15-b050-i05(exercise), ch15-b052(worked_example), ch15-b054-i01(exercise), ch15-b054-i02(exercise), ch15-b054-i03(exercise), ch15-b056(worked_example), ch15-b057-i01(exercise), ch15-b057-i02(exercise), ch15-b059(worked_example), ch15-b060-i01(exercise), ch15-b060-i02(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All review_items were inspected. Candidate proposal added for real-world angle problems. Definitions of adjacent/alternate/corresponding/vertically opposite angles are not new candidates because they are already the row AO concepts.

### Candidate atomic objective proposals
- `special-angles-candidate-ao-solve-real-world-angle-problems` [extension_or_enrichment; candidate_for_expert_review]
  - proposed objective: Solve real-world problems involving angles.
  - source records: ch15-b061, ch15-b062, ch15-b063-i01, ch15-b063-i02, ch15-b063-i03c
  - closest existing AOs: identification-and-properties-of-special-angles-ao-state-properties-of-angles
  - candidate evidence quote: "apply our knowledge in real life."
  - rationale: The records apply angle relationships in real-world settings; they are not direct identification of the named special-angle types.

---

## `jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line`

**Title:** Identification and properties of angles at a point and angles on a straight line  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, ao_no_evidence, no_reused_assessment, curriculum_textbook_mismatch

### Curriculum objectives (source)
- `jss1-math-angles-identification-and-properties-of-angles-at-a-point-and-angles-on-a-straight-line-po01`: Identify angles at a point and angles on a straight line and state their properties

### Atomic objectives
- `angles-at-a-point-and-on-a-straight-line-ao-identify-angles-at-a-point` [identify/remember]: Identify angles at a point.
- `angles-at-a-point-and-on-a-straight-line-ao-identify-angles-on-a-straight-line` [identify/remember]: Identify angles on a straight line.
- `angles-at-a-point-and-on-a-straight-line-ao-state-properties-of-angles-at-a-point` [state/remember]: State the properties of angles at a point.
- `angles-at-a-point-and-on-a-straight-line-ao-state-properties-of-angles-on-a-straight-line` [state/remember]: State the properties of angles on a straight line.

### Linked textbook records (21 total) — inspected
- `ch15-b020` [exposition] — placed in **shared_foundation**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines
  - evidence quote: "You will need to be able to identify and measure angles on a straight line as well as angles formed by two intersecting lines. When you know the properties of these angles, you can use them to solve problems that involv…"
- `ch15-b021` [exposition] — placed in **shared_foundation**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Angles on a straight line
  - evidence quote: "A straight line is also called a straight angle. A straight angle is equal to $180^{\circ}$. If a straight line is formed by more than one angle, the sum of those angles will be $180^{\circ}$. We say the angles are **su…"
- `ch15-b022` [hint] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Angles on a straight line
  - evidence quote: "Adjacent angles do not always have to be supplementary. In the diagram below the two angles are adjacent, but they do not add up to $180^{\circ}$."
- `ch15-b023` [exposition] — placed in **shared_foundation**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Angles on a straight line
  - evidence quote: "Source diagram for the note above, showing adjacent angles that do not add up to $180^{\circ}$.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-026.png]"
- `ch15-b024` [definition] — placed in **shared_foundation**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Angles on a straight line
  - evidence quote: "**supplementary angles** Two (or more) angles are supplementary if they add up to $180^{\circ}$.  **adjacent angles** Adjacent angles are next to each other. Two adjacent angles share the same vertex and a common arm."
- `ch15-b025` [worked_example] — placed in **AO:angles-at-a-point-and-on-a-straight-line-ao-state-properties-of-angles-on-a-straight-line (worked_example)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Worked example 15.8: Calculating angles on a straight line
  - evidence quote: "Consider the diagram given below. You are given the following information:  - $\overset{\leftrightarrow}{ST}$ is a straight line - $a = 65^{\circ}$ - $b = 68^{\circ}$ - $c = x^{\circ}$  Diagram source image: https://ele…"
- `ch15-b026` [hint] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Angles on a straight line
  - evidence quote: "When we refer to lines and line segments we can use different notations:  - $\overline{EF}$ means the line segment from point $E$ to point $F$. - $\overset{\leftrightarrow}{EF}$ means the line through points $E$ and $F$…"
- `ch15-b027` [exercise_block] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.3: Calculate angles on a straight line
  - evidence quote: "### Exercise 15.3: Calculate angles on a straight line"
- `ch15-b027-i01` [exercise_item] — placed in **AO:angles-at-a-point-and-on-a-straight-line-ao-state-properties-of-angles-on-a-straight-line (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.3: Calculate angles on a straight line
  - evidence quote: "### Exercise 15.3: Calculate angles on a straight line  1. $YZ$ is a straight line, with angles as shown in the diagram below.  Diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/it…"
- `ch15-b027-i02` [exercise_item] — placed in **AO:angles-at-a-point-and-on-a-straight-line-ao-state-properties-of-angles-on-a-straight-line (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.3: Calculate angles on a straight line
  - evidence quote: "### Exercise 15.3: Calculate angles on a straight line  2. $YZ$ is a straight line, with angles as shown below.  Diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/…"
- `ch15-b027-i03` [exercise_item] — placed in **AO:angles-at-a-point-and-on-a-straight-line-ao-state-properties-of-angles-on-a-straight-line (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.3: Calculate angles on a straight line
  - evidence quote: "### Exercise 15.3: Calculate angles on a straight line  3. $ST$ is a straight line, with angles as shown below.  Diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/…"
- `ch15-b027-i04` [exercise_item] — placed in **AO:angles-at-a-point-and-on-a-straight-line-ao-state-properties-of-angles-on-a-straight-line (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.3: Calculate angles on a straight line
  - evidence quote: "### Exercise 15.3: Calculate angles on a straight line  4. Examine the diagram below, and answer the two questions that follow.  Diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/i…"
- `ch15-b027-i05` [exercise_item] — placed in **AO:angles-at-a-point-and-on-a-straight-line-ao-state-properties-of-angles-on-a-straight-line (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.3: Calculate angles on a straight line
  - evidence quote: "### Exercise 15.3: Calculate angles on a straight line  5. Examine the diagram below, and answer the questions that follow.  Diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items…"
- `ch15-b027-i06` [exercise_item] — placed in **AO:angles-at-a-point-and-on-a-straight-line-ao-state-properties-of-angles-on-a-straight-line (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.3: Calculate angles on a straight line
  - evidence quote: "### Exercise 15.3: Calculate angles on a straight line  6. Examine the diagram below, and answer the two questions that follow.  Diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/i…"
- `ch15-b027-i07` [exercise_item] — placed in **AO:angles-at-a-point-and-on-a-straight-line-ao-state-properties-of-angles-on-a-straight-line (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.3: Calculate angles on a straight line
  - evidence quote: "### Exercise 15.3: Calculate angles on a straight line  7. In the diagram below, line $YZ$ is a straight line with angles labelled above and below it.  Diagram source image: https://electricbookworks.github.io/siyavula-…"
- `ch15-b027-i08` [exercise_item] — placed in **AO:angles-at-a-point-and-on-a-straight-line-ao-state-properties-of-angles-on-a-straight-line (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.3: Calculate angles on a straight line
  - evidence quote: "### Exercise 15.3: Calculate angles on a straight line  8. In the diagram below, $YZ$ is a straight line with angles labelled above and below it.  Diagram source image: https://electricbookworks.github.io/siyavula-open-…"
- `ch15-b028` [note] — placed in **shared_foundation**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Angles on a straight line
  - evidence quote: "You will not usually be asked to redraw the diagram to give the missing angle size."
- `ch15-b061` [exposition] — placed in **review_items**
  - heading: Chapter 15: Angles > 15.4 Practical applications
  - evidence quote: "When we know about different angles and how they are formed we can apply our knowledge in real life. For example, we can use angles to describe the position of a shop, or how we want to paint decorations. Many people us…"
- `ch15-b063` [exercise_block] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.4 Practical applications > Exercise 15.11: Solve real-world problems with angles
  - evidence quote: "### Exercise 15.11: Solve real-world problems with angles"
- `ch15-b063-i03c` [exercise_item] — placed in **review_items**
  - heading: Chapter 15: Angles > 15.4 Practical applications > Exercise 15.11: Solve real-world problems with angles
  - evidence quote: "### Exercise 15.11: Solve real-world problems with angles  3c. In the diagram below, what should the size of the angle marked $x$ be if $P\hat{R}S$ is equal to $120^{\circ}$?  Source image: https://electricbookworks.git…"
- `ch15-b064` [summary] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.5 Summary
  - evidence quote: "An angle is the amount of turn between two straight lines that have a common end point, called the vertex of the angle.  We use a protractor to measure angles in degrees. Always estimate an angle before you measure it,…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch15-b061 and ch15-b063-i03c are real-world records from a different subtopic.
- **ao_no_evidence**: identify-angles-at-a-point, identify-angles-on-a-straight-line, and state-properties-of-angles-at-a-point AOs have zero record_links; only state-properties-of-angles-on-a-straight-line is supported.
- **no_reused_assessment**: The state-properties-on-a-straight-line AO has direct exercises but no reused assessment.
- **curriculum_textbook_mismatch**: The textbook section linked here (ch15.2 angles on a straight line) does not cover angles at a point as a separate topic, leaving the at-a-point AOs unsupported.

### Per-atomic-objective evidence classification
- `angles-at-a-point-and-on-a-straight-line-ao-identify-angles-at-a-point` → evidence: **none** · categories: ao_no_evidence, curriculum_textbook_mismatch
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `angles-at-a-point-and-on-a-straight-line-ao-identify-angles-on-a-straight-line` → evidence: **none** · categories: ao_no_evidence
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `angles-at-a-point-and-on-a-straight-line-ao-state-properties-of-angles-at-a-point` → evidence: **none** · categories: ao_no_evidence, curriculum_textbook_mismatch
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `angles-at-a-point-and-on-a-straight-line-ao-state-properties-of-angles-on-a-straight-line` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch15-b025(worked_example), ch15-b027-i01(exercise), ch15-b027-i02(exercise), ch15-b027-i03(exercise), ch15-b027-i04(exercise), ch15-b027-i05(exercise), ch15-b027-i06(exercise), ch15-b027-i07(exercise), ch15-b027-i08(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All review_items were inspected. Candidate proposal added for real-world angle problems. The missing angles-at-a-point records are not candidate AOs because they are absent from the linked textbook records, not extra textbook skills.

### Candidate atomic objective proposals
- `angles-at-point-straight-line-candidate-ao-solve-real-world-angle-problems` [extension_or_enrichment; candidate_for_expert_review]
  - proposed objective: Solve real-world problems involving angles.
  - source records: ch15-b061, ch15-b063-i03c
  - closest existing AOs: angles-at-a-point-and-on-a-straight-line-ao-state-properties-of-angles-on-a-straight-line
  - candidate evidence quote: "apply our knowledge in real life."
  - rationale: The records apply angle facts to real-world problems rather than identifying or stating properties of angles at a point or on a straight line.

---

## `jss1-math-angles-supplementary-and-complementary-angles`

**Title:** Supplementary and complementary angles  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, ao_no_evidence, prerequisite_only_evidence, no_reused_assessment, curriculum_textbook_mismatch

### Curriculum objectives (source)
- `jss1-math-angles-supplementary-and-complementary-angles-po01`: Define supplementary angles and complementary angles
- `jss1-math-angles-supplementary-and-complementary-angles-po02`: Calculate the supplement or complement of a given angle

### Atomic objectives
- `supplementary-and-complementary-angles-ao-define-supplementary-angles` [define/remember]: Define supplementary angles.
- `supplementary-and-complementary-angles-ao-define-complementary-angles` [define/remember]: Define complementary angles.
- `supplementary-and-complementary-angles-ao-calculate-supplement` [calculate/apply]: Calculate the supplement of a given angle.
- `supplementary-and-complementary-angles-ao-calculate-complement` [calculate/apply]: Calculate the complement of a given angle.

### Linked textbook records (18 total) — inspected
- `ch15-b021` [exposition] — placed in **shared_foundation**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Angles on a straight line
  - evidence quote: "A straight line is also called a straight angle. A straight angle is equal to $180^{\circ}$. If a straight line is formed by more than one angle, the sum of those angles will be $180^{\circ}$. We say the angles are **su…"
- `ch15-b022` [hint] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Angles on a straight line
  - evidence quote: "Adjacent angles do not always have to be supplementary. In the diagram below the two angles are adjacent, but they do not add up to $180^{\circ}$."
- `ch15-b023` [exposition] — placed in **shared_foundation**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Angles on a straight line
  - evidence quote: "Source diagram for the note above, showing adjacent angles that do not add up to $180^{\circ}$.  [Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-15-026.png]"
- `ch15-b024` [definition] — placed in **AO:supplementary-and-complementary-angles-ao-define-supplementary-angles (foundation)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Angles on a straight line
  - evidence quote: "**supplementary angles** Two (or more) angles are supplementary if they add up to $180^{\circ}$.  **adjacent angles** Adjacent angles are next to each other. Two adjacent angles share the same vertex and a common arm."
- `ch15-b025` [worked_example] — placed in **AO:supplementary-and-complementary-angles-ao-calculate-supplement (worked_example)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Worked example 15.8: Calculating angles on a straight line
  - evidence quote: "Consider the diagram given below. You are given the following information:  - $\overset{\leftrightarrow}{ST}$ is a straight line - $a = 65^{\circ}$ - $b = 68^{\circ}$ - $c = x^{\circ}$  Diagram source image: https://ele…"
- `ch15-b026` [hint] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Angles on a straight line
  - evidence quote: "When we refer to lines and line segments we can use different notations:  - $\overline{EF}$ means the line segment from point $E$ to point $F$. - $\overset{\leftrightarrow}{EF}$ means the line through points $E$ and $F$…"
- `ch15-b027` [exercise_block] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.3: Calculate angles on a straight line
  - evidence quote: "### Exercise 15.3: Calculate angles on a straight line"
- `ch15-b027-i01` [exercise_item] — placed in **AO:supplementary-and-complementary-angles-ao-calculate-supplement (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.3: Calculate angles on a straight line
  - evidence quote: "### Exercise 15.3: Calculate angles on a straight line  1. $YZ$ is a straight line, with angles as shown in the diagram below.  Diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/it…"
- `ch15-b027-i02` [exercise_item] — placed in **AO:supplementary-and-complementary-angles-ao-calculate-supplement (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.3: Calculate angles on a straight line
  - evidence quote: "### Exercise 15.3: Calculate angles on a straight line  2. $YZ$ is a straight line, with angles as shown below.  Diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/…"
- `ch15-b027-i03` [exercise_item] — placed in **AO:supplementary-and-complementary-angles-ao-calculate-supplement (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.3: Calculate angles on a straight line
  - evidence quote: "### Exercise 15.3: Calculate angles on a straight line  3. $ST$ is a straight line, with angles as shown below.  Diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/…"
- `ch15-b027-i04` [exercise_item] — placed in **AO:supplementary-and-complementary-angles-ao-calculate-supplement (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.3: Calculate angles on a straight line
  - evidence quote: "### Exercise 15.3: Calculate angles on a straight line  4. Examine the diagram below, and answer the two questions that follow.  Diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/i…"
- `ch15-b027-i05` [exercise_item] — placed in **AO:supplementary-and-complementary-angles-ao-calculate-supplement (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.3: Calculate angles on a straight line
  - evidence quote: "### Exercise 15.3: Calculate angles on a straight line  5. Examine the diagram below, and answer the questions that follow.  Diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items…"
- `ch15-b027-i06` [exercise_item] — placed in **AO:supplementary-and-complementary-angles-ao-calculate-supplement (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.3: Calculate angles on a straight line
  - evidence quote: "### Exercise 15.3: Calculate angles on a straight line  6. Examine the diagram below, and answer the two questions that follow.  Diagram source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/i…"
- `ch15-b027-i07` [exercise_item] — placed in **AO:supplementary-and-complementary-angles-ao-calculate-supplement (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.3: Calculate angles on a straight line
  - evidence quote: "### Exercise 15.3: Calculate angles on a straight line  7. In the diagram below, line $YZ$ is a straight line with angles labelled above and below it.  Diagram source image: https://electricbookworks.github.io/siyavula-…"
- `ch15-b027-i08` [exercise_item] — placed in **AO:supplementary-and-complementary-angles-ao-calculate-supplement (exercise)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Exercise 15.3: Calculate angles on a straight line
  - evidence quote: "### Exercise 15.3: Calculate angles on a straight line  8. In the diagram below, $YZ$ is a straight line with angles labelled above and below it.  Diagram source image: https://electricbookworks.github.io/siyavula-open-…"
- `ch15-b028` [note] — placed in **AO:supplementary-and-complementary-angles-ao-calculate-supplement (instruction)**
  - heading: Chapter 15: Angles > 15.2 Angles on straight and intersecting lines > Angles on a straight line
  - evidence quote: "You will not usually be asked to redraw the diagram to give the missing angle size."
- `ch15-b063-i03c` [exercise_item] — placed in **review_items**
  - heading: Chapter 15: Angles > 15.4 Practical applications > Exercise 15.11: Solve real-world problems with angles
  - evidence quote: "### Exercise 15.11: Solve real-world problems with angles  3c. In the diagram below, what should the size of the angle marked $x$ be if $P\hat{R}S$ is equal to $120^{\circ}$?  Source image: https://electricbookworks.git…"
- `ch15-b064` [summary] — placed in **excluded**
  - heading: Chapter 15: Angles > 15.5 Summary
  - evidence quote: "An angle is the amount of turn between two straight lines that have a common end point, called the vertex of the angle.  We use a protractor to measure angles in degrees. Always estimate an angle before you measure it,…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch15-b063-i03c is a real-world angle problem outside the supplement/complement scope.
- **ao_no_evidence**: define-complementary-angles and calculate-complement AOs have zero record_links; the linked records cover only supplementary angles.
- **prerequisite_only_evidence**: define-supplementary-angles AO has only the definition record ch15-b024; the definition is foundational but no exercise_item directly asks the student to state or recall the supplementary definition.
- **no_reused_assessment**: The calculate-supplement AO has direct exercises and the define-supplementary AO has the definition, but no reused exercise_item assessment is anchored.
- **curriculum_textbook_mismatch**: Complementary angles are not covered in the linked Chapter 15 records for this subtopic.

### Per-atomic-objective evidence classification
- `supplementary-and-complementary-angles-ao-define-supplementary-angles` → evidence: **prerequisite_only** · categories: prerequisite_only_evidence, no_reused_assessment
  - linked records: ch15-b024(foundation)
  - assessment: _(none anchored)_
- `supplementary-and-complementary-angles-ao-define-complementary-angles` → evidence: **none** · categories: ao_no_evidence, curriculum_textbook_mismatch
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `supplementary-and-complementary-angles-ao-calculate-supplement` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch15-b025(worked_example), ch15-b027-i01(exercise), ch15-b027-i02(exercise), ch15-b027-i03(exercise), ch15-b027-i04(exercise), ch15-b027-i05(exercise), ch15-b027-i06(exercise), ch15-b027-i07(exercise), ch15-b027-i08(exercise), ch15-b028(instruction)
  - assessment: _(none anchored)_
- `supplementary-and-complementary-angles-ao-calculate-complement` → evidence: **none** · categories: ao_no_evidence, curriculum_textbook_mismatch
  - linked records: _(none)_
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-angles-sum-of-angles-of-a-triangle`

**Title:** Sum of angles of a triangle  
**Status:** `no_records`  
**Row review categories:** corpus_gap

### Curriculum objectives (source)
- `jss1-math-angles-sum-of-angles-of-a-triangle-po01`: State that the sum of angles of a triangle is 180 degrees
- `jss1-math-angles-sum-of-angles-of-a-triangle-po02`: Calculate a missing angle in a triangle given the other angles

### Atomic objectives
- `sum-of-angles-of-a-triangle-ao-state-sum-of-angles` [state/remember]: State that the sum of angles of a triangle is 180 degrees.
- `sum-of-angles-of-a-triangle-ao-calculate-missing-angle` [calculate/apply]: Calculate a missing angle in a triangle given the other angles.

### Linked textbook records (0 total) — inspected
_No textbook records are linked to this subtopic (corpus_gap)._

### Row-level review categories and manually authored reasons
- **corpus_gap**: No textbook records are linked to this subtopic in the linked corpus.

### Per-atomic-objective evidence classification
- `sum-of-angles-of-a-triangle-ao-state-sum-of-angles` → evidence: **none** · categories: corpus_gap
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `sum-of-angles-of-a-triangle-ao-calculate-missing-angle` → evidence: **none** · categories: corpus_gap
  - linked records: _(none)_
  - assessment: _(none anchored)_

---

## `jss1-math-need-for-statistics-purposes-of-statistics`

**Title:** Purposes of statistics  
**Status:** `needs_review`  
**Row review categories:** prerequisite_only_evidence, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-need-for-statistics-purposes-of-statistics-po01`: List purposes of statistics

### Atomic objectives
- `purposes-of-statistics-ao-list-purposes` [list/remember]: List purposes of statistics.

### Linked textbook records (41 total) — inspected
- `ch16-b001` [exposition] — placed in **AO:purposes-of-statistics-ao-list-purposes (instruction)**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics
  - evidence quote: "Statistics keeps us informed about what is happening in the world around us. Some examples of how statistics are useful are listed below.  - Weather information is given in newspapers, on the radio, on television and on…"
- `ch16-b002` [exposition] — placed in **shared_foundation**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Statistical data
  - evidence quote: "The first step in doing statistical work is to decide what it is you want to find out about. The next thing you do is plan how you are going to gather enough information so you can find out what you want to know. The in…"
- `ch16-b003` [note] — placed in **shared_foundation**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Statistical data
  - evidence quote: "If data is collected from a number of people, we say that we have surveyed the people. We "do a survey" to collect information from the people, such as where all the students in a school live."
- `ch16-b004` [definition] — placed in **shared_foundation**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Statistical data
  - evidence quote: "**data** Data is information in the form of facts, such as numbers, measurements or observations.  **collecting data** Collecting data is gathering together and recording the information needed.  **analysing data** Anal…"
- `ch16-b005` [worked_example] — placed in **AO:purposes-of-statistics-ao-list-purposes (worked_example)**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Worked example 16.1: Analysing data given in a table
  - evidence quote: "A researcher wanted to compare the numbers of female and male teachers at different schools. She did a survey to find out the number of male and female teachers there were in six different schools. She recorded the resu…"
- `ch16-b006` [exercise_block] — placed in **excluded**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Exercise 16.1: Analyse data given in a table
  - evidence quote: "### Exercise 16.1: Analyse data given in a table"
- `ch16-b006-i01` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Exercise 16.1: Analyse data given in a table
  - evidence quote: "### Exercise 16.1: Analyse data given in a table  You surveyed the students in your class at school to find out whether they preferred fruit juice, lemonade, orange fizz or cola.  The table shows the results of your sur…"
- `ch16-b006-i02` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Exercise 16.1: Analyse data given in a table
  - evidence quote: "### Exercise 16.1: Analyse data given in a table  You surveyed the students in your class at school to find out whether they preferred fruit juice, lemonade, orange fizz or cola.  The table shows the results of your sur…"
- `ch16-b006-i03` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Exercise 16.1: Analyse data given in a table
  - evidence quote: "### Exercise 16.1: Analyse data given in a table  You surveyed the students in your class at school to find out whether they preferred fruit juice, lemonade, orange fizz or cola.  The table shows the results of your sur…"
- `ch16-b006-i04` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Exercise 16.1: Analyse data given in a table
  - evidence quote: "### Exercise 16.1: Analyse data given in a table  You surveyed the students in your class at school to find out whether they preferred fruit juice, lemonade, orange fizz or cola.  The table shows the results of your sur…"
- `ch16-b006-i05` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Exercise 16.1: Analyse data given in a table
  - evidence quote: "### Exercise 16.1: Analyse data given in a table  The students in your class were surveyed to find out what size shoe they wear.  The results were organised into the following table.  | Shoe size | Total number | | ---:…"
- `ch16-b006-i06` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Exercise 16.1: Analyse data given in a table
  - evidence quote: "### Exercise 16.1: Analyse data given in a table  The students in your class were surveyed to find out what size shoe they wear.  The results were organised into the following table.  | Shoe size | Total number | | ---:…"
- `ch16-b006-i07` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Exercise 16.1: Analyse data given in a table
  - evidence quote: "### Exercise 16.1: Analyse data given in a table  The students in your class were surveyed to find out what size shoe they wear.  The results were organised into the following table.  | Shoe size | Total number | | ---:…"
- `ch16-b006-i08` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Exercise 16.1: Analyse data given in a table
  - evidence quote: "### Exercise 16.1: Analyse data given in a table  The students in your class were surveyed to find out what size shoe they wear.  The results were organised into the following table.  | Shoe size | Total number | | ---:…"
- `ch16-b007` [exposition] — placed in **shared_foundation**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Sources of statistical information
  - evidence quote: "One source of statistical information would be the results of a survey. A second source of statistical information is the newspaper and another source of statistical information is the internet.  - Information about the…"
- `ch16-b008` [worked_example] — placed in **AO:purposes-of-statistics-ao-list-purposes (worked_example)**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Worked example 16.2: Analysing statistical data about age groups
  - evidence quote: "Erioluwa found the following information about the Nigerian population on the Nigerian National Bureau of Statistics website. The table gives statistics about the percentage of the Nigerian population in the given five…"
- `ch16-b009` [exercise_block] — placed in **excluded**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Exercise 16.2: Analyse statistical data given in a table
  - evidence quote: "### Exercise 16.2: Analyse statistical data given in a table"
- `ch16-b009-i01a` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Exercise 16.2: Analyse statistical data given in a table
  - evidence quote: "### Exercise 16.2: Analyse statistical data given in a table  1. Chidi sourced information about the top eight causes of death in Nigeria from a survey published by the Centre for Disease Control and Prevention in 2013.…"
- `ch16-b009-i01b` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Exercise 16.2: Analyse statistical data given in a table
  - evidence quote: "### Exercise 16.2: Analyse statistical data given in a table  1. Chidi sourced information about the top eight causes of death in Nigeria from a survey published by the Centre for Disease Control and Prevention in 2013.…"
- `ch16-b009-i01c` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Exercise 16.2: Analyse statistical data given in a table
  - evidence quote: "### Exercise 16.2: Analyse statistical data given in a table  1. Chidi sourced information about the top eight causes of death in Nigeria from a survey published by the Centre for Disease Control and Prevention in 2013.…"
- `ch16-b009-i02a` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Exercise 16.2: Analyse statistical data given in a table
  - evidence quote: "### Exercise 16.2: Analyse statistical data given in a table  2. Abiodun wanted to know how the Lion, Leopard and Elephant Football teams were doing in the Nigerian Football League. He found the following table of resul…"
- `ch16-b009-i02b` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Exercise 16.2: Analyse statistical data given in a table
  - evidence quote: "### Exercise 16.2: Analyse statistical data given in a table  2. Abiodun wanted to know how the Lion, Leopard and Elephant Football teams were doing in the Nigerian Football League. He found the following table of resul…"
- `ch16-b009-i02c` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Exercise 16.2: Analyse statistical data given in a table
  - evidence quote: "### Exercise 16.2: Analyse statistical data given in a table  2. Abiodun wanted to know how the Lion, Leopard and Elephant Football teams were doing in the Nigerian Football League. He found the following table of resul…"
- `ch16-b009-i02d` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Exercise 16.2: Analyse statistical data given in a table
  - evidence quote: "### Exercise 16.2: Analyse statistical data given in a table  2. Abiodun wanted to know how the Lion, Leopard and Elephant Football teams were doing in the Nigerian Football League. He found the following table of resul…"
- `ch16-b009-i02e` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Exercise 16.2: Analyse statistical data given in a table
  - evidence quote: "### Exercise 16.2: Analyse statistical data given in a table  2. Abiodun wanted to know how the Lion, Leopard and Elephant Football teams were doing in the Nigerian Football League. He found the following table of resul…"
- `ch16-b009-i02f` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Exercise 16.2: Analyse statistical data given in a table
  - evidence quote: "### Exercise 16.2: Analyse statistical data given in a table  2. Abiodun wanted to know how the Lion, Leopard and Elephant Football teams were doing in the Nigerian Football League. He found the following table of resul…"
- `ch16-b009-i02g` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.1 The purposes of statistics > Exercise 16.2: Analyse statistical data given in a table
  - evidence quote: "### Exercise 16.2: Analyse statistical data given in a table  2. Abiodun wanted to know how the Lion, Leopard and Elephant Football teams were doing in the Nigerian Football League. He found the following table of resul…"
- `ch16-b014` [exposition] — placed in **AO:purposes-of-statistics-ao-list-purposes (instruction)**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Using statistics for predictions
  - evidence quote: "We can use statistics to help us with the planning of a project or a task. It can help us with financial decisions or with buying the correct stock for a business.  Writing statistics in a table often helps when it come…"
- `ch16-b015` [worked_example] — placed in **AO:purposes-of-statistics-ao-list-purposes (worked_example)**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Worked example 16.4: Using a table to predict and plan
  - evidence quote: "Adija sells Agege bread in large loaves and small loaves from her stall. Every day, she buys 24 large loaves and 24 small loaves from the bakery.  Adija finds that she has several loaves of bread each day that she has n…"
- `ch16-b016` [exercise_block] — placed in **excluded**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Exercise 16.4: Use statistics given in a table to predict and plan
  - evidence quote: "### Exercise 16.4: Use statistics given in a table to predict and plan"
- `ch16-b016-i01a` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Exercise 16.4: Use statistics given in a table to predict and plan
  - evidence quote: "### Exercise 16.4: Use statistics given in a table to predict and plan  1. A stationery shop kept a record of the number of exercise books it sold in a week, as well as the total profit it made on the sale of these exer…"
- `ch16-b016-i01b` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Exercise 16.4: Use statistics given in a table to predict and plan
  - evidence quote: "### Exercise 16.4: Use statistics given in a table to predict and plan  1. A stationery shop kept a record of the number of exercise books it sold in a week, as well as the total profit it made on the sale of these exer…"
- `ch16-b016-i01c` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Exercise 16.4: Use statistics given in a table to predict and plan
  - evidence quote: "### Exercise 16.4: Use statistics given in a table to predict and plan  1. A stationery shop kept a record of the number of exercise books it sold in a week, as well as the total profit it made on the sale of these exer…"
- `ch16-b016-i01d` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Exercise 16.4: Use statistics given in a table to predict and plan
  - evidence quote: "### Exercise 16.4: Use statistics given in a table to predict and plan  1. A stationery shop kept a record of the number of exercise books it sold in a week, as well as the total profit it made on the sale of these exer…"
- `ch16-b016-i01e` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Exercise 16.4: Use statistics given in a table to predict and plan
  - evidence quote: "### Exercise 16.4: Use statistics given in a table to predict and plan  1. A stationery shop kept a record of the number of exercise books it sold in a week, as well as the total profit it made on the sale of these exer…"
- `ch16-b016-i01f` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Exercise 16.4: Use statistics given in a table to predict and plan
  - evidence quote: "### Exercise 16.4: Use statistics given in a table to predict and plan  1. A stationery shop kept a record of the number of exercise books it sold in a week, as well as the total profit it made on the sale of these exer…"
- `ch16-b016-i02a` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Exercise 16.4: Use statistics given in a table to predict and plan
  - evidence quote: "### Exercise 16.4: Use statistics given in a table to predict and plan  2. This table shows some of the items sold in the local shop on a particular day, the number of each item sold that day, the price per item and the…"
- `ch16-b016-i02b` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Exercise 16.4: Use statistics given in a table to predict and plan
  - evidence quote: "### Exercise 16.4: Use statistics given in a table to predict and plan  2. This table shows some of the items sold in the local shop on a particular day, the number of each item sold that day, the price per item and the…"
- `ch16-b016-i02c` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Exercise 16.4: Use statistics given in a table to predict and plan
  - evidence quote: "### Exercise 16.4: Use statistics given in a table to predict and plan  2. This table shows some of the items sold in the local shop on a particular day, the number of each item sold that day, the price per item and the…"
- `ch16-b016-i02d` [exercise_item] — placed in **AO:purposes-of-statistics-ao-list-purposes (exercise)**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Exercise 16.4: Use statistics given in a table to predict and plan
  - evidence quote: "### Exercise 16.4: Use statistics given in a table to predict and plan  2. This table shows some of the items sold in the local shop on a particular day, the number of each item sold that day, the price per item and the…"
- `ch16-b017` [summary] — placed in **excluded**
  - heading: Chapter 16: Need for statistics > 16.4 Summary
  - evidence quote: "- Statistics keeps us informed about what is happening in the world around us. - Statistics can be given in table form. We can analyse these statistics in order to draw conclusions about the information given. - Governm…"

### Row-level review categories and manually authored reasons
- **prerequisite_only_evidence**: The AO is 'list purposes of statistics' (recall). Only ch16-b001 directly enumerates purposes; the worked examples (ch16-b005, b008, b015) and exercises (ch16-b006-i*, b009-i*, b016-i*) ask the student to analyse data tables or use statistics for prediction — applied skills rather than recall of the purposes themselves.
- **no_reused_assessment**: The reused assessment selected from ch16-b006-i03 asks the student to analyse a data table; this is not an AO-aligned 'list purposes of statistics' assessment.

### Per-atomic-objective evidence classification
- `purposes-of-statistics-ao-list-purposes` → evidence: **prerequisite_only** · categories: prerequisite_only_evidence, no_reused_assessment
  - linked records: ch16-b001(instruction), ch16-b005(worked_example), ch16-b006-i01(exercise), ch16-b006-i02(exercise), ch16-b006-i03(exercise), ch16-b006-i04(exercise), ch16-b006-i05(exercise), ch16-b006-i06(exercise), ch16-b006-i07(exercise), ch16-b006-i08(exercise), ch16-b008(worked_example), ch16-b009-i01a(exercise), ch16-b009-i01b(exercise), ch16-b009-i01c(exercise), ch16-b009-i02a(exercise), ch16-b009-i02b(exercise), ch16-b009-i02c(exercise), ch16-b009-i02d(exercise), ch16-b009-i02e(exercise), ch16-b009-i02f(exercise), ch16-b009-i02g(exercise), ch16-b014(instruction), ch16-b015(worked_example), ch16-b016-i01a(exercise), ch16-b016-i01b(exercise), ch16-b016-i01c(exercise), ch16-b016-i01d(exercise), ch16-b016-i01e(exercise), ch16-b016-i01f(exercise), ch16-b016-i02a(exercise), ch16-b016-i02b(exercise), ch16-b016-i02c(exercise), ch16-b016-i02d(exercise)
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All linked records were inspected. Candidate proposals retained for table analysis and prediction/planning records because they are applied statistical skills, not direct evidence for the recall AO.

### Candidate atomic objective proposals
- `purposes-of-statistics-candidate-ao-analyse-statistical-data-tables` [extension_or_enrichment; candidate_for_expert_review]
  - proposed objective: Analyse statistical data given in tables.
  - source records: ch16-b005, ch16-b006-i01, ch16-b006-i02, ch16-b006-i03, ch16-b006-i04, ch16-b006-i05, ch16-b006-i06, ch16-b006-i07, ch16-b006-i08, ch16-b008, ch16-b009-i01a, ch16-b009-i01b, ch16-b009-i01c, ch16-b009-i02a, ch16-b009-i02b, ch16-b009-i02c, ch16-b009-i02d, ch16-b009-i02e, ch16-b009-i02f, ch16-b009-i02g
  - closest existing AOs: purposes-of-statistics-ao-list-purposes
  - candidate evidence quote: "A researcher wanted to compare the numbers of female and male teachers at different schools."
  - rationale: These records require reading and analysing statistical tables. They demonstrate a use of statistics but do not ask the learner to list purposes.
- `purposes-of-statistics-candidate-ao-use-statistics-to-predict-and-plan` [extension_or_enrichment; candidate_for_expert_review]
  - proposed objective: Use statistics given in tables to predict and plan.
  - source records: ch16-b014, ch16-b015, ch16-b016-i01a, ch16-b016-i01b, ch16-b016-i01c, ch16-b016-i01d, ch16-b016-i01e, ch16-b016-i01f, ch16-b016-i02a, ch16-b016-i02b, ch16-b016-i02c, ch16-b016-i02d
  - closest existing AOs: purposes-of-statistics-ao-list-purposes
  - candidate evidence quote: "We can use statistics to help us with the planning of a project or a task."
  - rationale: These records ask learners to use statistical tables for prediction and planning. That is an applied objective, not a recall objective about purposes.

---

## `jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes`

**Title:** Need for collecting data for planning purposes  
**Status:** `mapped`  
**Row review categories:** _(none — mapped or no-records baseline)_

### Curriculum objectives (source)
- `jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes-po01`: Recognise the usefulness of statistics for planning purposes
- `jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes-po02`: Apply the occurrence of chance events / application of probabilities in everyday life
- `jss1-math-need-for-statistics-need-for-collecting-data-for-planning-purposes-po03`: Recognise the usefulness of statistics for prediction purposes

### Atomic objectives
- `need-for-collecting-data-for-planning-purposes-ao-recognise-usefulness-for-planning` [recognise/remember]: Recognise the usefulness of statistics for planning purposes.
- `need-for-collecting-data-for-planning-purposes-ao-apply-chance-events-and-probabilities` [apply/apply]: Apply the occurrence of chance events / application of probabilities in everyday life.
- `need-for-collecting-data-for-planning-purposes-ao-recognise-usefulness-for-prediction` [recognise/remember]: Recognise the usefulness of statistics for prediction purposes.

### Linked textbook records (24 total) — inspected
- `ch16-b010` [exposition] — placed in **AO:need-for-collecting-data-for-planning-purposes-ao-apply-chance-events-and-probabilities (instruction)**
  - heading: Chapter 16: Need for statistics > 16.2 Introduction to probability
  - evidence quote: "Probability is the study of the laws of chance. It is about how probable or how likely it is that something will happen.  We often use the word "chance" when we are talking about probability, for example, "I have no cha…"
- `ch16-b011` [exposition] — placed in **AO:need-for-collecting-data-for-planning-purposes-ao-apply-chance-events-and-probabilities (instruction)**
  - heading: Chapter 16: Need for statistics > 16.2 Introduction to probability > The probability scale
  - evidence quote: "To describe the probability that something will happen, we can use a probability scale.  The probability scale is a line that starts with impossible events at the left-hand end and ends with certain events at the right-…"
- `ch16-b012` [worked_example] — placed in **AO:need-for-collecting-data-for-planning-purposes-ao-apply-chance-events-and-probabilities (worked_example)**
  - heading: Chapter 16: Need for statistics > 16.2 Introduction to probability > Worked example 16.3: Using the probability scale to describe probability
  - evidence quote: "Use the probability scale to find a word description for each of the events listed below.  Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss2-15-1_016.png  1. Wh…"
- `ch16-b013` [exercise_block] — placed in **excluded**
  - heading: Chapter 16: Need for statistics > 16.2 Introduction to probability > Exercise 16.3: Use the probability scale to describe probability
  - evidence quote: "### Exercise 16.3: Use the probability scale to describe probability  Use the probability scale to give each of these events a word description from the scale.  Source image: https://electricbookworks.github.io/siyavula…"
- `ch16-b013-i01` [exercise_item] — placed in **AO:need-for-collecting-data-for-planning-purposes-ao-apply-chance-events-and-probabilities (exercise)**
  - heading: Chapter 16: Need for statistics > 16.2 Introduction to probability > Exercise 16.3: Use the probability scale to describe probability
  - evidence quote: "### Exercise 16.3: Use the probability scale to describe probability  Use the probability scale to give each of these events a word description from the scale.  Source image: https://electricbookworks.github.io/siyavula…"
- `ch16-b013-i02` [exercise_item] — placed in **AO:need-for-collecting-data-for-planning-purposes-ao-apply-chance-events-and-probabilities (exercise)**
  - heading: Chapter 16: Need for statistics > 16.2 Introduction to probability > Exercise 16.3: Use the probability scale to describe probability
  - evidence quote: "### Exercise 16.3: Use the probability scale to describe probability  Use the probability scale to give each of these events a word description from the scale.  Source image: https://electricbookworks.github.io/siyavula…"
- `ch16-b013-i03` [exercise_item] — placed in **AO:need-for-collecting-data-for-planning-purposes-ao-apply-chance-events-and-probabilities (exercise)**
  - heading: Chapter 16: Need for statistics > 16.2 Introduction to probability > Exercise 16.3: Use the probability scale to describe probability
  - evidence quote: "### Exercise 16.3: Use the probability scale to describe probability  Use the probability scale to give each of these events a word description from the scale.  Source image: https://electricbookworks.github.io/siyavula…"
- `ch16-b013-i04` [exercise_item] — placed in **AO:need-for-collecting-data-for-planning-purposes-ao-apply-chance-events-and-probabilities (exercise)**
  - heading: Chapter 16: Need for statistics > 16.2 Introduction to probability > Exercise 16.3: Use the probability scale to describe probability
  - evidence quote: "### Exercise 16.3: Use the probability scale to describe probability  Use the probability scale to give each of these events a word description from the scale.  Source image: https://electricbookworks.github.io/siyavula…"
- `ch16-b013-i05` [exercise_item] — placed in **AO:need-for-collecting-data-for-planning-purposes-ao-apply-chance-events-and-probabilities (exercise)**
  - heading: Chapter 16: Need for statistics > 16.2 Introduction to probability > Exercise 16.3: Use the probability scale to describe probability
  - evidence quote: "### Exercise 16.3: Use the probability scale to describe probability  Use the probability scale to give each of these events a word description from the scale.  Source image: https://electricbookworks.github.io/siyavula…"
- `ch16-b013-i06` [exercise_item] — placed in **AO:need-for-collecting-data-for-planning-purposes-ao-apply-chance-events-and-probabilities (exercise)**
  - heading: Chapter 16: Need for statistics > 16.2 Introduction to probability > Exercise 16.3: Use the probability scale to describe probability
  - evidence quote: "### Exercise 16.3: Use the probability scale to describe probability  Use the probability scale to give each of these events a word description from the scale.  Source image: https://electricbookworks.github.io/siyavula…"
- `ch16-b014` [exposition] — placed in **AO:need-for-collecting-data-for-planning-purposes-ao-recognise-usefulness-for-planning (instruction)**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Using statistics for predictions
  - evidence quote: "We can use statistics to help us with the planning of a project or a task. It can help us with financial decisions or with buying the correct stock for a business.  Writing statistics in a table often helps when it come…"
- `ch16-b015` [worked_example] — placed in **AO:need-for-collecting-data-for-planning-purposes-ao-recognise-usefulness-for-planning (worked_example)**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Worked example 16.4: Using a table to predict and plan
  - evidence quote: "Adija sells Agege bread in large loaves and small loaves from her stall. Every day, she buys 24 large loaves and 24 small loaves from the bakery.  Adija finds that she has several loaves of bread each day that she has n…"
- `ch16-b016` [exercise_block] — placed in **excluded**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Exercise 16.4: Use statistics given in a table to predict and plan
  - evidence quote: "### Exercise 16.4: Use statistics given in a table to predict and plan"
- `ch16-b016-i01a` [exercise_item] — placed in **AO:need-for-collecting-data-for-planning-purposes-ao-recognise-usefulness-for-planning (exercise)**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Exercise 16.4: Use statistics given in a table to predict and plan
  - evidence quote: "### Exercise 16.4: Use statistics given in a table to predict and plan  1. A stationery shop kept a record of the number of exercise books it sold in a week, as well as the total profit it made on the sale of these exer…"
- `ch16-b016-i01b` [exercise_item] — placed in **AO:need-for-collecting-data-for-planning-purposes-ao-recognise-usefulness-for-planning (exercise)**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Exercise 16.4: Use statistics given in a table to predict and plan
  - evidence quote: "### Exercise 16.4: Use statistics given in a table to predict and plan  1. A stationery shop kept a record of the number of exercise books it sold in a week, as well as the total profit it made on the sale of these exer…"
- `ch16-b016-i01c` [exercise_item] — placed in **AO:need-for-collecting-data-for-planning-purposes-ao-recognise-usefulness-for-planning (exercise)**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Exercise 16.4: Use statistics given in a table to predict and plan
  - evidence quote: "### Exercise 16.4: Use statistics given in a table to predict and plan  1. A stationery shop kept a record of the number of exercise books it sold in a week, as well as the total profit it made on the sale of these exer…"
- `ch16-b016-i01d` [exercise_item] — placed in **AO:need-for-collecting-data-for-planning-purposes-ao-recognise-usefulness-for-planning (exercise)**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Exercise 16.4: Use statistics given in a table to predict and plan
  - evidence quote: "### Exercise 16.4: Use statistics given in a table to predict and plan  1. A stationery shop kept a record of the number of exercise books it sold in a week, as well as the total profit it made on the sale of these exer…"
- `ch16-b016-i01e` [exercise_item] — placed in **AO:need-for-collecting-data-for-planning-purposes-ao-recognise-usefulness-for-planning (exercise)**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Exercise 16.4: Use statistics given in a table to predict and plan
  - evidence quote: "### Exercise 16.4: Use statistics given in a table to predict and plan  1. A stationery shop kept a record of the number of exercise books it sold in a week, as well as the total profit it made on the sale of these exer…"
- `ch16-b016-i01f` [exercise_item] — placed in **AO:need-for-collecting-data-for-planning-purposes-ao-recognise-usefulness-for-planning (exercise)**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Exercise 16.4: Use statistics given in a table to predict and plan
  - evidence quote: "### Exercise 16.4: Use statistics given in a table to predict and plan  1. A stationery shop kept a record of the number of exercise books it sold in a week, as well as the total profit it made on the sale of these exer…"
- `ch16-b016-i02a` [exercise_item] — placed in **AO:need-for-collecting-data-for-planning-purposes-ao-recognise-usefulness-for-prediction (exercise)**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Exercise 16.4: Use statistics given in a table to predict and plan
  - evidence quote: "### Exercise 16.4: Use statistics given in a table to predict and plan  2. This table shows some of the items sold in the local shop on a particular day, the number of each item sold that day, the price per item and the…"
- `ch16-b016-i02b` [exercise_item] — placed in **AO:need-for-collecting-data-for-planning-purposes-ao-recognise-usefulness-for-prediction (exercise)**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Exercise 16.4: Use statistics given in a table to predict and plan
  - evidence quote: "### Exercise 16.4: Use statistics given in a table to predict and plan  2. This table shows some of the items sold in the local shop on a particular day, the number of each item sold that day, the price per item and the…"
- `ch16-b016-i02c` [exercise_item] — placed in **AO:need-for-collecting-data-for-planning-purposes-ao-recognise-usefulness-for-prediction (exercise)**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Exercise 16.4: Use statistics given in a table to predict and plan
  - evidence quote: "### Exercise 16.4: Use statistics given in a table to predict and plan  2. This table shows some of the items sold in the local shop on a particular day, the number of each item sold that day, the price per item and the…"
- `ch16-b016-i02d` [exercise_item] — placed in **AO:need-for-collecting-data-for-planning-purposes-ao-recognise-usefulness-for-prediction (exercise)**
  - heading: Chapter 16: Need for statistics > 16.3 Practical applications > Exercise 16.4: Use statistics given in a table to predict and plan
  - evidence quote: "### Exercise 16.4: Use statistics given in a table to predict and plan  2. This table shows some of the items sold in the local shop on a particular day, the number of each item sold that day, the price per item and the…"
- `ch16-b017` [summary] — placed in **excluded**
  - heading: Chapter 16: Need for statistics > 16.4 Summary
  - evidence quote: "- Statistics keeps us informed about what is happening in the world around us. - Statistics can be given in table form. We can analyse these statistics in order to draw conclusions about the information given. - Governm…"

### Row-level review categories and manually authored reasons
_None — all AOs have direct evidence and a reused assessment._

### Per-atomic-objective evidence classification
- `need-for-collecting-data-for-planning-purposes-ao-recognise-usefulness-for-planning` → evidence: **direct** · categories: —
  - linked records: ch16-b014(instruction), ch16-b015(worked_example), ch16-b016-i01a(exercise), ch16-b016-i01b(exercise), ch16-b016-i01c(exercise), ch16-b016-i01d(exercise), ch16-b016-i01e(exercise), ch16-b016-i01f(exercise)
  - assessment: reused from `ch16-b016-i01c`
- `need-for-collecting-data-for-planning-purposes-ao-apply-chance-events-and-probabilities` → evidence: **direct** · categories: —
  - linked records: ch16-b010(instruction), ch16-b011(instruction), ch16-b012(worked_example), ch16-b013-i01(exercise), ch16-b013-i02(exercise), ch16-b013-i03(exercise), ch16-b013-i04(exercise), ch16-b013-i05(exercise), ch16-b013-i06(exercise)
  - assessment: reused from `ch16-b013-i03`
- `need-for-collecting-data-for-planning-purposes-ao-recognise-usefulness-for-prediction` → evidence: **direct** · categories: —
  - linked records: ch16-b016-i02a(exercise), ch16-b016-i02b(exercise), ch16-b016-i02c(exercise), ch16-b016-i02d(exercise)
  - assessment: reused from `ch16-b016-i02c`

---

## `jss1-math-need-for-statistics-collection-of-data`

**Title:** Collection of data  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, no_reused_assessment

### Curriculum objectives (source)
- `jss1-math-need-for-statistics-collection-of-data-po01`: Collect data from relevant sources

### Atomic objectives
- `collection-of-data-ao-collect-data-from-relevant-sources` [collect/apply]: Collect data from relevant sources.

### Linked textbook records (24 total) — inspected
- `ch17-b001` [exposition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data
  - evidence quote: "You have learnt that statistics is useful as it allows us to interpret what has happened in the past, so that we can predict what is likely to happen in the future, and plan for it. A vital part of working with statisti…"
- `ch17-b002` [definition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data
  - evidence quote: "**data handling** Data handling is gathering and recording information, and then presenting it in a way that can be understood easily and used by other people."
- `ch17-b003` [exposition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > The data handling cycle
  - evidence quote: "The process of data handling is summarised in the diagram below.  ![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-g10-math-lit-12-gd-0001.png)  We show the process of data hand…"
- `ch17-b004` [exposition] — placed in **AO:collection-of-data-ao-collect-data-from-relevant-sources (instruction)**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Different ways of collecting data
  - evidence quote: "The first step in any statistical process is **data collection**, which is gathering the facts and figures (the data).  What we are researching affects the way we collect the data. Four methods of collecting data are sh…"
- `ch17-b005` [definition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Different ways of collecting data
  - evidence quote: "**data collection** Data collection is gathering the facts and figures needed for the research."
- `ch17-b006` [worked_example] — placed in **AO:collection-of-data-ao-collect-data-from-relevant-sources (worked_example)**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Worked example 17.1: Choosing the best way to collect data
  - evidence quote: "Amaka wants to answer the following question: Is my baby crying too much? Consider which of the following would be the best method for her to use.  - Should Amaka interview people one-on-one to find out the answer to he…"
- `ch17-b007` [exercise_block] — placed in **excluded**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Exercise 17.1: Choose the best way to collect data
  - evidence quote: "### Exercise 17.1: Choose the best way to collect data"
- `ch17-b007-i01` [exercise_item] — placed in **AO:collection-of-data-ao-collect-data-from-relevant-sources (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Exercise 17.1: Choose the best way to collect data
  - evidence quote: "### Exercise 17.1: Choose the best way to collect data  1. Babangida wants to find out her classmates' favourite television programme.  What one of the following should Babangida do?  - Look up the answer in the newspap…"
- `ch17-b007-i02` [exercise_item] — placed in **AO:collection-of-data-ao-collect-data-from-relevant-sources (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Exercise 17.1: Choose the best way to collect data
  - evidence quote: "### Exercise 17.1: Choose the best way to collect data  2. Adanna wants to know how the price of cooking oil has increased over the last ten years.  Which one of the following should Adanna do?  - Go to the Nigerian Nat…"
- `ch17-b008` [exposition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Organising data
  - evidence quote: "After data has been collected, the next step is **organising the data**, by bringing it together in a systematic way that makes it easier to read. We can organise data by using tallies and frequency tables."
- `ch17-b009` [definition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Organising data
  - evidence quote: "**organising data** Organising data is bringing it together in a systematic way that makes it easier to read."
- `ch17-b010` [exposition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Tallies
  - evidence quote: "Tallies are a way of counting by drawing a short vertical line to record each item as you count it. To make reading the tally marks easier, for every fifth mark, you draw a diagonal line through the first four lines. Th…"
- `ch17-b011` [exposition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Frequency tables
  - evidence quote: "When we have finished counting, and add up all the tally marks, the totals tell us how many times the event occurred, which is called the **frequency**. So the frequency of red cars was 7, of green cars was 3, of blue c…"
- `ch17-b012` [definition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Frequency tables
  - evidence quote: "**frequency** The frequency is how many times the event occurred."
- `ch17-b013` [exposition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Frequency tables
  - evidence quote: "A frequency table shows the list of different categories, together with the number of times each item occurs. This frequency table shows the number of differently coloured cars.  | Car colours | Frequency | | --- | ---:…"
- `ch17-b014` [worked_example] — placed in **review_items**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Worked example 17.2: Counting tally marks
  - evidence quote: "Amina counted the number of students who belonged to the chess club, and used tally marks to show this data.  Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-…"
- `ch17-b015` [exercise_block] — placed in **excluded**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Exercise 17.2: Count tally marks
  - evidence quote: "### Exercise 17.2: Count tally marks"
- `ch17-b015-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Exercise 17.2: Count tally marks
  - evidence quote: "### Exercise 17.2: Count tally marks  1. Oladapo counted the number of students who have pets at home, and used tally marks to show this data.  Source image: https://electricbookworks.github.io/siyavula-open-textbooks-i…"
- `ch17-b015-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Exercise 17.2: Count tally marks
  - evidence quote: "### Exercise 17.2: Count tally marks  2. Adebisi counted the number of girls playing tennis, and used tally marks to show this data.  Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/item…"
- `ch17-b016` [worked_example] — placed in **review_items**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Worked example 17.3: Drawing up a frequency table
  - evidence quote: "15 students each had one chance to throw a die, and they recorded the number the die landed on each time.  The list of numbers is $\text{5 ; 1 ; 5 ; 1 ; 1 ; 2 ; 3 ; 5 ; 6 ; 4 ; 2 ; 4 ; 2 ; 5 ; 5}$.  Work out how many of…"
- `ch17-b017` [exercise_block] — placed in **excluded**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Exercise 17.3: Draw up frequency tables
  - evidence quote: "### Exercise 17.3: Draw up frequency tables"
- `ch17-b017-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Exercise 17.3: Draw up frequency tables
  - evidence quote: "### Exercise 17.3: Draw up frequency tables  1. 15 students each had one chance to throw a die. The number the die landed on was recorded.  The numbers were $\text{5 ; 1 ; 3 ; 3 ; 4 ; 5 ; 3 ; 1 ; 1 ; 3 ; 6 ; 3 ; 3 ; 6 ;…"
- `ch17-b017-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Exercise 17.3: Draw up frequency tables
  - evidence quote: "### Exercise 17.3: Draw up frequency tables  2. The marks out of 10 for a maths quiz are listed below. There were 20 students who took part in the quiz.  The marks were $\text{5 ; 7 ; 5 ; 7 ; 6 ; 7 ; 7 ; 5 ; 8 ; 8 ; 5 ;…"
- `ch17-b040` [summary] — placed in **excluded**
  - heading: Chapter 17: Data collection and presentation > 17.4 Summary
  - evidence quote: "- Collecting, organising and presenting data forms part of the data handling cycle. - Data can be collected using observations, interviews, questionnaires and existing databases. - The method chosen for collecting the d…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch17-b014/b015-i01/b015-i02/b016/b017-i01/b017-i02 are tally-counting and frequency-table tasks — these belong to organising/summarising data rather than collection.
- **no_reused_assessment**: Although a reused assessment was selected from ch17-b007-i02, the AO is 'collect data' and the chosen item asks the student to choose the best way to collect data; the alignment is partial and a stronger AO-aligned assessment is preferred.

### Per-atomic-objective evidence classification
- `collection-of-data-ao-collect-data-from-relevant-sources` → evidence: **direct** · categories: —
  - linked records: ch17-b004(instruction), ch17-b006(worked_example), ch17-b007-i01(exercise), ch17-b007-i02(exercise)
  - assessment: reused from `ch17-b007-i02`

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All review_items were inspected. Candidate proposals were added for tally-counting and frequency-table construction because those records are organising-data skills, not collection of data from sources.

### Candidate atomic objective proposals
- `collection-of-data-candidate-ao-count-tally-marks` [extension_or_enrichment; candidate_for_expert_review]
  - proposed objective: Count tally marks in collected data.
  - source records: ch17-b014, ch17-b015-i01, ch17-b015-i02
  - closest existing AOs: collection-of-data-ao-collect-data-from-relevant-sources
  - candidate evidence quote: "Amina counted the number of students who belonged to the chess club, and used tally marks to show this data."
  - rationale: These records ask learners to read/count tallies after data has been collected. That is an organising-data skill, not collecting data from sources.
- `collection-of-data-candidate-ao-draw-frequency-tables` [extension_or_enrichment; candidate_for_expert_review]
  - proposed objective: Draw frequency tables from collected data.
  - source records: ch17-b016, ch17-b017-i01, ch17-b017-i02
  - closest existing AOs: collection-of-data-ao-collect-data-from-relevant-sources
  - candidate evidence quote: "The frequency is the number of times each number was thrown."
  - rationale: These records require organising collected values into a frequency table, a post-collection representation skill.

---

## `jss1-math-data-collection-collect-data-in-the-class`

**Title:** Collect data in the class  
**Status:** `needs_review`  
**Row review categories:** ambiguous_record_scope, prerequisite_only_evidence

### Curriculum objectives (source)
- `jss1-math-data-collection-collect-data-in-the-class-po01`: Collect data in the class

### Atomic objectives
- `collect-data-in-the-class-ao-collect-data` [collect/apply]: Collect data in the class.

### Linked textbook records (24 total) — inspected
- `ch17-b001` [exposition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data
  - evidence quote: "You have learnt that statistics is useful as it allows us to interpret what has happened in the past, so that we can predict what is likely to happen in the future, and plan for it. A vital part of working with statisti…"
- `ch17-b002` [definition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data
  - evidence quote: "**data handling** Data handling is gathering and recording information, and then presenting it in a way that can be understood easily and used by other people."
- `ch17-b003` [exposition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > The data handling cycle
  - evidence quote: "The process of data handling is summarised in the diagram below.  ![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-g10-math-lit-12-gd-0001.png)  We show the process of data hand…"
- `ch17-b004` [exposition] — placed in **AO:collect-data-in-the-class-ao-collect-data (instruction)**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Different ways of collecting data
  - evidence quote: "The first step in any statistical process is **data collection**, which is gathering the facts and figures (the data).  What we are researching affects the way we collect the data. Four methods of collecting data are sh…"
- `ch17-b005` [definition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Different ways of collecting data
  - evidence quote: "**data collection** Data collection is gathering the facts and figures needed for the research."
- `ch17-b006` [worked_example] — placed in **AO:collect-data-in-the-class-ao-collect-data (worked_example)**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Worked example 17.1: Choosing the best way to collect data
  - evidence quote: "Amaka wants to answer the following question: Is my baby crying too much? Consider which of the following would be the best method for her to use.  - Should Amaka interview people one-on-one to find out the answer to he…"
- `ch17-b007` [exercise_block] — placed in **excluded**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Exercise 17.1: Choose the best way to collect data
  - evidence quote: "### Exercise 17.1: Choose the best way to collect data"
- `ch17-b007-i01` [exercise_item] — placed in **AO:collect-data-in-the-class-ao-collect-data (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Exercise 17.1: Choose the best way to collect data
  - evidence quote: "### Exercise 17.1: Choose the best way to collect data  1. Babangida wants to find out her classmates' favourite television programme.  What one of the following should Babangida do?  - Look up the answer in the newspap…"
- `ch17-b007-i02` [exercise_item] — placed in **AO:collect-data-in-the-class-ao-collect-data (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Exercise 17.1: Choose the best way to collect data
  - evidence quote: "### Exercise 17.1: Choose the best way to collect data  2. Adanna wants to know how the price of cooking oil has increased over the last ten years.  Which one of the following should Adanna do?  - Go to the Nigerian Nat…"
- `ch17-b008` [exposition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Organising data
  - evidence quote: "After data has been collected, the next step is **organising the data**, by bringing it together in a systematic way that makes it easier to read. We can organise data by using tallies and frequency tables."
- `ch17-b009` [definition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Organising data
  - evidence quote: "**organising data** Organising data is bringing it together in a systematic way that makes it easier to read."
- `ch17-b010` [exposition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Tallies
  - evidence quote: "Tallies are a way of counting by drawing a short vertical line to record each item as you count it. To make reading the tally marks easier, for every fifth mark, you draw a diagonal line through the first four lines. Th…"
- `ch17-b011` [exposition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Frequency tables
  - evidence quote: "When we have finished counting, and add up all the tally marks, the totals tell us how many times the event occurred, which is called the **frequency**. So the frequency of red cars was 7, of green cars was 3, of blue c…"
- `ch17-b012` [definition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Frequency tables
  - evidence quote: "**frequency** The frequency is how many times the event occurred."
- `ch17-b013` [exposition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Frequency tables
  - evidence quote: "A frequency table shows the list of different categories, together with the number of times each item occurs. This frequency table shows the number of differently coloured cars.  | Car colours | Frequency | | --- | ---:…"
- `ch17-b014` [worked_example] — placed in **review_items**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Worked example 17.2: Counting tally marks
  - evidence quote: "Amina counted the number of students who belonged to the chess club, and used tally marks to show this data.  Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/sv-qb-jss1-…"
- `ch17-b015` [exercise_block] — placed in **excluded**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Exercise 17.2: Count tally marks
  - evidence quote: "### Exercise 17.2: Count tally marks"
- `ch17-b015-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Exercise 17.2: Count tally marks
  - evidence quote: "### Exercise 17.2: Count tally marks  1. Oladapo counted the number of students who have pets at home, and used tally marks to show this data.  Source image: https://electricbookworks.github.io/siyavula-open-textbooks-i…"
- `ch17-b015-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Exercise 17.2: Count tally marks
  - evidence quote: "### Exercise 17.2: Count tally marks  2. Adebisi counted the number of girls playing tennis, and used tally marks to show this data.  Source image: https://electricbookworks.github.io/siyavula-open-textbooks-images/item…"
- `ch17-b016` [worked_example] — placed in **review_items**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Worked example 17.3: Drawing up a frequency table
  - evidence quote: "15 students each had one chance to throw a die, and they recorded the number the die landed on each time.  The list of numbers is $\text{5 ; 1 ; 5 ; 1 ; 1 ; 2 ; 3 ; 5 ; 6 ; 4 ; 2 ; 4 ; 2 ; 5 ; 5}$.  Work out how many of…"
- `ch17-b017` [exercise_block] — placed in **excluded**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Exercise 17.3: Draw up frequency tables
  - evidence quote: "### Exercise 17.3: Draw up frequency tables"
- `ch17-b017-i01` [exercise_item] — placed in **review_items**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Exercise 17.3: Draw up frequency tables
  - evidence quote: "### Exercise 17.3: Draw up frequency tables  1. 15 students each had one chance to throw a die. The number the die landed on was recorded.  The numbers were $\text{5 ; 1 ; 3 ; 3 ; 4 ; 5 ; 3 ; 1 ; 1 ; 3 ; 6 ; 3 ; 3 ; 6 ;…"
- `ch17-b017-i02` [exercise_item] — placed in **review_items**
  - heading: Chapter 17: Data collection and presentation > 17.1 Collecting and organising data > Exercise 17.3: Draw up frequency tables
  - evidence quote: "### Exercise 17.3: Draw up frequency tables  2. The marks out of 10 for a maths quiz are listed below. There were 20 students who took part in the quiz.  The marks were $\text{5 ; 7 ; 5 ; 7 ; 6 ; 7 ; 7 ; 5 ; 8 ; 8 ; 5 ;…"
- `ch17-b040` [summary] — placed in **excluded**
  - heading: Chapter 17: Data collection and presentation > 17.4 Summary
  - evidence quote: "- Collecting, organising and presenting data forms part of the data handling cycle. - Data can be collected using observations, interviews, questionnaires and existing databases. - The method chosen for collecting the d…"

### Row-level review categories and manually authored reasons
- **ambiguous_record_scope**: ch17-b014/b015-i01/b015-i02/b016/b017-i01/b017-i02 are tally and frequency-table tasks; not in-class data-collection tasks.
- **prerequisite_only_evidence**: The AO is specifically 'Collect data in the class'. The linked records cover general data-collection methods (ch17-b004 and the Exercise 17.1 items) but none of them is an in-class data-collection activity; the evidence is for the general skill of choosing a data-collection method, not for the in-class scope.

### Per-atomic-objective evidence classification
- `collect-data-in-the-class-ao-collect-data` → evidence: **prerequisite_only** · categories: prerequisite_only_evidence
  - linked records: ch17-b004(instruction), ch17-b006(worked_example), ch17-b007-i01(exercise), ch17-b007-i02(exercise)
  - assessment: reused from `ch17-b007-i02`

### Candidate AO review
- reviewed: true
- verdict: has_candidates
- rationale: All review_items and linked data-collection records were inspected. Candidate proposals retained for selecting collection methods, tally-counting, and frequency-table construction because none is the same as conducting in-class data collection.

### Candidate atomic objective proposals
- `collect-data-in-the-class-candidate-ao-choose-data-collection-methods` [prerequisite; candidate_for_expert_review]
  - proposed objective: Choose suitable methods for collecting data.
  - source records: ch17-b004, ch17-b006, ch17-b007-i01, ch17-b007-i02
  - closest existing AOs: collect-data-in-the-class-ao-collect-data
  - candidate evidence quote: "Four methods of collecting data are shown in the diagram."
  - rationale: Choosing a data-collection method supports classroom data collection, but it is not itself the in-class collection activity named by the current AO.
- `collect-data-in-the-class-candidate-ao-count-tally-marks` [extension_or_enrichment; candidate_for_expert_review]
  - proposed objective: Count tally marks in collected data.
  - source records: ch17-b014, ch17-b015-i01, ch17-b015-i02
  - closest existing AOs: collect-data-in-the-class-ao-collect-data
  - candidate evidence quote: "Amina counted the number of students who belonged to the chess club, and used tally marks to show this data."
  - rationale: These records ask learners to read/count tallies after data has been collected. That is an organising-data skill, not the act of collecting data in class.
- `collect-data-in-the-class-candidate-ao-draw-frequency-tables` [extension_or_enrichment; candidate_for_expert_review]
  - proposed objective: Draw frequency tables from collected data.
  - source records: ch17-b016, ch17-b017-i01, ch17-b017-i02
  - closest existing AOs: collect-data-in-the-class-ao-collect-data
  - candidate evidence quote: "15 students each had one chance to throw a die, and they recorded the number the die landed on each time."
  - rationale: These records require organising collected values into a frequency table. That is a distinct post-collection representation skill.

---

## `jss1-math-data-presentation-graphical-presentation-of-data`

**Title:** Graphical presentation of data  
**Status:** `needs_review`  
**Row review categories:** ao_no_evidence, no_reused_assessment, curriculum_textbook_mismatch

### Curriculum objectives (source)
- `jss1-math-data-presentation-graphical-presentation-of-data-po01`: Present data using bar charts, pie charts and histograms
- `jss1-math-data-presentation-graphical-presentation-of-data-po02`: Read and interpret information from bar charts, pie charts and histograms

### Atomic objectives
- `graphical-presentation-of-data-ao-present-using-bar-charts` [present/apply]: Present data using bar charts.
- `graphical-presentation-of-data-ao-present-using-pie-charts` [present/apply]: Present data using pie charts.
- `graphical-presentation-of-data-ao-present-using-histograms` [present/apply]: Present data using histograms.
- `graphical-presentation-of-data-ao-read-bar-charts` [read/remember]: Read information from bar charts.
- `graphical-presentation-of-data-ao-interpret-bar-charts` [interpret/understand]: Interpret information from bar charts.
- `graphical-presentation-of-data-ao-read-pie-charts` [read/remember]: Read information from pie charts.
- `graphical-presentation-of-data-ao-interpret-pie-charts` [interpret/understand]: Interpret information from pie charts.
- `graphical-presentation-of-data-ao-read-histograms` [read/remember]: Read information from histograms.
- `graphical-presentation-of-data-ao-interpret-histograms` [interpret/understand]: Interpret information from histograms.

### Linked textbook records (16 total) — inspected
- `ch17-b034` [exposition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.3 Presenting data
  - evidence quote: "So far we have collected the data, then organised the data, and summarised the data. Now we need to find ways to present the data, so that we can share the results of our research with other people.  There are many ways…"
- `ch17-b035` [definition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.3 Presenting data
  - evidence quote: "presenting data Presenting data is finding a way to show results so they can be shared with other people."
- `ch17-b036` [exposition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.3 Presenting data > Using bar graphs to present data
  - evidence quote: "Bar graphs are used to display data that has been collected and organised in categories. An example of categories is the cars of different colours that we looked at earlier in this chapter.  A bar graph is a chart that…"
- `ch17-b037` [note] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.3 Presenting data > Using bar graphs to present data
  - evidence quote: "It is important to use an appropriate interval on the graph to show the frequency.  This bar graph uses an interval of 100 along the vertical axis. If the largest frequency was only 15, an interval of 100 is not appropr…"
- `ch17-b038` [worked_example] — placed in **AO:graphical-presentation-of-data-ao-read-bar-charts (worked_example)**
  - heading: Chapter 17: Data collection and presentation > 17.3 Presenting data > Worked example 17.10: Reading information from bar graphs
  - evidence quote: "The school tuckshop staff keeps a record of how many hot dogs, sandwiches, salads and burgers they sell on one day. They draw a bar graph to represent the data.  Source image: https://electricbookworks.github.io/siyavul…"
- `ch17-b039` [exercise_block] — placed in **excluded**
  - heading: Chapter 17: Data collection and presentation > 17.3 Presenting data > Exercise 17.8: Read information off bar graphs
  - evidence quote: "### Exercise 17.8: Read information off bar graphs"
- `ch17-b039-i01a` [exercise_item] — placed in **AO:graphical-presentation-of-data-ao-read-bar-charts (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.3 Presenting data > Exercise 17.8: Read information off bar graphs
  - evidence quote: "### Exercise 17.8: Read information off bar graphs  1a. School A started a recycling project. The bar chart below shows the number of kilograms of each category School A recycled last week.  School A's recycling  Source…"
- `ch17-b039-i01b` [exercise_item] — placed in **AO:graphical-presentation-of-data-ao-read-bar-charts (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.3 Presenting data > Exercise 17.8: Read information off bar graphs
  - evidence quote: "### Exercise 17.8: Read information off bar graphs  1b. School A started a recycling project. The bar chart below shows the number of kilograms of each category School A recycled last week.  School A's recycling  Source…"
- `ch17-b039-i01c` [exercise_item] — placed in **AO:graphical-presentation-of-data-ao-read-bar-charts (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.3 Presenting data > Exercise 17.8: Read information off bar graphs
  - evidence quote: "### Exercise 17.8: Read information off bar graphs  1c. School A started a recycling project. The bar chart below shows the number of kilograms of each category School A recycled last week.  School A's recycling  Source…"
- `ch17-b039-i02a` [exercise_item] — placed in **AO:graphical-presentation-of-data-ao-read-bar-charts (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.3 Presenting data > Exercise 17.8: Read information off bar graphs
  - evidence quote: "### Exercise 17.8: Read information off bar graphs  2a. School B also started a recycling project. The bar chart below shows the number of kilograms of each category School B recycled last week.  School B's recycling  S…"
- `ch17-b039-i02b` [exercise_item] — placed in **AO:graphical-presentation-of-data-ao-read-bar-charts (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.3 Presenting data > Exercise 17.8: Read information off bar graphs
  - evidence quote: "### Exercise 17.8: Read information off bar graphs  2b. School B also started a recycling project. The bar chart below shows the number of kilograms of each category School B recycled last week.  School B's recycling  S…"
- `ch17-b039-i02c` [exercise_item] — placed in **AO:graphical-presentation-of-data-ao-read-bar-charts (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.3 Presenting data > Exercise 17.8: Read information off bar graphs
  - evidence quote: "### Exercise 17.8: Read information off bar graphs  2c. School B also started a recycling project. The bar chart below shows the number of kilograms of each category School B recycled last week.  School B's recycling  S…"
- `ch17-b039-i03a` [exercise_item] — placed in **AO:graphical-presentation-of-data-ao-read-bar-charts (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.3 Presenting data > Exercise 17.8: Read information off bar graphs
  - evidence quote: "### Exercise 17.8: Read information off bar graphs  3a. School C also started a recycling project. The bar chart below shows the number of kilograms of each item School C recycled last week.  School C's recycling  Sourc…"
- `ch17-b039-i03b` [exercise_item] — placed in **AO:graphical-presentation-of-data-ao-read-bar-charts (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.3 Presenting data > Exercise 17.8: Read information off bar graphs
  - evidence quote: "### Exercise 17.8: Read information off bar graphs  3b. School C also started a recycling project. The bar chart below shows the number of kilograms of each item School C recycled last week.  School C's recycling  Sourc…"
- `ch17-b039-i03c` [exercise_item] — placed in **AO:graphical-presentation-of-data-ao-read-bar-charts (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.3 Presenting data > Exercise 17.8: Read information off bar graphs
  - evidence quote: "### Exercise 17.8: Read information off bar graphs  3c. School C also started a recycling project. The bar chart below shows the number of kilograms of each item School C recycled last week.  School C's recycling  Sourc…"
- `ch17-b040` [summary] — placed in **excluded**
  - heading: Chapter 17: Data collection and presentation > 17.4 Summary
  - evidence quote: "- Collecting, organising and presenting data forms part of the data handling cycle. - Data can be collected using observations, interviews, questionnaires and existing databases. - The method chosen for collecting the d…"

### Row-level review categories and manually authored reasons
- **ao_no_evidence**: Eight of the nine AOs (present using bar charts, present using pie charts, present using histograms, interpret bar charts, read pie charts, interpret pie charts, read histograms, interpret histograms) have zero record_links — only read-bar-charts is supported by the linked records.
- **no_reused_assessment**: Read-bar-charts AO has direct exercises but no reused assessment was selected.
- **curriculum_textbook_mismatch**: The curriculum subtopic asks for presenting/reading/interpreting bar charts, pie charts, and histograms; the linked Chapter 17 records cover only bar-graph reading. Pie charts and histograms are absent.

### Per-atomic-objective evidence classification
- `graphical-presentation-of-data-ao-present-using-bar-charts` → evidence: **none** · categories: ao_no_evidence, curriculum_textbook_mismatch
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `graphical-presentation-of-data-ao-present-using-pie-charts` → evidence: **none** · categories: ao_no_evidence, curriculum_textbook_mismatch
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `graphical-presentation-of-data-ao-present-using-histograms` → evidence: **none** · categories: ao_no_evidence, curriculum_textbook_mismatch
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `graphical-presentation-of-data-ao-read-bar-charts` → evidence: **direct** · categories: no_reused_assessment
  - linked records: ch17-b038(worked_example), ch17-b039-i01a(exercise), ch17-b039-i01b(exercise), ch17-b039-i01c(exercise), ch17-b039-i02a(exercise), ch17-b039-i02b(exercise), ch17-b039-i02c(exercise), ch17-b039-i03a(exercise), ch17-b039-i03b(exercise), ch17-b039-i03c(exercise)
  - assessment: _(none anchored)_
- `graphical-presentation-of-data-ao-interpret-bar-charts` → evidence: **none** · categories: ao_no_evidence
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `graphical-presentation-of-data-ao-read-pie-charts` → evidence: **none** · categories: ao_no_evidence, curriculum_textbook_mismatch
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `graphical-presentation-of-data-ao-interpret-pie-charts` → evidence: **none** · categories: ao_no_evidence, curriculum_textbook_mismatch
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `graphical-presentation-of-data-ao-read-histograms` → evidence: **none** · categories: ao_no_evidence, curriculum_textbook_mismatch
  - linked records: _(none)_
  - assessment: _(none anchored)_
- `graphical-presentation-of-data-ao-interpret-histograms` → evidence: **none** · categories: ao_no_evidence, curriculum_textbook_mismatch
  - linked records: _(none)_
  - assessment: _(none anchored)_

### Candidate AO review
- reviewed: true
- verdict: no_candidate_records
- rationale: Candidate-AO review completed across this needs_review row. No candidate proposal was added because the non-direct records are ambiguous instances of existing AOs, assessment gaps, missing-corpus issues, or records already represented by another explicit curriculum subtopic rather than a distinct new measurable objective for this row.

---

## `jss1-math-data-presentation-mean`

**Title:** Mean (arithmetic mean)  
**Status:** `mapped`  
**Row review categories:** _(none — mapped or no-records baseline)_

### Curriculum objectives (source)
- `jss1-math-data-presentation-mean-po01`: Calculate the arithmetic mean of a given set of data

### Atomic objectives
- `mean-ao-calculate-arithmetic-mean` [calculate/apply]: Calculate the arithmetic mean of a given set of data.

### Linked textbook records (13 total) — inspected
- `ch17-b018` [exposition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data
  - evidence quote: "After we have collected and organised data, we need to summarise it. **Summarising data** allows us to see at a glance what important things the data has told us.  When we summarise data, we use different methods to sum…"
- `ch17-b019` [definition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data
  - evidence quote: "**summarising data** Summarising data is using the mean, the mode and the median to sum up what the whole set of data has told us."
- `ch17-b020` [exposition] — placed in **AO:mean-ao-calculate-arithmetic-mean (instruction)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > The mean
  - evidence quote: "The mean of a set of data gives the average of the data. The mean is calculated by adding all the values together and dividing by the number of values in the data set.  For example, you have these results as your data:…"
- `ch17-b021` [worked_example] — placed in **AO:mean-ao-calculate-arithmetic-mean (worked_example)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Worked example 17.4: Finding the mean
  - evidence quote: "Find the mean of the data set $\text{4; 6; 7; 3; 4; 8; 4; 2; 9}$."
- `ch17-b022` [exercise_block] — placed in **excluded**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Exercise 17.4: Find the mean of a data set
  - evidence quote: "### Exercise 17.4: Find the mean of a data set"
- `ch17-b022-i01` [exercise_item] — placed in **AO:mean-ao-calculate-arithmetic-mean (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Exercise 17.4: Find the mean of a data set
  - evidence quote: "### Exercise 17.4: Find the mean of a data set  1. Consider the following set of data:  $$ \text{8; 6; 9; 5; 11; 6; 7; 8} $$  Find the mean value of the data set. Round your answer to two decimal places."
- `ch17-b022-i02` [exercise_item] — placed in **AO:mean-ao-calculate-arithmetic-mean (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Exercise 17.4: Find the mean of a data set
  - evidence quote: "### Exercise 17.4: Find the mean of a data set  2. What is the mean value of the following data set? Round your answer to two decimal places.  $$ \text{6; 8; 7; 5; 10; 5; 7} $$"
- `ch17-b022-i03` [exercise_item] — placed in **AO:mean-ao-calculate-arithmetic-mean (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Exercise 17.4: Find the mean of a data set
  - evidence quote: "### Exercise 17.4: Find the mean of a data set  3. Find the mean value of the following data set. Round your answer to two decimal places.  $$ \text{8; 7; 10; 8; 7; 6; 5; 5; 6; 11} $$"
- `ch17-b032` [worked_example] — placed in **AO:mean-ao-calculate-arithmetic-mean (worked_example)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Worked example 17.9: Finding mean, median and mode for one data set
  - evidence quote: "Find the mean, median and mode for the data set $\text{5; 11; 9; 9; 10; 8; 9; 10; 6}$.  - If necessary, round your answer to two decimal places. - If there are two or more modes, give all of the mode values, separated b…"
- `ch17-b033` [exercise_block] — placed in **excluded**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Exercise 17.7: Find the mean, median and mode of a data set
  - evidence quote: "### Exercise 17.7: Find the mean, median and mode of a data set  If necessary, round your answer to two decimal places."
- `ch17-b033-i01` [exercise_item] — placed in **AO:mean-ao-calculate-arithmetic-mean (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Exercise 17.7: Find the mean, median and mode of a data set
  - evidence quote: "### Exercise 17.7: Find the mean, median and mode of a data set  If necessary, round your answer to two decimal places.  1. Find the mean, median and mode for the following set of data: $\text{11; 7; 9; 5; 7; 8; 7}$."
- `ch17-b033-i02` [exercise_item] — placed in **AO:mean-ao-calculate-arithmetic-mean (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Exercise 17.7: Find the mean, median and mode of a data set
  - evidence quote: "### Exercise 17.7: Find the mean, median and mode of a data set  If necessary, round your answer to two decimal places.  2. Find the mean, median and mode for the data set $\text{9; 6; 5; 9; 6; 10; 11; 8}$."
- `ch17-b040` [summary] — placed in **excluded**
  - heading: Chapter 17: Data collection and presentation > 17.4 Summary
  - evidence quote: "- Collecting, organising and presenting data forms part of the data handling cycle. - Data can be collected using observations, interviews, questionnaires and existing databases. - The method chosen for collecting the d…"

### Row-level review categories and manually authored reasons
_None — all AOs have direct evidence and a reused assessment._

### Per-atomic-objective evidence classification
- `mean-ao-calculate-arithmetic-mean` → evidence: **direct** · categories: —
  - linked records: ch17-b020(instruction), ch17-b021(worked_example), ch17-b022-i01(exercise), ch17-b022-i02(exercise), ch17-b022-i03(exercise), ch17-b032(worked_example), ch17-b033-i01(exercise), ch17-b033-i02(exercise)
  - assessment: reused from `ch17-b022-i03`

---

## `jss1-math-data-presentation-mode`

**Title:** Mode  
**Status:** `mapped`  
**Row review categories:** _(none — mapped or no-records baseline)_

### Curriculum objectives (source)
- `jss1-math-data-presentation-mode-po01`: Determine the mode of a given set of data

### Atomic objectives
- `mode-ao-determine-mode` [determine/apply]: Determine the mode of a given set of data.

### Linked textbook records (15 total) — inspected
- `ch17-b018` [exposition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data
  - evidence quote: "After we have collected and organised data, we need to summarise it. **Summarising data** allows us to see at a glance what important things the data has told us.  When we summarise data, we use different methods to sum…"
- `ch17-b019` [definition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data
  - evidence quote: "**summarising data** Summarising data is using the mean, the mode and the median to sum up what the whole set of data has told us."
- `ch17-b023` [exposition] — placed in **AO:mode-ao-determine-mode (instruction)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > The mode
  - evidence quote: "The mode is the data item that occurs most often in a set of data. No calculation is needed to find the mode. You may have to sort the data, and then count to find the value that appears most often.  For example, if you…"
- `ch17-b024` [worked_example] — placed in **AO:mode-ao-determine-mode (worked_example)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Worked example 17.5: Finding the mode
  - evidence quote: "Find the mode of this data set: $\text{10; 7; 7; 6; 9; 5}$."
- `ch17-b025` [worked_example] — placed in **AO:mode-ao-determine-mode (worked_example)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Worked example 17.6: Finding the mode when there is more than one mode
  - evidence quote: "Find the mode of the data set $\text{10; 8; 8; 9; 7; 9; 10; 11; 6; 11}$."
- `ch17-b026` [exercise_block] — placed in **excluded**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Exercise 17.5: Find the mode of a data set
  - evidence quote: "### Exercise 17.5: Find the mode of a data set"
- `ch17-b026-i01` [exercise_item] — placed in **AO:mode-ao-determine-mode (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Exercise 17.5: Find the mode of a data set
  - evidence quote: "### Exercise 17.5: Find the mode of a data set  1. Find the mode of the following set of data:  $$ \text{1; 2; 3; 4; 5; 1; 2; 3; 4; 1; 2; 3; 1; 2; 1} $$"
- `ch17-b026-i02` [exercise_item] — placed in **AO:mode-ao-determine-mode (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Exercise 17.5: Find the mode of a data set
  - evidence quote: "### Exercise 17.5: Find the mode of a data set  2. Find the mode of the following set of data:  $$ \text{5; 5; 6; 8; 9; 9; 11; 11} $$"
- `ch17-b026-i03` [exercise_item] — placed in **AO:mode-ao-determine-mode (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Exercise 17.5: Find the mode of a data set
  - evidence quote: "### Exercise 17.5: Find the mode of a data set  3. Find the mode of the following set of measurements:  $$ \text{ 4 m; 7 m; 6 m; 11 m; 8 m; 5 m; 9 m; 6 m; 11 m} $$"
- `ch17-b026-i04` [exercise_item] — placed in **AO:mode-ao-determine-mode (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Exercise 17.5: Find the mode of a data set
  - evidence quote: "### Exercise 17.5: Find the mode of a data set  4. Funeka decides to record the colours of everyone's schoolbags as they arrive at school. She makes a tally list to record the colours. Later, she uses the tallies to dra…"
- `ch17-b032` [worked_example] — placed in **AO:mode-ao-determine-mode (worked_example)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Worked example 17.9: Finding mean, median and mode for one data set
  - evidence quote: "Find the mean, median and mode for the data set $\text{5; 11; 9; 9; 10; 8; 9; 10; 6}$.  - If necessary, round your answer to two decimal places. - If there are two or more modes, give all of the mode values, separated b…"
- `ch17-b033` [exercise_block] — placed in **excluded**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Exercise 17.7: Find the mean, median and mode of a data set
  - evidence quote: "### Exercise 17.7: Find the mean, median and mode of a data set  If necessary, round your answer to two decimal places."
- `ch17-b033-i01` [exercise_item] — placed in **AO:mode-ao-determine-mode (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Exercise 17.7: Find the mean, median and mode of a data set
  - evidence quote: "### Exercise 17.7: Find the mean, median and mode of a data set  If necessary, round your answer to two decimal places.  1. Find the mean, median and mode for the following set of data: $\text{11; 7; 9; 5; 7; 8; 7}$."
- `ch17-b033-i02` [exercise_item] — placed in **AO:mode-ao-determine-mode (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Exercise 17.7: Find the mean, median and mode of a data set
  - evidence quote: "### Exercise 17.7: Find the mean, median and mode of a data set  If necessary, round your answer to two decimal places.  2. Find the mean, median and mode for the data set $\text{9; 6; 5; 9; 6; 10; 11; 8}$."
- `ch17-b040` [summary] — placed in **excluded**
  - heading: Chapter 17: Data collection and presentation > 17.4 Summary
  - evidence quote: "- Collecting, organising and presenting data forms part of the data handling cycle. - Data can be collected using observations, interviews, questionnaires and existing databases. - The method chosen for collecting the d…"

### Row-level review categories and manually authored reasons
_None — all AOs have direct evidence and a reused assessment._

### Per-atomic-objective evidence classification
- `mode-ao-determine-mode` → evidence: **direct** · categories: —
  - linked records: ch17-b023(instruction), ch17-b024(worked_example), ch17-b025(worked_example), ch17-b026-i01(exercise), ch17-b026-i02(exercise), ch17-b026-i03(exercise), ch17-b026-i04(exercise), ch17-b032(worked_example), ch17-b033-i01(exercise), ch17-b033-i02(exercise)
  - assessment: reused from `ch17-b026-i03`

---

## `jss1-math-data-presentation-median`

**Title:** Median  
**Status:** `mapped`  
**Row review categories:** _(none — mapped or no-records baseline)_

### Curriculum objectives (source)
- `jss1-math-data-presentation-median-po01`: Determine the median of a given set of data

### Atomic objectives
- `median-ao-determine-median` [determine/apply]: Determine the median of a given set of data.

### Linked textbook records (15 total) — inspected
- `ch17-b018` [exposition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data
  - evidence quote: "After we have collected and organised data, we need to summarise it. **Summarising data** allows us to see at a glance what important things the data has told us.  When we summarise data, we use different methods to sum…"
- `ch17-b019` [definition] — placed in **shared_foundation**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data
  - evidence quote: "**summarising data** Summarising data is using the mean, the mode and the median to sum up what the whole set of data has told us."
- `ch17-b027` [exposition] — placed in **AO:median-ao-determine-median (instruction)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > The median
  - evidence quote: "The median is the middle value in the set of data values. To find the middle, the data set has to be arranged in ascending order first.  For example, if you have that data set $\text{2; 3; 4; 5; 6; 7; 8}$, there are 7 n…"
- `ch17-b028` [worked_example] — placed in **AO:median-ao-determine-median (worked_example)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Worked example 17.7: Finding the median of an odd number of values
  - evidence quote: "Find the median of the data set: $\text{4; 6; 7; 4; 3; 4; 8; 2; 9; 7; 2}$."
- `ch17-b029` [worked_example] — placed in **AO:median-ao-determine-median (worked_example)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Worked example 17.8: Finding the median of an even number of values
  - evidence quote: "Find the median of the data set: $\text{4; 6; 4; 7; 2; 3; 8; 9; 7; 4}$."
- `ch17-b030` [exercise_block] — placed in **excluded**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Exercise 17.6: Find the median of a data set
  - evidence quote: "### Exercise 17.6: Find the median of a data set"
- `ch17-b030-i01` [exercise_item] — placed in **AO:median-ao-determine-median (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Exercise 17.6: Find the median of a data set
  - evidence quote: "### Exercise 17.6: Find the median of a data set  1. Find the median of the data set $\text{8; 5; 10; 9; 5; 7; 9; 10; 11; 7; 9; 5}$. If necessary, round your answer to one decimal place."
- `ch17-b030-i02` [exercise_item] — placed in **AO:median-ao-determine-median (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Exercise 17.6: Find the median of a data set
  - evidence quote: "### Exercise 17.6: Find the median of a data set  2. Find the median value of the following data set:  $$ \text{6; 7; 10; 5; 9; 7; 7; 5} $$"
- `ch17-b030-i03` [exercise_item] — placed in **AO:median-ao-determine-median (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Exercise 17.6: Find the median of a data set
  - evidence quote: "### Exercise 17.6: Find the median of a data set  3. Find the median value of the data set  $$ \text{7; 6; 11; 5; 10; 7; 11; 6; 9} $$"
- `ch17-b031` [exposition] — placed in **AO:median-ao-determine-median (instruction)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > The median
  - evidence quote: "Quite often, you will be asked to give the mean, median and mode for the same data set."
- `ch17-b032` [worked_example] — placed in **AO:median-ao-determine-median (worked_example)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Worked example 17.9: Finding mean, median and mode for one data set
  - evidence quote: "Find the mean, median and mode for the data set $\text{5; 11; 9; 9; 10; 8; 9; 10; 6}$.  - If necessary, round your answer to two decimal places. - If there are two or more modes, give all of the mode values, separated b…"
- `ch17-b033` [exercise_block] — placed in **excluded**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Exercise 17.7: Find the mean, median and mode of a data set
  - evidence quote: "### Exercise 17.7: Find the mean, median and mode of a data set  If necessary, round your answer to two decimal places."
- `ch17-b033-i01` [exercise_item] — placed in **AO:median-ao-determine-median (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Exercise 17.7: Find the mean, median and mode of a data set
  - evidence quote: "### Exercise 17.7: Find the mean, median and mode of a data set  If necessary, round your answer to two decimal places.  1. Find the mean, median and mode for the following set of data: $\text{11; 7; 9; 5; 7; 8; 7}$."
- `ch17-b033-i02` [exercise_item] — placed in **AO:median-ao-determine-median (exercise)**
  - heading: Chapter 17: Data collection and presentation > 17.2 Summarising data > Exercise 17.7: Find the mean, median and mode of a data set
  - evidence quote: "### Exercise 17.7: Find the mean, median and mode of a data set  If necessary, round your answer to two decimal places.  2. Find the mean, median and mode for the data set $\text{9; 6; 5; 9; 6; 10; 11; 8}$."
- `ch17-b040` [summary] — placed in **excluded**
  - heading: Chapter 17: Data collection and presentation > 17.4 Summary
  - evidence quote: "- Collecting, organising and presenting data forms part of the data handling cycle. - Data can be collected using observations, interviews, questionnaires and existing databases. - The method chosen for collecting the d…"

### Row-level review categories and manually authored reasons
_None — all AOs have direct evidence and a reused assessment._

### Per-atomic-objective evidence classification
- `median-ao-determine-median` → evidence: **direct** · categories: —
  - linked records: ch17-b027(instruction), ch17-b028(worked_example), ch17-b029(worked_example), ch17-b030-i01(exercise), ch17-b030-i02(exercise), ch17-b030-i03(exercise), ch17-b031(instruction), ch17-b032(worked_example), ch17-b033-i01(exercise), ch17-b033-i02(exercise)
  - assessment: reused from `ch17-b030-i03`

---
