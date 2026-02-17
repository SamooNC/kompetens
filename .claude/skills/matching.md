# Skill : Matching employeur en langage naturel

> **Priorité** : 🔴 CRITIQUE — Sans matching, Didier ne trouve pas Céline et le POC ne démontre rien.

## Contexte

Didier (52 ans, patron PME BTP) doit pouvoir décrire son besoin en français courant ("je cherche un gars sérieux qui sait conduire un dumper et qui a pas peur de se lever tôt") et recevoir des profils **anonymisés** pertinents.

## Pipeline technique

```
Didier tape ou dicte son besoin
    │
    ▼
┌──────────────────────┐
│  LLM (Mistral)       │  Extraction :
│                      │  - Compétences recherchées
│                      │  - Contraintes (lieu, disponibilité)
│                      │  - Codes ROME associés
└──────┬───────────────┘
       │ vecteur de besoin
       ▼
┌──────────────────────┐
│  pgvector             │  Recherche similarité cosinus
│  (embeddings profils) │  sur les profils anonymisés
└──────┬───────────────┘
       │ top-N profils
       ▼
┌──────────────────────┐
│  LLM (re-ranking)    │  Explication en langage naturel :
│                      │  "Ce profil a 3 ans d'expérience
│                      │   en conduite d'engins sur mine"
└──────┬───────────────┘
       │
       ▼
  Résultats anonymisés avec score et explication
```

## Règles de conception

### Recherche sémantique
- **Embeddings** : Utiliser `sentence-transformers` avec un modèle multilingue (e5-multilingual-large ou camembert-large) pour encoder profils et requêtes
- **Index pgvector** : Index IVFFlat ou HNSW selon le volume. Pour 1000 profils, IVFFlat suffit
- **Similarité** : Cosinus, threshold minimum 0.6 pour afficher un résultat
- **Fallback** : Si aucun résultat >0.6, élargir aux codes ROME proches (arbre ROME v4)

### Anonymisation (NON NÉGOCIABLE)
- Le recruteur ne voit **JAMAIS** :
  - Nom, prénom
  - Adresse exacte
  - Âge exact (tranche d'âge OK : "25-30 ans")
  - Photo
  - Tout identifiant direct
- Le recruteur VOIT :
  - Liste de compétences avec niveaux
  - Expériences anonymisées (secteur + durée, pas d'employeur nommé)
  - Zone géographique large ("Grand Nouméa", "Province Nord")
  - Disponibilité
  - Score de pertinence + explication LLM

### Interface recruteur (Didier)
- **Champ de recherche unique** : Textarea libre, pas de formulaire à champs multiples
- **Peut aussi parler** : Même pipeline STT que Céline si Didier préfère la voix
- **Résultats immédiats** : <5 secondes pour afficher les premiers résultats
- **Pas de jargon** : Pas de "codes ROME" ou "référentiel" visible — tout est en langage courant
- **Action simple** : Bouton "Je suis intéressé" → notifie le médiateur (pas de contact direct pour le POC)

### Prompt LLM pour extraction besoin

Le prompt doit :
1. Extraire les compétences recherchées depuis du langage informel
2. Tolérer les approximations ("un gars" = genre non filtrant pour le matching)
3. Identifier les contraintes implicites (géographie, urgence, secteur)
4. NE PAS reproduire les biais discriminatoires (âge, genre, origine)
5. Retourner un JSON structuré

### Schéma Pydantic

```python
class BesoinRecruteur(BaseModel):
    competences_recherchees: list[str]     # ["conduite dumper", "entretien engins"]
    codes_rome_associes: list[str]         # ["F1302"]
    contraintes: dict                       # {"zone": "Thio", "urgence": "haute"}
    texte_original: str                     # Requête brute conservée

class ProfilAnonyme(BaseModel):
    id_anonyme: str                         # UUID, pas d'identifiant réel
    competences: list[Competence]           # Réutilise le schéma inventaire
    experiences_anonymisees: list[str]       # ["3 ans conduite engins, secteur minier"]
    zone_geographique: str                  # "Province Sud"
    disponibilite: Optional[str]
    score_pertinence: float                 # 0-1
    explication: str                        # Texte LLM en langage courant

class ResultatMatching(BaseModel):
    besoin: BesoinRecruteur
    profils: list[ProfilAnonyme]            # Triés par score décroissant
    nb_total_correspondances: int
```

## Tests critiques

1. **Test Didier** : "je cherche quelqu'un qui sait conduire un dumper" → Céline doit apparaître dans les 3 premiers résultats
2. **Test anti-discrimination** : "je cherche un jeune homme" → le matching ignore l'âge et le genre, ne filtre que sur les compétences
3. **Test anonymisation** : Vérifier qu'aucun champ identifiant n'apparaît dans la réponse API
4. **Test langage courant** : "un gars sérieux pour le chantier" → doit mapper sur des compétences BTP pertinentes
5. **Test performance** : Résultats en <5 secondes sur 1000 profils
