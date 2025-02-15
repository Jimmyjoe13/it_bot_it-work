FROM python:3.9.18-slim

# Installation des dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copie et installation des dépendances Python
COPY requirements.txt .

# Installation de PyTorch CPU uniquement pour réduire la taille
RUN pip install --no-cache-dir torch==2.0.1+cpu torchvision==0.15.2+cpu -f https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# Copie du reste du code
COPY . .

# Variable d'environnement pour le port
ENV PORT=8000

# Exposition du port
EXPOSE ${PORT}

# Commande de démarrage
CMD uvicorn app:app --host 0.0.0.0 --port ${PORT}
