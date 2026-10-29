export const duration=3600;
const clamp=x=>Math.max(0,Math.min(1,x));
const smooth=(t,a,b)=>{const u=clamp((t-a)/(b-a));return u*u*u*(u*(u*6-15)+10);};
// Measured on the selected photographic light trail in the 390x844 composition.
// Monotone cubic interpolation keeps each bend inside its measured corridor.
export const anchors=[[219,664],[175,641],[142,618],[96,595],[79,572],[60,549],[65,526],[93,504],[141,481],[206,458],[293,435],[323,421],[304,412],[285,406]];
const ys=anchors.map(p=>-p[1]),xs=anchors.map(p=>p[0]);
const h=ys.slice(1).map((v,i)=>v-ys[i]),d=h.map((v,i)=>(xs[i+1]-xs[i])/v),m=Array(xs.length).fill(0);
function endpoint(h0,h1,d0,d1){let v=((2*h0+h1)*d0-h0*d1)/(h0+h1);if(v*d0<=0)v=0;else if(d0*d1<0&&Math.abs(v)>Math.abs(3*d0))v=3*d0;return v;}
m[0]=endpoint(h[0],h[1],d[0],d[1]);m[m.length-1]=endpoint(h.at(-1),h.at(-2),d.at(-1),d.at(-2));
for(let i=1;i<m.length-1;i++){if(d[i-1]*d[i]>0){const w1=2*h[i]+h[i-1],w2=h[i]+2*h[i-1];m[i]=(w1+w2)/(w1/d[i-1]+w2/d[i]);}}
export const routePoints=[];
for(let i=0;i<anchors.length-1;i++)for(let j=0;j<64;j++){const u=j/64,u2=u*u,u3=u2*u;routePoints.push([(2*u3-3*u2+1)*xs[i]+(u3-2*u2+u)*h[i]*m[i]+(-2*u3+3*u2)*xs[i+1]+(u3-u2)*h[i]*m[i+1],-(ys[i]+h[i]*u)]);}
routePoints.push(anchors.at(-1));
const cumulative=[0];for(let i=1;i<routePoints.length;i++)cumulative.push(cumulative[i-1]+Math.hypot(routePoints[i][0]-routePoints[i-1][0],routePoints[i][1]-routePoints[i-1][1]));
export const routeLength=cumulative.at(-1);
export function atDistance(distance){const s=Math.max(0,Math.min(routeLength,distance));let lo=0,hi=cumulative.length-1;while(lo+1<hi){const mid=(lo+hi)>>1;if(cumulative[mid]<s)lo=mid;else hi=mid;}const span=cumulative[hi]-cumulative[lo],u=span?(s-cumulative[lo])/span:0;return [routePoints[lo][0]+u*(routePoints[hi][0]-routePoints[lo][0]),routePoints[lo][1]+u*(routePoints[hi][1]-routePoints[lo][1])];}
const pathFrom=points=>points.map((p,i)=>(i?'L':'M')+p.map(v=>v.toFixed(3)).join(' ')).join(' ');
export function sample(t,reduced=false){
 if(reduced)t=2200;
 const u=clamp((t-210)/1510),progress=1.55*u-.55*u*u,distance=routeLength*progress;
 const depth=1-.62*progress,head=atDistance(distance),tailLength=20*depth;
 const tail=Array.from({length:9},(_,i)=>atDistance(distance-tailLength*(1-i/8))),nose=Array.from({length:4},(_,i)=>atDistance(distance-5*depth*(1-i/3)));
 return {alpha:smooth(t,0,90)*(1-smooth(t,2800,3200)),art:smooth(t,45,820)*.95,logo:smooth(t,560,1380),tag:smooth(t,1160,1700),
 progress,distance,depth,x:head[0],y:head[1],tailX:tail[0][0],tailY:tail[0][1],trail:pathFrom(tail),nose:pathFrom(nose),
 light:smooth(t,185,310)*(1-smooth(t,1530,1700)),dotSize:11*depth};
}
export function stageMarkup(assets={art:'../assets/coastal.jpg',logo:'../wordmark.svg',light:'../assets/lightpoint.png'}){
 return `<svg xmlns="http://www.w3.org/2000/svg" width="390" height="844" viewBox="0 0 390 844" role="img" aria-label="Coastal Afterglow refined animated Koast Driver splash"><defs><linearGradient id="trail-gradient" gradientUnits="userSpaceOnUse"><stop stop-color="#2dd4bf" stop-opacity="0"/><stop offset=".55" stop-color="#36d6c8" stop-opacity=".45"/><stop offset=".86" stop-color="#c4fff1" stop-opacity=".85"/><stop offset="1" stop-color="#f5fffc"/></linearGradient><radialGradient id="dot-fade"><stop offset=".3" stop-color="white"/><stop offset="1" stop-color="black"/></radialGradient><mask id="dot-mask" maskUnits="objectBoundingBox" maskContentUnits="objectBoundingBox"><rect width="1" height="1" fill="url(#dot-fade)"/></mask><filter id="dot-white"><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncR type="linear" slope="1.2"/><feFuncG type="linear" slope="1.2"/><feFuncB type="linear" slope="1.2"/></feComponentTransfer></filter></defs><rect width="390" height="844" fill="#0b0d10"/><g id="whole" opacity="0"><image id="art" href="${assets.art}" width="390" height="844" preserveAspectRatio="xMidYMid slice" opacity="0"/><g id="streak" opacity="0"><path id="halo" fill="none" stroke="#2dd4bf" stroke-opacity=".14" stroke-linecap="round"/><path id="trail" fill="none" stroke="url(#trail-gradient)" stroke-linecap="round"/><path id="nose" fill="none" stroke="#f2fff8" stroke-opacity=".95" stroke-linecap="round"/></g><image id="dot" href="${assets.light}" opacity="0" mask="url(#dot-mask)" filter="url(#dot-white)" style="mix-blend-mode:screen"/><image id="logo" href="${assets.logo}" x="67" y="278" width="256" height="${256*454/1472}" opacity="0"/><text id="tag" x="195" y="388" text-anchor="middle" font-family="Arial,sans-serif" font-size="17.5" font-weight="800" letter-spacing="-.5" fill="#f4f5f7" opacity="0">Drive <tspan fill="#2dd4bf">easy.</tspan></text></g></svg>`;
}
export function attributes(s,mode='streak'){
 return {whole:{opacity:s.alpha},art:{opacity:s.art},logo:{opacity:s.logo},tag:{opacity:s.tag},streak:{opacity:mode==='streak'?s.light:0},
 halo:{d:s.trail,'stroke-width':4*s.depth},trail:{d:s.trail,'stroke-width':1.85*s.depth},nose:{d:s.nose,'stroke-width':1*s.depth},
 'trail-gradient':{x1:s.tailX,y1:s.tailY,x2:s.x,y2:s.y},dot:{opacity:s.light*(mode==='dot'?1:.75),x:s.x-(mode==='dot'?s.dotSize:8*s.depth)/2,y:s.y-(mode==='dot'?s.dotSize:8*s.depth)/2,width:mode==='dot'?s.dotSize:8*s.depth,height:mode==='dot'?s.dotSize:8*s.depth}};
}
export function bindScene(svg){const nodes=new Map(),cache=new Map();return (s,mode='streak')=>{for(const [id,attrs]of Object.entries(attributes(s,mode))){if(!nodes.has(id))nodes.set(id,svg.querySelector('#'+id));const node=nodes.get(id);for(const [key,value]of Object.entries(attrs)){const text=String(value),token=id+':'+key;if(cache.get(token)!==text){node.setAttribute(key,text);cache.set(token,text);}}}};}
export function renderSvg(t,assets,mode='streak',reduced=false){let svg=stageMarkup(assets);const values=attributes(sample(t,reduced),mode);for(const [id,attrs]of Object.entries(values)){svg=svg.replace(new RegExp('<[^>]+id="'+id+'"[^>]*>'),tag=>{for(const [key,value]of Object.entries(attrs)){const re=new RegExp(' '+key+'="[^"]*"');tag=re.test(tag)?tag.replace(re,' '+key+'="'+value+'"'):tag.replace(/\/?>(?=$)/,' '+key+'="'+value+'"'+(tag.endsWith('/>')?'/>':'>'));}return tag;});}return svg;}
