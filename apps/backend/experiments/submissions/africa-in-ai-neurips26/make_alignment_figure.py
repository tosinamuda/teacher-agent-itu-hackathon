"""Redraw the teacher-alignment figure at this paper's column width.

Same content and constraints as the supplied figure: the full 0-100 scale, both
marker types, and every percentage carrying its counts. Only the geometry and type
sizes change, so the plot stays legible at 0.75 of a NeurIPS text column.

    uv run --with matplotlib python make_alignment_figure.py <data-dir>
"""

import csv
import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

CRITERION = "lesson_context_alignment"
CONDITIONS = ("C0", "C1", "C2", "C3")


def read(path: pathlib.Path, value: str, total: str) -> dict[str, tuple[int, int]]:
    rows = [r for r in csv.DictReader(path.open()) if r["criterion"] == CRITERION]
    return {r["condition"]: (int(r[value]), int(r[total])) for r in rows}


def main() -> None:
    data = pathlib.Path(sys.argv[1])
    individual = read(data / "part1_counts.csv", "favourable_n", "n_ratings")
    paired = read(data / "part1_paired.csv", "both_favourable_n", "n_paired_sections")

    plt.rcParams.update(
        {"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 9}
    )
    fig, ax = plt.subplots(figsize=(6.6, 1.85))
    for row, condition in enumerate(reversed(CONDITIONS)):
        for series, marker, colour, offset in (
            (individual, "o", "#1a1a1a", 0.16),
            (paired, "s", "#b03a2e", -0.16),
        ):
            hit, total = series[condition]
            share = 100 * hit / total
            ax.plot(share, row + offset, marker, ms=5, color=colour)
            ax.annotate(
                f"{share:.1f}% ({hit}/{total})",
                (share, row + offset),
                textcoords="offset points",
                xytext=(7, -3),
                fontsize=8,
            )

    ax.set_yticks(range(len(CONDITIONS)))
    ax.set_yticklabels(list(reversed(CONDITIONS)))
    ax.set_xlim(0, 118)
    ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.set_xlabel("Percentage meeting the rubric's 4-5 categories", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.plot([], [], "o", ms=5, color="#1a1a1a", label="Individual ratings at 4-5")
    ax.plot([], [], "s", ms=5, color="#b03a2e", label="Both raters at 4-5")
    ax.legend(frameon=False, fontsize=8, loc="lower left", handletextpad=0.4)
    fig.tight_layout(pad=0.4)
    fig.savefig(pathlib.Path(__file__).with_name("alignment.pdf"), bbox_inches="tight")
    print("written")


if __name__ == "__main__":
    main()
