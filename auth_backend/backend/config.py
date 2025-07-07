import os
from dotenv import load_dotenv

# Load environment variables from .env file at project root (auth_backend/.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "ajH98dj@i3!js92k!x")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# Database Configuration
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///users.db")
