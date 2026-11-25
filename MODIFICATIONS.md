# Plaquette caisses enregistreuses tactiles — création

Livrable : `Plaquette HelloLead - Caisses enregistreuses tactiles.pdf` (9 pages, 1440×810).
Déclinaison de la plaquette solaire corrigée, même charte (bleu HelloLead, Poppins, fonds pale), même structure : couverture, méthode et cinq leviers, modération & enrichissement, contact.

- Page 1 (couverture) : logo d'origine extrait du PDF solaire, titre « Caisses enregistreuses tactiles », cibles CHR, boulangeries, restauration rapide, commerces alimentaires ; visuel photoréaliste de caisse tactile en boulangerie (généré, sans texte lisible).
- Pages 3 à 7 : maquettes illustratives par levier (SMS/RCS, SEA, META Ads, CALL, Emailing) avec un exemple de lead fictif côté « Modération & enrichissement » (activité, projet, périmètre, besoins, budget, échéance) à confronter au formulaire CRM n° 2015589.
- Chaque maquette porte une mention « illustrative » (annonce, recherche, sponsorisé, objet) et le pied de page rappelle que les questions sont à valider avec le formulaire CRM.
- Visuels par métier : boulangerie (couverture, SMS), restaurant traditionnel (SEA), restauration rapide (META), épicerie/commerce (Emailing) ; les quatre photos sont générées et stockées dans `work/`.
- Pages 2, 8 et 9 conservées du modèle avec bandeaux et folios actualisés ; aucun contenu solaire résiduel (contrôle automatisé sur « solaire, photovolta, toiture, kWh, kWc, surplus »), aucun lien hypertexte du PDF source conservé.
- Métadonnées PDF : titre « HelloLead — Caisses enregistreuses tactiles ».
- Production : `work/creer_caisses.py` (PyMuPDF + Pillow, `python work/creer_caisses.py` depuis la racine, dépendances dans `work/requirements-caisses.txt`). Contrôles automatiques : 9 pages, texte dans les limites des pages, aucune référence solaire.

# Plaquette solaire — corrections

Livrable : `Plaquette HelloLead - Panneaux solaires - Corrigee.pdf` (9 pages).
Les deux PDF d'origine sont conservés sans modification.
Corrections effectuées (numéros physiques du PDF, couverture comprise) :
- Page 2 : remplacement des leviers d'acquisition par les cinq entrées demandées.
- Pages 3 et 4 : suppression de la ligne « avec revente du surplus » dans le type de projet.
- Page 4 : remplacement de la question et des cinq choix du formulaire par la question sur l'objectif principal et les trois cases demandées.
- Page 7 : reconstruction du bandeau gris et des deux boutons, avec dimensions identiques et libellés centrés.
- Page 8 : remplacement de l'illustration principale par un nouveau visuel généré au rendu photographique (ce n'est pas une photographie d'une équipe réelle).

## Règle permanente pour les prochaines déclinaisons
Le bloc « Choix de leviers adaptés au client » doit reprendre :
1. Télémarketing / Data propriétaire : Calls équipes internes et fichiers propriétaires
2. Marketing direct : SMS, RCS et emailing ciblés sur BDD propriétaires
3. Social Ads : Facebook, Instagram, LinkedIn…
4. SEA : Google Ads, Microsoft Ads…
5. Publicité conversationnelle IA : OpenAI Ads (ChatGPT)…

Le point-virgule après SEA dans la consigne est harmonisé en deux-points.

## Production
`work/modifier.py` contient le script de modification ; les ressources nécessaires sont dans `work/`.
Dépendances Python : PyMuPDF et Pillow.
Commande depuis la racine : `python work/modifier.py`.
Les cinq pages modifiées ont été rendues et contrôlées visuellement.

## Ajustement typographique
Le bloc central de la page 2 utilise désormais Poppins Regular 16 pt, comme les blocs voisins. Son encadré est agrandi vers le bas pour conserver les cinq leviers sans réduire la taille du texte. Le titre reste en Poppins Bold 25 pt.

## Alignement des encadrés
Les trois encadrés de la page 2 sont alignés en bas à 790 pt. Les encadrés latéraux sont prolongés vers le bas en conservant leurs coins arrondis et sans déplacer ni redimensionner les textes. Vérification visuelle effectuée sur le rendu de la page.
