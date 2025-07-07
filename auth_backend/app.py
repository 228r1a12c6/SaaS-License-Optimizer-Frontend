from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from db import init_db
from routes.auth_routes import auth_bp
from models import user_model  # Ensure the User model is loaded
from backend import config  # Make sure config.py is in root or importable

# Initialize Flask app
app = Flask(__name__)

# Load config
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
# Optionally: app.config['JWT_ALGORITHM'] = config.JWT_ALGORITHM

# Setup JWT
jwt = JWTManager(app)

# Configure and initialize the database
init_db(app)

# Create database tables inside app context
with app.app_context():
    from db import db
    db.create_all()

# Register authentication blueprint
app.register_blueprint(auth_bp)

# Basic route to verify API is working
@app.route("/")
def index():
    return jsonify({"message": "API is working!"}), 200

# Run the Flask development server
if __name__ == "__main__":
    app.run(debug=True)
