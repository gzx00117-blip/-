"""Export verified new-batch metadata. Earlier records are not silently upgraded."""
import argparse,json,re,html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def safe(value):
    value=html.unescape(re.sub('<[^>]+>','',str(value)))
    escaped={'\\':r'\textbackslash{}','{':r'\{','}':r'\}','&':r'\&','%':r'\%','_':r'\_','#':r'\#'}
    return ''.join(escaped.get(c,c) for c in value)
def bibtex(m):
    a=' and '.join(safe(x.get('family',''))+(', '+safe(x['given']) if x.get('given') else '') for x in m['authors'])
    date=m.get('published_online') or m.get('issued') or {}
    if isinstance(date,dict):date=(date.get('date-parts') or [[]])[0]
    # Crossref date is kept as parts, never fabricated from the DOI year.
    year=date[0] if isinstance(date,list) and date else ''
    fields={'author':a,'title':'{'+safe(m['title'])+'}','journal':safe(m['journal']),'year':year,'volume':m.get('volume'),'number':m.get('issue'),'pages':m.get('page') or m.get('article_number'),'doi':m['doi'],'url':'https://doi.org/'+m['doi']}
    return '@article{'+m['card_id']+',\n'+',\n'.join('  '+k+' = {'+str(v)+'}' for k,v in fields.items() if v is not None and v!='')+'\n}'
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--card');p.add_argument('--output',type=Path);a=p.parse_args()
    m=json.loads((ROOT/'analysis/methods_bibliography.json').read_text(encoding='utf-8'))
    if a.card:
        m=[x for x in m if x['card_id']==a.card.upper()]
        if not m:p.error('Only E122–E151 have verified metadata in this export snapshot.')
    out='\n\n'.join(bibtex(x) for x in m)+'\n'
    if a.output:a.output.write_text(out,encoding='utf-8')
    else:print(out,end='')
if __name__=='__main__':main()
