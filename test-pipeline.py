import os
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from infra.ansible.roles.mlflow.files.train import eval_metrics, get_wine_data_from_s3 

# Test de la fonction eval_metrics
def test_eval_metrics():
    actual = [3, 5, 7]
    predicted = [3, 5, 8]

    rmse, mae, r2 = eval_metrics(actual, predicted)

    assert rmse > 0, "RMSE should be greater than 0"
    assert mae > 0, "MAE should be greater than 0"
    assert -1 <= r2 <= 1, "R2 should be between -1 and 1"

# Test de la fonction get_wine_data_from_s3 avec mock
@patch("boto3.client")
def test_get_wine_data_from_s3(mock_boto_client, tmpdir):
    bucket_name = "test-bucket"
    file_key = "test-file.csv"
    local_cache = tmpdir.mkdir("cache")
    local_file_path = os.path.join(local_cache, "winequality-red.csv")

    # Mock S3 client
    mock_s3 = MagicMock()
    mock_boto_client.return_value = mock_s3

    # Simuler un fichier S3
    mock_s3.download_file.side_effect = lambda bucket, key, path: open(path, "w").write("fixed acidity;quality\n7.4;5")

    # Appeler la fonction
    data = get_wine_data_from_s3(bucket_name, file_key, local_cache=str(local_cache))

    # Vérifier le téléchargement et les données
    assert os.path.exists(local_file_path), "Le fichier téléchargé doit exister en local."
    assert not data.empty, "Les données ne doivent pas être vides."
    assert "fixed acidity" in data.columns, "Les colonnes doivent inclure 'fixed acidity'."
    assert "quality" in data.columns, "Les colonnes doivent inclure 'quality'."
