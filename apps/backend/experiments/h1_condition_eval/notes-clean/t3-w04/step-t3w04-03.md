#### Pyramids

A pyramid is named based on its base shape.

**fig-03.** A triangular base pyramid. The base triangle is drawn in perspective, its third vertex raised
into the middle of the figure, and the apex above is joined to all three base vertices.

\begin{center}
\begin{tikzpicture}[scale=0.55]
  \draw (2.05,0)--(5.45,0.25)--(3.75,2.4)--cycle;
  \draw (3.8,4.1)--(2.05,0);
  \draw (3.8,4.1)--(5.45,0.25);
  \draw (3.8,4.1)--(3.75,2.4);
  \node[align=center] at (3.6,-1.1) {Triangular base Pyramid\\(Tetrahedron)};
\end{tikzpicture}
\end{center}

**fig-04.** A square base pyramid. The base is drawn as an upright rectangle and the apex above is joined
to all four of its corners, so two edges run outside the rectangle and two cross it.

\begin{center}
\begin{tikzpicture}[scale=0.55]
  \draw (0.7,1.9) rectangle (4,5);
  \draw (2.5,7.4)--(0.7,5);
  \draw (2.5,7.4)--(4,5);
  \draw (2.5,7.4)--(0.7,1.9);
  \draw (2.5,7.4)--(4,1.9);
  \node at (2.35,0.9) {Square base Pyramid};
\end{tikzpicture}
\end{center}

**fig-05.** A pentagonal based pyramid. The base is drawn as a pentagon standing on one side with its
fifth vertex uppermost, and the apex above is joined to that vertex, to the two vertices
either side of it, and to the lower-right vertex — four edges from the apex, the last of them
crossing the face of the solid.

\begin{center}
\begin{tikzpicture}[scale=0.55]
  \draw (3.1,6.75)--(5.3,4.5)--(4.15,1.2)--(1.65,1.25)--(1.2,4.4)--cycle;
  \draw (3.3,9.65)--(1.2,4.4);
  \draw (3.3,9.65)--(3.1,6.75);
  \draw (3.3,9.65)--(5.3,4.5);
  \draw (3.3,9.65)--(4.15,1.2);
  \node[align=center] at (3,0.1) {Pentagonal based\\Pyramid};
\end{tikzpicture}
\end{center}

**fig-06.** A rectangular based pyramid, drawn like the square one but on a base wider than it is tall.

\begin{center}
\begin{tikzpicture}[scale=0.55]
  \draw (1.15,2.3) rectangle (5,4.45);
  \draw (2.9,8)--(1.15,4.45);
  \draw (2.9,8)--(5,4.45);
  \draw (2.9,8)--(1.15,2.3);
  \draw (2.9,8)--(5,2.3);
  \node[align=center] at (3,1.2) {Rectangular based\\Pyramid};
\end{tikzpicture}
\end{center}

##### Properties

| Shape | Faces | edges | Vertices |
|---|---|---|---|
| Triangular based Pyramid | 4 | 6 | 4 |
| Square based Pyramid | 5 | 8 | 5 |
| Pentagonal base Pyramid | 6 | 10 | 6 |
| Rectangular based Pyramid | 5 | 8 | 5 |

#### Cone

**fig-07.** Two drawings side by side. On the left an upright cone: an elliptical base with the two slant
sides running up from the ends of the ellipse to the apex. On the right a cone lying on its
side, apex at the left, its two slant sides reaching a narrow upright ellipse whose top and
bottom then continue as two parallel lines to a second narrow ellipse further right.

\begin{center}
\begin{tikzpicture}[scale=0.5]
  \draw (0,0) ellipse (1.6 and 0.83);
  \draw (-1.6,0)--(-0.15,4.1)--(1.6,0);
  \begin{scope}[xshift=7cm]
    \draw (2.6,1)--(0,0)--(2.6,-1);
    \draw (2.6,0) ellipse (0.45 and 1);
    \draw (9.6,0) ellipse (0.5 and 1.05);
    \draw (2.6,1)--(9.6,1.05);
    \draw (2.6,-1)--(9.6,-1.05);
  \end{scope}
\end{tikzpicture}
\end{center}

1. It has two faces, i.e. one curved face and one flat face.
2. It has one edge.
3. It has one vertex