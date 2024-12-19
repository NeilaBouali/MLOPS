import logging
import sys
import warnings
from urllib.parse import urlparse

import os
from pathlib import Path

import boto3
from botocore.exceptions import NoCredentialsError, ClientError

import numpy as np
import pandas as pd
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


def get_wine_data_from_s3(bucket_name, file_key, local_cache="cache"):
    """
    Télécharge un fichier CSV depuis un bucket S3 et le sauvegarde localement.
    """
    # Chemin de cache local
    local_path = os.path.join(local_cache, "winequality-red.csv")
    
    # Créer le répertoire cache si nécessaire
    os.makedirs(local_cache, exist_ok=True)

    # Télécharger si le fichier n'existe pas en cache local
    if not os.path.exists(local_path):
        print(f"Téléchargement de {file_key} depuis le bucket S3 '{bucket_name}'...")
        try:
            s3 = boto3.client("s3")
            s3.download_file(bucket_name, file_key, local_path)
            print("Téléchargement réussi.")
        except NoCredentialsError:
            print("Erreur : Pas d'identifiants AWS configurés.")
            raise
        except ClientError as e:
            print(f"Erreur : Impossible de télécharger le fichier depuis S3. {e}")
            raise
    else:
        print("Utilisation du fichier en cache.")

    # Charger le fichier CSV
    return pd.read_csv(local_path, sep=";")


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    np.random.seed(40)

    # Paramètres du bucket S3
    bucket_name = "mlflow-model-storage"  
    file_key = "winequality-red.csv"  

    # Lire les données du bucket S3
    data = get_wine_data_from_s3(bucket_name, file_key)

    # Split the data into training and test sets. (0.75, 0.25) split.
    train, test = train_test_split(data)

    # The predicted column is "quality" which is a scalar from [3, 9]
    train_x = train.drop(["quality"], axis=1)
    test_x = test.drop(["quality"], axis=1)
    train_y = train[["quality"]]
    test_y = test[["quality"]]

    alpha = float(os.getenv("ALPHA", 0.5))  # Valeur par défaut : 0.5
    l1_ratio = float(os.getenv("L1_RATIO", 0.5))  # Valeur par défaut : 0.5


    # Configuration de l'URI de suivi MLflow
    mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://15.237.37.51:5000")
    mlflow.set_tracking_uri(mlflow_tracking_uri)
    print("MLflow Tracking URI :", mlflow.get_tracking_uri())



    with mlflow.start_run():
        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        lr.fit(train_x, train_y)

        predicted_qualities = lr.predict(test_x)

        (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

        print(f"Elasticnet model (alpha={alpha:f}, l1_ratio={l1_ratio:f}):")
        print(f"  RMSE: {rmse}")
        print(f"  MAE: {mae}")
        print(f"  R2: {r2}")

        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        predictions = lr.predict(train_x)
        signature = infer_signature(train_x, predictions)

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        # Model registry does not work with file store
        if tracking_url_type_store != "file":
            mlflow.sklearn.log_model(
                lr, "model", registered_model_name="ElasticnetWineModel", signature=signature
            )
        else:
            mlflow.sklearn.log_model(lr, "model", signature=signature)
