
# Chapter 3: Binary numbers

In Chapter 1 you learnt that we use the **base ten number system** for everyday counting. When we count using the base ten number system, we put objects in groups of ten. We use the numbers 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 as digits to make any other number, no matter how big or how small it is.

The base ten number system is also called the decimal number system. The prefix \"deci-\" comes from a Latin word that means \"one tenth\".

## 3.1 The base two number system

In this chapter you will learn about the **base two number system**. The base two number system is used in computers and other devices that also use computing functions. It is therefore a very important number system.

When we count using the base two number system, we put objects in groups of two. We use only two digits, namely 0 and 1, to make up any number.

The base two number system is also called the binary number system. The prefix \"bi-\" comes from a Latin word that means \"two\" or \"twice\".

> **base ten number system** The base ten number system is a number system that counts in groups of 10, and uses the digits 0; 1; 2; 3; 4; 5; 6; 7; 8; 9 to represent any number. It is also called the decimal number system.
>
> **base two number system** The base two number system is a number system that counts in groups of 2, and uses only the digits 0 and 1 to represent any number. It is also called the binary number system.

### Counting in the base two number system

In the base two number system, we go to a new group each time we reach a number that is a power of 2. We therefore count as follows:\
$$
\begin{array}{l l}
    \circledast & 1 \text{ unit} \\ 
    \color{green}{\circledast \, \circledast} & 1 \text{ group of two and } 0 \text{ units} \\
    \color{green}{\circledast \, \circledast} \, \color{black}{\circledast} & 1 \text{ group of two and } 1 \text{ unit} \\
    \end{array}
$$

If we add another object, we have 2 groups of two, which is 4. We continue counting as follows:\
$$
\begin{array}{l l}
    \color{blue}{\circledast \, \circledast \, \circledast \, \circledast} & 1 \text{ group of four}, \, 0 \text{ groups of two and } 0 \text{ units} \\
    \color{blue}{\circledast \, \circledast \, \circledast \, \circledast}\, \color{black}{\circledast} & 1 \text{ group of four}, \, 0 \text{ groups of two and } 1 \text{ unit} \\
    \color{blue}{\circledast \, \circledast \, \circledast \, \circledast} \, \color{green}{\circledast \, \circledast} & 1 \text{ group of four}, \, 1 \text{ group of two and } 0 \text{ units} \\
    \color{blue}{\circledast \, \circledast \, \circledast \, \circledast} \, \color{green}{\circledast \, \circledast} \, \color{black}{\circledast} & 1 \text{ group of four}, \, 1 \text{ group of two and } 1 \text{ unit} \\
    \end{array}
$$

If we add another object, we have 3 groups of two, which is 8. We continue counting as follows:\
$$
\begin{array}{l l}
    \color{orange}{\circledast \, \circledast \, \circledast \, \circledast \, \circledast \, \circledast \, \circledast \, \circledast} & 1 \text{ group of eight}, \, 0 \text{ groups of four}, \, 0 \text{ groups of two and } 0 \text{ units} \\
    \color{orange}{\circledast \, \circledast \, \circledast \, \circledast \, \circledast \, \circledast \, \circledast \, \circledast} \, \color{black}{\circledast} & 1 \text{ group of eight}, \, 0 \text{ groups of four}, \, 0 \text{ groups of two and } 1 \text{ unit} \\
    \color{orange}{\circledast \, \circledast \, \circledast \, \circledast \, \circledast \, \circledast \, \circledast \, \circledast} \, \color{green}{\circledast \, \circledast} & 1 \text{ group of eight}, \, 0 \text{ groups of four}, \, 1 \text{ group of two and } 0 \text{ units} \\
    \color{orange}{\circledast \, \circledast \, \circledast \, \circledast \, \circledast \, \circledast \, \circledast \, \circledast} \, \color{green}{\circledast \, \circledast} \, \color{black}{\circledast} & 1 \text{ group of eight}, \, 0 \text{ groups of four}, \, 1 \text{ group of two and } 1 \text{ unit} \\
    \color{orange}{\circledast \, \circledast \, \circledast \, \circledast \, \circledast \, \circledast \, \circledast \, \circledast} \, \color{blue}{\circledast \, \circledast \, \circledast \, \circledast} \,  & 1 \text{ group of eight}, \, 1 \text{ group of four}, \, 0 \text{ groups of two and } 0 \text{ units} \\
    \end{array}
$$

We can carry on like this. When we have 4 groups of two, we count in 16s.

## 3.2 Powers of 2

In the base ten number system we work with powers of 10. In the base two number system, we work with powers of 2.

The first ten powers of 2 are:

$$
\begin{array}{|l|r|l|}
        \hline
        \textbf{Name} & \textbf{Number} & \textbf{Powers of 2}  \\
        \hline 
        \text{Two} & 2 & 2=2^1    \\
        \hline
        \text{Four} & 4 & 2\times2=2^2    \\
        \hline
        \text{Eight} & 8 & 2\times2\times2=2^3    \\
        \hline
        \text{Sixteen} & 16 & 2\times2\times2\times2=2^4    \\
        \hline
        \text{Thirty two} & 32 & 2\times2\times2\times2\times2=2^5    \\
        \hline
        \text{Sixty four} & 64 & 2\times2\times2\times2\times2\times2=2^6    \\
        \hline
        \text{One hundred and twenty eight} & 128 & 2\times2\times2\times2\times2\times2\times2=2^7    \\
        \hline
        \text{Two hundred and fifty six} & 256 & 2\times2\times2\times2\times2\times2\times2\times2=2^8    \\
        \hline
        \text{Five hundred and twelve} & 512 & 2\times2\times2\times2\times2\times2\times2\times2\times2=2^9    \\
        \hline
        \text{One thousand and twenty four} & 1,024 & 2\times2\times2\times2\times2\times2\times2\times2\times2\times2=2^{10}    \\
        \hline
        \end{array}
$$

In the base ten number system, you used place value tables to identify the value of each digit in a number. The place values were powers of 10.

We can use place value tables in the base two number system as well. The place values are powers of 2. For example:

$$
\begin{array}{|c|c|c|c|c|}
    \hline
    \text{sixteens} & \text{eights} & \text{fours} & \text{twos} & \text{units} \\
    (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\
    \hline
    &  &  & &  \\
    \hline
    \end{array}
$$

Remember that any number to the power of zero is equal to one. Therefore, $2^0=1$.

To work with binary numbers, you need to be able to write a decimal number as the sum of powers of 2.

Remember that a decimal number is a number that uses the base ten number system. Decimal numbers are the numbers we use in everyday life.


### Worked example 3.1: Writing a decimal number as the sum of powers of 2

> Write the number 53 as the sum of powers of 2. Then write the number in this base two place value table.

$$
\begin{array}{|c|c|c|c|c|c|}
    \hline
    \text{thirty twos} & \text{sixteens} & \text{eights} & \text{fours} & \text{twos} & \text{units} \\
    (2^5) & (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\
    \hline
    & &  &  & &  \\
    \hline
    \end{array}
$$

1.  Step 1: Find the largest power of 2 that is equal to or smaller than 53.

    There is not a power of 2 that is equal to 53.

    Try $2^6$. $2^6=64$, so it is bigger than 53 and we can\'t use it.

    The next, smaller power of 2 is $2^5$, and $2^5=32$. So the largest power of 2 that is equal to or smaller than 53 is $2^5=32$.

2.  Step 2: Write the given number, 53, as the sum of this power of 2 and what is still left.

    $$
    53-32=21
    $$

    So written as a sum, we get:

    $$
    53=32+21
    $$

3.  Step 3: Now we have to deal with the 21. Find the largest power of 2 that is equal to or smaller than 21.

    $$
    2^4=16
    $$
    $$
    21-16=5
    $$

4.  Step 4: Write the given number, 53, as the sum of all of these numbers.

    $$
    \begin{align}
        53&=32+21 \\
        &=32+16+5
        \end{align}
    $$

5.  Step 5: Now we have to deal with the 5. Find the largest power of 2 that is equal to or smaller than 5.

    $$
    2^2=4
    $$
    $$
    5-4=1
    $$

6.  Step 6: Write the given number, 53, as the sum of all of these numbers.

    $$
    \begin{align}
        53&=32+21 \\
        &=32+16+5 \\
        &=32+16+4+1
        \end{align}
    $$

    The last number found is 1, so there are no more powers of 2 that we can find.

7.  Step 7: Write the sum of powers of 2 in index form.

    Remember that $2^0 = 1$.

    $$
    53=2^5+2^4+2^2+2^0
    $$

8.  Step 8: Put the powers of 2 in a base two place value table.

    Where you have a power of 2 in your sum, you write a 1 in the place value table.

    Where you do not have a power of 2 in your sum, you write a 0 in the place value table. You do not have a $2^3$ or a $2^1$, so for those place values you write 0.

    $$
    \begin{array}{|c|c|c|c|c|c|}
        \hline
        \text{thirty twos} & \text{sixteens} & \text{eights} & \text{fours} & \text{twos} & \text{units} \\
        (2^5) & (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\
        \hline
        1 & 1 & 0 & 1 & 0 & 1 \\
        \hline
        \end{array}
    $$

This means that the decimal (base ten) number 53 written as a binary (base two) number is 110101.


Here is a table with the powers of 2. You can refer back to it as you answer the questions that follow.

$$
\begin{array}{|c|} 
    \hline
    2^0=1 \\
    \hline
    2^1=2 \\
    \hline
    2^2=4 \\
    \hline
    2^3=8 \\
    \hline
    2^4=16\\
    \hline
    2^5=32 \\
    \hline
    2^6=64 \\
    \hline
    2^7=128 \\
    \hline
    2^8=256 \\
    \hline
    \end{array}
$$


### Exercise 3.1: Write decimal numbers as the sum of powers of 2

Write each decimal number as the sum of powers of 2. Then write the number in a base two place value table.

1.  39

    $$
    \begin{align}
    39&=32+7 \\
    &=32+4+3 \\
    &=32+4+2+1 \\
    &=2^5+2^2+2^1+2^0
    \end{align}
    $$
$$
\begin{array}{|c|c|c|c|c|c|c|}
    \hline
    (2^6) & (2^5) & (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\
    \hline
    & 1 & 0 & 0 & 1 & 1 & 1 \\
    \hline
    \end{array}
$$

2.  75

    $$
    \begin{align}
    75&=64+11 \\
    &=64+8+3 \\
    &=64+8+2+1 \\
    &=2^6+2^3+2^1+2^0
    \end{align}
    $$
$$
\begin{array}{|c|c|c|c|c|c|c|}
    \hline
    (2^6) & (2^5) & (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\
    \hline
    1 & 0 & 0 & 1 & 0 & 1 & 1 \\
    \hline
    \end{array}
$$

3.  120

    $$
    \begin{align}
    120&=64+56 \\
    &=64+32+24 \\
    &=64+32+16+8 \\
    &=2^6+2^5+2^4+2^3
    \end{align}
    $$
$$
\begin{array}{|c|c|c|c|c|c|c|}
    \hline
    (2^6) & (2^5) & (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\
    \hline
    1 & 1 & 1 & 1 & 0 & 0 & 0 \\
    \hline
    \end{array}
$$

4.  228

    $$
    \begin{align}
    228&=128+100 \\
    &=128+64+36 \\
    &=128+64+32+4 \\
    &=2^7+2^6+2^5+2^2
    \end{align}
    $$
$$
\begin{array}{|c|c|c|c|c|c|c|c|}
    \hline
    (2^7) & (2^6) & (2^5) & (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\
    \hline
    1 & 1 & 1 & 0 & 0 & 1 & 0 & 0 \\
    \hline
    \end{array}
$$

5.  277

    $$
    \begin{align}
    277&=256+21 \\
    &=256+16+5 \\
    &=256+16+4+1 \\
    &=2^8+2^4+2^2+2^0
    \end{align}
    $$
$$
\begin{array}{|c|c|c|c|c|c|c|c|c|}
    \hline
    (2^8) & (2^7) & (2^6) & (2^5) & (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\
    \hline
    1 & 0 & 0 & 0 & 1 & 0 & 1 & 0 & 0 \\
    \hline
    \end{array}
$$


## 3.3 Binary numbers

The numbers in the base two number system are called **binary numbers**.

> **binary numbers** The numbers in the base two number system are called binary numbers. They are all represented by combinations of the digits 0 and 1.

We can use a place value table to write the numbers 1 to 16 in the decimal number system as binary numbers:

$$
\begin{array}{|c|c|c|c|c||c|c|}
    \hline
    \text{sixteens} & \text{eights} & \text{fours} & \text{twos} & \text{units} & \text{binary number} & \text{decimal number} \\
    (2^4) & (2^3) & (2^2) & (2^1) & (2^0) & & \\
    \hline
    & & &  & 1 & 1 & 1 \\
    \hline
    & & & 1 & 0 & 10 & 2 \\
    \hline
    & & & 1 & 1 & 11 & 3 \\
    \hline
    & & 1 & 0 & 0 & 100 & 4 \\
    \hline
    & & 1 & 0 & 1 & 101 & 5 \\
    \hline
    & & 1 & 1 & 0 & 110 & 6 \\
    \hline
    & & 1 & 1 & 1 & 111 & 7 \\
    \hline
    & 1 & 0 & 0 & 0 & 1000 & 8 \\
    \hline
    & 1 & 0 & 0 & 1 & 1001 & 9 \\
    \hline
    & 1 & 0 & 1 & 0 & 1010 & 10 \\
    \hline
    & 1 & 0 & 1 & 1 & 1011 & 11 \\
    \hline
    & 1 & 1 & 0 & 0 & 1100 & 12 \\
    \hline
    & 1 & 1 & 0 & 1 & 1101 & 13 \\
    \hline
    & 1 & 1 & 1 & 0 & 1110 & 14 \\
    \hline
    & 1 & 1 & 1 & 1 & 1111 & 15 \\
    \hline
    1 & 0 & 0 & 0 & 0 & 10000 & 16 \\
    \hline
    \end{array}
$$

### Notation of decimal and binary numbers

When we work with decimal and binary numbers together, we need a way to identify whether a number is a decimal number or a binary number. For example, the digits 100 represent one hundred objects in the base ten number system, but they represent four objects in the base two number system.

We use subscripts to tell us which system a certain combination of digits belong to. For example:

- $100_{10}$ or $100_{\text{ten}}$ means one hundred
- $100_2$ or $100_{\text{two}}$ means four.

## 3.4 Converting between decimal and binary numbers


### Worked example 3.2: Converting binary numbers to decimal numbers

> Write $11010_\text{two}$ as a base ten number.

1.  Step 1: Draw up a place value table for the powers of 2. Use the number of digits in the given number to help you do this.

    The number $11010_2$ has 5 digits. The place value table must have 5 columns.

    Start at the right with $2^0$, and count to the left. So this place value table goes up to $2^4$.

    $$
    \begin{array}{|c|c|c|c|c|}
        \hline
        \text{sixteens} & \text{eights} & \text{fours} & \text{twos} & \text{units} \\
        (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\
        \hline
          &  &  &  &  \\
        \hline
        \end{array}
    $$

2.  Step 2: Write the given number in the place value table.

    $$
    \begin{array}{|c|c|c|c|c|}
        \hline
        \text{sixteens} & \text{eights} & \text{fours} & \text{twos} & \text{units} \\
        (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\
        \hline
        1 & 1 & 0 & 1 & 0 \\
        \hline
        \end{array}
    $$

3.  Step 3: Write down the place value of each digit. Add all the values to get the base ten number.

    $$
    \begin{align}
        & \, 2^4+2^3+0+2^1+0 \\
        = & \, 16+8+2 \\
        = & \, 26
        \end{align}
    $$
$$
\therefore 11010_\text{two} = 26_\text{ten}
$$



### Exercise 3.2: Convert binary numbers to base ten numbers

Convert each of the following binary numbers to base ten numbers.

1.
    $$
    101_\text{two}
    $$

    $$
    \begin{array}{|c|c|c|c|c|}
    \hline
    (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\
    \hline
    &  & 1 & 0 & 1 \\
    \hline
    \end{array}
    $$
$$
4+1=5
$$
$$
\therefore 101_\text{two}=5_\text{ten}
$$

2.
    $$
    1001_\text{two}
    $$

    $$
    \begin{array}{|c|c|c|c|c|}
    \hline
    (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\
    \hline
    & 1 & 0 & 0 & 1 \\
    \hline
    \end{array}
    $$
$$
8+1=9
$$
$$
\therefore 1001_\text{two}=9_\text{ten}
$$

3.
    $$
    1111_\text{two}
    $$

    $$
    \begin{array}{|c|c|c|c|c|}
    \hline
    (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\
    \hline
    & 1 & 1 & 1 & 1 \\
    \hline
    \end{array}
    $$
$$
8+4+2+1=15
$$
$$
\therefore 1111_\text{two}=15_\text{ten}
$$

4.
    $$
    10011_\text{two}
    $$

    $$
    \begin{array}{|c|c|c|c|c|}
    \hline
    (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\
    \hline
    1 & 0 & 0 & 1 & 1 \\
    \hline
    \end{array}
    $$
$$
16+2+1=19
$$
$$
\therefore 10011_\text{two}=19_\text{ten}
$$

5.
    $$
    11000_\text{two}
    $$

    $$
    \begin{array}{|c|c|c|c|c|}
    \hline
    (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\
    \hline
    1 & 1 & 0 & 0 & 0 \\
    \hline
    \end{array}
    $$
$$
16+8=24
$$
$$
\therefore 11000_\text{two}=24_\text{ten}
$$

6.
    $$
    11110_\text{two}
    $$

    $$
    \begin{array}{|c|c|c|c|c|}
    \hline
    (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\
    \hline
    1 & 1 & 1 & 1 & 0 \\
    \hline
    \end{array}
    $$
$$
16+8+4+2=30
$$
$$
\therefore 11110_\text{two}=30_\text{ten}
$$

7.
    $$
    101001_\text{two}
    $$

    $$
    \begin{array}{|c|c|c|c|c|c|}
    \hline
    (2^5) & (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\
    \hline
    1 & 0 & 1 & 0 & 0 & 1 \\
    \hline
    \end{array}
    $$
$$
32+8+1=41
$$
$$
\therefore 101001_\text{two}=41_\text{ten}
$$

8.
    $$
    111010_\text{two}
    $$

    $$
    \begin{array}{|c|c|c|c|c|c|}
    \hline
    (2^5) & (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\
    \hline
    1 & 1 & 1 & 0 & 1 & 0 \\
    \hline
    \end{array}
    $$
$$
32+16+8+2=58
$$
$$
\therefore 111010_\text{two}=58_\text{ten}
$$

9.
    $$
    1000111_\text{two}
    $$

    $$
    \begin{array}{|c|c|c|c|c|c|c|}
    \hline
    (2^6) & (2^5) & (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\
    \hline
    1 & 0 & 0 & 0 & 1 & 1 & 1 \\
    \hline
    \end{array}
    $$
$$
64+4+2+1=71
$$
$$
\therefore 1000111_\text{two}=71_\text{ten}
$$

10.
    $$
    1010011_\text{two}
    $$

    $$
    \begin{array}{|c|c|c|c|c|c|c|}
    \hline
    (2^6) & (2^5) & (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\
    \hline
    1 & 0 & 1 & 0 & 0 & 1 & 1 \\
    \hline
    \end{array}
    $$
$$
64+16+2+1=83
$$
$$
\therefore 1010011_\text{two}=83_\text{ten}
$$



### Worked example 3.3: Converting decimal numbers to binary numbers

> Write $23_\text{ten}$ as a base two number.

1.  Step 1: Divide the given number repeatedly by 2, until you get zero. For each division, write down whether the remainder is 0 or 1.

    $$
    \begin{array}{r|rr}
        2 & 23 & \\
        \hline
        2 & 11 & \text{remainder: }1 \\
        \hline
        2 & 5 & \text{remainder: }1 \\
        \hline
        2 & 2 & \text{remainder: }1 \\
        \hline
        2 & 1 & \text{remainder: }0 \\
        \hline
          & 0 & \text{remainder: }1 \\
        \hline
        \end{array}
    $$

2.  Step 2: Write down the remainders from bottom to top. This gives the corresponding binary number.

    $$
    10111
    $$
    $$
    \therefore  23_\text{ten}= 10111_\text{two}
    $$

If you do not feel comfortable with the method explained here, you can write the decimal number as the sum of powers of 2 and then use a place value table. This is shown in Worked example 3.2.



### Exercise 3.3: Convert decimal numbers to base two numbers

Convert each of the following decimal numbers to base two numbers.

Remember that when you write the remainders, you start from the bottom one and go up to the top one.

1.
    $$
    7_\text{ten}
    $$

    $$
    \begin{array}{r|rr}
    2 & 7 & \\
    \hline
    2 & 3 & \text{remainder: }1 \\
    \hline
    2 & 1 & \text{remainder: }1 \\
    \hline
    & 0 & \text{remainder: }1 \\
    \hline
    \end{array}
    $$
$$
\therefore 7_\text{ten}=111_\text{two}
$$

2.
    $$
    11_\text{ten}
    $$

    $$
    \begin{array}{r|rr}
    2 & 11 & \\
    \hline
    2 & 5 & \text{remainder: }1 \\
    \hline
    2 & 2 & \text{remainder: }1 \\
    \hline
    2 & 1 & \text{remainder: }0 \\
    \hline
    & 0 & \text{remainder: }1 \\
    \hline
    \end{array}
    $$
$$
\therefore 11_\text{ten}=1011_\text{two}
$$

3.
    $$
    13_\text{ten}
    $$

    $$
    \begin{array}{r|rr}
    2 & 13 & \\
    \hline
    2 & 6 & \text{remainder: }1 \\
    \hline
    2 & 3 & \text{remainder: }0 \\
    \hline
    2 & 1 & \text{remainder: }1 \\
    \hline
    & 0 & \text{remainder: }1 \\
    \hline
    \end{array}
    $$
$$
\therefore 13_\text{ten}=1101_\text{two}
$$

4.
    $$
    20_\text{ten}
    $$

    $$
    \begin{array}{r|rr}
    2 & 20 & \\
    \hline
    2 & 10 & \text{remainder: }0 \\
    \hline
    2 & 5 & \text{remainder: }0 \\
    \hline
    2 & 2 & \text{remainder: }1 \\
    \hline
    2 & 1 & \text{remainder: }0 \\
    \hline    
    & 0 & \text{remainder: }1 \\
    \hline
    \end{array}
    $$
$$
\therefore 20_\text{ten}=10100_\text{two}
$$

5.
    $$
    29_\text{ten}
    $$

    $$
    \begin{array}{r|rr}
    2 & 29 & \\
    \hline
    2 & 14 & \text{remainder: }1 \\
    \hline
    2 & 7 & \text{remainder: }0 \\
    \hline
    2 & 3 & \text{remainder: }1 \\
    \hline
    2 & 1 & \text{remainder: }1 \\
    \hline    
    & 0 & \text{remainder: }1 \\
    \hline
    \end{array}
    $$
$$
\therefore 29_\text{ten}=11101_\text{two}
$$

6.
    $$
    36_\text{ten}
    $$

    $$
    \begin{array}{r|rr}
    2 & 36 & \\
    \hline
    2 & 18 & \text{remainder: }0 \\
    \hline
    2 & 9 & \text{remainder: }0 \\
    \hline
    2 & 4 & \text{remainder: }1 \\
    \hline
    2 & 2 & \text{remainder: }0 \\
    \hline    
    2 & 1 & \text{remainder: }0 \\
    \hline    
    & 0 & \text{remainder: }1 \\
    \hline
    \end{array}
    $$
$$
\therefore 36_\text{ten}=100100_\text{two}
$$

7.
    $$
    44_\text{ten}
    $$

    $$
    \begin{array}{r|rr}
    2 & 44 & \\
    \hline
    2 & 22 & \text{remainder: }0 \\
    \hline
    2 & 11 & \text{remainder: }0 \\
    \hline
    2 & 5 & \text{remainder: }1 \\
    \hline
    2 & 2 & \text{remainder: }1 \\
    \hline    
    2 & 1 & \text{remainder: }0 \\
    \hline    
    & 0 & \text{remainder: }1 \\
    \hline
    \end{array}
    $$
$$
\therefore 44_\text{ten}=101100_\text{two}
$$

8.
    $$
    65_\text{ten}
    $$

    $$
    \begin{array}{r|rr}
    2 & 65 & \\
    \hline
    2 & 32 & \text{remainder: }1 \\
    \hline
    2 & 16 & \text{remainder: }0 \\
    \hline
    2 & 8 & \text{remainder: }0 \\
    \hline
    2 & 4 & \text{remainder: }0 \\
    \hline    
    2 & 2 & \text{remainder: }0 \\
    \hline  
    2 & 1 & \text{remainder: }0 \\
    \hline    
    & 0 & \text{remainder: }1 \\
    \hline
    \end{array}
    $$
$$
\therefore 65_\text{ten}=1000001_\text{two}
$$

9.
    $$
    78_\text{ten}
    $$

    $$
    \begin{array}{r|rr}
    2 & 78 & \\
    \hline
    2 & 39 & \text{remainder: }0 \\
    \hline
    2 & 19 & \text{remainder: }1 \\
    \hline
    2 & 9 & \text{remainder: }1 \\
    \hline
    2 & 4 & \text{remainder: }1 \\
    \hline    
    2 & 2 & \text{remainder: }0 \\
    \hline  
    2 & 1 & \text{remainder: }0 \\
    \hline    
    & 0 & \text{remainder: }1 \\
    \hline
    \end{array}
    $$
$$
\therefore 78_\text{ten}=1001110_\text{two}
$$

10.
    $$
    97_\text{ten}
    $$

    $$
    \begin{array}{r|rr}
    2 & 97 & \\
    \hline
    2 & 48 & \text{remainder: }1 \\
    \hline
    2 & 24 & \text{remainder: }0 \\
    \hline
    2 & 12 & \text{remainder: }0 \\
    \hline
    2 & 6 & \text{remainder: }0 \\
    \hline    
    2 & 3 & \text{remainder: }0 \\
    \hline  
    2 & 1 & \text{remainder: }1 \\
    \hline    
    & 0 & \text{remainder: }1 \\
    \hline
    \end{array}
    $$
$$
\therefore 97_\text{ten}=1100001_\text{two}
$$


## 3.5 Summary

- The base two number system is a number system that counts in groups of 2, and uses only the digits 0 and 1 to represent any number.
- In the base ten number system we work with powers of 10. In the base two number system, we work with powers of 2.
- We can use place value tables in the base two number system. The place values are powers of 2. For example:\
  $$
  \begin{array}{|c|c|c|c|c|c|}
        \hline
        \text{thirty twos} & \text{sixteens} & \text{eights} & \text{fours} & \text{twos} & \text{units} \\
        (2^5) & (2^4) & (2^3) & (2^2) & (2^1) & (2^0) \\
        \hline
        &  &  & & & \\
        \hline
        \end{array}
  $$
- The numbers in the base two number system are called binary numbers. They are all represented by combinations of the digits 0 and 1.
- The binary numbers that correspond to the decimal numbers 1 to 10 are:\
  $$
  \begin{array}{|c|c|}
        \hline
        \text{decimal number} & \text{binary number} \\
        \hline
        1& 1 \\
        2& 10 \\
        3& 11 \\
        4& 100 \\
        5& 101 \\
        6& 110 \\
        7& 111 \\
        8& 1000 \\
        9& 1001 \\
        10& 1010 \\
        \hline
        \end{array}
  $$
- We use subscripts to tell us which system a certain combination of digits belong to. For example:
  - $100_{10}$ or $100_{\text{ten}}$ means one hundred
  - $100_2$ or $100_{\text{two}}$ means four
- We can convert binary numbers to decimal numbers, and decimal numbers to binary numbers.
