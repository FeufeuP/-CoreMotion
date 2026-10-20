(() => {
  'use strict';
  const $  = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const scenes = $$('.scene');
  const N = scenes.length;
  if (!N) return;

  const hud    = $('#hud');
  const hudCh  = $('#hudCh');
  const hudNum = $('#hudNum');
  const progFill = $('#progFill');
  const progTicks = $('#progTicks');
  const menu = $('#menu');
  const list = $('#menuList');

  /* ---------------------------------------------------------------- ticks */
  if (progTicks) {
    for (let i = 0; i < N; i++) progTicks.appendChild(document.createElement('i'));
  }

  /* ---------------------------------------------------------------- índice */
  if (list) {
    scenes.forEach((s, i) => {
      const li = document.createElement('li');
      const b = document.createElement('button');
      b.type = 'button';
      b.dataset.goto = String(i);
      b.innerHTML =
        '<span class="n">' + String(i + 1).padStart(2, '0') + '</span>' +
        '<span class="t">' + (s.dataset.ch || '') + '</span>' +
        '<span class="c">' + (s.dataset.kicker || '') + '</span>';
      li.appendChild(b);
      list.appendChild(li);
    });
  }

  /* ---------------------------------------------------------------- menu */
  let lastFocus = null;
  const isOpen = () => menu && menu.classList.contains('open');
  function openMenu() {
    if (!menu) return;
    lastFocus = document.activeElement;
    menu.classList.add('open');
    menu.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    const first = menu.querySelector('button');
    if (first) first.focus({ preventScroll: true });
  }
  function closeMenu() {
    if (!menu) return;
    menu.classList.remove('open');
    menu.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
  }
  const openBtn = $('#openMenu');
  const closeBtn = $('#menuClose');
  if (openBtn) openBtn.addEventListener('click', openMenu);
  if (closeBtn) closeBtn.addEventListener('click', closeMenu);
  if (menu) {
    menu.addEventListener('click', (e) => {
      const btn = e.target.closest('[data-goto]');
      if (btn) { closeMenu(); goTo(Number(btn.dataset.goto)); return; }
      if (e.target === menu) closeMenu();
    });
  }

  /* ---------------------------------------------------------------- navega */
  function goTo(i) {
    i = Math.max(0, Math.min(N - 1, i));
    const top = scenes[i].getBoundingClientRect().top + window.scrollY;
    window.scrollTo({ top, behavior: reduce ? 'auto' : 'smooth' });
  }

  let cur = -1;
  let ticking = false;

  function measure() {
    const vh = window.innerHeight || 1;
    const max = document.documentElement.scrollHeight - vh;
    if (progFill) progFill.style.width = (max > 0 ? (window.scrollY / max) * 100 : 0) + '%';

    let best = 0, bestScore = -1;

    scenes.forEach((s, i) => {
      const r = s.getBoundingClientRect();
      const seen = Math.min(r.bottom, vh) - Math.max(r.top, 0);
      const score = Math.max(0, seen) / vh;
      if (score > bestScore) { bestScore = score; best = i; }

      if (!reduce) {
        const p = (r.top + r.height / 2 - vh / 2) / vh;
        s.style.setProperty('--p', Math.max(-1.4, Math.min(1.4, p)).toFixed(3));
      }
      s.classList.toggle('on', score > 0.32);
    });

    if (best !== cur) {
      cur = best;
      if (hudCh) hudCh.textContent = scenes[best].dataset.ch || '';
      if (hudNum) hudNum.textContent = String(best + 1).padStart(2, '0');
      const tone = scenes[best].dataset.hud;
      if (hud) {
        hud.classList.toggle('hud--light', tone === 'light');
        hud.classList.toggle('hud--split', tone === 'split');
      }
      if (list) {
        $$('li', list).forEach((li, i) => li.classList.toggle('is-now', i === best));
      }
      if (history.replaceState) history.replaceState(null, '', '#' + scenes[best].id);
    }
  }

  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => { ticking = false; measure(); });
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);

  /* ---------------------------------------------------------------- teclado */
  window.addEventListener('keydown', (e) => {
    const tag = (e.target.tagName || '').toLowerCase();
    if (tag === 'input' || tag === 'textarea') return;

    if (isOpen()) {
      if (e.key === 'Escape') { e.preventDefault(); closeMenu(); }
      return;
    }
    const k = e.key;
    if (k === 'ArrowRight' || k === 'ArrowDown' || k === 'PageDown' || k === ' ') {
      e.preventDefault(); goTo((cur < 0 ? 0 : cur) + 1);
    } else if (k === 'ArrowLeft' || k === 'ArrowUp' || k === 'PageUp') {
      e.preventDefault(); goTo((cur < 0 ? 0 : cur) - 1);
    } else if (k === 'Home') {
      e.preventDefault(); goTo(0);
    } else if (k === 'End') {
      e.preventDefault(); goTo(N - 1);
    } else if (k === 'm' || k === 'M') {
      e.preventDefault(); openMenu();
    }
  });

  /* ---------------------------------------------------------------- cursor */
  const curEl = $('#cursor');
  const glow = $('#glow');
  let mx = window.innerWidth / 2, my = window.innerHeight / 2;
  let px = mx, py = my;

  window.addEventListener('mousemove', (e) => {
    mx = e.clientX; my = e.clientY;
    if (glow) {
      glow.style.setProperty('--mx', mx + 'px');
      glow.style.setProperty('--my', my + 'px');
    }
    if (curEl) curEl.classList.remove('is-out');
  }, { passive: true });

  window.addEventListener('mouseout', (e) => {
    if (curEl && !e.relatedTarget) curEl.classList.add('is-out');
  });

  const HOT = 'a,button,.pin,.why,.member,.ag__row,.layer,.state,.rev__c,.ask__c';
  document.addEventListener('mouseover', (e) => {
    if (!curEl || !e.target.closest) return;
    curEl.classList.toggle('is-big', !!e.target.closest(HOT));
  });

  if (curEl) {
    document.body.classList.add('has-cursor');
    (function loop() {
      px += (mx - px) * 0.18;
      py += (my - py) * 0.18;
      curEl.style.transform = 'translate(' + px.toFixed(1) + 'px,' + py.toFixed(1) + 'px) translate(-50%,-50%)';
      requestAnimationFrame(loop);
    })();
  }

  /* ---------------------------------------------------------------- parallax da capa */
  const art = $('.s1__art');
  if (art && !reduce) {
    let ax = 0, ay = 0, tx = 0, ty = 0, raf = null;
    window.addEventListener('mousemove', (e) => {
      const r = art.getBoundingClientRect();
      tx = ((e.clientX - (r.left + r.width / 2)) / r.width) * 22;
      ty = ((e.clientY - (r.top + r.height / 2)) / r.height) * 22;
      if (!raf) raf = requestAnimationFrame(step);
    }, { passive: true });
    function step() {
      ax += (tx - ax) * 0.08;
      ay += (ty - ay) * 0.08;
      art.style.transform = 'translate(' + ax.toFixed(2) + 'px,' + ay.toFixed(2) + 'px)';
      raf = (Math.abs(tx - ax) + Math.abs(ty - ay) > 0.2) ? requestAnimationFrame(step) : null;
    }
  }

  /* ---------------------------------------------------------------- fluxo (06) */
  const flow = $('#flow');
  const flowFill = $('#flowFill');
  const flowDot = $('#flowDot');
  let flowStep = 0, flowTimer = null;

  function paintFlow() {
    if (!flow) return;
    const nodes = $$('.node', flow);
    nodes.forEach((n, i) => n.classList.toggle('on', i <= flowStep));
    if (flowFill) flowFill.style.width = ((flowStep + 1) / 4 * 100) + '%';
    if (flowDot) flowDot.style.left = (((flowStep + 0.5) / 4) * 100) + '%';
  }
  if (flow) {
    paintFlow();
    flowTimer = setInterval(() => {
      if (cur !== 5 || document.hidden) return;
      flowStep = (flowStep + 1) % 4;
      if (flowStep === 0) {
        $$('.node', flow).forEach((n) => n.classList.remove('on'));
        setTimeout(paintFlow, 120);
      } else {
        paintFlow();
      }
    }, 2400);
  }

  /* ---------------------------------------------------------------- estados (08) */
  const states = $('#states');
  let st = 0;
  if (states) {
    const pills = $$('.state', states);
    const paintState = () => pills.forEach((p, i) => p.classList.toggle('on', i === st));
    paintState();
    setInterval(() => {
      if (cur !== 7 || document.hidden) return;
      st = (st + 1) % pills.length;
      paintState();
    }, 1900);
  }

  /* ---------------------------------------------------------------- deep link */
  if (location.hash) {
    const target = document.querySelector(location.hash);
    if (target) {
      document.documentElement.style.scrollBehavior = 'auto';
      window.scrollTo(0, target.getBoundingClientRect().top + window.scrollY);
      requestAnimationFrame(() => { document.documentElement.style.scrollBehavior = ''; });
    }
  }

  /* ---------------------------------------------------------------- start */
  measure();
  window.addEventListener('load', measure);
  setTimeout(measure, 300);
  setTimeout(measure, 1200);
})();
