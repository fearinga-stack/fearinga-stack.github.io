// Proof on demand: pointing at a sentence lets its image rise behind the words.
(function () {
  var proof = document.getElementById('proof');
  if (!proof) return;
  var links = document.querySelectorAll('[data-proof]');
  links.forEach(function (a) {
    function show() {
      proof.style.backgroundImage = 'url("' + a.getAttribute('data-proof') + '")';
      proof.classList.add('on');
    }
    function hide() { proof.classList.remove('on'); }
    a.addEventListener('mouseenter', show);
    a.addEventListener('mouseleave', hide);
    a.addEventListener('focus', show);
    a.addEventListener('blur', hide);
    // Touch: first tap shows the proof, second tap follows the link.
    a.addEventListener('touchend', function (e) {
      if (!proof.classList.contains('on') ||
          proof.style.backgroundImage.indexOf(a.getAttribute('data-proof')) === -1) {
        e.preventDefault();
        show();
      }
    });
  });
})();
