/* Narrow screens: the section links collapse behind one Menu button
   (same destinations, 44px targets) instead of being dropped. */
(function () {
  "use strict";
  const btn = document.querySelector(".navtoggle");
  const links = document.getElementById("navlinks");
  if (!btn || !links) return;

  const word = (k) => (window.I18N ? window.I18N.ui(k) : { menu: "Menu", close: "Close" }[k]);

  function set(open) {
    links.classList.toggle("open", open);
    btn.setAttribute("aria-expanded", String(open));
    btn.textContent = word(open ? "close" : "menu");
  }

  btn.textContent = word("menu");
  document.addEventListener("langchange", function () {
    btn.textContent = word(btn.getAttribute("aria-expanded") === "true" ? "close" : "menu");
  });

  btn.addEventListener("click", function () {
    set(btn.getAttribute("aria-expanded") !== "true");
  });

  links.addEventListener("click", function (e) {
    if (e.target.closest("a")) set(false);
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && btn.getAttribute("aria-expanded") === "true") {
      set(false);
      btn.focus();
    }
  });
})();
