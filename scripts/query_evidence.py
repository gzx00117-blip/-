"""Stdlib lexical search of authored cards, with optional local full-page retrieval."""
import argparse, json, os, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ALIASES={'供氢':['hydrogen','KIE','供氢','H-UPD'],'富勒烯':['fullerene','C60','fullerenol'],'溢流':['spillover','溢流','迁移'],'拉曼':['Raman','拉曼'],'电子':['electron','电子'],'脉冲':['pulse','pulsed','脉冲'],'尿素':['urea','尿素']}
def load_cards(): return json.loads((ROOT/'cards'/'evidence_cards.json').read_text(encoding='utf-8'))
def search(query,limit=6):
    words=re.findall(r'[\w*+-]+',query.lower())
    terms=set(w.rstrip('*') for w in words)
    for k,vals in ALIASES.items():
        if k in query: terms.update(x.lower() for x in vals)
    out=[]
    for c in load_cards():
        body=json.dumps(c,ensure_ascii=False).lower()
        score=sum(min(body.count(t),5) for t in terms if t)
        if score: out.append((score,c))
    return [c for _,c in sorted(out,key=lambda x:(-x[0],x[1]['card_id']))[:limit]]
def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('query',nargs='?',default=''); a.add_argument('--card'); a.add_argument('--limit',type=int,default=6)
    a.add_argument('--corpus',type=Path,action='append',help='Local extracted corpus; repeat for multiple dated corpora')
    a.add_argument('--source-pages',help='For --card only; PDF pages e.g. 3,5-6')
    args=a.parse_args()
    cards=load_cards()
    if args.card:
        cards=[c for c in cards if c['card_id'].upper()==args.card.upper()]
        if not cards: a.error('Unknown card')
        print(json.dumps(cards[0],ensure_ascii=False,indent=2))
        if args.source_pages:
            cfg=ROOT/'local_config.json'
            configured=json.loads(cfg.read_text(encoding='utf-8')) if cfg.exists() else {}
            env=os.environ.get('ELECTROCATALYSIS_CORPUS')
            corpora=args.corpus or ([env] if env else configured.get('source_corpora') or ([configured['source_corpus']] if configured.get('source_corpus') else []))
            if not corpora: a.error('Set --corpus, ELECTROCATALYSIS_CORPUS, or local_config.json source_corpora')
            targets=[Path(corpus)/'texts'/(cards[0]['doc_id']+'.json') for corpus in corpora]
            target=next((p for p in targets if p.exists()),None)
            if target is None:a.error('This paper is absent from configured local corpora')
            wanted=set()
            for part in args.source_pages.split(','):
                bounds=[int(x) for x in part.split('-')]
                if len(bounds)>2: a.error('Invalid page range')
                wanted.update(range(bounds[0],bounds[-1]+1))
            if not wanted or min(wanted)<1 or max(wanted)>cards[0]['page_count']: a.error('Page outside source bounds')
            for p in json.loads(target.read_text(encoding='utf-8')):
                if p['page'] in wanted: print(f"\nPDF PAGE {p['page']}\n{p['text']}")
    elif args.query:
        for c in search(args.query,args.limit):
            print(f"{c['card_id']} | {c['doi']} | {c['title']}\n{c['mechanism']}\nScope: {c['read_scope']}\n")
    else: a.print_help()
if __name__=='__main__': main()
