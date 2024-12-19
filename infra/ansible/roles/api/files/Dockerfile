# Utilise l'image Python 3.9 comme base
FROM python:3.9

# Installation des dépendances système (optionnel)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt pour installer les dépendances
COPY requirements.txt .

# Installer les bibliothèques nécessaires
RUN pip install --no-cache-dir -r requirements.txt

# Copier le fichier API (api.py) dans le conteneur
COPY api.py .

# Exposer le port 5000 pour l'API Flask
EXPOSE 5001

# Lancer l'API Flask
CMD ["python","api.py"]