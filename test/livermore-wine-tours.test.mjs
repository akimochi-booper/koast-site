import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const page=readFileSync(new URL('../wine-tours/livermore.html',import.meta.url),'utf8');
const schemas=[...page.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)].map(m=>JSON.parse(m[1]));
const url='https://koastride.com/wine-tours/livermore';

test('Livermore remains one indexable regional transport service with its existing social image',()=>{
  assert.equal((page.match(/<h1\b/g)||[]).length,1);
  assert.equal(page.match(/<title>(.*?)<\/title>/)[1],'Livermore Valley Wine Tours with a Private Driver | Koast');
  assert.equal(page.match(/<link rel="canonical" href="([^"]+)"/)[1],url);
  assert.equal(page.match(/<meta property="og:url" content="([^"]+)"/)[1],url);
  assert.doesNotMatch(page,/<meta[^>]*name="robots"[^>]*content="[^"]*noindex/);
  const service=schemas.filter(s=>s['@type']==='Service');
  assert.equal(service.length,1);
  assert.equal(service[0].url,url);
  assert.equal(service[0].areaServed.name,'Livermore Valley');
  assert.equal(service[0].areaServed.address.addressRegion,'CA');
  assert.equal(service[0].provider.url,'https://koastride.com/');
  assert.equal(schemas.filter(s=>['Winery','LocalBusiness'].includes(s['@type'])).length,0);
  assert.match(page,/wt-livermore\.jpg/);
});

test('all six Livermore answers match their searchable schema and preserve reservation boundaries',()=>{
  const text=s=>s.replace(/<[^>]*>/g,'').trim();
  const visible=[...page.matchAll(/<details><summary>([\s\S]*?)<\/summary><p>([\s\S]*?)<\/p><\/details>/g)].map(m=>({q:text(m[1]),a:text(m[2])}));
  assert.equal(visible.length,6);
  assert.deepEqual(schemas.find(s=>s['@type']==='FAQPage').mainEntity.map(x=>({q:x.name,a:x.acceptedAnswer.text})),visible);
  assert.match(page,/Vans, Sprinters and buses require a quote/);
  assert.match(page,/A transportation reservation does not reserve a tasting/);
  assert.match(page,/private car does not make the tasting private/);
  assert.doesNotMatch(page,/three to four tastings|Most days run 6|reservation-only tasting first|booked in under a minute/);
});

test('local winery destinations and route controls use current official planning resources',()=>{
  for(const value of ['5050 Arroyo Road','4590 Tesla Road','3005 Mines Road','reservations are encouraged','seated tastings']) assert.ok(page.toLowerCase().includes(value.toLowerCase()),value);
  for(const href of ['https://wentevineyards.com/visit/','https://concannon.wine/experiences/','https://murrietaswell.com/visit/','https://www.lvwine.org/itinerary-planner.php','https://www.lvwine.org/maps.php','/cities/san-francisco','/cities/san-jose','/blog/group-wine-tour-planning']) assert.ok(page.includes(`href="${href}"`),href);
  assert.ok(page.includes('href="https://customer.moovs.app/koast/request/new">Get a Livermore quote</a>'));
  assert.ok(page.includes('href="#plan-your-tastings"'));
  assert.ok(page.includes('id="plan-your-tastings" style="scroll-margin-top:100px"'));
  const city=readFileSync(new URL('../cities/san-jose.html',import.meta.url),'utf8');
  assert.match(city,/href="\/wine-tours\/livermore">[\s\S]{0,50}Livermore private-driver wine tours/);
});

test('pure Livermore renderer retains the existing booking slot and escapes a supplied quote URL',()=>{
  const result=spawnSync('python',['-c',`from src.livermore_wine_tours import render_livermore_body
print(render_livermore_body('<aside id="existing-booking">Booking</aside>', 'https://example.invalid/?a=1&b=" onmouseover="unsafe'))`],{cwd:fileURLToPath(new URL('../',import.meta.url)),encoding:'utf8'});
  assert.equal(result.status,0,result.stderr);
  const body=result.stdout;
  assert.equal((body.match(/id="existing-booking"/g)||[]).length,1);
  assert.equal((body.match(/href="https:\/\/example\.invalid\/\?a=1&amp;b=&quot; onmouseover=&quot;unsafe"/g)||[]).length,2);
  assert.doesNotMatch(body,/href="[^"]*" onmouseover=/);
  assert.doesNotMatch(body,/<script\b|<form\b/);
});
