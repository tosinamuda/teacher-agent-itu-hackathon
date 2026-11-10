"""Which calendar week of a term a scheme-of-work week falls on."""

from __future__ import annotations

from datetime import date, timedelta

DAYS_IN_A_WEEK = 7


def week_starts_on(term_starts_on: date, week_number: int) -> date:
    """Week 1 starts the day the term does."""
    return term_starts_on + timedelta(days=DAYS_IN_A_WEEK * (week_number - 1))


def current_week_number(term_starts_on: date, term_ends_on: date, today: date) -> int | None:
    """None before the term starts and after it ends."""
    if today < term_starts_on or today > term_ends_on:
        return None
    return (today - term_starts_on).days // DAYS_IN_A_WEEK + 1
