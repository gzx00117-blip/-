"""Retrieve authored argument/figure maps or separately identified SI audits."""
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/'analysis'/name).read_text(encoding='utf-8'))
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--card');p.add_argument('--query',default='');p.add_argument('--figure');p.add_argument('--si');p.add_argument('--limit',type=int,default=5)
 p.add_argument('--source-pages',help='SI selector only: retrieve complete local extracted physical pages, e.g. 5,7-8')
 a=p.parse_args()
 if a.limit<1:p.error('limit must be positive')
 if a.si:
  rows=[s for s in load('story_si_audits.json') if s['doc_id'].upper()==a.si.upper()]
  if not rows:p.error('unknown SI source')
  print(json.dumps(rows[0],ensure_ascii=False,indent=2))
  if a.source_pages:
   wanted=set()
   try:
    for part in a.source_pages.split(','):
     z=[int(x) for x in part.split('-')]
     if len(z)>2 or z[0]>z[-1]:raise ValueError()
     wanted.update(range(z[0],z[-1]+1))
   except ValueError:p.error('invalid page range')
   if not wanted or min(wanted)<1 or max(wanted)>rows[0]['page_count']:p.error('outside physical source bounds')
   cfg=ROOT/'local_config.json';corpora=json.loads(cfg.read_text(encoding='utf-8')).get('source_corpora',[]) if cfg.exists() else []
   src=next((Path(c)/'texts'/f'{a.si.upper()}.json' for c in corpora if (Path(c)/'texts'/f'{a.si.upper()}.json').exists()),None)
   if src is None:p.error('source not present in configured local corpora; public repo contains authored notes only')
   for page in json.loads(src.read_text(encoding='utf-8')):
    if page['page'] in wanted:print(f'\nSI PHYSICAL PDF PAGE {page["page"]}\n{page["text"]}')
  return
 if a.source_pages:p.error('use --si for SI pages; main pages use query_evidence.py --card --source-pages')
 rows=load('story_figure_maps.json')
 if a.card:rows=[r for r in rows if r['card_id'].upper()==a.card.upper()]
 if a.query:
  terms=a.query.lower().split();rank=[(sum(json.dumps(r,ensure_ascii=False).lower().count(t) for t in terms),r) for r in rows]
  rows=[r for score,r in sorted(rank,key=lambda x:-x[0]) if score]
 if a.figure:
  out=[]
  for r in rows:
   fs=[f for f in r['figure_story'] if f['figure_id'].lower().replace(' ','')==a.figure.lower().replace(' ','')]
   if fs:out.append({**r,'figure_story':fs})
  rows=out
 if not any((a.card,a.query,a.figure)):p.print_help();return
 for r in rows[:a.limit]:print(json.dumps(r,ensure_ascii=False,indent=2))
 if not rows:p.error('no matching argument map; earlier151 cards keep their original scopes')
if __name__=='__main__':main()
