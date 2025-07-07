import pandas as pd
from backend.models.cost_model import train_model

if __name__ == "__main__":
    print("📦 Loading and preparing data...")
    df = pd.read_csv("backend/data/license_usage.csv")  # Adjust path as needed

    print("🧠 Training model...")
    model = train_model(df)

    print("✅ Model trained and saved.")
