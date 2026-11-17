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
  const idea = trip.tourId ? 'Suggested wine day: '+trip.tourTitle+'\nIdea reference: '+trip.tourId+'\n' : '';
  const vehicle = trip.vehicle ? 'Requested vehicle: '+trip.vehicle+' (subject to confirmation)\n' : '';
  const notes = String(trip.notes||'').slice(0,1200);
  const body = 'Hello Koast,\n\nPlease quote private transportation for these plans:\n\n'+idea+vehicle+'Wine country: '+trip.region+'\nPickup: '+trip.pickup+'\nTravel date: '+(trip.date||'To be confirmed')+'\nParty: '+party+'\n\nWinery appointments, pickup time, return and other requirements:\n'+notes+'\n\nPlease confirm the itinerary, vehicle, service window, total price and availability. I understand tasting reservations and fees are separate.\n';
  return 'mailto:'+email+'?subject='+encodeURIComponent(trip.region+' transportation quote request')+'&body='+encodeURIComponent(body);
}

function resolveWineDayIdea(id, catalogue) {
  if(!Array.isArray(catalogue)) return null;
  return catalogue.find(idea=>idea.id===id && idea.state==='exploratory' && idea.price_state==='team_quote') || null;
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
  const vehicleInput = dialog.querySelector('[data-review-vehicle]');
  const notesInput = dialog.querySelector('[data-review-notes]');
  let catalogue=[];
  try { catalogue=JSON.parse(document.getElementById('wine-day-catalog')?.textContent||'[]'); } catch { /* Generic team request remains available. */ }
  let lastForm,lastTrip,selectedIdea=null,requestedVehicle='',quoteOpener;
  function updateEmail() {
    if(!lastTrip) return;
    lastTrip.vehicle=requestedVehicle;
    lastTrip.notes=notesInput.value;
    dialog.querySelector('[data-quote-email]').href=buildWineQuoteEmail(dialog.dataset.email,lastTrip);
  }
  function updateSelectedLabels() {
    document.querySelectorAll('[data-selected-wine-day-label]').forEach(label=>{
      label.textContent=selectedIdea ? selectedIdea.title+(requestedVehicle?' · '+requestedVehicle:'') : '';
    });
  }
  vehicleInput.addEventListener('change',()=>{requestedVehicle=vehicleInput.value;updateSelectedLabels();updateEmail();});
  notesInput.addEventListener('input',updateEmail);
  function selectedDay(idea) {
    selectedIdea=idea;
    requestedVehicle=idea?.vehicle||'';
    document.querySelector('.reference-cinema-hero')?.classList.toggle('has-selected-day',Boolean(idea));
    document.querySelectorAll('[data-selected-wine-day]').forEach(note=>{
      note.hidden=!idea;
    });
    updateSelectedLabels();
  }
  document.querySelectorAll('[data-clear-wine-day]').forEach(button=>button.addEventListener('click',()=>{
    selectedDay(null);button.closest('form').querySelector('[name="pickup"]').focus();
  }));
  function startQuote(opener) {
    quoteOpener=opener;
    const inline=document.querySelector('form[data-wine-quote]');
    if(inputs) {
      review.hidden=true;inputs.hidden=false;dialog.showModal();inputs.querySelector('[name="pickup"]').focus();
    } else if(inline) {
      inline.scrollIntoView({block:'center',behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'instant':'smooth'});
      inline.querySelector('[name="pickup"]').focus({preventScroll:true});
    }
  }
  document.querySelectorAll('[data-plan-wine-day]').forEach(button=>button.addEventListener('click',()=>{
    const idea=resolveWineDayIdea(button.dataset.planWineDay,catalogue);
    if(!idea) return;
    selectedDay(idea);startQuote(button);
  }));
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
      if (result.error) {
        (result.field==='party' ? form.querySelector('.reference-party-button') || form.elements.namedItem('party') : form.elements.namedItem(result.field))?.focus();
        return;
      }
      const trip = result.trip;
      if(selectedIdea) Object.assign(trip,{tourId:selectedIdea.id,tourTitle:selectedIdea.title,region:selectedIdea.region});
      lastForm = form;
      lastTrip = trip;
      dialog.querySelector('[data-review-pickup]').textContent = trip.pickup;
      dialog.querySelector('[data-review-date]').textContent = formattedDate(trip.date);
      dialog.querySelector('[data-review-party]').textContent = trip.party==='7+' ? '7+ guests · group quote' : trip.party+' guest'+(trip.party==='1'?'':'s');
      dialog.querySelector('[data-review-region]').textContent=trip.region;
      dialog.querySelector('[data-review-day-row]').hidden=!selectedIdea;
      dialog.querySelector('[data-review-day]').textContent=selectedIdea?.title||'';
      vehicleInput.value=requestedVehicle;
      vehicleInput.dispatchEvent(new Event('change',{bubbles:true}));
      updateEmail();
      review.hidden = false;
      if (inputs) inputs.hidden = true;
      if (!dialog.open) dialog.showModal();
      dialog.querySelector('[data-quote-email]').focus();
    });
  });
  document.querySelectorAll('[data-start-quote]').forEach(link => link.addEventListener('click',event => {
    event.preventDefault();
    startQuote(link);
  }));
  dialog.addEventListener('close',()=>{if(inputs) quoteOpener?.focus();});
  dialog.querySelector('[data-close-quote]').addEventListener('click',() => dialog.close());
  dialog.querySelector('[data-edit-quote]').addEventListener('click',() => {
    if (inputs) {
      review.hidden = true;
      inputs.hidden = false;
      lastForm.querySelector('[name="pickup"]').focus();
    } else { dialog.close(); lastForm?.querySelector('[name="pickup"]').focus(); }
  });
})();
