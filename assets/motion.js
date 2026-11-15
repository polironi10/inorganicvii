/* Extra motion for inorganicvii, GSAP (from the official gsap-skills).
   Only transform/opacity. Nothing here ever hides content: figures are
   always visible by default, and each animation is only created when its
   figure is actually on screen (or after a 2.5s fallback). If GSAP or the
   CDN is unavailable this file does nothing and the figures simply appear.
   Respects prefers-reduced-motion and the footer Pause motion button. */
(function () {
  if (!window.gsap) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var played = new WeakSet();
  function animateFigure(f) {
    if (played.has(f)) return;
    played.add(f);
    // Atoms dropping into place, staggered, with a small spring overshoot.
    var drops = f.querySelectorAll(".anim-drop");
    if (drops.length) {
      gsap.from(drops, { y: -10, autoAlpha: 0, stagger: 0.09, duration: 0.5, ease: "back.out(1.7)" });
    }
    // CFSE levels drawing themselves in, left to right.
    var lines = f.querySelectorAll(".anim-line");
    if (lines.length) {
      gsap.fromTo(lines, { scaleX: 0 }, {
        scaleX: 1, transformOrigin: "left center", stagger: 0.15,
        duration: 0.5, ease: "power2.out"
      });
    }
  }

  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { animateFigure(e.target); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -10% 0px" });
    document.querySelectorAll("figure").forEach(function (f) { io.observe(f); });
  }
  // Fallback: play every figure's animation after 2.5s, so nothing ever
  // stays unanimated because an observer never fired.
  setTimeout(function () {
    document.querySelectorAll("figure").forEach(animateFigure);
  }, 2500);

  // Pause motion button: stop GSAP and leave every diagram fully visible.
  var toggle = document.querySelector(".motion-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      if (document.body.classList.contains("no-motion")) {
        gsap.globalTimeline.pause();
        gsap.set("figure svg .anim-drop, figure svg .anim-line", { clearProps: "all" });
      } else {
        gsap.globalTimeline.play();
      }
    });
  }
})();
