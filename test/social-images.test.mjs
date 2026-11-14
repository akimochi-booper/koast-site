import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync, existsSync} from 'node:fs';

const root = new URL('../', import.meta.url);
const read = path => readFileSync(new URL(path, root), 'utf8');
const meta = (page, name) => page.match(new RegExp(`<meta (?:property|name)="${name}" content="([^"]*)">`))?.[1];

test('sharing images represent locations, services and routes while home keeps the brand card', () => {
  const cases = [
    ['index.html', 'og-image-v2.jpg'],
    ['cities/palo-alto.html', 'city-palo-alto-renewal-v1.jpg'],
    ['airports/oak.html', 'oakland-generated-social-v1.jpg'],
    ['airports/sjc.html', 'santana-generated-social-v1.jpg'],
    ['airports/sfo.html', 'blog-banner-sfo.jpg'],
    ['wine-tours/healdsburg.html', 'wt-healdsburg.jpg'],
    ['wineries/stags-leap-wine-cellars.html', 'blog-banner-napa.jpg'],
    ['routes/sjc-to-silicon-valley.html', 'city-palo-alto-renewal-v1.jpg'],
    ['routes/sfo-to-monterey.html', 'blog-banner-sfo.jpg'],
    ['services/corporate-travel.html', 'blog-banner-corporate.jpg'],
    ['services/weddings.html', 'svc-weddings.jpg'],
    ['blog/sfo-oak-sjc-silicon-valley-business-trip.html', 'bay-area-airport-trip-planning.jpg'],
  ];
  for (const [path, image] of cases) {
    const page = read(path);
    assert.equal(meta(page, 'og:image'), 'https://koastride.com/img/' + image, path);
  }
  assert.equal(meta(read('wineries/stags-leap-wine-cellars.html'), 'og:image:alt'), 'Napa Valley wine country');
  assert.match(meta(read('airports/oak.html'), 'og:image:alt'), /^AI-created illustration/);
  assert.ok(existsSync(new URL('img/og-image.jpg', root)), 'old shared image remains available');
});

test('every indexable sharing card references a local image with consistent metadata', () => {
  const urls = [...read('sitemap.xml').matchAll(/<loc>([^<]+)<\/loc>/g)].map(match => match[1]);
  assert.ok(urls.length >= 220);
  for (const url of urls) {
    const pathname = new URL(url).pathname;
    const path = pathname.endsWith('/') ? pathname.slice(1) + 'index.html' : pathname.slice(1) + '.html';
    const page = read(path);
    const image = meta(page, 'og:image');
    assert.ok(image?.startsWith('https://koastride.com/img/'), url);
    assert.ok(existsSync(new URL(new URL(image).pathname.slice(1), root)), image);
    assert.equal(meta(page, 'twitter:image'), image, url);
    assert.ok(Number(meta(page, 'og:image:width')) > 0, url);
    assert.ok(Number(meta(page, 'og:image:height')) > 0, url);
    assert.match(meta(page, 'og:image:type'), /^image\/(jpeg|png|webp)$/);
    assert.ok(meta(page, 'og:image:alt'), url);
    assert.equal(meta(page, 'twitter:image:alt'), meta(page, 'og:image:alt'), url);
  }
  assert.equal(meta(read('airports/oak.html'), 'og:image:width'), '1440');
  assert.equal(meta(read('airports/oak.html'), 'og:image:height'), '810');
  assert.equal(meta(read('index.html'), 'og:image:width'), '1200');
  assert.equal(meta(read('index.html'), 'og:image:height'), '630');
});
