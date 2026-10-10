/* Koast first-party acquisition events. No cookies, form values, or persistent visitor ID. */
(function () {
  'use strict';
  if (window.__koastAcquisitionLoaded) return;
  window.__koastAcquisitionLoaded = true;
  var ENDPOINT = 'https://koast-platform.euburaga.workers.dev/api/acquisition/events';
  var KEY = 'koast_acquisition_v1', OFF = 'koast_tracking_off', IDLE = 30 * 60 * 1000;
  var memory = null, disabled = false;
  var hosts = ['koastride.com', 'www.koastride.com'];
  if (location.protocol !== 'https:' || hosts.indexOf(location.hostname) < 0) return;
  function read(key) { try { return sessionStorage.getItem(key); } catch (_) { return null; } }
  function write(key, value) { try { sessionStorage.setItem(key, value); } catch (_) {} }
  var params = new URLSearchParams(location.search);
  if (params.get('koast_tracking') === 'off') { disabled = true; write(OFF, '1'); }
  function optedOut() { return disabled || read(OFF) === '1' || navigator.doNotTrack === '1' || window.doNotTrack === '1' || navigator.globalPrivacyControl === true; }
  if (optedOut()) return;
  function uuid() { return crypto.randomUUID(); }
  function label(value) {
    value = String(value || '').trim();
    // Campaign labels only: reject addresses, long number sequences, URLs, and arbitrary query data.
    if (!value || value.length > 100 || /[@:/?=&%]|\d{7}/.test(value) || !/^[a-zA-Z0-9 _.,()+-]+$/.test(value)) return '';
    return value;
  }
  function referrer(value) {
    try {
      var u = new URL(value);
      return /^https?:$/.test(u.protocol) && hosts.indexOf(u.hostname) < 0 ? u.origin : '';
    } catch (_) { return ''; }
  }
  function path() {
    // Canonical URLs identify generated public pages; unknown 404 paths may contain personal data.
    var canonical = document.querySelector('link[rel="canonical"]');
    try { var u = new URL(canonical.href); return hosts.indexOf(u.hostname) >= 0 ? u.pathname : '/404'; } catch (_) { return '/404'; }
  }
  function touch() {
    return { source: label(params.get('utm_source')), medium: label(params.get('utm_medium')),
      campaign: label(params.get('utm_campaign')), content: label(params.get('utm_content')),
      term: label(params.get('utm_term')), path: path(), referrer: referrer(document.referrer) };
  }
  function cleanTouch(t) {
    t = t || {};
    return {source: label(t.source), medium: label(t.medium), campaign: label(t.campaign),
      content: label(t.content), term: label(t.term),
      path: /^\/[a-zA-Z0-9/_-]*(?:\.html)?$/.test(t.path || '') ? t.path.slice(0, 240) : '/', referrer: referrer(t.referrer)};
  }
  function session() {
    var now = Date.now(), s = memory;
    if (!s) { try { s = JSON.parse(read(KEY)); } catch (_) {} }
    if (!s || !/^[0-9a-f-]{36}$/i.test(s.id || '') || !Number.isFinite(s.last) || now - s.last >= IDLE || s.last > now) {
      var t = touch(); s = {id: uuid(), last: now, first_touch: t, touch: t};
    } else {
      s.first_touch = cleanTouch(s.first_touch); s.touch = cleanTouch(s.touch);
      var current = touch();
      if (current.source || current.medium || current.campaign || current.referrer) s.touch = current;
    }
    s.last = now; memory = s; write(KEY, JSON.stringify(s)); return s;
  }
  function track(event, destination) {
    if (optedOut()) return;
    try {
      var s = session(), t = s.touch;
      var payload = {version: 1, event_id: uuid(), event: event, session_id: s.id,
        path: path(), referrer: t.referrer, utm_source: t.source, utm_medium: t.medium,
        utm_campaign: t.campaign, utm_content: t.content, utm_term: t.term,
        first_touch: {source: s.first_touch.source, medium: s.first_touch.medium, campaign: s.first_touch.campaign,
          path: s.first_touch.path, referrer: s.first_touch.referrer}, destination: destination || ''};
      // A simple cross-origin POST avoids a preflight. Never delay or cancel navigation.
      fetch(ENDPOINT, {method: 'POST', mode: 'cors', credentials: 'omit', keepalive: true,
        referrerPolicy: 'no-referrer', headers: {'Content-Type': 'text/plain;charset=UTF-8'}, body: JSON.stringify(payload)}).catch(function () {});
    } catch (_) { /* Tracking failure must never affect browsing or booking. */ }
  }
  track('page_view', '');
  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    try {
      var u = new URL(a.href, location.href);
      if (u.protocol === 'tel:' || u.protocol === 'mailto:') track('contact_click', u.protocol === 'tel:' ? 'phone' : 'email');
      else if (u.protocol === 'https:' && u.hostname === 'customer.moovs.app' && /^\/koast(?:\/|$)/.test(u.pathname)) track('booking_click', 'moovs');
      else if (u.protocol === 'https:' && u.hostname === 'app.koastride.com' && /^\/(?:book|booking|request)(?:\/|$)/.test(u.pathname)) track('booking_click', 'book');
    } catch (_) {}
  });
})();
