# Chatbot IA IT-Work avec Groq API

Ce projet est un chatbot intelligent spécialisé sur IT-Work, utilisant l'API Groq et le modèle Deepseek-R1-Distill-Llama-70b pour générer des réponses pertinentes en français.

## Fonctionnalités

- Interface web interactive et responsive
- Traitement du langage naturel en français
- Base de connaissances spécialisée sur IT-Work
- Scraping automatique des sites IT-Work
- Historique des conversations
- Support de l'accessibilité
- Intégration sécurisée avec l'API Groq

## Composants

- `app.py` : Application FastAPI principale
- `chatbot.py` : Logique du chatbot avec intégration Groq
- `scraper.py` : Scraper spécialisé pour les sites IT-Work
- `knowledge_base.py` : Gestion de la base de connaissances
- `requirements.txt` : Dépendances Python
- `.env` : Configuration des variables d'environnement

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

## Utilisation

1. Mettre à jour la base de connaissances :
```bash
python scraper.py
```

2. Démarrer le serveur :
```bash
python app.py
```

3. Accéder à l'application :
Ouvrir votre navigateur et aller à `http://localhost:8000`

## Structure des données

Les données scrapées sont stockées dans le dossier `scraped_data` avec la structure suivante :
```
scraped_data/
├── it-work_fr/
├── blog_it-work_fr/
└── landing_it-work_fr/
```

## Sécurité

- La clé API est stockée de manière sécurisée dans le fichier `.env`
- Les données sensibles ne sont pas exposées côté client
- Protection contre les injections XSS
- Validation des URLs lors du scraping

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Licence

MIT
