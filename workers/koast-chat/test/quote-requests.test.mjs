import test from 'node:test';
import assert from 'node:assert/strict';
import worker from '../worker.js';
import {handleQuoteRequests,validateQuoteRequest,quoteEmail,quoteRequestsReady} from '../quote-requests.mjs';

const NOW=Date.parse('2026-11-17T07:00:00Z');
const ID='4c13433d-29a0-40b5-8a64-86f915af028c';
const receipt='7c13433d-29a0-40b5-8a64-86f915af028c';
const base={requestId:ID,createdAt:NOW,name:'Website QA',email:'quote-test@example.com',pickup:'Hotel entrance & <lobby>',date:'2026-11-21',party:'7+',region:'Livermore Valley',vehicle:'Executive Sprinter',tourId:'livermore-executive-sprinter-day',tourTitle:'Livermore, Together',notes:'Wente & Concannon\nReturn to hotel',page:'/wine-tours/livermore',website:''};
function environment(){return {QUOTE_EMAIL_KEY:'local-stub-key',QUOTE_EMAIL_FROM:'Koast Website <quotes@koastride.com>',QUOTE_RATE_LIMITER:{limit:async()=>({success:true})},QUOTE_GLOBAL_LIMITER:{limit:async()=>({success:true})}};}
function request(body=base,headers={},method='POST'){return new Request('https://service.example/quote-requests',{method,headers:{Origin:'https://koastride.com','Content-Type':'application/json','CF-Connecting-IP':'192.0.2.1',...headers},...(method==='POST'?{body:typeof body==='string'?body:JSON.stringify(body)}:{})});}
const options=transport=>({now:NOW,transport});

test('request validation bounds contact/trip fields, real dates, paths and retry lifetime',()=>{
 assert.equal(validateQuoteRequest(base,NOW).quote.name,'Website QA');
 for(const [field,value] of [['name','\nInjected'],['email','customer@example.com\r\nBcc: other@example.com'],['pickup','x'.repeat(181)],['party','30'],['date','2026-02-30'],['date','2026-11-15'],['vehicle','Confirmed bus'],['notes','x'.repeat(1201)],['page','/wine-tours/livermore?email=private'],['tourId','<script>'],['website','bot']]) assert.ok(validateQuoteRequest({...base,[field]:value},NOW).error,field);
 assert.equal(validateQuoteRequest({...base,createdAt:NOW-24*3600000},NOW).error,'expired_request');
 assert.equal(validateQuoteRequest({...base,date:''},NOW).quote.date,'');
 assert.equal(validateQuoteRequest({...base,name:'   '},NOW).field,'name');
 assert.equal(validateQuoteRequest({...base,date:'2026-11-16'},NOW+22*3600000).quote.date,'2026-11-16','an unchanged retry stays valid across Pacific midnight');
});

test('only the fixed team inbox receives the branded enquiry and text alternative with customer reply-to',()=>{
 const payload=quoteEmail({...base,to:'attacker@example.com',from:'attacker@example.com'},'Koast Website <quotes@koastride.com>');
 assert.deepEqual(payload.to,['reserve@koastride.com']);assert.equal(payload.reply_to,base.email);
 assert.equal(payload.from,'Koast Website <quotes@koastride.com>');assert.match(payload.html,/<!doctype html>/);
 for(const value of [ID,base.name,base.email,base.pickup,base.vehicle,base.tourId,base.tourTitle,base.notes,'7+ guests','No booking'])assert.ok(payload.text.includes(value),value);
});

test('the inquiry presents human trip details before technical references and preserves untrusted notes safely',()=>{
 const quote={...base,name:'Alex <Guest> & "Team"',notes:'<img src=x onerror=alert(1)>\nSecond line & final request'};
 const payload=quoteEmail(quote,'Koast Website <quotes@koastride.com>');
 assert.match(payload.html,/Alex &lt;Guest&gt; &amp; &quot;Team&quot;/);
 assert.ok(payload.html.includes('&lt;img src=x onerror=alert(1)&gt;\nSecond line &amp; final request'));
 assert.doesNotMatch(payload.html,/<img src=x|<script/);
 assert.ok(payload.text.includes(quote.notes),'plain-text alternative retains the original customer note');
 assert.ok(payload.html.indexOf('Trip request')<payload.html.indexOf('Reference:'));
 assert.match(payload.html,/Sat, Nov 21, 2026/);
 assert.match(payload.subject,/Website inquiry · Livermore Valley · Sat, Nov 21, 2026 · Alex/);
 assert.match(payload.html,/7\+ guests — exact count to confirm/);
 assert.match(payload.html,/href="mailto:quote-test%40example.com"/);
 assert.match(payload.html,/https:\/\/koastride.com\/wine-tours\/livermore/);
 assert.match(payload.html,/width="146" height="45"/);
});

test('unknown plans remain unknown and a date-only choice never shifts to the previous day',()=>{
 const payload=quoteEmail({...base,date:'',vehicle:'',tourId:'',tourTitle:'',notes:''},'Koast Website <quotes@koastride.com>');
 for(const value of ['Date not provided','Customer would like help choosing','No day idea selected','No additional notes provided.','No booking']) {
  assert.ok(payload.text.includes(value),value);assert.ok(payload.html.includes(value),value);
 }
 assert.doesNotMatch(payload.text,/Phone:|Confirmed pickup|Confirmed itinerary/);
 const dated=quoteEmail({...base,date:'2026-11-21'},'Koast Website <quotes@koastride.com>');
 assert.match(dated.text,/Sat, Nov 21, 2026/);assert.doesNotMatch(dated.text,/Fri, Nov 20/);
});

test('origin, method and content-type rejection never call the email provider',async()=>{
 let calls=0;const run=(req)=>handleQuoteRequests(req,environment(),options(async()=>{calls++;throw Error('must not call');}));
 assert.equal((await run(request(base,{Origin:'https://other.example'}))).status,403);
 assert.equal((await run(request(base,{Origin:''}))).status,403);
 assert.equal((await run(request(null,{},'GET'))).status,405);
 assert.equal((await run(request(base,{'Content-Type':'text/plain'}))).status,415);
 const preflight=await run(request(null,{},'OPTIONS'));assert.equal(preflight.status,204);assert.equal(preflight.headers.get('Access-Control-Allow-Origin'),'https://koastride.com');assert.equal(calls,0);
});

test('missing delivery configuration and limiter failures fail closed',async()=>{
 let calls=0;const transport=async()=>{calls++;throw Error('must not call');};
 for(const field of ['QUOTE_EMAIL_KEY','QUOTE_EMAIL_FROM','QUOTE_RATE_LIMITER','QUOTE_GLOBAL_LIMITER']){
  const env=environment();delete env[field];assert.equal(quoteRequestsReady(env),false);assert.equal((await handleQuoteRequests(request(),env,options(transport))).status,503);
 }
 const env=environment();env.QUOTE_RATE_LIMITER.limit=async()=>{throw Error('offline');};
 assert.equal((await handleQuoteRequests(request(),env,options(transport))).status,503);
 assert.equal((await handleQuoteRequests(request(base,{'CF-Connecting-IP':''}),environment(),options(transport))).status,503);assert.equal(calls,0);
});

test('per-address and shared rate limits return a wait period before delivery',async()=>{
 for(const limiter of ['QUOTE_RATE_LIMITER','QUOTE_GLOBAL_LIMITER']){
  const env=environment();env[limiter].limit=async()=>({success:false});let calls=0;
  const response=await handleQuoteRequests(request(),env,options(async()=>{calls++;}));assert.equal(response.status,429);assert.equal(response.headers.get('Retry-After'),'60');assert.equal(calls,0);
 }
});

test('oversized, malformed and invalid input cannot send mail',async()=>{
 for(const [input,status] of [['x'.repeat(8193),413],['{bad',400],[{...base,email:'bad'},400],[{...base,createdAt:NOW-24*3600000},409]]){
  let calls=0;const response=await handleQuoteRequests(request(input),environment(),options(async()=>{calls++;}));assert.equal(response.status,status);assert.equal(calls,0);assert.equal(response.headers.get('Cache-Control'),'no-store');
 }
});

test('accepted email response returns a reference and stable key, without exposing provider/customer fields',async()=>{
 const sent=[];const env=environment();let addressKey;
 env.QUOTE_RATE_LIMITER.limit=async value=>{addressKey=value.key;return {success:true};};
 const transport=async(url,init)=>{sent.push({url,init});return Response.json({id:receipt});};
 for(let n=0;n<2;n++){
  const response=await handleQuoteRequests(request(),env,options(transport));assert.equal(response.status,200);assert.deepEqual(await response.json(),{ok:true,reference:ID});assert.equal(response.headers.get('Cache-Control'),'no-store');
 }
 assert.match(addressKey,/^[a-f0-9]{64}$/);assert.notEqual(addressKey,'192.0.2.1');
 assert.equal(sent[0].url,'https://api.resend.com/emails');assert.equal(sent[0].init.headers['Idempotency-Key'],'website-quote/'+ID);assert.equal(sent[0].init.body,sent[1].init.body);
});

test('provider error, timeout, malformed response or missing receipt never claim success',async()=>{
 for(const transport of [async()=>new Response('private diagnostic',{status:500}),async()=>{throw Error('timeout');},async()=>Response.json({ok:true}),async()=>new Response('{broken'),async()=>new Response('x'.repeat(4097))]){
  const response=await handleQuoteRequests(request(),environment(),options(transport));assert.equal(response.status,503);assert.deepEqual(await response.json(),{error:'delivery_unconfirmed',reference:ID});
 }
});

test('the existing Worker routes enquiries separately without using the assistant/model path',async()=>{
 const response=await worker.fetch(request(),{});assert.equal(response.status,503);assert.deepEqual(await response.json(),{error:'unavailable'});
});
