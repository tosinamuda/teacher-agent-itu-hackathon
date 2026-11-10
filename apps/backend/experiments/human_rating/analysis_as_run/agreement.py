"""Agreement between the two raters of a case, with A/B decoded to a common direction."""
import random, re, statistics as st
from collections import Counter, defaultdict
from pathlib import Path
from scipy import stats
from experiments.human_rating import mapping
from experiments.human_rating.results import h2_rows

LIVE = Path.home() / "Library/CloudStorage/GoogleDrive-tosinamuda@gmail.com/My Drive/Revision Material Evaluation"
CASE = re.compile(r"-c\d+$")
STRENGTH = {"clearly better": 2, "slightly better": 1}

def signed(r):
    t = r["chose"].lower()
    if "same" in t:
        return 0
    mag = next(v for k, v in STRENGTH.items() if k in t)
    return mag if r["favoured_arm"] == "P1" else -mag

rows = h2_rows(LIVE)
for r in rows:
    r["case"] = CASE.sub("", r["internal_packet_id"])
    r["signed"] = signed(r)

assigned = defaultdict(set)
for a in mapping.load_h2():
    assigned[CASE.sub("", a.internal_id)].add(a.rater)

panels = defaultdict(dict)
for r in rows:
    panels[(r["case"], r["objective_index"], r["criterion"])][r["rater"]] = r
paired = [(k, v) for k, v in panels.items() if len(v) == 2]
print(f"=== {len(paired)} panels carry two independent judgements ===")
print(f"    across {len({k[0] for k, _ in paired})} cases, "
      f"pairs: {dict(Counter(tuple(sorted(v)) for _, v in paired))}\n")

x, y = [], []
for k, v in paired:
    a, b = sorted(v)
    x.append(v[a]["signed"]); y.append(v[b]["signed"])

exact = sum(p == q for p, q in zip(x, y)) / len(x)
sign = lambda n: (n > 0) - (n < 0)
direction = sum(sign(p) == sign(q) for p, q in zip(x, y)) / len(x)
opposite = sum(sign(p) * sign(q) < 0 for p, q in zip(x, y))
print(f"  exact agreement (5-point) : {exact:.1%}")
print(f"  same direction            : {direction:.1%}")
print(f"  flatly opposite           : {opposite} of {len(x)} ({opposite/len(x):.1%})")
print(f"  mean absolute gap         : {st.mean(abs(p-q) for p, q in zip(x,y)):.2f} scale points")
print(f"  Pearson r                 : {stats.pearsonr(x,y)[0]:+.3f} (p={stats.pearsonr(x,y)[1]:.3f})")
print(f"  Spearman rho              : {stats.spearmanr(x,y).statistic:+.3f}")

cats = list(range(-2, 3)); k = len(cats); idx = {c: i for i, c in enumerate(cats)}
def kappa(px, py, power=2):
    n = len(px)
    O = [[0]*k for _ in range(k)]
    for p, q in zip(px, py): O[idx[p]][idx[q]] += 1
    ra = [sum(O[i]) for i in range(k)]; cb = [sum(O[i][j] for i in range(k)) for j in range(k)]
    W = [[abs(cats[i]-cats[j])**power / (k-1)**power for j in range(k)] for i in range(k)]
    num = sum(W[i][j]*O[i][j] for i in range(k) for j in range(k))
    den = sum(W[i][j]*ra[i]*cb[j]/n for i in range(k) for j in range(k))
    return 1 - num/den if den else float("nan")

random.seed(0)
boots = sorted(v for v in (kappa(*zip(*[random.choice(list(zip(x,y))) for _ in range(len(x))]))
                           for _ in range(4000)) if v == v)
print(f"  quadratic weighted kappa  : {kappa(x,y):+.3f}  "
      f"95% CI [{boots[int(.025*len(boots))]:+.3f}, {boots[int(.975*len(boots))]:+.3f}]")
print(f"  linear weighted kappa     : {kappa(x,y,1):+.3f}")

print("\n  agreement by criterion:")
for crit in (1, 2, 3):
    sub = [(v[sorted(v)[0]]["signed"], v[sorted(v)[1]]["signed"]) for kk, v in paired if kk[2] == crit]
    if len(sub) > 2:
        px, py = zip(*sub)
        print(f"    criterion {crit}: n={len(sub):2d}  exact={sum(p==q for p,q in sub)/len(sub):5.1%}  "
              f"opposite={sum(sign(p)*sign(q)<0 for p,q in sub):2d}  kappa={kappa(list(px),list(py)):+.3f}")

print("\n  agreement by rater pair:")
for pair in sorted({tuple(sorted(v)) for _, v in paired}):
    sub = [(v[pair[0]]["signed"], v[pair[1]]["signed"]) for _, v in paired if tuple(sorted(v)) == pair]
    px, py = zip(*sub)
    print(f"    {pair[0]} & {pair[1]}: n={len(sub):2d}  exact={sum(p==q for p,q in sub)/len(sub):5.1%}  "
          f"opposite={sum(sign(p)*sign(q)<0 for p,q in sub):2d}  mean gap={st.mean(abs(p-q) for p,q in sub):.2f}")

print("\n=== P1 vs P0, clustered by case ===")
per = defaultdict(list)
for r in rows: per[r["case"]].append(r["signed"])
means = {c: st.mean(v) for c, v in per.items()}
pos = sum(1 for m in means.values() if m > 0); neg = sum(1 for m in means.values() if m < 0)
print(f"  cases with any rating: {len(means)}  P1: {pos}  P0: {neg}  tied: {len(means)-pos-neg}")
print(f"  mean of case means: {st.mean(means.values()):+.3f}   "
      f"sign test p={stats.binomtest(pos, pos+neg, 0.5).pvalue:.4f}   "
      f"Wilcoxon p={stats.wilcoxon(list(means.values()), zero_method='wilcox').pvalue:.4f}")
