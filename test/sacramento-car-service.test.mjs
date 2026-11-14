import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

const page=readFileSync(new URL('../cities/sacramento.html',import.meta.url),'utf8');
const schemas=[...page.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)].map(m=>JSON.parse(m[1]));
const text=s=>s.replace(/<[^>]*>/g,'').replace(/\s+/g,' ').trim();

test('Sacramento keeps its canonical and local Service identity without an invented office',()=>{
  const url='https://koastride.com/cities/sacramento';
  assert.equal((page.match(/<h1\b/g)||[]).length,1);
  assert.equal(page.match(/<title>(.*?)<\/title>/)[1],'Sacramento Black Car Service & SMF Transfers | Koast');
  for(const [key,pattern] of [['canonical',/<link rel="canonical" href="([^"]+)"/],['social',/<meta property="og:url" content="([^"]+)"/]]) assert.equal(page.match(pattern)[1],url,key);
  assert.doesNotMatch(page,/<meta[^>]*name="robots"[^>]*content="[^"]*noindex/);
  const service=schemas.filter(s=>s['@type']==='Service');
  assert.equal(service.length,1);
  assert.equal(service[0].url,url);
  assert.equal(service[0].areaServed.name,'Sacramento');
  assert.equal(service[0].areaServed.address.addressRegion,'CA');
  assert.equal(schemas.filter(s=>s['@type']==='LocalBusiness').length,0);
  assert.match(page,/city-sacramento\.jpg/);
});

test('Sacramento answers match the search schema and preserve transport boundaries',()=>{
  const visible=[...page.matchAll(/<details><summary>([\s\S]*?)<\/summary><p>([\s\S]*?)<\/p><\/details>/g)].map(m=>({q:text(m[1]),a:text(m[2])}));
  assert.equal(visible.length,6);
  assert.deepEqual(schemas.find(s=>s['@type']==='FAQPage').mainEntity.map(x=>({q:x.name,a:x.acceptedAnswer.text})),visible);
  assert.match(page,/Vans, Sprinters and buses require a quote/);
  assert.match(page,/not a self-drive truck rental/);
  assert.doesNotMatch(page,/SMF \(20|Anywhere in Sacramento, anytime|constantly|booked in under a minute/i);
  assert.match(page,/tasting reservations separately/);
});

test('Sacramento planning and quote links resolve to existing destinations with a contextual inbound path',()=>{
  for(const path of ['/services/airport-transfers','/services/corporate-travel','/cities/san-francisco','/wine-tours/napa-valley','/wineries/stags-leap-wine-cellars']) assert.ok(page.includes(`href="${path}"`),path);
  assert.ok(page.includes('href="#plan-your-trip"'));
  assert.ok(page.includes('id="plan-your-trip" style="scroll-margin-top:100px"'));
  assert.match(page,/href="https:\/\/customer\.moovs\.app\/koast\/request\/new">Get a Sacramento quote<\/a>/);
  const napa=readFileSync(new URL('../wine-tours/napa-valley.html',import.meta.url),'utf8');
  assert.match(napa,/href="\/cities\/sacramento">[\s\S]{0,50}Sacramento pickups and return planning/);
});
