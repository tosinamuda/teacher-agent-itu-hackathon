## Step 2 — parallel and perpendicular lines

#### Parallel lines

**Examples:** construct a line through Point P so that it is parallel to AB.

(a) Place a set square so that one edge is accuratly along AB

**fig-01.** Line $AB$, with a point $P$ marked above it. A set square is drawn below $AB$ with
one edge along the line: the right angle is at the left end of that edge, one leg runs down from
it, and the hypotenuse closes back to a point on $AB$ to the right.

\begin{center}
\begin{tikzpicture}[scale=0.55,line width=0.5pt]
  \draw (0,0) -- (7,0);
  \node[left] at (0,0) {$A$};
  \node[above] at (7,0) {$B$};
  \fill (3.4,2.8) circle (1.6pt);
  \node[above] at (3.4,2.8) {$P$};
  \draw (2.7,0) -- (2.7,-1.1) -- (5.2,0);
  \draw (2.7,-0.26) -- (2.96,-0.26) -- (2.96,0);
\end{tikzpicture}
\end{center}

(b) Place a ruler along one of the other edge of the set square. Use the left hand edge if you
are right handed.

**fig-02.** The same set square on $AB$, with the ruler now drawn as a long strip lying along the
set square's downward edge. The ruler is vertical, so its edge meets $AB$ squarely and the right
angle is marked at that corner.

\begin{center}
\begin{tikzpicture}[scale=0.55,line width=0.5pt]
  \draw (0,0) -- (8,0);
  \node[below left] at (0,0) {$A$};
  \node[above] at (8,0) {$B$};
  \draw[rounded corners=3pt] (1.29,3.50) rectangle (1.72,-4.12);
  % The set square's vertical edge lies ALONG the ruler's right edge (x=1.72) — in the
  % source the two are layered, so only one line is visible. Drawn collinear, not offset.
  \draw (1.72,0) -- (1.72,-1.9) -- (5.4,0);
  \draw (1.72,-0.26) -- (1.98,-0.26) -- (1.98,0);
\end{tikzpicture}
\end{center}

**fig-03.** The same arrangement drawn a second time alongside the first, with the ruler leaning —
running from upper left to lower right across $AB$ instead of standing vertical. The ruler's
inclination does not affect the construction.

\begin{center}
\begin{tikzpicture}[scale=0.55,line width=0.5pt]
  \draw (0,0) -- (8,0);
  \node[below left] at (0,0) {$A$};
  \draw (-0.13,3.56) -- (3.426,-3.179) -- (3.046,-3.379) -- (-0.51,3.36) -- cycle;
  % The set square's edge is LAYERED on the ruler's right edge, as in fig-02 — collinear
  % with it and starting exactly at its crossing with AB (x=1.749), no gap.
  \draw (1.749,0) -- (2.377,-1.192) -- (5.11,0);
  % The mark she draws at this corner, rendered against the two edges it actually sits
  % between. The corner is acute — the mark is carried over from fig-02 (see _lesson-notes.md).
  \draw (2.049,0) -- (2.189,-0.265) -- (1.889,-0.265);
\end{tikzpicture}
\end{center}

(c) Hold the ruler firmly, slide the set square along the ruler towards P. Stop when the edge that
was on AB reaches P. Draw a line along this edge of the set square through P.

**fig-04.** The vertical ruler held fixed, with the set square drawn twice — once with its edge on
$AB$ and once higher up, its edge on a second line parallel to $AB$ — and an arrow between the two
positions pointing up along the ruler.

\begin{center}
\begin{tikzpicture}[scale=0.55,line width=0.5pt]
  \draw (0,0) -- (8,0);
  \node[below left] at (0,0) {$A$};
  \node[above] at (8,0) {$B$};
  \draw (0.71,2.40) -- (8,2.40);
  \draw[rounded corners=3pt] (0.28,3.65) rectangle (0.71,-3.97);
  % ONE set square drawn in two positions, translated straight up the ruler's right edge
  % (x=0.71). Both are congruent — leg 1.21, width 2.68 — so the two hypotenuses are
  % exactly parallel, which is the visible signature of a slide.
  \draw (0.71,0) -- (0.71,-1.21) -- (3.39,0);
  \draw (0.71,-0.26) -- (0.97,-0.26) -- (0.97,0);
  \draw (0.71,2.40) -- (0.71,1.19) -- (3.39,2.40);
  \draw (0.71,2.14) -- (0.97,2.14) -- (0.97,2.40);
  \draw[->] (2.44,0.1) -- (2.44,1.37);
\end{tikzpicture}
\end{center}

**fig-05.** The same slide drawn a second time alongside it, with the leaning ruler. Here the upper
line carries the point $P$, and the set square's upper position has its edge running through $P$.


\begin{center}
\begin{tikzpicture}[scale=0.55,line width=0.5pt]
  \draw (0,0) -- (8,0);
  \node[below left] at (0,0) {$A$};
  \draw (0.15,2.63) -- (8,2.63);
  \fill (3.24,2.63) circle (1.6pt);
  \node[above] at (3.24,2.63) {$P$};
  \draw (-0.33,3.58) -- (3.14,-3.20) -- (2.755,-3.392) -- (-0.715,3.388) -- cycle;
  % ONE set square in two positions, translated ALONG the ruler's right edge — layered on
  % it, each starting exactly at its crossing (y=2.63 at x=0.156; AB at x=1.502). Both are
  % congruent (leg 1.26, width 3.084), so the edge running from the ruler to AB and the one
  % running from the ruler to P are exactly parallel. The upper edge meets P by construction.
  \draw (0.156,2.63) -- (0.730,1.508) -- (3.240,2.63);
  \draw (0.456,2.63) -- (0.593,2.363) -- (0.293,2.363);
  \draw (1.502,0) -- (2.076,-1.122) -- (4.586,0);
  \draw[->] (3.21,0.1) -- (2.467,1.551);
\end{tikzpicture}
\end{center}

#### Perpendicular lines

Two lines are said to be perpendicular to each other when they meet at a right angle i.e
$90^\circ$

**fig-06.** Line $AB$ with a second line $XY$ crossing it, $X$ above and $Y$ below, and a
right-angle mark in the upper right quadrant at the crossing.

\begin{center}
\begin{tikzpicture}[scale=0.55,line width=0.5pt]
  \draw (-0.5,0) -- (7.5,0);
  \draw (0,0.25) -- (0,-0.25);
  \draw (5,0.25) -- (5,-0.25);
  \node[below] at (0,-0.3) {$A$};
  \node[below] at (5,-0.3) {$B$};
  \draw (2.5,2.6) -- (2.5,-2.6);
  \node[above] at (2.5,2.6) {$X$};
  \node[below] at (2.5,-2.6) {$Y$};
  \draw (2.82,0) -- (2.82,0.32) -- (2.5,0.32);
\end{tikzpicture}
\end{center}

1. Draw a line AB mark a point Q on the line.

**fig-07.** A plain line with a stroke at each end, labelled $A$ on the left and $B$ on the right.

\begin{center}
\begin{tikzpicture}[scale=0.55,line width=0.5pt]
  \draw (0,0) -- (7,0);
  \draw (0,0.22) -- (0,-0.22);
  \draw (7,0.22) -- (7,-0.22);
  \node[below] at (0,-0.28) {$A$};
  \node[below] at (7,-0.28) {$B$};
\end{tikzpicture}
\end{center}

2. Place the edge of the set square on line AB. Let the edge of the ruler meet the hypotenuse of
   the set square as shown.

**fig-08.** Line $AB$ with the set square standing on it as a narrow right-angled triangle: a
short base along $AB$, a near-vertical edge rising from the right end of that base, and the
hypotenuse running up from the left.


\begin{center}
\begin{tikzpicture}[scale=0.55,line width=0.5pt]
  \draw (0,0) -- (8,0);
  \node[below] at (0.41,-0.05) {$A$};
  \node[above] at (3.93,0.05) {$B$};
  \draw (1.54,0) -- (2.20,1.0) -- (2.25,0);
\end{tikzpicture}
\end{center}

3. Pressing firmly on the ruler, slide the set square down along the hypotenuse side until the
   third edges touches point Q. Draw a line XY

**fig-09.** Line $AB$ with $XY$ now drawn across it, $X$ above and $Y$ below, and a right-angle
mark in the upper right quadrant at the foot of $XY$.

\begin{center}
\begin{tikzpicture}[scale=0.55,line width=0.5pt]
  \draw (0,0) -- (8,0);
  \node[below] at (0.15,-0.1) {$A$};
  \node[above] at (4.52,0.1) {$B$};
  \draw (2.1,1.85) -- (2.15,-0.8);
  \node[above] at (2.1,1.85) {$X$};
  \node[below] at (2.15,-0.8) {$Y$};
  \draw (2.44,0) -- (2.44,0.32) -- (2.12,0.32);
\end{tikzpicture}
\end{center}

---

## Step 3 — construction of line segments

**Procedures:**

1. Open a pair of compasses so that the radius is about $\frac{3}{4}$ of the length of AB.
2. To bisect the line segment AB means to divide it into two equal halves

**fig-10.** The line segment $AB$, a stroke at each end, $A$ on the left and $B$ on the right.

\begin{center}
\begin{tikzpicture}[scale=0.55,line width=0.5pt]
  \draw (0,0) -- (7,0);
  \draw (0,0.22) -- (0,-0.22);
  \draw (7,0.22) -- (7,-0.22);
  \node[below left] at (0,-0.1) {$A$};
  \node[below right] at (7,-0.1) {$B$};
\end{tikzpicture}
\end{center}

3. Place the sharp point of the compass on A, Draw two arcs, one above and the other below the
   midle of AB.

**fig-11.** The segment $AB$ with arc pairs crossing above and below it, the upper crossing
labelled $P$ and the lower one $Q$. Each crossing is drawn as a small X where an arc from $A$ meets
an arc from $B$.

\begin{center}
\begin{tikzpicture}[scale=0.55,line width=0.5pt]
  \draw (0,0) -- (6,0);
  \draw (0,0.22) -- (0,-0.22);
  \draw (6,0.22) -- (6,-0.22);
  \node[below left] at (0,-0.1) {$A$};
  \node[below right] at (6,-0.1) {$B$};
  \draw (0,0) ++(37:4.5) arc (37:59:4.5);
  \draw (6,0) ++(121:4.5) arc (121:143:4.5);
  \draw (0,0) ++(-59:4.5) arc (-59:-37:4.5);
  \draw (6,0) ++(-143:4.5) arc (-143:-121:4.5);
  \node[above] at (3,3.5) {$P$};
  \node[below] at (3,-3.5) {$Q$};
\end{tikzpicture}
\end{center}

4. With the same radius, and place the sharp point of the compasses on B Draw two arc so that they
   cut the first arc at P and Q

**fig-12.** The same arcs with $P$ joined to $Q$, the joining line crossing $AB$ at its middle and
carrying a right-angle mark in the upper right quadrant.

\begin{center}
\begin{tikzpicture}[scale=0.55,line width=0.5pt]
  \draw (0,0) -- (6,0);
  \draw (0,0.22) -- (0,-0.22);
  \draw (6,0.22) -- (6,-0.22);
  \node[below left] at (0,-0.1) {$A$};
  \node[below right] at (6,-0.1) {$B$};
  \draw (0,0) ++(37:4.5) arc (37:59:4.5);
  \draw (6,0) ++(121:4.5) arc (121:143:4.5);
  \draw (0,0) ++(-59:4.5) arc (-59:-37:4.5);
  \draw (6,0) ++(-143:4.5) arc (-143:-121:4.5);
  \draw (3,3.35) -- (3,-3.35);
  \node[above] at (3,3.35) {$P$};
  \node[below] at (3,-3.35) {$Q$};
  \draw (3.32,0) -- (3.32,0.32) -- (3,0.32);
\end{tikzpicture}
\end{center}

---

## Step 4 — angle $90^\circ$

**Procedure:**

1. Draw a straight line $AB$ and mark a point $C$ on it, where the $90^\circ$ angle is to be
   constructed.
2. With the compasses at $C$, draw an arc that cuts the line at two points, $D$ and $E$.
3. Open the compasses WIDER than $DC$ — the width used in step 2 will not work, because arcs of
   that width meet only at $C$ itself. With the compasses at $D$ at this new wider setting, draw an
   arc above the line.
4. With the compasses still at the wider setting of step 3, place them at $E$ and draw another arc,
   cutting the first at $F$.
5. Join $C$ to $F$ with a ruler.
6. $CF$ is perpendicular to $AB$, so $\angle FCB = 90^\circ$.

**fig-13.** The segment $AB$, $A$ at the left end and $B$ at the right, with $C$ marked on the line
between them. An arc swung from $C$ cuts the line at $D$ and $E$, one near each end, and short
strokes stand on the line at those cuts. Two further arcs, struck from $D$ and from $E$ and opened
wider than $DC$, cross each other at $F$ above the line. A straight line runs from $F$ down to $C$,
where a right angle is marked.

\begin{center}
\begin{tikzpicture}[scale=0.55,line width=0.5pt]
  \draw (0,0) -- (7,0);
  \draw (0,0.22) -- (0,-0.22);
  \draw (7,0.22) -- (7,-0.22);
  \node[below left] at (0,-0.1) {$A$};
  \node[below right] at (7,-0.1) {$B$};
  \draw (0.29,0.22) -- (0.29,-0.22);
  \draw (0.84,0.34) -- (0.84,-0.34);
  \draw (6.13,0.22) -- (6.13,-0.22);
  \draw (6.60,0.34) -- (6.60,-0.34);
  \draw (3.8,0) -- (3.8,3.2);
  \draw (4.12,0) -- (4.12,0.32) -- (3.8,0.32);
  \draw (2.9,2.55) -- (4.7,3.05);
  \draw (2.9,3.05) -- (4.7,2.55);
\end{tikzpicture}
\end{center}

---

## Step 5 — angle $60^\circ$

**Procedure:**

1. Draw a line segment BC with centre B at any convinent radius. Draw an arc to cut BC at X
2. with centre X and the same radius as in (i) draw an arc to cut the first arc at A
3. Join AB.

**fig-14.** The line $BC$ with $B$ at the left, a stroke marking $X$ part way along, a long arc
swung from $B$ through $X$ and up to the left, a shorter arc swung from $X$ cutting it, and a
straight line from $B$ to that crossing.

\begin{center}
\begin{tikzpicture}[scale=0.55,line width=0.5pt]
  \draw (0,0) -- (7,0);
  \draw (0,0.22) -- (0,-0.22);
  \node[below left] at (0,-0.05) {$B$};
  \node[above right] at (7,0) {$C$};
  \draw (5.17,0.22) -- (5.17,-0.22);
  \node[below] at (5.17,-0.25) {$X$};
  \draw (0,0) ++(5:5.17) arc (5:74:5.17);
  \draw (5.17,0) ++(103:5.17) arc (103:140:5.17);
  \draw (0,0) -- (2.59,4.48);
\end{tikzpicture}
\end{center}