import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync,readdirSync} from 'node:fs';
import {randomUUID} from 'node:crypto';
import {join} from 'node:path';
const source=readFileSync(new URL('../koast-acquisition.js',import.meta.url),'utf8');
function browser(options={}) {
  const url=new URL(options.url || 'https://koastride.com/services/wine-tours?utm_source=google&utm_medium=organic&utm_campaign=autumn');
  const events=[], listeners={}, store=options.store || new Map();
  let now=options.now || 1_000_000;
  const navigator={...options.navigator};
  const document={referrer:options.referrer || '', querySelector:()=>options.noCanonical?null:{href:'https://koastride.com/services/wine-tours'},
    addEventListener:(type,fn)=>listeners[type]=fn};
  const context=vm.createContext({URL,URLSearchParams,Number,window:{addEventListener:(type,fn)=>listeners[type]=fn},location:url,document,navigator,crypto:{randomUUID},
    Date:{now:()=>now},sessionStorage:{getItem:k=>{if(options.brokenStorage)throw Error('denied');return store.get(k)||null},setItem:(k,v)=>{if(options.brokenStorage)throw Error('denied');store.set(k,v)}},
    fetch:(endpoint,init)=>{if(options.brokenFetch)throw Error('offline');events.push({endpoint,init,data:JSON.parse(init.body)});return Promise.resolve({ok:true})}});
  function run(){vm.runInContext(source,context)}
  run();
  return {events,store,run,navigator,advance:ms=>now+=ms,pageshow:persisted=>listeners.pageshow?.({persisted}),click:href=>{
    let canceled=false;listeners.click?.({target:{closest:()=>({href})},preventDefault:()=>canceled=true});assert.equal(canceled,false);
  }};
}
test('one page view per document, sanitized campaign and referring origin only',()=>{
 const b=browser({referrer:'https://www.google.com/search?q=private@example.com'});b.run();
 assert.equal(b.events.length,1);const p=b.events[0].data;
 assert.equal(p.event,'page_view');assert.equal(p.path,'/services/wine-tours');assert.equal(p.referrer,'https://www.google.com');
 assert.equal(p.utm_source,'google');assert.equal(p.first_touch.campaign,'autumn');
 assert.equal(b.events[0].init.credentials,'omit');assert.equal(b.events[0].init.referrerPolicy,'no-referrer');
 assert.equal(JSON.stringify(p).includes('private@example.com'),false);
});
test('booking and contact clicks count intent without addresses, URLs or navigation interception',()=>{
 const b=browser(); b.click('https://customer.moovs.app/koast/request/new?email=private@example.com');
 b.click('tel:+14155551212');b.click('mailto:private@example.com');b.click('https://app.koastride.com/book');
 b.click('https://customer.moovs.app/another/request/new');b.click('https://app.koastride.com/account');b.click('https://koastride.com/blog');
 assert.deepEqual(b.events.map(x=>[x.data.event,x.data.destination]),[['page_view',''],['booking_click','moovs'],['contact_click','phone'],['contact_click','email'],['booking_click','book']]);
 const json=JSON.stringify(b.events);assert.equal(json.includes('private@example.com'),false);assert.equal(json.includes('14155551212'),false);
 assert.equal(new Set(b.events.map(x=>x.data.event_id)).size,5);
});
test('DNT, GPC, opt out and non-production hosts suppress all events',()=>{
 for(const opt of [{navigator:{doNotTrack:'1'}},{navigator:{globalPrivacyControl:true}},{url:'https://koastride.com/?koast_tracking=off'},{url:'http://localhost:8770/'},{url:'https://preview.koast.pages.dev/'},{url:'http://koastride.com/'}]){
  const b=browser(opt);b.click('tel:123');assert.equal(b.events.length,0);
 }
 const store=new Map();browser({store,url:'https://koastride.com/?koast_tracking=off'});assert.equal(browser({store}).events.length,0);
 const b=browser();b.navigator.globalPrivacyControl=true;b.click('tel:123');assert.equal(b.events.length,1);
});
test('session identity and attribution survive internal navigation, then expire after 30 idle minutes',()=>{
 const first=browser({now:1_000_000});
 const second=browser({store:first.store,now:1_100_000,url:'https://koastride.com/blog',referrer:'https://koastride.com/services/wine-tours?email=secret@example.com'});
 assert.equal(second.events[0].data.session_id,first.events[0].data.session_id);
 assert.equal(second.events[0].data.utm_source,'google');assert.equal(second.events[0].data.referrer,'');
 const third=browser({store:first.store,now:3_000_001,url:'https://koastride.com/'});
 assert.notEqual(third.events[0].data.session_id,first.events[0].data.session_id);assert.equal(third.events[0].data.utm_source,'');
});
test('new campaigns update last touch while keeping first touch',()=>{
 const first=browser();const second=browser({store:first.store,url:'https://koastride.com/?utm_source=newsletter&utm_medium=email&utm_campaign=holiday'});
 const p=second.events[0].data;assert.equal(p.first_touch.source,'google');assert.equal(p.utm_source,'newsletter');
});
test('reject personal-looking campaign labels and unknown paths',()=>{
 const b=browser({url:'https://koastride.com/private@example.com?utm_source=person%40example.com&utm_campaign=14155551212&utm_term=https%3A%2F%2Fbad.test',noCanonical:true});
 const p=b.events[0].data;assert.equal(p.path,'/404');assert.equal(p.utm_source,'');assert.equal(p.utm_campaign,'');assert.equal(Object.hasOwn(p,'utm_term'),false);
});
test('storage and network failures do not break browsing; in-memory session still works',()=>{
 const b=browser({brokenStorage:true});b.click('tel:123');assert.equal(b.events[0].data.session_id,b.events[1].data.session_id);
 assert.doesNotThrow(()=>browser({brokenFetch:true}).click('tel:123'));
 const bad=browser({store:new Map([['koast_acquisition_v1','invalid json']])});assert.equal(bad.events.length,1);
});
test('every generated HTML page loads the tracker once and CSP permits collector',()=>{
 const root=new URL('..',import.meta.url).pathname.replace(/^\/([A-Za-z]:)/,'$1');
 function html(dir){return readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()&&!e.name.startsWith('.')?html(join(dir,e.name)):e.isFile()&&e.name.endsWith('.html')?[join(dir,e.name)]:[])}
 const pages=html(root);assert.ok(pages.length>100,'Run python generate.py before this test');
 for(const p of pages){const text=readFileSync(p,'utf8');assert.equal((text.match(/src="\/koast-acquisition\.js\?v=2"/g)||[]).length,1,p);assert.equal(p.includes('care-rides.html'),false);}
 const headers=readFileSync(new URL('../_headers',import.meta.url),'utf8');assert.match(headers,/connect-src[^;]*https:\/\/koast-platform\.euburaga\.workers\.dev/);
});

test('campaign labels match backend grammar, length, and lowercase contract',()=>{
 for(const label of ['Wine + Dinner (October)','x'.repeat(81),'1234567','-leading']){
  const b=browser({url:'https://koastride.com/?utm_campaign='+encodeURIComponent(label)});
  assert.equal(b.events[0].data.utm_campaign,'');
 }
 const b=browser({url:'https://koastride.com/?utm_campaign=Autumn_2026-VIP.A'});
 assert.equal(b.events[0].data.utm_campaign,'autumn_2026-vip.a');
});
test('advertising marker types persist without transmitting or storing their values or search terms',()=>{
 for(const [key,type] of [['gclid','google'],['gbraid','google'],['wbraid','google'],['msclkid','microsoft'],['fbclid','meta']]){
  const b=browser({url:'https://koastride.com/?'+key+'=sensitive-click-identity&utm_term=sensitive-search-phrase'});
  assert.equal(b.events[0].data.first_touch.click_id_type,type);
  const next=browser({store:b.store,url:'https://koastride.com/blog',referrer:'https://koastride.com/'});
  assert.equal(next.events[0].data.first_touch.click_id_type,type);
  for(const serialized of [JSON.stringify(b.events),JSON.stringify(next.events),JSON.stringify([...b.store])]){
   assert.equal(serialized.includes('sensitive-click-identity'),false);assert.equal(serialized.includes('sensitive-search-phrase'),false);
   assert.equal(serialized.includes('utm_term'),false);
  }
 }
 assert.equal(browser({url:'https://koastride.com/?gclid='}).events[0].data.first_touch.click_id_type,'');
});
test('restored history pages count another page view, respect opt out, and expire idle sessions',()=>{
 const b=browser();const original=b.events[0].data.session_id;
 b.pageshow(false);assert.equal(b.events.length,1);
 b.pageshow(true);assert.equal(b.events.length,2);assert.equal(b.events[1].data.session_id,original);
 b.advance(30*60*1000);b.pageshow(true);assert.notEqual(b.events[2].data.session_id,original);
 b.store.set('koast_tracking_off','1');b.pageshow(true);assert.equal(b.events.length,3);
});
test('restored history page adopts the newer session written in the same tab',()=>{
 const b=browser();const next=browser({store:b.store,now:3_000_001,url:'https://koastride.com/?utm_source=newsletter'});
 b.advance(2_000_002);b.pageshow(true);
 assert.equal(b.events[1].data.session_id,next.events[0].data.session_id);
 assert.equal(b.events[1].data.first_touch.source,'newsletter');
});

test('Moovs login and unrelated or lookalike paths are not booking intent',()=>{
 const b=browser();
 for(const href of [
  'https://customer.moovs.app/koast/new/info',
  'https://customer.moovs.app/koast/',
  'https://customer.moovs.app/koast/iframe',
  'https://customer.moovs.app/koast/request/newer',
  'https://customer.moovs.app/koast/request/new/extra',
  'https://customer.moovs.app/koast-other/request/new',
  'https://customer.moovs.app.evil.example/koast/request/new',
  'http://customer.moovs.app/koast/request/new'
 ]) b.click(href);
 assert.equal(b.events.length,1,'Non-booking paths must not add booking clicks');
 for(const href of [
  'https://customer.moovs.app/koast/request/new',
  'https://customer.moovs.app/koast/request/new/?utm_source=website',
  'https://customer.moovs.app/koast/request/new#ride'
 ]) b.click(href);
 assert.deepEqual(b.events.slice(1).map(x=>[x.data.event,x.data.destination]),[
  ['booking_click','moovs'],['booking_click','moovs'],['booking_click','moovs']
 ]);
});