# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-1",
  "topic_key": "jss1-math-fractions",
  "topic": "Fractions",
  "subtopic_id": "jss1-math-fractions-ordering-of-fractions",
  "subtopic_title": "Ordering of fractions",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-fractions-ordering-of-fractions-po01",
        "source_performance_objective_index": 1,
        "text": "Arrange fractions in ascending/descending order"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "ordering-of-fractions-ao-arrange-ascending",
          "text": "Arrange fractions in ascending order."
        },
        {
          "atomic_objective_id": "ordering-of-fractions-ao-arrange-descending",
          "text": "Arrange fractions in descending order."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch04-b027",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.3 Comparing fractions",
      "h3": null
    },
    "content_text": "It may be difficult to compare fractions that do not have the same denominator. Look at the two diagrams below. The fraction of the circle that is shaded is given below each diagram.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-018.png)\n\nWhich fraction is larger, $\\frac{2}{3}$ or $\\frac{3}{4}$? It is not so easy to decide this just by looking at the diagrams or the fractions themselves. However, if we express both fractions with the same denominator, it becomes easier to compare them.\n\n$$\n\\frac{2\\times4}{3\\times4}=\\frac{8}{12}\n$$\n$$\n\\frac{3\\times3}{4\\times3}=\\frac{9}{12}\n$$\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-019.png)\n\nNow it is clear that $\\frac{3}{4}$ is the larger fraction. We may write this in two ways:\n\n- $\\frac{2}{3}<\\frac{3}{4}$, which means $\\frac{2}{3}$ is smaller than $\\frac{3}{4}$\n- $\\frac{3}{4}>\\frac{2}{3}$, which means $\\frac{3}{4}$ is larger than $\\frac{2}{3}$\n- $\\frac{3}{4}&amp;gt;\\frac{2}{3}$\n\nTo be able to compare fractions, we first need to find the lowest common denominator (LCD) for the fractions. This is the lowest common multiple (LCM) of the denominators. Then we need to express the two fractions as equivalent fractions using this same denominator.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-ordering-of-fractions"
  },
  {
    "record_id": "ch04-b028",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.3 Comparing fractions",
      "h3": null
    },
    "content_text": "lowest common denominator (LCD)\n\nThe LCD is the smallest whole number into which the denominators of two or more fractions can divide without a remainder.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-ordering-of-fractions"
  },
  {
    "record_id": "ch04-b029",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.3 Comparing fractions",
      "h3": null
    },
    "content_text": "If necessary, go back to Chapter 2 to see how to find the LCM of two or more numbers.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-ordering-of-fractions"
  },
  {
    "record_id": "ch04-b030",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.3 Comparing fractions",
      "h3": null
    },
    "content_text": "If we express more than two fractions using the same denominator, this allows us to order the fractions in ascending order or descending order. Fractions that are arranged in ascending order start with the smallest fraction, then have the next smallest, and so on, and the largest fraction is last. For example $\\frac{1}{7};\\space\\frac{3}{7};\\space\\frac{6}{7}$. Fractions that are arranged in descending order start with the largest fraction, then have the next largest, and so on, and the smallest fraction is last. For example $\\frac{5}{7};\\space\\frac{4}{7};\\space\\frac{2}{7}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-ordering-of-fractions"
  },
  {
    "record_id": "ch04-b031",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.3 Comparing fractions",
      "h3": null
    },
    "content_text": "ascending order\n\nWhen numbers of any kind are arranged in ascending order, they are arranged from the smallest to the largest.\n\ndescending order\n\nWhen numbers of any kind are arranged in descending order, they are arranged from the largest to the smallest.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-ordering-of-fractions"
  },
  {
    "record_id": "ch04-b032",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.3 Comparing fractions",
      "h3": "Worked example 4.5: Ordering fractions"
    },
    "content_text": "",
    "prompt_text": "Arrange the following fractions in ascending order:\n\n$$\n\\frac{5}{6};\\space\\frac{7}{8};\\space\\frac{3}{4}\n$$",
    "answer_text": "Step 1: Before we can compare fractions, we need to give equivalent fractions using the same denominator. To do this, first find the LCD of the fractions.\n\nThe denominators expressed as products of their prime factors are:\n$6=2\\times3$\n$8=2^3$\n$4=2^2$\n\n$$\n\\therefore \\text{LCD} = 2^3\\times3=8\\times3=24\n$$\n\nStep 2: For each given fraction, find an equivalent fraction using the denominator calculated in Step 1.\n\n$$\n\\frac{5}{6}=\\frac{\\square}{24}\\space \\Rightarrow\\space \\frac{5\\times4}{6\\times4}=\\frac{20}{24}\n$$\n$$\n\\frac{7}{8}=\\frac{\\square}{24}\\space \\Rightarrow\\space \\frac{7\\times3}{8\\times3}=\\frac{21}{24}\n$$\n$$\n\\frac{3}{4}=\\frac{\\square}{24}\\space \\Rightarrow\\space \\frac{3\\times6}{4\\times6}=\\frac{18}{24}\n$$\n\nStep 3: Write the original fractions in the required order.\n\nAscending order means we have to start with the smallest fraction and end with the largest fraction: $\\frac{18}{24};\\;\\frac{20}{24};\\;\\frac{21}{24}$.\n\nThe original fractions, arranged in ascending order, are:\n$$\n\\frac{3}{4};\\space\\frac{5}{6};\\space\\frac{7}{8}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-ordering-of-fractions"
  },
  {
    "record_id": "ch04-b033",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.3 Comparing fractions",
      "h3": "Exercise 4.6: Order and compare fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.6: Order and compare fractions",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-ordering-of-fractions"
  },
  {
    "record_id": "ch04-b033-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.3 Comparing fractions",
      "h3": "Exercise 4.6: Order and compare fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.6: Order and compare fractions\n\n1. Arrange the following fractions in ascending order: $\\frac{8}{9};\\space\\frac{11}{12};\\space\\frac{5}{6}$",
    "answer_text": "$\\phantom{0}9=3^2$\n$\\phantom{0}6=2\\times3$\n$12=2^2\\times3$\n$\\phantom{0}9=3^2; \\phantom{0}6=2\\times3$\n\n$$\n\\therefore \\text{LCD}=2^2\\times3^2=4\\times9=36\n$$\n$$\n\\frac{8}{9}=\\frac{\\square}{36}\\space \\Rightarrow\\space \\frac{8\\times4}{9\\times4}=\\frac{32}{36}\n$$\n$$\n\\frac{11}{12}=\\frac{\\square}{36}\\space \\Rightarrow\\space \\frac{11\\times3}{12\\times3}=\\frac{33}{36}\n$$\n$$\n\\frac{5}{6}=\\frac{\\square}{36}\\space \\Rightarrow\\space \\frac{5\\times6}{6\\times6}=\\frac{30}{36}\n$$\nAscending order: $\\frac{5}{6};\\space\\frac{8}{9};\\space\\frac{11}{12}$",
    "primary_subtopic_id": "jss1-math-fractions-ordering-of-fractions"
  },
  {
    "record_id": "ch04-b033-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.3 Comparing fractions",
      "h3": "Exercise 4.6: Order and compare fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.6: Order and compare fractions\n\n2. Arrange the following fractions in descending order: $\\frac{5}{8};\\space\\frac{8}{14};\\space\\frac{18}{28}$",
    "answer_text": "$\\phantom{0}8=2^3$\n$14=2\\times7$\n$28=2^2\\times7$\n$\\phantom{0}8=2^3$\n\n$$\n\\therefore \\text{LCD}=2^3\\times7=8\\times7=56\n$$\n$$\n\\frac{5}{8}=\\frac{\\square}{56}\\space \\Rightarrow\\space \\frac{5\\times7}{8\\times7}=\\frac{35}{56}\n$$\n$$\n\\frac{8}{14}=\\frac{\\square}{56}\\space \\Rightarrow\\space \\frac{8\\times4}{14\\times4}=\\frac{32}{56}\n$$\n$$\n\\frac{18}{28}=\\frac{\\square}{56}\\space \\Rightarrow\\space \\frac{18\\times2}{28\\times2}=\\frac{36}{56}\n$$\nDescending order: $\\frac{18}{28};\\space\\frac{5}{8};\\space\\frac{8}{14}$",
    "primary_subtopic_id": "jss1-math-fractions-ordering-of-fractions"
  },
  {
    "record_id": "ch04-b033-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.3 Comparing fractions",
      "h3": "Exercise 4.6: Order and compare fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.6: Order and compare fractions\n\n3. Look at this list of fractions: $\\frac{13}{4};\\space\\frac{8}{28};\\space\\frac{17}{6};\\space\\frac{15}{35};\\space\\frac{9}{21}$. From the list, identify:\n\na. two fractions that are equivalent\nb. the fraction with the highest value\nc. the fraction with the lowest value\nd. an improper fraction that is smaller than 3\ne. a fraction that is equivalent to $\\frac{26}{91}$",
    "answer_text": "a. $$\n\\frac{15\\div5}{35\\div5}=\\frac{3}{7}\n$$\n$$\n\\frac{9\\div3}{21\\div3}=\\frac{3}{7}\n$$\n$$\n\\therefore \\frac{15}{35}=\\frac{9}{21}\n$$\n\nb. The proper fractions are all smaller than 1. The two improper fractions are larger than 1, so work only with them.\n$$\n\\frac{13}{4}=3\\frac{1}{4}\n$$\n$$\n\\frac{17}{6}=2\\frac{5}{6}\n$$\n$$\n\\therefore \\text{Highest value}=\\frac{13}{4}\n$$\n\nc. Both improper fractions are larger than 1. The three proper fractions are smaller than 1, so work only with them.\nFrom a) above:\n$$\n\\frac{15}{35}=\\frac{9}{21}=\\frac{3}{7}\n$$\nBut:\n$$\n\\frac{8\\div4}{28\\div4}=\\frac{2}{7}\n$$\n$$\n\\therefore \\text{Lowest value}=\\frac{8}{28}\n$$\n\nd. From b) above:\n$$\n\\frac{17}{6}=2\\frac{5}{6}\n$$\n$$\n\\therefore\\frac{17}{6}<3\n$$\n\ne. $$\n\\frac{26\\div13}{91\\div13}=\\frac{2}{7}\n$$\nFrom c) above:\n$$\n\\frac{8}{28}=\\frac{2}{7}\n$$\n$$\n\\frac{26\\div13}{91\\div13}=\\frac{2}{7}\n$$\n$$\n\\therefore \\frac{26}{91}=\\frac{8}{28}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-ordering-of-fractions"
  },
  {
    "record_id": "ch04-b057-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": "Exercise 4.12: Use equivalent fractions to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.12: Use equivalent fractions to solve problems\n\n5. Atinuke and Eniola buy a bag of rice. Atinuke gets $\\frac{3}{7}$ of the bag, Eniola gets $\\frac{5}{9}$ of the bag and a little bit is left over. Who received the larger portion of rice, Atinuke or Eniola?",
    "answer_text": "$$\n\\text{LCD}=63\n$$\n\n$$\n\\frac{3}{7}=\\frac{3\\times9}{7\\times9}=\\frac{27}{63}\n$$\n\n$$\n\\frac{5}{9}=\\frac{5\\times7}{9\\times7}=\\frac{35}{63}\n$$\n\nEniola received the larger portion of the rice.",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
  },
  {
    "record_id": "ch04-b058",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.7 Summary",
      "h3": null
    },
    "content_text": "- A common fraction is written as $\\frac{\\text{numerator}}{\\text{denominator}}$.\n- A proper fraction is smaller than 1, for example $\\frac{2}{7}$.\n- A mixed number consists of a whole number and a proper fraction, for example $5\\frac{1}{6}$.\n- An improper fraction is larger than 1, for example $\\frac{9}{4}$.\n- Equivalent fractions have different numerators and denominators but the same value, for example $\\frac{1}{2}=\\frac{2}{4}=\\frac{4}{8}$.\n- A fraction is in its simplest form when the numerator and denominator have no common factor.\n- To compare fractions, we must express them with the same denominators. The lowest common denominator is the smallest whole number into which all the denominators can divide without a remainder.\n- A decimal fraction is written in decimal notation, where the numerator is written after a decimal point and the denominator is a power of ten.\n- In decimal notation, the decimal point separates whole numbers from fractions.\n- If there are three digits after the decimal point, the denominator is $10\\times10\\times10=1,000$.\n- A percentage is a fraction with denominator 100, written with only the numerator followed by a percentage symbol.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
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
  "theme_key": "jss1-theme-1",
  "topic_key": "jss1-math-fractions",
  "topic": "Fractions",
  "subtopic_id": "jss1-math-fractions-ordering-of-fractions",
  "subtopic_title": "Ordering of fractions",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-fractions-ordering-of-fractions-po01",
        "source_performance_objective_index": 1,
        "text": "Arrange fractions in ascending/descending order"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "ordering-of-fractions-ao-arrange-ascending",
          "text": "Arrange fractions in ascending order."
        },
        {
          "atomic_objective_id": "ordering-of-fractions-ao-arrange-descending",
          "text": "Arrange fractions in descending order."
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
    "record_id": "ch04-b027",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.3 Comparing fractions",
      "h3": null
    },
    "content_text": "It may be difficult to compare fractions that do not have the same denominator. Look at the two diagrams below. The fraction of the circle that is shaded is given below each diagram.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-018.png)\n\nWhich fraction is larger, $\\frac{2}{3}$ or $\\frac{3}{4}$? It is not so easy to decide this just by looking at the diagrams or the fractions themselves. However, if we express both fractions with the same denominator, it becomes easier to compare them.\n\n$$\n\\frac{2\\times4}{3\\times4}=\\frac{8}{12}\n$$\n$$\n\\frac{3\\times3}{4\\times3}=\\frac{9}{12}\n$$\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-019.png)\n\nNow it is clear that $\\frac{3}{4}$ is the larger fraction. We may write this in two ways:\n\n- $\\frac{2}{3}<\\frac{3}{4}$, which means $\\frac{2}{3}$ is smaller than $\\frac{3}{4}$\n- $\\frac{3}{4}>\\frac{2}{3}$, which means $\\frac{3}{4}$ is larger than $\\frac{2}{3}$\n- $\\frac{3}{4}&amp;gt;\\frac{2}{3}$\n\nTo be able to compare fractions, we first need to find the lowest common denominator (LCD) for the fractions. This is the lowest common multiple (LCM) of the denominators. Then we need to express the two fractions as equivalent fractions using this same denominator.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-ordering-of-fractions"
  },
  {
    "record_id": "ch04-b028",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.3 Comparing fractions",
      "h3": null
    },
    "content_text": "lowest common denominator (LCD)\n\nThe LCD is the smallest whole number into which the denominators of two or more fractions can divide without a remainder.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-ordering-of-fractions"
  },
  {
    "record_id": "ch04-b029",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.3 Comparing fractions",
      "h3": null
    },
    "content_text": "If necessary, go back to Chapter 2 to see how to find the LCM of two or more numbers.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-ordering-of-fractions"
  },
  {
    "record_id": "ch04-b030",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.3 Comparing fractions",
      "h3": null
    },
    "content_text": "If we express more than two fractions using the same denominator, this allows us to order the fractions in ascending order or descending order. Fractions that are arranged in ascending order start with the smallest fraction, then have the next smallest, and so on, and the largest fraction is last. For example $\\frac{1}{7};\\space\\frac{3}{7};\\space\\frac{6}{7}$. Fractions that are arranged in descending order start with the largest fraction, then have the next largest, and so on, and the smallest fraction is last. For example $\\frac{5}{7};\\space\\frac{4}{7};\\space\\frac{2}{7}$.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-ordering-of-fractions"
  },
  {
    "record_id": "ch04-b031",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.3 Comparing fractions",
      "h3": null
    },
    "content_text": "ascending order\n\nWhen numbers of any kind are arranged in ascending order, they are arranged from the smallest to the largest.\n\ndescending order\n\nWhen numbers of any kind are arranged in descending order, they are arranged from the largest to the smallest.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-ordering-of-fractions"
  },
  {
    "record_id": "ch04-b032",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.3 Comparing fractions",
      "h3": "Worked example 4.5: Ordering fractions"
    },
    "content_text": "",
    "prompt_text": "Arrange the following fractions in ascending order:\n\n$$\n\\frac{5}{6};\\space\\frac{7}{8};\\space\\frac{3}{4}\n$$",
    "answer_text": "Step 1: Before we can compare fractions, we need to give equivalent fractions using the same denominator. To do this, first find the LCD of the fractions.\n\nThe denominators expressed as products of their prime factors are:\n$6=2\\times3$\n$8=2^3$\n$4=2^2$\n\n$$\n\\therefore \\text{LCD} = 2^3\\times3=8\\times3=24\n$$\n\nStep 2: For each given fraction, find an equivalent fraction using the denominator calculated in Step 1.\n\n$$\n\\frac{5}{6}=\\frac{\\square}{24}\\space \\Rightarrow\\space \\frac{5\\times4}{6\\times4}=\\frac{20}{24}\n$$\n$$\n\\frac{7}{8}=\\frac{\\square}{24}\\space \\Rightarrow\\space \\frac{7\\times3}{8\\times3}=\\frac{21}{24}\n$$\n$$\n\\frac{3}{4}=\\frac{\\square}{24}\\space \\Rightarrow\\space \\frac{3\\times6}{4\\times6}=\\frac{18}{24}\n$$\n\nStep 3: Write the original fractions in the required order.\n\nAscending order means we have to start with the smallest fraction and end with the largest fraction: $\\frac{18}{24};\\;\\frac{20}{24};\\;\\frac{21}{24}$.\n\nThe original fractions, arranged in ascending order, are:\n$$\n\\frac{3}{4};\\space\\frac{5}{6};\\space\\frac{7}{8}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-ordering-of-fractions"
  },
  {
    "record_id": "ch04-b033",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.3 Comparing fractions",
      "h3": "Exercise 4.6: Order and compare fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.6: Order and compare fractions",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-ordering-of-fractions"
  },
  {
    "record_id": "ch04-b033-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.3 Comparing fractions",
      "h3": "Exercise 4.6: Order and compare fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.6: Order and compare fractions\n\n1. Arrange the following fractions in ascending order: $\\frac{8}{9};\\space\\frac{11}{12};\\space\\frac{5}{6}$",
    "answer_text": "$\\phantom{0}9=3^2$\n$\\phantom{0}6=2\\times3$\n$12=2^2\\times3$\n$\\phantom{0}9=3^2; \\phantom{0}6=2\\times3$\n\n$$\n\\therefore \\text{LCD}=2^2\\times3^2=4\\times9=36\n$$\n$$\n\\frac{8}{9}=\\frac{\\square}{36}\\space \\Rightarrow\\space \\frac{8\\times4}{9\\times4}=\\frac{32}{36}\n$$\n$$\n\\frac{11}{12}=\\frac{\\square}{36}\\space \\Rightarrow\\space \\frac{11\\times3}{12\\times3}=\\frac{33}{36}\n$$\n$$\n\\frac{5}{6}=\\frac{\\square}{36}\\space \\Rightarrow\\space \\frac{5\\times6}{6\\times6}=\\frac{30}{36}\n$$\nAscending order: $\\frac{5}{6};\\space\\frac{8}{9};\\space\\frac{11}{12}$",
    "primary_subtopic_id": "jss1-math-fractions-ordering-of-fractions"
  },
  {
    "record_id": "ch04-b033-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.3 Comparing fractions",
      "h3": "Exercise 4.6: Order and compare fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.6: Order and compare fractions\n\n2. Arrange the following fractions in descending order: $\\frac{5}{8};\\space\\frac{8}{14};\\space\\frac{18}{28}$",
    "answer_text": "$\\phantom{0}8=2^3$\n$14=2\\times7$\n$28=2^2\\times7$\n$\\phantom{0}8=2^3$\n\n$$\n\\therefore \\text{LCD}=2^3\\times7=8\\times7=56\n$$\n$$\n\\frac{5}{8}=\\frac{\\square}{56}\\space \\Rightarrow\\space \\frac{5\\times7}{8\\times7}=\\frac{35}{56}\n$$\n$$\n\\frac{8}{14}=\\frac{\\square}{56}\\space \\Rightarrow\\space \\frac{8\\times4}{14\\times4}=\\frac{32}{56}\n$$\n$$\n\\frac{18}{28}=\\frac{\\square}{56}\\space \\Rightarrow\\space \\frac{18\\times2}{28\\times2}=\\frac{36}{56}\n$$\nDescending order: $\\frac{18}{28};\\space\\frac{5}{8};\\space\\frac{8}{14}$",
    "primary_subtopic_id": "jss1-math-fractions-ordering-of-fractions"
  },
  {
    "record_id": "ch04-b033-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.3 Comparing fractions",
      "h3": "Exercise 4.6: Order and compare fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.6: Order and compare fractions\n\n3. Look at this list of fractions: $\\frac{13}{4};\\space\\frac{8}{28};\\space\\frac{17}{6};\\space\\frac{15}{35};\\space\\frac{9}{21}$. From the list, identify:\n\na. two fractions that are equivalent\nb. the fraction with the highest value\nc. the fraction with the lowest value\nd. an improper fraction that is smaller than 3\ne. a fraction that is equivalent to $\\frac{26}{91}$",
    "answer_text": "a. $$\n\\frac{15\\div5}{35\\div5}=\\frac{3}{7}\n$$\n$$\n\\frac{9\\div3}{21\\div3}=\\frac{3}{7}\n$$\n$$\n\\therefore \\frac{15}{35}=\\frac{9}{21}\n$$\n\nb. The proper fractions are all smaller than 1. The two improper fractions are larger than 1, so work only with them.\n$$\n\\frac{13}{4}=3\\frac{1}{4}\n$$\n$$\n\\frac{17}{6}=2\\frac{5}{6}\n$$\n$$\n\\therefore \\text{Highest value}=\\frac{13}{4}\n$$\n\nc. Both improper fractions are larger than 1. The three proper fractions are smaller than 1, so work only with them.\nFrom a) above:\n$$\n\\frac{15}{35}=\\frac{9}{21}=\\frac{3}{7}\n$$\nBut:\n$$\n\\frac{8\\div4}{28\\div4}=\\frac{2}{7}\n$$\n$$\n\\therefore \\text{Lowest value}=\\frac{8}{28}\n$$\n\nd. From b) above:\n$$\n\\frac{17}{6}=2\\frac{5}{6}\n$$\n$$\n\\therefore\\frac{17}{6}<3\n$$\n\ne. $$\n\\frac{26\\div13}{91\\div13}=\\frac{2}{7}\n$$\nFrom c) above:\n$$\n\\frac{8}{28}=\\frac{2}{7}\n$$\n$$\n\\frac{26\\div13}{91\\div13}=\\frac{2}{7}\n$$\n$$\n\\therefore \\frac{26}{91}=\\frac{8}{28}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-ordering-of-fractions"
  },
  {
    "record_id": "ch04-b057-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.6 Practical applications",
      "h3": "Exercise 4.12: Use equivalent fractions to solve problems"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.12: Use equivalent fractions to solve problems\n\n5. Atinuke and Eniola buy a bag of rice. Atinuke gets $\\frac{3}{7}$ of the bag, Eniola gets $\\frac{5}{9}$ of the bag and a little bit is left over. Who received the larger portion of rice, Atinuke or Eniola?",
    "answer_text": "$$\n\\text{LCD}=63\n$$\n\n$$\n\\frac{3}{7}=\\frac{3\\times9}{7\\times9}=\\frac{27}{63}\n$$\n\n$$\n\\frac{5}{9}=\\frac{5\\times7}{9\\times7}=\\frac{35}{63}\n$$\n\nEniola received the larger portion of the rice.",
    "primary_subtopic_id": "jss1-math-fractions-quantitative-aptitude-reasoning"
  },
  {
    "record_id": "ch04-b058",
    "record_type": "summary",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.7 Summary",
      "h3": null
    },
    "content_text": "- A common fraction is written as $\\frac{\\text{numerator}}{\\text{denominator}}$.\n- A proper fraction is smaller than 1, for example $\\frac{2}{7}$.\n- A mixed number consists of a whole number and a proper fraction, for example $5\\frac{1}{6}$.\n- An improper fraction is larger than 1, for example $\\frac{9}{4}$.\n- Equivalent fractions have different numerators and denominators but the same value, for example $\\frac{1}{2}=\\frac{2}{4}=\\frac{4}{8}$.\n- A fraction is in its simplest form when the numerator and denominator have no common factor.\n- To compare fractions, we must express them with the same denominators. The lowest common denominator is the smallest whole number into which all the denominators can divide without a remainder.\n- A decimal fraction is written in decimal notation, where the numerator is written after a decimal point and the denominator is a power of ten.\n- In decimal notation, the decimal point separates whole numbers from fractions.\n- If there are three digits after the decimal point, the denominator is $10\\times10\\times10=1,000$.\n- A percentage is a fraction with denominator 100, written with only the numerator followed by a percentage symbol.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
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
