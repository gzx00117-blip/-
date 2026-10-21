"""Stdlib lexical search of authored cards, with optional local full-page retrieval."""
import argparse, json, os, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ALIASES={'供氢':['hydrogen','KIE','供氢','H-UPD'],'富勒烯':['fullerene','C60','fullerenol'],'溢流':['spillover','溢流','迁移'],'拉曼':['Raman','拉曼'],'电子':['electron','电子'],'脉冲':['pulse','pulsed','脉冲'],'尿素':['urea','尿素'],'绘图':['visual_review','figure','绘图'],'软件':['software','VESTA','Origin','软件'],'重构':['reconstruction','重构'],'晶面':['facet','晶面']}
ALIASES.update({'定量':['assay','blank','calibration'],'重复':['replication','replicate'],'公平':['benchmarking','conversion','charge'],'失活':['failure','stability'],'工况':['operando','protocol_mismatch'],'同位素':['isotope'],'归一化':['normalization','ECSA'],'传质':['transport'],'矛盾':['counterexample','conflict'],'动力学':['kinetics'],'系统边界':['system_boundary','device_boundary','paired_anode']})
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
    a.add_argument('--source-units',help='For JATS cards only; indexed units e.g. 11,19-20, never PDF pages')
    a.add_argument('--si-pages',help='For explicitly available SI PDF only; physical file pages, separate from main text')
    a.add_argument('--capability',help='Exact capability tag, e.g. assay, counterexample, replication (new batch)')
    a.add_argument('--kind',help='Document kind filter; reviews and calculations are not independent experimental repeats')
    a.add_argument('--disclosed-software',help='Filter actual main-text disclosures, not our recommended software')
    a.add_argument('--figures',action='store_true',help='Show selected-figure observations and recommended remake')
    args=a.parse_args()
    cards=load_cards()
    if args.card:
        cards=[c for c in cards if c['card_id'].upper()==args.card.upper()]
        if not cards: a.error('Unknown card')
        print(json.dumps(cards[0],ensure_ascii=False,indent=2))
        if args.source_pages or args.source_units or args.si_pages:
            is_xml=cards[0].get('source_format')=='JATS XML'
            if sum(bool(v) for v in (args.source_pages,args.source_units,args.si_pages))>1: a.error('Choose main pages, main units, or SI pages, not multiple')
            if args.si_pages and not cards[0].get('si_review'):a.error('No explicitly recorded SI source for this card')
            if is_xml and args.source_pages: a.error('This card uses JATS units; use --source-units')
            if not is_xml and args.source_units: a.error('This card uses PDF pages; use --source-pages')
            cfg=ROOT/'local_config.json'
            configured=json.loads(cfg.read_text(encoding='utf-8')) if cfg.exists() else {}
            env=os.environ.get('ELECTROCATALYSIS_CORPUS')
            corpora=args.corpus or ([env] if env else configured.get('source_corpora') or ([configured['source_corpus']] if configured.get('source_corpus') else []))
            if not corpora: a.error('Set --corpus, ELECTROCATALYSIS_CORPUS, or local_config.json source_corpora')
            targets=[Path(corpus)/'texts'/(cards[0]['doc_id']+('_SI' if args.si_pages else '')+'.json') for corpus in corpora]
            target=next((p for p in targets if p.exists()),None)
            if target is None:a.error('This paper is absent from configured local corpora')
            wanted=set()
            for part in (args.source_units or args.source_pages or args.si_pages).split(','):
                bounds=[int(x) for x in part.split('-')]
                if len(bounds)>2: a.error('Invalid page range')
                wanted.update(range(bounds[0],bounds[-1]+1))
            count=cards[0]['si_review']['page_count'] if args.si_pages else cards[0].get('locator_count',cards[0].get('page_count',0))
            if not wanted or min(wanted)<1 or max(wanted)>count: a.error('Position outside source bounds')
            for p in json.loads(target.read_text(encoding='utf-8')):
                position=p.get('unit',p.get('page'))
                if position in wanted: print(f"\n{'SI PHYSICAL PDF PAGE' if args.si_pages else 'JATS UNIT' if is_xml else 'PDF PAGE'} {position}\n{p['text']}")
    elif args.query or args.disclosed_software or args.figures or args.capability or args.kind:
        matches=search(args.query,len(cards)) if args.query else cards
        if args.capability:matches=[c for c in matches if args.capability in c.get('capabilities',[])]
        if args.kind:matches=[c for c in matches if args.kind==c.get('document_kind')]
        if args.disclosed_software:
            matches=[c for c in matches if any(args.disclosed_software.lower() in s['name'].lower() for s in c.get('visual_review',{}).get('software_disclosure',[]))]
        if args.figures:matches=[c for c in matches if c.get('visual_review')]
        for c in matches[:args.limit]:
            print(f"{c['card_id']} | {c['doi']} | {c['title']}\n{c['mechanism']}\nScope: {c['read_scope']}\n")
            if args.disclosed_software:print('DISCLOSED:',json.dumps(c['visual_review']['software_disclosure'],ensure_ascii=False))
            if args.figures:print('FIGURE:',json.dumps(c['visual_review'],ensure_ascii=False))
    else: a.print_help()
if __name__=='__main__': main()
