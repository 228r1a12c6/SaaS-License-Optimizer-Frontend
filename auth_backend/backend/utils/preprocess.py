import pandas as pd
from datetime import datetime
from pathlib import Path

def load_and_filter_data(file_path, service_name, start_date, end_date):
    df = pd.read_csv(file_path)

    # ✅ Updated: Correct date parsing with dayfirst=True
    df['last_used'] = pd.to_datetime(df['last_used'], dayfirst=True)
    df['start_date'] = pd.to_datetime(df['start_date'], dayfirst=True)

    # Optional: filter by service
    if service_name != "all":
        df = df[df['service'] == service_name]

    mask = (
        (df['last_used'] >= pd.to_datetime(start_date)) &
        (df['last_used'] <= pd.to_datetime(end_date))
    )
    return df[mask]

def extract_features(df):
    df['usage_days'] = (df['last_used'] - df['start_date']).dt.days.clip(lower=1)
    df['usage_frequency'] = df['usage_count'] / df['usage_days'].replace(0, 1)
    return df[['license_id', 'usage_days', 'cost', 'usage_frequency']]

def preprocess_input(df):
    """
    Prepares input DataFrame for model prediction.
    Expects columns: ['license_id', 'service', 'usage_count', 'last_used', 'start_date', 'cost']
    """
    df['last_used'] = pd.to_datetime(df['last_used'], dayfirst=True)
    df['start_date'] = pd.to_datetime(df['start_date'], dayfirst=True)

    df['usage_days'] = (df['last_used'] - df['start_date']).dt.days.clip(lower=1)
    df['usage_frequency'] = df['usage_count'] / df['usage_days'].replace(0, 1)

    features = df[['usage_days', 'cost', 'usage_frequency']]
    return features
