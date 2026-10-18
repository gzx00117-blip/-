"""Generate original, explicitly synthetic training figures at physical journal widths."""
import csv,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
EX=ROOT/'figure_examples';OUT=EX/'generated'
COLORS=['#555555','#0072B2','#D55E00'];MARKERS=['o','s','^'];STYLES=['-','--',':']
def main():
 OUT.mkdir(exist_ok=True)
 rng=np.random.default_rng(121)
 records=[]
 potentials=np.array([-.85,-.75,-.65,-.55,-.45,-.35])
 for k,sample in enumerate(['Control','Modified','Reference']):
  for v in potentials:
   for rep in range(1,4):
    fe=80-65*(v+.55)**2+[0,11,5][k]+rng.normal(0,1.5)
    j=-(28+190*abs(v+.25))*[1,1.16,1.05][k]*(1+rng.normal(0,.025))
    records.append(dict(data_kind='SYNTHETIC_TRAINING',sample=sample,E_V_RHE=v,replicate=rep,FE_NH3_percent=fe,j_total_mA_cm2=j,j_NH3_mA_cm2=abs(j)*fe/100))
 with (EX/'synthetic_training.csv').open('w',newline='',encoding='utf8') as h:
  w=csv.DictWriter(h,fieldnames=records[0]);w.writeheader();w.writerows(records)
 wave=np.linspace(900,1500,450)
 spectra=[np.exp(-.5*((wave-1080-8*k)/25)**2)+.6*np.exp(-.5*((wave-1280)/40)**2)+rng.normal(0,.015,len(wave)) for k in range(2)]
 with (EX/'synthetic_spectra.csv').open('w',newline='',encoding='utf8') as h:
  w=csv.writer(h);w.writerow(['data_kind','wavenumber_cm_inverse','simulated_A','simulated_B','B_display_offset'])
  w.writerows(('SYNTHETIC_TRAINING',v,a,b,1.3) for v,a,b in zip(wave,*spectra))
 profiles=json.loads((ROOT/'analysis/journal_profiles.json').read_text(encoding='utf8'))['profiles']
 try:
  font_manager.findfont('Arial',fallback_to_default=False);font='Arial'
 except ValueError:font='DejaVu Sans'
 reports=[]
 for key,p in profiles.items():
  cfg=p['working_preset'];width=cfg['double_mm'];height=116
  plt.rcParams.update({'font.family':font,'font.size':cfg['font_pt'],'axes.labelsize':cfg['font_pt'],'xtick.labelsize':cfg['font_pt'],'ytick.labelsize':cfg['font_pt'],'legend.fontsize':cfg['font_pt'],'axes.linewidth':cfg['axis_pt'],'lines.linewidth':cfg['line_pt'],'svg.fonttype':'none','pdf.fonttype':42,'savefig.facecolor':'white'})
  fig,axs=plt.subplots(2,2,figsize=(width/25.4,height/25.4))
  fig.subplots_adjust(left=.105,right=.975,bottom=.12,top=.90,wspace=.40,hspace=.55)
  fig.text(.5,.975,'SYNTHETIC TRAINING | '+p['journal'],ha='center',va='top',fontsize=8)
  for k,sample in enumerate(['Control','Modified','Reference']):
   means=[];sds=[];jmeans=[];jsds=[]
   for v in potentials:
    a=[x for x in records if x['sample']==sample and x['E_V_RHE']==v]
    f=np.array([x['FE_NH3_percent'] for x in a]);j=np.array([x['j_NH3_mA_cm2'] for x in a]);means.append(f.mean());sds.append(f.std(ddof=1));jmeans.append(j.mean());jsds.append(j.std(ddof=1))
   opts=dict(color=COLORS[k],marker=MARKERS[k],linestyle=STYLES[k],markersize=3,capsize=2,elinewidth=.6,label=sample)
   axs[0,0].errorbar(potentials,means,yerr=sds,**opts)
   axs[0,1].errorbar(potentials,jmeans,yerr=jsds,**opts)
   a=[x['FE_NH3_percent'] for x in records if x['sample']==sample and x['E_V_RHE']==-.65]
   axs[1,0].scatter(k+np.array([-.10,0,.10]),a,s=13,color=COLORS[k],marker=MARKERS[k],zorder=3)
   axs[1,0].errorbar(k,np.mean(a),yerr=np.std(a,ddof=1),fmt='_',color=COLORS[k],capsize=5,markersize=15,zorder=2)
  axs[0,0].set(xlabel='Potential (V vs. RHE)',ylabel=r'NH$_3$ Faradaic efficiency (%)',ylim=(0,105));axs[0,0].legend(frameon=False,loc='lower left',handlelength=2)
  axs[0,1].set(xlabel='Potential (V vs. RHE)',ylabel=r'NH$_3$ partial current (mA cm$^{-2}$)')
  for ax in axs[0]:ax.set_xticks([-.8,-.6,-.4])
  axs[1,0].set(xticks=[0,1,2],xticklabels=['Control','Modified','Reference'],ylabel=r'NH$_3$ FE (%)',ylim=(65,100));axs[1,0].text(.04,.95,'3 synthetic replicates; mean ± SD',transform=axs[1,0].transAxes,va='top',fontsize=7.5)
  for k in range(2):
   signal=spectra[k]
   axs[1,1].plot(wave,signal+k*1.3,color=COLORS[k],label=['Simulated A','Simulated B'][k])
  axs[1,1].set(xlabel=r'Wavenumber (cm$^{-1}$)',ylabel='Simulated intensity (a.u.)',yticks=[],xticks=[900,1100,1300,1500],ylim=(-.15,3.05))
  axs[1,1].text(.97,.95,'Offset for clarity\nNo chemical assignments',ha='right',va='top',transform=axs[1,1].transAxes,fontsize=7.5)
  for label,ax in zip('abcd',axs.flat):
   ax.text(-.19,1.08,label,transform=ax.transAxes,fontweight='bold',fontsize=cfg['panel_pt'])
   ax.tick_params(direction='out',length=2.5,width=.6)
   ax.spines[['top','right']].set_visible(False)
  fig.text(.105,.035,'Paired j = |j_total| × FE/100. All values generated for layout practice; no experimental claims.',fontsize=7.5)
  fig.canvas.draw();renderer=fig.canvas.get_renderer();outside=[]
  for t in fig.findobj(matplotlib.text.Text):
   if not t.get_visible() or not t.get_text():continue
   box=t.get_window_extent(renderer)
   if box.x0 < -1 or box.y0 < -1 or box.x1 > fig.bbox.width+1 or box.y1 > fig.bbox.height+1:outside.append(t.get_text())
  for ext in ['svg','pdf','png']:fig.savefig(OUT/f'{key}_training.{ext}',dpi=600)
  plt.close(fig)
  im=Image.open(OUT/f'{key}_training.png');im.convert('L').save(OUT/f'{key}_grayscale.png')
  reports.append({'profile':key,'width_mm':width,'height_mm':height,'font':font,'font_pt':cfg['font_pt'],'out_of_canvas_text':outside,'svg':f'{key}_training.svg','pdf':f'{key}_training.pdf','png':f'{key}_training.png'})
 svg='''<svg xmlns="http://www.w3.org/2000/svg" width="55mm" height="50mm" viewBox="0 0 550 500"><rect width="550" height="500" fill="white"/><g font-family="Arial, sans-serif" fill="#222"><text x="275" y="35" text-anchor="middle" font-size="28">TRAINING CONCEPT</text><text x="275" y="80" text-anchor="middle" font-size="28">Where does charge go?</text><rect x="45" y="130" width="460" height="65" rx="12" fill="#eeeeee"/><text x="275" y="173" text-anchor="middle" font-size="28">Interface modification</text><path d="M275 205 L145 280 M275 205 L405 280" fill="none" stroke="#777" stroke-width="4" stroke-dasharray="10 8"/><rect x="35" y="290" width="220" height="70" rx="10" fill="#e5f1f8"/><rect x="295" y="290" width="220" height="70" rx="10" fill="#f9eee5"/><text x="145" y="336" text-anchor="middle" font-size="28">NH3 pathway?</text><text x="405" y="336" text-anchor="middle" font-size="28">H2 pathway?</text><text x="275" y="410" text-anchor="middle" font-size="28">Proposed; validate products</text><text x="275" y="465" text-anchor="middle" font-size="25">Dashed arrows: hypotheses</text></g></svg>'''
 (OUT/'toc_concept_editable.svg').write_text(svg,encoding='utf8')
 (ROOT/'analysis/figure_generation.json').write_text(json.dumps({'data_kind':'SYNTHETIC_TRAINING','matplotlib_version':matplotlib.__version__,'reports':reports},indent=2)+'\n',encoding='utf8')
 print(json.dumps(reports,indent=2))
if __name__=='__main__':main()
