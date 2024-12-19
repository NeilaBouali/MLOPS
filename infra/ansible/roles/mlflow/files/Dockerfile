# Utiliser une image Ubuntu de base
FROM ubuntu:22.04

# Définir le fuseau horaire
ENV TZ=UTC
RUN apt-get update && apt-get install -y tzdata && \
    ln -sf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Installer Python et pip
RUN apt-get install -y python3 python3-pip

# Installer les bibliothèques nécessaires
RUN pip3 install boto3 pandas numpy scikit-learn mlflow==2.1.1

# Définir les variables pour MLflow Tracking
ENV MLFLOW_TRACKING_URI="http://13.36.167.142:5000"
ENV ALPHA=0.5
ENV L1_RATIO=0.5

# Copier le script train.py dans l'image
COPY infra/ansible/roles/mlflow/files/train.py /opt/mlflow/train.py

# Définir le point d'entrée du conteneur
CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000"]
