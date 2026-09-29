#!/usr/bin/env python3
"""Fieldnotes: searchable original engineering knowledge library."""
import html, json, os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse, urlencode
ROOT=Path(__file__).resolve().parent
ARTICLES=json.loads((ROOT/'content/articles.json').read_text())
TOPICS=['API integration','AI automation','Legacy software','WordPress']
def esc(s):return html.escape(str(s),quote=True)
def shell(title,body,saved=False):
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} — Fieldnotes</title><meta name="description" content="Practical notes on AI automation, API integration, legacy software and WordPress by Ismail Habib."><link rel="stylesheet" href="/assets/style.css"><script src="/assets/bookmarks.js" defer></script></head><body data-saved="{str(saved).lower()}"><a class="skip" href="#main">Skip to content</a><header><a class="brand" href="/"><span class="brandmark">≡</span>fieldnotes<span class="byline">by Ismail Habib</span></a><nav aria-label="Main navigation"><a href="/">The library</a><a class="navbutton" href="/saved">Saved <span data-count>0</span></a><a href="/about">About ↗</a></nav></header><main id="main" class="wrap"><div id="storage-warning" class="notice" hidden>Browser storage is unavailable. Saved articles will last only for this page visit.</div>{body}</main><footer><span>Original practical notes by Ismail Habib · Independent project</span><span>No tracking. Bookmarks stay in your browser.</span></footer></body></html>'''
def card(a):
 cls={'API integration':'api','AI automation':'ai','Legacy software':'legacy','WordPress':'wp'}[a['topic']]
 symbols={'api':'{ } ⇄ { }','ai':'✳ → ✓','legacy':'[ C++ ]','wp':'▤ → ↗'}
 return f'''<article class="card" data-card="{a['slug']}"><div class="art {cls}" aria-hidden="false"><span class="symbol" aria-hidden="true">{symbols[cls]}</span><button class="bookmark" type="button" data-bookmark="{a['slug']}" aria-pressed="false" aria-label="Save article">▢</button></div><div class="cardbody"><div class="tagline">{esc(a['topic'])} / {esc(a['type'])}</div><h3><a href="/articles/{a['slug']}">{esc(a['title'])}</a></h3><p>{esc(a['intro'])}</p><div class="cardfoot"><span>{a['minutes']} min read</span><a href="/articles/{a['slug']}" aria-label="Read {esc(a['title'])}">Open note ↗</a></div></div></article>'''
def library(q='',topic='',saved=False):
 selected=[a for a in ARTICLES if (not topic or a['topic']==topic) and (not q or q.casefold() in json.dumps(a,ensure_ascii=False).casefold())]
 heading='Your useful notes,<br><em>kept close.</em>' if saved else 'Good systems start<br>with <em>clear thinking.</em>'
 intro='Your saved reading list. Bookmarks are stored on this browser only.' if saved else 'Practical field guides for connecting tools, building useful AI and keeping existing software working.'
 form='' if saved else f'''<form class="searchbar" action="/" method="get" role="search"><span class="searchicon" aria-hidden="true">⌕</span><label class="skip" for="query">Search the knowledge library</label><input type="search" id="query" name="q" value="{esc(q)}" placeholder="Search workflows, APIs, migrations…"><input type="hidden" name="topic" value="{esc(topic)}"><button type="submit">Search ↗</button></form><div class="filters" aria-label="Filter by topic">'''+''.join(f'<a class="filter {"active" if topic==t else ""}" href="/?{urlencode({"q":q,"topic":t})}" {"aria-current=page" if topic==t else ""}>{esc(t or "All topics")}</a>' for t in ['']+TOPICS)+'</div>'
 cards=''.join(card(a) for a in selected)
 if not selected:cards='<div class="empty"><h2>No notes match this search.</h2><p>Try a shorter phrase or choose another topic.</p><a href="/">Reset filters</a></div>'
 if saved:cards+='<div class="empty" id="saved-empty" hidden><h2>Your reading list is ready for its first note.</h2><p>Use the bookmark button on any article to save it here.</p><a href="/">Explore the library ↗</a></div>'
 return f'''<section class="hero"><div><div class="eyebrow">THE PRACTICAL ENGINEERING LIBRARY</div><h1>{heading}</h1><p class="lead">{intro}</p></div><aside class="edition"><div class="eyebrow">Built to be useful</div><p><b>{len(ARTICLES)} original resources.</b>Four connected disciplines.<br>One place to find the next step.</p><span class="small">Field guides · Playbooks · Checklists</span></aside></section>{form}<div class="resultshead"><h2>{'Saved resources' if saved else 'From the notebook'}</h2><span id="result-count" aria-live="polite">{len(selected)} resources{f' for “{esc(q)}”' if q else ''}</span></div><section class="grid" aria-label="Resources">{cards}</section><aside class="banner"><div><h2>From a useful note to a working system.</h2><p>I work across AI automation, APIs, legacy software and WordPress.</p></div><a href="https://en.malt.de/profile/ismailhabib">Meet Ismail on Malt ↗</a></aside>'''
def article(a):
 sections=''.join(f'<section><h2>{esc(h)}</h2><p>{esc(p)}</p></section>' for h,p in a['sections'])
 checks=''.join(f'<li>{esc(x)}</li>' for x in a['checklist'])
 return f'''<article class="article"><div class="breadcrumbs"><a href="/">Library</a> / <a href="/?{urlencode({'topic':a['topic']})}">{esc(a['topic'])}</a></div><div class="eyebrow">{esc(a['topic'])} / {esc(a['type'])}</div><h1>{esc(a['title'])}</h1><p class="intro">{esc(a['intro'])}</p><div class="resultshead"><span>Ismail Habib · {a['minutes']} min read · Original editorial content</span><button class="bookmark wide" data-bookmark="{a['slug']}" aria-pressed="false">Save for later</button></div><pre aria-label="Workflow summary">{esc(a['code'])}</pre>{sections}<h2>Take this into your next project</h2><ul>{checks}</ul><p class="small">A practical starting point, to adapt to your system. Examples are explanatory workflows, not measurements from a client engagement.</p><a href="/">← Back to the library</a></article>'''
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def send(self,body,status=200,ctype='text/html; charset=utf-8'):
  if isinstance(body,str):body=body.encode()
  self.send_response(status);self.send_header('Content-Type',ctype);self.send_header('Content-Length',str(len(body)));self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Security-Policy',"default-src 'self'; style-src 'self'; script-src 'self'; base-uri 'self'; frame-ancestors 'none'; form-action 'self'");self.end_headers();self.wfile.write(body)
 def do_GET(self):
  p=urlparse(self.path);q=parse_qs(p.query)
  if p.path in ['/assets/style.css','/assets/bookmarks.js']:
   return self.send((ROOT/p.path.lstrip('/')).read_bytes(),ctype='text/css' if p.path.endswith('css') else 'application/javascript')
  if p.path=='/health':return self.send(json.dumps({'status':'ok','articles':len(ARTICLES)}),ctype='application/json')
  if p.path=='/api/resources':
   term=q.get('q',[''])[0].casefold();topic=q.get('topic',[''])[0];rows=[a for a in ARTICLES if (not topic or a['topic']==topic) and (not term or term in json.dumps(a).casefold())]
   return self.send(json.dumps(rows,ensure_ascii=False),ctype='application/json; charset=utf-8')
  if p.path=='/':return self.send(shell('Practical engineering library',library(q.get('q',[''])[0][:200],q.get('topic',[''])[0])))
  if p.path=='/saved':return self.send(shell('Saved resources',library(saved=True),True))
  if p.path=='/about':return self.send(shell('About the library','<article class="article"><div class="eyebrow">About this independent project</div><h1>Notes that help<br>you take the next step.</h1><p class="intro">Fieldnotes is an original resource library for the practical work between an idea and a dependable system.</p><h2>Four connected disciplines</h2><p>The content covers AI automation, API integration, legacy software and WordPress. Each article focuses on a specific decision, workflow or verification step. The library is maintained as editable structured content.</p><h2>Designed to stay simple</h2><p>Search the full article text, filter by topic and save useful notes in your browser. No account or tracking service is required. Saved notes remain on this device and can disappear when browser storage is cleared.</p><h2>About Ismail</h2><p>Ismail Habib works across website development, AI-powered workflows, API connections and existing C++ Windows applications. These original notes are new editorial work, not claims of past client results.</p><a href="https://en.malt.de/profile/ismailhabib">View Ismail’s Malt profile ↗</a></article>'))
  if p.path.startswith('/articles/'):
   a=next((a for a in ARTICLES if a['slug']==p.path.split('/')[-1]),None)
   if a:return self.send(shell(a['title'],article(a)))
  self.send(shell('Not found','<article class="article"><h1>That note is not here.</h1><a href="/">Return to the library</a></article>'),404)
if __name__=='__main__':
 port=int(os.environ.get('PORT','8108'));print(f'Library: http://127.0.0.1:{port}',flush=True);ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()
