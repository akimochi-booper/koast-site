#!/usr/bin/env python3
"""Koast site generator. Data lives in data.py — add a city there and re-run."""
import os
from data import BOOK, PHONE, SMS, EMAIL, FLEET, CITIES, AIRPORTS, WINE_REGIONS

ROOT = os.path.dirname(os.path.abspath(__file__))

# Care Rides launch switch — False keeps the service out of the built site
CARE_RIDES_LIVE = False

def head(title, desc, prefix="", extra=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}css/main.css?v=11">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#0e1013">{extra}
</head>
<body>"""

NAV_ITEMS = [("index.html#fleet","Fleet","fleet"),
             ("services/airport-transfers.html","Airports","airport"),
             ("services/corporate-travel.html","Corporate","corporate"),
             ("services/wine-tours.html","Wine Tours","wine"),
             ("cities/index.html","Cities","cities"),
             ("blog/index.html","Guides","blog"),
             ("support.html","Support","support")]

def nav(prefix="", active=""):
    AC = ' class="active"'
    ca = "".join(f'<a href="{prefix}wine-tours/{s}.html">{r["name"]}</a>' for s,r in WINE_REGIONS.items() if r["area"]=="ca")
    us = "".join(f'<a href="{prefix}wine-tours/{s}.html">{r["name"]}</a>' for s,r in WINE_REGIONS.items() if r["area"]=="us")
    _cpop = ["san-francisco","los-angeles","new-york","chicago","miami","las-vegas"]
    _cmore = ["seattle","dallas","boston","washington-dc","san-diego","atlanta"]
    cpop = "".join(f'<a href="{prefix}cities/{c}.html">{CITIES[c]["name"]}</a>' for c in _cpop if c in CITIES)
    cmore = "".join(f'<a href="{prefix}cities/{c}.html">{CITIES[c]["name"]}</a>' for c in _cmore if c in CITIES)
    _orange = 'style="color:var(--orange)!important;font-weight:700"'
    svc_active = active in ('airport','corporate','services','weddings','party-bus','fleet')

    services_dd = f'''<div class="nav-dd"><a href="{prefix}services/airport-transfers.html"{AC if svc_active else ''}>Services <span class="caret">&#9662;</span></a>
      <div class="dd-menu"><div class="dd-col"><h5>Ride types</h5><a href="{prefix}services/airport-transfers.html">Airport Transfers</a><a href="{prefix}services/corporate-travel.html">Corporate Travel</a><a href="{prefix}services/weddings.html">Weddings</a><a href="{prefix}services/party-bus.html">Party Bus</a><a href="{prefix}index.html#fleet">Our Fleet</a></div></div></div>'''
    wine_dd = f'''<div class="nav-dd"><a href="{prefix}services/wine-tours.html"{AC if active=='wine' else ''}>Wine <span class="caret">&#9662;</span></a>
      <div class="dd-menu"><div class="dd-col"><h5>California</h5>{ca}</div><div class="dd-col"><h5>Nationwide</h5>{us}</div><div class="dd-col"><h5>Browse</h5><a href="{prefix}wineries/index.html" {_orange}>All 72 wineries &#8594;</a><a href="{prefix}services/wine-tours.html">Wine tour service</a></div></div></div>'''
    cities_dd = f'''<div class="nav-dd"><a href="{prefix}cities/index.html"{AC if active=='cities' else ''}>Cities <span class="caret">&#9662;</span></a>
      <div class="dd-menu"><div class="dd-col"><h5>Popular</h5>{cpop}</div><div class="dd-col"><h5>More</h5>{cmore}<a href="{prefix}cities/index.html" {_orange}>All cities &#8594;</a></div></div></div>'''
    links = services_dd + wine_dd + cities_dd
    links += f'<a href="{prefix}blog/index.html"{AC if active=="blog" else ""}>Guides</a>'
    links += f'<a href="{prefix}support.html"{AC if active=="support" else ""}>Support</a>'

    mlinks = f'''<details class="mm-dd"><summary>Services <span class="mm-caret">&#9662;</span></summary><div class="mm-dd-list"><a href="{prefix}services/airport-transfers.html">Airport Transfers</a><a href="{prefix}services/corporate-travel.html">Corporate Travel</a><a href="{prefix}services/weddings.html">Weddings</a><a href="{prefix}services/party-bus.html">Party Bus</a><a href="{prefix}index.html#fleet">Our Fleet</a></div></details>
      <details class="mm-dd"><summary>Wine <span class="mm-caret">&#9662;</span></summary><div class="mm-dd-list"><a href="{prefix}services/wine-tours.html" class="mm-all">Wine tour service &#8594;</a><a href="{prefix}wineries/index.html" class="mm-all">Browse all wineries &#8594;</a><h6>California</h6>{ca}<h6>Nationwide</h6>{us}</div></details>
      <details class="mm-dd"><summary>Cities <span class="mm-caret">&#9662;</span></summary><div class="mm-dd-list"><a href="{prefix}cities/index.html" class="mm-all">All cities &#8594;</a>{cpop}{cmore}</div></details>
      <a href="{prefix}blog/index.html">Guides</a>
      <a href="{prefix}support.html">Support</a>'''

    return f"""
<nav class="site-nav"><div class="wrap nav-inner">
  <a class="logo" href="{prefix}index.html"><img src="{prefix}img/logo-transparent.png" alt="Koast — Premier Chauffeur Service" style="height:58px;width:auto"></a>
  <div class="nav-links">{links}</div>
  <div class="nav-cta">
    <a class="btn btn-line" href="https://customer.moovs.app/koast/new/info">Log In</a>
    <a class="btn btn-orange" href="{BOOK}">Book a Ride</a>
    <button class="nav-burger" onclick="document.body.classList.toggle('nav-open')" aria-label="Menu">&#9776;</button>
  </div>
</div>
<div class="mobile-menu">{mlinks}<a href="https://customer.moovs.app/koast/new/info">Log In</a></div>
</nav>"""


# ============================ AI CHAT WIDGET ============================
# After deploying the Worker, set its URL here and re-run generate.py
CHAT_WORKER_URL = "https://koast-chat.euburaga.workers.dev"

CHAT_WIDGET = """
<button id="kchat-fab" aria-label="Chat with Koast" onclick="document.body.classList.toggle('kchat-open')">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
</button>
<div id="kchat" role="dialog" aria-label="Koast assistant">
  <div class="kchat-head">
    <div class="kchat-id"><span class="kcoin">K</span><div><strong>Koast Agent</strong><span>Online — answers in seconds</span></div></div>
    <button class="kchat-x" onclick="document.body.classList.remove('kchat-open')" aria-label="Close">&times;</button>
  </div>
  <div class="kchat-msgs" id="kchat-msgs">
    <div class="km bot">Hi! Ask me anything about booking, airports, the fleet, or wine tours. For exact prices, the instant-quote widget is the way.</div>
    <div class="kchat-chips">
      <button onclick="kchatAsk(this.textContent)">How does airport pickup work?</button>
      <button onclick="kchatAsk(this.textContent)">Do you have car seats?</button>
      <button onclick="kchatAsk(this.textContent)">What's included in the price?</button>
    </div>
  </div>
  <div id="kchat-att" class="kchat-att"></div>
  <div class="kchat-foot">
    <button id="kchat-mic" class="kchat-tool" type="button" aria-label="Speak" title="Speak"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line></svg></button>
    <button id="kchat-attach" class="kchat-tool" type="button" aria-label="Attach a photo" title="Attach a photo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><path d="M21 15l-5-5L5 21"></path></svg></button>
    <input id="kchat-in" type="text" placeholder="Type, speak, or attach a photo…" maxlength="500">
    <button id="kchat-send" aria-label="Send">→</button>
    <input id="kchat-file" type="file" accept="image/*" multiple hidden>
  </div>
  <a class="kchat-sms" href="mailto:reserve@koastride.com">Prefer a human? Email us →</a>
</div>
<script>
(function(){
  var URL_="__CHAT_URL__";
  var IMG_LIVE=false; /* flip to true once the booking system handles photos/itineraries */
  var msgs=document.getElementById('kchat-msgs'),inp=document.getElementById('kchat-in'),btn=document.getElementById('kchat-send');
  var mic=document.getElementById('kchat-mic'),attBtn=document.getElementById('kchat-attach'),fileIn=document.getElementById('kchat-file'),attWrap=document.getElementById('kchat-att'),panel=document.getElementById('kchat');
  var hist=[],busy=false,atts=[];
  function add(cls,text){var d=document.createElement('div');d.className='km '+cls;if(text)d.textContent=text;msgs.appendChild(d);msgs.scrollTop=msgs.scrollHeight;return d;}
  window.kchatAsk=function(q){inp.value=q;send();};

  /* image attach + drag-and-drop */
  function renderAtts(){
    attWrap.innerHTML='';attWrap.style.display=atts.length?'flex':'none';
    atts.forEach(function(a,i){
      var t=document.createElement('div');t.className='kchat-thumb';
      var im=document.createElement('img');im.src=a.url;t.appendChild(im);
      var x=document.createElement('button');x.type='button';x.setAttribute('aria-label','Remove');x.innerHTML='&times;';
      x.addEventListener('click',function(){atts.splice(i,1);renderAtts();});
      t.appendChild(x);attWrap.appendChild(t);
    });
  }
  function addFiles(files){
    for(var i=0;i<files.length;i++){(function(f){
      if(!f.type||f.type.indexOf('image/')!==0)return;
      if(atts.length>=4)return;
      var rd=new FileReader();rd.onload=function(){atts.push({name:f.name,url:rd.result});renderAtts();};rd.readAsDataURL(f);
    })(files[i]);}
  }
  attBtn.addEventListener('click',function(){fileIn.click();});
  fileIn.addEventListener('change',function(){addFiles(fileIn.files);fileIn.value='';});
  ['dragover','dragenter'].forEach(function(ev){panel.addEventListener(ev,function(e){e.preventDefault();panel.classList.add('drag');});});
  ['dragleave','dragend'].forEach(function(ev){panel.addEventListener(ev,function(e){e.preventDefault();panel.classList.remove('drag');});});
  panel.addEventListener('drop',function(e){e.preventDefault();panel.classList.remove('drag');if(e.dataTransfer&&e.dataTransfer.files)addFiles(e.dataTransfer.files);});

  /* voice to text (Web Speech API) */
  var SR=window.SpeechRecognition||window.webkitSpeechRecognition,rec=null,listening=false;
  if(SR){
    rec=new SR();rec.lang='en-US';rec.interimResults=true;rec.continuous=false;
    rec.onstart=function(){listening=true;mic.classList.add('rec');};
    rec.onend=function(){listening=false;mic.classList.remove('rec');};
    rec.onerror=function(){listening=false;mic.classList.remove('rec');};
    rec.onresult=function(e){var t='';for(var i=0;i<e.results.length;i++)t+=e.results[i][0].transcript;inp.value=t;};
    mic.addEventListener('click',function(){if(listening){rec.stop();return;}try{rec.start();}catch(err){}});
  } else { mic.style.display='none'; }

  function send(){
    var q=inp.value.trim();var imgs=atts.slice();
    if((!q && !imgs.length)||busy)return;
    if(listening&&rec){try{rec.stop();}catch(e){}}
    inp.value='';busy=true;
    var chips=msgs.querySelector('.kchat-chips');if(chips)chips.remove();
    var ud=add('user',q||'');
    if(imgs.length){var g=document.createElement('div');g.className='km-imgs';imgs.forEach(function(a){var im=document.createElement('img');im.src=a.url;g.appendChild(im);});ud.appendChild(g);}
    atts=[];renderAtts();
    if(imgs.length && !IMG_LIVE){
      add('bot',"Thanks for the photo! Reading itineraries and screenshots is coming soon with our new booking system. For now, tell me what you need in a message, or email us at reserve@koastride.com and a human will help.");
      if(!q){hist.push({role:'user',content:'(photo attached)'});busy=false;return;}
      hist.push({role:'user',content:q});
    } else {
      hist.push(imgs.length?{role:'user',content:q,images:imgs.map(function(a){return a.url;})}:{role:'user',content:q});
    }
    var dots=add('bot dots','…');
    fetch(URL_,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({messages:hist})})
      .then(function(r){return r.json()})
      .then(function(d){dots.remove();var a=d.reply||"Sorry — something went wrong. Email us at reserve@koastride.com and a human will help.";add('bot',a);hist.push({role:'assistant',content:a});busy=false;})
      .catch(function(){dots.remove();add('bot',"I can't connect right now — email us at reserve@koastride.com and a real person will answer.");busy=false;});
  }
  btn.addEventListener('click',send);
  inp.addEventListener('keydown',function(e){if(e.key==='Enter')send();});
})();
</script>
""".replace("__CHAT_URL__", CHAT_WORKER_URL)

# Externalize the chat script to one file (smaller pages, cached once across the site)
import re as _re0
_sm = _re0.search(r"<script>(.*?)</script>", CHAT_WIDGET, _re0.S)
if _sm:
    open(os.path.join(ROOT, "koast-chat.js"), "w", encoding="utf-8").write(_sm.group(1).strip())
    CHAT_WIDGET = CHAT_WIDGET.replace(_sm.group(0), '<script src="/koast-chat.js" defer></script>')

def footer(prefix=""):
    return f"""
<footer class="site-footer"><div class="wrap">
  <div class="foot-grid">
    <div>
      <div class="foot-logo"><img src="{prefix}img/logo-transparent.png" alt="Koast" style="height:58px;width:auto;margin-bottom:8px"></div>
      <p>Headquartered in San Francisco, California · Serving major cities nationwide</p>
      <p>{EMAIL}</p>
      <p style="margin-top:8px"><a href="mailto:{EMAIL}" style="color:#0e9d8e;font-weight:700">Email us anytime →</a></p>
    </div>
    <div><h4>Services</h4>
      <a href="{prefix}services/airport-transfers.html">Airport Transfers</a>
      <a href="{prefix}services/corporate-travel.html">Corporate Travel</a>
      <a href="{prefix}services/wine-tours.html">Wine Tours</a>
      <a href="{prefix}wineries/index.html">Wineries</a>
      {('<a href="' + prefix + 'services/care-rides.html">Care Rides</a>') if CARE_RIDES_LIVE else ""}
      <a href="{prefix}services/weddings.html">Weddings</a>
      <a href="{prefix}services/party-bus.html">Party Bus</a>
    </div>
    <div><h4>Cities</h4>
      <a href="{prefix}cities/san-francisco.html">San Francisco</a>
      <a href="{prefix}cities/new-york.html">New York</a>
      <a href="{prefix}cities/los-angeles.html">Los Angeles</a>
      <a href="{prefix}cities/chicago.html">Chicago</a>
      <a href="{prefix}cities/miami.html">Miami</a>
      <a href="{prefix}cities/index.html">All cities →</a>
    </div>
    <div><h4>Company</h4>
      <a href="{prefix}support.html">Support</a>
      <a href="{prefix}blog/index.html">Guides</a>
      <a href="{prefix}terms.html">Terms</a>
      <a href="{prefix}privacy.html">Privacy</a>
    </div>
  </div>
  <div class="foot-bottom">
    <span>© 2026 Koast. All rights reserved. · <em>Ride easy.</em></span>
    <span>Professional chauffeur service · Nationwide</span>
  </div>
</div></footer>
<script>if("serviceWorker" in navigator)navigator.serviceWorker.register("/sw.js");</script>
""" + CHAT_WIDGET + """
</body>
</html>"""

def book_card():
    return f"""
<div class="book-card book-widget">
  <iframe src="https://customer.moovs.app/koast/iframe" title="Book a ride with Koast"
    loading="lazy" style="width:100%;height:620px;border:none;border-radius:12px;background:#fff"></iframe>
  <div class="widget-fallback">Widget not loading? <a href="{BOOK}">Book directly here →</a></div>
  <script>
  window.addEventListener('message',function(e){{
    if(String(e.origin).indexOf('moovs')===-1)return;
    var h=null,d=e.data;
    if(d&&typeof d==='object')h=d.height||d.frameHeight||(d.payload&&d.payload.height);
    if(typeof d==='string'){{var m=d.match(/"height"\s*:\s*(\d+)/);if(m)h=+m[1];}}
    if(h&&h>300&&h<4000)document.querySelectorAll('.book-widget iframe').forEach(function(f){{f.style.height=h+'px';}});
  }});
  </script>
</div>"""

FLEET_INTERIORS = {
 "fleet-sedan.jpg": [("int-sedan-1.jpg","Rear seat"),("int-sedan-2.jpg","Passenger view"),("int-sedan-3.jpg","Front cabin"),("int-sedan-4.jpg","Trunk space")],
 "fleet-business-suv.jpg": [("int-bsuv-1.jpg","Second row"),("int-bsuv-2.jpg","Third row"),("int-bsuv-3.jpg","Front cabin"),("int-bsuv-4.jpg","Trunk space"),("int-bsuv-5.jpg","Seat map")],
 "fleet-first-class-suv.jpg": [("int-fsuv-1.jpg","Captain seats"),("int-fsuv-2.jpg","Third row"),("int-fsuv-3.jpg","Front cabin"),("int-fsuv-4.jpg","Trunk space"),("int-fsuv-5.jpg","Seat map")],
}

def fleet_section(prefix=""):
    cards = ""
    for v in FLEET:
        tags = "".join(f'<span class="tag">{t}</span>' for t in v["tags"][:2])
        if v.get("badge"):
            tags += f'<span class="tag tag-badge">{v["badge"]}</span>'
        ints = FLEET_INTERIORS.get(v["img"])
        strip = ""
        if ints:
            cells = "".join(f'<div><img src="{prefix}img/{f}" alt="Koast {v["name"]} — {lbl}" title="{lbl}" loading="lazy"></div>' for f, lbl in ints)
            strip = (f'<div class="int-wrap"><button class="int-nav iprev off" aria-label="Previous photos">‹</button>'
                     f'<div class="int-strip">{cells}</div>'
                     f'<button class="int-nav inext" aria-label="More photos">›</button></div>')
        cards += f"""
    <div class="card fleet-card">
      <div class="car-cut"><img src="{prefix}img/{v['img'].replace('.jpg','-cut.webp')}" alt="Koast {v['name']}" loading="lazy"></div>
      {strip}<h3>{v['name']}</h3>
      <div class="sub">{v['sub']}</div>
      <div class="tags">{tags}</div>
      <ul class="amen">{"".join(f"<li>{a}</li>" for a in v.get("amen", []))}</ul>
      <div class="row"><span>{v['price']}</span><a class="btn-book" href="{BOOK}">{v['cta']} →</a></div>
    </div>"""
    return f"""
<section id="fleet" style="padding-top:64px"><div class="wrap">
  <div class="sec-head center">
    <span class="pill">Our Fleet</span>
    <h2>Choose your ride. Know your price.</h2>
    <p style="margin-left:auto;margin-right:auto;max-width:560px">Every vehicle comes with a professional chauffeur, complimentary water, chargers, and free airport wait time.</p>
  </div>
  <div class="car-wrap">
    <button class="car-arrow prev" data-dir="-1" aria-label="Previous vehicles">←</button>
    <div class="car-track">{cards}
    </div>
    <button class="car-arrow next" data-dir="1" aria-label="Next vehicles">→</button>
  </div>
  <div class="car-dots"></div>
  <script>
  (function(){{
    var s=document.currentScript.closest('section'),t=s.querySelector('.car-track'),d=s.querySelector('.car-dots');
    var orig=t.children.length,K=2;
    var w=function(){{return t.children[0].offsetWidth+22}};
    var kids=[].slice.call(t.children);
    for(var i=0;i<K;i++) t.appendChild(kids[i].cloneNode(true));
    for(var j=orig-1;j>=orig-K;j--) t.insertBefore(kids[j].cloneNode(true),t.firstChild);
    requestAnimationFrame(function(){{t.scrollLeft=K*w()}});
    for(var i=0;i<orig;i++)(function(i){{var b=document.createElement('button');b.setAttribute('aria-label','Vehicle '+(i+1));b.onclick=function(){{t.scrollTo({{left:(i+K)*w(),behavior:'smooth'}})}};d.appendChild(b)}})(i);
    function wrap(){{
      var W=w();
      if(t.scrollLeft < (K-1)*W) t.scrollLeft += orig*W;
      else if(t.scrollLeft > (K+orig-1)*W) t.scrollLeft -= orig*W;
      var i=Math.round(t.scrollLeft/W)-K;
      i=((i%orig)+orig)%orig;
      Array.prototype.forEach.call(d.children,function(b,j){{b.classList.toggle('on',j===i)}});
    }}
    t.addEventListener('scroll',function(){{requestAnimationFrame(wrap)}});
    t.addEventListener('touchstart',function(){{s.classList.add('scrolled')}},{{passive:true,once:true}});
    var pv=s.querySelector('.car-arrow.prev'),nx=s.querySelector('.car-arrow.next');
    [pv,nx].forEach(function(b){{if(b)b.onclick=function(){{t.scrollBy({{left:parseInt(b.dataset.dir)*w(),behavior:'smooth'}})}}}});
    wrap();
    /* interior lightbox */
    if(!document.getElementById('klb')){{
      var lb=document.createElement('div');lb.id='klb';lb.className='klb';
      lb.innerHTML='<span class="klb-x">&times;</span><button class="klb-a klb-prev">&#8592;</button><img alt=""><button class="klb-a klb-next">&#8594;</button><div class="klb-cap"></div>';
      document.body.appendChild(lb);
      var im=lb.querySelector('img'),cap=lb.querySelector('.klb-cap'),set=[],idx=0;
      function show(i){{idx=(i+set.length)%set.length;im.src=set[idx].src;cap.textContent=set[idx].title||set[idx].alt;}}
      function close(){{lb.classList.remove('on');document.body.style.overflow=''}}
      lb.addEventListener('click',function(e){{if(e.target===lb||e.target.classList.contains('klb-x'))close()}});
      lb.querySelector('.klb-prev').onclick=function(e){{e.stopPropagation();show(idx-1)}};
      lb.querySelector('.klb-next').onclick=function(e){{e.stopPropagation();show(idx+1)}};
      document.addEventListener('keydown',function(e){{if(!lb.classList.contains('on'))return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(idx-1);if(e.key==='ArrowRight')show(idx+1)}});
      document.addEventListener('click',function(e){{
        var d=e.target.closest('.int-strip div');if(!d)return;
        var strip=d.closest('.int-strip');set=Array.prototype.map.call(strip.querySelectorAll('img'),function(x){{return x}});
        show(Array.prototype.indexOf.call(strip.children,d));
        lb.classList.add('on');document.body.style.overflow='hidden';
      }});
      document.addEventListener('click',function(e){{
        var b=e.target.closest('.int-nav');if(!b)return;
        var st=b.parentElement.querySelector('.int-strip');
        var w=st.children[0].offsetWidth+8;
        st.scrollBy({{left:(b.classList.contains('inext')?1:-1)*w*2,behavior:'smooth'}});
      }});
      function updInt(st){{
        var wr=st.parentElement,pv=wr.querySelector('.iprev'),nx=wr.querySelector('.inext');
        if(!pv)return;
        pv.classList.toggle('off',st.scrollLeft<8);
        nx.classList.toggle('off',st.scrollLeft>st.scrollWidth-st.clientWidth-8);
      }}
      Array.prototype.forEach.call(document.querySelectorAll('.int-strip'),function(st){{
        st.addEventListener('scroll',function(){{requestAnimationFrame(function(){{updInt(st)}})}});updInt(st);
      }});
    }}
  }})();
  </script>
</div></section>"""

ICONS = {
 "price": '<circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 18V6"/>',
 "plane": '<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>',
 "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
 "building": '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/>',
 "receipt": '<path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z"/><path d="M14 8H8"/><path d="M16 12H8"/><path d="M13 16H8"/>',
 "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
 "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
 "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
}

def feat(icon, tone, title, text):
    return f"""<div class="feat-card"><div class="feat-ic {tone}"><svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</svg></div><div><h3>{title}</h3><p>{text}</p></div></div>"""

def why_section():
    return f"""
<section style="padding-top:0"><div class="wrap">
  <div class="sec-head center">
    <span class="pill pill-orange">Why Koast</span>
    <h2>Everything rideshare isn't.</h2>
  </div>
  <div class="grid-2">
    {feat("price","o","Fixed, upfront pricing","Your quote is your final price. No surge, no hidden fees, itemized receipts.")}
    {feat("plane","t","Flight tracking built in","We watch your flight and adjust automatically — 30 min free wait domestic, 1 hr international.")}
    {feat("shield","o","Vetted professional chauffeurs","Commercially licensed and insured. Your driver's details sent before every trip.")}
    {feat("building","t","Corporate accounts","Account-based billing, passenger lists, and team ride coordination for businesses.")}
  </div>
</div></section>"""

def routes_table(routes, h1="Popular route", h2="Typical time"):
    rows = "\n".join(f'<tr><td>{r}</td><td>{t}</td><td><a href="{BOOK}">Get quote →</a></td></tr>' for r,t in routes)
    return f'<table class="routes"><tr><th>{h1}</th><th>{h2}</th><th></th></tr>{rows}</table>'

def faq_section(items, title="Common questions"):
    blocks = "\n".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in items)
    return f"""
<section style="padding-top:0"><div class="wrap">
  <div class="sec-head center"><span class="pill">FAQ</span><h2>{title}</h2></div>
  <div class="faq">{blocks}</div>
</div></section>"""

def cta_section(h="Ride easy.", p=None):
    p = p or f"Get an instant quote now — or email us at {EMAIL}."
    return f"""
<section style="padding-top:0"><div class="wrap"><div class="cta">
  <h2>{h}</h2><p>{p}</p>
  <a class="btn btn-orange btn-lg" href="{BOOK}">Get an Instant Quote</a>
</div></div></section>"""

def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    with open(full, "w") as f: f.write(html)
    print("wrote", path)

TESTIMONIALS = [
 ("Our executives fly into SFO every month and Koast hasn't missed a pickup yet. Flight delayed two hours — the driver was simply there when they landed.","Sarah M.","Corporate Travel Manager · enterprise software company, SF"),
 ("I coordinate ground travel for three executives across two time zones. One dashboard, driver details before every pickup, one invoice at month end.","Danielle R.","Executive Assistant · global investment firm, New York"),
 ("Booked the Sprinter for a client offsite to Napa — fourteen people, four wineries, zero logistics on my plate. Clients still bring it up.","Marcus T.","Account Director · marketing agency, SF"),
 ("Every candidate we fly in gets a Koast pickup now. It sets the tone before they ever reach the office, and the booking takes my team ninety seconds.","Priya K.","Head of People · biotech company, South San Francisco"),
 ("My calendar moves constantly. The hourly charter just absorbs it — driver waits, route adjusts, and I've never once thought about parking on Sand Hill.","James W.","Partner · venture capital firm, Menlo Park"),
 ("We moved 120 conference guests between venues over three days. Koast ran it like a transit system — buses on time, every time.","Elena V.","Event Producer · hospitality group, Las Vegas"),
 ("O'Hare in winter is chaos. Koast is the only car service that's never left me refreshing an app at the curb at midnight.","Robert C.","CFO · manufacturing company, Chicago"),
 ("Discretion matters in our work. Professional drivers, immaculate cars, no small talk unless you want it. Exactly right.","Aisha B.","Director of Operations · law firm, Washington D.C."),
 ("Three-city roadshow weeks used to mean coordinating three car services. Now it's one account and the same standard in every city.","Tom H.","VP of Sales · medical devices company, Boston"),
 ("The party bus made the wedding weekend. Thirty guests between hotel, vineyard, and reception — nobody stranded, nobody driving.","Nicole F.","Wedding planner, Napa Valley"),
 ("I take 4:30 AM airport runs twice a month. The car is confirmed the night before and waiting when I walk out. That peace of mind is the product.","David L.","Management consultant, Seattle"),
 ("My CEO notices everything. After six months of Koast, the only feedback I've gotten is 'keep using them' — which is the highest praise that exists.","Grace P.","Executive Assistant to CEO · consumer brand, Los Angeles"),
]

def testi_section():
    cards = ""
    for q, name, role in TESTIMONIALS:
        cards += f"""
    <div class="card">
      <div style="color:var(--orange);letter-spacing:3px;margin-bottom:14px">★★★★★</div>
      <p style="font-size:14.5px;color:var(--muted);font-style:italic;margin-bottom:18px">"{q}"</p>
      <div style="font-weight:700;font-size:14px">{name}<span style="display:block;color:var(--teal-dark);font-weight:600;font-size:12.5px">{role}</span></div>
    </div>"""
    return f"""
<section id="reviews" style="padding-top:0"><div class="wrap">
  <div class="sec-head">
    <span class="pill">Riders Say</span>
    <h2>Trusted by people who travel for a living.</h2>
  </div>
  <div class="car-wrap">
    <button class="car-arrow prev" data-dir="-1" aria-label="Previous testimonials">←</button>
    <div class="car-track">{cards}
    </div>
    <button class="car-arrow next" data-dir="1" aria-label="Next testimonials">→</button>
  </div>
  <div class="car-dots tdots"></div>
  <script>
  (function(){{
    var s=document.currentScript.closest('section'),t=s.querySelector('.car-track'),d=s.querySelector('.car-dots');
    var orig=t.children.length,K=2;
    var w=function(){{return t.children[0].offsetWidth+22}};
    var kids=[].slice.call(t.children);
    for(var i=0;i<K;i++) t.appendChild(kids[i].cloneNode(true));
    for(var j=orig-1;j>=orig-K;j--) t.insertBefore(kids[j].cloneNode(true),t.firstChild);
    requestAnimationFrame(function(){{t.scrollLeft=K*w()}});
    for(var i=0;i<orig;i++)(function(i){{var b=document.createElement('button');b.setAttribute('aria-label','Review '+(i+1));b.onclick=function(){{t.scrollTo({{left:(i+K)*w(),behavior:'smooth'}})}};d.appendChild(b)}})(i);
    function wrap(){{
      var W=w();
      if(t.scrollLeft < (K-1)*W) t.scrollLeft += orig*W;
      else if(t.scrollLeft > (K+orig-1)*W) t.scrollLeft -= orig*W;
      var i=Math.round(t.scrollLeft/W)-K;
      i=((i%orig)+orig)%orig;
      Array.prototype.forEach.call(d.children,function(b,j){{b.classList.toggle('on',j===i)}});
    }}
    t.addEventListener('scroll',function(){{requestAnimationFrame(wrap)}});
    var pv=s.querySelector('.car-arrow.prev'),nx=s.querySelector('.car-arrow.next');
    [pv,nx].forEach(function(b){{if(b)b.onclick=function(){{t.scrollBy({{left:parseInt(b.dataset.dir)*w(),behavior:'smooth'}})}}}});
    wrap();
  }})();
  </script>
</div></section>"""

SERVICE_AREAS = [
 ("San Francisco","cities/san-francisco.html","blog-banner-sf.jpg"),
 ("New York City","cities/new-york.html","blog-banner-nyc.jpg"),
 ("Los Angeles","cities/los-angeles.html","blog-banner-la.jpg"),
 ("Chicago","cities/chicago.html","blog-banner-chicago.jpg"),
 ("Miami","cities/miami.html","blog-banner-miami.jpg"),
 ("Las Vegas","cities/las-vegas.html","blog-banner-vegas.jpg"),
 ("Denver","cities/denver.html","blog-banner-denver.jpg"),
 ("Wine Country","services/wine-tours.html","blog-banner-napa.jpg"),
 ("San Jose","cities/san-jose.html","city-san-jose.jpg"),
 ("Oakland","cities/oakland.html","city-oakland.jpg"),
 ("Palo Alto","cities/palo-alto.html","city-palo-alto.jpg"),
 ("Seattle","cities/seattle.html","city-seattle.jpg"),
 ("Boston","cities/boston.html","city-boston.jpg"),
 ("Washington, D.C.","cities/washington-dc.html","city-washington-dc.jpg"),
 ("Dallas","cities/dallas.html","city-dallas.jpg"),
 ("Houston","cities/houston.html","city-houston.jpg"),
 ("Austin","cities/austin.html","city-austin.jpg"),
 ("Atlanta","cities/atlanta.html","city-atlanta.jpg"),
 ("San Diego","cities/san-diego.html","city-san-diego.jpg"),
 ("Philadelphia","cities/philadelphia.html","city-philadelphia.jpg"),
 ("Phoenix","cities/phoenix.html","city-phoenix.jpg"),
 ("Charlotte","cities/charlotte.html","city-charlotte.jpg"),
 ("Nashville","cities/nashville.html","city-nashville.jpg"),
 ("Minneapolis","cities/minneapolis.html","city-minneapolis.jpg"),
 ("Orlando","cities/orlando.html","city-orlando.jpg"),
 ("Portland","cities/portland.html","city-portland.jpg"),
 ("Sacramento","cities/sacramento.html","city-sacramento.jpg"),
 ("New Orleans","cities/new-orleans.html","city-new-orleans.jpg"),
 ("Tampa","cities/tampa.html","city-tampa.jpg"),
 ("Detroit","cities/detroit.html","city-detroit.jpg"),
 ("Salt Lake City","cities/salt-lake-city.html","city-salt-lake-city.jpg"),
 ("San Antonio","cities/san-antonio.html","city-san-antonio.jpg"),
 ("Raleigh","cities/raleigh.html","city-raleigh.jpg"),
]

def service_areas_section(prefix=""):
    cards = ""
    for name, href, img in SERVICE_AREAS:
        cards += f"""
    <a class="area-card" href="{prefix}{href}" style="background-image:linear-gradient(rgba(10,12,15,.38),rgba(10,12,15,.5)),url('{prefix}img/{img}')">
      <span>{name}</span>
    </a>"""
    return f"""
<section class="tight" id="areas"><div class="wrap">
  <div class="sec-head center"><h2>Browse by Service Areas</h2></div>
  <div class="car-wrap">
    <button class="car-arrow prev" data-dir="-1" aria-label="Previous areas">←</button>
    <div class="car-track area-track">{cards}
    </div>
    <button class="car-arrow next" data-dir="1" aria-label="Next areas">→</button>
  </div>
  <div class="swipe-hint show-m"><span>←</span><span>→</span></div>
  <div class="center" style="margin-top:28px"><a class="btn btn-line" href="{prefix}cities/index.html">View All Service Areas</a></div>
  <script>
  (function(){{
    var s=document.currentScript.closest('section'),t=s.querySelector('.car-track');
    var orig=t.children.length,K=3;
    var w=function(){{return t.children[0].offsetWidth+22}};
    // clone for infinite loop
    var kids=[].slice.call(t.children);
    for(var i=0;i<K;i++) t.appendChild(kids[i].cloneNode(true));
    for(var j=orig-1;j>=orig-K;j--) t.insertBefore(kids[j].cloneNode(true),t.firstChild);
    requestAnimationFrame(function(){{t.scrollLeft=K*w()}});
    function wrap(){{
      var W=w();
      if(t.scrollLeft < (K-1)*W) t.scrollLeft += orig*W;
      else if(t.scrollLeft > (K+orig-1)*W) t.scrollLeft -= orig*W;
    }}
    t.addEventListener('scroll',function(){{requestAnimationFrame(wrap)}});
    var pv=s.querySelector('.car-arrow.prev'),nx=s.querySelector('.car-arrow.next');
    [pv,nx].forEach(function(b){{if(b)b.onclick=function(){{t.scrollBy({{left:parseInt(b.dataset.dir)*w(),behavior:'smooth'}})}}}});
    var hint=s.querySelector('.swipe-hint');
    if(hint){{var hs=hint.querySelectorAll('span');
      if(hs[0])hs[0].onclick=function(){{t.scrollBy({{left:-w(),behavior:'smooth'}})}};
      if(hs[1])hs[1].onclick=function(){{t.scrollBy({{left:w(),behavior:'smooth'}})}};
    }}
  }})();
  </script>
</div></section>"""

SERVICES_CAROUSEL = [
 ("Airport Transfers","Flight-tracked pickups, SFO to JFK","services/airport-transfers.html","blog-banner-sfo.jpg"),
 ("Corporate Travel","One account, every city","services/corporate-travel.html","blog-banner-corporate.jpg"),
 ("Wine Tours","Napa, Sonoma & beyond","services/wine-tours.html","blog-banner-napa.jpg"),
 ("Care Rides","Senior & medical appointments","services/care-rides.html","svc-care.jpg"),
 ("Events & Weddings","Sprinters & party buses","https://customer.moovs.app/koast/request/new","svc-weddings.jpg"),
 ("Hourly Charter","Your chauffeur, your schedule","https://customer.moovs.app/koast/request/new","svc-hourly.jpg"),
]

if not CARE_RIDES_LIVE:
    SERVICES_CAROUSEL = [e for e in SERVICES_CAROUSEL if "care-rides" not in e[2]]

def services_section(prefix=""):
    cards = ""
    import os as _sos
    for name, sub, href, img in SERVICES_CAROUSEL:
        url = href if href.startswith("http") else prefix + href
        if not _sos.path.exists(os.path.join(ROOT, "img", img)):
            img = "fleet-first-class-suv.jpg"
        cards += f"""
    <a class="svc-card" href="{url}" style="background-image:linear-gradient(180deg,rgba(10,12,15,.04) 32%,rgba(10,12,15,.82)),url('{prefix}img/{img}')">
      <div class="svc-meta"><strong>{name}</strong><span>{sub}</span></div>
    </a>"""
    return f"""
<section class="tight" id="services"><div class="wrap">
  <div class="sec-head center"><h2>Our Services</h2></div>
  <div class="car-wrap">
    <button class="car-arrow prev" data-dir="-1" aria-label="Previous services">←</button>
    <div class="car-track svc-track">{cards}
    </div>
    <button class="car-arrow next" data-dir="1" aria-label="Next services">→</button>
  </div>
  <div class="swipe-hint show-m"><span>←</span><span>→</span></div>
  <script>
  (function(){{
    var s=document.currentScript.closest('section'),t=s.querySelector('.car-track');
    var orig=t.children.length,K=3;
    var w=function(){{return t.children[0].offsetWidth+22}};
    // clone for infinite loop
    var kids=[].slice.call(t.children);
    for(var i=0;i<K;i++) t.appendChild(kids[i].cloneNode(true));
    for(var j=orig-1;j>=orig-K;j--) t.insertBefore(kids[j].cloneNode(true),t.firstChild);
    requestAnimationFrame(function(){{t.scrollLeft=K*w()}});
    function wrap(){{
      var W=w();
      if(t.scrollLeft < (K-1)*W) t.scrollLeft += orig*W;
      else if(t.scrollLeft > (K+orig-1)*W) t.scrollLeft -= orig*W;
    }}
    t.addEventListener('scroll',function(){{requestAnimationFrame(wrap)}});
    var pv=s.querySelector('.car-arrow.prev'),nx=s.querySelector('.car-arrow.next');
    [pv,nx].forEach(function(b){{if(b)b.onclick=function(){{t.scrollBy({{left:parseInt(b.dataset.dir)*w(),behavior:'smooth'}})}}}});
    var hint=s.querySelector('.swipe-hint');
    if(hint){{var hs=hint.querySelectorAll('span');
      if(hs[0])hs[0].onclick=function(){{t.scrollBy({{left:-w(),behavior:'smooth'}})}};
      if(hs[1])hs[1].onclick=function(){{t.scrollBy({{left:w(),behavior:'smooth'}})}};
    }}
  }})();
  </script>
</div></section>"""

# ============================ HOMEPAGE ============================
home = head("Koast — Professional Black Car & Chauffeur Service | Nationwide",
            "Flat-rate chauffeured black car service nationwide. Airport transfers, corporate travel, wine tours & events. Vetted drivers, no surge pricing, 24/7.",
            extra='\n<link rel="preload" as="image" href="img/hero-mobile.webp" media="(max-width:900px)">\n<link rel="preload" as="image" href="img/hero-desktop.webp" media="(min-width:901px)">')
home += nav("")
home += f"""
<header class="hero hero-split hero-photo"><div class="wrap hero-grid">
  <div class="hero-copy">
    <h1>Ride <span class="o">easy.</span></h1>
    <p class="lede hide-m">Flat-rate chauffeured black car service — instant quotes, vetted professional drivers, flight tracking included. 24/7.</p>
    <p class="lede show-m">Flat-rate black car service — no surge, 24/7, nationwide.</p>
    <ul class="check check-o hide-m" style="margin-bottom:0">
      <li>Fixed all-inclusive pricing — never surge</li>
      <li>Flight tracking &amp; free airport wait time</li>
      <li>Vetted, commercially licensed chauffeurs</li>
    </ul>
  </div>
  {book_card()}
</div></header>"""
home += fleet_section()
home += why_section()
home += """
<section style="padding:0"><div class="count-band"><div class="wrap">
  <div class="count-row" id="kstats">
    <div><strong data-seq="0/0|6/1|12/3|18/5|24/7">0/0</strong><span>Always available</span></div>
    <div><strong class="t"><b data-count="30" data-fmt="int">0</b>+</strong><span>Cities served</span></div>
    <div><strong class="o"><b data-count="3100" data-fmt="comma">0</b>+</strong><span>Chauffeurs nationwide</span></div>
    <div><strong><b data-count="99" data-fmt="int">0</b>%</strong><span>Trips without issue</span></div>
  </div>
  <script>
  (function(){
    var row=document.getElementById('kstats'),done=false;
    function fmt(v,f){return f==='comma'?Math.round(v).toLocaleString():Math.round(v)}
    var rm=window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches;
    function run(){
      if(done)return; done=true;
      row.querySelectorAll('[data-count]').forEach(function(el){
        var to=+el.dataset.count,f=el.dataset.fmt,t0=null;
        if(rm){el.textContent=fmt(to,f);return;}
        function step(t){if(!t0)t0=t;var p=Math.min((t-t0)/1600,1);p=1-Math.pow(1-p,3);el.textContent=fmt(to*p,f);if(p<1)requestAnimationFrame(step);}
        requestAnimationFrame(step);
      });
      row.querySelectorAll('[data-seq]').forEach(function(el){
        var parts=el.dataset.seq.split('|');
        if(rm){el.textContent=parts[parts.length-1];return;}
        parts.forEach(function(s,i){setTimeout(function(){el.textContent=s},i*320)});
      });
    }
    if('IntersectionObserver' in window){
      new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)run()})},{threshold:.4}).observe(row);
    } else { run(); }
  })();
  </script>
</div></div></section>"""
home += service_areas_section()
home += f"""
<section style="padding-top:0"><div class="wrap"><div class="steps">
  <h2>Booked in under a minute.</h2>
  <p>No account. No app download. No phone tag.</p>
  <div class="grid-3">
    <div class="step"><div class="num">STEP 01</div><h3>Enter your trip</h3><p>Pickup, drop-off, date and time. Get an instant all-inclusive price.</p></div>
    <div class="step"><div class="num">STEP 02</div><h3>Confirm your ride</h3><p>Choose your vehicle class and pay securely. Change plans anytime.</p></div>
    <div class="step"><div class="num">STEP 03</div><h3>Meet your chauffeur</h3><p>Get driver details, live GPS tracking, and text updates before pickup.</p></div>
  </div>
</div></div></section>"""
home += testi_section()
home += services_section()
home += faq_section([
  ("How is Koast different from Uber or Lyft?",
   "Koast is a professional black car and chauffeur service — not a rideshare app. Every driver is a vetted, commercially licensed, and insured chauffeur. You get a fixed price upfront, a luxury vehicle, and a professional who tracks your flight and handles your luggage."),
  ("What areas does Koast serve?",
   "Koast is headquartered in the San Francisco Bay Area and serves major cities nationwide — including New York, Los Angeles, Chicago, Miami, Las Vegas, Dallas, Boston, Seattle, and more — through our vetted professional network."),
  ("Is Koast available for corporate and business travel?",
   "Yes. We offer account-based billing, ride coordination for teams, and consistent professional service for airport transfers, client pickups, and offsite meetings."),
  ("Is Koast available 24/7?",
   "Yes. Early morning airport transfers, late-night event pickups, holidays — we operate around the clock, every day."),
])
home += cta_section()
home += footer("")
write("index.html", home)

# ============================ INTERNAL LINKS: "PLAN YOUR TRIP" ============================
GUIDE_TITLE = {
 "san-francisco-summer-2026-events":"SF Summer 2026 Events",
 "sfo-to-san-francisco-black-car-guide":"SFO Black Car Guide",
 "nyc-events-calendar":"NYC Events Calendar",
 "nyc-ground-travel-guide":"Getting Around New York",
 "chicago-summer-festivals":"Chicago Festival Summer",
 "chicago-ohare-midway-guide":"O'Hare or Midway?",
 "miami-art-week":"Miami Art Week",
 "miami-getting-around":"Getting Around Miami",
 "nashville-music-calendar":"Nashville Music Calendar",
 "houston-rodeo-guide":"Houston Rodeo Guide",
 "seattle-events-guide":"Seattle Event Season",
 "seattle-getting-around":"Getting Around Seattle",
 "austin-festival-season":"Austin Festival Season",
 "vegas-convention-transportation":"Vegas Convention Playbook",
 "boston-logan-guide":"Logan Airport Done Right",
 "dc-airport-decision":"DCA, IAD or BWI?",
 "denver-mountain-transfers":"Denver Mountain Transfers",
 "lax-airport-black-car-guide":"LAX Pickup Guide",
 "black-car-vs-rideshare-cost":"Black Car vs. Rideshare Costs",
 "choosing-corporate-car-service":"Choosing a Corporate Car Service",
 "napa-sonoma-chauffeur-day-trip":"Napa &amp; Sonoma Day Trip",
 "sonoma-first-timers":"A First-Timer's Sonoma",
 "temecula-balloons-tastings":"Temecula Balloons &amp; Tastings",
 "willamette-pinot-weekend":"Willamette Pinot Weekend",
 "group-wine-tour-planning":"Group Wine Tour Planning",
 "jfk-black-car-guide":"JFK Black Car Guide",
 "atlanta-airport-black-car-guide":"ATL Black Car Guide",
 "dfw-black-car-guide":"DFW Black Car Guide",
 "miami-airport-black-car-guide":"MIA Black Car Guide",
 "investor-roadshow-ground-travel":"Investor Roadshow Playbook",
 "group-airport-transfers":"Group Airport Transfers",
}
DEFAULT_GUIDES = ["black-car-vs-rideshare-cost","choosing-corporate-car-service"]
CITY_GUIDES = {
 "san-francisco":["san-francisco-summer-2026-events","sfo-to-san-francisco-black-car-guide"],
 "new-york":["nyc-events-calendar","nyc-ground-travel-guide","jfk-black-car-guide"],
 "chicago":["chicago-summer-festivals","chicago-ohare-midway-guide"],
 "miami":["miami-art-week","miami-getting-around","miami-airport-black-car-guide"],
 "atlanta":["atlanta-airport-black-car-guide"],
 "dallas":["dfw-black-car-guide"],
 "nashville":["nashville-music-calendar"],
 "houston":["houston-rodeo-guide"],
 "seattle":["seattle-events-guide","seattle-getting-around"],
 "austin":["austin-festival-season"],
 "las-vegas":["vegas-convention-transportation"],
 "boston":["boston-logan-guide"],
 "washington-dc":["dc-airport-decision"],
 "denver":["denver-mountain-transfers"],
 "los-angeles":["lax-airport-black-car-guide"],
}
CITY_AP = {
 "san-francisco":["sfo","oak","sjc"], "san-jose":["sjc","sfo","oak"], "oakland":["oak","sfo","sjc"],
 "palo-alto":["sfo","sjc","oak"], "new-york":["jfk","lga","ewr"], "los-angeles":["lax"],
 "chicago":["ord","mdw"], "miami":["mia"], "las-vegas":["las"], "dallas":["dfw","dal"],
 "houston":["iah","hou"], "atlanta":["atl"], "boston":["bos"], "washington-dc":["iad","dca"],
 "san-diego":["san"], "austin":["aus"], "nashville":["bna"], "denver":["den"], "phoenix":["phx"],
 "philadelphia":["phl"], "orlando":["mco"], "charlotte":["clt"], "minneapolis":["msp"],
}
CITY_WINE = {
 "san-francisco":["napa-valley","sonoma","healdsburg","livermore"],
 "oakland":["napa-valley","sonoma","livermore"], "san-jose":["livermore","santa-ynez"],
 "palo-alto":["napa-valley","livermore"], "sacramento":["napa-valley","livermore"],
 "los-angeles":["santa-ynez","temecula","paso-robles"], "san-diego":["temecula"],
 "portland":["willamette-valley"], "seattle":["walla-walla"],
 "austin":["texas-hill-country"], "san-antonio":["texas-hill-country"],
 "washington-dc":["virginia"], "new-york":["finger-lakes"],
}
AP_GUIDES = {
 "sfo":["sfo-to-san-francisco-black-car-guide"], "bos":["boston-logan-guide"],
 "ord":["chicago-ohare-midway-guide"], "mdw":["chicago-ohare-midway-guide"],
 "lax":["lax-airport-black-car-guide"], "iad":["dc-airport-decision"], "dca":["dc-airport-decision"],
 "jfk":["jfk-black-car-guide","nyc-ground-travel-guide"], "lga":["nyc-ground-travel-guide","jfk-black-car-guide"], "ewr":["nyc-ground-travel-guide","jfk-black-car-guide"],
 "mia":["miami-airport-black-car-guide","miami-getting-around"], "las":["vegas-convention-transportation"],
 "den":["denver-mountain-transfers"], "aus":["austin-festival-season"],
 "iah":["houston-rodeo-guide"], "hou":["houston-rodeo-guide"], "bna":["nashville-music-calendar"],
 "atl":["atlanta-airport-black-car-guide"], "dfw":["dfw-black-car-guide"], "dal":["dfw-black-car-guide"],
}
AP_CITY = {ap: city for city, aps in CITY_AP.items() for ap in aps}
WINE_CITY = {
 "napa-valley":["san-francisco","sacramento"], "sonoma":["san-francisco"],
 "healdsburg":["san-francisco"], "livermore":["san-francisco","san-jose"],
 "paso-robles":["los-angeles","san-francisco"], "santa-ynez":["los-angeles"],
 "temecula":["san-diego","los-angeles"], "willamette-valley":["portland"],
 "walla-walla":["seattle"], "finger-lakes":["new-york"],
 "texas-hill-country":["austin","san-antonio"], "virginia":["washington-dc"],
}
WINE_BLOGS = {
 "napa-valley":["napa-sonoma-chauffeur-day-trip"], "sonoma":["sonoma-first-timers","napa-sonoma-chauffeur-day-trip"],
 "healdsburg":["sonoma-first-timers","napa-sonoma-chauffeur-day-trip"],
 "temecula":["temecula-balloons-tastings"], "willamette-valley":["willamette-pinot-weekend"],
}

def plan_trip(groups, lead=""):
    secs = ""
    for label, chips in groups:
        if not chips: continue
        ch = "".join(f'<a class="chip" href="{href}"><i>{ic}</i> {txt}</a>' for href, txt, ic in chips)
        secs += f'<h6>{label}</h6><div class="chips">{ch}</div>'
    if not secs: return ""
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    return f"""
<section class="tight ptrip"><div class="wrap">
  <span class="pill">Plan your trip</span>
  <h2>Guides &amp; nearby</h2>
  {lead_html}
  {secs}
</div></section>"""

# ============================ CITY PAGES ============================
for slug, c in CITIES.items():
    bay = c["region"] == "bay"
    h = head(f"Black Car Service in {c['name']} | Koast Chauffeur Service",
             f"Professional black car & chauffeur service in {c['name']}. Flat rates, vetted drivers, airport transfers & corporate travel. Book 24/7.", "../")
    h += nav("../", "cities")
    h += f"""
<header class="hero-dark"><div class="wrap">
  <div class="crumbs"><a href="../index.html">Home</a><span>/</span><a href="index.html">Cities</a><span>/</span>{c['name']}</div>
  <div class="hero-grid">
    <div class="hero-copy">
      <h1>Black car service in <span class="o">{c['name']}.</span></h1>
      <p class="lede">{c['blurb']}</p>
      <ul class="check" style="color:#cdd3dc">
        <li>Fixed all-inclusive pricing — never surge</li>
        <li>Airport transfers — {c['airports']}</li>
        <li>Available 24/7, booked in under a minute</li>
      </ul>
    </div>
    {book_card()}
  </div>
</div></header>
<section class="tight"><div class="wrap grid-2" style="align-items:center;gap:60px">
  <div>
    <span class="pill">Local Coverage</span>
    <h2 style="font-size:32px;margin:14px 0 16px">Anywhere in {c['name']}, anytime</h2>
    <p style="color:var(--muted);margin-bottom:20px">We cover {c['hoods']} — plus every hotel, office, hospital, and venue in between.</p>
    <ul class="check">
      <li>Airport transfers — {c['airports']}</li>
      <li>Corporate &amp; executive travel</li>
      <li>Events, weddings &amp; nights out</li>
      <li>Hourly charters with a dedicated chauffeur</li>
    </ul>
  </div>
  <div>
    <h3 style="margin-bottom:16px">Popular {c['short']} routes</h3>
    {routes_table(c['routes'])}
  </div>
</div></section>"""
    h += fleet_section("../")
    h += faq_section([
      (f"How much does a black car cost in {c['name']}?",
       "Pricing is flat-rate and depends on your pickup and drop-off. Enter your trip at the top of this page for an instant all-inclusive quote — no surge, no hidden fees."),
      c['faq_extra'],
      ("How far in advance should I book?",
       "Most riders book a few hours to a few days ahead. Same-day rides are often available, but for early-morning airport runs or event dates we recommend booking 24+ hours out."),
    ], f"{c['name']} questions")
    h += plan_trip([
      ("Guides", [(f"../blog/{g}.html", GUIDE_TITLE[g], "✦") for g in CITY_GUIDES.get(slug, DEFAULT_GUIDES)]),
      ("Airports we serve", [(f"../airports/{ap}.html", f"{AIRPORTS[ap]['code']} · {AIRPORTS[ap]['name']}", "→") for ap in CITY_AP.get(slug, [])]),
      ("Wine country day trips", [(f"../wine-tours/{w}.html", WINE_REGIONS[w]["name"], "→") for w in CITY_WINE.get(slug, [])]),
    ], f"Everything Koast serves around {c['name']} — airport rides, day trips, and what's on this season.")
    h += cta_section(f"Ride easy in {c['name']}.")
    h += footer("../")
    write(f"cities/{slug}.html", h)

# ============================ CITY / AIRPORT IMAGES ============================
CITY_IMG = {
 "san-francisco":"blog-banner-sf.jpg","san-jose":"city-san-jose.jpg","oakland":"city-oakland.jpg",
 "palo-alto":"city-palo-alto.jpg","new-york":"blog-banner-nyc.jpg","los-angeles":"blog-banner-la.jpg",
 "chicago":"blog-banner-chicago.jpg","miami":"blog-banner-miami.jpg","las-vegas":"blog-banner-vegas.jpg",
 "denver":"blog-banner-denver.jpg","dallas":"city-dallas.jpg","houston":"city-houston.jpg",
 "atlanta":"city-atlanta.jpg","boston":"city-boston.jpg","seattle":"city-seattle.jpg",
 "washington-dc":"city-washington-dc.jpg","san-diego":"city-san-diego.jpg","austin":"city-austin.jpg",
 "nashville":"city-nashville.jpg","phoenix":"city-phoenix.jpg","philadelphia":"city-philadelphia.jpg",
 "orlando":"city-orlando.jpg","charlotte":"city-charlotte.jpg","minneapolis":"city-minneapolis.jpg",
 "portland":"city-portland.jpg","sacramento":"city-sacramento.jpg","new-orleans":"city-new-orleans.jpg",
 "tampa":"city-tampa.jpg","detroit":"city-detroit.jpg","salt-lake-city":"city-salt-lake-city.jpg",
 "san-antonio":"city-san-antonio.jpg","raleigh":"city-raleigh.jpg",
}
AP_IMG = {
 "sfo":"blog-banner-sfo.jpg","oak":"city-oakland.jpg","sjc":"city-san-jose.jpg",
 "jfk":"blog-banner-nyc.jpg","lga":"ap-lga.jpg","ewr":"ap-ewr.jpg",
 "lax":"blog-banner-la.jpg","ord":"blog-banner-chicago.jpg","mdw":"ap-mdw.jpg",
 "mia":"blog-banner-miami.jpg","las":"blog-banner-vegas.jpg","den":"blog-banner-denver.jpg",
 "dfw":"city-dallas.jpg","dal":"ap-dal.jpg","iah":"city-houston.jpg","hou":"ap-hou.jpg",
 "aus":"city-austin.jpg","atl":"city-atlanta.jpg","bos":"city-boston.jpg",
 "iad":"city-washington-dc.jpg","dca":"ap-dca.jpg","san":"city-san-diego.jpg",
 "phl":"city-philadelphia.jpg","phx":"city-phoenix.jpg","clt":"city-charlotte.jpg",
 "bna":"city-nashville.jpg","msp":"city-minneapolis.jpg","mco":"city-orlando.jpg",
}

# ============================ CITIES INDEX ============================
def city_cards(region):
    out = ""
    for slug, c in CITIES.items():
        if c["region"] != region: continue
        img = CITY_IMG.get(slug, "hero-banner.jpg")
        out += f"""<a class="card city-card" href="{slug}.html">
        <div class="card-img"><img src="../img/{img}" alt="{c['name']} chauffeur service" loading="lazy"></div>
        <h3>{c['name']}</h3>
        <div class="sub">{c['blurb'][:95]}…</div>
        <div class="row"><span>{c['airports'].split('(')[0].strip()}</span><span style="color:var(--orange);font-weight:700">View →</span></div></a>"""
    return out

ci = head("Cities We Serve | Koast Black Car Service Nationwide",
          "Koast professional chauffeur service — San Francisco Bay Area home base, serving New York, LA, Chicago, Miami & major cities nationwide.", "../")
ci += nav("../", "cities")
ci += f"""
<header class="hero-dark"><div class="wrap">
  <div class="crumbs"><a href="../index.html">Home</a><span>/</span>Cities</div>
  <h1>Where we <span class="o">drive.</span></h1>
  <p class="lede">Bay Area born and headquartered — now serving major cities across the United States.</p>
</div></header>
<section style="padding:40px 0 0"><div class="wrap">
  <div class="ksearch"><input id="csearch" type="search" placeholder="Find your city — try Dallas, Seattle, Miami…" aria-label="Find a city"></div>
</div></section>
<section class="cgrp"><div class="wrap">
  <div class="sec-head"><span class="pill">Home Base</span><h2>San Francisco Bay Area</h2>
  <p>Our headquarters and home fleet — full service, every vehicle class, 24/7.</p></div>
  <div class="grid-2">{city_cards("bay")}</div>
</div></section>
<section style="padding-top:0" class="cgrp"><div class="wrap">
  <div class="sec-head"><span class="pill pill-orange">Nationwide</span><h2>Major cities across the U.S.</h2>
  <p>The same Koast standard — professional chauffeurs, flat rates, flight tracking — in every city we serve.</p></div>
  <div class="grid-2">{city_cards("national")}</div>
</div></section>"""
ci += """
<script>
(function(){
  var i=document.getElementById('csearch');if(!i)return;
  i.addEventListener('input',function(){
    var q=i.value.trim().toLowerCase();
    document.querySelectorAll('.cgrp').forEach(function(sec){
      var v=0;
      sec.querySelectorAll('.city-card').forEach(function(c){
        var h=!q||c.textContent.toLowerCase().indexOf(q)>-1;
        c.style.display=h?'':'none';if(h)v++;
      });
      sec.style.display=v?'':'none';
    });
  });
})();
</script>"""
ci += cta_section()
ci += footer("../")
write("cities/index.html", ci)

# ============================ AIRPORT PAGES ============================
for slug, a in AIRPORTS.items():
    h = head(f"{a['code']} Airport Black Car Service & Transfers | Koast",
             f"Chauffeured airport transfers at {a['name']} ({a['code']}). Flight tracking, free wait time, flat rates. Book 24/7.", "../")
    h += nav("../", "airport")
    h += f"""
<header class="hero-dark"><div class="wrap">
  <div class="crumbs"><a href="../index.html">Home</a><span>/</span><a href="../services/airport-transfers.html">Airports</a><span>/</span>{a['code']}</div>
  <div class="hero-grid">
    <div class="hero-copy">
      <h1>{a['code']} airport transfers, <span class="o">handled.</span></h1>
      <p class="lede">{a['blurb']}</p>
      <ul class="check" style="color:#cdd3dc">
        <li>Live flight tracking — we adjust automatically</li>
        <li>{a['wait']}</li>
        <li>Flight-tracked curbside pickup, timed to your landing</li>
      </ul>
    </div>
    {book_card()}
  </div>
</div></header>
<section class="tight"><div class="wrap grid-2" style="align-items:start;gap:60px">
  <div>
    <span class="pill">How pickup works</span>
    <h2 style="font-size:32px;margin:14px 0 16px">We're there when you land</h2>
    <ul class="check">
      <li>Live flight tracking — delays &amp; early arrivals handled</li>
      <li>Curbside pickup, timed to your landing</li>
      <li>{a['wait']}</li>
      <li>Serving {a['terminals']}</li>
      <li>Luggage handled by your chauffeur</li>
    </ul>
  </div>
  <div>
    <img class="ap-photo" src="../img/{AP_IMG.get(slug,'hero-banner.jpg')}" alt="{a['name']} chauffeur service" loading="lazy">
    <h3 style="margin-bottom:16px">Popular {a['code']} routes</h3>
    {routes_table(a['routes'])}
  </div>
</div></section>"""
    h += fleet_section("../")
    h += faq_section([
      (f"Where does my driver meet me at {a['code']}?",
       "Your chauffeur tracks your flight and is ready when you land, with pickup timed to your actual arrival — you'll receive their name, photo, contact details, and live location before you land."),
      ("What happens if my flight is delayed?",
       f"Nothing you need to do — we track your flight and adjust the pickup automatically. {a['wait']}."),
      ("Are tolls and fees included in the price?",
       "Yes. Your quote is all-inclusive: tolls, airport fees, and standard gratuity are itemized upfront. The price you see is the price you pay."),
    ], f"{a['code']} pickup questions")
    _city = AP_CITY.get(slug)
    h += plan_trip([
      ("Guides", [(f"../blog/{g}.html", GUIDE_TITLE[g], "✦") for g in AP_GUIDES.get(slug, DEFAULT_GUIDES[:1])]),
      ("City service", [(f"../cities/{_city}.html", f"Black car service in {CITIES[_city]['name']}", "→")] if _city else []),
    ])
    h += cta_section(f"Land at {a['code']}. Leave in minutes.")
    h += footer("../")
    write(f"airports/{slug}.html", h)

# ============================ SERVICE: AIRPORT TRANSFERS ============================
BAY_APS = ("sfo","oak","sjc")
def airport_cards(group):
    out = ""
    for slug, a in AIRPORTS.items():
        if (slug in BAY_APS) != (group == "bay"): continue
        out += f"""<a class="card city-card" href="../airports/{slug}.html">
        <div class="card-img"><img src="../img/{AP_IMG.get(slug,'hero-banner.jpg')}" alt="{a['name']} black car service" loading="lazy"><span class="ap-code">{a['code']}</span></div>
        <h3>{a['name']}</h3>
        <div class="row"><span>Flight tracking &amp; free wait</span><span style="color:var(--orange);font-weight:700">View →</span></div></a>"""
    return out


# ============================ AIRPORT ROUTE LANDING PAGES ============================
ROUTES = {
 "sfo-to-san-francisco": {"from":"SFO","navname":"SFO → San Francisco","to":"San Francisco","h1_to":"downtown San Francisco",
   "title":"SFO to San Francisco Car Service | Private Black Car | Koast",
   "desc":"Private chauffeured car service from SFO to downtown San Francisco. Flight-tracked, flat upfront pricing, no surge. Book your airport transfer 24/7.",
   "miles":"about 13 miles","time":"roughly 20–35 minutes","route":"US-101 or I-280","goodfor":"Arrivals, business travel, anyone headed downtown",
   "lede":"The classic run — flight-tracked, flat-rate, and timed to your actual landing so you're moving the moment you clear the terminal.",
   "drive_h":"A short hop where timing is everything",
   "drive":["It's only about 13 miles up US-101 or I-280, but the timing is the whole game. Arrivals stack up, the 101 corridor backs up at rush hour, and the SFO curb is its own kind of chaos. Your chauffeur tracks your flight and is waiting curbside when you land, so all you do is walk to the car.",
     "Into the city we know which approach wins at which hour — 101 toward the Embarcadero and downtown, 280 for the western neighborhoods and SoMa. The price is fixed before you book, with no surge no matter when you touch down."],
   "airport":("../airports/sfo.html","SFO airport transfers","→"),"dest":("../cities/san-francisco.html","San Francisco black car service","→"),
   "faqs":[("How much is a car service from SFO to San Francisco?","You get a flat, all-in price up front when you book — no surge and no meter, whatever time you land. Tell us your destination for an instant quote."),
     ("How long does SFO to downtown San Francisco take?","Usually about 20 to 35 minutes for the roughly 13-mile trip, depending on traffic and the approach. Your chauffeur picks the fastest route for your arrival time."),
     ("What if my flight is delayed?","We track your flight and adjust pickup automatically, early or late. Every arrival includes complimentary wait time, so a delay never costs you the ride."),
     ("Can you pick up late at night or very early?","Yes — we run 24/7. Book a red-eye or a 5 a.m. departure and a flight-tracked chauffeur is there, at the price you were quoted.")]},
 "sfo-to-napa": {"from":"SFO","navname":"SFO → Napa Valley","to":"Napa Valley","h1_to":"Napa Valley",
   "title":"SFO to Napa Valley Car Service | Private Transfer | Koast",
   "desc":"Private chauffeured car service from SFO to Napa Valley. Flight-tracked, flat upfront pricing, no surge. Book your airport-to-wine-country transfer 24/7.",
   "miles":"about 50 miles","time":"roughly 1 to 1.5 hours","route":"US-101 + CA-37, or I-80 + CA-29","goodfor":"Weddings, offsites, wine-country weekends, groups",
   "lede":"Land at SFO and step straight into wine country — one flat rate, your flight tracked, and a chauffeur who knows the valley.",
   "drive_h":"Airport to wine country, handled",
   "drive":["Napa sits about 50 miles north of SFO — roughly an hour to ninety minutes depending on the bridges and the time of day. The route runs up US-101 and across CA-37, or via I-80 and CA-29, and the right call shifts with traffic, weekends, and harvest season.",
     "It's a favorite run for weddings, corporate offsites, and groups flying in for a tasting weekend. We track your flight, hold the car if you're delayed, and you ride straight to your hotel or first winery — luggage handled, nobody navigating, nobody driving."],
   "airport":("../airports/sfo.html","SFO airport transfers","→"),"dest":("../wine-tours/napa-valley.html","Napa Valley wine tours","→"),
   "faqs":[("How much is a car from SFO to Napa?","One flat rate, quoted upfront before you book — no surge, no meter. Group size and vehicle set the price; tell us the details for an instant quote."),
     ("How long is the drive from SFO to Napa Valley?","About 50 miles and roughly an hour to ninety minutes, depending on the bridges and time of day. Weekends and harvest season run longer, and your chauffeur plans for it."),
     ("Can you take a group with luggage?","Yes — a First-Class SUV fits a small group comfortably, and the Executive Sprinter handles larger parties with room for bags and cases."),
     ("Can the same car take us on a wine tour after?","Absolutely. Book hourly and your chauffeur stays with you for the day — airport pickup, then winery to winery, then back — all on one flat hourly rate.")]},
 "sfo-to-sonoma": {"from":"SFO","navname":"SFO → Sonoma","to":"Sonoma","h1_to":"Sonoma",
   "title":"SFO to Sonoma Car Service | Private Wine Country Transfer | Koast",
   "desc":"Private chauffeured car service from SFO to Sonoma. Flight-tracked, flat upfront pricing, no surge. Airport-to-wine-country, booked 24/7.",
   "miles":"about 50 miles","time":"roughly 1 to 1.5 hours","route":"US-101 + CA-37","goodfor":"Wine weekends, weddings, groups",
   "lede":"Land at SFO and ride straight into Sonoma — one flat rate, flight tracked, and a chauffeur who knows the back roads.",
   "drive_h":"Airport to Sonoma, handled",
   "drive":["Sonoma is about 50 miles north of SFO, roughly an hour to ninety minutes up US-101 and across CA-37, depending on the bridge and the time of day. Weekends and harvest season run longer, and your chauffeur plans for it.",
     "It's a favorite for wine weekends, weddings, and groups flying in to taste. We track your flight, hold the car if you're delayed, and you ride straight to your hotel or first winery — luggage handled, nobody driving."],
   "airport":("../airports/sfo.html","SFO airport transfers","→"),"dest":("../wine-tours/sonoma.html","Sonoma wine tours","→"),
   "faqs":[("How much is SFO to Sonoma?","One flat rate quoted upfront — no surge, no meter. Group size and vehicle set the price; tell us the details for a quote."),
     ("How long is the drive from SFO to Sonoma?","About 50 miles and roughly an hour to ninety minutes via US-101 and CA-37, longer on weekends and during harvest."),
     ("Can you take a group with luggage?","Yes — a First-Class SUV for small groups, the Executive Sprinter for larger parties, with room for bags and cases."),
     ("Can the same car stay for a wine tour?","Absolutely. Book hourly and your chauffeur stays for the day, winery to winery, then back — on one flat hourly rate.")]},
 "sfo-to-monterey": {"from":"SFO","navname":"SFO → Monterey & Carmel","to":"Monterey & Carmel","h1_to":"Monterey & Carmel",
   "title":"SFO to Monterey & Carmel Car Service | Private Transfer | Koast",
   "desc":"Private chauffeured car service from SFO to Monterey, Carmel and Pebble Beach. Flight-tracked, flat upfront pricing, no surge. Book 24/7.",
   "miles":"about 110 miles","time":"roughly 2 to 2.5 hours","route":"US-101 south to CA-1","goodfor":"Golf, weddings, Pebble Beach, coastal getaways",
   "lede":"SFO to the Monterey Peninsula — Pebble Beach, Carmel, and the coast — in a flat-rate car with the driving handled.",
   "drive_h":"Down the coast to the Peninsula",
   "drive":["Monterey and Carmel sit about 110 miles south of SFO, generally two to two and a half hours down US-101 and over to CA-1. It's a long enough run that a comfortable car and a chauffeur who knows the route make the difference between arriving relaxed and arriving frazzled.",
     "It's the route for Pebble Beach golf, coastal weddings, and Carmel getaways. We track your flight, load your clubs and bags, and you ride straight to the resort — one fixed price, no surge, no navigating CA-1 after a long flight."],
   "airport":("../airports/sfo.html","SFO airport transfers","→"),"dest":None,
   "faqs":[("How much is SFO to Monterey or Carmel?","A flat rate quoted upfront — no surge, no meter, no matter the distance. Tell us your destination and group for an instant quote."),
     ("How long is the drive from SFO to Monterey?","About 110 miles and roughly two to two and a half hours via US-101 and CA-1, depending on traffic."),
     ("Can you carry golf clubs and luggage?","Yes — an SUV or Sprinter has room for clubs, bags, and a group headed to Pebble Beach or Carmel."),
     ("Can you do the return trip too?","Yes — book the round trip or a scheduled return, flight-tracked, at a price quoted up front.")]},
 "oak-to-san-francisco": {"from":"OAK","navname":"OAK → San Francisco","to":"San Francisco","h1_to":"downtown San Francisco",
   "title":"OAK to San Francisco Car Service | Private Black Car | Koast",
   "desc":"Private chauffeured car service from Oakland Airport (OAK) to San Francisco. Flight-tracked, flat upfront pricing, no surge. Book 24/7.",
   "miles":"about 12 miles","time":"roughly 20–35 minutes","route":"I-80 across the Bay Bridge","goodfor":"Arrivals, business travel, East Bay and SF",
   "lede":"Across the Bay Bridge and into the city — flight-tracked, flat-rate, and timed to your landing at OAK.",
   "drive_h":"Over the Bay Bridge, timed right",
   "drive":["Oakland sits about 12 miles from downtown San Francisco, straight across the Bay Bridge on I-80. It's quick when the bridge is clear and a slog when it isn't — backups and the toll plaza are the whole story, and a chauffeur who runs it daily knows which lane moves.",
     "We track your flight and have a car waiting curbside when you land, so you skip the BART transfer and the rideshare lot. Fixed price quoted before you book, no surge no matter the hour."],
   "airport":("../airports/oak.html","OAK airport transfers","→"),"dest":("../cities/san-francisco.html","San Francisco black car service","→"),
   "faqs":[("How much is a car from OAK to San Francisco?","A flat, all-in price up front — no surge, no meter, whatever time you land. Tell us your destination for an instant quote."),
     ("How long does OAK to San Francisco take?","Usually about 20 to 35 minutes across the Bay Bridge, depending on bridge traffic and the toll plaza. Your chauffeur times the run to your arrival."),
     ("What about Bay Bridge tolls and traffic?","Tolls are included in your flat rate, and your chauffeur plans around the known backup windows. A delayed flight just means we adjust — wait time is complimentary."),
     ("Do you run late at night?","Yes, 24/7. Red-eyes and early departures included, at the price you were quoted.")]},
 "oak-to-napa": {"from":"OAK","navname":"OAK → Napa Valley","to":"Napa Valley","h1_to":"Napa Valley",
   "title":"OAK to Napa Valley Car Service | Private Transfer | Koast",
   "desc":"Private chauffeured car service from Oakland Airport (OAK) to Napa Valley. Flight-tracked, flat pricing, no surge. Airport-to-wine-country, booked 24/7.",
   "miles":"about 45 miles","time":"roughly 1 to 1.25 hours","route":"I-80 to CA-29","goodfor":"Weddings, offsites, wine-country weekends, groups",
   "lede":"From the Oakland curb to your first tasting — one flat rate, flight tracked, and a chauffeur who knows the valley.",
   "drive_h":"East Bay to wine country",
   "drive":["Napa is about 45 miles north of OAK, generally an hour to an hour and a quarter up I-80 and CA-29. Oakland is often the quicker Bay Area gateway to Napa than SFO, with no bridge crossing between you and the vineyards.",
     "It's a popular run for weddings, corporate offsites, and tasting weekends. We track your flight, hold the car if you're delayed, and you ride straight to your hotel or first winery — bags handled, nobody driving."],
   "airport":("../airports/oak.html","OAK airport transfers","→"),"dest":("../wine-tours/napa-valley.html","Napa Valley wine tours","→"),
   "faqs":[("How much is OAK to Napa?","One flat rate quoted upfront — no surge, no meter. Group size and vehicle set the price; tell us the details for a quote."),
     ("How long is the drive from OAK to Napa?","About 45 miles and roughly an hour to an hour and a quarter, depending on traffic. Oakland skips the bridge crossing to wine country, which often makes it the faster Bay gateway."),
     ("Can you take a group with luggage?","Yes — a First-Class SUV fits a small group, and the Executive Sprinter handles larger parties with room for bags and cases."),
     ("Can the same car stay for a wine tour?","Absolutely. Book hourly and your chauffeur stays for the day — airport pickup, winery to winery, then back — on one flat hourly rate.")]},
 "oak-to-sonoma": {"from":"OAK","navname":"OAK → Sonoma","to":"Sonoma","h1_to":"Sonoma",
   "title":"OAK to Sonoma Car Service | Private Wine Country Transfer | Koast",
   "desc":"Private chauffeured car service from Oakland Airport (OAK) to Sonoma. Flight-tracked, flat pricing, no surge. Airport-to-wine-country, booked 24/7.",
   "miles":"about 45 miles","time":"roughly 1 to 1.25 hours","route":"CA-37 to CA-121","goodfor":"Wine weekends, weddings, groups",
   "lede":"Oakland to Sonoma without the bridge — flat-rate, flight-tracked, straight to the tasting room.",
   "drive_h":"A clean run to Sonoma",
   "drive":["Sonoma sits about 45 miles from OAK, roughly an hour to an hour and a quarter via CA-37 and CA-121 along the top of the bay. From Oakland it's an easy, bridge-free run into the southern Sonoma wineries and the town square.",
     "We track your flight and have the car ready when you land, then it's straight to your hotel or first stop. One flat price, quoted up front, with the car available to stay for the day if you want a full tour."],
   "airport":("../airports/oak.html","OAK airport transfers","→"),"dest":("../wine-tours/sonoma.html","Sonoma wine tours","→"),
   "faqs":[("How much is OAK to Sonoma?","A flat rate quoted upfront — no surge, no meter. Tell us your group size and destination for an instant quote."),
     ("How long is OAK to Sonoma?","About 45 miles and roughly an hour to an hour and a quarter via CA-37, with no bridge crossing from Oakland."),
     ("Can the car stay for a wine tour?","Yes — book hourly and your chauffeur drives you winery to winery all day, then back, on one flat hourly rate."),
     ("Can you handle a group?","Yes — SUVs for small groups, the Executive Sprinter for larger parties, with room for luggage and cases.")]},
 "sjc-to-silicon-valley": {"from":"SJC","navname":"SJC → Silicon Valley","to":"Silicon Valley","h1_to":"Silicon Valley",
   "title":"SJC to Silicon Valley Car Service | Palo Alto & Sand Hill | Koast",
   "desc":"Chauffeured car service from San Jose Airport (SJC) to Palo Alto, Mountain View and Sand Hill Road. Flight-tracked, flat pricing, corporate accounts.",
   "miles":"about 10–25 miles","time":"roughly 15–35 minutes","route":"US-101 or I-280","goodfor":"Roadshows, campus visits, investor meetings, exec arrivals",
   "lede":"SJC drops you in the middle of the Valley — flight-tracked transfers to Palo Alto, Mountain View, Cupertino, and Sand Hill Road.",
   "drive_h":"You're already in the Valley",
   "drive":["San Jose is the heart of Silicon Valley, so SJC is the closest gateway to most of it — Palo Alto and Mountain View around 15 to 25 miles up US-101 or I-280, Cupertino and the southern campuses even closer. Most transfers run 15 to 35 minutes outside of peak.",
     "It's the practical choice for roadshows, campus visits, and investor meetings. Fixed pricing, account billing, and a flight-tracked pickup so a delayed arrival doesn't derail the schedule."],
   "airport":("../airports/sjc.html","SJC airport transfers","→"),"dest":("../cities/palo-alto.html","Palo Alto car service","→"),
   "faqs":[("How much is SJC to Palo Alto or Mountain View?","A flat, upfront price set by destination and vehicle — no surge. Corporate accounts and itemized receipts available. Get an instant quote."),
     ("How long is the drive?","Palo Alto and Mountain View are about 15 to 35 minutes from SJC; closer campuses are quicker. Your chauffeur routes around the 101 crunch."),
     ("Do you handle corporate travel?","Yes — account billing, passenger lists, and multi-stop days for teams, roadshows, and investor visits."),
     ("Can you do multiple stops?","Book hourly and the car stays with you across campuses, Sand Hill Road, and meetings — one chauffeur, one flat hourly rate.")]},
 "sjc-to-san-francisco": {"from":"SJC","navname":"SJC → San Francisco","to":"San Francisco","h1_to":"downtown San Francisco",
   "title":"SJC to San Francisco Car Service | Private Black Car | Koast",
   "desc":"Private chauffeured car service from San Jose Airport (SJC) to San Francisco. Flight-tracked, flat upfront pricing, no surge. Book 24/7.",
   "miles":"about 45 miles","time":"roughly 45–70 minutes","route":"US-101 or I-280 north","goodfor":"Arrivals, business travel, Peninsula and SF",
   "lede":"Up the Peninsula to the city — flat-rate, flight-tracked, straight from the SJC curb.",
   "drive_h":"Up the Peninsula, planned around the 101",
   "drive":["San Francisco is about 45 miles north of SJC, generally 45 to 70 minutes up US-101 or I-280 depending on the hour. The 101 corridor is famously slow at peak, and a driver who runs the Peninsula daily knows when 280 is the smarter line.",
     "We track your flight and have a car waiting when you land, with stops on the Peninsula easy to add. One fixed price, quoted before you book, with complimentary wait time on every arrival."],
   "airport":("../airports/sjc.html","SJC airport transfers","→"),"dest":("../cities/san-francisco.html","San Francisco black car service","→"),
   "faqs":[("How much is SJC to San Francisco?","A flat, all-in price up front — no surge, no meter. Tell us your destination for an instant quote."),
     ("How long does SJC to San Francisco take?","Usually 45 to 70 minutes for the roughly 45-mile trip, depending on 101 traffic and the time of day."),
     ("Can you add a Peninsula stop?","Yes — Palo Alto, Burlingame, or anywhere up the 101 is easy to add; book hourly if you want the car to wait."),
     ("Do you run late or early?","Yes, 24/7. Red-eyes and early departures included at your quoted price.")]},
 "sfo-to-silicon-valley": {"from":"SFO","navname":"SFO → Silicon Valley","to":"Silicon Valley","h1_to":"Silicon Valley",
   "title":"SFO to Silicon Valley Car Service | Palo Alto & San Jose | Koast",
   "desc":"Private chauffeured car service from SFO to Palo Alto, Menlo Park, Mountain View and San Jose. Flight-tracked, flat pricing, corporate accounts. Book 24/7.",
   "miles":"about 20–35 miles","time":"roughly 30–50 minutes","route":"US-101 or I-280 south","goodfor":"Roadshows, investor visits, exec arrivals, Sand Hill Road",
   "lede":"Flight-tracked transfers from SFO to Palo Alto, Menlo Park, Mountain View, and San Jose — flat-rate, discreet, and built for packed schedules.",
   "drive_h":"The corridor, run by people who run it daily",
   "drive":["Most of the Valley sits 20 to 35 miles south of SFO — Palo Alto and Menlo Park around 20 miles, San Jose closer to 35 — generally 30 to 50 minutes down US-101 or I-280 outside of peak. The 101 corridor is notorious at rush hour, and a driver who runs it every day knows when 280 wins.",
     "It's the route for roadshows, investor visits, and executive arrivals on Sand Hill Road. Fixed pricing, account billing available, and a flight-tracked pickup so a delayed red-eye doesn't blow up the morning."],
   "airport":("../airports/sfo.html","SFO airport transfers","→"),"dest":("../cities/palo-alto.html","Palo Alto car service","→"),
   "faqs":[("How much is SFO to Palo Alto or San Jose?","A flat, upfront price set by your destination and vehicle — no surge, ever. Corporate accounts and itemized receipts are available. Get an instant quote with your details."),
     ("How long does the drive take?","Palo Alto and Menlo Park are about 30 to 45 minutes from SFO; San Jose runs closer to 45 to 60 in traffic. Your chauffeur runs the corridor daily and routes around the 101 crunch."),
     ("Do you handle corporate and roadshow travel?","Yes — account billing, passenger lists, and multi-stop days for teams and investor visits. A flight-tracked pickup keeps a delayed red-eye from derailing the morning."),
     ("Can you do multiple stops?","Book hourly and the car stays with you across Sand Hill Road, campus visits, and meetings — one chauffeur, one flat hourly rate, no re-summoning a ride between stops.")]},
}

def route_page(slug, d):
    import json as _rj
    f = d["from"]
    url = BASE_URL + "/routes/" + slug + ".html"
    drive_html = "".join(f'<p style="color:var(--muted);margin-bottom:16px">{para}</p>' for para in d["drive"])
    p = head(d["title"], d["desc"], "../")
    p += nav("../", "airport")
    p += f"""
<header class="hero-dark"><div class="wrap">
  <div class="crumbs"><a href="../index.html">Home</a><span>/</span><a href="../services/airport-transfers.html">Airport Transfers</a><span>/</span>{f} to {d["to"]}</div>
  <div class="hero-grid">
    <div class="hero-copy">
      <span class="wy-eyebrow">{f} airport transfer &middot; {d["miles"]}</span>
      <h1>{f} to {d["h1_to"]}, <span class="o">chauffeured.</span></h1>
      <p class="lede">{d["lede"]}</p>
      <ul class="check" style="color:#cdd3dc">
        <li>Your flight tracked &mdash; pickup timed to your actual landing</li>
        <li>One flat price, quoted upfront &mdash; no surge</li>
        <li>Complimentary wait time on every arrival</li>
      </ul>
    </div>
    {book_card()}
  </div>
</div></header>
<section class="tight"><div class="wrap grid-2" style="align-items:start;gap:60px">
  <div>
    <span class="pill">The route</span>
    <h2 style="font-size:clamp(28px,3.4vw,36px);margin:14px 0 16px">{d["drive_h"]}</h2>
    {drive_html}
  </div>
  <div>
    <div class="wy-facts">
      <h3>{f} &rarr; {d["to"]}</h3>
      <div class="wy-row"><span class="wy-k">Distance</span><span class="wy-v">{d["miles"]}</span></div>
      <div class="wy-row"><span class="wy-k">Typical time</span><span class="wy-v">{d["time"]}</span></div>
      <div class="wy-row"><span class="wy-k">Route</span><span class="wy-v">{d["route"]}</span></div>
      <div class="wy-row"><span class="wy-k">Pricing</span><span class="wy-v">Flat rate, quoted upfront</span></div>
      <div class="wy-row"><span class="wy-k">Good for</span><span class="wy-v">{d["goodfor"]}</span></div>
    </div>
  </div>
</div></section>
<section class="tight"><div class="wrap grid-2" style="align-items:center;gap:60px">
  <div>
    <span class="pill">Why book ahead</span>
    <h2 style="font-size:clamp(28px,3.4vw,36px);margin:14px 0 16px">No surge, no scramble</h2>
    <ul class="check">
      <li>We track your flight and adjust for delays automatically</li>
      <li>Curbside pickup, timed to when you actually land</li>
      <li>Your chauffeur's name, photo, and live location before you arrive</li>
      <li>One fixed price &mdash; the quote you book is the price you pay</li>
      <li>Licensed, insured, vetted chauffeurs &mdash; not a rotating app driver</li>
    </ul>
    <a class="btn btn-orange btn-lg" href="{BOOK}" style="margin-top:8px">Get an Instant Quote</a>
  </div>
  <div>
    <h3 style="margin-bottom:16px">Match the vehicle to the trip</h3>
    {routes_table([("Business Class Sedan","1–3 passengers"),("Business / First-Class SUV","up to 6"),("Executive Sprinter","up to 14"),("Party bus","groups &amp; events")], "Vehicle", "Best for")}
  </div>
</div></section>"""
    p += faq_section(d["faqs"], f"{f} to {d['to']} questions")
    _same = [s2 for s2 in ROUTES if s2 != slug and ROUTES[s2]["from"] == f]
    _diff = [s2 for s2 in ROUTES if s2 != slug and ROUTES[s2]["from"] != f]
    _order = (_same + _diff)[:5]
    others = [(s2 + ".html", ROUTES[s2]["navname"], "→") for s2 in _order]
    trip = [d["airport"]] + ([d["dest"]] if d.get("dest") else [])
    p += plan_trip([("This trip", trip), ("Other routes", others)])
    p += cta_section(f"Book your {f} to {d['to']} ride.", "Tell us your flight and where you're headed — we'll handle the rest.")
    p += footer("../")
    service = {"@context":"https://schema.org","@type":"Service","name":f"{f} to {d['to']} car service",
        "serviceType":"Chauffeured airport transfer","provider":{"@id":BASE_URL+"/#org"},
        "areaServed":d["to"],"url":url,"description":d["desc"]}
    crumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":BASE_URL+"/"},
        {"@type":"ListItem","position":2,"name":"Airport Transfers","item":BASE_URL+"/services/airport-transfers.html"},
        {"@type":"ListItem","position":3,"name":f"{f} to {d['to']}","item":url}]}
    p += ('<script type="application/ld+json">'+_rj.dumps(service,ensure_ascii=False)+"</script>"
          '<script type="application/ld+json">'+_rj.dumps(crumb,ensure_ascii=False)+"</script>")
    write(f"routes/{slug}.html", p)

def route_section():
    cards = ""
    for slug, d in ROUTES.items():
        cards += (f'<a class="card" href="../routes/{slug}.html" style="display:block">'
                  f'<h3 style="margin:0 0 6px">{d["navname"]}</h3>'
                  f'<div class="sub" style="color:var(--muted);font-size:13.5px">{d["miles"]} &middot; {d["time"]}</div>'
                  f'<div class="row" style="margin-top:10px"><span>Flat-rate transfer</span><span style="color:var(--orange);font-weight:700">View &rarr;</span></div></a>')
    return (f'<section class="tight"><div class="wrap">'
            f'<div class="sec-head"><span class="pill pill-orange">Popular routes</span><h2>Most-booked Bay Area routes</h2>'
            f'<p>Flat-rate, flight-tracked transfers on the runs we drive most — from SFO, OAK, and SJC.</p></div>'
            f'<div class="grid-3">{cards}</div></div></section>')

s = head("Airport Transfer Service | Koast Black Car",
         "Professional chauffeured airport transfers — flight tracking, free wait time, flat rates. Bay Area & nationwide. 24/7.", "../")
s += nav("../", "airport")
s += f"""
<header class="hero-dark"><div class="wrap">
  <div class="crumbs"><a href="../index.html">Home</a><span>/</span>Airport Transfers</div>
  <div class="hero-grid">
    <div class="hero-copy">
      <h1>The airport ride that's <span class="o">already waiting.</span></h1>
      <p class="lede">Flight-tracked pickups, complimentary wait time, and flat-rate pricing — in the Bay Area and major airports nationwide.</p>
      <ul class="check" style="color:#cdd3dc">
        <li>28 major airports — SFO to JFK, all terminals</li>
        <li>Free wait time on every arrival</li>
        <li>Driver details &amp; live tracking before pickup</li>
      </ul>
    </div>
    {book_card()}
  </div>
</div></header>
<section style="padding:40px 0 0"><div class="wrap">
  <div class="ksearch"><input id="asearch" type="search" placeholder="Find your airport — try JFK, LAX, ORD…" aria-label="Find an airport"></div>
</div></section>
<section class="tight agrp"><div class="wrap">
  <div class="sec-head"><span class="pill">Bay Area Airports</span><h2>Our home airports</h2></div>
  <div class="grid-3">{airport_cards("bay")}</div>
</div></section>
<section style="padding-top:0" class="agrp"><div class="wrap">
  <div class="sec-head"><span class="pill pill-orange">Nationwide</span><h2>Major airports across the U.S.</h2>
  <p>The same flight-tracked, flat-rate pickup — at every major airport we serve.</p></div>
  <div class="grid-3">{airport_cards("national")}</div>
</div></section>"""
s += route_section()
s += """
<script>
(function(){
  var i=document.getElementById('asearch');if(!i)return;
  i.addEventListener('input',function(){
    var q=i.value.trim().toLowerCase();
    document.querySelectorAll('.agrp').forEach(function(sec){
      var v=0;
      sec.querySelectorAll('.city-card').forEach(function(c){
        var h=!q||c.textContent.toLowerCase().indexOf(q)>-1;
        c.style.display=h?'':'none';if(h)v++;
      });
      sec.style.display=v?'':'none';
    });
  });
})();
</script>"""
s += why_section()
s += fleet_section("../")
s += cta_section("Never sweat an airport ride again.")
s += footer("../")
write("services/airport-transfers.html", s)

# ============================ SERVICE: CORPORATE ============================
s = head("Corporate Travel & Executive Car Service | Koast",
         "Executive chauffeur service for businesses — account billing, team coordination, consistent professional service. Bay Area & nationwide.", "../")
s += nav("../", "corporate")
s += f"""
<header class="hero-dark"><div class="wrap">
  <div class="crumbs"><a href="../index.html">Home</a><span>/</span>Corporate Travel</div>
  <h1>Ground travel your team <span class="o">doesn't think about.</span></h1>
  <p class="lede">One account. Every executive, client, and candidate moved professionally — in the Bay Area and every major city your team flies to.</p>
  <div style="display:flex;gap:14px;position:relative;z-index:2;flex-wrap:wrap">
    <a class="btn btn-orange btn-lg" href="mailto:{EMAIL}?subject=Corporate%20Account%20Inquiry">Set Up a Corporate Account</a>
    <a class="btn btn-ghost-light btn-lg" href="{BOOK}">Book a Single Ride</a>
  </div>
</div></header>
<section><div class="wrap">
  <div class="sec-head"><span class="pill">For Companies</span><h2>Built for travel managers &amp; EAs</h2></div>
  <div class="grid-2">
    {feat("receipt","o","Consolidated billing","One monthly invoice across all riders and trips. Itemized, exportable, accounting-friendly.")}
    {feat("users","t","Book for anyone","Create passenger lists and book for executives, clients, candidates, or entire teams in seconds.")}
    {feat("pin","o","Live visibility","GPS tracking and automated status texts — know your VIP was picked up without asking.")}
    {feat("globe","t","One standard, nationwide","The same vetted-chauffeur experience in every major city — one account, one invoice, zero surprises.")}
  </div>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="steps">
  <h2>Common corporate use cases</h2>
  <p>Where companies rely on Koast every week.</p>
  <div class="grid-3">
    <div class="step"><div class="num">EXECUTIVES</div><h3>Airport &amp; roadshow travel</h3><p>Flight-tracked transfers and hourly charters for packed schedules — in any city.</p></div>
    <div class="step"><div class="num">CLIENTS</div><h3>VIP &amp; investor visits</h3><p>Flight-tracked arrivals with a chauffeur ready the moment they land — the tone is set before the meeting starts.</p></div>
    <div class="step"><div class="num">TEAMS</div><h3>Offsites &amp; events</h3><p>Sprinters and buses for team offsites, conferences, and company celebrations.</p></div>
  </div>
</div></div></section>"""
s += cta_section("Let's set up your account.", f"Email {EMAIL} or book a first ride and experience the standard.")
s += footer("../")
write("services/corporate-travel.html", s)


# ============================ SERVICE: CARE RIDES ============================
if CARE_RIDES_LIVE:
    s = head("Care Rides by Koast — Senior & Medical Appointment Transportation",
             "Concierge senior and medical-appointment rides. Book for a parent — door-to-door chauffeur, text updates, and waiting during appointments. 24/7.", "../")
    s += nav("../", "")
    s += f"""
    <header class="hero-dark"><div class="wrap">
      <div class="crumbs"><a href="../index.html">Home</a><span>/</span>Care Rides</div>
      <h1>Care Rides <span class="o">by Koast.</span></h1>
      <p class="lede">Concierge senior &amp; medical appointment transportation. Book for a parent or loved one, get a text at every step, and know a vetted professional chauffeur is at the wheel — there and back, door to door.</p>
      <div style="display:flex;gap:14px;position:relative;z-index:2;flex-wrap:wrap">
        <a class="btn btn-orange btn-lg" href="{BOOK}">Book a Care Ride</a>
        <a class="btn btn-ghost-light btn-lg" href="mailto:{EMAIL}">Email Us a Question</a>
      </div>
    </div></header>
    <section><div class="wrap">
      <div class="sec-head"><span class="pill">For Families</span><h2>Built for booking on their behalf</h2>
      <p>Most Care Rides are arranged by a son, daughter, or caregiver. The whole service is designed around that.</p></div>
      <div class="grid-2">
        {feat("users","o","The same chauffeur, ride after ride","For recurring Care Rides we match your loved one with the same chauffeur whenever possible — a familiar face they get to know and trust, not a stranger every week.")}
        {feat("pin","t","Text updates at every step","Chauffeur assigned, arriving, picked up, dropped off — you know without calling anyone.")}
        {feat("receipt","o","A patient, steady hand","Our chauffeurs walk riders to and from the door, offer a steadying arm, stow canes and folding walkers, and never rush.")}
        {feat("globe","t","Book for them, from anywhere","Put the ride in their name and your phone number on the updates. You arrange everything; they just walk out the front door.")}
        {feat("receipt","t","Recurring appointments, handled","Dialysis, physical therapy, oncology — set a standing schedule once and we take it from there.")}
        {feat("users","o","Comfort they can count on","Same clean vehicle class, same routine, same calm professionalism every time. Routine is reassurance.")}
      </div>
    </div></section>
    <section style="padding-top:0"><div class="wrap"><div class="steps">
      <h2>How a Care Ride works</h2>
      <p>Senior transportation, the concierge way.</p>
      <div class="grid-3">
        <div class="step"><div class="num">1</div><h3>Book in their name</h3><p>Use the booking widget or email us — rider's name and address, your number for updates, flat all-inclusive price upfront.</p></div>
        <div class="step"><div class="num">2</div><h3>Door-to-door pickup</h3><p>The chauffeur meets them at the door, offers an arm, handles bags and walkers, and gets them settled comfortably.</p></div>
        <div class="step"><div class="num">3</div><h3>We wait, or come back</h3><p>For medical appointments, book hourly and your chauffeur waits on site — or schedule a return pickup. Either way, you get the updates.</p></div>
      </div>
    </div></div></section>
    <section class="tight"><div class="wrap">
      <div class="sec-head"><span class="pill pill-orange">The Honest Fine Print</span><h2>What Care Rides are — and aren't</h2></div>
      <div class="grid-2" style="align-items:start">
        <div class="card"><h3 style="color:var(--teal-dark)">Care Rides are for</h3>
          <ul class="check" style="margin-top:12px">
            <li>Riders who can walk on their own — a cane or folding walker is no problem</li>
            <li>Medical, dental &amp; therapy appointments, errands, family visits, and outings</li>
            <li>Families who want updates without making calls</li>
            <li>Private-pay riders — simple card payment, clean receipts</li>
          </ul>
        </div>
        <div class="card"><h3 style="color:var(--orange-dark)">What we don't do</h3>
          <p style="font-size:14.5px;color:var(--muted);margin-top:12px;line-height:1.7">Koast is a transportation company, not a medical provider. We don't operate wheelchair-lift vehicles, provide physical transfer assistance, or carry medical equipment. If your loved one needs hands-on or wheelchair-accessible transport, email us — we'll gladly point you to a specialized provider in your area.</p>
        </div>
      </div>
    </div></section>"""
    s += faq_section([
      ("Can I book a ride for my parent or someone else?",
       "Yes — that's exactly what Care Rides are designed for. Book in the rider's name with your phone number on the reservation, and you'll receive the status updates while they get the ride."),
      ("Will the chauffeur help them to the door?",
       "Yes. Chauffeurs walk riders between the door and the car, offer a steadying arm, and stow canes, folding walkers, and bags. Riders do need to be able to walk on their own — we can't provide lifting or transfer assistance."),
      ("Can the driver wait during a medical appointment?",
       "Yes — book hourly and your chauffeur waits on site and brings them home whenever they're ready. For predictable appointments, a scheduled round trip also works."),
      ("Do you take Medicare, Medicaid, or insurance?",
       "No — Care Rides are private-pay only, by credit or debit card. We're not a medical transport provider and don't bill insurance, which is also why we can keep the service simple and on time."),
      ("Can my parent have the same chauffeur every time?",
       "That's the goal — for recurring Care Rides we match riders with the same chauffeur whenever possible. Familiarity matters: riders relax with a driver they know, and the chauffeur learns their routine, their door, and their pace."),
      ("Can you handle recurring appointments like dialysis or PT?",
       "Yes. Email us the standing schedule once and we'll set up the recurring rides — same chauffeur whenever possible, same routine, updates to your phone every time."),
    ], "Care Rides questions")
    s += cta_section("Get them there. Ride easy.", "Book in under a minute, or email us and we'll set everything up for you.")
    s += footer("../")
    write("services/care-rides.html", s)

# ============================ SERVICE: WINE TOURS ============================
s = head("Napa & Sonoma Wine Tours by Private Chauffeur | Koast",
         "Private chauffeured wine tours to Napa Valley & Sonoma from San Francisco and the Bay Area. Your itinerary, your pace — no designated driver needed.", "../")
s += nav("../", "wine")
s += f"""
<header class="hero-dark"><div class="wrap">
  <div class="crumbs"><a href="../index.html">Home</a><span>/</span>Wine Tours</div>
  <div class="hero-grid">
    <div class="hero-copy">
      <h1>Wine country, <span class="o">without the worry.</span></h1>
      <p class="lede">Private chauffeured day trips to Napa Valley and Sonoma — your wineries, your pace, and nobody skipping the tasting to drive home.</p>
      <ul class="check" style="color:#cdd3dc">
        <li>Hourly charter with a dedicated chauffeur</li>
        <li>Sedan for two, Sprinter for the whole crew</li>
        <li>Pickup anywhere in the Bay Area</li>
      </ul>
    </div>
    {book_card()}
  </div>
</div></header>
<section><div class="wrap">
  <div class="sec-head"><span class="pill">How It Works</span><h2>Your day, designed around the glass</h2></div>
  <div class="grid-3">
    <div class="card"><h3>1 · Pick your valley</h3><div class="sub">Napa, Sonoma, Healdsburg, or Livermore</div><p style="font-size:14.5px;color:var(--muted)">Tell us where you're tasting — or ask for route suggestions. Most groups visit 3–4 wineries comfortably in a day.</p></div>
    <div class="card"><h3>2 · We handle the driving</h3><div class="sub">Door-to-door, all day</div><p style="font-size:14.5px;color:var(--muted)">Your chauffeur waits at each stop, keeps water cold, and adjusts the route as the day unfolds. Lunch detours encouraged.</p></div>
    <div class="card"><h3>3 · Everyone tastes</h3><div class="sub">No designated driver needed</div><p style="font-size:14.5px;color:var(--muted)">The whole group enjoys the day. We get everyone home safely — whether that's the city, the Peninsula, or the East Bay.</p></div>
  </div>
</div></section>
<section style="padding-top:0"><div class="wrap grid-2" style="align-items:center;gap:60px">
  <div>
    <span class="pill pill-orange">Group Sizes</span>
    <h2 style="font-size:32px;margin:14px 0 16px">From date day to bachelorette</h2>
    <ul class="check">
      <li><strong>Couples</strong> — Business Sedan or First-Class SUV</li>
      <li><strong>Friends &amp; families (up to 6)</strong> — Business or First-Class SUV</li>
      <li><strong>Groups up to 14</strong> — Executive Sprinter</li>
      <li><strong>Big celebrations (up to 32)</strong> — Mid-Size or Large Party Bus</li>
    </ul>
  </div>
  <div>
    <h3 style="margin-bottom:16px">Popular wine country trips</h3>
    {routes_table([("San Francisco → Napa Valley","1.5 hr each way"),("San Francisco → Sonoma Square","1–1.5 hr"),("Peninsula → Healdsburg","1.5–2 hr"),("East Bay → Livermore Valley","30–45 min")])}
  </div>
</div></section>"""

WINE_IMG = {
 "napa-valley":"blog-banner-napa.jpg","sonoma":"blog-banner-sonoma.jpg",
 "temecula":"blog-banner-temecula.jpg","willamette-valley":"blog-banner-willamette.jpg",
 "healdsburg":"wt-healdsburg.jpg","paso-robles":"wt-paso-robles.jpg",
 "santa-ynez":"wt-santa-ynez.jpg","livermore":"wt-livermore.jpg",
 "walla-walla":"wt-walla-walla.jpg","finger-lakes":"wt-finger-lakes.jpg",
 "texas-hill-country":"wt-texas-hill-country.jpg","virginia":"wt-virginia.jpg",
}
import os as _os
def wine_card(slug, r):
    img = WINE_IMG.get(slug)
    has = img and _os.path.exists(_os.path.join(ROOT, "img", img))
    pic = f'<div class="card-img"><img src="../img/{img}" alt="{r["name"]} wine tours" loading="lazy"></div>' if has else ""
    return f"""<a class="card wt-card city-card" href="../wine-tours/{slug}.html">{pic}<h3>{r['name']}</h3><div class="sub">{r['known'][:70]}…</div><div class="row"><span>{r['drive'].capitalize()}</span><span style="color:var(--orange);font-weight:700">Explore →</span></div></a>"""

ca_cards = "".join(wine_card(slug, r) for slug, r in WINE_REGIONS.items() if r["area"]=="ca")
us_cards = "".join(wine_card(slug, r) for slug, r in WINE_REGIONS.items() if r["area"]=="us")
s += f"""
<section style="padding-top:0"><div class="wrap">
  <div class="sec-head"><span class="pill">Wine Regions</span><h2>Where we pour</h2>
  <p>Chauffeured tasting days in California's great valleys — and America's best wine country beyond.</p></div>
  <div class="ksearch" style="margin:0 auto 34px">
    <input id="wsearch" type="search" placeholder="Find a wine region — try Napa, Temecula, Willamette…" aria-label="Find a wine region">
  </div>
  <div class="wgrp"><h3 style="margin-bottom:16px">California</h3>
  <div class="grid-3" style="margin-bottom:36px">{ca_cards}</div></div>
  <div class="wgrp"><h3 style="margin-bottom:16px">Nationwide</h3>
  <div class="grid-3">{us_cards}</div></div>
  <div style="text-align:center;margin-top:34px"><a class="btn btn-line btn-lg" href="../wineries/index.html">Browse all 72 wineries &rarr;</a></div>
</div></section>"""
s += """
<script>
(function(){
  var i=document.getElementById('wsearch');if(!i)return;
  i.addEventListener('input',function(){
    var q=i.value.trim().toLowerCase();
    document.querySelectorAll('.wgrp').forEach(function(g){
      var v=0;
      g.querySelectorAll('.wt-card').forEach(function(c){
        var h=!q||c.textContent.toLowerCase().indexOf(q)>-1;
        c.style.display=h?'':'none';if(h)v++;
      });
      g.style.display=v?'':'none';
    });
  });
})();
</script>"""
s += faq_section([
  ("How is a wine tour priced?",
   "Wine tours are booked as hourly charters — one flat hourly rate that covers the vehicle, your dedicated chauffeur, water, and all driving for the day. Most tours run 6–8 hours door to door."),
  ("Can you recommend wineries?",
   "Yes — tell us your taste (big cabs, sparkling, small family producers) and we'll suggest a route. We can also coordinate timed tasting reservations."),
  ("Can we bring wine back in the vehicle?",
   "Absolutely. Cases ride safely in the back, and your chauffeur handles the loading at every stop."),
], "Wine tour questions")
s += cta_section("Book your wine country day.", "Tell us your date and group size — we'll handle everything else.")
s += footer("../")
write("services/wine-tours.html", s)

# ============================ BLOG FAQ (retrofit) ============================
BLOG_FAQ = {
 "lax-airport-black-car-guide": [
  ("How much is a black car from LAX?", "A flat, all-inclusive rate quoted before you book — tolls and gratuity included, with no surge during peak arrivals. Enter your pickup and drop-off for an instant price."),
  ("How does pickup work with the LAX-it lot?", "Your chauffeur tracks your flight and coordinates pickup for your terminal, so you skip the LAX-it shuttle and ride-app lot entirely. The car is arranged to meet you on arrival."),
  ("How long will the chauffeur wait if my flight is late?", "LAX arrivals include complimentary wait time — 30 minutes domestic, an hour international — and the flight is tracked, so pickup shifts with your actual landing at no extra charge."),
 ],
 "chicago-ohare-midway-guide": [
  ("Is a black car cheaper from O'Hare or Midway?", "Pricing is by distance and flat-rate either way, with no surge. Midway is closer to downtown, so that ride is usually shorter; O'Hare serves more airlines and international routes."),
  ("How long is the ride from O'Hare to downtown Chicago?", "Typically 30–45 minutes off-peak and longer in rush hour or winter weather. Your chauffeur picks the fastest route — the Kennedy or surface alternates — for conditions."),
  ("Do you operate in winter weather and flight delays?", "Yes, 24/7. Flights are tracked so pickups adjust automatically to delays, and the flat price doesn't change when O'Hare backs up in a snow event."),
 ],
 "boston-logan-guide": [
  ("How much is a black car from Logan Airport?", "A flat, all-inclusive price quoted before you book — tunnel tolls and gratuity included, no surge. Enter your pickup and drop-off for an instant quote."),
  ("How long is Logan to downtown Boston or Cambridge?", "Usually 10–25 minutes via the Ted Williams or Sumner tunnels, depending on the hour. Tunnel traffic is the main variable; your chauffeur routes around the worst of it."),
  ("Where does the chauffeur meet me at Logan?", "Pickup is arranged for your arriving terminal using your flight details, with the flight tracked so the car is there when you land — including the Terminal E international scrum."),
 ],
 "dc-airport-decision": [
  ("Which D.C. airport is best for a black car downtown?", "Reagan National (DCA) is closest to downtown and usually the shortest ride. Dulles (IAD) and BWI are farther out — a flat rate keeps the longer rides predictable with no surge."),
  ("How long is each airport to downtown D.C.?", "DCA is roughly 15–25 minutes, IAD 40–60, and BWI 45–70, all traffic-dependent. We quote a flat price for any of the three before you book."),
  ("Can you do interstate runs between the D.C. airports and cities?", "Yes — airport transfers plus point-to-point and longer regional rides, including runs to Baltimore, Annapolis, and Virginia, all at flat, all-inclusive rates."),
 ],
 "nyc-events-calendar": [
  ("What's the best way to get around New York during a big event?", "A pre-scheduled black car beats fighting for a rideshare when streets close and surge spikes. Your pickup is set in advance, so you're not refreshing an app during a marathon or parade."),
  ("Does pricing surge during marathons, concerts, or holidays?", "No. Koast is flat-rate, so a New Year's Eve or US Open night costs the same per the route as any other day — no event surge, ever."),
  ("Can you handle multiple stops across an event-packed evening?", "Yes. An hourly booking keeps the same car and chauffeur on standby across galas, dinners, and after-parties, so you're not re-summoning a ride between stops."),
 ],
 "chicago-summer-festivals": [
  ("How do you get to Lollapalooza or a Grant Park festival without parking?", "A black car drops you at the closest open access point and picks you up after on a pre-set corner — no festival parking, no surge, and no walking back to a far lot at midnight."),
  ("Does pricing change during festival weekends?", "No. Flat-rate pricing means Lollapalooza weekend or the Air & Water Show costs the same per route as any other day."),
  ("Can a group ride together to a festival?", "Yes — an SUV for up to six or a Sprinter for a larger crew keeps everyone together, with one drop-off and a scheduled pickup for the ride home."),
 ],
 "miami-art-week": [
  ("How do you get around Miami during Art Basel?", "A scheduled black car with a chauffeur who knows causeway timing beats rideshare surge during Art Week. Pickups are pre-set so you make every fair, dinner, and party on time."),
  ("Does pricing surge during Art Basel and Miami Art Week?", "No. Koast is flat-rate, so the busiest week of the Miami calendar costs the same per route as any other — no surge between the beach and the mainland."),
  ("Can you keep a car on standby for fair-hopping?", "Yes. An hourly booking holds the same car and chauffeur all evening, so you can move between Basel, the satellite fairs, and late-night events without re-booking."),
 ],
 "nashville-music-calendar": [
  ("How do you get around Nashville during CMA Fest or a big weekend?", "A pre-scheduled black car skips the Broadway gridlock and rideshare surge. Your pickup is set in advance for honky-tonks, arenas, and the airport run home."),
  ("Does pricing surge during festivals and bachelorette weekends?", "No. Flat-rate pricing means a CMA Fest Saturday or a packed bachelorette weekend costs the same per route as any other day."),
  ("Can a group move between venues together?", "Yes — an SUV for up to six or a Sprinter for the whole party keeps the group together between Broadway, dinner, and the show, with scheduled pickups."),
 ],
 "houston-rodeo-guide": [
  ("What's the best way to get to NRG Park for the rodeo?", "A black car drop-off at the gate skips the half-mile lot hike and the post-show parking crawl. Pickup is pre-arranged on the Fannin side so you're at dinner while the lots are still clearing."),
  ("Does pricing surge on concert nights?", "No. Koast is flat-rate, so a headline rodeo concert night costs the same per route as any other day — no event surge."),
  ("Can a group ride to the rodeo together?", "Yes — a Suburban for six or a Sprinter for fourteen keeps everyone together, with room for the cooler and a scheduled pickup for the ride home."),
 ],
 "seattle-events-guide": [
  ("How do you get around Seattle on a stadium or festival day?", "A pre-scheduled black car skips the I-5 and SoDo crush. Pickups are set on streets like First Avenue so you're moving while the stadium lots are still gridlocked."),
  ("Does pricing surge during Seafair, Bumbershoot, or game days?", "No. Flat-rate pricing means the busiest Seattle event days cost the same per route as any other — no surge when 50,000 people share two exits."),
  ("Can you coordinate around bridge and freeway closures?", "Yes. Your chauffeur knows the Seafair bridge windows and stadium-day patterns and routes around them, with the flat price holding regardless of the detour."),
 ],
 "austin-festival-season": [
  ("How do you get around Austin during SXSW or ACL?", "A pre-scheduled black car beats the downtown gridlock and rideshare surge when the city doubles in size. Pickups are set in advance so you make panels, shows, and the airport on time."),
  ("Does pricing surge during SXSW and ACL?", "No. Koast is flat-rate, so festival weeks cost the same per route as any other — no surge during Austin's busiest stretches."),
  ("Can a group ride together during festival season?", "Yes — an SUV for up to six or a Sprinter for a larger crew keeps the group together between venues, with a scheduled pickup for the ride home."),
 ],
 "miami-getting-around": [
  ("What's the fastest way across Miami's causeways?", "It depends on the hour — your chauffeur knows when the MacArthur is flowing versus the Julia Tuttle or Venetian, and routes for the moment rather than guessing with an app."),
  ("When does Miami traffic peak?", "Causeway and I-95 traffic stacks hardest during morning and evening rush and around events. A scheduled pickup with a local chauffeur is how you time the crossings."),
  ("Do you serve Brickell, South Beach, Coral Gables, and the airport?", "Yes — point-to-point rides anywhere across Miami plus MIA and FLL airport transfers and PortMiami cruise runs, all at flat, all-inclusive rates."),
 ],
 "seattle-getting-around": [
  ("What's the best way to move between Seattle and the Eastside?", "Timing the bridges is everything — your chauffeur knows when the 520 and I-90 are flowing and routes around the worst, so a Seattle-to-Bellevue or Redmond run stays predictable."),
  ("When does Seattle traffic peak?", "I-5 and the bridges stack hardest during rush hour and around stadium events. A scheduled pickup with a local chauffeur is the reliable way through it."),
  ("Do you serve the tech campuses and both downtowns?", "Yes — rides between Seattle, Bellevue, Redmond, and the campuses, plus airport transfers, all at flat rates with the same chauffeur standard."),
 ],
 "denver-mountain-transfers": [
  ("How much is a car from Denver to Vail, Breckenridge, or Keystone?", "A flat, all-inclusive rate quoted before you book — no surge, no metered surprises on a long I-70 run. Enter your resort for an instant price."),
  ("How long is the I-70 drive to the ski resorts?", "Roughly 1.5–2.5 hours to the main resorts depending on conditions, longer on powder days or holiday weekends. A professional chauffeur handles the mountain driving while you rest."),
  ("Is there room for ski and snowboard gear?", "Yes — an SUV or Sprinter carries the group plus skis, boards, and luggage, which is why travelers skip the rental car and the chains entirely."),
 ],
 "vegas-convention-transportation": [
  ("How do you move a team through CES or a big convention week?", "Pre-scheduled black cars and Sprinters with set pickups skip the taxi and rideshare lines that swallow hours during convention weeks. One account keeps every ride coordinated."),
  ("Does pricing surge during CES and major conventions?", "No. Koast is flat-rate, so even the busiest Las Vegas convention week costs the same per route as any other — no surge when the city fills up."),
  ("Can you handle airport pickups for a whole team?", "Yes — staggered arrivals grouped into waves, flight-tracked, with vehicles sized to the group and everything billed to one corporate account."),
 ],
 "choosing-corporate-car-service": [
  ("What should I ask a corporate car service before signing on?", "Confirm commercial licensing and insurance, real coverage in the cities you travel, consolidated billing, flat transparent pricing, and a real human dispatcher to reach when plans change."),
  ("Why use a corporate account instead of rideshare for business travel?", "Account billing, passenger lists, consistent vetted chauffeurs, flight tracking, and one invoice — plus flat pricing with no surge, which rideshare can't guarantee for executives."),
  ("Can one account cover travel across multiple cities?", "Yes. A single Koast corporate account books the same standard of service in every market we serve, with one consolidated invoice instead of a vendor in each city."),
 ],
 "chauffeur-terms-glossary": [
  ("What does flat-rate or all-inclusive pricing mean?", "The price you're quoted before booking is the final price — tolls, fees, and gratuity included, with no surge. What you see is what you pay."),
  ("What is complimentary wait time at the airport?", "It's free wait time built into airport pickups — 30 minutes for domestic flights and an hour for international — with the flight tracked so the clock follows your actual landing."),
  ("What's the difference between a transfer and an hourly booking?", "A transfer is point-to-point at a flat rate. An hourly booking keeps the same car and chauffeur on standby for a set number of hours — ideal for multiple stops or an as-directed day."),
 ],
 "sonoma-first-timers": [
  ("Do I need reservations for Sonoma wineries?", "Many require them, especially weekends and for groups. Your chauffeur and our team can help time a relaxed three-stop day so you're not rushing between appointments."),
  ("How does a chauffeured Sonoma day work?", "An hourly booking holds the car for the day — you taste, we drive. No designated driver, no parking, and no rush to make the next reservation."),
  ("Is Sonoma good for a first wine-country trip?", "Yes — it's more laid-back than Napa, with the historic square and a short, scenic spread of tasting rooms that make an easy, unhurried first day."),
 ],
 "temecula-balloons-tastings": [
  ("Can you do an early balloon launch plus afternoon tastings?", "Yes — an hourly booking covers a dawn balloon launch and a full day of tastings on one flat rate, with the chauffeur handling every transfer in between."),
  ("How far is Temecula from San Diego or Los Angeles?", "Roughly an hour from San Diego and about 90 minutes from much of L.A., traffic depending. A flat rate keeps the round trip predictable."),
  ("Is Temecula good for groups?", "Yes — an SUV or Sprinter keeps the group together across wineries, with no designated-driver problem and a scheduled pickup for the ride home."),
 ],
 "willamette-pinot-weekend": [
  ("Where should I base a Willamette Valley wine weekend?", "Dundee, McMinnville, and Newberg put you central to the best Pinot Noir tasting rooms. A chauffeur for the day means you taste freely without managing the rural drives."),
  ("How does a chauffeured Willamette day work?", "An hourly booking holds the car for the day across the valley's spread-out wineries — no designated driver and no navigating country roads between appointments."),
  ("Are winter visits to the Willamette Valley worth it?", "Yes — quieter tasting rooms, easier reservations, and the same world-class Pinot. A warm car and a chauffeur make the off-season drive genuinely pleasant."),
 ],
 "group-wine-tour-planning": [
  ("What size vehicle do I need for a group wine tour?", "Up to six rides comfortably in an SUV; larger groups take a Sprinter (up to fourteen) or a party bus. Matching the vehicle to the group keeps everyone together with room for cases."),
  ("How far ahead should I book a group wine tour?", "Book a few weeks out for weekends and peak season — both the vehicle and the winery reservations fill up. We can help sequence stops and timing."),
  ("Does a chauffeured wine tour solve the designated-driver problem?", "Yes — that's the point. Everyone tastes, the chauffeur drives, and there's no parking, no navigation, and no one drawing the short straw."),
 ],
 "black-car-vs-rideshare-cost": [
  ("Is a black car actually more expensive than rideshare?", "Once you add surge, airport fees, tips, and the occasional cancellation, the gap narrows — and a flat, all-inclusive black car price removes the uncertainty rideshare can't."),
  ("Does a black car ever beat rideshare on price?", "During surge — airport peaks, bad weather, big events — a flat-rate black car can come in lower than a surged rideshare, while always being more predictable."),
  ("What's included in a Koast flat rate?", "Tolls, fees, and gratuity, with no surge. The quoted price is the final price, so there's nothing added after the ride."),
 ],
 "sfo-to-san-francisco-black-car-guide": [
  ("How much is a black car from SFO to San Francisco?", "A flat, all-inclusive rate quoted before you book — tolls and gratuity included, no surge. Enter your pickup and drop-off for an instant price."),
  ("How long is SFO to downtown San Francisco?", "Usually 25–40 minutes depending on the hour and whether the 101 is flowing. Your chauffeur routes for the conditions; the flat price holds either way."),
  ("How long will the chauffeur wait if my flight is delayed?", "SFO arrivals include complimentary wait time — 30 minutes domestic, an hour international — and the flight is tracked so pickup follows your actual landing at no extra charge."),
 ],
 "san-francisco-summer-2026-events": [
  ("What's the best way to get around SF during a big summer event?", "A pre-scheduled black car skips the road closures and rideshare surge around World Cup matches, Outside Lands, and street festivals. Pickups are set in advance so you arrive on time."),
  ("Does pricing surge during major SF events?", "No. Koast is flat-rate, so the busiest summer weekends cost the same per route as any other day — no event surge."),
  ("Can a group ride together to an event?", "Yes — an SUV for up to six or a Sprinter for a larger crew keeps everyone together, with one drop-off and a scheduled pickup for the ride home."),
 ],
 "napa-sonoma-chauffeur-day-trip": [
  ("How does a chauffeured Napa or Sonoma day trip work?", "An hourly booking holds the car for the day — you taste, we drive. No designated driver, no parking, and no rushing between winery reservations."),
  ("How far is wine country from San Francisco?", "Napa and Sonoma are roughly 60–90 minutes from the city, traffic depending. A flat rate keeps the round trip predictable with no metered surprises."),
  ("What vehicle is best for a wine-country day?", "A sedan or SUV suits couples and small groups; a Sprinter fits up to fourteen with room for cases — all with the same chauffeur standard and no designated-driver problem."),
 ],
 "nyc-ground-travel-guide": [
  ("JFK, LaGuardia, or Newark — which is best for a black car?", "LaGuardia is closest to Midtown when traffic cooperates, Newark can win for the West Side and New Jersey, and JFK is the international gateway with the most predictable ride. We quote a flat rate for any of them."),
  ("When is a black car worth it over the subway in New York?", "Airport runs with luggage, late nights, group travel, and tight schedules — anytime predictability and door-to-door beat saving a few dollars on a transfer-heavy subway trip."),
  ("Does pricing surge during rush hour or events in NYC?", "No. Koast is flat-rate, so a rush-hour or event-night ride costs the same per route as any other — no surge."),
 ],
 "ea-guide-executive-ground-travel": [
  ("How can an EA book ground travel for an executive?", "Book for anyone from one account, with driver details sent before every pickup, flight tracking, and one place to make changes when the schedule moves at 6 a.m."),
  ("What makes ground travel reliable for executives?", "Vetted, commercially licensed chauffeurs, flight-tracked airport pickups, flat pricing with no surge, and a real human dispatcher to reach — not an app chatbot — when plans change."),
  ("Can one account coordinate travel across cities and time zones?", "Yes. A single corporate account books the same standard in every market, with passenger lists and consolidated billing, so coordinating principals across time zones runs from one place."),
 ],
}

# ============================ BLOG ============================
BLOG = [
 ("nyc-events-calendar.html","blog-banner-nyc-events.jpg","City Events","New York Events Worth Planning Around","The concerts, marathons, and openings that move Manhattan — and how to arrive when the streets don't cooperate."),
 ("chicago-summer-festivals.html","blog-banner-chi-fest.jpg","City Events","Chicago's Festival Summer, Mapped","Lolla, Taste of Chicago, the Air & Water Show — what closes, what crowds, and how locals hop between them."),
 ("miami-art-week.html","blog-banner-miami-art.jpg","City Events","Miami Art Week Without the Gridlock","Art Basel logistics for people with more than one party to make — causeway timing, fair-hopping, and late-night moves."),
 ("nashville-music-calendar.html","blog-banner-nash-music.jpg","City Events","Nashville's Music Calendar: CMA Fest to New Year's Eve","Broadway's biggest weeks, when hotels spike, and how groups move between honky-tonks and arenas."),
 ("houston-rodeo-guide.html","blog-banner-hou-rodeo.jpg","City Events","Houston Rodeo Season: The Getting-There Guide","Three weeks, two million visitors, one parking nightmare — the NRG Park playbook for rodeo nights."),
 ("seattle-events-guide.html","blog-banner-sea-events.jpg","City Events","Seattle's Event Season: Bumbershoot to Game Day","Festivals, sold-out shows, and stadium Saturdays — moving around Seattle when everyone has plans."),
 ("san-francisco-summer-2026-events.html","blog-banner-sf.jpg","City Events","San Francisco Summer 2026: World Cup, Outside Lands & More","The Bay's biggest summer ever — what's on, where it is, and how to get there without parking nightmares."),
 ("lax-airport-black-car-guide.html","blog-banner-la.jpg","Airport Guides","LAX Without the Chaos: The Black Car Pickup Guide","Terminal-by-terminal pickup reality, the LAX-it lot problem, and how chauffeured pickup actually works."),
 ("chicago-ohare-midway-guide.html","blog-banner-chicago.jpg","Airport Guides","O'Hare or Midway? The Chicago Airport Decision","Which airport to fly into, what each ride downtown really takes, and winter travel survival."),
 ("vegas-convention-transportation.html","blog-banner-vegas.jpg","Corporate","The Las Vegas Convention Playbook","Moving a team through CES week without losing hours in taxi lines — venue logistics that work."),
 ("miami-getting-around.html","blog-banner-miami.jpg","City Guides","Getting Around Miami: Brickell, South Beach & Beyond","Why the causeways rule everything, when traffic peaks, and how locals time their crossings."),
 ("denver-mountain-transfers.html","blog-banner-denver.jpg","Trips","Denver to the Slopes: The Mountain Transfer Guide","Vail, Breck, Keystone — what the I-70 drive really takes and why skiers skip the rental car."),
 ("napa-sonoma-chauffeur-day-trip.html","blog-banner-napa.jpg","Wine Country","Napa & Sonoma by Chauffeur: A Day-Trip Playbook","Wine country without a designated driver problem — routes, timing, and vehicle picks."),
 ("nyc-ground-travel-guide.html","blog-banner-nyc.jpg","City Guides","Getting Around New York Without Losing Your Mind","JFK vs. LGA vs. EWR, when the subway wins, and when a black car is worth every penny."),
 ("black-car-vs-rideshare-cost.html","blog-banner-rideshare.jpg","Industry","Black Car vs. Rideshare: The Real Cost Math","Surge, airport fees, tips, cancellations — what the price comparison looks like when you count everything."),
 ("choosing-corporate-car-service.html","blog-banner-corporate.jpg","Corporate","How to Choose a Corporate Car Service: 9 Questions to Ask","The vetting checklist travel managers use — insurance, billing, coverage, and the questions vendors dodge."),
 ("chauffeur-terms-glossary.html","blog-banner-glossary.jpg","Industry","Wait Time, Hourly & Flat Rate: Chauffeur Terms, Explained","The industry's vocabulary decoded, so you know exactly what you're booking."),
 ("sfo-to-san-francisco-black-car-guide.html","blog-banner-sfo.jpg","Airport Guides","SFO to San Francisco: The Complete Black Car Guide","What it costs, how pickup works, and why travelers are switching from rideshare for airport runs."),
 ("ea-guide-executive-ground-travel.html","blog-banner-ea-guide.jpg","Corporate","The EA's Guide to Booking Executive Ground Travel","How executive assistants coordinate flawless ground transportation for leadership teams."),
 ("austin-festival-season.html","city-austin.jpg","City Events","Austin Festival Season, Survived","SXSW and ACL move half a million people — how locals and pros get around when the city doubles."),
 ("boston-logan-guide.html","city-boston.jpg","Airport Guides","Logan Airport Done Right","Boston's tunnels, the Ted Williams, and why pre-booked beats the rideshare scrum at Terminal E."),
 ("seattle-getting-around.html","city-seattle.jpg","City Guides","Getting Around Seattle & the Eastside","Two downtowns with a lake between them — timing the bridges and moving between campuses."),
 ("dc-airport-decision.html","city-washington-dc.jpg","Airport Guides","DCA, IAD or BWI? The D.C. Decision","Three airports, practically three different cities — how to choose and what each ride downtown takes."),
 ("sonoma-first-timers.html","blog-banner-sonoma.jpg","Wine Country","A First-Timer's Day in Sonoma","The square, the valley, and a relaxed three-stop day that converts Napa loyalists."),
 ("temecula-balloons-tastings.html","blog-banner-temecula.jpg","Wine Country","Temecula: Balloons at Dawn, Tastings by Noon","SoCal's wine country does mornings like nowhere else — the full balloon-to-bottle day."),
 ("willamette-pinot-weekend.html","blog-banner-willamette.jpg","Wine Country","A Pinot Weekend in the Willamette Valley","Oregon's quiet giant — where to base, how to pace it, and why winter visits are underrated."),
 ("group-wine-tour-planning.html","blog-banner-winegroup.jpg","Wine Country","How to Plan a Group Wine Tour: 7 Decisions","Group size, region, reservations, lunch, and the vehicle math — get these right and the day runs itself."),
 ("jfk-black-car-guide.html","blog-jfk.jpg","Airport Guides","JFK Black Car Service: The Arrivals Playbook","How arrivals pickup works at JFK, real drive times to Manhattan, and why travelers skip the for-hire line."),
 ("atlanta-airport-black-car-guide.html","blog-atl.jpg","Airport Guides","ATL Black Car Service: The World's Busiest Airport, Handled","Domestic vs. international arrivals, ground-transport reality, and flat-rate rides to Buckhead, Midtown & downtown."),
 ("dfw-black-car-guide.html","blog-dfw.jpg","Airport Guides","DFW Black Car Service: Five Terminals, One Easy Pickup","DFW vs. Love Field, drive times across the Metroplex, and why pre-booked beats wandering a city-sized airport."),
 ("miami-airport-black-car-guide.html","blog-mia.jpg","Airport Guides","MIA Black Car Service: Arrivals to South Beach, Brickell & the Port","Causeway timing, real drive times, and cruise-day logistics from Miami International."),
 ("investor-roadshow-ground-travel.html","blog-roadshow.jpg","Corporate","The Investor Roadshow Ground-Travel Playbook","One account across cities, on time between back-to-back meetings, and a single invoice at the end."),
 ("group-airport-transfers.html","blog-group.jpg","Corporate","Group Airport Transfers: Moving a Team Through Arrivals","Staggered flights, one vehicle vs. several, and keeping a whole team moving on arrival."),
]

def post_card(href, img, cat, title, excerpt):
    return f"""
  <a class="card post-card" href="{href}">
    <div class="thumb"><img src="../img/{img}" alt="{title}" loading="lazy"></div>
    <div class="body"><div class="meta"><b>{cat}</b> · June 2026</div>
    <h3>{title}</h3>
    <p>{excerpt}</p></div>
  </a>"""

CAT_ORDER = ["City Events","Airport Guides","City Guides","Wine Country","Trips","Corporate","Industry"]

b = head("Koast Blog — Travel, Airports & Ground Transportation",
         "Guides on airports, black car travel, corporate ground transportation, wine country, and getting around the cities we serve.", "../")
b += nav("../", "blog")
b += """
<header class="hero" style="padding-bottom:24px"><div class="wrap">
  <span class="pill">The Koast Blog</span>
  <h1 style="font-size:clamp(36px,5vw,54px)">Travel smarter, <span class="t">ride easier.</span></h1>
  <p class="lede">Airport guides, travel tips, and everything ground transportation.</p>
  <div class="blog-tools">
    <div class="ksearch"><input id="bsearch" type="search" placeholder="Search articles — try Napa or LAX…" aria-label="Search articles"></div>
    <div class="chips" id="bchips"></div>
  </div>
</div></header>
<section class="tight" style="padding-top:28px"><div class="wrap" id="bwrap">
"""
for cat in CAT_ORDER:
    posts = [p for p in BLOG if p[2] == cat]
    if not posts: continue
    cards = "".join(post_card(*p) for p in posts)
    b += f"""
  <div class="bcat" data-cat="{cat}">
    <h2 class="bcat-title">{cat}</h2>
    <div class="grid-3">{cards}</div>
  </div>"""
b += """
  <div id="bempty" style="display:none;text-align:center;color:var(--muted);padding:50px 0">No articles match — try another search.</div>
</div></section>
<script>
(function(){
  var cats = Array.prototype.map.call(document.querySelectorAll('.bcat'), function(c){return c.dataset.cat});
  var chips = document.getElementById('bchips');
  var activeCat = 'All';
  ['All'].concat(cats).forEach(function(c){
    var btn = document.createElement('button');
    btn.textContent = c; btn.className = c==='All' ? 'on' : '';
    btn.onclick = function(){ activeCat = c; Array.prototype.forEach.call(chips.children, function(x){x.className = x.textContent===c ? 'on' : ''}); filter(); };
    chips.appendChild(btn);
  });
  var q = document.getElementById('bsearch');
  q.addEventListener('input', filter);
  function filter(){
    var term = q.value.toLowerCase(); var any = false;
    document.querySelectorAll('.bcat').forEach(function(sec){
      var secMatch = (activeCat==='All' || sec.dataset.cat===activeCat); var vis = 0;
      sec.querySelectorAll('.post-card').forEach(function(card){
        var hit = secMatch && card.textContent.toLowerCase().indexOf(term) > -1;
        card.style.display = hit ? '' : 'none'; if(hit) vis++;
      });
      sec.style.display = vis ? '' : 'none'; if(vis) any = true;
    });
    document.getElementById('bempty').style.display = any ? 'none' : 'block';
  }
})();
</script>"""
b += cta_section()
b += footer("../")
write("blog/index.html", b)

p = head("SFO to San Francisco: The Complete Black Car Guide (2026) | Koast",
         "How much a black car from SFO to San Francisco costs, how pickup works, and how it compares to rideshare. Updated 2026.", "../")
p += nav("../", "blog")
p += f"""
<section class="tight"><div class="wrap article">
  <span class="pill">Airport Guides</span>
  <h1>SFO to San Francisco: The Complete Black Car Guide</h1>
  <div class="meta">By the Koast Team · Updated June 2026 · 5 min read</div>
  <img class="post-hero" src="../img/blog-banner-sfo.jpg" alt="San Francisco airport at dawn">
  <p>Landing at SFO after a long flight, the last thing you want is a 25-minute wait in the rideshare lot watching your driver cancel twice. Here's how chauffeured airport transfer actually works, what it costs, and when it makes sense over rideshare.</p>
  <h2>How pickup works</h2>
  <p>With a pre-booked black car, your driver tracks your flight and times the pickup to your actual arrival — early, late, or on time. You'll have their name, photo, and phone number before you land. Your driver pulls up curbside when you're ready, or helps with your bags — pickup timed to your actual arrival.</p>
  <div class="callout"><p><strong>Wait time is free:</strong> 30 minutes on domestic arrivals and a full hour on international — enough for customs, baggage, and a coffee.</p></div>
  <h2>What it costs</h2>
  <p>Black car pricing is flat-rate: quoted upfront, all-inclusive of tolls, airport fees, and gratuity. Rideshare from SFO to downtown often looks cheaper — until surge pricing, airport pickup fees, and tips stack up. On busy evenings, rideshare can exceed a fixed black car rate while delivering a fraction of the experience.</p>
  <h2>When black car beats rideshare</h2>
  <ul>
    <li><strong>Early or critical flights</strong> — a confirmed, scheduled pickup beats hoping a driver accepts at 4:30 AM.</li>
    <li><strong>Business travel</strong> — receipts, consistency, and a quiet professional environment between calls.</li>
    <li><strong>Groups &amp; luggage</strong> — SUVs and Sprinters swallow ski bags, golf clubs, and sample cases.</li>
    <li><strong>Guests you care about</strong> — clients, candidates, parents. A chauffeur ready the moment they land sets the tone.</li>
  </ul>
  <h2>Booking it</h2>
  <p>Enter your flight and drop-off at <a href="{BOOK}" style="color:var(--orange);font-weight:700">koastride.com</a> for an instant quote. No account or app needed — you'll get text updates and live driver tracking automatically.</p>
</div></section>"""
p += cta_section("Try it on your next landing.")
p += faq_section(BLOG_FAQ["sfo-to-san-francisco-black-car-guide"])
p += footer("../")
write("blog/sfo-to-san-francisco-black-car-guide.html", p)

print("Done - site generated.")

# ============================ BLOG: SF SUMMER 2026 ============================
p = head("San Francisco Summer 2026: World Cup, Outside Lands & Every Big Event | Koast",
         "SF's biggest summer ever — World Cup matches at Levi's Stadium, Outside Lands, Stern Grove, Fillmore Jazz Fest. What's on and how to get there.", "../")
p += nav("../", "blog")
p += f"""
<section class="tight"><div class="wrap article">
  <span class="pill">City Events</span>
  <h1>San Francisco Summer 2026: The Bay's Biggest Season Ever</h1>
  <div class="meta">By the Koast Team · June 2026 · 6 min read</div>
  <img class="post-hero" src="../img/blog-banner-sf.jpg" alt="San Francisco summer events illustration">
  <p>Between the FIFA World Cup coming to the Bay, Outside Lands in Golden Gate Park, and a packed calendar of street festivals, summer 2026 is the busiest the Bay Area has been in years. Here's what's on — and a local's advice on getting to each one, because parking is about to get historic.</p>
  <h2>The World Cup comes to the Bay (June 11 – July 19)</h2>
  <p>FIFA World Cup matches run at Levi's Stadium in Santa Clara, with fan zones and watch parties across San Francisco, Oakland, and San Jose all tournament long. If you're heading to a match, know this: Levi's Stadium on event days is a traffic event of its own. Pre-booked drop-off beats the parking lots by a wide margin — your driver drops you at the gate, and is waiting at a set pickup point when the final whistle blows.</p>
  <div class="callout"><p><strong>Pro tip:</strong> book match-day rides as round trips with hourly wait. Surge pricing on rideshare after a World Cup match will be brutal; a flat rate locked in weeks ahead won't be.</p></div>
  <h2>Outside Lands — August 7–9, Golden Gate Park</h2>
  <p>The lineup spans pop, rap, R&amp;B and rock — Charli XCX, PinkPantheress, and GloRilla headline the bill. There is functionally no parking near Golden Gate Park during Outside Lands. Get dropped on the park's edge and walk in like the veterans do.</p>
  <h2>Free music all summer</h2>
  <p>The Stern Grove Festival runs free Sunday concerts June 14 through August 16 under the eucalyptus — this year's lineup includes Major Lazer (July 5), Public Enemy (Aug 15), and Al Green (Aug 16). In July, the Fillmore Jazz Festival takes over twelve blocks of Pacific Heights as the largest free jazz festival on the West Coast.</p>
  <h2>Street festival season</h2>
  <ul>
    <li><strong>June:</strong> SF Pride, the Union Street Festival (June 6–7), Juneteenth on Fillmore (June 13), and the North Beach Festival (June 20–21) celebrating the neighborhood's Italian-American and Beat heritage.</li>
    <li><strong>July 4:</strong> fireworks and free entertainment along the waterfront.</li>
    <li><strong>August:</strong> the Pistahan Parade &amp; Festival (Aug 8–9) at Yerba Buena Gardens — the West Coast's largest Filipino celebration.</li>
  </ul>
  <h2>Getting around it all</h2>
  <p>Big-event weekends are exactly when ground transportation falls apart — surge pricing, closed streets, drivers canceling. A pre-booked chauffeur with a flat rate and a fixed pickup point removes all of it. For groups, a Sprinter or party bus turns the ride to the show into part of the night.</p>
  <p><a href="{BOOK}" style="color:var(--orange);font-weight:700">Lock in your event-day ride →</a></p>
</div></section>"""
p += cta_section("Make event days easy.")
p += faq_section(BLOG_FAQ["san-francisco-summer-2026-events"])
p += footer("../")
write("blog/san-francisco-summer-2026-events.html", p)

# ============================ BLOG: NAPA PLAYBOOK ============================
p = head("Napa & Sonoma by Chauffeur: A Day-Trip Playbook | Koast",
         "How to plan a wine country day from San Francisco — routes, timing, how many wineries to visit, and which vehicle fits your group.", "../")
p += nav("../", "blog")
p += f"""
<section class="tight"><div class="wrap article">
  <span class="pill">Wine Country</span>
  <h1>Napa &amp; Sonoma by Chauffeur: A Day-Trip Playbook</h1>
  <div class="meta">By the Koast Team · June 2026 · 5 min read</div>
  <img class="post-hero" src="../img/blog-banner-napa.jpg" alt="Napa Valley vineyards illustration">
  <p>Wine country has exactly one design flaw: somebody has to drive home. Solve that, and a Napa day becomes one of the best days the Bay Area offers. Here's how regulars structure it.</p>
  <h2>The golden rule: 3–4 wineries, no more</h2>
  <p>First-timers try to hit six wineries and remember none of them. Tastings run 60–90 minutes once you factor in the pour, the tour, and the "we should get a case" conversation. Three stops with a long lunch is the perfect day; four is the ceiling.</p>
  <h2>A proven route</h2>
  <ul>
    <li><strong>9:00 AM</strong> — pickup in the city. The drive north over the Golden Gate is part of the experience; ask for the coastal side.</li>
    <li><strong>10:30 AM</strong> — first tasting, the reservation-only one. Morning palates are sharp and crowds are thin.</li>
    <li><strong>12:30 PM</strong> — long lunch in Yountville or Sonoma Square. Book ahead; this is the anchor of the day.</li>
    <li><strong>2:30 &amp; 4:00 PM</strong> — two relaxed afternoon tastings, ending with sparkling or a view patio.</li>
    <li><strong>5:30 PM</strong> — doze on the ride home. Your cases ride in the back.</li>
  </ul>
  <div class="callout"><p><strong>Napa or Sonoma?</strong> Napa is polish — grand estates, cabernet, reservations. Sonoma is charm — family producers, walkable square, easier pace. Healdsburg splits the difference beautifully. Can't decide? They're 30 minutes apart; do one of each.</p></div>
  <h2>Matching the vehicle to the group</h2>
  <p>Two people: a Business Sedan feels right. Four to six: a First-Class SUV gives everyone a window and legroom for the nap home. Eight to fourteen: the Executive Sprinter — the group stays together, and the ride between wineries becomes part of the party. Bigger celebrations ride the party buses.</p>
  <h2>Why hourly charter beats point-to-point</h2>
  <p>Wine tours are booked as one flat hourly rate: your chauffeur waits at every stop, the route flexes when you fall in love with a patio, and there's no app-refreshing in a parking lot with no cell signal. Most days run 6–8 hours door to door.</p>
  <p><a href="../services/wine-tours.html" style="color:var(--orange);font-weight:700">See our wine tour service →</a></p>
</div></section>"""
p += cta_section("Plan your wine country day.")
p += faq_section(BLOG_FAQ["napa-sonoma-chauffeur-day-trip"])
p += footer("../")
write("blog/napa-sonoma-chauffeur-day-trip.html", p)

# ============================ BLOG: NYC GUIDE ============================
p = head("Getting Around New York Without Losing Your Mind | Koast",
         "JFK vs LGA vs EWR, when the subway wins, when a black car is worth it, and how locals move through Manhattan.", "../")
p += nav("../", "blog")
p += f"""
<section class="tight"><div class="wrap article">
  <span class="pill">City Guides</span>
  <h1>Getting Around New York Without Losing Your Mind</h1>
  <div class="meta">By the Koast Team · June 2026 · 5 min read</div>
  <img class="post-hero" src="../img/blog-banner-nyc.jpg" alt="New York City skyline illustration">
  <p>New York has the best and worst ground transportation in America, often on the same block. Here's the honest playbook for moving through it — including when you genuinely don't need us.</p>
  <h2>The three-airport problem</h2>
  <ul>
    <li><strong>JFK</strong> — biggest, busiest, 45–75 minutes to Manhattan depending on the hour. International arrivals + luggage + jet lag = the single strongest case for a pre-booked car anywhere in the city.</li>
    <li><strong>LGA</strong> — closest to Manhattan (25–40 min) and dramatically better than its old reputation, but it has no rail link. A car isn't a luxury at LaGuardia; it's the only direct option.</li>
    <li><strong>EWR</strong> — often the cheapest flight, in New Jersey. 40–60 minutes to Midtown. Watch the tolls on a rideshare; flat-rate quotes include them.</li>
  </ul>
  <h2>When the subway wins</h2>
  <p>Honesty first: for one person going Midtown to Downtown on a weekday, the subway beats any car, ours included. $2.90 and no traffic. Where cars win: airport runs with luggage, three-plus people splitting a ride, late nights, multi-stop days, and any time you're in a suit you'd rather not wear onto the 4 train in July.</p>
  <h2>The Manhattan traffic reality</h2>
  <p>Crosstown traffic is the slowest mile in America — plan around it, never through it. Going up or down the island, the FDR and West Side Highway are your friends. A good chauffeur knows this; it's why pre-booked cars quote times honestly instead of optimistically.</p>
  <div class="callout"><p><strong>Hamptons &amp; weekend escapes:</strong> summer Fridays, Manhattan to the East End runs 2–3 hours. A chauffeured SUV with the whole group beats the Jitney and lets you start the weekend at pickup, not at arrival.</p></div>
  <h2>The bottom line</h2>
  <p>Use the subway when you're light and flexible. Book a car when you're carrying, gathering, or arriving — and book it ahead, because hailing in the rain at rush hour is a rookie move.</p>
  <p><a href="../cities/new-york.html" style="color:var(--orange);font-weight:700">Koast in New York →</a></p>
</div></section>"""
p += cta_section("Ride easy in New York.")
p += faq_section(BLOG_FAQ["nyc-ground-travel-guide"])
p += footer("../")
write("blog/nyc-ground-travel-guide.html", p)

# ============================ BLOG: EA GUIDE ============================
p = head("The EA's Guide to Booking Executive Ground Travel | Koast",
         "How executive assistants coordinate flawless ground transportation — pre-trip checklists, flight tracking, billing, and backup plans.", "../")
p += nav("../", "blog")
p += f"""
<section class="tight"><div class="wrap article">
  <span class="pill">Corporate</span>
  <h1>The EA's Guide to Booking Executive Ground Travel</h1>
  <div class="meta">By the Koast Team · June 2026 · 6 min read</div>
  <img class="post-hero" src="../img/blog-banner-ea-guide.jpg" alt="Executive watching plane from airport window">
  <p>Every executive assistant knows the math: a flawless car booking earns zero credit, and a failed one ruins the whole trip report. This guide is for making ground travel the part of the itinerary nobody thinks about.</p>
  <h2>The non-negotiables</h2>
  <ul>
    <li><strong>Flight-tracked pickups.</strong> Never book a fixed pickup time for an airport arrival. The service should track the tail number and adjust automatically — delays, early landings, gate changes.</li>
    <li><strong>Driver details in advance.</strong> Name, photo, phone number, and vehicle, sent before the trip — forwarded to the principal so there's zero curbside confusion.</li>
    <li><strong>Live visibility.</strong> You should know the pickup happened without texting anyone. GPS tracking and automated status updates are the difference between monitoring and worrying.</li>
    <li><strong>A real human to call.</strong> When plans change at 6 AM, an app chatbot doesn't cut it. Text or call a dispatcher who knows the booking.</li>
  </ul>
  <h2>The pre-trip checklist</h2>
  <ul>
    <li>Confirm your terminal and curbside pickup point</li>
    <li>Add the principal's mobile for direct driver contact — and yours as backup</li>
    <li>Note luggage count and any preferences (temperature, quiet ride, water)</li>
    <li>For multi-stop days, book hourly rather than chaining point-to-points</li>
    <li>Share a one-line itinerary with the dispatcher for context</li>
  </ul>
  <div class="callout"><p><strong>The hourly trick:</strong> any day with 3+ stops or shifting times should be an hourly charter. One chauffeur stays with the schedule all day — no re-booking when the 2 PM runs long.</p></div>
  <h2>Billing that doesn't create work</h2>
  <p>Account-based billing turns twenty ride receipts into one monthly invoice — itemized by rider, trip, and cost center. If you're reconciling individual rideshare receipts for a leadership team, you're doing work the vendor should be doing.</p>
  <h2>Build the relationship once</h2>
  <p>The real upgrade is a service that knows your principals — preferred vehicles, regular routes, standing preferences. First booking takes five minutes; every one after takes one.</p>
  <p><a href="../services/corporate-travel.html" style="color:var(--orange);font-weight:700">Set up a corporate account →</a></p>
</div></section>"""
p += cta_section("Make ground travel the easy part.")
p += faq_section(BLOG_FAQ["ea-guide-executive-ground-travel"])
p += footer("../")
write("blog/ea-guide-executive-ground-travel.html", p)


# ============================ TERMS (ported from koastride.com) ============================
p = head("Terms & Conditions | Koast", "Koast's Terms and Conditions: bookings, cancellations, payments, and liability for our chauffeured transportation services.", "")
p += nav("")
p += f"""
<section class="tight"><div class="wrap article">
  <span class="pill">Legal</span>
  <h1>Terms &amp; Conditions</h1>
  <div class="meta">Version: San Francisco, January 2024</div>

  <h2>1. General provisions</h2>
  <p>Koast, headquartered in San Francisco, California (hereinafter referred to as "Koast") enables its users to book transportation services via its own online platform by integrating third-party online platforms and applications for mobile devices ("apps"; all methods collectively referred to as "Koast Tools"). Koast's service consists of arranging for the transportation of a user by an independent ride service provider (Transportation Service Provider or "TSP"). Koast arranges this business service for the user but does not provide the actual transportation service.</p>
  <p>These General Terms and Conditions ("T&amp;Cs") are part of each agreement of the user concerning Koast's arrangement of business service contracts. They also describe the details of the transportation services for which Koast provides the user a direct claim against a particular TSP.</p>
  <p>Conflicting general terms and conditions of the user are hereby also contradicted in the case of confirmation letters and services accepted without condition. Any terms to the contrary shall only apply insofar as the management of Koast has expressly consented to this in writing.</p>

  <h2>2. Contractual relationship and contract conclusion</h2>
  <p><strong>2.1 Contractual relationship.</strong> Koast does not itself provide the transportation services in connection with the Koast Tools and does not do so by way of third-party agents. Koast only provides the user with a claim for transport against a TSP, which is independent of Koast. For this purpose, Koast concludes the necessary agreements on its own behalf with the TSP that provide the user with a claim for transport against the TSP ("contract for the benefit of third parties"). On this basis, the user is entitled to request the transportation service and any further claims in respect of that service directly from the TSP. Koast and the user only agree to the arrangement of a business service contract and not to the arrangement of the actual transportation services. The claim for compensation by Koast includes the compensation for arranging business services as well as the compensation distributed to the TSP for the transportation services.</p>
  <p><strong>2.2 Conclusion of contract.</strong> By transmitting a completed booking form via the Koast Tools or by making arrangements by telephone with Koast, the user transmits an offer to conclude a business service contract ("ride request"). Koast first transmits an email confirmation of the details of the requested ride service it has received; in so doing, Koast only confirms receipt of the ride request. It is only by separate declaration ("booking confirmation") by email from Koast that the business service contract between Koast and the user is concluded for the desired ride service. The user is then directly entitled vis-à-vis the TSP to request the ride service and to assert further claims in respect of such ride service directly against the TSP.</p>

  <h2>3. Registration obligation</h2>
  <p>The user provides assurance to Koast that all information it transmits or has transmitted to Koast on its behalf by another person is complete and accurate. Registrations by automated processes are prohibited.</p>

  <h2>4. Selected content of the transportation contract</h2>
  <p><strong>4.1 Ride types, service changes.</strong> Depending on local availability, the user can select ride requests that include transfer rides, long-distance rides (transfer rides starting at 100 miles), rides on demand ("chauffeur hailing") and hourly bookings. If the ride actually carried out involves additional expenditure of effort due to requests that differ from the initially requested ride, the TSP will accommodate these requests to the extent possible; additional effort may result in additional costs (see Section 5). Subject to availability, changes may be requested even after conclusion of the contract but may result in additional charges.</p>
  <p>For transfers, long-distance rides and rides on demand, the displayed price is determined on the basis of a start and a destination address; additional stopovers may incur an additional fee. An hourly booking always begins at the booked pickup time and ends in the city area of the pickup location; if the ride completes outside that area, or the booked miles or duration are exceeded, additional fees may apply.</p>
  <p><strong>4.2 Pickup time.</strong> The agreed pickup time is the pickup time specified in the Koast booking confirmation. In the event of an airport pickup for which the user has provided a correct flight number, enabling Koast to track the arrival time, the agreed pickup time will be postponed if the flight is late.</p>
  <p><strong>4.3 Vehicle class, upgrades.</strong> Depending on regional availability, the user can choose from different vehicle classes (for example "Business Class Sedan", "Business Class SUV", "First Class Sedan", "First Class SUV", or "Sprinter Class"). Vehicles shown in the Koast Tools are illustrative examples; there is no right to a particular vehicle model within a booked class. Koast may upgrade a booking to a higher vehicle class at any time at no additional cost, depending on availability: "Business Class Sedan" may be upgraded to "Business Class SUV", "First Class SUV", or "First Class Sedan"; "Business Class SUV" may be upgraded to "First Class SUV". Koast will never downgrade your vehicle to a cheaper vehicle type or a smaller one — for example, sending a Sedan if you reserved an SUV.</p>
  <p><strong>4.4 Transport safety.</strong> The price in the booking confirmation includes the number of pieces of luggage specified in the booking form. Excess or bulky luggage (such as a wheelchair), weapons, or animals must be specified during booking; the TSP may refuse transport of items not agreed upon, including animals not housed in a closed, suitable transport box, except where local law requires accommodation. If the TSP permits carriage of additional items, surcharges may apply. The need for child restraints must be specified in the ride request, including the number and age of children and the type of restraints required. The transport of unaccompanied minors may be rejected by the TSP. The maximum number of passengers and luggage for a specific vehicle is set out in a binding luggage policy; the TSP may refuse transport where space and safety conditions do not permit it. If transport is refused because mandatory requirements were not correctly communicated by the user, Koast remains entitled to compensation.</p>
  <p><strong>4.5 Delays.</strong> Exceptional situations such as air traffic control strikes or inclement weather can only be compensated to a limited extent; in these cases longer waiting times or short-notice cancellations must be accepted.</p>
  <p><strong>4.6 Cancellations, rebookings and no-shows.</strong> For transfer rides, long-distance rides, and hourly bookings, cancellation is free if made more than 24 hours before the agreed pickup time. Between 12–24 hours before pickup, a 50% refund applies. Within 12 hours of pickup, the full price is payable. An effective cancellation can only be carried out by emailing us. Rebookings are generally treated as new bookings, and the cancellation rules apply to the originally agreed ride. A transfer ride is considered a no-show if the guest does not appear within 30 minutes after the agreed pickup time (60 minutes at airports); hourly bookings are a no-show if the guest does not appear by the end of the booked hours. No-show rides must be fully compensated unless a later pickup time was agreed with the TSP.</p>
  <p><strong>4.7 Behavior in the vehicle.</strong> During the entire ride, applicable road traffic rules apply to all guests, particularly seat belt requirements. The TSP's instructions must be followed. Guests may not open doors during the ride, throw objects from the vehicle, extend any body part from or scream from the vehicle. Use of equipment in the vehicle requires the TSP's prior permission. Smoking is prohibited; violations bear the cost of vehicle cleaning and resulting loss of serviceability. Food is discouraged; alcoholic drinks only with prior consent.</p>

  <h2>5. Remuneration and payment</h2>
  <p><strong>5.1 General.</strong> The booking confirmation specifies Koast's remuneration claim. Key factors include the selected vehicle class, route, advance booking time, pickup time and location. Special requests (multilingual chauffeurs, vehicle marking, stopovers, bulky luggage, child seats, etc.) may increase the price.</p>
  <p><strong>5.2 Ride changes.</strong> Ride requests may be changed after the contract concludes and, where possible for the TSP, after the ride begins. Upgrades or additional distance/hours are recalculated and charged per the applicable price schedule; for hourly bookings, each commenced half hour is rounded up. If the booked distance or hours are shortened, the agreed compensation remains unaffected.</p>
  <p><strong>5.3 Waiting times (transfer rides).</strong> No surcharges apply for waiting up to 30 minutes (domestic flights) or 60 minutes (international flights) after the agreed pickup time at airports; for delayed flights, pickup time starts when the plane has landed. In all other cases, no surcharge for the first 5 minutes. Each additional minute is invoiced as follows, plus applicable sales tax:</p>
  <ul>
    <li>Business Class Sedan (Continental, CT5, 5 Series, E-Class, or similar) — $2.08 per minute</li>
    <li>Business Class SUV (Suburban, Expedition, Yukon, or similar) — $2.50 per minute</li>
    <li>First Class SUV with Captain Seats (Escalade, Navigator, or Denali) — $2.91 per minute</li>
  </ul>
  <p><strong>Additional miles for hourly bookings.</strong> Hourly bookings include 20 miles per hour. Additional miles are invoiced separately:</p>
  <ul>
    <li>Business Class Sedan — $5.15 per mile</li>
    <li>Business Class SUV — $6.00 per mile</li>
    <li>First Class SUV with Captain Seats — $7.00 per mile</li>
  </ul>
  <p><strong>5.4 Payment.</strong> Users can pay by credit card; credit card fees are borne by Koast. The user bears transaction fees for payments by transfer. For each payment warning notice Koast may charge a reasonable reminder fee; failed credit card debits may incur the resulting bank/processor expenses plus a reasonable processing fee. Invoices are made available electronically in the user account; credit card payments are due immediately. Vouchers are one-off, individually redeemable, may not be combined, and cannot be redeemed for cash.</p>

  <h2>6. Liability</h2>
  <p>Koast is liable for damages caused by Koast or its vicarious and service agents through intent or gross negligence. The TSP, including its chauffeurs, are neither vicarious nor service agents of Koast for the performance of transportation services. In the event of damages caused by simple negligence, Koast is liable only for the violation of a material contractual obligation and only for foreseeable and typical damages. Limitations of liability do not apply within the scope of warranties provided, in the event of injuries to life, body and health, or for claims arising from the Product Liability Act.</p>
  <p>Koast is not liable for the correctness, reliability, completeness, and validity of content disseminated free of charge within the Koast Tools, except for damages caused intentionally or by gross negligence; nor for the availability and functionality of offered functions; nor for the content, freedom from error, legality, and functionality of third-party websites referred to by links. Koast accepts no responsibility for correct and complete transmission of information (excepting the content of the booking confirmation), nor for disruptions due to force majeure, including failure of communication networks and gateways. The user shall indemnify Koast for all claims and costs, including reasonable legal defense costs, asserted by third parties owing to non-contractual use of the Koast Tools or violation of these T&amp;Cs. No liability is assumed for objects forgotten in the vehicle.</p>

  <h2>7. Amendment of the offer</h2>
  <p>Koast reserves the right to change the Koast Tools at any time in a manner reasonable for the user in order to develop and improve them. Koast may temporarily or permanently terminate its offer for a material reason, even without separately informing the user.</p>

  <h2>8. Protection of content</h2>
  <p>The content within the Koast Tools is protected by copyright. Koast grants the user a revocable right to use the Koast Tools according to their intended purpose, conditioned on compliance with these T&amp;Cs. Any use beyond this scope — changes, copies, re-releases, transmission, dissemination, or other non-intended purposes — is prohibited.</p>

  <h2>9. Final provisions</h2>
  <p>These T&amp;Cs constitute the entire agreement between Koast and the user for the contractually agreed services; there are no collateral agreements, and amendments must be made in writing. The user may only set off against Koast's claims or assert retention rights if counterclaims are legally established or undisputed, and may not assign claims to third parties without Koast's express written consent. The law of the United States of America applies to all legal relations between Koast and the user; the place of fulfillment is San Francisco, and the exclusive place of jurisdiction is San Francisco insofar as the user is a merchant or has no fixed place of residence in the USA. Koast is neither willing nor obliged to participate in dispute resolution proceedings before a consumer arbitration board. Should individual provisions of these T&amp;Cs be or become ineffective, the remaining provisions remain effective and shall be replaced by provisions most closely approximating the intended meaning and economic purpose.</p>

  <p>Questions: <a href="mailto:{EMAIL}" style="color:var(--orange);font-weight:700">{EMAIL}</a></p>
</div></section>"""
p += footer("")
write("terms.html", p)

# ============================ PRIVACY (ported from koastride.com) ============================
p = head("Privacy Policy | Koast", "How Koast collects, uses, and safeguards your personal information.", "")
p += nav("")
p += f"""
<section class="tight"><div class="wrap article">
  <span class="pill">Legal</span>
  <h1>Privacy Policy</h1>
  <p>Koast wants you to know that we value the privacy of your information and will not sell or market your personal information to any other company. However, certain profile information may be used to create specific messages or advertising to you as described further in this privacy policy.</p>
  <p>Koast and/or its corporate affiliates and/or subsidiaries (collectively "Koast," "us," or "we") collects information about you when you use our mobile applications, websites, and other online products and services provided by Koast (collectively, the "Services"), and through other interactions and communications that you may have with us. This Privacy Policy describes how Koast collects and uses the personal information that you provide through the Services, the choices available to you regarding our use of your personal information, and how you can access and update this information.</p>

  <h2>Scope and application</h2>
  <p>This Privacy Policy applies to persons who use our application or access our Services to request transportation, delivery, or other services ("Clients"). It does not apply to information that we collect from or about vehicle drivers, couriers, partner transportation companies, or any other persons or entities (collectively "Drivers"). If you interact with the Services as both a Client and a Driver, the applicable Privacy Policy applies to your different interactions respectively.</p>

  <h2>Collection of information</h2>
  <p><strong>Information you provide to us.</strong> We only collect information that you directly provide, such as when you create or modify your account, request on-demand services, contact customer support, or otherwise communicate with us. This may include: name, email, phone number, postal address, profile picture, payment method, and other information you choose to provide. You can choose not to provide certain information, but then you may not be able to take advantage of many features, including receiving pricing or making a reservation. To use the Services you must first create an account by providing your first and last name, email, and phone number. You may also supply information by participating in a contest or questionnaire, communicating with customer service, providing employer information for a corporate account, providing reviews, or using notification services. We use this information for our general commercial purposes, including responding to your requests, improving and customizing future Services, and communicating with you.</p>
  <p><strong>Information we collect through your use of the Services:</strong></p>
  <ul>
    <li><strong>Location information:</strong> when you permit the Services to access location services, we typically collect the precise location of your trip via your device when the application or website is running. We may also derive approximate location from your IP address.</li>
    <li><strong>Contacts information:</strong> when you permit access to your device address book, we may access and store names and contact information to facilitate social interactions through the Services.</li>
    <li><strong>Transaction information:</strong> service type, date and time, amount charged, distance traveled, and related details. If someone uses your promo code, we may associate your name with that person.</li>
    <li><strong>Usage and preference information:</strong> how you interact with our Services, preferences, and settings, in some cases via cookies, pixel tags, and similar technologies. The website may use cookies to track trip bookings, including abandoned bookings, used to determine when to send booking reminders via SMS and email.</li>
    <li><strong>Device information:</strong> hardware model, operating system and version, software versions, language, unique device identifiers, advertising identifiers, serial number, motion data, and mobile network information.</li>
    <li><strong>Call and SMS data:</strong> in facilitating communications between Clients and Drivers, we receive call data including date, time, the parties' phone numbers, and where applicable the content of SMS messages.</li>
    <li><strong>Log information:</strong> server logs including device IP address, access dates and times, pages viewed, crashes and system activity, browser type, and referring sites or apps.</li>
  </ul>
  <p><strong>Information from other sources.</strong> We may receive information from other sources and combine it with information collected through the Services — for example, from a linked payment provider or social media service, from your employer if it uses one of our enterprise solutions, from Drivers who provide a user rating after a trip, or from your interactions with the Services in another capacity.</p>

  <h2>Use of information</h2>
  <p>We may use the information we collect about you to: provide, maintain, and improve the Services (including facilitating payments, sending receipts, providing requested services, developing new and safety features, authenticating Clients, and sending product updates and administrative messages); perform internal operations (fraud prevention, troubleshooting, data analysis, testing, research, and monitoring usage trends); send or facilitate communications between you and a Driver (such as ETAs) or between you and your contacts at your direction; send you communications we think will interest you, including products, services, promotions, news, and events, where permissible under applicable law, and process promotion entries and awards; and personalize and improve the Services, including features, content, social connections, referrals, and advertisements.</p>
  <p>We may transfer, process, and store information in the United States and other countries, some of which may have less protective data protection laws than your region. Where this is the case, we take appropriate measures to protect your personal information in accordance with this Privacy Policy.</p>

  <h2>Sharing of information</h2>
  <p>We may share your information: with Drivers to enable the transportation services you request (for example your name, photo if provided, average user rating, and pickup/drop-off locations); with other Clients if using a ride-sharing option, or with people you direct us to share with (such as ETA sharing or fare splitting); with third parties to provide a Service you requested through a partnership or promotional offering; with the general public if you submit content to a public forum; with third parties you authorize, such as apps integrating with our API; with third parties to display or manage advertising (you may opt out of interest-based use of your information on other websites; you will continue to receive generic advertisements); and with your employer and necessary third parties (such as expense management providers) if you participate in our enterprise solutions. Text messaging originator opt-in data and consent will not be shared with any third parties.</p>
  <p>We may also share your information: with Koast affiliates and subsidiaries; with independent third-party transportation providers and logistics providers ("Transport Providers") providing services through the Services; with entities that conduct data processing on our behalf; with vendors, consultants, and marketing partners who need access to carry out work on our behalf; in response to a request by a competent authority where disclosure is in accordance with or required by law; with law enforcement or other parties if we believe your actions are inconsistent with our agreements or policies, or to protect the rights, property, or safety of Koast or others; in connection with any merger, sale of assets, consolidation, restructuring, financing, or acquisition; with your consent; and in aggregated and/or anonymized form which cannot reasonably be used to identify you.</p>

  <h2>Social sharing features</h2>
  <p>The Services may integrate with social sharing features that let you share actions you take on our Services with other apps, sites, or media. Use of such features enables sharing with your friends or the public depending on your settings with the social sharing service — refer to their privacy policies. Analytics and advertising services may use cookies, web beacons, SDKs, and other technologies to identify your device when you visit our site and other online services, for audience measurement and to serve and measure advertisements on our behalf.</p>

  <h2>SMS/MMS mobile messaging</h2>
  <p>We will only use your mobile phone numbers with explicit consent provided through our services or via our website. We use the information you provide through the program to transmit your mobile messages and respond to you, which may include sharing with platform providers, phone companies, and other vendors who assist in message delivery. We do not share phone numbers collected through the program with any third party, though we reserve the right to disclose information as necessary to satisfy any law, regulation, or governmental request, avoid liability, or protect our rights or property. When you provide information in connection with the program, you agree to provide accurate, complete, and true information and not to use a false or misleading name. If we believe information is untrue or you opted in for an ulterior purpose, we may refuse access to the program and pursue appropriate legal remedies.</p>

  <h2>Your choices</h2>
  <p><strong>Account information:</strong> you may correct your account information at any time by logging into your Koast account. To cancel your account, contact us at {EMAIL}. We may retain certain information as required by law or for legitimate business purposes.</p>
  <p><strong>Access rights:</strong> Koast will comply with individuals' requests regarding access, correction, objection, and/or deletion of the personal data it stores in accordance with applicable law.</p>
  <p><strong>Location information:</strong> you can disable collection of precise location via your device settings, though this limits certain features and does not limit collection of trip location from a Driver's device or approximate location from your IP address.</p>
  <p><strong>Promotional communications:</strong> opt out by following the "unsubscribe" instructions in those messages. We may still send non-promotional communications about your account, requested services, or ongoing business relations.</p>

  <h2>Google user data (Calendar integration)</h2>
  <p>If you choose to connect your Google Calendar to Koast, we access your Google user data only to provide the features you turn on, and in accordance with the <a href="https://developers.google.com/terms/api-services-user-data-policy" rel="noopener" target="_blank">Google API Services User Data Policy</a>, including its Limited Use requirements.</p>
  <p><strong>What we access:</strong> with your permission, Koast reads your upcoming calendar events (title, time, and location) and can create or update calendar events for rides you book.</p>
  <p><strong>How we use it:</strong> solely to show your schedule alongside your rides, to suggest and correctly time chauffeur pickups for events and flights on your calendar, and to keep ride events on your calendar up to date. We do not use Google user data for advertising, we do not sell it, and no humans read it except with your consent, for security purposes, or where required by law.</p>
  <p><strong>Storage and sharing:</strong> your Google authorization token is stored encrypted; calendar event details are processed to render your schedule and are not shared with third parties. Google user data is never transferred to data brokers or used to build advertising profiles.</p>
  <p><strong>Revoking access:</strong> you can disconnect Google Calendar at any time in the Koast app (Account &rarr; Calendar), which deletes our stored authorization, or via your <a href="https://myaccount.google.com/permissions" rel="noopener" target="_blank">Google account permissions</a>.</p>

  <h2>Your California privacy rights</h2>
  <p>California law permits residents of California to request certain details about how their information is shared with third parties for direct marketing purposes. Koast does not share your personally identifiable information with third parties for the third parties' direct marketing purposes unless you provide us with consent to do so.</p>

  <h2>Changes to this policy</h2>
  <p>We may change this Privacy Policy from time to time. If we make significant changes in the way we treat your personal information, we will provide you notice through the Services or by some other means, such as email.</p>

  <h2>Contact us</h2>
  <p>If you have any questions about this privacy statement, please contact us at <a href="mailto:{EMAIL}" style="color:var(--orange);font-weight:700">{EMAIL}</a> or by email.</p>
</div></section>"""
p += footer("")
write("privacy.html", p)

# ============================ SEO POST-PROCESSING ============================
import re as _re, json as _json, glob as _glob

BASE_URL = "https://koastride.com"

def _schema_for(rel, src, url, title, desc):
    blocks = []
    org = {"@context":"https://schema.org","@type":"LocalBusiness","@id":BASE_URL+"/#org",
        "name":"Koast","description":"Professional chauffeured black car service. Flat-rate pricing, vetted drivers, flight tracking. Bay Area based, serving major cities nationwide.",
        "url":BASE_URL,"email":EMAIL,
        "logo":BASE_URL+"/img/logo-transparent.png","image":BASE_URL+"/img/hero-banner.jpg",
        "slogan":"Ride easy.","priceRange":"$$$",
        "address":{"@type":"PostalAddress","addressLocality":"San Francisco","addressRegion":"CA","addressCountry":"US"},
        "areaServed":[c["name"] for c in CITIES.values()],
        "openingHours":"Mo-Su 00:00-24:00"}
    if rel == "index.html":
        blocks.append(org)
    # FAQ schema from <details> blocks
    faqs = _re.findall(r"<details><summary>(.*?)</summary><p>(.*?)</p></details>", src, _re.S)
    if faqs:
        blocks.append({"@context":"https://schema.org","@type":"FAQPage",
            "mainEntity":[{"@type":"Question","name":_re.sub(r"<.*?>","",q).strip(),
                "acceptedAnswer":{"@type":"Answer","text":_re.sub(r"<.*?>","",a).strip()}} for q,a in faqs]})
    # City/airport pages -> Service schema
    if (rel.startswith("cities/") or rel.startswith("airports/")) and not rel.endswith("index.html"):
        h1 = _re.search(r"<h1>(.*?)</h1>", src, _re.S)
        nm = _re.sub(r"<.*?>","",h1.group(1)).strip() if h1 else title
        blocks.append({"@context":"https://schema.org","@type":"Service","name":nm,
            "serviceType":"Chauffeured black car transportation","provider":{"@id":BASE_URL+"/#org"},
            "url":url,"description":desc})
    # Blog posts -> BlogPosting
    if rel.startswith("blog/") and rel != "blog/index.html":
        h1 = _re.search(r"<h1>(.*?)</h1>", src, _re.S)
        img = _re.search(r'class="post-hero" src="\.\./(img/[^"]+)"', src)
        blocks.append({"@context":"https://schema.org","@type":"BlogPosting",
            "headline":_re.sub(r"<.*?>","",h1.group(1)).strip() if h1 else title,
            "description":desc,"url":url,
            "image":BASE_URL+"/"+img.group(1) if img else BASE_URL+"/img/hero-banner.jpg",
            "datePublished":"2026-06-01","dateModified":"2026-06-12",
            "author":{"@type":"Organization","name":"Koast"},
            "publisher":{"@id":BASE_URL+"/#org"}})
    # BreadcrumbList for section pages
    _crumb_parents = {"cities":("Cities","/cities/index.html"),
                      "airports":("Airports","/services/airport-transfers.html"),
                      "wine-tours":("Wine Tours","/services/wine-tours.html"),
                      "blog":("Guides","/blog/index.html")}
    top = rel.split("/")[0]
    if "/" in rel and top in _crumb_parents and not rel.endswith("index.html"):
        pname, purl = _crumb_parents[top]
        leaf = title.split("|")[0].strip()
        blocks.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":"Home","item":BASE_URL+"/"},
            {"@type":"ListItem","position":2,"name":pname,"item":BASE_URL+purl},
            {"@type":"ListItem","position":3,"name":leaf,"item":url}]})
    return blocks

def enhance():
    pages = sorted(_glob.glob(os.path.join(ROOT,"**","*.html"), recursive=True))
    urls = []
    for fp in pages:
        rel = os.path.relpath(fp, ROOT).replace("\\","/")
        if not CARE_RIDES_LIVE and rel == "services/care-rides.html": continue
        url = BASE_URL + "/" + ("" if rel=="index.html" else rel)
        urls.append(url)
        src = open(fp).read()
        if 'rel="canonical"' in src: continue
        title = _re.search(r"<title>(.*?)</title>", src, _re.S).group(1).strip()
        desc_m = _re.search(r'name="description" content="(.*?)"', src)
        desc = desc_m.group(1) if desc_m else ""
        ogimg = BASE_URL + "/img/og-image.jpg"
        him = _re.search(r'class="post-hero" src="\.\./(img/[^"]+)"', src)
        if him: ogimg = BASE_URL + "/" + him.group(1)
        ogtype = "article" if rel.startswith("blog/") and rel != "blog/index.html" else "website"
        ogdims = '\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">' if ogimg.endswith("og-image.jpg") else ""
        inject = f"""<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" sizes="32x32" href="/img/favicon-32.png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<meta property="og:type" content="{ogtype}">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="Koast">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{ogimg}">{ogdims}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{ogimg}">
"""
        for b in _schema_for(rel, src, url, title, desc):
            inject += '<script type="application/ld+json">' + _json.dumps(b, ensure_ascii=False) + "</script>\n"
        src = src.replace("</head>", inject + "</head>", 1)
        open(fp,"w").write(src)
        print("enhanced", rel)
    # sitemap.xml
    import datetime as _dt
    _today = _dt.date.today().isoformat()
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        sm += f"  <url><loc>{u}</loc><lastmod>{_today}</lastmod></url>\n"
    sm += "</urlset>\n"
    open(os.path.join(ROOT,"sitemap.xml"),"w").write(sm)
    # PWA: manifest + minimal service worker (quiet install eligibility; real prompt ships with the booker portal)
    _manifest = {"name": "Koast — Black Car Service", "short_name": "Koast",
        "description": "Chauffeured black car service. Flat rates, vetted drivers. Ride easy.",
        "start_url": "/", "scope": "/", "display": "standalone",
        "background_color": "#0e1013", "theme_color": "#0e1013",
        "icons": [{"src": "/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/img/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]}
    open(os.path.join(ROOT, "site.webmanifest"), "w").write(_json.dumps(_manifest))
    open(os.path.join(ROOT, "sw.js"), "w").write(
        "self.addEventListener('install',e=>self.skipWaiting());"
        "self.addEventListener('activate',e=>e.waitUntil(clients.claim()));"
        "self.addEventListener('fetch',()=>{});")
    # robots.txt
    open(os.path.join(ROOT,"robots.txt"),"w").write(
f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
""")
    # llms.txt for AI crawlers + the live fact sheet for the chat agent (auto-rebuilt every deploy)
    _care_facts = (", Care Rides (concierge senior and medical appointment transportation)\n"
        "- Care Rides: door-to-door rides for seniors and medical appointments, designed for family members booking on a parent's behalf. "
        "Chauffeur walks the rider to and from the door, offers a steadying arm, stows canes and folding walkers; text status updates go to the family member; "
        "hourly booking lets the chauffeur wait during appointments; recurring schedules (dialysis, PT) can be set up by email; recurring riders are matched with the same chauffeur "
        "whenever possible so they see a familiar, trusted face every time. Riders must be able to walk on their own. Private-pay only (no Medicare/Medicaid/insurance billing). "
        "Koast is not a medical provider: no wheelchair-lift vehicles, no physical transfer assistance — we refer those riders to specialized providers. "
        "Page: https://koastride.com/services/care-rides.html") if CARE_RIDES_LIVE else ""
    cities_list = ", ".join(c["name"] for c in CITIES.values())
    airports_list = ", ".join(f"{a['code']} ({a['name']})" for a in AIRPORTS.values())
    fleet_lines = "\n".join(f"- {v['name']}: {', '.join(v['tags'])} — {v['sub']}" for v in FLEET)
    wine_lines = ""
    for _ws, _wr in WINE_REGIONS.items():
        _wl = WINERIES.get(_ws, [])
        _names = "; ".join(f"{w['name']} ({w['area']}, known for {w['known']}, {w['res'].lower()})" for w in _wl)
        wine_lines += f"- {_wr['name']}: {_wr['drive']}, known for {_wr['known']}. Notable wineries: {_names}\n"
    open(os.path.join(ROOT,"llms.txt"),"w").write(
f"""# Koast — Professional Chauffeured Black Car Service

> Koast is a professional black car and chauffeur service headquartered in San Francisco, California, serving the Bay Area and major U.S. cities nationwide. Motto: "Ride easy."

Key facts:
- Flat-rate, all-inclusive pricing — no surge pricing, ever
- Vetted, commercially licensed and insured professional chauffeurs
- Live flight tracking with free airport wait time (30 min domestic, 60 min international)
- Available 24/7; booking takes under a minute at {BASE_URL} with no account required
- Services: airport transfers, corporate travel with account billing, chauffeured wine tours, events and weddings, hourly charters{_care_facts}
- Cities served: {cities_list}
- Airports served: {airports_list}
- Car seats: forward-facing, rear-facing, and boosters available on request
- Payment: all major credit/debit cards via the secure booking portal
- Contact: {EMAIL}

Fleet:
{fleet_lines}

Wine tour regions:
{wine_lines}

Key pages:
- [Book a ride]({BOOK})
- [Airport transfers]({BASE_URL}/services/airport-transfers.html)
- [Corporate travel]({BASE_URL}/services/corporate-travel.html)
- [Wine tours]({BASE_URL}/services/wine-tours.html)
- [All cities]({BASE_URL}/cities/index.html)
- [Blog]({BASE_URL}/blog/index.html)
""")
    print("sitemap.xml, robots.txt, llms.txt written")


# ============================ BLOG BATCH 2 ============================
def blog_page(slug, title, desc, cat, img, minutes, body, cta):
    p = head(title + " | Koast", desc, "../")
    p += nav("../", "blog")
    p += f"""
<section class="tight"><div class="wrap article">
  <span class="pill">{cat}</span>
  <h1>{title}</h1>
  <div class="meta">By the Koast Team · June 2026 · {minutes} min read</div>
  <img class="post-hero" src="../img/{img}" alt="{title}">
  {body}
</div></section>"""
    if slug in BLOG_FAQ:
        p += faq_section(BLOG_FAQ[slug])
    p += cta_section(cta)
    p += footer("../")
    write(f"blog/{slug}.html", p)

blog_page("lax-airport-black-car-guide",
 "LAX Without the Chaos: The Black Car Pickup Guide",
 "How black car pickup works at LAX — terminal logistics, the LAX-it lot problem, and flat-rate rides to Beverly Hills, Santa Monica & Downtown.",
 "Airport Guides","blog-banner-la.jpg","5", f"""
  <p>LAX moves more origin-and-destination passengers than almost any airport on earth, and its ground transportation shows it. Rideshare pickups happen at the LAX-it lot — a shuttle ride or long walk from your terminal — where waits stretch past 30 minutes on busy evenings. Here's how travelers skip all of it.</p>
  <h2>How chauffeured pickup works at LAX</h2>
  <p>Licensed chauffeured vehicles meet passengers in ways rideshares can't: your driver tracks your flight and is ready the moment you land, helps with your bags, and walks you to the car. No app-refreshing, no lot shuttle, no guessing which curb level. After a long-haul flight into Tom Bradley International, that difference is everything.</p>
  <div class="callout"><p><strong>The math that surprises people:</strong> with surge pricing on weekend evenings, a rideshare to the Westside can exceed a flat-rate black car — while delivering a fraction of the experience.</p></div>
  <h2>Typical drive times from LAX</h2>
  <ul>
    <li><strong>Santa Monica / Venice</strong> — 20–40 minutes depending on the 405</li>
    <li><strong>Beverly Hills / West Hollywood</strong> — 30–50 minutes</li>
    <li><strong>Downtown LA</strong> — 30–60 minutes; avoid 4–7 PM if you can</li>
    <li><strong>Pasadena / Burbank</strong> — 45–75 minutes</li>
  </ul>
  <p>LA traffic is the variable everything bends around. A pre-booked car with a professional who knows when Sepulveda beats the 405 saves real time, not just stress.</p>
  <h2>Booking it</h2>
  <p>Enter your flight and drop-off at <a href="{BOOK}" style="color:var(--orange);font-weight:700">koastride.com</a> for a flat-rate quote — tolls, fees, and gratuity included, with free wait time on every arrival.</p>""",
 "Land at LAX. Leave like a local.")

blog_page("chicago-ohare-midway-guide",
 "O'Hare or Midway? The Chicago Airport Decision",
 "ORD vs MDW — drive times to the Loop, when each airport wins, and how to handle Chicago winter travel by black car.",
 "Airport Guides","blog-banner-chicago.jpg","4", f"""
  <p>Chicago gives you two airports and a real choice. The right answer depends on where you're going, when you land, and how much you trust the weather. Here's the local calculus.</p>
  <h2>The quick comparison</h2>
  <ul>
    <li><strong>O'Hare (ORD)</strong> — the giant: more flights, more delays, 35–60 minutes to the Loop via the Kennedy. Best for international and schedule flexibility.</li>
    <li><strong>Midway (MDW)</strong> — the sleeper pick: smaller, faster to clear, 25–40 minutes to the Loop. If a Midway flight matches your schedule, take it.</li>
  </ul>
  <h2>The winter factor</h2>
  <p>From November to March, Chicago ground transportation is a different sport. Rideshare queues at O'Hare in a snowstorm are legendarily grim, and surge pricing peaks exactly when you least want to negotiate. A pre-booked car with flight tracking absorbs delays automatically — your driver knows your wheels-down time before you do, and free wait time means a customs line or de-icing delay costs you nothing.</p>
  <div class="callout"><p><strong>Suburban tip:</strong> heading to Schaumburg, Naperville, or Evanston? Pre-booked flat rates beat metered options decisively on suburban runs, where rideshare driver availability gets thin.</p></div>
  <h2>Booking it</h2>
  <p>Flat-rate quotes for both airports at <a href="{BOOK}" style="color:var(--orange);font-weight:700">koastride.com</a> — with a professional who's driven the Kennedy in February more times than they can count.</p>""",
 "Chicago winters are hard. Your ride shouldn't be.")

blog_page("vegas-convention-transportation",
 "The Las Vegas Convention Playbook",
 "Moving a team through CES, conventions and trade shows in Las Vegas — group transportation logistics that actually work.",
 "Corporate","blog-banner-vegas.jpg","5", f"""
  <p>Nothing humbles a travel plan like a Las Vegas convention week. 100,000+ attendees, taxi lines that wrap around buildings, and surge pricing that turns a two-mile ride into a forty-dollar decision. If you're bringing a team, logistics are the difference between a productive show and an exhausted one.</p>
  <h2>The convention week reality</h2>
  <p>During CES and the major shows, the distance between your hotel and the convention center matters less than the throughput of the route between them. Monorail queues, rideshare lot waits, and walking in convention shoes all tax your team before the first meeting. The companies that do this well treat transportation as part of the show budget, not an afterthought.</p>
  <h2>What works</h2>
  <ul>
    <li><strong>A dedicated Sprinter on hourly charter</strong> — one vehicle, your schedule, moving 8–14 people between hotel, convention center, and dinners. The vehicle becomes a rolling green room for prep between stops.</li>
    <li><strong>Scheduled airport waves</strong> — book arrivals in clusters so each inbound group is met and moved without anyone standing at LAS baggage claim coordinating by group text.</li>
    <li><strong>Evening shuttle loops</strong> — client dinners and after-events run on time when the ride is standing by, not summoned into a 60-deep queue.</li>
  </ul>
  <div class="callout"><p><strong>Book early:</strong> convention-week vehicle inventory in Vegas sells out weeks ahead. The teams that book with their hotel block, win.</p></div>
  <p>One account, one invoice, every ride visible — <a href="../services/corporate-travel.html" style="color:var(--orange);font-weight:700">set up corporate billing</a> before the show and expense reporting becomes one line item.</p>""",
 "Bring the whole team. Move like one.")

blog_page("miami-getting-around",
 "Getting Around Miami: Brickell, South Beach & Beyond",
 "How Miami traffic actually works — causeway timing, neighborhood logistics, and getting between MIA, Brickell and the Beach.",
 "City Guides","blog-banner-miami.jpg","4", f"""
  <p>Miami looks compact on a map and drives like it isn't. The city's geography — a mainland business district and an island beach community connected by a handful of causeways — means everything comes down to timing your crossings.</p>
  <h2>The causeway rule</h2>
  <p>Between Brickell/Downtown and South Beach, every route funnels onto the MacArthur or Julia Tuttle causeways. Midday, it's a 20-minute hop. Friday evening or event nights, it can triple. Locals plan around the crossings the way San Franciscans plan around the Bay Bridge.</p>
  <h2>Neighborhood quick reference</h2>
  <ul>
    <li><strong>MIA → Brickell</strong> — 15–25 minutes; the easiest airport run in any major US city</li>
    <li><strong>MIA → South Beach</strong> — 20–30 minutes off-peak, more when the beach is busy</li>
    <li><strong>Brickell → Wynwood</strong> — 10–15 minutes for galleries and dinner</li>
    <li><strong>Miami → Palm Beach</strong> — 1.5 hours up I-95 for the day trip</li>
  </ul>
  <div class="callout"><p><strong>Event weeks</strong> — Art Basel, Miami Grand Prix, music festival weekends — transform the whole equation. Surge pricing hits hard and street closures multiply. Those are precisely the weeks a pre-booked flat rate earns its keep.</p></div>
  <p>Flat-rate rides across South Florida at <a href="{BOOK}" style="color:var(--orange);font-weight:700">koastride.com</a> — FLL and Palm Beach included.</p>""",
 "Miami, handled.")

blog_page("denver-mountain-transfers",
 "Denver to the Slopes: The Mountain Transfer Guide",
 "DEN to Vail, Breckenridge & Keystone — what the I-70 drive really takes, and why ski travelers skip the rental car.",
 "Trips","blog-banner-denver.jpg","4", f"""
  <p>Every ski trip to Colorado starts with the same decision at Denver International: rent a car and drive I-70 yourself, or get driven. After one February drive through the Eisenhower Tunnel in weather, most people choose differently the second time.</p>
  <h2>What the drive really takes</h2>
  <ul>
    <li><strong>DEN → Breckenridge / Keystone</strong> — about 2 hours in good conditions</li>
    <li><strong>DEN → Vail</strong> — about 2 hours; add 30–60+ minutes on peak Saturdays</li>
    <li><strong>DEN → Winter Park</strong> — 90 minutes over Berthoud Pass</li>
  </ul>
  <p>"Good conditions" is the operative phrase. I-70 ski traffic on weekend mornings is its own weather system, and chain laws turn rental sedans into roadside ornaments. A chauffeured SUV with a driver who reads CDOT conditions daily — and room for every ski bag — turns the transfer into the first relaxing hours of the vacation.</p>
  <div class="callout"><p><strong>The rental car math:</strong> a week of SUV rental, airport fees, resort parking ($30–50/night at Vail), and the white-knuckle factor — versus two flat-rate transfers and never touching a snow brush. Run it for your group size; it's closer than you'd think, and one of them includes naps.</p></div>
  <p>Book mountain transfers with luggage and gear noted at <a href="{BOOK}" style="color:var(--orange);font-weight:700">koastride.com</a> — your chauffeur tracks the inbound flight and the mountain forecast.</p>""",
 "First chair, not first gear.")

blog_page("black-car-vs-rideshare-cost",
 "Black Car vs. Rideshare: The Real Cost Math",
 "Surge pricing, airport fees, tips, cancellations — an honest cost comparison between rideshare and flat-rate black car service.",
 "Industry","blog-banner-rideshare.jpg","5", f"""
  <p>The sticker price comparison everyone makes — rideshare app quote versus black car rate — misses most of the real math. Here's the honest version, including the cases where rideshare genuinely wins.</p>
  <h2>Where rideshare wins</h2>
  <p>Short, flexible, solo trips in off-peak hours: rideshare is cheaper, full stop. A two-mile hop to dinner on a Tuesday doesn't need a chauffeur. We'd rather tell you that than pretend otherwise.</p>
  <h2>Where the math flips</h2>
  <ul>
    <li><strong>Airport runs at peak times.</strong> Surge multipliers, airport pickup fees, and tip stack onto the quote. A 5 PM Friday airport rideshare routinely lands within a few dollars of a flat-rate black car — and sometimes above it.</li>
    <li><strong>Early-morning critical rides.</strong> The rideshare quote assumes a driver accepts. At 4:30 AM in the suburbs, that's a coin flip — and the cost of a missed flight makes the comparison absurd.</li>
    <li><strong>Groups.</strong> Two rideshare XLs versus one Sprinter: the Sprinter usually wins on price and always wins on the experience of arriving together.</li>
    <li><strong>Multi-stop days.</strong> Four separate rideshares with four waits, versus one hourly charter where the car is simply there each time you walk out.</li>
  </ul>
  <h2>The costs nobody prices in</h2>
  <p>Cancellation roulette before dawn flights. The 25-minute airport lot wait after a redeye. Standing in rain watching the car icon circle. Reimbursement paperwork for twelve separate receipts. Black car pricing is higher on average and dramatically more predictable — what you're buying is the variance.</p>
  <div class="callout"><p><strong>Honest bottom line:</strong> use rideshare for errands. Use a flat rate for anything where being late, wet, or stranded costs more than the fare difference.</p></div>
  <p>See your flat rate in ten seconds at <a href="{BOOK}" style="color:var(--orange);font-weight:700">koastride.com</a>.</p>""",
 "Predictable beats cheap-ish.")

blog_page("choosing-corporate-car-service",
 "How to Choose a Corporate Car Service: 9 Questions to Ask",
 "The vetting checklist for travel managers — insurance, billing, coverage, communication, and the questions vendors hope you don't ask.",
 "Corporate","blog-banner-corporate.jpg","6", f"""
  <p>Picking a corporate ground transportation partner is a decision you make once and live with every travel day. These are the nine questions that separate professional operations from a guy with a nice car.</p>
  <h2>The nine questions</h2>
  <ul>
    <li><strong>1. Are your chauffeurs commercially licensed and insured?</strong> Ask for proof of commercial insurance and permits. This is the bright line between a regulated operation and exposure your legal team won't enjoy discovering.</li>
    <li><strong>2. How does flight tracking work?</strong> "We check flights" is not a system. The right answer involves automatic pickup adjustment with no action from your travelers.</li>
    <li><strong>3. What exactly is included in the rate?</strong> Tolls, airport fees, gratuity, wait time — itemized upfront, or discovered on the invoice?</li>
    <li><strong>4. What's the cancellation policy?</strong> Executive schedules change. Know the windows before you need them.</li>
    <li><strong>5. How does billing work?</strong> One monthly itemized invoice by rider and cost center, or a shoebox of receipts your AP team gets to enjoy?</li>
    <li><strong>6. What cities do you cover?</strong> One partner across your travel footprint beats a vendor per city — one standard, one account, one number to call.</li>
    <li><strong>7. Who do we call when something changes at 6 AM?</strong> A dispatcher who answers, not a support ticket.</li>
    <li><strong>8. How do travelers get driver details?</strong> Name, photo, phone and vehicle before pickup — sent automatically, forwardable to the principal.</li>
    <li><strong>9. Can we book for others easily?</strong> EAs and coordinators do most of the booking. Passenger profiles and book-for-guest flows should take seconds.</li>
  </ul>
  <div class="callout"><p><strong>The tell:</strong> ask question 3 and watch. Vendors with clean answers quote all-inclusive instantly. Vendors with asterisks start explaining.</p></div>
  <p>Koast's answers to all nine: <a href="../services/corporate-travel.html" style="color:var(--orange);font-weight:700">corporate travel</a> — or email {EMAIL} and test how fast a human responds.</p>""",
 "Nine questions. One decision.")

blog_page("chauffeur-terms-glossary",
 "Wait Time, Hourly & Flat Rate: Chauffeur Terms, Explained",
 "The chauffeured transportation glossary — what wait time, hourly charter, flat rate and TSP actually mean for your booking.",
 "Industry","blog-banner-glossary.jpg","4", f"""
  <p>Every industry has vocabulary that insiders stop noticing. Here's what chauffeured transportation terms actually mean — so you know exactly what you're booking.</p>
  <h2>The glossary</h2>
  <ul>
    <li><strong>Flat rate</strong> — a fixed, all-inclusive price quoted before the ride. No meter, no surge. The price you see is the price you pay.</li>
    
    <li><strong>Curbside pickup</strong> — the lighter option: you text when you have your bags, the car pulls up to the curb. Faster if you're traveling light.</li>
    <li><strong>Complimentary wait time</strong> — the included buffer after your flight lands (typically 30 minutes domestic, 60 international) before any waiting charges apply. Crucially, it starts at <em>actual</em> wheels-down, not scheduled arrival.</li>
    <li><strong>Hourly charter (as-directed)</strong> — you book the vehicle and chauffeur by the hour; the route is whatever your day requires. The right structure for multi-stop days, events, and wine tours.</li>
    <li><strong>Transfer</strong> — a simple point-A-to-point-B ride, like an airport run. Priced flat by route.</li>
    <li><strong>Vehicle class</strong> — the tier you book (Business Sedan, First-Class SUV, Sprinter) rather than a specific car. A guaranteed standard, with a model from that class — and reputable operators only ever upgrade, never downgrade.</li>
    <li><strong>Gratuity included</strong> — standard tip is built into the quoted price. No awkward end-of-ride calculation.</li>
  </ul>
  <div class="callout"><p><strong>Why it matters:</strong> most billing surprises in this industry are vocabulary problems. Know these eight terms and no invoice will ever surprise you.</p></div>
  <p>Test your new fluency: <a href="{BOOK}" style="color:var(--orange);font-weight:700">get an instant flat-rate quote</a>.</p>""",
 "Now you speak chauffeur.")

# ============================ WINE REGION PAGES ============================
# ============================ WINERY LISTINGS ============================
WINERIES = {
 "napa-valley": [
  {"name":"Domaine Carneros","area":"Carneros","known":"méthode traditionnelle sparkling wines and Pinot Noir","vibe":"grand Louis XV-style château with terrace vineyard views","res":"Reservations required"},
  {"name":"Stag's Leap Wine Cellars","area":"Stags Leap District","known":"Judgment of Paris-winning Cabernet Sauvignon","vibe":"serene estate with cave tours below the Stags Leap palisades","res":"Reservations required"},
  {"name":"Inglenook","area":"Rutherford","known":"Rubicon Bordeaux-style blends from a historic 1879 estate","vibe":"the Coppola family's storied ivy-covered château and courtyard","res":"Reservations required"},
  {"name":"Frog's Leap Winery","area":"Rutherford","known":"organically farmed Sauvignon Blanc, Zinfandel and Cabernet","vibe":"red barn, gardens and porch tastings on a working farm","res":"Reservations required"},
  {"name":"V. Sattui Winery","area":"St. Helena","known":"a broad estate lineup with an artisan deli and marketplace","vibe":"lively picnic grounds and Italian-style stone winery","res":"Walk-ins welcome"},
  {"name":"Castello di Amorosa","area":"Calistoga","known":"Italian-style reds and the La Castellana super Tuscan blend","vibe":"13th-century-inspired Tuscan castle with towers and caves","res":"Reservations required"},
 ],
 "sonoma": [
  {"name":"Buena Vista Winery","area":"Sonoma","known":"historic Pinot Noir and Chardonnay at California's oldest premium winery","vibe":"1857 stone cellars and storybook grounds","res":"Walk-ins welcome"},
  {"name":"Gundlach Bundschu Winery","area":"Sonoma","known":"estate Gewürztraminer and reds from America's oldest family-owned winery","vibe":"laid-back vineyard courtyard with a six-generation backstory","res":"Reservations recommended"},
  {"name":"Benziger Family Winery","area":"Glen Ellen","known":"biodynamic and certified-sustainable estate wines","vibe":"tractor-tram tours through Sonoma Mountain vineyards","res":"Reservations recommended"},
  {"name":"Chateau St. Jean","area":"Kenwood","known":"the Cinq Cépages Cabernet blend and acclaimed Chardonnays","vibe":"elegant château with formal gardens at Sugarloaf Ridge","res":"Reservations recommended"},
  {"name":"St. Francis Winery & Vineyards","area":"Kenwood","known":"Zinfandel, Merlot and celebrated wine-and-food pairings","vibe":"mission-style winery framed by the Mayacamas Mountains","res":"Reservations recommended"},
  {"name":"Larson Family Winery","area":"Carneros","known":"small-lot Chardonnay, Pinot Noir and Gewürztraminer","vibe":"converted rodeo barn with lawn games, dogs and farm animals","res":"Reservations required"},
 ],
 "healdsburg": [
  {"name":"Jordan Vineyard & Winery","area":"Alexander Valley","known":"age-worthy Cabernet Sauvignon and Russian River Chardonnay","vibe":"ivy-clad French-style château with seated food-and-wine pairings","res":"Reservations required"},
  {"name":"Francis Ford Coppola Winery","area":"Geyserville","known":"the Diamond Collection and approachable everyday bottlings","vibe":"movie-memorabilia museum, restaurant and resort-style pool","res":"Reservations recommended"},
  {"name":"Dry Creek Vineyard","area":"Dry Creek Valley","known":"benchmark Sauvignon Blanc and old-vine Zinfandel","vibe":"ivy-covered, nautical-themed tasting room with picnic lawn","res":"Reservations recommended"},
  {"name":"Ridge Vineyards Lytton Springs","area":"Dry Creek Valley","known":"single-vineyard old-vine Zinfandel field blends","vibe":"eco-friendly straw-bale tasting room amid century-old vines","res":"Reservations recommended"},
  {"name":"Gary Farrell Vineyards & Winery","area":"Russian River Valley","known":"single-vineyard Pinot Noir and Chardonnay","vibe":"hilltop terrace perched above the Russian River","res":"Reservations required"},
  {"name":"Rochioli Vineyards & Winery","area":"Russian River Valley","known":"cult-status estate Pinot Noir from Westside Road","vibe":"modest family tasting room with vineyard-view patio","res":"Reservations required"},
 ],
 "paso-robles": [
  {"name":"DAOU Vineyards","area":"Adelaida District","known":"acclaimed mountaintop Cabernet Sauvignon and Bordeaux-style reds","vibe":"glamorous hilltop estate with sweeping vineyard views","res":"Reservations required"},
  {"name":"JUSTIN Vineyards & Winery","area":"Adelaida District","known":"the iconic ISOSCELES Bordeaux-style blend","vibe":"polished estate with restaurant and manicured grounds","res":"Reservations recommended"},
  {"name":"Tablas Creek Vineyard","area":"Adelaida District","known":"pioneering organic and biodynamic Rhône blends","vibe":"laid-back seated tastings overlooking estate vines","res":"Reservations required"},
  {"name":"Eberle Winery","area":"Highway 46 East","known":"award-winning Cabernet and estate Syrah","vibe":"founding-family winery with underground cave tours","res":"Walk-ins welcome"},
  {"name":"Halter Ranch","area":"Adelaida District","known":"regenerative-organic Rhône and Bordeaux blends","vibe":"grand ranch estate with covered bridge and modern winery","res":"Reservations recommended"},
  {"name":"Turley Wine Cellars","area":"Templeton","known":"old-vine Zinfandel from historic California vineyards","vibe":"cult-favorite tasting room in a rustic farmhouse setting","res":"Reservations recommended"},
 ],
 "santa-ynez": [
  {"name":"Sunstone Winery","area":"Santa Ynez","known":"estate-grown Rhône-style reds and rosé","vibe":"Tuscan-style villa with lavender-lined courtyards","res":"Reservations recommended"},
  {"name":"Fess Parker Winery & Vineyard","area":"Foxen Canyon","known":"Chardonnay, Pinot Noir and Syrah","vibe":"storied ranch estate from the famed Hollywood family","res":"Reservations recommended"},
  {"name":"Firestone Vineyard","area":"Los Olivos","known":"Bordeaux-style reds at Santa Barbara County's first estate winery","vibe":"relaxed hilltop tasting room above sweeping vineyards","res":"Walk-ins welcome"},
  {"name":"The Brander Vineyard","area":"Los Olivos","known":"benchmark Sauvignon Blanc since 1975","vibe":"charming pink chateau with garden courtyard tastings","res":"Walk-ins welcome"},
  {"name":"Gainey Vineyard","area":"Santa Ynez","known":"estate Chardonnay, Pinot Noir and Merlot","vibe":"Spanish-style winery with vineyard-view terraces","res":"Reservations recommended"},
  {"name":"Alma Rosa Winery & Vineyards","area":"Solvang","known":"Sta. Rita Hills Pinot Noir and Chardonnay of Sideways fame","vibe":"stylish tasting room in the Danish village","res":"Reservations recommended"},
 ],
 "livermore": [
  {"name":"Wente Vineyards","area":"Livermore","known":"Chardonnay at America's oldest continuously operated family winery","vibe":"grand estate with gardens, restaurant and cave tours","res":"Reservations recommended"},
  {"name":"Concannon Vineyard","area":"Tesla Road","known":"America's first Petite Sirah on a historic 1883 estate","vibe":"landmark winery with lawns and shaded terraces","res":"Walk-ins welcome"},
  {"name":"Murrieta's Well","area":"Livermore","known":"small-lot estate blends from 1884 vineyard roots","vibe":"intimate historic estate with patio and barrel-room tastings","res":"Reservations recommended"},
  {"name":"McGrail Vineyards and Winery","area":"Greenville Road","known":"estate Cabernet Sauvignon","vibe":"hilltop tasting room with lawn and valley views","res":"Reservations recommended"},
  {"name":"The Steven Kent Winery","area":"Vasco Road","known":"collector-level Cabernet and Bordeaux varietals","vibe":"focused, wine-first tastings in an intimate barrel room","res":"Reservations recommended"},
  {"name":"Las Positas Vineyards","area":"Wetmore Road","known":"estate-grown small-lot wines","vibe":"family-owned winery with patio tastings and live music","res":"Walk-ins welcome"},
 ],
 "temecula": [
  {"name":"Wilson Creek Winery & Vineyard","area":"Rancho California Rd","known":"the famous Almond Sparkling Wine","vibe":"festive family-run estate with creekside grounds","res":"Reservations recommended"},
  {"name":"South Coast Winery Resort & Spa","area":"Rancho California Rd","known":"award-winning sparkling and estate wines","vibe":"full wine-country resort with spa and villas","res":"Reservations recommended"},
  {"name":"Ponte Winery","area":"Rancho California Rd","known":"Italian-inspired estate reds and blends","vibe":"manicured gardens with an acclaimed al fresco restaurant","res":"Reservations recommended"},
  {"name":"Leoness Cellars","area":"De Portola Wine Trail","known":"Rhône-style wines and estate Cabernet","vibe":"French-country hilltop winery with vineyard-view dining","res":"Reservations recommended"},
  {"name":"Doffo Winery","area":"Calle Contento","known":"boutique Malbec, Zinfandel and bold reds","vibe":"micro-boutique family winery with a vintage motorcycle collection","res":"Walk-ins welcome"},
  {"name":"Robert Renzoni Vineyards & Winery","area":"De Portola Wine Trail","known":"estate Italian varietals and Super Tuscan blends","vibe":"old-world Italian winery with brick-oven trattoria","res":"Reservations recommended"},
 ],
 "willamette-valley": [
  {"name":"Domaine Drouhin Oregon","area":"Dundee Hills","known":"Burgundian-style Pinot Noir and Chardonnay","vibe":"hilltop estate with sweeping valley views","res":"Reservations recommended"},
  {"name":"The Eyrie Vineyards","area":"McMinnville","known":"pioneering Oregon Pinot Noir and Pinot Gris","vibe":"historic, intimate in-town tasting room","res":"Reservations required"},
  {"name":"Argyle Winery","area":"Dundee","known":"acclaimed sparkling wines and Pinot Noir","vibe":"stylish tasting house on Dundee's main strip","res":"Reservations recommended"},
  {"name":"Adelsheim Vineyard","area":"Chehalem Mountains","known":"founding-family Pinot Noir and Chardonnay","vibe":"relaxed estate tastings amid vineyard trails","res":"Reservations recommended"},
  {"name":"Brooks Wine","area":"Eola-Amity Hills","known":"biodynamic Riesling and Pinot Noir","vibe":"warm hilltop tasting room with food pairings","res":"Reservations recommended"},
  {"name":"King Estate Winery","area":"South Valley","known":"benchmark Oregon Pinot Gris","vibe":"grand chateau-style estate with organic gardens","res":"Reservations required"},
 ],
 "walla-walla": [
  {"name":"L'Ecole No 41","area":"Lowden","known":"estate Bordeaux blends and Semillon","vibe":"tastings in a restored 1915 schoolhouse","res":"Walk-ins welcome"},
  {"name":"Woodward Canyon Winery","area":"Lowden","known":"old-vine Cabernet Sauvignon from a founding winery","vibe":"homey 1870s farmhouse and garden patio","res":"Walk-ins welcome"},
  {"name":"Long Shadows Vintners","area":"Frenchtown","known":"all-star winemaker collaboration wines","vibe":"sleek tasting room filled with Chihuly glass art","res":"Reservations recommended"},
  {"name":"Dunham Cellars","area":"Airport District","known":"powerhouse Syrah and Cabernet","vibe":"laid-back lounge in a WWII airplane hangar","res":"Walk-ins welcome"},
  {"name":"Pepper Bridge Winery","area":"Southside","known":"estate-grown Merlot and Cabernet Sauvignon","vibe":"seated tastings overlooking the vineyard estate","res":"Reservations recommended"},
  {"name":"Sleight of Hand Cellars","area":"Southside","known":"rock-and-roll Syrahs and Rieslings","vibe":"vinyl-records tasting room where you pick the LP","res":"Walk-ins welcome"},
 ],
 "finger-lakes": [
  {"name":"Dr. Konstantin Frank Winery","area":"Keuka Lake","known":"pioneering dry Riesling and vinifera wines","vibe":"historic estate terrace above Keuka Lake","res":"Reservations recommended"},
  {"name":"Hermann J. Wiemer Vineyard","area":"Seneca Lake","known":"top-rated single-vineyard Rieslings","vibe":"minimalist tastings in a converted barn winery","res":"Reservations recommended"},
  {"name":"Fox Run Vineyards","area":"Seneca Lake","known":"estate Riesling and dry reds","vibe":"friendly family winery with cafe and lake views","res":"Walk-ins welcome"},
  {"name":"Wagner Vineyards Estate Winery","area":"Seneca Lake","known":"wide-ranging Rieslings since 1979","vibe":"octagonal winery with brewery and lakeside cafe","res":"Walk-ins welcome"},
  {"name":"Sheldrake Point Winery","area":"Cayuga Lake","known":"dry Riesling and ice wine","vibe":"lakeshore tasting room steps from the water","res":"Reservations recommended"},
  {"name":"Heron Hill Winery","area":"Keuka Lake","known":"cool-climate Riesling and Chardonnay","vibe":"striking hilltop tasting room over Keuka Lake","res":"Reservations recommended"},
 ],
 "texas-hill-country": [
  {"name":"Becker Vineyards","area":"Stonewall","known":"Viognier and estate-grown classics","vibe":"lavender fields and a German-style stone barn tasting room","res":"Walk-ins welcome"},
  {"name":"William Chris Vineyards","area":"Hye","known":"100% Texas-grown Mourvèdre and field blends","vibe":"seated tastings on a laid-back farmhouse estate","res":"Reservations required"},
  {"name":"Grape Creek Vineyards","area":"Fredericksburg","known":"award-winning Bordeaux- and Italian-style blends","vibe":"Tuscan-style villa among 25 acres of vines","res":"Reservations recommended"},
  {"name":"Pedernales Cellars","area":"Stonewall","known":"Texas Tempranillo and Viognier","vibe":"hilltop deck with sweeping Hill Country views","res":"Reservations recommended"},
  {"name":"Signor Vineyards","area":"Fredericksburg","known":"Rhône-style blends and rosé","vibe":"manicured gardens and a chic French-country wine barn","res":"Reservations recommended"},
  {"name":"Lost Draw Cellars","area":"Johnson City","known":"Texas High Plains Rhône and Spanish varieties","vibe":"modern tasting room on a nine-acre estate vineyard","res":"Reservations recommended"},
 ],
 "virginia": [
  {"name":"Barboursville Vineyards","area":"Monticello AVA","known":"the Octagon Bordeaux-style blend, Nebbiolo and Vermentino","vibe":"historic Italian-owned estate with Jefferson-designed ruins","res":"Reservations recommended"},
  {"name":"King Family Vineyards","area":"Crozet","known":"Meritage and Viognier","vibe":"family farm with Sunday polo beneath the Blue Ridge","res":"Walk-ins welcome"},
  {"name":"Pippin Hill Farm & Vineyards","area":"North Garden","known":"estate wines with farm-to-table pairings","vibe":"polished culinary vineyard with Blue Ridge views","res":"Reservations recommended"},
  {"name":"Stone Tower Winery","area":"Leesburg","known":"Chardonnay and Bordeaux-style estate reds","vibe":"grand hilltop barns atop Hogback Mountain","res":"Walk-ins welcome"},
  {"name":"Breaux Vineyards","area":"Purcellville","known":"Nebbiolo and 13 estate-grown varieties","vibe":"Cajun-spirited hospitality on a 400-acre estate","res":"Reservations recommended"},
  {"name":"Greenhill Vineyards","area":"Middleburg","known":"100% Virginia-grown Chardonnay and Bordeaux-style reds","vibe":"refined, 21-and-over tasting room in hunt country","res":"Reservations recommended"},
 ],
}


import re as _wyre
def wyslug(name):
    s = name.lower().replace("&", "and")
    s = _wyre.sub(r"['.’]", "", s)
    s = _wyre.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

WINERY_DETAIL = {
 "domaine-carneros": {
   "name":"Domaine Carneros","region":"napa-valley","region_name":"Napa Valley",
   "area":"Los Carneros AVA","address":"1240 Duhig Road, Napa, CA 94559","founded":"1987",
   "known":"méthode-traditionnelle sparkling wines and estate Pinot Noir",
   "website":"https://www.domainecarneros.com","res":"Reservations required",
   "miles":"≈50 miles · about an hour","from_sf_short":"About an hour",
   "intro":"A hilltop Champagne-house château at the southern gate of Napa — and the easiest serious tasting to reach from the city.",
   "about_h":"Champagne-house sparkling at the gate of Napa",
   "about":[
     "Domaine Carneros was founded in 1987 by the Champagne house Taittinger, built to make California sparkling wine by the same méthode traditionnelle used in Reims. The château that crowns the hill is modeled on Taittinger's Château de la Marquetterie, and its terrace looks south across the Carneros vineyards toward San Pablo Bay.",
     "It is one of the few Napa estates where tastings are served at your table rather than at a bar — a calm, unhurried way to work through the sparkling lineup.",
   ],
   "tasting":"The house is known for its Brut Cuvée, Brut Rosé, and the late-disgorged Le Rêve Blanc de Blancs, alongside estate Pinot Noir. Seated flights are reservation-only and pair naturally with caviar, oysters, and cheese. All guests are 21 and over.",
   "standout":"Among the most prominent French Champagne investments in California, the château is one of the valley's most photographed landmarks.",
   "desc":"Chauffeured visits to Domaine Carneros, the Taittinger sparkling-wine château in Carneros. Door-to-door from San Francisco, fixed pricing, no one driving home.",
 },
 "stags-leap-wine-cellars": {
   "name":"Stag's Leap Wine Cellars","region":"napa-valley","region_name":"Napa Valley",
   "area":"Stags Leap District AVA","address":"5766 Silverado Trail, Napa, CA 94558","founded":"1970",
   "known":"Judgment of Paris-winning Cabernet Sauvignon",
   "website":"https://www.stagsleapwinecellars.com","res":"Reservations required",
   "miles":"≈60 miles · about 1 hr 15 min","from_sf_short":"About 1 hr 15 min",
   "intro":"The estate whose Cabernet beat Bordeaux in Paris — set against the Stags Leap palisades on the Silverado Trail.",
   "about_h":"The Cabernet that beat Bordeaux",
   "about":[
     "Founded in 1970 by Warren Winiarski, Stag's Leap Wine Cellars made the wine that changed Napa's reputation overnight. Today the estate is owned by the Antinori family of Tuscany.",
     "Tastings look out over the famed SLV and FAY vineyards, with a temperature-controlled cave Great Room at the heart of the visit.",
   ],
   "tasting":"Cabernet Sauvignon is the focus — the flagship CASK 23, the single-vineyard SLV and FAY bottlings, and the approachable ARTEMIS, plus the KARIA Chardonnay. Visits are seated and by reservation; the estate is 21 and over.",
   "standout":"Its 1973 Cabernet took first place at the 1976 Judgment of Paris, beating Bordeaux's first-growths; a bottle now sits in the Smithsonian.",
   "desc":"Chauffeured trips to Stag's Leap Wine Cellars in Napa — home of the Judgment of Paris Cabernet. Fixed pricing, door-to-door from SF.",
 },
 "inglenook": {
   "name":"Inglenook","region":"napa-valley","region_name":"Napa Valley",
   "area":"Rutherford AVA","address":"1991 St. Helena Highway, Rutherford, CA 94573","founded":"1879",
   "known":"Rubicon Bordeaux-style blends from a historic 1879 estate",
   "website":"https://www.inglenook.com","res":"Reservations required",
   "miles":"≈65 miles · about 1 hr 30 min","from_sf_short":"About 1 hr 30 min",
   "intro":"Francis Ford Coppola's storied 1879 Rutherford estate — château-grand and deeply historic.",
   "about_h":"An 1879 estate, restored",
   "about":[
     "Inglenook was founded in 1879 by Finnish sea captain Gustave Niebaum and became one of Napa's most acclaimed estates. Francis Ford Coppola began reuniting the property in 1975 and reclaimed the original Inglenook name in 2011, restoring both the land and the brand.",
     "The 1880s château sits on a vast estate on the Rutherford Bench, with a museum-like sense of Napa history throughout.",
   ],
   "tasting":"The estate is known for Rubicon, its Cabernet-based Bordeaux-style blend, along with estate Cabernet Sauvignon, Cabernet Franc, and the Blancaneaux white. Tastings and tours run by reservation.",
   "standout":"One of Napa's oldest and most significant estates, and the only major valley winery owned by a famous filmmaker — reassembled over 36 years.",
   "desc":"Chauffeured visits to Inglenook, Coppola's historic 1879 Rutherford estate. Door-to-door from San Francisco, fixed upfront pricing, and no one driving home.",
 },
 "frogs-leap-winery": {
   "name":"Frog's Leap Winery","region":"napa-valley","region_name":"Napa Valley",
   "area":"Rutherford AVA","address":"8815 Conn Creek Road, Rutherford, CA 94573","founded":"1981",
   "known":"organically farmed Sauvignon Blanc, Zinfandel and Cabernet",
   "website":"https://www.frogsleap.com","res":"Reservations recommended",
   "miles":"≈65 miles · about 1 hr 30 min","from_sf_short":"About 1 hr 30 min",
   "intro":"A green, dry-farmed Rutherford original — relaxed porch tastings around a historic red barn.",
   "about_h":"Organic, dry-farmed, and refreshingly unfussy",
   "about":[
     "Frog's Leap was founded in 1981 by John Williams and built its name on organic, dry-farmed, lower-alcohol wines and a deliberately playful identity. The name nods to the property's past as a frog farm.",
     "Tastings happen around the historic Red Barn and its gardens — a casual, conversation-friendly counterpoint to Napa's grander estates.",
   ],
   "tasting":"Look for Sauvignon Blanc, Cabernet Sauvignon, Zinfandel, Merlot, and the Shale & Stone Chardonnay, all from organic, dry-farmed fruit. Garden and house tastings are best booked ahead, and the winery is closed Wednesdays.",
   "standout":"A pioneer of organic and dry-farming in Napa — sustainability-minded long before it was fashionable.",
   "desc":"Private chauffeured trips to Frog's Leap, the organic dry-farmed winery in Rutherford. Door-to-door from San Francisco, fixed pricing, no one driving home.",
 },
 "v-sattui-winery": {
   "name":"V. Sattui Winery","region":"napa-valley","region_name":"Napa Valley",
   "area":"St. Helena","address":"1111 White Lane, St. Helena, CA 94574","founded":"1885",
   "known":"a broad estate lineup with an artisan deli and marketplace",
   "website":"https://www.vsattui.com","res":"Walk-ins welcome",
   "miles":"≈70 miles · about 1 hr 30 min","from_sf_short":"About 1 hr 30 min",
   "intro":"A St. Helena institution — picnic grounds, a famous deli, and bottles you can only buy here.",
   "about_h":"A St. Helena picnic institution",
   "about":[
     "V. Sattui traces to 1885, when Vittorio Sattui founded it in San Francisco; it closed during Prohibition and was reopened in St. Helena in 1976 by his great-grandson Dario Sattui. 2026 marks 50 years in the valley.",
     "The Italian-style stone winery anchors two-and-a-half acres of shaded picnic grounds and a large marketplace deli — one of Napa's most popular, family-friendly stops.",
   ],
   "tasting":"The estate pours a broad lineup, from Cabernet Sauvignon and reserve reds to whites, rosé, sparkling, and dessert wines — sold only at the winery or online. Walk-ins are welcome, but weekend reservations are wise, and the on-site deli makes it the valley's classic picnic stop.",
   "standout":"One of Napa's most-visited wineries; its founder's descendant also built nearby Castello di Amorosa.",
   "desc":"Chauffeured visits to V. Sattui Winery in St. Helena — Napa's classic deli-and-picnic estate. Door-to-door from San Francisco, fixed pricing, no driving home.",
 },
 "castello-di-amorosa": {
   "name":"Castello di Amorosa","region":"napa-valley","region_name":"Napa Valley",
   "area":"Calistoga","address":"4045 St. Helena Highway, Calistoga, CA 94515","founded":"2007",
   "known":"Italian-style reds and the La Castellana super Tuscan blend",
   "website":"https://www.castellodiamorosa.com","res":"Reservations required",
   "miles":"≈75 miles · about 1 hr 30–1 hr 50 min","from_sf_short":"About 1 hr 30 min",
   "intro":"A genuine medieval Tuscan castle at the north end of the valley — Napa's most theatrical destination winery.",
   "about_h":"A real Tuscan castle in Calistoga",
   "about":[
     "Castello di Amorosa opened in 2007 after Dario Sattui spent more than a decade building an authentically styled, 13th-century-inspired Tuscan castle using period materials and methods.",
     "The 121-room castle has a drawbridge, moat, towers, a frescoed great hall, and a vast barrel cellar — a destination as much for the architecture as the wine, and a hit with families.",
   ],
   "tasting":"Italian-leaning reds lead the list — including the La Castellana Super Tuscan-style blend and Il Barone Cabernet — alongside whites, rosé, and sparkling, many sold only at the castle. Tours and tastings are by reservation.",
   "standout":"One of the most elaborate castle wineries in North America, built over roughly 14 years.",
   "desc":"Chauffeured visits to Castello di Amorosa, the medieval Tuscan castle winery in Calistoga. Door-to-door from San Francisco, fixed pricing, no one driving home.",
 },
}

import json as _wjload
try:
    _extra = _wjload.load(open(os.path.join(ROOT, "wineries_extra.json"), encoding="utf-8"))
    for _o in _extra:
        _sl = wyslug(_o["name"])
        if _sl not in WINERY_DETAIL:
            WINERY_DETAIL[_sl] = _o
except FileNotFoundError:
    pass

def winery_section(slug, nm):
    wl = WINERIES.get(slug, [])
    if not wl: return ""
    import json as _wj
    def cap(s): return s[:1].upper() + s[1:]
    import re as _wre, os as _wos
    rows = ""
    for w in wl:
        cls = "req" if w["res"] == "Reservations required" else ("walk" if w["res"] == "Walk-ins welcome" else "")
        wslug = wyslug(w["name"])
        thumb = ""
        if _wos.path.exists(os.path.join(ROOT, "img", "wy-" + wslug + ".jpg")):
            thumb = '<img class="wthumb" src="../img/wy-' + wslug + '.jpg" alt="' + w["name"] + '" loading="lazy">'
        badge = '<span class="wres ' + cls + '">' + w["res"] + '</span>'
        inner = (thumb + '<div class="wmain"><b>' + w["name"] + '</b>'
                 '<span class="warea">' + w["area"] + '</span>'
                 '<p>' + cap(w["known"]) + ' &middot; ' + w["vibe"] + '.</p></div>' + badge)
        if wslug in WINERY_DETAIL:
            rows += '<a class="wrow wrow-link" href="../wineries/' + wslug + '.html">' + inner + '</a>'
        else:
            rows += '<div class="wrow">' + inner + '</div>'
    ilist = _wj.dumps({"@context":"https://schema.org","@type":"ItemList",
        "name":"Notable wineries in " + nm,
        "itemListElement":[{"@type":"ListItem","position":i+1,"name":w["name"]} for i,w in enumerate(wl)]}, ensure_ascii=False)
    return ('<section class="tight"><div class="wrap">'
            '<div class="sec-head"><span class="pill">Where Regulars Stop</span>'
            '<h2>' + nm + ' wineries we love driving to</h2>'
            '<p style="color:var(--muted)">A few favorites from years of ' + nm + ' runs — tell us your taste and we\'ll build the route around them.</p></div>'
            '<div class="wlist">' + rows + '</div>'
            '<script type="application/ld+json">' + ilist + '</script>'
            '</div></section>')


for slug, r in WINE_REGIONS.items():
    nm = r["name"]
    _wd = f"Private chauffeured wine tours in {nm} — {r['known']}. Your wineries, your pace, one fixed price. Book 24/7."
    if len(_wd) > 158: _wd = _wd[:155].rsplit(' ', 1)[0].rstrip(' ,—-') + "…"
    p = head(f"{nm} Wine Tours by Private Chauffeur | Koast", _wd, "../")
    p += nav("../", "wine")
    p += f"""
<header class="hero-dark"><div class="wrap">
  <div class="crumbs"><a href="../index.html">Home</a><span>/</span><a href="../services/wine-tours.html">Wine Tours</a><span>/</span>{nm}</div>
  <div class="hero-grid">
    <div class="hero-copy">
      <h1>{nm} wine tours, <span class="o">chauffeured.</span></h1>
      <p class="lede">Your wineries, your pace, nobody driving home but us — {r['drive']}.</p>
      <ul class="check" style="color:#cdd3dc">
        <li>Hourly charter with a dedicated chauffeur</li>
        <li>Known for {r['known']}</li>
        <li>Door-to-door from your home or hotel</li>
      </ul>
    </div>
    {book_card()}
  </div>
</div></header>
<section class="tight"><div class="wrap grid-2" style="align-items:center;gap:60px">
  <div>
    <span class="pill">The {nm} Day</span>
    <h2 style="font-size:32px;margin:14px 0 16px">How regulars do {nm}</h2>
    <p style="color:var(--muted);margin-bottom:20px">{nm} is {r['drive']}, known for {r['known']}. Most tours anchor around {r['towns']} — three to four tastings with a long lunch in the middle.</p>
    <ul class="check">
      <li>Morning pickup, reservation-only tasting first</li>
      <li>Long lunch — we'll suggest spots in {r['towns'].split(',')[0]}</li>
      <li>Two relaxed afternoon stops; route flexes as the day unfolds</li>
      <li>Cases ride safely in the back on the way home</li>
    </ul>
  </div>
  <div>
    <h3 style="margin-bottom:16px">Match the vehicle to the group</h3>
    {routes_table([("Couples & small groups — Business Sedan / SUV","1–6 guests"),("Friends & celebrations — First-Class SUV","up to 6"),("The whole crew — Executive Sprinter","up to 14"),("Big celebrations — Party Bus","up to 32")], "Group", "Guests")}
  </div>
</div></section>"""
    p += winery_section(slug, nm)
    p += faq_section([
      (f"How is a {nm} wine tour priced?",
       "As an hourly charter — one flat hourly rate covering the vehicle, your dedicated chauffeur, water, and all driving. Most days run 6–8 hours door to door."),
      r["faq"],
      ("Can you help plan the winery lineup?",
       "Yes — tell us your taste and group size and we'll suggest a route, and can coordinate timed tasting reservations."),
    ], f"{nm} questions")
    p += plan_trip([
      ("Guides", [(f"../blog/{g}.html", GUIDE_TITLE[g], "✦") for g in WINE_BLOGS.get(slug, []) + ["group-wine-tour-planning"]]),
      ("Getting there", [(f"../cities/{ct}.html", f"From {CITIES[ct]['name']}", "→") for ct in WINE_CITY.get(slug, []) if ct in CITIES]),
    ])
    p += cta_section(f"Plan your {nm} day.", "Tell us your date and group size — we'll handle everything else.")
    p += footer("../")
    write(f"wine-tours/{slug}.html", p)


# ============================ INDIVIDUAL WINERY PAGES ============================
def winery_page(wslug, d):
    import json as _wj2
    nm = d["name"]; rs = d["region"]; rn = WINE_REGIONS[rs]["name"]
    gw = CITIES[WINE_CITY[rs][0]]["name"] if WINE_CITY.get(rs) else "the city"
    drive = WINE_REGIONS[rs]["drive"]
    drive_cap = drive[:1].upper() + drive[1:]
    dist = d.get("miles", drive)
    url = BASE_URL + "/wineries/" + wslug + ".html"
    region_url = BASE_URL + "/wine-tours/" + rs + ".html"
    title = f"{nm} Car Service & Wine Tours | Koast"
    if len(title) > 60: title = f"{nm} Car Service | Koast"
    res_low = d["res"].lower()
    if "required" in res_low:
        res_faq_q = f"Do we need a reservation at {nm}?"
        res_faq_a = (f"{nm} tastings are seated and by reservation. Tell us your date and group size and "
                     f"we'll help time your visit and build the day around it.")
    elif "recommended" in res_low:
        res_faq_q = f"Do we need a reservation at {nm}?"
        res_faq_a = (f"Reservations are recommended at {nm}, especially on weekends. Give us your date and "
                     f"group size and we'll help line up timed tastings across your stops.")
    else:
        res_faq_q = f"Can we just walk in at {nm}?"
        res_faq_a = (f"{nm} welcomes walk-ins, but weekends fill up. We can help you time the visit and add "
                     f"reservations at the other stops on your day.")

    p = head(title, d["desc"], "../")
    p += nav("../", "wine")
    about_html = "".join(
        f'<p style="color:var(--muted);margin-bottom:16px">{para}</p>' for para in d["about"])
    p += f"""
<header class="hero-dark"><div class="wrap">
  <div class="crumbs"><a href="../index.html">Home</a><span>/</span><a href="../services/wine-tours.html">Wine Tours</a><span>/</span><a href="../wine-tours/{rs}.html">{rn}</a><span>/</span>{nm}</div>
  <div class="hero-grid">
    <div class="hero-copy">
      <span class="wy-eyebrow">{rn} &middot; {d["area"]}</span>
      <h1>{nm}, <span class="o">chauffeured.</span></h1>
      <p class="lede">{d["intro"]}</p>
      <ul class="check" style="color:#cdd3dc">
        <li>Known for {d["known"]}</li>
        <li>{drive_cap}</li>
        <li>Door-to-door &mdash; nobody driving home but us</li>
      </ul>
    </div>
    {book_card()}
  </div>
</div></header>
<section class="tight"><div class="wrap grid-2" style="align-items:start;gap:60px">
  <div>
    <span class="pill">About {nm}</span>
    <h2 style="font-size:clamp(28px,3.4vw,36px);margin:14px 0 16px">{d["about_h"]}</h2>
    {about_html}
    <h3 style="margin:22px 0 10px">What you'll taste</h3>
    <p style="color:var(--muted);margin-bottom:16px">{d["tasting"]}</p>
    <p style="color:var(--muted)"><strong style="color:var(--ink)">Worth knowing:</strong> {d["standout"]}</p>
  </div>
  <div>
    <div class="wy-facts">
      <h3>{nm} at a glance</h3>
      <div class="wy-row"><span class="wy-k">Region</span><span class="wy-v">{rn} &middot; {d["area"]}</span></div>
      <div class="wy-row"><span class="wy-k">Address</span><span class="wy-v">{d["address"]}</span></div>
      <div class="wy-row"><span class="wy-k">Founded</span><span class="wy-v">{d["founded"]}</span></div>
      <div class="wy-row"><span class="wy-k">Known for</span><span class="wy-v">{d["known"][:1].upper() + d["known"][1:]}</span></div>
      <div class="wy-row"><span class="wy-k">Visits</span><span class="wy-v">{d["res"]}</span></div>
      <div class="wy-row"><span class="wy-k">Getting there</span><span class="wy-v">{dist}</span></div>
      <div class="wy-row"><span class="wy-k">Website</span><span class="wy-v"><a href="{d["website"]}" target="_blank" rel="noopener nofollow">{d["website"].replace("https://www.","").replace("https://","").rstrip("/")}</a></span></div>
    </div>
  </div>
</div></section>
<section class="tight"><div class="wrap grid-2" style="align-items:center;gap:60px">
  <div>
    <span class="pill">Getting there</span>
    <h2 style="font-size:clamp(28px,3.4vw,36px);margin:14px 0 16px">Why chauffeur the visit</h2>
    <ul class="check">
      <li>Door-to-door from your home or hotel &mdash; {dist}</li>
      <li>Hourly charter: the car and chauffeur stay with you all day</li>
      <li>Nobody in your group skips a pour to drive</li>
      <li>Cases ride safely in the back on the way home</li>
      <li>One fixed price, quoted upfront</li>
    </ul>
    <a class="btn btn-orange btn-lg" href="{BOOK}" style="margin-top:8px">Get an Instant Quote</a>
  </div>
  <div>
    <h3 style="margin-bottom:16px">Match the vehicle to the group</h3>
    {routes_table([("Couples &amp; small groups &mdash; Business Sedan / SUV","1–6 guests"),("Friends &amp; celebrations &mdash; First-Class SUV","up to 6"),("The whole crew &mdash; Executive Sprinter","up to 14"),("Big celebrations &mdash; Party Bus","up to 32")], "Group", "Guests")}
  </div>
</div></section>"""
    p += faq_section([
      (f"Can you drive us to {nm}?",
       f"Yes. We run private door-to-door trips to {nm} from {gw} and the surrounding area "
       f"({drive}). You're picked up at your home or hotel and brought home the same way, with no one in your group driving."),
      (f"How does pricing work for a trip to {nm}?",
       "As an hourly charter: one flat hourly rate covering the vehicle, your dedicated chauffeur, water, and all "
       "driving for the day. You get the price upfront — no surge, no surprises."),
      (res_faq_q, res_faq_a),
      ("Can we visit other wineries the same day?",
       f"Absolutely. Most {rn} days are three to four tastings with a long lunch. Tell us your taste and we'll "
       "suggest a route and keep the car with you all day."),
    ], f"{nm} questions")
    _sibs = [s for s, v in WINERY_DETAIL.items() if v.get("region") == rs and s != wslug]
    p += plan_trip([
      (f"More {rn} wineries", [(f"{s}.html", WINERY_DETAIL[s]["name"], "✦") for s in _sibs]),
      (f"{rn} day", [(f"../wine-tours/{rs}.html", f"{rn} wine tours", "→")]),
      ("Getting there", [(f"../cities/{ct}.html", f"From {CITIES[ct]['name']}", "→") for ct in WINE_CITY.get(rs, []) if ct in CITIES]),
    ])
    p += cta_section(f"Plan your {nm} visit.", "Tell us your date and group size — we'll handle the rest.")
    p += footer("../")
    service = {"@context":"https://schema.org","@type":"Service",
        "name":f"Chauffeured wine tours to {nm}",
        "serviceType":"Chauffeured black car transportation",
        "provider":{"@id":BASE_URL+"/#org"},"areaServed":rn,"url":url,"description":d["desc"]}
    crumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":BASE_URL+"/"},
        {"@type":"ListItem","position":2,"name":"Wine Tours","item":BASE_URL+"/services/wine-tours.html"},
        {"@type":"ListItem","position":3,"name":rn,"item":region_url},
        {"@type":"ListItem","position":4,"name":nm,"item":url}]}
    p += ('<script type="application/ld+json">' + _wj2.dumps(service, ensure_ascii=False) + "</script>"
          '<script type="application/ld+json">' + _wj2.dumps(crumb, ensure_ascii=False) + "</script>")
    write(f"wineries/{wslug}.html", p)

def wineries_index():
    import json as _wj3
    secs = ""
    listitems = []
    pos = 0
    for rs in WINE_REGIONS:
        rn = WINE_REGIONS[rs]["name"]
        drive = WINE_REGIONS[rs]["drive"]
        items = [(s, v) for s, v in WINERY_DETAIL.items() if v.get("region") == rs]
        if not items:
            continue
        rows = ""
        for s, v in items:
            pos += 1
            listitems.append({"@type": "ListItem", "position": pos, "name": v["name"], "item": BASE_URL + "/wineries/" + s + ".html"})
            cls = "req" if v["res"] == "Reservations required" else ("walk" if v["res"] == "Walk-ins welcome" else "")
            rows += ('<a class="wrow wrow-link" href="' + s + '.html"><div class="wmain"><b>' + v["name"] + '</b>'
                     '<span class="warea">' + v["area"] + '</span>'
                     '<p>' + v["known"][:1].upper() + v["known"][1:] + '.</p></div>'
                     '<span class="wres ' + cls + '">' + v["res"] + '</span></a>')
        secs += ('<section class="tight wreg"><div class="wrap">'
                 '<div class="sec-head"><h2 style="margin-bottom:6px"><a href="../wine-tours/' + rs + '.html" style="color:inherit;text-decoration:none">' + rn + ' &rarr;</a></h2>'
                 '<p style="color:var(--muted)">' + drive[:1].upper() + drive[1:] + '</p></div>'
                 '<div class="wlist">' + rows + '</div></div></section>')
    total = sum(1 for v in WINERY_DETAIL.values() if v.get("region"))
    p = head("All Wineries We Drive To — Chauffeured Wine Tours | Koast",
             "Browse every winery Koast chauffeurs visit — Napa, Sonoma, Paso Robles, Willamette, Walla Walla, Finger Lakes, Texas and more. Door-to-door, fixed pricing.", "../")
    p += nav("../", "wine")
    p += ('<header class="hero-dark"><div class="wrap">'
          '<div class="crumbs"><a href="../index.html">Home</a><span>/</span><a href="../services/wine-tours.html">Wine Tours</a><span>/</span>Wineries</div>'
          '<div class="hero-grid"><div class="hero-copy">'
          '<span class="wy-eyebrow">' + str(total) + ' wineries &middot; 12 regions</span>'
          '<h1>Every winery we <span class="o">drive to.</span></h1>'
          '<p class="lede">Pick a winery and we build the day around it &mdash; door-to-door, one fixed price, and nobody in your group driving home.</p>'
          '<a class="btn btn-orange btn-lg" href="' + BOOK + '" style="margin-top:10px">Get an Instant Quote</a>'
          '</div></div></div></header>')
    p += ('<section class="tight" style="padding-bottom:0"><div class="wrap">'
          '<div class="ksearch" style="margin:0 auto">'
          '<input id="wysearch" type="search" placeholder="Search 72 wineries — name, town, or wine…" aria-label="Search wineries">'
          '</div></div></section>')
    p += secs
    p += ("<script>(function(){var i=document.getElementById('wysearch');if(!i)return;"
          "i.addEventListener('input',function(){var q=i.value.trim().toLowerCase();"
          "document.querySelectorAll('.wreg').forEach(function(sec){var v=0;"
          "sec.querySelectorAll('.wrow-link').forEach(function(r){"
          "var h=!q||r.textContent.toLowerCase().indexOf(q)>-1;r.style.display=h?'':'none';if(h)v++;});"
          "sec.style.display=v?'':'none';});});})();</script>")
    p += cta_section("Plan your wine country day.", "Tell us your date, group size, and which wineries — we'll handle the rest.")
    p += footer("../")
    p += '<script type="application/ld+json">' + _wj3.dumps({"@context": "https://schema.org", "@type": "CollectionPage", "name": "Wineries Koast drives to", "url": BASE_URL + "/wineries/index.html", "mainEntity": {"@type": "ItemList", "itemListElement": listitems}}, ensure_ascii=False) + '</script>'
    return p

for _wslug, _wd in WINERY_DETAIL.items():
    winery_page(_wslug, _wd)
write("wineries/index.html", wineries_index())
for _rslug, _rd in ROUTES.items():
    route_page(_rslug, _rd)

# ============================ OCCASION PAGES (weddings, party bus) ============================
OCCASIONS = {
 "weddings": {
   "navlabel":"Weddings","image":"svc-weddings.jpg",
   "alt":"Black luxury SUV outside a vineyard winery estate at sunset",
   "title":"Wedding Transportation | Chauffeured Cars & Party Buses | Koast",
   "desc":"Chauffeured wedding transportation — sedans, SUVs, Sprinters and party buses for the couple, wedding party and guests. Flat-rate and on-time.",
   "eyebrow":"Weddings & celebrations",
   "h1":"Wedding transportation, <span class=\"o\">handled.</span>",
   "lede":"From the couple's getaway car to guest shuttles and the wedding-party bus — flat-rate, on-time, and one less thing to worry about on the day.",
   "hero_check":["Door-to-door for the couple, the party, and guests","Vehicles for two or for the whole celebration","Flat-rate, booked and confirmed in advance"],
   "about_h":"The detail nobody notices when it's done right",
   "about":[
     "A wedding day runs on timing, and transportation is where it quietly succeeds or falls apart. A late shuttle, a guest stranded at the hotel, a couple waiting on a car that never confirmed — those are the moments people remember. We make sure they don't happen.",
     "Koast handles the whole day: the couple's car, the wedding party, and guest shuttles between hotel, ceremony, and reception. Professional, licensed chauffeurs, fixed pricing agreed in advance, and a schedule we hold to.",
   ],
   "cover_h":"What we cover",
   "cover":["A dedicated car for the couple — arrival and the getaway","The wedding party in an SUV or Executive Sprinter, kept together","Guest shuttles by party bus between hotel, ceremony, and reception","Venue-to-venue moves on a coordinated timeline","Late-night returns so everyone gets home safe"],
   "vehicles":[("Couple & VIPs — Business / First-Class SUV","1–6"),("Wedding party — Executive Sprinter","up to 14"),("Guests — Mid-size party bus","groups"),("Large party — Large party bus","25+")],
   "related":[("Wine country weddings",[("../wine-tours/napa-valley.html","Napa Valley wine tours","→"),("../wine-tours/sonoma.html","Sonoma wine tours","→")]),("Getting there",[("../services/airport-transfers.html","Airport transfers","→"),("../routes/sfo-to-napa.html","SFO to Napa","→")])],
   "faqs":[
     ("How far in advance should we book wedding transportation?","As early as you can — popular dates and larger vehicles book out months ahead, especially in wine country and peak season. Once your date and venues are set, lock the cars in."),
     ("Can you shuttle our guests, not just the couple?","Yes — we run guest shuttles between hotels, ceremony, and reception with party buses and Sprinters, plus a dedicated car for the couple and the wedding party."),
     ("Can we book multiple vehicles?","Absolutely. A typical wedding uses a getaway car for the couple, an SUV or Sprinter for the wedding party, and a party bus or two for guests — all coordinated on one schedule."),
     ("How does pricing work?","Flat-rate and quoted up front — by the trip for point-to-point, or hourly when you want vehicles on standby through the day. No surge, no surprises on the invoice."),
     ("What areas do you cover?","The Bay Area and wine country are home, and we serve major cities nationwide — tell us your venues and we'll build the plan."),
   ],
 },
 "party-bus": {
   "navlabel":"Party Bus","image":"svc-party-bus.jpg",
   "alt":"Black luxury party bus on a city street at night",
   "title":"Party Bus Rental with Driver | Black Car Service | Koast",
   "desc":"Chauffeured party bus and group transportation — birthdays, bachelorette parties, wine tours, nights out and corporate events. Flat-rate, vetted drivers.",
   "eyebrow":"Group celebrations",
   "h1":"Party bus, <span class=\"o\">fully chauffeured.</span>",
   "lede":"Birthdays, bachelorette and bachelor parties, wine tours, and big nights out — your group stays together, nobody drives, and the ride is part of the night.",
   "hero_check":["Mid-size and large party buses with a professional driver","One flat hourly rate — no surge, no per-head app math","Wine tours, nights out, birthdays, corporate events"],
   "about_h":"The whole group, together, all night",
   "about":[
     "The point of a party bus is simple: the group stays together and nobody has to drive. No three cars getting separated in traffic, no designated driver sitting out the fun, no surge pricing at 1 a.m. when everyone's ready to head home.",
     "Koast runs party buses and large coaches with a professional, licensed chauffeur at the wheel. You book by the hour, the bus stays with you across every stop, and the ride between places becomes part of the celebration.",
   ],
   "cover_h":"Built for the occasion",
   "cover":["Bachelorette and bachelor parties","Birthdays and milestone celebrations","Wine-country tours, winery to winery","Concerts, games, and nights out","Corporate events and team outings"],
   "vehicles":[("Smaller groups — Executive Sprinter","up to 14"),("Mid-size party bus","groups & events"),("Large party bus","25+"),("Need two? We'll coordinate","any size")],
   "related":[("Popular for",[("../services/wine-tours.html","Wine tours","→"),("../services/corporate-travel.html","Corporate events","→")]),("Wine country",[("../wine-tours/napa-valley.html","Napa Valley","→"),("../wine-tours/sonoma.html","Sonoma","→")])],
   "faqs":[
     ("How many people fit on a party bus?","We run mid-size and large party buses — the large bus seats 25 or more — plus an Executive Sprinter for smaller groups. Tell us your headcount and we'll match the vehicle."),
     ("How does party bus pricing work?","One flat hourly rate covering the bus, your professional driver, and all the driving — no surge and no per-person app math. You get the price up front."),
     ("Can you do a wine tour on the party bus?","Yes — it's one of the most popular uses. Book hourly and the bus stays with you winery to winery, with cases riding safely in the back."),
     ("Can we make multiple stops?","Of course. The bus and driver stay with you all night across dinners, bars, and venues, so nobody's re-summoning a ride between stops."),
     ("How far ahead should we book?","Weekends and peak season fill up fast, so book as soon as your date is set — especially for larger groups."),
   ],
 },
}

def occasion_page(slug, d):
    import json as _oj
    url = BASE_URL + "/services/" + slug + ".html"
    hero_check = "".join(f"<li>{x}</li>" for x in d["hero_check"])
    about_html = "".join(f'<p style="color:var(--muted);margin-bottom:16px">{p}</p>' for p in d["about"])
    def _cc(x):
        if " — " in x:
            a,b = x.split(" — ",1)
            return f'<div class="card"><p style="margin:0;font-weight:700;color:var(--ink)">{a}</p><p style="margin:6px 0 0;font-size:14px;color:var(--muted);line-height:1.5">{b}</p></div>'
        return f'<div class="card"><p style="margin:0;font-weight:600;color:var(--ink);line-height:1.45">{x}</p></div>'
    cover_cards = "".join(_cc(x) for x in d["cover"])
    p = head(d["title"], d["desc"], "../")
    p += nav("../", "")
    p += f"""
<header class="hero-dark"><div class="wrap">
  <div class="crumbs"><a href="../index.html">Home</a><span>/</span>{d["navlabel"]}</div>
  <div class="hero-grid">
    <div class="hero-copy">
      <span class="wy-eyebrow">{d["eyebrow"]}</span>
      <h1>{d["h1"]}</h1>
      <p class="lede">{d["lede"]}</p>
      <ul class="check" style="color:#cdd3dc">{hero_check}</ul>
    </div>
    {book_card()}
  </div>
</div></header>
<section class="tight"><div class="wrap grid-2" style="align-items:center;gap:55px">
  <div><img class="post-hero" src="../img/{d["image"]}" alt="{d["alt"]}" loading="lazy" style="width:100%;height:auto;border-radius:16px;display:block"></div>
  <div>
    <span class="pill">Overview</span>
    <h2 style="font-size:clamp(28px,3.4vw,36px);margin:14px 0 16px">{d["about_h"]}</h2>
    {about_html}
  </div>
</div></section>
<section class="tight" style="padding-top:0"><div class="wrap grid-2" style="align-items:center;gap:55px">
  <div>
    <span class="pill pill-orange">{d["cover_h"]}</span>
    <div class="grid-2" style="margin-top:14px;gap:12px">{cover_cards}</div>
  </div>
  <div>
    <div class="sec-head"><span class="pill pill-orange">Vehicles</span><h2 style="font-size:24px;margin-top:8px">Match the vehicle to the group</h2></div>
    {routes_table(d["vehicles"], "Vehicle", "Group")}
  </div>
</div></section>
<section class="tight"><div class="wrap">
  <div class="sec-head center"><span class="pill">Why Koast</span><h2>Flat-rate, professional, on time</h2></div>
  <div class="grid-2">
    {feat("receipt","o","Flat-rate pricing","One fixed price quoted upfront — no surge, and no per-head app math.")}
    {feat("shield","t","Vetted chauffeurs","Licensed, insured, and professionally vetted — not a rotating app driver.")}
    {feat("users","o","Your group, together","Book by the hour and the vehicle stays with you across every stop.")}
    {feat("globe","t","Bay Area & beyond","Home in the Bay Area and wine country, serving major cities nationwide.")}
  </div>
  <div style="text-align:center;margin-top:30px"><a class="btn btn-orange btn-lg" href="{BOOK}">Get an Instant Quote</a></div>
</div></section>"""
    p += faq_section(d["faqs"], f"{d['navlabel']} questions")
    p += plan_trip(d["related"])
    p += cta_section(f"Plan your {d['navlabel'].lower()} ride.", "Tell us your date, group size, and stops — we'll handle the rest.")
    p += footer("../")
    service = {"@context":"https://schema.org","@type":"Service","name":d["title"].split("|")[0].strip(),
        "serviceType":"Chauffeured group and event transportation","provider":{"@id":BASE_URL+"/#org"},
        "url":url,"description":d["desc"]}
    crumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":BASE_URL+"/"},
        {"@type":"ListItem","position":2,"name":d["navlabel"],"item":url}]}
    p += ('<script type="application/ld+json">'+_oj.dumps(service,ensure_ascii=False)+"</script>"
          '<script type="application/ld+json">'+_oj.dumps(crumb,ensure_ascii=False)+"</script>")
    write(f"services/{slug}.html", p)

for _oslug, _od in OCCASIONS.items():
    occasion_page(_oslug, _od)




# ============================ BLOG BATCH 3 ============================
blog_page("austin-festival-season",
 "Austin Festival Season, Survived",
 "SXSW, ACL and F1 weekend transportation in Austin — how to move when half a million visitors hit town.",
 "City Events","city-austin.jpg","4", f"""
  <p>Austin triples its energy several times a year — SXSW in March, ACL's two October weekends, F1 in the fall. The music is world-class. The transportation situation, famously, is not. Here's how people who do these events every year handle it.</p>
  <h2>The festival math</h2>
  <p>Downtown street closures shrink the road grid exactly when demand peaks. Rideshare surge during SXSW evenings is legendary, and the pickup zones move daily. The pros book scheduled rides at fixed times — into downtown before panels, out after the last showcase — and treat the quote they got in February as locked.</p>
  <h2>What works</h2>
  <ul>
    <li><strong>Hourly charters for teams.</strong> Brand and label teams keep one Sprinter on call all day — it becomes the mobile green room between venues.</li>
    <li><strong>Scheduled AUS runs.</strong> The airport is only 15–25 minutes out, but festival-week traffic makes that 45+. Pre-booked pickup with flight tracking takes the gamble out.</li>
    <li><strong>Out-of-center stays.</strong> Staying by the Domain? A fixed-rate evening loop beats parking downtown twice over.</li>
  </ul>
  <div class="callout"><p><strong>Book early:</strong> festival-week vehicles in Austin sell out weeks ahead — reserve when you book the hotel, not the week of.</p></div>
  <p>Flat-rate festival rides at <a href="{BOOK}" style="color:var(--orange);font-weight:700">koastride.com</a>.</p>""",
 "Festival days, handled.")

blog_page("boston-logan-guide",
 "Logan Airport Done Right",
 "Boston Logan transfers — the tunnels, the Ted Williams, terminal logistics, and why pre-booked wins in Boston.",
 "Airport Guides","city-boston.jpg","4", f"""
  <p>Logan is closer to downtown than almost any major US airport — 15 to 30 minutes — and yet it produces outsized transportation misery. The reason is geography: water on every side, and every route funneling through tunnels.</p>
  <h2>The tunnel problem</h2>
  <p>The Ted Williams, Sumner, and Callahan tunnels are the only ways across the harbor, and at rush hour they meter the whole city's airport traffic. A good driver knows which tunnel wins at which hour — and when the Tobin around the top beats them all.</p>
  <h2>Terminal notes</h2>
  <ul>
    <li><strong>Terminal E</strong> (international) — the rideshare scrum after a long-haul arrival is grim. A flight-tracked pickup timed to your landing is the move.</li>
    <li><strong>Terminals A–C</strong> — tighter curbs; curbside pickup works if you're carry-on light and communicative.</li>
    <li><strong>Winter</strong> — Boston snow days break app-based dispatch first. Pre-booked cars with committed drivers keep showing up.</li>
  </ul>
  <div class="callout"><p><strong>Beyond the city:</strong> Cambridge runs add 10 minutes; Providence about an hour; Cape traffic is its own season. All flat-rate quoted upfront.</p></div>
  <p>Flight-tracked Logan pickups at <a href="{BOOK}" style="color:var(--orange);font-weight:700">koastride.com</a>.</p>""",
 "Logan, minus the tunnel anxiety.")

blog_page("seattle-getting-around",
 "Getting Around Seattle & the Eastside",
 "Seattle transportation guide — timing the 520 and I-90 bridges, Sea-Tac runs, and moving between downtown and Bellevue.",
 "City Guides","city-seattle.jpg","4", f"""
  <p>Seattle is really two cities: the downtown core and the Eastside tech corridor — Bellevue, Redmond, Kirkland — with Lake Washington in between. Your whole transportation experience comes down to when you cross it.</p>
  <h2>The bridge rule</h2>
  <p>Two floating bridges — the 520 and I-90 — carry everything between the halves. Midday they're a breeze; at the wrong hour they're parking lots with a view of the lake. Locals plan meetings around crossings the way they plan around the rain: with quiet fatalism and good timing.</p>
  <h2>The runs that matter</h2>
  <ul>
    <li><strong>Sea-Tac → downtown</strong> — 25–40 minutes; the light rail is decent solo, a car wins with luggage or colleagues</li>
    <li><strong>Sea-Tac → Bellevue/Redmond</strong> — 30–50 minutes; no direct rail, this is car territory</li>
    <li><strong>Campus-to-campus days</strong> — investor and partner visits often hit both sides of the lake; an hourly charter absorbs the bridge variance</li>
  </ul>
  <div class="callout"><p><strong>Rain reality:</strong> Seattle drizzle barely slows traffic — but the first real downpour of fall reliably breaks it. Book ahead in October.</p></div>
  <p>Flat rates across the Sound at <a href="{BOOK}" style="color:var(--orange);font-weight:700">koastride.com</a>.</p>""",
 "Both sides of the lake, easy.")

blog_page("dc-airport-decision",
 "DCA, IAD or BWI? The D.C. Decision",
 "Washington D.C.'s three airports compared — drive times, when each wins, and getting downtown from National, Dulles, or BWI.",
 "Airport Guides","city-washington-dc.jpg","4", f"""
  <p>Washington gives you three airports in three directions, and choosing wrong costs you an hour. Here's the capital calculus.</p>
  <h2>The three options</h2>
  <ul>
    <li><strong>DCA (National)</strong> — 15–25 minutes to downtown, practically in the city. If a DCA flight exists at a sane price, take it. Period.</li>
    <li><strong>IAD (Dulles)</strong> — the international workhorse, 40–60 minutes out in Virginia. Beautiful terminal, long ride; this is where pre-booked cars earn their keep.</li>
    <li><strong>BWI (Baltimore)</strong> — often the cheapest fares, 50–70 minutes from the District. The fare savings evaporate if you don't plan the ground leg.</li>
  </ul>
  <h2>Capital specifics</h2>
  <p>Government and contractor travel runs on punctuality and discretion — drivers who know which building entrance, invoices that survive an audit. Security perimeters and motorcades reroute traffic without notice; drivers who work D.C. daily route around them by habit.</p>
  <div class="callout"><p><strong>The Tysons factor:</strong> if your meetings are in Tysons or Reston, Dulles is actually the convenient airport — 25 minutes against National's 40 in traffic.</p></div>
  <p>All three airports, flat-rate, at <a href="{BOOK}" style="color:var(--orange);font-weight:700">koastride.com</a>.</p>""",
 "Three airports. Zero guesswork.")

blog_page("sonoma-first-timers",
 "A First-Timer's Day in Sonoma",
 "How to plan your first Sonoma wine tasting day — the square, the valley wineries, and a relaxed three-stop itinerary.",
 "Wine Country","blog-banner-sonoma.jpg","4", f"""
  <p>Sonoma converts people. Visitors come expecting a smaller Napa and leave preferring the original — family producers, tastings poured by people who made the wine, and a town square you can wander between stops.</p>
  <h2>The shape of the day</h2>
  <ul>
    <li><strong>10:30 AM</strong> — first tasting in the valley proper; book this one ahead. Morning pours with the fog just lifting are the best of the day.</li>
    <li><strong>12:30 PM</strong> — lunch on the historic plaza. The square's restaurants fill by 1; reserve or go early.</li>
    <li><strong>2:30 PM</strong> — an estate stop toward Glen Ellen or Kenwood, where the Valley of the Moon does its golden afternoon thing.</li>
    <li><strong>4:00 PM</strong> — optional third tasting or cheese shop raid on the square before the easy ride home.</li>
  </ul>
  <h2>Why three stops, not five</h2>
  <p>Sonoma rewards lingering. The producers here have time to talk — rushing to a fourth appointment means missing the conversations that make the region what it is.</p>
  <div class="callout"><p><strong>Getting there:</strong> 1 to 1.5 hours from San Francisco, and the whole point is that nobody in your group drives any of it. <a href="../wine-tours/sonoma.html" style="color:var(--teal-dark);font-weight:700">Our Sonoma tours →</a></p></div>""",
 "Sonoma, properly done.")

blog_page("temecula-balloons-tastings",
 "Temecula: Balloons at Dawn, Tastings by Noon",
 "The Temecula Valley double feature — sunrise hot-air balloon over the vineyards, then a chauffeured tasting day.",
 "Wine Country","blog-banner-temecula.jpg","4", f"""
  <p>No California wine region does mornings like Temecula. At sunrise, dozens of hot-air balloons drift over the vines; by noon, the same people who watched the valley from a basket are tasting through it on the ground. It's Southern California's best one-day show.</p>
  <h2>The balloon-to-bottle day</h2>
  <ul>
    <li><strong>5:30 AM</strong> — pickup from San Diego or Orange County; balloon companies launch at first light</li>
    <li><strong>6:30–8:00 AM</strong> — the flight: vineyards, ranches, and on clear days the ocean</li>
    <li><strong>9:00 AM</strong> — champagne landing breakfast (a ballooning tradition we endorse)</li>
    <li><strong>11:00 AM–4:00 PM</strong> — tastings along the De Portola trail and Rancho California Road, lunch at a winery restaurant</li>
    <li><strong>5:00 PM</strong> — asleep in the back seat by Oceanside. Perfect day.</li>
  </ul>
  <div class="callout"><p><strong>The logistics catch:</strong> balloon launches and tastings are 15+ minutes apart, and everyone wants a mimosa at breakfast — this is the definition of a day that needs a chauffeur. One vehicle, dawn to dusk. <a href="../wine-tours/temecula.html" style="color:var(--teal-dark);font-weight:700">Our Temecula tours →</a></p></div>""",
 "Up at dawn. Pouring by noon.")

blog_page("willamette-pinot-weekend",
 "A Pinot Weekend in the Willamette Valley",
 "Planning a Willamette Valley wine weekend — Dundee Hills, McMinnville, and why Oregon's Pinot country rewards two days.",
 "Wine Country","blog-banner-willamette.jpg","4", f"""
  <p>Oregon's Willamette Valley makes Pinot Noir that goes bottle-for-bottle with Burgundy, in a setting that still feels like farm country. It's an hour from Portland and a world away — and it's best done as a weekend, not a sprint.</p>
  <h2>The two-day shape</h2>
  <ul>
    <li><strong>Day one: Dundee Hills.</strong> The red volcanic soils that made the valley's name. Three tastings, lunch in Dundee, sunset from a hilltop estate.</li>
    <li><strong>Day two: McMinnville &amp; Carlton.</strong> Smaller producers, the best small-town main street in Oregon wine, and a slower pace home.</li>
  </ul>
  <h2>When to go</h2>
  <p>Harvest (September–October) is the spectacle. But winter is the secret: tasting rooms are quiet, fires are lit, and the winemaker is often the one pouring. Bring a coat; skip the crowds.</p>
  <div class="callout"><p><strong>Getting around:</strong> valley roads are dark, winding, and cell-patchy — exactly the place a dedicated chauffeur turns a good weekend into a relaxed one. We run multi-day charters from Portland. <a href="../wine-tours/willamette-valley.html" style="color:var(--teal-dark);font-weight:700">Our Willamette tours →</a></p></div>""",
 "Pinot country, properly paced.")

blog_page("group-wine-tour-planning",
 "How to Plan a Group Wine Tour: 7 Decisions",
 "Planning a group wine tasting trip — group size, region choice, reservations, lunch, pacing, and the vehicle math.",
 "Wine Country","blog-banner-winegroup.jpg","5", f"""
  <p>Group wine days are either the best day of the year or a logistics headache, and the difference is decided before anyone pours. Seven decisions, in order:</p>
  <h2>The seven</h2>
  <ul>
    <li><strong>1. Group size first.</strong> Everything keys off this. Six fits an SUV and intimate tastings; fourteen needs a Sprinter and group-friendly wineries; thirty needs a bus and advance winery approval.</li>
    <li><strong>2. Region to match the vibe.</strong> Celebration energy → Temecula or Sonoma. Serious tasters → Napa or Willamette. Short notice from the Bay → Livermore.</li>
    <li><strong>3. Reservations, always.</strong> Post-2020, walk-ins are dead for groups. Most wineries cap groups at 8 without special arrangement — book 3–4 weeks out and state your exact headcount.</li>
    <li><strong>4. Two or three wineries, not five.</strong> Groups move slowly. Two tastings plus a long lunch beats four rushed pours every time.</li>
    <li><strong>5. Lunch is load-bearing.</strong> Book a real sit-down meal between tastings. A picnic at a winery that allows it is the upgrade move.</li>
    <li><strong>6. Set the pickup time honestly.</strong> Add 30 minutes to whatever the group thinks it needs to get moving in the morning.</li>
    <li><strong>7. The vehicle decides the day.</strong> One vehicle keeps the group together, kills the "who's driving" question, and lets everyone actually taste. That's the whole point.</li>
  </ul>
  <div class="callout"><p><strong>Make it easy:</strong> tell us the headcount, region, and date — we'll match the vehicle, plan the route timing, and keep the day on rails. <a href="../services/wine-tours.html" style="color:var(--teal-dark);font-weight:700">Plan a group wine tour →</a></p></div>""",
 "One vehicle. Zero designated drivers.")


# ============================ SUPPORT PAGE ============================
sp = head("Support & FAQs | Koast Black Car Service",
          "Get help with your Koast booking — contact us by email, and find detailed answers on pricing, airport pickups, changes, and vehicles.")
sp += nav("", "support")
sp += f"""
<header class="hero-dark"><div class="wrap">
  <div class="crumbs"><a href="index.html">Home</a><span>/</span>Support</div>
  <h1>How can we <span class="o">help?</span></h1>
  <p class="lede">Real humans, 24/7. Most questions are answered below — and the best way to reach us is email.</p>
</div></header>
<section class="tight" style="padding-bottom:0"><div class="wrap">
  <div class="ask-agent aa-live">
    <div class="aa-copy">
      <h2>Ask our agent</h2>
      <p>Instant answers about booking, airports, pricing rules, and the fleet — 24/7, in seconds. For anything personal, a human is one email away.</p>
      <div class="aa-chips">
        <button onclick="kaiAsk(this.textContent)">How does airport pickup work?</button>
        <button onclick="kaiAsk(this.textContent)">What's included in the price?</button>
        <button onclick="kaiAsk(this.textContent)">Can you handle a group of 20?</button>
      </div>
    </div>
    <div class="kai">
      <div class="kai-head"><span class="kcoin">K</span><div><b>Koast Agent</b><small>Online — answers in seconds</small></div></div>
      <div class="kai-msgs" id="kai-msgs">
        <div class="km bot">Hi! I'm Koast's agent. Ask me anything about booking, airports, the fleet, or how pricing works.</div>
      </div>
      <div class="kai-foot">
        <input id="kai-in" type="text" placeholder="Type a question…" maxlength="500">
        <button id="kai-send" aria-label="Send">→</button>
      </div>
      <a class="kai-sms" href="mailto:reserve@koastride.com">Prefer a human? Email us →</a>
    </div>
  </div>
  <style>#kchat-fab,#kchat{{display:none!important}}</style>
  <script>
  (function(){{
    var URL_="{CHAT_WORKER_URL}";
    var msgs=document.getElementById('kai-msgs'),inp=document.getElementById('kai-in'),btn=document.getElementById('kai-send');
    var hist=[],busy=false;
    function add(cls,text){{var d=document.createElement('div');d.className='km '+cls;d.textContent=text;msgs.appendChild(d);msgs.scrollTop=msgs.scrollHeight;return d;}}
    window.kaiAsk=function(q){{inp.value=q;send();inp.focus();}};
    function send(){{
      var q=inp.value.trim();if(!q||busy)return;
      inp.value='';busy=true;
      add('user',q);hist.push({{role:'user',content:q}});
      var dots=add('bot dots','…');
      fetch(URL_,{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{messages:hist}})}})
        .then(function(r){{return r.json()}})
        .then(function(d){{
          dots.remove();
          var a=d.reply||"Sorry — something went wrong. Email us at reserve@koastride.com and a human will help.";
          add('bot',a);hist.push({{role:'assistant',content:a}});busy=false;
        }})
        .catch(function(){{
          dots.remove();
          add('bot',"I can't connect right now — email us at reserve@koastride.com and a real person will answer.");
          busy=false;
        }});
    }}
    btn.addEventListener('click',send);
    inp.addEventListener('keydown',function(e){{if(e.key==='Enter')send();}});
  }})();
  </script>
</div></section>
<section class="tight"><div class="wrap">
  <div class="sec-head center"><span class="pill">Contact</span><h2>Talk to us</h2></div>
  <div class="grid-3">
    <a class="card" href="{BOOK}" style="text-align:center">
      <div style="font-size:13px;font-weight:800;letter-spacing:.1em;color:var(--teal);margin-bottom:8px">BOOK</div>
      <h3 style="font-size:20px">Get a quote</h3>
      <div class="sub" style="margin-top:6px">Fixed price, instant — no account needed</div>
    </a>
    <a class="card" href="mailto:{EMAIL}" style="text-align:center">
      <div style="font-size:13px;font-weight:800;letter-spacing:.1em;color:var(--orange);margin-bottom:8px">EMAIL</div>
      <h3 style="font-size:20px">{EMAIL}</h3>
      <div class="sub" style="margin-top:6px">Quotes, invoices &amp; corporate</div>
    </a>
    <a class="card" href="https://customer.moovs.app/koast/new/info" style="text-align:center">
      <div style="font-size:13px;font-weight:800;letter-spacing:.1em;color:var(--teal);margin-bottom:8px">MANAGE BOOKING</div>
      <h3 style="font-size:20px">Rider portal</h3>
      <div class="sub" style="margin-top:6px">View, change or review your trips</div>
    </a>
  </div>
</div></section>"""

SUPPORT_FAQS = [
 ("Booking & quotes", [
  ("How do I get a quote?",
   "Enter your pickup, drop-off, and time in the booking widget on any page — you'll see an instant, all-inclusive price for each vehicle class. No account needed to get a quote."),
  ("How far in advance should I book?",
   "Same-day rides are often available, but we recommend booking 24+ hours ahead for early-morning airport runs, and 1–2 weeks ahead for weekends, events, and wine tours so your preferred vehicle is available."),
  ("Can I book by email instead of online?",
   f"Absolutely — email {EMAIL} any time and we'll set it up for you. It's usually the fastest way to book."),
  ("Do you do last-minute pickups?",
   "Often, yes — availability depends on your city and time. Email us your pickup location and we'll confirm within minutes."),
  ("Can I book a multi-stop or hourly trip?",
   "Yes. Choose Hourly in the booking widget for as-directed service with multiple stops, or add stops to a one-way trip. Hourly is usually the better value once you have three or more stops."),
 ]),
 ("Pricing & payments", [
  ("Is the price really all-inclusive?",
   "Yes. Your quote includes the fare, tolls, airport fees, taxes, and standard gratuity — itemized upfront. The price you see is the price you pay."),
  ("Do you ever surge price?",
   "Never. Rates are flat regardless of demand, weather, or time of night."),
  ("How do I pay?",
   "All major credit and debit cards through our secure booking portal. Corporate clients can set up account billing with consolidated monthly invoices."),
  ("Is gratuity included?",
   "A standard gratuity is included and itemized in your quote. Additional tipping is never expected — though chauffeurs always appreciate it for exceptional service."),
 ]),
 ("Airport pickups", [
  ("Where does my chauffeur meet me?",
   "Your chauffeur tracks your flight and is ready when you land, with pickup timed to your actual arrival. You'll receive your chauffeur's name, photo, phone number, and live location before you land."),
  ("What if my flight is early or delayed?",
   "Nothing to do — we track your flight and adjust the pickup automatically, at no charge."),
  ("How much wait time is included?",
   "30 minutes free on domestic arrivals and 60 minutes free on international arrivals, counted from wheels-down. After that, wait time is billed per minute by vehicle class — see our <a href='terms.html'>Terms</a> for exact rates."),
  ("Which airports do you serve?",
   "All three Bay Area airports (SFO, OAK, SJC) plus 25 major airports nationwide — JFK, LGA, EWR, LAX, ORD, ATL, and more. <a href='services/airport-transfers.html'>See the full list →</a>"),
 ]),
 ("Changes & cancellations", [
  ("How do I change my pickup time or address?",
   f"Email {EMAIL} with your updated details, or use the rider portal. Changes are free when made with reasonable notice and subject to availability."),
  ("What's the cancellation policy?",
   "Cancellation windows vary by vehicle class — sedans and SUVs have shorter windows, Sprinters and buses longer ones. The full schedule is in our <a href='terms.html'>Terms &amp; Conditions</a>. When in doubt, email us — we'll always tell you exactly where you stand before you decide."),
  ("I left something in the vehicle — what do I do?",
   f"Email {EMAIL} with your trip date and pickup location. We'll contact your chauffeur immediately and arrange return of your item."),
 ]),
 ("Vehicles & chauffeurs", [
  ("Who are your chauffeurs?",
   "Vetted, background-checked, commercially licensed professionals — not gig drivers. Many have been with us for years."),
  ("What vehicles do you operate?",
   "Business sedans, business and first-class SUVs, executive Sprinter vans, and party buses up to 32 passengers. <a href='index.html#fleet'>See the fleet →</a>"),
  ("Do you have car seats?",
   "Yes — forward-facing, rear-facing, and boosters are available on request. Add a note when booking or email us and we'll have them installed before pickup."),
  ("Can you handle large groups?",
   "Up to 32 in a single vehicle, and we coordinate multi-vehicle moves for bigger groups, weddings, and corporate events. Tell us your headcount and we'll propose the right mix."),
 ]),
]

faq_html = ""
for cat, items in SUPPORT_FAQS:
    blocks = "\n".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in items)
    faq_html += f"""
  <h3 style="font-size:22px;margin:38px 0 14px">{cat}</h3>
  <div class="faq">{blocks}</div>"""

sp += f"""
<section style="padding-top:24px"><div class="wrap" style="max-width:880px">
  <div class="sec-head center"><span class="pill">FAQ</span><h2>Detailed answers</h2></div>
  <div class="blog-tools" style="margin-bottom:8px">
    <div class="ksearch"><input id="fsearch" type="search" placeholder="Search the FAQs — wait time, cancel, car seats…" aria-label="Search FAQs"></div>
  </div>
  <div id="faqwrap">{faq_html}</div>
  <p id="fnone" style="display:none;text-align:center;color:var(--muted);margin-top:26px">No matches — try a different word, or <a href="mailto:reserve@koastride.com" style="color:var(--orange);font-weight:700">email us</a> and a human will answer.</p>
</div></section>
<script>
(function(){{
  var inp=document.getElementById('fsearch'),wrap=document.getElementById('faqwrap'),none=document.getElementById('fnone');
  var groups=[];
  wrap.querySelectorAll('h3').forEach(function(h){{
    var faq=h.nextElementSibling;
    groups.push({{h:h,items:Array.prototype.slice.call(faq.querySelectorAll('details'))}});
  }});
  inp.addEventListener('input',function(){{
    var q=inp.value.trim().toLowerCase(),any=false;
    groups.forEach(function(g){{
      var vis=0;
      g.items.forEach(function(d){{
        var hit=!q||d.textContent.toLowerCase().indexOf(q)>-1;
        d.style.display=hit?'':'none';
        if(hit)vis++;
        if(q&&hit&&vis===1)d.open=false;
      }});
      g.h.style.display=vis?'':'none';
      g.h.nextElementSibling.style.display=vis?'':'none';
      if(vis)any=true;
    }});
    none.style.display=any?'none':'block';
  }});
}})();
</script>"""
sp += cta_section("Still have a question?", f"Email us at {EMAIL} — a real person answers, 24/7.")
sp += footer("")
write("support.html", sp)



# ============================ EVENT BLOGS BATCH 4 ============================
blog_page("nyc-events-calendar",
 "New York Events Worth Planning Around",
 "The NYC events calendar that moves Manhattan — marathons, premieres, festivals — and how to get anywhere on those days.",
 "City Events","blog-banner-nyc-events.jpg","6", f"""
  <p>New York doesn't slow down for events — it reroutes around them. The trick to event days in Manhattan isn't avoiding them; it's knowing exactly which streets stop working and planning your rides around the closures.</p>
  <h2>The calendar that matters</h2>
  <ul>
    <li><strong>NYC Marathon (early November).</strong> All five boroughs, dozens of bridge and avenue closures from dawn to late afternoon. Crosstown travel north of 59th is the day's real challenge.</li>
    <li><strong>US Open (late August–early September).</strong> Flushing Meadows pulls heavy traffic onto the Grand Central Parkway — evening sessions collide with LaGuardia runs, so pad airport trips by 30 minutes.</li>
    <li><strong>UN General Assembly week (September).</strong> The East Side simply closes. Motorcades freeze First Avenue and everything near Turtle Bay. Stay west, or plan double the time.</li>
    <li><strong>Summer concert season.</strong> Central Park and Forest Hills shows let out all at once — pre-booking your pickup point two blocks from the exit beats fighting 20,000 people for cars.</li>
    <li><strong>Macy's Thanksgiving Parade & NYE.</strong> Midtown west becomes pedestrian-only. Hotels inside the frozen zone require walking out to a pre-arranged corner.</li>
  </ul>
  <h2>The chauffeur advantage on event days</h2>
  <p>A driver who watches closures in real time and adjusts your pickup corner is the difference between making the curtain and watching the app's car circle four blocks away. We pre-route around every major closure and confirm your exact pickup point by text. <a href="../cities/new-york.html" style="color:var(--teal-dark);font-weight:700">Koast in New York →</a></p>""",
 "Arrive like you knew all along.")

blog_page("chicago-summer-festivals",
 "Chicago's Festival Summer, Mapped",
 "Lollapalooza, Taste of Chicago, the Air & Water Show — Chicago's summer festival logistics, closures, and how to move between them.",
 "City Events","blog-banner-chi-fest.jpg","6", f"""
  <p>From June to September, Chicago's lakefront becomes one rolling festival — and Lake Shore Drive becomes a variable. Here's the summer, in logistics terms.</p>
  <h2>The big four</h2>
  <ul>
    <li><strong>Lollapalooza (early August).</strong> Grant Park for four days. Columbus Drive closes, Michigan Avenue crawls, and ride pickups push west of State Street. Pre-arranged pickup corners save 40 minutes a night.</li>
    <li><strong>Taste of Chicago (summer weekends).</strong> Grant Park again, gentler footprint — but evening fireworks empty everyone at once.</li>
    <li><strong>Air & Water Show (August).</strong> North Avenue Beach: the lakefront parks fill by 9am and Lake Shore Drive slows to a parade.</li>
    <li><strong>Riot Fest & area street fests.</strong> Douglass Park and neighborhood closures most weekends — quick to check, easy to route around with a driver who knows the grid.</li>
  </ul>
  <h2>Festival-week playbook</h2>
  <p>Hourly charters work brilliantly here: one vehicle holding your group's day — beach, festival gate, dinner in Fulton Market, late pickup — with no surge math at 11pm. <a href="../cities/chicago.html" style="color:var(--teal-dark);font-weight:700">Koast in Chicago →</a></p>""",
 "The lakefront, handled.")

blog_page("miami-art-week",
 "Miami Art Week Without the Gridlock",
 "Art Basel and Miami Art Week logistics — causeway timing, fair-hopping between Miami Beach and Wynwood, and late-night moves.",
 "City Events","blog-banner-miami-art.jpg","5", f"""
  <p>For one week in early December, the art world lands on two islands connected by causeways that were full in November. Art Week isn't about distance — Miami Beach to Wynwood is seven miles — it's about timing.</p>
  <h2>The geography problem</h2>
  <ul>
    <li><strong>Basel proper</strong> lives at the Convention Center on the Beach; <strong>satellite fairs</strong> (Untitled, Scope, NADA) dot the sand and the mainland; <strong>Wynwood and the Design District</strong> hold the parties.</li>
    <li>The MacArthur and Julia Tuttle causeways jam from 4pm — a 20-minute hop becomes an hour at gallery-dinner time.</li>
    <li>Parking on the Beach functionally disappears. Valet queues at the big hotels run 45 minutes on peak nights.</li>
  </ul>
  <h2>How collectors actually move</h2>
  <p>One chauffeured SUV on hourly, all day: fairs in the morning, the car holds your purchases while you lunch, mainland galleries before sunset, and a driver waiting outside dinner when the night's third stop gets decided at the table. <a href="../cities/miami.html" style="color:var(--teal-dark);font-weight:700">Koast in Miami →</a></p>""",
 "Seven miles, zero stress.")

blog_page("nashville-music-calendar",
 "Nashville's Music Calendar: CMA Fest to New Year's Eve",
 "Nashville's biggest music weeks — CMA Fest, NYE on Broadway, stadium season — and how groups move when downtown fills up.",
 "City Events","blog-banner-nash-music.jpg","5", f"""
  <p>Nashville runs on a calendar of crescendos — weeks when Lower Broadway closes, hotels triple, and the city's bachelorette economy hits maximum throughput. Time your trip with it (or against it) deliberately.</p>
  <h2>The loud weeks</h2>
  <ul>
    <li><strong>CMA Fest (June).</strong> Four days, multiple stages, Broadway pedestrianized. Nissan Stadium shows empty 60,000 people across one bridge — your pickup point matters more than your dinner reservation.</li>
    <li><strong>July 4th & New Year's Eve.</strong> The Big Bash brings half a million to a closed downtown; plan pickups north of Church Street.</li>
    <li><strong>Stadium season.</strong> Titans Sundays and stadium tours reshape the east bank all fall.</li>
    <li><strong>Year-round:</strong> Friday-to-Sunday bachelorette flow means Broadway gridlock every single weekend — not just festival weeks.</li>
  </ul>
  <h2>The group answer</h2>
  <p>Sprinters were built for this town: 14 friends, one vehicle, honky-tonk to dinner to the Gulch with zero "where's the second Uber" texts. <a href="../cities/nashville.html" style="color:var(--teal-dark);font-weight:700">Koast in Nashville →</a></p>""",
 "Music City, in sync.")

blog_page("houston-rodeo-guide",
 "Houston Rodeo Season: The Getting-There Guide",
 "Houston Livestock Show and Rodeo logistics — NRG Park traffic, concert nights, and how groups skip the parking crawl.",
 "City Events","blog-banner-hou-rodeo.jpg","5", f"""
  <p>For three weeks every spring, Houston's center of gravity moves to NRG Park — 2 million-plus visitors, nightly headline concerts, and a parking operation the size of a small city. The rodeo is wonderful; the parking crawl is not.</p>
  <h2>What rodeo nights look like</h2>
  <ul>
    <li><strong>Concert nights peak hard:</strong> the 610 Loop and Kirby Drive back up from 5pm; the lots take 30–45 minutes to clear post-show.</li>
    <li><strong>Drop-off beats parking:</strong> a curbside drop at the gate saves the half-mile lot hike in boots.</li>
    <li><strong>Pickup is the real win:</strong> while the lots crawl, a pre-arranged pickup on the Fannin side has you at dinner before the parking queue moves.</li>
  </ul>
  <h2>Group nights, done right</h2>
  <p>Company rodeo nights and family outings ride better in one vehicle — Suburban for six, Sprinter for fourteen — with the cooler space for the trip home. <a href="../cities/houston.html" style="color:var(--teal-dark);font-weight:700">Koast in Houston →</a></p>""",
 "Boots on. Parking off.")

blog_page("seattle-events-guide",
 "Seattle's Event Season: Bumbershoot to Game Day",
 "Seattle's festival and stadium calendar — Bumbershoot, Seafair, sold-out stadium Saturdays — and how to move when everyone has plans.",
 "City Events","blog-banner-sea-events.jpg","5", f"""
  <p>Seattle's events problem is geometry: two stadiums side by side, a festival center at the Space Needle, and exactly one freeway between them. When the calendar stacks, I-5 keeps the score.</p>
  <h2>The dates that move the city</h2>
  <ul>
    <li><strong>Bumbershoot (Labor Day weekend).</strong> Seattle Center fills; Mercer Street — already the city's slowest mile — sets personal records.</li>
    <li><strong>Seafair (August).</strong> Blue Angels close I-90 for practice runs. Plan around the bridge windows or embrace the lake.</li>
    <li><strong>Stadium Saturdays.</strong> When Mariners and Sounders games stack in SoDo, 50,000 people share two exits. Pre-set pickups on First Avenue skip the worst of it.</li>
    <li><strong>Convention surges</strong> downtown make hotel taxi lines spectacular — schedule pickups instead.</li>
  </ul>
  <h2>The reliable move</h2>
  <p>Flight-tracked airport runs plus scheduled event pickups — the combination that makes a Seattle weekend feel easy even when the calendar fights you. <a href="../cities/seattle.html" style="color:var(--teal-dark);font-weight:700">Koast in Seattle →</a></p>""",
 "Rain or game day. Ride easy.")

# ============================ BLOG BATCH 3 — airport + corporate guides ============================
blog_page("jfk-black-car-guide",
 "JFK Black Car Service: The Arrivals Playbook",
 "Flat-rate black car service from JFK — how arrivals pickup works, real drive times to Manhattan, and why travelers skip the for-hire line.",
 "Airport Guides","blog-jfk.jpg","6", """
  <p>JFK is New York's front door — and arrivals is where a good trip turns into a long one. The for-hire vehicle queue after a red-eye, the AirTrain to a far-flung lot, surge pricing that spikes the moment a wide-body lands. A flat-rate black car takes the variables out: one price quoted before you fly, a chauffeur tracking your flight, and a car waiting when you clear the terminal.</p>
  <h2>What the ride into Manhattan actually takes</h2>
  <p>JFK sits in southeast Queens, so the clock depends entirely on the hour. Off-peak, Midtown is 45&ndash;55 minutes. Hit the Van Wyck at rush, or land into a Friday afternoon, and 75&ndash;90 minutes is realistic. Your chauffeur picks the route &mdash; Van Wyck to the LIE and Midtown Tunnel, or the Belt Parkway when the expressways clot &mdash; but no route beats Manhattan-bound traffic at 5 p.m.</p>
  <ul>
    <li><strong>Midtown / Times Square</strong> &mdash; 45&ndash;75 min depending on the hour</li>
    <li><strong>Lower Manhattan / FiDi</strong> &mdash; 40&ndash;60 min</li>
    <li><strong>Brooklyn (Williamsburg, Downtown)</strong> &mdash; 30&ndash;50 min, often the easiest run</li>
    <li><strong>Upper East / West Side</strong> &mdash; 50&ndash;80 min through cross-town traffic</li>
  </ul>
  <h2>How pickup works at JFK</h2>
  <p>Your chauffeur watches the flight. If you're early, they're early; if you're three hours late on a delayed red-eye, the price doesn't move &mdash; there's no surge, ever. JFK arrivals include complimentary wait time (30 minutes domestic, a full hour international), so there's room to clear customs and baggage without a meter running. The price you saw at booking is the price you pay, tolls and gratuity included.</p>
  <h2>JFK, LaGuardia or Newark?</h2>
  <p>If you're still choosing where to fly, each airport is practically a different commute. We broke down the trade-offs in <a href="../blog/nyc-ground-travel-guide.html" style="color:var(--teal-dark);font-weight:700">Getting Around New York &rarr;</a> &mdash; LaGuardia is closest to Midtown when traffic cooperates, Newark can win for the West Side, and JFK is the international gateway with the most predictable (if longest) ride.</p>
  <h2>Teams and business travel</h2>
  <p>Flying a group in for an offsite or moving executives between meetings? A corporate account keeps every JFK pickup on one invoice, and a Sprinter keeps a team of fourteen together instead of scattered across cars. <a href="../services/corporate-travel.html" style="color:var(--teal-dark);font-weight:700">Koast for business &rarr;</a> &middot; <a href="../cities/new-york.html" style="color:var(--teal-dark);font-weight:700">Koast in New York &rarr;</a></p>
  <div class="faq" style="margin-top:36px">
    <details><summary>How much is a black car from JFK to Manhattan?</summary><p>You see a flat, all-inclusive price before you book &mdash; tolls and gratuity included, no surge. Enter your exact pickup and drop-off for an instant quote; the price holds even if your flight is delayed.</p></details>
    <details><summary>How long does JFK to Midtown take?</summary><p>Roughly 45&ndash;55 minutes off-peak and 75&ndash;90 minutes at rush hour or on a busy Friday. Your chauffeur chooses the fastest route for the conditions.</p></details>
    <details><summary>What happens if my flight is delayed?</summary><p>We track your flight and adjust the pickup automatically. There's no charge for the delay and no surge &mdash; your quoted fare doesn't change.</p></details>
    <details><summary>How long will the chauffeur wait at the airport?</summary><p>JFK arrivals include complimentary wait time &mdash; 30 minutes for domestic flights and a full hour for international &mdash; so you have room to clear customs and collect bags.</p></details>
    <details><summary>Can I book a return ride to JFK?</summary><p>Yes. Book the return at the same time or whenever plans firm up. For departures we build in time for traffic and terminal drop-off so you're never cutting it close.</p></details>
  </div>""",
 "From the gate to the city. Ride easy.")

blog_page("atlanta-airport-black-car-guide",
 "ATL Black Car Service: The World's Busiest Airport, Handled",
 "Flat-rate black car at Hartsfield-Jackson (ATL) — domestic vs. international arrivals, drive times, and rides to Buckhead, Midtown & downtown.",
 "Airport Guides","blog-atl.jpg","5", """
  <p>Hartsfield-Jackson moves more people than any airport on earth, and ground transportation is its own marathon. The good news for arriving travelers: a pre-booked black car turns the busiest airport in the world into a quiet, fixed-price handoff &mdash; no rideshare lot, no surge, no guessing.</p>
  <h2>Domestic vs. international arrivals</h2>
  <p>ATL's domestic terminal and the Maynard H. Jackson International Terminal sit on opposite ends of the airport, connected by the Plane Train. Where your chauffeur meets you depends on which one you land at &mdash; book with your flight details and pickup is arranged for the right side, so there's no cross-airport scramble after a long flight.</p>
  <h2>Drive times that matter</h2>
  <ul>
    <li><strong>Downtown / GWCC</strong> &mdash; 15&ndash;25 min off-peak; the Connector decides rush hour</li>
    <li><strong>Midtown</strong> &mdash; 20&ndash;30 min</li>
    <li><strong>Buckhead</strong> &mdash; 25&ndash;40 min, longer when 75/85 stacks up</li>
    <li><strong>Sandy Springs / Perimeter</strong> &mdash; 30&ndash;45 min</li>
  </ul>
  <p>Atlanta traffic is famously non-linear &mdash; a 20-minute ride at 10 a.m. is 45 at 5 p.m. A chauffeur who knows the surface-street workarounds beats a navigation app guessing at the Connector.</p>
  <h2>How pickup works</h2>
  <p>Flight tracked, wait time included (30 minutes domestic, an hour international), and one flat price quoted before you fly. Conventions at the Georgia World Congress Center and games downtown spike demand and rideshare pricing &mdash; a pre-arranged pickup doesn't flinch.</p>
  <h2>For business &amp; conventions</h2>
  <p>Moving a team through a convention week or hosting clients in town? Account billing keeps every ride on one invoice. <a href="../services/corporate-travel.html" style="color:var(--teal-dark);font-weight:700">Koast for business &rarr;</a> &middot; <a href="../cities/atlanta.html" style="color:var(--teal-dark);font-weight:700">Koast in Atlanta &rarr;</a></p>
  <div class="faq" style="margin-top:36px">
    <details><summary>How much is a black car from ATL?</summary><p>A flat, all-inclusive rate quoted before you book &mdash; no surge during conventions or game days. Enter your pickup and drop-off for an instant price.</p></details>
    <details><summary>Where does the chauffeur meet me at the world's busiest airport?</summary><p>Pickup is arranged for your arriving terminal &mdash; domestic or the Maynard H. Jackson International Terminal &mdash; based on the flight details you provide, so there's no cross-airport walk.</p></details>
    <details><summary>How long is the ride to downtown Atlanta?</summary><p>Usually 15&ndash;25 minutes off-peak. The Downtown Connector controls rush hour, so plan 30&ndash;40 in heavy traffic.</p></details>
    <details><summary>Is it available during conventions and Falcons/Hawks games?</summary><p>Yes, 24/7, at the same flat rate &mdash; no event surge. Pre-booking is the easy way past the rideshare crush.</p></details>
  </div>""",
 "The busiest airport, made simple.")

blog_page("dfw-black-car-guide",
 "DFW Black Car Service: Five Terminals, One Easy Pickup",
 "Flat-rate black car from DFW and Dallas Love Field — terminal logistics, drive times across the Metroplex, and why pre-booked beats the queue.",
 "Airport Guides","blog-dfw.jpg","5", """
  <p>DFW is its own zip code &mdash; five terminals connected by the Skylink train, spread across an airport bigger than Manhattan. For an arriving traveler, that scale is exactly why a pre-arranged pickup pays off: your chauffeur knows which terminal, which level, and which exit, so you're not wandering a city-sized airport with bags.</p>
  <h2>DFW or Dallas Love Field?</h2>
  <p>If you can choose, the airport changes your commute. DFW sits between Dallas and Fort Worth and serves the whole Metroplex. Love Field (DAL) is tucked closer to central Dallas and can be the faster run to downtown or Uptown when your airline flies there. Tell us your flight and we cover either.</p>
  <h2>Drive times across the Metroplex</h2>
  <ul>
    <li><strong>Downtown Dallas</strong> &mdash; 25&ndash;35 min from DFW; 15&ndash;20 from Love Field</li>
    <li><strong>Las Colinas / Irving</strong> &mdash; 10&ndash;20 min, the closest major hub</li>
    <li><strong>Downtown Fort Worth</strong> &mdash; 25&ndash;35 min</li>
    <li><strong>Frisco / Plano</strong> &mdash; 30&ndash;45 min north up the Tollway</li>
  </ul>
  <h2>How pickup works</h2>
  <p>Flight tracked, complimentary wait time, and a flat all-inclusive price &mdash; tolls included, which matters in a region built on toll roads. No surge when a wave of flights lands at once.</p>
  <h2>Corporate travel in the Metroplex</h2>
  <p>The Metroplex runs on business travel &mdash; corporate campuses in Las Colinas, conventions downtown, client visits across two cities. One account covers every ride, every terminal. <a href="../services/corporate-travel.html" style="color:var(--teal-dark);font-weight:700">Koast for business &rarr;</a> &middot; <a href="../cities/dallas.html" style="color:var(--teal-dark);font-weight:700">Koast in Dallas &rarr;</a></p>
  <div class="faq" style="margin-top:36px">
    <details><summary>How much is a black car from DFW?</summary><p>A flat, all-inclusive rate including tolls and gratuity, quoted before you book &mdash; no surge. Enter your pickup and drop-off for an instant price.</p></details>
    <details><summary>Which terminal will the chauffeur meet me at?</summary><p>Pickup is arranged for your specific arriving terminal at DFW (or Dallas Love Field) using your flight details, so there's no cross-airport guessing.</p></details>
    <details><summary>How long is the ride to downtown Dallas?</summary><p>About 25&ndash;35 minutes from DFW off-peak, or 15&ndash;20 minutes from Love Field. Tollway and traffic conditions move those numbers at rush hour.</p></details>
    <details><summary>Do you serve both DFW and Love Field?</summary><p>Yes &mdash; both airports, plus rides anywhere across Dallas, Fort Worth, and the suburbs, all at flat rates.</p></details>
  </div>""",
 "Five terminals. One simple ride.")

blog_page("miami-airport-black-car-guide",
 "MIA Black Car Service: Arrivals to South Beach, Brickell & the Port",
 "Flat-rate black car from Miami International (MIA) — arrivals pickup, real drive times to South Beach, Brickell & PortMiami, and cruise-day logistics.",
 "Airport Guides","blog-mia.jpg","5", """
  <p>Miami International is a busy international gateway, and the ride out of it lives and dies by the causeways. A flat-rate black car means the price is set before you land &mdash; no surge after an evening bank of flights from Latin America, no negotiating at the curb &mdash; and a chauffeur who knows when the MacArthur is moving and when to take the Julia Tuttle.</p>
  <h2>Drive times that depend on the bridges</h2>
  <ul>
    <li><strong>Brickell / Downtown</strong> &mdash; 15&ndash;25 min, the quickest run</li>
    <li><strong>South Beach</strong> &mdash; 20&ndash;35 min depending on which causeway is flowing</li>
    <li><strong>Coral Gables</strong> &mdash; 15&ndash;25 min</li>
    <li><strong>PortMiami (cruise terminals)</strong> &mdash; 15&ndash;25 min, but cruise mornings change everything</li>
  </ul>
  <p>Why the causeways rule the trip &mdash; and how locals time them &mdash; is the whole story in <a href="../blog/miami-getting-around.html" style="color:var(--teal-dark);font-weight:700">Getting Around Miami &rarr;</a>.</p>
  <h2>Cruise-day logistics</h2>
  <p>MIA to PortMiami is a short hop on paper, but embarkation mornings turn the port into a parking lot. A pre-booked transfer with flight tracking gets you there with luggage handled and time to spare &mdash; and the return, after you disembark into a crowd of thousands, is the ride you'll be most glad you booked ahead.</p>
  <h2>How pickup works</h2>
  <p>Your flight is tracked, international arrivals include a full hour of complimentary wait time for customs, and the fixed price holds no matter when you actually clear. Tolls and gratuity included.</p>
  <p><a href="../services/airport-transfers.html" style="color:var(--teal-dark);font-weight:700">Airport transfers &rarr;</a> &middot; <a href="../cities/miami.html" style="color:var(--teal-dark);font-weight:700">Koast in Miami &rarr;</a></p>
  <div class="faq" style="margin-top:36px">
    <details><summary>How much is a black car from MIA?</summary><p>A flat, all-inclusive price quoted before you book &mdash; tolls and gratuity included, no surge. Enter your pickup and drop-off for an instant quote.</p></details>
    <details><summary>How long is MIA to South Beach?</summary><p>Usually 20&ndash;35 minutes, depending on which causeway is moving. Your chauffeur picks the fastest crossing for the moment.</p></details>
    <details><summary>Can you handle a cruise transfer from the airport to PortMiami?</summary><p>Yes &mdash; airport-to-port and port-to-airport transfers with flight tracking and luggage help. Cruise mornings and disembarkation crowds are exactly when booking ahead pays off.</p></details>
    <details><summary>How long do you wait for an international arrival?</summary><p>International arrivals at MIA include a full hour of complimentary wait time, with the flight tracked so pickup adjusts to when you actually land and clear customs.</p></details>
  </div>""",
 "Past the causeways. Ride easy.")

blog_page("investor-roadshow-ground-travel",
 "The Investor Roadshow Ground-Travel Playbook",
 "How to run ground transportation for a multi-city investor roadshow — one account across cities, on time between meetings, and a single invoice at the end.",
 "Corporate","blog-roadshow.jpg","6", """
  <p>A roadshow is a logistics problem wearing a suit: five cities in five days, back-to-back meetings, flights that leave no margin, and principals who cannot &mdash; under any circumstances &mdash; be late to the next one. The flights get all the attention. The ground travel between them is what actually breaks schedules.</p>
  <h2>One account, every city</h2>
  <p>The first fix is structural: don't rebook a new local car service in each market. A single corporate account covers New York, Boston, San Francisco, and everywhere the week goes &mdash; same standard, same booking flow, same dispatcher relationship, one invoice at the end. <a href="../services/corporate-travel.html" style="color:var(--teal-dark);font-weight:700">Koast for business &rarr;</a></p>
  <h2>The buffer math</h2>
  <p>Roadshow days fail at the seams &mdash; the ten minutes that evaporate between a meeting running long and the next one starting on time. Build cushion into the ground legs, not the meetings: assume traffic, assume the elevator, assume the lobby small-talk. A chauffeur staged and waiting downstairs turns a tight transfer into a non-event. For longer gaps, an hourly booking keeps the same car and driver on standby so there's no re-summoning between stops.</p>
  <h2>Airport legs are the high-risk legs</h2>
  <p>Every city change is an airport on each end, and that's where a delay cascades through the whole day. Flight-tracked pickups absorb the delay automatically; the next morning's departure leg gets built with traffic baked in. No surge means a 6 a.m. car costs what a noon car costs.</p>
  <h2>Hand the booking to the desk that owns it</h2>
  <p>Roadshows are usually run by an EA or a corporate travel manager juggling principals across time zones. The same patterns that make executive ground travel reliable apply at roadshow scale &mdash; we wrote them up in <a href="../blog/ea-guide-executive-ground-travel.html" style="color:var(--teal-dark);font-weight:700">The EA's Guide to Booking Executive Ground Travel &rarr;</a>. Passenger lists, driver details before every pickup, and one place to make a change at 6 a.m. when the schedule moves.</p>
  <div class="faq" style="margin-top:36px">
    <details><summary>Can one account cover ground travel in every roadshow city?</summary><p>Yes. A single corporate account books the same standard of service in every market we serve, with consolidated billing and one invoice at month-end &mdash; no setting up a new local vendor in each city.</p></details>
    <details><summary>How do you keep a tight back-to-back schedule from slipping?</summary><p>Chauffeurs are staged and waiting before the principal comes down, ground legs are planned with traffic buffers, and hourly bookings keep the same car on standby between closely spaced meetings.</p></details>
    <details><summary>What happens when a flight is delayed mid-roadshow?</summary><p>Pickups are flight-tracked and adjust automatically, with no delay charge and no surge. The next departure leg is planned with cushion so one late flight doesn't topple the next day.</p></details>
    <details><summary>Who can book and manage the rides?</summary><p>An EA, chief of staff, or travel manager can book for anyone, see driver details before each pickup, and make changes from one place &mdash; ideal for coordinating principals across time zones.</p></details>
  </div>""",
 "Every city. One standard.")

blog_page("group-airport-transfers",
 "Group Airport Transfers: Moving a Team Through Arrivals",
 "How to coordinate airport transfers for a whole team — staggered flights, one vehicle vs. several, Sprinter vs. SUVs, and keeping everyone moving on arrival.",
 "Corporate","blog-group.jpg","5", """
  <p>Moving one executive from the airport is easy. Moving twelve people arriving on six flights into one offsite is a different sport. The mistake is treating it like twelve separate bookings &mdash; the fix is treating it like one coordinated operation.</p>
  <h2>One vehicle or several?</h2>
  <p>The first decision is the vehicle math. A team that lands together rides better in one cabin: an Executive Sprinter keeps fourteen people and their bags together, which means one drop-off, one headcount, and a group that arrives as a group. When flights are scattered across the day, two or three SUVs staged to match arrival waves beats one van waiting four hours for the last straggler. <a href="../index.html#fleet" style="color:var(--teal-dark);font-weight:700">See the fleet &rarr;</a></p>
  <h2>Staggered flights, one plan</h2>
  <p>The real work is the schedule. Collect everyone's flight numbers, group the arrivals into waves, and assign vehicles to waves rather than to individuals. Each pickup is flight-tracked, so a delayed connection doesn't strand a car or the people waiting in it. A dispatcher who has the whole manifest can shuffle in real time when one flight slips.</p>
  <h2>Give it to one point of contact</h2>
  <p>Group travel goes sideways when ten people each text the driver. Route it through one coordinator and one dispatcher relationship: the booker holds the manifest, drivers' details go out before pickup, and changes happen in one place. That's the difference between a calm arrivals curb and a parking-lot group text.</p>
  <h2>One invoice for the whole move</h2>
  <p>Account billing rolls every vehicle and every leg into a single invoice instead of a pile of receipts to reconcile. <a href="../services/corporate-travel.html" style="color:var(--teal-dark);font-weight:700">Koast for business &rarr;</a> &middot; <a href="../services/airport-transfers.html" style="color:var(--teal-dark);font-weight:700">Airport transfers &rarr;</a></p>
  <div class="faq" style="margin-top:36px">
    <details><summary>Should a group ride together or split across vehicles?</summary><p>If everyone lands together, one Executive Sprinter (up to fourteen with luggage) keeps the group together. If flights are staggered, several SUVs matched to arrival waves usually beats one vehicle waiting hours for the last arrival.</p></details>
    <details><summary>How do you handle a team arriving on different flights?</summary><p>We group arrivals into waves and assign vehicles to each wave, with every pickup flight-tracked so delays don't strand a car. A dispatcher with the full manifest adjusts in real time.</p></details>
    <details><summary>Can one person book and manage the whole group?</summary><p>Yes. A single coordinator holds the manifest and makes changes in one place, with driver details sent before each pickup &mdash; no group text with the drivers.</p></details>
    <details><summary>How is a group transfer billed?</summary><p>Through a corporate account, every vehicle and leg lands on one consolidated invoice rather than separate receipts to reconcile.</p></details>
  </div>""",
 "The whole team, moving as one.")

# SEO enhance — must run last
enhance()
