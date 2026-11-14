import test from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {readFileSync} from 'node:fs';

// Exercise the pure owner without mutating or importing the site generator.
const root = fileURLToPath(new URL('../', import.meta.url));
const result = spawnSync('python', ['-c', `
import json
from src.stags_leap_transport import STAGS_LEAP_TITLE, STAGS_LEAP_DESCRIPTION, STAGS_LEAP_FAQS, render_body
print(json.dumps({
    'title': STAGS_LEAP_TITLE, 'description': STAGS_LEAP_DESCRIPTION,
    'faqs': STAGS_LEAP_FAQS,
    'body': render_body('<aside id="existing-booking">Existing native booking card</aside>',
                        'https://example.invalid/quote?a=1&b=" onmouseover="unsafe')
}))
`], {cwd: root, encoding: 'utf8'});
assert.equal(result.status, 0, result.stderr);
const {title, description, faqs, body} = JSON.parse(result.stdout);

test('transport owner preserves the native booking slot and escapes the injected quote URL', () => {
  assert.equal((body.match(/id="existing-booking"/g) || []).length, 1);
  assert.match(body, /<aside id="existing-booking">Existing native booking card<\/aside>/);
  assert.equal((body.match(/href="https:\/\/example\.invalid\/quote\?a=1&amp;b=&quot; onmouseover=&quot;unsafe"/g) || []).length, 2);
  assert.doesNotMatch(body, /href="[^"]*" onmouseover=/);
  assert.equal((body.match(/<h1\b/g) || []).length, 1);
  assert.doesNotMatch(body, /<form\b|<script\b|<h1\b[^>]*>[\s\S]*<h1\b/);
});

test('small-party answers distinguish winery admission, shared experiences and vehicle capacity', () => {
  assert.equal(faqs.length, 6);
  assert.equal(new Set(faqs.map(([question]) => question)).size, faqs.length);
  const answers = faqs.map(([, answer]) => answer).join(' ');
  assert.match(faqs[0][0], /small-group tours available in Stags Leap/);
  assert.match(answers, /does not sell seats on a shared or join-in tour/);
  assert.match(answers, /private car does not make the winery experience private/);
  assert.match(answers, /Winery admission and tasting fees are separate/);
  assert.match(answers, /Vans, Sprinters and buses require a quote/);
  assert.match(answers, /party-size rules separately from the vehicle's seating/);
  assert.match(answers, /one-way transfer does not reserve a car/);
  assert.match(answers, /at least 21/);
  assert.doesNotMatch(body + answers, /\b(?:up to \d+|\d+ guests|\d+ minutes|three to four tastings)\b/i);
});

test('destination clarification and itinerary planning remain useful and navigable', () => {
  assert.ok(title.length <= 60);
  assert.ok(description.length <= 160);
  assert.match(body, /Stag's Leap Wine Cellars[\s\S]*5766 Silverado Trail, Napa, CA 94558/);
  assert.match(body, /Stags' Leap Winery[\s\S]*6150 Silverado Trail, Napa, CA 94558/);
  assert.match(body, /https:\/\/www\.stagsleapwinecellars\.com\/visit-us\/experiences\//);
  assert.match(body, /https:\/\/www\.stagsleap\.com\/pages\/visit/);
  assert.match(body, /pickup entrance/);
  assert.match(body, /return address and required return time/);
  assert.match(body, /service window/);
  for (const target of [...body.matchAll(/href="#([^"]+)"/g)].map(match => match[1])) {
    assert.ok(body.includes(`id="${target}"`), `anchor ${target}`);
  }
});

test('generated winery page retains one indexable service and exactly matching visible FAQs',()=>{
  const page=readFileSync(new URL('../wineries/stags-leap-wine-cellars.html',import.meta.url),'utf8');
  const url='https://koastride.com/wineries/stags-leap-wine-cellars';
  assert.equal((page.match(/<h1\b/g)||[]).length,1);
  assert.equal(page.match(/<link rel="canonical" href="([^"]+)"/)[1],url);
  assert.equal(page.match(/<meta property="og:url" content="([^"]+)"/)[1],url);
  assert.doesNotMatch(page,/<meta[^>]*name="robots"[^>]*content="[^"]*noindex/);
  const schemas=[...page.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)].map(m=>JSON.parse(m[1]));
  const service=schemas.filter(s=>s['@type']==='Service');
  assert.equal(service.length,1);
  assert.equal(service[0].url,url);
  assert.equal(service[0].provider['@id'],'https://koastride.com/#org');
  assert.equal(service[0].areaServed,'Napa Valley');
  assert.equal(schemas.filter(s=>s['@type']==='Winery'||s['@type']==='LocalBusiness').length,0);
  const plain=s=>s.replace(/<[^>]*>/g,'').trim();
  const visible=[...page.matchAll(/<details><summary>([\s\S]*?)<\/summary><p>([\s\S]*?)<\/p><\/details>/g)].map(m=>({q:plain(m[1]),a:plain(m[2])}));
  assert.equal(visible.length,6);
  assert.deepEqual(schemas.find(s=>s['@type']==='FAQPage').mainEntity.map(x=>({q:x.name,a:x.acceptedAnswer.text})),visible);
  assert.equal(schemas.find(s=>s['@type']==='BreadcrumbList').itemListElement.at(-1).item,url);
  assert.ok(page.includes('href="https://customer.moovs.app/koast/request/new">Get a transportation quote</a>'));
  assert.ok(page.includes('href="/cities/sacramento"'));
  const napa=readFileSync(new URL('../wine-tours/napa-valley.html',import.meta.url),'utf8');
  assert.ok(napa.includes("Stag's Leap small-group transportation"));
});
