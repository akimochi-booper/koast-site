import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';

const source=readFileSync(new URL('../quote-request.js',import.meta.url),'utf8');
const context=vm.createContext({fetch,Date,AbortSignal,crypto});vm.runInContext(source,context);
const ID='4c13433d-29a0-40b5-8a64-86f915af028c',NOW=Date.parse('2026-11-17T07:00:00Z');
const base={name:'Website QA',email:'quote-test@example.com',pickup:'Hotel entrance',date:'2026-11-21',party:'4',region:'Livermore Valley',vehicle:'SUV',tourId:'livermore-private-suv-day',tourTitle:'Livermore, Your Way',notes:'Hotel return',page:'/wine-tours/livermore'};
const create=transport=>context.createQuoteSubmission({transport,uuid:()=>ID,now:()=>NOW});

test('name and reply email validation fails before starting a request',async()=>{
 let calls=0;const controller=create(async()=>{calls++;});
 assert.equal((await controller.submit({...base,name:''})).field,'name');
 assert.equal((await controller.submit({...base,email:'bad'})).field,'email');assert.equal(calls,0);assert.equal(controller.state().locked,false);
});

test('a double click sends once while pending and success cannot be resent',async()=>{
 let complete,calls=0;const controller=create(async()=>{calls++;return new Promise(resolve=>{complete=resolve;});});
 const pending=controller.submit(base);assert.equal(controller.state().pending,true);assert.equal(controller.state().locked,true);
 assert.equal((await controller.submit(base)).pending,true);assert.equal(calls,1);
 complete(Response.json({ok:true,reference:ID}));assert.equal((await pending).ok,true);assert.equal(controller.state().accepted,ID);
 assert.equal((await controller.submit(base)).ok,true);assert.equal(calls,1);
});

test('uncertain retry sends the identical frozen payload and key despite edited values',async()=>{
 const bodies=[];const controller=create(async(url,init)=>{assert.equal(url,'https://koast-chat.euburaga.workers.dev/quote-requests');assert.equal(init.credentials,'omit');bodies.push(init.body);if(bodies.length===1)throw Error('reply lost');return Response.json({ok:true,reference:ID});});
 assert.equal((await controller.submit(base)).error,'delivery_unconfirmed');assert.equal(controller.state().locked,true);assert.equal(controller.reset(),false);
 assert.equal((await controller.submit({...base,pickup:'Different hotel',email:'different@example.com'})).ok,true);assert.equal(bodies[0],bodies[1]);
 const body=JSON.parse(bodies[1]);assert.equal(body.pickup,base.pickup);assert.equal(body.email,base.email);assert.equal(body.requestId,ID);
});

test('non-JSON, unknown success, unavailable and mismatched receipt responses remain unconfirmed',async()=>{
 for(const transport of [async()=>new Response('bad'),async()=>Response.json({ok:true,reference:'other'}),async()=>Response.json({error:'unavailable'},{status:503})]){
  const controller=create(transport);assert.equal((await controller.submit(base)).error,'delivery_unconfirmed');assert.equal(controller.state().accepted,null);assert.equal(controller.state().locked,true);
 }
});

test('definite validation errors allow correction, rate limits retain the request and expiry blocks automatic resend',async()=>{
 const invalid=create(async()=>Response.json({error:'email',field:'email'},{status:400}));assert.equal((await invalid.submit(base)).error,'invalid_request');assert.equal(invalid.state().locked,false);
 const limited=create(async()=>Response.json({error:'rate_limit'},{status:429}));assert.equal((await limited.submit(base)).error,'rate_limit');assert.equal(limited.state().locked,true);
 let clock=NOW,calls=0;const expired=context.createQuoteSubmission({uuid:()=>ID,now:()=>clock,transport:async()=>{calls++;throw Error('unknown');}});
 await expired.submit(base);clock+=24*3600000;assert.equal((await expired.submit(base)).error,'expired_request');assert.equal(calls,1);assert.equal(expired.state().expired,true);
});

test('form data never enters browser storage, analytics or automatic customer email',()=>{
 assert.doesNotMatch(source,/localStorage|sessionStorage|sendBeacon|analytics|mailto:/);
});
