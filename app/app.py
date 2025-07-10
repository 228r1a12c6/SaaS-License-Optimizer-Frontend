import json
import pickle
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Load model once
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

def lambda_handler(event, context):
    logger.info("Lambda triggered")
    logger.info(f"Received event: {event}")

    if isinstance(event, str):
        event = json.loads(event)

    input_data = event.get("input", [1, 2, 3, 4])
    logger.info(f"Input data: {input_data}")

    try:
        prediction = model.predict([input_data])
        logger.info(f"Prediction: {prediction.tolist()}")
        return {
            "input": input_data,
            "prediction": prediction.tolist()
        }
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        return {
            "error": str(e)
        }
