import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

const read = path => readFileSync(new URL('../' + path, import.meta.url), 'utf8');
const page = read('cities/palo-alto.html');
const url = 'https://koastride.com/cities/palo-alto';
const schemas = [...page.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)].map(match => JSON.parse(match[1]));
const text = html => html.replace(/<[^>]*>/g, '').replace(/\s+/g, ' ').trim();

test('Palo Alto retains one indexable URL and a truthful local service identity', () => {
  assert.equal((page.match(/<h1\b/g) || []).length, 1);
  assert.match(page, /<title>Palo Alto Car Service \| SFO & SJC Airport Transfers \| Koast<\/title>/);
  assert.equal(page.match(/rel="canonical" href="([^"]+)"/)[1], url);
  assert.equal(page.match(/property="og:url" content="([^"]+)"/)[1], url);
  assert.doesNotMatch(page, /<meta[^>]*name="robots"[^>]*content="[^"]*noindex/);
  const services = schemas.filter(schema => schema['@type'] === 'Service');
  assert.equal(services.length, 1);
  assert.equal(services[0].url, url);
  assert.equal(services[0].areaServed.name, 'Palo Alto');
  assert.equal(services[0].areaServed.address.addressRegion, 'CA');
  assert.ok(!schemas.some(schema => schema['@type'] === 'LocalBusiness'), 'no invented local office');
  assert.match(page, /property="og:image" content="https:\/\/koastride.com\/img\/city-palo-alto.jpg"/);
});

test('airport intent and quote planning use the established destinations', () => {
  for (const destination of ['/routes/sfo-to-silicon-valley', '/routes/sjc-to-silicon-valley', '/airports/sfo', '/airports/sjc', '/services/corporate-travel']) {
    assert.ok(page.includes(`href="${destination}"`), destination);
  }
  assert.match(page, /id="airport-options"/);
  assert.match(page, /href="#airport-options"/);
  assert.match(page, /href="https:\/\/customer.moovs.app\/koast\/request\/new">Get a Palo Alto quote/);
  assert.match(page, /full address[\s\S]*Sand Hill Road in Menlo Park/);
  assert.match(page, /Vans, Sprinters[\s\S]*require a quote/);
  assert.doesNotMatch(page, /booked in under a minute|SFO \(30 min\)|every hotel, office, hospital/);
});

test('Palo Alto FAQ schema is exactly the visible FAQ and relevant inbound links remain', () => {
  const visible = [...page.matchAll(/<details><summary>([\s\S]*?)<\/summary><p>([\s\S]*?)<\/p><\/details>/g)]
    .map(match => ({question: text(match[1]), answer: text(match[2])}));
  assert.equal(visible.length, 6);
  const faq = schemas.find(schema => schema['@type'] === 'FAQPage');
  assert.deepEqual(faq.mainEntity.map(item => ({question: item.name, answer: item.acceptedAnswer.text})), visible);
  assert.match(read('blog/sfo-oak-sjc-silicon-valley-business-trip.html'), /href="\/cities\/palo-alto">Palo Alto airport transfers/);
  assert.ok(/href="\/wine-tours\/healdsburg">[\s\S]{0,50}Healdsburg private drivers and winery routes/.test(read('wine-tours/sonoma.html')), 'Sonoma planning links to the Healdsburg driver page');
});
