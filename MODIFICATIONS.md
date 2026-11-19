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
