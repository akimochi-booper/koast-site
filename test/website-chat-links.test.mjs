import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
const source=readFileSync(new URL('../koast-chat-links.js',import.meta.url),'utf8');
function fixture(){
 class Node{
  constructor(tag=''){this.tagName=tag;this.children=[];this.value='';}
  set textContent(value){this.value=value;this.children=[];}
  get textContent(){return this.value+this.children.map(child=>child.textContent).join('');}
  set innerHTML(value){throw new Error('HTML insertion is forbidden');}
  appendChild(child){this.children.push(child);return child;}
 }
 const document={createElement:tag=>new Node(tag),createTextNode:text=>{const node=new Node('#text');node.textContent=text;return node;}},window={};
 vm.runInNewContext(source,{document,window});return {api:window.KoastReplyLinks,node:new Node('div')};
}
test('exact approved destinations become same-context native links with visible literal labels',()=>{
 const {api,node}=fixture();
 const text='Quote: https://customer.moovs.app/koast/request/new. Existing ride: (https://customer.moovs.app/koast/new/info). Email reserve@koastride.com; see https://koastride.com/services/airport-transfers.';
 api.render(node,text);assert.equal(node.textContent,text);
 const links=node.children.filter(child=>child.tagName==='a');assert.equal(links.length,4);
 assert.deepEqual(links.map(link=>link.href),['https://customer.moovs.app/koast/request/new','https://customer.moovs.app/koast/new/info','mailto:reserve@koastride.com','https://koastride.com/services/airport-transfers']);
 for(const link of links){assert.equal(link.target,undefined);assert.equal(link.onclick,undefined);assert.equal(link.children.length,0);}
});
const attacks=[
 'javascript:alert(1)','data:text/html,evil','http://koastride.com/','//koastride.com/',
 'https://koastride.com.evil.test/','https://evil.test/https://koastride.com/',
 'https://koastride.com@evil.test/','https://evil@koastride.com/',
 'https://koastride.com:443/','https://koastride.com./','https://www.koastride.com/',
 'https://koastride.com/unknown','https://koastride.com/?next=https://evil.test',
 'https://koastride.com/#unknown','https://koastride.com/%2f','https://koastride.com/%2e%2e/',
 'https://koastride.com/\\evil','https://koastride.com/\u0000','https://koastride.com/\u200b',
 'https://koastride.com/\u202eevil','https://koastrіde.com/','HTTPS://KOASTRIDE.COM/',
 'https://customer.moovs.app/koast/request/new/','https://customer.moovs.app/other/request/new',
 'https://customer.moovs.app/koast/request/new?email=private','https://customer.moovs.app/koast/new/info#private',
 'https://customer.moovs.app.evil/koast/request/new','reserve@koastride.com.evil',
 'mailto:reserve@koastride.com?bcc=evil@example.test','mailto:evil@koastride.com',
 'https://koastride.com&#47;','https://%6boastride.com/','https://koastride.com/%252f',
 'prefixhttps://koastride.com/','[Click](https://koastride.com/)'
];
for(const attack of attacks)test('keeps unapproved token literal: '+JSON.stringify(attack),()=>{
 const {api,node}=fixture();assert.equal(api.approvedDestination(attack),null);
 api.render(node,'Before '+attack+' after');assert.equal(node.textContent,'Before '+attack+' after');assert.equal(node.children.length,0);
});
test('HTML-looking content stays text even when followed by an approved link',()=>{
 const {api,node}=fixture();const text='<img src=x onerror=alert(1)> https://koastride.com/';api.render(node,text);
 assert.equal(node.textContent,text);assert.equal(node.children.filter(child=>child.tagName==='a').length,1);
 assert.equal(node.children.some(child=>child.tagName==='img'),false);
});
test('empty and unlinked replies retain exact text without extra elements',()=>{
 for(const text of ['', 'How many bags?\nNo URL needed.']){const {api,node}=fixture();api.render(node,text);assert.equal(node.textContent,text);assert.equal(node.children.length,0);}
});
test('bare canonical host gets a native root link without changing its displayed text',()=>{
 const {api,node}=fixture();api.render(node,'Visit https://koastride.com.');
 assert.equal(node.textContent,'Visit https://koastride.com.');
 const link=node.children.find(child=>child.tagName==='a');assert.equal(link.href,'https://koastride.com/');assert.equal(link.textContent,'https://koastride.com');
});
test('every allowed public Koast destination has a generated canonical page',()=>{
 const sitemap=readFileSync(new URL('../sitemap.xml',import.meta.url),'utf8');
 const publicPages=new Set(Array.from(sitemap.matchAll(/<loc>([^<]+)<\/loc>/g),match=>match[1]));
 const destinations=Array.from(source.matchAll(/'(https:\/\/koastride\.com[^']*)'/g),match=>match[1]);
 assert.ok(destinations.length>=9);
 for(const destination of destinations){const canonical=new URL(destination);canonical.hash='';assert.ok(publicPages.has(canonical.href),'Missing canonical page: '+destination);}
});
