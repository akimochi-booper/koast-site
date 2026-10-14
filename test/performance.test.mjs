import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
const html=readFileSync(new URL('../airports/sjc.html',import.meta.url),'utf8');
const script=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]).find(s=>s.includes("iframe[data-src]"));
function setup(observer=true){
 const listeners={}, frame={dataset:{src:'https://customer.moovs.app/koast/iframe'},style:{},addEventListener:(n,fn)=>listeners[n]=fn};
 let callback,disconnected=false,writes=0,src;
 Object.defineProperty(frame,'src',{get:()=>src,set:v=>{src=v;writes++}});
 const window={addEventListener:(n,fn)=>listeners[n]=fn};
 class IO{constructor(fn){callback=fn}observe(f){assert.equal(f,frame)}disconnect(){disconnected=true}}
 if(observer)window.IntersectionObserver=IO;
 vm.runInNewContext(script,{window,IntersectionObserver:IO,document:{currentScript:{parentElement:{querySelector:()=>frame}},querySelectorAll:()=>[frame]}});
 return {frame,listeners,enter:v=>callback([{isIntersecting:v}]),writes:()=>writes,disconnected:()=>disconnected};
}
test('offscreen booking waits until near viewport and loads only once',()=>{
 const b=setup();assert.equal(b.frame.src,undefined);b.enter(false);assert.equal(b.writes(),0);
 b.enter(true);assert.equal(b.frame.src,'https://customer.moovs.app/koast/iframe');assert.equal(b.disconnected(),true);
 b.listeners.focus();assert.equal(b.writes(),1);
});
test('keyboard focus and browsers without IntersectionObserver can load booking',()=>{
 const b=setup();b.listeners.focus();assert.equal(b.writes(),1);assert.equal(setup(false).writes(),1);
});
test('booking sizing ignores other origins and unreasonable heights',()=>{
 const b=setup();b.listeners.message({origin:'https://untrusted.test',data:{height:900}});assert.equal(b.frame.style.height,undefined);
 b.listeners.message({origin:'https://customer.moovs.app',data:{height:5000}});assert.equal(b.frame.style.height,undefined);
 b.listeners.message({origin:'https://customer.moovs.app',data:{height:850}});assert.equal(b.frame.style.height,'850px');
});
