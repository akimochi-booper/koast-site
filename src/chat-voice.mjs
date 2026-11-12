/** Shared browser dictation owner. No provider calls, persistence, or automatic Send.
 * Adapters supply current-principal/field guards, localized copy and draft callbacks.
 * stop drains final recognition; finish fences immediately; cancel restores start draft.
 */
export function installChatVoice(win) {
  'use strict';
  if (win.KoastVoice) return;
  var doc = win.document, current = null;
  var defaults = {voice:'Dictate a message',stop:'Stop dictation',cancel:'Cancel dictation',requesting:'Starting microphone',listening:'Listening',speaking:'Listening',stopping:'Finishing',unavailable:'Dictation is unavailable. You can type your message.',permissionDenied:'Microphone access is blocked. You can type your message.',noSpeech:'No speech detected. You can try again or type your message.'};
  var css = '.kv-shelf{box-sizing:border-box;display:flex;align-items:center;gap:10px;min-width:0;width:100%;height:48px;flex:none;border-top:1px solid color-mix(in srgb,currentColor 18%,transparent);margin:0 0 4px;color:var(--kv-ink,inherit);font:inherit}.kv-cancel{display:grid;place-items:center;flex:0 0 44px;width:44px;height:44px;min-width:44px;padding:0;border:0;border-radius:12px;background:transparent;color:inherit;cursor:pointer;touch-action:manipulation;-webkit-tap-highlight-color:transparent}.kv-cancel svg{width:20px;height:20px}.kv-cancel:focus-visible{outline:2px solid currentColor;outline-offset:-3px}.kv-wave{display:block;flex:1 1 80px;min-width:24px;height:28px;color:var(--kv-accent,#35c4b3)}.kv-status{flex:0 1 auto;display:flex;gap:5px;min-width:0;max-width:55%;white-space:nowrap;font-size:12px;line-height:18px;padding-inline-end:6px}.kv-time{flex-shrink:0;font-variant-numeric:tabular-nums;opacity:.7}.kv-shelf [role=status]{min-width:0;white-space:normal;overflow-wrap:anywhere;line-height:16px}[data-koast-composer][data-koast-composer][data-koast-composer][data-koast-composer] [data-composer-action].kv-stop,#kchat .kv-stop,.kv-stop{position:relative!important;color:var(--kv-accent,#35c4b3)!important;background:color-mix(in srgb,var(--kv-accent,#35c4b3) 15%,transparent)!important}.kv-stop>svg{visibility:hidden!important}.kv-stop::after{content:"";position:absolute;left:50%;top:50%;width:13px;height:13px;border-radius:3px;background:currentColor;transform:translate(-50%,-50%);pointer-events:none}.kv-layout{flex-wrap:wrap!important}.kv-layout>.kv-shelf{flex-basis:100%;order:-1}.kv-shelf[data-state=requesting] .kv-wave,.kv-shelf[data-state=stopping] .kv-wave{opacity:.45}@media(prefers-reduced-motion:reduce){.kv-shelf *{transition:none!important;animation:none!important}}@media(forced-colors:active){.kv-shelf{border-color:CanvasText}.kv-wave{color:CanvasText}.kv-stop{color:ButtonText!important;background:ButtonFace!important}}';
  function copy(s,key) { return s.o.copy ? s.o.copy(key) : defaults[key]; }
  function matches(root) { return current && (!root || current.o.root === root || root === current.o.input || (root.contains && root.contains(current.o.input))); }
  function visible(element) { for(var node=element;node&&node.nodeType!==9;node=node.parentElement){if(node.hidden||node.inert||node.getAttribute&&node.getAttribute('aria-hidden')==='true')return false;var style=win.getComputedStyle(node);if(style.display==='none'||style.visibility==='hidden')return false;}return true; }
  function valid(s) { return current === s && s.o.input.isConnected !== false && s.o.button.isConnected !== false && !s.o.input.disabled && !s.o.input.readOnly && visible(s.o.input) && visible(s.o.button) && (!s.o.isCurrent || s.o.isCurrent()); }
  function emit(s) { s.writing=true;try{s.o.input.dispatchEvent(new win.Event('input',{bubbles:true}));if(s.o.onInput)s.o.onInput();}finally{s.writing=false;} }
  function text(s,state) { s.state=state;s.shelf.dataset.state=state;s.label.textContent=copy(s,state);if(s.o.onState)s.o.onState(state); }
  function elapsed(s) { var seconds=Math.floor((Date.now()-s.started)/1000);s.time.textContent=String(Math.floor(seconds/60)).padStart(2,'0')+':'+String(seconds%60).padStart(2,'0'); }
  function releaseAudio(s) {
    if(s.frame)win.cancelAnimationFrame(s.frame);s.frame=0;
    if(s.stream){s.stream.getTracks().forEach(function(track){track.stop();});s.stream=null;}
    if(s.source){try{s.source.disconnect();}catch(e){}s.source=null;}
    if(s.context){try{var p=s.context.close();if(p&&p.catch)p.catch(function(){});}catch(e){}s.context=null;}
  }
  function draw(s,samples) {
    var canvas=s.canvas,ctx=canvas.getContext&&canvas.getContext('2d');if(!ctx)return;
    var width=canvas.clientWidth||140,height=28,ratio=win.devicePixelRatio||1;
    if(canvas.width!==Math.round(width*ratio)||canvas.height!==height*ratio){canvas.width=Math.round(width*ratio);canvas.height=height*ratio;}
    ctx.setTransform(ratio,0,0,ratio,0,0);ctx.clearRect(0,0,width,height);
    ctx.strokeStyle=win.getComputedStyle(canvas).color;ctx.lineWidth=3;ctx.lineCap='round';
    // Each bar is a peak from the current real time-domain sample window. No invented motion.
    var bars=Math.max(5,Math.floor(width/6)),step=width/bars;
    for(var i=0;i<bars;i++){var peak=0;if(samples){var a=Math.floor(i*samples.length/bars),b=Math.floor((i+1)*samples.length/bars);for(var j=a;j<b;j++)peak=Math.max(peak,Math.abs(samples[j]-128)/128);}var h=Math.max(2,Math.min(26,peak*54));ctx.beginPath();ctx.moveTo(i*step+step/2,14-h/2);ctx.lineTo(i*step+step/2,14+h/2);ctx.stroke();}
  }
  function meter(s) {
    var Audio=win.AudioContext||win.webkitAudioContext,media=win.navigator&&win.navigator.mediaDevices;
    if(!Audio||!media||!media.getUserMedia){draw(s,null);return;}
    try{s.context=new Audio();var resumed=s.context.resume();if(resumed&&resumed.catch)resumed.catch(function(){});}catch(e){releaseAudio(s);draw(s,null);return;}
    media.getUserMedia({audio:true}).then(function(stream){
      if(!valid(s)||s.state==='stopping'){stream.getTracks().forEach(function(t){t.stop();});return;}
      s.stream=stream;try{var analyser=s.context.createAnalyser();analyser.fftSize=256;analyser.smoothingTimeConstant=.7;s.source=s.context.createMediaStreamSource(stream);s.source.connect(analyser);var samples=new Uint8Array(analyser.fftSize);var last=0;
        function frame(now){if(!valid(s)){finishSession(s,false,false);return;}if(now-last>=50){analyser.getByteTimeDomainData(samples);draw(s,samples);last=now;}s.frame=win.requestAnimationFrame(frame);}s.frame=win.requestAnimationFrame(frame);
      }catch(e){releaseAudio(s);draw(s,null);}
    }).catch(function(){if(current===s){releaseAudio(s);draw(s,null);}});
  }
  function finishSession(s,restore,drain) {
    if(current!==s)return;
    if(drain){if(s.state==='stopping')return;text(s,'stopping');releaseAudio(s);try{s.rec.stop();}catch(e){finishSession(s,false,false);return;}if(current===s)s.timeout=win.setTimeout(function(){finishSession(s,false,false);},1200);return;}
    current=null;win.clearInterval(s.timer);win.clearTimeout(s.timeout);win.clearTimeout(s.startTimeout);releaseAudio(s);if(s.observer)s.observer.disconnect();
    s.o.input.removeEventListener('input',s.manual);s.o.input.removeEventListener('keydown',s.escape);s.o.button.classList.remove('kv-stop');s.o.button.setAttribute('aria-pressed','false');s.o.button.setAttribute('aria-label',copy(s,'voice'));s.o.button.title=copy(s,'voice');
    s.shelf.remove();if(s.addLayout)s.host.classList.remove('kv-layout');
    s.rec.onstart=s.rec.onresult=s.rec.onerror=s.rec.onend=null;try{s.rec.abort();}catch(e){}
    if(restore&&s.o.input.value===s.last&&(!s.o.isCurrent||s.o.isCurrent())){s.o.input.value=s.original;emit(s);}
    if(s.o.onState)s.o.onState('idle');
  }
  function start(o) {
    if(matches()&&current.o.button===o.button){finishSession(current,false,true);return;}
    if(current)finishSession(current,false,false);
    var Speech=win.SpeechRecognition||win.webkitSpeechRecognition;
    if(!Speech||!o||!o.input||!o.button||!o.root||o.isCurrent&&!o.isCurrent()){if(o&&o.onError)o.onError('unavailable');return;}
    if(!doc.getElementById('koast-voice-style')){var style=doc.createElement('style');style.id='koast-voice-style';style.textContent=css;doc.head.appendChild(style);}
    var original=o.input.value,startAt=typeof o.input.selectionStart==='number'?o.input.selectionStart:original.length,endAt=typeof o.input.selectionEnd==='number'?o.input.selectionEnd:startAt;
    var s={o:o,original:original,last:original,prefix:original.slice(0,startAt),suffix:original.slice(endAt),started:Date.now(),host:o.shelfHost||o.root,rec:new Speech(),frame:0,completed:'',state:'requesting'};current=s;
    s.shelf=doc.createElement('div');s.shelf.className='kv-shelf';s.shelf.dataset.state='requesting';
    var cancel=doc.createElement('button');s.cancel=cancel;cancel.type='button';cancel.className='kv-cancel';cancel.setAttribute('aria-label',copy(s,'cancel'));cancel.title=copy(s,'cancel');
    // Reuse the product's ordinary two-stroke Close glyph; this is an interface control.
    cancel.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18"/></svg>';
    s.canvas=doc.createElement('canvas');s.canvas.className='kv-wave';s.canvas.setAttribute('aria-hidden','true');
    var status=doc.createElement('span');status.className='kv-status';s.label=doc.createElement('span');s.label.setAttribute('role','status');s.time=doc.createElement('span');s.time.className='kv-time';s.time.setAttribute('aria-hidden','true');status.appendChild(s.label);status.appendChild(s.time);s.shelf.appendChild(cancel);s.shelf.appendChild(s.canvas);s.shelf.appendChild(status);
    // Row-shaped legacy roots need a full-width shelf while retaining their current children.
    var display=win.getComputedStyle(s.host).display;if(display==='flex'&&win.getComputedStyle(s.host).flexDirection==='row'){s.addLayout=!s.host.classList.contains('kv-layout');s.host.classList.add('kv-layout');}
    var row=s.host.querySelector&&s.host.querySelector('[data-composer-row]');s.host.insertBefore(s.shelf,row&&row.parentElement===s.host?row:s.host.firstChild);o.button.classList.add('kv-stop');o.button.setAttribute('aria-pressed','true');o.button.setAttribute('aria-label',copy(s,'stop'));o.button.title=copy(s,'stop');
    cancel.addEventListener('pointerdown',function(e){if(e.button===0||e.button==null)e.preventDefault();});cancel.addEventListener('click',function(){finishSession(s,true,false);if(o.input.isConnected)o.input.focus({preventScroll:true});});
    s.manual=function(){if(current===s&&!s.writing){s.last=o.input.value;finishSession(s,false,false);}};s.escape=function(e){if(e.key==='Escape'){e.preventDefault();e.stopPropagation();finishSession(s,true,false);}};o.input.addEventListener('input',s.manual);o.input.addEventListener('keydown',s.escape);
    s.rec.lang=o.lang||'en-US';s.rec.interimResults=true;s.rec.continuous=!!o.continuous;
    s.rec.onstart=function(){if(!valid(s)){finishSession(s,false,false);return;}win.clearTimeout(s.startTimeout);if(!s.hasStarted){s.started=Date.now();s.hasStarted=true;}text(s,'listening');};
    s.rec.onresult=function(event){if(!valid(s)){finishSession(s,false,false);return;}var textValue=s.completed,finalSegment='';for(var i=0;i<event.results.length;i++){textValue+=event.results[i][0].transcript;if(event.results[i].isFinal)finalSegment+=event.results[i][0].transcript;}s.finalSegment=finalSegment;var gap=s.prefix&&!/\s$/.test(s.prefix)&&textValue&&!/^\s/.test(textValue)?' ':'';var trailing=s.suffix&&!/^\s/.test(s.suffix)&&textValue&&!/\s$/.test(textValue)?' ':'';s.last=s.prefix+gap+textValue+trailing+s.suffix;if(o.input.maxLength>0)s.last=s.last.slice(0,o.input.maxLength);o.input.value=s.last;emit(s);};
    s.rec.onerror=function(event){if(current!==s)return;var key=event.error==='not-allowed'||event.error==='service-not-allowed'?'permissionDenied':event.error==='no-speech'?'noSpeech':'unavailable';finishSession(s,false,false);if(o.onError)o.onError(key);};
    s.rec.onend=function(){if(current!==s)return;if(o.restartNaturalEnd&&valid(s)&&s.state!=='stopping'){if(s.finalSegment)s.completed=(s.completed+s.finalSegment).trimEnd()+' ';s.finalSegment='';text(s,'requesting');try{s.rec.start();return;}catch(e){finishSession(s,false,false);if(o.onError)o.onError('unavailable');return;}}finishSession(s,false,false);};
    if(win.MutationObserver){s.observer=new win.MutationObserver(function(){if(!valid(s))finishSession(s,false,false);});s.observer.observe(doc.body,{childList:true,subtree:true,attributes:true,attributeFilter:['hidden','aria-hidden','inert']});}
    text(s,'requesting');elapsed(s);draw(s,null);s.timer=win.setInterval(function(){if(!valid(s)){finishSession(s,false,false);return;}elapsed(s);},250);
    s.startTimeout=win.setTimeout(function(){if(current===s&&s.state==='requesting'){finishSession(s,false,false);if(o.onError)o.onError('unavailable');}},15000);
    try{s.rec.start();if(current===s)meter(s);}catch(e){finishSession(s,false,false);if(o.onError)o.onError('unavailable');}
  }
  win.KoastVoice={start:start,stop:function(root){if(matches(root))finishSession(current,false,true);},finish:function(root){if(matches(root))finishSession(current,false,false);},cancel:function(root){if(matches(root))finishSession(current,true,false);},active:function(root){return!!matches(root);}};
  win.KoastVoice.dispose=win.KoastVoice.cancel;
  win.KoastVoice.refreshCopy=function(){var s=current;if(!s)return;s.cancel.setAttribute('aria-label',copy(s,'cancel'));s.cancel.title=copy(s,'cancel');s.label.textContent=copy(s,s.state);s.o.button.setAttribute('aria-label',copy(s,'stop'));s.o.button.title=copy(s,'stop');};
  win.addEventListener('pagehide',function(){if(current)finishSession(current,false,false);});doc.addEventListener('visibilitychange',function(){if(doc.hidden&&current)finishSession(current,false,false);});
}
export const CHAT_VOICE_JS = '(function(){var __name=function(fn){return fn;};(' + installChatVoice.toString() + ')(window);})();';
