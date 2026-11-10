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
5. Join $P$ to $Q$ with a ruler.
6. $PQ$ crosses $AB$ at $M$. $M$ is the midpoint of $AB$, so $AM = MB$, and $PQ$ meets $AB$ at
   $90^\circ$.

**fig-12.** The same arcs with $P$ joined to $Q$, the joining line crossing $AB$ at its middle at
$M$ and carrying a right-angle mark in the upper right quadrant.

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
  \node[below right] at (3,-0.1) {$M$};
  \draw (3.32,0) -- (3.32,0.32) -- (3,0.32);
\end{tikzpicture}
\end{center}