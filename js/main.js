(function () {
  'use strict';

  // Menu mobile
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('menu');
  var english = document.documentElement.lang === 'en';
  var labels = english
    ? { open: 'Open menu', close: 'Close menu' }
    : { open: 'Ouvrir le menu', close: 'Fermer le menu' };

  function setMenu(open) {
    nav.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? labels.close : labels.open);
  }

  toggle.addEventListener('click', function () {
    setMenu(!nav.classList.contains('open'));
  });
  nav.addEventListener('click', function (event) {
    if (event.target.closest('a')) setMenu(false);
  });
  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') setMenu(false);
  });

  // Apparition des blocs au défilement
  var blocks = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    blocks.forEach(function (block) { observer.observe(block); });
  } else {
    blocks.forEach(function (block) { block.classList.add('visible'); });
  }

  document.getElementById('annee').textContent = new Date().getFullYear();
})();
