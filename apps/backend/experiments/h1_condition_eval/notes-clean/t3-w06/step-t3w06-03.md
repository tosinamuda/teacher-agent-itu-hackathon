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
short base along $AB$, the upright edge rising from the right end of that base with the right
angle marked there, and the hypotenuse closing back down to the left.

\begin{center}
\begin{tikzpicture}[scale=0.55,line width=0.5pt]
  \draw (0,0) -- (8,0);
  \node[below] at (0.41,-0.05) {$A$};
  \node[above] at (3.93,0.05) {$B$};
  % The upright edge stands square on the base: step 2 and 3 name a hypotenuse and a
  % "third edge", which only a marked right angle lets the reader tell apart.
  \draw (1.54,0) -- (2.25,1.0) -- (2.25,0) -- cycle;
  \draw (1.97,0) -- (1.97,0.28) -- (2.25,0.28);
\end{tikzpicture}
\end{center}

3. Pressing firmly on the ruler, slide the set square down along the hypotenuse side until the
   third edges touches point Q. Draw a line XY

**fig-09.** Line $AB$ with $XY$ now drawn across it, $X$ above and $Y$ below, and a right-angle
mark in the upper right quadrant.

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