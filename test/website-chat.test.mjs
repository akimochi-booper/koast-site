import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
const source=readFileSync(new URL('../koast-chat.js',import.meta.url),'utf8');
const settle=()=>new Promise(resolve=>setImmediate(resolve));
function fixture({voice=false,lateVoice=false,photos=false,preparePhoto=async()=> 'data:image/jpeg;base64,cGhvdG8='}={}){
 const elements={},requests=[],timers=new Map(),background=[],viewportListeners=new Map();let timer=0,doc,recognition,photoComposer;
 class Element{
  constructor(id=''){this.id=id;this.children=[];this.attributes={};this.listeners={};this.value='';this.disabled=false;this.hidden=false;this.textContent='';this.className='';this.offsetParent={};this.style={setProperty(){}};const classes=new Set();this.classList={add:k=>classes.add(k),remove:k=>classes.delete(k),toggle:(k,on)=>on?classes.add(k):classes.delete(k),contains:k=>classes.has(k)};}
  setAttribute(k,v){this.attributes[k]=v;}getAttribute(k){return this.attributes[k];}removeAttribute(k){delete this.attributes[k];}
  addEventListener(k,fn){this.listeners[k]=fn;}
  emit(k,event={}){this.listeners[k]?.(event);}
  click(){if(!this.disabled)this.emit('click');}
  focus(){doc.activeElement=this;}
  appendChild(child){child.parent=this;this.children.push(child);return child;}
  remove(){if(this.parent)this.parent.children=this.parent.children.filter(x=>x!==this);}
  querySelector(selector){return this.children.find(x=>x.className.split(' ').includes(selector.slice(1)))||null;}
  querySelectorAll(selector){if(selector==='[data-question]')return [starter];return [close,input,mic,send,quote,email].filter(x=>!x.disabled);}
 }
 for(const id of ['kchat','kchat-msgs','kchat-in','kchat-send','kchat-mic','kchat-status','kchat-fab','kchat-title','kchat-attach','kchat-photo-input','kchat-photo-tray','kchat-photo-notice'])elements[id]=new Element(id);
 const panel=elements.kchat,messages=elements['kchat-msgs'],input=elements['kchat-in'],send=elements['kchat-send'],mic=elements['kchat-mic'],close=new Element('close'),starter=new Element('starter'),quote=new Element('quote'),email=new Element('email');
 starter.setAttribute('data-question','How does airport pickup work?');panel.querySelector=selector=>selector==='.kchat-x'?close:null;
 const welcome=new Element();welcome.className='kchat-welcome';messages.appendChild(welcome);
 doc={body:new Element('body'),activeElement:null,getElementById:id=>elements[id],createElement:()=>new Element()};
 const viewport={height:844,offsetTop:0,addEventListener:(name,fn)=>viewportListeners.set(name,fn),removeEventListener:name=>viewportListeners.delete(name)};
 const window={innerHeight:844,visualViewport:viewport,koastModalBackground:(element,open)=>background.push(open)};
 if(voice)window.SpeechRecognition=class{constructor(){recognition=this;this.stops=0;}start(){this.onstart();}stop(){this.stops++;if(!lateVoice)this.onend();}};
 const context={window,document:doc,DataView,Uint8Array,AbortSignal,createImageBitmap:()=>{},AbortController,fetch:(url,options)=>new Promise((resolve,reject)=>{if(String(url).endsWith('/capabilities'))return resolve({ok:true,json:async()=>({photos:true})});const request={url,options,resolve,reject};requests.push(request);options.signal.addEventListener('abort',()=>reject(new Error('aborted')));}),setTimeout:fn=>{timers.set(++timer,fn);return timer;},clearTimeout:id=>timers.delete(id)};
 if(photos){vm.runInNewContext(readFileSync(new URL('../koast-chat-photos.js',import.meta.url),'utf8'),context);const Actual=window.KoastPhotoComposer;window.KoastPhotoComposer=function(o){photoComposer=new Actual({...o,prepare:preparePhoto});return photoComposer;};}
 vm.runInNewContext(source,context);
 return {elements,panel,messages,input,send,mic,close,starter,doc,requests,background,viewportListeners,recognition:()=>recognition,photos:()=>photoComposer,timeout:()=>[...timers.values()].forEach(fn=>fn()),write:text=>{input.value=text;input.emit('input');},reply:async(index,text)=>{requests[index].resolve({ok:true,json:async()=>({reply:text})});await settle();}};
}
test('welcome opens without a software-keyboard focus and Escape restores launcher/background',()=>{
 const h=fixture();assert.equal(h.send.disabled,true);assert.equal(h.mic.hidden,true);
 h.elements['kchat-fab'].click();assert.equal(h.doc.activeElement.id,'kchat-title');assert.equal(h.elements.kchat.attributes['aria-hidden'],'false');assert.equal(h.viewportListeners.size,2);
 h.panel.emit('keydown',{key:'Tab',shiftKey:true,preventDefault(){}});assert.equal(h.doc.activeElement.id,'email');
 h.panel.emit('keydown',{key:'Escape',preventDefault(){}});assert.equal(h.doc.activeElement.id,'kchat-fab');assert.equal(h.elements.kchat.attributes['aria-hidden'],'true');assert.equal(h.viewportListeners.size,0);assert.deepEqual(h.background,[true,false]);
});
test('quick question uses text-only API; busy blocks duplicates and keeps a newly typed draft',async()=>{
 const h=fixture();h.starter.click();assert.equal(h.requests.length,1);assert.equal(h.send.disabled,true);assert.equal(h.messages.querySelector('.kchat-welcome'),null);
 assert.deepEqual(JSON.parse(h.requests[0].options.body),{messages:[{role:'user',content:'How does airport pickup work?'}]});
 h.write('A new draft while waiting');h.starter.click();h.send.click();assert.equal(h.requests.length,1);
 await h.reply(0,'<b>This remains literal text</b>');assert.equal(h.input.value,'A new draft while waiting');assert.equal(h.send.disabled,false);
 assert.equal(h.messages.children.at(-1).textContent,'<b>This remains literal text</b>');assert.equal(h.messages.children.at(-1).children.length,0);
});
test('failed request retries the same payload without duplicating the user message or clearing a draft',async()=>{
 const h=fixture();h.write('Compare vehicles');h.send.click();h.requests[0].reject(new Error('offline'));await settle();
 const failure=h.messages.children.at(-1);assert.match(failure.textContent,/couldn’t connect/);assert.equal(h.send.disabled,true);
 h.write('Keep my new draft');failure.children[0].click();assert.equal(h.requests.length,2);assert.equal(h.requests[1].options.body,h.requests[0].options.body);assert.equal(h.input.value,'Keep my new draft');
 await h.reply(1,'How many people are traveling?');assert.equal(h.messages.children.filter(e=>e.className==='km user').length,1);assert.equal(h.messages.children.some(e=>e.className.includes('kchat-error')),false);assert.equal(h.send.disabled,false);
});
test('a stalled request aborts and recovers controls with a manual retry',async()=>{
 const h=fixture();h.write('Airport pickup');h.send.click();h.timeout();await settle();
 assert.equal(h.requests[0].options.signal.aborted,true);assert.match(h.messages.children.at(-1).textContent,/couldn’t connect/);assert.equal(h.messages.attributes['aria-busy'],'false');assert.equal(h.messages.children.at(-1).children[0].textContent,'Try again');
});
test('IME Enter is retained and outgoing conversation history is bounded',async()=>{
 const h=fixture();h.write('正在输入');h.input.emit('keydown',{key:'Enter',isComposing:true,preventDefault(){throw new Error('composition was interrupted');}});assert.equal(h.requests.length,0);
 for(let i=0;i<8;i++){h.write('Question '+i);h.send.click();await h.reply(i,'Answer '+i);}
 const payload=JSON.parse(h.requests.at(-1).options.body);assert.equal(payload.messages.length,12);assert.equal(payload.messages.at(-1).role,'user');assert.equal(payload.messages.at(-1).content,'Question 7');
});
test('closing the assistant stops active dictation and restores its accessible state',()=>{
 const h=fixture({voice:true});h.elements['kchat-fab'].click();h.mic.click();assert.equal(h.mic.attributes['aria-pressed'],'true');h.close.click();assert.equal(h.recognition().stops,1);assert.equal(h.mic.attributes['aria-pressed'],'false');assert.equal(h.doc.activeElement.id,'kchat-fab');
});

test('late dictation results after send or close cannot replace a newer draft',async()=>{
 const h=fixture({voice:true,lateVoice:true});h.elements['kchat-fab'].click();h.mic.click();
 h.recognition().onresult({results:[[{transcript:'Original spoken message'}]]});h.send.click();h.write('Keep this new draft');
 h.recognition().onresult({results:[[{transcript:'A late final result'}]]});assert.equal(h.input.value,'Keep this new draft');
 await h.reply(0,'Reply');h.close.click();h.recognition().onresult({results:[[{transcript:'Another late result'}]]});assert.equal(h.input.value,'Keep this new draft');
});
test('explicitly stopping dictation still accepts its final result before ending',()=>{
 const h=fixture({voice:true,lateVoice:true});h.elements['kchat-fab'].click();h.mic.click();h.mic.click();
 h.recognition().onresult({results:[[{transcript:'Final intentional dictation'}]]});assert.equal(h.input.value,'Final intentional dictation');
 h.recognition().onend();h.recognition().onresult({results:[[{transcript:'Expired result'}]]});assert.equal(h.input.value,'Final intentional dictation');
});

test('image-only send sends the prepared attachment and keeps previews out of ordinary text',async()=>{
 const h=fixture({photos:true});h.elements['kchat-fab'].click();await settle();await h.photos().select([{}]);assert.equal(h.send.disabled,false);h.send.click();const body=JSON.parse(h.requests[0].options.body);assert.equal(body.messages.at(-1).images.length,1);assert.match(body.messages.at(-1).content,/photos/);assert.equal(h.photos().items.length,0);assert.equal(h.messages.children.find(e=>e.className==='km user').children[0].alt,'Sent photo 1');await h.reply(0,'Photo-aware reply');
 h.write('What about a second bag?');h.send.click();assert.equal(JSON.parse(h.requests[1].options.body).messages[0].images.length,1);await h.reply(1,'Follow up');
 await h.photos().select([{},{}]);h.send.click();const next=JSON.parse(h.requests[2].options.body);assert.equal(next.messages.reduce((n,m)=>n+(m.images?.length||0),0),2);
});
test('photo retry retains the exact attachment payload and a newer typed draft',async()=>{
 const h=fixture({photos:true});h.elements['kchat-fab'].click();await settle();await h.photos().select([{}]);h.write('See my luggage');h.send.click();h.requests[0].reject(Error('offline'));await settle();h.write('Keep this draft');h.messages.children.at(-1).children[0].click();assert.equal(h.requests[0].options.body,h.requests[1].options.body);await h.reply(1,'Reply');assert.equal(h.input.value,'Keep this draft');assert.equal(h.messages.children.filter(e=>e.className==='km user').length,1);
});

test('photo failure can explicitly clear image context and continue with text without an automatic send',async()=>{
 const h=fixture({photos:true});h.elements['kchat-fab'].click();await settle();await h.photos().select([{}]);h.write('See my luggage');h.send.click();h.requests[0].reject(Error('unavailable'));await settle();h.write('There are two suitcases');const failure=h.messages.children.at(-1);assert.equal(failure.children[1].textContent,'Continue without photos');failure.children[1].click();assert.equal(h.requests.length,1);assert.equal(h.input.value,'There are two suitcases');h.send.click();assert.equal(JSON.parse(h.requests[1].options.body).messages.some(m=>m.images?.length),false);
});

test('continuing with text also cancels a new photo still being prepared',async()=>{
 let calls=0,release;const h=fixture({photos:true,preparePhoto:()=>++calls===1?Promise.resolve('data:image/jpeg;base64,Zmlyc3Q='):new Promise(r=>release=r)});h.elements['kchat-fab'].click();await settle();await h.photos().select([{}]);h.send.click();h.requests[0].reject(Error('offline'));await settle();const failure=h.messages.children.at(-1);const pending=h.photos().select([{}]);h.write('Two suitcases');failure.children[1].click();release('data:image/jpeg;base64,bGF0ZQ==');await pending;assert.equal(h.photos().items.length,0);h.send.click();assert.equal(JSON.parse(h.requests[1].options.body).messages.some(m=>m.images?.length),false);
});
