"""Where a multiple-choice item's correct answer sits.

A model writing items tends to put the answer first. Left there, a learner who always picks A
scores full marks, and the learner state built from the answers says nothing. So each item's
options are re-lettered to put the answer at a position drawn from the item's own stem: fixed
for an item, spread across a test.
"""

from __future__ import annotations

import hashlib
from typing import NamedTuple


class PlacedOptions(NamedTuple):
    options: dict[str, str]
    correct_option: str
    #: Wrong option letter -> misconception code, following each option to its new letter.
    misconceptions: dict[str, str]


def placed(
    options: dict[str, str], correct_option: str, misconceptions: dict[str, str], *, stem: str
) -> PlacedOptions:
    """The item's options re-lettered with the answer at the slot its stem hashes to."""
    letters = sorted(options)
    slot = int(hashlib.sha256(stem.encode()).hexdigest(), 16) % len(letters)
    others = [letter for letter in letters if letter != correct_option]
    order = [*others[:slot], correct_option, *others[slot:]]
    was = dict(zip(letters, order, strict=True))
    return PlacedOptions(
        options={letter: options[old] for letter, old in was.items()},
        correct_option=letters[slot],
        misconceptions={
            letter: misconceptions[old] for letter, old in was.items() if old in misconceptions
        },
    )
