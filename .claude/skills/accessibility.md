# Skill : Accessibilité & bas débit

> **Priorité** : 🔴 CRITIQUE — Transversal à TOUTE fonctionnalité. Pas une couche ajoutée après coup.

## Contexte

La Nouvelle-Calédonie a une connectivité très inégale : fibre à Nouméa, 3G instable en brousse, zones blanches en tribu. Le public cible inclut des personnes en situation d'illettrisme. L'accessibilité n'est pas un nice-to-have, c'est la raison d'être du projet.

## Contraintes réseau

### Profils de connexion à tester

| Profil | Débit descendant | Latence | Persona |
|---|---|---|---|
| **Fibre Nouméa** | 100 Mbps | 20ms | Didier, Marie |
| **4G correcte** | 10 Mbps | 50ms | Nadia |
| **3G brousse** | 384 kbps | 500ms | Céline, Steeve |
| **3G dégradée** | 128 kbps | 1000ms | L'Écolo |

### Règles techniques

- **Budget taille page initiale** : < 200 Ko (HTML + CSS + JS critique). Le reste en lazy loading.
- **Service Worker** : Mettre en cache les assets statiques et l'UI shell pour un affichage instantané même hors-ligne.
- **Audio streaming** : Chunks de 2s, codec Opus (compact). Ne PAS attendre la fin de l'enregistrement pour envoyer.
- **Images** : Format WebP, taille max 50 Ko par image, lazy loading systématique.
- **Pas de CDN externe** : Tous les assets critiques sont servis depuis le serveur NC.
- **Feedback réseau** : Indicateur visible de l'état de connexion. Si dégradé, informer l'utilisateur avec une icône (pas de texte).
- **Compression** : Gzip/Brotli activé sur le serveur.

### Mode dégradé (hors-ligne partiel)

Pour le POC, le mode hors-ligne complet est hors périmètre, MAIS :
- L'UI shell doit s'afficher même sans connexion (Service Worker)
- Un message vocal/visuel explique qu'il faut une connexion pour utiliser le service
- Les données déjà chargées restent affichables

## Accessibilité illettrisme

### Principes d'interface

1. **Navigation par icônes** : Chaque action a une icône explicite + texte pour les voyants. Le texte n'est JAMAIS le seul moyen de comprendre l'action.
2. **Code couleur cohérent** :
   - 🟢 Vert = positif / valider / continuer
   - 🔴 Rouge = annuler / supprimer / problème
   - 🔵 Bleu = information / aide
3. **Boutons larges** : Zone de touch minimum 48x48px (recommandation WCAG), idéalement 64x64px pour les actions principales.
4. **Pas de formulaire textuel** en mode vocal. Le seul input est le micro.
5. **Feedback sonore** : Chaque action produit un retour audio (bip de confirmation, voix de synthèse pour les résultats).
6. **Progression visuelle** : Étapes du parcours représentées par des icônes / cercles, pas par du texte.

### Composants UI requis

```
<VocalButton />       — Gros bouton micro, push-to-talk
<AudioPlayer />       — Lecture des réponses TTS avec contrôles simples
<StepIndicator />     — Progression visuelle (cercles/icônes)
<ConnectionStatus />  — Indicateur réseau (icône, pas texte)
<IconAction />        — Bouton avec icône + label optionnel
<ConfirmDialog />     — Dialogue de confirmation vocal + visuel
```

### Parcours vocal — zéro lecture requise

```
Écran d'accueil
│  [Icône micro + animation "pulse"]
│  TTS : "Bonjour, bienvenue. Appuyez sur le bouton pour commencer."
│
▼ Appui sur le bouton
│  TTS : "Racontez-moi ce que vous savez faire dans votre travail."
│  [Enregistrement en cours — animation visuelle]
│
▼ Fin d'enregistrement (relâche ou silence 3s)
│  [Animation de traitement]
│  TTS : "J'ai compris que vous savez conduire un dumper.
│         Est-ce que vous faisiez aussi autre chose ?"
│
▼ Boucle de conversation (2-3 tours max)
│
▼ Résumé vocal
│  TTS : "Voici ce que j'ai retenu : [liste des compétences].
│         Appuyez sur le bouton vert si c'est correct,
│         ou le bouton bleu pour modifier."
│
▼ Confirmation
│  Badge(s) généré(s) → feedback sonore de succès
```

## Mode accompagnement (Nadia)

Quand l'aidant utilise l'outil avec l'usager :

- **Vue duale** : L'aidant voit un écran enrichi (texte + données structurées) pendant que l'usager voit l'interface vocale simplifiée.
- **Pas de prise de contrôle** : L'aidant guide mais c'est l'usager qui parle et valide.
- **Guide aidant** : Instructions pas-à-pas affichées à l'aidant (overlay ou panneau latéral).
- **Activation** : Toggle "Mode accompagnement" dans les paramètres (icône de deux personnes).

## Tests d'accessibilité

1. **Test 3G** : Utiliser Chrome DevTools Network Throttling (384 kbps, 500ms latence) — la page doit se charger en <5s et le vocal fonctionner
2. **Test zéro lecture** : Un testeur ferme les yeux et utilise le parcours uniquement à l'oreille + au toucher. Doit pouvoir compléter l'inventaire.
3. **Test boutons** : Tous les boutons interactifs font au minimum 48x48px
4. **Test offline** : Couper le réseau après chargement initial → l'UI shell reste affichée
5. **Test contraste** : Ratio de contraste WCAG AA (4.5:1) minimum sur tous les textes
