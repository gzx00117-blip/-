"""NH3 rate/partial-current dimensional check, assuming identical time and area bases."""
import argparse,json
F=96485.33212
ELECTRONS={'NO3':8,'NO2':6,'NO':5}
def current_ma(rate_mmol,substrate):return rate_mmol*ELECTRONS[substrate]*F/3600
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--substrate',choices=ELECTRONS,required=True)
 g=p.add_mutually_exclusive_group(required=True)
 g.add_argument('--rate-mmol',type=float,help='mmol NH3 h−1 cm−2')
 g.add_argument('--rate-mg-nh3',type=float,help='mg NH3 h−1 cm−2')
 g.add_argument('--rate-mg-n',type=float,help='mg NH3-N h−1 cm−2')
 p.add_argument('--current-ma',type=float,help='Reported NH3 PARTIAL current, mA cm−2; not total current')
 a=p.parse_args()
 rate=a.rate_mmol if a.rate_mmol is not None else (a.rate_mg_nh3/17.031 if a.rate_mg_nh3 is not None else a.rate_mg_n/14.007)
 if rate<0:p.error('Use a nonnegative production rate')
 expected=current_ma(rate,a.substrate)
 result={'substrate':a.substrate,'electron_number':ELECTRONS[a.substrate],'rate_mmol_h_cm2':rate,'expected_partial_current_mA_cm2':expected,'assumptions':'Same sample, time, area and product basis; NH3 only. For mixed NOx use a justified N/electron balance, not an arbitrary average.'}
 if a.current_ma is not None:
  result['reported_partial_current_mA_cm2']=abs(a.current_ma)
  result['relative_difference_percent']=100*abs(abs(a.current_ma)-expected)/expected if expected else None
  result['interpretation']='Check conditions, integration, units, mass basis, calibration and raw data before drawing a conclusion. This calculation does not establish experimental error or misconduct.'
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
