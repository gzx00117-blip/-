"""Report known mismatches and missing fields; never rank catalysts by journal or FE alone."""
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FIELDS=('reaction','target','cell','electrolyte','pH','substrate_concentration_m','substrate_basis','potential_v','reference','ir_compensation_fraction','normalization','temperature_c','loading','duration_s','flow','paired_anode','assay','replicate_unit')
def compare(a,b):
    same=[];different=[];unknown=[]
    for key in FIELDS:
        av=a.get(key);bv=b.get(key)
        if av is None or bv is None:unknown.append(key)
        elif av!=bv:different.append(dict(field=key,a=av,b=bv))
        else:same.append(key)
    return dict(verdict='known_mismatches' if different else 'insufficient_information' if unknown else 'listed_conditions_match',mismatches=different,unknown_fields=unknown,matching_fields=same,scope='Exact field comparison of explicitly entered conditions; no chemical synonym reasoning or automatic causal/quality score. Matching fields do not prove equivalent catalysts or mechanisms.')
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--a');p.add_argument('--b');p.add_argument('--profiles',type=Path,default=ROOT/'analysis/comparison_profiles.json');p.add_argument('--list',action='store_true');a=p.parse_args()
    profiles=json.loads(a.profiles.read_text(encoding='utf-8'))
    if a.list:print('\n'.join(profiles));return
    if a.a not in profiles or a.b not in profiles:p.error('Choose both --a and --b from --list, or supply your own --profiles JSON mapping.')
    print(json.dumps(dict(a=a.a,b=a.b,source_a=profiles[a.a].get('source'),source_b=profiles[a.b].get('source'),**compare(profiles[a.a],profiles[a.b])),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
