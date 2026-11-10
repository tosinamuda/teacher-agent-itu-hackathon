"""Make Homebrew's native libraries loadable on macOS.

WeasyPrint and cairosvg load pango, cairo and their kin through ``ctypes``. On macOS those
live in ``$(brew --prefix)/lib``, which is not on the default dyld search path, so the
import fails unless the caller exported ``DYLD_FALLBACK_LIBRARY_PATH``. On Linux the
libraries are on the standard loader path and this does nothing.
"""

from __future__ import annotations

import os
from pathlib import Path

_HOMEBREW_LIBS = ("/opt/homebrew/lib", "/usr/local/lib")


def ensure_native_lib_path() -> None:
    """Add the Homebrew lib dirs to ``DYLD_FALLBACK_LIBRARY_PATH`` when it is unset."""
    if os.name != "posix" or os.environ.get("DYLD_FALLBACK_LIBRARY_PATH"):
        return
    present = [path for path in _HOMEBREW_LIBS if Path(path).is_dir()]
    if present:
        os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = os.pathsep.join(present)
