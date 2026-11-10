# `worksheet_html` — WeasyPrint rater-pack renderers

**WeasyPrint is the active PDF renderer for the expert rater packs.** This package
renders both packs from Jinja2 HTML templates + a shared print CSS
(`worksheet.css`) to PDF with **WeasyPrint**, replacing the reportlab path on the
download route:

| Pack | Entry point | Template | Replaces (kept as fallback) |
| ---- | ----------- | -------- | --------------------------- |
| H1 reading-note review worksheet | `render_h1_worksheet_html_pdf` | `worksheet.html.j2` | `../h1_worksheet_pdf.py` |
| Source-grounding audit pack | `render_source_audit_pack_html_pdf` | `audit_pack.html.j2` | `../audit_pack_pdf.py` |

```python
from app.domains.evaluation.application.worksheet_html import (
    render_h1_worksheet_html_pdf,
    render_source_audit_pack_html_pdf,
)

pdf_bytes: bytes = render_h1_worksheet_html_pdf(detail)        # same `detail` shape as the reportlab H1 renderer
audit_bytes: bytes = render_source_audit_pack_html_pdf(detail) # same `detail` shape as the reportlab audit pack
```

The H1 `detail` is the exact mapping produced by
`_PacketDetailProjection._build_h1_packet_detail` (see
`tests/test_h1_packet_worksheet_pdf._sample_detail`). The audit `detail` is the
`{textbook_name, items[]}` mapping built in
`AuditPresenter.export_source_audit_pack`.

## Why this exists

The reportlab path hand-rolls markdown with regex (`_apply_emphasis`) and maps
non-CP1252 glyphs to ASCII to dodge missing-glyph boxes. WeasyPrint renders real
HTML with the full Unicode-capable Computer Modern TTFs, so reading-note / excerpt
markdown (`**bold**`, `*italic*`, lists, headings, tables) renders natively via
python-markdown, and exotic glyphs (`10⁹`, `→`, `⟦REF-1⟧`) survive unchanged — no
`■` boxes. Selection markers are CSS shapes (circle = single-select score cells,
square = multi-select flags), not font glyphs.

The Computer Modern TTFs are vendored under `../fonts/` and referenced by absolute
`file://` URL, so no system-font installation is assumed (identical on CI/Docker).

### Math rendering (LaTeX → inline SVG)

WeasyPrint has **no MathML support and no JavaScript engine**, so a `<math>`
element renders as its bare text content — `\frac{3}{4}` collapsed to "34", `6/8`
to "68". The on-screen reader is fine (it runs KaTeX); the PDFs were the only
broken surface. `math_svg.py` fixes this: `pymdownx.arithmatex` marks `$…$` /
`$$…$$` math, and `renderer._convert_arithmatex_to_svg` turns each expression into
a self-contained inline `<svg>` of glyph outlines via **matplotlib's mathtext**
(`cm` font set = Computer Modern, matching the body font). The SVG is sized in
`em` and baseline-aligned via `vertical-align`, with `fill="currentColor"` so math
inherits the prose colour. A snippet matplotlib cannot parse falls back to the raw
LaTeX marker — a bad expression never crashes an export. matplotlib is pure-pip (no
system TeX), so this needs no extra native libs beyond WeasyPrint's.

## Native libraries (required by WeasyPrint)

WeasyPrint is not pure Python — it loads Pango, cairo, gdk-pixbuf, fontconfig and
HarfBuzz via `ctypes`. The Python wheel (`weasyprint`, already in `pyproject`) does
**not** bundle these; they must be present on the OS.

### macOS dev (Homebrew)

```bash
brew install pango cairo gdk-pixbuf fontconfig harfbuzz
# (pango pulls in glib/libgobject + harfbuzz transitively)
```

On macOS the Homebrew dylibs live under `$(brew --prefix)/lib`
(`/opt/homebrew/lib` on Apple Silicon, `/usr/local/lib` on Intel), which is **not**
on the default dyld search path. Without help, `import weasyprint` fails with
`cannot load library 'libgobject-2.0-0'`. `renderer._ensure_native_lib_path()`
handles this automatically: it prepends those dirs to `DYLD_FALLBACK_LIBRARY_PATH`
(only when the var is unset) before WeasyPrint is imported. To set it yourself:

```bash
export DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib
```

### Debian / Ubuntu (Linux / CI)

```bash
apt-get update && apt-get install -y \
    libpango-1.0-0 libpangoft2-1.0-0 libpangocairo-1.0-0 \
    libcairo2 libgdk-pixbuf-2.0-0 libffi-dev libharfbuzz0b fontconfig
```

On Linux these land on the standard loader path, so no `DYLD_*`/`LD_*` tweak is
needed (`_ensure_native_lib_path()` is a no-op off macOS).

### Docker (when the backend is containerized)

There is **no backend Dockerfile**. When you containerize the backend, add this to
the image before `uv sync` (Debian/Ubuntu `*-slim` base):

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpango-1.0-0 \
        libpangoft2-1.0-0 \
        libpangocairo-1.0-0 \
        libcairo2 \
        libgdk-pixbuf-2.0-0 \
        libffi-dev \
        libharfbuzz0b \
        fontconfig \
    && rm -rf /var/lib/apt/lists/*
```

Alpine note: prefer a `*-slim` Debian base; Alpine's musl + the above packages
(`pango`, `cairo`, `gdk-pixbuf`, `harfbuzz`, `fontconfig`, `ttf-*`) work but are
fiddlier.

## Where it's wired in

The active swap lives in `app/domains/evaluation/application/service.py`:

- `generate_h1_worksheet` → `render_h1_worksheet_html_pdf(detail)`
- `export_audit_pack` → `render_source_audit_pack_html_pdf(detail)`

The reportlab modules (`../h1_worksheet_pdf.py`, `../audit_pack_pdf.py`) are kept
in place as a fallback. `H1_MAJOR_ISSUE_FLAGS` remains defined in (and imported
from) `h1_worksheet_pdf.py` — its source of truth. The API routes
(`api/routes.py`) and the frontend need no changes — same bytes, same
`application/pdf` response.

## Tests

- `tests/test_h1_worksheet_html.py`
- `tests/test_audit_pack_html.py`

Each test renders a sample `detail` via the WeasyPrint renderer and asserts on the
extracted PDF text (title, sections, teacher-friendly labels, audit criteria,
markdown emphasis, no `■` boxes). They `pytest.skip(...)` cleanly when WeasyPrint
or its native libs are unavailable (caught `ImportError`/`OSError`). The reportlab
tests in `tests/test_h1_packet_worksheet_pdf.py` are left untouched as fallback
coverage.
