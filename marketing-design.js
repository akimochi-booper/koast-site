/* Quote planning stays in the page. Only the visitor opens an email draft or
   the existing booking destination; no form values enter storage or analytics. */
function validateWineTrip(values, today) {
  const pickup = String(values.pickup || '').trim();
  const party = String(values.party || '');
  const date = String(values.date || '');
  if (!pickup || pickup.length > 180) return {error:'Enter your pickup location.',field:'pickup'};
  if (!/^(?:[1-6]|7\+)$/.test(party)) return {error:'Choose your party size.',field:'party'};
  if (date || !values.dateOptional) {
    const parsed = new Date(date+'T12:00:00Z');
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || !Number.isFinite(parsed.getTime()) || parsed.toISOString().slice(0,10)!==date || date < today) {
      return {error:'Choose today or a future travel date.',field:'date'};
    }
  }
  return {trip:{pickup,party,date,region:String(values.region || '').slice(0,100)}};
}

function buildWineQuoteEmail(email, trip) {
  const party = trip.party === '7+' ? '7+ guests (group quote)' : trip.party+' guest'+(trip.party==='1'?'':'s');
  const body = 'Hello Koast,\n\nPlease quote private transportation for these plans:\n\nWine country: '+trip.region+'\nPickup: '+trip.pickup+'\nTravel date: '+(trip.date||'To be confirmed')+'\nParty: '+party+'\n\nWinery appointments, pickup time, return and other requirements:\n\nPlease confirm the vehicle, route, service window, total price and availability. I understand tasting reservations and fees are separate.\n';
  return 'mailto:'+email+'?subject='+encodeURIComponent(trip.region+' transportation quote request')+'&body='+encodeURIComponent(body);
}

(() => {
  if (typeof document === 'undefined') return;
  function revealTarget() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    if (!id) return;
    const target = document.getElementById(id);
    if (!target) return;
    const details = target.closest('details.renewal-planning, details.reference-more') || target.querySelector('details.renewal-planning');
    if (details) details.open = true;
    const supplement = target.closest('details.reference-more');
    if (supplement) supplement.open = true;
  }
  addEventListener('hashchange', revealTarget);
  revealTarget();
  const dialog = document.getElementById('quote-request');
  if (!dialog) return;
  const review = dialog.querySelector('[data-quote-review]');
  const inputs = dialog.querySelector('[data-quote-inputs]');
  let lastForm;
  const now = new Date();
  const today = [now.getFullYear(),String(now.getMonth()+1).padStart(2,'0'),String(now.getDate()).padStart(2,'0')].join('-');
  const formattedDate = date => date ? new Intl.DateTimeFormat(undefined,{month:'long',day:'numeric',year:'numeric'}).format(new Date(date+'T12:00:00')) : 'To be confirmed';
  document.querySelectorAll('[data-wine-quote]').forEach(form => {
    const date = form.elements.namedItem('date');
    if (date) {
      date.min = today;
      date.addEventListener('change',() => {
        const label = form.querySelector('[data-date-label]');
        if (label) label.textContent = date.value ? new Intl.DateTimeFormat(undefined,{month:'short',day:'numeric'}).format(new Date(date.value+'T12:00:00')) : 'Date';
      });
    }
    form.querySelector('button[type="submit"]').disabled = false;
    form.addEventListener('submit',event => {
      event.preventDefault();
      const result = validateWineTrip({pickup:form.elements.namedItem('pickup').value,date:date?.value||'',party:form.elements.namedItem('party').value,dateOptional:form.dataset.dateOptional==='true',region:form.dataset.region},today);
      const status = form.querySelector('[role="status"]');
      status.textContent = result.error || '';
      if (result.error) { form.elements.namedItem(result.field)?.focus(); return; }
      const trip = result.trip;
      lastForm = form;
      dialog.querySelector('[data-review-pickup]').textContent = trip.pickup;
      dialog.querySelector('[data-review-date]').textContent = formattedDate(trip.date);
      dialog.querySelector('[data-review-party]').textContent = trip.party==='7+' ? '7+ guests · group quote' : trip.party+' guest'+(trip.party==='1'?'':'s');
      dialog.querySelector('[data-quote-email]').href = buildWineQuoteEmail(dialog.dataset.email,trip);
      review.hidden = false;
      if (inputs) inputs.hidden = true;
      if (!dialog.open) dialog.showModal();
      dialog.querySelector('[data-quote-email]').focus();
    });
  });
  document.querySelectorAll('[data-start-quote]').forEach(link => link.addEventListener('click',event => {
    event.preventDefault();
    const inline = document.querySelector('form[data-wine-quote]');
    if (inputs) {
      review.hidden = true;
      inputs.hidden = false;
      dialog.showModal();
      inputs.querySelector('[name="pickup"]').focus();
    } else if (inline) {
      inline.scrollIntoView({block:'center',behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'instant':'smooth'});
      inline.querySelector('[name="pickup"]').focus({preventScroll:true});
    }
  }));
  dialog.querySelector('[data-close-quote]').addEventListener('click',() => dialog.close());
  dialog.querySelector('[data-edit-quote]').addEventListener('click',() => {
    if (inputs) {
      review.hidden = true;
      inputs.hidden = false;
      lastForm.querySelector('[name="pickup"]').focus();
    } else { dialog.close(); lastForm?.querySelector('[name="pickup"]').focus(); }
  });
})();
