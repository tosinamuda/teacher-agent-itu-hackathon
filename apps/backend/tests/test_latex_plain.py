"""Maths between $ signs becomes plain text a slide program can show and edit."""

from __future__ import annotations

import pytest

from app.shared.latex_plain import plain_maths


@pytest.mark.parametrize(
    ("written", "plain"),
    [
        (r"$60\text{ cm} \times 8,315\text{ steps}$", "60 cm × 8,315 steps"),
        (r"$\approx 60 \times 8,000 = 480,000\text{ cm}$", "≈ 60 × 8,000 = 480,000 cm"),
        (r"$480,000\text{ cm} ÷ 100 = 4,800\text{ m}$", "480,000 cm ÷ 100 = 4,800 m"),
        (r"$7{,}500\text{ steps}$", "7,500 steps"),
        (r"$\frac{3}{4}$ of a pizza", "3/4 of a pizza"),
        (r"$\frac{75\text{ cm}}{100}$", "(75 cm)/100"),
        (r"Area is $\pi r^2$", "Area is π r²"),
        (r"$x^{10}$ and $a_1$", "x¹⁰ and a₁"),
        (r"$\sqrt{49} = 7$", "√(49) = 7"),
        (r"$4{,}800\text{ m}=4.8\text{ km}$", "4,800 m = 4.8 km"),
        (r"$x<5$ and $y>2$", "x < 5 and y > 2"),
        ("football\u2011pitch and 60\u202fcm", "football-pitch and 60 cm"),
        (r"$180^\circ$", "180°"),
        (r"$\text{Chimaka}\ \rightarrow\ \text{proper}$", "Chimaka → proper"),
        (r"$\text{Convert cm to m (÷100)}$", "Convert cm to m (÷100)"),
        (r"$\unknown{3}$", "unknown3"),
        ("no maths here", "no maths here"),
        (r"Costs \$5 not $5\times 2$", "Costs $5 not 5 × 2"),
    ],
)
def test_maths_is_written_in_symbols_and_plain_letters(written: str, plain: str) -> None:
    assert plain_maths(written) == plain


def test_a_character_escaped_outside_maths_is_written_as_itself() -> None:
    assert plain_maths(r"about \_\_\_ m, 50\% and \$5") == "about ___ m, 50% and $5"


def test_a_blank_to_fill_in_is_written_as_underscores() -> None:
    assert plain_maths(r"about $\underline{\hspace{1cm}}$ m") == "about ____ m"
    assert plain_maths(r"$5\hspace{2mm}\text{ m}$") == "5 m"


def test_a_thin_space_command_reads_as_a_space_and_a_negative_one_as_nothing() -> None:
    assert plain_maths("$60$\\,cm and $8$\\;m and $5\\!0$") == "60 cm and 8 m and 50"
