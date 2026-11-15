(function () {
  var btn = document.getElementById('search-btn');
  var panel = document.getElementById('search-panel');
  var input = document.getElementById('search-input');
  var results = document.getElementById('search-results');
  var closeBtn = document.getElementById('search-close');
  var data = null;
  if (!btn || !panel) return;
  function open() {
    panel.hidden = false;
    btn.setAttribute('aria-expanded', 'true');
    input.focus();
  }
  function shut() {
    panel.hidden = true;
    btn.setAttribute('aria-expanded', 'false');
    input.value = '';
    results.innerHTML = '';
  }
  btn.addEventListener('click', function () { panel.hidden ? open() : shut(); });
  closeBtn.addEventListener('click', shut);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') shut();
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); open(); }
  });
  function load() {
    if (data) return Promise.resolve(data);
    return fetch(panel.getAttribute('data-index')).then(function (r) { return r.json(); }).then(function (j) { data = j; return j; });
  }
  function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  input.addEventListener('input', function () {
    var q = input.value.trim().toLowerCase();
    if (q.length < 2) { results.innerHTML = ''; return; }
    load().then(function (items) {
      var hits = items.filter(function (it) {
        return (it.t + ' ' + it.x).toLowerCase().indexOf(q) > -1;
      }).slice(0, 8);
      if (!hits.length) {
        results.innerHTML = '<li class="no-results">Nothing found for &ldquo;' + esc(input.value) + '&rdquo;.</li>';
        return;
      }
      results.innerHTML = hits.map(function (it) {
        var at = it.x.toLowerCase().indexOf(q);
        var start = Math.max(0, at - 40);
        var excerpt = (start > 0 ? '…' : '') + it.x.slice(start, start + 140) + '…';
        return '<li><a href="' + esc(it.u) + (it.a ? '#' + esc(it.a) : '') + '">' + esc(it.t) + '</a><span>' + esc(excerpt) + '</span></li>';
      }).join('');
    }).catch(function () {
      results.innerHTML = '<li class="no-results">Search could not load. Try again.</li>';
    });
  });
})();
