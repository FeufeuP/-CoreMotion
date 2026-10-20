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
  const hudTotal = $('#hudTotal');
  const menu = $('#menu');
  const list = $('#menuList');
  const thumbList = $('#thumbList');
  const pptSlideStatus = $('#pptSlideStatus');
  const pptPageName = $('#pptPageName');

  if (hudTotal) hudTotal.textContent = '/' + String(N).padStart(2, '0');

  /* Miniaturas da interface de edição do PowerPoint. As ferramentas da fita
     são só visuais; as miniaturas continuam sendo navegação de slide. */
  if (thumbList) {
    scenes.forEach((scene, i) => {
      const li = document.createElement('li');
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'pptThumb';
      button.dataset.goto = String(i);
      button.setAttribute('aria-label', 'Ir ao slide ' + (i + 1) + ': ' + (scene.dataset.ch || ''));
      const title = scene.querySelector('.h1,.h2,.s0__word,.s12__r .big');
      const heading = (title ? title.textContent : scene.dataset.ch || 'CoreMotion')
        .replace(/\s+/g, ' ').trim().slice(0, 46);
      const accent = scene.classList.contains('scene--red') ? '#ff3333' :
                     scene.classList.contains('scene--blue') ? '#0066ff' : '#ff3333';
      button.style.setProperty('--thumb-accent', accent);
      button.innerHTML = '<span class="pptThumb__num">' + String(i + 1).padStart(2, '0') + '</span>' +
        '<span class="pptThumb__page"><i></i><b></b><strong></strong><em></em></span>' +
        '<span class="pptThumb__label">' + (scene.dataset.ch || 'Slide') + '</span>';
      button.querySelector('.pptThumb__page b').textContent = heading;
      button.querySelector('.pptThumb__page strong').textContent = scene.dataset.kicker || '';
      li.appendChild(button);
      thumbList.appendChild(li);
    });
    thumbList.addEventListener('click', (e) => {
      const button = e.target.closest('[data-goto]');
      if (button) goTo(Number(button.dataset.goto));
    });
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

  /* ---------------------------------------------------------------- palco */
  /* Slide 16:9 fixo, como um slide do PowerPoint: 1600x900 unidades de
     projeto, reduzidas por escala para caber na janela (letterbox em volta). */
  const STAGE_W = 1600;
  const STAGE_H = 900;
  const deck = $('#deck');

  const editorCanvas = $('#pptCanvas');
  function fitStage() {
    if (!deck) return;
    const vw = window.innerWidth || STAGE_W;
    const vh = window.innerHeight || STAGE_H;
    const baseW = Math.min(vw, vh * 16 / 9);
    const baseH = baseW * 9 / 16;
    const areaW = editorCanvas ? editorCanvas.clientWidth : vw;
    const areaH = editorCanvas ? editorCanvas.clientHeight : vh;
    const k = document.documentElement.classList.contains('is-presenting') ? 1 :
      Math.min(1, Math.max(.1, (areaW - 40) / baseW), Math.max(.1, (areaH - 32) / baseH));
    document.documentElement.style.setProperty('--editor-scale', k.toFixed(4));
  }
  fitStage();

  /* ---------------------------------------------------------------- navega */
  let cur = -1;
  let dir = 1;
  let animTimer = null;

  function clearAnim() {
    scenes.forEach((sc) => sc.classList.remove('is-in-next', 'is-in-prev', 'is-out-next', 'is-out-prev'));
  }

  function paint(i, animate) {
    const prev = cur;
    cur = i;

    clearTimeout(animTimer);
    clearAnim();

    scenes.forEach((sc, k) => sc.classList.toggle('on', k === i));

    if (animate && prev >= 0 && prev !== i) {
      const incoming = scenes[i];
      const outgoing = scenes[prev];
      incoming.classList.add(dir > 0 ? 'is-in-next' : 'is-in-prev');
      outgoing.classList.add(dir > 0 ? 'is-out-next' : 'is-out-prev');
      outgoing.classList.remove('on');
      animTimer = setTimeout(clearAnim, 760);
    }

    if (hudCh) hudCh.textContent = scenes[i].dataset.ch || '';
    if (hudNum) hudNum.textContent = String(i + 1).padStart(2, '0');
    if (hud) {
      hud.classList.add('hud--light');           // tema escuro em todos os slides
      hud.classList.remove('hud--split');
      hud.classList.toggle('hud--red', scenes[i].classList.contains('scene--red'));
      hud.classList.toggle('hud--blue', scenes[i].classList.contains('scene--blue'));
    }
    if (progFill) progFill.style.width = (N > 1 ? (i / (N - 1)) * 100 : 100) + '%';
    if (list) $$('li', list).forEach((li, k) => li.classList.toggle('is-now', k === i));
    if (thumbList) $$('.pptThumb', thumbList).forEach((button, k) => {
      const selected = k === i;
      button.classList.toggle('is-selected', selected);
      if (selected) {
        button.setAttribute('aria-current', 'page');
        button.scrollIntoView({ block: 'nearest' });
      } else button.removeAttribute('aria-current');
    });
    if (pptSlideStatus) pptSlideStatus.textContent = 'Slide ' + (i + 1) + ' de ' + N;
    if (pptPageName) pptPageName.textContent = scenes[i].dataset.ch || '';
    if (history.replaceState) history.replaceState(null, '', '#' + scenes[i].id);
  }

  function goTo(i, animate) {
    i = Math.max(0, Math.min(N - 1, i));
    if (i === cur) return;
    dir = i > cur ? 1 : -1;
    paint(i, animate !== false);
  }

  /* ---------------------------------------------------------------- teclado */  /* ---------------------------------------------------------------- teclado */
  window.addEventListener('keydown', (e) => {
    const tag = (e.target.tagName || '').toLowerCase();
    if (tag === 'input' || tag === 'textarea') return;

    /* F5 / Shift+F5: apresentar do começo / do slide atual */
    if (e.key === 'F5') {
      e.preventDefault();
      if (presenting) stopPresent(); else startPresent(!e.shiftKey);
      return;
    }
    if (e.key === 'Escape' && presenting) {
      e.preventDefault();
      if (pshowMenu && !pshowMenu.hidden) closePshowMenu();
      else stopPresent();
      return;
    }

    if (isOpen()) {
      if (e.key === 'Escape') { e.preventDefault(); closeMenu(); }
      return;
    }

    /* dentro da apresentação: passagem de slides do PowerPoint */
    if (presenting) {
      if (/^[0-9]$/.test(e.key)) { e.preventDefault(); typeGoto(e.key); return; }
      if (e.key === 'Enter') {
        e.preventDefault();
        if (gotoBuf) goToNumber();
        else goTo(currentIndex() + 1);
        wakeHud();
        return;
      }
      if (e.key === ' ' || e.key === 'ArrowRight' || e.key === 'ArrowDown' ||
          e.key === 'PageDown' || e.key === 'n' || e.key === 'N') {
        e.preventDefault(); goTo(currentIndex() + 1); wakeHud();
      } else if (e.key === 'Backspace' || e.key === 'ArrowLeft' || e.key === 'ArrowUp' ||
                 e.key === 'PageUp' || e.key === 'p' || e.key === 'P') {
        e.preventDefault(); goTo(currentIndex() - 1); wakeHud();
      } else if (e.key === 'Home') {
        e.preventDefault(); goTo(0); wakeHud();
      } else if (e.key === 'End') {
        e.preventDefault(); goTo(N - 1); wakeHud();
      }
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

  /* ---------------------------------------------------------------- apresentação */
  /* HUD do PowerPoint: barra inferior esquerda + botão de apresentar.
     Só a apresentação (tela cheia) e a passagem de slides funcionam — caneta,
     ver todos, zoom e legendas são o desenho do HUD, como pedido. */
  const presentBtn = $('#presentBtn');
  const pshow = $('#pshow');
  const pshowMenu = $('#pshowMenu');
  const pshowGoto = $('#pshowGoto');
  const moreBtn = pshow ? pshow.querySelector('[data-ps="more"]') : null;

  let presenting = false;
  let hudTimer = null;
  let idleTimer = null;
  let gotoBuf = '';
  let gotoTimer = null;

  function currentIndex() { return cur < 0 ? 0 : cur; }

  function wakeHud() {
    if (!presenting || !pshow) return;
    pshow.classList.add('on');
    pshow.setAttribute('aria-hidden', 'false');
    clearTimeout(hudTimer);
    hudTimer = setTimeout(() => {
      const busy = pshow.matches(':hover') || pshow.contains(document.activeElement) ||
                   (pshowMenu && !pshowMenu.hidden);
      if (busy) { wakeHud(); return; }
      pshow.classList.remove('on');
      pshow.setAttribute('aria-hidden', 'true');
    }, 2800);
  }

  function wakeCursor() {
    document.documentElement.classList.remove('is-idle');
    clearTimeout(idleTimer);
    if (!presenting) return;
    idleTimer = setTimeout(() => {
      if (pshow && pshow.matches(':hover')) { wakeCursor(); return; }
      document.documentElement.classList.add('is-idle');
    }, 2200);
  }

  function openPshowMenu() {
    if (!pshowMenu) return;
    pshowMenu.hidden = false;
    if (moreBtn) moreBtn.setAttribute('aria-expanded', 'true');
    wakeHud();
  }
  function closePshowMenu() {
    if (!pshowMenu) return;
    pshowMenu.hidden = true;
    if (moreBtn) moreBtn.setAttribute('aria-expanded', 'false');
  }
  function togglePshowMenu() {
    if (!pshowMenu) return;
    if (pshowMenu.hidden) openPshowMenu(); else closePshowMenu();
  }

  function showGoto() {
    if (!pshowGoto) return;
    clearTimeout(gotoTimer);
    if (!gotoBuf) { pshowGoto.hidden = true; return; }
    pshowGoto.innerHTML = 'Slide <i>' + gotoBuf + '</i> + Enter';
    pshowGoto.hidden = false;
    gotoTimer = setTimeout(() => { gotoBuf = ''; pshowGoto.hidden = true; }, 2400);
  }
  function typeGoto(d) {
    gotoBuf = (gotoBuf + d).replace(/^0+(?=\d)/, '').slice(0, 3) || '0';
    showGoto();
  }
  function goToNumber() {
    const n = parseInt(gotoBuf, 10);
    gotoBuf = '';
    if (pshowGoto) pshowGoto.hidden = true;
    if (n >= 1 && n <= N) goTo(n - 1);
    wakeHud();
  }

  function startPresent(fromStart) {
    if (presenting) return;
    presenting = true;
    closeMenu();
    closePshowMenu();
    document.documentElement.classList.add('is-presenting');
    goTo(fromStart ? 0 : currentIndex());
    const el = document.documentElement;
    if (el.requestFullscreen) {
      const p = el.requestFullscreen({ navigationUI: 'hide' });
      if (p && p.catch) p.catch(() => {});   // iframe sem allowfullscreen: segue em tela cheia falsa
    }
    wakeHud();
    wakeCursor();
    setTimeout(fitStage, 140);
  }

  function stopPresent() {
    if (!presenting) return;
    presenting = false;
    closePshowMenu();
    document.documentElement.classList.remove('is-presenting', 'is-idle');
    if (pshow) { pshow.classList.remove('on'); pshow.setAttribute('aria-hidden', 'true'); }
    clearTimeout(hudTimer);
    clearTimeout(idleTimer);
    gotoBuf = '';
    if (pshowGoto) pshowGoto.hidden = true;
    if (document.fullscreenElement && document.exitFullscreen) {
      document.exitFullscreen().catch(() => {});
    }
  }

  if (presentBtn) presentBtn.addEventListener('click', () => startPresent(false));
  $$('.pptPresent').forEach((button) => {
    button.addEventListener('click', () => startPresent(button.dataset.from === 'start'));
  });

  if (pshow) {
    pshow.addEventListener('click', (e) => {
      const b = e.target.closest('[data-ps]');
      if (!b) return;
      const act = b.dataset.ps;
      if (act === 'prev') { closePshowMenu(); goTo(currentIndex() - 1); }
      else if (act === 'next') { closePshowMenu(); goTo(currentIndex() + 1); }
      else if (act === 'more') togglePshowMenu();
      else if (act === 'end') { closePshowMenu(); stopPresent(); }
      wakeHud();
    });
  }

  if (pshowMenu) {
    pshowMenu.addEventListener('click', (e) => {
      const b = e.target.closest('[data-ps="end"]');
      if (b) { closePshowMenu(); stopPresent(); }
    });
  }

  /* clique no slide avança, como no PowerPoint */
  document.addEventListener('click', (e) => {
    if (!presenting) return;
    if (e.target.closest('.pshow, .pshow__menu, .pshow__goto')) return;
    if (e.target.closest('a, button, input, textarea, select, .menu')) return;
    if (pshowMenu && !pshowMenu.hidden) { closePshowMenu(); return; }
    goTo(currentIndex() + 1);
    wakeHud();
  });

  window.addEventListener('mousemove', () => {
    if (!presenting) return;
    wakeHud();
    wakeCursor();
  }, { passive: true });

  document.addEventListener('fullscreenchange', () => {
    if (presenting && !document.fullscreenElement) stopPresent();
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


  /* ---------------------------------------------------------------- fx 3D */
  /* Relevo 3D monocromático: cada ícone é um <symbol> com a silhueta
     "extrudada" (5 cópias deslocadas + a face por cima, tudo na mesma cor).
     As cenas recebem uma camada .fx3d com 7 peças soltas; a última cena fica
     limpa. A cor vem da cena (fx.css), nunca do ícone. */

  const FX_ICONS = {
    /* tênis — perfil, bico à esquerda */
    sneaker: [
      'M3 68 L97 68 L97 77 C97 81 94 83 90 83 L10 83 C6 83 3 81 3 77 Z',
      'M4 66 C5 62 8 58 13 55 C22 50 32 47 40 42 C46 38 49 33 52 27 C54 24 58 23 61 25 L68 29 C70 31 71 34 71 37 L71 49 L88 56 C93 58 96 61 96 65 L96 66 L4 66 Z',
      'M71 42 C79 45 86 48 92 51 L92 54 C86 51 78 48 71 46 Z'
    ],
    /* camisa esportiva */
    jersey: [
      'M32 12 L42 8 C46 17 54 17 58 8 L68 12 L88 26 L79 40 L70 34 L70 90 L30 90 L30 34 L21 40 L12 26 Z'
    ],
    /* boné */
    cap: [
      'M14 60 C14 35 30 18 50 18 C70 18 86 35 86 60 Z',
      'M86 60 C96 60 100 66 100 71 L14 71 C14 65 18 60 26 60 Z',
      'M50 10 a4 4 0 1 0 .01 0 Z'
    ],
    /* garrafa */
    bottle: [
      'M40 4 h20 v14 h-20 z',
      'M38 22 L62 22 L62 30 C68 33 70 38 70 44 L70 88 C70 92 67 95 63 95 L37 95 C33 95 30 92 30 88 L30 44 C30 38 32 33 38 30 Z'
    ],
    /* halter */
    dumbbell: [
      'M8 30 h11 v40 h-11 z',
      'M81 30 h11 v40 h-11 z',
      'M19 36 h10 v28 h-10 z',
      'M71 36 h10 v28 h-10 z',
      'M29 44 h42 v12 h-42 z'
    ],
    /* medalha */
    medal: [
      'M34 6 L46 6 L58 43 L50 50 Z',
      'M66 6 L54 6 L42 43 L50 50 Z',
      'M50 44 a24 24 0 1 0 .01 0 Z M50 53 L53.5 62.9 L64 63.3 L55.6 69.8 L58.6 79.9 L50 73.8 L41.4 79.9 L44.4 69.8 L36 63.3 L46.5 62.9 Z'
    ],
    /* relógio / smartband */
    watch: [
      'M40 6 h20 v22 h-20 z',
      'M40 70 h20 v24 h-20 z',
      'M70 41 h7 v12 h-7 z',
      'M39 26 H61 A9 9 0 0 1 70 35 V63 A9 9 0 0 1 61 72 H39 A9 9 0 0 1 30 63 V35 A9 9 0 0 1 39 26 Z M38 38 H62 V60 H38 Z'
    ],
    /* faixa de cabeça */
    headband: [
      'M6 66 C6 34 25 14 50 14 C75 14 94 34 94 66 L74 66 C74 46 63 34 50 34 C37 34 26 46 26 66 Z'
    ],
    /* mochila */
    backpack: [
      'M24 36 C24 24 32 16 42 16 H58 C68 16 76 24 76 36 V88 C76 92 73 95 69 95 H31 C27 95 24 92 24 88 Z M34 62 H66 V86 H34 Z',
      'M42 16 C42 5 58 5 58 16 L53 16 C53 11 47 11 47 16 Z'
    ],
    /* óculos escuros */
    sunglasses: [
      'M4 38 a8 8 0 0 1 8 -8 h24 a8 8 0 0 1 8 8 v14 a8 8 0 0 1 -8 8 h-24 a8 8 0 0 1 -8 -8 Z',
      'M56 38 a8 8 0 0 1 8 -8 h24 a8 8 0 0 1 8 8 v14 a8 8 0 0 1 -8 8 h-24 a8 8 0 0 1 -8 -8 Z',
      'M44 40 h12 v6 h-12 z',
      'M0 36 h4 v6 h-4 z',
      'M96 36 h4 v6 h-4 z'
    ],
    /* bola */
    ball: [
      'M50 8 a42 42 0 1 0 .01 0 Z' +
      ' M50 33 L60.5 40.6 L56.5 52.9 H43.5 L39.5 40.6 Z' +
      ' M21 28 L29.4 34.1 L26.2 44.2 H15.8 L12.6 34.1 Z' +
      ' M79 28 L87.4 34.1 L84.2 44.2 H73.8 L70.6 34.1 Z' +
      ' M50 74 L58.4 80.1 L55.2 90.2 H44.8 L41.6 80.1 Z'
    ],
    /* raquete */
    racket: [
      'M50 6 C67 6 80 19 80 36 C80 53 67 64 50 64 C33 64 20 53 20 36 C20 19 33 6 50 6 Z M50 14 C38 14 29 23 29 36 C29 49 38 57 50 57 C62 57 71 49 71 36 C71 23 62 14 50 14 Z',
      'M45 62 h10 l3 32 h-16 z'
    ]
  };

  function mulberry32(a) {
    return function () {
      a |= 0; a = a + 0x6D2B79F5 | 0;
      let t = Math.imul(a ^ a >>> 15, 1 | a);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }

  const SVG_NS = 'http://www.w3.org/2000/svg';
  const XLINK_NS = 'http://www.w3.org/1999/xlink';
  function svgEl(name, attrs) {
    const n = document.createElementNS(SVG_NS, name);
    if (attrs) for (const k in attrs) {
      n.setAttribute(k, attrs[k]);
      if (k === 'href') n.setAttributeNS(XLINK_NS, 'xlink:href', attrs[k]);   // Safari/engine antiga
    }
    return n;
  }

  function fxSprite() {
    const svg = svgEl('svg', { width: '0', height: '0', 'aria-hidden': 'true', focusable: 'false' });
    svg.setAttribute('fill-rule', 'evenodd');
    svg.setAttribute('fill', 'currentColor');
    svg.style.position = 'absolute';
    const defs = svgEl('defs');

    Object.keys(FX_ICONS).forEach((name) => {
      const face = svgEl('g', { id: 'fxp-' + name });
      FX_ICONS[name].forEach((d) => face.appendChild(svgEl('path', { d })));
      defs.appendChild(face);

      // relevo: 5 cópias deslocadas para o canto + a face por cima
      const sym = svgEl('symbol', { id: 'fx-' + name, viewBox: '0 0 112 112' });
      for (let k = 5; k >= 1; k--) {
        sym.appendChild(svgEl('use', {
          href: '#fxp-' + name, x: (k * 2).toFixed(1), y: (k * 2).toFixed(1), opacity: '.42'
        }));
      }
      sym.appendChild(svgEl('use', { href: '#fxp-' + name }));
      defs.appendChild(sym);
    });

    svg.appendChild(defs);
    document.body.appendChild(svg);
  }

  /* paleta do deck: cada peça recebe UMA cor, sorteada entre as cores do slide */
  const PALETTES = {
    paper: ['#ff3333', '#0066ff', '#00cc00', '#cc00cc', '#ffff00', '#ffffff'],
    dark:  ['#ffff00', '#ff3333', '#0066ff', '#00cc00', '#cc00cc', '#ffffff'],
    red:   ['#ffff00', '#ffffff', '#0066ff', '#00cc00', '#cc00cc'],
    blue:  ['#ffff00', '#ffffff', '#ff3333', '#00cc00', '#cc00cc'],
    split: ['#ff3333', '#0066ff', '#00cc00', '#cc00cc', '#ffff00', '#ffffff']
  };

  function paletteOf(scene) {
    if (scene.classList.contains('scene--dark')) return PALETTES.dark;
    if (scene.classList.contains('scene--red')) return PALETTES.red;
    if (scene.classList.contains('scene--blue')) return PALETTES.blue;
    if (scene.classList.contains('s12')) return PALETTES.split;
    return PALETTES.paper;
  }

  function mountFx() {
    const all = $$('.scene');
    if (!all.length) return;
    fxSprite();

    const names = Object.keys(FX_ICONS);
    const small = window.matchMedia('(max-width:760px)').matches;
    const vw = window.innerWidth || 1280;
    const count = small ? 4 : 7;

    all.forEach((scene, si) => {
      if (si === all.length - 1) return;              // último slide: sem decoração
      if (scene.dataset.fx === 'off') return;

      const layer = document.createElement('div');
      layer.className = 'fx3d';
      layer.setAttribute('aria-hidden', 'true');

      const soft = scene.dataset.fx === 'soft';   // capa: peças menores, mais discreta
      const pal = paletteOf(scene);
      const rand = mulberry32(9137 + si * 7919);
      const used = [];
      const bag = [];
      const colorBag = [];
      const total = soft ? Math.max(4, count - 2) : count;

      for (let i = 0; i < total; i++) {
        let l = 0, t = 0, guard = 0;
        do {
          l = 12 + rand() * 63;
          t = 10 + rand() * 70;
          guard++;
        } while (guard < 26 && used.some((p) => Math.hypot(p[0] - l, p[1] - t) < 21));
        used.push([l, t]);

        if (!bag.length) {                   // reabastece sem repetir na mesma cena
          bag.push.apply(bag, names);
          for (let j = bag.length - 1; j > 0; j--) {
            const k = Math.floor(rand() * (j + 1));
            const tmp = bag[j]; bag[j] = bag[k]; bag[k] = tmp;
          }
        }
        const name = bag.pop();
        if (!colorBag.length) {              // uma cor de cada vez: variedade garantida
          colorBag.push.apply(colorBag, pal);
          for (let j = colorBag.length - 1; j > 0; j--) {
            const k = Math.floor(rand() * (j + 1));
            const tmp = colorBag[j]; colorBag[j] = colorBag[k]; colorBag[k] = tmp;
          }
        }
        const color = colorBag.pop();
        const w = Math.round((small ? 58 : 100) + rand() * (small ? 70 : Math.min(150, vw * 0.105)))
                    * (soft ? 0.62 : 1);
        const dur = 8 + rand() * 9;
        const drift = (18 + rand() * 12) * (rand() > 0.5 ? 1 : -1);
        const rise = (8 + rand() * 8) * (rand() > 0.5 ? 1 : -1);
        const z = Math.round(-240 + rand() * 330);
        const turn = 9 + rand() * 8;
        const rx = rand() * 20 - 10, ry = rand() * 36 - 18, rz = rand() * 30 - 15;

        const item = document.createElement('div');
        item.className = 'fx';
        item.style.cssText =
          '--l:' + l.toFixed(2) + '%;' +
          '--t:' + t.toFixed(2) + '%;' +
          '--fx:' + color + ';' +
          '--w:' + w + 'px;' +
          '--dx:' + drift.toFixed(1) + 'vw;' +
          '--dy:' + rise.toFixed(1) + 'vh;' +
          '--z:' + z + 'px;' +
          '--dur:' + dur.toFixed(1) + 's;' +
          '--del:' + (-rand() * dur).toFixed(1) + 's;' +
          '--bob:' + (6 + rand() * 16).toFixed(1) + 'px;' +
          '--bdur:' + (5 + rand() * 4).toFixed(1) + 's;' +
          '--bdel:' + (-rand() * 10).toFixed(1) + 's;' +
          '--fo:' + (0.72 + rand() * 0.55).toFixed(2) + ';';

        const inner = document.createElement('div');
        inner.className = 'fx__in';
        inner.style.cssText =
          '--tdur:' + turn.toFixed(1) + 's;' +
          '--tdel:' + (-rand() * turn).toFixed(1) + 's;' +
          '--rx:' + rx.toFixed(1) + 'deg;--rx2:' + (rx + (rand() * 10 - 5)).toFixed(1) + 'deg;' +
          '--ry:' + ry.toFixed(1) + 'deg;--ry2:' + (ry + (rand() * 26 - 13)).toFixed(1) + 'deg;' +
          '--rz:' + rz.toFixed(1) + 'deg;--rz2:' + (rz + (rand() * 16 - 8)).toFixed(1) + 'deg;' +
          '--sx:' + (rand() > 0.5 ? -1 : 1) + ';';

        const svg = svgEl('svg', { viewBox: '0 0 112 112', 'aria-hidden': 'true' });
        svg.appendChild(svgEl('use', { href: '#fx-' + name }));
        inner.appendChild(svg);
        item.appendChild(inner);
        layer.appendChild(item);
      }

      scene.insertBefore(layer, scene.firstChild);
    });
  }
  mountFx();

  /* ---------------------------------------------------------------- deep link */
  function fromHash() {
    const id = (location.hash || '').replace('#', '');
    const i = id ? scenes.findIndex((sc) => sc.id === id) : -1;
    return i >= 0 ? i : 0;
  }

  /* ---------------------------------------------------------------- start */
  document.documentElement.classList.add('is-stage');
  paint(fromHash(), false);

  window.addEventListener('resize', fitStage);
  window.addEventListener('load', fitStage);
  window.addEventListener('fullscreenchange', () => setTimeout(fitStage, 60));

  /* roda do mouse: passagem de slide, um por gesto (como no PowerPoint) */
  let wheelAt = 0;
  window.addEventListener('wheel', (e) => {
    if (pshowMenu && !pshowMenu.hidden) return;
    if (Math.abs(e.deltaY) < 4) return;
    e.preventDefault();
    const now = Date.now();
    if (now - wheelAt < 420) return;
    wheelAt = now;
    goTo(currentIndex() + (e.deltaY > 0 ? 1 : -1));
    if (presenting) wakeHud();
  }, { passive: false });

  /* swipe em tela de toque */
  let tX = 0, tY = 0, touchOn = false;
  window.addEventListener('touchstart', (e) => {
    if (e.touches.length !== 1) return;
    touchOn = true;
    tX = e.touches[0].clientX;
    tY = e.touches[0].clientY;
  }, { passive: true });
  window.addEventListener('touchend', (e) => {
    if (!touchOn) return;
    touchOn = false;
    const t = e.changedTouches[0];
    const dx = t.clientX - tX;
    const dy = t.clientY - tY;
    if (Math.max(Math.abs(dx), Math.abs(dy)) < 46) return;
    goTo(currentIndex() + ((dy < 0 || dx < -46) ? 1 : -1));
    if (presenting) wakeHud();
  }, { passive: true });
})();
