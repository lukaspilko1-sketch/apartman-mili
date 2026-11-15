/* Apartmán Mili – minimální JS: menu, galerie (lightbox), odkrývání sekcí, záložní fotky. */
(function () {
  'use strict';

  /* 1) Chybějící fotka se skryje (místo ikony rozbitého obrázku zůstane barevná plocha). */
  document.querySelectorAll('main img').forEach(function (img) {
    function onFail() { img.classList.add('is-missing'); }
    img.addEventListener('error', onFail);
    /* Nenačtené lazy fotky hlásí complete=true s šířkou 0, proto je tu nekontrolujeme. */
    if (img.loading !== 'lazy' && img.complete && img.naturalWidth === 0) onFail();
  });

  /* 2) Mobilní menu */
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', String(open));
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        nav.classList.remove('is-open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        nav.classList.remove('is-open');
        btn.setAttribute('aria-expanded', 'false');
        btn.focus();
      }
    });
  }

  /* 3) Lightbox */
  var dlg = document.getElementById('lightbox');
  var buttons = Array.prototype.slice.call(document.querySelectorAll('.gallery__btn'));
  if (dlg && buttons.length && typeof dlg.showModal === 'function') {
    var big = dlg.querySelector('.lightbox__fig img');
    var current = 0;
    var lastFocus = null;

    function show(i) {
      current = (i + buttons.length) % buttons.length;
      var src = buttons[current].querySelector('img');
      big.src = src.currentSrc || src.src;
      big.alt = src.alt;
    }
    buttons.forEach(function (b, i) {
      b.addEventListener('click', function () {
        lastFocus = b;
        show(i);
        dlg.showModal();
      });
    });
    dlg.querySelector('.lightbox__close').addEventListener('click', function () { dlg.close(); });
    dlg.querySelector('.lightbox__nav--prev').addEventListener('click', function () { show(current - 1); });
    dlg.querySelector('.lightbox__nav--next').addEventListener('click', function () { show(current + 1); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener('close', function () { if (lastFocus) lastFocus.focus(); });
    dlg.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') show(current - 1);
      if (e.key === 'ArrowRight') show(current + 1);
    });
    var x0 = null;
    dlg.addEventListener('touchstart', function (e) { x0 = e.changedTouches[0].clientX; }, { passive: true });
    dlg.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 50) show(current + (dx < 0 ? 1 : -1));
      x0 = null;
    });
  }

  /* 4) Odkrývání sekcí při scrollu (obsah je bez JS i při reduced-motion viditelný) */
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  /* 5) Pevné tlačítko "Rezervovat" na mobilu: zobrazí se po odrolování z hero */
  var sticky = document.querySelector('.sticky-cta');
  var hero = document.querySelector('.hero');
  if (sticky && hero && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      sticky.classList.toggle('is-visible', !entries[0].isIntersecting);
    }, { threshold: 0 }).observe(hero);
  } else if (sticky) {
    sticky.classList.add('is-visible');
  }
})();
