"""Behavioral regression checks, not independent validation of scientific truth."""
import json,math,subprocess,sys
from pathlib import Path
from query_evidence import ROOT,load_cards,search
from compare_conditions import compare,FIELDS
from quant_checks import F,molar_from_mg_l,electrons_per_nitrate,corrected_urea
from export_citations import bibtex
def main():
    checks=[]
    def check(ok,label):
        if not ok:raise AssertionError(label)
        checks.append(label)
    p=json.loads((ROOT/'analysis/comparison_profiles.json').read_text(encoding='utf-8'))
    r=compare(p['E151-performance'],p['E151-raman'])
    check({'pH','cell','electrolyte'}<={x['field'] for x in r['mismatches']},'Find spectro/performance pH and cell mismatch')
    r=compare(p['E134-performance'],p['E134-ATR'])
    check('ir_compensation_fraction' in r['unknown_fields'] and any(x['field']=='electrolyte' for x in r['mismatches']),'Missing ATR iR stays unknown; matrix mismatch retained')
    check(any(x['field']=='flow' for x in compare(p['E135-gentle'],p['E135-vigorous'])['mismatches']),'Detect stirring change within one paper')
    check(compare({}, {})['verdict']=='insufficient_information','Two empty profiles never count as matched')
    check(compare(dict.fromkeys(FIELDS,'synthetic'),dict.fromkeys(FIELDS,'synthetic'))['verdict']=='listed_conditions_match','Positive synthetic condition-match control')
    check(abs(molar_from_mg_l(14.0067,'N')-.001)<1e-12 and abs(molar_from_mg_l(62.0049,'NO3')-.001)<1e-12,'N and nitrate mass bases convert to same molar amount')
    check(molar_from_mg_l(10,'N')/molar_from_mg_l(10,'NO3')>4.4,'Equal mg/L with different bases never treated as equal nitrate amount')
    e=electrons_per_nitrate(.1*F*.01*.02,.01,.02)
    check(abs(e-.1)<1e-12 and abs(e/8-.0125)<1e-12,'0.1 electron per nitrate gives1.25 percent NH3 ceiling')
    u=corrected_urea(5e-6,2e-6,1e-6,1e-7,1e-7,1e-7)
    check(abs(u['urea_mol']-1e-6)<1e-18 and u['sd_mol']>0,'Enzyme blank and two-N stoichiometry with uncertainty')
    check(corrected_urea(1,2,1)['urea_mol']<0,'Retain negative blank-corrected diagnostic')
    rejected=0
    for v in [-1,float('nan'),float('inf')]:
        try:molar_from_mg_l(v,'N')
        except ValueError:rejected+=1
    check(rejected==3,'Reject negative/nonfinite input')
    for query,expected in [('0.592','E134'),('同晶圆','E131'),('Raman pH13 pH14','E151')]:
        check(expected in [c['card_id'] for c in search(query,8)],'Retrieve '+expected+' from '+query)
    cards=load_cards();new=cards[121:]
    check(len([c for c in new if c.get('si_review')])==6 and sum(len(c['si_review']['read_pages']) for c in new if c.get('si_review'))==24,'SI receipt scope6 sources24 physical pages')
    check(any(c['card_id']=='E150' and 'failure' in c['capabilities'] for c in new),'Failure case has searchable route')
    check(not next(c for c in new if c['card_id']=='E132')['visual_review']['software_disclosure'],'Do not attribute another group CP-VASP mention to this paper software')
    meta=json.loads((ROOT/'analysis/methods_bibliography.json').read_text(encoding='utf-8'))
    check(len(meta)==30 and all('year = {202' in bibtex(m) and m['doi'] in bibtex(m) for m in meta),'Export all30 resolved DOI citations with years')
    # These CLI errors test semantic locator separation rather than merely matching text.
    cmd=[sys.executable,str(ROOT/'scripts/query_evidence.py'),'--card','E134']
    r=subprocess.run(cmd+['--source-pages','3'],capture_output=True,text=True,encoding='utf-8')
    check(r.returncode!=0 and 'JATS units' in r.stderr,'Reject main-text PDF pages on a JATS card')
    r=subprocess.run(cmd+['--si-pages','3','--source-units','1'],capture_output=True,text=True,encoding='utf-8')
    check(r.returncode!=0 and 'not multiple' in r.stderr,'Reject mixing SI page and main-unit selectors')
    print(json.dumps(dict(ok=True,checks=len(checks),passed=checks,scope='Local behavioral regression; no claim of independent model benchmark improvement'),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
