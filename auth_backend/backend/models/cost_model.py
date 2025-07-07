import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from pathlib import Path
import joblib

MODEL_PATH = Path("models_store/rf_model.pkl")

def save_model(model, path=MODEL_PATH):
    """Save the trained model to disk."""
    joblib.dump(model, path)

def load_model(path=MODEL_PATH):
    """Load the trained model from disk if it exists."""
    if path.exists():
        return joblib.load(path)
    return None

def train_model(df: pd.DataFrame) -> RandomForestRegressor:
    print("Columns in dataframe before training:", df.columns.tolist())

    df.loc[:, 'memory_usage'] = 0
    df.loc[:, 'storage_usage'] = 0
    df.loc[:, 'license_cost'] = df['cost']

    required_features = ['cpu_usage', 'memory_usage', 'storage_usage', 'license_cost']
    missing_cols = [col for col in required_features if col not in df.columns]

    if missing_cols:
        raise ValueError(f"Missing required columns for training: {missing_cols}")

    df = df.dropna(subset=required_features)
    df.loc[:, 'waste_score'] = df['cpu_usage'] / df['license_cost'].replace(0, 1)

    X = df[required_features]
    y = df['waste_score']

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    save_model(model)

    return model

def predict_waste(model, features_df: pd.DataFrame):
    """
    Predict waste score given features dataframe.
    Expects columns: 'cpu_usage', 'memory_usage', 'storage_usage', 'license_cost'
    """
    required_features = ['cpu_usage', 'memory_usage', 'storage_usage', 'license_cost']
    missing_cols = [col for col in required_features if col not in features_df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns for prediction: {missing_cols}")

    X = features_df[required_features]
    return model.predict(X)
