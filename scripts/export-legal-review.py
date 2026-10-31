"""Export repository-authored legal bodies to plain Markdown for owner review."""
from html.parser import HTMLParser
from pathlib import Path
import argparse

class Markdown(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.links = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('h2','h3'): self.out.append('\n\n'+('## ' if tag == 'h2' else '### '))
        elif tag == 'p': self.out.append('\n\n')
        elif tag == 'li': self.out.append('\n- ')
        elif tag in ('strong', 'em'): self.out.append('**' if tag == 'strong' else '*')
        elif tag == 'a':
            self.out.append('[')
            href = attrs.get('href', '')
            self.links.append('https://koastride.com'+href if href.startswith('/') else href)
    def handle_endtag(self, tag):
        if tag in ('strong', 'em'): self.out.append('**' if tag == 'strong' else '*')
        elif tag == 'a': self.out.append(']('+self.links.pop()+')')
        elif tag in ('h2', 'h3', 'ul'): self.out.append('\n')
    def handle_data(self, text):
        text = ' '.join(text.split())
        if text:
            # Preserve spaces around inline markup without duplicating structural newlines.
            self.out.append(text)
        elif text == '' and self.out and self.out[-1] not in ('\n','\n\n'):
            pass

parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
out=Path(args.output).resolve()
out.mkdir(parents=True,exist_ok=True)
for name,title in [('privacy','Shared Privacy Policy'),('rider','Rider Terms'),('driver','Driver App Terms'),('connect','Connect Terms')]:
    # Inline whitespace is meaningful in source HTML. Convert structural tags first,
    # then use a parser for entity decoding and accurate link destinations.
    body=(root/'content/legal'/f'{name}.inc').read_text(encoding='utf-8')
    import re
    body=re.sub(r'\s*\n\s*','\n',body)
    class ReviewMarkdown(Markdown):
        def handle_data(self,text): self.out.append(text)
    md=ReviewMarkdown();md.feed(body)
    text=''.join(md.out)
    text=re.sub(r'\n{3,}','\n\n',text).strip()
    prefix=f'# {title}\n\n**Draft for owner review — October 30, 2026. Not effective or published.**\n\n'
    (out/f'{name.upper()}.md').write_text(prefix+text+'\n',encoding='utf-8',newline='\n')
    print(out/f'{name.upper()}.md')
