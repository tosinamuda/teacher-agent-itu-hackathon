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
#### Identify common multiples of two or more whole numbers (extended)

*explanation*

A **multiple** of a whole number is a product that can be divided by that number without remainder. When the same number is a multiple of two (or more) numbers, it is a **common multiple**. For example, 12 is a common multiple of 3 and 4 because both divide 12 exactly.

_Sources: REF-1_

*explanation*

**Worked Example (concise):** Find the common multiples of 4 and 6.
1. Multiples of 4: 4, 8, 12, 16, 20, 24 …
2. Multiples of 6: 6, 12, 18, 24, 30, 36 …
3. Numbers appearing in both lists are 12, 24, … – these are the common multiples.

_Sources: REF-2_

*practice*

**Practice – stretch challenge** – Write down **three** common multiples for each pair of numbers.
1. 5 and 6: ____, ____, ____
2. 8 and 12: ____, ____, ____
3. 9 and 15: ____, ____, ____
(You may continue the lists if you wish.)

_Sources: REF-3_

### Candidate B
#### Identify common multiples of two or more whole numbers

*explanation*

A **multiple** of a whole number is the product of that number and a whole‑number factor. A **common multiple** of two or more numbers is a number that appears in each of their multiple lists. Recognising common multiples sets the stage for finding the least common multiple (LCM).

*worked_example*

**Quick Example:** Find common multiples of 4 and 6.
- Multiples of 4: 4, 8, 12, 16, 20, 24, …
- Multiples of 6: 6, 12, 18, 24, 30, 36, …
Common multiples that appear in both lists are 12 and 24 (and continue).
These illustrate how to spot common multiples.

*practice*

**Practice – List three common multiples for each pair.**
1. 6 and 15: ____, ____, ____
2. 8 and 20: ____, ____, ____
3. 9 and 12: ____, ____, ____
(You may continue the lists if you wish.)

**Judgement (fill in): A / B / tie — why:**

---

## Objective lop02

### Candidate A
#### Finding the LCM using the Definition of Common Multiples

*explanation*

The **lowest common multiple (LCM)** of a set of whole numbers is the *smallest* positive number that is a multiple of each of the numbers. A **multiple** is a number that can be divided by another number without a remainder, and a **common multiple** is a multiple that works for two or more numbers. For example, 12 is a common multiple of 3 and 4 because both 3 and 4 divide into 12 exactly. The LCM is simply the *least* of these common multiples.  

*Sources: REF‑1, REF‑2*

*worked_example*

**Worked Example – LCM of 4 and 6**

1. List a few multiples of each number:
   - Multiples of 4: 4, **8**, **12**, 16, …
   - Multiples of 6: 6, **12**, 18, …
2. Identify the **common multiples** (numbers that appear in both lists). From the lists above, the common multiples are **12**, 24, …
3. The **smallest** common multiple is **12**. Therefore, LCM(4, 6) = **12**.

> *Why 10 is not the answer*: A common slip is to add the numbers (4 + 6 = 10) and think the sum is the LCM. Adding gives a total, not a number that both original numbers divide into without remainder. Since 10 ÷ 4 leaves a remainder, it cannot be a common multiple.  

*Source for the definition of a common multiple: REF‑1*

*practice*

**Practice Problems**

1. Find the LCM of 4 and 6.
   *Hint*: Write out several multiples of each number and look for the smallest one they share.

2. Find the LCM of 8, 12 and 15.
   *Hint*: List a few multiples of each number; the LCM is the first number that appears in **all** three lists.

*These problems echo the textbook activity that asks for common multiples (see REF‑3).*

### Candidate B
#### Finding the LCM using the Prime‑Factor Method

*explanation*

The **lowest common multiple (LCM)** of a set of whole numbers is the smallest positive number that is a multiple of each of the numbers. It is the first common multiple that appears when the multiples of the numbers are listed.

A common slip is to think the LCM can be found by **adding** the numbers together. Adding 4 + 6 to get 10, for example, does not give a number that is a multiple of both 4 and 6. The LCM must be **divisible** by each original number.

_Sources: REF‑1_

*worked_example*

**Worked Example – Finding the LCM of 12 and 18 using the prime‑factor method**

1. Write the prime factorisation of each number:
   - 12 = 2² × 3¹
   - 18 = 2¹ × 3²
2. For each distinct prime, take the highest power that appears:
   - For 2, the highest power is 2².
   - For 3, the highest power is 3².
3. Multiply these highest powers together:
   LCM = 2² × 3² = 4 × 9 = **36**.

Thus, the LCM of 12 and 18 is 36.

_Sources: REF‑2_

*worked_example*

**Worked Example – LCM of 4 and 6 (addressing the addition misconception)**

1. List the multiples of each number (or use prime factors).
   - Multiples of 4: 4, 8, **12**, 16,…
   - Multiples of 6: 6, **12**, 18,…
2. Identify the smallest common multiple – it is **12**.

Why 10 (4 + 6) is tempting but wrong: 10 is not a multiple of 4 (4 × 2 = 8, 4 × 3 = 12) nor of 6 (6 × 1 = 6, 6 × 2 = 12). The LCM must be divisible by *both* numbers.

_Sources: REF‑2_

*worked_example*

**Worked Example – LCM of 8, 12 and 15 (addressing the “sum of numbers” slip)**

1. Prime‑factorise each number:
   - 8 = 2³
   - 12 = 2² × 3¹
   - 15 = 3¹ × 5¹
2. For each distinct prime, take the highest power:
   - 2³ (from 8)
   - 3¹ (appears in 12 and 15, highest power 3¹)
   - 5¹ (from 15)
3. Multiply the highest powers: LCM = 2³ × 3¹ × 5¹ = 8 × 3 × 5 = **120**.

Why 90 (the sum‑based guess) is tempting but wrong: 90 = 8 + 12 + 15 + ...? It is not a multiple of 8 (8 × 11 = 88, 8 × 12 = 96). The correct LCM must be divisible by **each** of the three numbers.

_Sources: REF‑2_

*practice*

**Practice Problems – with step‑by‑step hints**

1. Find the LCM of 8 and 20.
   *Hint 1:* Write the prime factors.
   *Hint 2:* Choose the highest power of each prime.
   *Solution:* 8 = 2³, 20 = 2² × 5¹ → LCM = 2³ × 5¹ = **40**.

2. Find the LCM of 15, 25 and 35.
   *Hint 1:* Prime‑factor each number.
   *Hint 2:* For each prime, keep the greatest exponent.
   *Solution:* 15 = 3¹ × 5¹, 25 = 5², 35 = 5¹ × 7¹ → LCM = 3¹ × 5² × 7¹ = **525**.

Check your answers against the textbook solutions.

_Sources: REF‑3_

**Judgement (fill in): A / B / tie — why:**

---
