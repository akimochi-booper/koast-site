import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const read=p=>readFileSync(new URL('../'+p,import.meta.url),'utf8').replace(/\r\n/g,'\n');

test('published legal pages resolve every role and show the approved effective date',()=>{
  for(const [path,title] of [['privacy.html','Privacy Policy'],['terms/rider/index.html','Rider Terms'],['terms/driver/index.html','Driver App Terms'],['terms/connect/index.html','Connect Terms'],['legal/index.html','Policies and terms']]){
    const html=read(path);
    assert.ok(html.includes('<h1>'+title+'</h1>'),path);
    assert.ok(html.includes('Effective October 30, 2026'),path);
    assert.doesNotMatch(html,/Draft for owner review|Not effective or published|Existing published agreements remain in effect/);
    for(const href of ['/privacy','/terms/rider/','/terms/driver/','/terms/connect/','/sms-terms'])assert.ok(html.includes('href="'+href+'"'),path+' -> '+href);
    assert.doesNotMatch(html,/\{EMAIL\}|\{PHONE\}|TODO|PLACEHOLDER/);
  }
});

test('legacy URL and role URL serve identical ride-specific terms and preserve privacy anchors',()=>{
  const current=read('terms.html'),rider=read('terms/rider/index.html');
  const body=read('content/legal/rider.inc');
  for(const sentence of ['those accepted ride-specific terms take precedence','Each leg of a reservation may have different terms','do not retroactively change an accepted ride','Email is not the only accepted cancellation method.','These general terms do not create a universal cancellation window','Request permanent deletion now'])assert.ok(body.includes(sentence),sentence);
  assert.doesNotMatch(body,/50% refund|more than 24 hours|Within 12 hours|each commenced half hour is rounded up|include 20 miles per hour|\$2\.08 per minute|\$5\.15 per mile|An effective cancellation can only/);
  assert.ok(body.includes('id="cancellations"'));
  assert.ok(current.includes(body)&&rider.includes(body));
  assert.ok(read('privacy.html').includes('id="account-deletion"'));
});

test('public service copy no longer advertises the superseded universal ride schedules',()=>{
  for(const file of ['generate.py','data.py']){
    const body=read(file);
    assert.doesNotMatch(body,/published Terms include 30 minutes|30 minutes (?:free|included) (?:on|for) domestic|30 minutes for domestic flights and 60 minutes for international|full schedule is in our|Terms<\/a> for exact rates/);
  }
});

test('shared privacy covers actual safety, permissions and future feature boundaries',()=>{
  const body=read('content/legal/privacy.inc');
  for(const text of ['garage positioning','automatically uploaded','no incident report','provider revocation','OpenAI','90-day','not a currently available control','Limited Use','STOP','HELP'])assert.ok(body.includes(text),text);
  assert.doesNotMatch(body,/It does not apply to information that we collect from or about vehicle drivers/);
});
