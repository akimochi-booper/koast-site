import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

const read=path=>readFileSync(new URL('../'+path,import.meta.url),'utf8');
const page=read('blog/group-airport-transfers.html');
const index=read('blog/index.html');
const url='https://koastride.com/blog/group-airport-transfers';

test('refresh preserves the existing URL and month-only visible publication without a duplicate card',()=>{
  assert.equal((index.match(/href="\/blog\/group-airport-transfers"/g)||[]).length,1);
  assert.match(page,/By the Koast Team · June 2026 · Updated November 9, 2026/);
  assert.doesNotMatch(page,/June 1, 2026/);
  assert.match(index,/Corporate<\/b> · June 2026/);
  assert.equal(page.match(/<link rel="canonical" href="([^"]+)"/)[1],url);
  // Other dated articles retain their day precision.
  assert.match(read('blog/flying-home-with-wine.html'),/November 7, 2026/);
});

test('refresh retains the historical schema date and exposes only its real modification date',()=>{
  const schemas=[...page.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)].map(m=>JSON.parse(m[1]));
  const article=schemas.find(s=>s['@type']==='BlogPosting');
  assert.equal(article.datePublished,'2026-06-01');
  assert.equal(article.dateModified,'2026-11-09');
  assert.equal(article.mainEntityOfPage['@id'],url);
  const sitemap=read('sitemap.xml');
  assert.equal((sitemap.match(/<loc>https:\/\/koastride.com\/blog\/group-airport-transfers<\/loc>/g)||[]).length,1);
  assert.ok(sitemap.includes('<loc>'+url+'</loc><lastmod>2026-11-09</lastmod>'));
  assert.equal((page.match(/<h1\b/g)||[]).length,1);
});
