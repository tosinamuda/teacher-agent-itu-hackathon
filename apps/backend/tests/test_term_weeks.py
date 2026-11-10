from datetime import date

from app.domains.teaching.domain.term_weeks import current_week_number, week_starts_on

TERM_START = date(2026, 9, 14)
TERM_END = date(2026, 12, 11)


def test_week_one_starts_with_the_term_and_each_week_a_week_later() -> None:
    assert week_starts_on(TERM_START, 1) == TERM_START
    assert week_starts_on(TERM_START, 4) == date(2026, 10, 5)


def test_the_current_week_counts_from_the_first_day_of_term() -> None:
    assert current_week_number(TERM_START, TERM_END, TERM_START) == 1
    assert current_week_number(TERM_START, TERM_END, date(2026, 9, 20)) == 1
    assert current_week_number(TERM_START, TERM_END, date(2026, 9, 21)) == 2
    assert current_week_number(TERM_START, TERM_END, TERM_END) == 13


def test_there_is_no_current_week_outside_the_term() -> None:
    assert current_week_number(TERM_START, TERM_END, date(2026, 9, 13)) is None
    assert current_week_number(TERM_START, TERM_END, date(2026, 12, 12)) is None
