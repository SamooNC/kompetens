# Skill : Pipeline Open Data NC

> **Priorité** : 🟡 IMPORTANTE — Alimente la démo avec des données réelles calédoniennes.

## Contexte

Le POC doit ingérer au moins deux sources de données calédoniennes pour produire une première typologie des métiers en tension. Cela donne de la crédibilité au POC face aux décideurs (Kevin).

## Sources identifiées

### 1. Open Data du Gouvernement NC (API)
- **URL** : https://data.gouv.nc
- **Format** : API REST (JSON)
- **Données utiles** : Démographie, entreprises (RIDET), secteurs d'activité
- **Authentification** : Clé API publique ou libre accès

### 2. ISEE (Institut de la Statistique et des Études Économiques)
- **Format** : CSV téléchargeables
- **Données utiles** : Emploi par secteur, taux de chômage, population active par commune
- **Fréquence** : Annuelle / trimestrielle

### 3. DTEFP (Direction du Travail, de l'Emploi et de la Formation Professionnelle)
- **Format** : CSV
- **Données utiles** : Offres d'emploi enregistrées, secteurs en tension, formations
- **Fréquence** : Variable

## Architecture pipeline

```
Sources brutes (API / CSV)
    │
    ▼
┌─────────────────────┐
│  Ingestion           │  scripts/import-opendata.py
│  (requests + pandas) │  Téléchargement + nettoyage
└──────┬──────────────┘
       │ DataFrames nettoyés
       ▼
┌─────────────────────┐
│  Normalisation       │  Mapping vers référentiel ROME v4
│                     │  Géocodage (commune → province)
│                     │  Harmonisation codes secteurs
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  PostgreSQL          │  Tables :
│                     │  - secteurs_tension
│                     │  - offres_par_zone
│                     │  - stats_emploi
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  API FastAPI         │  Endpoints :
│                     │  GET /api/opendata/tensions
│                     │  GET /api/opendata/stats/{zone}
└─────────────────────┘
```

## Schéma de données

```python
class SecteurTension(BaseModel):
    code_rome: str              # "F1302"
    libelle_rome: str           # "Conduite d'engins"
    zone: str                   # "Province Sud", "Province Nord", "Îles"
    nb_offres: int              # Nombre d'offres sur la période
    nb_demandeurs: int          # Nombre de demandeurs inscrits
    ratio_tension: float        # offres/demandeurs (>1 = tension)
    source: str                 # "DTEFP", "ISEE"
    periode: str                # "2025-T3"

class StatEmploi(BaseModel):
    zone: str
    population_active: int
    taux_chomage: float
    secteurs_principaux: list[str]
    source: str
    annee: int
```

## Règles de conception

- **Idempotent** : Le script d'import peut être relancé sans dupliquer les données (UPSERT)
- **Traçabilité** : Chaque donnée importée conserve sa source et sa date d'import
- **Tolérance** : Les CSV calédoniens sont souvent mal formatés (encodage, séparateurs, colonnes manquantes). Le script doit gérer gracieusement les erreurs avec des logs clairs.
- **Pas de temps réel** : Import batch, pas de connexion live aux sources
- **Données simulées en fallback** : Si une source est indisponible, on utilise des données simulées cohérentes pour la démo

## Tests critiques

1. **Test import API** : Le script ingère les données de data.gouv.nc sans erreur
2. **Test import CSV** : Les fichiers ISEE/DTEFP sont parsés malgré les imperfections de format
3. **Test mapping ROME** : Au moins 80% des secteurs importés sont mappés à un code ROME v4
4. **Test endpoint** : `/api/opendata/tensions` retourne les secteurs en tension par zone
