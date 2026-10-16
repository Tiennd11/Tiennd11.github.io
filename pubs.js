/* ------------------------------------------------------------------
   Publication list — published and accepted only.
   Manuscripts under review / under revision / submitted are not listed.

   Author strings:  *name*  marks Duc Tien Nguyen
                    ^       after a name marks equal contribution
   tags:            sciml | robotics | fracture | structdyn | uq | agentic
   ------------------------------------------------------------------ */

const THREADS = {
  sciml:     { label: "Scientific ML",       color: "#0072B2" },
  robotics:  { label: "Robotics",            color: "#009E73" },
  fracture:  { label: "Fracture",            color: "#D55E00" },
  structdyn: { label: "Structural dynamics", color: "#CC79A7" },
  uq:        { label: "Uncertainty",         color: "#E69F00" },
  agentic:   { label: "Agentic AI",          color: "#56B4E9" }
};

const PUBS = [
  /* ---------------------------------- 2026 */
  { y: 2026, type: "journal", tags: ["robotics", "sciml"],
    t: "Trajectory-based sequential learning for efficient and stable inverse kinematics of robotic manipulators",
    a: "*D. T. Nguyen*, V. T. T. Nguyen, D. T. Luu, T. Do, V. L. Nguyen",
    v: "Robotics and Autonomous Systems" },

  { y: 2026, type: "journal", tags: ["structdyn", "uq"],
    t: "Stochastic nonlinear behavior of graphene origami auxetic metamaterial plates under uncertain excitation using different sampling strategies",
    a: "T. T. Minh, N. H. Minh, N. M. Dzung, T. D. Nguyen, D. V. Truong, V. L. Nguyen, *D. T. Nguyen*^, D. G. Ninh^",
    v: "Aerospace Science and Technology" },

  { y: 2026, type: "journal", tags: ["sciml"],
    t: "ST-PINN: Shared-trunk PINNs for discontinuous multi-domain PDEs",
    a: "*D. T. Nguyen*, H. Tran, V. L. Nguyen",
    v: "Engineering with Computers" },

  { y: 2026, type: "journal", tags: ["robotics", "sciml", "uq"],
    t: "Physics-informed learning for forward kinematics of robotic manipulators under uncertainty",
    a: "*D. T. Nguyen*, X. T. Vu, T. Do, V. L. Nguyen",
    v: "Journal of Mechanisms and Robotics" },

  { y: 2026, type: "journal", tags: ["robotics"],
    t: "Multi-solution inverse kinematics for robotic manipulators via permutation-invariant set prediction",
    a: "*D. T. Nguyen*, T. Do, V. L. Nguyen",
    v: "IEEE Robotics and Automation Letters" },

  { y: 2026, type: "journal", tags: ["sciml", "structdyn"],
    t: "Physics-informed and data-driven inverse parameter identification for nonlinear vibrations of BNNT-reinforced composite plates",
    a: "*D. T. Nguyen*, N. M. Dzung, N. N. Quang, V. T. Nguyen, V. L. Nguyen, D. G. Ninh",
    v: "European Journal of Mechanics - A/Solids" },

  { y: 2026, type: "conference", tags: ["robotics"],
    t: "History-conditioned neural inverse kinematics for redundant manipulators",
    a: "*D. T. Nguyen*, L. Scalera, V. L. Nguyen",
    v: "IFToMM International Symposium on Robotics and Mechatronics" },

  { y: 2026, type: "conference", tags: ["robotics"],
    t: "Robust deep reinforcement learning control via active disturbance rejection for nonlinear robotic manipulators",
    a: "X. T. Vu, V. T. Nguyen, D. T. Luu, *D. T. Nguyen*, V. L. Nguyen",
    v: "IFToMM International Symposium on Robotics and Mechatronics" },

  { y: 2026, type: "conference", tags: ["robotics", "sciml"],
    t: "Weak-form physics-structured sparse Lagrangian regression for noise-robust multibody dynamics identification",
    a: "*D. T. Nguyen*, V. T. T. Nguyen, T. Do, V. L. Nguyen",
    v: "IFToMM International Symposium on Robotics and Mechatronics" },

  /* ---------------------------------- 2025 */
  { y: 2025, type: "journal", tags: ["structdyn", "uq"],
    t: "Stochastic nonlinear dynamic investigation of laminated nanocomposite non-rectangular plates under random loading",
    a: "N. M. Dzung^, *D. T. Nguyen*^, V. T. Thang, D. G. Ninh",
    v: "Communications in Nonlinear Science and Numerical Simulation" },

  { y: 2025, type: "journal", tags: ["structdyn", "sciml"],
    t: "Inverse problem solution and optimization in the vibration analysis of a nanocomposite cylindrical shell using the L-BFGS-B algorithm",
    a: "*D. T. Nguyen*, N. C. Tan, D. Yawson, D. G. Ninh",
    v: "Composite Structures" },

  { y: 2025, type: "journal", tags: ["uq", "structdyn"],
    t: "Modeling and quantifying uncertainty in nanocomposite shell vibrations using heteroscedastic Gaussian processes",
    a: "*D. T. Nguyen*, D. G. Ninh",
    v: "Engineering Applications of Artificial Intelligence" },

  { y: 2025, type: "journal", tags: ["sciml", "structdyn"],
    t: "Highly efficient prediction of beating phenomena in laminated nanocomposite plates using a hybrid neural–numerical–analytical framework",
    a: "*D. T. Nguyen*, N. D. Manh, N. M. Dzung, D. G. Ninh",
    v: "European Journal of Mechanics - A/Solids" },

  { y: 2025, type: "journal", tags: ["structdyn"],
    t: "Novel sandwich composite shell structures in nonlinear geometric and dynamic analyses",
    a: "N. C. Tan, N. M. Dzung, N. H. Ha, *D. T. Nguyen*, N. C. Hung, A. H. Sofiyev, D. G. Ninh",
    v: "AIAA Journal" },

  { y: 2025, type: "journal", tags: ["fracture"],
    t: "An adaptive mesh refinement algorithm for stress-based phase-field fracture models for heterogeneous media: Application using FEniCS to ice-rock cliff failures",
    a: "*D. T. Nguyen*, A. Gupta, R. Duddu, C. Annavarapu",
    v: "Finite Elements in Analysis and Design",
    doi: "10.1016/j.finel.2024.104311" },

  /* ---------------------------------- 2024 */
  { y: 2024, type: "journal", tags: ["sciml", "structdyn"],
    t: "Utilizing optimal physics-informed neural networks for dynamical analysis of nanocomposite one-variable-edge plates",
    a: "*D. T. Nguyen*^, N. C. Tan^, N. M. Dzung, N. H. Ha, N. T. Dong, D. G. Ninh",
    v: "Thin-Walled Structures" },

  { y: 2024, type: "journal", tags: ["fracture"],
    t: "Damage mechanics challenge: Predictions from an adaptive finite element implementation of the stress-based phase-field fracture model",
    a: "A. Gupta, *D. T. Nguyen*, R. Duddu",
    v: "Engineering Fracture Mechanics",
    doi: "10.1016/j.engfracmech.2024.110252" },

  { y: 2024, type: "journal", tags: ["structdyn", "fracture"],
    t: "Effects of edge-crack orientation and depth on nonlinear dynamics of laminated nanocomposite single-variable-edge plates",
    a: "N. M. Dzung, N. C. Tan, N. H. Ha, *D. T. Nguyen*, H. Eslami, D. G. Ninh",
    v: "Engineering Structures" },

  /* ---------------------------------- 2023 */
  { y: 2023, type: "journal", tags: ["structdyn"],
    t: "Thermal vibrations of complex-generatrix shells made of sandwich CNTRC sheets on both sides and open/closed cellular functionally graded porous core",
    a: "D. G. Ninh, N. H. Ha, N. T. Long, N. C. Tan, *D. T. Nguyen*, D. V. Dao",
    v: "Thin-Walled Structures" },

  /* ---------------------------------- 2021 */
  { y: 2021, type: "journal", tags: ["structdyn"],
    t: "Nonlinear dynamics of functionally graded graphene nanoplatelet reinforced polymer doubly-curved shallow shells resting on elastic foundation using a micromechanical model",
    a: "V. N. Viet Hoang, *D. T. Nguyen*, D. G. Ninh, V. T. Thang, D. V. Truong",
    v: "Journal of Sandwich Structures and Materials" },

  { y: 2021, type: "journal", tags: ["structdyn"],
    t: "Nonlinear dynamics and chaos of a nanocomposite plate subjected to electro-thermo-mechanical loads using Flügge–Lur'e–Byrne theory",
    a: "*D. T. Nguyen*, V. N. Viet Hoang, D. G. Ninh, V. L. Huy, N. C. Hung",
    v: "Journal of Vibration and Control" },

  /* ---------------------------------- 2020 */
  { y: 2020, type: "journal", tags: ["structdyn"],
    t: "Vibration of cylindrical shells made of three-layer W–Cu composite containing heavy water using Flügge–Lur'e–Byrne theory",
    a: "D. G. Ninh, *D. T. Nguyen*, V. N. Viet Hoang, D. H. Bich",
    v: "Thin-Walled Structures" },

  /* ---------------------------------- 2019 */
  { y: 2019, type: "journal", tags: ["structdyn"],
    t: "Analyses of nonlinear dynamics of imperfect nanocomposite circular cylindrical shells with swirling annular and internal fluid flow using higher-order shear deformation shell theory",
    a: "D. G. Ninh, *D. T. Nguyen*, V. N. Viet Hoang",
    v: "Engineering Structures" },

  { y: 2019, type: "journal", tags: ["structdyn"],
    t: "Investigation of electro-thermo-mechanical vibration of nanocomposite cylindrical shells with internal fluid flow",
    a: "D. G. Ninh, *D. T. Nguyen*",
    v: "Aerospace Science and Technology" }
];

/* ------------------------------------------------------------------ */

(function () {
  "use strict";

  const esc = (s) => s.replace(/[&<>"]/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  const authors = (s) => esc(s)
    .replace(/\*([^*]+)\*/g, "<b>$1</b>")
    .replace(/\^/g, '<sup title="equal contribution">*</sup>');

  const lists = {
    journal: document.getElementById("pubs-journal"),
    conference: document.getElementById("pubs-conference")
  };
  const groups = {
    journal: document.getElementById("group-journal"),
    conference: document.getElementById("group-conference")
  };
  const tallies = {
    journal: document.getElementById("tally-journal"),
    conference: document.getElementById("tally-conference")
  };
  const noresults = document.getElementById("noresults");
  const filterBar = document.getElementById("filters");

  if (!lists.journal) return;

  /* ---- build the list items once -------------------------------- */
  const items = PUBS
    .slice()
    .sort((p, q) => q.y - p.y)
    .map((p) => {
      const li = document.createElement("li");
      li.className = "pub";
      li.dataset.tags = p.tags.join(" ");
      li.dataset.year = p.y;

      const doi = p.doi
        ? ' <a class="doi" href="https://doi.org/' + esc(p.doi) + '">doi:' + esc(p.doi) + "</a>"
        : "";

      const chips = p.tags.map((k) =>
        '<li style="--c:' + THREADS[k].color + '">' + esc(THREADS[k].label) + "</li>"
      ).join("");

      li.innerHTML =
        '<span class="y" aria-hidden="true"></span>' +
        '<div class="pbody">' +
          '<p class="ptitle">' + esc(p.t) + "</p>" +
          '<p class="pauth">' + authors(p.a) + "</p>" +
          '<p class="pven"><em>' + esc(p.v) + "</em>, " + p.y + doi + "</p>" +
          '<ul class="ptags">' + chips + "</ul>" +
        "</div>";

      lists[p.type].appendChild(li);
      return li;
    });

  /* ---- filtering ------------------------------------------------- */
  let active = "all";

  function apply() {
    let total = 0;

    Object.keys(lists).forEach((type) => {
      let shown = 0;
      let lastYear = null;

      Array.prototype.forEach.call(lists[type].children, (li) => {
        const hit = active === "all" || li.dataset.tags.split(" ").indexOf(active) > -1;
        li.hidden = !hit;
        if (!hit) return;
        shown++;
        // print the year only on the first entry of each run
        const y = li.dataset.year;
        li.querySelector(".y").textContent = y === lastYear ? "" : y;
        lastYear = y;
      });

      total += shown;
      tallies[type].textContent = shown;
      groups[type].hidden = shown === 0;
    });

    noresults.hidden = total > 0;
  }

  /* ---- filter buttons -------------------------------------------- */
  const used = Object.keys(THREADS).filter((k) =>
    PUBS.some((p) => p.tags.indexOf(k) > -1));

  const mk = (key, label, color) => {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "chip";
    b.textContent = label;
    b.setAttribute("aria-pressed", key === "all");
    if (color) b.style.setProperty("--c", color);
    b.addEventListener("click", () => {
      active = active === key ? "all" : key;
      Array.prototype.forEach.call(filterBar.children, (el) =>
        el.setAttribute("aria-pressed", el.dataset.key === active));
      apply();
    });
    b.dataset.key = key;
    return b;
  };

  filterBar.appendChild(mk("all", "All work", null));
  used.forEach((k) => filterBar.appendChild(mk(k, THREADS[k].label, THREADS[k].color)));

  apply();

  const n = PUBS.length;
  const nj = PUBS.filter((p) => p.type === "journal").length;
  document.getElementById("pubcount").textContent =
    n + " entries — " + nj + " journal articles and " + (n - nj) + " conference papers.";
})();
