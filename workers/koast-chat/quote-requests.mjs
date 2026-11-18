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
  const escape=value=>String(value).replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const date=quote.date ? new Intl.DateTimeFormat('en-US',{weekday:'short',month:'short',day:'numeric',year:'numeric',timeZone:'UTC'}).format(new Date(quote.date+'T12:00:00Z')) : 'Date not provided';
  const party=quote.party==='7+'?'7+ guests — exact count to confirm':quote.party+' guest'+(quote.party==='1'?'':'s');
  const source='https://koastride.com'+quote.page;
  const reply='mailto:'+encodeURIComponent(quote.email);
  const created=new Intl.DateTimeFormat('en-US',{dateStyle:'medium',timeStyle:'short',timeZone:'America/Los_Angeles'}).format(new Date(quote.createdAt))+' Pacific';
  const trip=[['Travel date',date],['Passengers',party],['Pickup location',quote.pickup],['Requested vehicle',quote.vehicle||'Customer would like help choosing']];
  const context=[['Wine region',quote.region],['Wine-day idea',quote.tourTitle||'No day idea selected']];
  const notes=quote.notes||'No additional notes provided.';
  const notice='Quote request only. No booking, price, availability or tasting reservation has been confirmed.';
  const fields=rows=>rows.map(([label,value])=>label+': '+value).join('\n');
  const text=['NEW WEBSITE INQUIRY',quote.name+' · '+quote.region,'ACTION: Reply to '+quote.email+' to clarify the plans and prepare a quote.','CONTACT\n'+fields([['Name',quote.name],['Email',quote.email]]),'TRIP REQUEST\n'+fields(trip),'CUSTOMER NOTES\n'+notes,'BROWSING CONTEXT\n'+fields(context),'Before quoting: confirm the pickup time, return plan, exact party size where needed, and tasting appointments with the customer.',notice,'REQUEST DETAILS\n'+fields([['Source page',source],['Request created',created],['Reference',quote.requestId],['Idea reference',quote.tourId||'Not selected']])].join('\n\n');
  const rows=items=>items.map(([label,value])=>`<tr><td style="padding:12px 0;border-bottom:1px solid #e7e4dd"><div style="font-size:12px;line-height:18px;color:#59616a">${escape(label)}</div><div style="font-size:16px;line-height:24px;color:#20242a;overflow-wrap:anywhere;word-break:break-word">${escape(value)}</div></td></tr>`).join('');
  const section=(title,content)=>`<h2 style="margin:26px 0 4px;font-size:13px;line-height:20px;color:#59616a;text-transform:uppercase;letter-spacing:1px">${title}</h2>${content}`;
  const table=items=>`<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">${rows(items)}</table>`;
  const html=`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>New website inquiry</title></head>
<body style="margin:0;background:#f4f2ed;color:#20242a;font-family:Arial,Helvetica,sans-serif">
<div style="display:none;max-height:0;overflow:hidden">${escape(quote.name)} · ${escape(quote.region)} · ${escape(date)} · ${escape(party)}</div>
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background:#f4f2ed"><tr><td align="center" style="padding:24px 12px">
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="max-width:620px;background:#fff;border:1px solid #e7e4dd;border-radius:16px"><tr><td style="padding:28px 24px">
<a href="https://koastride.com/"><img src="https://koastride.com/img/koast-wordmark-orange-v1.png" alt="Koast" width="146" height="45" style="display:block;width:146px;height:45px;border:0"></a>
<p style="margin:24px 0 6px;font-size:12px;letter-spacing:1px;color:#59616a">NEW WEBSITE INQUIRY</p>
<h1 style="margin:0;font-size:26px;line-height:34px;overflow-wrap:anywhere">${escape(quote.name)}</h1>
<p style="margin:8px 0 20px;font-size:16px;line-height:24px;color:#59616a">${escape(quote.region)} · ${escape(date)}<br>${escape(party)}</p>
<a href="${escape(reply)}" style="display:inline-block;padding:13px 20px;background:#f7a339;border-radius:10px;color:#241205;font-size:15px;font-weight:bold;text-decoration:none">Reply to customer</a>
<p style="font-size:13px;line-height:20px;color:#59616a">Replies go to <a href="${escape(reply)}" style="color:#a63b10;overflow-wrap:anywhere">${escape(quote.email)}</a>.</p>
${section('Trip request',table(trip))}
${section('Customer notes',`<div style="padding:16px;background:#f8f6f1;border-left:3px solid #e9ad59;font-size:16px;line-height:25px;white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word">${escape(notes)}</div>`)}
${section('Browsing context',table(context))}
<p style="margin:24px 0 12px;font-size:14px;line-height:22px">Before quoting, confirm the pickup time, return plan, exact party size where needed, and tasting appointments with the customer.</p>
<p style="padding:14px;background:#f8f6f1;font-size:13px;line-height:21px;color:#59616a">${notice}</p>
${section('Request details',`<p style="font-size:12px;line-height:20px;color:#59616a;overflow-wrap:anywhere;word-break:break-word">Source: <a href="${escape(source)}" style="color:#a63b10">${escape(source)}</a><br>Request created: ${escape(created)}<br>Reference: ${escape(quote.requestId)}<br>Idea reference: ${escape(quote.tourId||'Not selected')}</p>`)}
</td></tr></table><p style="margin:16px 0;font-size:12px;color:#59616a">Koast website · Internal team notification</p></td></tr></table></body></html>`;
  return {from,to:[TEAM_EMAIL],reply_to:quote.email,subject:'Website inquiry · '+quote.region+' · '+date+' · '+quote.name,text,html};
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
