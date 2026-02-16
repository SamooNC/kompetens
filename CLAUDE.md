# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **Ce fichier est la constitution du projet. Claude Code doit le lire avant toute action.**

## Project identity

**Kompetens** — POC (Proof of Concept), NOT a finished product.
Deadline: May 2026 demo. Sponsor: Commission Data & IA, cluster OPEN NC (Nouvelle-Calédonie).
License: PolyForm Noncommercial 1.0.0.

**Mission**: Prove that a voice-first, sovereign tool can connect job-seekers (including illiterate users) with recruiters through human intermediaries, in New Caledonia.

## Key references

- **BACKLOG.md** — 7-sprint roadmap (S0–S6, Feb 17 → May 25 2026), detailed user stories, velocity, risks
- **.claude/vocal.md** — Voice inventory extraction pipeline (CRITICAL, priority #1)
- **.claude/matching.md** — Semantic matching with anonymization rules (CRITICAL)
- **.claude/badges.md** — Open Badges v3 cryptographic workflow
- **.claude/opendata.md** — NC government data ingestion pipeline
- **.claude/accessibility.md** — Low-bandwidth & illiteracy accessibility constraints (transversal)

Read the relevant skill file before working on that domain.

## Non-negotiable principles

These override ALL technical decisions.

### 1. "Code for Céline"
Céline, 25, dump truck driver, partially illiterate. If she can't use a feature (no reading, no writing, voice only, 3G on a cheap phone), **the feature is rejected**.

### 2. Data sovereignty
- All personal data stays on the NC server — NO cloud LLM/STT API calls (OpenAI, Anthropic, Google) in production
- LLM, STT, TTS, embeddings all run locally on NVIDIA H100
- RGPD compliance mandatory

### 3. Scope golden rule
> If adding a feature endangers the voice inventory (Objective 1) or the May demo (Objective 3), it is **automatically rejected**.

New features require PO (Damien) approval AND must not impact the critical path.

## Tech stack

| Layer | Technology |
|---|---|
| **Frontend** | React + Vite (PWA), Tailwind CSS, Zustand |
| **Backend** | Python + FastAPI (async) |
| **Database** | PostgreSQL + pgvector (Alembic migrations) |
| **LLM** | Mistral 7B or Mixtral 8x7B via vLLM (local) |
| **STT** | Whisper large-v3 (local) |
| **TTS** | Piper TTS (local, French) |
| **Embeddings** | sentence-transformers (camembert/e5-multilingual) |
| **Badges** | Open Badges v3 (JSON-LD, Ed25519 signing) |
| **Job taxonomy** | ROME v4 (Pôle Emploi) |

### Architecture

```
SERVEUR NC (H100)
  vLLM (Mistral) + Whisper + Piper TTS
       ↓
  FastAPI Backend (auth/consent + competence/ROME pipeline)
       ↓
  PostgreSQL + pgvector (profiles, embeddings, badges)
       ↓ HTTPS (REST + WebSocket audio)
  PWA React (vocal mode, hybrid mode, helper mode, recruiter UI)
```

## Planned monorepo structure

> **NOTE**: This is the target structure. Not all directories exist yet — create them as needed following this layout.

```
kompetens/
├── CLAUDE.md
├── BACKLOG.md
├── .claude/                     # Skill files for Claude Code
│   ├── vocal.md / matching.md / badges.md / opendata.md / accessibility.md
├── apps/
│   ├── web/                     # React PWA (Vite + Tailwind + Zustand)
│   │   └── src/ (components/, pages/, hooks/, services/, stores/, i18n/)
│   └── api/                     # FastAPI backend
│       ├── app/ (main.py, routers/, services/, models/, db/, config.py)
│       ├── tests/
│       └── alembic/
├── packages/shared/             # Shared types/constants
├── data/ (rome/, opendata/, seeds/)
├── docs/
├── scripts/ (seed.py, import-rome.py, import-opendata.py)
├── docker-compose.yml
├── Makefile
└── pyproject.toml
```

## Commands

> **NOTE**: These commands require the Makefile to be created (Sprint S0). Until then, run the underlying tools directly.

```bash
# Development
make up                  # docker-compose up (API + DB + models)
make dev-web             # Vite dev server
make dev-api             # uvicorn --reload

# Testing
make test                # All tests
make test-api            # pytest (backend only)
make test-web            # Frontend tests only

# Single test file (direct)
cd apps/api && python -m pytest tests/test_matching.py -v
cd apps/web && npx vitest run src/components/VocalButton.test.tsx

# Database
make db-migrate          # Alembic migrations
make db-seed             # Inject simulated data

# Code quality
make lint                # ruff check + ESLint
make format              # ruff format + Prettier

# Data import
make import-rome         # Import ROME v4 taxonomy
make import-opendata     # Import NC data (ISEE, DTEFP)
```

## Personas

Every feature must be testable against at least one persona.

| Persona | Validation gate |
|---|---|
| **Céline** (25, illiterate, dump truck) | Works without reading/writing, voice-only, on 3G |
| **Steeve** (38, ex-mining, medium digital) | Can mix voice and pre-filled text (hybrid mode) |
| **Didier** (52, BTP employer) | Finds Céline with plain-language search |
| **Nadia** (34, librarian, helper) | Clear helper guide, dual-screen companion flow |
| **L'Écolo** (engineer, remote tribe) | Works degraded (offline shell), can endorse a badge |
| **Kevin** (40, OPEN NC board) | Understands the POC in 10 min demo |
| **Clément** (23, data student) | Can clone, understand, and contribute |

## Code conventions

### Python (Backend)
- Format: `ruff format` (99 char line max)
- Lint: `ruff check`
- Type hints mandatory on all public functions
- Docstrings: Google style — French for business logic, English for technical
- Tests: `pytest`, 60% min coverage on critical services (LLM, matching, anonymization)
- All FastAPI routes are `async`

### React (Frontend)
- Format: Prettier
- Lint: ESLint (recommended config)
- Functional components + hooks only (no classes)
- Tailwind CSS, Zustand for global state
- `aria-*` attributes mandatory on interactive elements

### General
- Commits: Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`)
- Branches: `main` → `dev` → `feat/xxx` or `fix/xxx`
- Code language: English (variables, functions, technical comments)
- Business language: French (user-facing field names, labels, docs)

## Rules for Claude Code

### MUST do
1. Verify changes don't break Céline's voice path
2. Follow the monorepo structure — don't create files outside the defined tree
3. Write tests alongside code for critical services
4. Use Python type hints (Pydantic) and TypeScript everywhere
5. Document every API endpoint with FastAPI docstrings (auto-OpenAPI)
6. Anonymize by default — no name, surname, or direct identifier in matching responses

### MUST NOT do
1. Add dependencies on cloud LLM/STT services (OpenAI, Anthropic API, Google Cloud Speech)
2. Store personal data without consent
3. Add features not in the validated backlog without explicit approval
4. Remove or simplify the oral consent mechanism
5. Build voice interface that requires reading to function
6. Use external CDNs for critical assets (must work offline-degraded)

### MUST ASK before
- Adding a new Python or npm dependency
- Modifying the database schema
- Changing the LLM or STT pipeline
- Any modification to anonymization or consent logic

## Definition of Done

A feature is complete only when:
- Passes automated tests
- Usable by the target persona (Céline for vocal, Didier for matching, etc.)
- Works under simulated low bandwidth (3G throttled: 384 kbps, 500ms latency)
- Personal data anonymized by default
- Consent collected before any data collection
- Code documented (docstrings + comments for complex logic)

## New Caledonia context

- **Connectivity**: Very uneven — fiber in Nouméa, 3G/dead zones in bush/tribes
- **Target audience**: 20%+ adult illiteracy, major digital divide
- **Economy**: Mining (nickel) in crisis, construction, agriculture, services
- **Legal**: RGPD applies in NC (CNIL nationale competent)
- **Job taxonomy**: No local reference → adapting ROME v4
- **Languages**: French + 28 Kanak languages (out of POC scope, but architecture allows future support)
