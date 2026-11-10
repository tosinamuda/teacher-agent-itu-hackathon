#### Hints

Plane shapes are also known as two dimensional shapes (2-D shapes). They include: triangle,
rectangle, squares, parallelogram, trapezium, circle and other polygons.

#### Triangles

**fig-01.** Isosceles: a single tick on each of the two slanted sides, an arc at each base angle. Scalene:
one, two and three ticks on the three sides, an arc at each vertex. Equilateral: a single tick
on each of the three sides, an arc at each vertex.

\begin{center}
\begin{tikzpicture}[scale=0.42]
  \draw (0,0)--(4,0)--(2,4)--cycle;
  \draw (0.8,1.6)--(1.2,1.4);
  \draw (3.2,1.6)--(2.8,1.4);
  \draw (0,0)++(0:0.7) arc[start angle=0, end angle=63, radius=0.7];
  \draw (4,0)++(180:0.7) arc[start angle=180, end angle=117, radius=0.7];
  \node[below] at (2,-0.6) {Isosceles};
  \begin{scope}[xshift=7cm]
    \draw (0,0)--(5,0)--(1.4,3.4)--cycle;
    \draw (0.38,1.83)--(1.02,1.57);
    \draw (3.02,1.87)--(3.50,2.38);
    \draw (3.38,1.53)--(3.86,2.04);
    \foreach \d in {-0.25,0,0.25} { \draw (2.5+\d,-0.25)--(2.5+\d,0.25); }
    \draw (0,0)++(0:0.7) arc[start angle=0, end angle=68, radius=0.7];
    \draw (5,0)++(180:0.8) arc[start angle=180, end angle=137, radius=0.8];
    \draw (1.4,3.4)++(-113:0.7) arc[start angle=-113, end angle=-25, radius=0.7];
    \node[below] at (2.5,-0.6) {Scalene};
  \end{scope}
  \begin{scope}[xshift=14cm]
    \draw (0,0)--(4,0)--(2,3.46)--cycle;
    \draw (0.8,1.55)--(1.2,1.32);
    \draw (3.2,1.55)--(2.8,1.32);
    \draw (1.8,-0.25)--(2.2,0.25);
    \draw (0,0)++(0:0.7) arc[start angle=0, end angle=60, radius=0.7];
    \draw (4,0)++(180:0.7) arc[start angle=180, end angle=120, radius=0.7];
    \draw (2,3.46)++(-120:0.7) arc[start angle=-120, end angle=-60, radius=0.7];
    \node[below] at (2,-0.6) {Equilateral};
  \end{scope}
\end{tikzpicture}
\end{center}

| Isosceles | Scalene | Equilateral |
|---|---|---|
| (i) 2 adjacent side are equal | No side equal | 3 sides are equal |
| (ii) base angles are equal | No angle is equal to the other | All angles are equal ($60^\circ$ each) |
| (iii) one line of symmetry | No line of symmetry. | 3 lines of symmetry. |

#### Squares and Rectangles

**fig-02.** Square: a right-angle mark at each corner, a single tick on each of the four sides. Rectangle: a
right-angle mark at each corner, a single tick on each of the two longer sides and a double tick
on each of the two shorter sides.

\begin{center}
\begin{tikzpicture}[scale=0.42]
  \draw (0,0) rectangle (3.4,3.4);
  \draw (0,0.5)--(0.5,0.5)--(0.5,0);
  \draw (3.4,0.5)--(2.9,0.5)--(2.9,0);
  \draw (0,2.9)--(0.5,2.9)--(0.5,3.4);
  \draw (3.4,2.9)--(2.9,2.9)--(2.9,3.4);
  \draw (1.7,-0.25)--(1.7,0.25);
  \draw (1.7,3.15)--(1.7,3.65);
  \draw (-0.25,1.7)--(0.25,1.7);
  \draw (3.15,1.7)--(3.65,1.7);
  \node[below] at (1.7,-0.9) {Squares};
  \begin{scope}[xshift=8cm]
    \draw (0,0) rectangle (5,3);
    \draw (0,0.5)--(0.5,0.5)--(0.5,0);
    \draw (5,0.5)--(4.5,0.5)--(4.5,0);
    \draw (0,2.5)--(0.5,2.5)--(0.5,3);
    \draw (5,2.5)--(4.5,2.5)--(4.5,3);
    \draw (2.5,-0.25)--(2.5,0.25);
    \draw (2.5,2.75)--(2.5,3.25);
    \draw (-0.25,1.35)--(0.25,1.35); \draw (-0.25,1.65)--(0.25,1.65);
    \draw (4.75,1.35)--(5.25,1.35); \draw (4.75,1.65)--(5.25,1.65);
    \node[below] at (2.5,-0.9) {Rectangles};
  \end{scope}
\end{tikzpicture}
\end{center}

| Squares | Rectangles |
|---|---|
| i) All sides are equal | 2 opposite sides are equal |
| (ii) 2 pairs of parallel sides | 2 pair of parallel sides. |
| (iii) All angles are equal ($90^\circ$) each. | All angles are equal ($90^\circ$) each. |
| (iv) Four lines of symmetry | Two lines of symmetry |
| (v) Diagonals bisect it at right angle. | Diagonals bisect it but not at right angle. |

#### Parallelograms and Trapezium

**fig-03.** Parallelogram: a single arrow on each of the two horizontal sides, a double arrow on
each of the two slanted sides. Trapezium: a single arrow on each of the two parallel sides, and
one diagonal drawn in.

\begin{center}
\begin{tikzpicture}[scale=0.42]
  \draw (0,0)--(5,0)--(6.6,3)--(1.6,3)--cycle;
  \draw[->] (2.4,0)--(2.6,0);
  \draw[->] (3.9,3)--(4.1,3);
  \draw[->] (5.7,1.4)--(5.85,1.65);
  \draw[->] (5.85,1.4)--(6.0,1.65);
  \draw[->] (0.7,1.4)--(0.85,1.65);
  \draw[->] (0.85,1.4)--(1.0,1.65);
  \node[below] at (3,-0.6) {Parallelogram};
  \begin{scope}[xshift=10cm]
    \draw (0,0)--(6,0)--(4.6,3)--(1.6,3)--cycle;
    \draw (0,0)--(4.6,3);
    \draw[->] (2.9,0)--(3.1,0);
    \draw[->] (3.0,3)--(3.2,3);
    \node[below] at (3,-0.6) {Trapezium};
  \end{scope}
\end{tikzpicture}
\end{center}

| Parallelogram | Trapezium |
|---|---|
| i) 2 pairs of opposite side are equal and parallel | Only a pair of sides are parallel |
| (ii) opposite angles are equal | opposite angles are not equal |
| (iii) No line of symmetry | No line of symmetry |
| (iv) Diagonals divide it into equal triangles | Diagonal divide it into two unequal triangles. |

#### Polygons

A polygon is a closed shape that has three or more straight sides.

| Name of Polygon | No of sides | No of triangle ($n-2$) |
|---|---|---|
| Triangle | 3 | 1 |
| Quadrilateral | 4 | 2 |
| Pentagon | 5 | 3 |
| Hexagon | 6 | 4 |
| Heptagon | 7 | 5 |
| Octagon | 8 | 6 |
| Nonagon | 9 | 7 |
| Decagon | 10 | 8 |
| Hendecagon or undecagon | 11 | 9 |
| Dodecagon | 12 | 10 |