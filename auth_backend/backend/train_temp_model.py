import pandas as pd
from backend.models.cost_model import train_model

# Dummy training data
data = {
    'cpu_usage': [40, 60, 80, 30],
    'memory_usage': [70, 80, 60, 50],
    'storage_usage': [20, 40, 60, 30],
    'license_cost': [100, 200, 150, 120]
}
df = pd.DataFrame(data)

# Train and save the model
train_model(df)
print("✅ Model trained and saved successfully!")
