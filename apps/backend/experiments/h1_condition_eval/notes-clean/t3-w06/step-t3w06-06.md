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
  \draw (0,0) ++(0:5.17) arc (0:74:5.17);
  \draw (5.17,0) ++(103:5.17) arc (103:140:5.17);
  \draw (0,0) -- (2.59,4.48);
\end{tikzpicture}
\end{center}