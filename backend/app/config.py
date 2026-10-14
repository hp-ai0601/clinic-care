import os

APP_NAME = "ClinicCare"
APP_VERSION = "0.1.0"

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./clinic.db")

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
JWT_ALG = "HS256"
TOKEN_EXPIRE_MINUTES = 480
