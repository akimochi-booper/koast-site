import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const source=readFileSync(new URL('../koast-acquisition.js',import.meta.url),'utf8');
function browser({enabled=true,off=false,fail=false}={}){
 const timers=[],calls=[],listeners={},store=new Map(),anchor={href:'https://app.koastride.com/book?ref=keep#review'};
 const document={querySelector:s=>s.startsWith('meta')?{getAttribute:()=>enabled?'enabled':'disabled'}:{href:'https://koastride.com/wine-tours/napa'},querySelectorAll:()=>[anchor],addEventListener:(k,v)=>{listeners[k]=v},referrer:''};
 const context={document,window:{addEventListener(){}},location:new URL('https://koastride.com/wine-tours/napa'),navigator:{globalPrivacyControl:off},URL,URLSearchParams,crypto,Number,Date,
 sessionStorage:{getItem:k=>store.get(k)||null,setItem:(k,v)=>store.set(k,v)},setTimeout:f=>timers.push(f),
 fetch:async(url,init)=>{calls.push({url,body:JSON.parse(init.body),init});if(url.endsWith('/bridge'))return {ok:!fail,json:async()=>({token:'signed.local.token',expires_at:Date.now()+600000})};return {ok:true};}};
 vm.runInNewContext(source,context);return {timers,calls,anchor,listeners,store};
}
test('approved bridge prepares asynchronously and is carried only to an exact native route fragment',async()=>{
 const b=browser();assert.equal(b.calls.length,1);for(const fn of b.timers)fn();await new Promise(r=>setImmediate(r));
 const u=new URL(b.anchor.href);assert.equal(u.searchParams.get('ref'),'keep');assert.equal(u.hash,'#review&kj=signed.local.token');
 const bridge=b.calls.find(x=>x.url.endsWith('/bridge'));assert.equal(bridge.body.session_id,b.calls[0].body.session_id);assert.deepEqual(Object.keys(bridge.body),['session_id']);assert.equal(bridge.init.referrerPolicy,'no-referrer');
 let prevented=false;b.listeners.click({target:{closest:()=>b.anchor},preventDefault:()=>{prevented=true}});assert.equal(prevented,false);
 b.store.set('koast_tracking_off','1');b.listeners.click({target:{closest:()=>b.anchor}});assert.equal(new URL(b.anchor.href).hash,'#review');assert.equal(new URL(b.anchor.href).searchParams.get('ka_tracking'),'off');
});
test('OFF, privacy and unavailable bridge leave native navigation usable and unlinked',async()=>{
 for(const options of [{enabled:false},{off:true},{fail:true}]){const b=browser(options);for(const fn of b.timers)fn();await new Promise(r=>setImmediate(r));assert.ok(!b.anchor.href.includes('kj='));assert.equal(new URL(b.anchor.href).pathname,'/book');if(options.off||options.enabled===false)assert.ok(!b.calls.some(x=>x.url.endsWith('/bridge')));}
});
