# -*- coding: utf-8 -*-
"""
Création dela plaquette HelloLead « Caisses enregistreuses tactiles ».
Déclinaison de la plaquette solaire corrigée (même charte, même structure).
Commande depuis la racine : .venv/bin/python work/creer_caisses.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pymupdf
from plaquette_lib import (Page, W, H, BLUE, PALE, GREY_TITLE, BLACK, MUTED,
                           NAVY, LIGHT_LINE, wrap, text_width, draw_text,
                           text_center, text_right, panel, card, rect, line,
                           image, pill, curved_arrow, circle, arrow, GEN)

ROOT = Path(__file__).resolve().parent.parent
SOLAR = ROOT / "Plaquette HelloLead - Panneaux solaires - Corrigee.pdf"
OUT = ROOT / "Plaquette HelloLead - Caisses enregistreuses tactiles.pdf"
A = Path(__file__).resolve().parent  # assets

BLUE = BLUE
DARK = "#111111"
SOFT = "#737373"
BORDER = "#DDE1EC"
ORANGE = "#F08A45"


# ---------------------------------------------------------------- composants
def left_column(pg, title, subtitle, bullets, top=28, bottom_min=560,
                note=None, subtitle_size=24):
    """Colonne de gauche : panneau pale, titre, accroche et puces."""
    x, w = 61, 384
    y = top + 18
    ops = []
    title_lines = wrap(title, "PB", 30, w)
    for ln in title_lines:
        ops.append(("t", title_lines.index(ln) * 0 + 0, y, ln, "PB", 30, BLUE))
        y += 40
    y += 8
    for ln in wrap(subtitle, "PR", subtitle_size, w - 4):
        ops.append(("t", 0, y, ln, "PR", subtitle_size, BLUE))
        y += subtitle_size * 1.18
    y += 18
    for b in bullets:
        lines = wrap(b, "PR", 14, w - 24)
        ops.append(("b", 0, y, lines, "PR", 14, BLACK))
        y += len(lines) * 23.5 + 22
    if note:
        y += 4
        for ln in wrap(note, "PR", 8, w - 20):
            ops.append(("t", 0, y, ln, "PR", 8, "#8A93A3"))
            y += 11
    bottom = max(bottom_min, y + 14)
    panel(pg.page, (44, top, 466, bottom))
    for op in ops:
        if op[0] == "t":
            draw_text(pg.page, x + op[1], op[2], op[3], op[4], op[5], op[6])
        else:
            draw_text(pg.page, x + 2, op[2] + 0.5, "•", "PR", 14, BLACK)
            for i, ln in enumerate(op[3]):
                draw_text(pg.page, x + 18, op[2] + i * 23.5, ln, "PR", 14, BLACK)
    return bottom


def right_panel(pg, fields, company, title=("Modération &", "Enrichissement"),
                bottom=792, x=1080, width=316):
    """Panneau « Modération & Enrichissement » + exemple de lead."""
    tx = x + 19
    tw = width - 32
    ops = []
    y = 0
    for ln in title:
        ops.append(("t", tx, y, ln, "PR", 25, BLUE))
        y += 29.5
    y += 8
    for label, value in fields:
        for ln in wrap(label, "PB", 13, tw):
            ops.append(("t", tx, y, ln, "PB", 13, BLUE))
            y += 19.5
        for ln in wrap(value, "PR", 13, tw):
            ops.append(("t", tx, y, ln, "PR", 13, BLACK))
            y += 19.5
        y += 4
    # entreprise / lead
    y += 10
    for item in company:
        if item[0] == "t":
            for ln in wrap(item[1], "PR", 13, tw):
                ops.append(("t", tx, y, ln, "PR", 13, BLACK))
                y += 19.5
        else:  # champ masqué
            draw_y = y
            ops.append(("mask", tx, draw_y, item))
            y += 19.5
    height = y
    top = bottom - height - 42
    top = max(top, 90)
    panel(pg.page, (x, top, x + width, bottom))
    for op in ops:
        if op[0] == "t":
            draw_text(pg.page, op[1], top + 24 + op[2], op[3], op[4], op[5], op[6])
        else:
            label, bar_w = op[3][1], op[3][2]
            yy = top + 24 + op[2]
            draw_text(pg.page, op[1], yy, label, "PR", 13, BLACK)
            bx = op[1] + text_width(label, "PR", 13) + 6
            rect(pg.page, (bx, yy + 7, bx + bar_w, yy + 15), fill="#A9A9A9")
    return top


def mock_label(pg, x, y, s, size=7, color=SOFT, font="PS"):
    pg.t(x, y, s, font, size, color)


def input_box(pg, r, placeholder, size=8, chevron=True, fill="#FFFFFF"):
    pg.rect(r, fill=fill, color="#D7DBE6", width=0.8, radius=4)
    pg.t(r[0] + 10, (r[1] + r[3]) / 2 - size * 0.75, placeholder, "PR", size, "#8A93A3")
    if chevron:
        cx = r[2] - 14
        cy = (r[1] + r[3]) / 2
        pg.page.draw_polyline([pymupdf.Point(cx - 4, cy - 2),
                               pymupdf.Point(cx, cy + 2),
                               pymupdf.Point(cx + 4, cy - 2)],
                              color=(0.45, 0.48, 0.55), width=1)


def checkbox(pg, x, y, checked=False, size=8, label=None, lsize=7.5):
    pg.rect((x, y, x + size, y + size), fill="#FFFFFF", color="#9AA4B5", width=0.7,
            radius=1.2)
    if checked:
        pg.page.draw_polyline([pymupdf.Point(x + 2, y + size * 0.55),
                               pymupdf.Point(x + size * 0.42, y + size - 2.2),
                               pymupdf.Point(x + size - 1.6, y + 2.2)],
                              color=(0.04, 0.36, 1.0), width=1.6)
    if label:
        draw_text(pg.page, x + size + 6, y - 1, label, "PR", lsize, "#2B2F36")


# ------------------------------------------------------------------- page 1
def page_cover(doc):
    pg = Page(doc)
    p = pg.page
    # logo
    image(p, A / "logo-render.png", (186, 118, 546, 195))
    # titre
    for i, ln in enumerate(["Caisses", "enregistreuses", "tactiles"]):
        text_center(p, 360, 238 + i * 80, ln, "PE", 59, GREY_TITLE)
    # accroche
    sub = ("Des leads qualifiés auprès des CHR, boulangeries, restauration "
           "rapide et commerces alimentaires")
    y = 500
    for ln in wrap(sub, "PB", 26, 580):
        text_center(p, 360, y, ln, "PB", 26, BLUE)
        y += 36
    # pied
    pg.t(81, 690, "Expert lead gen", "PR", 20, BLACK)
    line(p, (81, 742), (720, 742), BLUE, 2)
    # visuel
    image(p, A / "photo-cover.jpg", (720, 0, 1500, 810), radius=34,
          corners=(1, 0, 0, 1), crop_ratio=780 / 810)
    return pg


# ------------------------------------------------------------------- page 3
def page_sms(doc):
    pg = Page(doc)
    p = pg.page
    left_column(
        pg, "SMS - RCS",
        "Un contact direct et immédiat sur mobile",
        ["Taux de lecture quasi instantané",
         "Base propriétaire opt-in de gérants et de décideurs",
         "Ciblage précis : métier, zone de chalandise, nombre de points de vente",
         "Message court avec call-to-action clair : demande de démo",
         "Redirection vers une landing page dédiée",
         "Leads rapides, réactifs et intentionnistes"],
        note=("Maquette illustrative : enseignes, chiffres et coordonnées fictifs. "
              "Questions et champs à valider avec le formulaire CRM n° 2015589."),
    )

    # panneau central
    panel(pg.page, (483, 40, 1065, 762))
    pg.t(512, 66, "Campagnes immersives et personnalisées", "PR", 24, BLUE)
    pg.t(512, 97, "SMS enrichi et RCS : un visuel, un message, une action.", "PR", 10.5,
         MUTED)

    cards = [
        ("photo-boulangerie.jpg", "CAISSE TACTILE", "Une caisse pensée pour la boulangerie",
         "Encaissez plus vite, gérez vos stocks sur un seul écran.",
         "Demander une démo", 112),
        ("photo-restaurant.jpg", "CAISSE TACTILE", "Le service, sans friction en salle",
         "Commandes, addition et encaissement sur un même écran.",
         "Être rappelé", 310),
    ]
    for photo, over, title, body, cta, top in cards:
        card(pg.page, (512, top, 722, top + 188), radius=9)
        image(p, A / photo, (512, top, 722, top + 78), corners=(1, 1, 0, 0),
              crop_ratio=210 / 78)
        pg.t(524, top + 86, over, "PB", 6.5, BLUE)
        yy = top + 98
        for ln in wrap(title, "PB", 11.5, 186):
            pg.t(524, yy, ln, "PB", 11.5, "#1A1D24")
            yy += 15
        yy = max(yy, top + 128)
        for ln in wrap(body, "PR", 8, 186):
            pg.t(524, yy + 3, ln, "PR", 8, MUTED)
            yy += 11
        pill(pg.page, (524, top + 158, 710, top + 180), cta, BLUE, "#FFFFFF", "PS", 8.5)

    # aperçu SMS
    card(pg.page, (512, 508, 722, 700), radius=9)
    pg.t(524, 520, "SMS - RCS", "PB", 9, BLUE)
    pg.tr(710, 520, "CaissePro", "PS", 7, SOFT)
    line(p, (524, 536), (710, 536), LIGHT_LINE, 0.8)
    bubble = ("Bonjour M. Lefèvre, votre projet de caisse tactile nous intéresse. "
              "Recevez un comparatif gratuit en 1 clic.")
    by = 546
    hp = 0
    for ln in wrap(bubble, "PR", 7.8, 150):
        hp += 12
    pg.rect((524, by, 698, by + hp + 18), fill="#EDF0F7", radius=8)
    yy = by + 8
    for ln in wrap(bubble, "PR", 7.8, 150):
        pg.t(532, yy, ln, "PR", 7.8, "#252A32")
        yy += 12
    pill(pg.page, (524, by + hp + 26, 698, by + hp + 46), "Je veux une démo", BLUE,
         "#FFFFFF", "PS", 8)
    pg.t(524, by + hp + 54, "SMS vérifié · 134 caractères · lien tracké", "PR", 6.8, SOFT)

    # landing page
    card(pg.page, (742, 112, 1040, 706), radius=10)
    pg.t(756, 126, "CaissePro", "PB", 15, BLUE)
    pg.tr(1026, 128, "marque blanche", "PR", 6.8, SOFT)
    line(p, (742, 152), (1040, 152), LIGHT_LINE, 0.9)
    image(p, A / "photo-lp.jpg", (742, 153, 1040, 278), crop_ratio=298 / 125)
    yy = 290
    for ln in wrap("Trouvez la caisse tactile adaptée à votre établissement", "PB", 12,
                   268):
        pg.t(756, yy, ln, "PB", 12, "#122C4A")
        yy += 15
    for ln in wrap("Comparez les solutions et les logiciels de gestion adaptés à votre "
                   "métier, avec un installateur de votre région.", "PR", 8, 268):
        pg.t(756, yy + 2, ln, "PR", 8, MUTED)
        yy += 11
    yy += 10
    pg.t(756, yy, "Votre métier :", "PS", 8, "#1A1D24")
    yy += 15
    for lab in ["Restaurant / café", "Boulangerie / pâtisserie", "Commerce alimentaire"]:
        pg.page.draw_circle((761, yy + 4), 3.2, color=(0.6, 0.64, 0.7), width=0.8,
                            fill=(1, 1, 1))
        draw_text(p, 770, yy, lab, "PR", 7.6, "#2B2F36")
        yy += 16
    yy += 4
    pg.t(756, yy, "Nombre de points de vente :", "PS", 8, "#1A1D24")
    yy += 13
    input_box(pg, (756, yy, 1026, yy + 24), "Sélectionner", 7.6)
    yy += 32
    pg.t(756, yy, "Vous souhaitez être équipé :", "PS", 8, "#1A1D24")
    yy += 13
    for i, lab in enumerate(["Sous 3 mois", "3 à 6 mois", "Plus de 6 mois"]):
        r = (756 + i * 92, yy, 756 + i * 92 + 86, yy + 20)
        pg.rect(r, fill="#F2F5FA" if i else "#E7EEFF",
                color=BLUE if i == 0 else "#DDE1EC", width=0.8, radius=10)
        text_center(p, (r[0] + r[2]) / 2, yy + 5.5, lab, "PS", 6.8,
                    BLUE if i == 0 else "#4A5364")
    yy += 28
    checkbox(pg, 756, yy, checked=True, size=7)
    pg.t(768, yy - 1, "J'accepte d'être recontacté par un conseiller", "PR", 6.5, MUTED)
    yy += 14
    pg.rect((756, yy, 1026, yy + 30), fill=BLUE, radius=5)
    text_center(p, 891, yy + 9, "Recevoir mon comparatif gratuit", "PS", 8.5, "#FFFFFF")
    yy += 40
    pg.t(756, yy, "Réponse sous 24 h · Devis gratuit · Sans engagement", "PR", 6.5, SOFT)
    line(p, (756, yy + 18), (1026, yy + 18), "#E7EAF0", 0.9)
    pg.t(756, yy + 28, "Ce que vous recevez :", "PS", 8, "#1A1D24")
    avantages = [("Un comparatif de 2 à 3 solutions", "adaptées à votre métier"),
                 ("L'avis d'un installateur local", "et un devis chiffré"),
                 ("Un accompagnement à la reprise", "de vos données de caisse")]
    yb = yy + 44
    for i, (l1, l2) in enumerate(avantages):
        circle(p, (762, yb + 4), 5, fill=BLUE)
        p.draw_polyline([pymupdf.Point(759.2, yb + 4),
                         pymupdf.Point(761.2, yb + 6.2),
                         pymupdf.Point(764.8, yb + 1.8)],
                        color=(1, 1, 1), width=1.1)
        pg.t(772, yb - 1, l1, "PS", 6.5, "#1A1D24")
        pg.t(772, yb + 8, l2, "PR", 6.2, MUTED)
        yb += 24
    pg.t(756, yb + 2, "Données traitées conformément au RGPD.", "PR", 5.8, "#9AA3B0")

    # annotation
    pg.t(512, 714, "→  Lien du SMS / RCS vers la landing page (formulaire)", "PR", 9.5,
         BLUE)

    fields = [
        ("Type d'établissement :", "Boulangerie-pâtisserie artisanale"),
        ("Statut de l'acheteur :", "Gérant (B2B), propriétaire"),
        ("Nombre de points de vente :", "2 boutiques"),
        ("Type de caisse recherchée :", "Caisse tactile 15\" avec logiciel de gestion"),
        ("Budget envisagé :", "1 500 € à 3 000 €"),
        ("Sous quel délai souhaitez-vous être équipé ?", "Moins de 3 mois"),
    ]
    company = [
        ("t", "Entreprise : BOULANGERIE DES HALLES"),
        ("t", "Siret : 91234567800021"),
        ("t", "Activité : (Boulangerie-pâtisserie artisanale,"),
        ("t", "2 boutiques)"),
        ("mask", "Contact :", 84),
        ("t", "Adresse : 12 rue des Halles"),
        ("t", "Ville : Lyon"),
        ("t", "Code postal : 69002"),
        ("mask", "Tél :", 74),
        ("mask", "Mail :", 128),
    ]
    right_panel(pg, fields, company)
    return pg


# ------------------------------------------------------------------- page 4
def page_sea(doc):
    pg = Page(doc)
    p = pg.page
    left_column(
        pg, "SEA - Google Ads",
        "Capter l'intention au moment de la recherche",
        ["Présence sur les requêtes « caisse enregistreuse tactile », « logiciel de "
         "caisse restaurant »…",
         "Le lead capté à la source du besoin",
         "Ciblage local par zone de chalandise",
         "Métriques précises : clics, coût par lead, taux de conversion",
         "Annonces et extensions adaptées à chaque métier",
         "Puissance de l'IA native de Google Ads",
         "Pilotage total et stratégie data-driven"],
        note=("Maquette illustrative : enseignes, chiffres et coordonnées fictifs. "
              "Questions et champs à valider avec le formulaire CRM n° 2015589."),
    )

    panel(pg.page, (483, 40, 1065, 762))
    pg.t(512, 66, "LP : visuels et messages de capture", "PR", 24, BLUE)
    pg.t(512, 97, "Annonce search, puis landing page : chaque clic mène au formulaire.",
         "PR", 10.5, MUTED)

    # --- résultats Google
    card(pg.page, (512, 112, 1040, 300), radius=8)
    letters = [("G", "#4285F4"), ("o", "#EA4335"), ("o", "#FBBC05"),
               ("g", "#4285F4"), ("l", "#34A853"), ("e", "#EA4335")]
    gx = 528
    for ch, col in letters:
        draw_text(p, gx, 124, ch, "PB", 20, col)
        gx += text_width(ch, "PB", 20)
    pg.rect((620, 122, 1024, 150), fill="#FFFFFF", color="#DFE2E8", width=0.9,
            radius=14)
    pg.t(634, 130, "caisse enregistreuse tactile restaurant", "PR", 8.5, "#33383F")
    circle(p, (1006, 136), 4.2, color=(0.35, 0.42, 0.55), width=1.1)
    p.draw_line(pymupdf.Point(1009, 139), pymupdf.Point(1013, 143),
                color=(0.35, 0.42, 0.55), width=1.1)
    tabs = [("Tous", True), ("Images", False), ("Actualités", False),
            ("Vidéos", False), ("Maps", False)]
    tx = 528
    for lab, active in tabs:
        draw_text(p, tx, 158, lab, "PR", 7, BLUE if active else "#5F6368")
        if active:
            p.draw_line(pymupdf.Point(tx, 169), pymupdf.Point(tx + 22, 169),
                        color=(0.04, 0.36, 1.0), width=1.6)
        tx += text_width(lab, "PR", 7) + 20
    line(p, (512, 175), (1040, 175), "#E8EAED", 0.9)
    # annonce
    pg.t(528, 184, "Sponsorisé", "PS", 7.2, "#202124")
    pg.t(528, 198, "caissepro.fr › caisses-tactiles", "PR", 7, "#1B6B3A")
    pg.t(528, 210, "Caisse tactile pour restaurant | Démo gratuite en 24 h", "PR", 13,
         "#1A0DAB")
    for i, ln in enumerate(wrap("Comparez les caisses tactiles et les logiciels de "
                               "gestion adaptés aux CHR : installation, reprise de "
                               "données et formation incluses.", "PR", 8, 470)):
        pg.t(528, 230 + i * 11, ln, "PR", 8, "#4D5156")
    links = ["Caisse pour café", "Logiciel de caisse", "Demander une démo"]
    lx = 528
    for lab in links:
        draw_text(p, lx, 256, lab, "PR", 7.2, "#1A0DAB")
        lx += text_width(lab, "PR", 7.2) + 22
    # résultat organique
    line(p, (528, 274), (1024, 274), "#EBEDEF", 0.7)
    pg.t(528, 280, "Caisse tactile : le comparatif 2026 des solutions pour CHR", "PR",
         8.2, "#1A0DAB")

    # --- formulaire
    card(pg.page, (512, 314, 1040, 724), radius=8)
    pg.rect((512, 314, 1040, 378), fill=NAVY, radius=8)
    pg.rect((512, 360, 1040, 378), fill=NAVY)
    pg.t(528, 326, "Extrait du formulaire", "PB", 15, "#FFFFFF")
    pg.t(528, 352, "Étape 2 - Précisez votre établissement", "PR", 8.5, "#D6E2F0")
    yy = 396
    pg.t(528, yy, "Quel est votre métier ?", "PB", 10, "#16324F")
    yy += 22
    metiers = ["Café / bar", "Hôtel", "Restaurant", "Boulangerie", "Restauration rapide",
               "Commerce alimentaire"]
    for i, lab in enumerate(metiers):
        col = i % 2
        row = i // 2
        xx = 528 + col * 200
        yyy = yy + row * 22
        checkbox(pg, xx, yyy, checked=(lab == "Restaurant"), size=7.5)
        draw_text(p, xx + 14, yyy - 1, lab, "PR", 7.6, "#2B2F36")
    yy += 22 + 26
    line(p, (528, yy), (1024, yy), "#E7EAF0", 0.9)
    yy += 14
    pg.t(528, yy, "Combien de points de vente gérez-vous ?", "PB", 10, "#16324F")
    yy += 22
    for lab in ["1 établissement", "2 à 5 établissements", "Plus de 5 établissements"]:
        circle(p, (532, yy + 4), 3.1, color=(0.6, 0.64, 0.7), width=0.8,
                      fill=(1, 1, 1))
        draw_text(p, 542, yy, lab, "PR", 7.6, "#2B2F36")
        yy += 18
    yy += 6
    line(p, (528, yy), (1024, yy), "#E7EAF0", 0.9)
    yy += 14
    pg.t(528, yy, "Quel budget avez-vous prévu pour votre caisse ?", "PB", 10, "#16324F")
    yy += 22
    for lab in ["Moins de 1 500 €", "1 500 € à 4 000 €", "Plus de 4 000 €"]:
        circle(p, (532, yy + 4), 3.1, color=(0.6, 0.64, 0.7), width=0.8,
                      fill=(1, 1, 1))
        draw_text(p, 542, yy, lab, "PR", 7.6, "#2B2F36")
        yy += 18
    pg.t(528, 692, "Étape 2 sur 3", "PR", 7, "#8A93A3")
    pg.rect((944, 682, 1024, 708), fill="#1273C8", radius=4)
    text_center(p, 984, 690, "Suivant", "PS", 8.5, "#FFFFFF")

    fields = [
        ("Type d'établissement :", "Restaurant traditionnel (90 couverts)"),
        ("Statut de l'acheteur :", "Gérant (B2B), décideur"),
        ("Type de caisse recherchée :", "Caisse tactile + logiciel de gestion"),
        ("Fonction attendue :", "Prise de commande à table"),
        ("Budget envisagé :", "2 500 € à 5 000 €"),
        ("Sous quel délai souhaitez-vous être équipé ?", "1 à 3 mois"),
    ]
    company = [
        ("t", "Entreprise : LE COMPTOIR DU MARCHÉ"),
        ("t", "Siret : 90135792400035"),
        ("t", "Activité : (Restauration traditionnelle,"),
        ("t", "90 couverts)"),
        ("mask", "Contact :", 88),
        ("t", "Adresse : 8 quai Saint-Antoine"),
        ("t", "Ville : Lyon"),
        ("t", "Code postal : 69002"),
        ("mask", "Tél :", 76),
        ("mask", "Mail :", 132),
    ]
    right_panel(pg, fields, company)
    return pg


# ------------------------------------------------------------------- page 5
def page_meta(doc):
    pg = Page(doc)
    p = pg.page
    left_column(
        pg, "META Ads",
        "Une audience puissante à maîtriser",
        ["Ciblage des gérants et décideurs CHR par fonction et centres d'intérêt",
         "Audiences personnalisées à partir de nos bases intentionnistes",
         "Créations adaptées à chaque métier : boulangerie, restauration, commerce",
         "Formulaires instantanés ou redirection vers landing page",
         "Tests A/B continus pour améliorer le taux de conversion",
         "Pilotage en temps réel et ajustement des campagnes"],
        note=("Maquette illustrative : enseignes, chiffres et coordonnées fictifs. "
              "Questions et champs à valider avec le formulaire CRM n° 2015589."),
    )

    panel(pg.page, (483, 40, 1065, 762))
    pg.t(512, 66, "Formulaire instantané ou landing page", "PR", 24, BLUE)
    pg.t(512, 97, "Un visuel par métier, un formulaire sans friction.", "PR", 10.5, MUTED)

    # --- post sponsorisé
    card(pg.page, (512, 112, 760, 540), radius=8)
    pg.t(526, 124, "facebook", "PB", 12, "#1877F2")
    p.draw_circle((742, 128), 4, color=(0.52, 0.57, 0.64), width=1)
    p.draw_line(pymupdf.Point(745, 131), pymupdf.Point(748, 134),
                color=(0.52, 0.57, 0.64), width=1)
    line(p, (512, 146), (760, 146), "#E6E8EB", 0.9)
    circle(p, (530, 166), 12, fill="#E7EEFF", color=None)
    text_center(p, 530, 159, "CP", "PB", 7.5, BLUE)
    pg.t(548, 154, "CaissePro", "PB", 8, "#1C1E21")
    pg.t(548, 167, "Sponsorisé", "PR", 6.4, "#65676B")
    yy = 186
    for ln in wrap("CAISSE TACTILE 2026 — La caisse qui suit le rythme du service, "
                   "même en plein rush.", "PR", 7.6, 210):
        pg.t(522, yy, ln, "PR", 7.6, "#1C1E21")
        yy += 11
    image(p, A / "photo-rapide.jpg", (512, 214, 760, 430), crop_ratio=248 / 216)
    # aperçu du lien
    pg.rect((512, 430, 760, 490), fill="#F0F2F5")
    pg.t(522, 438, "CAISSEPRO.FR", "PR", 6, "#65676B")
    pg.t(522, 448, "Caisse tactile pour la restauration rapide", "PB", 7.4, "#1C1E21")
    pg.t(522, 460, "Devis gratuit, installation et formation incluses.", "PR", 6.2,
         "#65676B")
    pg.rect((668, 470, 750, 482), fill="#E4E6EB", radius=3)
    text_center(p, 709, 471.5, "En savoir plus", "PS", 5.8, "#050505")
    # barre d'engagement
    line(p, (512, 498), (760, 498), "#E6E8EB", 0.9)
    labels = ["J'aime", "Commenter", "Partager"]
    for i, lab in enumerate(labels):
        cx = 554 + i * 76
        text_center(p, cx, 508, lab, "PR", 6.4, "#65676B")

    # --- carrousel
    pg.t(512, 560, "Carrousel : un visuel par métier", "PS", 8.5, "#1A1D24")
    metas = [("photo-patisserie.jpg", "Boulangerie"), ("photo-epicerie.jpg", "Commerce"),
             ("photo-restaurant.jpg", "Restaurant")]
    for i, (ph, lab) in enumerate(metas):
        x0 = 512 + i * 84
        image(p, A / ph, (x0, 578, x0 + 76, 654), radius=5, crop_ratio=76 / 76)
        pg.t(x0 + 2, 658, lab, "PS", 6.2, "#5A6472")
    pg.t(512, 674, "Formats 4:5 et 9:16 déclinés automatiquement.", "PR", 6.4, SOFT)

    # --- formulaire instantané
    card(pg.page, (774, 112, 1040, 724), radius=8)
    pg.rect((774, 112, 1040, 232), fill="#122C4A", radius=8)
    pg.rect((774, 210, 1040, 232), fill="#122C4A")
    circle(p, (1002, 140), 16, fill="#1E4A78", color=None)
    pg.t(792, 130, "CaissePro", "PB", 13, "#FFFFFF")
    pg.t(792, 152, "Caisse tactile & logiciel de gestion", "PR", 7, "#BFD2E6")
    pg.t(792, 176, "Recevez votre comparatif", "PB", 11, "#FFFFFF")
    pg.t(792, 194, "3 questions · 1 minute · réponse sous 24 h", "PR", 6.8, "#CFE0F0")

    yy = 248
    questions = [("Quel est votre métier ?", "Sélectionner"),
                 ("Combien de points de vente ?", "Sélectionner"),
                 ("Quand souhaitez-vous être équipé ?", "Sélectionner")]
    for q, ph in questions:
        pg.t(790, yy, q, "PS", 7.6, "#1A1D24")
        yy += 13
        input_box(pg, (790, yy, 1024, yy + 26), ph, 7.4)
        yy += 38
    checkbox(pg, 790, yy, checked=True, size=6.5)
    pg.t(801, yy - 1, "J'accepte d'être recontacté par CaissePro", "PR", 6.2, MUTED)
    yy += 18
    pg.rect((790, yy, 1024, yy + 30), fill=BLUE, radius=5)
    text_center(p, 907, yy + 9, "Continuer", "PS", 8.6, "#FFFFFF")
    yy += 38
    text_center(p, 907, yy, "Powered by META", "PS", 5.6, "#8A93A3")

    line(p, (790, 480), (1024, 480), "#E7EAF0", 0.9)
    pg.t(790, 496, "Pourquoi le formulaire instantané ?", "PB", 9, "#16324F")
    args = ["Coordonnées pré-remplies depuis le profil META",
            "Aucune sortie d'application, moins d'abandon",
            "Lead transmis en temps réel à vos équipes"]
    yy = 518
    for a in args:
        draw_text(p, 790, yy, "•", "PR", 8, BLUE)
        for ln in wrap(a, "PR", 7.2, 214):
            pg.t(800, yy, ln, "PR", 7.2, "#2B2F36")
            yy += 11
        yy += 8
    pg.rect((790, 584, 1024, 646), fill="#F3F6FC", radius=6)
    pg.t(802, 594, "Bon à savoir", "PS", 7.2, BLUE)
    yy = 606
    for ln in wrap("Le formulaire peut aussi renvoyer vers votre landing page pour "
                   "les campagnes de notoriété.", "PR", 6.6, 206):
        pg.t(802, yy, ln, "PR", 6.6, "#4A5364")
        yy += 9
    line(p, (790, 668), (1024, 668), "#E7EAF0", 0.9)
    pg.t(790, 680, "Lead transmis en temps réel dans le CRM HelloLead.", "PR", 6.6, MUTED)

    fields = [
        ("Type d'établissement :", "Restauration rapide (2 points de vente)"),
        ("Statut de l'acheteur :", "Gérant de franchise (B2B)"),
        ("Type de caisse recherchée :", "Caisse tactile + borne de commande"),
        ("Fonction attendue :", "Click & collect et commande sur place"),
        ("Budget envisagé :", "8 000 € à 15 000 €"),
        ("Sous quel délai souhaitez-vous être équipé ?", "Moins de 6 mois"),
    ]
    company = [
        ("t", "Entreprise : SNACK & CO"),
        ("t", "Siret : 91357924600018"),
        ("t", "Activité : (Restauration rapide sous"),
        ("t", "franchise, 2 points de vente)"),
        ("mask", "Contact :", 86),
        ("t", "Adresse : 24 rue Nationale"),
        ("t", "Ville : Lille"),
        ("t", "Code postal : 59800"),
        ("mask", "Tél :", 78),
        ("mask", "Mail :", 126),
    ]
    right_panel(pg, fields, company)
    return pg


# ------------------------------------------------------------------- page 6
def page_call(doc):
    pg = Page(doc)
    p = pg.page
    left_column(
        pg, "CALL",
        "L'humain au service du lead",
        ["Data propriétaire de décideurs identifiés : gérants, responsables de salle, "
         "directeurs d'exploitation",
         "Segmentation sectorielle avancée par code NAF",
         "Opérateurs spécialisés CHR et commerce alimentaire",
         "Qualification : nombre de points de vente, matériel, logiciel, budget",
         "Maîtrise des enjeux et attentes métiers",
         "Validation des données avant livraison",
         "Prise de rendez-vous directement dans l'agenda de vos commerciaux"],
        subtitle_size=24,
        note=("Maquette illustrative : enseignes, chiffres et coordonnées fictifs. "
              "Questions et champs à valider avec le formulaire CRM n° 2015589."),
    )

    panel(pg.page, (483, 40, 1065, 762))
    pg.t(512, 66, "Précision du discours, richesse de l'échange", "PR", 24, BLUE)
    pg.t(512, 97, "Chaque appel est qualifié et saisi dans le CRM.", "PR", 10.5, MUTED)

    # --- fenêtre CRM
    card(pg.page, (512, 112, 1048, 492), radius=6)
    pg.rect((512, 112, 1048, 138), fill=NAVY, radius=6)
    pg.rect((512, 130, 1048, 138), fill=NAVY)
    pg.t(524, 118, "HelloLead", "PB", 9, "#FFFFFF")
    pg.t(760, 120, "Campagne : Caisses tactiles", "PR", 6, "#C9D8E8")
    for i in range(3):
        circle(p, (1034 - i * 9, 123), 2, fill="#7E9FBF", color=None)
    pg.rect((512, 138, 1048, 158), fill="#F1F3F7")
    menu = ["Menu", "Paramétrage", "Statistiques", "Référents Appels", "Modération"]
    mx = 520
    for m in menu:
        draw_text(p, mx, 144, m, "PR", 5.6, "#3F4753" if m != "Modération" else BLUE)
        mx += text_width(m, "PR", 5.6) + 18
    line(p, (512, 158), (1048, 158), "#DDE1E8", 0.8)

    # liste de gauche
    pg.rect((512, 158, 790, 492), fill="#F8F9FB")
    pg.t(520, 164, "SOURCITE", "PS", 5.4, "#98A1AE")
    pg.t(700, 164, "Acheteur", "PS", 5.4, "#98A1AE")
    rows = [("BRASSERIE DES ALPES", "Annecy · 06 12 34 56 78"),
            ("LE COMPTOIR DU MARCHÉ", "Lyon · 06 23 45 67 89"),
            ("SNACK & CO", "Lille · 06 34 56 78 90"),
            ("HÔTEL DU LAC", "Annecy · 04 50 12 34 56"),
            ("ÉPICERIE DU MARCHÉ", "Bordeaux · 06 45 67 89 01"),
            ("PIZZERIA BELUGA", "Nantes · 06 56 78 90 12"),
            ("CAFÉ DES ARTS", "Rennes · 06 67 89 01 23")]
    yy = 174
    for i, (name, sub) in enumerate(rows):
        if i == 3:
            pg.rect((512, yy - 4, 790, yy + 34), fill="#E4EEFB")
            pg.rect((512, yy - 4, 515, yy + 34), fill=BLUE)
        pg.t(520, yy, name, "PB", 6.4, "#1C2430")
        pg.t(520, yy + 12, sub, "PR", 5.6, "#6B7585")
        pg.tr(782, yy, "B2B", "PS", 5.2, "#8A93A3")
        line(p, (520, yy + 29), (782, yy + 29), "#E7EAF0", 0.6)
        yy += 41

    # formulaire de droite
    pg.rect((790, 158, 1048, 180), fill="#E8F0FB")
    pg.t(798, 164, "DEMANDE DE DEVIS : Caisses tactiles", "PS", 6.4, "#1B5AA6")
    pg.tr(1040, 165, "×", "PR", 8, "#6B7585")
    fx = 798
    yy = 190
    pg.t(fx, yy, "Avez-vous un projet de caisse tactile dans les 6 mois ?", "PS", 5.2,
         "#1C2430")
    yy += 12
    for i, lab in enumerate(["Oui", "Non"]):
        circle(p, (fx + 2 + i * 44, yy + 3), 2.4, color=(0.62, 0.67, 0.74),
                      width=0.7, fill=(1, 1, 1))
        draw_text(p, fx + 8 + i * 44, yy, lab, "PR", 5.4, "#3C4552")
    yy += 15
    pg.t(fx, yy, "Quel type de caisse recherchez-vous ?", "PS", 5.2, "#1C2430")
    yy += 12
    for lab in ["Caisse tactile + logiciel", "Borne de commande", "Caisse mobile"]:
        circle(p, (fx + 2, yy + 3), 2.4, color=(0.62, 0.67, 0.74), width=0.7,
                      fill=(1, 1, 1))
        draw_text(p, fx + 8, yy, lab, "PR", 5.4, "#3C4552")
        yy += 11
    yy += 4
    pg.t(fx, yy, "Vos enjeux pour ce projet :", "PS", 5.2, "#1C2430")
    yy += 12
    for i, lab in enumerate(["Gain de temps", "Gestion des stocks", "Commandes à table",
                             "Click & collect", "Fidélité", "Multi-sites"]):
        checkbox(pg, fx, yy + i * 11, size=5.6,
                 checked=(lab == "Gestion des stocks"), lsize=5.2, label=lab)
    yy += 70
    pg.t(fx, yy, "Nombre de points de vente :", "PS", 5.2, "#1C2430")
    yy += 12
    for i, lab in enumerate(["1", "2 à 5", "Plus de 5"]):
        circle(p, (fx + 2 + i * 44, yy + 3), 2.4, color=(0.62, 0.67, 0.74),
                      width=0.7, fill=(1, 1, 1))
        draw_text(p, fx + 8 + i * 44, yy, lab, "PR", 5.4, "#3C4552")
    yy += 16
    pg.t(fx, yy, "Budget prévisionnel :", "PS", 5.2, "#1C2430")
    yy += 12
    for i, lab in enumerate(["Moins de 5 000 €", "5 000 à 15 000 €", "Plus de 15 000 €"]):
        circle(p, (fx + 2, yy + 3), 2.4, color=(0.62, 0.67, 0.74),
                      width=0.7, fill=(1, 1, 1))
        draw_text(p, fx + 8, yy, lab, "PR", 5.4, "#3C4552")
        yy += 11

    # encart matching
    pg.rect((942, 190, 1040, 256), fill="#FFF6E8", color="#F2C98A", width=0.7,
            radius=4)
    pg.t(948, 196, "Résultats du matching", "PS", 5, "#A3611A")
    pg.t(948, 208, "CAISSES TACTILES (B2B)", "PB", 5.4, "#1B5AA6")
    for i, lab in enumerate(["Caisse tactile", "Logiciel de gestion", "Borne"]):
        pg.t(948, 220 + i * 10, "· " + lab, "PR", 4.8, "#3C4552")
    pg.rect((942, 266, 1040, 312), fill="#EAF2FB", radius=4)
    pg.t(948, 272, "Lead à forte valeur", "PS", 5, "#1B5AA6")
    for i, lab in enumerate(["Score de maturité : élevé", "Projet à moins de 6 mois"]):
        pg.t(948, 284 + i * 10, lab, "PR", 4.7, "#3C4552")

    # photo centre d'appels
    image(p, A / "callcenter.jpg", (512, 508, 1048, 726), radius=8, crop_ratio=536 / 218)
    pg.t(512, 736, "Équipe de modération et de qualification HelloLead", "PR", 6.4, SOFT)

    fields = [
        ("Catégorie CRM du besoin :", "Caisses tactiles / logiciel de caisse"),
        ("Type d'établissement :", "Hôtel-restaurant (3 établissements)"),
        ("Statut de l'acheteur :", "Directeur d'exploitation (B2B)"),
        ("Type de caisse recherchée :", "Caisse tactile + interface PMS"),
        ("Budget envisagé :", "10 000 € à 20 000 €"),
        ("Disponibilité pour un appel :", "Demain à 11h00"),
    ]
    company = [
        ("t", "Entreprise : HÔTEL DU LAC"),
        ("t", "Siret : 90579135700043"),
        ("t", "Activité : (Hôtellerie-restauration,"),
        ("t", "3 établissements)"),
        ("mask", "Contact :", 92),
        ("t", "Adresse : 5 avenue du Lac"),
        ("t", "Ville : Annecy"),
        ("t", "Code postal : 74000"),
        ("mask", "Tél :", 72),
        ("mask", "Mail :", 124),
    ]
    right_panel(pg, fields, company)
    return pg


# ------------------------------------------------------------------- page 7
def page_emailing(doc):
    pg = Page(doc)
    p = pg.page
    left_column(
        pg, "Emailing",
        "La prospection ciblée et personnalisée",
        ["Ciblage NAF (5 niveaux) ultra précis pour les éditeurs de caisses",
         "Personnalisation par métier : CHR, boulangerie, restauration rapide",
         "Templates et landing pages adaptés à la cible",
         "Campagnes marque blanche ou dédiées",
         "Déploiement rapide",
         "Mesure précise des taux d'ouverture et de clic",
         "La Data : des audiences issues de nos bases propriétaires"],
        note=("Maquette illustrative : enseignes, chiffres et coordonnées fictifs. "
              "Questions et champs à valider avec le formulaire CRM n° 2015589."),
    )

    panel(pg.page, (483, 40, 1065, 762))
    pg.t(512, 66, "Un message sur-mesure, une diffusion ciblée", "PR", 24, BLUE)
    pg.t(512, 97, "Deux exemples d'e-mails, deux métiers, un seul objectif : la démo.",
         "PR", 10.5, MUTED)

    # --- e-mail A
    card(pg.page, (512, 112, 760, 660), radius=8)
    pg.rect((512, 112, 760, 124), fill=BLUE)
    pg.t(526, 132, "CaissePro", "PB", 11, BLUE)
    pg.tr(746, 134, "NEWSLETTER · CHR", "PS", 5.4, "#98A1AE")
    line(p, (512, 144), (760, 144), "#E7EAF0", 0.9)
    pg.t(526, 154, "Objet : Équipez votre restaurant d'une caisse tactile", "PB", 8.4,
         "#1A1D24")
    pg.t(526, 168, "Caisse tactile & logiciel de gestion · mars 2026", "PR", 6, SOFT)
    image(p, A / "photo-restaurant.jpg", (512, 184, 760, 316), crop_ratio=248 / 132)
    yy = 330
    for ln in wrap("La caisse qui suit le rythme du service", "PB", 12, 220):
        pg.t(526, yy, ln, "PB", 12, "#16324F")
        yy += 15
    for ln in wrap("Commandes à table, addition, encaissement et pilotage : tout se "
                   "pilote depuis un seul écran tactile. Installation et reprise de "
                   "vos données incluses.", "PR", 6.8, 220):
        pg.t(526, yy + 2, ln, "PR", 6.8, "#4A5364")
        yy += 10
    pg.rect((526, yy + 10, 746, yy + 36), fill="#F4B41A", radius=4)
    text_center(p, 636, yy + 18, "Réserver une démo gratuite", "PS", 7.6, "#20242B")
    yy += 48
    line(p, (526, yy), (746, yy), "#E7EAF0", 0.8)
    yy += 10
    pg.t(526, yy, "Deux formats, un même parcours", "PS", 7.4, "#16324F")
    yy += 14
    for i, (ph, lab) in enumerate([("photo-boulangerie.jpg", "Boulangerie"),
                                   ("photo-epicerie.jpg", "Commerce")]):
        x0 = 526 + i * 112
        image(p, A / ph, (x0, yy, x0 + 104, yy + 62), radius=4, crop_ratio=104 / 62)
        pg.t(x0 + 2, yy + 68, lab, "PS", 6, "#5A6472")
    yy += 88
    for ln in wrap("Vous recevez cet e-mail car votre établissement correspond aux "
                   "critères de notre campagne. Se désabonner · Mentions légales.",
                   "PR", 5.4, 220):
        pg.t(526, yy, ln, "PR", 5.4, "#9AA3B0")
        yy += 8
    pg.tr(746, 638, "caissepro.fr", "PR", 5.4, "#9AA3B0")

    # --- e-mail B
    card(pg.page, (774, 112, 1040, 660), radius=8)
    image(p, A / "photo-patisserie.jpg", (774, 112, 1040, 238), corners=(1, 1, 0, 0),
          crop_ratio=266 / 126)
    pg.rect((790, 154, 904, 190), fill="#FFFFFF", radius=4)
    pg.t(798, 161, "CaissePro", "PB", 9, BLUE)
    pg.t(798, 175, "Boulangerie & pâtisserie", "PR", 5.4, "#6B7585")
    yy = 250
    pg.t(788, yy, "Boulangerie : une caisse qui gère aussi vos stocks", "PB", 10.5,
         "#16324F")
    for ln in wrap("Rendement, invendus, commandes de fêtes : la caisse tactile "
                   "CaissePro relie votre comptoir à votre production.", "PR", 6.6, 234):
        pg.t(788, yy + 34, ln, "PR", 6.6, "#4A5364")
        yy += 9
    yy += 4
    pg.rect((788, yy + 38, 1026, yy + 66), fill="#F3F6FC", radius=5)
    pg.t(798, yy + 44, "Testée par 120 boulangeries", "PS", 6.8, BLUE)
    pg.t(798, yy + 55, "Installation en 48 h · formation incluse", "PR", 5.8, "#4A5364")
    yy += 80
    for i, (t1, t2) in enumerate([("Mise en route", "Accompagnement"),
                                  ("Reprise des données", "Sans rupture"),
                                  ("SAV local", "7j/7")]):
        col = i % 2
        row = i // 2
        bx = 788 + col * 122
        by = yy + row * 44
        pg.rect((bx, by, bx + 114, by + 36), fill="#FAFBFE", color="#E7EAF0",
                width=0.7, radius=4)
        pg.t(bx + 6, by + 6, t1, "PS", 5.6, "#1A1D24")
        pg.t(bx + 6, by + 17, t2, "PR", 5.2, "#6B7585")
    yy += 92
    pg.rect((788, yy, 1026, yy + 30), fill=BLUE, radius=4)
    text_center(p, 907, yy + 8, "Demander mon comparatif", "PS", 7.6, "#FFFFFF")
    yy += 46
    line(p, (788, yy), (1026, yy), "#E7EAF0", 0.8)
    yy += 14
    pg.rect((788, yy, 1026, yy + 62), fill="#F3F6FC", radius=5)
    pg.t(798, yy + 10, "« Installation en 48 h, sans interrompre", "PS", 6.6, "#16324F")
    pg.t(798, yy + 21, "le service. »", "PS", 6.6, "#16324F")
    pg.t(798, yy + 36, "Gérante · Boulangerie des Halles, Lyon", "PR", 5.6, "#5A6472")
    yy += 76
    for ln in wrap("CaissePro — 12 rue de l'Artisanat, 44000 Nantes. E-mail envoyé à "
                   "votre adresse professionnelle. Se désabonner.", "PR", 5.4, 238):
        pg.t(788, yy, ln, "PR", 5.4, "#9AA3B0")
        yy += 8

    # séquence recommandée
    pg.t(512, 678, "Séquence recommandée en 3 temps", "PB", 9, "#16324F")
    steps = [("J+0", "Présentation de l'offre", "Visuel métier + CTA démo"),
             ("J+4", "Preuve sociale", "Cas client et chiffres clés"),
             ("J+9", "Dernière relance", "Invitation à un échange court")]
    for i, (j, t1, t2) in enumerate(steps):
        x0 = 512 + i * 180
        pg.rect((x0, 696, x0 + 168, 744), fill="#FFFFFF", radius=6)
        circle(p, (x0 + 16, 714), 9, fill="#E7EEFF", color=None)
        text_center(p, x0 + 16, 709.5, str(i + 1), "PB", 7, BLUE)
        pg.t(x0 + 31, 704, j, "PS", 6.2, BLUE)
        pg.t(x0 + 31, 713, t1, "PS", 6.8, "#1A1D24")
        pg.t(x0 + 31, 726, t2, "PR", 6, MUTED)

    fields = [
        ("Établissement déjà équipé en caisse tactile ?", "Oui, matériel vieillissant"),
        ("Type d'établissement :", "Commerce alimentaire (épicerie fine)"),
        ("Statut de l'acheteur :", "Gérant (B2B), propriétaire"),
        ("Nombre de caisses à équiper :", "2"),
        ("Fonction attendue :", "Gestion de stock et pesée"),
        ("Budget envisagé :", "3 000 € à 6 000 €"),
        ("Échéance du projet :", "3 à 6 mois"),
    ]
    company = [
        ("t", "Entreprise : ÉPICERIE DU MARCHÉ"),
        ("t", "Siret : 90246813500027"),
        ("t", "Activité : (Commerce alimentaire de"),
        ("t", "proximité)"),
        ("mask", "Contact :", 90),
        ("t", "Adresse : 21 rue Nationale"),
        ("t", "Ville : Bordeaux"),
        ("t", "Code postal : 33000"),
        ("mask", "Tél :", 76),
        ("mask", "Mail :", 130),
    ]
    right_panel(pg, fields, company)
    return pg


# ------------------------------------------------------------------- montage
def main():
    doc = pymupdf.open()
    page_cover(doc)
    src = pymupdf.open(SOLAR)
    doc.insert_pdf(src, from_page=1, to_page=1)   # méthode & leviers (page 2)
    page_sms(doc)
    page_sea(doc)
    page_meta(doc)
    page_call(doc)
    page_emailing(doc)
    doc.insert_pdf(src, from_page=7, to_page=8)   # modération & contact

    for page in doc:
        for lnk in list(page.get_links()):
            page.delete_link(lnk)

    doc.set_metadata({
        "title": "HelloLead — Caisses enregistreuses tactiles",
        "author": "HelloLead",
        "subject": "Génération de leads qualifiés pour les éditeurs de caisses tactiles",
        "keywords": "leads, caisses tactiles, CHR, boulangerie, restauration",
    })
    doc.save(OUT, garbage=4, deflate=True)
    print("PDF écrit :", OUT, doc.page_count, "pages")


if __name__ == "__main__":
    main()
