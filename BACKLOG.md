# BACKLOG.md — Kompetens POC

> **Cadence** : Sprints de 2 semaines
> **Capacité** : 4 devs × 10h/semaine = 80h/sprint
> **Horizon** : 7 sprints (17 février → 25 mai 2026)
> **PO** : Damien

---

## Vue d'ensemble des sprints

| Sprint | Dates | Thème | Objectif clé |
|---|---|---|---|
| **S0** | 17 fév — 2 mars | Fondations | Infra qui tourne, spike vocal |
| **S1** | 3 mars — 16 mars | Inventaire vocal MVP | Céline parle → compétences extraites |
| **S2** | 17 mars — 30 mars | Matching MVP | Didier cherche → trouve Céline |
| **S3** | 31 mars — 13 avril | Accompagnement + Badges | Nadia guide Céline, badge émis |
| **S4** | 14 avril — 27 avril | Open Data + Données | Pipeline NC + seed 1000 profils |
| **S5** | 28 avril — 11 mai | Intégration & Souveraineté | Tout connecté, doc architecture |
| **S6** | 12 mai — 25 mai | Démo & Polish | Scénario 10 min, bug fixes, docs |

---

## Sprint 0 — Fondations (17 fév → 2 mars)

**But** : Tout le monde peut coder, les briques ML tournent, l'architecture est validée.

### Stories

#### S0-1 · Setup monorepo
**En tant que** développeur (Clément)
**Je veux** cloner le repo et lancer le projet avec une seule commande
**Afin de** pouvoir contribuer immédiatement

**Critères d'acceptation** :
- [ ] `git clone` + `make up` lance le stack complet (API + DB + front)
- [ ] README avec instructions de setup (<5 min)
- [ ] Docker Compose avec services : postgres, api, web
- [ ] CI basique (lint + tests) configurée

**Estimation** : 12h

---

#### S0-2 · Spike Whisper local
**En tant que** développeur
**Je veux** vérifier que Whisper large-v3 fonctionne sur le H100 avec de l'audio français
**Afin de** valider la faisabilité du STT souverain

**Critères d'acceptation** :
- [ ] Script Python qui prend un fichier WAV français → retourne la transcription
- [ ] Benchmark : temps de transcription pour 30s / 1min / 2min d'audio
- [ ] Test avec audio bruité (simulation bruit de chantier)
- [ ] Résultat documenté dans `docs/spikes/whisper-benchmark.md`

**Estimation** : 8h

---

#### S0-3 · Spike LLM local (vLLM + Mistral)
**En tant que** développeur
**Je veux** vérifier que Mistral (7B ou Mixtral 8x7B) tourne via vLLM sur le H100
**Afin de** valider la faisabilité du LLM souverain

**Critères d'acceptation** :
- [ ] vLLM qui sert Mistral avec endpoint OpenAI-compatible
- [ ] Test de prompt d'extraction de compétences (input = transcription simulée)
- [ ] Benchmark : tokens/seconde, latence first token
- [ ] Comparaison 7B vs Mixtral 8x7B (qualité vs performance)
- [ ] Résultat documenté dans `docs/spikes/llm-benchmark.md`

**Estimation** : 10h

---

#### S0-4 · Spike TTS local (Piper)
**En tant que** développeur
**Je veux** vérifier que Piper TTS produit de la synthèse vocale française intelligible
**Afin de** valider le feedback vocal pour Céline

**Critères d'acceptation** :
- [ ] Script Python : texte français → fichier audio WAV
- [ ] Qualité subjective : intelligible, pas robotique au point de gêner la compréhension
- [ ] Benchmark : temps de génération pour 1 phrase / 1 paragraphe
- [ ] Test des voix françaises disponibles (masculine/féminine)

**Estimation** : 6h

---

#### S0-5 · Schéma DB initial + migrations
**En tant que** développeur
**Je veux** un schéma PostgreSQL de base avec Alembic configuré
**Afin de** pouvoir stocker profils, compétences et badges dès le Sprint 1

**Critères d'acceptation** :
- [ ] Tables : `users`, `profiles`, `competences`, `experiences`, `badges`, `consents`
- [ ] Extension pgvector activée, colonne `embedding` sur `profiles`
- [ ] Alembic initialisé avec première migration
- [ ] Script seed minimal (10 profils de test)

**Estimation** : 8h

---

#### S0-6 · Squelette frontend PWA
**En tant que** développeur frontend
**Je veux** un projet React+Vite configuré avec Tailwind, router et PWA manifest
**Afin de** commencer le développement UI au Sprint 1

**Critères d'acceptation** :
- [ ] Vite + React + TypeScript + Tailwind configurés
- [ ] React Router avec routes placeholder (accueil, inventaire, recruteur, aidant)
- [ ] PWA manifest + Service Worker basique (cache shell)
- [ ] Composant `<VocalButton />` placeholder (UI seulement, pas de logique audio)
- [ ] Fonctionne sur mobile (responsive)

**Estimation** : 8h

---

#### S0-7 · Import ROME v4
**En tant que** développeur
**Je veux** importer le référentiel ROME v4 en base de données
**Afin de** pouvoir mapper les compétences extraites sur des codes standardisés

**Critères d'acceptation** :
- [ ] Script `scripts/import-rome.py` qui parse les fichiers ROME v4 (XML/CSV)
- [ ] Tables `rome_metiers`, `rome_competences`, `rome_appellations`
- [ ] Recherche full-text fonctionnelle sur les intitulés
- [ ] Stats : nombre de fiches importées logué

**Estimation** : 8h

---

**Total Sprint 0 : ~60h** (marge de 20h pour imprévus setup)

---

## Sprint 1 — Inventaire vocal MVP (3 mars → 16 mars)

**But** : Céline parle dans son téléphone et obtient un inventaire de compétences.

### Stories

#### S1-1 · Capture audio navigateur
**En tant que** Céline
**Je veux** appuyer sur un gros bouton et parler dans mon téléphone
**Afin de** décrire ce que je sais faire sans avoir à écrire

**Critères d'acceptation** :
- [ ] Bouton push-to-talk (64x64px minimum) avec animation visuelle
- [ ] Capture audio via MediaRecorder API (WebM/Opus)
- [ ] Détection de silence (VAD) → arrêt auto après 3s de silence
- [ ] Envoi par WebSocket au backend (streaming chunks 2s)
- [ ] Feedback visuel : "j'écoute" / "je réfléchis" / "je parle"
- [ ] Fonctionne sur Chrome Android

**Estimation** : 15h

---

#### S1-2 · Endpoint STT (Whisper)
**En tant que** le système
**Je veux** recevoir un flux audio et retourner la transcription en texte
**Afin d'** alimenter le LLM en texte

**Critères d'acceptation** :
- [ ] WebSocket `/ws/stt` qui accepte des chunks audio
- [ ] Transcription via Whisper large-v3 local
- [ ] Retour du texte transcrit en <3 secondes pour 30s d'audio
- [ ] Gestion des erreurs (audio trop court, format invalide)

**Estimation** : 10h

---

#### S1-3 · Extraction de compétences par LLM
**En tant que** le système
**Je veux** analyser une transcription vocale et extraire des compétences structurées
**Afin de** produire l'inventaire de Céline

**Critères d'acceptation** :
- [ ] Prompt système optimisé (cf. `skills/vocal.md`)
- [ ] Sortie JSON validée par schéma Pydantic (`InventaireVocal`)
- [ ] Mapping automatique vers codes ROME v4 (top 3 les plus proches)
- [ ] Questions de relance générées en langage simple (niveau A2-B1)
- [ ] Tests avec 5 transcriptions simulées (mine, BTP, service, agriculture, commerce)

**Estimation** : 15h

---

#### S1-4 · Boucle conversationnelle vocale
**En tant que** Céline
**Je veux** que le système me pose des questions pour compléter mon inventaire
**Afin d'** avoir un inventaire plus complet sans effort de ma part

**Critères d'acceptation** :
- [ ] Le LLM génère 1-2 questions de relance après chaque tour
- [ ] Les questions sont converties en audio via Piper TTS
- [ ] L'audio est joué automatiquement dans le navigateur
- [ ] 2-3 tours de conversation maximum puis résumé final
- [ ] Le résumé est lu à voix haute pour confirmation

**Estimation** : 15h

---

#### S1-5 · Génération d'embeddings profil
**En tant que** le système
**Je veux** générer un vecteur d'embedding pour chaque profil complété
**Afin de** permettre le matching sémantique au Sprint 2

**Critères d'acceptation** :
- [ ] Service d'embedding (sentence-transformers, modèle multilingue)
- [ ] L'embedding est calculé à partir des compétences + expériences
- [ ] Stockage dans la colonne pgvector du profil
- [ ] Recalcul automatique si le profil est mis à jour

**Estimation** : 8h

---

#### S1-6 · Consentement oral
**En tant que** Céline
**Je veux** donner mon accord à voix haute avant que mes données soient enregistrées
**Afin que** mes droits RGPD soient respectés même si je ne sais pas lire

**Critères d'acceptation** :
- [ ] Le système lit la demande de consentement à voix haute (TTS)
- [ ] Céline répond "oui" ou "d'accord" → STT détecte l'approbation
- [ ] L'enregistrement audio du consentement est conservé comme preuve
- [ ] Horodatage et hash de l'audio stockés en base
- [ ] Si refus, aucune donnée n'est conservée
- [ ] Texte du consentement relu par un juriste (TODO Damien)

**Estimation** : 10h

---

**Total Sprint 1 : ~73h** (marge de 7h)

---

## Sprint 2 — Matching MVP (17 mars → 30 mars)

**But** : Didier cherche → trouve le profil anonymisé de Céline.

### Stories

#### S2-1 · Interface recherche recruteur
**En tant que** Didier
**Je veux** décrire mon besoin dans un champ libre et obtenir des profils
**Afin de** trouver quelqu'un qui correspond sans passer par un jobboard

**Critères d'acceptation** :
- [ ] Page recruteur avec textarea unique + bouton "Chercher"
- [ ] Option vocale (même bouton micro que Céline)
- [ ] Résultats affichés en cartes : score, compétences, zone, explication
- [ ] < 5 secondes pour les résultats
- [ ] Zéro donnée identifiante visible

**Estimation** : 15h

---

#### S2-2 · Endpoint matching sémantique
**En tant que** le système
**Je veux** recevoir un besoin recruteur et retourner les profils les plus pertinents
**Afin de** connecter l'offre et la demande

**Critères d'acceptation** :
- [ ] `POST /api/matching/search` — reçoit texte libre, retourne `ResultatMatching`
- [ ] Le LLM extrait les compétences du besoin → embedding
- [ ] Recherche pgvector (cosinus) sur les profils
- [ ] Re-ranking LLM avec explication en langage courant
- [ ] Anonymisation stricte en sortie (cf. `skills/matching.md`)
- [ ] Filtrage anti-discrimination : le matching ignore genre, âge, origine

**Estimation** : 18h

---

#### S2-3 · Seed de données simulées
**En tant que** développeur
**Je veux** 1000 profils simulés et 200 offres réalistes en base
**Afin de** tester le matching à une échelle crédible pour la démo

**Critères d'acceptation** :
- [ ] Script `scripts/seed.py` qui génère les données via LLM
- [ ] Profils variés : mine, BTP, service, agriculture, commerce, artisanat
- [ ] Distribution réaliste des zones (60% Grand Nouméa, 25% Nord, 15% Îles)
- [ ] Chaque profil a des compétences, expériences et un embedding
- [ ] 200 offres d'emploi couvrant les principaux secteurs NC
- [ ] 50 comptes recruteurs fictifs

**Estimation** : 12h

---

#### S2-4 · Mode hybride (Steeve)
**En tant que** Steeve
**Je veux** voir un résumé texte de mon inventaire vocal et pouvoir le corriger
**Afin de** vérifier et compléter ce que le système a compris

**Critères d'acceptation** :
- [ ] Après l'inventaire vocal, un écran "Résumé" affiche les compétences en texte
- [ ] Chaque compétence est éditable (champ pré-rempli, modifiable)
- [ ] Bouton "Ajouter une compétence" (texte libre)
- [ ] Bouton "Tout est bon" (valide et génère l'embedding)
- [ ] Ce mode est optionnel — Céline ne le voit pas en mode vocal pur

**Estimation** : 10h

---

#### S2-5 · Expression d'intérêt recruteur
**En tant que** Didier
**Je veux** indiquer que je suis intéressé par un profil
**Afin que** la mise en relation puisse se faire (via un médiateur)

**Critères d'acceptation** :
- [ ] Bouton "Je suis intéressé" sur chaque carte profil
- [ ] L'action est logguée en base (recruteur_id, profil_id, timestamp)
- [ ] Pas de contact direct : pour le POC, un médiateur voit la liste des intérêts
- [ ] Confirmation visuelle : "Votre intérêt a été enregistré"

**Estimation** : 5h

---

**Total Sprint 2 : ~60h** (marge de 20h — rattrapage Sprint 1 si besoin)

---

## Sprint 3 — Accompagnement + Badges (31 mars → 13 avril)

**But** : Nadia guide Céline, L'Écolo valide un badge.

### Stories

#### S3-1 · Mode accompagnement (duo aidant + usager)
**En tant que** Nadia
**Je veux** activer un mode qui me montre un guide pas-à-pas pendant que Céline utilise le vocal
**Afin de** l'accompagner sans prendre sa place

**Critères d'acceptation** :
- [ ] Toggle "Mode accompagnement" (icône deux personnes)
- [ ] Panneau latéral ou overlay avec instructions pour l'aidant
- [ ] L'aidant voit le texte transcrit et les compétences en cours d'extraction
- [ ] L'usager garde l'interface vocale simplifiée
- [ ] Guide aidant : 5-7 étapes avec conseils ("Laissez-la parler, ne répondez pas à sa place")

**Estimation** : 15h

---

#### S3-2 · Guide aidant (documentation)
**En tant que** Nadia
**Je veux** un guide papier/PDF que je peux imprimer pour mes sessions d'accompagnement
**Afin de** savoir comment utiliser l'outil avec le public

**Critères d'acceptation** :
- [ ] Document `docs/guide-aidant.md` (convertible en PDF)
- [ ] Étapes illustrées (captures d'écran annotées)
- [ ] Section "Ce qu'il faut dire / ne pas dire"
- [ ] FAQ : problèmes courants et solutions
- [ ] < 4 pages

**Estimation** : 6h

---

#### S3-3 · Émission de badges Open Badges v3
**En tant que** le système
**Je veux** générer un badge certifiant une compétence après l'inventaire vocal
**Afin de** donner une preuve vérifiable à Céline

**Critères d'acceptation** :
- [ ] Après validation de l'inventaire, badges générés (1 par compétence principale)
- [ ] Badge au format JSON-LD Open Badges v3 (cf. `skills/badges.md`)
- [ ] Signature Ed25519 avec clé du serveur
- [ ] Statut initial : `pending_endorsement` (en attente de recommandation)
- [ ] Stockage en base + endpoint `GET /api/badges/{id}`

**Estimation** : 12h

---

#### S3-4 · Workflow de recommandation tuteur
**En tant que** L'Écolo (tuteur)
**Je veux** recevoir un lien pour confirmer qu'une personne possède bien une compétence
**Afin de** renforcer la crédibilité du badge

**Critères d'acceptation** :
- [ ] Génération d'un lien unique (token) envoyable par email/SMS
- [ ] Page de recommandation : compétence + contexte anonymisé
- [ ] Boutons : "Je confirme" / "Je ne peux pas confirmer"
- [ ] Si confirmé → badge passe en statut `issued`
- [ ] L'endorsement est enregistré dans le badge JSON-LD

**Estimation** : 10h

---

#### S3-5 · Affichage des badges utilisateur
**En tant que** Clément
**Je veux** voir mes badges sur mon profil et pouvoir les télécharger
**Afin de** les partager ou les vérifier

**Critères d'acceptation** :
- [ ] Page profil avec liste des badges (icône + nom compétence + statut)
- [ ] Badge cliquable → détail avec date, recommandeur (anonymisé), score
- [ ] Bouton "Télécharger" → JSON-LD standard
- [ ] Endpoint vérification : `GET /api/badges/{id}/verify`

**Estimation** : 8h

---

**Total Sprint 3 : ~51h** (marge confortable de 29h — attendue car badges = nouveau terrain)

---

## Sprint 4 — Open Data + Données (14 avril → 27 avril)

**But** : Données calédoniennes réelles injectées, dashboard métiers en tension.

### Stories

#### S4-1 · Import Open Data NC (API)
**En tant que** Farid
**Je veux** que les données de data.gouv.nc soient importées en base
**Afin d'** alimenter les statistiques de métiers en tension

**Critères d'acceptation** :
- [ ] Script `scripts/import-opendata.py` fonctionnel
- [ ] Données sectorielles et démographiques importées
- [ ] Mapping vers codes ROME v4 quand applicable
- [ ] Idempotent (réexécutable sans doublons)
- [ ] Logs clairs en cas d'erreur

**Estimation** : 10h

---

#### S4-2 · Import CSV ISEE/DTEFP
**En tant que** Farid
**Je veux** importer les fichiers CSV de l'ISEE et du DTEFP
**Afin d'** avoir des données d'emploi réelles calédoniennes

**Critères d'acceptation** :
- [ ] Parsing robuste (encodage, séparateurs variés, colonnes manquantes)
- [ ] Nettoyage et normalisation automatique
- [ ] Stockage en tables `stats_emploi` et `secteurs_tension`
- [ ] Au moins 2 jeux de données importés avec succès

**Estimation** : 10h

---

#### S4-3 · API métiers en tension
**En tant que** Kevin (pour la démo)
**Je veux** un endpoint qui retourne les secteurs en tension par zone
**Afin de** montrer que le POC s'appuie sur des données réelles

**Critères d'acceptation** :
- [ ] `GET /api/opendata/tensions?zone=Province+Nord`
- [ ] Retourne les top 10 métiers en tension avec ratio offres/demandeurs
- [ ] Filtrable par zone (Province Sud, Province Nord, Îles Loyauté)
- [ ] Données sourcées et datées

**Estimation** : 6h

---

#### S4-4 · Dashboard données (vue simple)
**En tant que** Marie
**Je veux** une page web avec les statistiques clés de l'emploi en NC
**Afin de** valider l'utilité de l'outil pour les institutions

**Critères d'acceptation** :
- [ ] Page `/dashboard` avec 3-4 indicateurs visuels
- [ ] Graphique : top 5 métiers en tension par province
- [ ] Chiffre : nombre de profils, nombre de matchings réalisés
- [ ] Source et date des données affichées
- [ ] Responsive (lisible sur tablette pour les réunions)

**Estimation** : 10h

---

**Total Sprint 4 : ~36h** (marge de 44h — sprint plus léger volontairement, sert de buffer)

---

## Sprint 5 — Intégration & Souveraineté (28 avril → 11 mai)

**But** : Tout est connecté de bout en bout, la souveraineté est documentée.

### Stories

#### S5-1 · Parcours intégré de bout en bout
**En tant que** Kevin
**Je veux** que le parcours Céline → inventaire → badge → matching Didier fonctionne sans interruption
**Afin de** dérouler la démo sans accroc

**Critères d'acceptation** :
- [ ] Test end-to-end : inventaire vocal → profil créé → embedding calculé → matching fonctionne
- [ ] Pas de step manuelle entre les étapes
- [ ] Temps total du parcours Céline < 5 minutes
- [ ] Temps total du parcours Didier < 2 minutes

**Estimation** : 15h

---

#### S5-2 · Document d'architecture souveraineté (1 page)
**En tant que** Kevin
**Je veux** un document d'une page prouvant la souveraineté de l'architecture
**Afin de** rassurer les financeurs et partenaires institutionnels

**Critères d'acceptation** :
- [ ] `docs/architecture.md` — 1 page max
- [ ] Schéma montrant : données → serveur NC → pas de sortie vers l'étranger
- [ ] Liste des composants et leur localisation (tout local)
- [ ] Mention de la conformité RGPD
- [ ] Mention du consentement oral
- [ ] Validé par Damien

**Estimation** : 4h

---

#### S5-3 · Sécurisation et anonymisation audit
**En tant que** Marie
**Je veux** vérifier que l'anonymisation fonctionne correctement partout
**Afin de** m'assurer qu'aucune donnée personnelle ne fuit

**Critères d'acceptation** :
- [ ] Audit de tous les endpoints : aucun ne retourne de données identifiantes aux recruteurs
- [ ] Test : créer un profil avec nom/prénom → vérifier qu'ils n'apparaissent nulle part côté recruteur
- [ ] Les logs ne contiennent pas de données personnelles
- [ ] Le consentement est vérifié avant chaque accès aux données d'un profil

**Estimation** : 10h

---

#### S5-4 · Documentation API
**En tant que** Clément
**Je veux** une documentation API auto-générée et à jour
**Afin de** pouvoir comprendre et contribuer au projet

**Critères d'acceptation** :
- [ ] Swagger/OpenAPI accessible à `/docs`
- [ ] Tous les endpoints documentés (description, paramètres, exemples)
- [ ] Schémas Pydantic visibles dans la doc
- [ ] `docs/api.md` avec guide de démarrage rapide

**Estimation** : 6h

---

#### S5-5 · Tests de charge basiques
**En tant que** développeur
**Je veux** vérifier que le système tient avec les 1000 profils simulés
**Afin d'** éviter les surprises pendant la démo

**Critères d'acceptation** :
- [ ] Matching sur 1000 profils < 5 secondes
- [ ] STT + LLM pipeline < 10 secondes pour 30s d'audio
- [ ] 5 utilisateurs simultanés ne font pas tomber le système
- [ ] Résultats documentés dans `docs/benchmarks.md`

**Estimation** : 8h

---

**Total Sprint 5 : ~43h** (marge de 37h — sprint réaliste avant la démo)

---

## Sprint 6 — Démo & Polish (12 mai → 25 mai)

**But** : Tout est prêt pour la démonstration du 25 mai.

### Stories

#### S6-1 · Scénario de démo (10 minutes)
**En tant que** Kevin
**Je veux** un scénario de démonstration détaillé et répétable
**Afin de** présenter le POC de manière convaincante à des non-techniciens

**Critères d'acceptation** :
- [ ] `docs/demo-scenario.md` avec script minute par minute
- [ ] Séquence : contexte (1 min) → Céline parle (3 min) → badge émis (1 min) → Didier cherche (2 min) → dashboard (1 min) → souveraineté (1 min) → conclusion (1 min)
- [ ] Données de démo préchargées et fiables
- [ ] Plan B si le réseau est lent (données en cache)
- [ ] Répété au moins 2 fois par l'équipe

**Estimation** : 10h

---

#### S6-2 · Bug fixes & polish UI
**En tant que** utilisateur
**Je veux** que l'interface soit fluide et sans bugs bloquants
**Afin de** ne pas être gêné pendant l'utilisation

**Critères d'acceptation** :
- [ ] Tous les bugs critiques (P0) sont résolus
- [ ] Interface testée sur Chrome Android (téléphone bas de gamme)
- [ ] Animations et transitions fluides
- [ ] Messages d'erreur clairs (visuels, pas uniquement texte)
- [ ] Pas de console errors

**Estimation** : 20h

---

#### S6-3 · Documentation open source
**En tant que** Clément
**Je veux** un README complet et un CONTRIBUTING guide
**Afin de** pouvoir reproduire et contribuer au projet

**Critères d'acceptation** :
- [ ] README.md : description, setup, usage, architecture, licence
- [ ] CONTRIBUTING.md : comment contribuer, conventions, process de PR
- [ ] LICENSE : PolyForm Noncommercial 1.0.0
- [ ] `make` commandes documentées
- [ ] Code source commenté sur les parties complexes (pipeline LLM, matching)

**Estimation** : 8h

---

#### S6-4 · Mise en production serveur NC
**En tant que** développeur
**Je veux** déployer le POC sur le serveur NC avec Docker
**Afin que** la démo tourne sur l'infrastructure souveraine

**Critères d'acceptation** :
- [ ] Docker Compose de production (sans hot-reload, avec volumes persistants)
- [ ] HTTPS configuré (Let's Encrypt ou certificat auto-signé)
- [ ] Backup de la base de données automatisé
- [ ] Monitoring basique (logs centralisés, uptime check)
- [ ] URL accessible pour la démo

**Estimation** : 12h

---

**Total Sprint 6 : ~50h** (marge de 30h — buffer critique pour imprévus démo)

---

## Récapitulatif de la vélocité

| Sprint | Estimé (h) | Capacité (h) | Marge | Risque |
|---|---|---|---|---|
| S0 | 60 | 80 | 20h | 🟢 Faible |
| S1 | 73 | 80 | 7h | 🟠 Moyen (STT/LLM intégration) |
| S2 | 60 | 80 | 20h | 🟢 Faible |
| S3 | 51 | 80 | 29h | 🟢 Faible |
| S4 | 36 | 80 | 44h | 🟢 Buffer intentionnel |
| S5 | 43 | 80 | 37h | 🟢 Faible |
| S6 | 50 | 80 | 30h | 🟡 Démo = stress |
| **Total** | **373** | **560** | **187h** | Marge globale 33% |

> **La marge de 33% est intentionnelle.** Sur un projet en 10h/semaine en parallèle d'autres activités, les imprévus sont la norme : absences, bugs infra, dépendances externes (données NC). La marge sera absorbée naturellement.

---

## Risques identifiés

| Risque | Impact | Mitigation |
|---|---|---|
| Whisper/LLM ne tourne pas sur H100 | 🔴 Bloquant | Spike Sprint 0, fallback sur modèles plus petits |
| Données ISEE/DTEFP indisponibles ou inutilisables | 🟠 Moyen | Données simulées en fallback |
| Disponibilité réelle <10h/semaine | 🟠 Moyen | Sprints 4-5 servent de buffer |
| Qualité STT en français calédonien | 🟡 Faible | Accent pas trop éloigné du français standard, fine-tuning possible post-POC |
| Complexité Open Badges v3 | 🟡 Faible | Implémentation minimale, pas de wallet décentralisé |
