// Public website photo boundary. No storage, uploaded URLs, filenames or logging.
export const MAX_PHOTOS = 2;
export const MAX_FILE_BYTES = 8 * 1024 * 1024;
export const MAX_PHOTO_BYTES = 350 * 1024;
export const MAX_BODY_BYTES = Math.floor(1.1 * 1024 * 1024);
const MAX_DIMENSION = 1280;
const MAX_PIXELS = MAX_DIMENSION * MAX_DIMENSION;

export class ChatInputError extends Error {
  constructor(code, status, reply) { super(code); this.code = code; this.status = status; this.reply = reply; }
}
const invalidPhoto = () => new ChatInputError('invalid_photo', 415, 'Choose a valid JPEG, PNG or WebP photo and try again.');
const unavailable = () => new ChatInputError('photos_unavailable', 503, 'Photos are unavailable right now. Remove the photos to send a text message.');
const tooLarge = () => new ChatInputError('photo_too_large', 413, 'This photo is too large. Choose a smaller photo and try again.');

export async function readBoundedBytes(stream, maximum, onOversize) {
  if (!stream) return new Uint8Array();
  const reader = stream.getReader(); const chunks = []; let size = 0;
  try {
    for (;;) {
      const {value, done} = await reader.read(); if (done) break;
      size += value.byteLength;
      if (size > maximum) { await reader.cancel(); throw onOversize(); }
      chunks.push(value);
    }
  } finally { reader.releaseLock(); }
  const bytes = new Uint8Array(size); let offset = 0;
  for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.byteLength; }
  return bytes;
}

export async function readChatBody(request) {
  if (!/^application\/json(?:\s*;|$)/i.test(request.headers.get('Content-Type') || ''))
    throw new ChatInputError('content_type', 415, 'Send a chat message as JSON.');
  const oversized = () => new ChatInputError('request_too_large', 413, 'This message is too large. Remove a photo or shorten your message.');
  const declared = request.headers.get('Content-Length');
  if (declared && (!/^\d+$/.test(declared) || Number(declared) > MAX_BODY_BYTES)) throw oversized();
  const bytes = await readBoundedBytes(request.body, MAX_BODY_BYTES, oversized);
  try { return JSON.parse(new TextDecoder('utf-8', {fatal:true}).decode(bytes)); }
  catch { throw new ChatInputError('bad_json', 400, 'This message could not be read. Try again.'); }
}

export function photosReady(env) {
  return Boolean(env.OPENAI_API_KEY && typeof env.IMAGES?.info === 'function' && typeof env.IMAGES?.input === 'function'
    && typeof env.PHOTO_RATE_LIMITER?.limit === 'function' && typeof env.PHOTO_GLOBAL_LIMITER?.limit === 'function');
}

export function sanitizeMessages(body) {
  if (!body || !Array.isArray(body.messages)) throw new ChatInputError('no_user_message', 400, 'Enter a message or attach a photo.');
  let count = 0;
  for (const message of body.messages) {
    if (!message || !['user','assistant'].includes(message.role) || typeof message.content !== 'string')
      throw new ChatInputError('invalid_message', 400, 'This conversation could not be read. Start a new message.');
    if (message.images !== undefined) {
      if (message.role !== 'user' || !Array.isArray(message.images)) throw invalidPhoto();
      count += message.images.length;
      if (count > MAX_PHOTOS) throw new ChatInputError('too_many_photos', 400, 'Send up to two photos at a time.');
    }
  }
  const messages = body.messages.slice(-12).map(message => ({role:message.role, content:message.content.slice(0,1000),
    ...(message.images?.length ? {images:message.images} : {})}));
  const last = messages.at(-1);
  if (!last || last.role !== 'user' || (!last.content.trim() && !last.images?.length))
    throw new ChatInputError('no_user_message', 400, 'Enter a message or attach a photo.');
  return messages;
}

function toBase64(bytes) {
  let value = '';
  for (let offset = 0; offset < bytes.length; offset += 8192) value += String.fromCharCode(...bytes.subarray(offset, offset + 8192));
  return btoa(value);
}

// Walk all JPEG scans, not only its first header. APP and COM segments are
// discarded even between progressive scans; trailing payloads are rejected.
export function inspectJpeg(bytes) {
  if (bytes.length < 12 || bytes[0] !== 255 || bytes[1] !== 216) throw invalidPhoto();
  const kept = [bytes.subarray(0,2)]; let offset = 2, dimensions = null, sawScan = false;
  while (offset < bytes.length) {
    const start = offset;
    if (bytes[offset++] !== 255) throw invalidPhoto();
    while (bytes[offset] === 255) offset++;
    const marker = bytes[offset++];
    if (marker === 217) {
      if (!dimensions || !sawScan || offset !== bytes.length) throw invalidPhoto();
      kept.push(bytes.subarray(start,offset));
      const clean = new Uint8Array(kept.reduce((sum,part)=>sum+part.length,0)); let at = 0;
      for (const part of kept) { clean.set(part,at); at += part.length; }
      return {...dimensions, bytes:clean};
    }
    if (marker === undefined || marker === 0 || marker === 216 || marker === 1 || marker >= 208 && marker <= 215) throw invalidPhoto();
    if (offset + 2 > bytes.length) throw invalidPhoto();
    const length = bytes[offset] * 256 + bytes[offset + 1];
    if (length < 2 || offset + length > bytes.length) throw invalidPhoto();
    if (marker >= 192 && marker <= 207 && ![196,200,204].includes(marker)) {
      if (![192,193,194].includes(marker) || dimensions || length < 8 || bytes[offset+2] !== 8) throw invalidPhoto();
      const height = bytes[offset+3]*256+bytes[offset+4], width = bytes[offset+5]*256+bytes[offset+6];
      if (!width || !height || width > MAX_DIMENSION || height > MAX_DIMENSION || width*height > MAX_PIXELS) throw tooLarge();
      const components = bytes[offset+7];
      if (![1,3].includes(components) || length !== 8 + 3*components) throw invalidPhoto();
      dimensions = {width,height};
    }
    offset += length;
    if (!(marker >= 224 && marker <= 239) && marker !== 254) kept.push(bytes.subarray(start,offset));
    if (marker === 218) {
      if (!dimensions) throw invalidPhoto(); sawScan = true; const scan = offset;
      for (;;) {
        if (offset >= bytes.length) throw invalidPhoto();
        if (bytes[offset++] !== 255) continue;
        const next = bytes[offset];
        if (next === 0 || next >= 208 && next <= 215) { offset++; continue; }
        offset--; break;
      }
      kept.push(bytes.subarray(scan,offset));
    }
  }
  throw invalidPhoto();
}

function decodePhoto(url) {
  if (typeof url !== 'string' || !url.startsWith('data:image/jpeg;base64,')) throw invalidPhoto();
  const encoded = url.slice(23);
  if (encoded.length > Math.ceil(MAX_PHOTO_BYTES / 3) * 4) throw tooLarge();
  if (!encoded || encoded.length % 4 || !/^[A-Za-z0-9+/]+={0,2}$/.test(encoded)) throw invalidPhoto();
  let binary; try { binary = atob(encoded); } catch { throw invalidPhoto(); }
  if (btoa(binary) !== encoded) throw invalidPhoto();
  if (binary.length > MAX_PHOTO_BYTES) throw tooLarge();
  return inspectJpeg(Uint8Array.from(binary, character=>character.charCodeAt(0)));
}

async function checkPhotoRate(request, env) {
  if (!photosReady(env)) throw unavailable();
  // Cloudflare overwrites this header at its edge. Never use X-Forwarded-For.
  const ip = request.headers.get('CF-Connecting-IP');
  if (!ip || ip.length > 45 || !/^[0-9a-f:.]+$/i.test(ip)) throw unavailable();
  const hash = await crypto.subtle.digest('SHA-256', new TextEncoder().encode('koast-chat-photo-v1:' + ip));
  const key = Array.from(new Uint8Array(hash), value=>value.toString(16).padStart(2,'0')).join('');
  try {
    const perIp = await env.PHOTO_RATE_LIMITER.limit({key});
    if (perIp?.success !== true) throw new ChatInputError('photo_rate_limit', 429, 'Please wait a minute before sending more photos.');
    const shared = await env.PHOTO_GLOBAL_LIMITER.limit({key:'website-photo'});
    if (shared?.success !== true) throw new ChatInputError('photo_rate_limit', 429, 'Photos are busy right now. Wait a minute or send a text message.');
  } catch (error) { if (error instanceof ChatInputError) throw error; throw unavailable(); }
}

export async function prepareModelMessages(messages, request, env) {
  const hasPhotos = messages.some(message=>message.images?.length);
  if (!hasPhotos) return messages;
  await checkPhotoRate(request, env);
  const input = [];
  for (const message of messages) {
    if (!message.images?.length) { input.push(message); continue; }
    const content = [{type:'input_text',text:message.content || 'Help me with this photo for my ride.'}];
    for (const image of message.images) {
      const source = decodePhoto(image);
      let transformed;
      try {
        const info = await env.IMAGES.info(new Response(source.bytes).body);
        if (!info || !['jpeg','image/jpeg'].includes(info.format) || info.width !== source.width || info.height !== source.height) throw invalidPhoto();
        const result = await env.IMAGES.input(new Response(source.bytes).body)
          .transform({width:MAX_DIMENSION,height:MAX_DIMENSION,fit:'scale-down'})
          .output({format:'image/jpeg',quality:75,anim:false});
        const response = result.response();
        if (!response.ok) throw unavailable();
        transformed = await readBoundedBytes(response.body,MAX_PHOTO_BYTES,tooLarge);
      } catch (error) { if (error instanceof ChatInputError) throw error; throw unavailable(); }
      // Re-encoding is mandatory; never forward the original bytes. Independently
      // remove all metadata and check the encoder's output before model input.
      const clean = inspectJpeg(transformed);
      content.push({type:'input_image',image_url:'data:image/jpeg;base64,'+toBase64(clean.bytes),detail:'auto'});
    }
    input.push({role:'user',content});
  }
  return input;
}
