/* Website reply navigation: exact destinations only, never model-authored HTML. */
(function(root){
  'use strict';
  var destinations=new Set([
    'https://koastride.com/',
    'https://koastride.com/#fleet',
    'https://koastride.com/services/airport-transfers',
    'https://koastride.com/services/corporate-travel',
    'https://koastride.com/services/wine-tours',
    'https://koastride.com/cities/',
    'https://koastride.com/blog/',
    'https://koastride.com/wineries/',
    'https://koastride.com/wine-tours/healdsburg',
    'https://customer.moovs.app/koast/request/new',
    'https://customer.moovs.app/koast/new/info',
    'mailto:reserve@koastride.com'
  ]);
  function approvedDestination(text){
    if(typeof text!=='string'||/[^\x21-\x7e]/.test(text))return null;
    if(text==='https://koastride.com')return 'https://koastride.com/';
    if(text==='reserve@koastride.com')return 'mailto:reserve@koastride.com';
    return destinations.has(text)?text:null;
  }
  // Examine complete tokens; never extract a trusted substring from a host/path.
  function parts(text){
    var result=[],cursor=0,match,tokens=/\S+/g;
    while((match=tokens.exec(text))){
      var token=match[0],leading=(token.match(/^[([{"']*/)||[''])[0];
      var trailing=(token.match(/[)\]}"'.,!;:]*$/)||[''])[0];
      var end=token.length-trailing.length,candidate=token.slice(leading.length,end);
      var href=approvedDestination(candidate);if(!href)continue;
      var start=match.index+leading.length;
      if(start>cursor)result.push({text:text.slice(cursor,start)});
      result.push({text:candidate,href:href});cursor=match.index+end;
    }
    if(cursor<text.length)result.push({text:text.slice(cursor)});
    return result;
  }
  function render(node,text){
    var segments=parts(text);
    if(!segments.some(function(part){return part.href;})){node.textContent=text;return;}
    node.textContent='';
    segments.forEach(function(part){
      if(!part.href){node.appendChild(document.createTextNode(part.text));return;}
      var link=document.createElement('a');link.href=part.href;link.textContent=part.text;
      node.appendChild(link);
    });
  }
  root.KoastReplyLinks={approvedDestination:approvedDestination,parts:parts,render:render};
})(typeof window==='undefined'?globalThis:window);
