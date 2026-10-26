"""Regression checks for consequential evidence-boundary errors, using known cases."""
import copy,json
from audit_argument import ROOT,audit
def main():
 cards=json.loads((ROOT/'cards/evidence_cards.json').read_text(encoding='utf-8'))
 plan=json.loads((ROOT/'templates/argument_plan_example.json').read_text(encoding='utf-8'))
 checks={}
 checks['bounded_correlation_allowed']=audit(plan,cards)['ok']
 def codes(p):return {f['code'] for f in audit(p,cards)['flags']}
 bad=copy.deepcopy(plan);bad['panels'][0]['inference_tags']=['intensity_to_rate'];checks['Raman_rate_gap_detected']='intensity_not_rate' in codes(bad)
 bad=copy.deepcopy(plan);bad['panels'][0]['inference_tags']=['activation_barrier'];bad['panels'][0]['evidence']['energy_kind']='reaction_state';checks['DG_not_TS_detected']='state_energy_not_barrier' in codes(bad)
 bad=copy.deepcopy(plan);bad['panels'][0]['inference_tags']=['cross_condition_maxima'];checks['FE_j_maxima_splicing_detected']='maxima_splicing' in codes(bad)
 bad=copy.deepcopy(plan);bad['panels'][0]['replication']={'independent_n':12,'independent_units':4};checks['nested_repeats_detected']='nested_replication' in codes(bad)
 bad=copy.deepcopy(plan);bad['panels'][0]['source']['locators']=[69];checks['physical_page_bounds_detected']='locator_bounds' in codes(bad)
 bad=copy.deepcopy(plan);bad['panels'][0]['source']['locator_kind']='jats_unit';checks['PDF_JATS_confusion_detected']='locator_kind' in codes(bad)
 bad=copy.deepcopy(plan);bad['panels'][0]['inference_tags']=['derived_quantity'];checks['KPFM_derivative_uncertainty_detected']='derived_quantity_gap' in codes(bad)
 maps=json.loads((ROOT/'analysis/story_figure_maps.json').read_text(encoding='utf-8'))
 checks['all_new_card_maps_present']={x['card_id'] for x in maps}=={f'E{x}' for x in range(152,184)}
 si=json.loads((ROOT/'analysis/story_si_audits.json').read_text(encoding='utf-8'))
 checks['SI01_not_counted_as_full_paper']=next(s for s in si if s['doc_id']=='SI01')['parent_card_id'] is None
 checks['commentary_type_preserved']=next(c for c in cards if c['card_id']=='E168')['document_kind']=='commentary'
 print(json.dumps(dict(ok=all(checks.values()),checks=checks),ensure_ascii=False,indent=2));raise SystemExit(0 if all(checks.values()) else 1)
if __name__=='__main__':main()
