import pymupdf as f, re, io
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
D=f.open('Plaquette HelloLead - Panneaux solaires (1).pdf')
bg=(244/255,245/255,252/255);blue=(10/255,91/255,1)
def font(p,n,x): p.insert_font(fontname=n,fontfile=f'work/font{x}.ttf')
def box(p,r,t,size=14,name='pr',color=(0,0,0),align=0):
 v=p.insert_textbox(f.Rect(r),t,fontname=name,fontsize=size,color=color,align=align)
 assert v>=0,(t,v)
# Keep the same Poppins body size as the adjacent cards (16 pt).
# Extend the middle card downward to accommodate the five complete entries.
p=D[1]
p.add_redact_annot(f.Rect(536,470,908,719),fill=bg)
p.apply_redactions(images=0,graphics=0)
p.draw_rect(f.Rect(519.69,449.62,920.46,790),color=None,fill=bg,radius=0.0524)
font(p,'pr',432);font(p,'pb',438)
p.insert_text((537.89,497.49),'Choix de leviers adaptés au',fontname='pb',fontsize=25,color=blue)
p.insert_text((537.89,526.74),'client :',fontname='pb',fontsize=25,color=blue)
items=["Télémarketing / Data propriétaire : Calls équipes internes et fichiers propriétaires","Marketing direct : SMS, RCS et emailing ciblés sur BDD propriétaires","Social Ads : Facebook, Instagram, LinkedIn…","SEA : Google Ads, Microsoft Ads…","Publicité conversationnelle IA : OpenAI Ads (ChatGPT)…"]
y=542.25
ft=f.Font(fontfile='work/font432.ttf')
for t in items:
 lines=[];s=''
 for w in t.split():
  if ft.text_length((s+' '+w).strip(),fontsize=16)>337:lines.append(s);s=w
  else:s=(s+' '+w).strip()
 lines.append(s)
 # Round bullets match the adjacent lists.
 p.draw_circle((551.76,y+10),2.3,color=None,fill=(0,0,0))
 for j,line in enumerate(lines):
  p.insert_text((565.09,y+16.8+j*23.25),line,fontname='pr',fontsize=16)
 y+=len(lines)*23.25+4
assert y<780,y
# Remove obsolete standalone text streams without concealing searchable text.
D.update_stream(446,b'');D.update_stream(606,b'')
# Form: remove old question and answers from the source stream.
s=D.xref_stream(601).decode('latin1')
for yy in ['616.32','598.42','573.42','548.42','523.42','498.41999']:
 s=re.sub(r'q [^q]*?BT/djr4 [^q]*?739 '+re.escape(yy)+r' TD.*?ET Q','',s) if yy!='616.32' else s
# precisely remove BT..ET for question/answers, preserving balanced graphics state
s=D.xref_stream(601).decode('latin1')
s=re.sub(r'BT/djr4 (?:8.6|8.5) Tf (?:717 616.32|739 (?:598.42|573.42|548.42|523.42|498.41999)) TD\[.*?\]TJ ET','',s)
D.update_stream(601,s.encode('latin1'))
# Remove all 5 old checkbox drawings in the reusable form, retain the next button.
s=D.xref_stream(600).decode('latin1');a=s.index('.784314 .819608 .847059 RG');b=s.index('.090196 .6 .784314 rg 854')
s=s[:a]+s[b:];D.update_stream(600,s.encode('latin1'))
p=D[3];font(p,'dr',535)
# PDF coordinates have media-box lower offset 7.92; visible y = 817.92 - PDF y.
box(p,(717,190,931,226),"Quel est l'objectif principal de l'installation de panneaux photovoltaïques ?",8.6,'dr',(.35,.4,.46))
for y,t in [(236,"L'auto consommation d'énergie"),(271,"La revente d'énergie solaire"),(306,"Louer votre toiture à un exploitant")]:
 p.draw_rect(f.Rect(719,y,732,y+13),color=(.78,.82,.85),fill=(1,1,1),width=.8)
 box(p,(739,y-1,933,y+28),t,8.5,'dr',(.09,.2,.33))
# Email CTA: rebuild the dark banner at 4x resolution, with identical pills.
im=Image.open('work/email-original.png').convert('RGB').resize((1284,3128),Image.Resampling.LANCZOS)
a=ImageDraw.Draw(im);scale=4
# Original banner extends from y=508 to y=652.
a.rectangle((0,508*4,1283,652*4),fill='#393939')
def txt(text,y,size,color):
 ft=ImageFont.truetype('work/font432.ttf',size*4);bb=a.textbbox((0,0),text,font=ft);a.text(((1284-(bb[2]-bb[0]))/2,y*4-bb[1]),text,font=ft,fill=color)
txt('Votre projet solaire chiffré en 1 minute,',525,7,'#f6d52c');txt('par des installateurs agréés RGE !',539,7,'#f6d52c')
txt('Trouvez l’installateur solaire qui correspond à votre projet',561,6,'#dddddd')
for x,label in [(20,"J’en profite"),(166,'Être rappelé par un installateur')]:
 rect=(x*4,583*4,(x+135)*4,611*4);a.rounded_rectangle(rect,radius=56,outline='#efd13b',width=4)
 ft=ImageFont.truetype('work/font432.ttf',20);bb=a.textbbox((0,0),label,font=ft)
 a.text(((x+67.5)*4-(bb[2]-bb[0])/2,597*4-(bb[3]-bb[1])/2-bb[1]),label,font=ft,fill='#efd13b')
im.save('work/email-corrige.png');D[6].replace_image(724,filename='work/email-corrige.png')
# Crop the new photographic-style visual to the exact panoramic window.
im=Image.open('work/equipe-realiste.png').convert('RGB');w,h=im.size;target=3729/1419
if w/h>target:
 nw=int(h*target);im=im.crop(((w-nw)//2,0,(w+nw)//2,h))
else:
 nh=int(w/target);im=im.crop((0,(h-nh)//2,w,(h+nh)//2))
im.save('work/equipe-panorama.jpg',quality=95)
D[7].replace_image(215,filename='work/equipe-panorama.jpg')
s=D.xref_stream(214).decode('latin1');s=s.replace('3729.5732 0 0 -1983.9335 .40332031 1700.3253 cm','3729 0 0 -1419 0 1419 cm');D.update_stream(214,s.encode('latin1'))
D.save('Plaquette HelloLead - Panneaux solaires - Corrigee.pdf',garbage=4,deflate=True)
for i in [1,2,3,6,7]: D[i].get_pixmap(matrix=f.Matrix(1.3,1.3)).save(f'work/controle-page-{i+1}.png')
print('PDF generated')
