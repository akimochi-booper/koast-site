/* Region filtering and manual paging only; quote preparation has one owner. */
function wineDayMatchesRegion(ideaRegion, selectedRegion) {
  return selectedRegion==='all' || ideaRegion===selectedRegion;
}
(() => {
  if(typeof document==='undefined') return;
  document.querySelectorAll('[data-wine-days]').forEach(collection=>{
    const track=collection.querySelector('[data-wine-day-track]');
    const cards=[...track.querySelectorAll('[data-wine-day-card]')];
    const previous=collection.querySelector('[data-wine-day-previous]');
    const next=collection.querySelector('[data-wine-day-next]');
    const count=collection.querySelector('[data-wine-day-count]');
    const controls=()=>{
      previous.disabled=track.scrollLeft<=2;
      next.disabled=track.scrollLeft>=track.scrollWidth-track.clientWidth-2;
    };
    collection.querySelectorAll('[data-wine-day-region]').forEach(button=>button.addEventListener('click',()=>{
      cards.forEach(card=>{card.hidden=!wineDayMatchesRegion(card.dataset.region,button.dataset.wineDayRegion);});
      collection.querySelectorAll('[data-wine-day-region]').forEach(item=>item.setAttribute('aria-pressed',String(item===button)));
      count.textContent=cards.filter(card=>!card.hidden).length+' wine-day ideas';
      track.scrollTo({left:0,behavior:'instant'});controls();
    }));
    const page=direction=>track.scrollBy({left:direction*track.clientWidth,behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'instant':'smooth'});
    previous.addEventListener('click',()=>page(-1));next.addEventListener('click',()=>page(1));
    track.addEventListener('scroll',controls,{passive:true});new ResizeObserver(controls).observe(track);controls();
  });
})();
