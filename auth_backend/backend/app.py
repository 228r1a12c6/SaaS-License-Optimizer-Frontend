from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
import backend.config as config
from backend.db import init_db, db
from backend.routes.auth_routes import auth_bp
from backend.routes.predict_routes import predict_bp

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY

jwt = JWTManager(app)

init_db(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp)
app.register_blueprint(predict_bp, url_prefix='/predict')

@app.route("/")
def index():
    return jsonify({"message": "API is working!"}), 200

if __name__ == "__main__":
    app.run(debug=True)
