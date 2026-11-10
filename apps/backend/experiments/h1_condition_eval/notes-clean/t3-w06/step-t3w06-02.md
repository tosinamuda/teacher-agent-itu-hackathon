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
set square's downward edge. The right angle marked at the corner is the set square's own,
between the edge lying along $AB$ and the edge running down from it.

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

**fig-03.** The same set square on $AB$ as in fig-02, with the ruler moved to rest against its
sloping edge instead of its upright one. The set square has not moved; only the ruler has, so it
now leans across $AB$, running from lower left to upper right. The right angle is still where the
edge on $AB$ meets the short upright edge, and it is marked there. The ruler's inclination does
not affect the construction. The set square is drawn at one particular size, and with its right
angle at one particular end; neither is part of the method. Any set square works, either way
round, so long as one edge lies along $AB$ and the ruler rests against another.

\begin{center}
\begin{tikzpicture}[scale=0.55,line width=0.5pt]
  \draw (0,0) -- (8,0);
  \node[below left] at (0,0) {$A$};
  \node[above right] at (8,0) {$B$};
  % The ruler now lies along the sloping edge, extending past it at both ends. Drawn a
  % hairline clear of that edge so the set square stays visible as a triangle.
  \draw[rounded corners=2pt] (-0.171,-3.033) -- (6.760,0.545) -- (6.967,0.145) -- (0.036,-3.433) -- cycle;
  \draw (1.72,0) -- (1.72,-1.9) -- (5.4,0);
  \draw (1.72,-0.26) -- (1.98,-0.26) -- (1.98,0);
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

**fig-05.** The same slide as fig-04, made against the leaning ruler of fig-03. The set square is
drawn twice: once with its edge on $AB$, and once slid along the ruler until that edge passes
through $P$. The two positions are congruent and point the same way — sliding along a held ruler
moves the set square without turning it — so the edge through $P$ stays parallel to $AB$. The
arrow gives the direction of the slide, along the ruler's edge, and the right angle is marked in
both positions.

\begin{center}
\begin{tikzpicture}[scale=0.55,line width=0.5pt]
  \draw (0,0) -- (8,0);
  \node[below left] at (0,0) {$A$};
  \node[above right] at (8,0) {$B$};
  \draw (0.35,2.2) -- (8,2.2);
  \fill (6.0,2.2) circle (1.6pt);
  \node[above] at (6.0,2.2) {$P$};
  % The ruler is held still; it spans both positions of the set square, drawn a hairline
  % clear of their sloping edges.
  \draw[rounded corners=2pt] (-0.026,-2.119) -- (7.616,2.247) -- (7.824,1.882) -- (0.182,-2.484) -- cycle;
  \draw (0.6,0) -- (0.6,-1.6) -- (3.4,0);
  \draw (0.6,-0.26) -- (0.86,-0.26) -- (0.86,0);
  % The same set square, translated along the ruler until its edge reaches P.
  \draw (4.45,2.2) -- (4.45,0.6) -- (7.25,2.2);
  \draw (4.45,1.94) -- (4.71,1.94) -- (4.71,2.2);
  \draw[->] (2.6,0.55) -- (4.0,1.35);
\end{tikzpicture}
\end{center}