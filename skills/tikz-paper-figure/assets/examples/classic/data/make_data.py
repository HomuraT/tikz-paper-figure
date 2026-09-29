"""Generate the data behind the classic-style examples (numpy only; every draw is seeded, so reruns agree).

    python make_data.py            # writes the .dat files next to this script, prints the inline snippets

Large sets go into .dat files that the figures read with \\addplot table; small ones are printed as TeX
coordinates and pasted into the figure source, so each example stays readable on its own. The statistics
(fits, confidence bands, box-plot numbers, KDEs, ellipses, p-values) are computed here, not in TeX, so a figure
and its numbers cannot drift apart.
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


# --------------------------------------------------------------------------- helpers
def write_dat(name: str, columns: dict[str, np.ndarray], fmt: str = "{:.5g}") -> None:
    keys = list(columns)
    n = len(columns[keys[0]])
    with open(HERE / name, "w", encoding="utf-8", newline="\n") as f:
        f.write(" ".join(keys) + "\n")
        for i in range(n):
            f.write(" ".join(fmt.format(float(columns[k][i])) for k in keys) + "\n")
    print(f"[data] {name}: {n} rows")


def coords(xs, ys, fx="{:g}", fy="{:g}") -> str:
    return " ".join(f"({fx.format(float(a))},{fy.format(float(b))})" for a, b in zip(xs, ys))


def betacf(a: float, b: float, x: float) -> float:
    """Continued fraction for the regularized incomplete beta function (Numerical Recipes 6.4)."""
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    d = 1.0 / (d if abs(d) > 1e-30 else 1e-30)
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d; d = 1.0 / (d if abs(d) > 1e-30 else 1e-30)
        c = 1.0 + aa / c if abs(c) > 1e-30 else 1e-30
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d; d = 1.0 / (d if abs(d) > 1e-30 else 1e-30)
        c = 1.0 + aa / c if abs(c) > 1e-30 else 1e-30
        de = d * c
        h *= de
        if abs(de - 1.0) < 3e-14:
            break
    return h


def betai(a: float, b: float, x: float) -> float:
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * betacf(a, b, x) / a
    return 1.0 - bt * betacf(b, a, 1.0 - x) / b


def t_sf2(t: float, df: float) -> float:
    """Two-sided p-value of Student's t."""
    return betai(0.5 * df, 0.5, df / (df + t * t))


def t_quantile(p: float, df: float) -> float:
    """Upper quantile t such that P(T > t) = 1 - p, by bisection."""
    lo, hi = 0.0, 50.0
    target = 2.0 * (1.0 - p)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if t_sf2(mid, df) > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def welch(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
    t = (a.mean() - b.mean()) / math.sqrt(va + vb)
    df = (va + vb) ** 2 / (va ** 2 / (len(a) - 1) + vb ** 2 / (len(b) - 1))
    return t, t_sf2(abs(t), df)


def stars(p: float) -> str:
    return "***" if p < 1e-3 else "**" if p < 1e-2 else "*" if p < 0.05 else "n.s."


def kde(x: np.ndarray, grid: np.ndarray, bw: float | None = None) -> np.ndarray:
    """Gaussian KDE with Scott's rule (scipy.stats.gaussian_kde's default)."""
    n = len(x)
    h = bw if bw is not None else x.std(ddof=1) * n ** (-1 / 5)
    z = (grid[:, None] - x[None, :]) / h
    return np.exp(-0.5 * z ** 2).sum(axis=1) / (n * h * math.sqrt(2 * math.pi))


def boxstats(x: np.ndarray) -> dict[str, float]:
    """Matplotlib's boxplot_stats (whis=1.5, linear percentiles)."""
    q1, med, q3 = np.percentile(x, [25, 50, 75])
    iqr = q3 - q1
    lo = x[x >= q1 - 1.5 * iqr].min()
    hi = x[x <= q3 + 1.5 * iqr].max()
    return dict(q1=q1, med=med, q3=q3, lo=lo, hi=hi, mean=x.mean(), fliers=x[(x < lo) | (x > hi)])


def ellipse(x: np.ndarray, y: np.ndarray, n_std: float, n: int = 120) -> tuple[np.ndarray, np.ndarray]:
    """Covariance ellipse as in Matplotlib's confidence_ellipse example (Pearson construction)."""
    cov = np.cov(x, y)
    r = cov[0, 1] / math.sqrt(cov[0, 0] * cov[1, 1])
    rx, ry = math.sqrt(1 + r), math.sqrt(1 - r)
    t = np.linspace(0, 2 * math.pi, n)
    ex, ey = rx * np.cos(t), ry * np.sin(t)
    # rotate by 45 degrees, then scale by n_std standard deviations and shift to the mean
    c, s = math.cos(math.pi / 4), math.sin(math.pi / 4)
    ux, uy = c * ex - s * ey, s * ex + c * ey
    sx, sy = math.sqrt(cov[0, 0]) * n_std, math.sqrt(cov[1, 1]) * n_std
    return x.mean() + ux * sx, y.mean() + uy * sy


# --------------------------------------------------------------------------- figures
def kinetics() -> None:
    rng = np.random.default_rng(21)
    t = np.array([0, 2, 4, 6, 8, 10, 15, 20, 30, 40, 50, 60], float)
    for name, k in (("A", 0.12), ("blank", 0.04)):
        y = 1 - np.exp(-k * t) + rng.normal(0, 0.018, len(t))
        y = np.minimum(y, 0.997 - 0.004 * rng.random(len(t)))    # a conversion cannot exceed 1
        y[0] = 0.0
        e = 0.012 + 0.02 * rng.random(len(t))
        e[0] = 0.0
        # least-squares k of the first-order model on the points (log-linearised fit is biased near 1)
        ks = np.linspace(0.5 * k, 1.5 * k, 20001)
        sse = ((y[None, :] - (1 - np.exp(-ks[:, None] * t[None, :]))) ** 2).sum(axis=1)
        kf = ks[sse.argmin()]
        print(f"KINETICS {name}: k_fit={kf:.4f}  t_half={math.log(2) / kf:.2f}")
        print("   ", " ".join(f"({a:g},{b:.3f}) +- (0,{c:.3f})" for a, b, c in zip(t, y, e)))


def calibration() -> None:
    x = np.array([0.000,0.345,0.690,1.034,1.379,1.724,2.069,2.414,2.759,3.103,3.448,3.793,4.138,4.483,4.828,5.172,
                  5.517,5.862,6.207,6.552,6.897,7.241,7.586,7.931,8.276,8.621,8.966,9.310,9.655,10.000])
    y = np.array([1.12,2.22,2.36,2.46,3.71,3.90,5.83,8.01,6.77,7.40,9.39,10.02,10.52,10.15,11.92,13.49,12.02,13.77,
                  12.95,14.40,14.56,17.11,16.74,19.21,19.86,20.25,18.46,21.41,22.73,23.68])
    n = len(x)
    b, a = np.polyfit(x, y, 1)
    res = y - (a + b * x)
    s = math.sqrt((res ** 2).sum() / (n - 2))
    sxx = ((x - x.mean()) ** 2).sum()
    r2 = 1 - (res ** 2).sum() / ((y - y.mean()) ** 2).sum()
    tq = t_quantile(0.975, n - 2)
    lod = 3.3 * s / b
    print(f"CALIB a={a:.4f} b={b:.4f} s={s:.4f} xbar={x.mean():.4f} Sxx={sxx:.4f} R2={r2:.4f} t={tq:.4f} n={n} LOD={lod:.3f}")
    print("CALIB residuals:", coords(x, res, "{:.3f}", "{:.3f}"))


def errorbars() -> None:
    rng = np.random.default_rng(5)
    T = np.array([25, 40, 55, 70, 85], float)
    u = 1 / (T + 273.15)
    R = 8.314e-3
    for name, lnA, Ea in (("A", 12.3, 30.0), ("B", 12.6, 32.5)):
        k = np.exp(lnA - Ea / (R * (T + 273.15))) * np.exp(rng.normal(0, 0.03, len(T)))
        e = k * (0.06 + 0.03 * rng.random(len(T)))
        # weighted fit of ln k = c0 + c1 u  (weights 1/var of ln k)
        w = (k / e) ** 2
        W = np.diag(w)
        X = np.c_[np.ones_like(u), u]
        cov = np.linalg.inv(X.T @ W @ X)
        c0, c1 = cov @ X.T @ W @ np.log(k)
        print(f"ARRH {name}: c0={c0:.4f} c1={c1:.2f} Ea={-c1 * R:.2f} kJ/mol  cov00={cov[0,0]:.6g} cov01={cov[0,1]:.6g} cov11={cov[1,1]:.6g}")
        print("   ", " ".join(f"({a:g},{b:.3f}) +- (0,{c:.3f})" for a, b, c in zip(T, k, e)))


def histogram() -> None:
    rng = np.random.default_rng(3)
    h1 = rng.normal(5.0, 0.8, 500)
    h2 = rng.normal(6.4, 1.0, 500)
    bins = np.linspace(2, 10, 33)
    for name, h in (("1", h1), ("2", h2)):
        c, _ = np.histogram(h, bins)
        print(f"HIST{name} mean={h.mean():.3f} sd={h.std(ddof=1):.3f} median={np.median(h):.3f} n={len(h)}")
        print("   bars:", coords(bins, list(c) + [0]))
        # outline of histtype='step': start and end on the baseline
        xs = [bins[0]] + [v for v in bins for _ in (0, 1)][1:-1] + [bins[-1]]
        ys = [0] + [v for v in c for _ in (0, 1)] + [0]
        print("   step:", coords(xs, ys))


def boxplot() -> None:
    rng = np.random.default_rng(11)
    groups = ["A", "B", "C", "D"]
    data = [rng.normal(m, s, 30) for m, s in [(72, 4), (80, 3), (65, 6), (84, 2.5)]]
    data[1] = np.append(data[1], [68.5])
    data[3] = np.append(data[3], [76.0, 91.5])
    for i, (g, d) in enumerate(zip(groups, data), start=1):
        st = boxstats(d)
        print(f"BOX {g}: median={st['med']:.2f}, lower quartile={st['q1']:.2f}, upper quartile={st['q3']:.2f}, "
              f"lower whisker={st['lo']:.2f}, upper whisker={st['hi']:.2f}  mean={st['mean']:.2f}  "
              f"fliers={' '.join(f'{v:.2f}' for v in st['fliers'])}")
        jit = rng.uniform(-0.12, 0.12, len(d))
        print("   pts:", coords(i + jit, d, "{:.3f}", "{:.2f}"))
    for a, b in ((1, 4), (2, 4), (3, 4), (1, 2)):
        t, p = welch(data[a - 1], data[b - 1])
        print(f"BOX welch {groups[a-1]} vs {groups[b-1]}: t={t:.2f} p={p:.2e} {stars(p)}")


def heatmap() -> None:
    temps = [40, 50, 60, 70, 80, 90]
    loads = [0.5, 1, 2, 3, 4, 5]
    rows = []
    for T in temps:
        row = []
        for L in loads:
            conv = 1 - math.exp(-0.32 * L * (T / 50) ** 1.6)
            decomp = math.exp(-((max(T - 70, 0)) / 28) ** 2)     # the product degrades above 70 C
            row.append(round(97 * conv * decomp))
        rows.append(row)
    print("HEAT rows (T top to bottom):", rows)
    print("   ", " ".join(f"({c},{r}) [{rows[r][c]}]" for r in range(len(temps)) for c in range(len(loads))))


def twin_axes() -> None:
    rng = np.random.default_rng(8)
    t = np.round(np.arange(0, 24.001, 0.2), 3)
    T = np.empty_like(t)
    for i, ti in enumerate(t):
        if ti <= 3:
            T[i] = 70 - 48 * math.exp(-ti / 0.9) * math.cos(0.6 * ti)
        elif ti <= 18:
            T[i] = 70 + 1.6 * math.exp(-(ti - 3) / 2.5) * math.sin(2.1 * (ti - 3)) + rng.normal(0, 0.25)
        else:
            T[i] = 24 + 46 * math.exp(-(ti - 18) / 1.6)
    Tk = T + 273.15
    P = np.where(t < 3, 1.0 * Tk / 295.15, 1.0 * Tk / 295.15 + 2.9 * (1 - np.exp(-(t - 3) / 3.8)) * Tk / 343.15)
    P = P + rng.normal(0, 0.015, len(t))
    write_dat("twin-axes.dat", {"t": t, "T": T, "P": P}, "{:.4g}")


def raincloud() -> None:
    rng = np.random.default_rng(42)
    groups = {
        "solgel": rng.lognormal(math.log(12), 0.18, 60),
        "hydro": rng.normal(18, 2.2, 60),
        "coprec": rng.lognormal(math.log(22), 0.25, 60),
        "micro": np.r_[rng.normal(10.5, 1.4, 34), rng.normal(19.5, 1.8, 26)],   # bimodal: the box hides it
    }
    grid = np.linspace(2, 40, 200)
    cols = {"x": grid}
    for k, v in groups.items():
        d = kde(v, grid)
        cols[k] = d / d.max()           # every cloud scaled to the same peak height
    write_dat("raincloud-kde.dat", cols, "{:.4g}")
    for i, (k, v) in enumerate(groups.items(), start=1):
        st = boxstats(v)
        print(f"RAIN {k}: median={st['med']:.2f}, lower quartile={st['q1']:.2f}, upper quartile={st['q3']:.2f}, "
              f"lower whisker={st['lo']:.2f}, upper whisker={st['hi']:.2f}  mean={v.mean():.2f} n={len(v)}")
    pts = {"x": [], "y": [], "g": []}
    for i, (k, v) in enumerate(groups.items(), start=1):
        pts["x"] += list(v)
        pts["y"] += list(i - 0.24 + rng.uniform(-0.09, 0.09, len(v)))
        pts["g"] += [i] * len(v)
    write_dat("raincloud-points.dat", {k: np.array(v) for k, v in pts.items()}, "{:.4g}")


def joint() -> None:
    rng = np.random.default_rng(7)
    n = 120
    x1 = rng.normal(44, 7.5, n)
    y1 = 89 - 0.32 * (x1 - 44) + rng.normal(0, 2.6, n)
    x2 = rng.normal(63, 6.5, n)
    y2 = 78 - 0.48 * (x2 - 63) + rng.normal(0, 3.2, n)
    write_dat("joint-points.dat", {"x1": x1, "y1": y1, "x2": x2, "y2": y2}, "{:.4g}")
    cols = {}
    for tag, (x, y) in (("a", (x1, y1)), ("b", (x2, y2))):
        for s in (1, 2):
            ex, ey = ellipse(x, y, s)
            cols[f"{tag}{s}x"], cols[f"{tag}{s}y"] = ex, ey
        r = np.corrcoef(x, y)[0, 1]
        print(f"JOINT {tag}: mean=({x.mean():.2f},{y.mean():.2f}) sd=({x.std(ddof=1):.2f},{y.std(ddof=1):.2f}) r={r:.3f}")
    write_dat("joint-ellipses.dat", cols, "{:.4g}")
    bx = np.arange(20, 90.1, 2.5)
    by = np.arange(62, 102.1, 1.5)
    gx, gy = np.linspace(20, 90, 200), np.linspace(62, 102, 200)
    hx, hy = {"e": bx}, {"e": by}      # bin edges and counts, a trailing 0 closing the last bin
    for tag, (x, y) in (("a", (x1, y1)), ("b", (x2, y2))):
        cx, _ = np.histogram(x, bx)
        cy, _ = np.histogram(y, by)
        hx[tag], hy[tag] = list(cx) + [0], list(cy) + [0]
        print(f"JOINT {tag} histx:", coords(bx, hx[tag]))
        print(f"JOINT {tag} histy:", coords(by, hy[tag]))
        cols2 = {"gx": gx, "kx": kde(x, gx) * n * 2.5, "gy": gy, "ky": kde(y, gy) * n * 1.5}
        write_dat(f"joint-kde-{tag}.dat", cols2, "{:.4g}")
    write_dat("joint-histx.dat", hx, "{:g}")
    write_dat("joint-histy.dat", hy, "{:g}")


def pseudo_voigt(x: np.ndarray, x0: float, fwhm: float, eta: float = 0.5) -> np.ndarray:
    g = np.exp(-4 * math.log(2) * ((x - x0) / fwhm) ** 2)
    lor = 1 / (1 + 4 * ((x - x0) / fwhm) ** 2)
    return eta * lor + (1 - eta) * g


ANATASE = [(25.28, 100, "101"), (36.95, 10, "103"), (37.80, 20, "004"), (38.58, 10, "112"), (48.05, 35, "200"),
           (53.89, 20, "105"), (55.06, 20, "211"), (62.12, 4, "213"), (62.69, 14, "204"), (68.76, 6, "116"),
           (70.31, 6, "220"), (74.03, 1, "107"), (75.03, 10, "215"), (76.02, 4, "301")]
RUTILE = [(27.45, 100, "110"), (36.09, 50, "101"), (39.19, 8, "200"), (41.23, 25, "111"), (44.05, 10, "210"),
          (54.32, 60, "211"), (56.64, 20, "220"), (62.74, 10, "002"), (64.04, 10, "310"), (69.01, 20, "301")]


def xrd() -> None:
    rng = np.random.default_rng(12)
    tt = np.round(np.arange(20, 80.0001, 0.02), 3)
    fwhm = lambda x: 0.42 + 0.004 * (x - 20)          # peaks broaden with angle (size + strain)

    def base(t: np.ndarray) -> np.ndarray:           # air scatter + amorphous hump + anatase
        y = 60 + 900 * np.exp(-(t - 20) / 9) + 40 * np.exp(-0.5 * ((t - 27) / 6) ** 2)
        for x0, i, _ in ANATASE:
            y = y + 5200 * i / 100 * pseudo_voigt(t, x0, fwhm(x0))
        return y

    def rutile(t: np.ndarray) -> np.ndarray:         # 3.5 % rutile
        return sum(5200 * 0.035 * i / 100 * pseudo_voigt(t, x0, fwhm(x0) * 0.9) for x0, i, _ in RUTILE)

    y = rng.poisson(base(tt) + rutile(tt)).astype(float)
    write_dat("xrd.dat", {"tt": tt, "I": y}, "{:.5g}")
    # the model over the zoomed window: without and with the rutile phase
    tz = np.round(np.arange(26.0, 28.8001, 0.01), 3)
    write_dat("xrd-inset.dat", {"tt": tz, "base": base(tz), "fit": base(tz) + rutile(tz)}, "{:.5g}")
    print("XRD anatase sticks:", " ".join(f"({x},{i})" for x, i, _ in ANATASE))
    print("XRD rutile sticks:", " ".join(f"({x},{i})" for x, i, _ in RUTILE))
    for x0, i, h in ANATASE:
        m = (tt > x0 - 0.3) & (tt < x0 + 0.3)
        print(f"   A {h} at {x0}: peak counts {y[m].max():.0f}")
    m = (tt > 27.2) & (tt < 27.7)
    print(f"   R 110 peak counts {y[m].max():.0f}")


def mep() -> None:
    """Minimum energy path of the Mueller-Brown potential by the simplified string method (E, Ren, Vanden-Eijnden 2007)."""
    A = np.array([-200, -100, -170, 15.0]); a = np.array([-1, -1, -6.5, 0.7]); b = np.array([0, 0, 11, 0.6])
    c = np.array([-10, -10, -6.5, 0.7]); x0 = np.array([1, 0, -0.5, -1.0]); y0 = np.array([0, 0.5, 1.5, 1.0])

    def V(x, y):
        dx, dy = x[..., None] - x0, y[..., None] - y0
        return (A * np.exp(a * dx ** 2 + b * dx * dy + c * dy ** 2)).sum(-1)

    def grad(x, y):
        dx, dy = x[..., None] - x0, y[..., None] - y0
        e = A * np.exp(a * dx ** 2 + b * dx * dy + c * dy ** 2)
        return (e * (2 * a * dx + b * dy)).sum(-1), (e * (b * dx + 2 * c * dy)).sum(-1)

    n = 60
    s = np.linspace(0, 1, n)
    x = -0.558 + (0.623 + 0.558) * s                   # straight line from minimum A to minimum B
    y = 1.442 + (0.028 - 1.442) * s
    for _ in range(40000):
        gx, gy = grad(x, y)
        x, y = x - 1e-4 * gx, y - 1e-4 * gy
        x[0], y[0], x[-1], y[-1] = -0.558, 1.442, 0.623, 0.028
        d = np.r_[0, np.cumsum(np.hypot(np.diff(x), np.diff(y)))]
        d /= d[-1]
        x, y = np.interp(s, d, x), np.interp(s, d, y)
    e = V(x, y)
    print("MEP:", coords(x[::2], y[::2], "{:.3f}", "{:.3f}"))
    i = np.argsort(e)
    print("MEP energies along the path (max = barrier):", f"{e.max():.2f} at ({x[e.argmax()]:.3f},{y[e.argmax()]:.3f})")
    for px, py, lab in ((-0.558, 1.442, "A"), (0.623, 0.028, "B"), (-0.050, 0.467, "C"),
                        (-0.822, 0.624, "TS1"), (0.212, 0.293, "TS2")):
        print(f"   {lab}: V={V(np.array(px), np.array(py)):.2f}")


def rsm() -> None:
    """Central composite design on a quadratic response surface: yield vs temperature and time."""
    rng = np.random.default_rng(4)
    f = lambda T, t: 88 - 0.022 * (T - 78) ** 2 - 0.9 * (t - 5.2) ** 2 + 0.035 * (T - 78) * (t - 5.2)
    a = math.sqrt(2)
    pts = [(-1, -1), (1, -1), (-1, 1), (1, 1), (-a, 0), (a, 0), (0, -a), (0, a), (0, 0), (0, 0), (0, 0)]
    Tc, Th, tc, th = 70, 15, 5, 2.2      # centre and half-range in real units
    out = []
    for u, v in pts:
        T, t = Tc + Th * u, tc + th * v
        out.append((T, t, f(T, t) + rng.normal(0, 0.8)))
    print("RSM design points:", " ".join(f"({T:.1f},{t:.2f},{yv:.1f})" for T, t, yv in out))
    print("RSM optimum: T=78, t=5.2, yield=88")


def spectra_waterfall() -> None:
    print("WATERFALL: expressions in the figure; nothing to generate")


DASH = {"a": (112, 8.0, 8.0, 52), "b": (141, 9.0, 1.6, 64), "c": (168, 10.0, 0.35, 76)}   # T50, w, r(110 C), Ea


def dashboard() -> None:
    """Three Pt catalysts in CO oxidation: light-off, Arrhenius plot in the kinetic regime, stability."""
    rng = np.random.default_rng(21)
    T = np.arange(50, 250.1, 10)
    cols = {"T": T}
    for k, (t50, w, _, _) in DASH.items():
        x = 100 / (1 + np.exp(-(T - t50) / w)) + rng.normal(0, 1.2, T.size)
        cols[k] = np.clip(x, 0, 100)
    write_dat("lightoff.dat", cols, "{:.4g}")
    Tk = np.arange(90, 130.1, 10) + 273.15
    for k, (_, _, r110, ea) in DASH.items():
        r = r110 * np.exp(-ea * 1e3 / 8.314 * (1 / Tk - 1 / 383.15)) * np.exp(rng.normal(0, 0.03, Tk.size))
        x, y = 1000 / Tk, np.log(r)
        b, a = np.polyfit(x, y, 1)
        print(f"DASH arrhenius {k}: fit ln r = {a:.4f} + ({b:.4f}) x  Ea = {-b * 8.314:.1f} kJ/mol  pts:", coords(x, y, "{:.4f}", "{:.3f}"))
    t = np.arange(0, 50.01, 0.5)
    regen = t >= 30
    tt = np.where(regen, t - 30, t)
    stab = {"t": t,
            "a": 99.3 - 0.01 * t + rng.normal(0, 0.35, t.size),
            "b": 52 + np.where(regen, 20, 21) * np.exp(-tt / 20) + rng.normal(0, 0.8, t.size),
            "c": 5 + np.where(regen, 4.5, 5) * np.exp(-tt / 12) + rng.normal(0, 0.4, t.size)}
    stab["a"] = np.clip(stab["a"], 0, 100)
    write_dat("stability.dat", stab, "{:.4g}")


if __name__ == "__main__":
    kinetics(); calibration(); errorbars(); histogram(); boxplot(); heatmap(); twin_axes(); raincloud(); joint()
    xrd(); mep(); rsm(); dashboard()
