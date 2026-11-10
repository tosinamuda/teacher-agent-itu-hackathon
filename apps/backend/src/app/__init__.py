"""Backend API package."""

# dspy >= 3.3 makes numpy optional and plants a lazy proxy in sys.modules["numpy"]
# when it loads first; the numpy stack (scipy.stats, matplotlib mathtext) then
# materializes through that proxy and breaks — wilcoxon returned None, math-SVG
# rendering raised, one path hit RecursionError inside numpy.__getattr__.
# dspy's require() honours an ALREADY-imported numpy, so importing the real one
# here — every app module import passes through this package first — keeps the
# proxy from ever being installed.
import numpy as _numpy  # noqa: F401
