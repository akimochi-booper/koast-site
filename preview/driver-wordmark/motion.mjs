export const duration=4000;
export const names=['Macro reveal','Teal field','Precision turn','Focus'];
export const files=['01-macro-reveal','02-teal-field','03-precision-turn','04-focus'];
export const descriptions=[
 'Start inside the K’s road curve, then pull back to the full wordmark.',
 'A full teal field transitions into the wordmark on charcoal.',
 'The wordmark turns gently toward you and settles squarely into place.',
 'Soft teal shapes come into crisp focus; DRIVER appears last.'
];
const p=(t,a,b)=>Math.max(0,Math.min(1,(t-a)/(b-a)));
const smooth=(t,a,b)=>{const u=p(t,a,b);return u*u*(3-2*u);};
const out=(t,a,b)=>1-Math.pow(1-p(t,a,b),3);
export function sample(option,t,reduced=false){
 if(reduced)t=2200;
 const alpha=smooth(t,0,100)*(1-smooth(t,3000,3350));
 const u=out(t,100,1600),scale=option===0?Math.exp(Math.log(8)*(1-u)):option===3?1+.08*(1-out(t,140,1500)):1;
 const w=310*scale,h=w*454/1472;
 const fx=option===0?.145+.355*u:.5,fy=option===0?.54-.04*u:.5;
 return {alpha,x:195-w*fx,y:388-h*fy,w,h,opacity:option===0?1:smooth(t,60,440),blur:option===3?14*(1-out(t,140,1500)):0,
 angleY:option===2?-66*(1-out(t,120,1550)):0,angleZ:option===2?-6*(1-out(t,120,1550)):0,
 edge:-25+150*smooth(t,350,1500),caption:smooth(t,1250,1770),captionY:464+4*(1-out(t,1250,1770))};
}
