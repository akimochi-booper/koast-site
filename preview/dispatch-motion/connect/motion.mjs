export const DURATION=3600,SETTLED=2100;
const clamp=x=>Math.max(0,Math.min(1,x));
const ease=(t,a,b)=>{const p=clamp((t-a)/(b-a));return p*p*p*(p*(p*6-15)+10)};
export function bind(stage){
 const scene=stage.querySelector('.scene'),map=stage.querySelector('.coastal-map'),base=stage.querySelector('.map-base'),light=stage.querySelector('.map-light'),brand=stage.querySelector('.identity'),label=stage.querySelector('.connect-label');
 // Measurement geometry follows the photographed road; it is never rendered as replacement artwork.
 const path=document.createElementNS('http://www.w3.org/2000/svg','path');path.setAttribute('d','M713 1390 C694 1300 672 1260 614 1233 S350 1134 192 1071 S68 1034 74 986 C75 945 112 923 163 906 S275 871 312 846 C350 815 405 800 487 781 S655 759 678 714 S706 677 722 660 C744 634 733 625 722 610 C700 586 742 574 807 558 C855 542 877 530 883 507 S874 490 881 479 C899 458 822 452 795 435 C766 416 828 416 863 409 S929 401 935 399');
 const length=path.getTotalLength();let width=390,height=487,scale=1,offX=0,offY=0;
 function resize(){width=map.clientWidth||390;height=map.clientHeight||487;scale=Math.max(width/1122,height/1402);offX=(width-1122*scale)/2;offY=(height-1402*scale)/2;}resize();
 const opacity=(node,p)=>node.style.opacity=String(Math.round(p*10000)/10000);
 function draw(t,{reviewFade=false}={}){t=Math.max(0,t);opacity(scene,reviewFade?1-ease(t,3380,3590):1);opacity(base,.86*ease(t,80,920));const p=ease(t,260,1490),point=path.getPointAtLength(length*p),x=(point.x*scale+offX)/width*100,y=(point.y*scale+offY)/height*100;const mask='radial-gradient(ellipse 17% 10% at '+x+'% '+y+'%,#000 5%,transparent 100%)';light.style.maskImage=mask;light.style.webkitMaskImage=mask;opacity(light,.58*ease(t,170,400)*(1-ease(t,1390,1930)));opacity(brand,ease(t,880,1600));opacity(label,ease(t,1120,1810));}
 return{draw,resize};
}