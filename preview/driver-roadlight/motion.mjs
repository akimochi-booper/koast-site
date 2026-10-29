export const duration=3600;
export const names=['Refined Flow','The On-Ramp','Night Interchange'];
export const descriptions=['The current road language, with a cleaner light pass and a quieter finish.','One sweeping foreground road carries the light upward toward the identity.','Layered roads, with traffic passing behind and emerging from the overpass.'];
// Exact road geometry from the current Driver splash; no replacement icon artwork.
export const paths=[
 'M-10 160 C 90 150, 150 100, 200 98 S 300 120, 320 70',
 'M320 180 C 240 170, 190 130, 130 128 S 30 140, -10 100',
 'M-10 70 C 70 76, 210 50, 320 130'
];
const cubics=[[[[-10,160],[90,150],[150,100],[200,98]],[[200,98],[250,96],[300,120],[320,70]]],[[[320,180],[240,170],[190,130],[130,128]],[[130,128],[70,126],[30,140],[-10,100]]],[[[-10,70],[70,76],[210,50],[320,130]]]];
export const lengths=cubics.map(segments=>segments.reduce((sum,points)=>{let previous=points[0],length=0;for(let i=1;i<=1000;i++){const t=i/1000,u=1-t,next=[0,1].map(axis=>u*u*u*points[0][axis]+3*u*u*t*points[1][axis]+3*u*t*t*points[2][axis]+t*t*t*points[3][axis]);length+=Math.hypot(next[0]-previous[0],next[1]-previous[1]);previous=next;}return sum+length;},0));
export const layouts=[
 {logo:[82,202,226],road:[0,320,390,524],tag:297,size:15,order:[2,0,1]},
 {logo:[65,285,260],road:[-35,250,460,700],tag:395,size:17.5,order:[1,2,0]},
 {logo:[67,255,256],road:[-20,335,430,470],tag:365,size:17.5,order:[0,2,1]}
];
const clamp=x=>Math.max(0,Math.min(1,x));
const part=(t,a,b)=>{const u=clamp((t-a)/(b-a));return u*u*u*(u*(u*6-15)+10);};
const glide=(t,a,b)=>{const u=clamp((t-a)/(b-a)),r=.16;return (u<r?u*u/(2*r):u-r/2)/(1-r/2);};
export function sample(option,t,reduced=false){
 if(reduced)t=2200;
 const passes=option===1?[[170,1650],[0,1],[0,1]]:option===2?[[180,1770],[760,2060],[490,1640]]:[[120,1500],[650,1830],[370,1460]];
 const lanes=passes.map(([a,b],lane)=>{
  const active=!(option===1&&lane!==0);
  const p=glide(t,a,b),front=1200*p;
  return {front,opacity:active?part(t,a,a+100)*(1-part(t,b-100,b))*(lane===1?.55:1):0};
 });
 return {alpha:part(t,0,80)*(1-part(t,2800,3200)),logo:option===1?part(t,480,1400):part(t,150,1050),rise:option===0?6*(1-part(t,150,1050)):0,
 reveal:1,tag:part(t,option===1?1220:1030,option===1?1720:1570),lanes};
}
export function stageMarkup(option,href='wordmark.svg'){
 const c=layouts[option],[x,y,w]=c.logo,[rx,ry,rw,rh]=c.road,h=w*454/1472;
 const laneMarkup=lane=>{
  const isWarm=lane===1,color=isWarm?'#ff8a38':lane===2?'#b4e2df':'#2dd4bf';
  const dim=option===1&&lane!==0?.16:1,road=option===2?12:11;
  const lights=[['haze',95,6,.35],['tail',100,2.6,.2],['trail',44,2.2,.65],['front',5,2.4,.95]].map(([id,length,width,opacity])=>`<path id="lane-${lane}-${id}" d="${paths[lane]}" fill="none" stroke="${id==='front'?'#e7ffff':color}" stroke-width="${width}" stroke-linecap="round" stroke-dasharray="${length*(isWarm?.65:1)*lengths[lane]/1000} 100000" stroke-dashoffset="${length*(isWarm?.65:1)*lengths[lane]/1000}" opacity="${opacity}" ${id==='haze'?'filter="url(#glow)"':''}/>`).join('');
  return `<g opacity="${dim}"><path d="${paths[lane]}" fill="none" stroke="#04080b" stroke-width="${road+5}" stroke-linecap="round"/><path d="${paths[lane]}" fill="none" stroke="url(#roadSurface)" stroke-width="${road}" stroke-linecap="round"/><path d="${paths[lane]}" fill="none" stroke="#34464e" stroke-width=".5" stroke-linecap="round" opacity=".24" transform="translate(0 -4.7)"/><g id="lane-${lane}" opacity="0">${lights}</g></g>`;
 };
 return `<svg xmlns="http://www.w3.org/2000/svg" width="390" height="844" viewBox="0 0 390 844" aria-label="${names[option]} animated Koast Driver splash" role="img"><defs><linearGradient id="roadSurface" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#17232a"/><stop offset="1" stop-color="#10171c"/></linearGradient><filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="2.4"/></filter><linearGradient id="reveal" x1="0" y1="0" x2="0" y2="1"><stop id="mask-dark" offset="1" stop-color="black"/><stop id="mask-light" offset="1" stop-color="white"/></linearGradient><mask id="logoMask"><rect x="${x-2}" y="${y-2}" width="${w+4}" height="${h+4}" fill="url(#reveal)"/></mask></defs><rect width="390" height="844" fill="#0b0d10"/><g id="whole" opacity="0"><svg x="${rx}" y="${ry}" width="${rw}" height="${rh}" viewBox="0 0 300 220" preserveAspectRatio="none" overflow="visible">${c.order.map(laneMarkup).join('')}</svg><g id="hero" opacity="0"><image href="${href}" x="${x}" y="${y}" width="${w}" height="${h}" ${option===1?'mask="url(#logoMask)"':''}/></g><text id="tagline" x="195" y="${c.tag}" text-anchor="middle" fill="#f4f5f7" font-family="Arial,sans-serif" font-size="${c.size}" font-weight="800" letter-spacing="-.45" opacity="0">Drive <tspan fill="#2dd4bf">easy.</tspan></text></g></svg>`;
}
export function applyFrame(svg,s){
 const q=id=>svg.querySelector('#'+id);
 q('whole').setAttribute('opacity',s.alpha);q('hero').setAttribute('opacity',s.logo);q('hero').setAttribute('transform','translate(0 '+s.rise+')');q('tagline').setAttribute('opacity',s.tag);
 const edge=1.18-1.36*s.reveal;q('mask-dark').setAttribute('offset',clamp(edge-.12));q('mask-light').setAttribute('offset',clamp(edge+.12));
 s.lanes.forEach((lane,i)=>{q('lane-'+i).setAttribute('opacity',lane.opacity);for(const [key,length] of [['haze',95],['tail',100],['trail',44],['front',5]])q('lane-'+i+'-'+key).setAttribute('stroke-dashoffset',(length*(i===1?.65:1)-lane.front)*lengths[i]/1000)});
}
export function renderSvg(option,t,href,reduced=false){
 const s=sample(option,t,reduced),edge=1.18-1.36*s.reveal;
 let text=stageMarkup(option,href);
 const attr=(id,name,value)=>{text=text.replace(new RegExp('(<[^>]+id="'+id+'"[^>]*?) '+name+'="[^"]*"'),'$1 '+name+'="'+value+'"');};
 attr('whole','opacity',s.alpha);attr('hero','opacity',s.logo);text=text.replace('id="hero"','transform="translate(0 '+s.rise+')" id="hero"');attr('tagline','opacity',s.tag);attr('mask-dark','offset',clamp(edge-.12));attr('mask-light','offset',clamp(edge+.12));
 s.lanes.forEach((lane,i)=>{attr('lane-'+i,'opacity',lane.opacity);for(const [key,length] of [['haze',95],['tail',100],['trail',44],['front',5]])attr('lane-'+i+'-'+key,'stroke-dashoffset',(length*(i===1?.65:1)-lane.front)*lengths[i]/1000)});
 return text;
}
