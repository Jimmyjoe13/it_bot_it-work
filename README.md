# IT-Bot - Assistant IT Intelligent

Un chatbot d'assistance IT intelligent développé pour IT-Work, utilisant l'IA pour fournir un support technique efficace.

## Fonctionnalités

- Interface de chat interactive avec Gradio
- Recherche sémantique avec FAISS
- Intégration avec l'API Groq (Mixtral 8x7B)
- Base de connaissances personnalisée
- Support multilingue (français)

## Configuration

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```

2. Configurer la variable d'environnement :
```bash
GROQ_API_KEY=votre_clé_api
```

3. Lancer l'application :
```bash
python app.py
```

## Déploiement

Ce projet est configuré pour être déployé sur Replit.

## Structure du Projet

```
.
├── app.py              # Application principale
├── chatbot.py          # Logique du chatbot
├── knowledge_base.py   # Gestion de la base de connaissances
├── static/            # Fichiers statiques
└── scraped_data/      # Données du chatbot
```

## Auteur

Développé par Jimmy pour IT-Work
