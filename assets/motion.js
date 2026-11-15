/* Extra motion for inorganicvii, GSAP (from the official gsap-skills).
   Only transform/opacity. Nothing here hides content if GSAP or the CDN
   is unavailable: with no gsap object this file does nothing and the
   figures simply appear. Respects prefers-reduced-motion and the footer
   Pause motion button. */
(function () {
  if (!window.gsap || !window.ScrollTrigger) return;
  gsap.registerPlugin(ScrollTrigger);
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  // Once-only scroll reveal for figures (figures only, never the prose).
  gsap.utils.toArray("figure").forEach(function (f) {
    gsap.from(f, {
      autoAlpha: 0, y: 24, duration: 0.5, ease: "power3.out",
      scrollTrigger: { trigger: f, start: "top 88%", once: true }
    });
    // Atoms dropping into place, staggered, with a small spring overshoot.
    var drops = f.querySelectorAll(".anim-drop");
    if (drops.length) {
      gsap.from(drops, {
        y: -10, autoAlpha: 0, stagger: 0.09, duration: 0.5, ease: "back.out(1.7)",
        scrollTrigger: { trigger: f, start: "top 88%", once: true }
      });
    }
    // CFSE levels drawing themselves in, left to right.
    var lines = f.querySelectorAll(".anim-line");
    if (lines.length) {
      gsap.fromTo(lines, { scaleX: 0 }, {
        scaleX: 1, transformOrigin: "left center", stagger: 0.15,
        duration: 0.5, ease: "power2.out",
        scrollTrigger: { trigger: f, start: "top 88%", once: true }
      });
    }
  });

  // Pause motion button: stop every GSAP tween and leave everything visible.
  var toggle = document.querySelector(".motion-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      if (document.body.classList.contains("no-motion")) {
        ScrollTrigger.getAll().forEach(function (st) { st.kill(); });
        gsap.set("figure", { clearProps: "all" });
        gsap.set("figure svg .anim-drop, figure svg .anim-line", { clearProps: "all" });
        gsap.globalTimeline.pause();
      } else {
        gsap.globalTimeline.play();
      }
    });
  }
})();
