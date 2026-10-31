// Local review of the generated site. No remote APIs or business writes.
import {createServer} from 'node:http';
import {readFile,stat} from 'node:fs/promises';
import {resolve,sep,extname} from 'node:path';
const root=resolve(new URL('..',import.meta.url).pathname.replace(/^\/([A-Za-z]:)/,'$1'));
const port=Number(process.env.PORT);
if(!Number.isInteger(port)||port<8980||port>8999)throw Error('Set PORT to the allocated shared Koast preview port (8980–8999).');
const mime={'.html':'text/html;charset=utf-8','.css':'text/css;charset=utf-8','.js':'text/javascript;charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp','.woff2':'font/woff2','.json':'application/json'};
createServer(async(req,res)=>{
  try{
    const url=new URL(req.url,'http://127.0.0.1');
    if(req.method!=='GET'&&req.method!=='HEAD'){res.writeHead(405).end();return;}
    if(url.pathname.startsWith('/api/')||url.pathname.startsWith('/oauth/')){res.writeHead(403).end('Local legal preview: external actions disabled.');return;}
    let file=resolve(root,'.'+decodeURIComponent(url.pathname));
    if(file!==root&&!file.startsWith(root+sep)){res.writeHead(403).end();return;}
    try{if((await stat(file)).isDirectory())file=resolve(file,'index.html');}
    catch{if(!extname(file))file+='.html';}
    const body=await readFile(file);
    res.writeHead(200,{'content-type':mime[extname(file)]||'application/octet-stream','cache-control':'no-store'}).end(req.method==='HEAD'?undefined:body);
  }catch{res.writeHead(404).end('Not found in local legal preview.');}
}).listen(port,'127.0.0.1',()=>console.log('Legal review: http://127.0.0.1:'+port+'/legal/'));
