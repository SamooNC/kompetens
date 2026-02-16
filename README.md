# Kompetens

POC (Proof of Concept) d'un outil **voice-first** et **souverain** de mise en relation entre chercheurs d'emploi et recruteurs, concu pour la Nouvelle-Caledonie.

**Mission** : Prouver qu'un outil vocal peut connecter les chercheurs d'emploi (y compris les personnes en situation d'illettrisme) avec les recruteurs, via des intermediaires humains.

Projet porte par la Commission Data & IA du cluster OPEN NC.

## Stack technique

| Couche | Technologie |
|---|---|
| Frontend | React + Vite (PWA), Tailwind CSS, Zustand |
| Backend | Python + FastAPI (async) |
| Base de donnees | PostgreSQL + pgvector (migrations Alembic) |
| LLM | Mistral 7B / Mixtral 8x7B via vLLM (local) |
| STT | Whisper large-v3 (local) |
| TTS | Piper TTS (local, francais) |
| Embeddings | sentence-transformers (e5-multilingual) |
| Badges | Open Badges v3 (JSON-LD, Ed25519) |
| Taxonomie emploi | ROME v4 (Pole Emploi) |

Toute l'IA tourne **localement** sur serveur NC (NVIDIA H100) — aucun appel cloud.

## Demarrage rapide

```bash
git clone <url-du-repo> && cd kompetens
cp .env.example .env
make up            # Lance PostgreSQL + API + Frontend (Docker)
make db-migrate    # Applique les migrations Alembic
make db-seed       # Injecte les donnees de test
```

L'API est accessible sur `http://localhost:8000`, le frontend sur `http://localhost:5173`.

## Commandes disponibles

```bash
# Developpement
make up              # docker compose up (API + DB + front)
make down            # docker compose down
make dev-api         # uvicorn --reload (hors Docker)
make dev-web         # vite dev server (hors Docker)

# Tests
make test            # Tous les tests (API + web)
make test-api        # pytest (backend)
make test-web        # vitest (frontend)

# Qualite de code
make lint            # ruff check + eslint
make format          # ruff format + prettier

# Base de donnees
make db-migrate      # Alembic upgrade head
make db-seed         # Donnees simulees

# Import de donnees
make import-rome     # Taxonomie ROME v4
make import-opendata # Donnees NC (ISEE, DTEFP)
```

## Structure du projet

```
kompetens/
├── apps/
│   ├── web/             # PWA React (Vite + Tailwind + Zustand)
│   └── api/             # Backend FastAPI
│       ├── app/         # Code applicatif
│       ├── tests/
│       └── alembic/     # Migrations DB
├── data/                # ROME, open data, seeds
├── scripts/             # Scripts d'import et utilitaires
├── docker-compose.yml
├── Makefile
└── CLAUDE.md            # Instructions pour Claude Code
```

## Personas

Le POC est concu pour ces utilisateurs types :

| Persona | Role |
|---|---|
| **Celine** (25 ans, conductrice d'engins) | Chercheur d'emploi, illettrisme partiel — voix uniquement |
| **Steeve** (38 ans, ex-mines) | Chercheur d'emploi — mode hybride voix/texte |
| **Didier** (52 ans, employeur BTP) | Recruteur — recherche en langage naturel |
| **Nadia** (34 ans, bibliothecaire) | Aidante — accompagnement en binome |

## Contribuer

Voir `CLAUDE.md` pour les conventions de code, la structure du projet et les regles de contribution.

Les commits suivent le format [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, etc.).

## Licence

[PolyForm Noncommercial 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0/)
