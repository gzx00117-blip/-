"""Small dimensional checks; calculations do not certify an assay or mechanism."""
import argparse, json, math
F=96485.33212
MOLAR_MASS={'N':14.0067,'NO3':62.0049,'NH3':17.03052,'NH4':18.03846}
def finite(value,name,positive=False):
    if not math.isfinite(value) or (value<=0 if positive else value<0):
        raise ValueError(name+' must be finite and '+('positive' if positive else 'nonnegative'))
def molar_from_mg_l(value,basis):
    finite(value,'concentration')
    if basis not in MOLAR_MASS:raise ValueError('basis must be explicit: '+','.join(MOLAR_MASS))
    return value/1000/MOLAR_MASS[basis]
def electrons_per_nitrate(charge_c,concentration_m,volume_l):
    finite(charge_c,'charge magnitude');finite(concentration_m,'concentration',True);finite(volume_l,'volume',True)
    return charge_c/(F*concentration_m*volume_l)
def corrected_urea(after,before,enzyme_blank,sd_after=0,sd_before=0,sd_blank=0):
    for name,v in [('after',after),('before',before),('blank',enzyme_blank),('SD_after',sd_after),('SD_before',sd_before),('SD_blank',sd_blank)]:finite(v,name)
    return dict(urea_mol=(after-before-enzyme_blank)/2,sd_mol=math.sqrt(sd_after**2+sd_before**2+sd_blank**2)/2,assumption='independent NH4 amount uncertainties; covariance not available',negative_policy='negative corrected values are retained; investigate blanks/LOQ, do not clip')
def main():
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='command',required=True)
    c=sub.add_parser('concentration');c.add_argument('--mg-l',type=float,required=True);c.add_argument('--basis',choices=MOLAR_MASS,required=True)
    c=sub.add_parser('charge');c.add_argument('--coulomb',type=float,required=True);c.add_argument('--molar',type=float,required=True);c.add_argument('--litre',type=float,required=True)
    c=sub.add_parser('urea');c.add_argument('--after',type=float,required=True);c.add_argument('--before',type=float,required=True);c.add_argument('--enzyme-blank',type=float,required=True)
    a=p.parse_args()
    try:
        if a.command=='concentration':out=dict(molar=molar_from_mg_l(a.mg_l,a.basis),basis=a.basis,note='Input mg/L, not unspecified ppm. Same N amount has different compound mass.')
        elif a.command=='charge':
            e=electrons_per_nitrate(a.coulomb,a.molar,a.litre)
            out=dict(electrons_per_initial_nitrate=e,maximum_fraction_to_NH3_at_100_percent_FE=e/8,maximum_fraction_to_NO2_at_100_percent_FE=e/2,note='Stoichiometric ceiling before substrate exhaustion; not measured conversion. Low-conversion benchmarking and treatment have different objectives.')
        else:out=corrected_urea(a.after,a.before,a.enzyme_blank)
    except ValueError as exc:p.error(str(exc))
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
