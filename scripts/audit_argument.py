"""Explicit-field checklist for an argument plan; not a truth or acceptance score."""
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def audit(plan,cards=None):
 flags=[]
 def flag(code,panel,reason):flags.append(dict(code=code,panel=panel,reason=reason))
 if not plan.get('question'):flag('missing_question',None,'Define an unresolved scientific question.')
 if not plan.get('panels'):flag('missing_panels',None,'No evidence panels.')
 for p in plan.get('panels',[]):
  name=p.get('id','unnamed')
  for k in ('observation','inference','alternatives','next_check','source'):
   if not p.get(k):flag('missing_'+k,name,k+' is absent.')
  cond=p.get('conditions',{})
  for k in ('sample','reactor','electrolyte','potential_reference','normalization'):
   if not cond.get(k):flag('missing_condition',name,k+' absent; write not_applicable with justification if appropriate.')
  src=p.get('source',{})
  if not src.get('doi') or not src.get('figure') or not src.get('locator_kind') or not src.get('locators'):flag('source_locator',name,'Need DOI, figure and typed source locators.')
  if cards and src.get('card_id'):
   c=next((c for c in cards if c['card_id']==src['card_id']),None)
   if c is None:flag('unknown_card',name,'Card does not exist.')
   else:
    xml=c.get('source_format')=='JATS XML';expected='jats_unit' if xml else 'physical_pdf_page'
    if src.get('locator_kind')!=expected:flag('locator_kind',name,'Main PDF pages and JATS units differ. SI uses a separate audit.')
    count=c.get('locator_count',c.get('page_count',0))
    if any(not isinstance(v,int) or not 1<=v<=count for v in src.get('locators',[])):flag('locator_bounds',name,'Main source locator outside bounds.')
    if src.get('doi','').lower()!=c['doi'].lower():flag('doi_mismatch',name,'DOI differs from card.')
  tags=p.get('inference_tags',[]);e=p.get('evidence',{})
  if 'intensity_to_rate' in tags and not (e.get('quantitative_calibration') and e.get('matched_optics') and e.get('independent_product_rate')):flag('intensity_not_rate',name,'Signal intensity needs calibrated optics and independent product kinetics; correlation alone is insufficient.')
  if 'activation_barrier' in tags and e.get('energy_kind')!='transition_state':flag('state_energy_not_barrier',name,'State/adsorption energy is not a TS activation barrier.')
  if 'causal' in tags and not e.get('discriminating_controls'):flag('causal_gap',name,'Need controls distinguishing the listed alternatives.')
  if 'cross_condition_maxima' in tags and not e.get('same_operating_point'):flag('maxima_splicing',name,'Best FE/current/lifetime from different conditions cannot become one operating point.')
  rep=p.get('replication',{})
  if rep.get('independent_n',0)>rep.get('independent_units',rep.get('independent_n',0)):flag('nested_replication',name,'Locations/pixels/readings do not add independent samples.')
  if 'derived_quantity' in tags and not e.get('processing_and_uncertainty'):flag('derived_quantity_gap',name,'Keep raw signal, transform, parameters and uncertainty for derived quantities.')
 return dict(ok=not flags,flags=flags,scope='explicit-field checklist only; does not validate raw data, causal truth, novelty or journal acceptance')
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);a=p.parse_args()
 cards=json.loads((ROOT/'cards/evidence_cards.json').read_text(encoding='utf-8'))
 result=audit(json.loads(a.plan.read_text(encoding='utf-8')),cards);print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(0 if result['ok'] else 2)
if __name__=='__main__':main()
