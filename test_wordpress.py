"""Read-only integration checks against the local WordPress library."""
import json,re
from urllib.request import urlopen
from urllib.parse import urlencode
base='http://127.0.0.1:8188'
def get(p):return urlopen(base+p).read().decode()
home=get('/');assert 'Good systems start' in home;assert len(re.findall(r'data-card=',home))==8;print('PASS: actual WordPress theme lists 8 imported resources')
search=get('/?'+urlencode({'query':'idempotency'}));assert 'Retries should recover' in search;assert len(re.findall(r'data-card=',search))==1;print('PASS: WordPress full-text search finds body content')
topic=get('/?'+urlencode({'topic':'WordPress'}));assert len(re.findall(r'data-card=',topic))==2;print('PASS: custom metadata topic filter')
empty=get('/?'+urlencode({'query':'nonexistent-term-abc'}));assert 'No notes match' in empty;print('PASS: useful empty state')
article=get('/articles/trace-an-api-request/');assert 'Trace one request.' in article;assert 'Check each boundary' in article;print('PASS: real permalink and full editable article content')
rest=json.loads(get('/wp-json/wp/v2/fieldnote?per_page=100'));assert len(rest)==8;print('PASS: registered content type exposes 8 published resources')
assert 'data-saved="true"' in get('/?saved=1');print('PASS: saved-reading-list view')
print('7 WordPress integration checks passed.')
