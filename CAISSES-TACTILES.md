# Plaquette HelloLead — Caisses enregistreuses tactiles

## Livrable
`Plaquette HelloLead - Caisses enregistreuses tactiles.pdf` — 9 pages, format paysage 1440 × 810 pt, texte sélectionnable.

Nouvelle déclinaison de la plaquette HelloLead corrigée déjà présente dans le dépôt. Les PDF existants restent inchangés.

## Contenu
1. Couverture dédiée aux caisses enregistreuses tactiles.
2. Présentation HelloLead et leviers d’acquisition, conservés du modèle corrigé.
3. SMS / RCS : exemple boulangerie et parcours mobile.
4. SEA : exemple restaurant et proposition de formulaire.
5. META Ads : exemple restauration rapide.
6. Appels : trame de qualification et exemple commerce alimentaire.
7. Emailing : maquette et exemple commerce multi-sites.
8. Modération et enrichissement : méthode du modèle existant.
9. Contact HelloLead : page du modèle existant.

## Cadrage et validations
- La plaquette s’adresse aux fournisseurs de solutions d’encaissement, pour leur proposer l’acquisition de prospects professionnels. Les acheteurs finaux représentés sont les CHR, boulangers, restaurateurs rapides et commerçants alimentaires/de proximité.
- JDC SA, Cashmag, Lightspeed, L’Addition, SumUp, Clyo Systems, Zelty, Innovorder et Tactill sont les entreprises destinataires potentielles indiquées dans le brief, pas des références clients. Leurs logos ne figurent pas dans la plaquette et aucun partenariat n’est affirmé.
- Le formulaire CRM indiqué par Pierre n’a pas été consulté. Ses questions exactes et ses options restent à fournir pour aligner les maquettes. Le lien d’administration ne figure pas dans le document commercial.
- Les questions de qualification sont proposées : activité, première installation/remplacement, équipement existant, sites/terminaux, fonctionnalités, budget/financement, délai, décideur et coordonnées.
- Les cinq exemples de leads sont fictifs et identifiés comme tels. Budgets, délais et périmètres illustrent le rendu ; ce ne sont ni des tarifs du marché ni des résultats réels. Aucune identité personnelle ni aucun faux SIRET n’est ajouté.
- Le bloc permanent des cinq leviers de la page 2 est conservé à l’identique, y compris la mention OpenAI Ads (ChatGPT). Il provient du modèle fourni ; la disponibilité commerciale des plateformes n’a pas été vérifiée dans cette déclinaison.
- Les chiffres HelloLead (13 ans d’expérience, 150 clients actifs), les affirmations de méthode et les coordonnées sont repris du modèle existant, sans nouvelle vérification.
- Les maquettes restent illustratives : mentions, émetteur, mécanisme de désinscription et traitement des données sont à adapter avant toute diffusion de campagne.
- Le visuel de caisse est généré par IA, sans représenter un produit ou une marque identifiés. La photo d’équipe générée et le schéma de modération de la page 8 sont repris du modèle.

## Production et contrôle
```sh
python -m venv .venv
.venv/bin/pip install -r work/requirements-caisses.txt
.venv/bin/python work/creer_caisses.py
```

Le script utilise le PDF corrigé, les polices Poppins existantes et `work/caisse-tactile.jpg`. Il génère le PDF et des rendus de contrôle ignorés par Git.

Contrôles : 9 pages, dimensions, absence de texte solaire résiduel, absence de texte hors page et contrôle visuel des nouvelles pages. Les pages génériques 2, 8 et 9 sont reprises du modèle, avec un repère de thématique ajouté sur les pages 2 et 8.
