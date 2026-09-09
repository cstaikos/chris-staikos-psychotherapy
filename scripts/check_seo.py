"""Check preview and production metadata after the README's SEO test builds."""
from html.parser import HTMLParser
from pathlib import Path
import json
import xml.etree.ElementTree as ET

class Head(HTMLParser):
    def __init__(self, source):
        super().__init__(); self.meta={}; self.canonical=[]; self.json=[]; self.reading=False; self.buffer=''
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='meta':
            key=a.get('name',a.get('property'))
            if key:
                assert key not in self.meta, f'Duplicate meta: {key}'
                self.meta[key]=a.get('content')
        if tag=='link' and a.get('rel')=='canonical': self.canonical.append(a['href'])
        if tag=='script' and a.get('type')=='application/ld+json': self.reading=True;self.buffer=''
    def handle_data(self,data):
        if self.reading:self.buffer+=data
    def handle_endtag(self,tag):
        if tag=='script' and self.reading:
            self.json.append(json.loads(self.buffer));self.reading=False

preview=Path('_site');production=Path('tmp/seo-production')
for p in preview.rglob('*.html'):
    h=Head(p.read_text())
    assert 'noindex' in h.meta['robots']
    assert not h.canonical and not h.json
    assert 'google-site-verification' not in h.meta and 'msvalidate.01' not in h.meta
assert len(ET.parse(preview/'sitemap.xml').getroot())==0
assert 'Sitemap:' not in (preview/'robots.txt').read_text()
urls=set()
for p in production.rglob('*.html'):
    h=Head(p.read_text());relative=p.relative_to(production).as_posix().removesuffix('index.html')
    canonical='https://example.org/practice/'+relative;urls.add(canonical)
    assert h.canonical==[canonical], (p,h.canonical)
    assert h.meta['og:url']==canonical
    assert h.meta['robots']=='index, follow, max-image-preview:large'
    assert h.meta['google-site-verification']=='test-google-token'
    assert h.meta['msvalidate.01']=='test-bing-token'
    assert h.meta['og:locale']=='en_CA'
    assert h.meta['description'] and h.meta['twitter:description']
    assert len(h.json)==1 and len(h.json[0]['@graph'])==3
    assert h.json[0]['@graph'][2]['url']==canonical
    assert 'Registered Psychotherapist (Qualifying)'==h.json[0]['@graph'][1]['jobTitle']
sitemap=ET.parse(production/'sitemap.xml').getroot()
listed={entry.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text for entry in sitemap}
assert listed==urls and len(listed)==6,(listed,urls)
assert 'Sitemap: https://example.org/practice/sitemap.xml' in (production/'robots.txt').read_text()
print('PASS: preview noindex; production verification tags, canonical URLs, JSON-LD, six-page sitemap and robots sitemap reference, including repository base path.')
