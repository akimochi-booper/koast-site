import {sample as baseSample,atDistance,stageMarkup as baseMarkup,attributes as baseAttributes} from './motion-v2.mjs';
export {duration} from './motion-v2.mjs';
export const names=['Bright Glint','Twin Headlights','Light Sweep'];
export const filenames=['glint.gif','headlights.gif','sweep.gif'];
export const descriptions=['A brighter white glint with a compact teal wake.','Two small white lamps, with a short shared light trail.','A longer illuminated sweep with a bright white leading edge.'];
const pathFrom=points=>points.map((p,i)=>(i?'L':'M')+p.map(v=>v.toFixed(3)).join(' ')).join(' ');
export function sample(style,t,reduced=false){
 const s=baseSample(t,reduced),depth=s.depth;
 const tailLength=style===2?58*depth+5:(style===1?13:7)*depth;
 const count=style===2?23:9,tail=Array.from({length:count},(_,i)=>atDistance(s.distance-tailLength*(1-i/(count-1))));
 const nose=Array.from({length:5},(_,i)=>atDistance(s.distance-(style===2?9:3)*depth*(1-i/4)));
 const before=atDistance(s.distance-.7),after=atDistance(s.distance+.7),dx=after[0]-before[0],dy=after[1]-before[1],length=Math.hypot(dx,dy)||1,gap=5*depth+1;
 const nx=-dy/length,ny=dx/length;
 const u=Math.max(0,Math.min(1,(t-1250)/400)),rise=u*u*u*(u*(u*6-15)+10);
 return {...s,art:s.art/.95*(.66+.29*(reduced?1:rise)),trail:pathFrom(tail),nose:pathFrom(nose),tailX:tail[0][0],tailY:tail[0][1],
 firstX:s.x+nx*gap/2,firstY:s.y+ny*gap/2,secondX:s.x-nx*gap/2,secondY:s.y-ny*gap/2,
 lampSize:7*depth+1.5,dotSize:style===0?20*depth+3:style===2?12*depth+2:7*depth+1.5};
}
export function stageMarkup(assets={art:'../../assets/coastal.jpg',logo:'../../wordmark.svg',light:'../../assets/lightpoint.png'}){
 let svg=baseMarkup(assets).replace(/slope="1.2"/g,'slope="1.5"');
 const second=`<image id="lamp-second" href="${assets.light}" opacity="0" mask="url(#dot-mask)" filter="url(#dot-white)" style="mix-blend-mode:screen"/><circle id="lamp-core-a" fill="#f7fffc" opacity="0"/><circle id="lamp-core-b" fill="#f7fffc" opacity="0"/>`;
 return svg.replace('<image id="logo"',second+'<image id="logo"');
}
export function attributes(s,style=0){
 const values=baseAttributes(s,'streak');
 const depth=s.depth;
 values.streak.opacity=s.light*(style===0?.40:1);
 values.halo['stroke-width']=(style===2?7:style===1?3:2.4)*depth;
 values.trail['stroke-width']=(style===2?3.5:style===1?1.55:1.1)*depth+(style===2?.5:0);
 values.trail.opacity=style===1?.45:1;
 values.nose['stroke-width']=(style===2?2:style===1?.7:.8)*depth+(style===2?.2:0);
 values.nose['stroke-opacity']=style===1?0:.95;
 const size=s.dotSize;
 values.dot={opacity:s.light*(style===2?.72:1),x:s.x-size/2,y:s.y-size/2,width:size,height:size};
 values['lamp-second']={opacity:0};values['lamp-core-a']={opacity:0};values['lamp-core-b']={opacity:0};
 if(style===1){values.dot={opacity:s.light,x:s.firstX-s.lampSize/2,y:s.firstY-s.lampSize/2,width:s.lampSize,height:s.lampSize};values['lamp-second']={opacity:s.light,x:s.secondX-s.lampSize/2,y:s.secondY-s.lampSize/2,width:s.lampSize,height:s.lampSize};values['lamp-core-a']={opacity:s.light,cx:s.firstX,cy:s.firstY,r:1.05*depth+.2};values['lamp-core-b']={opacity:s.light,cx:s.secondX,cy:s.secondY,r:1.05*depth+.2};}
 return values;
}
export function bindScene(svg){const nodes=new Map(),cache=new Map();return(s,style=0)=>{for(const[id,attrs]of Object.entries(attributes(s,style))){if(!nodes.has(id))nodes.set(id,svg.querySelector('#'+id));const node=nodes.get(id);for(const[key,value]of Object.entries(attrs)){const text=String(value),token=id+':'+key;if(cache.get(token)!==text){node.setAttribute(key,text);cache.set(token,text);}}}};}
export function renderSvg(style,t,assets,reduced=false){let svg=stageMarkup(assets);for(const[id,attrs]of Object.entries(attributes(sample(style,t,reduced),style))){svg=svg.replace(new RegExp('<[^>]+id="'+id+'"[^>]*>'),tag=>{for(const[key,value]of Object.entries(attrs)){const re=new RegExp(' '+key+'="[^"]*"');tag=re.test(tag)?tag.replace(re,' '+key+'="'+value+'"'):tag.replace(/\/?>(?=$)/,' '+key+'="'+value+'"'+(tag.endsWith('/>')?'/>':'>'));}return tag;});}return svg;}
