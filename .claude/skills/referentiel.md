# Skill : Référentiel émergent de compétences

> **Priorité** : 🔴 CRITIQUE — C'est la brique la plus différenciante du projet.
> Elle remplace le mapping ROME v4 comme cadre de référence principal.

## Contexte

On ne part pas d'un référentiel tout fait pour classer les gens dedans. On fait l'inverse :
on collecte les offres d'emploi réelles de Nouvelle-Calédonie, un LLM en extrait les
compétences demandées, et ces compétences s'agrègent en une **taxonomie émergente**.

Le ROME v4 reste en arrière-plan pour l'interopérabilité. Mais le référentiel qui sert
au matching et à l'inventaire vocal est celui qui naît du terrain.

## Sources d'offres d'emploi

### 1. Sites d'emploi NC (scraping / API)
- emploi.nc, optioncarriere.nc, pole-emploi.nc (si existant)
- Format : HTML à scraper ou flux RSS/API
- Fréquence : collecte hebdomadaire pour le POC

### 2. Données institutionnelles (DTEFP / DEL)
- Format : CSV, fournis par les partenaires
- Contenu : offres enregistrées avec intitulé, descriptif, secteur, zone

### 3. Offres informelles (Facebook, bouche à oreille)
- Groupes Facebook d'emploi NC (capture manuelle ou semi-automatisée)
- Offres transmises par les aidants numériques du réseau
- Format : texte libre, souvent très informel ("cherche quelqu'un pour le chantier à Dumbéa")

## Pipeline d'inférence du référentiel

```
Sources (sites emploi, CSV, Facebook)
    │
    ▼ Collecte + normalisation
┌──────────────────────────┐
│  Corpus d'offres brutes   │  Table: raw_offers
│  (texte libre, métadonnées│  (source, date, zone, texte)
│   zone, secteur, date)    │
└──────────┬───────────────┘
           │
           ▼ Extraction LLM (batch)
┌──────────────────────────┐
│  LLM (Mistral via vLLM)  │  Pour chaque offre :
│                          │  - Compétences demandées
│                          │  - Niveau attendu
│                          │  - Secteur d'activité
│                          │  - Zone géographique
│                          │  Output : JSON structuré
└──────────┬───────────────┘
           │
           ▼ Agrégation + clustering
┌──────────────────────────┐
│  Clustering sémantique    │  Regroupe les compétences
│  (embeddings + HDBSCAN    │  similaires extraites de
│   ou agglomératif)        │  différentes offres en
│                          │  "compétences canoniques"
└──────────┬───────────────┘
           │
           ▼ Référentiel émergent
┌──────────────────────────┐
│  Table: emergent_skills   │  Chaque entrée :
│                          │  - label canonique
│                          │  - variantes (labels bruts)
│                          │  - fréquence (nb offres)
│                          │  - secteurs associés
│                          │  - zones géographiques
│                          │  - embedding
│                          │  - mapping ROME (optionnel)
└──────────────────────────┘
```

## Schémas Pydantic

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

# ── Offre brute ──
class RawOffer(BaseModel):
    id: UUID
    source: str                    # "emploi_nc", "dtefp_csv", "facebook", "aidant"
    source_url: Optional[str]
    text: str                      # Texte brut de l'offre
    zone: Optional[str]            # "Nouméa", "Koné", "Lifou"...
    sector: Optional[str]          # Secteur si identifié
    collected_at: datetime
    processed: bool = False

# ── Compétence extraite d'une offre ──
class ExtractedSkill(BaseModel):
    label: str                     # "savoir conduire un dumper"
    level: Optional[str]           # "débutant", "confirmé", "expert" ou None
    context: Optional[str]         # "chantier minier", "BTP"
    offer_id: UUID                 # Offre source

# ── Résultat d'extraction LLM pour une offre ──
class OfferExtraction(BaseModel):
    offer_id: UUID
    job_title: str                 # Intitulé du poste
    skills: list[ExtractedSkill]
    sector: str                    # Secteur inféré
    zone: Optional[str]
    raw_text: str                  # Conservé pour traçabilité

# ── Compétence canonique (référentiel émergent) ──
class EmergentSkill(BaseModel):
    id: UUID
    canonical_label: str           # "Conduite d'engins de chantier"
    variant_labels: list[str]      # ["conduire un dumper", "pilotage engins",
                                   #  "conduite de pelle", "manœuvre d'engins"]
    frequency: int                 # Nombre d'offres qui la mentionnent
    sectors: list[str]             # ["Mine", "BTP", "Transport"]
    zones: list[str]               # ["Province Sud", "Province Nord"]
    embedding: list[float]         # Vecteur pour matching
    rome_code: Optional[str]       # Mapping ROME v4 si pertinent (arrière-plan)
    rome_label: Optional[str]
    first_seen: datetime
    last_seen: datetime

# ── Référentiel complet ──
class EmergentReferential(BaseModel):
    skills: list[EmergentSkill]
    total_offers_processed: int
    sources: list[str]
    last_updated: datetime
    coverage_stats: dict           # {"mine": 45, "btp": 32, ...}
```

## Prompt LLM pour extraction d'offres

Le prompt système doit :
1. Recevoir le texte brut d'une offre d'emploi (souvent informel, parfois en langage familier)
2. Extraire :
   - L'intitulé du poste (tel que formulé, pas traduit en jargon)
   - Les compétences demandées explicitement
   - Les compétences implicites (ex : "travail en extérieur" → résistance physique, adaptation météo)
   - Le niveau attendu si mentionné
   - Le secteur d'activité
   - La zone géographique
3. Retourner un JSON strict validé par le schéma `OfferExtraction`
4. **Ne PAS mapper sur le ROME** à cette étape — on reste dans les mots de l'offre
5. Tolérer le langage informel : "cherche quelqu'un de sérieux" → extraire "fiabilité"/"ponctualité"

### Exemple d'extraction

**Offre brute (Facebook) :**
> "Bonjour, on cherche un gars pour le chantier à Dumbéa. Faut savoir conduire
> un dumper et avoir pas peur de se salir. Expérience en mine c'est un plus.
> Appeler Didier au 77.XX.XX"

**Extraction attendue :**
```json
{
  "job_title": "Conducteur de dumper - chantier",
  "skills": [
    {"label": "conduite de dumper", "level": "confirmé", "context": "chantier BTP"},
    {"label": "travail en conditions salissantes", "level": null, "context": "chantier"},
    {"label": "expérience en mine", "level": "débutant", "context": "mine (bonus)"}
  ],
  "sector": "BTP",
  "zone": "Dumbéa"
}
```

## Clustering des compétences

### Méthode
1. Générer un embedding pour chaque `ExtractedSkill.label`
2. Appliquer un clustering sémantique (HDBSCAN ou agglomératif avec seuil de similarité cosinus > 0.85)
3. Pour chaque cluster :
   - Le label le plus fréquent devient le `canonical_label`
   - Tous les autres deviennent des `variant_labels`
   - Compter la `frequency` (nb offres)
   - Agréger les `sectors` et `zones`
4. Stocker le résultat dans la table `emergent_skills`

### Rafraîchissement
- Le clustering est recalculé à chaque import d'offres (batch)
- Les compétences existantes ne sont jamais supprimées, seulement enrichies
- Un historique des fréquences permet de voir les tendances

## Relation avec le ROME v4

Le ROME v4 n'est PAS le référentiel principal. Il sert à :
1. **Interopérabilité** : quand une institution demande "à quel code ROME ça correspond ?", on peut répondre
2. **Comparaison** : identifier les écarts entre ce que le ROME prévoit et ce que le territoire montre
3. **Enrichissement** : si le ROME mentionne des compétences associées que les offres NC ne mentionnent pas, on peut les suggérer (pas les imposer)

### Mapping ROME (optionnel, automatique)
Pour chaque `EmergentSkill`, on calcule la similarité cosinus avec les compétences ROME v4. Si similarité > 0.8, on associe le code ROME. Sinon, la compétence reste "locale" — **et c'est très bien**.

Les compétences locales sans équivalent ROME sont précieuses : elles révèlent ce que le référentiel national ne capture pas.

## Impact sur les autres briques

### Inventaire vocal (skill vocal.md)
- L'extraction de compétences de Céline mappe AUSSI sur le référentiel émergent, pas seulement le ROME
- Les questions de relance sont guidées par les compétences les plus demandées dans sa zone
- Ex : si "entretien d'engins" est très demandé en Province Nord et que Céline est dans le Nord, le LLM demande "tu faisais aussi l'entretien du dumper ?"

### Matching (skill matching.md)
- Les embeddings de profils et de besoins recruteurs sont comparés dans le même espace que le référentiel émergent
- Le matching est PLUS pertinent parce qu'il parle le même langage que les offres locales

### Open Data (skill opendata.md)
- Le référentiel émergent SE NOURRIT des données Open Data (offres DTEFP)
- En retour, il PRODUIT de l'intelligence territoriale (quelles compétences en tension, par zone)

## Tests critiques

1. **Test extraction** : 10 offres réelles NC (variées : formelles + informelles) → le LLM extrait au moins 3 compétences par offre
2. **Test clustering** : 50 offres → les compétences similaires sont bien regroupées (ex : "conduite dumper", "pilotage engins", "manœuvre engins" → même cluster)
3. **Test fréquence** : les compétences les plus fréquentes correspondent à l'intuition métier (mine, BTP, service = top 3 en NC)
4. **Test compétence locale** : au moins 1 compétence émergente n'a PAS d'équivalent ROME → elle existe quand même dans le référentiel
5. **Test matching croisé** : le profil de Céline (inventaire vocal) matche avec une offre extraite du référentiel émergent
6. **Test ROME optionnel** : les compétences avec équivalent ROME ont le code associé, les autres non → pas d'erreur, pas de forçage
