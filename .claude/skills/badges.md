# Skill : Infrastructure Open Badges v3

> **Priorité** : 🟡 IMPORTANTE — Nécessaire pour la démo mais moins critique que vocal + matching.

## Contexte

Le POC doit pouvoir émettre des badges certifiant les compétences, avec un mécanisme de recommandation par un tuteur (persona « L'Écolo »). Clément (étudiant) veut aussi des badges pour valoriser ses compétences Data/IA.

## Standard Open Badges v3

Open Badges v3 (1EdTech, anciennement IMS Global) utilise des **Verifiable Credentials** (W3C). Un badge est un JSON-LD signé.

### Structure minimale pour le POC

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://purl.imsglobal.org/spec/ob/v3p0/context-3.0.3.json"
  ],
  "type": ["VerifiableCredential", "OpenBadgeCredential"],
  "issuer": {
    "id": "https://kompetens.nc/issuer",
    "type": "Profile",
    "name": "Kompetens POC — Open NC"
  },
  "validFrom": "2026-05-01T00:00:00Z",
  "credentialSubject": {
    "type": "AchievementSubject",
    "achievement": {
      "id": "https://kompetens.nc/badges/conduite-engins",
      "type": "Achievement",
      "name": "Conduite d'engins de chantier",
      "description": "Compétence validée par inventaire vocal et recommandation tuteur",
      "criteria": {
        "narrative": "Déclaration vocale + recommandation par un tiers de confiance"
      }
    }
  }
}
```

### Ce qu'on implémente pour le POC

| Fonctionnalité | Statut POC |
|---|---|
| Émission de badges JSON-LD | ✅ Implémenté |
| Signature cryptographique (Ed25519) | ✅ Implémenté (clé serveur) |
| Recommandation tuteur | ✅ Implémenté (workflow simplifié) |
| Vérification de badge | ✅ Endpoint de vérification basique |
| Wallet utilisateur | ⚠️ Stockage serveur simple (pas de wallet décentralisé) |
| Gouvernance des certificateurs | ❌ Hors périmètre POC |
| Révocation | ❌ Hors périmètre POC |

### Workflow de recommandation (POC)

```
1. Céline complète son inventaire vocal
   → Compétences identifiées (ex: "Conduite dumper")

2. Le système génère un badge EN ATTENTE
   → Statut : "pending_endorsement"

3. L'Écolo (tuteur) reçoit une notification
   → Voit : compétence + contexte anonymisé
   → Action : "Je confirme" / "Je ne peux pas confirmer"

4. Si confirmé → badge signé et émis
   → Statut : "issued"
   → Le badge contient la référence au tuteur (anonymisée)
```

### Schéma base de données

```python
class Badge(BaseModel):
    id: UUID
    recipient_id: UUID           # Lien vers profil (anonymisé en sortie)
    achievement_code: str        # Code ROME ou identifiant compétence
    achievement_name: str        # "Conduite d'engins de chantier"
    status: str                  # "pending_endorsement", "issued", "rejected"
    issued_at: Optional[datetime]
    endorser_id: Optional[UUID]  # Le tuteur qui recommande
    credential_json: Optional[dict]  # Le JSON-LD signé final
    signature: Optional[str]     # Signature Ed25519

class Endorsement(BaseModel):
    id: UUID
    badge_id: UUID
    endorser_id: UUID
    decision: str                # "confirmed", "declined"
    comment: Optional[str]       # Commentaire libre du tuteur
    decided_at: datetime
```

## Règles de conception

- **Pas de blockchain** : On signe avec une clé Ed25519 côté serveur. Simple, vérifiable, souverain.
- **Pas de wallet externe** : Les badges sont stockés en base et exportables en JSON-LD.
- **Tuteur = humain identifié** : Pour le POC, le tuteur s'authentifie par un lien unique (token + email/téléphone). Pas de système de comptes complexe.
- **Un badge = une compétence** : Pas de badges composites pour le POC.

## Tests critiques

1. **Test émission** : L'inventaire vocal de Céline génère au moins 1 badge en attente
2. **Test recommandation** : L'Écolo peut confirmer un badge via le lien de recommandation
3. **Test signature** : Le JSON-LD émis est un Verifiable Credential valide (validation JSON Schema)
4. **Test export** : Clément peut télécharger son badge au format JSON-LD standard
