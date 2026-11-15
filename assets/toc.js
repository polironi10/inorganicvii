(function () {
  var btn = document.getElementById('toc-btn');
  var panel = document.getElementById('toc-panel');
  var closeBtn = document.getElementById('toc-close');
  if (!btn || !panel) return;
  function open() {
    panel.hidden = false;
    btn.setAttribute('aria-expanded', 'true');
  }
  function shut() {
    panel.hidden = true;
    btn.setAttribute('aria-expanded', 'false');
  }
  btn.addEventListener('click', function () { panel.hidden ? open() : shut(); });
  if (closeBtn) closeBtn.addEventListener('click', shut);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') shut(); });
  panel.addEventListener('click', function (e) { if (e.target.tagName === 'A') shut(); });
})();
