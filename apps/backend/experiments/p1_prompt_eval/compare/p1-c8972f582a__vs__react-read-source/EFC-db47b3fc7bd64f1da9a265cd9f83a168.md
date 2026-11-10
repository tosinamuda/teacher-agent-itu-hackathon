# EFC-db47b3fc7bd64f1da9a265cd9f83a168

## Ground truth (learner state both candidates were judged against)
```json
{
  "lop01": {
    "lesson_objective_id": "lop01",
    "mastery_band": "extend",
    "mastery": "2 of 2 diagnostic questions correct",
    "confidence": "somewhat sure (3/5)",
    "perceived_difficulty": "okay (3/5)",
    "evidence_items": []
  },
  "lop02": {
    "lesson_objective_id": "lop02",
    "mastery_band": "remediate",
    "mastery": "0 of 2 diagnostic questions correct",
    "confidence": "a little sure (2/5)",
    "perceived_difficulty": "difficult (4/5)",
    "misconception": "Addition mistake",
    "evidence_items": [
      {
        "question": "What is the least common multiple (LCM) of 4 and 6?",
        "options": {
          "A": "10",
          "B": "12",
          "C": "14",
          "D": "8"
        },
        "correct_option": "B",
        "student_choice": "A",
        "chosen_option_misconception": "Addition mistake"
      },
      {
        "question": "Find the LCM of 8, 12, and 15.",
        "options": {
          "A": "120",
          "B": "60",
          "C": "240",
          "D": "90"
        },
        "correct_option": "A",
        "student_choice": "D",
        "chosen_option_misconception": "Sum of numbers"
      }
    ]
  }
}
```

## Objective lop01

### Candidate A
#### Identify common multiples of two or more whole numbers

*explanation*

A **multiple** of a whole number is any product of that number with another whole‑number factor. A **common multiple** of two numbers is a number that is a multiple of each of them (e.g., 12 is a common multiple of 3 and 4).

*worked_example*

**Worked Example:** Find the common multiples of 4 and 6.
1. Multiples of 4: 4, 8, 12, 16, 20, 24, …
2. Multiples of 6: 6, 12, 18, 24, 30, 36, …
3. Numbers appearing in both lists are the common multiples: 12, 24, …
(The smallest common multiple, 12, is the LCM, but here we only note the common multiples.)

*practice*

**Practice:** Find three common multiples of 5 and 6.

*practice*

**Extension Practice:** Find three common multiples of 7 and 8 and identify the smallest one (the LCM).
*Hint:* List multiples of each number up to at least 56.
*Feedback cue:* Compare the two lists; the first number that appears in both is the LCM.

### Candidate B
#### Identify common multiples of two or more whole numbers

*explanation*

A **multiple** of a whole number is a number that can be divided by that number without a remainder. A **common multiple** of two or more numbers is a number that is a multiple of each of them. For example, 12 is a common multiple of 3 and 4 because both 3 and 4 divide into 12 exactly.

*worked_example*

**Worked Example:** Find the common multiples of 4 and 6.
1. List a few multiples of 4: 4, 8, 12, 16, 20, 24, …
2. List a few multiples of 6: 6, 12, 18, 24, 30, 36, …
3. The numbers that appear in both lists are the common multiples: 12 and 24 (and continue).
These are the common multiples of 4 and 6.

*practice*

**Practice (stretch):** Find three common multiples of 5 and 6.
Enter your answers below.
1. _____
2. _____
3. _____
(You may continue the list if needed.)

**Judgement (fill in): A / B / tie — why:**

---

## Objective lop02

### Candidate A
#### Finding the LCM using the Prime‑Factor Method

*explanation*

**What is the Lowest Common Multiple (LCM)?**

The LCM of a set of whole numbers is the *smallest positive number* that is a multiple of each of the numbers. In other words, it is the first **common multiple** that appears when you list the multiples of the numbers.

- A *multiple* of a number is a number that can be divided by the original number without leaving a remainder.
- Two (or more) numbers share a *common multiple* when the same number appears in the multiples of each of them.

The textbook explains a common multiple as “a multiple of two or more numbers” and gives the example that 12 is a common multiple of 3 and 4【"source_refs": ["REF-1", "REF-2"]】.  Remember, **the LCM is **not** found by adding the numbers together**; a common slip is to think 4 + 6 = 10 is the LCM of 4 and 6, but addition gives a sum, not a multiple.

*Key point to keep in mind*: first identify the common multiples, then pick the smallest one – that is the LCM.

*worked_example*

**Worked Example – Finding the LCM of 12 and 18 using the prime‑factor method**

1. **Prime factorise each number**
   - 12 = 2² × 3¹
   - 18 = 2¹ × 3²
2. **Identify every distinct prime** that appears (here, 2 and 3).
3. **Take the highest power** of each prime that shows up in any factorisation:
   - For 2, the highest power is 2².
   - For 3, the highest power is 3².
4. **Multiply those highest powers together**:
   LCM = 2² × 3² = 4 × 9 = **36**.

Why does this work? The product we obtain is a number that contains *at least* the factors of each original number, so it is divisible by both 12 and 18 – making it a common multiple. Because we chose the highest powers, no smaller number can satisfy this condition, so it is the *lowest* common multiple.

(Concept of a common multiple is drawn from the textbook definition【"source_refs": ["REF-2"]】.)

*practice*

**Practice – Find the LCM**

1. **What is the LCM of 4 and 6?**
   - *Hint*: List a few multiples of each number or use the prime‑factor method. Remember, a common multiple is a number that both 4 and 6 divide into without a remainder【"source_refs": ["REF-1"]】.
   - *Full feedback*: The correct answer is **12**. A common slip is to add the numbers (4 + 6 = 10); however, 10 is not divisible by 4 or 6, so it cannot be the LCM.

2. **Find the LCM of 8, 12 and 15.**
   - *Hint*: First write the prime factorisation of each number, then take the highest power of each prime that appears.
   - *Full feedback*: The correct answer is **120**. If you simply added the numbers (8 + 12 + 15 = 35), you would get a sum that is not a common multiple of the three numbers.

*Extra practice from the textbook*: “Find three common multiples of 5 and 6.” (Use these to see how the smallest of the three is the LCM)【"source_refs": ["REF-3"]】.

Work through each problem slowly, checking each step against the definition of a common multiple.

### Candidate B
#### Finding the LCM using the Prime‑Factor Method

*explanation*

The **lowest common multiple (LCM)** of a set of whole numbers is the smallest positive number that is a multiple of each of the numbers. A *multiple* is a number that can be divided by another number without a remainder, and a *common multiple* is a multiple shared by two or more numbers. For example, 12 is a common multiple of 3 and 4 because both 3 and 4 divide evenly into 12. The LCM is simply the **first** common multiple you encounter when you list the multiples of each number. (see REF‑1) (see REF‑2)

*worked_example*

**Worked Example 1 – LCM of 12 and 18 (prime‑factor method)**
1. Factor each number into primes:
   - 12 = 2² × 3¹
   - 18 = 2¹ × 3²
2. For each distinct prime, keep the highest exponent that appears:
   - Highest power of 2 → 2²
   - Highest power of 3 → 3²
3. Multiply those highest powers:
   LCM = 2² × 3² = 4 × 9 = **36**.

**Worked Example 2 – LCM of 4 and 6 (addressing the “addition mistake”)**
A common slip is to add the numbers (4 + 6 = 10) and think that is the LCM. Instead, list the multiples:
- Multiples of 4: 4, 8, **12**, 16, …
- Multiples of 6: 6, **12**, 18, …
The first number that appears in both lists is 12, so the LCM is **12**. (see REF‑1)

This shows why adding the numbers gives an incorrect answer and how to correctly find the smallest common multiple.

*practice*

**Practice – Find the LCM**
1. **LCM of 8 and 20**
   - *Hint:* Write the prime factorisation of each number.
   - 8 = 2³, 20 = 2² × 5¹
   - Highest powers → 2³ and 5¹
   - LCM = 2³ × 5¹ = 8 × 5 = **40**
   - *Feedback:* You have used the highest power of each prime, which gives the smallest common multiple.

2. **LCM of 5 and 6** (similar to the textbook activity in REF‑3)
   - *Hint:* List a few multiples of each number.
   - Multiples of 5: 5, 10, **15**, 20, …
   - Multiples of 6: 6, 12, **18**, **24**, …
   - The first common multiple is **30** (5 × 6), so LCM = **30**.
   - *Feedback:* When two numbers are co‑prime, the LCM equals their product.

Check your answers with the solutions above. If you made an addition mistake, remember to look for *common multiples* rather than adding the numbers together.

**Judgement (fill in): A / B / tie — why:**

---
