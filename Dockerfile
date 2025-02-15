# Stage de build
FROM python:3.9.18-slim as builder

# Installation des dépendances minimales pour le build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copie et installation des dépendances Python
COPY requirements.txt .

# Installation de PyTorch CPU uniquement et autres dépendances
RUN pip install --no-cache-dir torch==2.0.1+cpu -f https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

# Stage final
FROM python:3.9.18-slim

WORKDIR /app

# Copie des packages Python depuis le builder
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/

# Copie du code de l'application
COPY . .

# Variable d'environnement pour le port
ENV PORT=8000

# Exposition du port
EXPOSE ${PORT}

# Commande de démarrage
CMD uvicorn app:app --host 0.0.0.0 --port ${PORT}
