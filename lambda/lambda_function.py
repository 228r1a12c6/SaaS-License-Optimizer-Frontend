import os
import pickle
import logging
import pandas as pd
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Manual env setup
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

# Constants
GOOGLE_SHEET_ID = "1PAAWt-MG-B5st4h6BSQEwzfJLRFZTfzR16T8OiyOcvs"
RANGE = "Sheet1!A1:E1000"

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
logger.info("Model loaded.")

# Setup Google Sheets
creds = service_account.Credentials.from_service_account_file(
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
)
sheet_service = build("sheets", "v4", credentials=creds)
sheet = sheet_service.spreadsheets()

def fetch_data():
    logger.info("Fetching data from Google Sheets...")
    result = sheet.values().get(spreadsheetId=GOOGLE_SHEET_ID, range=RANGE).execute()
    rows = result.get("values", [])
    if not rows or len(rows) < 2:
        logger.error("No rows found in Google Sheet.")
        return None
    df = pd.DataFrame(rows[1:], columns=rows[0])
    df["License Count"] = pd.to_numeric(df["License Count"], errors="coerce")
    df["Monthly Cost"] = pd.to_numeric(df["Monthly Cost"], errors="coerce")
    df["Active Users"] = pd.to_numeric(df["Active Users"], errors="coerce")
    df["Last Used Date"] = pd.to_datetime(df["Last Used Date"], errors="coerce")
    logger.info(f"Dataframe loaded with {len(df)} records.")
    return df

def predict(df):
    features = df[["License Count", "Monthly Cost", "Active Users"]]
    df["Waste Prediction"] = model.predict(features)
    logger.info("Predictions generated.")
    return df

def lambda_handler(event, context):
    logger.info("Lambda invoked for Google Sheets prediction.")
    df = fetch_data()
    if df is None:
        logger.error("Failed to fetch data.")
        return {"statusCode": 500, "body": "No data or failed to fetch"}

    df = predict(df)
    return {
        "statusCode": 200,
        "body": df[["Service Name", "Waste Prediction"]].to_dict(orient="records")
    }
