import test from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {readFileSync} from 'node:fs';

const result=spawnSync('python',['-c',`
import json
from src.marketing_design import renew_page
head='<html><head></head><body><nav>Navigation</nav><main>'
end='</main><footer>Footer</footer></body></html>'
account='<header class="hero-dark"><div class="wrap"><h1>Corporate</h1><p class="lede">Travel</p><div><a class="btn btn-orange" href="mailto:reserve@example.com?subject=Corporate">Account inquiry</a><a href="https://example.com/book">Single ride</a></div></div></header>'
booking='<div class="book-card book-widget"><div><iframe data-src="https://example.com/iframe" title="Quote"></iframe></div><script>window.bookingInitialized=true;</script></div>'
hero='<header class="hero-dark"><div class="wrap"><div class="crumbs"><a href="/">Home</a><span>/</span>City</div><div class="hero-grid"><div class="hero-copy"><h1>City</h1><p class="lede">Arrival</p><ul class="check"><li>Flight tracking</li></ul></div>'+booking+'</div></div></header>'
render=lambda src,path:renew_page(head+src+end,path,'img/city.jpg','City view','https://example.com/book?a=1&b=2')
print(json.dumps({'account':render(account,'services/corporate-travel.html'),'booking':render(hero,'cities/example.html'),'preview':render(hero,'preview/example.html'),'original':head+hero+end,'repeated':renew_page(render(account,'services/corporate-travel.html'),'services/corporate-travel.html','img/city.jpg','City view','https://example.com/book?a=1&b=2')}))
`],{encoding:'utf8'});
assert.equal(result.status,0,result.stderr);
const fixtures=JSON.parse(result.stdout);

test('marketing renewal preserves corporate and secondary hero actions',()=>{
  assert.match(fixtures.account,/href="mailto:reserve@example.com\?subject=Corporate">Account inquiry/);
  assert.match(fixtures.account,/href="https:\/\/example.com\/book">Single ride/);
  assert.equal((fixtures.account.match(/<h1>/g)||[]).length,1);
});

test('marketing renewal retains one complete nested booking widget and moves its initializer with it',()=>{
  const page=fixtures.booking;
  assert.equal((page.match(/<iframe\b/g)||[]).length,1);
  assert.equal((page.match(/window.bookingInitialized=true/g)||[]).length,1);
  assert.ok(page.indexOf('<iframe')>page.indexOf('</header>'));
  assert.match(page,/Flight tracking/);
  assert.match(page,/id="reserve-ride"/);
  assert.match(page,/href="https:\/\/example.com\/book\?a=1&amp;b=2"/);
  assert.equal((page.match(/class="crumbs"/g)||[]).length,1);
});

test('marketing renewal leaves held preview designs untouched',()=>{
  assert.equal(fixtures.preview,fixtures.original);
  assert.equal(fixtures.repeated,fixtures.account);
});

test('generated public families preserve identity and quote-only groups',()=>{
  for(const path of ['cities/palo-alto.html','wine-tours/livermore.html','wineries/stags-leap-wine-cellars.html','airports/sfo.html','services/corporate-travel.html']){
    const page=readFileSync(new URL('../'+path,import.meta.url),'utf8');
    assert.equal((page.match(/<h1\b/g)||[]).length,1,path);
    assert.match(page,/koast-acquisition\.js\?v=3/,path);
    assert.match(page,/marketing-design\.css\?v=1/,path);
    assert.match(page,/rel="canonical"/,path);
  }
  for(const path of ['wine-tours/napa-valley.html','wineries/wente-vineyards.html']){
    const page=readFileSync(new URL('../'+path,import.meta.url),'utf8');
    assert.match(page,/Buses · Quote required/);
    assert.doesNotMatch(page,/up to 32/);
  }
});
