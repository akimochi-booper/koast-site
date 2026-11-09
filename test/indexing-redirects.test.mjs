import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

test('reported legacy San Francisco URL redirects to the indexable city page', () => {
  const redirects = readFileSync(new URL('../_redirects', import.meta.url), 'utf8');
  assert.equal(redirects.split(/\r?\n/).filter(line => line.startsWith('/sedans/cities/san-francisco.html ')).join(''),
    '/sedans/cities/san-francisco.html /cities/san-francisco 301');
  const destination = readFileSync(new URL('../cities/san-francisco.html', import.meta.url), 'utf8');
  assert.match(destination, /<link rel="canonical" href="https:\/\/koastride\.com\/cities\/san-francisco">/);
  assert.doesNotMatch(destination, /<meta[^>]*name="robots"[^>]*content="[^"]*noindex/i);
  const sitemap = readFileSync(new URL('../sitemap.xml', import.meta.url), 'utf8');
  assert.ok(sitemap.includes('<loc>https://koastride.com/cities/san-francisco</loc>'));
  assert.ok(!sitemap.includes('/sedans/cities/san-francisco.html'));
});
