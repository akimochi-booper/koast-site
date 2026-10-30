export const SETTLED=2600,DURATION=3800;
const clamp=x=>Math.max(0,Math.min(1,x)),mix=(a,b,p)=>a+(b-a)*p;
const ease=(t,a,b)=>{let p=clamp((t-a)/(b-a));return p*p*p*(p*(p*6-15)+10)};
const logo='<img class="logo" src="../wordmark.svg" alt="">';
const lockup=()=>'<div class="brand">'+logo+'<div class="dispatch-label" aria-hidden="true"></div></div>';
const roads=['M-80 790 C60 765 40 566 145 518 C186 499 195 478 195 452','M195 940 C195 752 262 642 220 550 C204 515 195 480 195 452','M470 790 C333 760 345 557 247 518 C210 501 195 478 195 452'];
function routeSvg(){return '<svg class="route-art" viewBox="0 0 390 844" aria-hidden="true"><defs><filter id="route-glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="3.5"/></filter><linearGradient id="route-asphalt" x1="0" y1="1" x2="0" y2="0"><stop stop-color="#1a2127"/><stop offset="1" stop-color="#111a1f"/></linearGradient></defs>'+roads.map((d,i)=>'<g class="road road-'+i+'"><path class="asphalt" d="'+d+'" fill="none" stroke="url(#route-asphalt)" stroke-width="18"/><path class="road-edge" d="'+d+'" fill="none" stroke="'+(i===1?'#a17e4b':'#376965')+'" stroke-width=".65"/><path class="route-soft" d="'+d+'" fill="none" stroke="'+(i===1?'#ffb955':'#63d8cb')+'" stroke-width="7" filter="url(#route-glow)"/><path class="route-light" d="'+d+'" fill="none" stroke="'+(i===1?'#ffc778':'#70e0d4')+'" stroke-width="1.5" stroke-linecap="round"/></g>').join('')+'</svg>'}
export function markup(kind){
 if(kind==='converge')return '<div class="scene converge">'+routeSvg()+lockup()+'</div>';
 if(kind==='match')return '<div class="scene match">'+lockup()+'<div class="pairing"><div class="pair-head"><span>RIDES</span><span>CHAUFFEURS</span></div>'+[0,1,2].map(i=>'<div class="pair-row"><div class="ride-tile"><i class="ride-tab"></i><span class="tile-detail"><i></i><i></i></span></div><div class="pair-bridge"><i></i></div><div class="driver-tile"><span class="driver-portrait"></span><span class="driver-detail"><i></i></span></div></div>').join('')+'</div></div>';
 return '<div class="scene signature"><div class="glass-lockup"><div class="etched">'+lockup()+'</div><div class="colored">'+lockup()+'</div><div class="sheen">'+lockup()+'</div></div><div class="reflected">'+lockup()+'</div><div class="glass-light"></div></div>';
}
export function bind(stage,kind){
 const scene=stage.querySelector('.scene');let width=390,height=844;const resize=()=>{width=stage.clientWidth||390;height=stage.clientHeight||844};resize();
 const op=(n,p)=>{if(n)n.style.opacity=String(Math.round(p*10000)/10000)};
 const brand=stage.querySelector('.brand'),label=brand?.querySelector('.dispatch-label');
 const light=[...stage.querySelectorAll('.route-light')],soft=[...stage.querySelectorAll('.route-soft')],road=[...stage.querySelectorAll('.road')],lengths=light.map(p=>p.getTotalLength());
 const pairing=stage.querySelector('.pairing'),rows=[...stage.querySelectorAll('.pair-row')],colored=stage.querySelector('.colored'),etched=stage.querySelector('.etched'),sheen=stage.querySelector('.sheen'),reflected=stage.querySelector('.reflected'),glass=stage.querySelector('.glass-light');
 function signatureAt(t,a,b){const p=ease(t,a,b);op(brand,p);brand.style.transform='translate3d(0,'+((1-p)*4)+'px,0)';op(label,ease(t,a+160,b+150));}
 function draw(time,{reviewFade=false}={}){const t=Math.max(0,time);op(scene,reviewFade?ease(t,0,80)*(1-ease(t,3550,3780)):1);
  if(kind==='converge'){
   const fade=mix(1,.24,ease(t,1850,2500));
   light.forEach((n,i)=>{const p=ease(t,[180,310,90][i],[1350,1400,1380][i]),len=lengths[i],segment=len*.21,offset=segment-p*(len+segment);for(const path of[n,soft[i]]){path.style.strokeDasharray=segment+' '+(len*4);path.style.strokeDashoffset=String(offset);op(path,ease(t,80,250)*(1-ease(t,1410,1660)));}op(road[i],fade);});signatureAt(t,1130,1770);
  }else if(kind==='match'){
   signatureAt(t,1220,1850);op(pairing,ease(t,100,280)*(1-ease(t,1830,2390)));pairing.style.transform='translate3d(0,'+mix(0,-12,ease(t,1700,2350))+'px,0)';
   rows.forEach((row,i)=>{const arrive=ease(t,170+i*130,760+i*130),match=ease(t,630+i*130,1100+i*130),settle=ease(t,1260,1600);row.querySelector('.ride-tile').style.transform='translate3d('+mix(-70,0,arrive)+'px,0,0)';row.querySelector('.driver-tile').style.transform='translate3d('+mix(70,0,arrive)+'px,0,0)';op(row,arrive);const bridge=row.querySelector('.pair-bridge i');bridge.style.transform='scaleX('+match+')';op(bridge,.85*match);row.style.filter='brightness('+mix(1,1.22,match*(1-settle))+')';});
  }else{
   const reveal=ease(t,340,1770),front=mix(-30,120,reveal);op(etched,.07*ease(t,80,450)*(1-ease(t,1730,2150)));op(colored,1);const mask='linear-gradient(90deg,#000 '+(front-16)+'%,transparent '+front+'%)';colored.style.maskImage=mask;colored.style.webkitMaskImage=mask;
   const beam='linear-gradient(90deg,transparent '+(front-16)+'%,#000 '+(front-9)+'%,transparent '+(front+2)+'%)';sheen.style.maskImage=beam;sheen.style.webkitMaskImage=beam;op(sheen,.58*ease(t,250,650)*(1-ease(t,1490,1870)));
   op(reflected,.11*ease(t,570,1100)*(1-ease(t,1610,2260)));reflected.style.transform='translate3d(0,'+mix(0,16,ease(t,1250,2300))+'px,0) scaleY(-1)';op(glass,.12*ease(t,300,1000)*(1-ease(t,1500,2200)));glass.style.transform='translate3d('+mix(-width,width,reveal)+'px,0,0)';
  }
 }
 return{resize,draw};
}
