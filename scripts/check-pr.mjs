// Local/CI validation only. Publication remains in the existing deploy workflow.
import {readdirSync} from 'node:fs';
import {dirname,resolve} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {spawnSync} from 'node:child_process';

const repository=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const testDirectories=['test','workers/koast-chat/test'];
const syntaxFiles=[
  'koast-acquisition.js','marketing-design.js','koast-chat-links.js','koast-chat-photos.js',
  'koast-chat.js','koast-chat-voice.js','sw.js','src/chat-voice.mjs',
  'workers/koast-chat/worker.js','workers/koast-chat/photo-input.mjs',
];

export function siteDate(now=new Date()){
  const parts=new Intl.DateTimeFormat('en-US',{
    timeZone:'America/Los_Angeles',year:'numeric',month:'2-digit',day:'2-digit',
  }).formatToParts(now);
  const value=type=>parts.find(part=>part.type===type).value;
  return `${value('year')}-${value('month')}-${value('day')}`;
}

export function collectSiteTests(root=repository){
  return testDirectories.flatMap(directory=>{
    const files=readdirSync(resolve(root,directory),{withFileTypes:true})
      .filter(entry=>{
        if(!entry.name.endsWith('.test.mjs'))return false;
        if(!entry.isFile())throw Error(`Site test must be a regular file: ${directory}/${entry.name}`);
        return true;
      })
      .map(entry=>`${directory}/${entry.name}`);
    if(!files.length)throw Error(`Site test discovery is empty: ${directory}`);
    return files;
  }).sort();
}

export function runSiteChecks({root=repository,today=siteDate(),run=spawnSync}={}){
  const parsed=new Date(today+'T00:00:00Z');
  if(!/^\d{4}-\d{2}-\d{2}$/.test(today)||!Number.isFinite(parsed.getTime())||parsed.toISOString().slice(0,10)!==today){
    throw Error('Site check date must be a real YYYY-MM-DD date in America/Los_Angeles.');
  }
  const tests=collectSiteTests(root);
  const steps=[
    ['Generate site','python',['generate.py']],
    ...syntaxFiles.map(file=>[`Parse ${file}`,process.execPath,['--check',file]]),
    ['Test website and assistant',process.execPath,['--test','--test-concurrency=2',...tests]],
    ['Check generated pages','python',['scripts/check_site.py','--today',today]],
  ];
  console.log(`Site validation: ${tests.length} test files, ${syntaxFiles.length} JavaScript syntax checks; Pacific date ${today}.`);
  for(const [name,command,args] of steps){
    console.log(name);
    const result=run(command,args,{cwd:root,stdio:'inherit',shell:false,windowsHide:true});
    if(result.error||result.signal||result.status!==0){
      console.error(`${name} failed: ${result.error?.message||result.signal||'exit '+result.status}`);
      return Number.isInteger(result.status)&&result.status>0?result.status:1;
    }
  }
  return 0;
}

if(process.argv[1]&&pathToFileURL(resolve(process.argv[1])).href===import.meta.url){
  try{
    const args=process.argv.slice(2);
    if(args.length===1&&args[0]==='--help'){
      console.log('Usage: node scripts/check-pr.mjs [--today YYYY-MM-DD]\nRegenerates local pages, parses JavaScript, runs all website/assistant tests, then validates links and metadata. Defaults to the current Pacific date. Never deploys.');
    }else{
      if(args.length&&!(args.length===2&&args[0]==='--today'&&args[1]))throw Error('Usage: node scripts/check-pr.mjs [--today YYYY-MM-DD]');
      process.exitCode=runSiteChecks(args.length?{today:args[1]}:{});
    }
  }catch(error){console.error(error.message);process.exitCode=1;}
}
