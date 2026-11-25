# Plaquette caisses enregistreuses tactiles — création

Livrable : `Plaquette HelloLead - Caisses enregistreuses tactiles.pdf` (9 pages, 1440×810).
Déclinaison de la plaquette solaire corrigée : même charte (bleu HelloLead #0A5BFF, Poppins, fonds pâles #F4F5FB, mêmes gabarits de panneaux) et même structure : couverture, méthode et cinq leviers, un levier par page avec maquettes, modération & enrichissement, contact.

- Page 1 (couverture) : logo HelloLead repris du PDF solaire (rendu 600 dpi), titre « Caisses enregistreuses tactiles », cibles CHR, boulangeries, restauration rapide et commerces alimentaires ; visuel de caisse tactile en boulangerie (généré, sans texte lisible).
- Page 2 : « Génération de leads » conservée du modèle (méthode, 13 ans d'expérience, cinq leviers conformes à la règle permanente ci-dessous).
- Pages 3 à 7 : un levier par page — SMS/RCS, SEA - Google Ads, META Ads, CALL, Emailing. Chaque page reprend le gabarit du modèle : panneau de gauche (accroche + bénéfices), panneau central de maquettes, panneau de droite « Modération & Enrichissement » avec un lead fictif (établissement, statut, type de caisse, fonction attendue, budget, échéance, coordonnées masquées).
- Maquettes dessinées en vectoriel : cartes SMS/RCS et landing page avec formulaire (p. 3), résultats Google et formulaire qualifiant (p. 4), post sponsorisé Facebook, carrousel par métier et formulaire instantané (p. 5), écran CRM HelloLead et photo de centre d'appels (p. 6), deux e-mails type et séquence de relance en 3 temps (p. 7).
- Visuels par métier : boulangerie (couverture, SMS), restaurant (SEA, e-mail), restauration rapide (META), épicerie fine et pâtisserie (Emailing). Les sept photos sont générées pour la plaquette et stockées dans `work/` ; la photo du centre d'appels est reprise du PDF solaire.
- Chaque page de levier porte la mention « Maquette illustrative : enseignes, chiffres et coordonnées fictifs. Questions et champs à valider avec le formulaire CRM n° 2015589. »
- Pages 8 (modération & enrichissement) et 9 (contact) conservées du modèle ; aucun contenu solaire résiduel (contrôle automatisé sur « solaire, photovolta, toiture, kWh, kWc, surplus, autoconsommation, panneaux »), aucun lien hypertexte conservé, textes dans les limites des pages et du panneau de droite.
- Métadonnées PDF : titre « HelloLead — Caisses enregistreuses tactiles », auteur HelloLead.

## Production
- `work/creer_caisses.py` : construction des pages 1 et 3 à 7, montage des pages 2, 8 et 9 reprises du PDF solaire, contrôles et écriture du PDF.
- `work/plaquette_lib.py` : moteur de mise en page (polices, panneaux arrondis, textes, pastilles, images à coins arrondis, flèches).
- Polices Poppins (Regular, Medium, SemiBold, Bold, ExtraBold) téléchargées depuis `google/fonts` et stockées dans `work/`.
- Dépendances : PyMuPDF et Pillow dans `.venv`.
- Commande depuis la racine : `.venv/bin/python work/creer_caisses.py`.

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
