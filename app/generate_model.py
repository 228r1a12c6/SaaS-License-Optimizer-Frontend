import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

# Load mock training data
df = pd.read_csv("lambda/mock_training_data.csv")

X = df[["License Count", "Monthly Cost", "Active Users"]]
y = df["Waste"]

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save model
model_path = os.path.join("lambda", "model.pkl")
with open(model_path, "wb") as f:
    pickle.dump(model, f)

print("✅ model.pkl created at:", model_path)
