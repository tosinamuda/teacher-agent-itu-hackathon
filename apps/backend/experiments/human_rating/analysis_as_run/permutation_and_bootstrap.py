"""The four analysis targets, kept separate, with learner-cluster inference.

Nine learners were drawn three per attainment stratum, so the bootstrap resamples
learners WITHIN stratum: that is the sampling design, and an unstratified resample can
return a replicate with no top-stratum learner at all.
"""
import random, re, statistics as st, warnings
from collections import defaultdict
from pathlib import Path
warnings.filterwarnings("ignore")
from scipy import stats
from experiments.human_rating.results import h2_rows, students

LIVE = Path.home() / "Library/CloudStorage/GoogleDrive-<account>/My Drive/Revision Material Evaluation"
CASE = re.compile(r"-c\d+$"); S = {"clearly better": 2, "slightly better": 1}
stu = {s["student"]: s for s in students()}
rows = h2_rows(LIVE)
for r in rows:
    r["case"] = CASE.sub("", r["internal_packet_id"])
    t = r["chose"].lower()
    f = 0 if "same" in t else next(v for k, v in S.items() if k in t)*(1 if r["favoured_arm"]=="P1" else -1)
    r["y"] = (f > 0) - (f < 0)

by_learner = defaultdict(list)
for r in rows: by_learner[r["student"]].append(r["y"])
strat = {s: stu[s]["ability_stratum"] for s in by_learner}
groups = defaultdict(list)
for s in by_learner: groups[strat[s]].append(s)

def summarise(pick):
    """pick: list of learner ids (may repeat). Equal weight per learner."""
    lm = {i: st.mean(by_learner[s]) for i, s in enumerate(pick)}
    top = [lm[i] for i, s in enumerate(pick) if strat[s] == "top"]
    rest = [lm[i] for i, s in enumerate(pick) if strat[s] != "top"]
    per_str = {g: [lm[i] for i, s in enumerate(pick) if strat[s] == g] for g in ("lower","middle","top")}
    return dict(
        overall=st.mean(lm.values()),
        top=st.mean(top) if top else float("nan"),
        rest=st.mean(rest) if rest else float("nan"),
        diff=(st.mean(top) - st.mean(rest)) if top and rest else float("nan"),
        trend=st.mean(per_str["top"]) - st.mean(per_str["lower"]) if per_str["top"] and per_str["lower"] else float("nan"),
        lower=st.mean(per_str["lower"]), middle=st.mean(per_str["middle"]),
    )

obs = summarise(sorted(by_learner))
random.seed(20260908)
reps = []
for _ in range(20000):
    pick = [random.choice(groups[g]) for g in ("lower","middle","top") for _ in range(3)]
    reps.append(summarise(pick))

print("═══ FOUR SEPARATE TARGETS — equal weight per learner, n=9 ═══")
print("    stratified cluster bootstrap over learners, 20,000 replicates\n")
print(f"  {'target':38s} {'estimate':>9s}  {'95% CI':>20s}  {'excludes 0?':>12s}")
print("  " + "─"*84)
LABEL = [
    ("overall",  "Q1  overall P1 - P0"),
    ("top",      "Q4  P1 - P0 among TOP attainers"),
    ("rest",     "     P1 - P0 among the rest"),
    ("lower",    "     P1 - P0 among LOWER attainers"),
    ("middle",   "     P1 - P0 among MIDDLE attainers"),
    ("diff",     "Q2  top MINUS rest (the -0.675)"),
    ("trend",    "Q3  top MINUS lower (ordered ends)"),
]
for key, label in LABEL:
    vals = sorted(r[key] for r in reps if r[key] == r[key])
    lo, hi = vals[int(.025*len(vals))], vals[int(.975*len(vals))]
    mark = "YES" if (lo > 0 or hi < 0) else "no"
    print(f"  {label:38s} {obs[key]:>+9.3f}  [{lo:>+7.3f}, {hi:>+7.3f}]  {mark:>12s}")

print("\n═══ the reviewer's counter-example, checked against the real numbers ═══")
print(f"  Is 'top minus rest is negative' the same as 'top is negative'?")
print(f"    rest = {obs['rest']:+.3f}   top = {obs['top']:+.3f}   difference = {obs['diff']:+.3f}")
print(f"    -> top is {'BELOW' if obs['top'] < 0 else 'ABOVE'} zero, so the two are"
      f" {'aligned here' if obs['top'] < 0 else 'NOT aligned'} — but that had to be checked, not assumed.")

print("\n═══ hard limit: signed-rank on 3 top-stratum learners ═══")
topv = [st.mean(by_learner[s]) for s in groups["top"]]
print(f"  the three top learners: {[round(v,3) for v in topv]}")
print(f"  exact two-sided signed-rank, n=3, all same sign: p = {2/2**3:.3f} (the floor)")
print(f"  scipy gives: p = {stats.wilcoxon(topv).pvalue:.4f}")
