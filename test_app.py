import json,os,socket,subprocess,sys,time,unittest
from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError,URLError
from urllib.parse import urlencode
ROOT=Path(__file__).resolve().parent
class LibraryTests(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  with socket.socket() as s:s.bind(('127.0.0.1',0));c.port=s.getsockname()[1]
  c.proc=subprocess.Popen([sys.executable,str(ROOT/'app.py')],env={**os.environ,'PORT':str(c.port)},stdout=subprocess.DEVNULL);c.base=f'http://127.0.0.1:{c.port}'
  for i in range(50):
   try:urlopen(c.base+'/health',timeout=1);break
   except URLError:time.sleep(.05)
 @classmethod
 def tearDownClass(c):c.proc.terminate();c.proc.wait()
 def get(self,p):return urlopen(self.base+p).read().decode()
 def test_eight_complete_articles(self):
  resources=json.loads(self.get('/api/resources'));self.assertEqual(len(resources),8)
  for a in resources:
   text=self.get('/articles/'+a['slug']);self.assertIn(a['title'],text);self.assertIn('Take this into your next project',text);self.assertEqual(len(a['sections']),3)
 def test_full_text_search(self):
  rows=json.loads(self.get('/api/resources?'+urlencode({'q':'idempotency'})));self.assertEqual([x['slug'] for x in rows],['design-a-retry-policy'])
 def test_topic_filter_and_combined_query(self):
  rows=json.loads(self.get('/api/resources?'+urlencode({'topic':'WordPress'})));self.assertEqual(len(rows),2)
  rows=json.loads(self.get('/api/resources?'+urlencode({'topic':'WordPress','q':'idempotency'})));self.assertEqual(rows,[])
 def test_empty_results_and_escaping(self):
  self.assertIn('No notes match',self.get('/?q=nonexistent-term-abc'))
  text=self.get('/?'+urlencode({'q':'<script>alert(1)</script>'}));self.assertNotIn('<script>alert',text);self.assertIn('&lt;script&gt;',text)
 def test_saved_and_404(self):
  self.assertIn('data-saved="true"',self.get('/saved'));self.assertIn('localStorage',self.get('/assets/bookmarks.js'))
  with self.assertRaises(HTTPError) as x:self.get('/articles/missing')
  self.assertEqual(x.exception.code,404)
if __name__=='__main__':unittest.main(verbosity=2)
