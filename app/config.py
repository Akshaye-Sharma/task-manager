import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)

class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
    DB_NAME = os.getenv("DB_NAME", "taskmanager")
    DB_USER = os.getenv("DB_USER", "akshayesharma")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "nigs")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")

class TestingConfig:
    TESTING = True
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "testsecretkey")
    DB_NAME = "manager_test"
    DB_USER = "akshayesharma"
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = "localhost"
    DB_PORT = "5432"