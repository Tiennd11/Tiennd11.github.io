/* ==================================================================
   Research-interest diagrams.

   Each card holds one small SVG figure. They only animate while the
   card is actually on screen and the tab is in front, and never at all
   when the visitor has asked for reduced motion. CSS animations are
   gated by a .run class; the one SMIL animation (the arm, whose joint
   positions are precomputed IK and cannot be expressed in CSS) is
   gated with pauseAnimations / unpauseAnimations.
   ================================================================== */

(function () {
  "use strict";

  const cards = Array.prototype.slice.call(document.querySelectorAll(".int"));
  if (!cards.length) return;

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)");

  function svgsIn(card) {
    return Array.prototype.slice.call(card.querySelectorAll("svg"));
  }

  function run(card, on) {
    if (on && !reduced.matches) {
      card.classList.add("run");
      svgsIn(card).forEach(function (s) {
        if (s.unpauseAnimations) s.unpauseAnimations();
      });
    } else {
      card.classList.remove("run");
      svgsIn(card).forEach(function (s) {
        if (s.pauseAnimations) s.pauseAnimations();
      });
    }
  }

  function stopAll() { cards.forEach(function (c) { run(c, false); }); }

  /* start paused: nothing animates until it is both visible and allowed */
  stopAll();

  const onscreen = new WeakSet();

  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) onscreen.add(e.target);
        else onscreen.delete(e.target);
        run(e.target, e.isIntersecting && !document.hidden);
      });
    }, { rootMargin: "80px 0px", threshold: 0.15 });

    cards.forEach(function (c) { io.observe(c); });
  } else {
    cards.forEach(function (c) { onscreen.add(c); run(c, true); });
  }

  document.addEventListener("visibilitychange", function () {
    cards.forEach(function (c) {
      run(c, !document.hidden && onscreen.has(c));
    });
  });

  const onReduce = function () {
    cards.forEach(function (c) {
      run(c, !reduced.matches && !document.hidden && onscreen.has(c));
    });
  };
  if (reduced.addEventListener) reduced.addEventListener("change", onReduce);
  else if (reduced.addListener) reduced.addListener(onReduce);
})();
