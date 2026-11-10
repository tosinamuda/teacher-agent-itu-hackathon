
# Chapter 8: Operations with binary numbers

In Chapter 3 you learnt about the base two number system. The base two or binary number system counts in groups of 2, and uses only the digits 0 and 1 to represent any number. The numbers in the base two number system are called binary numbers.

We can use place value tables in the base two number system. The place values are powers of 2. For example:

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

The binary numbers that correspond to the decimal numbers 1 to 10 are:

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

We use subscripts to tell us which system a certain combination of digits belong to. For example:

- $100_{10}$ or $100_{\text{ten}}$ means one hundred
- $100_2$ or $100_{\text{two}}$ means four

In this chapter you will learn how to add, subtract and multiply binary numbers.

## 8.1 Addition

When we add binary numbers, we follow the same principles as when we add numbers in the base ten number system.


### Worked example 8.1: Revision of addition in the base ten number system

> Find the total of $794+648+89$.

1.  Step 1: Write the numbers one below the other. Line up the units, tens, hundreds, thousands, and so on.

    $$
    \begin{array}{r r}
         & \text{th}\, \text{h}\, \text{t}\, \text{u} \\
         & 7\,9\,4 \\
         +& 6\,4\,8 \\
         +& 8\,9 \\
         \hline
         \end{array}
    $$

2.  Step 2: Add the units. Divide the answer by 10. Carry over the quotient and write down the remainder.

    Remember that the quotient is the result you get after you have divided.

    $$
    4+8+9=21
    $$
    $$
    21=(2\times10)+1
    $$
    $$
    \begin{array}{r r}
         & \text{th}\, \text{h}\, \text{t}\, \text{u} \\
         &_{2} \,\phantom{0}\\
         & 7\,9\,4 \\
         +& 6\,4\,8 \\
         +& 8\,9 \\
         \hline
         &1\\
         \hline
         \end{array}
    $$

3.  Step 3: Repeat Step 2 for the tens column.

    $$
    2+9+4+8=23
    $$
    $$
    23=(2\times10)+3
    $$
    $$
    \begin{array}{r r}
         & \text{th}\, \text{h}\, \text{t}\, \text{u} \\
         &_{2}\,_{2} \,\phantom{0}\\
         & 7\,9\,4 \\
         +& 6\,4\,8 \\
         +& 8\,9 \\
         \hline
         &3\,1\\
         \hline
         \end{array}
    $$

4.  Step 4: Repeat Step 3 for the hundreds column.

    $$
    2+7+6=15
    $$
    $$
    15=(1\times10)+5
    $$
    $$
    \begin{array}{r r}
         & \text{th}\, \text{h}\, \text{t}\, \text{u} \\
         &_{1}\,_{2}\,_{2} \,\phantom{0}\\
         & 7\,9\,4 \\
         +& 6\,4\,8 \\
         +& 8\,9 \\
         \hline
         &5\,3\,1\\
         \hline
         \end{array}
    $$

5.  Step 5: Bring down the quotient that was carried over to the thousands column.

    $$
    \begin{array}{r r}
         & \text{th}\, \text{h}\, \text{t}\, \text{u} \\
         &_{1}\,_{2}\,_{2} \,\phantom{0}\\
         & 7\,9\,4 \\
         +& 6\,4\,8 \\
         +& 8\,9 \\
         \hline
         &1,\,5\,3\,1\\
         \hline
         \end{array}
    $$

    The answer is 1,531.


In the base two number system, we work in groups of 2. So, instead of dividing by 10, we divide by 2.


### Worked example 8.2: Addition in the base two number system (Method 1)

> Find the sum of $101_\text{two}$ and $111_\text{two}$.

1.  Step 1: Write the numbers one below the other, without the subscript \"two\". Line up the units ( $2^0$), twos ( $2^1$), fours ( $2^2$) and eights ( $2^3$).

    $$
    \begin{array}{r r}
         & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
         & 1\;\;0\;\;1\;\, \\
         +& 1\;\;1\;\;1\;\, \\
         \hline
         \end{array}
    $$

2.  Step 2: Add the units (in the $2^0$ column). Divide the answer by 2. Carry over the quotient and write down the remainder.

    $$
    1+1=2
    $$
    $$
    2=(1\times2)+0
    $$
    $$
    \begin{array}{r r}
         & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
         &_{1} \phantom{000}\\
         & 1\;\;0\;\;1\;\, \\
         +& 1\;\;1\;\;1\;\, \\
         \hline
         & 0\;\, \\
         \hline
         \end{array}
    $$

3.  Step 3: Repeat Step 2 for the twos ( $2^1$) column.

    $$
    1+1=2
    $$
    $$
    2=(1\times2)+0
    $$
    $$
    \begin{array}{r r}
         & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
         &_{1}\;\;_{1} \phantom{000}\\
         & 1\;\;0\;\;1\;\, \\
         +& 1\;\;1\;\;1\;\, \\
         \hline
         & 0\;\;0\;\, \\
         \hline
         \end{array}
    $$

4.  Step 4: Repeat Step 3 for the fours ( $2^2$) column.

    $$
    1+1+1=3
    $$
    $$
    3=(1\times2)+1
    $$
    $$
    \begin{array}{r r}
         & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
         &_{1}\;\;_{1}\;\;_{1} \phantom{000}\\
         & 1\;\;0\;\;1\;\, \\
         +& 1\;\;1\;\;1\;\, \\
         \hline
         & 1\;\;0\;\;0\;\, \\
         \hline
         \end{array}
    $$

5.  Step 5: Bring down the quotient that was carried over to the eights ( $2^3$) column.

    $$
    \begin{array}{r r}
         & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
         &_{1}\;\;_{1}\;\;_{1} \phantom{000}\\
         & 1\;\;0\;\;1\;\, \\
         +& 1\;\;1\;\;1\;\, \\
         \hline
         &1\;\; 1\;\;0\;\;0\;\, \\
         \hline
         \end{array}
    $$

    The answer is $1100_\text{two}$.

6.  Step 6: Check your answer by converting to the base ten number system, adding, and then converting back to a base two number.

    $$
    \begin{align}
         101_2&=2^2+0+2^0 \\
         &=4+1 \\
         &=5_{10}\\
         \end{align}
    $$
$$
\quad
$$
$$
\begin{align}
         111_2&=2^2+2^1+2^0 \\
         &=4+2+1 \\
         &=7_{10}\\
         \end{align}
$$
$$
\quad
$$
$$
5+7=12
$$
$$
\quad
$$
$$
\begin{align}
         12_{10}&=8+4 \\
         &=2^3+2^2+0+0 \\
         &=1100_2\\
         \end{align}
$$

    The answer is correct.


Another way to do addition in the base two number system is to use these basic rules:

$0+0=0$\
$0+1=1$\
$1+0=1$\
$1+1=10$\
$1+1+1=11$

> Remember:\
> $2_\text{ten}=10_\text{two}$\
> $3_\text{ten}=11_\text{two}$


### Worked example 8.3: Addition in the base two number system (Method 2)

> Find the sum of $101_\text{two}$ and $111_\text{two}$.

1.  Step 1: Write the numbers one below the other, without the subscript \"two\". Line up the units ( $2^0$), twos ( $2^1$), fours ( $2^2$) and eights ( $2^3$).

    $$
    \begin{array}{r r}
         & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
         & 1\;\;0\;\;1\;\, \\
         +& 1\;\;1\;\;1\;\, \\
         \hline
         \end{array}
    $$

2.  Step 2: Add the units in the base two number system. If the answer is 10 or 11, carry over the left-hand 1 and write down the right-hand 0 or 1.

    Remember to use $1+1=10$ and $1+1+1=11$.

    $$
    \begin{array}{r r}
         & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
         &_{1} \phantom{000}\\
         & 1\;\;0\;\;1\;\, \\
         +& 1\;\;1\;\;1\;\, \\
         \hline
         & 0\;\, \\
         \hline
         \end{array}
    $$

3.  Step 3: Repeat Step 2 for the twos ( $2^1$) column.

    $$
    1+1=10
    $$
    $$
    \begin{array}{r r}
         & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
         &_{1}\;\;_{1} \phantom{000}\\
         & 1\;\;0\;\;1\;\, \\
         +& 1\;\;1\;\;1\;\, \\
         \hline
         & 0\;\;0\;\, \\
         \hline
         \end{array}
    $$

4.  Step 4: Repeat Step 3 for the fours ( $2^2$) column.

    $$
    1+1+1=11
    $$
    $$
    \begin{array}{r r}
         & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
         &_{1}\;\;_{1}\;\;_{1} \phantom{000}\\
         & 1\;\;0\;\;1\;\, \\
         +& 1\;\;1\;\;1\;\, \\
         \hline
         & 1\;\;0\;\;0\;\, \\
         \hline
         \end{array}
    $$

5.  Step 5: Bring down the one that was carried over to the eights ( $2^3$) column.

    $$
    \begin{array}{r r}
         & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
         &_{1}\;\;_{1}\;\;_{1} \phantom{000}\\
         & 1\;\;0\;\;1\;\, \\
         +& 1\;\;1\;\;1\;\, \\
         \hline
         &1\;\; 1\;\;0\;\;0\;\, \\
         \hline
         \end{array}
    $$

    The answer is $1100_\text{two}$.

6.  Step 6: Check your answer using the base ten number system.

    $$
    \begin{align}
         101_2&=2^2+0+2^0 \\
         &=4+1 \\
         &=5_{10}\\
         \end{align}
    $$
$$
\quad
$$
$$
\begin{align}
         111_2&=2^2+2^1+2^0 \\
         &=4+2+1 \\
         &=7_{10}\\
         \end{align}
$$
$$
\quad
$$
$$
5+7=12
$$
$$
\quad
$$
$$
\begin{align}
         12_{10}&=8+4 \\
         &=2^3+2^2+0+0 \\
         &=1100_2\\
         \end{align}
$$

    The answer is correct.



### Exercise 8.1: Add binary numbers

Calculate each of the following in the base two number system.

1.
    $$
    100+10
    $$

    $$
    \begin{array}{r r}
    & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
    & \phantom{000}\\
    & 1\;\;0\;\;0\;\, \\
    +& 1\;\;0\;\, \\
    \hline
    &1\;\; 1\;\;0\;\;0\;\, \\
    \hline
    \end{array}
    $$

2.
    $$
    101+11
    $$

    > Remember to use $1+1=10$ where you need to.
    >
    $$
    \begin{array}{r r}
    & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
    &_{1}\;\;_{1}\;\;_{1} \phantom{000}\\
    & 1\;\;0\;\;1\;\, \\
    +& 1\;\;1\;\, \\
    \hline
    &1\;\; 0\;\;0\;\;0\;\, \\
    \hline
    \end{array}
    $$

3.
    $$
    110+11
    $$

    $$
    \begin{array}{r r}
    & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
    &_{1}\;\;_{1} \phantom{00000}\\
    & 1\;\;1\;\;0\;\, \\
    +& 1\;\;1\;\, \\
    \hline
    &1\;\; 0\;\;0\;\;1\;\, \\
    \hline
    \end{array}
    $$

4.
    $$
    111+10
    $$

    $$
    \begin{array}{r r}
    & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
    &_{1}\;\;_{1} \phantom{00000}\\
    & 1\;\;1\;\;1\;\, \\
    +& 1\;\;0\;\, \\
    \hline
    &1\;\; 0\;\;0\;\;1\;\, \\
    \hline
    \end{array}
    $$

5.
    $$
    100+101
    $$

    $$
    \begin{array}{r r}
    & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
    &_{1}\;\;\phantom{000000}\\
    & 1\;\;0\;\;0\;\, \\
    +& 1\;\;0\;\;1\;\, \\
    \hline
    &1\;\; 0\;\;0\;\;1\;\, \\
    \hline
    \end{array}
    $$

6.
    $$
    101+110
    $$

    $$
    \begin{array}{r r}
    & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
    &_{1}\;\;\phantom{000000}\\
    & 1\;\;0\;\;1\;\, \\
    +& 1\;\;1\;\;0\;\, \\
    \hline
    &1\;\; 0\;\;1\;\;1\;\, \\
    \hline
    \end{array}
    $$

7.
    $$
    110+111
    $$

    > Remember to use $1+1=10$ and $1+1+1=11$ where you need to.
    >
    $$
    \begin{array}{r r}
    & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
    &_{1}\;\;_{1}\phantom{00000}\\
    & 1\;\;1\;\;0\;\, \\
    +& 1\;\;1\;\;1\;\, \\
    \hline
    &1\;\; 1\;\;0\;\;1\;\, \\
    \hline
    \end{array}
    $$

8.
    $$
    111+111
    $$

    $$
    \begin{array}{r r}
    & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
    &_{1}\;\;_{1}\;\;_{1}\phantom{000}\\
    & 1\;\;1\;\;1\;\, \\
    +& 1\;\;1\;\;1\;\, \\
    \hline
    &1\;\; 1\;\;1\;\;0\;\, \\
    \hline
    \end{array}
    $$

9.
    $$
    1010+11
    $$

    $$
    \begin{array}{r r}
    & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
    &_{1}\phantom{00000}\\
    & 1\;\;0\;\;1\;\;0\;\, \\
    +& 1\;\;1\;\, \\
    \hline
    &1\;\; 1\;\;0\;\;1\;\, \\
    \hline
    \end{array}
    $$

10.
    $$
    1111+11
    $$

    $$
    \begin{array}{r r}
    & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
    &_{1}\;\;_{1}\;\;_{1}\;\;_{1}\phantom{000}\\
    & 1\;\;1\;\;1\;\;1\;\, \\
    +& 1\;\;1\;\, \\
    \hline
    &1\;\;0\;\; 0\;\;1\;\;0\;\, \\
    \hline
    \end{array}
    $$


## 8.2 Subtraction

When we subtract binary numbers, we follow the same principles as when we subtract numbers in the base ten number system.


### Worked example 8.4: Revision of subtraction in the base ten number system

> Subtract 178 from 4,032.

1.  Step 1: Write the numbers one below the other. Line up the units, tens, hundreds, thousands, and so on.

    $$
    \begin{array}{r r}
          & \text{th}\, \text{h}\, \text{t}\, \text{u} \\
         & 4,0\,3\,2 \\
                 - & 1\,7\,8 \\
         \hline
         \end{array}
    $$

2.  Step 2: Subtract the units column. If there are not enough units to subtract from, move a group of ten from the column to the left.

    Move one group from the tens column to the units column:

    - The tens column becomes $3-1=2$.
    - The units column becomes $2+10=12$.

    $$
    \begin{array}{r r}
          & \text{th}\;\, \text{h}\;\, \text{t}\;\, \text{u}\; \\
          &_{2}\;\,_{12} \\
         & 4,0\,\cancel{3}\cancel{2} \\
                 - & 1\;\,7\;8\;\, \\
         \hline
         &4\;\,\\
         \hline
         \end{array}
    $$

3.  Step 3: Repeat Step 2 with the tens column. If needed, move a group of ten from the column to the left.

    There are no groups in the hundreds column. Move one group from the thousands column to the hundreds column. Then move one group from the hundreds column to the tens column.

    - The thousands column becomes $4-1=3$.
    - The hundreds column becomes $0+10-1=9$.
    - The tens column becomes $2+10=12$.

    $$
    \begin{array}{r r}
          & \text{th}\phantom{0}\; \text{h}\phantom{0}\; \text{t}\phantom{0} \text{u}\; \\
          &_{3}\;\;\; _{9}\;\;_{12}\,_{12}\, \\
         & \cancel{4},\cancel{0}\,\cancel{3}\cancel{2} \\
                 - & 1\;\;\,7\;\,8\; \\
          \hline
         &5\;\,4\;\\
         \hline
         \end{array}
    $$

4.  Step 4: Repeat Step 3 with the hundreds and thousands columns.

    $$
    \begin{array}{r r}
          & \text{th}\phantom{0}\; \text{h}\phantom{0}\; \text{t}\phantom{0} \text{u}\; \\
          &_{3}\;\;\; _{9}\;\;_{12}\,_{12}\, \\
         & \cancel{4},\cancel{0}\,\cancel{3}\cancel{2} \\
                 - & 1\;\;\,7\;\,8\; \\
          \hline
         &3,\phantom{0}8\;\;\,5\;\,4\;\\
         \hline
         \end{array}
    $$


In the base two number system, we work in groups of 2. So, instead of moving groups of 10 between columns, we move groups of 2.


### Worked example 8.5: Subtraction in the base two number system (Method 1)

> Subtract $101_\text{two}$ from $1010_\text{two}$.

1.  Step 1: Write the numbers one below the other, without the subscript \"two\". Line up the units ( $2^0$), twos ( $2^1$), fours ( $2^2$), eights ( $2^3$), and so on.

    $$
    \begin{array}{r r}
         & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
         & 1\;\;0\;\;1\;\;0\;\, \\
         -& 1\;\;0\;\;1\;\, \\
         \hline
         \end{array}
    $$

2.  Step 2: Subtract the units column. If there are not enough units to subtract from, move a group of two from the column to the left.

    Move one group from the twos ( $2^1$) column to the units ( $2^0$) column:

    - The twos column ( $2^1$) becomes $1-1=0$.
    - The units column ( $2^0$) becomes $0+2=2$.

    $$
    \begin{array}{r r}
         & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
         &_{0}\;\;_{2} \;\,\\
         & 1\;\,0\;\cancel{1}\;0\;\, \\
         -& 1\;\;0\;\;1\;\, \\
         \hline
         &1\;\, \\
         \hline
         \end{array}
    $$

3.  Step 3: Repeat Step 2 for the twos ( $2^1$) column.

    $$
    \begin{array}{r r}
         & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
         &_{0}\;\;_{2} \;\,\\
         & 1\;\,0\;\cancel{1}\;0\;\, \\
         -& 1\;\;0\;\;1\;\, \\
         \hline 
         &0\;\;1\;\, \\
         \hline
         \end{array}
    $$

4.  Step 4: Repeat Step 2 for the fours ( $2^2$) column.

    Move one group from the eights ( $2^3$) column to the fours ( $2^2$) column:

    - The eights column ( $2^3$) becomes $1-1=0$.
    - The fours column ( $2^2$) becomes $0+2=2$.

    $$
    \begin{array}{r r}
         & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
         &_{0}\;\;_{2}\;\;\,_{0}\;\;_{2} \;\,\\
         & \cancel{1}\;0\;\cancel{1}\;0\;\, \\
         -& 1\;\;0\;\;1\;\, \\
         \hline
         &1\;\;0\;\;1\;\, \\
         \hline
         \end{array}
    $$

5.  Step 5: Check your answer using the base ten number system.

    $$
    \begin{align}
         1010_2&=2^3+0+2^1+0 \\
         &=8+2 \\
         &=10_{10}\\
         \end{align}
    $$
$$
\quad
$$
$$
\begin{align}
         101_2&=2^2+0+2^0 \\
         &=4+1 \\
         &=5_{10}\\
         \end{align}
$$
$$
\quad
$$
$$
10-5=5
$$
$$
\quad
$$
$$
\begin{align}
         5_{10}&=4+1 \\
         &=2^2+0+2^0 \\
         &=101_2\\
         \end{align}
$$

    The answer is correct.


Another way to do subtraction in the base two number system is to use these basic rules:

$0-0=0$\
$1-0=0$\
$1-1=0$\
$10-1=1$\
$11-1=10$

> Remember:\
> $2_\text{ten}=10_\text{two}$\
> $3_\text{ten}=11_\text{two}$


### Worked example 8.6: Subtraction in the base two number system (Method 2)

> Subtract $101_\text{two}$ from $1010_\text{two}$.

1.  Step 1: Write the numbers one below the other, without the subscript \"two\". Line up the units ( $2^0$), twos ( $2^1$), fours ( $2^2$), eights ( $2^3$), and so on.

    $$
    \begin{array}{r r}
         & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
         & 1\;\;0\;\;1\;\;0\;\, \\
         -& 1\;\;0\;\;1\;\, \\
         \hline
         \end{array}
    $$

2.  Step 2: Subtract the units column. If the top digit in the column is 0 and the bottom digit 1, move 1 from the column to left.

    Move the 1 from the twos ( $2^1$) column to the units ( $2^0$) column.

    - The twos column ( $2^1$) becomes $0$.
    - The units column ( $2^0$) becomes $10$.

    In the base two number system, $10-1=1$.

    $$
    \begin{array}{r r}
         & \color{blue}{2^3 \; 2^2 \; 2^1 \; 2^0 }\\
         &_{0}\,\phantom{000} \\
         & 1\;\;0\;\cancel{1} \color{red}{1}\color{black}{0}\;\, \\
         -& 1\;\;0\;\;\,1\;\, \\
         \hline
         &1\;\, \\
         \hline
         \end{array}
    $$

3.  Step 3: Repeat Step 2 for the twos ( $2^1$) column.

    $$
    \begin{array}{r r}
         & \color{blue}{2^3 \; 2^2 \; 2^1 \; 2^0 }\\
         &_{0}\,\phantom{000} \\
         & 1\;\;0\;\cancel{1} \color{red}{1}\color{black}{0}\;\, \\
         -& 1\;\;0\;\;\,1\;\, \\
         \hline
         &0\;\;\,1\;\, \\
         \hline
         \end{array}
    $$

4.  Step 4: Repeat Step 2 for the fours ( $2^2$) column.

    Move the 1 from the eights ( $2^3$) column to the fours ( $2^2$) column.

    - The eights column ( $2^3$) becomes $0$.
    - The fours column ( $2^2$) becomes $10$.

    In the base two number system $10-1=1$.

    $$
    \begin{array}{r r}
         & \color{blue}{2^3 \; 2^2 \; 2^1 \; 2^0 }\\
         &_{0}\,\phantom{000}_{0}\,\phantom{000} \\
         & \cancel{1}\color{red}{1}\color{black}{0} \cancel{1} \color{red}{1}\color{black}{0}\;\, \\
         -& 1\;\;0\;\;\,1\;\, \\
         \hline
         &1\;\;0\;\;\,1\;\, \\
         \hline
         \end{array}
    $$

5.  Step 5: Check your answer using the base ten number system.

    $$
    \begin{align}
         1010_2&=2^3+0+2^1+0 \\
         &=8+2 \\
         &=10_{10}\\
         \end{align}
    $$
$$
\quad
$$
$$
\begin{align}
         101_2&=2^2+0+2^0 \\
         &=4+1 \\
         &=5_{10}\\
         \end{align}
$$
$$
\quad
$$
$$
10-5=5
$$
$$
\quad
$$
$$
\begin{align}
         5_{10}&=4+1 \\
         &=2^2+0+2^0 \\
         &=101_2\\
         \end{align}
$$

    The answer is correct.



### Exercise 8.2: Subtract binary numbers

Calculate each of the following in the base two number system.

1.
    $$
    111-110
    $$

    $$
    \begin{array}{r r}
    & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
    & \phantom{000}\\
    & 1\;\;1\;\;1\;\, \\
    -& 1\;\;1\;\;0\;\, \\
    \hline
    &1\;\, \\
    \hline
    \end{array}
    $$

2.
    $$
    111-101
    $$

    $$
    \begin{array}{r r}
    & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
    & \phantom{000}\\
    & 1\;\;1\;\;1\;\, \\
    -& 1\;\;0\;\;1\;\, \\
    \hline
    &1\;\;0\;\, \\
    \hline
    \end{array}
    $$

3.
    $$
    111-100
    $$

    $$
    \begin{array}{r r}
    & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
    & \phantom{000}\\
    & 1\;\;1\;\;1\;\, \\
    -& 1\;\;0\;\;0\;\, \\
    \hline
    &1\;\;1\;\, \\
    \hline
    \end{array}
    $$

4.
    $$
    110-100
    $$

    $$
    \begin{array}{r r}
    & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
    & \phantom{000}\\
    & 1\;\;1\;\;0\;\, \\
    -& 1\;\;0\;\;0\;\, \\
    \hline
    &1\;\;0\;\, \\
    \hline
    \end{array}
    $$

5.
    $$
    101-11
    $$

    > Remember, in the base two number system, $10-1=1$.
    >
    $$
    \begin{array}{r r}
    & \color{blue}{2^3 \, 2^2 \; 2^1 \, 2^0 }\\
    &_{0}\;\phantom{00000} \\
    & \cancel{1} \color{red}{1}\color{black}{0}\;\;1\;\, \\
    -& 1\;\;1\;\, \\
    \hline
    &1\;\;0\;\, \\
    \hline
    \end{array}
    $$

6.
    $$
    110-101
    $$

    $$
    \begin{array}{r r}
    & \color{blue}{2^3 \, 2^2 \, 2^1 \; 2^0 }\\
    &_{0}\,\phantom{000} \\
    & 1\;\cancel{1} \color{red}{1}\color{black}{0}\;\, \\
    -& 1\;\;0\;\;\,1\;\, \\
    \hline
    &1\;\, \\
    \hline
    \end{array}
    $$

7.
    $$
    110-11
    $$

    $$
    \begin{array}{r r}
    & \color{blue}{2^3 \, 2^2 \, 2^1 \; 2^0 }\\
    &_{0}\;\,_{\color{red}{1}\color{black}{0}}\phantom{000} \\
    & \cancel{1} \cancel{1} \color{red}{1}\color{black}{0}\;\, \\
    -& 1\;\;1\;\, \\
    \hline
    &1\;\;1\;\, \\
    \hline
    \end{array}
    $$

8.
    $$
    100-11
    $$

    $$
    \begin{array}{r r}
    & \color{blue}{2^3 \;\; 2^2 \;\; 2^1 \;\, 2^0 }\\
    &_{0}\,\phantom{00}_{1}\phantom{000}\; \\
    & \cancel{1\phantom{.}}\! \cancel{\color{red}{1}\color{black}{0}} \color{red}{1}\color{black}{0}\;\, \\
    -& 1\;\;\;1\;\, \\
    \hline
    &1\;\, \\
    \hline
    \end{array}
    $$
    >
    > When you move the 1 from the fours column, you have 10 in the twos column. When you then move 1 from the twos column, there is $10-1=1$ left in the twos column. And $1-1=0$.

9.
    $$
    1001-10
    $$

    $$
    \begin{array}{r r}
    & \color{blue}{2^3 \;\; 2^2 \;\; 2^1 \;\, 2^0 }\\
    &_{0}\,\phantom{00}_{1}\phantom{00000}\; \\
    & \cancel{1\phantom{.}}\! \cancel{\color{red}{1}\color{black}{0}} \color{red}{1}\color{black}{0}\;\;1\;\, \\
    -& 1\;\;0\;\, \\
    \hline
    &1\;\;\,1\;\;1\;\, \\
    \hline
    \end{array}
    $$
    >
    > When you move the 1 from the eights column, you have 10 in the fours column. When you then move 1 from the fours column, there is $10-1=1$ left in the fours column. And \$\$1-0=1\$.

10.
    $$
    1000-11
    $$

    > Remember that $10-1=1$ in the base two number system.
    >
    $$
    \begin{array}{r r}
    & \color{blue}{2^3 \;\; 2^2 \;\; 2^1 \;\, 2^0 }\\
    &_{0}\,\phantom{00}_{1}\,\phantom{00}_{1}\phantom{000}\; \\
    & \cancel{1\phantom{.}}\! \cancel{\color{red}{1}\color{black}{0}} \cancel{\color{red}{1}\color{black}{0}} \color{red}{1}\color{black}{0}\;\, \\
    -& 1\;\;\;1\;\, \\
    \hline
    &1\;\;\;\,0\;\;\;1\;\, \\
    \hline
    \end{array}
    $$


## 8.3 Multiplication

Last year you learnt how to multiply integers using long multiplication. We use the same principles when multiplying numbers in the base two number system.


### Worked example 8.7: Revision of multiplication in the base ten number system

> Multiply 32 by 14.

1.  Step 1: Write the numbers one below the other. Line up the units, tens, hundreds, and so on.

    $$
    \begin{array}{r r}
         & \text{h}\, \text{t}\, \text{u} \\
         & 3\,2 \\
         \times & 1\,4 \\
         \hline
         \end{array}
    $$

2.  Step 2: Multiply the first (top) number by the units of the second number.

    $$
    \begin{array}{r r}
         & \text{h}\, \text{t}\, \text{u} \\
         & 3\,2 \\
         \times & 1\,\color{red}{4} \\
         \hline
         & 1\,2\,8
         \end{array}
    $$

3.  Step 3: Start a new line. Insert a zero in the units column.

    $$
    \begin{array}{r r}
         & \text{h}\, \text{t}\, \text{u} \\
         & 3\,2 \\
         \times & 1\,4 \\
         \hline
         & 1\,2\,8 \\
         & 0
         \end{array}
    $$

4.  Step 4: Multiply the first (top) number by the tens of the second number.

    $$
    \begin{array}{r r}
         & \text{h}\, \text{t}\, \text{u} \\
         & 3\,2 \\
         \times & \color{red}{1}\, \color{black}{4} \\
         \hline
         & 1\,2\,8 \\
         & 3\,2\,0 
         \end{array}
    $$

5.  Step 5: Add the two numbers from Step 4.

    $$
    \begin{array}{r r}
         & \text{h}\, \text{t}\, \text{u} \\
         & 3\,2 \\
         \times & 1\, 4 \\
         \hline
         & 1\,2\,8 \\
         & 3\,2\,0 \\
         \hline
         & 4\,4\,8 \\
         \hline
         \end{array}
    $$


Multiplication of the digits 0 and 1 work the same in the base ten and base two number systems:

$0\times0=0$\
$1\times0=0$\
$0\times1=0$\
$1\times1=1$


### Worked example 8.8: Multiplication in the base two number system

> Multiply $11_\text{two}$ by $11_\text{two}$.

1.  Step 1: Write the numbers one below the other, without the subscript \"two\". Line up the units ( $2^0$), twos ( $2^1$), fours ( $2^2$), eights ( $2^3$), and so on.

    $$
    \begin{array}{r r}
         & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
         & 1\;\;1\;\, \\
         \times& 1\;\;1\;\, \\
         \hline
         \end{array}
    $$

2.  Step 2: Multiply the first (top) number by the units of the second number.

    $$
    \begin{array}{r r}
         & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
         & 1\;\;1\;\, \\
         \times& 1\;\;\color{red}{1}\;\, \\
         \hline
         & 1\;\;1\;\, 
         \end{array}
    $$

3.  Step 3: Start a new line. Insert a zero in the units ( $2^0$) column.

    $$
    \begin{array}{r r}
         & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
         & 1\;\;1\;\, \\
         \times& 1\;\;\color{red}{1}\;\, \\
         \hline
         & 1\;\;1\;\, \\
         & 0 \;\,
         \end{array}
    $$

4.  Step 4: Multiply the first (top) number by the twos ( $2^1$) of the second number.

    $$
    \begin{array}{r r}
         & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
         & 1\;\;1\;\, \\
         \times& \color{red}{1} \;\;\color{black}{1}\;\, \\
         \hline
         & 1\;\;1\;\, \\
         & 1\;\;1\;\;0 \;\,
         \end{array}
    $$

5.  Step 5: Add the two numbers from Step 4.

    This adding step in a multiplication works differently in the base two number system. You need to use the base two addition rules: $1+1=10$ and $1+1+1=11$.

    If the answer in any column is 10 or 11, carry over the left-hand 1 and write down the right-hand 0 or 1.

    $$
    \begin{array}{r r}
         & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
         & 1\;\;1\;\, \\
         \times& 1 \;\; 1\;\, \\
         \hline
         & 1\;\;1\;\, \\
         & ^1\;^1 1\;\;1\;\;0 \;\, \\
         \hline
         & 1\;\;0\;\;0\;\;1\;\, \\
         \hline
         \end{array}
    $$

6.  Step 6: Check your answer using the base ten number system.

    $$
    \begin{align}
         11_2&=2^1+2^0 \\
         &=2+1 \\
         &=3_{10}\\
         \end{align}
    $$
$$
\quad
$$
$$
3 \times 3 = 9
$$
$$
\quad
$$
$$
\begin{align}
         9_{10}&=8+1 \\
         &=2^3+0+0+2^0 \\
         &=1001_2\\
         \end{align}
$$

    The answer is correct.



### Exercise 8.3: Multiply binary numbers

Calculate each of the following in the base two number system.

1.
    $$
    10 \times 10
    $$

    $$
    \begin{array}{r r}
    & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
    & 1\;\;0\;\, \\
    \times& 1 \;\; 0\;\, \\
    \hline
    & 0\;\;0\;\, \\
    & 1\;\;0\;\;0 \;\, \\
    \hline
    & 1\;\;0\;\;0\;\, \\
    \hline
    \end{array}
    $$

2.
    $$
    10 \times 11
    $$

    $$
    \begin{array}{r r}
    & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
    & 1\;\;0\;\, \\
    \times& 1 \;\; 1\;\, \\
    \hline
    & 1\;\;0\;\, \\
    & 1\;\;0\;\;0 \;\, \\
    \hline
    & 1\;\;1\;\;0\;\, \\
    \hline
    \end{array}
    $$

3.
    $$
    100 \times 10
    $$

    $$
    \begin{array}{r r}
    & \color{blue}{2^3 \, 2^2 \, 2^1 \, 2^0 }\\
    & 1\;\;0\;\;0\;\, \\
    \times& 1 \;\; 0\;\, \\
    \hline
    & 0\;\;0\;\;0\;\, \\
    & 1\;\;0\;\;0\;\;0 \;\, \\
    \hline
    & 1\;\;0\;\;0\;\;0\;\, \\
    \hline
    \end{array}
    $$

4.
    $$
    110 \times 11
    $$

    $$
    \begin{array}{r r}
    & \color{blue}{2^4 \,2^3 \, 2^2 \, 2^1 \, 2^0 }\\
    & 1\;\;1\;\;0\;\, \\
    \times& 1 \;\; 1\;\, \\
    \hline
    & 1\;\;1\;\;0\;\, \\
    & ^1 \;^1 1\;\;1\;\;0\;\;0 \;\, \\
    \hline
    & 1\;\;0\;\;0\;\;1\;\;0\;\, \\
    \hline
    \end{array}
    $$

5.
    $$
    111 \times 11
    $$

    $$
    \begin{array}{r r}
    & \color{blue}{2^4 \,2^3 \, 2^2 \, 2^1 \, 2^0 }\\
    & 1\;\;1\;\;1\;\, \\
    \times& 1 \;\; 1\;\, \\
    \hline
    & ^1 1\;\;1\;\;1\;\, \\
    & ^1 \;^1 1\;\;1\;\;1\;\;0 \;\, \\
    \hline
    & 1\;\;0\;\;1\;\;0\;\;1\;\, \\
    \hline
    \end{array}
    $$


## 8.4 Summary

- From Chapter 3 you know that:
  - $2_\text{ten}=10_\text{two}$Â 
  - $3_\text{ten}=11_\text{two}$Â 
- Use the following basic rules when adding binary numbers:
  - $0+0=0$Â 
  - $0+1=1$Â 
  - $1+0=1$Â 
  - $1+1=10$Â 
  - $1+1+1=11$Â 
- Use the following basic rules when subtracting binary numbers:
  - $0-0=0$Â 
  - $1-0=0$Â 
  - $1-1=0$Â 
  - $10-1=1$Â 
  - $11-1=10$Â 
- Multiplication of the digits 0 and 1 work the same in the base ten and base two number systems:
  - $0\times0=0$Â 
  - $1\times0=0$Â 
  - $0\times1=0$Â 
  - $1\times1=1$Â 
- The adding step in a multiplication works differently in the base two number system, because you need to use the base two addition rules.
