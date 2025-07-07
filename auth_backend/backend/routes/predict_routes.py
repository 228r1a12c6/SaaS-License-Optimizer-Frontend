from flask import Blueprint, request, jsonify
import pandas as pd
from backend.models.cost_model import load_model, predict_waste
from flask_jwt_extended import jwt_required, get_jwt_identity

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/waste", methods=["POST"])
@jwt_required()
def get_prediction():
    """
    Authenticated endpoint to predict waste score from posted JSON data.

    Expected JSON:
    {
      "usage_days": int,
      "usage_frequency": int,
      "cost": float
    }

    Returns:
        JSON with predicted waste score.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    required_fields = ["usage_days", "usage_frequency", "cost"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    try:
        usage_days = int(data["usage_days"])
        usage_frequency = int(data["usage_frequency"])
        cost = float(data["cost"])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid data types for usage_days, usage_frequency or cost"}), 400

    df = pd.DataFrame([{
        "usage_days": usage_days,
        "usage_frequency": usage_frequency,
        "cost": cost
    }])

    model = load_model()
    if model is None:
        return jsonify({"error": "Model could not be loaded"}), 500

    prediction = predict_waste(model, df)
    waste_score = float(prediction[0])

    return jsonify({"waste_score": waste_score}), 200
