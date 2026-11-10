import test from 'node:test';
import assert from 'node:assert/strict';
import worker from '../worker.js';

test('planning instructions receive answered context and preserve the stateless tool-less contract',async t=>{
 const messages=[
  {role:'user',content:'We need SFO to Napa on November 20 for four adults.'},
  {role:'assistant',content:'How much luggage will your group have?'},
  {role:'user',content:'Four checked bags. No child seats. What should we do next?'}
 ];
 let sent;
 t.mock.method(globalThis,'fetch',async(url,init)=>{
  if(String(url).endsWith('/llms.txt'))return new Response('Verified Koast ground transportation information. '.repeat(20));
  sent=JSON.parse(init.body);
  return Response.json({status:'completed',output:[{type:'message',content:[{type:'output_text',text:'Get a quote at https://customer.moovs.app/koast/request/new.'}]}]});
 });
 const request=new Request('https://koast-chat.euburaga.workers.dev/',{method:'POST',headers:{Origin:'https://koastride.com','Content-Type':'application/json'},body:JSON.stringify({messages})});
 const response=await worker.fetch(request,{OPENAI_API_KEY:'test-only-key'});
 assert.deepEqual(sent.input,messages);assert.equal(sent.store,false);assert.equal(sent.tools,undefined);
 assert.equal(sent.model,'gpt-6.1-sol');assert.equal(response.status,200);
 assert.deepEqual(await response.json(),{reply:'Get a quote at https://customer.moovs.app/koast/request/new.'});
 assert.match(sent.instructions,/at most ONE relevant follow-up question at a time/);
 assert.match(sent.instructions,/Do not repeat questions already answered/);
 assert.match(sent.instructions,/general service question, answer directly/);
 assert.match(sent.instructions,/Do not request IDs, card\/payment details, account credentials/);
 assert.match(sent.instructions,/exact private street address/);
 assert.match(sent.instructions,/Once enough context is available/);
 assert.match(sent.instructions,/Never claim a live price, live availability/);
 assert.match(sent.instructions,/Larger vans, Sprinters and buses require a quote/);
 assert.match(sent.instructions,/never use a markdown link/);
 assert.match(sent.instructions,/Never invent a URL/);
});
