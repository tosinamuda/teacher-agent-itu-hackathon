# Draw the picture on a slide

The three drawings below are shapes to build from. Replace every number and label with the lesson's
own; none of the numbers in them belongs on your slide.

A picture is shown to a whole class from the back of a room. Draw one idea, large and plain.

- One `tikzpicture` environment, and nothing outside it.
- Lines at least `thick`. Labels `\large` or bigger, at most seven on a slide.
- Every label and number in the drawing is a number of the example on the slide. A drawing that
  disagrees with its points teaches the class the wrong thing.
- Place things by calculation, not by eye: on a number line that runs from 0 to 10,000 over 5 cm,
  a mark at 7,500 sits at `x = 3.75`, because 7,500 × 0.0005 = 3.75.
- Load no library: a drawing is one `tikzpicture` and only the core of TikZ is there.
- Colour is for emphasis only, one colour besides black, and the slide still reads in black and
  white.
- Draw a plain shape, angle, number line, bar or array. Never draw a construction that a ruler and
  compasses make: a construction drawn by guesswork is wrong more often than right. Copy the
  note's own drawing of it, exactly as it is.
- Put what the drawing shows in a title or one point, and what to point at in the speaker notes.

## A number line, with a number marked and rounded

Mark the whole number below the number and the whole number above it, and the number itself.
The line is 10 long. Put the lower whole number at 0 and the higher at 10, and the number
between them at 10 × (its value − the lower whole number) ÷ (the higher − the lower). A number
a tenth of the way along is a tenth of the line from its whole number; never put it halfway.

Write the whole numbers below the line and the number you mark above it, so their labels never
meet. Start every label with `\Huge`: the picture is shown across the whole slide, and a smaller
label cannot be read from the back of the room. A longer line makes the labels smaller, so keep
it at 10: the deck is sent back for a line longer than 12.

```latex
\begin{tikzpicture}
  \draw[thick] (0,0) -- (10,0);
  \foreach \x/\label in {0/LOWER, 10/HIGHER} {
    \draw[thick] (\x,0.2) -- (\x,-0.2);
    \node[below=4pt] at (\x,0) {\Huge \label};
  }
  \draw[thick] (MARKAT,0.4) -- (MARKAT,-0.4);
  \node[above=4pt] at (MARKAT,0.4) {\Huge NUMBER};
\end{tikzpicture}
```

Put the lesson's own values in place of LOWER, HIGHER and NUMBER, and the position worked out as
above in place of MARKAT. The label stands at the top end of the mark's tick, so the tick never
crosses it.

## A bar model: a whole split into parts

```latex
\begin{tikzpicture}
  \draw[thick] (0,0) rectangle (8,1);
  \draw[thick] (3,0) -- (3,1);
  \node at (1.5,0.5) {\Large 3 parts};
  \node at (5.5,0.5) {\Large 5 parts};
  \draw[thick] (0,1.3) -- (8,1.3);
  \node[above] at (4,1.3) {\Large 8 parts in all};
\end{tikzpicture}
```

## An array of equal groups

```latex
\begin{tikzpicture}
  \foreach \row in {0,1,2} {
    \foreach \col in {0,1,2,3} {
      \fill (\col*0.8, -\row*0.8) circle (0.25);
    }
  }
  \node[right] at (3.6,-0.8) {\Large 3 rows of 4};
\end{tikzpicture}
```
