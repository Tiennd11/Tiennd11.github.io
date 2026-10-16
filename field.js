/* ==================================================================
   Hero field.

   Draws isolines of a superposition of bending modes on a rectangular
   plate,  w(x,y,t) = Σ aₖ sin(mₖπx) sin(nₖπy) cos(ωₖt + φₖ),  with a
   scatter of collocation points on top. Contours are extracted with
   marching squares on a uniform grid.

   The mode shapes are separable, so sin(mπx) and sin(nπy) are tabulated
   once per resize and only the five cos(ωt) factors change per frame.
   ================================================================== */

(function () {
  "use strict";

  const cv = document.getElementById("field");
  if (!cv || !cv.getContext) return;

  const ctx = cv.getContext("2d", { alpha: true });
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* mf / nf are relative wavenumbers. The actual mode numbers are picked
     from the canvas size at layout time so a contour cell stays about the
     same number of pixels whether the hero is wide or tall. */
  const CELL = 190;
  const MODES = [
    { mf: 0.55, nf: 0.55, a: 1.00, w: 0.052, p: 0.0 },
    { mf: 0.85, nf: 0.50, a: 0.82, w: 0.081, p: 1.3 },
    { mf: 0.50, nf: 0.85, a: 0.74, w: 0.069, p: 2.4 },
    { mf: 1.15, nf: 0.80, a: 0.60, w: 0.110, p: 0.7 },
    { mf: 0.80, nf: 1.15, a: 0.52, w: 0.127, p: 3.1 },
    { mf: 1.40, nf: 1.25, a: 0.36, w: 0.151, p: 1.9 }
  ];

  /* Contour levels as a fraction of the current peak deflection, so the
     plot stays evenly filled as the modes beat against each other. */
  const LEVELS = [];
  for (let L = -0.94; L <= 0.95; L += 0.105) LEVELS.push(L);

  const STEP = 14;          // target grid spacing, css px
  const FRAME = 1000 / 30;  // cap at 30fps — this is background texture

  let W = 0, H = 0, dpr = 1;
  let cols = 0, rows = 0, cw = 0, ch = 0;
  let SX = [], SY = [], vals = null;
  let pts = [];
  let cNeg = "#0072B2", cPos = "#D55E00", cDot = "#0E1B26", baseAlpha = 0.3;

  /* deterministic scatter, so the layout never jumps between reloads */
  function rng(seed) {
    let s = seed >>> 0;
    return function () {
      s = (s * 1664525 + 1013904223) >>> 0;
      return s / 4294967296;
    };
  }

  function readTheme() {
    const cs = getComputedStyle(document.documentElement);
    const get = (n, f) => (cs.getPropertyValue(n) || "").trim() || f;
    cNeg = get("--blue", "#0072B2");
    cPos = get("--vermilion", "#D55E00");
    cDot = get("--ink", "#0E1B26");
    baseAlpha = window.matchMedia("(prefers-color-scheme: dark)").matches ? 0.38 : 0.27;
  }

  function resize() {
    const r = cv.getBoundingClientRect();
    if (!r.width || !r.height) return false;

    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = r.width;
    H = r.height;
    cv.width = Math.round(W * dpr);
    cv.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    cols = Math.max(12, Math.round(W / STEP));
    rows = Math.max(10, Math.round(H / STEP));
    cw = W / cols;
    ch = H / rows;

    const mOf = (f) => Math.max(1, Math.round(f * W / CELL));
    const nOf = (f) => Math.max(1, Math.round(f * H / CELL));

    SX = MODES.map((k) => {
      const m = mOf(k.mf);
      const row = new Float32Array(cols + 1);
      for (let i = 0; i <= cols; i++) row[i] = Math.sin(m * Math.PI * (i / cols));
      return row;
    });
    SY = MODES.map((k) => {
      const n = nOf(k.nf);
      const col = new Float32Array(rows + 1);
      for (let j = 0; j <= rows; j++) col[j] = Math.sin(n * Math.PI * (j / rows));
      return col;
    });

    vals = new Float32Array((cols + 1) * (rows + 1));

    const rand = rng(20250614);
    const n = Math.round((W * H) / 13000);
    pts = [];
    for (let i = 0; i < n; i++) {
      pts.push([0.03 + rand() * 0.94, 0.05 + rand() * 0.9]);
    }
    return true;
  }

  function sample(t) {
    const amp = MODES.map((k) => k.a * Math.cos(k.w * t + k.p));
    const stride = cols + 1;
    let peak = 1e-6;
    for (let j = 0; j <= rows; j++) {
      for (let i = 0; i <= cols; i++) {
        let v = 0;
        for (let k = 0; k < MODES.length; k++) v += amp[k] * SX[k][i] * SY[k][j];
        vals[j * stride + i] = v;
        const m = v < 0 ? -v : v;
        if (m > peak) peak = m;
      }
    }
    return peak;
  }

  /* marching squares, one level at a time */
  function contour(level) {
    const stride = cols + 1;
    ctx.beginPath();

    for (let j = 0; j < rows; j++) {
      for (let i = 0; i < cols; i++) {
        const o = j * stride + i;
        const tl = vals[o], tr = vals[o + 1];
        const bl = vals[o + stride], br = vals[o + stride + 1];

        let idx = 0;
        if (tl > level) idx |= 8;
        if (tr > level) idx |= 4;
        if (br > level) idx |= 2;
        if (bl > level) idx |= 1;
        if (idx === 0 || idx === 15) continue;

        const x0 = i * cw, y0 = j * ch, x1 = x0 + cw, y1 = y0 + ch;
        const lerp = (a, b) => (level - a) / (b - a || 1e-9);

        const top    = () => [x0 + cw * lerp(tl, tr), y0];
        const right  = () => [x1, y0 + ch * lerp(tr, br)];
        const bottom = () => [x0 + cw * lerp(bl, br), y1];
        const left   = () => [x0, y0 + ch * lerp(tl, bl)];

        let seg;
        switch (idx) {
          case 1: case 14: seg = [left(), bottom()]; break;
          case 2: case 13: seg = [bottom(), right()]; break;
          case 3: case 12: seg = [left(), right()]; break;
          case 4: case 11: seg = [top(), right()]; break;
          case 6: case 9:  seg = [top(), bottom()]; break;
          case 7: case 8:  seg = [top(), left()]; break;
          case 5:  ctx.moveTo(top()[0], top()[1]);    ctx.lineTo(left()[0], left()[1]);
                   ctx.moveTo(bottom()[0], bottom()[1]); ctx.lineTo(right()[0], right()[1]);
                   continue;
          case 10: ctx.moveTo(top()[0], top()[1]);    ctx.lineTo(right()[0], right()[1]);
                   ctx.moveTo(left()[0], left()[1]);  ctx.lineTo(bottom()[0], bottom()[1]);
                   continue;
          default: continue;
        }
        ctx.moveTo(seg[0][0], seg[0][1]);
        ctx.lineTo(seg[1][0], seg[1][1]);
      }
    }
    ctx.stroke();
  }

  function draw(t) {
    const peak = sample(t);
    ctx.clearRect(0, 0, W, H);
    ctx.lineWidth = 1;
    ctx.lineCap = "round";

    for (let i = 0; i < LEVELS.length; i++) {
      const L = LEVELS[i];
      // inner contours read stronger, outer ones fade — as on a field plot
      ctx.strokeStyle = L < 0 ? cNeg : cPos;
      ctx.globalAlpha = baseAlpha * (1 - Math.abs(L) * 0.4);
      contour(L * peak);
    }

    ctx.globalAlpha = baseAlpha * 0.75;
    ctx.fillStyle = cDot;
    for (let i = 0; i < pts.length; i++) {
      ctx.fillRect(Math.round(pts[i][0] * W) - 1, Math.round(pts[i][1] * H) - 1, 2, 2);
    }
    ctx.globalAlpha = 1;
  }

  /* ------------------------------------------------------- driving */

  let raf = 0, last = 0, t0 = 0, visible = true, ready = false, tries = 0;

  function loop(now) {
    raf = requestAnimationFrame(loop);
    if (now - last < FRAME) return;
    last = now;
    if (!t0) t0 = now;
    draw((now - t0) / 1000);
  }

  function start() {
    if (!ready || raf || reduced || !visible || document.hidden) return;
    last = 0;
    raf = requestAnimationFrame(loop);
  }

  function stop() {
    if (raf) cancelAnimationFrame(raf);
    raf = 0;
  }

  /* The canvas can still be unlaid-out on the first pass; retry a few
     frames before giving up rather than racing the observers. */
  function boot() {
    if (ready) return;
    readTheme();
    if (!resize()) {
      if (tries++ < 30) requestAnimationFrame(boot);
      return;
    }
    ready = true;
    draw(0);
    cv.classList.add("on");
    start();
  }

  let rt = 0;
  window.addEventListener("resize", function () {
    clearTimeout(rt);
    rt = setTimeout(function () {
      if (!ready) return;
      stop();
      if (resize()) { draw(0); start(); }
    }, 180);
  });

  document.addEventListener("visibilitychange", function () {
    if (document.hidden) stop(); else start();
  });

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (es) {
      visible = es[0].isIntersecting;
      if (visible) start(); else stop();
    }, { threshold: 0 }).observe(cv);
  }

  const mq = window.matchMedia("(prefers-color-scheme: dark)");
  const onScheme = function () { readTheme(); if (ready && !raf) draw(0); };
  if (mq.addEventListener) mq.addEventListener("change", onScheme);
  else if (mq.addListener) mq.addListener(onScheme);

  boot();
  window.addEventListener("load", boot);
})();
