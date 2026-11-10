"""Artefacts core HTTP transport — routes are imported directly from ``routes.py``.

Empty by intent: re-exporting ``router`` from this package init re-creates an
eager-load cycle with ``post_class_review_pack/api`` (the post-class route
imports schemas from this package; the package init would then load
``routes.py``, which imports the post-class route mid-init). Callers that want
the router use ``from app.domains.artefacts.core.api.routes import router``.
"""
