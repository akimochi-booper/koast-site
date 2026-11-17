/* Quote planning stays in the page. Explicit Send submits the team enquiry;
   contact/trip fields stay out of browser persistence and analytics. */
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
  const reference = trip.requestId ? 'Website request reference: '+trip.requestId+'\nPlease check the status before treating this as another request.\n\n' : '';
  const body = 'Hello Koast,\n\nPlease quote private transportation for these plans:\n\n'+reference+idea+vehicle+'Wine country: '+trip.region+'\nPickup: '+trip.pickup+'\nTravel date: '+(trip.date||'To be confirmed')+'\nParty: '+party+'\n\nWinery appointments, pickup time, return and other requirements:\n'+notes+'\n\nPlease confirm the itinerary, vehicle, service window, total price and availability. I understand tasting reservations and fees are separate.\n';
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
  const nameInput=dialog.querySelector('[data-quote-name]');
  const emailInput=dialog.querySelector('[data-quote-contact-email]');
  const sendButton=dialog.querySelector('[data-send-quote]');
  const quoteStatus=dialog.querySelector('[data-quote-status]');
  const success=dialog.querySelector('[data-quote-success]');
  const submission=createQuoteSubmission();
  let catalogue=[];
  try { catalogue=JSON.parse(document.getElementById('wine-day-catalog')?.textContent||'[]'); } catch { /* Generic team request remains available. */ }
  let lastForm,lastTrip,selectedIdea=null,requestedVehicle='',quoteOpener;
  function updateEmail() {
    if(!lastTrip) return;
    lastTrip.vehicle=requestedVehicle;
    lastTrip.notes=notesInput.value;
    lastTrip.requestId=submission.state().reference;
    dialog.querySelector('[data-quote-email-fallback]').href=buildWineQuoteEmail(dialog.dataset.email,lastTrip);
  }
  function renderSubmissionState() {
    const state=submission.state();
    updateEmail();
    [nameInput,emailInput,notesInput,vehicleInput].forEach(field=>{field.disabled=state.locked||state.pending;});
    const vehicleButton=vehicleInput.parentElement.querySelector('.reference-choice-button');
    if(vehicleButton)vehicleButton.disabled=vehicleInput.disabled;
    dialog.querySelector('[data-edit-quote]').disabled=state.locked||state.pending;
    sendButton.disabled=state.pending||state.expired;
    sendButton.setAttribute('aria-busy',String(state.pending));
    sendButton.textContent=state.pending?'Sending request…':state.locked?'Retry sending request':'Send quote request';
    dialog.querySelector('#quote-dialog-title').textContent=state.accepted?'Request sent.':"Let's plan your wine day.";
    dialog.querySelector('.reference-book-online:not([data-quote-email-fallback])').hidden=Boolean(state.accepted)||state.locked;
    dialog.querySelector('[data-quote-email-fallback]').hidden=!state.locked||state.pending;
    review.hidden=Boolean(state.accepted);
    success.hidden=!state.accepted;
    if(state.accepted){
      dialog.querySelector('[data-quote-reference]').textContent=state.accepted;
      if(dialog.open)success.focus();
    }
  }
  sendButton.addEventListener('click',async()=>{
    if(!lastTrip||submission.state().pending)return;
    const contact=validateQuoteContact({name:nameInput.value,email:emailInput.value});
    if(contact.field&&!submission.state().locked){quoteStatus.textContent=contact.message;(contact.field==='name'?nameInput:emailInput).focus();return;}
    updateEmail();
    quoteStatus.textContent='';
    const sending=submission.submit({...lastTrip,name:nameInput.value,email:emailInput.value,page:location.pathname.replace(/\.html$/,''),website:dialog.querySelector('[data-quote-website]').value});
    renderSubmissionState();
    const result=await sending;
    renderSubmissionState();
    if(result.ok)return;
    if(dialog.open&&!submission.state().expired)sendButton.focus();
    quoteStatus.textContent=result.error==='rate_limit'?'Please wait a minute, then retry this request. Your details are kept here.':result.error==='expired_request'?'This request is too old to retry safely. Email our team with your plans and reference '+result.reference+'.':result.error==='invalid_request'?'Check your request details and try again.':'We couldn’t confirm your request was sent. Your details are kept here. Retry this same request, or email our team for help.';
  });
  dialog.querySelector('[data-quote-done]').addEventListener('click',()=>dialog.close());
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
    if(submission.state().locked){if(!dialog.open)dialog.showModal();renderSubmissionState();return;}
    if(submission.state().accepted){submission.reset();nameInput.value='';emailInput.value='';notesInput.value='';quoteStatus.textContent='';renderSubmissionState();}
    const inline=document.querySelector('form[data-wine-quote]');
    if(inputs) {
      review.hidden=true;inputs.hidden=false;dialog.showModal();inputs.querySelector('[name="pickup"]').focus();
    } else if(inline) {
      inline.scrollIntoView({block:'center',behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'instant':'smooth'});
      inline.querySelector('[name="pickup"]').focus({preventScroll:true});
    }
  }
  document.querySelectorAll('[data-plan-wine-day]').forEach(button=>button.addEventListener('click',()=>{
    if(submission.state().locked){startQuote(button);return;}
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
      if(submission.state().locked){if(!dialog.open)dialog.showModal();renderSubmissionState();return;}
      if(submission.state().accepted)submission.reset();
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
      renderSubmissionState();
      review.hidden = false;
      if (inputs) inputs.hidden = true;
      if (!dialog.open) dialog.showModal();
      nameInput.focus();
    });
  });
  document.querySelectorAll('[data-start-quote]').forEach(link => link.addEventListener('click',event => {
    event.preventDefault();
    startQuote(link);
  }));
  dialog.addEventListener('close',()=>{if(inputs) quoteOpener?.focus();});
  dialog.querySelector('[data-close-quote]').addEventListener('click',() => dialog.close());
  dialog.querySelector('[data-edit-quote]').addEventListener('click',() => {
    if(submission.state().locked)return;
    if (inputs) {
      review.hidden = true;
      inputs.hidden = false;
      lastForm.querySelector('[name="pickup"]').focus();
    } else { dialog.close(); lastForm?.querySelector('[name="pickup"]').focus(); }
  });
})();
