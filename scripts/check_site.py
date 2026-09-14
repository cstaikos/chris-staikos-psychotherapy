"""Validate built pages and internal links without third-party dependencies."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
base=sys.argv[2].rstrip('/') if len(sys.argv)>2 else ''
class Page(HTMLParser):
 def __init__(self,path):
  super().__init__(convert_charrefs=True);self.path=path;self.ids=[];self.links=[];self.h1=0;self.lang=None;self.description=False;self.noindex=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='html':self.lang=a.get('lang')
  if tag=='meta' and a.get('name')=='description':self.description=bool(a.get('content'))
  if tag=='meta' and a.get('name')=='robots':self.noindex='noindex' in a.get('content','')
  if tag in ('a','link','img','script','iframe'):
   u=a.get('href',a.get('src'))
   if u:self.links.append(u)
pages={}
errors=[]
for file in root.rglob('*.html'):
 p=Page(file);p.feed(file.read_text());pages[file]=p
 if p.h1!=1:errors.append(f'{file}: {p.h1} H1 headings')
 if p.lang!='en-CA':errors.append(f'{file}: wrong language')
 if not p.description:errors.append(f'{file}: no description')
 if not p.noindex:errors.append(f'{file}: preview not noindexed')
 if len(p.ids)!=len(set(p.ids)):errors.append(f'{file}: duplicate IDs')
for file,p in pages.items():
 for link in p.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  path=unquote(u.path)
  if base and path.startswith('/'):
   if not path.startswith(base+'/'):errors.append(f'{file}: missing baseurl: {link}')
   path=path[len(base):]
  target=(root/path.lstrip('/')) if path.startswith('/') else (file.parent/path if path else file)
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'{file}: missing {link}')
  elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append(f'{file}: missing anchor {link}')
content=' '.join(f.read_text() for f in pages)
for phrase in ['Registered Psychotherapist (Qualifying)','Trauma Processing','Three hours total','9am','Psychology Today','reveal-email','BSc Cognitive Science','Triphasic Trauma Treatment','Can I book a one-off']:
 if phrase not in content:errors.append(f'Missing required content: {phrase}')
for private in ['My Ideal Client','Highly motivated','financially, relationally','chris.staikos.psychotherapy@proton.me','All 10 designs']:
 if private in content:errors.append(f'Private or obsolete content present: {private}')
if len(pages)!=7:errors.append(f'Expected 7 pages, found {len(pages)}')
if errors:
 print('\n'.join(errors));sys.exit(1)
print(f'PASS: {len(pages)} pages; all internal links, anchors and assets resolve; one H1, description, en-CA and noindex on every page; required content present; only the selected multipage site remains.')
