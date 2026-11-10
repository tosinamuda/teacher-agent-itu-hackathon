# Manual AO-Textbook Linkage Prompt

Use this prompt for one-subtopic, manual AO-to-textbook linkage. Fill the two placeholders with:

- `{
  "theme_key": "jss1-theme-1",
  "topic_key": "jss1-math-fractions",
  "topic": "Fractions",
  "subtopic_id": "jss1-math-fractions-equivalent-fractions",
  "subtopic_title": "Equivalent fractions",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-fractions-equivalent-fractions-po01",
        "source_performance_objective_index": 1,
        "text": "Identify equivalent fractions"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "equivalent-fractions-ao-identify-equivalent-fractions",
          "text": "Identify equivalent fractions."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-fractions-equivalent-fractions-po02",
        "source_performance_objective_index": 2,
        "text": "Find the equivalence of any given fraction using a formula"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "equivalent-fractions-ao-find-equivalence-using-formula",
          "text": "Find the equivalence of any given fraction using a formula."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-fractions-equivalent-fractions-po03",
        "source_performance_objective_index": 3,
        "text": "Apply equivalent fractions in sharing commodities"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "equivalent-fractions-ao-apply-in-sharing-commodities",
          "text": "Apply equivalent fractions in sharing commodities."
        }
      ]
    }
  ]
}`: the single subtopic row from `dataset/processed/curriculum/manual_authoring/jss1-math_atomic_objectives_all_topics.jsonl`
- `[
  {
    "record_id": "ch04-b014",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": null
    },
    "content_text": "Fractions that represent the same part of a whole in different ways are called equivalent fractions. Look at the three diagrams below. The fraction of the rectangle that is shaded is given next to each diagram.\n\nAll three fractions represent half of the rectangle. The fractions have different numerators and denominators, but they all represent the value $\\frac{1}{2}$.\n\n$$\n\\therefore\\frac{1}{2}=\\frac{2}{4}=\\frac{4}{8}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b015",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": null
    },
    "content_text": "equivalent fractions\n\nEquivalent fractions are fractions that have different numerators and denominators, but they represent the same part of a whole, and they have the same value.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b016",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": null
    },
    "content_text": "We find equivalent fractions by multiplying or dividing the numerator and the denominator by the same whole number.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b017",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Worked example 4.3: Working out equivalent fractions"
    },
    "content_text": "",
    "prompt_text": "Find the missing numbers in these equivalent fractions:\n\n$$\n\\frac{3}{4}=\\frac{\\square}{16}=\\frac{6}{\\square}=\\frac{15}{\\square}\n$$",
    "answer_text": "$$\n\\frac{3}{4}=\\frac{\\square}{16}=\\frac{6}{\\square}=\\frac{15}{\\square}\n$$\n\n            Step 1: Start with the first pair. Identify what is given, which in this case is the two denominators. Was the first denominator multiplied or divided to get the second denominator, and by what whole number?\n\n            $$\n\\frac{3}{4}=\\frac{\\square}{16}\n$$\n\n            The denominator was multiplied by 4 to get 16:\n\n            $$\n\\frac{3\\phantom{000}}{4\\times 4}=\\frac{\\square}{16}\n$$\n\n            Step 2: Repeat the action identified in Step 1 for the remaining part of the fraction.\n\n            The numerator must also be multiplied by 4:\n\n            $$\n\\frac{3\\times 4}{4\\times 4}=\\frac{12}{16}\n$$\n\n            Step 3: Repeat Steps 1 and 2 to find the next missing number.\n\n            $$\n\\frac{3}{4}=\\frac{12}{16}=\\frac{6}{\\square}\n$$\n\n            The numerator was divided by 2:\n\n            $$\n\\frac{3}{4}=\\frac{12\\div2}{16\\phantom{000}}=\\frac{6}{\\square}\n$$\n\n            The denominator must also be divided by 2:\n\n            $$\n\\frac{3}{4}=\\frac{12\\div2}{16\\div 2}=\\frac{6}{8}\n$$\n\n            Step 4: Repeat Steps 1 and 2 for the last fraction. If it is not possible to perform Step 1 with the fraction to the left of the missing number, use any other fraction that is complete.\n\n            $$\n\\frac{3}{4}=\\frac{12}{16}=\\frac{6}{8}=\\frac{15}{\\square}\n$$\n\n            It is not possible to multiply the numerator 6 or the numerator 12 by a whole number and then get 15 as an answer. You have to use the fraction $\\frac{3}{4}$.\n\n            The numerator was multiplied by 5:\n\n            $$\n\\frac{3}{4}=\\frac{3\\times5}{4\\phantom{000}}=\\frac{15}{\\square}\n$$\n\n            The denominator must also be multiplied by 5:\n\n            $$\n\\frac{3}{4}=\\frac{3\\times5}{4\\times5}=\\frac{15}{20}\n$$\n\n            Step 5: Write down the full answer.\n\n            $$\n\\frac{3}{4}=\\frac{12}{16}=\\frac{6}{8}=\\frac{15}{20}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b018",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Find equivalent fractions"
    },
    "content_text": "Improper fractions can also have equivalent fractions. Earlier on in this chapter, we showed that $2\\frac{1}{2}$ apples is equal to $\\frac{5}{2}$ apples. The improper fraction $\\frac{5}{2}$ tells us that we are dealing with apple halves and that we have 5 apple halves.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-013.png)\n\nSuppose we cut each apple half into two pieces. We will then have ten apple quarters.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-016.png)\n\nThis may be expressed as $\\frac{10}{4}$. The denominator tells us that there are 4 parts in one whole apple, so we are dealing with quarters. The numerator tells us that we have 10 quarters. Therefore, the fractions $\\frac{5}{2}$ and $\\frac{10}{4}$ are equivalent fractions. In this case, the numerator and denominator were multiplied by 2:\n\n$$\n\\frac{5\\times2}{2\\times2}=\\frac{10}{4}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b019",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.3: Determine equivalent fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.3: Determine equivalent fractions\n\nFind the missing numbers in each list of equivalent fractions.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b019-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.3: Determine equivalent fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.3: Determine equivalent fractions\n\nFind the missing numbers in each list of equivalent fractions.\n\n1. $$\n\\frac{3}{7}=\\frac{\\square}{42}=\\frac{9}{\\square}=\\frac{6}{\\square}\n$$",
    "answer_text": "$$\n\\frac{3\\times6}{7\\times6}=\\frac{\\fbox{18}}{42}\n$$\n\n$$\n\\frac{18\\div2}{42\\div2}=\\frac{9}{\\fbox{21}}\n$$\n\n$$\n\\frac{3\\times2}{7\\times2}=\\frac{6}{\\fbox{14}}\n$$\n\n$$\n\\therefore\\frac{3}{7}=\\frac{18}{42}=\\frac{9}{21}=\\frac{6}{14}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b019-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.3: Determine equivalent fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.3: Determine equivalent fractions\n\nFind the missing numbers in each list of equivalent fractions.\n\n2. $$\n\\frac{2}{5}=\\frac{\\square}{15}=\\frac{8}{\\square}=\\frac{\\square}{250}\n$$",
    "answer_text": "$$\n\\frac{2\\times3}{5\\times3}=\\frac{\\fbox{6}}{15}\n$$\n\n$$\n\\frac{2\\times4}{5\\times4}=\\frac{8}{\\fbox{20}}\n$$\n\n$$\n\\frac{2\\times50}{5\\times50}=\\frac{\\fbox{100}}{250}\n$$\n\n$$\n\\therefore\\frac{2}{5}=\\frac{6}{15}=\\frac{8}{20}=\\frac{100}{250}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b019-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.3: Determine equivalent fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.3: Determine equivalent fractions\n\nFind the missing numbers in each list of equivalent fractions.\n\n3. $$\n\\frac{\\square}{6}=\\frac{5}{30}=\\frac{15}{\\square}=\\frac{\\square}{12}\n$$",
    "answer_text": "$$\n\\frac{5\\div5}{30\\div5}=\\frac{\\fbox{1}}{6}\n$$\n\n$$\n\\frac{5\\times3}{30\\times3}=\\frac{15}{\\fbox{90}}\n$$\n\n$$\n\\frac{1\\times2}{6\\times2}=\\frac{\\fbox{2}}{12}\n$$\n\n$$\n\\therefore\\frac{1}{6}=\\frac{5}{30}=\\frac{15}{90}=\\frac{2}{12}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b019-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.3: Determine equivalent fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.3: Determine equivalent fractions\n\nFind the missing numbers in each list of equivalent fractions.\n\n4. $$\n\\frac{8}{3}=\\frac{\\square}{6}=\\frac{\\square}{24}=\\frac{24}{\\square}\n$$",
    "answer_text": "$$\n\\frac{8\\times2}{3\\times2}=\\frac{\\fbox{16}}{6}\n$$\n\n$$\n\\frac{16\\times4}{6\\times4}=\\frac{\\fbox{64}}{24}\n$$\n\n$$\n\\frac{8\\times3}{3\\times3}=\\frac{24}{\\fbox{9}}\n$$\n\n$$\n\\therefore\\frac{8}{3}=\\frac{16}{6}=\\frac{64}{24}=\\frac{24}{9}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b019-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.3: Determine equivalent fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.3: Determine equivalent fractions\n\nFind the missing numbers in each list of equivalent fractions.\n\n5. $$\n\\frac{24}{27}=\\frac{8}{\\square}=\\frac{64}{\\square}=\\frac{40}{\\square}\n$$",
    "answer_text": "$$\n\\frac{24\\div3}{27\\div3}=\\frac{8}{\\fbox{9}}\n$$\n\n$$\n\\frac{8\\times8}{9\\times8}=\\frac{64}{\\fbox{72}}\n$$\n\n$$\n\\frac{8\\times5}{9\\times5}=\\frac{40}{\\fbox{45}}\n$$\n\n$$\n\\therefore\\frac{24}{27}=\\frac{8}{9}=\\frac{64}{72}=\\frac{40}{45}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b020",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Simplify equivalent fractions"
    },
    "content_text": "A fraction is in its **simplest form** when the numerator and the denominator have no common factor. For example, $\\frac{1}{2}$ is the simplest form of the fractions $\\frac{2}{4}$ and $\\frac{4}{8}$. These fractions are not in their simplest form, because in $\\frac{2}{4}$, 2 and 4 have 2 as a common factor, and in $\\frac{4}{8}$, 4 and 8 have 2 and 4 as common factors.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b021",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Simplify equivalent fractions"
    },
    "content_text": "**simplest form** A fraction is in its simplest form when the numerator and denominator have no common factor.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b022",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Worked example 4.4: Finding the simplest form of a fraction"
    },
    "content_text": "",
    "prompt_text": "Find the simplest form of the fraction $\\frac{40}{60}$.",
    "answer_text": "Step 1: Find the smallest prime number that is a factor of both the numerator and the denominator. In this case the factor is 2.\nStep 2: Divide both the numerator and denominator by this prime number. Write down the equivalent fraction.\nStep 3: Repeat until the prime number can no longer divide into both the numerator and the denominator.\nStep 4: Move on to the next prime number that is a factor of both the numerator and the denominator. In this case the factor is 5. Divide both the numerator and the denominator by 5.\nStep 5: Repeat this process until the numerator and the denominator have no more common factors.\n\n$$\n\\frac{40\\div2}{60\\div2}=\\frac{20}{30}\n$$\n\n$$\n\\frac{20\\div2}{30\\div2}=\\frac{10}{15}\n$$\n\n$$\n\\frac{10\\div5}{15\\div5}=\\frac{2}{3}\n$$\n\nThe simplest form of $\\frac{40}{60}$ is $\\frac{2}{3}$.\n\nMethod 2 (HCF)\n1. Express both the numerator and the denominator as a product of their prime numbers.\n2. Find the HCF of the numerator and the denominator.\n3. Divide the numerator and the denominator by their HCF.\n\n$$\n\\begin{array}{r | r}\n 2 & 40 \\\\\n \\hline\n 2 & 20 \\\\\n \\hline\n 2 & 10 \\\\\n \\hline\n 5 & 5 \\\\\n \\hline\n & 1\n \\end{array}\n$$\n\n$$\n40=2^3\\times5\n$$\n\n$$\n\\begin{array}{r | r}\n 2 & 60 \\\\\n \\hline\n 2 & 30 \\\\\n \\hline\n 3 & 15 \\\\\n \\hline\n 5 & 5 \\\\\n \\hline\n & 1\n \\end{array}\n$$\n\n$$\n60=2^2\\times3\\times5\n$$\n\n$$\n\\therefore \\text{HCF}=2^2\\times5=2\\times2\\times5=20\n$$\n\n$$\n\\frac{40\\div20}{60\\div20}=\\frac{2}{3}\n$$\n\nThe simplest form of $\\frac{40}{60}$ is $\\frac{2}{3}$.\n\nIf necessary, go back to Chapter 2 to see how to find the highest common factor (HCF) of two or more numbers.\n\nMethod 3 (Inspection)\n1. Find any common factor of the numerator and the denominator.\n2. Divide both the numerator and denominator by this factor. Write down the equivalent fraction.\n3. Repeat this process until the numerator and the denominator have no more common factors.\n\n$$\n\\frac{40\\div10}{60\\div10}=\\frac{4}{6}\n$$\n\n$$\n\\frac{4\\div2}{6\\div2}=\\frac{2}{3}\n$$\n\nThe simplest form of $\\frac{40}{60}$ is $\\frac{2}{3}$.",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b023",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.4: Simplify fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.4: Simplify fractions\n\nFind the simplest form of each of the following fractions, using the method of your choice.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b023-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.4: Simplify fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.4: Simplify fractions\n\nFind the simplest form of each of the following fractions, using the method of your choice.\n\n1. $$\n\\frac{39}{78}\n$$",
    "answer_text": "Using Method 1 (Prime numbers):\n\n$$\n\\frac{39\\div3}{78\\div3}=\\frac{13}{26}\n$$\n\n$$\n\\frac{13\\div13}{26\\div13}=\\frac{1}{2}\n$$\n\nThe simplest form of $\\frac{39}{78}$ is $\\frac{1}{2}$.",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b023-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.4: Simplify fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.4: Simplify fractions\n\nFind the simplest form of each of the following fractions, using the method of your choice.\n\n2. $$\n\\frac{12}{108}\n$$",
    "answer_text": "Using Method 1 (Prime numbers):\n\n$$\n\\frac{12\\div2}{108\\div2}=\\frac{6}{54}\n$$\n\n$$\n\\frac{6\\div2}{54\\div2}=\\frac{3}{27}\n$$\n\n$$\n\\frac{3\\div3}{27\\div3}=\\frac{1}{9}\n$$\n\nThe simplest form of $\\frac{12}{108}$ is $\\frac{1}{9}$.",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b023-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.4: Simplify fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.4: Simplify fractions\n\nFind the simplest form of each of the following fractions, using the method of your choice.\n\n3. $$\n\\frac{16}{64}\n$$",
    "answer_text": "Using Method 2 (HCF):\n\n$$\n16=2^4\n$$\n\n$$\n64=2^6\n$$\n\n$$\n\\therefore \\text{HCF}=2^4=2\\times2\\times2\\times2=16\n$$\n\n$$\n\\frac{16\\div16}{64\\div16}=\\frac{1}{4}\n$$\n\nThe simplest form of $\\frac{16}{64}$ is $\\frac{1}{4}$.",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b023-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.4: Simplify fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.4: Simplify fractions\n\nFind the simplest form of each of the following fractions, using the method of your choice.\n\n4. $$\n\\frac{45}{75}\n$$",
    "answer_text": "Using Method 2 (HCF):\n\n$$\n45=3^2\\times5\n$$\n\n$$\n75=3\\times5^2\n$$\n\n$$\n\\therefore \\text{HCF}=3\\times5=15\n$$\n\n$$\n\\frac{45\\div15}{75\\div15}=\\frac{3}{5}\n$$\n\nThe simplest form of $\\frac{45}{75}$ is $\\frac{3}{5}$.",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b023-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.4: Simplify fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.4: Simplify fractions\n\nFind the simplest form of each of the following fractions, using the method of your choice.\n\n5. $$\n\\frac{250}{150}\n$$",
    "answer_text": "Using Method 3 (Inspection):\n\n$$\n\\frac{250\\div10}{150\\div10}=\\frac{25}{15}\n$$\n\n$$\n\\frac{25\\div5}{15\\div5}=\\frac{5}{3}\n$$\n\nThe simplest form of $\\frac{250}{150}$ is $\\frac{5}{3}$.",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b024",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Identify equivalent fractions"
    },
    "content_text": "Fractions that are equivalent have the same simplest form. Look at the two diagrams below. The fraction of the rectangle that is shaded is given next to each diagram.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-017.png)\n\nIt is easy to see that the fractions $\\frac{6}{8}$ and $\\frac{4}{8}$ are not equivalent. They do not represent the same part of the whole rectangle. We can check this by finding the simplest form of each fraction.\n\n$$\n\\frac{6\\div2}{8\\div2}=\\frac{3}{4}\n$$\n\n$$\n\\frac{4\\div4}{8\\div4}=\\frac{1}{2}\n$$\n\n$$\n\\frac{3}{4}\\neq\\frac{1}{2}\n$$\n\nThis shows that the fractions $\\frac{6}{8}$ and $\\frac{4}{8}$ do not have the same value. They are therefore not equivalent.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b025",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Identify equivalent fractions"
    },
    "content_text": "Remember that equivalent fractions have the same simplest form.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b026",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Comparing fractions",
      "h3": "Exercise 4.5: Determine whether fractions are equivalent or not"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.5: Determine whether fractions are equivalent or not\n\nFor each of the following pairs of fractions, determine whether they are equivalent or not.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b026-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Comparing fractions",
      "h3": "Exercise 4.5: Determine whether fractions are equivalent or not"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.5: Determine whether fractions are equivalent or not\n\n1. $\\frac{15}{18}$ and $\\frac{20}{24}$",
    "answer_text": "$$\n\\frac{15\\div3}{18\\div3}=\\frac{5}{6}\n$$\n$$\n\\frac{20\\div4}{24\\div4}=\\frac{5}{6}\n$$\nThe fractions $\\frac{15}{18}$ and $\\frac{20}{24}$ are equivalent.",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b026-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Comparing fractions",
      "h3": "Exercise 4.5: Determine whether fractions are equivalent or not"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.5: Determine whether fractions are equivalent or not\n\n2. $\\frac{14}{70}$ and $\\frac{21}{105}$",
    "answer_text": "$$\n\\frac{14\\div7}{70\\div7}=\\frac{2}{10}=\\frac{1}{5}\n$$\n$$\n\\frac{21\\div7}{105\\div7}=\\frac{3}{15}=\\frac{1}{5}\n$$\nThe fractions $\\frac{14}{70}$ and $\\frac{21}{105}$ are equivalent.",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b026-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Comparing fractions",
      "h3": "Exercise 4.5: Determine whether fractions are equivalent or not"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.5: Determine whether fractions are equivalent or not\n\n3. $\\frac{16}{48}$ and $\\frac{18}{72}$",
    "answer_text": "$$\n\\frac{16\\div8}{48\\div8}=\\frac{2}{6}=\\frac{1}{3}\n$$\n$$\n\\frac{18\\div6}{72\\div6}=\\frac{3}{12}=\\frac{1}{4}\n$$\nThe fractions $\\frac{16}{48}$ and $\\frac{18}{72}$ are NOT equivalent.",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b026-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Comparing fractions",
      "h3": "Exercise 4.5: Determine whether fractions are equivalent or not"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.5: Determine whether fractions are equivalent or not\n\n4. $\\frac{36}{24}$ and $\\frac{24}{16}$",
    "answer_text": "$$\n\\frac{36\\div12}{24\\div12}=\\frac{3}{2}\n$$\n$$\n\\frac{24\\div8}{16\\div8}=\\frac{3}{2}\n$$\nThe fractions $\\frac{36}{24}$ and $\\frac{24}{16}$ are equivalent.",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b026-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Comparing fractions",
      "h3": "Exercise 4.5: Determine whether fractions are equivalent or not"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.5: Determine whether fractions are equivalent or not\n\n5. $\\frac{8}{10}$ and $\\frac{18}{20}$",
    "answer_text": "$$\n\\frac{8\\div2}{10\\div2}=\\frac{4}{5}\n$$\n$$\n\\frac{18\\div2}{20\\div2}=\\frac{9}{10}\n$$\nThe fractions $\\frac{8}{10}$ and $\\frac{18}{20}$ are NOT equivalent.",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
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
  "subtopic_id": "jss1-math-fractions-equivalent-fractions",
  "subtopic_title": "Equivalent fractions",
  "curriculum_objectives": [
    {
      "source": {
        "curriculum_objective_id": "jss1-math-fractions-equivalent-fractions-po01",
        "source_performance_objective_index": 1,
        "text": "Identify equivalent fractions"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "equivalent-fractions-ao-identify-equivalent-fractions",
          "text": "Identify equivalent fractions."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-fractions-equivalent-fractions-po02",
        "source_performance_objective_index": 2,
        "text": "Find the equivalence of any given fraction using a formula"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "equivalent-fractions-ao-find-equivalence-using-formula",
          "text": "Find the equivalence of any given fraction using a formula."
        }
      ]
    },
    {
      "source": {
        "curriculum_objective_id": "jss1-math-fractions-equivalent-fractions-po03",
        "source_performance_objective_index": 3,
        "text": "Apply equivalent fractions in sharing commodities"
      },
      "atomic_decomposition": [
        {
          "atomic_objective_id": "equivalent-fractions-ao-apply-in-sharing-commodities",
          "text": "Apply equivalent fractions in sharing commodities."
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
    "record_id": "ch04-b014",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": null
    },
    "content_text": "Fractions that represent the same part of a whole in different ways are called equivalent fractions. Look at the three diagrams below. The fraction of the rectangle that is shaded is given next to each diagram.\n\nAll three fractions represent half of the rectangle. The fractions have different numerators and denominators, but they all represent the value $\\frac{1}{2}$.\n\n$$\n\\therefore\\frac{1}{2}=\\frac{2}{4}=\\frac{4}{8}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b015",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": null
    },
    "content_text": "equivalent fractions\n\nEquivalent fractions are fractions that have different numerators and denominators, but they represent the same part of a whole, and they have the same value.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b016",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": null
    },
    "content_text": "We find equivalent fractions by multiplying or dividing the numerator and the denominator by the same whole number.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b017",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Worked example 4.3: Working out equivalent fractions"
    },
    "content_text": "",
    "prompt_text": "Find the missing numbers in these equivalent fractions:\n\n$$\n\\frac{3}{4}=\\frac{\\square}{16}=\\frac{6}{\\square}=\\frac{15}{\\square}\n$$",
    "answer_text": "$$\n\\frac{3}{4}=\\frac{\\square}{16}=\\frac{6}{\\square}=\\frac{15}{\\square}\n$$\n\n            Step 1: Start with the first pair. Identify what is given, which in this case is the two denominators. Was the first denominator multiplied or divided to get the second denominator, and by what whole number?\n\n            $$\n\\frac{3}{4}=\\frac{\\square}{16}\n$$\n\n            The denominator was multiplied by 4 to get 16:\n\n            $$\n\\frac{3\\phantom{000}}{4\\times 4}=\\frac{\\square}{16}\n$$\n\n            Step 2: Repeat the action identified in Step 1 for the remaining part of the fraction.\n\n            The numerator must also be multiplied by 4:\n\n            $$\n\\frac{3\\times 4}{4\\times 4}=\\frac{12}{16}\n$$\n\n            Step 3: Repeat Steps 1 and 2 to find the next missing number.\n\n            $$\n\\frac{3}{4}=\\frac{12}{16}=\\frac{6}{\\square}\n$$\n\n            The numerator was divided by 2:\n\n            $$\n\\frac{3}{4}=\\frac{12\\div2}{16\\phantom{000}}=\\frac{6}{\\square}\n$$\n\n            The denominator must also be divided by 2:\n\n            $$\n\\frac{3}{4}=\\frac{12\\div2}{16\\div 2}=\\frac{6}{8}\n$$\n\n            Step 4: Repeat Steps 1 and 2 for the last fraction. If it is not possible to perform Step 1 with the fraction to the left of the missing number, use any other fraction that is complete.\n\n            $$\n\\frac{3}{4}=\\frac{12}{16}=\\frac{6}{8}=\\frac{15}{\\square}\n$$\n\n            It is not possible to multiply the numerator 6 or the numerator 12 by a whole number and then get 15 as an answer. You have to use the fraction $\\frac{3}{4}$.\n\n            The numerator was multiplied by 5:\n\n            $$\n\\frac{3}{4}=\\frac{3\\times5}{4\\phantom{000}}=\\frac{15}{\\square}\n$$\n\n            The denominator must also be multiplied by 5:\n\n            $$\n\\frac{3}{4}=\\frac{3\\times5}{4\\times5}=\\frac{15}{20}\n$$\n\n            Step 5: Write down the full answer.\n\n            $$\n\\frac{3}{4}=\\frac{12}{16}=\\frac{6}{8}=\\frac{15}{20}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b018",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Find equivalent fractions"
    },
    "content_text": "Improper fractions can also have equivalent fractions. Earlier on in this chapter, we showed that $2\\frac{1}{2}$ apples is equal to $\\frac{5}{2}$ apples. The improper fraction $\\frac{5}{2}$ tells us that we are dealing with apple halves and that we have 5 apple halves.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-013.png)\n\nSuppose we cut each apple half into two pieces. We will then have ten apple quarters.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-016.png)\n\nThis may be expressed as $\\frac{10}{4}$. The denominator tells us that there are 4 parts in one whole apple, so we are dealing with quarters. The numerator tells us that we have 10 quarters. Therefore, the fractions $\\frac{5}{2}$ and $\\frac{10}{4}$ are equivalent fractions. In this case, the numerator and denominator were multiplied by 2:\n\n$$\n\\frac{5\\times2}{2\\times2}=\\frac{10}{4}\n$$",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b019",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.3: Determine equivalent fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.3: Determine equivalent fractions\n\nFind the missing numbers in each list of equivalent fractions.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b019-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.3: Determine equivalent fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.3: Determine equivalent fractions\n\nFind the missing numbers in each list of equivalent fractions.\n\n1. $$\n\\frac{3}{7}=\\frac{\\square}{42}=\\frac{9}{\\square}=\\frac{6}{\\square}\n$$",
    "answer_text": "$$\n\\frac{3\\times6}{7\\times6}=\\frac{\\fbox{18}}{42}\n$$\n\n$$\n\\frac{18\\div2}{42\\div2}=\\frac{9}{\\fbox{21}}\n$$\n\n$$\n\\frac{3\\times2}{7\\times2}=\\frac{6}{\\fbox{14}}\n$$\n\n$$\n\\therefore\\frac{3}{7}=\\frac{18}{42}=\\frac{9}{21}=\\frac{6}{14}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b019-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.3: Determine equivalent fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.3: Determine equivalent fractions\n\nFind the missing numbers in each list of equivalent fractions.\n\n2. $$\n\\frac{2}{5}=\\frac{\\square}{15}=\\frac{8}{\\square}=\\frac{\\square}{250}\n$$",
    "answer_text": "$$\n\\frac{2\\times3}{5\\times3}=\\frac{\\fbox{6}}{15}\n$$\n\n$$\n\\frac{2\\times4}{5\\times4}=\\frac{8}{\\fbox{20}}\n$$\n\n$$\n\\frac{2\\times50}{5\\times50}=\\frac{\\fbox{100}}{250}\n$$\n\n$$\n\\therefore\\frac{2}{5}=\\frac{6}{15}=\\frac{8}{20}=\\frac{100}{250}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b019-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.3: Determine equivalent fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.3: Determine equivalent fractions\n\nFind the missing numbers in each list of equivalent fractions.\n\n3. $$\n\\frac{\\square}{6}=\\frac{5}{30}=\\frac{15}{\\square}=\\frac{\\square}{12}\n$$",
    "answer_text": "$$\n\\frac{5\\div5}{30\\div5}=\\frac{\\fbox{1}}{6}\n$$\n\n$$\n\\frac{5\\times3}{30\\times3}=\\frac{15}{\\fbox{90}}\n$$\n\n$$\n\\frac{1\\times2}{6\\times2}=\\frac{\\fbox{2}}{12}\n$$\n\n$$\n\\therefore\\frac{1}{6}=\\frac{5}{30}=\\frac{15}{90}=\\frac{2}{12}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b019-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.3: Determine equivalent fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.3: Determine equivalent fractions\n\nFind the missing numbers in each list of equivalent fractions.\n\n4. $$\n\\frac{8}{3}=\\frac{\\square}{6}=\\frac{\\square}{24}=\\frac{24}{\\square}\n$$",
    "answer_text": "$$\n\\frac{8\\times2}{3\\times2}=\\frac{\\fbox{16}}{6}\n$$\n\n$$\n\\frac{16\\times4}{6\\times4}=\\frac{\\fbox{64}}{24}\n$$\n\n$$\n\\frac{8\\times3}{3\\times3}=\\frac{24}{\\fbox{9}}\n$$\n\n$$\n\\therefore\\frac{8}{3}=\\frac{16}{6}=\\frac{64}{24}=\\frac{24}{9}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b019-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.3: Determine equivalent fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.3: Determine equivalent fractions\n\nFind the missing numbers in each list of equivalent fractions.\n\n5. $$\n\\frac{24}{27}=\\frac{8}{\\square}=\\frac{64}{\\square}=\\frac{40}{\\square}\n$$",
    "answer_text": "$$\n\\frac{24\\div3}{27\\div3}=\\frac{8}{\\fbox{9}}\n$$\n\n$$\n\\frac{8\\times8}{9\\times8}=\\frac{64}{\\fbox{72}}\n$$\n\n$$\n\\frac{8\\times5}{9\\times5}=\\frac{40}{\\fbox{45}}\n$$\n\n$$\n\\therefore\\frac{24}{27}=\\frac{8}{9}=\\frac{64}{72}=\\frac{40}{45}\n$$",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b020",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Simplify equivalent fractions"
    },
    "content_text": "A fraction is in its **simplest form** when the numerator and the denominator have no common factor. For example, $\\frac{1}{2}$ is the simplest form of the fractions $\\frac{2}{4}$ and $\\frac{4}{8}$. These fractions are not in their simplest form, because in $\\frac{2}{4}$, 2 and 4 have 2 as a common factor, and in $\\frac{4}{8}$, 4 and 8 have 2 and 4 as common factors.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b021",
    "record_type": "definition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Simplify equivalent fractions"
    },
    "content_text": "**simplest form** A fraction is in its simplest form when the numerator and denominator have no common factor.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b022",
    "record_type": "worked_example",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Worked example 4.4: Finding the simplest form of a fraction"
    },
    "content_text": "",
    "prompt_text": "Find the simplest form of the fraction $\\frac{40}{60}$.",
    "answer_text": "Step 1: Find the smallest prime number that is a factor of both the numerator and the denominator. In this case the factor is 2.\nStep 2: Divide both the numerator and denominator by this prime number. Write down the equivalent fraction.\nStep 3: Repeat until the prime number can no longer divide into both the numerator and the denominator.\nStep 4: Move on to the next prime number that is a factor of both the numerator and the denominator. In this case the factor is 5. Divide both the numerator and the denominator by 5.\nStep 5: Repeat this process until the numerator and the denominator have no more common factors.\n\n$$\n\\frac{40\\div2}{60\\div2}=\\frac{20}{30}\n$$\n\n$$\n\\frac{20\\div2}{30\\div2}=\\frac{10}{15}\n$$\n\n$$\n\\frac{10\\div5}{15\\div5}=\\frac{2}{3}\n$$\n\nThe simplest form of $\\frac{40}{60}$ is $\\frac{2}{3}$.\n\nMethod 2 (HCF)\n1. Express both the numerator and the denominator as a product of their prime numbers.\n2. Find the HCF of the numerator and the denominator.\n3. Divide the numerator and the denominator by their HCF.\n\n$$\n\\begin{array}{r | r}\n 2 & 40 \\\\\n \\hline\n 2 & 20 \\\\\n \\hline\n 2 & 10 \\\\\n \\hline\n 5 & 5 \\\\\n \\hline\n & 1\n \\end{array}\n$$\n\n$$\n40=2^3\\times5\n$$\n\n$$\n\\begin{array}{r | r}\n 2 & 60 \\\\\n \\hline\n 2 & 30 \\\\\n \\hline\n 3 & 15 \\\\\n \\hline\n 5 & 5 \\\\\n \\hline\n & 1\n \\end{array}\n$$\n\n$$\n60=2^2\\times3\\times5\n$$\n\n$$\n\\therefore \\text{HCF}=2^2\\times5=2\\times2\\times5=20\n$$\n\n$$\n\\frac{40\\div20}{60\\div20}=\\frac{2}{3}\n$$\n\nThe simplest form of $\\frac{40}{60}$ is $\\frac{2}{3}$.\n\nIf necessary, go back to Chapter 2 to see how to find the highest common factor (HCF) of two or more numbers.\n\nMethod 3 (Inspection)\n1. Find any common factor of the numerator and the denominator.\n2. Divide both the numerator and denominator by this factor. Write down the equivalent fraction.\n3. Repeat this process until the numerator and the denominator have no more common factors.\n\n$$\n\\frac{40\\div10}{60\\div10}=\\frac{4}{6}\n$$\n\n$$\n\\frac{4\\div2}{6\\div2}=\\frac{2}{3}\n$$\n\nThe simplest form of $\\frac{40}{60}$ is $\\frac{2}{3}$.",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b023",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.4: Simplify fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.4: Simplify fractions\n\nFind the simplest form of each of the following fractions, using the method of your choice.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b023-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.4: Simplify fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.4: Simplify fractions\n\nFind the simplest form of each of the following fractions, using the method of your choice.\n\n1. $$\n\\frac{39}{78}\n$$",
    "answer_text": "Using Method 1 (Prime numbers):\n\n$$\n\\frac{39\\div3}{78\\div3}=\\frac{13}{26}\n$$\n\n$$\n\\frac{13\\div13}{26\\div13}=\\frac{1}{2}\n$$\n\nThe simplest form of $\\frac{39}{78}$ is $\\frac{1}{2}$.",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b023-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.4: Simplify fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.4: Simplify fractions\n\nFind the simplest form of each of the following fractions, using the method of your choice.\n\n2. $$\n\\frac{12}{108}\n$$",
    "answer_text": "Using Method 1 (Prime numbers):\n\n$$\n\\frac{12\\div2}{108\\div2}=\\frac{6}{54}\n$$\n\n$$\n\\frac{6\\div2}{54\\div2}=\\frac{3}{27}\n$$\n\n$$\n\\frac{3\\div3}{27\\div3}=\\frac{1}{9}\n$$\n\nThe simplest form of $\\frac{12}{108}$ is $\\frac{1}{9}$.",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b023-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.4: Simplify fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.4: Simplify fractions\n\nFind the simplest form of each of the following fractions, using the method of your choice.\n\n3. $$\n\\frac{16}{64}\n$$",
    "answer_text": "Using Method 2 (HCF):\n\n$$\n16=2^4\n$$\n\n$$\n64=2^6\n$$\n\n$$\n\\therefore \\text{HCF}=2^4=2\\times2\\times2\\times2=16\n$$\n\n$$\n\\frac{16\\div16}{64\\div16}=\\frac{1}{4}\n$$\n\nThe simplest form of $\\frac{16}{64}$ is $\\frac{1}{4}$.",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b023-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.4: Simplify fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.4: Simplify fractions\n\nFind the simplest form of each of the following fractions, using the method of your choice.\n\n4. $$\n\\frac{45}{75}\n$$",
    "answer_text": "Using Method 2 (HCF):\n\n$$\n45=3^2\\times5\n$$\n\n$$\n75=3\\times5^2\n$$\n\n$$\n\\therefore \\text{HCF}=3\\times5=15\n$$\n\n$$\n\\frac{45\\div15}{75\\div15}=\\frac{3}{5}\n$$\n\nThe simplest form of $\\frac{45}{75}$ is $\\frac{3}{5}$.",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b023-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Exercise 4.4: Simplify fractions"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.4: Simplify fractions\n\nFind the simplest form of each of the following fractions, using the method of your choice.\n\n5. $$\n\\frac{250}{150}\n$$",
    "answer_text": "Using Method 3 (Inspection):\n\n$$\n\\frac{250\\div10}{150\\div10}=\\frac{25}{15}\n$$\n\n$$\n\\frac{25\\div5}{15\\div5}=\\frac{5}{3}\n$$\n\nThe simplest form of $\\frac{250}{150}$ is $\\frac{5}{3}$.",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b024",
    "record_type": "exposition",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Identify equivalent fractions"
    },
    "content_text": "Fractions that are equivalent have the same simplest form. Look at the two diagrams below. The fraction of the rectangle that is shaded is given next to each diagram.\n\n![](https://electricbookworks.github.io/siyavula-open-textbooks-images/items/images/web/ebw-jss1-04-017.png)\n\nIt is easy to see that the fractions $\\frac{6}{8}$ and $\\frac{4}{8}$ are not equivalent. They do not represent the same part of the whole rectangle. We can check this by finding the simplest form of each fraction.\n\n$$\n\\frac{6\\div2}{8\\div2}=\\frac{3}{4}\n$$\n\n$$\n\\frac{4\\div4}{8\\div4}=\\frac{1}{2}\n$$\n\n$$\n\\frac{3}{4}\\neq\\frac{1}{2}\n$$\n\nThis shows that the fractions $\\frac{6}{8}$ and $\\frac{4}{8}$ do not have the same value. They are therefore not equivalent.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b025",
    "record_type": "note",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Equivalent fractions",
      "h3": "Identify equivalent fractions"
    },
    "content_text": "Remember that equivalent fractions have the same simplest form.",
    "prompt_text": "",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b026",
    "record_type": "exercise_block",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Comparing fractions",
      "h3": "Exercise 4.5: Determine whether fractions are equivalent or not"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.5: Determine whether fractions are equivalent or not\n\nFor each of the following pairs of fractions, determine whether they are equivalent or not.",
    "answer_text": "",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b026-i01",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Comparing fractions",
      "h3": "Exercise 4.5: Determine whether fractions are equivalent or not"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.5: Determine whether fractions are equivalent or not\n\n1. $\\frac{15}{18}$ and $\\frac{20}{24}$",
    "answer_text": "$$\n\\frac{15\\div3}{18\\div3}=\\frac{5}{6}\n$$\n$$\n\\frac{20\\div4}{24\\div4}=\\frac{5}{6}\n$$\nThe fractions $\\frac{15}{18}$ and $\\frac{20}{24}$ are equivalent.",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b026-i02",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Comparing fractions",
      "h3": "Exercise 4.5: Determine whether fractions are equivalent or not"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.5: Determine whether fractions are equivalent or not\n\n2. $\\frac{14}{70}$ and $\\frac{21}{105}$",
    "answer_text": "$$\n\\frac{14\\div7}{70\\div7}=\\frac{2}{10}=\\frac{1}{5}\n$$\n$$\n\\frac{21\\div7}{105\\div7}=\\frac{3}{15}=\\frac{1}{5}\n$$\nThe fractions $\\frac{14}{70}$ and $\\frac{21}{105}$ are equivalent.",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b026-i03",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Comparing fractions",
      "h3": "Exercise 4.5: Determine whether fractions are equivalent or not"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.5: Determine whether fractions are equivalent or not\n\n3. $\\frac{16}{48}$ and $\\frac{18}{72}$",
    "answer_text": "$$\n\\frac{16\\div8}{48\\div8}=\\frac{2}{6}=\\frac{1}{3}\n$$\n$$\n\\frac{18\\div6}{72\\div6}=\\frac{3}{12}=\\frac{1}{4}\n$$\nThe fractions $\\frac{16}{48}$ and $\\frac{18}{72}$ are NOT equivalent.",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b026-i04",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Comparing fractions",
      "h3": "Exercise 4.5: Determine whether fractions are equivalent or not"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.5: Determine whether fractions are equivalent or not\n\n4. $\\frac{36}{24}$ and $\\frac{24}{16}$",
    "answer_text": "$$\n\\frac{36\\div12}{24\\div12}=\\frac{3}{2}\n$$\n$$\n\\frac{24\\div8}{16\\div8}=\\frac{3}{2}\n$$\nThe fractions $\\frac{36}{24}$ and $\\frac{24}{16}$ are equivalent.",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
  },
  {
    "record_id": "ch04-b026-i05",
    "record_type": "exercise_item",
    "heading_path": {
      "h1": "Chapter 4: Equivalent fractions",
      "h2": "4.2 Comparing fractions",
      "h3": "Exercise 4.5: Determine whether fractions are equivalent or not"
    },
    "content_text": "",
    "prompt_text": "### Exercise 4.5: Determine whether fractions are equivalent or not\n\n5. $\\frac{8}{10}$ and $\\frac{18}{20}$",
    "answer_text": "$$\n\\frac{8\\div2}{10\\div2}=\\frac{4}{5}\n$$\n$$\n\\frac{18\\div2}{20\\div2}=\\frac{9}{10}\n$$\nThe fractions $\\frac{8}{10}$ and $\\frac{18}{20}$ are NOT equivalent.",
    "primary_subtopic_id": "jss1-math-fractions-equivalent-fractions"
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
