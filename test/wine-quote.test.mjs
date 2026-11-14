import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,readdirSync} from 'node:fs';
import vm from 'node:vm';

const source=readFileSync(new URL('../marketing-design.js',import.meta.url),'utf8');
const context=vm.createContext({Date,String,Number,encodeURIComponent});
vm.runInContext(source,context);
const validate=(data)=>context.validateWineTrip(data,'2026-11-14');
const base={pickup:'San Francisco hotel',date:'2026-11-20',party:'4',region:'Livermore Valley'};

test('quote planner validates required fields and real future calendar dates',()=>{
  assert.equal(validate(base).trip.pickup,base.pickup);
  for(const bad of ['', '2026-02-30','2026-11-13','not-a-date']) assert.equal(validate({...base,date:bad}).field,'date');
  assert.equal(validate({...base,pickup:' '}).field,'pickup');
  assert.equal(validate({...base,party:'32'}).field,'party');
  assert.equal(validate({...base,party:'7+'}).trip.party,'7+');
  assert.equal(validate({...base,date:'',dateOptional:true}).trip.date,'');
});

test('reviewed email draft retains all trip inputs, encodes special characters and makes no reservation',()=>{
  const pickup='Hotel & restaurant <front entrance> #2';
  const trip=validate({...base,pickup}).trip;
  const href=context.buildWineQuoteEmail('reserve@koastride.com',trip);
  assert.ok(href.startsWith('mailto:reserve@koastride.com?'));
  const query=new URLSearchParams(href.split('?')[1]);
  assert.match(query.get('subject'),/Livermore Valley/);
  for(const value of [pickup,base.date,'4 guests','separate']) assert.ok(query.get('body').includes(value),value);
  assert.doesNotMatch(source,/localStorage|sessionStorage|sendBeacon|fetch\(/);
});

test('three design previews stay separate, noindex, and outside the sitemap',()=>{
  const sitemap=readFileSync(new URL('../sitemap.xml',import.meta.url),'utf8');
  for(const variant of ['cinema','journal','gallery']){
    const page=readFileSync(new URL('../preview/wine-designs/'+variant+'.html',import.meta.url),'utf8');
    assert.match(page,new RegExp('wine-reference reference-'+variant));
    assert.match(page,/name="robots" content="noindex, nofollow"/);
    assert.match(page,/\/css\/wine-reference\.css\?v=1/);
    assert.equal((page.match(/<h1\b/g)||[]).length,1);
    assert.equal((page.match(/<form\b/g)||[]).length,1);
    assert.match(page,/data-wine-quote/);
    assert.doesNotMatch(sitemap,new RegExp('/preview/wine-designs/'+variant));
  }
});

test('winery exploration stays on Koast across every winery, region and design preview',()=>{
  const files=['wine-tours/','wineries/'].flatMap(dir=>readdirSync(new URL('../'+dir,import.meta.url)).filter(name=>name.endsWith('.html')).map(name=>dir+name));
  files.push('services/wine-tours.html',...['cinema','journal','gallery'].map(name=>'preview/wine-designs/'+name+'.html'));
  assert.ok(files.length>20,'Check the complete generated wine destination collection');
  for(const file of files){
    const page=readFileSync(new URL('../'+file,import.meta.url),'utf8');
    // Booking/account handoffs belong to Koast's existing transaction flow.
    for(const [,href] of page.matchAll(/<a\b[^>]*\bhref="([^"]+)"/gi)){
      if(!/^(?:https?:)?\/\//i.test(href)) continue;
      const url=new URL(href,'https://koastride.com');
      assert.ok(['koastride.com','www.koastride.com','customer.moovs.app'].includes(url.hostname),`${file} sends winery exploration away: ${href}`);
      if(url.hostname==='customer.moovs.app') assert.ok(['/koast/request/new','/koast/new/info'].includes(url.pathname),`${file} uses an unexpected provider path`);
    }
    if(file.startsWith('wineries/')&&!file.endsWith('/index.html')){
      assert.match(page,/href="#winery-details">About this winery/);
      assert.match(page,/<details[^>]*id="winery-details"/);
    }
  }
});
