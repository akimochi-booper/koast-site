/* Progressive enhancement for winery discovery and the website's Compact choice pickers.
   Native form values remain authoritative; date and address editors stay native. */
function matchesWinery(searchable, query) {
  return String(searchable).normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase()
    .includes(String(query).normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase().trim());
}

(() => {
  if (typeof document === 'undefined') return;
  const motion = () => matchMedia('(prefers-reduced-motion:reduce)').matches ? 'instant' : 'smooth';
  document.querySelectorAll('[data-winery-browser]').forEach(browser => {
    const track = browser.querySelector('[data-winery-track]');
    const cards = [...track.querySelectorAll('[data-winery-card]')];
    const tools = browser.querySelector('[data-browse-tools]');
    if (!tools) return;
    const search = browser.querySelector('[data-winery-search]');
    const clear = browser.querySelector('[data-clear-winery]');
    const previous = browser.querySelector('[data-winery-previous]');
    const next = browser.querySelector('[data-winery-next]');
    const count = browser.querySelector('[data-winery-count]');
    const empty = browser.querySelector('[data-winery-empty]');
    tools.hidden = false;
    track.classList.add('is-carousel');
    function controls() {
      previous.disabled = track.scrollLeft <= 2;
      next.disabled = track.scrollLeft >= track.scrollWidth - track.clientWidth - 2;
    }
    function filter() {
      cards.forEach(card => { card.hidden = !matchesWinery(card.dataset.search,search?.value || ''); });
      const shown = cards.filter(card => !card.hidden).length;
      count.textContent = shown+' of '+cards.length+' wineries';
      empty.hidden = shown !== 0;
      track.hidden = shown === 0;
      if (clear) clear.hidden = !search.value;
      track.scrollTo({left:0,behavior:'instant'});
      controls();
    }
    previous.addEventListener('click',() => track.scrollBy({left:-track.clientWidth,behavior:motion()}));
    next.addEventListener('click',() => track.scrollBy({left:track.clientWidth,behavior:motion()}));
    track.addEventListener('scroll',controls,{passive:true});
    new ResizeObserver(controls).observe(track);
    search?.addEventListener('input',filter);
    clear?.addEventListener('click',() => { search.value=''; filter(); search.focus(); });
    filter();
  });

  let closeCurrent;
  document.querySelectorAll('[data-wine-quote] select[name="party"], [data-review-vehicle]').forEach((select,index) => {
    const field = select.closest('.reference-field, .reference-review-field');
    const choiceLabel = select.hasAttribute('data-review-vehicle') ? 'Requested vehicle' : 'Your party';
    const trigger = document.createElement('button');
    trigger.type = 'button';
    trigger.className = 'reference-choice-button'+(select.name==='party'?' reference-party-button':'');
    trigger.setAttribute('aria-haspopup','listbox');
    trigger.setAttribute('aria-expanded','false');
    trigger.setAttribute('aria-controls','wine-choice-options-'+index);
    const label = document.createElement('span');
    trigger.append(label);
    if(select.hasAttribute('data-review-vehicle')) {
      const chevron=document.createElement('img');chevron.src='/img/icons/tabler/chevron-down.svg';
      chevron.alt='';chevron.width=14;chevron.height=14;chevron.setAttribute('aria-hidden','true');trigger.append(chevron);
    }
    const sync = () => {
      label.textContent = select.selectedOptions[0]?.textContent || 'Your party';
      trigger.setAttribute('aria-label',choiceLabel+': '+label.textContent);
    };
    sync();
    select.addEventListener('change',sync);
    select.hidden = true;
    field.insertBefore(trigger,select);
    const choices = [...select.options].filter(option => !option.disabled);
    let menu, active = 0, typed = '', typedAt = 0;
    function close(focus=false) {
      if (!menu) return;
      menu.remove(); menu = null;
      trigger.setAttribute('aria-expanded','false');
      document.removeEventListener('pointerdown',outside,true);
      window.removeEventListener('resize',resized);
      document.removeEventListener('scroll',scrolled,true);
      if (closeCurrent === close) closeCurrent = undefined;
      if (focus) trigger.focus();
    }
    function outside(event) { if (!field.contains(event.target) && !menu?.contains(event.target)) close(); }
    function resized() { close(true); }
    function scrolled(event) { if (menu && !menu.contains(event.target)) close(true); }
    function mark() {
      [...menu.children].forEach((option,i) => option.classList.toggle('is-active',i===active));
      menu.setAttribute('aria-activedescendant',menu.children[active].id);
      // Scroll this list only: scrollIntoView can also move its containing dialog.
      const option=menu.children[active];
      const top=option.offsetTop, bottom=top+option.offsetHeight;
      if(top<menu.scrollTop) menu.scrollTop=top;
      else if(bottom>menu.scrollTop+menu.clientHeight) menu.scrollTop=bottom-menu.clientHeight;
    }
    function choose(i) {
      select.value = choices[i].value;
      select.dispatchEvent(new Event('change',{bubbles:true}));
      close(true);
    }
    function open(last=false,keyboard=false) {
      closeCurrent?.();
      menu = document.createElement('div');
      menu.id = 'wine-choice-options-'+index;
      menu.className = 'reference-compact-picker';
      menu.classList.toggle('is-keyboard',keyboard);
      menu.role = 'listbox'; menu.tabIndex = -1;
      menu.setAttribute('aria-label',choiceLabel);
      choices.forEach((choice,i) => {
        const option = document.createElement('div');
        option.id = menu.id+'-'+i;
        option.role = 'option';
        option.setAttribute('aria-selected',String(choice.value===select.value));
        const text = document.createElement('span'); text.textContent = choice.textContent;
        const check = document.createElement('span'); check.className='picker-check'; check.textContent='✓'; check.setAttribute('aria-hidden','true');
        option.append(text,check);
        option.addEventListener('click',() => choose(i));
        option.addEventListener('pointermove',() => { menu.classList.remove('is-keyboard');active=i;mark(); });
        menu.append(option);
      });
      (select.closest('dialog') || document.body).append(menu);
      const rect = field.getBoundingClientRect();
      const width = Math.min(360,Math.max(rect.width,240),innerWidth-24);
      const below = innerHeight-rect.bottom-12;
      const above = rect.top-12;
      const height = Math.min(264,Math.max(48,Math.max(below,above)));
      menu.style.width = width+'px';
      menu.style.maxHeight = height+'px';
      menu.style.left = Math.max(12,Math.min(rect.left,innerWidth-width-12))+'px';
      if (below >= Math.min(264,choices.length*48+8) || below >= above) menu.style.top = (rect.bottom+6)+'px';
      else menu.style.bottom = (innerHeight-rect.top+6)+'px';
      active = choices.findIndex(choice => choice.value===select.value);
      if (active<0) active = last ? choices.length-1 : 0;
      trigger.setAttribute('aria-expanded','true');
      menu.addEventListener('keydown',event => {
        menu.classList.add('is-keyboard');
        if (event.key==='Escape') { event.preventDefault(); event.stopPropagation(); close(true); return; }
        if (event.key==='Tab') { close(true); return; }
        if (event.key==='Enter' || event.key===' ') { event.preventDefault(); choose(active); return; }
        if (['ArrowDown','ArrowUp','Home','End'].includes(event.key)) {
          event.preventDefault();
          active = event.key==='Home' ? 0 : event.key==='End' ? choices.length-1 : (active+(event.key==='ArrowDown'?1:-1)+choices.length)%choices.length;
          mark(); return;
        }
        if (event.key.length===1 && !event.ctrlKey && !event.metaKey && !event.altKey) {
          const now=Date.now(); typed = now-typedAt>600 ? event.key : typed+event.key; typedAt=now;
          const found=choices.findIndex(choice => choice.textContent.toLocaleLowerCase().startsWith(typed.toLocaleLowerCase()));
          if (found>=0) { active=found; mark(); }
        }
      });
      document.addEventListener('pointerdown',outside,true);
      window.addEventListener('resize',resized);
      document.addEventListener('scroll',scrolled,true);
      closeCurrent=close;
      menu.focus({preventScroll:true}); mark();
    }
    trigger.addEventListener('click',event => menu ? close(true) : open(false,event.detail===0));
    trigger.addEventListener('keydown',event => {
      if (event.key==='ArrowDown' || event.key==='ArrowUp') { event.preventDefault(); open(event.key==='ArrowUp',true); }
    });
    select.form?.addEventListener('reset',() => { close(); queueMicrotask(sync); });
    select.closest('dialog')?.addEventListener('close',() => close());
  });
})();
