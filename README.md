➜  entretien-14-10 GEMINI_MODEL="gemini-3.8-flash" python3 Agent_exemple.py
Mini agent entreprises (Ctrl+C pour quitter)

Question > Où est le siège de Virbac et quand a-t-elle été créée ?
  [outil] rechercher_entreprise({'recherche': 'Virbac'})

D'après les données officielles de l'INSEE :

* **Siège social :** LID 2065 M 1ère Avenue, 06510 Carros (Alpes-Maritimes).
* **Date de création :** 1ᵉʳ avril 1984 *(pour l'entité juridique VIRBAC - SIREN 417 350 311)*.

Question > Compare Virbac et Boiron
  [outil] rechercher_entreprise({'recherche': 'Virbac'})
  [outil] rechercher_entreprise({'recherche': 'Boiron'})

Voici une comparaison entre les deux laboratoires pharmaceutiques français, d'après les données officielles de l'INSEE :

| Caractéristique | **VIRBAC** | **BOIRON** |
| :--- | :--- | :--- |
| **Secteur / Activité (NAF)** | Fabrication de préparations pharmaceutiques (`21.20Z`) – *Santé animale* | Fabrication de préparations pharmaceutiques (`21.20Z`) – *Homéopathie /Santé humaine* |
| **Numéro SIREN** | 417 350 311 | 967 504 697 |
| **Date de création** | 1er avril 1984 | 1er janvier 1967 |
| **Siège social** | Carros (Alpes-Maritimes - 06) | Messimy (Rhône - 69) |
| **Catégorie d'entreprise** | ETI (Entreprise de taille intermédiaire) | ETI (Entreprise de taille intermédiaire) |
| **Tranche d'effectifs (siège/entité)** | 1 000 à 1 999 salariés (code 42) | 1 000 à 1 999 salariés (code 42) |
| **Établissements actifs** | 4 | 14 |
| **Statut administratif** | Active | Active |

**Points communs :** Toutes deux sont des ETI françaises du secteur de l'industrie pharmaceutique (code NAF 21.20Z) employant plus de 1 000 salariés en France.

**Différences :** Virbac est positionné sur la santé vétérinaire et basé dans le sud-est (Carros), tandis que Boiron est spécialisé dans les produits homéopathiques et la santé humaine, avec un siège en région lyonnaise (Messimy) et un réseau plus étendu d'établissements en France.

Question > À qui correspond le SIREN 417350311 ?
  [outil] rechercher_entreprise({'recherche': '417350311'})

Le numéro SIREN **417350311** correspond à l'entreprise **VIRBAC**.

* **Dénomination :** VIRBAC
* **Activité principale (NAF) :** 21.20Z (Fabrication de préparations pharmaceutiques)
* **Siège social :** LID 2065 M 1ère Avenue, 06510 Carros
* **Statut :** Active
* **Catégorie d'entreprise :** ETI

Question > Quelle est la capitale de l'Italie ?

La capitale de l'Italie est Rome.








(Fallback to other Gemini models on quota/overload errors) example :






Mini agent entreprises (Ctrl+C pour quitter)

Question > Bonjour
  [gemini] gemini-3.8-flash indisponible (429), modele suivant...

Bonjour ! Comment puis-je vous aider ? Si vous recherchez des informations sur une entreprise française, indiquez-moi son nom, son numéro SIREN ou son SIRET.