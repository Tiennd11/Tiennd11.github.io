"""Generate the eight research-interest figures as inline SVG.

Writes the whole <div class="interests"> block so index.html can be spliced
in one go. Geometry is computed rather than eyeballed: the arm poses are
real IK, the hex lattice really tiles, the attention band really is causal.
"""
import math

W, H = 220, 140

def rnd(seed):
    s = seed & 0xFFFFFFFF
    def nxt():
        nonlocal s
        s = (s * 1664525 + 1013904223) & 0xFFFFFFFF
        return s / 0x100000000
    return nxt

def plate():
    return '<rect class="dg-plate" x=".5" y=".5" width="%g" height="%g"/>' % (W - 1, H - 1)

def svg(cls, label, body):
    return (
        '<svg class="dg %s" viewBox="0 0 %d %d" role="img" aria-label="%s">\n      %s\n    </svg>'
        % (cls, W, H, label, body)
    )

# ---------------------------------------------------------------- 1. LLM
def fig_llm():
    cols, rows, cell = 11, 6, 16
    x0, y0 = 22, 22
    r = rnd(7)
    cells = []
    for i in range(rows):
        for j in range(cols):
            if j > i + 5:                      # causal mask
                continue
            near = 1.0 - abs((i + 5) - j) / 10.0
            op = 0.07 + 0.62 * near * (0.45 + 0.55 * r())
            cells.append(
                '<rect x="%g" y="%g" width="%g" height="%g" fill-opacity="%.2f"/>'
                % (x0 + j * cell + 0.6, y0 + i * cell + 0.6, cell - 1.2, cell - 1.2, op)
            )
    keys = "".join(
        '<rect x="%g" y="11" width="%g" height="5"/>' % (x0 + j * cell + 1.5, cell - 3)
        for j in range(cols)
    )
    qrys = "".join(
        '<rect x="12" y="%g" width="5" height="%g"/>' % (y0 + i * cell + 1.5, cell - 3)
        for i in range(rows)
    )
    body = (
        plate()
        + '<g class="dg-fill cells">' + "".join(cells) + "</g>"
        + '<g class="dg-faintfill">' + keys + qrys + "</g>"
        + '<rect class="row dg-acc" x="%g" y="%g" width="%g" height="%g" rx="1"/>'
          % (x0 - 1, y0 - 1, cols * cell + 2, cell + 2)
    )
    return svg("dg-llm", "A causal attention map, one query row highlighted at a time", body)

# -------------------------------------------------------------- 2. agent
def fig_agent():
    cx, cy, R = 110, 70, 44
    P = lambda a: (cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a)))
    arcs = []
    for a1, a2 in [(-72, -18), (18, 72), (108, 162), (198, 252)]:
        x1, y1 = P(a1)
        x2, y2 = P(a2)
        arcs.append('<path d="M%.1f %.1f A %d %d 0 0 1 %.1f %.1f" marker-end="url(#ah)"/>'
                    % (x1, y1, R, R, x2, y2))

    nodes = ""
    for a in (-90, 0, 90, 180):
        x, y = P(a)
        nodes += '<circle cx="%.0f" cy="%.0f" r="13"/>' % (x, y)

    glyphs = (
        '<path d="M104 25h12M104 29h12M104 33h8"/>'            # plan
        '<path d="M151 64l8 6-8 6z" fill="currentColor"/>'      # run
        '<circle cx="110" cy="114" r="5"/><circle cx="110" cy="114" r="1.6" fill="currentColor"/>'
        '<path d="M72 65a7 7 0 1 0-6 9"/><path d="M69 71l-3 3 4 2"/>'   # revise
    )

    body = (
        plate()
        + '<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5"'
          ' markerHeight="5" orient="auto-start-reverse">'
          '<path d="M0 1l8 4-8 4z" fill="currentColor"/></marker></defs>'
        + '<g class="dg-loop">' + "".join(arcs) + "</g>"
        + '<g class="dg-node">' + nodes + "</g>"
        + '<g class="dg-glyph">' + glyphs + "</g>"
        + '<g class="orbit"><circle class="dg-fill" cx="%d" cy="%d" r="5.5"/></g>' % (cx, cy - R)
    )
    return svg("dg-agent", "An agent circling a plan, run, observe and revise loop", body)

# ----------------------------------------------------------------- 3. CV
def fig_cv():
    grid = "".join('<path d="M16 %dh188"/>' % y for y in range(34, 124, 18))
    grid += "".join('<path d="M%d 16v108"/>' % x for x in range(42, 204, 26))

    # three abstract things in the scene: a person, a crate, a vehicle
    scene = (
        '<rect x="44" y="70" width="20" height="40" rx="9"/><circle cx="54" cy="59" r="9"/>'
        '<rect x="97" y="79" width="37" height="29" rx="2"/>'
        '<rect x="155" y="80" width="38" height="17" rx="5"/>'
        '<path d="M160 76h20l7 5h-34z"/>'
        '<circle cx="164" cy="99" r="5"/><circle cx="184" cy="99" r="5"/>'
    )

    boxes = [(38, 46, 33, 68), (91, 73, 50, 41), (149, 70, 50, 36)]

    def det(i, x, y, w, h):
        c = 8
        br = ("M%g %gV%gh%g M%g %gh%g v%g M%g %gv%g h-%g M%g %gh-%g v-%g"
              % (x, y + c, y, c, x + w - c, y, c, c,
                 x + w, y + h - c, c, c, x + w - c, y + h, c, c))
        br = ("M%g %gV%gh%g" % (x, y + c, y, c)
              + "M%g %gh%gv%g" % (x + w - c, y, c, c)
              + "M%g %gv%gh-%g" % (x + w, y + h - c, c, c)
              + "M%g %gh-%gv-%g" % (x + w - c, y + h, c, c))
        return ('<g class="det d%d">'
                '<rect class="dg-tint" x="%g" y="%g" width="%g" height="%g"/>'
                '<path class="dg-acc" d="%s"/>'
                '<rect class="dg-fill" x="%g" y="%g" width="24" height="8"/>'
                "</g>" % (i, x, y, w, h, br, x, y - 10))

    body = (
        plate()
        + '<defs><linearGradient id="scang" x1="0" y1="0" x2="0" y2="1">'
          '<stop offset="0" stop-color="currentColor" stop-opacity="0"/>'
          '<stop offset=".5" stop-color="currentColor" stop-opacity=".26"/>'
          '<stop offset="1" stop-color="currentColor" stop-opacity="0"/>'
          "</linearGradient></defs>"
        + '<rect class="dg-tint-2" x="16" y="16" width="188" height="108"/>'
        + '<g class="dg-hair">' + grid + "</g>"
        + '<g class="dg-scene">' + scene + "</g>"
        + '<g class="dg-ghostbox">'
        + "".join('<rect x="%g" y="%g" width="%g" height="%g"/>' % b for b in boxes)
        + "</g>"
        + "".join(det(i + 1, *b) for i, b in enumerate(boxes))
        + '<rect class="scan" x="16" y="0" width="188" height="22" fill="url(#scang)"/>'
        + '<rect class="dg-ink" x="16" y="16" width="188" height="108"/>'
    )
    return svg("dg-cv", "A scan crossing a camera frame while detections lock onto each object in turn", body)

# --------------------------------------------------------------- 4. PINN
def fig_pinn():
    """A PINN training run, start to finish.

    The network's prediction (solid) starts far from the exact solution
    (dashed) and converges onto it; the error area between them shrinks
    to nothing, the collocation points ride the prediction, and the
    residual strip underneath collapses in step. All of it is one SMIL
    timeline, so it pauses and resumes together.
    """
    X0, X1 = 16.0, 204.0          # plot span
    MID, AMP = 56.0, 34.0         # u(x) axis
    STRIP = 128.0                 # residual strip baseline
    N = 48                        # samples along the curves
    NC = 11                       # collocation points
    DUR = "7s"

    def exact(s):
        return 0.82 * math.sin(2 * math.pi * s) + 0.22 * math.sin(5 * math.pi * s)

    def guess(s):                 # an untrained network: nearly flat, wrong
        return 0.18 * math.sin(math.pi * s) - 0.28

    K = 18                        # keyframes in the converging phase
    # ease in and out, so the wrong start and the converged end both read
    ws = [0.5 - 0.5 * math.cos(math.pi * k / (K - 1)) for k in range(K)]

    def pred(s, w):
        return guess(s) * (1 - w) + exact(s) * w

    X = lambda s: X0 + (X1 - X0) * s
    Y = lambda u: MID - AMP * u
    ss = [i / (N - 1) for i in range(N)]
    fmt = lambda pts: " ".join("%.1f,%.1f" % p for p in pts)

    exact_pts = [(X(s), Y(exact(s))) for s in ss]
    pred_frames = [[(X(s), Y(pred(s, w))) for s in ss] for w in ws]
    err_frames = [fmt(f + exact_pts[::-1]) for f in pred_frames]

    # timeline: hold the untrained guess, converge over 0.10..0.72,
    # hold the solution, fade out, restart
    conv = [0.10 + 0.62 * k / (K - 1) for k in range(K)]
    kt = [0.0] + conv + [0.9, 1.0]
    def track(frames):
        return ";".join([frames[0]] + frames + [frames[-1], frames[-1]])
    keytimes = ";".join("%.4f" % t for t in kt)

    def anim(attr, frames):
        return ('<animate attributeName="%s" dur="%s" repeatCount="indefinite"'
                ' calcMode="linear" keyTimes="%s" values="%s"/>'
                % (attr, DUR, keytimes, track(frames)))

    cs = [0.04 + 0.92 * i / (NC - 1) for i in range(NC)]
    dots, bars = "", ""
    for s in cs:
        cy = ["%.1f" % Y(pred(s, w)) for w in ws]
        r = [abs(pred(s, w) - exact(s)) for w in ws]
        h = ["%.1f" % max(0.8, 20 * v) for v in r]
        y = ["%.1f" % (STRIP - max(0.8, 20 * v)) for v in r]
        dots += ('<circle class="pinn-dot" cx="%.1f" cy="%s" r="3.2">%s</circle>'
                 % (X(s), cy[0], anim("cy", cy)))
        bars += ('<rect class="pinn-bar" x="%.1f" y="%s" width="5" height="%s">%s%s</rect>'
                 % (X(s) - 2.5, y[0], h[0], anim("y", y), anim("height", h)))

    fade = ('<animate attributeName="opacity" dur="%s" repeatCount="indefinite"'
            ' keyTimes="0;0.02;0.88;0.96;1" values="0;1;1;0;0"/>' % DUR)

    body = (
        plate()
        + '<path class="pinn-axis" d="M%g %gH%g"/>' % (X0, MID, X1)
        + '<path class="pinn-axis" d="M%g %gH%g"/>' % (X0, STRIP, X1)
        + '<polyline class="pinn-exact" points="%s"/>' % fmt(exact_pts)
        + '<g class="pinn-run">' + fade
        + '<polygon class="pinn-err" points="%s">%s</polygon>' % (err_frames[0], anim("points", err_frames))
        + '<polyline class="pinn-pred" points="%s">%s</polyline>'
          % (fmt(pred_frames[0]), anim("points", [fmt(f) for f in pred_frames]))
        + dots + bars
        + "</g>"
    )
    return svg("dg-pinn", "A physics-informed network converging onto the exact solution while its residuals shrink to zero", body)

# ---------------------------------------------------------------- 5. arm
def two_link(px, py, qx, qy, a, b, up=True):
    dx, dy = qx - px, qy - py
    dist = math.hypot(dx, dy)
    if dist > a + b or dist < abs(a - b) or dist == 0:
        return None
    ca = max(-1.0, min(1.0, (dist * dist + a * a - b * b) / (2 * a * dist)))
    th = math.atan2(dy, dx) + (math.acos(ca) if up else -math.acos(ca))
    return px + a * math.cos(th), py + a * math.sin(th)

def arm_poses():
    BX, BY = 30.0, 118.0
    TX, TY = 186.0, 36.0
    L1, L2, L3 = 78.0, 70.0, 55.0
    out = []
    N = 14
    for i in range(N):
        u = i / (N - 1)
        s = 0.5 - 0.5 * math.cos(math.pi * u)
        th1 = math.radians(16) + math.radians(60) * s
        ex, ey = BX + L1 * math.cos(th1), L1 * math.sin(th1)
        sol = two_link(ex, ey, TX, BY - TY, L2, L3, up=False)
        if sol is None:
            continue
        wx, wy = sol
        out.append([(BX, 0.0), (ex, ey), (wx, wy), (TX, BY - TY)])
    return [[(x, BY - y) for x, y in p] for p in out]

def fig_arm():
    """Draw the arm as real link bodies rotating about real joints.

    The IK solves for joint positions; those are converted back to joint
    ANGLES so each link can be a shaped body inside a nested rotation
    group, instead of a bare polyline.
    """
    poses = arm_poses()
    seq = poses + poses[-2:0:-1]
    L = (78.0, 70.0, 55.0)
    BX, BY = 30.0, 118.0
    DUR = "8s"

    def angles(p):
        out, prev = [], 0.0
        for k in range(3):
            (x1, y1), (x2, y2) = p[k], p[k + 1]
            a = math.degrees(math.atan2(y2 - y1, x2 - x1))
            out.append(a - prev)
            prev = a
        return out

    tracks = [[], [], []]
    for p in seq:
        for k, a in enumerate(angles(p)):
            tracks[k].append("%.2f" % a)

    def anim(k):
        return ('<animateTransform attributeName="transform" type="rotate" dur="%s"'
                ' repeatCount="indefinite" calcMode="linear" values="%s"/>'
                % (DUR, ";".join(tracks[k])))

    def link(i, length, h):
        """One capsule body plus the joint it pivots on."""
        return (
            '<rect class="dg-body" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f"/>'
            '<circle class="dg-joint" cx="0" cy="0" r="%.1f"/>'
            '<circle class="dg-pin" cx="0" cy="0" r="1.7"/>'
            % (-h / 2, -h / 2, length + h, h, h / 2, h / 2 - 1.2)
        )

    gripper = (
        '<g class="dg-grip">'
        '<path d="M%.0f -3.5v-5l8-3M%.0f 3.5v5l8 3" />'
        '<path d="M%.0f -8.5h3M%.0f 8.5h3"/>'
        "</g>" % (L[2], L[2], L[2] + 8, L[2] + 8)
    )

    arm = (
        '<g transform="translate(%g,%g)">'
        '<g class="j1">%s%s'
        '<g transform="translate(%g,0)"><g class="j2">%s%s'
        '<g transform="translate(%g,0)"><g class="j3">%s%s%s'
        "</g></g></g></g></g></g>"
        % (BX, BY,
           anim(0), link(0, L[0], 15),
           L[0], anim(1), link(1, L[1], 12.5),
           L[1], anim(2), link(2, L[2], 10), gripper)
    )

    fmt = lambda p: " ".join("%.1f,%.1f" % (x, y) for x, y in p)
    ghosts = "".join('<polyline points="%s"/>' % fmt(poses[i])
                     for i in (0, len(poses) - 1))

    body = (
        plate()
        + '<g class="dg-ghostline">' + ghosts + "</g>"
        + '<g class="target"><circle class="dg-ring" cx="186" cy="36" r="11"/>'
          '<path class="dg-acc" d="M170 36h32M186 20v32"/></g>'
        + arm
        + '<path class="dg-solid" d="M14 134h32l-9-18h-14z"/>'
        + '<path class="dg-hatch" d="M10 137h40M14 141l5-7M24 141l5-7M34 141l5-7M44 141l5-7"/>'
        + '<circle class="dg-fill" cx="186" cy="36" r="3.6"/>'
    )
    return svg("dg-arm", "A redundant three-link arm sweeping its null space while the gripper stays on target", body)

# ----------------------------------------------------------- 6. materials
def fig_mat():
    r = 20.0
    hw = 0.8660254 * r
    pts = " ".join("%.1f,%.1f" % (hw * dx, r * dy) for dx, dy in
                   [(0, -1), (1, -0.5), (1, 0.5), (0, 1), (-1, 0.5), (-1, -0.5)])
    rand = rnd(31)
    uses = []
    for row, y in enumerate((24, 54, 84, 114)):
        off = 0 if row % 2 == 0 else hw
        x = 20.0 + off
        while x < W + hw:
            delay = (x - 6) / 200.0 * 3.6
            base = 0.05 + 0.11 * rand()
            uses.append('<use href="#hx" x="%.1f" y="%d" fill-opacity="%.3f"'
                        ' style="--o:%.3f;--d:%.2fs"/>'
                        % (x, y, base, base, max(0.0, delay)))
            x += 2 * hw
    body = (
        plate()
        + '<defs><polygon id="hx" points="%s"/>'
          '<clipPath id="matclip"><rect x="1" y="1" width="%g" height="%g"/></clipPath></defs>' % (pts, W - 2, H - 2)
        + '<g class="grains" clip-path="url(#matclip)">' + "".join(uses) + "</g>"
        + '<line class="sweep" x1="0" y1="1" x2="0" y2="%g" clip-path="url(#matclip)"/>' % (H - 1)
    )
    return svg("dg-mat", "A scan crossing a grain microstructure, lighting each grain as it passes", body)

# ----------------------------------------------------------------- 7. SHM
def fig_shm():
    body = (
        plate()
        + '<path class="mode" d="M26 76 Q110 20 194 76" vector-effect="non-scaling-stroke"/>'
        + '<rect class="dg-solid" x="26" y="76" width="168" height="5"/>'
        + '<path class="dg-solid" d="M26 81h22l-11 16zM172 81h22l-11 16z"/>'
        + '<path class="dg-hatch" d="M22 100h34M168 100h34M26 104l-4 6M34 104l-4 6M42 104l-4 6M50 104l-4 6'
          'M172 104l-4 6M180 104l-4 6M188 104l-4 6M196 104l-4 6"/>'
        + '<g class="dg-solid sensors">'
          '<rect x="56" y="68" width="9" height="8"/><rect x="105" y="68" width="9" height="8"/>'
          '<rect x="154" y="68" width="9" height="8"/></g>'
        + '<g class="dg-hair"><path d="M60.5 68V56M109.5 68V56M158.5 68V56"/></g>'
        + '<g class="crack"><path d="M150 72l5 7-4 5 5 7"/><circle cx="153" cy="79" r="13"/></g>'
    )
    return svg("dg-shm", "A beam vibrating in its first mode with sensors mounted and a damage site marked", body)

# ------------------------------------------------------------------ 8. UQ
def fig_uq():
    mean = 70
    band = lambda a, b: "M20 %g L200 %g L200 %g L20 %g Z" % (mean - a, mean - b, mean + b, mean + a)
    rand = rnd(5)
    obs = []
    for i in range(11):
        x = 24 + i * 17.2
        spread = 4 + 38 * ((x - 20) / 180.0) ** 1.4
        obs.append('<circle cx="%.0f" cy="%.1f" r="3.4"/>' % (x, mean + (rand() - 0.5) * spread))
    body = (
        plate()
        + '<path class="band b2" d="%s"/>' % band(7, 48)
        + '<path class="band b1" d="%s"/>' % band(3.5, 24)
        + '<path class="dg-ink2" d="M20 %d h180"/>' % mean
        + '<g class="obs">' + "".join(obs) + "</g>"
    )
    return svg("dg-uq", "A predictive interval widening to the right around a mean, with scattered observations", body)

# ------------------------------------------------------------------ build
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs_story import fig_uq, fig_llm, fig_agent, fig_cv, fig_arm, fig_mat, fig_shm  # story versions

METHODS = [
    (fig_pinn, "Physics-informed learning",
     "Putting the governing equation in the loss. Physics-informed networks and neural "
     "operators for PDEs with discontinuities, multiple domains, and multi-scale structure."),
    (fig_uq, "Uncertainty quantification",
     "Heteroscedastic Gaussian processes and ensembles for problems where the noise "
     "itself changes across the input space, not just the prediction."),
    (fig_llm, "Large language models",
     "Transformer models and retrieval-augmented pipelines pointed at engineering "
     "literature and data, where an answer is only useful if it can be checked "
     "against its source."),
    (fig_agent, "Agentic AI for science",
     "Systems that run their own loop — proposing a hypothesis space for sparse "
     "system discovery, testing it, and revising, instead of waiting to be handed one."),
]

APPLIED = [
    (fig_cv, "Computer vision",
     "Reading images and video as measurements: microstructure images that predict "
     "material properties, and camera pipelines that return numbers rather than labels."),
    (fig_arm, "Robot learning and control",
     "Inverse kinematics for redundant manipulators as set prediction, sparse regression "
     "for multibody dynamics, and disturbance-rejecting control for nonlinear arms."),
    (fig_mat, "Materials science",
     "Nonlinear behaviour of nanocomposite plates and shells, and data-driven design "
     "that searches a composition space instead of enumerating it."),
    (fig_shm, "Structural health monitoring",
     "Vibration signatures read as a diagnostic: what a shift in the mode shape says "
     "about where damage sits and how far it has grown."),
]

_UNUSED = [
    (fig_llm, "Large language models",
     "Transformer models and retrieval-augmented pipelines pointed at engineering "
     "literature and data, where an answer is only useful if it can be checked "
     "against its source."),
    (fig_agent, "Agentic AI for science",
     "Systems that run their own loop — proposing a hypothesis space for sparse "
     "system discovery, testing it, and revising, instead of waiting to be handed one."),
    (fig_cv, "Computer vision",
     "Reading images and video as measurements: microstructure images that predict "
     "material properties, and camera pipelines that return numbers rather than labels."),
    (fig_pinn, "Physics-informed learning",
     "Putting the governing equation in the loss. Physics-informed networks and neural "
     "operators for PDEs with discontinuities, multiple domains, and multi-scale structure."),
    (fig_arm, "Robot learning and control",
     "Inverse kinematics for redundant manipulators as set prediction, sparse regression "
     "for multibody dynamics, and disturbance-rejecting control for nonlinear arms."),
    (fig_mat, "Materials science",
     "Nonlinear behaviour of nanocomposite plates and shells, and data-driven design "
     "that searches a composition space instead of enumerating it."),
    (fig_shm, "Structural health monitoring",
     "Vibration signatures read as a diagnostic: what a shift in the mode shape says "
     "about where damage sits and how far it has grown."),
    (fig_uq, "Uncertainty quantification",
     "Heteroscedastic Gaussian processes and ensembles for problems where the noise "
     "itself changes across the input space, not just the prediction."),
]

def grid(cards):
    out = ['    <div class="interests grid-4">']
    for fn, title, text in cards:
        out.append('      <article class="int card">')
        out.append('        <div class="dgwrap">')
        out.append("          " + fn())
        out.append("        </div>")
        out.append("        <h3>%s</h3>" % title)
        out.append("        <p>%s</p>" % text)
        out.append("      </article>\n")
    out.append("    </div>")
    return "\n".join(out)

def group(heading, note, cards):
    out = ['    <h3 class="sub">%s <span class="subnote">%s</span></h3>' % (heading, note)]
    out.append('    <div class="interests">')
    for fn, title, text in cards:
        out.append('      <article class="int">')
        out.append('        <div class="dgwrap">')
        out.append("          " + fn())
        out.append("        </div>")
        out.append("        <h4>%s</h4>" % title)
        out.append("        <p>%s</p>" % text)
        out.append("      </article>\n")
    out.append("    </div>\n")
    return "\n".join(out)

frag = "\n".join([
    '    <div class="bandhead">',
    '      <h2>Research interests</h2>',
    '      <p class="section-lede">One question runs through all of it: how do you put physics',
    '      inside a learning system so that it generalises, converges, and can be trusted on',
    '      problems where data is expensive and the governing equations are already known?</p>',
    '    </div>\n',
    grid(METHODS + APPLIED),
])

with open("interests.html", "w", encoding="utf-8") as f:
    f.write(frag)

print("wrote interests.html,", len(frag), "chars")
