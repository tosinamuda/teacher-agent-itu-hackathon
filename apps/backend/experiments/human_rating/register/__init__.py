"""The results register: every result the dissertation reports, recomputed from the study workbook.

The workbook ``Lesson_Plan_Study_Raw_to_Charts.xlsx`` is the single source of truth for the
evaluation's numbers. This package reads its raw and calculated sheets, recomputes each reported
result, checks it against the figure the dissertation prints, and writes the register into the
workbook as ``60_Results_Register``. Results the dissertation no longer reports stay in the same
register with their status, so there is one list, not an old one and a new one.
"""
