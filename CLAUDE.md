# CLAUDE.md — Kompetens POC

> **Ce fichier est la constitution du projet. Claude Code doit le lire avant toute action.**
> **Lire d'abord le VISION.md** pour comprendre le sens du projet.

## Identité du projet

**Nom** : Kompetens (nom de travail)
**Nature** : Démonstrateur technologique (POC) — PAS un produit fini
**Échéance** : Mai 2026 (livraison démo)
**Porteur** : Commission Data & IA du cluster OPEN NC (Nouvelle-Calédonie)
**Licence** : PolyForm Noncommercial 1.0.0

**Vision** : Rendre visible ce qui existe déjà — les savoir-faire des gens, dans leurs propres mots — et leur donner le pouvoir de choisir ce qu'ils en font. C'est un démonstrateur technologique souverain, open source et reproductible, construit depuis la Nouvelle-Calédonie pour prouver qu'une autre façon de reconnaître les compétences est possible.

---

## Principes non négociables

Ces règles ont priorité sur TOUTE décision technique ou fonctionnelle.

### 1. L'humain d'abord — « On code pour Céline »
Céline, 25 ans, conductrice de dumper, en situation d'illettrisme partiel. Si elle ne peut pas utiliser une fonctionnalité (sans lire, sans écrire, via la voix, en 3G sur un téléphone bas de gamme), **cette fonctionnalité est rejetée**.

### 2. Émancipation — « L'outil révèle, il ne classe pas »
Le projet ne traite jamais l'utilisateur comme un déficit. Il explicite les compétences implicites, il valorise activement, il restaure la dignité. Pas de score d'employabilité. Pas de jargon d'insertion. Si une fonctionnalité infantilise, classe, ou réduit l'utilisateur à un profil déficient, elle est rejetée.

### 3. Référentiel émergent — « Le territoire d'abord »
On ne classe pas les gens dans une grille importée. Le référentiel de compétences émerge des offres d'emploi réelles de Nouvelle-Calédonie. Le ROME v4 reste en arrière-plan pour l'interopérabilité, mais il n'est pas le cadre de référence. Les compétences qui comptent sont celles que les gens d'ici demandent et pratiquent.

### 4. Souveraineté des données
- Toutes les données personnelles restent sur le serveur en Nouvelle-Calédonie
- AUCUN appel API vers des LLM cloud (OpenAI, Anthropic, Google) en production
- Modèles LLM et STT exécutés localement
- Conformité RGPD obligatoire

### 5. Règle d'or du périmètre
> Si l'ajout d'une idée met en danger l'inventaire vocal (Objectif 1), le référentiel émergent (Objectif 2) ou la démo de mai (Objectif 3), elle est **automatiquement rejetée**.

Toute nouvelle feature doit être validée par le PO (Damien) ET ne pas impacter le chemin critique.

---

## Stack technique

| Couche | Technologie | Justification |
|---|---|---|
| **Frontend** | React + Vite (PWA) | Léger, fonctionne en 3G, installable |
| **Backend** | Python + FastAPI | Écosystème ML, équipe compétente |
| **Base de données** | PostgreSQL + pgvector | Matching sémantique vectoriel |
| **LLM local** | Mistral 7B ou Mixtral 8x7B via vLLM | Souveraineté, H100 disponible |
| **STT** | Whisper large-v3 (local) | Français, précision, local |
| **TTS** | Piper TTS (local) | Léger, français, open source |
| **Embeddings** | sentence-transformers (camembert/e5-multilingual) | Français natif, pgvector compatible |
| **Clustering** | HDBSCAN ou agglomératif (scikit-learn) | Clustering sémantique pour référentiel émergent |
| **Open Badges** | Standard 1EdTech Open Badges v3 | Interopérabilité |
| **Référentiel** | Émergent (inféré des offres NC) + ROME v4 (arrière-plan) | Souveraineté intellectuelle |
| **Serveur** | Local NC — NVIDIA H100 | Souveraineté + capacité LLM/STT |

### Architecture simplifiée

```
┌──────────────────────────────────────────────────────────────────┐
│                       SERVEUR NC (H100)                          │
│                                                                  │
│  ┌─────────┐  ┌──────────┐  ┌────────────┐                     │
│  │  vLLM   │  │ Whisper  │  │  Piper TTS │                     │
│  │ Mistral │  │ large-v3 │  │  (français) │                     │
│  └────┬────┘  └────┬─────┘  └─────┬──────┘                     │
│       │             │              │                             │
│  ┌────┴─────────────┴──────────────┴───────────────────────┐    │
│  │                   FastAPI Backend                        │    │
│  │                                                         │    │
│  │  ┌──────────────┐  ┌─────────────────────────────────┐  │    │
│  │  │ Pipeline      │  │ Pipeline inventaire vocal       │  │    │
│  │  │ référentiel   │  │ (STT → LLM → compétences)      │  │    │
│  │  │ émergent      │  │                                 │  │    │
│  │  │ (offres NC →  │  └─────────────────────────────────┘  │    │
│  │  │  extraction → │                                       │    │
│  │  │  clustering)  │  ┌─────────────────────────────────┐  │    │
│  │  └──────┬────────┘  │ Matching sémantique             │  │    │
│  │         │           │ (besoin recruteur ↔ profils     │  │    │
│  │         │           │  via référentiel émergent)      │  │    │
│  │         ▼           └─────────────────────────────────┘  │    │
│  │  ┌──────────────┐                                        │    │
│  │  │ Référentiel  │ ← Source de vérité pour le matching    │    │
│  │  │ émergent     │   et l'inventaire vocal                │    │
│  │  │ (emergent_   │                                        │    │
│  │  │  skills)     │  ┌─────────────────────────────────┐   │    │
│  │  └──────────────┘  │ ROME v4 (arrière-plan)          │   │    │
│  │                    │ interop. + comparaison uniquement│   │    │
│  │  ┌──────────────┐  └─────────────────────────────────┘   │    │
│  │  │ Auth/Consent │                                        │    │
│  │  │ Anonymisation│                                        │    │
│  │  └──────────────┘                                        │    │
│  └──────────────────────────┬──────────────────────────────┘    │
│                              │                                   │
│  ┌───────────────────────────┴──────────────────────┐           │
│  │  PostgreSQL + pgvector                           │           │
│  │  Tables : profiles, emergent_skills, raw_offers, │           │
│  │  badges, consents, rome_* (arrière-plan)         │           │
│  └──────────────────────────────────────────────────┘           │
└──────────────────────────────────────────────────────────────────┘
            │
            │ HTTPS (API REST + WebSocket audio)
            │
┌───────────┴───────────┐
│   PWA React (Vite)    │
│   - Mode vocal        │
│   - Mode hybride      │
│   - Mode accompagnement│
│   - Interface recruteur│
└───────────────────────┘
```

---

## Structure du monorepo

```
kompetens/
├── VISION.md                    # Fondation conceptuelle (lire en premier)
├── CLAUDE.md                    # Ce fichier (constitution technique)
├── BACKLOG.md                   # Stories + sprint plan
├── .claude/
│   └── skills/                  # Instructions spécialisées Claude Code
│       ├── referentiel.md       # 🔑 Référentiel émergent (brique clé)
│       ├── vocal.md             # Inventaire vocal
│       ├── matching.md          # Matching sémantique
│       ├── badges.md            # Open Badges v3
│       ├── opendata.md          # Pipeline Open Data
│       └── accessibility.md     # Accessibilité & bas débit
├── apps/
│   ├── web/                     # Frontend React PWA
│   │   ├── src/
│   │   │   ├── components/
│   │   │   ├── pages/
│   │   │   ├── hooks/
│   │   │   ├── services/
│   │   │   ├── stores/
│   │   │   └── i18n/
│   │   ├── public/
│   │   │   └── manifest.json
│   │   └── vite.config.ts
│   └── api/                     # Backend FastAPI
│       ├── app/
│       │   ├── main.py
│       │   ├── routers/
│       │   │   ├── vocal.py     # Endpoints inventaire vocal
│       │   │   ├── matching.py  # Endpoints matching recruteur
│       │   │   ├── badges.py    # Endpoints Open Badges
│       │   │   ├── profiles.py  # Gestion profils
│       │   │   ├── referentiel.py # Endpoints référentiel émergent
│       │   │   └── opendata.py  # Pipeline données / stats
│       │   ├── services/
│       │   │   ├── llm.py       # Interface vLLM
│       │   │   ├── stt.py       # Interface Whisper
│       │   │   ├── tts.py       # Interface Piper
│       │   │   ├── embeddings.py# Génération embeddings
│       │   │   ├── referentiel.py # Extraction + clustering offres NC
│       │   │   ├── rome.py      # Mapping ROME v4 (arrière-plan)
│       │   │   └── anonymizer.py# Anonymisation profils
│       │   ├── models/          # Modèles SQLAlchemy/Pydantic
│       │   ├── db/
│       │   └── config.py
│       ├── tests/
│       └── alembic/
├── packages/
│   └── shared/
├── data/
│   ├── rome/                    # Données ROME v4 (arrière-plan)
│   ├── offers/                  # Offres NC collectées (brutes)
│   ├── opendata/                # Données NC (ISEE, DTEFP)
│   └── seeds/                   # Données simulées POC
├── docs/
│   ├── architecture.md          # Schéma souveraineté (1 page)
│   ├── demo-scenario.md         # Scénario démo 10 min
│   ├── guide-aidant.md          # Guide pour Nadia
│   ├── api.md                   # Documentation API
│   └── spikes/                  # Résultats des spikes
│       ├── whisper-benchmark.md
│       ├── llm-benchmark.md
│       ├── tts-benchmark.md
│       └── offers-collection.md # Spike collecte offres NC
├── scripts/
│   ├── seed.py                  # Génération profils + offres simulés
│   ├── import-rome.py           # Import ROME v4 (arrière-plan)
│   ├── import-opendata.py       # Import données NC
│   ├── collect-offers.py        # Collecte offres emploi NC
│   └── build-referentiel.py     # Extraction + clustering → référentiel
├── docker-compose.yml
├── Makefile
└── pyproject.toml
```

---

## Personas de référence

Chaque feature doit être testable contre au moins un persona.

| Persona | Rôle | Critère de validation |
|---|---|---|
| **Céline** (25, illettrée, dumper) | Go/No-go du projet | Fonctionne sans lire/écrire, en vocal, en 3G |
| **Steeve** (38, ex-mine, numérique moyen) | Mode hybride | Peut mixer vocal et texte pré-rempli |
| **Didier** (52, patron BTP) | Matching recruteur | Trouve Céline en langage courant |
| **Nadia** (34, médiathèque, aidante) | Mode accompagnement | Guide aidant clair, parcours à deux fluide |
| **L'Écolo** (ingé, tribu isolée) | Zone blanche + badges | Fonctionne en dégradé, peut recommander un badge |
| **Kevin** (40, CA Open NC) | Démo | Comprend le POC en 10 min, convaincu |
| **Farid** (30, data scientist territorial) | Référentiel émergent | Pipeline reproductible, données traçables |
| **Clément** (23, étudiant Data) | Open source | Peut cloner, comprendre et contribuer |

---

## Conventions de code

### Python (Backend)
- **Formatage** : `ruff format` (ligne max 99 caractères)
- **Linting** : `ruff check` avec règles par défaut
- **Types** : Type hints obligatoires sur toutes les fonctions publiques
- **Docstrings** : Google style, en français pour le métier, en anglais pour le technique
- **Tests** : `pytest`, couverture minimum 60% sur les services critiques (LLM, matching, référentiel, anonymisation)
- **Async** : Toutes les routes FastAPI sont `async`
- **Nommage** :
  - Modules/fichiers : `snake_case`
  - Classes : `PascalCase`
  - Variables/fonctions : `snake_case`
  - Constantes : `UPPER_SNAKE_CASE`

### React (Frontend)
- **Formatage** : Prettier (défaut)
- **Linting** : ESLint avec config recommandée
- **Composants** : Functional components + hooks uniquement (pas de classes)
- **Style** : Tailwind CSS avec design system minimal
- **État** : Zustand pour le global, React state pour le local
- **Nommage** :
  - Composants : `PascalCase.tsx`
  - Hooks : `useCamelCase.ts`
  - Utilitaires : `camelCase.ts`
- **Accessibilité** : Attributs `aria-*` obligatoires sur les éléments interactifs

### Général
- **Commits** : Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`)
- **Branches** : `main` (stable) → `dev` (intégration) → `feat/xxx` ou `fix/xxx`
- **PR** : Revue par au moins 1 autre dev avant merge sur `dev`
- **Langue du code** : Anglais (variables, fonctions, commentaires techniques)
- **Langue du métier** : Français (noms de champs utilisateur, labels, docs)

---

## Commandes courantes

```bash
# Démarrage complet
make up                  # docker-compose up (API + DB + modèles)
make dev-web             # Frontend en mode dev (Vite)
make dev-api             # Backend en mode dev (uvicorn --reload)

# Tests
make test                # Tous les tests
make test-api            # Tests backend uniquement
make test-web            # Tests frontend uniquement

# Base de données
make db-migrate          # Appliquer les migrations Alembic
make db-seed             # Injecter données simulées

# Qualité
make lint                # Ruff + ESLint
make format              # Ruff format + Prettier

# Données
make import-rome         # Importer ROME v4 (arrière-plan)
make import-opendata     # Importer données NC (ISEE, DTEFP)
make collect-offers      # Collecter offres emploi NC
make build-referentiel   # Construire le référentiel émergent

# Audit
make audit-anon          # Vérifier l'anonymisation
```

---

## Règles pour Claude Code

### Ce que Claude Code DOIT faire
1. **Toujours vérifier** qu'une modification ne casse pas le parcours vocal de Céline
2. **Mapper sur le référentiel émergent en priorité** — le ROME v4 est un fallback, pas la source de vérité
3. **Respecter la structure monorepo** — ne pas créer de fichiers hors de l'arborescence définie
4. **Écrire les tests** en même temps que le code pour les services critiques
5. **Utiliser les types** Python (Pydantic) et TypeScript partout
6. **Documenter** chaque endpoint API avec des docstrings FastAPI (auto-OpenAPI)
7. **Anonymiser par défaut** — aucun nom, prénom ou identifiant direct dans les réponses de matching
8. **Respecter le ton d'émancipation** — pas de score, pas de classement, pas de vocabulaire déficitaire

### Ce que Claude Code NE DOIT PAS faire
1. **Jamais** ajouter de dépendance vers un service cloud LLM/STT (OpenAI, Anthropic API, Google Cloud Speech)
2. **Jamais** stocker de données personnelles en clair sans consentement
3. **Jamais** ajouter une feature qui n'est pas dans le backlog validé sans accord explicite
4. **Jamais** supprimer ou simplifier le mécanisme de consentement oral
5. **Jamais** écrire d'interface qui nécessite de savoir lire pour fonctionner (mode vocal)
6. **Jamais** utiliser de CDN externe pour les assets critiques (fonctionne hors-ligne dégradé)
7. **Jamais** traiter le ROME v4 comme la source de vérité des compétences — c'est le référentiel émergent
8. **Jamais** coder de « score d'employabilité » ou de classement des profils par « qualité »

### Quand Claude Code doit DEMANDER confirmation
- Ajout d'une nouvelle dépendance Python ou npm
- Modification du schéma de base de données
- Changement dans la pipeline LLM ou STT
- Modification du pipeline de construction du référentiel émergent
- Toute modification touchant à l'anonymisation ou au consentement

---

## Définition de « Done »

Une feature n'est terminée que si :

- [ ] Elle passe les tests automatisés
- [ ] Elle est utilisable par le persona cible (Céline pour le vocal, Didier pour le matching, etc.)
- [ ] Elle fonctionne en simulation bas débit (3G throttlé)
- [ ] Les données personnelles sont anonymisées par défaut
- [ ] Le consentement est recueilli avant toute collecte
- [ ] Le code est documenté (docstrings + commentaires si logique complexe)
- [ ] Elle a été revue par au moins 1 dev
- [ ] Elle ne traite pas l'utilisateur comme un déficit (principe d'émancipation)
- [ ] Si elle touche aux compétences : elle utilise le référentiel émergent, pas uniquement le ROME

---

## Contexte Nouvelle-Calédonie

- **Connectivité** : Très inégale. Nouméa = fibre, brousse/tribus = 3G voire zone blanche
- **Public cible** : Fort taux d'illettrisme (20%+ de la population adulte), fracture numérique majeure
- **Tissu économique** : Dominé par la mine (nickel) en crise, BTP, agriculture, services
- **Cadre légal** : Le RGPD s'applique en NC. Pas de CNIL locale mais la CNIL nationale est compétente
- **Référentiels** : Pas de référentiel local des métiers en tension → c'est exactement ce que le projet construit via le référentiel émergent
- **Langues** : Français + 28 langues kanak (hors périmètre POC, mais architecture prévue pour)
- **Offres d'emploi** : Souvent informelles (Facebook, bouche à oreille), le marché formel ne capture qu'une partie de la réalité
