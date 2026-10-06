"""Check preview and production metadata after the README's SEO test builds."""
from html.parser import HTMLParser
from pathlib import Path
import json
import sys
import xml.etree.ElementTree as ET

class Head(HTMLParser):
    def __init__(self, source):
        super().__init__(); self.meta={}; self.canonical=[]; self.json=[]; self.reading=False; self.buffer=''
        self.titles=[]; self.in_title=False; self.h1=[]; self.in_h1=False
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='title': self.titles.append(''); self.in_title=True
        if tag=='h1': self.h1.append(''); self.in_h1=True
        if tag=='meta':
            key=a.get('name',a.get('property'))
            if key:
                assert key not in self.meta, f'Duplicate meta: {key}'
                self.meta[key]=a.get('content')
        if tag=='link' and a.get('rel')=='canonical': self.canonical.append(a['href'])
        if tag=='script' and a.get('type')=='application/ld+json': self.reading=True;self.buffer=''
    def handle_data(self,data):
        if self.in_title: self.titles[-1]+=data
        if self.in_h1: self.h1[-1]+=data
        if self.reading:self.buffer+=data
    def handle_endtag(self,tag):
        if tag=='title': self.in_title=False
        if tag=='h1': self.in_h1=False
        if tag=='script' and self.reading:
            self.json.append(json.loads(self.buffer));self.reading=False

preview=Path('_site');production=Path(sys.argv[1] if len(sys.argv)>1 else 'tmp/seo-production')
origin=sys.argv[2].rstrip('/') if len(sys.argv)>2 else 'https://example.org/practice'
expected_headings={'': 'Chris Staikos Psychotherapy', 'about/': 'About Chris',
                   'psychotherapy/': 'Psychotherapy', 'breathwork/': 'Breathwork',
                   'psychedelic-support/': 'Psychedelic Support',
                   'faq/': 'Frequently Asked Questions', 'contact/': 'Contact'}
titles=set(); descriptions=set()
for p in preview.rglob('*.html'):
    h=Head(p.read_text())
    assert 'noindex' in h.meta['robots']
    assert not h.canonical and not h.json
    assert 'google-site-verification' not in h.meta and 'msvalidate.01' not in h.meta
assert len(ET.parse(preview/'sitemap.xml').getroot())==0
assert 'Sitemap:' not in (preview/'robots.txt').read_text()
urls=set()
for p in production.rglob('*.html'):
    if p.name == '404.html':
        h=Head(p.read_text())
        assert 'noindex' in h.meta['robots']
        assert not h.canonical and not h.json
        continue
    h=Head(p.read_text());relative=p.relative_to(production).as_posix().removesuffix('index.html')
    canonical=origin+'/'+relative;urls.add(canonical)
    assert h.h1==[expected_headings[relative]], (p,h.h1)
    assert len(h.titles)==1 and h.titles[0].strip(), (p,h.titles)
    title=h.titles[0]
    assert title not in titles and h.meta['description'] not in descriptions, p
    titles.add(title); descriptions.add(h.meta['description'])
    assert h.meta['og:title']==h.meta['twitter:title']==title
    assert h.meta['og:description']==h.meta['twitter:description']==h.meta['description']
    assert h.meta['og:type']=='website'
    assert h.meta['og:image']==h.meta['twitter:image']==origin+'/assets/images/forest.jpg'
    assert (production/'assets/images/forest.jpg').is_file()
    assert h.meta['og:image:alt']==h.meta['twitter:image:alt']
    assert h.canonical==[canonical], (p,h.canonical)
    assert h.meta['og:url']==canonical
    assert h.meta['robots']=='index, follow, max-image-preview:large'
    if len(sys.argv)==1:
        assert h.meta['google-site-verification']=='test-google-token'
        assert h.meta['msvalidate.01']=='test-bing-token'
    assert h.meta['og:locale']=='en_CA'
    assert h.meta['description'] and h.meta['twitter:description']
    assert len(h.json)==1 and len(h.json[0]['@graph'])==3
    assert h.json[0]['@graph'][2]['url']==canonical
    assert h.json[0]['@graph'][2]['name']==title
    assert 'Registered Psychotherapist (Qualifying)'==h.json[0]['@graph'][1]['jobTitle']
sitemap=ET.parse(production/'sitemap.xml').getroot()
listed={entry.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text for entry in sitemap}
assert listed==urls=={origin+'/'+route for route in expected_headings},(listed,urls)
robots=(production/'robots.txt').read_text()
assert 'Sitemap: '+origin+'/sitemap.xml' in robots
assert 'Allow: /' in robots and 'Disallow:' not in robots
print('PASS: preview noindex; unique production titles/descriptions, preserved H1s, social metadata/images, canonical URLs, JSON-LD, exact seven-page sitemap and crawlable robots rules.')
