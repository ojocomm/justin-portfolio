/* justinnorman.nl — site behaviour (header, mobile menu, scroll animations, contact form) */
(function () {
  'use strict';
  var doc = document, root = doc.documentElement, body = doc.body;
  root.classList.add('js');

  /* ---- fixed header: expose its height to CSS (first section padding, menu offset) */
  var header = doc.getElementById('header');
  function setHeaderHeight() {
    if (!header) return;
    var h = header.offsetHeight;
    root.style.setProperty('--header-height', h + 'px');
    root.style.scrollPaddingTop = h + 'px';
  }
  setHeaderHeight();
  window.addEventListener('resize', setHeaderHeight);
  if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(setHeaderHeight);
  window.addEventListener('load', setHeaderHeight);

  /* ---- mobile menu */
  var burger = doc.querySelector('.burger');
  var menu = doc.getElementById('header-menu');
  function setMenu(open) {
    body.classList.toggle('header--menu-open', open);
    if (burger) {
      burger.classList.toggle('burger--active', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Menu sluiten' : 'Menu openen');
    }
  }
  if (burger && menu) {
    burger.addEventListener('click', function () { setMenu(!body.classList.contains('header--menu-open')); });
    doc.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
    window.matchMedia('(min-width: 800px) and (pointer: fine)').addEventListener('change', function (e) { if (e.matches) setMenu(false); });
  }

  /* ---- site-wide "fade / slide" animations (same look as the Squarespace theme setting) */
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var textSel = '.sqs-html-content h1, .sqs-html-content h2, .sqs-html-content h3, .sqs-html-content h4';
  var fadeSel = '.sqs-html-content p, .sqs-html-content ul, .sqs-html-content ol, .sqs-block-button-element, .sqs-block-horizontalrule hr, .fluid-image-animation-wrapper, .sqs-shape-block-container, .contact-form, .sqs-svg-icon--outer';
  if (!reduce && 'IntersectionObserver' in window) {
    var items = [];
    doc.querySelectorAll('.page-section, .site-footer').forEach(function (sec) {
      var i = 0;
      sec.querySelectorAll(textSel).forEach(function (el) { el.classList.add('preSlide'); el.style.transitionDelay = Math.min(0.06 * i++, 0.36).toFixed(3) + 's'; items.push(el); });
      sec.querySelectorAll(fadeSel).forEach(function (el) { el.classList.add('preFade'); el.style.transitionDelay = Math.min(0.06 * i++, 0.36).toFixed(3) + 's'; items.push(el); });
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting || en.boundingClientRect.top < 0) {
          en.target.classList.add('animation-in');
          io.unobserve(en.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.01 });
    items.forEach(function (el) { io.observe(el); });
    /* header elements animate straight away */
    doc.querySelectorAll('.header-title-logo, .header-nav-item a, .header-actions > *').forEach(function (el, i) {
      el.classList.add('preSlide');
      el.style.transitionDelay = (0.03 * i).toFixed(3) + 's';
      requestAnimationFrame(function () { requestAnimationFrame(function () { el.classList.add('animation-in'); }); });
    });
  }

  /* ---- contact form: no server behind a static site, so hand the message to the visitor's mail app */
  var form = doc.querySelector('.contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var status = form.querySelector('.form-status');
      var invalid = false;
      form.querySelectorAll('[required]').forEach(function (f) {
        var bad = !f.value.trim() || (f.type === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.value));
        f.classList.toggle('is-invalid', bad);
        f.setAttribute('aria-invalid', bad ? 'true' : 'false');
        invalid = invalid || bad;
      });
      if (invalid) {
        status.hidden = false;
        status.textContent = 'Vul de verplichte velden in (naam en een geldig e-mailadres).';
        return;
      }
      var v = function (id) { return (form.querySelector('#' + id) || {}).value || ''; };
      var subject = 'Contact via justinnorman.nl — ' + v('f-fname') + ' ' + v('f-lname');
      var bodyTxt = 'Naam: ' + v('f-fname') + ' ' + v('f-lname') + '\nE-mail: ' + v('f-email') +
        '\nTelefoon: ' + v('f-phone') + '\n\n' + v('f-message');
      window.location.href = 'mailto:' + form.getAttribute('data-mailto') +
        '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(bodyTxt);
      status.hidden = false;
      status.textContent = 'Je e-mailprogramma wordt geopend met het ingevulde bericht.';
    });
  }
})();

/* ---- terug-naar-boven-knop (alle pagina's) */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var btn = document.createElement('button');
  btn.className = 'to-top';
  btn.type = 'button';
  btn.setAttribute('aria-label', 'Terug naar boven');
  btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 19V5M6 11l6-6 6 6"/></svg>';
  document.body.appendChild(btn);
  var toggle = function () { btn.classList.toggle('is-visible', window.scrollY > 600); };
  window.addEventListener('scroll', toggle, { passive: true });
  toggle();
  btn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
  });
})();
