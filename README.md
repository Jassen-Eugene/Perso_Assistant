# Assistant Personnel Intelligent (API)

**Statut du projet : EN COURS DE DÉVELOPPEMENT**

---

## Objectif du projet

Ce projet vise à créer un **assistant personnel intelligent** capable d'aider son utilisateur dans ses tâches quotidiennes, tout en offrant des fonctionnalités ludiques et interactives.

L'assistant est conçu pour :

- Reconnaitre la **voix** de son utilisateur et converser naturellement avec lui.
- Lire et identifier une **musique** dans une phrase, puis la jouer automatiquement.
- Générer des **images** à partir de descriptions textuelles.
- Donner des **informations pratiques** comme l’heure, la météo, l’agenda ou un itinéraire.
- Échanger sur des **sujets personnels**, dans un style conversationnel naturel.

Le projet utilise des modèles de langage (LLM), la reconnaissance vocale, la génération d'image et l'analyse audio pour offrir une expérience complète.

---

## Fonctionnalités prévues / en cours

### 🎙️ Interaction vocale
- Enregistrement de la voix et transcription automatique (`record.py`, `speech_to_text.py`)
- Synthèse vocale pour répondre à l'utilisateur (`read_response.py`, `output.wav`)
- Détection des locuteurs (`detect.py`, `detect_locutor.py`)

### Organisation & Productivité
- Gestion d'agenda : ajout et consultation d'événements (`agenda.py`)
- Alarmes programmables (`alarme.py`, `agenda_alarm.py`)
- Rappels vocaux enregistrés avec stockage JSON (`rappel.py`, `rappels.json`)

### Services utiles
- Heure locale (`heure.py`)
- Météo actuelle (`meteo.py`)
- Itinéraires avec génération de cartes (`itineraire.py`, `itineraire.png`)

### Divertissement
- Lecture de musiques depuis un répertoire (`musics.py`, `voice_me`)
- Génération d’images à partir de requêtes texte (Stable Diffusion, `image.py`)
- Lecture des actualités / news (`news.py`)

### Intelligence & mémoire
- Historique des conversations pour personnalisation (`conversation_history.json`)
- Prise en conte de la nature des demandes de l'utilisateur (`model.py`)
- Réponses contextuelles basées sur la mémoire (`model_memoire.py`)
- Réponses longues avec support d’outils externes (`model_long.py`)

### Expérimentation & test
- Fichiers audio pour l'intéraction entre le modèle et l'utilisateur (`jassen.wav`, `enregistrement_silence.wav`)
- Modèle de décision principal pour piloter les actions (`decision.py`)

---

## Lancement du programme

### 1. Pré-requis

Assurez-vous d’avoir :

- Python 3.10+
- Un environnement virtuel activé (recommandé)
- Un **microphone** fonctionnel (obligatoire pour l’entrée vocale)
- Des **clés API valides** pour les services (ex: OpenAI, Groq, etc.)

### 2. Installation des dépendances

Dans votre terminal :

```bash
pip install -r requirements.txt
```

### 3. Lancer l'assistant

```bash
python decision.py
```

L’assistant écoutera votre voix, analysera vos demandes, et exécutera la tâche correspondante automatiquement.

---

## Notes

- Le système est actuellement en phase de test. Certaines fonctions peuvent ne pas être totalement stables.

---



