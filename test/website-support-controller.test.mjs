import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';

// Exercise the authored Support controller without generating pages or contacting a provider.
const generator=readFileSync(new URL('../generate.py',import.meta.url),'utf8');
const start=generator.indexOf('    var URL_="{CHAT_WORKER_URL}";');
const end=generator.indexOf('  }})();',start);
assert.ok(start>0&&end>start,'Locate the owning inline Support controller');
const source=generator.slice(start,end).replaceAll('{{','{').replaceAll('}}','}')
  .replace('{CHAT_WORKER_URL}','https://synthetic.invalid/chat');
const settle=()=>new Promise(resolve=>setImmediate(resolve));

function fixture(){
  const requests=[],timers=new Map();let timerId=0,document;
  class Element{
    constructor(){this.value='';this.disabled=false;this.children=[];this.listeners={};this.attributes={};this.style={};this.className='';this.textContent='';}
    setAttribute(name,value){this.attributes[name]=value;}
    addEventListener(name,fn){(this.listeners[name]??=[]).push(fn);}
    emit(name,event={}){for(const fn of this.listeners[name]||[])fn(event);}
    click(){if(!this.disabled)this.emit('click');}
    focus(){document.activeElement=this;}
    appendChild(node){this.children.push(node);node.parent=this;return node;}
    remove(){if(this.parent)this.parent.children=this.parent.children.filter(node=>node!==this);}
  }
  const input=new Element(),send=new Element(),messages=new Element();
  const elements={'kai-in':input,'kai-send':send,'kai-msgs':messages};
  document={activeElement:null,getElementById:id=>elements[id],createElement:()=>new Element()};
  const window={};
  vm.runInNewContext(source,{
    window,document,AbortController,
    setTimeout(fn,delay){timers.set(++timerId,{fn,delay});return timerId;},
    clearTimeout(id){timers.delete(id);},
    fetch(url,options){return new Promise((resolve,reject)=>{
      requests.push({url,options,resolve,reject});
      options.signal.addEventListener('abort',()=>reject(new Error('aborted')));
    });},
  });
  const users=()=>messages.children.filter(node=>node.className==='km user');
  const errors=()=>messages.children.filter(node=>node.className==='km bot kai-error');
  return {
    window,document,input,send,messages,requests,timers,users,errors,
    write(text){input.value=text;input.emit('input');},
    async reply(index,text){requests[index].resolve({ok:true,json:async()=>({reply:text})});await settle();},
    async reject(index){requests[index].reject(new Error('offline'));await settle();},
  };
}

test('empty and pending Send states are accurate and busy starters preserve the next draft',async()=>{
  const h=fixture();
  assert.equal(h.send.disabled,true);assert.equal(h.send.attributes['aria-busy'],'false');
  h.write('   ');assert.equal(h.send.disabled,true);
  h.window.kaiAsk('How does airport pickup work?');
  assert.equal(h.requests.length,1);assert.equal(h.send.disabled,true);
  assert.equal(h.send.attributes['aria-busy'],'true');assert.equal(h.messages.attributes['aria-busy'],'true');
  h.write('Keep my next draft');h.window.kaiAsk('A different starter');h.send.click();
  assert.equal(h.requests.length,1);assert.equal(h.input.value,'Keep my next draft');
  await h.reply(0,'Use your confirmed pickup instructions.');
  assert.equal(h.input.value,'Keep my next draft');assert.equal(h.send.disabled,false);
  assert.equal(h.messages.attributes['aria-busy'],'false');assert.equal(h.send.attributes['aria-busy'],'false');
  assert.equal(h.timers.size,0);assert.equal(h.users().length,1);
});

test('IME and Shift+Enter remain native; ordinary Enter sends once and clears the accepted draft',()=>{
  const h=fixture();h.write('Unfinished composition');
  const native=()=>{throw new Error('Native composition was interrupted');};
  for(const extra of [{isComposing:true},{keyCode:229},{shiftKey:true}]){
    h.input.emit('keydown',{key:'Enter',preventDefault:native,...extra});
  }
  assert.equal(h.requests.length,0);assert.equal(h.input.value,'Unfinished composition');
  let prevented=0;h.input.emit('keydown',{key:'Enter',preventDefault(){prevented++;}});
  assert.equal(prevented,1);assert.equal(h.requests.length,1);assert.equal(h.input.value,'');
  assert.equal(JSON.parse(h.requests[0].options.body).messages[0].content,'Unfinished composition');
});

test('manual retry reuses the failed payload without another user bubble or clearing a newer draft',async()=>{
  const h=fixture();h.write('Compare vehicles');h.send.click();await h.reject(0);
  assert.equal(h.errors().length,1);assert.equal(h.send.disabled,true);
  const retry=h.errors()[0].children[0];assert.equal(retry.type,'button');assert.equal(retry.style.minHeight,'44px');
  h.write('Keep this new draft');retry.click();retry.click();
  assert.equal(h.requests.length,2);assert.equal(h.requests[1].options.body,h.requests[0].options.body);
  assert.equal(h.users().length,1);assert.equal(h.errors().length,0);
  assert.equal(h.input.value,'Keep this new draft');assert.equal(h.document.activeElement,h.input);
  await h.reply(1,'How many people are traveling?');
  assert.equal(h.input.value,'Keep this new draft');assert.equal(h.send.disabled,false);
  h.send.click();assert.equal(h.requests.length,3);
  const history=JSON.parse(h.requests[2].options.body).messages;
  assert.deepEqual(history.map(message=>message.role),['user','assistant','user']);
});

test('a stalled request aborts after forty seconds and exposes manual recovery without replay',async()=>{
  const h=fixture();h.write('Airport pickup');h.send.click();h.write('My following draft');
  const timer=[...h.timers.values()][0];assert.equal(timer.delay,40000);timer.fn();await settle();
  assert.equal(h.requests[0].options.signal.aborted,true);assert.equal(h.requests.length,1);
  assert.equal(h.input.value,'My following draft');assert.equal(h.send.disabled,false);
  assert.equal(h.send.attributes['aria-busy'],'false');assert.equal(h.timers.size,0);
  assert.equal(h.errors()[0].children[0].textContent,'Try again');
  h.errors()[0].children[0].click();assert.equal(h.requests.length,2);assert.equal(h.users().length,1);
});

test('HTTP errors, malformed replies and provider error envelopes all remain recoverable failures',async()=>{
  for(const response of [
    {ok:false,json:async()=>({reply:'Do not display this server error as success'})},
    {ok:true,json:async()=>{throw new Error('Invalid JSON');}},
    {ok:true,json:async()=>({reply:'   '})},
    {ok:true,json:async()=>({reply:42})},
    {ok:true,json:async()=>({reply:'Provider unavailable',error:true})},
  ]){
    const h=fixture();h.write('My question');h.send.click();h.requests[0].resolve(response);await settle();
    assert.equal(h.errors().length,1);assert.equal(h.errors()[0].children.length,1);
    assert.equal(h.send.attributes['aria-busy'],'false');assert.equal(h.timers.size,0);
    assert.equal(h.messages.children.some(node=>node.className==='km bot dots'),false);
  }
});

test('new messages retire failed retries, bound conversation history and render replies as literal text',async()=>{
  const h=fixture();h.write('First');h.send.click();await h.reject(0);
  const staleRetry=h.errors()[0].children[0];h.write('A new question');h.send.click();
  assert.equal(h.errors().length,0);assert.equal(h.users().length,2);
  await h.reply(1,'<img src=x onerror=alert(1)>');
  const literal=h.messages.children.at(-1);assert.equal(literal.textContent,'<img src=x onerror=alert(1)>');assert.equal(literal.children.length,0);
  staleRetry.click();assert.equal(h.requests.length,2);
  for(let i=0;i<8;i++){
    h.write('Question '+i);h.send.click();await h.reply(h.requests.length-1,'Answer '+i);
  }
  const history=JSON.parse(h.requests.at(-1).options.body).messages;
  assert.equal(history.length,12);assert.equal(history.at(-1).content,'Question 7');
  assert.equal(h.timers.size,0);
});
