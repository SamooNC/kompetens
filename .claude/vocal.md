# Skill : Inventaire de compétences vocal

> **Priorité** : 🔴 CRITIQUE — C'est l'objectif n°1 du POC. Si ça ne marche pas, le projet échoue.

## Contexte

Céline (25 ans, illettrée, conductrice de dumper) doit pouvoir décrire ses expériences professionnelles **par la voix** et obtenir un inventaire structuré de compétences mappé sur le ROME v4, sans jamais avoir à lire ou écrire.

## Pipeline technique

```
Micro utilisateur (PWA)
    │
    ▼ WebSocket (streaming audio chunks)
┌──────────────┐
│  Whisper      │  STT : audio → texte français
│  large-v3     │  (local, H100)
└──────┬───────┘
       │ texte brut
       ▼
┌──────────────────┐
│  LLM (Mistral)   │  Extraction structurée :
│  via vLLM         │  - Expériences identifiées
│                   │  - Compétences inférées
│                   │  - Mapping codes ROME v4
└──────┬───────────┘
       │ JSON structuré
       ▼
┌──────────────────┐
│  Conversation de  │  Le LLM pose des questions de relance
│  relance          │  pour affiner/compléter ("Tu as dit que
│                   │  tu conduisais un dumper. Tu faisais
│                   │  aussi l'entretien de l'engin ?")
└──────┬───────────┘
       │
       ▼ TTS (Piper) → audio réponse
┌──────────────────┐
│  Inventaire       │  Document structuré final :
│  structuré        │  compétences + niveaux + codes ROME
└──────────────────┘
```

## Règles de conception

### Audio
- **Format d'entrée** : WebM/Opus (natif navigateur) ou WAV 16kHz mono en fallback
- **Streaming** : Envoyer les chunks audio toutes les ~2 secondes via WebSocket pour feedback rapide
- **Silence detection** : Couper l'enregistrement après 3 secondes de silence (VAD côté client)
- **Taille max** : Limiter à 2 minutes par segment (relancer l'enregistrement ensuite)

### Prompting LLM pour extraction
- Le prompt système doit :
  1. Expliquer qu'il reçoit la transcription d'une personne qui décrit son parcours professionnel
  2. Extraire les **expériences** (poste, lieu, durée estimée)
  3. Inférer les **compétences** associées (y compris les compétences implicites — ex : conduire un dumper implique « lecture de terrain », « respect consignes sécurité »)
  4. Mapper sur les codes ROME v4 les plus proches
  5. Formuler 1-2 questions de relance en **langage simple** (niveau A2-B1 français)
- Le prompt NE doit JAMAIS utiliser de jargon RH dans les questions posées à l'utilisateur
- Format de sortie : JSON strict avec schéma Pydantic validé

### Mode hybride (Steeve)
- Si l'utilisateur préfère, il peut voir un résumé texte et corriger manuellement
- Les champs texte sont **pré-remplis** par le LLM à partir du vocal
- Jamais de champ texte vide à remplir from scratch

### UX vocale
- **Feedback constant** : indicateur visuel quand le système écoute / traite / parle
- **Gros bouton unique** : appuyer = parler, relâcher = envoyer (push-to-talk)
- **Pas de menu texte** : la navigation se fait par la voix ou par des boutons iconographiques
- **Confirmation vocale** : le système relit le résumé à voix haute avant validation

## Schéma Pydantic de sortie

```python
from pydantic import BaseModel
from typing import Optional

class Competence(BaseModel):
    label: str                    # "Conduite d'engins de chantier"
    code_rome: Optional[str]      # "F1302"
    niveau: str                   # "pratiqué", "maîtrisé", "expert"
    source: str                   # "déclaré" ou "inféré"

class Experience(BaseModel):
    intitule: str                 # "Conductrice de dumper"
    contexte: Optional[str]       # "Mine de nickel, Thio"
    duree_estimee: Optional[str]  # "3 ans"
    competences: list[Competence]

class InventaireVocal(BaseModel):
    experiences: list[Experience]
    questions_relance: list[str]  # Questions pour affiner
    resume_oral: str              # Texte à lire par TTS pour confirmation
    confiance_globale: float      # 0-1, confiance du mapping
```

## Tests critiques

1. **Test Céline** : Enregistrement audio simulé (3 phrases simples sur le dumper) → doit produire un inventaire avec au moins 3 compétences pertinentes
2. **Test bruit** : Audio avec bruit de fond (chantier) → Whisper doit quand même transcrire correctement 80%+
3. **Test relance** : Le LLM doit poser une question pertinente et en langage simple
4. **Test 3G** : Le streaming audio doit fonctionner avec 500ms de latence et 384kbps de bande passante
5. **Test mode hybride** : Steeve voit un résumé éditable pré-rempli après avoir parlé
