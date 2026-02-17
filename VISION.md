# VISION.md — Kompetens

> Ce document est la fondation conceptuelle du projet. Il précède et oriente toute décision technique.
> Il doit être lu avant le CLAUDE.md.

---

## En une phrase

**Kompetens rend visible ce qui existe déjà — les savoir-faire des gens, dans leurs propres mots — et leur donne le pouvoir de choisir ce qu'ils en font.**

**C'est un démonstrateur technologique souverain, open source et reproductible, construit depuis la Nouvelle-Calédonie pour prouver qu'une autre façon de reconnaître les compétences est possible.**

---

## Le diagnostic — 3 fractures

### 1. La fracture de la preuve

Les compétences existent. Céline conduit un dumper depuis 3 ans. Mais elle ne peut pas le prouver : pas de diplôme, pas de CV, pas de LinkedIn. Le système actuel exige de l'écrit pour attester un savoir-faire. Si tu ne sais pas écrire, tu n'existes pas professionnellement.

Le problème est aggravé par le fait que les cadres de reconnaissance — le diplôme, le CV, le vocabulaire RH — sont des cadres importés, conçus pour des parcours qui ne sont pas ceux de la Nouvelle-Calédonie. Beaucoup de compétences réelles et pratiquées au quotidien ne rentrent dans aucune case parce qu'aucun référentiel n'a été conçu pour les capturer.

Et le plus insidieux : à force de ne pas être reconnus, les gens finissent par croire eux-mêmes qu'ils n'ont rien à offrir. « Moi je sais rien faire, je conduis juste le dumper. » C'est l'auto-sabordage — la conviction intériorisée que ses propres compétences ne comptent pas.

### 2. La fracture de la rencontre

Didier, patron de PME BTP, cherche désespérément quelqu'un. Céline cherche désespérément du travail. Ils sont peut-être à 15 km l'un de l'autre. Mais aucun canal ne les relie.

Les outils existants (jobboards, DEL) parlent un langage que ni Céline ni Didier ne maîtrisent : le jargon RH. L'une ne sait pas se décrire dans les termes attendus. L'autre ne sait pas chercher avec les bons mots-clés. Le pont manque — et ce pont ne peut pas être un formulaire à remplir.

### 3. La fracture de la confiance

Même si Céline peut prouver ses compétences et que Didier peut la trouver, il reste un vide : pourquoi Didier croirait-il un profil généré par une machine ? Et pourquoi Céline confierait-elle ses données à un outil numérique ?

Il manque un tiers humain. Quelqu'un qui dit à Didier « oui, je la connais, elle sait faire ça ». Quelqu'un qui dit à Céline « viens, on fait ça ensemble, c'est safe ». Sans ce maillage humain, l'outil reste un outil. Avec, il devient un écosystème.

---

## La réponse — 6 briques conceptuelles

### A. La voix comme CV

L'interface vocale n'est pas un choix d'accessibilité. C'est un choix politique.

La voix permet à quelqu'un de se décrire dans ses propres mots, sans passer par un filtre qui n'a pas été fait pour lui. Le système écoute, comprend, et structure — mais il ne force jamais l'utilisateur à entrer dans une catégorie préétablie.

L'inventaire vocal fait plus que transcrire : il **explicite l'implicite**. Quand Céline dit « je conduis le dumper sur la mine », le système infère et nomme ce qu'elle ne sait pas qu'elle sait : lecture de terrain, gestion du risque, coordination d'équipe en conditions extrêmes. C'est un acte de **valorisation active**, pas de classification passive.

### B. Le référentiel émergent

**C'est la brique la plus différenciante du projet.**

On ne part pas d'un référentiel tout fait (ROME, RNCP, O*NET) pour classer les gens dedans. On fait l'inverse :

1. On collecte les offres d'emploi réelles de Nouvelle-Calédonie — sites d'emploi, données DTEFP/DEL, annonces informelles (Facebook, bouche à oreille)
2. Un LLM en extrait les compétences demandées, dans les mots des employeurs locaux
3. Ces compétences s'agrègent progressivement en une **taxonomie émergente** — un référentiel qui naît du terrain

Ce référentiel n'est pas figé. Il reflète ce que le territoire demande réellement, pas ce qu'une grille nationale prédit qu'il devrait demander.

Le ROME v4 reste en arrière-plan pour l'interopérabilité (pouvoir communiquer avec les institutions nationales) et la comparaison (identifier les écarts entre ce que le ROME prévoit et ce que le terrain montre). Mais il n'est plus le cadre de référence — c'est le territoire qui l'est.

**Pourquoi c'est important :** Importer un référentiel, c'est importer une vision du travail. Un référentiel émergent dit : les compétences qui comptent ici sont celles que les gens d'ici demandent et pratiquent. C'est un acte de souveraineté intellectuelle.

### C. Le langage naturel comme pont

Le matching ne repose pas sur des mots-clés ou des codes. Il repose sur le sens.

Didier dit « je cherche un gars sérieux qui sait conduire un dumper et qui a pas peur de se lever tôt ». Le système comprend : compétences en conduite d'engins, fiabilité, disponibilité horaire. Et il trouve Céline.

Le langage naturel est le seul pont possible entre deux personnes qui ne parlent pas le même vocabulaire professionnel. Le jargon RH est une barrière, pas une aide. L'outil le supprime.

### D. L'intelligence territoriale

Le pipeline de données NC n'est pas un accessoire technique. C'est ce qui donne au projet son ancrage.

Quand l'outil montre qu'il y a 3 fois plus d'offres que de candidats en conduite d'engins dans le Nord, il dit quelque chose sur le pays. Quand il révèle que les compétences les plus demandées à Koné ne sont pas les mêmes qu'à Nouméa, il produit une connaissance qui n'existait pas.

L'outil n'est pas seulement utile à Céline et Didier. Il est utile à Marie (la cadre institutionnelle) qui a besoin de données fiables pour piloter des politiques publiques. Et à Kevin (le facilitateur) qui a besoin de chiffres pour convaincre un élu.

### E. Le maillage humain comme infrastructure

La technologie seule ne résout rien si personne n'accompagne Céline jusqu'à l'outil. Le projet assume que l'humain est une composante de l'architecture, pas un utilisateur passif.

Trois rôles humains sont intégrés dans le design :
- **L'aidant** (Nadia) : accompagne l'usager dans l'utilisation de l'outil, sans prendre sa place
- **Le tuteur** (L'Écolo) : confirme les compétences, crée de la confiance par la recommandation
- **Le médiateur** : facilite la mise en relation entre profil et recruteur (pas de contact direct)

Le mode accompagnement est conçu pour que l'aidant guide sans faire à la place. L'usager parle, l'usager valide, l'usager choisit. L'aidant est un facilitateur, pas un intermédiaire.

### F. La souveraineté comme fondation

La souveraineté n'est pas une contrainte technique. C'est une condition de la confiance.

Souveraineté des données : tout reste en Nouvelle-Calédonie. Aucun appel vers des serveurs étrangers. Souveraineté des modèles : LLM et STT locaux, open source.

Mais aussi souveraineté des personnes : le profil appartient à l'utilisateur. Il décide ce qu'il montre, à qui, et pour combien de temps. Le consentement est oral (parce que l'écrit exclut). L'anonymisation est par défaut (parce que la confiance se construit).

---

## Le principe d'émancipation — transversal

L'émancipation n'est pas une fonctionnalité. C'est la posture du projet. Elle traverse chaque brique.

### Couche 1 — Décoloniser la reconnaissance

Le système accepte les compétences telles qu'elles sont exprimées, dans les mots de la personne et dans les mots du territoire. Le référentiel émerge du terrain, il n'est pas importé.

### Couche 2 — Expliciter l'implicite

Le LLM ne se contente pas de transcrire. Il nomme ce que la personne ne sait pas qu'elle sait. Il valorise activement, il ne classe pas passivement.

### Couche 3 — Redonner le contrôle

Le profil appartient à la personne. Le badge est sa propriété. Elle valide, elle modifie, elle masque. L'outil est un miroir qu'elle oriente, pas un système qui la catégorise.

### Couche 4 — Restaurer la dignité

Le ton, le design, le vocabulaire ne traitent jamais l'utilisateur comme un déficit. Pas de score d'employabilité. Pas de jargon d'insertion. L'outil dit : tu as des savoir-faire, ils ont de la valeur, voici qui en a besoin.

**Critère transversal de « Done »** : si une fonctionnalité infantilise, classe, ou réduit l'utilisateur à un profil déficient, elle est rejetée — au même titre qu'une fonctionnalité inaccessible à Céline.

---

## La posture open source — reproductibilité

Ce qui est construit pour la Nouvelle-Calédonie doit pouvoir être repris par n'importe quel territoire isolé : une île du Pacifique, un département rural français, un pays d'Afrique francophone.

La souveraineté n'est pas défensive (« nos données restent chez nous »). Elle est générative (« notre code part chez vous »).

L'open source n'est pas un choix technique. C'est un choix éthique : les outils d'émancipation ne doivent pas être la propriété de ceux qui les construisent.

---

## Schéma conceptuel

```
┌──────────────────────────────────────────────────────────────┐
│                         VISION                                │
│                                                               │
│  "Rendre visible ce qui existe déjà — dans les mots des      │
│   gens et du territoire — et leur donner le pouvoir de        │
│   choisir ce qu'ils en font."                                 │
│                                                               │
├───────────────────────┬──────────────────────────────────────┤
│                       │                                       │
│  FRACTURES            │  BRIQUES                              │
│  (le problème)        │  (la réponse)                         │
│                       │                                       │
│  1. Fracture de       │  A. La voix comme CV                  │
│     la preuve         │     → explicitation de l'implicite    │
│                       │  B. Le référentiel émergent           │
│                       │     → inféré du territoire, pas       │
│                       │       importé d'ailleurs              │
│                       │                                       │
│  2. Fracture de       │  C. Le langage naturel comme pont     │
│     la rencontre      │     → ni jargon RH, ni mots-clés     │
│                       │  D. L'intelligence territoriale       │
│                       │     → données NC, métiers en tension  │
│                       │                                       │
│  3. Fracture de       │  E. Le maillage humain                │
│                       │     → aidant, tuteur, médiateur       │
│     la confiance      │  F. La souveraineté                   │
│                       │     → données, modèles, personnes     │
│                       │                                       │
├───────────────────────┴──────────────────────────────────────┤
│                                                               │
│  ÉMANCIPATION (principe transversal)                          │
│                                                               │
│  Décoloniser la    Expliciter     Redonner le    Restaurer   │
│  reconnaissance    l'implicite    contrôle       la dignité   │
│                                                               │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  REPRODUCTIBILITÉ (posture)                                   │
│                                                               │
│  Open source · Souverain · Reproductible · Adaptable         │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Ce que le projet N'EST PAS

- Ce n'est pas un jobboard vocal
- Ce n'est pas un LinkedIn calédonien
- Ce n'est pas un outil d'insertion qui classe les gens par employabilité
- Ce n'est pas une importation de grilles métropolitaines avec une interface vocale par-dessus
- Ce n'est pas un produit fini — c'est un démonstrateur qui prouve qu'une autre voie est possible

---

## Horizon

Le POC de mai 2026 prouve la faisabilité. Il montre que :
1. Une personne peut décrire ses compétences par la voix et obtenir un inventaire structuré
2. Un référentiel de compétences peut émerger des offres d'emploi du territoire
3. Un employeur peut trouver un profil pertinent en langage courant
4. Le maillage humain (aidant + tuteur) s'intègre dans l'outil
5. Tout ça fonctionne sur un serveur souverain, en open source, sans dépendance étrangère

Ce qui vient après — intégration institutionnelle, recherche sur la réidentification, mode hors-ligne, langues kanak — dépend de ce que le POC prouve.
