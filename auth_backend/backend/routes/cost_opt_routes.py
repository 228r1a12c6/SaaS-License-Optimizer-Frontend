from flask import Blueprint, request
from backend.utils.jwt_utils import decode_jwt
from backend.utils.response_formatter import format_response
from backend.models.preprocess import preprocess_input
import pandas as pd
import joblib
import os

cost_opt_routes = Blueprint('cost_opt_routes', __name__)

# Load model at startup
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'cost_model.pkl')
model = joblib.load(model_path)

@cost_opt_routes.route('/api/cost_optimization', methods=['POST'])
def optimize_cost():
    # 1. JWT Authentication
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return format_response(False, "Missing or invalid Authorization header."), 401

    token = auth_header.split(" ")[1]
    user = decode_jwt(token)
    if not user:
        return format_response(False, "Invalid or expired token."), 403

    # 2. Parse input JSON
    try:
        payload = request.get_json()
        df = pd.DataFrame(payload['data'])
    except Exception as e:
        return format_response(False, f"Invalid input format: {e}"), 400

    if df.empty:
        return format_response(False, "No data provided."), 400

    # 3. Preprocess
    try:
        processed_df = preprocess_input(df)
    except Exception as e:
        return format_response(False, f"Preprocessing failed: {e}"), 500

    # 4. Predict costs
    try:
        predictions = model.predict(processed_df)
        df['predicted_cost'] = predictions
    except Exception as e:
        return format_response(False, f"Prediction failed: {e}"), 500

    # 5. Extract insights
    top_services = (
        df.groupby('service')['predicted_cost']
        .sum()
        .sort_values(ascending=False)
        .head(3)
        .reset_index()
        .to_dict(orient='records')
    )

    savings = df[df['usage_count'] < 5][['license_id', 'service', 'cost', 'predicted_cost']]
    savings['suggested_savings'] = savings['cost'] - savings['predicted_cost']
    savings_suggestions = savings.to_dict(orient='records')

    # 6. Respond
    return format_response(True, "Prediction successful.", {
        "predictions": df[['license_id', 'service', 'predicted_cost']].to_dict(orient='records'),
        "top_costly_services": top_services,
        "savings_suggestions": savings_suggestions
    })
