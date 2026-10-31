import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const read=p=>readFileSync(new URL('../'+p,import.meta.url),'utf8').replace(/\r\n/g,'\n');
const normalize=s=>s.replace(/\s+/g,' ').trim();
const plain=s=>s.replace(/<[^>]+>/g,' ').replace(/&quot;/g,'"').replace(/&#x27;/g,"'").replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&');

test('public authorization renders exactly the customer contract frozen for acceptance',()=>{
  const bytes=readFileSync(new URL('../content/legal/standing-authorization.txt',import.meta.url));
  assert.equal(createHash('sha256').update(bytes).digest('hex'),'e5f9e37380b57bffa720dd13f9fc4088499b0d481b8b57433f9937c44b383600');
  const canonical=read('content/legal/standing-authorization.txt');
  const body=read('content/legal/standing-authorization.inc');
  assert.equal(normalize(plain(body)),normalize(canonical.replace(/^- /gm,'')));
  assert.equal((body.match(/<h2 id=/g)||[]).length,8);
  const html=read('terms/standing-authorization/index.html');
  assert.ok(html.includes(body));
  assert.ok(html.includes('standing-booking-payment-v1-20261031'));
  assert.ok(html.includes('Effective October 31, 2026'));
  assert.ok(html.includes('<link rel="canonical" href="https://koastride.com/terms/standing-authorization/">'));
  assert.ok(read('sitemap.xml').includes('<loc>https://koastride.com/terms/standing-authorization/</loc>'));
  assert.doesNotMatch(body,/Customer-facing draft|Initial card-entry presentation|Dispatch coverage and records|Implementation and publication boundary|Sources checked|this draft/);
});

test('standing authorization preserves company, request, pricing and payment limits',()=>{
  const body=read('content/legal/standing-authorization.txt');
  for(const text of [
    'For Koast\'s own operating business, the Company is Krujim Inc, doing business as Koast.',
    'Staff access to Dispatch alone does not establish your approval.',
    'Quote-only services remain subject to an agreed quote',
    'still requires an authorized service request and a determinable charge under the agreed framework',
    'receiving it or failing to cancel is not a substitute for agreement to a new rule outside that framework',
    'The presence of a deposit field, manual amount adjustment, custom line or auto-collection setting does not independently authorize a charge.',
    'An alternate-payment balance may be collected from a saved card only if that fallback was expressly included in your authorization.',
    'An optional gratuity cannot be increased at staff discretion',
    'this authorization does not automatically transfer to it',
    'Customer permissions for marketing messages, optional recording, device tracking or cross-operator profile sharing remain separate.'
  ])assert.ok(body.includes(text),text);
});

test('rider discovery and privacy records support separate, scoped authorization',()=>{
  const rider=read('content/legal/rider.inc'),hub=read('legal/index.html'),privacy=read('content/legal/privacy.inc');
  assert.ok(rider.includes('href="/terms/standing-authorization/"'));
  assert.ok(rider.includes('an already saved card do not by themselves establish that authorization'));
  assert.ok(hub.includes('requires separate acceptance'));
  assert.ok(privacy.includes('the version and content of accepted terms and pricing or ride-policy schedules'));
  assert.ok(privacy.includes('later changes or withdrawal'));
});
