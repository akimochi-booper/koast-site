// Memory-only website submission. One immutable request/key survives uncertain retries.
function validateQuoteContact(values) {
  const name=String(values.name||'').trim(),email=String(values.email||'').trim();
  if(!name||name.length>80||/[\u0000-\u001f\u007f]/.test(name)) return {field:'name',message:'Enter your name.'};
  if(email.length>254||!/^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+$/.test(email)) return {field:'email',message:'Enter a valid email so we can reply.'};
  return {name,email};
}

function createQuoteSubmission({transport=fetch,now=Date.now,uuid=()=>crypto.randomUUID()}={}) {
  let attempt=null,pending=false,accepted=null,expired=false;
  const state=()=>({pending,locked:Boolean(attempt)&&!accepted,accepted,expired,reference:attempt?.requestId||null});
  return {
    state,
    reset(){if(pending||attempt&&!accepted)return false;attempt=null;accepted=null;expired=false;return true;},
    async submit(values) {
      if(pending)return {pending:true};
      if(accepted)return {ok:true,reference:accepted};
      if(expired)return {error:'expired_request',reference:attempt.requestId};
      if(!attempt) {
        const contact=validateQuoteContact(values);
        if(contact.field)return {error:'contact',...contact};
        attempt={requestId:uuid(),createdAt:now(),name:contact.name,email:contact.email,pickup:values.pickup,date:values.date,party:values.party,region:values.region,vehicle:values.vehicle||'',tourId:values.tourId||'',tourTitle:values.tourTitle||'',notes:values.notes||'',page:values.page,website:values.website||''};
      }
      pending=true;
      try {
        if(now()-attempt.createdAt>23*3600000){expired=true;return {error:'expired_request',reference:attempt.requestId};}
        const response=await transport('https://koast-chat.euburaga.workers.dev/quote-requests',{method:'POST',headers:{'Content-Type':'application/json'},credentials:'omit',cache:'no-store',redirect:'error',body:JSON.stringify(attempt),signal:AbortSignal.timeout(15000)});
        const data=await response.json();
        if(response.ok&&data.ok===true&&data.reference===attempt.requestId){accepted=data.reference;return {ok:true,reference:accepted};}
        if(response.status===400&&['name','email','pickup','party','date','vehicle','notes','region','idea','page','invalid_request'].includes(data.error)) {
          attempt=null;return {error:'invalid_request',field:data.field};
        }
        if(response.status===409&&data.error==='expired_request')expired=true;
        return {error:expired?'expired_request':data.error==='rate_limit'?'rate_limit':'delivery_unconfirmed',reference:attempt.requestId};
      } catch { return {error:'delivery_unconfirmed',reference:attempt.requestId}; }
      finally {pending=false;}
    },
  };
}
