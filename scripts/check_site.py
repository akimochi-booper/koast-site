"""Read-only checks for generated pages; run after generate.py."""
from collections import Counter
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import argparse
import json
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from editorial import load_posts

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.refs=[]; self.title=""; self.desc=""; self.h1=0; self.in_title=False; self.noindex=False; self.canonical=""
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=="title": self.in_title=True
        if tag=="h1": self.h1+=1
        if tag=="meta" and attrs.get("name")=="description": self.desc=attrs.get("content", "")
        if tag=="meta" and attrs.get("name", "").lower()=="robots" and "noindex" in attrs.get("content", "").lower(): self.noindex=True
        if tag=="link" and attrs.get("rel")=="canonical": self.canonical=attrs.get("href", "")
        if tag in ("a","link","script","img"):
            ref=attrs.get("href") or attrs.get("src")
            if ref: self.refs.append(ref)
    def handle_endtag(self, tag):
        if tag=="title": self.in_title=False
    def handle_data(self, data):
        if self.in_title: self.title+=data

parser=argparse.ArgumentParser()
parser.add_argument("--today", required=True, help="Current date in America/Los_Angeles")
args=parser.parse_args()
today=date.fromisoformat(args.today)
errors=[]; titles=Counter(); descriptions=Counter(); page_count=0; nonindexable=set()
for path in sorted(ROOT.rglob("*.html")):
    if "dist" in path.relative_to(ROOT).parts: continue
    page_count+=1
    page=Page(); page.feed(path.read_text(encoding="utf-8"))
    if page.noindex and page.canonical: nonindexable.add(page.canonical)
    titles[page.title]+=1; descriptions[page.desc]+=1
    if not page.title or not page.desc or page.h1!=1: errors.append(f"{path.name}: missing title/description or H1 count {page.h1}")
    for ref in page.refs:
        url=urlsplit(ref)
        if not url.path or url.scheme or url.netloc: continue
        target=ROOT/unquote(url.path).lstrip("/") if url.path.startswith("/") else path.parent/unquote(url.path)
        candidates=[target,target/"index.html"]
        if target.name and not target.suffix: candidates.append(target.with_suffix(".html"))
        if not any(candidate.is_file() for candidate in candidates): errors.append(f"{path.relative_to(ROOT)}: missing {ref}")
posts=load_posts(ROOT)
index=(ROOT/"blog/index.html").read_text(encoding="utf-8")
sitemap=(ROOT/"sitemap.xml").read_text(encoding="utf-8")
ns={"s":"http://www.sitemaps.org/schemas/sitemap/0.9"}
sitemap_dates={entry.findtext("s:loc",namespaces=ns):entry.findtext("s:lastmod",namespaces=ns) for entry in ET.fromstring(sitemap).findall("s:url",ns)}
dated_urls={"https://koastride.com/blog/"+post["slug"] for post in posts}
for url,modified in sitemap_dates.items():
    if url in nonindexable: errors.append(f"{url}: noindex page listed in sitemap")
    if modified is not None and url not in dated_urls: errors.append(f"{url}: unverified sitemap modification date")
for post in posts:
    slug=post["slug"]; public="https://koastride.com/blog/"+slug
    src=(ROOT/"blog"/(slug+".html")).read_text(encoding="utf-8")
    if date.fromisoformat(post["published"])>today or date.fromisoformat(post["modified"])>today: errors.append(f"{slug}: future date")
    checks={"index":'/blog/'+slug in index,"sitemap":public in sitemap,"canonical":f'<link rel="canonical" href="{public}">' in src}
    import re
    schemas=[json.loads(block) for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>',src,re.S)]
    article=next((block for block in schemas if block.get("@type")=="BlogPosting"),{})
    image_url="https://koastride.com/img/"+post["image"]
    checks["schema_image"]=article.get("image")==image_url
    checks["social_image"]=f'<meta property="og:image" content="{image_url}">' in src
    from html import escape
    checks["image_alt"]=f'alt="{escape(post["image_alt"], quote=True)}"' in src
    checks["image_dimensions"]=f'width="{post["image_width"]}" height="{post["image_height"]}"' in src
    checks["published"]=article.get("datePublished")==post["published"]
    checks["modified"]=article.get("dateModified")==post["modified"]
    checks["sitemap_modified"]=sitemap_dates.get(public)==post["modified"]
    checks["author_identity"]=article.get("author",{}).get("url")=="https://koastride.com/"
    checks["publisher_identity"]=article.get("publisher",{}).get("name")=="Koast" and article.get("publisher",{}).get("url")=="https://koastride.com/"
    checks["main_entity"]=article.get("mainEntityOfPage",{}).get("@id")==public
    checks["large_image_preview"]='<meta name="robots" content="max-image-preview:large">' in src
    for check,ok in checks.items():
        if not ok: errors.append(f"{slug}: {check} failed")
for kind,counts in (("title",titles),("description",descriptions)):
    for text,count in counts.items():
        if count>1: errors.append(f"Duplicate {kind} ({count}): {text}")
print(json.dumps({"pages":page_count,"blog_posts":len(list((ROOT/"blog").glob("*.html")))-1,"dated_editorial_posts":len(posts),"errors":errors},indent=2))
if errors: sys.exit(1)
