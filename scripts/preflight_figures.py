"""Check generated artifacts, including correct sizes and editable vector text."""
import json,re,xml.etree.ElementTree as ET
from pathlib import Path
from pypdf import PdfReader
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];EX=ROOT/'figure_examples/generated'
def main():
 gen=json.loads((ROOT/'analysis/figure_generation.json').read_text(encoding='utf8'));errors=[];out=[]
 for row in gen['reports']:
  key=row['profile'];pdf=PdfReader(EX/row['pdf']);p=pdf.pages[0];width=float(p.mediabox.width)*25.4/72;height=float(p.mediabox.height)*25.4/72
  s=(EX/row['svg']).read_text(encoding='utf8');root=ET.fromstring(s);text_nodes=len(root.findall('.//{http://www.w3.org/2000/svg}text'))
  im=Image.open(EX/row['png']);expected=(round(row['width_mm']/25.4*600),round(row['height_mm']/25.4*600))
  fonts=[]
  for f in p['/Resources'].get('/Font',{}).values():
   f=f.get_object();sub=f.get('/Subtype');embedded=False
   if '/DescendantFonts' in f:
    d=f['/DescendantFonts'][0].get_object().get('/FontDescriptor',{}).get_object();embedded=any(k in d for k in ('/FontFile','/FontFile2','/FontFile3'))
   fonts.append({'type':str(sub),'embedded':embedded})
  if abs(width-row['width_mm'])>.01 or abs(height-row['height_mm'])>.01:errors.append(key+' PDF physical size')
  if not text_nodes or '<image' in s:errors.append(key+' expected editable all-vector text/plots')
  if any(abs(a-b)>1 for a,b in zip(im.size,expected)):errors.append(key+' PNG dimensions')
  if row['out_of_canvas_text']:errors.append(key+' text outside canvas')
  if any(not f['embedded'] for f in fonts):errors.append(key+' font embedding')
  if 'SYNTHETIC TRAINING' not in p.extract_text():errors.append(key+' missing synthetic marker')
  out.append({'profile':key,'pdf_width_mm':width,'pdf_height_mm':height,'svg_text_nodes':text_nodes,'png_pixels':im.size,'font_resources':fonts,'outside_text':row['out_of_canvas_text']})
 toc=ET.parse(EX/'toc_concept_editable.svg').getroot()
 if toc.get('width')!='55mm' or toc.get('height')!='50mm':errors.append('TOC size')
 result={'ok':not errors,'checked':'Physical size, vector text, font embedding, PNG pixels, synthetic marker, canvas bounds. Human visual review is separate.','results':out,'errors':errors}
 (ROOT/'analysis/figure_validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8');print(json.dumps(result,indent=2));raise SystemExit(bool(errors))
if __name__=='__main__':main()
