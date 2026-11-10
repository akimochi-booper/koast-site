import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import worker from '../worker.js';
import {inspectJpeg,MAX_BODY_BYTES,MAX_PHOTO_BYTES} from '../photo-input.mjs';

const jpeg = new Uint8Array(readFileSync(new URL('./fixtures/photo.jpg',import.meta.url)));
const encoded = new Uint8Array(readFileSync(new URL('./fixtures/encoded-photo.jpg',import.meta.url)));
const url = bytes => 'data:image/jpeg;base64,'+Buffer.from(bytes).toString('base64');
const photoMessage = (images=[url(jpeg)],content='Will this luggage fit?') => ({role:'user',content,images});
const request = (messages=[photoMessage()], headers={}) => new Request('https://koast-chat.euburaga.workers.dev/',{method:'POST',headers:{Origin:'https://koastride.com','Content-Type':'application/json','CF-Connecting-IP':'203.0.113.5',...headers},body:JSON.stringify({messages})});
const response = {status:'completed',model:'gpt-6.1-sol',output:[{type:'message',content:[{type:'output_text',text:'How many people are traveling?'}]}]};
function withMetadata(bytes) {
  const metadata = new TextEncoder().encode('Exif\0\0GPS PRIVATE-METADATA <script>');
  const length = metadata.length+2;
  return Uint8Array.from([255,216,255,225,length>>8,length&255,...metadata,...bytes.subarray(2)]);
}
function fixture(t,options={}) {
  const seen={info:[],source:[],transforms:[],outputs:[],rates:[],fetches:[]};
  const env={OPENAI_API_KEY:'test-key',
    IMAGES:{info:async stream=>{seen.info.push(new Uint8Array(await new Response(stream).arrayBuffer()));return options.info||{format:'jpeg',width:16,height:12};},input(stream){
      const chain={transform(value){seen.transforms.push(value);return chain;},async output(value){seen.outputs.push(value);seen.source.push(new Uint8Array(await new Response(stream).arrayBuffer()));if(options.transformError)throw Error('PRIVATE_PROVIDER_MESSAGE');return {response:()=>new Response(options.encoded||withMetadata(encoded),{headers:{'Content-Type':'image/jpeg'}})};}};return chain;
    }},
    PHOTO_RATE_LIMITER:{limit:async value=>{seen.rates.push(['ip',value]);return {success:options.ipAllowed!==false};}},
    PHOTO_GLOBAL_LIMITER:{limit:async value=>{seen.rates.push(['shared',value]);return {success:options.sharedAllowed!==false};}}
  };
  t.mock.method(globalThis,'fetch',async (target,init)=>{seen.fetches.push({target,init});return String(target).endsWith('/llms.txt')?new Response('Verified airport and ground transportation facts. '.repeat(20)):Response.json(response);});
  return {env,seen};
}

test('uses decoded and re-encoded image input without forwarding source metadata',async t=>{
  const {env,seen}=fixture(t);const res=await worker.fetch(request([photoMessage([url(withMetadata(jpeg))])]),env);
  assert.equal(res.status,200);assert.equal(res.headers.get('Cache-Control'),'no-store');
  assert.deepEqual(await res.json(),{reply:'How many people are traveling?'});
  const body=JSON.parse(seen.fetches.at(-1).init.body);
  assert.equal(body.store,false);assert.equal(body.tools,undefined);assert.equal(body.input.length,1);
  assert.equal(body.input[0].content[0].type,'input_text');assert.equal(body.input[0].content[1].type,'input_image');
  assert.equal(body.input[0].content[1].detail,'auto');assert.notEqual(body.input[0].content[1].image_url,url(jpeg));
  const cleaned=Buffer.from(body.input[0].content[1].image_url.split(',')[1],'base64');
  assert.equal(inspectJpeg(cleaned).width,8);assert.equal(cleaned.includes(Buffer.from('PRIVATE-METADATA')),false);
  assert.equal(Buffer.from(seen.source[0]).includes(Buffer.from('PRIVATE-METADATA')),false);
  assert.match(body.instructions,/untrusted customer content/);assert.match(body.instructions,/do not identify people/i);
  assert.equal(seen.outputs[0].format,'image/jpeg');assert.equal(seen.outputs[0].anim,false);
  assert.equal(seen.rates[0][1].key.length,64);assert.equal(seen.rates[0][1].key.includes('203.0.113.5'),false);
  assert.deepEqual(seen.rates[1],['shared',{key:'website-photo'}]);
});

test('two images and photo-only messages are valid, while mixed role history stays plain text',async t=>{
  const {env,seen}=fixture(t);
  await worker.fetch(request([{role:'user',content:'Earlier question'},{role:'assistant',content:'Earlier answer'},photoMessage([url(jpeg),url(jpeg)],'')]),env);
  const body=JSON.parse(seen.fetches.at(-1).init.body);
  assert.equal(body.input[1].role,'assistant');assert.equal(typeof body.input[1].content,'string');
  assert.equal(body.input.at(-1).content.length,3);assert.match(body.input.at(-1).content[0].text,/photo/);
});

for (const [label,image,status] of [
  ['URL','https://attacker.test/photo.jpg',415],
  ['SVG','data:image/svg+xml;base64,PHN2Zy8+',415],
  ['fake MIME','data:image/jpeg;base64,PHN2Zy8+',415],
  ['bad padding',url(jpeg).slice(0,-1),415],
  ['noncanonical base64','data:image/jpeg;base64,/9j=',415],
  ['truncated',url(jpeg.subarray(0,jpeg.length-1)),415],
  ['trailing active content',url(Uint8Array.from([...jpeg,...new TextEncoder().encode('<script>')])),415],
  ['over byte limit',url(new Uint8Array(MAX_PHOTO_BYTES+1)),413],
  ['maximum bounded non-JPEG payload',url(new Uint8Array(MAX_PHOTO_BYTES)),415],
]) test('rejects '+label+' before decoder or model',async t=>{
  const {env,seen}=fixture(t);const res=await worker.fetch(request([photoMessage([image])]),env);
  assert.equal(res.status,status);assert.equal(seen.info.length,0);assert.equal(seen.fetches.length,0);
  assert.equal(typeof (await res.json()).reply,'string');
});

test('metadata between the final scan and EOI is removed too',()=>{
  const note=new TextEncoder().encode('PRIVATE-METADATA');
  const source=Uint8Array.from([...jpeg.subarray(0,-2),255,254,0,note.length+2,...note,255,217]);
  const clean=inspectJpeg(source);
  assert.equal(Buffer.from(clean.bytes).includes(Buffer.from('PRIVATE-METADATA')),false);
  assert.deepEqual(clean.bytes,inspectJpeg(jpeg).bytes);
});

test('rejects oversized dimensions before decode, even with a small compressed file',async t=>{
  const changed=jpeg.slice();let at=-1;
  for(let i=2;i<changed.length-8;i++)if(changed[i]===255&&changed[i+1]===192){at=i;break;}
  assert.notEqual(at,-1);changed[at+7]=0x7f;changed[at+8]=0xff;
  const {env,seen}=fixture(t);const res=await worker.fetch(request([photoMessage([url(changed)])]),env);
  assert.equal(res.status,413);assert.equal(seen.info.length,0);assert.equal(seen.fetches.length,0);
});

for(const [label,messages] of [
  ['assistant images',[{role:'assistant',content:'Photo',images:[url(jpeg)]},{role:'user',content:'Question'}]],
  ['non-array images',[{role:'user',content:'Question',images:url(jpeg)}]],
  ['excess photos',[photoMessage([url(jpeg),url(jpeg)]),photoMessage()]],
  ['empty conversation',[]],['null message',[null]],['empty final turn',[{role:'user',content:''}]],
]) test('rejects '+label+' before image service',async t=>{
  const {env,seen}=fixture(t);const res=await worker.fetch(request(messages),env);
  assert.ok(res.status===400||res.status===415);assert.equal(seen.info.length,0);assert.equal(seen.fetches.length,0);
});

for(const name of ['IMAGES','PHOTO_RATE_LIMITER','PHOTO_GLOBAL_LIMITER','OPENAI_API_KEY'])test('photos fail closed without '+name+' while capabilities reports disabled',async t=>{
  const {env,seen}=fixture(t);delete env[name];
  const res=await worker.fetch(request(),env);assert.equal(res.status,503);assert.equal(seen.fetches.length,0);
  const cap=await worker.fetch(new Request('https://koast-chat.euburaga.workers.dev/capabilities',{headers:{Origin:'https://koastride.com'}}),env);
  assert.deepEqual(await cap.json(),{photos:false,maxPhotos:2,maxFileBytes:8388608});
});

test('capabilities are no-store and expose no key or provider internals',async t=>{
  const {env}=fixture(t);const res=await worker.fetch(new Request('https://koast-chat.euburaga.workers.dev/capabilities',{headers:{Origin:'https://koastride.com'}}),env);
  assert.equal(res.headers.get('Cache-Control'),'no-store');assert.deepEqual(await res.json(),{photos:true,maxPhotos:2,maxFileBytes:8388608});
});

for(const scope of ['ip','shared'])test(scope+' rate rejection runs before decoder and model',async t=>{
  const {env,seen}=fixture(t,{[scope==='ip'?'ipAllowed':'sharedAllowed']:false});
  const res=await worker.fetch(request(),env);assert.equal(res.status,429);assert.equal(res.headers.get('Retry-After'),'60');
  assert.equal(seen.info.length,0);assert.equal(seen.fetches.length,0);assert.equal(seen.rates.length,scope==='ip'?1:2);
});

test('missing edge identity and limiter outages fail closed without content disclosure',async t=>{
  const {env,seen}=fixture(t);let r=request();r.headers.delete('CF-Connecting-IP');r.headers.set('X-Forwarded-For','203.0.113.5');
  assert.equal((await worker.fetch(r,env)).status,503);
  env.PHOTO_RATE_LIMITER.limit=async()=>{throw Error('private limiter credentials');};
  const res=await worker.fetch(request(),env);assert.equal(res.status,503);assert.doesNotMatch(await res.text(),/credentials/);assert.equal(seen.fetches.length,0);
});

test('decoder disagreement, corrupt output and transformation failures never reach model',async t=>{
  for(const options of [{info:{format:'jpeg',width:100,height:100}},{encoded:new Uint8Array([1,2,3])},{transformError:true}]){
    const {env,seen}=fixture(t,options);const res=await worker.fetch(request(),env);
    assert.ok([415,503].includes(res.status));assert.equal(seen.fetches.length,0);assert.doesNotMatch(await res.text(),/PRIVATE/);
  }
});

test('JSON stream is bounded independently of declared length',async t=>{
  const {env,seen}=fixture(t);
  const bytes=new Uint8Array(MAX_BODY_BYTES+1);const stream=new ReadableStream({start(c){c.enqueue(bytes.subarray(0,700000));c.enqueue(bytes.subarray(700000));c.close();}});
  const req=new Request('https://koast-chat.euburaga.workers.dev/',{method:'POST',headers:{Origin:'https://koastride.com','Content-Type':'application/json'},body:stream,duplex:'half'});
  assert.equal((await worker.fetch(req,env)).status,413);assert.equal(seen.fetches.length,0);
  assert.equal((await worker.fetch(request([{role:'user',content:'Hello'}],{'Content-Length':String(MAX_BODY_BYTES+1)}),env)).status,413);
});

test('untrusted origins and content types are rejected; legacy text needs no photo bindings',async t=>{
  const {env,seen}=fixture(t);delete env.IMAGES;delete env.PHOTO_RATE_LIMITER;delete env.PHOTO_GLOBAL_LIMITER;
  const ok=await worker.fetch(request([{role:'user',content:'Airport question'}]),env);assert.equal(ok.status,200);
  for(const origin of ['', 'https://evil.example','https://koastride.com.evil.example']){
    const res=await worker.fetch(request(undefined,{Origin:origin}),env);assert.equal(res.status,403);assert.equal(res.headers.get('Access-Control-Allow-Origin'),null);
  }
  assert.equal((await worker.fetch(request(undefined,{'Content-Type':'text/plain'}),env)).status,415);
  assert.equal(seen.fetches.length,2);
});
