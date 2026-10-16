"""Validate portable evidence integrity and a few meaningful retrieval behaviors."""
import json, re, sys
from pathlib import Path
from query_evidence import ROOT, load_cards, search
def main():
    c=load_cards(); errors=[]
    def check(cond,msg):
        if not cond: errors.append(msg)
    status=json.loads((ROOT/'analysis'/'library_status.json').read_text(encoding='utf-8'))
    check(len(c)==status['papers'],'Paper count differs from snapshot manifest')
    check(len([x for x in c if int(x['card_id'][1:])>=32])==status['new_papers'],'New batch count mismatch')
    check(len({x['doi'].lower() for x in c})==len(c),'Duplicate DOI')
    check(len({x['card_id'] for x in c})==len(c),'Duplicate card ID')
    for x in c:
        cid=x['card_id']
        check(bool(re.fullmatch(r'10\.\d{4,9}/\S+',x['doi'])),cid+' DOI format')
        check(bool(re.fullmatch(r'[a-f0-9]{64}',x['sha256'])),cid+' source hash')
        check(all(1<=p<=x['page_count'] for p in x['read_pages']),cid+' reading bounds')
        check(bool(x['read_scope']),cid+' scope missing')
        for claim in x['claims']:
            check(bool(claim['statement'] and claim['type'] and claim['pages']),cid+' incomplete claim')
            check(all(p in x['read_pages'] for p in claim['pages']),cid+' claim outside reading range')
        for key in ('conditions','mechanism','limits','writing','figure','experiment'):
            check(bool(x[key]),cid+' missing '+key)
        check((ROOT/'cards'/f'{cid}.md').exists(),cid+' markdown missing')
    checks={}
    for q,expected in [('1128 1266 Raman','E001'),('KSCN','E020'),('Fc/Fc','E029'),('fixed unfixed','E030'),('晶格氮','E056'),('次表层','E074'),('repelling','E091')]:
        ids=[x['card_id'] for x in search(q,8)]
        checks[q]=ids; check(expected in ids,'Retrieval failed '+q)
    # A portable repository should have only authored text and executable helpers.
    allowed={'.md','.json','.py','.gitignore'}
    tracked=[]
    for p in ROOT.rglob('*'):
        rel=p.relative_to(ROOT)
        if not p.is_file() or any(s in rel.parts for s in ('.git','__pycache__','backups_local')) or p.name=='local_config.json': continue
        check(p.suffix in allowed or p.name=='.gitignore','Unexpected portable artifact '+str(rel))
        if p.suffix in ('.md','.json','.py'):
            s=p.read_text(encoding='utf-8')
            check(not re.search(r'[A-Z]:[\\/]Users[\\/]|D:[\\/]文献|zotero\.sqlite',s),'Local source path leaked '+str(rel))
        tracked.append(str(rel).replace('\\','/'))
    from check_faraday import current_ma
    check(abs(current_ma(10.5,'NO')-1407.0778)<0.01,'NO five-electron rate conversion')
    check(abs(current_ma(1,'NO3')/current_ma(1,'NO2')-8/6)<1e-12,'NO3/NO2 electron accounting')
    canonical=lambda x:x.lower().replace('10.1002/ange.','10.1002/anie.')
    check(len({canonical(x['doi']) for x in c})==len(c),'German/International DOI alias duplicate')
    result=dict(ok=not errors,papers=len(c),new_papers=status['new_papers'],distinct_dois=len({canonical(x['doi']) for x in c}),claims=sum(len(x['claims']) for x in c),retrieval=checks,portable_files=len(tracked),errors=errors)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    sys.exit(0 if not errors else 1)
if __name__=='__main__': main()
