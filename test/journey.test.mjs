import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
const source=readFileSync(new URL('../koast-journey.js',import.meta.url),'utf8');
function browser({enabled=true,off=false}={}){
 const events=[],listeners={},windowListeners={};let now=Date.now();
 class Clock extends Date{constructor(...args){super(...(args.length?args:[now]))}static now(){return now}}
 const doc={visibilityState:'visible',documentElement:{scrollHeight:2000},querySelector:selector=>selector.startsWith('meta[')?{content:enabled?'enabled':'disabled'}:null,querySelectorAll:()=>[],addEventListener:(type,fn)=>listeners[type]=fn};
 const win={innerWidth:390,innerHeight:844,scrollY:0,addEventListener:(type,fn)=>windowListeners[type]=fn};
 const context=vm.createContext({window:win,document:doc,navigator:{userAgent:'Safari/123 secret-raw-agent',language:'en-US'},crypto,Date:Clock,Number,URL,location:new URL('https://koastride.com/wine-tours/napa')});
 vm.runInContext(source,context);win.createKoastJourney({optedOut:()=>off,session:()=>({id:'anonymous',first_touch:{source:'google'}}),path:()=>'/wine-tours/napa',send:payload=>events.push(payload)});
 return {win,doc,events,listeners,windowListeners,advance:ms=>now+=ms,privacy:value=>off=value};
}
test('default-off initializes no observers, event handlers or identity',()=>{
 const b=browser({enabled:false});assert.equal(b.events.length,0);assert.deepEqual(Object.keys(b.listeners),[]);assert.equal(b.win.koastJourney,undefined);
});
test('an initial privacy opt-out creates no journey owner or handlers',()=>{
 const b=browser({off:true});assert.equal(b.events.length,0);assert.equal(b.win.koastJourney,undefined);assert.deepEqual(Object.keys(b.listeners),[]);
});
test('only coarse context and fixed milestone properties are serialized',()=>{
 const b=browser();b.win.koastJourney.record('quote_submit',{email:'private@example.com',notes:'secret',amount:12000});b.win.koastJourney.record('booking_confirmed',{customer:'secret'});
 assert.equal(b.events.length,2);assert.deepEqual(JSON.parse(JSON.stringify(b.events[0].properties)),{device:'phone',browser:'safari',language:'en'});
 assert.doesNotMatch(JSON.stringify(b.events),/private|secret|raw-agent|12000|customer|en-US/);
 assert.deepEqual(b.events.map(x=>x.sequence),[1,2]);
});
test('scroll quartiles are bounded/deduplicated and opt-out stops subsequent events',()=>{
 const b=browser();b.win.scrollY=300;b.windowListeners.scroll();b.windowListeners.scroll();assert.deepEqual(b.events.filter(x=>x.event==='scroll_depth').map(x=>x.properties.percent),[25]);
 b.win.scrollY=2000;b.windowListeners.scroll();assert.deepEqual(b.events.filter(x=>x.event==='scroll_depth').map(x=>x.properties.percent),[25,50,75,100]);
 const count=b.events.length;b.privacy(true);b.win.koastJourney.record('quote_submit');b.windowListeners.scroll();assert.equal(b.events.length,count);
});
test('visibility time excludes hidden duration; duplicate hide does not duplicate an observation',()=>{
 const b=browser();b.advance(10000);b.doc.visibilityState='hidden';b.listeners.visibilitychange();b.windowListeners.pagehide();
 b.advance(60000);b.doc.visibilityState='visible';b.listeners.visibilitychange();b.advance(5000);b.doc.visibilityState='hidden';b.listeners.visibilitychange();
 assert.deepEqual(b.events.filter(x=>x.event==='engagement').map(x=>x.properties.active_seconds),[10,15]);
});
test('private links and invalid properties are discarded and per-page volume is bounded',()=>{
 const b=browser();for(const path of ['/auth/reset','/blog?email=private','https://private.example','/r/private'])b.win.koastJourney.record('navigation_click',{target_path:path});
 assert.equal(b.events.length,1);for(let i=0;i<200;i++)b.win.koastJourney.record('quote_review');assert.equal(b.events.length,80);
});
