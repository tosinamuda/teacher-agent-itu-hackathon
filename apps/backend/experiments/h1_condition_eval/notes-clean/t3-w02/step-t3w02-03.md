#### Parts of a circle

**fig-04.** Two labelled circles. The first has the diameter drawn across it and a radius from its centre to
the circumference, with the arc and the circumference labelled. The second has a chord near the
top with the segment above it shaded, a shaded sector below with its right-hand bounding line
labelled Radius, and a tangent touching it on the right.

\begin{center}
\begin{tikzpicture}[scale=0.42]
  \draw (0,0) circle (3);
  \draw (-3,0)--(3,0);
  \node[above] at (0,0.1) {Diameter};
  \draw (0,0)--(0,-3);
  \node[right] at (0.45,-1.9) {Radius};
  \draw[->] (-5.9,-3.4)--(-2.3,-1.9);
  \node[left] at (-5.9,-3.4) {arc};
  \draw[->] (4.4,3.4)--(2.2,2.2);
  \node[right] at (4.4,3.4) {Circumference};
  \begin{scope}[xshift=17cm]
    \draw (0,0) circle (3);
    \draw (-2.29,1.94)--(2.29,1.94);
    \begin{scope}
      \clip (0,0) circle (3);
      \clip (-3,1.94) rectangle (3,3);
      \foreach \x in {-3,-2.7,...,3} { \draw (\x,1.8)--(\x+1.2,3.0); }
    \end{scope}
    \node[below] at (0,1.9) {Chord};
    \draw[->] (3.2,4.2)--(0.6,2.5);
    \node[right] at (3.2,4.2) {Segment};
    \begin{scope}
      \clip (0,0)--(-80:3) arc[start angle=-80, end angle=-25, radius=3]--cycle;
      \foreach \y in {-3.4,-3.1,...,0} { \draw (0,\y)--(3,\y+1.2); }
    \end{scope}
    \draw (0,0)--(-80:3);
    \draw (0,0)--(-25:3) node[midway, sloped, above] {Radius};
    \draw[->] (-3.6,-4.2)--(1.0,-2.0);
    \node[left] at (-3.6,-4.2) {Sector};
    \draw (3,-2.4)--(3,2.4);
    \node[right] at (3.2,0) {Tangent};
  \end{scope}
\end{tikzpicture}
\end{center}

- **Arc:** This is a curved part of the circumference.
- **Radius:** This is any straight line joining the centre of the circle to the circumference.
- **Chord:** This is any straight line joining two point on the circumference of a circle.
- **Diameter:** Any chord that passes through the centre of the circle.