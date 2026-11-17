import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import vm from 'node:vm';

const fixture=spawnSync('python',['-m','src.wine_days'],{encoding:'utf8'});
assert.equal(fixture.status,0,fixture.stderr);
const catalogue=JSON.parse(fixture.stdout);
assert.equal(catalogue.schemaVersion,1);assert.equal(catalogue.bookerIntegration,'none');
const ideas=catalogue.ideas;
const ctx=vm.createContext({});
const quoteSource=readFileSync(new URL('../marketing-design.js',import.meta.url),'utf8');
vm.runInContext(quoteSource,ctx);
vm.runInContext(readFileSync(new URL('../wine-days.js',import.meta.url),'utf8'),ctx);

test('one wine-day catalogue supplies distinct region/vehicle ideas without invented prices or durations',()=>{
  assert.equal(ideas.length,9);
  assert.equal(new Set(ideas.map(idea=>idea.id)).size,9);
  assert.equal(new Set(ideas.map(idea=>idea.image)).size,9);
  for(const region of ['napa-valley','sonoma','livermore']) {
    assert.deepEqual(ideas.filter(idea=>idea.region_slug===region).map(idea=>idea.vehicle),['SUV','Executive Sprinter','Party bus / coach']);
  }
  for(const idea of ideas){
    assert.equal(idea.state,'exploratory');assert.equal(idea.price_state,'team_quote');
    assert.equal(idea.duration_hours,null);assert.equal(idea.itinerary_verified,false);assert.deepEqual(idea.stops,[]);
    assert.deepEqual(idea.requestable_vehicle_classes,['SUV','First-Class SUV','Executive Sprinter','Party bus / coach']);
    assert.equal(idea.exclusions.includes('Tasting reservations and fees'),true);
  }
});

test('active region filtering excludes other regions and All retains the full collection',()=>{
  assert.equal(ideas.filter(idea=>ctx.wineDayMatchesRegion(idea.region_slug,'napa-valley')).length,3);
  assert.equal(ideas.filter(idea=>ctx.wineDayMatchesRegion(idea.region_slug,'sonoma')).every(idea=>idea.region_slug==='sonoma'),true);
  assert.equal(ideas.filter(idea=>ctx.wineDayMatchesRegion(idea.region_slug,'all')).length,9);
  assert.equal(ideas.filter(idea=>ctx.wineDayMatchesRegion(idea.region_slug,'unknown')).length,0);
});

test('manual quote context resolves an authored idea and rejects unknown or non-quote entries',()=>{
  assert.equal(ctx.resolveWineDayIdea(ideas[0].id,ideas).title,ideas[0].title);
  assert.equal(ctx.resolveWineDayIdea('unknown',ideas),null);
  assert.equal(ctx.resolveWineDayIdea(ideas[0].id,[{...ideas[0],price_state:'instant_buy'}]),null);
  assert.equal(ctx.resolveWineDayIdea(ideas[0].id,{}),null);
});

test('email preparation retains selected tour, requested class and custom stops without provider submission',()=>{
  const idea=ideas.find(item=>item.vehicle==='Executive Sprinter');
  const notes='Wente & Concannon <not confirmed>\nHotel return';
  const href=ctx.buildWineQuoteEmail('reserve@koastride.com',{pickup:'Hotel entrance',date:'2026-11-21',party:'7+',region:idea.region,tourId:idea.id,tourTitle:idea.title,vehicle:idea.vehicle,notes});
  const body=new URLSearchParams(href.split('?')[1]).get('body');
  for(const value of [idea.id,idea.title,idea.vehicle,notes,'subject to confirmation','7+ guests','separate']) assert.ok(body.includes(value),value);
  assert.doesNotMatch(quoteSource,/fetch\(|sendBeacon|localStorage|sessionStorage/);
});

test('homepage keeps ordinary booking before tour discovery and all styles retain the current online handoff',()=>{
  const home=readFileSync(new URL('../index.html',import.meta.url),'utf8');
  assert.ok(home.indexOf('renewal-booking-section')<home.indexOf('id="wine-day-ideas"'));
  for(const file of ['index.html','services/wine-tours.html','wine-tours/napa-valley.html','wine-tours/sonoma.html','wine-tours/livermore.html','wine-tours/healdsburg.html']){
    const page=readFileSync(new URL('../'+file,import.meta.url),'utf8');
    assert.match(page,/id="wine-day-catalog"/);assert.match(page,/data-plan-wine-day=/);
    assert.match(page,/Open email draft/);assert.match(page,/You send the request through your email app/);
    assert.match(page,/https:\/\/customer\.moovs\.app\/koast\/request\/new/);
    assert.doesNotMatch(page,/Get my exact price|Price after pickup|\$960|\$860/);
    assert.equal((page.match(/id="quote-request"/g)||[]).length,1,file);
  }
});
