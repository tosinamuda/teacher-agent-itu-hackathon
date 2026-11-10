"""School pure-domain layer — no cross-domain imports.

The subject-offering catalog used to be re-exported from here via a shim
(``school.domain.subject_offerings``) that delegated to ``curriculum``. That
created a runtime ``school.domain → curriculum.domain`` edge in the
innermost layer (P4.4). Removed — consumers import the catalog directly
from ``curriculum.domain.subject_offerings`` (its single source of truth).
"""
