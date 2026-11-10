# Independent geometry audit of t3-w06 (computed from the TikZ coordinates)

## Captions that assert what the drawing does not show

**fig-13 (90 degrees).** The caption says "An arc swung from C cuts the line at D and E".
The figure contains NO arc commands at all. The four strokes sit at x = 0.29, 0.84, 6.13,
6.60, i.e. 3.51, 2.96, 2.33 and 2.80 from C at x = 3.8. No pair is equidistant from C, so
no single arc centred at C could have produced them. The crossing drawn for F is two
straight segments meeting at (3.8, 2.8); it is not equidistant from any candidate D and E
(4.074 vs 3.960 for the taller pair), so it does not lie on the perpendicular bisector of
DE. The figure records an approximate freehand sketch, not a constructed diagram.

**fig-03 and fig-05 (parallel lines, leaning ruler).** The triangle drawn as the set square
has angles 62.22 / 94.22 / 23.56 (fig-03) and 62.91 / 93.01 / 24.09 (fig-05). Neither
contains a right angle, yet a right-angle mark is drawn on the ~62 degree corner. The
arrangement is impossible in principle: if the set square's AB-edge and ruler-edge meet at
90 degrees, the ruler cannot lean.

**fig-08 (perpendicular lines).** Step 2 says "Let the edge of the ruler meet the hypotenuse
of the set square as shown", but fig-08 draws only a line and a triangle -- no ruler. The
triangle is also not right-angled (angles 56.58 / 36.29 / 87.14) and carries no right-angle
mark, so the figure does not identify the hypotenuse or the "third edge".

> **Half resolved (2026-08-19).** The triangle is REDRAWN square on its base with the right
> angle marked, so the hypotenuse and the third edge are now tellable apart. The missing
> ruler is NOT drawn -- step 2 refers to it and the figure still omits it. Still open.

**fig-14 (60 degrees).** The arc is drawn `arc (5:74:5.17)`, so it starts 0.45 units above
the line and never reaches BC. The caption says it is "swung from B through X"; as drawn it
does not cut BC at X.

> **Resolved (2026-08-19).** `arc (0:74:5.17)`. The arc springs from X on BC, so the caption
> is now true of the drawing rather than of the intention.

## Procedure that stops short

**Bisection (objective 2).** The numbered steps end with "cut the first arc at P and Q" and
never instruct the student to join P to Q, nor name the midpoint. Executed literally the
steps leave the segment unbisected. The join exists only inside fig-12's drawing source.
The arc geometry itself is correct (radius 3/4 AB exceeds AB/2, so the arcs do meet).

## Confirmed correct -- do not change

The 90-degree procedure (steps 1-6) is complete and correct, including its step-3
justification that arcs of radius DC struck from D and E are externally tangent and meet
only at C. The 60-degree equilateral construction is correct. The parallel and perpendicular
slide methods are correct as prose.

## What the caption pass deliberately left

The 2026-08 pass on this lesson rewrote captions and redrew only fig-03 and fig-05, where
the arrangement was impossible in principle. fig-08 and fig-14 were left with captions that
name geometry the drawing does not have. Both are now redrawn, and both redraws are
declared in `note_editorial.DECLARED_ADDITIONS`. fig-13 is NOT redrawn: it contains no arc
commands at all, so making it show the construction is a new drawing rather than a
correction, and its caption is honest about what is there.
