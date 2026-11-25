"""Déclinaison HelloLead : caisses tactiles. Exécuter depuis la racine du dépôt."""
from pathlib import Path
import io
import pymupdf as f
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'Plaquette HelloLead - Panneaux solaires - Corrigee.pdf'
OUT = ROOT / 'Plaquette HelloLead - Caisses enregistreuses tactiles.pdf'
D = f.open(SRC)
BLUE = (0.06, .35, 1)
INK = (.10, .16, .25)
MUTED = (.40, .45, .53)
PALE = (.9569, .9608, .9882)
WHITE = (1, 1, 1)
FONT = f.Font(fontfile=str(ROOT/'work/font432.ttf'))
BOLD = f.Font(fontfile=str(ROOT/'work/font438.ttf'))

def fonts(p):
    p.insert_font(fontname='pr', fontfile=str(ROOT/'work/font432.ttf'))
    p.insert_font(fontname='pb', fontfile=str(ROOT/'work/font438.ttf'))

def rect(p, x, y, w, h, fill=PALE, radius=12, border=None):
    p.draw_rect(f.Rect(x,y,x+w,y+h), color=border, fill=fill, radius=min(radius/min(w,h), .49) if radius else None)

def text(p, x, y, s, size=18, width=300, bold=False, color=INK, leading=1.42, align=0):
    ft = BOLD if bold else FONT
    lines=[]
    for para in s.split('\n'):
        line=''
        for word in para.split():
            test=(line+' '+word).strip()
            if ft.text_length(test, fontsize=size)>width and line:
                lines.append(line); line=word
            else: line=test
        lines.append(line)
    for line in lines:
        xx=x
        if align==1: xx=x+(width-ft.text_length(line,fontsize=size))/2
        p.insert_text((xx,y+size),line,fontname='pb' if bold else 'pr',fontsize=size,color=color)
        y+=size*leading
    return y

def bullets(p,x,y,items,width=280,size=18,gap=15):
    for s in items:
        p.draw_circle((x+4,y+size*.7),2.3,fill=BLUE,color=None)
        y=text(p,x+19,y,s,size,width-19)+gap
    return y

IM_Boulangerie=Image.open(ROOT/'work/caisse-tactile.jpg').convert('RGB')
IM_Restaurant=Image.open(ROOT/'work/restaurant-caisse.jpg').convert('RGB')
IM_FastFood=Image.open(ROOT/'work/fastfood-caisse.jpg').convert('RGB')
IM_Epicerie=Image.open(ROOT/'work/epicerie-caisse.jpg').convert('RGB')
def photo(p, r, corners=False, im=None):
    if im is None: im=IM_Boulangerie
    w,h=int(r.width*1.5),int(r.height*1.5)
    ratio=max(w/im.width,h/im.height)
    z=im.resize((round(im.width*ratio), round(im.height*ratio)),Image.Resampling.LANCZOS)
    left=(z.width-w)//2;top=(z.height-h)//2
    z=z.crop((left,top,left+w,top+h)).convert('RGBA')
    if corners:
        mask=Image.new('L',(w,h)); ImageDraw.Draw(mask).rounded_rectangle((0,0,w,h),radius=55,fill=255); z.putalpha(mask)
    b=io.BytesIO();z.save(b,format='PNG');p.insert_image(r,stream=b.getvalue())

def label(p,x,y,s,w=220):
    rect(p,x,y,w,29,fill=(.90,.93,1),radius=9)
    text(p,x+12,y+4,s,12,w-24,bold=True,color=BLUE)

def button(p,x,y,s,w=220):
    rect(p,x,y,w,39,fill=BLUE,radius=10)
    text(p,x,y+7,s,14,w,bold=True,color=WHITE,align=1)

def field(p,x,y,title,value,w=305):
    y=text(p,x,y,title,14,w,bold=True,color=BLUE,leading=1.25)
    return text(p,x,y+3,value,16,w,leading=1.32)+12

def base(index,title,sub,items,tag):
    p=f.open(); page=p.new_page(width=1440,height=810);fonts(page)
    text(page,55,22,'HelloLead  /  CAISSES ENREGISTREUSES TACTILES',12,900,bold=True,color=MUTED)
    text(page,1280,22,f'0{index} / 09',12,105,color=MUTED,align=1)
    rect(page,55,75,345,674)
    y=text(page,78,98,title,31,300,bold=True,color=BLUE,leading=1.12)
    y=text(page,78,y+20,sub,22,297,color=BLUE,leading=1.25)
    y=bullets(page,78,y+29,items,294,17,17)
    assert y<715,(title,y)
    rect(page,430,75,555,674)
    label(page,451,94,tag,510)
    rect(page,1015,149,370,600)
    text(page,1038,172,'Modération &\nenrichissement',26,320,color=BLUE,leading=1.15)
    text(page,1038,244,'EXEMPLE DE LEAD FICTIF',11,320,bold=True,color=MUTED)
    # Directional progression between acquisition, capture and qualification.
    for x in [405,990]:
        page.draw_line((x,394),(x+18,394),color=BLUE,width=2)
        page.draw_polyline([(x+11,387),(x+18,394),(x+11,401)],color=BLUE,width=2)
    text(page,55,772,'Maquettes illustratives • Questions et critères de qualification proposés, à valider avec le formulaire CRM.',12,1270,color=MUTED)
    return p,page

def lead(p,fields,sector):
    y=279
    for k,v in fields: y=field(p,1038,y,k,v,321)
    assert y<667,y
    p.draw_line((1038,674),(1361,674),color=(.81,.85,.94),width=1)
    text(p,1038,686,sector,13,322,bold=True,color=BLUE)
    text(p,1038,710,'Contact décideur à vérifier avant livraison.',11,322,color=MUTED)

def replace_page(i,tmp):
    D.delete_page(i);D.insert_pdf(tmp,start_at=i);tmp.close()

# Couverture : identité de la plaquette d'origine, nouveau sujet et visuel.
old=D[0]
logo_mask = next(img[1] for img in old.get_images() if img[0] == 13)
logo = f.Pixmap(f.Pixmap(D, 13), f.Pixmap(D, logo_mask)).tobytes('png')
c=f.open();p=c.new_page(width=1440,height=810);fonts(p)
p.insert_image(f.Rect(98,95,429,166),stream=logo)
label(p,98,210,'GÉNÉRATION DE LEADS B2B',350)
y=text(p,98,274,'Caisses\nenregistreuses\ntactiles',47,555,bold=True,color=BLUE,leading=1.16)
text(p,98,y+27,'Rencontrez les professionnels\nqui souhaitent s’équiper.',25,550,bold=True,leading=1.35)
text(p,98,603,'CHR • Boulangeries • Restauration rapide\nCommerces alimentaires et de proximité',17,555,color=MUTED)
p.draw_line((98,718),(657,718),color=BLUE,width=2)
text(p,98,735,'Expert lead gen  /  Des projets à qualifier, des échanges à créer',13,560)
photo(p,f.Rect(720,0,1440,810),True)
replace_page(0,c)

# SMS / RCS
c,p=base(3,'SMS – RCS','Un contact direct\nsur mobile',[
    'Diffusion sur des bases professionnelles opt-in.',
    'Ciblage par activité et zone géographique.',
    'Messages adaptés aux enjeux du point de vente.',
    'Appel à l’action clair vers une page dédiée.',
    'Collecte du besoin, du délai et des coordonnées.'
],'DU MESSAGE AU PROJET')
# Two phone-like frames.
rect(p,455,149,226,548,fill=INK,radius=24)
rect(p,462,157,212,532,fill=WHITE,radius=20)
text(p,480,172,'Messages',15,175,bold=True)
rect(p,478,213,180,228,fill=PALE,radius=12)
sy=text(p,491,227,'Votre caisse\nvous ralentit ?',18,154,bold=True,color=BLUE,leading=1.25)
text(p,491,sy+18,'Découvrez une solution tactile adaptée à votre commerce. Décrivez votre projet.',13,151,leading=1.4)
button(p,478,457,'Voir les solutions',180)
text(p,480,516,'Annonce illustrative\nÉmetteur et modalités\nde désinscription à prévoir.',11,171,color=MUTED)
rect(p,705,149,255,548,fill=WHITE,radius=15)
photo(p,f.Rect(718,162,947,316),True)
y=text(p,721,333,'Une caisse pensée\npour votre activité',21,220,bold=True,color=BLUE,leading=1.2)
text(p,721,y+16,'Quel est votre secteur ?',14,218,bold=True)
for yy,s in [(454,'Café / Hôtel / Restaurant'),(494,'Boulangerie / Snacking'),(534,'Commerce alimentaire')]:
    rect(p,721,yy,224,33,fill=PALE,radius=7);text(p,730,yy+7,s,12,206)
button(p,721,600,'Décrire mon projet',224)
lead(p,[('Activité','Boulangerie-pâtisserie'),('Projet','Remplacer une caisse existante'),('Périmètre','1 point de vente · 2 terminaux'),('Besoins','Encaissement et fidélité'),('Budget indicatif','2 000 à 4 000 €'),('Échéance','Dans les 3 mois')],'BOULANGERIE')
replace_page(2,c)

# SEA
c,p=base(4,'SEA','Capter une recherche\nau bon moment',[
    'Réponse aux recherches liées aux caisses tactiles.',
    'Groupes d’annonces par métier et par besoin.',
    'Pages dédiées : restaurant, boulangerie, commerce…',
    'Mesure des conversions et optimisation des campagnes.',
    'Qualification du projet avant transmission.'
],'UNE PAGE DÉDIÉE À L’INTENTION')
rect(p,451,147,510,68,fill=WHITE,radius=10)
text(p,469,157,'RECHERCHE ILLUSTRATIVE',10,470,bold=True,color=MUTED)
text(p,469,178,'caisse tactile pour restaurant',20,469,color=INK)
photo(p,f.Rect(451,231,961,411),True,IM_Restaurant)
rect(p,451,427,510,286,fill=WHITE,radius=12)
text(p,472,441,'Équipez votre restaurant',25,466,bold=True,color=BLUE)
text(p,472,480,'Quel est l’objectif de votre projet ?',17,465,bold=True)
for yy,s in [(520,'Une première installation'),(560,'Le remplacement de mon équipement'),(600,'L’équipement de plusieurs sites')]:
    p.draw_rect(f.Rect(474,yy+3,488,yy+17),color=(.7,.75,.84),width=1)
    text(p,501,yy,s,15,431)
button(p,692,656,'Préciser mon besoin',246)
lead(p,[('Activité','Restaurant traditionnel'),('Projet','Première installation'),('Périmètre','1 établissement · 2 terminaux'),('Besoins','Plan de salle et prise de commande'),('Budget indicatif','À définir avec le fournisseur'),('Échéance','Ouverture dans 2 mois')],'CAFÉS • HÔTELS • RESTAURANTS')
replace_page(3,c)

# META
c,p=base(5,'META Ads','Donner envie de\nfaire évoluer sa caisse',[
    'Créations adaptées aux usages de chaque métier.',
    'Ciblage et audiences personnalisées selon les possibilités des plateformes.',
    'Formulaire instantané ou page dédiée.',
    'Tests de visuels et de messages.',
    'Validation du besoin et de la maturité du projet.'
],'UNE CRÉATION MÉTIER, UN PARCOURS COURT')
rect(p,479,148,455,566,fill=WHITE,radius=13)
p.draw_circle((511,178),13,fill=BLUE,color=None)
text(p,535,160,'Solutions d’encaissement',17,355,bold=True)
text(p,535,184,'Sponsorisé · Maquette illustrative',11,350,color=MUTED)
photo(p,f.Rect(493,221,920,446),True,IM_FastFood)
y=text(p,500,466,'Le coup de feu mérite\nune caisse à la hauteur.',25,415,bold=True,color=BLUE,leading=1.2)
text(p,500,y+15,'Commandes, menus, encaissement : présentez vos besoins et échangez avec un fournisseur.',16,414,leading=1.42)
button(p,500,646,'Étudier mon projet',412)
lead(p,[('Activité','Restauration rapide'),('Projet','Faire évoluer la solution existante'),('Périmètre','2 points de vente'),('Besoins','Commandes et suivi multi-sites'),('Mode souhaité','Abonnement à étudier'),('Échéance','Dans les 3 à 6 mois')],'RESTAURATION RAPIDE')
replace_page(4,c)

# CALL
c,p=base(6,'CALL','L’échange humain\npour préciser le projet',[
    'Ciblage B2B par activité et zone de prospection.',
    'Identification du décideur et de l’établissement.',
    'Échange sur l’équipement et les usages actuels.',
    'Qualification du périmètre, du budget et du délai.',
    'Confirmation de l’intérêt et des coordonnées.'
],'UNE TRAME D’ÉCHANGE ADAPTÉE AUX MÉTIERS')
text(p,457,153,'Comprendre avant de transmettre',25,505,bold=True,color=BLUE,leading=1.2)
y=236
for num,title,body in [
    ('01','L’existant','Quel équipement utilisez-vous aujourd’hui ? Qu’est-ce qui motive le changement ?'),
    ('02','Le fonctionnement','Combien de sites et de terminaux ? Quels usages : tables, stocks, commandes, fidélité ?'),
    ('03','Le projet','Quel calendrier, quel budget ou mode de financement ? Qui décide de l’équipement ?'),
    ('04','La suite','Valider l’intérêt pour un échange avec un fournisseur et le créneau de rappel souhaité.')]:
    rect(p,455,y,506,101,fill=WHITE,radius=11)
    text(p,470,y+15,num,23,52,bold=True,color=BLUE)
    text(p,532,y+10,title,18,409,bold=True)
    text(p,532,y+39,body,14,407,leading=1.35)
    y+=115
lead(p,[('Activité','Commerce alimentaire indépendant'),('Projet','Remplacer une caisse vieillissante'),('Périmètre','1 magasin · 1 terminal'),('Besoins','Stocks et gestion des articles'),('Décideur','Gérant de l’établissement'),('Suite souhaitée','Présentation de la solution')],'COMMERCE ALIMENTAIRE')
replace_page(5,c)

# Email
c,p=base(7,'Emailing','Une prospection\nciblée et personnalisée',[
    'Segmentation des établissements par activité.',
    'Message adapté à la réalité du point de vente.',
    'Création dédiée ou campagne en marque blanche.',
    'Lien vers un formulaire de projet.',
    'Suivi des clics, des demandes et des conversions.'
],'UN MESSAGE CENTRÉ SUR LE BESOIN')
rect(p,463,149,489,565,fill=WHITE,radius=13)
text(p,484,168,'OBJET',11,445,bold=True,color=MUTED)
text(p,484,192,'Et si votre caisse suivait votre rythme ?',19,445,bold=True)
p.draw_line((483,234),(931,234),color=PALE,width=2)
photo(p,f.Rect(484,250,931,443),True,IM_Epicerie)
y=text(p,484,460,'Un encaissement adapté\nà votre commerce.',25,447,bold=True,color=BLUE,leading=1.2)
text(p,484,y+14,'Première installation ou remplacement : partagez vos priorités pour être recontacté au sujet de votre projet.',16,443,leading=1.4)
button(p,484,637,'Être recontacté pour mon projet',447)
text(p,484,688,'Maquette • Mentions et lien de désinscription à intégrer.',10,445,color=MUTED)
lead(p,[('Activité','Commerce de proximité'),('Projet','Moderniser l’encaissement'),('Périmètre','3 magasins'),('Besoins','Suivi centralisé et fidélité'),('Budget indicatif','À préciser'),('Échéance','Dans les 6 mois')],'COMMERCE MULTI-SITES')
replace_page(6,c)

# Marquer explicitement la thématique sur les pages génériques conservées.
for i in [1,7]:
    p=D[i]; fonts(p)
    text(p,76,14,'CAISSES ENREGISTREUSES TACTILES  /  NOTRE MÉTHODE',11,900,bold=True,color=MUTED)
# Ajouter un pied discret aux pages génériques sans changer leur contenu.
for i in [1,7]:
    p=D[i];text(p,1320,789,f'0{i+1} / 09',10,90,color=MUTED)
D.set_metadata({'title':'HelloLead — Caisses enregistreuses tactiles','author':'HelloLead','subject':'Génération de leads B2B pour les fournisseurs de solutions d’encaissement','keywords':'caisses tactiles, leads, CHR, boulangerie, commerce, HelloLead'})
D.save(OUT,garbage=4,deflate=True)
D.close()
print(OUT)
# Contrôle automatisé : format, nombre de pages et absence de l’ancienne verticale.
check=f.open(OUT)
assert len(check)==9
for i,p in enumerate(check):
    s=p.get_text().lower()
    for forbidden in ['solaire','photovolta','toiture','kwh','kwc','surplus']:
        assert forbidden not in s,(i+1,forbidden)
    for b in p.get_text('dict')['blocks']:
        if 'lines' not in b: continue
        for line in b['lines']:
            for sp in line['spans']:
                r=f.Rect(sp['bbox']);assert r.x0>=0 and r.y0>=0 and r.x1<=1441 and r.y1<=811,(i+1,sp)
    p.get_pixmap(matrix=f.Matrix(.75,.75)).save(ROOT/f'work/caisses-controle-{i+1}.png')
print('Contrôles réussis : 9 pages, texte dans les pages, aucune référence solaire.')
