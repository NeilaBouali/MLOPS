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
ENV MLFLOW_TRACKING_URI="http://15.237.37.51:5000"     
ENV MLFLOW_S3_ENDPOINT_URL="https://mlflow-model-storage.s3.eu-west-3.amazonaws.com/Mlflow_endpoint/"

# Copier le script train.py dans l'image
COPY train.py /opt/mlflow/train.py

# Définir le point d'entrée du conteneur
CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000"]