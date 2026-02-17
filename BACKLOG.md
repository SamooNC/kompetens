# BACKLOG.md — Kompetens POC (v3 — pivot référentiel émergent)

> **Changement majeur v3** : Le référentiel émergent (inféré des offres NC) devient
> une brique 🔴 Now. Le ROME v4 passe en arrière-plan. L'épic E-10 monte en priorité
> et une nouvelle épic E-10b (référentiel émergent) est créée.
>
> **Cadence** : Sprints de 2 semaines
> **Capacité** : 4 devs × 10h/semaine = 80h/sprint
> **Horizon** : 7 sprints (17 février → 25 mai 2026)
> **PO** : Damien
> **Dernière mise à jour** : février 2026

---

## Règles de pilotage (Damien)

> 1. On ne commence un **Next** que quand les **Now** sont en bonne voie. Pas avant.
> 2. On ne commence un **Later** que quand les **Next** sont stabilisés.
> 3. Si mai approche et qu'il reste des Now en cours, on **sacrifie les Later sans regret**.
> 4. La priorité peut changer — mais seulement si l'équipe est d'accord et que les objectifs 1, 2 et 3 restent protégés.
> 5. Chaque épic a un porteur identifié. Pas « tout le monde ».

---

## Épics révisées

| # | Épic | Priorité v2 | **Priorité v3** | Justification du changement |
|---|---|---|---|---|
| E-01 | Dialogue vocal → inventaire | 🔴 Now | 🔴 Now | Inchangé |
| E-02 | Consentement oral | 🔴 Now | 🔴 Now | Inchangé |
| E-03 | Matching employeur | 🔴 Now | 🔴 Now | Inchangé, mais mappe sur référentiel émergent |
| E-04 | Anonymisation profils | 🔴 Now | 🔴 Now | Inchangé |
| E-05 | Scénario démo end-to-end | 🔴 Now | 🔴 Now | Inclut le référentiel émergent dans la démo |
| E-06 | Schéma souveraineté | 🔴 Now | 🔴 Now | Inclut la souveraineté intellectuelle (référentiel) |
| **E-10b** | **Référentiel émergent** | — | **🔴 Now** | **NOUVEAU. Brique clé. Collecte offres NC + extraction + clustering** |
| E-07 | Mode hybride voix/texte | 🟠 Next | 🟠 Next | Inchangé |
| E-08 | Mode accompagnement aidant | 🟠 Next | 🟠 Next | Inchangé |
| E-09 | Open badges | 🟠 Next | 🟠 Next | Inchangé |
| E-10 | Pipeline open data (stats) | 🟠 Next | 🟠 Next | Réduit au dashboard stats (la partie offres NC est dans E-10b) |
| E-11 | Dépôt open source + README | 🟠 Next | 🟠 Next | Inchangé |

---

## Vue synthétique v3

```
🔴 NOW (sans ça, pas de démo)
 ├── E-01   Dialogue vocal → inventaire
 ├── E-02   Consentement oral
 ├── E-03   Matching employeur (via référentiel émergent)
 ├── E-04   Anonymisation
 ├── E-05   Scénario de démo
 ├── E-06   Schéma souveraineté
 └── E-10b  ⭐ Référentiel émergent (offres NC → taxonomie)

🟠 NEXT (enrichit le POC)
 ├── E-07   Mode hybride voix/texte
 ├── E-08   Mode accompagnement aidant
 ├── E-09   Open badges
 ├── E-10   Pipeline open data (stats territoriales)
 └── E-11   Dépôt open source + README

🟢 LATER (si on a le temps)
 ├── E-12   Matching tutorat
 ├── E-13   Tableau de bord territorial
 ├── E-14   Spike : français calédonien
 └── E-15   Spike : identité sans e-mail

⚪ PERSPECTIVE (hors POC)
 ├── E-16   Architecture recherche
 ├── E-17   Mode hors-ligne
 └── E-18   Intégration institutionnelle
```

---

## Matrice épics ↔ sprints

| # | Épic | Prio | S0 | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|---|---|---|
| E-10b | **Référentiel émergent** | 🔴 | **spike** | **collecte** | **MVP** | ✓ | — | E2E | démo |
| E-01 | Dialogue vocal → inventaire | 🔴 | spike | MVP | ✓ | — | — | E2E | démo |
| E-02 | Consentement oral | 🔴 | — | MVP | ✓ | — | — | audit | — |
| E-03 | Matching employeur | 🔴 | spike | — | MVP | ✓ | — | E2E | démo |
| E-04 | Anonymisation profils | 🔴 | — | — | MVP | ✓ | — | audit | — |
| E-05 | Scénario démo | 🔴 | — | — | — | — | — | intég | MVP |
| E-06 | Schéma souveraineté | 🔴 | — | — | — | — | — | MVP | ✓ |
| E-07 | Mode hybride | 🟠 | — | — | — | MVP | ✓ | — | — |
| E-08 | Mode accompagnement | 🟠 | — | — | — | — | MVP | ✓ | — |
| E-09 | Open badges | 🟠 | — | — | — | — | MVP | ✓ | — |
| E-10 | Open data stats | 🟠 | — | — | — | — | MVP | ✓ | — |
| E-11 | Open source | 🟠 | — | — | — | — | — | — | MVP |
| — | Infra technique | 🔴 | setup | CI | seed | — | — | deploy | — |

**Changement clé** : E-10b (référentiel émergent) démarre au Sprint 0 et tourne en parallèle de E-01 pendant les Sprints 1-2. C'est le flux de données qui alimente tout le reste.

---

## Sprint 0 — Fondations (17 fév → 2 mars)

**Objectif** : Infra qui tourne + spikes ML + spike collecte offres NC.
**Épics** : Infrastructure + spikes E-01, E-03, **E-10b**

### Stories

#### S0-1 · Setup monorepo + Docker + CI
**Persona** : Clément · **Épic** : Infra
**En tant que** contributeur open source
**Je veux** cloner le repo et lancer le projet avec une seule commande

**Acceptation** :
- [ ] `git clone` + `make up` lance le stack complet
- [ ] Docker Compose : postgres+pgvector, api, web
- [ ] CI : lint + tests sur push
- [ ] README setup < 5 min
- [ ] Structure monorepo conforme au CLAUDE.md

**Porteur** : Dev 4 · **Estimation** : 12h

---

#### S0-2 · Spike : Whisper large-v3 sur H100
**Persona** : développeur · **Épic** : E-01
**Je veux** valider Whisper sur le H100 avec audio français

**Acceptation** :
- [ ] Script Python : WAV français → transcription
- [ ] Benchmark : latence 30s / 1min / 2min
- [ ] Test audio bruité
- [ ] `docs/spikes/whisper-benchmark.md`
- [ ] Décision Go/No-Go

**Porteur** : Dev 1 · **Estimation** : 8h

---

#### S0-3 · Spike : LLM local (vLLM + Mistral/Mixtral)
**Persona** : développeur · **Épic** : E-01, E-03, E-10b
**Je veux** valider le LLM sur H100 pour extraction de compétences ET extraction d'offres

**Acceptation** :
- [ ] vLLM servant le modèle (endpoint OpenAI-compatible)
- [ ] Test 1 : prompt extraction compétences depuis transcription vocale (E-01)
- [ ] Test 2 : prompt extraction compétences depuis offre d'emploi brute (E-10b)
- [ ] Benchmark : tokens/s, latence
- [ ] Comparatif Mistral 7B vs Mixtral 8x7B
- [ ] Décision Go/No-Go
- [ ] `docs/spikes/llm-benchmark.md`

**Porteur** : Dev 1 · **Estimation** : 12h

---

#### S0-4 · Spike : TTS local (Piper)
**Persona** : développeur · **Épic** : E-01
**Je veux** valider Piper TTS en français

**Acceptation** :
- [ ] Script Python : texte → WAV
- [ ] Qualité intelligible
- [ ] `docs/spikes/tts-benchmark.md`

**Porteur** : Dev 2 · **Estimation** : 6h

---

#### S0-5 · ⭐ Spike : collecte d'offres d'emploi NC
**Persona** : Farid · **Épic** : E-10b
**Je veux** valider qu'on peut collecter des offres d'emploi NC en volume suffisant

**Acceptation** :
- [ ] Identifier les sources scrapables (emploi.nc, autres sites NC)
- [ ] Tester le scraping sur 1 source (50+ offres)
- [ ] Identifier les CSV DTEFP disponibles et leur format
- [ ] Collecter manuellement 20 offres informelles (Facebook, groupes NC)
- [ ] Documenter le volume total atteignable et les contraintes légales
- [ ] `docs/spikes/offers-collection.md`
- [ ] **Décision** : quelles sources on retient pour le POC

**Porteur** : Dev 4 · **Estimation** : 10h

---

#### S0-6 · Schéma DB initial + migrations
**Persona** : développeur · **Épic** : Infra + E-10b
**Je veux** un schéma PostgreSQL avec pgvector incluant le référentiel émergent

**Acceptation** :
- [ ] Tables : `users`, `profiles`, `competences`, `experiences`, `consents`
- [ ] Tables référentiel : `raw_offers`, `extracted_skills`, `emergent_skills`
- [ ] Tables ROME (arrière-plan) : `rome_metiers`, `rome_competences`
- [ ] Extension pgvector, colonnes `embedding` sur `profiles` et `emergent_skills`
- [ ] Alembic initialisé, première migration
- [ ] Seed : 10 profils de test

**Porteur** : Dev 2 · **Estimation** : 10h

---

#### S0-7 · Squelette frontend PWA
**Persona** : Dev 3 · **Épic** : Infra

**Acceptation** :
- [ ] Vite + React + TypeScript + Tailwind
- [ ] React Router : accueil, inventaire, recruteur, aidant
- [ ] PWA manifest + Service Worker
- [ ] `<VocalButton />` placeholder
- [ ] Responsive mobile, boutons ≥ 48x48px

**Porteur** : Dev 3 · **Estimation** : 8h

---

#### S0-8 · Import ROME v4 (arrière-plan)
**Persona** : développeur · **Épic** : E-10b (comparaison)

**Acceptation** :
- [ ] Script `scripts/import-rome.py`
- [ ] Tables `rome_metiers`, `rome_competences`, `rome_appellations`
- [ ] Recherche full-text fonctionnelle
- [ ] Clairement documenté comme **référence secondaire**, pas source de vérité

**Porteur** : Dev 4 · **Estimation** : 6h

---

**Total Sprint 0 : ~72h / 80h — marge 8h**
**⚠️ Sprint plus chargé qu'en v2** à cause du spike offres (S0-5). Si besoin, S0-8 (ROME) peut glisser au Sprint 1.

---

## Sprint 1 — Inventaire vocal MVP + Pipeline offres [E-01 + E-02 + E-10b] (3 mars → 16 mars)

**Objectif** : Céline parle → compétences extraites. En parallèle, le pipeline d'offres NC tourne et commence à construire le référentiel émergent.
**Changement v3** : Le référentiel émergent se construit EN MÊME TEMPS que l'inventaire vocal. Les deux pipelines partagent le LLM.

### Stories

#### S1-1 · Capture audio navigateur + streaming
**Épic** : E-01 · **Persona** : Céline

**Acceptation** :
- [ ] Bouton push-to-talk 64x64px, animation "pulse"
- [ ] MediaRecorder API (WebM/Opus)
- [ ] VAD : arrêt après 3s silence
- [ ] Streaming WebSocket chunks 2s
- [ ] Feedback visuel : "j'écoute" / "je réfléchis" / "je parle"
- [ ] Chrome Android (bas de gamme)

**Porteur** : Dev 3 · **Estimation** : 15h

---

#### S1-2 · Endpoint STT (Whisper)
**Épic** : E-01

**Acceptation** :
- [ ] WebSocket `/ws/stt` accepte chunks audio
- [ ] Whisper large-v3 local
- [ ] Retour texte < 3s pour 30s d'audio
- [ ] Gestion erreurs

**Porteur** : Dev 1 · **Estimation** : 10h

---

#### S1-3 · Extraction compétences LLM (inventaire vocal)
**Épic** : E-01

**Acceptation** :
- [ ] Prompt système optimisé (cf. `skills/vocal.md`)
- [ ] Sortie JSON Pydantic (`InventaireVocal`)
- [ ] Mapping sur **référentiel émergent en priorité** (si assez peuplé), ROME v4 en fallback
- [ ] Questions de relance en langage simple (A2-B1)
- [ ] Le LLM explicite l'implicite (compétences inférées, pas seulement déclarées)
- [ ] Tests : 5 transcriptions simulées

**Porteur** : Dev 1 · **Estimation** : 15h

---

#### S1-4 · ⭐ Collecte et ingestion des offres NC
**Épic** : E-10b · **Persona** : Farid

**En tant que** Farid
**Je veux** un pipeline qui ingère les offres d'emploi NC de différentes sources
**Afin d'** alimenter le référentiel émergent

**Acceptation** :
- [ ] Script `scripts/collect-offers.py` :
  - Scraping de la source identifiée au spike S0-5
  - Import CSV DTEFP
  - Import manuel (fichier texte des offres informelles)
- [ ] Stockage en table `raw_offers` (source, date, zone, texte brut)
- [ ] Idempotent (pas de doublons)
- [ ] Objectif : **200+ offres** ingérées pour le Sprint 2
- [ ] Logs clairs, erreurs gérées

**Porteur** : Dev 4 · **Estimation** : 12h

---

#### S1-5 · ⭐ Extraction de compétences depuis les offres (LLM batch)
**Épic** : E-10b · **Persona** : Farid

**En tant que** système
**Je veux** extraire les compétences de chaque offre NC via le LLM
**Afin de** construire la matière première du référentiel émergent

**Acceptation** :
- [ ] Script `scripts/build-referentiel.py` (étape 1 : extraction)
- [ ] Prompt LLM optimisé pour offres NC (cf. `skills/referentiel.md`)
- [ ] Tolérance au langage informel ("cherche quelqu'un de sérieux")
- [ ] Sortie : `extracted_skills` en base (label, niveau, contexte, offer_id)
- [ ] Traitement batch (pas temps réel) — peut tourner la nuit
- [ ] Test : 10 offres réelles → au moins 3 compétences par offre

**Porteur** : Dev 1 · **Estimation** : 10h

---

#### S1-6 · Consentement oral
**Épic** : E-02 · **Persona** : Céline

**Acceptation** :
- [ ] TTS lit la demande de consentement
- [ ] STT détecte "oui" / "d'accord"
- [ ] Audio conservé (preuve RGPD)
- [ ] Horodatage + hash en base
- [ ] Si refus → aucune donnée conservée
- [ ] Texte consentement : **TODO Damien** (validation juridique)

**Porteur** : Dev 2 + Dev 3 · **Estimation** : 10h

---

**Total Sprint 1 : ~72h / 80h — marge 8h**
**⚠️ Sprint tendu.** La boucle conversationnelle vocale (relance TTS) est repoussée au Sprint 2 pour faire de la place au pipeline offres. Au Sprint 1, le vocal fonctionne en mode aller simple (parler → résultat).

---

## Sprint 2 — Matching MVP + Référentiel émergent [E-03 + E-04 + E-10b] (17 mars → 30 mars)

**Objectif** : Le référentiel émergent existe. Didier cherche → trouve Céline via ce référentiel. La boucle conversationnelle vocale est complétée.

### Stories

#### S2-1 · ⭐ Clustering sémantique → référentiel émergent
**Épic** : E-10b · **Persona** : Farid

**En tant que** Farid
**Je veux** que les compétences extraites des offres soient regroupées en compétences canoniques
**Afin d'** avoir un référentiel émergent utilisable pour le matching

**Acceptation** :
- [ ] Script `scripts/build-referentiel.py` (étape 2 : clustering)
- [ ] Embeddings de chaque `extracted_skill` (sentence-transformers)
- [ ] Clustering HDBSCAN ou agglomératif (seuil cosinus > 0.85)
- [ ] Chaque cluster → 1 `EmergentSkill` (label canonique + variantes + fréquence + zones + secteurs)
- [ ] Mapping ROME optionnel automatique (cosinus > 0.8)
- [ ] Table `emergent_skills` peuplée
- [ ] Au moins 1 compétence sans équivalent ROME → elle existe quand même
- [ ] `GET /api/referentiel/skills` retourne le référentiel complet
- [ ] `GET /api/referentiel/skills?zone=Province+Nord` filtre par zone

**Porteur** : Dev 1 + Dev 4 · **Estimation** : 15h

---

#### S2-2 · Boucle conversationnelle vocale (complément S1)
**Épic** : E-01 · **Persona** : Céline

**Acceptation** :
- [ ] LLM génère 1-2 questions de relance par tour
- [ ] Questions guidées par les compétences fréquentes du référentiel émergent dans la zone de Céline
- [ ] Questions → Piper TTS → audio lu automatiquement
- [ ] 2-3 tours max puis résumé final
- [ ] Résumé lu à voix haute pour confirmation

**Porteur** : Dev 1 + Dev 3 · **Estimation** : 12h

---

#### S2-3 · Génération d'embeddings profil
**Épic** : E-01, E-03

**Acceptation** :
- [ ] Service embedding (sentence-transformers)
- [ ] Embedding calculé dans le **même espace vectoriel** que le référentiel émergent
- [ ] Stockage pgvector
- [ ] Recalcul auto si profil mis à jour

**Porteur** : Dev 2 · **Estimation** : 8h

---

#### S2-4 · Interface recherche recruteur
**Épic** : E-03 · **Persona** : Didier

**Acceptation** :
- [ ] Page recruteur : textarea unique + bouton "Chercher"
- [ ] Option vocale
- [ ] Résultats en cartes : score, compétences, zone, explication LLM
- [ ] < 5 secondes
- [ ] Zéro donnée identifiante (E-04)
- [ ] Pas de filtre discriminant dans l'UI
- [ ] Les compétences affichées sont celles du **référentiel émergent** (pas des codes ROME)

**Porteur** : Dev 3 · **Estimation** : 12h

---

#### S2-5 · Endpoint matching sémantique
**Épic** : E-03 + E-04

**Acceptation** :
- [ ] `POST /api/matching/search` → `ResultatMatching`
- [ ] LLM extrait compétences du besoin → embedding
- [ ] Recherche pgvector (cosinus, threshold 0.6)
- [ ] Re-ranking LLM avec explication en langage courant
- [ ] Les compétences retournées sont libellées selon le **référentiel émergent**
- [ ] Anonymisation stricte (cf. `skills/matching.md`)
- [ ] Filtrage anti-discrimination

**Porteur** : Dev 1 + Dev 2 · **Estimation** : 15h

---

#### S2-6 · Seed 1000 profils + 200 offres
**Épic** : E-03, E-05

**Acceptation** :
- [ ] Script `scripts/seed.py`
- [ ] Les profils sont générés **à partir du référentiel émergent** (pas du ROME)
- [ ] 1000 profils variés, distribution réaliste zones NC
- [ ] 200 offres cohérentes avec le référentiel émergent
- [ ] 50 comptes recruteurs

**Porteur** : Dev 4 · **Estimation** : 10h

---

#### S2-7 · Expression d'intérêt recruteur
**Épic** : E-03 · **Persona** : Didier

**Acceptation** :
- [ ] Bouton "Je suis intéressé" sur chaque carte
- [ ] Log en base
- [ ] Pas de contact direct
- [ ] Confirmation visuelle

**Porteur** : Dev 3 · **Estimation** : 5h

---

**Total Sprint 2 : ~77h / 80h — marge 3h**
**⚠️ Sprint très chargé** — c'est le sprint pivot où tout se connecte. Si besoin, S2-7 (expression d'intérêt) glisse au Sprint 3.

---

## Sprint 3 — Solidification Now + premiers Next [E-07] (31 mars → 13 avril)

**Objectif** : Tous les 🔴 Now sont solides. Le référentiel émergent est validé. On attaque E-07 si le PO confirme.
**Gate Damien** : Si Now pas stables → 100% consolidation.

### Stories

#### S3-1 · Test intégration Céline → Référentiel → Didier
**Épic** : E-01 + E-03 + E-10b · **Persona** : Kevin

**Acceptation** :
- [ ] Parcours bout en bout :
  - Céline parle → compétences mappées sur référentiel émergent → profil créé
  - Didier cherche → trouve Céline via le même référentiel
- [ ] Les compétences sont en langage local (pas en codes ROME)
- [ ] Temps total < 7 minutes
- [ ] Fonctionne en 3G throttlé

**Porteur** : Dev 1 + Dev 3 · **Estimation** : 12h

---

#### S3-2 · Mode hybride voix/texte (si gate Now OK)
**Épic** : E-07 · **Persona** : Steeve

**Acceptation** :
- [ ] Après inventaire vocal, écran "Résumé" avec compétences en texte
- [ ] Compétences libellées selon le référentiel émergent
- [ ] Chaque compétence éditable
- [ ] Bouton "Ajouter une compétence"
- [ ] Bouton "Tout est bon" → valide + recalcule embedding
- [ ] Mode optionnel (Céline ne le voit pas en mode vocal pur)

**Porteur** : Dev 3 + Dev 2 · **Estimation** : 12h

---

#### S3-3 · Hardening anonymisation
**Épic** : E-04 · **Persona** : Marie

**Acceptation** :
- [ ] Audit tous les endpoints
- [ ] Test : profil avec nom/prénom → absence dans toute réponse matching
- [ ] Logs sans données personnelles
- [ ] `make audit-anon` automatisé

**Porteur** : Dev 2 · **Estimation** : 8h

---

#### S3-4 · Itération qualité référentiel émergent
**Épic** : E-10b · **Persona** : Farid

**Acceptation** :
- [ ] Revue manuelle de 20 `EmergentSkill` (labels pertinents ? clusters cohérents ?)
- [ ] Ajustement seuil clustering si nécessaire
- [ ] Ajout d'offres supplémentaires (objectif : 500+ offres totales)
- [ ] Re-run du pipeline complet
- [ ] Comparaison référentiel émergent vs ROME : documenter les écarts intéressants
- [ ] `docs/referentiel-emergent-v1.md` : état du référentiel, couverture, limites

**Porteur** : Dev 4 + Dev 1 · **Estimation** : 10h

---

#### S3-5 · Amélioration prompts LLM
**Épic** : E-01 + E-03 + E-10b

**Acceptation** :
- [ ] Revue résultats extraction vocale + extraction offres
- [ ] Ajustement prompts (faux positifs, compétences manquées)
- [ ] 5 nouveaux cas de test
- [ ] Résultats avant/après documentés

**Porteur** : Dev 1 · **Estimation** : 8h

---

#### S3-6 · Tests 3G et accessibilité
**Épic** : E-01, E-03

**Acceptation** :
- [ ] Page initiale < 200 Ko
- [ ] Service Worker opérationnel
- [ ] Tous parcours testés 384kbps / 500ms
- [ ] Indicateur réseau visuel
- [ ] Boutons ≥ 48x48px
- [ ] Contraste WCAG AA

**Porteur** : Dev 3 · **Estimation** : 8h

---

**Total Sprint 3 : ~58h / 80h — marge 22h (buffer consolidation)**

---

## Sprint 4 — Next : Accompagnement, Badges, Open Data stats [E-08, E-09, E-10] (14 avril → 27 avril)

**Objectif** : Les 🟠 Next enrichissent le POC.
**Gate Damien** : Si Now + référentiel pas stables → Sprint 4 = consolidation.

### Stories

#### S4-1 · Mode accompagnement aidant
**Épic** : E-08 · **Persona** : Nadia

**Acceptation** :
- [ ] Toggle "Mode accompagnement"
- [ ] Panneau aidant : instructions + transcription en cours
- [ ] Usager garde l'interface vocale simplifiée
- [ ] Guide aidant (5-7 étapes)
- [ ] Guide exportable PDF < 4 pages

**Porteur** : Dev 3 + Dev 4 · **Estimation** : 15h

---

#### S4-2 · Émission badges Open Badges v3
**Épic** : E-09 · **Persona** : Céline, Clément

**Acceptation** :
- [ ] Badges générés après validation inventaire (1 par compétence principale)
- [ ] Les compétences badgées sont libellées selon le **référentiel émergent**
- [ ] JSON-LD Open Badges v3
- [ ] Signature Ed25519
- [ ] Statut `pending_endorsement`
- [ ] Endpoint `GET /api/badges/{id}`

**Porteur** : Dev 2 · **Estimation** : 12h

---

#### S4-3 · Workflow recommandation tuteur
**Épic** : E-09 · **Persona** : L'Écolo

**Acceptation** :
- [ ] Lien unique (token)
- [ ] Page recommandation légère (fonctionne connexion lente)
- [ ] "Je confirme" / "Je ne peux pas confirmer"
- [ ] Badge `issued` si confirmé

**Porteur** : Dev 2 + Dev 3 · **Estimation** : 10h

---

#### S4-4 · API métiers en tension (Open Data stats)
**Épic** : E-10 · **Persona** : Kevin, Marie

**En tant que** Kevin
**Je veux** voir les métiers en tension par zone, construits à partir du référentiel émergent
**Afin de** montrer l'intelligence territoriale du POC

**Acceptation** :
- [ ] `GET /api/opendata/tensions?zone=Province+Nord`
- [ ] Construit à partir du référentiel émergent (fréquence des compétences par zone)
- [ ] Enrichi par les données ISEE/DTEFP si disponibles
- [ ] Top 10 métiers/compétences en tension
- [ ] Données sourcées et datées

**Porteur** : Dev 4 · **Estimation** : 8h

---

#### S4-5 · Import complémentaire Open Data NC
**Épic** : E-10

**Acceptation** :
- [ ] Import CSV ISEE (stats emploi)
- [ ] Import CSV DTEFP (offres enregistrées — viennent aussi nourrir le référentiel)
- [ ] Parsing robuste
- [ ] Tables `stats_emploi`

**Porteur** : Dev 4 · **Estimation** : 8h

---

**Total Sprint 4 : ~53h / 80h — marge 27h**

---

## Sprint 5 — Intégration & Souveraineté [E-05, E-06] (28 avril → 11 mai)

**Objectif** : Tout connecté bout en bout. Souveraineté documentée. Le référentiel émergent est dans la démo.

### Stories

#### S5-1 · Parcours end-to-end intégré
**Épic** : E-05

**Acceptation** :
- [ ] Céline : vocal → inventaire → consentement → profil → badge pending
- [ ] Tuteur : recommandation → badge issued
- [ ] Didier : recherche → trouve Céline (avec badge, compétences du référentiel émergent)
- [ ] Kevin : voit les métiers en tension par zone
- [ ] Pas d'étape manuelle
- [ ] Parcours Céline < 5 min, Didier < 2 min

**Porteur** : Tous · **Estimation** : 15h

---

#### S5-2 · Document architecture souveraineté (1 page)
**Épic** : E-06

**Acceptation** :
- [ ] `docs/architecture.md` — 1 page max
- [ ] Schéma : données → serveur NC → rien ne sort
- [ ] **Inclut la souveraineté intellectuelle** : le référentiel émerge du territoire, il n'est pas importé
- [ ] Mention RGPD + consentement oral
- [ ] Relu par profil juridique + DSI (TODO Damien)

**Porteur** : Dev 1 · **Estimation** : 4h

---

#### S5-3 · Audit anonymisation final
**Épic** : E-04

**Acceptation** :
- [ ] `make audit-anon`
- [ ] Audit logs
- [ ] Vérification consentement
- [ ] `docs/audit-anonymisation.md`

**Porteur** : Dev 2 · **Estimation** : 6h

---

#### S5-4 · Documentation API
**Épic** : E-11

**Acceptation** :
- [ ] Swagger à `/docs`
- [ ] Tous endpoints documentés (incluant `/api/referentiel/*`)
- [ ] `docs/api.md`

**Porteur** : Dev 2 · **Estimation** : 6h

---

#### S5-5 · Tests de charge
**Épic** : E-05

**Acceptation** :
- [ ] Matching sur 1000 profils < 5s
- [ ] Pipeline STT+LLM < 10s pour 30s audio
- [ ] Pipeline extraction offre < 5s par offre
- [ ] 5 utilisateurs simultanés = pas de crash
- [ ] `docs/benchmarks.md`

**Porteur** : Dev 1 · **Estimation** : 8h

---

#### S5-6 · Affichage badges profil (si marge)
**Épic** : E-09

**Acceptation** :
- [ ] Page profil : badges
- [ ] Téléchargement JSON-LD
- [ ] Endpoint vérification

**Porteur** : Dev 3 · **Estimation** : 8h

---

**Total Sprint 5 : ~47h / 80h — marge 33h (buffer pré-démo)**

---

## Sprint 6 — Démo & Polish [E-05, E-11] (12 mai → 25 mai)

**Objectif** : Démo prête. Code livré. Zéro nouvelle fonctionnalité.

### Stories

#### S6-1 · Scénario de démo (10 minutes)
**Épic** : E-05 · **Persona** : Kevin

**Acceptation** :
- [ ] `docs/demo-scenario.md` minute par minute :
  1. Contexte + vision (1 min)
  2. Céline parle → inventaire vocal (3 min)
  3. Badge émis + recommandation tuteur (1 min)
  4. Didier cherche → trouve Céline (2 min)
  5. **Référentiel émergent + métiers en tension** (1 min) ← NOUVEAU
  6. Souveraineté (1 min)
  7. Conclusion + open source (1 min)
- [ ] Données de démo préchargées
- [ ] Plan B réseau lent
- [ ] Répété ≥ 2 fois
- [ ] Version courte 5 min identifiée

**Porteur** : Tous · **Estimation** : 10h

---

#### S6-2 · Bug fixes & polish UI
**Épic** : Tous

**Acceptation** :
- [ ] Bugs P0 résolus
- [ ] Chrome Android réel (bas de gamme)
- [ ] Animations fluides
- [ ] Messages d'erreur visuels
- [ ] Pas de console errors

**Porteur** : Dev 3 + tous · **Estimation** : 20h

---

#### S6-3 · Documentation open source
**Épic** : E-11

**Acceptation** :
- [ ] README.md complet (inclut section sur le référentiel émergent)
- [ ] CONTRIBUTING.md
- [ ] LICENSE : PolyForm Noncommercial 1.0.0
- [ ] Commandes `make` documentées
- [ ] Installation + démo < 1h

**Porteur** : Dev 4 · **Estimation** : 8h

---

#### S6-4 · Déploiement serveur NC
**Épic** : E-05

**Acceptation** :
- [ ] Docker Compose production
- [ ] HTTPS
- [ ] Backup DB
- [ ] Monitoring basique
- [ ] URL accessible

**Porteur** : Dev 4 · **Estimation** : 12h

---

**Total Sprint 6 : ~50h / 80h — marge 30h**

---

## Épics 🟢 Later — non planifiées

| # | Épic | Prérequis | Estimation |
|---|---|---|---|
| E-12 | Matching tutorat | E-01 + E-09 | 20-30h |
| E-13 | Tableau de bord territorial | E-10 + E-10b | 15-20h |
| E-14 | Spike : français calédonien | E-01 | 8-12h |
| E-15 | Spike : identité sans e-mail | E-08 | 8-12h |

## Épics ⚪ Perspective — hors POC

| # | Épic |
|---|---|
| E-16 | Architecture recherche (ANR/thèse) |
| E-17 | Mode hors-ligne |
| E-18 | Intégration institutionnelle (DEL, CAFAT) |

---

## Récapitulatif vélocité

| Sprint | Estimé (h) | Capacité (h) | Marge | Focus |
|---|---|---|---|---|
| S0 | 72 | 80 | 8h 🟠 | Infra + spikes ML + **spike offres NC** |
| S1 | 72 | 80 | 8h 🟠 | 🔴 E-01 + E-02 + **E-10b collecte** |
| S2 | 77 | 80 | 3h 🔴 | 🔴 E-03 + E-04 + **E-10b clustering** |
| S3 | 58 | 80 | 22h 🟢 | Consolidation Now + 🟠 E-07 |
| S4 | 53 | 80 | 27h 🟢 | 🟠 E-08, E-09, E-10 |
| S5 | 47 | 80 | 33h 🟢 | Intégration E-05, E-06 |
| S6 | 50 | 80 | 30h 🟢 | Démo + E-11 |
| **Total** | **429** | **560** | **131h (23%)** | |

> **Marge globale 23%** — plus serrée qu'en v2 (29%) à cause du référentiel émergent.
> Les sprints 0-2 sont tendus mais c'est justifié : les 3 piliers (vocal, référentiel, matching) doivent être en MVP avant la mi-sprint 3.
> Les sprints 3-5 absorbent les retards éventuels.

---

## Risques (mis à jour v3)

| # | Risque | Impact | Mitigation | Épic |
|---|---|---|---|---|
| R1 | Whisper/LLM ne tourne pas sur H100 | 🔴 Bloquant | Spike S0, fallback modèles plus petits | E-01 |
| R2 | Qualité extraction compétences insuffisante | 🟠 Élevé | Itérations prompts S3, tests variés | E-01, E-10b |
| **R3** | **Volume d'offres NC insuffisant pour construire un référentiel crédible** | **🟠 Élevé** | **Spike S0-5, sources multiples (formel + informel), seed si nécessaire** | **E-10b** |
| **R4** | **Clustering produit des compétences incohérentes** | **🟠 Moyen** | **Revue manuelle S3, ajustement seuils, itération** | **E-10b** |
| R5 | Données ISEE/DTEFP indisponibles | 🟡 Faible | Données simulées en fallback (le référentiel émergent est la priorité) | E-10 |
| R6 | Disponibilité réelle < 10h/semaine | 🟠 Moyen | Buffer sprints 3-5 | Tous |
| R7 | Complexité Open Badges v3 | 🟡 Faible | Implémentation minimale | E-09 |
| R8 | Texte consentement non validé juridiquement | 🟠 Moyen | **Action Damien** : faire relire avant S2 | E-02 |
| R9 | Scraping sites emploi NC bloqué (anti-bot, CGU) | 🟡 Moyen | Fallback : offres DTEFP + collecte manuelle | E-10b |

---

## Répartition des devs (mise à jour v3)

| Dev | Spécialité | Focus principal | Focus secondaire |
|---|---|---|---|
| **Dev 1** (backend ML) | Python, ML, LLM | Pipeline vocal (STT→LLM→compétences) | Extraction compétences offres, clustering |
| **Dev 2** (backend) | Python, FastAPI, DB | API, matching, badges, anonymisation | Consentement, schéma DB |
| **Dev 3** (frontend) | React, UX, accessibilité | Interface Céline, Didier, Nadia | PWA, Service Worker, 3G |
| **Dev 4** (fullstack) | Mix, DevOps, data | **Collecte offres NC, pipeline référentiel** | Docker, CI, Open Data, déploiement |

**Changement v3** : Dev 4 devient le **porteur du référentiel émergent** (collecte + pipeline). C'est son fil rouge tout au long du projet.
