// Public website enquiries only. Fixed team recipient; no booking/account/model effects.
import {readBoundedBytes} from './photo-input.mjs';

const ORIGINS = new Set(['https://koastride.com','https://www.koastride.com']);
const TEAM_EMAIL = 'reserve@koastride.com';
const VEHICLES = new Set(['','SUV','First-Class SUV','Executive Sprinter','Party bus / coach']);
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const EMAIL = /^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+$/;
const singleLine = (value,max) => typeof value==='string' && value.trim().length<=max && !/[\u0000-\u001f\u007f]/.test(value);

export function validateQuoteRequest(value,now=Date.now()) {
  if(!value || typeof value!=='object' || Array.isArray(value)) return {error:'invalid_request'};
  if(!UUID.test(value.requestId||'') || !Number.isFinite(value.createdAt)) return {error:'invalid_request'};
  // Resend retains idempotency keys for24h. Never replay an old uncertain send beyond that window.
  if(value.createdAt<now-23*3600000 || value.createdAt>now+300000) return {error:'expired_request'};
  if(value.website) return {error:'invalid_request'};
  if(!singleLine(value.name,80)||!value.name.trim()) return {error:'name',field:'name'};
  if(!singleLine(value.email,254)||!EMAIL.test(value.email.trim())) return {error:'email',field:'email'};
  if(!singleLine(value.pickup,180)||!value.pickup.trim()) return {error:'pickup',field:'pickup'};
  if(!/^(?:[1-6]|7\+)$/.test(value.party||'')) return {error:'party',field:'party'};
  if(!singleLine(value.region,100)||!value.region.trim()) return {error:'region'};
  if(!VEHICLES.has(value.vehicle)) return {error:'vehicle'};
  if(typeof value.date!=='string') return {error:'date'};
  if(value.date) {
    const parsed=new Date(value.date+'T12:00:00Z');
    const today=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Los_Angeles',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date(value.createdAt));
    if(!/^\d{4}-\d{2}-\d{2}$/.test(value.date)||!Number.isFinite(parsed.getTime())||parsed.toISOString().slice(0,10)!==value.date||value.date<today) return {error:'date',field:'date'};
  }
  if(!singleLine(value.tourId,80)||!singleLine(value.tourTitle,100)|| (value.tourId && !/^[a-z0-9-]+$/.test(value.tourId))) return {error:'idea'};
  if(typeof value.notes!=='string'||value.notes.length>1200||/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/.test(value.notes)) return {error:'notes'};
  if(typeof value.page!=='string'||!/^\/(?:$|services\/wine-tours|wine-tours\/[a-z0-9-]+|wineries\/[a-z0-9-]+)$/.test(value.page)) return {error:'page'};
  return {quote:{requestId:value.requestId.toLowerCase(),createdAt:value.createdAt,name:value.name.trim(),email:value.email.trim(),pickup:value.pickup.trim(),date:value.date,party:value.party,region:value.region.trim(),vehicle:value.vehicle,tourId:value.tourId,tourTitle:value.tourTitle,notes:value.notes.trim(),page:value.page}};
}

export function quoteEmail(quote,from) {
  const fields=[['Reference',quote.requestId],['Name',quote.name],['Reply email',quote.email],['Wine country',quote.region],['Suggested day (unconfirmed)',quote.tourTitle||'Custom plans'],['Idea reference',quote.tourId||'None'],['Requested vehicle (unconfirmed)',quote.vehicle||'Help me choose'],['Pickup',quote.pickup],['Travel date',quote.date||'To be confirmed'],['Party',quote.party==='7+'?'7+ guests · group quote':quote.party+' guest'+(quote.party==='1'?'':'s')],['Customer notes',quote.notes||'None'],['Public page','https://koastride.com'+quote.page]];
  return {from,to:[TEAM_EMAIL],reply_to:quote.email,subject:'Website quote request · '+quote.region+' · '+quote.requestId.slice(0,8),text:'New website transportation enquiry\n\n'+fields.map(([label,value])=>label+': '+value).join('\n\n')+'\n\nCustomer-supplied enquiry only. No booking, price, availability or tasting reservation has been confirmed. Reply to the customer to arrange the quote.'};
}

export function quoteRequestsReady(env) {
  return Boolean(env.QUOTE_EMAIL_KEY && typeof env.QUOTE_EMAIL_FROM==='string' && /^Koast Website <[A-Za-z0-9._+-]+@(?:[A-Za-z0-9-]+\.)*koastride\.com>$/.test(env.QUOTE_EMAIL_FROM) && env.QUOTE_RATE_LIMITER?.limit && env.QUOTE_GLOBAL_LIMITER?.limit);
}

export async function handleQuoteRequests(request,env,{transport=fetch,now=Date.now()}={}) {
  const origin=request.headers.get('Origin')||'';
  const headers={'Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Vary':'Origin','Access-Control-Allow-Methods':'POST, OPTIONS','Access-Control-Allow-Headers':'Content-Type',...(ORIGINS.has(origin)?{'Access-Control-Allow-Origin':origin}:{})};
  const respond=(body,status=200,extra={})=>Response.json(body,{status,headers:{...headers,...extra}});
  if(!ORIGINS.has(origin)) return respond({error:'origin'},403);
  if(request.method==='OPTIONS') return new Response(null,{status:204,headers});
  if(request.method!=='POST') return respond({error:'method'},405,{'Allow':'POST, OPTIONS'});
  if(!/^application\/json(?:\s*;|$)/i.test(request.headers.get('Content-Type')||'')) return respond({error:'content_type'},415);
  if(!quoteRequestsReady(env)) return respond({error:'unavailable'},503);
  const edgeIp=request.headers.get('CF-Connecting-IP');
  if(!edgeIp) return respond({error:'unavailable'},503);
  try {
    const digest=await crypto.subtle.digest('SHA-256',new TextEncoder().encode('website-quote:'+edgeIp));
    const ipKey=Array.from(new Uint8Array(digest),byte=>byte.toString(16).padStart(2,'0')).join('');
    if(!(await env.QUOTE_RATE_LIMITER.limit({key:ipKey})).success || !(await env.QUOTE_GLOBAL_LIMITER.limit({key:'website-quotes'})).success) return respond({error:'rate_limit'},429,{'Retry-After':'60'});
  } catch { return respond({error:'unavailable'},503); }
  let input;
  try {
    const bytes=await readBoundedBytes(request.body,8192,()=>new Error('too_large'));
    input=JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(bytes));
  } catch(error) { return respond({error:error.message==='too_large'?'too_large':'invalid_request'},error.message==='too_large'?413:400); }
  const result=validateQuoteRequest(input,now);
  if(result.error) return respond(result,result.error==='expired_request'?409:400);
  const quote=result.quote;
  try {
    const response=await transport('https://api.resend.com/emails',{method:'POST',headers:{'Authorization':'Bearer '+env.QUOTE_EMAIL_KEY,'Content-Type':'application/json','Idempotency-Key':'website-quote/'+quote.requestId},body:JSON.stringify(quoteEmail(quote,env.QUOTE_EMAIL_FROM)),signal:AbortSignal.timeout(12000)});
    if(!response.ok) {
      // No customer/provider response body is logged or exposed; uncertain retries keep the same key.
      console.warn(JSON.stringify({event:'website_quote_delivery_unconfirmed',reference:quote.requestId,status:response.status}));
      return respond({error:'delivery_unconfirmed',reference:quote.requestId},503);
    }
    const data=JSON.parse(new TextDecoder().decode(await readBoundedBytes(response.body,4096,()=>new Error('response_too_large'))));
    if(typeof data.id!=='string'||!/^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(data.id)) throw new Error('missing_provider_receipt');
    console.info(JSON.stringify({event:'website_quote_accepted',reference:quote.requestId,providerId:data.id}));
    return respond({ok:true,reference:quote.requestId},200);
  } catch {
    return respond({error:'delivery_unconfirmed',reference:quote.requestId},503);
  }
}
