/* Supplementary first-party interaction measurement. Activation requires the
   reviewed notice, meta opt-in and matching collector flag. No replay/keystrokes. */
(function () {
  'use strict';
  window.createKoastJourney = function (context) {
    var meta = document.querySelector('meta[name="koast-journey"]');
    if (!meta || meta.content !== 'enabled' || context.optedOut()) return;
    var page = crypto.randomUUID(), sequence = 0, count = 0, seen = {}, activeStart = document.visibilityState === 'hidden' ? null : Date.now(), active = 0, sentSeconds = 0;
    var events = ['visit_context','navigation_click','control_click','section_view','scroll_depth','engagement','faq_open','media_play','media_pause','quote_open','quote_started','quote_review','quote_validation','quote_submit','quote_acknowledged','quote_unconfirmed','assistant_open','assistant_send','assistant_reply','assistant_unconfirmed'];
    var actions = ['header','footer','content','wine_plan','wine_idea','wine_vehicle','wine_region','wine_search','wine_filter','wine_clear','quote_edit','quote_close','assistant_close','assistant_voice','assistant_photo'];
    function emit(name, values) {
      if (context.optedOut() || count >= 80 || events.indexOf(name) < 0) return;
      // A new tab session cannot inherit page-level sequencing/activity from an
      // expired session. Each event obtains current privacy/session state.
      var session = context.session(), properties = {}, p = values || {};
      if (actions.indexOf(p.action) >= 0) properties.action = p.action;
      if (['hero','services','fleet','wine','planning','faq','reviews','booking','contact','article'].indexOf(p.section) >= 0) properties.section = p.section;
      if (name === 'navigation_click') {
        if (typeof p.target_path !== 'string' || !/^\/[a-zA-Z0-9_./-]*$/.test(p.target_path) || p.target_path.length > 220 || /\.\.|\d{7}|(?:^|\/)(?:api|account|auth|reset|receipt|reservation|r|t|d)(?:\/|$)/i.test(p.target_path)) return;
        properties.target_path = p.target_path;
      }
      if (name === 'scroll_depth') { if ([25,50,75,100].indexOf(p.percent) < 0) return; properties.percent = p.percent; }
      if (name === 'engagement') { if (!Number.isInteger(p.active_seconds) || p.active_seconds < 1 || p.active_seconds > 7200) return; properties.active_seconds = p.active_seconds; }
      if (name === 'faq_open') { if (!Number.isInteger(p.index) || p.index < 1 || p.index > 200) return; properties.index = p.index; }
      if (name === 'quote_validation') { if (['trip','contact','request'].indexOf(p.step) < 0) return; properties.step = p.step; }
      if (name === 'visit_context') {
        // Coarse categories only; never send/store a raw user agent or viewport.
        var ua = navigator.userAgent || '', width = window.innerWidth;
        properties.device = width < 768 ? 'phone' : width < 1100 ? 'tablet' : 'desktop';
        properties.browser = /Edg\//.test(ua) ? 'edge' : /Firefox\//.test(ua) ? 'firefox' : /Chrome\/|CriOS\//.test(ua) ? 'chrome' : /Safari\//.test(ua) ? 'safari' : 'other';
        var language = String(navigator.language || '').split('-')[0].toLowerCase();
        if (/^[a-z]{2,3}$/.test(language)) properties.language = language;
      }
      count++;
      context.send({version:2,event_id:crypto.randomUUID(),session_id:session.id,page_id:page,sequence:++sequence,event:name,
        path:context.path(),first_touch:session.first_touch,occurred_at:new Date().toISOString(),properties:properties});
    }
    function once(key, event, values) { if (seen[key]) return; seen[key] = true; emit(event, values); }
    function milestone(event, properties) { try { emit(event, properties); } catch (_) {} }
    // Explicit producers supply fixed event codes, never DOM text/form values.
    window.koastJourney = {record:milestone};
    emit('visit_context');
    document.addEventListener('click', function (event) {
      try {
        var node = event.target && event.target.closest ? event.target : null;
        if (!node) return;
        var link = node.closest('a[href]');
        if (link) {
          var url = new URL(link.href, location.href);
          if (['koastride.com','www.koastride.com'].indexOf(url.hostname) >= 0 && url.protocol === 'https:' && url.pathname !== location.pathname) {
            emit('navigation_click',{target_path:url.pathname,action:link.closest('footer')?'footer':link.closest('header,nav')?'header':'content'});
          }
        }
        var action = node.closest('[data-plan-wine-day],[data-clear-wine-day],[data-edit-quote],[data-quote-done]');
        if (action) {
          if (action.hasAttribute('data-plan-wine-day')) emit('control_click',{action:'wine_plan'});
          else if (action.hasAttribute('data-clear-wine-day')) emit('control_click',{action:'wine_clear'});
          else if (action.hasAttribute('data-edit-quote')) emit('control_click',{action:'quote_edit'});
          else if (action.hasAttribute('data-quote-done')) emit('control_click',{action:'quote_close'});
        }
      } catch (_) {}
    },{passive:true});
    document.addEventListener('toggle',function(event){
      try { var details=event.target;if(!details.open||!details.matches('details'))return;
        var list=Array.from(document.querySelectorAll('details')).filter(function(node){return !node.matches('.mm-dd,.reference-more,.renewal-planning');});
        var index=list.indexOf(details);if(index>=0)once('faq'+index,'faq_open',{index:index+1});
      } catch (_) {}
    },true);
    document.addEventListener('focusin',function(event){
      try{if(event.target.closest('form[data-wine-quote],#quote-request'))once('quote_started','quote_started');}catch(_){}
    },{passive:true});
    document.addEventListener('change',function(event){
      try{var node=event.target;if(node.matches('[data-review-vehicle]'))emit('control_click',{action:'wine_vehicle'});}catch(_){}
    },{passive:true});
    function scroll(){
      if(context.optedOut())return;
      var height=document.documentElement.scrollHeight-window.innerHeight;
      if(height<=0)return;
      var percent=Math.min(100,Math.max(0,(window.scrollY||0)/height*100));
      [25,50,75,100].forEach(function(value){if(percent>=value-1)once('scroll'+value,'scroll_depth',{percent:value});});
    }
    window.addEventListener('scroll',scroll,{passive:true});
    var observer;
    if(typeof IntersectionObserver==='function'){
      // Fixed public sections only; names/DOM copy never enter the payload.
      var selectors={hero:'.reference-cinema-hero,.hero',services:'#services',fleet:'#fleet',wine:'#wine-regions',planning:'#planning',faq:'.faq,#faq',reviews:'#reviews',booking:'[data-wine-quote]',contact:'#contact',article:'article'};
      Object.keys(selectors).forEach(function(section){var node=document.querySelector(selectors[section]);if(node)node.setAttribute('data-journey-section',section);});
      observer=new IntersectionObserver(function(entries){entries.forEach(function(entry){if(entry.isIntersecting){var section=entry.target.getAttribute('data-journey-section');once('section'+section,'section_view',{section:section});observer.unobserve(entry.target);}});},{threshold:0.25});
      document.querySelectorAll('[data-journey-section]').forEach(function(node){observer.observe(node);});
    }
    ['play','pause'].forEach(function(type){document.addEventListener(type,function(event){try{if(event.target.matches('video,audio'))emit(type==='play'?'media_play':'media_pause');}catch(_){}},true);});
    function finish(){
      var now=Date.now();if(activeStart!==null){active+=Math.max(0,now-activeStart);activeStart=null;}
      var seconds=Math.min(7200,Math.floor(active/1000));if(seconds>sentSeconds){sentSeconds=seconds;emit('engagement',{active_seconds:seconds});}
    }
    document.addEventListener('visibilitychange',function(){if(document.visibilityState==='hidden')finish();else activeStart=Date.now();});
    window.addEventListener('pagehide',finish);
    window.addEventListener('pageshow',function(event){if(event.persisted){page=crypto.randomUUID();sequence=0;count=0;seen={};active=0;sentSeconds=0;activeStart=document.visibilityState==='hidden'?null:Date.now();emit('visit_context');}});
    return window.koastJourney;
  };
})();
