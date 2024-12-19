from flask import Flask, request, jsonify, render_template_string
from prometheus_flask_exporter import PrometheusMetrics
import mlflow
import pandas as pd

app = Flask(__name__)

# Initialiser Prometheus
metrics = PrometheusMetrics(app)

# Configuration du chemin MLflow pour récupérer le modèle
MLFLOW_TRACKING_URI = "http://15.237.37.51:5000"
RUN_ID = "77242a872ff44c00b12cc5a9a958c48f" 
MODEL_URI = f"runs:/{RUN_ID}/model"

# Définition l'URI de suivi MLflow et charger le modèle
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
model = mlflow.sklearn.load_model(MODEL_URI)

# Exposer l'endpoint pour les métriques
@app.route("/metrics")
def metrics_view():
    # Prometheus exporte automatiquement les métriques avec cette configuration
    return metrics.handle()

@app.route("/", methods=["GET"])
def home():
    # Page HTML pour entrer les données
    html = '''
    <html>
        <body>
            <h2>Predict Wine Quality</h2>
            <form action="/predict" method="POST">
                <label for="fixed_acidity">Fixed Acidity:</label><br>
                <input type="text" id="fixed_acidity" name="fixed_acidity"><br>
                <label for="volatile_acidity">Volatile Acidity:</label><br>
                <input type="text" id="volatile_acidity" name="volatile_acidity"><br>
                <label for="citric_acid">Citric Acid:</label><br>
                <input type="text" id="citric_acid" name="citric_acid"><br>
                <label for="residual_sugar">Residual Sugar:</label><br>
                <input type="text" id="residual_sugar" name="residual_sugar"><br>
                <label for="chlorides">Chlorides:</label><br>
                <input type="text" id="chlorides" name="chlorides"><br>
                <label for="free_sulfur_dioxide">Free Sulfur Dioxide:</label><br>
                <input type="text" id="free_sulfur_dioxide" name="free_sulfur_dioxide"><br>
                <label for="total_sulfur_dioxide">Total Sulfur Dioxide:</label><br>
                <input type="text" id="total_sulfur_dioxide" name="total_sulfur_dioxide"><br>
                <label for="density">Density:</label><br>
                <input type="text" id="density" name="density"><br>
                <label for="pH">pH:</label><br>
                <input type="text" id="pH" name="pH"><br>
                <label for="sulphates">Sulphates:</label><br>
                <input type="text" id="sulphates" name="sulphates"><br>
                <label for="alcohol">Alcohol:</label><br>
                <input type="text" id="alcohol" name="alcohol"><br><br>
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    '''
    return render_template_string(html)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Récupération des données du formulaire HTML
        input_data = [
            {
                "fixed acidity": float(request.form['fixed_acidity']),
                "volatile acidity": float(request.form['volatile_acidity']),
                "citric acid": float(request.form['citric_acid']),
                "residual sugar": float(request.form['residual_sugar']),
                "chlorides": float(request.form['chlorides']),
                "free sulfur dioxide": float(request.form['free_sulfur_dioxide']),
                "total sulfur dioxide": float(request.form['total_sulfur_dioxide']),
                "density": float(request.form['density']),
                "pH": float(request.form['pH']),
                "sulphates": float(request.form['sulphates']),
                "alcohol": float(request.form['alcohol'])
            }
        ]
        
        # Conversion en DataFrame
        input_df = pd.DataFrame(input_data)

        # Faire la prédiction avec le modèle
        predictions = model.predict(input_df)

        # Afficher les résultats sur la même page
        result_html = f'''
        <h3>Prediction Result:</h3>
        <p>The predicted quality is: {predictions[0]}</p>
        <br><a href="/">Go back</a>
        '''
        return render_template_string(result_html)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "API is running successfully!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
