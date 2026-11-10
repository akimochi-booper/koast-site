/* Website Kopilot photo preparation. Originals never leave the browser; no storage APIs. */
(function(root){
  'use strict';
  var MAX_FILE=8*1024*1024,MAX_ENCODED=350*1024,MAX_PIXELS=24000000;
  function dimensions(bytes){
    var v=new DataView(bytes.buffer,bytes.byteOffset,bytes.byteLength),n=bytes.length;
    if(n>=24&&v.getUint32(0)===0x89504e47&&v.getUint32(4)===0x0d0a1a0a&&v.getUint32(12)===0x49484452)return [v.getUint32(16),v.getUint32(20),'image/png'];
    if(n>12&&bytes[0]===255&&bytes[1]===216){
      var i=2;while(i+4<=n){if(bytes[i++]!==255)break;while(bytes[i]===255)i++;var marker=bytes[i++];if(marker===0xda||marker===0xd9)break;if(marker===1||(marker>=0xd0&&marker<=0xd7))continue;if(i+2>n)break;var size=v.getUint16(i);if(size<2||i+size>n)break;if([192,193,194,195,197,198,199,201,202,203,205,206,207].indexOf(marker)>=0&&size>=8)return [v.getUint16(i+5),v.getUint16(i+3),'image/jpeg'];i+=size;}
    }
    if(n>=30&&v.getUint32(0)===0x52494646&&v.getUint32(8)===0x57454250){
      var kind=v.getUint32(12);
      if(kind===0x56503858)return [1+bytes[24]+(bytes[25]<<8)+(bytes[26]<<16),1+bytes[27]+(bytes[28]<<8)+(bytes[29]<<16),'image/webp'];
      if(kind===0x56503820&&bytes[23]===157&&bytes[24]===1&&bytes[25]===42)return [v.getUint16(26,true)&16383,v.getUint16(28,true)&16383,'image/webp'];
      if(kind===0x5650384c&&bytes[20]===47)return [1+bytes[21]+((bytes[22]&63)<<8),1+(bytes[22]>>6)+(bytes[23]<<2)+((bytes[24]&15)<<10),'image/webp'];
    }
    throw new Error('Choose a JPEG, PNG or WebP photo. Other files aren’t supported.');
  }
  async function prepare(file){
    if(!file||!file.size||file.size>MAX_FILE)throw new Error('Each photo must be 8 MB or smaller.');
    if(['image/jpeg','image/png','image/webp'].indexOf(file.type)<0)throw new Error('Choose a JPEG, PNG or WebP photo. For an iPhone HEIC photo, export it as JPEG first.');
    var size=dimensions(new Uint8Array(await file.arrayBuffer()));
    if(size[2]!==file.type||!size[0]||!size[1]||size[0]*size[1]>MAX_PIXELS||Math.max(size[0],size[1])>12000)throw new Error('This photo is too large or isn’t a valid image. Export a smaller JPEG and try again.');
    var bitmap;try{bitmap=await createImageBitmap(file,{imageOrientation:'from-image'});}catch(error){throw new Error('This photo couldn’t be opened. Try a different JPEG, PNG or WebP photo.');}
    try{
      if(bitmap.width*bitmap.height>MAX_PIXELS)throw new Error('This photo is too large. Export a smaller image.');
      var scale=Math.min(1,1280/Math.max(bitmap.width,bitmap.height));
      var canvas=document.createElement('canvas');canvas.width=Math.max(1,Math.round(bitmap.width*scale));canvas.height=Math.max(1,Math.round(bitmap.height*scale));
      var ctx=canvas.getContext('2d',{alpha:false});if(!ctx)throw new Error('Photo preparation is unavailable in this browser.');
      ctx.fillStyle='#fff';ctx.fillRect(0,0,canvas.width,canvas.height);ctx.drawImage(bitmap,0,0,canvas.width,canvas.height);
      for(var quality of [.8,.65,.5]){var url=canvas.toDataURL('image/jpeg',quality);if(url.startsWith('data:image/jpeg;base64,')&&(url.length-23)*.75<=MAX_ENCODED)return url;}
      throw new Error('This photo is still too detailed. Choose a smaller image.');
    }finally{bitmap.close();}
  }
  function Composer(options){
    var self=this;this.items=[];this.processing=false;this.busy=false;this.enabled=false;this.revision=0;this.options=options;
    options.button.addEventListener('click',function(){if(self.enabled&&!self.busy&&!self.processing)options.picker.click();});
    options.picker.addEventListener('change',function(){self.select(Array.from(options.picker.files||[]));options.picker.value='';});
  }
  Composer.prototype.load=async function(endpoint){
    if(this.loaded)return;this.loaded=true;
    try{var res=await fetch(endpoint.replace(/\/$/,'')+'/capabilities',{signal:AbortSignal.timeout(5000)});var data=await res.json();this.enabled=res.ok&&data.photos===true&&typeof createImageBitmap==='function';}catch(error){this.enabled=false;}
    if(!this.enabled)this.loaded=false;this.options.button.hidden=!this.enabled;this.render();
  };
  Composer.prototype.select=async function(files){
    if(!this.enabled||this.busy||this.processing||!files.length)return;
    var revision=++this.revision,self=this;
    if(this.items.length+files.length>2){this.options.notice.textContent='Add up to 2 photos per message.';return;}
    this.processing=true;this.options.notice.textContent='Preparing photos…';this.render();
    try{var prepared=[];for(var file of files){if(revision!==this.revision)break;prepared.push(await (this.options.prepare||prepare)(file));}if(revision===this.revision){this.items=this.items.concat(prepared);this.options.notice.textContent='';}}
    catch(error){if(revision===this.revision)this.options.notice.textContent=error.message||'This photo couldn’t be prepared. Try another photo.';}
    finally{self.processing=false;self.render();}
  };
  Composer.prototype.render=function(){
    var self=this,o=this.options;o.tray.textContent='';o.tray.hidden=!this.items.length;
    this.items.forEach(function(url,index){var tile=document.createElement('div');tile.className='kchat-photo';var image=document.createElement('img');image.src=url;image.alt='Attached photo '+(index+1);var remove=document.createElement('button');remove.type='button';remove.className='kchat-photo-remove';remove.setAttribute('aria-label','Remove photo '+(index+1));remove.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18"/></svg>';remove.disabled=self.busy||self.processing;remove.addEventListener('click',function(){self.items.splice(index,1);self.render();o.button.focus();});tile.appendChild(image);tile.appendChild(remove);o.tray.appendChild(tile);});
    o.button.disabled=this.busy||this.processing||this.items.length>=2;o.onChange();
  };
  Composer.prototype.take=function(){var result=this.items.slice();this.items=[];this.options.notice.textContent='';this.render();return result;};
  Composer.prototype.cancelPreparation=function(){this.revision++;if(this.options.notice.textContent==='Preparing photos…')this.options.notice.textContent='';this.render();};
  Composer.prototype.setBusy=function(value){this.busy=value;this.options.button.disabled=value||this.processing||this.items.length>=2;};
  root.KoastPhotoComposer=Composer;root.KoastPhotoPreparation={dimensions:dimensions,prepare:prepare};
})(typeof window==='undefined'?globalThis:window);
