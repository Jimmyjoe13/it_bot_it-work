# Chatbot IA avec Groq API

Ce projet est un chatbot intelligent utilisant l'API Groq et le modèle Deepseek-R1-Distill-Llama-70b pour générer des réponses pertinentes en français.

## Fonctionnalités

- Interface web interactive et responsive
- Traitement du langage naturel en français
- Historique des conversations
- Support de l'accessibilité
- Intégration sécurisée avec l'API Groq

## Prérequis

- Python 3.8+
- Clé API Groq valide

## Installation

1. Cloner le repository :
```bash
git clone [URL_DU_REPO]
cd chatbotia
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurer la clé API :
- Créer un fichier `.env` à la racine du projet
- Ajouter votre clé API Groq : `GROQ_API_KEY=votre_clé_api`

## Lancement

1. Démarrer le serveur :
```bash
python app.py
```

2. Accéder à l'application :
Ouvrir votre navigateur et aller à `http://localhost:8000`

## Structure du Projet

```
chatbotia/
├── app.py              # Application FastAPI principale
├── chatbot.py          # Logique du chatbot
├── requirements.txt    # Dépendances Python
├── .env               # Configuration des variables d'environnement
├── static/            # Fichiers statiques (CSS, JS)
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
└── templates/         # Templates HTML
    └── index.html
```

## Sécurité

- La clé API est stockée de manière sécurisée dans le fichier `.env`
- Les données sensibles ne sont pas exposées côté client
- Protection contre les injections XSS

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Licence

MIT
