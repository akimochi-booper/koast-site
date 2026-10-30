export const SETTLED=2600,DURATION=4000;
const clip=x=>Math.max(0,Math.min(1,x)),mix=(a,b,p)=>a+(b-a)*p;
const ease=(t,a,b)=>{let p=clip((t-a)/(b-a));return p*p*p*(p*(p*6-15)+10)};
const brand='<div class="network-brand"><img class="network-wordmark" src="../wordmark.svg" alt=""><div class="network-label">NETWORK</div></div>';
export function markup(kind){
 if(kind==='formation')return '<div class="scene formation"><div class="floor-light"></div>'+[0,1,2].map(i=>'<div class="fleet-unit fleet-unit-'+i+'"><img src="./assets/suv-topdown.webp" alt=""></div>').join('')+brand+'</div>';
 const file=kind==='city'?'night-city':'after-hours';return '<div class="scene '+kind+'"><div class="photo-scene"><img class="photo-base" src="./assets/'+file+'.webp" alt=""><img class="photo-pass" src="./assets/'+file+'.webp" alt=""></div>'+brand+'</div>';
}
export function bind(stage,kind){
 const scene=stage.querySelector('.scene'),logo=stage.querySelector('.network-brand'),label=stage.querySelector('.network-label'),units=[...stage.querySelectorAll('.fleet-unit')],base=stage.querySelector('.photo-base'),pass=stage.querySelector('.photo-pass'),photo=stage.querySelector('.photo-scene'),floor=stage.querySelector('.floor-light');
 let width=390,height=844;const resize=()=>{width=stage.clientWidth||390;height=stage.clientHeight||width*844/390};resize();
 const opacity=(node,p)=>{if(node)node.style.opacity=String(Math.round(p*10000)/10000)};
 function identity(t,a,b){const p=ease(t,a,b);opacity(logo,p);logo.style.transform='translate3d(0,'+mix(5,0,p)+'px,0)';opacity(label,ease(t,a+210,b+210));}
 function draw(time,{reviewFade=false}={}){const t=Math.max(0,time);opacity(scene,reviewFade?ease(t,0,90)*(1-ease(t,3720,3980)):1);
  if(kind==='formation'){
   const xs=[.23,.5,.77],ys=[.728,.665,.728],start=[.02,.5,.98],delays=[240,60,390];
   units.forEach((unit,i)=>{const p=ease(t,delays[i],delays[i]+1370),x=mix(start[i],xs[i],p),y=mix(1.23,ys[i],p),angle=mix(i===0?9:i===2?-9:0,0,ease(t,delays[i]+200,delays[i]+1180));unit.style.width=width*.245+'px';unit.style.height=width*.49+'px';unit.style.transform='translate3d('+(x*width-width*.1225)+'px,'+(y*height-width*.245)+'px,0) rotate('+angle+'deg)';opacity(unit,ease(t,delays[i],delays[i]+220));});
   opacity(floor,.65*ease(t,280,1400));identity(t,980,1770);
  }else if(kind==='city'){
   const progress=ease(t,150,2170),camera=ease(t,100,2450);opacity(base,.12+.64*ease(t,100,1600));photo.style.transform='scale('+mix(1.055,1,camera)+')';
   const x=mix(.13,.95,progress),y=mix(.91,.51,progress),mask='radial-gradient(ellipse 18% 13% at '+(x*100)+'% '+(y*100)+'%,#000,transparent)';pass.style.maskImage=mask;pass.style.webkitMaskImage=mask;opacity(pass,.8*ease(t,100,400)*(1-ease(t,1700,2390)));identity(t,850,1640);
  }else{
   const progress=ease(t,100,1710),camera=ease(t,100,2320);opacity(base,.10+.68*ease(t,80,1550));photo.style.transform='translate3d('+mix(-3,0,camera)+'px,0,0) scale('+mix(1.018,1,camera)+')';
   const x=mix(-.04,1.08,progress),y=.6114-.1424*x,mask='radial-gradient(ellipse 17% 6% at '+(x*100)+'% '+(y*100)+'%,#000,transparent)';pass.style.maskImage=mask;pass.style.webkitMaskImage=mask;opacity(pass,.85*ease(t,70,330)*(1-ease(t,1560,2280)));identity(t,780,1600);
  }
 }
 return{resize,draw};
}
