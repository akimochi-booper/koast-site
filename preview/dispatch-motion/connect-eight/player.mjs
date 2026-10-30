import{bind,DURATION,SETTLED}from'./motion.mjs?v=2';
const $=id=>document.getElementById(id),stage=$('stage'),motion=bind(stage),reduce=matchMedia('(prefers-reduced-motion:reduce)');
let ready=false,playing=false,manual=false,time=0,last=0,hiddenWasPlaying=false;
function render(){if(!ready)return;motion.draw(time,{reviewFade:$('loop').checked&&playing});$('time').value=String(Math.round(time));$('time-label').textContent=(time/1000).toFixed(1)+' / 4.4 s';$('play').textContent=playing?'Pause':reduce.matches&&!manual?'Play motion':'Play';$('focus-play').textContent=playing?'Pause animation':'Play animation';}
function start(explicit=false){if(!ready)return;if(explicit)manual=true;if(reduce.matches&&!manual){playing=false;time=SETTLED;$('status').textContent='Reduced Motion is enabled. Use Play motion to preview.';}else{playing=true;last=performance.now();$('status').textContent='';}render();}
function replay(){hiddenWasPlaying=false;time=0;start(true);}
function layout(wide,restart=true){stage.classList.toggle('is-wide',wide);$('phone').setAttribute('aria-pressed',String(!wide));$('desktop').setAttribute('aria-pressed',String(wide));motion.resize();if(ready&&restart){time=0;start();}else render();}
function expand(restart=true){document.body.classList.add('expanded');$('close').hidden=false;$('focus-controls').hidden=false;motion.resize();if(restart)replay();$('close').focus();}
function close(){document.body.classList.remove('expanded');$('close').hidden=true;$('focus-controls').hidden=true;motion.resize();render();$('expand').focus();}
$('phone').onclick=()=>layout(false);$('desktop').onclick=()=>layout(true);$('replay').onclick=replay;$('focus-replay').onclick=replay;$('expand').onclick=()=>expand();$('close').onclick=close;
$('play').onclick=()=>{hiddenWasPlaying=false;if(playing){playing=false;render();}else{if(time>=DURATION||(reduce.matches&&!manual))time=0;start(true);}};$('focus-play').onclick=()=>$('play').click();
$('time').oninput=()=>{hiddenWasPlaying=false;playing=false;time=Number($('time').value);render();};$('loop').onchange=render;
window.addEventListener('resize',()=>{motion.resize();render();},{passive:true});document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!$('close').hidden)close();});
reduce.addEventListener('change',()=>{manual=false;start();});document.addEventListener('visibilitychange',()=>{if(document.hidden){hiddenWasPlaying=playing;playing=false;}else{const resume=hiddenWasPlaying;hiddenWasPlaying=false;last=performance.now();if(resume)start();}});
function tick(now){if(ready&&playing&&!document.hidden){time+=Math.min(64,Math.max(0,now-last));if(time>DURATION){if($('loop').checked)time%=DURATION;else{time=DURATION;playing=false;}}render();}last=now;requestAnimationFrame(tick);}
const initial=new URLSearchParams(location.search).get('view');layout(initial==='desktop'||(initial!=='phone'&&innerWidth>=1050),false);
if(new URLSearchParams(location.search).get('focus')==='1')expand(false);
Promise.all([document.fonts.ready,...[...stage.querySelectorAll('img')].map(img=>new Promise((resolve,reject)=>{function decode(){if(!img.naturalWidth){reject(Error('Image unavailable'));return;}Promise.resolve(img.decode?.()).then(resolve,reject);}if(img.complete)decode();else{img.onload=decode;img.onerror=reject;}}))]).then(()=>{ready=true;stage.dataset.ready='true';$('play').disabled=$('replay').disabled=$('time').disabled=false;motion.resize();start();requestAnimationFrame(tick);}).catch(()=>{$('status').textContent='Artwork did not load. ';const retry=document.createElement('button');retry.textContent='Reload';retry.onclick=()=>location.reload();$('status').appendChild(retry);});

// This is a motion prototype: it neither reads credentials nor sends authentication requests.
const feedback=$('entry-feedback');
$('entry-form').addEventListener('submit',event=>{event.preventDefault();feedback.textContent='This is a design preview. Use Open live sign in to access your account.';});
$('show-password').onclick=()=>{const field=$('entry-password'),show=field.type==='password';field.type=show?'text':'password';$('show-password').textContent=show?'Hide':'Show';$('show-password').setAttribute('aria-label',show?'Hide password':'Show password');};
document.querySelectorAll('[data-preview-mode]').forEach(button=>button.onclick=()=>{feedback.textContent='This is a design preview. '+({reset:'Password recovery',google:'Google sign-in',text:'Text-code sign-in',signup:'Company setup'}[button.dataset.previewMode])+' is available through Open live sign in.';});
