"""Story figures for the research grid.

Every figure here follows the pattern of the PINN figure: a short story
with a before and an after (hold, ease through the change, hold, fade,
loop), all on one SMIL timeline so diagrams.js can pause and resume a
figure as a unit. Geometry comes from the real model wherever there is
one: a real Gaussian process, real Voronoi grains, real inverse
kinematics.
"""
import heapq
import math

import numpy as np
from scipy.spatial import Voronoi

W, H = 220, 140


# ------------------------------------------------------------- helpers
def plate():
    return '<rect class="dg-plate" x=".5" y=".5" width="%g" height="%g"/>' % (W - 1, H - 1)


def svg(cls, label, body):
    return ('<svg class="dg %s" viewBox="0 0 %d %d" role="img" aria-label="%s">\n      %s\n    </svg>'
            % (cls, W, H, label, body))


def kts(times):
    return ";".join("%.4f" % t for t in times)


def anim(attr, values, times, dur, calc="linear"):
    return ('<animate attributeName="%s" dur="%s" repeatCount="indefinite" calcMode="%s"'
            ' keyTimes="%s" values="%s"/>' % (attr, dur, calc, kts(times), ";".join(values)))


def fade(dur, hold_end=0.88, gone=0.96, start=0.03):
    return anim("opacity", ["0", "1", "1", "0", "0"], [0, start, hold_end, gone, 1], dur)


def pts(seq):
    return " ".join("%.1f,%.1f" % (x, y) for x, y in seq)


def ease(u):
    return 0.5 - 0.5 * math.cos(math.pi * min(1.0, max(0.0, u)))


# ------------------------------------------------- uncertainty (GP)
def fig_uq():
    DUR = "9s"
    X0, X1, MID, AMP = 16.0, 204.0, 68.0, 34.0
    X = lambda s: X0 + (X1 - X0) * s
    Y = lambda u: min(132.0, max(8.0, MID - AMP * u))

    f = lambda s: 0.72 * np.sin(2.2 * np.pi * s) + 0.22 * np.sin(5.4 * np.pi * s + 0.4)
    sd = lambda s: 0.03 + 0.20 * s                  # noise grows to the right

    rng = np.random.default_rng(11)
    xo = np.array([0.05, 0.16, 0.28, 0.39, 0.51, 0.62, 0.73, 0.85, 0.95])
    yo = f(xo) + sd(xo) * rng.standard_normal(len(xo))
    order = [4, 1, 7, 2, 6, 0, 8, 3, 5]

    sf, ell = 0.6, 0.11
    kern = lambda a, b: sf ** 2 * np.exp(-((a[:, None] - b[None, :]) ** 2) / (2 * ell ** 2))
    g = np.linspace(0, 1, 30)

    states = []
    for k in range(len(order) + 1):
        idx = order[:k]
        if not idx:
            mu = np.zeros_like(g)
            var = np.full_like(g, sf ** 2)
        else:
            xs, ys = xo[idx], yo[idx]
            K = kern(xs, xs) + np.diag(sd(xs) ** 2)
            Ks = kern(g, xs)
            sol = np.linalg.solve(K, np.column_stack([ys, Ks.T]))
            mu = Ks @ sol[:, 0]
            var = np.clip(sf ** 2 - np.einsum("ij,ji->i", Ks, sol[:, 1:]), 1e-6, None)
        band = 2 * np.sqrt(var + sd(g) ** 2)
        top = [(X(s), Y(m + b)) for s, m, b in zip(g, mu, band)]
        bot = [(X(s), Y(m - b)) for s, m, b in zip(g, mu, band)]
        states.append((pts([(X(s), Y(m)) for s, m in zip(g, mu)]), pts(top + bot[::-1])))

    n = len(states)
    times = [0.0] + [0.06 + 0.70 * k / (n - 1) for k in range(n)] + [1.0]
    means = [states[0][0]] + [s[0] for s in states] + [states[-1][0]]
    bands = [states[0][1]] + [s[1] for s in states] + [states[-1][1]]

    dots = ""
    for rank, i in enumerate(order):
        t = 0.06 + 0.70 * (rank + 1) / (n - 1)
        dots += ('<circle class="uq-obs" cx="%.1f" cy="%.1f" r="3.4">%s</circle>'
                 % (X(xo[i]), Y(yo[i]), anim("opacity", ["0", "1", "1"], [0, t, 1], DUR, "discrete")))

    body = (
        plate()
        + '<polyline class="uq-true" points="%s"/>' % pts([(X(s), Y(v)) for s, v in zip(g, f(g))])
        + "<g>" + fade(DUR)
        + '<polygon class="uq-band" points="%s">%s</polygon>' % (bands[1], anim("points", bands, times, DUR))
        + '<polyline class="uq-mean" points="%s">%s</polyline>' % (means[1], anim("points", means, times, DUR))
        + dots + "</g>"
    )
    return svg("dg-uq", "A Gaussian process tightening its uncertainty band as observations arrive, wider where noise grows", body)


# ------------------------------------------------ LLM: generation + attention
def fig_llm():
    DUR = "8s"
    n, prompt = 9, 4
    cw, gap, y0, ch = 18.0, 3.2, 100.0, 20.0
    x0 = (W - (n * cw + (n - 1) * gap)) / 2
    cx = [x0 + i * (cw + gap) + cw / 2 for i in range(n)]
    steps = n - prompt
    T0, T1 = 0.06, 0.82
    d = (T1 - T0) / steps

    rng = np.random.default_rng(5)
    chips, arcs = "", ""
    for i in range(n):
        x = x0 + i * (cw + gap)
        cls = "llm-prompt" if i < prompt else "llm-gen"
        inner = ('<rect class="llm-chip %s" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4"/>'
                 '<rect class="llm-ink %s" x="%.1f" y="%.1f" width="8" height="2.4" rx="1.2"/>'
                 % (cls, x, y0, cw, ch, cls, x + 5, y0 + ch / 2 - 1.2))
        if i < prompt:
            chips += inner
        else:
            ts = T0 + (i - prompt) * d
            chips += ("<g>%s%s%s</g>" % (
                anim("opacity", ["0", "0", "1", "1"], [0, ts, ts + 0.02, 1], DUR),
                '<animateTransform attributeName="transform" type="translate" dur="%s"'
                ' repeatCount="indefinite" keyTimes="%s" values="0 6;0 6;0 0;0 0"/>'
                % (DUR, kts([0, ts, ts + 0.03, 1])),
                inner))

    for s in range(steps):
        k = prompt + s
        logits = rng.normal(0, 1.0, k) + np.linspace(-0.6, 0.6, k) + (np.arange(k) < prompt) * 0.5
        w = np.exp(1.6 * logits)
        w /= w.sum()
        top = int(np.argmax(w))
        ts, te = T0 + s * d, (T0 + (s + 1) * d if s < steps - 1 else 0.88)
        paths = ""
        for j in range(k):
            dx = abs(cx[k] - cx[j])
            cy = y0 - 8 - 0.62 * dx
            cls = "llm-arc top" if j == top else "llm-arc"
            paths += ('<path class="%s" d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" stroke-width="%.2f" stroke-opacity="%.2f"/>'
                      % (cls, cx[k], y0, (cx[k] + cx[j]) / 2, cy, cx[j], y0,
                         0.9 + 3.2 * w[j] / w.max(), 0.25 + 0.75 * w[j] / w.max()))
        arcs += ("<g>%s%s</g>" % (
            anim("opacity", ["0", "0", "1", "1", "0", "0"],
                 [0, ts, ts + 0.025, te - 0.02, te, 1], DUR), paths))

    body = plate() + "<g>" + fade(DUR) + arcs + chips + "</g>"
    return svg("dg-llm", "A language model emitting tokens one at a time, each attending back over the sequence", body)


# ------------------------------------------------------------ agentic loop
def fig_agent():
    DUR = "4.8s"
    cx, cy, R = 110.0, 72.0, 44.0
    C = 2 * math.pi * R
    ring = "M%.1f %.1f A%.0f %.0f 0 1 1 %.2f %.1f" % (cx, cy - R, R, R, cx - 0.01, cy - R)

    comet = ""
    for L, op, wdt in ((70, 0.16, 5), (40, 0.38, 4), (16, 0.9, 3.2)):
        comet += ('<path class="agent-comet" d="%s" stroke-width="%.1f" stroke-opacity="%.2f"'
                  ' stroke-dasharray="%.1f %.1f">%s</path>'
                  % (ring, wdt, op, L, C - L,
                     anim("stroke-dashoffset", ["%.1f" % L, "%.1f" % (L - C)], [0, 1], DUR)))

    nodes = ""
    for p, ang in ((0.0, -90), (0.25, 0), (0.5, 90), (0.75, 180)):
        x = cx + R * math.cos(math.radians(ang))
        y = cy + R * math.sin(math.radians(ang))
        if p == 0:
            glow = anim("opacity", [".55", "0", "0", ".55"], [0, 0.14, 0.94, 1], DUR)
        else:
            glow = anim("opacity", ["0", "0", ".55", "0", "0"], [0, p - 0.05, p, p + 0.14, 1], DUR)
        nodes += '<circle class="agent-glow" cx="%.1f" cy="%.1f" r="19" opacity="0">%s</circle>' % (x, y, glow)
        nodes += '<circle class="agent-node" cx="%.1f" cy="%.1f" r="14"/>' % (x, y)
        if ang == -90:     # plan: a short list
            nodes += ('<path class="agent-glyph" d="M%.1f %.1fh12M%.1f %.1fh12M%.1f %.1fh8"/>'
                      % (x - 6, y - 4.5, x - 6, y, x - 6, y + 4.5))
        elif ang == 0:     # run: play
            nodes += ('<path class="agent-solid" d="M%.1f %.1fL%.1f %.1fL%.1f %.1fZ"/>'
                      % (x - 3.5, y - 6, x + 6, y, x - 3.5, y + 6))
        elif ang == 90:    # observe: a small bar chart
            nodes += ('<path class="agent-solid" d="M%.1f %.1fh3v4.5h-3zM%.1f %.1fh3v8.5h-3zM%.1f %.1fh3v12h-3z"/>'
                      % (x - 6.5, y + 1.5, x - 1.5, y - 2.5, x + 3.5, y - 6))
        else:              # revise: a turning arrow
            nodes += ('<path class="agent-glyph" d="M%.1f %.1fA5.6 5.6 0 1 0 %.1f %.1f"/>'
                      '<path class="agent-solid" d="M%.1f %.1fl4.6 -.4l-2.2 4z"/>'
                      % (x + 4.6, y - 2.6, x + 3.8, y + 4.2, x + 2.4, y - 5.4))

    head = ('<g><animateTransform attributeName="transform" type="rotate" from="0 %.0f %.0f" to="360 %.0f %.0f"'
            ' dur="%s" repeatCount="indefinite"/><circle class="agent-head" cx="%.0f" cy="%.0f" r="4.8"/></g>'
            % (cx, cy, cx, cy, DUR, cx, cy - R))

    body = (plate()
            + '<circle class="agent-track" cx="%.0f" cy="%.0f" r="%.0f"/>' % (cx, cy, R)
            + '<circle class="agent-inner" cx="%.0f" cy="%.0f" r="22"/>' % (cx, cy)
            + comet + nodes + head)
    return svg("dg-agent", "An agent circling plan, run, observe and revise, each stage lighting as it is reached", body)


# ---------------------------------------------------- computer vision
def fig_cv():
    DUR = "7s"
    T0, T1 = 0.06, 0.62
    scene = (
        '<rect class="cv-sky" x="16" y="16" width="188" height="90"/>'
        '<rect class="cv-ground" x="16" y="106" width="188" height="18"/>'
        '<path class="cv-horizon" d="M16 106H204"/>'
        # person
        '<g class="cv-obj"><circle cx="53" cy="56" r="6.6"/>'
        '<rect x="45.5" y="64" width="15" height="25" rx="6.5"/>'
        '<rect x="46.5" y="84" width="5.4" height="22" rx="2.7"/>'
        '<rect x="54.1" y="84" width="5.4" height="22" rx="2.7"/></g>'
        # cone
        '<g class="cv-obj"><path d="M93.6 87h4.8l4.4 17h-13.6z"/><rect x="87" y="103" width="18" height="3.4" rx="1"/></g>'
        # car
        '<g class="cv-obj"><path d="M124 101V91q1-6 9-7l13-1l10-10q2-2 6-2h14q4 0 7 4l7 9q3 2 3 7v10z"/>'
        '<circle cx="139" cy="101" r="6.6"/><circle cx="178" cy="101" r="6.6"/></g>'
        '<g class="cv-glass"><path d="M150 82l8-8q1-1 3-1h6v9z"/><path d="M170 73h6q2 0 3 2l5 7h-14z"/></g>'
    )
    boxes = [(40, 47, 26, 61, 0.97), (84, 82, 24, 26, 0.88), (119, 64, 78, 44, 0.94)]
    det = ""
    for bx, by, bw, bh, conf in boxes:
        t = T0 + (T1 - T0) * ((bx + bw / 2) - 6) / 198
        per = 2 * (bw + bh)
        det += ('<rect class="cv-box" x="%g" y="%g" width="%g" height="%g" stroke-dasharray="%.1f">%s</rect>'
                % (bx, by, bw, bh, per,
                   anim("stroke-dashoffset", ["%.1f" % per, "%.1f" % per, "0", "0"], [0, t, t + 0.07, 1], DUR)))
        det += ('<g>%s<rect class="cv-tab" x="%g" y="%g" width="30" height="9" rx="1.5"/>'
                '<rect class="cv-conf" x="%g" y="%g" height="3" rx="1.5" width="0">%s</rect></g>'
                % (anim("opacity", ["0", "0", "1", "1"], [0, t + 0.04, t + 0.06, 1], DUR),
                   bx, by - 11, bx + 3, by - 8,
                   anim("width", ["0", "0", "%.1f" % (24 * conf), "%.1f" % (24 * conf)],
                        [0, t + 0.05, t + 0.14, 1], DUR)))

    band = ('<rect class="cv-scan" x="0" y="16" width="28" height="108" fill="url(#cvscan)">%s</rect>'
            % '<animateTransform attributeName="transform" type="translate" dur="%s" repeatCount="indefinite"'
              ' keyTimes="%s" values="-10 0;-10 0;190 0;190 0"/>' % (DUR, kts([0, T0, T1, 1])))

    body = (plate()
            + '<defs><linearGradient id="cvscan" x1="0" x2="1" y1="0" y2="0">'
              '<stop offset="0" stop-color="currentColor" stop-opacity="0"/>'
              '<stop offset=".7" stop-color="currentColor" stop-opacity=".28"/>'
              '<stop offset="1" stop-color="currentColor" stop-opacity="0"/></linearGradient>'
              '<clipPath id="cvframe"><rect x="16" y="16" width="188" height="108"/></clipPath></defs>'
            + scene
            + '<g clip-path="url(#cvframe)">' + fade(DUR) + band + det + "</g>"
            + '<rect class="cv-frame" x="16" y="16" width="188" height="108"/>')
    return svg("dg-cv", "A scan crossing a camera frame, drawing a labelled detection around each object it passes", body)


# ------------------------------------------------ robot: writes "Tien"
def _glyph_strokes():
    """Single-line strokes for T, i, e, n in unit glyph space (y down)."""
    T = [[(0.0, 0.0), (0.72, 0.0)], [(0.36, 0.0), (0.36, 1.0)]]
    i = [[(0.14, 0.12), (0.14, 0.17)], [(0.14, 0.38), (0.14, 1.0)]]
    e_arc = [(0.29 + 0.29 * math.cos(math.radians(a)),
              0.69 - 0.31 * math.sin(math.radians(a))) for a in range(0, 301, 15)]
    e = [[(0.0, 0.69), (0.58, 0.69)] + e_arc]
    n = [[(0.0, 0.38), (0.0, 1.0), (0.0, 0.62), (0.06, 0.47), (0.18, 0.39),
          (0.32, 0.38), (0.44, 0.44), (0.49, 0.58), (0.49, 1.0)]]
    out, x = [], 0.0
    for strokes, adv in ((T, 0.84), (i, 0.40), (e, 0.74), (n, 0.6)):
        out += [[(x + px, py) for px, py in st] for st in strokes]
        x += adv
    return out, x


def fig_arm():
    DUR = "11s"
    BX, BY = 110.0, 10.0                         # ceiling mount
    L1, L2, L3 = 60.0, 56.0, 20.0
    S = 36.0
    OY = 84.0

    strokes, width = _glyph_strokes()
    OX = (W - S * width) / 2 + 4                 # centre the word
    strokes = [[(OX + S * x, OY + S * y) for x, y in st] for st in strokes]
    home = (OX + S * width / 2, OY - 10)         # where the pen rests

    # sample the whole run: travel (pen up) and strokes (pen down)
    def dense(a, b, step):
        n = max(1, int(math.dist(a, b) / step))
        return [(a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n) for k in range(1, n + 1)]

    samples = [(home, False)]
    for st in strokes:
        for q in dense(samples[-1][0], st[0], 6.0):
            samples.append((q, False))
        for a_, b_ in zip(st, st[1:]):
            for q in dense(a_, b_, 3.0):
                samples.append((q, True))
    for q in dense(samples[-1][0], home, 6.0):
        samples.append((q, False))

    # time: pen-down at writing speed, pen-up twice as fast
    cost = [0.0]
    for (p, d_), (q, _) in zip(samples, samples[1:]):
        cost.append(cost[-1] + math.dist(p, q) * (1.0 if d_ else 0.5))
    T0, T1 = 0.03, 0.80
    write_end = len(samples) - 1 - len(dense(strokes[-1][-1], home, 6.0))
    # writing occupies T0..T1; the trip home happens during the fade
    tot = cost[write_end]
    times = []
    for k, c in enumerate(cost):
        if k <= write_end:
            times.append(T0 + (T1 - T0) * c / tot)
        else:
            u = (c - cost[write_end]) / (cost[-1] - cost[write_end])
            times.append(0.90 + 0.09 * u)
    times = [0.0] + times + [1.0]
    samples = [samples[0]] + samples + [samples[-1]]

    a1s, a2s, a3s = [], [], []
    for (tx, ty), _ in samples:
        wx, wy = tx, ty - L3                       # gripper points straight down
        dx, dy = wx - BX, wy - BY
        dd = math.hypot(dx, dy)
        c = max(-1.0, min(1.0, (dd * dd + L1 * L1 - L2 * L2) / (2 * L1 * dd)))
        base = math.atan2(dy, dx)
        elb = base - math.acos(c)                  # one branch: elbow out to the side
        ex, ey = BX + L1 * math.cos(elb), BY + L1 * math.sin(elb)
        a2abs = math.atan2(wy - ey, wx - ex)
        a1s.append(elb); a2s.append(a2abs - elb); a3s.append(math.pi / 2 - a2abs)
    tracks = [np.degrees(np.unwrap(np.array(t))) for t in (a1s, a2s, a3s)]

    def rot(track):
        return ('<animateTransform attributeName="transform" type="rotate" dur="%s" repeatCount="indefinite"'
                ' calcMode="linear" keyTimes="%s" values="%s"/>'
                % (DUR, kts(times), ";".join("%.1f" % v for v in track)))

    def link(length, h):
        return ('<rect class="arm-body" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f"/>'
                '<circle class="arm-joint" r="%.1f"/><circle class="arm-pin" r="1.8"/>'
                % (-h / 2, -h / 2, length + h, h, h / 2, h / 2 - 1.3))

    pen = ('<rect class="arm-body" x="-4" y="-4" width="14" height="8" rx="4"/>'
           '<circle class="arm-joint" r="3.4"/>'
           '<path class="arm-pen" d="M10 -3.2 L%.0f 0 L10 3.2 Z"/>' % L3)

    arm = ('<g transform="translate(%g,%g)"><g>%s%s'
           '<g transform="translate(%g,0)"><g>%s%s'
           '<g transform="translate(%g,0)"><g>%s%s</g></g></g></g></g></g>'
           % (BX, BY, rot(tracks[0]), link(L1, 15),
              L1, rot(tracks[1]), link(L2, 12.5),
              L2, rot(tracks[2]), pen))

    # ink: each stroke draws itself while the pen is on it
    ink, cursor = "", 1
    for st in strokes:
        idx = [k for k in range(cursor, len(samples)) if samples[k][1]]
        k0 = idx[0] - 1
        run = [k0]
        k = idx[0]
        while k < len(samples) and samples[k][1]:
            run.append(k); k += 1
        cursor = k
        t0, t1 = times[k0], times[run[-1]]
        L = sum(math.dist(a_, b_) for a_, b_ in zip(st, st[1:]))
        ink += ('<polyline class="arm-ink" points="%s" stroke-dasharray="%.1f %.1f">%s</polyline>'
                % (pts(st), L + 1, L + 1,
                   anim("stroke-dashoffset", ["%.1f" % (L + 1), "%.1f" % (L + 1), "0", "0"],
                        [0, t0, t1, 1], DUR)))

    guide = '<path class="arm-guide" d="M%g %gH%g"/>' % (OX - 4, OY + S + 1, OX + S * width - 6)
    body = (plate()
            + guide
            + "<g>" + fade(DUR, hold_end=0.88, gone=0.95, start=0.0) + ink + "</g>"
            + arm
            + '<path class="arm-base" d="M%g 1h36l-7 12h-22z"/>' % (BX - 18)
            + '<path class="arm-hatch" d="M%g 1.5h52"/>' % (BX - 26))
    return svg("dg-arm", "A ceiling-mounted three-link robot arm writing the word Tien with a pen, stroke by stroke", body)


# ------------------------------------- materials: intergranular crack
def fig_mat():
    DUR = "8s"
    x0, y0, x1, y1 = 1.0, 1.0, W - 1.0, H - 1.0
    rng = np.random.default_rng(23)
    cols, rows = 8, 5
    seeds = []
    for r in range(rows):
        for c in range(cols):
            seeds.append((x0 + (c + 0.5 + rng.uniform(-0.38, 0.38)) * (x1 - x0) / cols,
                          y0 + (r + 0.5 + rng.uniform(-0.38, 0.38)) * (y1 - y0) / rows))
    P = np.array(seeds)
    n = len(P)
    mirrors = [P,
               np.column_stack([2 * x0 - P[:, 0], P[:, 1]]), np.column_stack([2 * x1 - P[:, 0], P[:, 1]]),
               np.column_stack([P[:, 0], 2 * y0 - P[:, 1]]), np.column_stack([P[:, 0], 2 * y1 - P[:, 1]])]
    vor = Voronoi(np.vstack(mirrors))

    grains = ""
    for i in range(n):
        reg = vor.regions[vor.point_region[i]]
        poly = [tuple(vor.vertices[v]) for v in reg]
        grains += ('<polygon class="mat-grain" points="%s" fill-opacity="%.3f"/>'
                   % (pts(poly), 0.06 + 0.24 * rng.random()))

    key = lambda v: (round(float(v[0]), 1), round(float(v[1]), 1))
    graph = {}
    for (a, b), (va, vb) in zip(vor.ridge_points, vor.ridge_vertices):
        if a >= n or b >= n or va < 0 or vb < 0:
            continue
        p, q = key(vor.vertices[va]), key(vor.vertices[vb])
        L = math.dist(p, q)
        cost = L * (1 + 1.6 * abs(p[1] - q[1]) / max(L, 1e-6))
        graph.setdefault(p, []).append((q, cost))
        graph.setdefault(q, []).append((p, cost))

    left = [v for v in graph if abs(v[0] - x0) < 0.6]
    right = {v for v in graph if abs(v[0] - x1) < 0.6}
    start = min(left, key=lambda v: abs(v[1] - 74))
    dist, prev, heap = {start: 0.0}, {}, [(0.0, start)]
    end = None
    while heap:
        dcur, v = heapq.heappop(heap)
        if v in right:
            end = v
            break
        if dcur > dist[v]:
            continue
        for w_, c in graph[v]:
            nd = dcur + c
            if nd < dist.get(w_, 1e18):
                dist[w_], prev[w_] = nd, v
                heapq.heappush(heap, (nd, w_))
    path = [end]
    while path[-1] != start:
        path.append(prev[path[-1]])
    path.reverse()
    d = "M" + " L".join("%.1f %.1f" % p for p in path)

    T0, T1 = 0.08, 0.72
    crack = ('<path class="mat-crack" d="%s" pathLength="1" stroke-dasharray="1 1">%s</path>'
             % (d, anim("stroke-dashoffset", ["1", "1", "0", "0"], [0, T0, T1, 1], DUR)))
    tip = ('<circle class="mat-tip" r="3.4"><animateMotion dur="%s" repeatCount="indefinite"'
           ' calcMode="linear" keyTimes="0;%.2f;%.2f;1" keyPoints="0;0;1;1" path="%s"/>%s</circle>'
           % (DUR, T0, T1, d, anim("opacity", ["0", "1", "1", "0", "0"], [0, T0, T1, T1 + 0.04, 1], DUR)))

    body = (plate()
            + '<defs><clipPath id="matclip"><rect x="1" y="1" width="%g" height="%g" rx="1"/></clipPath></defs>'
              % (W - 2, H - 2)
            + '<g clip-path="url(#matclip)">' + grains
            + "<g>" + fade(DUR, start=0.0) + crack + tip + "</g></g>")
    return svg("dg-mat", "A crack running along the grain boundaries of a polycrystal from one edge to the other", body)


# ---------------------------------------- structural health monitoring
def fig_shm():
    DUR = "9s"
    XA, XB, BEAM = 26.0, 194.0, 44.0
    NB = 15
    M = 48
    TD = 0.45                                   # damage appears
    f1, f2 = 5.2, 3.6                           # cycles per timeline before / after

    phase, ph = [], 0.0
    for i in range(M + 1):
        t = i / M
        phase.append(ph)
        fr = f1 if t < TD else f1 + (f2 - f1) * ease((t - TD) / 0.12)
        ph += 2 * math.pi * fr / M
    amp = [11 * math.cos(p) for p in phase]
    times = [i / M for i in range(M + 1)]

    xs = [XA + (XB - XA) * j / (NB - 1) for j in range(NB)]
    shape = lambda s: math.sin(math.pi * s)
    frames = [pts([(x, BEAM - a * shape(j / (NB - 1))) for j, x in enumerate(xs)]) for a in amp]
    beam = '<polyline class="shm-beam" points="%s">%s</polyline>' % (frames[0], anim("points", frames, times, DUR))

    sensors = ""
    for s in (0.25, 0.5, 0.75):
        x = XA + (XB - XA) * s
        ys = ["%.1f" % (BEAM - 7 - a * shape(s)) for a in amp]
        sensors += ('<rect class="shm-sensor" x="%.1f" width="7" height="6" y="%s" rx="1">%s</rect>'
                    % (x - 3.5, ys[0], anim("y", ys, times, DUR)))

    sc = 0.68
    dmg_y = ["%.1f" % (-a * shape(sc)) for a in amp]
    damage = ('<g><animateTransform attributeName="transform" type="translate" dur="%s" repeatCount="indefinite"'
              ' keyTimes="%s" values="%s"/>%s<path class="shm-crack" d="M%.1f %.1fl3 4-3 3 3 4"/>'
              '<circle class="shm-ring" cx="%.1f" cy="%.1f" r="9"/></g>'
              % (DUR, kts(times), ";".join("0 " + v for v in dmg_y),
                 anim("opacity", ["0", "0", "1", "1"], [0, TD, TD + 0.03, 1], DUR),
                 XA + (XB - XA) * sc - 1.5, BEAM - 5.5, XA + (XB - XA) * sc, BEAM))

    SX0, SX1, SB = 26.0, 194.0, 128.0
    def spectrum(fc, hgt):
        out = []
        for j in range(44):
            x = SX0 + (SX1 - SX0) * j / 43
            out.append((x, SB - hgt / (1 + ((x - fc) / 9.0) ** 2)))
        return out
    healthy, damaged = spectrum(140, 32), spectrum(102, 27)
    fill = lambda sp: pts(sp + [(SX1, SB), (SX0, SB)])
    st = [0, TD + 0.02, TD + 0.16, 1]
    curve = ('<polyline class="shm-spec" points="%s">%s</polyline>'
             % (pts(healthy), anim("points", [pts(healthy), pts(healthy), pts(damaged), pts(damaged)], st, DUR)))
    area = ('<polygon class="shm-area" points="%s">%s</polygon>'
            % (fill(healthy), anim("points", [fill(healthy), fill(healthy), fill(damaged), fill(damaged)], st, DUR)))
    shift = ('<g>%s<path class="shm-shift" d="M138 90H106M110 86.5l-4 3.5 4 3.5"/></g>'
             % anim("opacity", ["0", "0", "1", "1"], [0, TD + 0.16, TD + 0.2, 1], DUR))

    body = (plate()
            + '<path class="shm-support" d="M%.0f %.0fl-6 10h12z M%.0f %.0fl-6 10h12z"/>' % (XA, BEAM + 2, XB, BEAM + 2)
            + '<path class="shm-axis" d="M%g %gH%g"/>' % (SX0, SB, SX1)
            + '<polyline class="shm-ref" points="%s"/>' % pts(healthy)
            + "<g>" + fade(DUR, hold_end=0.9, gone=0.97) + area + curve + shift
            + beam + sensors + damage + "</g>")
    return svg("dg-shm", "A vibrating beam develops a crack and its resonance peak shifts to a lower frequency", body)
