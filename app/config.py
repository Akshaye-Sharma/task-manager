import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "myspecialKey")
    DB_NAME = os.getenv("DB_NAME", "taskmanager")
    DB_USER = os.getenv("DB_USER", "akshayesharma")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")

class TestingConfig:
    TESTING = True
    JWT_SECRET_KEY = "testing-secret"
    DB_NAME = "manager_test"
    DB_USER = "akshayesharma"
    DB_PASSWORD = ""
    DB_HOST = "localhost"
    DB_PORT = "5432"