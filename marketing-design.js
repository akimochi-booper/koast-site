/* Open practical trip details when a native in-page link targets their section. */
(() => {
  function revealTarget() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    if (!id) return;
    const target = document.getElementById(id);
    if (!target) return;
    const details = target.closest('details.renewal-planning') || target.querySelector('details.renewal-planning');
    if (details) details.open = true;
  }
  addEventListener('hashchange', revealTarget);
  revealTarget();
})();
