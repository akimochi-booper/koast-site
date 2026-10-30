export const SETTLED=2200;export const DURATION=3400;
const clamp=x=>Math.max(0,Math.min(1,x));
const smooth=x=>{x=clamp(x);return x*x*x*(x*(x*6-15)+10)};
const ease=(t,a,b)=>smooth((t-a)/(b-a));
const lerp=(a,b,u)=>a+(b-a)*u;
const point='<img class="beam" src="./assets/lightpoint.webp" alt="">';
const signature='<img class="logo" src="./wordmark.svg" alt=""><div class="dispatch-label" aria-hidden="true"></div>';
export function markup(kind){
 if(kind==='relay')return '<div class="scene relay">'+point+point.replace('beam','beam teal')+'<img class="merge" src="./assets/lightpoint.webp" alt="">'+signature+'</div>';
 if(kind==='sync')return '<div class="scene sync"><div class="sync-lines"><i class="sync-lane"></i><i class="sync-lane"></i><i class="sync-lane"></i>'+[0,1,2].map(i=>'<img class="sync-light'+(i===1?' teal':'')+'" src="./assets/lightpoint.webp" alt="">').join('')+'</div>'+signature+'</div>';
 return '<div class="scene fleet"><img class="fleet-plate" src="./assets/fleet-ready.webp" alt="">'+[1,2,3].map(n=>'<img class="fleet-wash wash-'+['one','two','three'][n-1]+'" src="./assets/fleet-ready.webp" alt="">').join('')+[0,1,2].map(()=>'<img class="fleet-glow" src="./assets/lightpoint.webp" alt="">').join('')+signature+'</div>';
}
export function bind(stage,kind){
 const scene=stage.querySelector('.scene'),logo=stage.querySelector('.logo'),label=stage.querySelector('.dispatch-label');
 const nodes={beams:[...stage.querySelectorAll('.beam')],merge:stage.querySelector('.merge'),laneBox:stage.querySelector('.sync-lines'),lanes:[...stage.querySelectorAll('.sync-lane')],lights:[...stage.querySelectorAll('.sync-light')],plate:stage.querySelector('.fleet-plate'),washes:[...stage.querySelectorAll('.fleet-wash')],glows:[...stage.querySelectorAll('.fleet-glow')]};
 let width=390,height=844;const resize=()=>{width=stage.clientWidth||390;height=stage.clientHeight||width*844/390};resize();
 function opacity(node,value){if(node)node.style.opacity=String(Math.round(value*10000)/10000)}
 function pos(node,x,y,w,h){node.style.width=w+'px';node.style.height=h+'px';node.style.transform='translate3d('+(x*width-w/2)+'px,'+(y*height-h/2)+'px,0)'}
 function signatureAt(t,a,b){const p=ease(t,a,b);opacity(logo,p);logo.style.transform='translate3d(0,'+(6*(1-p))+'px,0)';logo.style.filter='blur('+(1.2*(1-p))+'px)';const q=ease(t,a+170,b+250);opacity(label,q);label.style.transform='translate3d(0,'+(3*(1-q))+'px,0)';}
 function draw(time,{reviewFade=true}={}){
  const t=Math.max(0,time),fade=reviewFade?ease(t,0,120)*(1-ease(t,3150,3380)):1;opacity(scene,fade);
  if(kind==='relay'){
   const a=ease(t,150,1010),b=ease(t,300,1140),exit=1-ease(t,1130,1450);
   pos(nodes.beams[0],lerp(-.12,.5,a),.568,width*.267,width*.033);opacity(nodes.beams[0],ease(t,100,300)*exit);
   pos(nodes.beams[1],lerp(1.12,.5,b),.568,width*.267,width*.033);opacity(nodes.beams[1],ease(t,250,450)*exit);
   nodes.merge.style.width=width*.205+'px';nodes.merge.style.height=width*.205+'px';opacity(nodes.merge,.32*ease(t,930,1150)*(1-ease(t,1200,1580)));signatureAt(t,900,1430);
  }else if(kind==='sync'){
   opacity(nodes.laneBox,1);const dismiss=1-ease(t,1520,1950);
   nodes.lanes.forEach((line,i)=>{const p=ease(t,150+i*130,870+i*130);line.style.transform='translate3d('+((i===1?35:-35)*(1-p))+'px,0,0) scaleX('+lerp(.18,1,p)+')';opacity(line,.42*ease(t,100+i*130,400+i*130)*dismiss);});
   nodes.lights.forEach((light,i)=>{const p=ease(t,300+i*170,1120+i*170),box=nodes.laneBox;const x=lerp(i===1?1.12:-.12,i===1?-.12:1.12,p),w=width*.205,h=width*.025;light.style.width=w+'px';light.style.height=h+'px';light.style.transform='translate3d('+(x*width*.64-w/2)+'px,'+(i*height*.15*.15-h/2)+'px,0)';opacity(light,.75*ease(t,240+i*170,430+i*170)*(1-ease(t,970+i*170,1180+i*170))*dismiss);});signatureAt(t,680,1350);
  }else{
   opacity(nodes.plate,.10+.58*ease(t,200,1800));nodes.washes.forEach((wash,i)=>opacity(wash,.36*ease(t,200+i*340,650+i*340)*(1-.62*ease(t,1400,2150))));
   [[.134,.584],[.321,.643],[.465,.711]].forEach(([x,y],i)=>{pos(nodes.glows[i],x,y,width*.108,width*.108);opacity(nodes.glows[i],.45*ease(t,300+i*340,610+i*340)*(1-.65*ease(t,1650,2200)));});signatureAt(t,1120,1750);
  }
 }
 return {draw,resize};
}
