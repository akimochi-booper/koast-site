// Optional asset-authoring tool, never required by the production site build.
// npm install --prefix .favicon-tools --no-save @resvg/resvg-js@2.6.2 @xmldom/xmldom@0.9.12
// node scripts/build-favicon.mjs
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {readFile, writeFile, mkdir} from 'node:fs/promises';
import {resolve, dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const tools = resolve(root, process.env.KOAST_FAVICON_TOOLS || '.favicon-tools');
const require = createRequire(resolve(tools, 'package.json'));
const {Resvg} = require('@resvg/resvg-js');
const {DOMParser, XMLSerializer} = require('@xmldom/xmldom');
const sourcePath = resolve(root, 'img/koast-wordmark-orange-v1.svg');
const source = await readFile(sourcePath, 'utf8');
const parser = new DOMParser({onError(level, message) { throw new Error('SVG XML ' + level + ': ' + message); }});
const document = parser.parseFromString(source, 'image/svg+xml');
const children = node => Array.from(node.childNodes).filter(child => child.nodeType === 1);
const outer = children(document.documentElement).find(node => node.localName === 'g');
const monogram = children(outer).find(node => node.localName === 'g');
const gradient = Array.from(document.getElementsByTagName('linearGradient')).find(node => node.getAttribute('id') === 'gold-k');
assert.ok(monogram && gradient, 'Approved K group and gold-k gradient must exist.');
assert.equal(outer.getAttribute('fill-rule'), 'evenodd');
const sourcePaths = Array.from(monogram.getElementsByTagName('path'));
assert.equal(sourcePaths.length, 2, 'The approved K consists of exactly two paths.');
assert.ok(sourcePaths.every(path => path.getAttribute('fill') === 'url(#gold-k)'));

const serialize = node => new XMLSerializer().serializeToString(node);
const artwork = '<defs>' + serialize(gradient) + '</defs><g fill-rule="evenodd">' + serialize(monogram) + '</g>';
const svg = (viewBox, width) => '<svg xmlns="http://www.w3.org/2000/svg" width="' + width + '" height="' + width + '" viewBox="' + viewBox + '"><title>Koast</title>' + artwork + '</svg>\n';
// Measure in source coordinates, with a 1:1 root viewBox, retaining the original
// K translate/scale and gradient. Only the square viewport/padding changes.
const probe = '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="0 0 1600 1000">' + artwork + '</svg>';
const bounds = new Resvg(probe, {font:{loadSystemFonts:false}}).getBBox();
assert.ok(bounds && bounds.width > 0 && bounds.height > 0, 'K must have visible geometry.');
const side = Math.max(bounds.width, bounds.height) / 0.875; // 6.25% clear space on each edge.
const viewBox = [bounds.x + bounds.width / 2 - side / 2, bounds.y + bounds.height / 2 - side / 2, side, side].map(value => Number(value.toFixed(9))).join(' ');
const favicon = svg(viewBox, 64);
const generated = parser.parseFromString(favicon, 'image/svg+xml');
const faviconPaths = Array.from(generated.getElementsByTagName('path'));
assert.deepEqual(faviconPaths.map(path => path.getAttribute('d')), sourcePaths.map(path => path.getAttribute('d')));
assert.deepEqual(faviconPaths.map(path => path.getAttribute('fill')), sourcePaths.map(path => path.getAttribute('fill')));
const generatedGroup = Array.from(generated.getElementsByTagName('g')).find(node => node.hasAttribute('transform'));
assert.equal(generatedGroup.getAttribute('transform'), monogram.getAttribute('transform'));
assert.equal(serialize(generated.getElementsByTagName('linearGradient')[0]), serialize(gradient));
await writeFile(resolve(root, 'img/koast-favicon-v2.svg'), favicon);

const images = [];
for (const size of [16,32,48]) {
  const rendered = new Resvg(favicon, {fitTo:{mode:'width',value:size},font:{loadSystemFonts:false}}).render();
  const png = rendered.asPng();
  assert.equal(png.readUInt32BE(16), size); assert.equal(png.readUInt32BE(20), size);
  // Renderer pixels verify transparency and contained, centered visible artwork.
  const alpha = rendered.pixels; let left=size,top=size,right=-1,bottom=-1;
  for(let y=0;y<size;y++)for(let x=0;x<size;x++)if(alpha[(y*size+x)*4+3]>0){left=Math.min(left,x);right=Math.max(right,x);top=Math.min(top,y);bottom=Math.max(bottom,y);}
  assert.ok(left>=1 && top>=1 && right<size-1 && bottom<size-1, 'Transparent padding must surround the K.');
  assert.ok(Math.abs(left-(size-1-right))<=1 && Math.abs(top-(size-1-bottom))<=1, 'Visible artwork must be centered.');
  await writeFile(resolve(root, 'img/koast-favicon-v2-' + size + '.png'), png);
  images.push({size,png,bounds:{left,top,right,bottom}});
}

const header = Buffer.alloc(6 + images.length * 16); header.writeUInt16LE(1,2); header.writeUInt16LE(images.length,4);
let offset = header.length;
for (let index=0;index<images.length;index++) {
  const {size,png}=images[index], entry=6+index*16;
  header[entry]=size; header[entry+1]=size; header.writeUInt16LE(1,entry+4); header.writeUInt16LE(32,entry+6);
  header.writeUInt32LE(png.length,entry+8); header.writeUInt32LE(offset,entry+12); offset+=png.length;
}
const ico=Buffer.concat([header,...images.map(image=>image.png)]);
for(let index=0;index<images.length;index++) {
  const entry=6+index*16, start=ico.readUInt32LE(entry+12), length=ico.readUInt32LE(entry+8);
  assert.deepEqual(ico.subarray(start,start+length),images[index].png);
  assert.equal(ico.readUInt32BE(start+16),images[index].size);
}
await writeFile(resolve(root,'favicon-v2.ico'),ico);
await mkdir(tools,{recursive:true});
await writeFile(resolve(tools,'favicon-preview.png'),new Resvg(favicon,{fitTo:{mode:'width',value:256},font:{loadSystemFonts:false}}).render().asPng());
console.log(JSON.stringify({source:'img/koast-wordmark-orange-v1.svg',sourceSha256:createHash('sha256').update(source).digest('hex'),sourceBounds:{x:bounds.x,y:bounds.y,width:bounds.width,height:bounds.height},viewBox,pathsIdentical:true,transformIdentical:true,gradientIdentical:true,images:images.map(({size,png,bounds})=>({size,bytes:png.length,bounds})),icoBytes:ico.length,renderer:'@resvg/resvg-js2.6.2',xmlParser:'@xmldom/xmldom0.9.12'},null,2));
