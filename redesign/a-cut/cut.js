// Frame counter: updates as each full-screen cut takes the screen.
(function () {
  var cuts = Array.prototype.slice.call(document.querySelectorAll('.cut'));
  var counter = document.getElementById('counter');
  if (!counter || !cuts.length) return;
  var total = String(cuts.length).padStart(2, '0');
  function show(i) { counter.textContent = String(i + 1).padStart(2, '0') + ' / ' + total; }
  show(0);
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) show(cuts.indexOf(e.target));
      });
    }, { threshold: 0.6 });
    cuts.forEach(function (c) { io.observe(c); });
  }
  // Arrow keys cut forward / back.
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp') return;
    var y = window.scrollY, h = window.innerHeight;
    var i = Math.round(y / h) + (e.key === 'ArrowDown' ? 1 : -1);
    if (i < 0 || i >= cuts.length) return;
    e.preventDefault();
    cuts[i].scrollIntoView({ behavior: 'auto' }); // hard cut, no easing
  });
})();
