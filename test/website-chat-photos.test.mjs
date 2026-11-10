import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
const code=readFileSync(new URL('../koast-chat-photos.js',import.meta.url),'utf8');
function harness(prepare,capability={photos:true}){
 let active;class Element{constructor(){this.listeners={};this.children=[];this.disabled=false;this.hidden=false;this.files=[];this._text='';}set textContent(t){this._text=t;this.children=[];}get textContent(){return this._text;}addEventListener(k,f){this.listeners[k]=f;}appendChild(e){this.children.push(e);return e;}setAttribute(k,v){this[k]=v;}focus(){active=this;}click(){if(!this.disabled)this.listeners.click?.();}}
 const window={},doc={createElement:()=>new Element()};let changed=0;
 vm.runInNewContext(code,{window,document:doc,DataView,Uint8Array,AbortSignal,createImageBitmap:()=>{},fetch:async()=>{if(capability instanceof Error)throw capability;return {ok:true,json:async()=>capability};}});
 const o={button:new Element(),picker:new Element(),tray:new Element(),notice:new Element(),onChange:()=>changed++,prepare};
 return {p:new window.KoastPhotoComposer(o),o,api:window.KoastPhotoPreparation,active:()=>active};
}
test('photo choice is gated by capability and keeps preparation local until taken',async()=>{
 const h=harness(async f=>'data:image/jpeg;base64,'+f.name);await h.p.select([{name:'ignored'}]);assert.equal(h.p.items.length,0);
 await h.p.load('https://example.test');await h.p.select([{name:'a'},{name:'b'}]);assert.equal(h.p.items.length,2);assert.equal(h.o.button.disabled,true);assert.equal(h.o.tray.children.length,2);
 assert.equal(h.p.take().length,2);assert.equal(h.p.items.length,0);assert.equal(h.o.tray.hidden,true);
});
test('batch conversion failure is atomic and leaves a prior photo intact',async()=>{
 const h=harness(async f=>{if(f.bad)throw Error('Invalid photo');return 'data:image/jpeg;base64,a';});h.p.enabled=true;
 await h.p.select([{}]);await h.p.select([{bad:true}]);assert.equal(h.p.items.length,1);assert.equal(h.o.notice.textContent,'Invalid photo');assert.equal(h.p.processing,false);
});
test('closing during preparation discards late results and restores controls',async()=>{
 let finish;const h=harness(()=>new Promise(r=>finish=r));h.p.enabled=true;const pending=h.p.select([{}]);assert.equal(h.p.processing,true);h.p.cancelPreparation();finish('data:image/jpeg;base64,late');await pending;assert.equal(h.p.items.length,0);assert.equal(h.p.processing,false);
});
test('removal returns focus to attach and busy blocks file changes',async()=>{
 const h=harness(async()=> 'data:image/jpeg;base64,a');h.p.enabled=true;await h.p.select([{}]);h.o.tray.children[0].children[1].click();assert.equal(h.p.items.length,0);assert.equal(h.active(),h.o.button);
 h.p.setBusy(true);await h.p.select([{}]);assert.equal(h.p.items.length,0);assert.equal(h.o.button.disabled,true);
});
test('count guard rejects oversize batches before decoding',async()=>{
 let calls=0;const h=harness(async()=>{calls++;return 'data:image/jpeg;base64,a';});h.p.enabled=true;await h.p.select([{},{},{}]);assert.equal(calls,0);assert.match(h.o.notice.textContent,/2 photos/);
});
test('original file size/type and decompression bomb headers are rejected before bitmap decode',async()=>{
 const h=harness();await assert.rejects(h.api.prepare({size:9*1024*1024,type:'image/jpeg'}),/8 MB/);
 await assert.rejects(h.api.prepare({size:1,type:'image/svg+xml'}),/JPEG/);
 const bytes=new Uint8Array(24),v=new DataView(bytes.buffer);v.setUint32(0,0x89504e47);v.setUint32(4,0x0d0a1a0a);v.setUint32(12,0x49484452);v.setUint32(16,100000);v.setUint32(20,100000);
 await assert.rejects(h.api.prepare({size:24,type:'image/png',arrayBuffer:async()=>bytes.buffer}),/too large/);
 await assert.rejects(h.api.prepare({size:24,type:'image/jpeg',arrayBuffer:async()=>bytes.buffer}),/valid image/);
});
test('non-image bytes cannot be decoded as uploaded photos',()=>{const h=harness();assert.throws(()=>h.api.dimensions(new TextEncoder().encode('<svg onload="evil()"/>')),/JPEG/);});

test('cancelled batch never starts file two or overlaps a replacement decode',async()=>{
 let release,calls=0;const h=harness(()=>{calls++;return new Promise(r=>release=r);});h.p.enabled=true;const old=h.p.select([{},{}]);h.p.cancelPreparation();await h.p.select([{}]);assert.equal(calls,1);assert.equal(h.p.processing,true);release('data:image/jpeg;base64,old');await old;assert.equal(calls,1);assert.equal(h.p.items.length,0);assert.equal(h.p.processing,false);const next=h.p.select([{}]);assert.equal(calls,2);release('data:image/jpeg;base64,new');await next;assert.equal(h.p.items.length,1);
});
test('false and unavailable capabilities keep attachments hidden and allow a later retry',async()=>{
 for(const result of [{photos:false},new Error('offline')]){const h=harness(null,result);await h.p.load('https://example.test');assert.equal(h.p.enabled,false);assert.equal(h.o.button.hidden,true);assert.equal(h.p.loaded,false);}
});
test('PNG, JPEG and all common WebP headers return expected dimensions',()=>{
 const h=harness();const png=new Uint8Array(30),p=new DataView(png.buffer);p.setUint32(0,0x89504e47);p.setUint32(4,0x0d0a1a0a);p.setUint32(12,0x49484452);p.setUint32(16,800);p.setUint32(20,600);assert.deepEqual(Array.from(h.api.dimensions(png)),[800,600,'image/png']);
 const jpeg=Uint8Array.from([255,216,255,192,0,8,8,2,88,3,32,3,0,0]);assert.deepEqual(Array.from(h.api.dimensions(jpeg)),[800,600,'image/jpeg']);
 for(const kind of [0x56503858,0x56503820,0x5650384c]){const bytes=new Uint8Array(30),v=new DataView(bytes.buffer);v.setUint32(0,0x52494646);v.setUint32(8,0x57454250);v.setUint32(12,kind);if(kind===0x56503858){bytes[24]=31;bytes[25]=3;bytes[27]=87;bytes[28]=2;}else if(kind===0x56503820){bytes[23]=157;bytes[24]=1;bytes[25]=42;v.setUint16(26,800,true);v.setUint16(28,600,true);}else{bytes[20]=47;bytes[21]=31;bytes[22]=195;bytes[23]=149;}assert.deepEqual(Array.from(h.api.dimensions(bytes)),[800,600,'image/webp']);}
 for(const bytes of [new Uint8Array(0),Uint8Array.from([255,216,255,192,0,255])])assert.throws(()=>h.api.dimensions(bytes),/JPEG/);
});
