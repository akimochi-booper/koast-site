import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdirSync,mkdtempSync,writeFileSync,readFileSync,rmSync,renameSync,realpathSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {dirname,basename,join,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {collectSiteTests,runSiteChecks,siteDate} from '../scripts/check-pr.mjs';

const repository=resolve(dirname(fileURLToPath(import.meta.url)),'..');
function fixture(t){
  const root=mkdtempSync(join(tmpdir(),'koast-site-ci-'));
  t.after(()=>{
    const target=realpathSync(root);
    assert.equal(dirname(target),realpathSync(tmpdir()));
    assert.match(basename(target),/^koast-site-ci-[^\\/]+$/);
    rmSync(target,{recursive:true,force:true});
  });
  for(const file of ['test/public.test.mjs','workers/koast-chat/test/assistant.test.mjs']){
    mkdirSync(dirname(join(root,file)),{recursive:true});writeFileSync(join(root,file),'');
  }
  t.mock.method(console,'log',()=>{});t.mock.method(console,'error',()=>{});
  return root;
}

test('test discovery includes both owners and newly added files in stable order',t=>{
  const root=fixture(t);
  writeFileSync(join(root,'test/new-public.test.mjs'),'');
  writeFileSync(join(root,'workers/koast-chat/test/new-backend.test.mjs'),'');
  assert.deepEqual(collectSiteTests(root),[
    'test/new-public.test.mjs','test/public.test.mjs',
    'workers/koast-chat/test/assistant.test.mjs','workers/koast-chat/test/new-backend.test.mjs',
  ]);
});

test('missing, empty or non-file test owners fail before any process starts',t=>{
  for(const mode of ['missing','empty','non-file']){
    const root=fixture(t),directory=join(root,'workers/koast-chat/test');
    if(mode==='missing')renameSync(directory,join(root,'unavailable-tests'));
    if(mode==='empty')renameSync(join(directory,'assistant.test.mjs'),join(directory,'assistant.old'));
    if(mode==='non-file')mkdirSync(join(directory,'directory.test.mjs'));
    let calls=0;
    assert.throws(()=>runSiteChecks({root,today:'2026-11-13',run:()=>{calls++;return {status:0};}}));
    assert.equal(calls,0);
  }
});

test('validation generates first, includes every discovered suite, and checks pages last without a shell',t=>{
  const root=fixture(t),calls=[];
  assert.equal(runSiteChecks({root,today:'2026-11-13',run:(...args)=>{calls.push(args);return {status:0};}}),0);
  assert.deepEqual(calls[0].slice(0,2),['python',['generate.py']]);
  const testCall=calls.find(([,args])=>args[0]==='--test');
  assert.equal(testCall[0],process.execPath);
  assert.deepEqual(testCall[1],['--test','--test-concurrency=2',...collectSiteTests(root)]);
  const syntax=calls.filter(([,args])=>args[0]==='--check').map(([,args])=>args[1]);
  assert(syntax.includes('koast-chat.js'));assert(syntax.includes('koast-chat-voice.js'));
  assert(syntax.includes('sw.js'));
  assert(syntax.includes('workers/koast-chat/worker.js'));assert(syntax.includes('workers/koast-chat/photo-input.mjs'));
  assert.deepEqual(calls.at(-1).slice(0,2),['python',['scripts/check_site.py','--today','2026-11-13']]);
  for(const [,args,options] of calls){
    assert.equal(options.cwd,root);assert.equal(options.shell,false);assert.equal(options.windowsHide,true);
    assert(!args.some(arg=>/deploy|wrangler|https?:/.test(arg)),'validation has no deployment or service command');
  }
});

test('nonzero exits, signals and launch errors stop validation and remain failures',t=>{
  const root=fixture(t);
  for(const [result,expected] of [[{status:7},7],[{status:null,signal:'SIGTERM'},1],[{error:Error('unavailable Python')},1]]){
    let calls=0;
    assert.equal(runSiteChecks({root,today:'2026-11-13',run:()=>{calls++;return result;}}),expected);
    assert.equal(calls,1,'later checks must not disguise an earlier failure');
  }
  let calls=0;
  assert.equal(runSiteChecks({root,today:'2026-11-13',run:()=>({status:++calls===3?8:0})}),8);
  assert.equal(calls,3);
});

test('the default date follows the Pacific midnight boundary',()=>{
  assert.equal(siteDate(new Date('2026-11-13T07:59:59Z')),'2026-11-12');
  assert.equal(siteDate(new Date('2026-11-13T08:00:00Z')),'2026-11-13');
  assert.equal(siteDate(new Date('2026-07-01T06:59:59Z')),'2026-06-30');
  assert.equal(siteDate(new Date('2026-07-01T07:00:00Z')),'2026-07-01');
});

test('impossible or malformed dates cannot start the build',t=>{
  const root=fixture(t);
  for(const today of ['2026-02-30','2026-1-13','not-a-date','2026-11-13; deploy']){
    let calls=0;
    assert.throws(()=>runSiteChecks({root,today,run:()=>{calls++;return {status:0};}}),/real YYYY-MM-DD/);
    assert.equal(calls,0);
  }
});

test('CLI help works without site files and unknown arguments fail without starting validation',t=>{
  const root=fixture(t),script=join(root,'scripts/check-pr.mjs');
  mkdirSync(dirname(script));writeFileSync(script,readFileSync(join(repository,'scripts/check-pr.mjs')));
  renameSync(join(root,'test'),join(root,'unavailable-test'));
  const run=(...args)=>spawnSync(process.execPath,[script,...args],{cwd:root,encoding:'utf8',windowsHide:true,timeout:10000});
  const help=run('--help');assert.equal(help.status,0,help.stderr);assert.match(help.stdout,/Never deploys/);
  for(const args of [['--unknown'],['--today'],['--help','--today','2026-11-13']]){
    const result=run(...args);assert.notEqual(result.status,0);assert.match(result.stderr,/^Usage:/);assert.equal(result.stdout,'');
  }
});
