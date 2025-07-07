import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from pathlib import Path
from flask import Blueprint, request, jsonify

cost_api = Blueprint('cost_api', __name__)

# Dynamically resolve model path relative to this file
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "waste_model.pkl"

def train_model(df: pd.DataFrame) -> RandomForestRegressor:
    df = df.dropna()
    features = ['usage_days', 'usage_frequency', 'cost']
    df['waste_score'] = (df['usage_days'] * df['cost']) / (df['usage_frequency'] + 1)
    X = df[features]
    y = df['waste_score']
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def save_model(model: RandomForestRegressor, model_path: Path = MODEL_PATH):
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)

def load_model(model_path: Path = MODEL_PATH) -> RandomForestRegressor | None:
    if model_path.exists():
        return joblib.load(model_path)
    return None

def predict_waste(model: RandomForestRegressor, features_df: pd.DataFrame):
    required_features = ['usage_days', 'usage_frequency', 'cost']
    return model.predict(features_df[required_features])

# Load the model at import time (can be None if not trained yet)
MODEL = load_model()

@cost_api.route('/predict_waste', methods=['POST'])
def predict_waste_route():
    """
    POST JSON list of records:
    [
      {"usage_days": int, "usage_frequency": int, "cost": float},
      ...
    ]
    Returns predicted waste scores.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    if MODEL is None:
        return jsonify({"error": "Model not trained yet"}), 500

    try:
        df = pd.DataFrame(data)
        predictions = predict_waste(MODEL, df)
        return jsonify({"predictions": predictions.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
