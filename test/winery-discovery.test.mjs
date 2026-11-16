import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,readdirSync} from 'node:fs';
import vm from 'node:vm';

const source=readFileSync(new URL('../wine-controls.js',import.meta.url),'utf8');
const context={}; vm.createContext(context); vm.runInContext(source,context);

test('winery search matches names, styles and areas without accent or case surprises',()=>{
  for(const [text,query,expected] of [
    ['Château St. Jean Sonoma Chardonnay','chateau',true],
    ['Wente Vineyards Arroyo Road Reservations encouraged','  ARROYO ',true],
    ['Ridge Zinfandel Dry Creek','zinfandel',true],
    ['Ridge Zinfandel Dry Creek','pinot',false],
    ['Concannon Vineyard','',true],
  ]) assert.equal(context.matchesWinery(text,query),expected);
});

test('every wine destination has concise visible planning and distinct photographs within the page',()=>{
  const files=['wine-tours','wineries'].flatMap(dir=>readdirSync(new URL('../'+dir+'/',import.meta.url))
    .filter(name=>name.endsWith('.html')&&name!=='index.html').map(name=>dir+'/'+name));
  assert.ok(files.length>=80);
  const wineryPhotos=new Map();
  for(const file of files){
    const html=readFileSync(new URL('../'+file,import.meta.url),'utf8');
    assert.doesNotMatch(html,/Detailed winery, pickup and return planning|Pacing &amp; reservations|class="reference-detail"/,file);
    assert.match(html,/class="reference-plan-grid"/,file);
    assert.match(html,/Vans, Sprinters and buses require a quote/,file);
    const photos=[...html.matchAll(/<img\b[^>]*src="(\/img\/[^\"]+\.(?:jpg|webp|png))"/g)].map(match=>match[1]);
    assert.ok(photos.length>=7,file);
    assert.equal(new Set(photos).size,photos.length,`${file}: repeated page photography`);
    const cards=[...html.matchAll(/<article\b[^>]*data-winery-card/g)];
    assert.ok(cards.length>=6,file+': complete regional discovery');
    assert.match(html,/data-winery-search/,file+': search for six or more stops');
    // All visits remain in authored HTML, before any carousel/search JavaScript.
    assert.equal((html.match(/data-search="/g)||[]).length,cards.length,file);
    for(const [,photo,name] of html.matchAll(/<article\b[^>]*data-winery-card[^>]*>\s*<img[^>]*src="([^"]+)"[^>]*>\s*<div[^>]*><h3>([^<]+)<\/h3>/g)){
      const key=name.replaceAll('&#x27;',"'").replaceAll('’',"'");
      if(wineryPhotos.has(key)) assert.equal(photo,wineryPhotos.get(key),`${key} changed card imagery between pages`);
      wineryPhotos.set(key,photo);
    }
    if(file.startsWith('wineries/')) assert.match(html,/<section class="reference-visit" id="winery-details">/,file);
  }
  assert.ok(wineryPhotos.size>=72,'Compare winery identities across the complete collection');
});

test('planning changes leave authored articles and legal reading surfaces outside the wine enhancer',()=>{
  for(const file of ['blog/group-wine-tour-planning.html','privacy.html','terms.html']){
    const html=readFileSync(new URL('../'+file,import.meta.url),'utf8');
    assert.doesNotMatch(html,/data-winery-browser|wine-controls\.js|reference-plan-grid/,file);
  }
});
