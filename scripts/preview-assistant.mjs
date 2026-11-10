import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import {resolve,extname,sep} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=resolve(fileURLToPath(new URL('..',import.meta.url)));
const port=Number(process.env.PORT);if(!Number.isInteger(port)||port<1024)throw new Error('Use the allocated PORT.');
const failed=new Set();
const mime={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.svg':'image/svg+xml','.webp':'image/webp','.jpg':'image/jpeg','.png':'image/png','.woff2':'font/woff2','.json':'application/json'};
createServer(async(req,res)=>{
 const url=new URL(req.url,'http://127.0.0.1:'+port);
 const send=(status,type,body)=>{res.writeHead(status,{'Content-Type':type,'Cache-Control':'no-store'});res.end(body);};
 if(url.pathname==='/__preview_booking')return send(200,'text/html','<html style="background:#f8f5ef"><body style="font:14px system-ui;color:#777;padding:24px">Booking widget is inactive in this local preview.</body></html>');
 if(url.pathname==='/__preview_chat/capabilities')return send(200,'application/json',JSON.stringify({photos:true,maxPhotos:2,maxFileBytes:8388608}));
 if(url.pathname==='/__preview_chat'){
  let raw='';for await(const chunk of req){raw+=chunk;if(raw.length>1153434)return send(413,'application/json','{}');}
  let body;try{body=JSON.parse(raw);}catch{return send(400,'application/json','{}');}
  const question=String(body.messages?.at(-1)?.content||'');
  if(question.toLowerCase().includes('retry preview')&&!failed.has(question)){failed.add(question);return send(503,'application/json','{}');}
  const count=(body.messages||[]).reduce((n,m)=>n+(m.images?.length||0),0);
  const reply=count?'I can see '+count+' attached sample photo'+(count>1?'s':'')+' in this local test. For a ride, tell me your passenger count and luggage details; our team confirms vehicle fit and availability.':question.toLowerCase().includes('vehicle')?'I can help you compare vehicle classes. How many people are traveling, and how much luggage will you have? For the final price and availability, use Get a quote below.':question.toLowerCase().includes('wine')?'Start with your pickup location, group size, and preferred wineries. I can help you think through the itinerary. Our team confirms your route, availability, and fixed price in the quote.':'For an airport pickup, include your flight details when requesting your ride. Which airport are you arriving at, and how many people are traveling?';
  return setTimeout(()=>send(200,'application/json',JSON.stringify({reply})),question.toLowerCase().includes('pending preview')?2500:650);
 }
 let relative=decodeURIComponent(url.pathname).replace(/^\/+/,''),file=resolve(root,relative||'index.html');
 if(!file.startsWith(root+sep)&&file!==resolve(root,'index.html'))return send(403,'text/plain','Forbidden');
 try{let data;try{data=await readFile(file);}catch{if(!extname(file)){try{file+='.html';data=await readFile(file);}catch{file=resolve(root,relative,'index.html');data=await readFile(file);}}else throw new Error('missing');}const ext=extname(file);if(ext==='.js'&&file.endsWith('koast-chat.js'))data=data.toString().replace('https://koast-chat.euburaga.workers.dev','/__preview_chat');if(ext==='.html')data=data.toString().replaceAll('https://customer.moovs.app/koast/iframe','/__preview_booking').replace('<body>','<body><div style="position:fixed;top:0;left:0;right:0;z-index:950;font:10px/18px system-ui;text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#ade8df;background:#102624">LOCAL PREVIEW · sample replies · no production actions</div>');return send(200,mime[ext]||'application/octet-stream',data);}catch{return send(404,'text/plain','Not found');}
}).listen(port,'127.0.0.1',()=>console.log('Website assistant local fixture http://127.0.0.1:'+port+'; no upstream chat or booking requests.'));
