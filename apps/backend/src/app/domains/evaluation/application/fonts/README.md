# Bundled fonts — Computer Modern Unicode

The expert rater packs (H1/H2 worksheets + source-grounding audit packs) render
with **Computer Modern**, the typeface of the thesis itself, so the printed rater
materials match the report.

reportlab cannot rely on a system font being installed (CI, Docker, other
machines), so the four faces are vendored here and registered explicitly by
[`../pdf_fonts.py`](../pdf_fonts.py):

| File          | Face        |
| ------------- | ----------- |
| `cmunrm.ttf`  | Regular     |
| `cmunbx.ttf`  | Bold        |
| `cmunti.ttf`  | Italic      |
| `cmunbi.ttf`  | Bold Italic |

**Source / licence:** Computer Modern Unicode fonts (project `cm-unicode`,
TrueType build), released under the SIL Open Font License — free to use, embed,
and redistribute. They are Unicode-coverage builds of Donald Knuth's Computer
Modern, so glyph coverage is broad; the worksheet text sanitiser is kept as a
safety net regardless.
