"""Every criterion subset, under both codings."""
import random, re, statistics as st
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from scipy import stats
from experiments.human_rating.results import h2_rows, students
from app.domains.evaluation.domain.study_instrument import H2_CRITERIA

LIVE = Path.home() / "Library/CloudStorage/GoogleDrive-tosinamuda@gmail.com/My Drive/Revision Material Evaluation"
CASE = re.compile(r"-c\d+$"); S = {"clearly better": 2, "slightly better": 1}
SHORT = {1: "learner-evidence", 2: "calibration", 3: "integrity"}
rows = h2_rows(LIVE)
for r in rows:
    r["case"] = CASE.sub("", r["internal_packet_id"])
    t = r["chose"].lower()
    r["five"] = 0 if "same" in t else next(v for k, v in S.items() if k in t) * (1 if r["favoured_arm"] == "P1" else -1)
    r["three"] = (r["five"] > 0) - (r["five"] < 0)
strat = {s["student"]: s["ability_stratum"] for s in students()}
rank = {"lower": 0, "middle": 1, "top": 2}
case_student = {r["case"]: r["student"] for r in rows}

def analyse(subset, key, cats):
    sub = [r for r in rows if r["criterion"] in subset]
    panels = defaultdict(dict)
    for r in sub: panels[(r["case"], r["objective_index"], r["criterion"])][r["rater"]] = r
    P = [(v[sorted(v)[0]][key], v[sorted(v)[1]][key]) for v in panels.values() if len(v) == 2]
    K = len(cats); idx = {c: i for i, c in enumerate(cats)}
    def kap(pairs):
        n = len(pairs); O = [[0]*K for _ in range(K)]
        for p, q in pairs: O[idx[p]][idx[q]] += 1
        ra = [sum(O[i]) for i in range(K)]; cb = [sum(O[i][j] for i in range(K)) for j in range(K)]
        Wt = [[abs(cats[i]-cats[j])**2/(K-1)**2 for j in range(K)] for i in range(K)]
        num = sum(Wt[i][j]*O[i][j] for i in range(K) for j in range(K))
        den = sum(Wt[i][j]*ra[i]*cb[j]/n for i in range(K) for j in range(K))
        return 1 - num/den if den else float("nan")
    random.seed(0)
    bs = sorted(v for v in (kap([random.choice(P) for _ in P]) for _ in range(3000)) if v == v)
    per = defaultdict(list)
    for r in sub: per[r["case"]].append(r[key])
    cm = {c: st.mean(v) for c, v in per.items()}
    cs = sorted(cm)
    xs = [rank[strat[case_student[c]]] for c in cs]
    rho = stats.spearmanr(xs, [cm[c] for c in cs])
    top = [m for c, m in cm.items() if strat[case_student[c]] == "top"]
    rest = [m for c, m in cm.items() if strat[case_student[c]] != "top"]
    vals = list(cm.values())
    return dict(n=len(P), kappa=kap(P), lo=bs[int(.025*len(bs))], hi=bs[int(.975*len(bs))],
                eff=st.mean(vals), effp=stats.wilcoxon(vals, zero_method="wilcox").pvalue,
                rho=rho.statistic, rhop=rho.pvalue,
                gap=st.mean(rest)-st.mean(top), gapp=stats.mannwhitneyu(top, rest).pvalue)

subsets = [(1,2,3)] + [(a,b) for a,b in combinations((1,2,3),2)] + [(c,) for c in (1,2,3)]
def name(s): return "all three" if len(s)==3 else " + ".join(SHORT[c] for c in s)

print("═══ RELIABILITY (kappa, 95% CI) ═══\n")
print(f"{'criteria':34s} {'n':>4s}  {'5 boxes':>22s}   {'collapsed':>22s}")
print("─"*88)
for s in subsets:
    a = analyse(s, "five", list(range(-2,3))); b = analyse(s, "three", [-1,0,1])
    star = " *" if b["lo"] > 0 else ("  " if a["lo"] <= 0 else " *")
    print(f"{name(s):34s} {a['n']:>4d}  {a['kappa']:+.3f} [{a['lo']:+.3f},{a['hi']:+.3f}]   "
          f"{b['kappa']:+.3f} [{b['lo']:+.3f},{b['hi']:+.3f}]{star}")
print("\n  * = collapsed interval excludes zero")

print("\n\n═══ MAIN EFFECT (+ favours P1) ═══\n")
print(f"{'criteria':34s}  {'5 boxes':>18s}   {'collapsed':>18s}")
print("─"*78)
for s in subsets:
    a = analyse(s, "five", list(range(-2,3))); b = analyse(s, "three", [-1,0,1])
    print(f"{name(s):34s}  {a['eff']:+.3f} p={a['effp']:.3f}   {b['eff']:+.3f} p={b['effp']:.3f}")

print("\n\n═══ ABILITY GRADIENT ═══\n")
print(f"{'criteria':34s}  {'5 boxes: rho, p':>22s}   {'collapsed: rho, p':>22s}")
print("─"*86)
for s in subsets:
    a = analyse(s, "five", list(range(-2,3))); b = analyse(s, "three", [-1,0,1])
    m1 = "*" if a["rhop"] < .05 else " "; m2 = "*" if b["rhop"] < .05 else " "
    print(f"{name(s):34s}  {a['rho']:+.3f} p={a['rhop']:.4f}{m1}   {b['rho']:+.3f} p={b['rhop']:.4f}{m2}")
