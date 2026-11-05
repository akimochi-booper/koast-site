import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

const page=readFileSync(new URL('../wine-tours/healdsburg.html',import.meta.url),'utf8');
const url='https://koastride.com/wine-tours/healdsburg';
const schemas=[...page.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)].map(match=>JSON.parse(match[1]));
const text=html=>html.replace(/<[^>]*>/g,'').replace(/\s+/g,' ').trim();

test('the existing Healdsburg URL stays indexable with one heading and consistent service identity',()=>{
  assert.equal((page.match(/<h1\b/g)||[]).length,1);
  assert.equal(page.match(/<link rel="canonical" href="([^"]+)"/)[1],url);
  assert.equal(page.match(/<meta property="og:url" content="([^"]+)"/)[1],url);
  assert.doesNotMatch(page,/<meta[^>]*name="robots"[^>]*content="[^"]*noindex/);
  const services=schemas.filter(schema=>schema['@type']==='Service');
  assert.equal(services.length,1);
  assert.equal(services[0].url,url);
  assert.equal(services[0].areaServed.name,'Healdsburg');
  assert.equal(services[0].provider.url,'https://koastride.com/');
});

test('all searchable FAQ answers are exactly the answers presented to visitors',()=>{
  const visible=[...page.matchAll(/<details><summary>([\s\S]*?)<\/summary><p>([\s\S]*?)<\/p><\/details>/g)]
    .map(match=>({question:text(match[1]),answer:text(match[2])}));
  const faq=schemas.find(schema=>schema['@type']==='FAQPage');
  assert.ok(visible.length>0);
  assert.deepEqual(faq.mainEntity.map(item=>({question:item.name,answer:item.acceptedAnswer.text})),visible);
  const crumb=schemas.find(schema=>schema['@type']==='BreadcrumbList');
  assert.equal(crumb.itemListElement.at(-1).item,url);
});
