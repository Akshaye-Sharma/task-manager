from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
import psycopg2
from routes import register_routes

def create_app():
    app = Flask(__name__)

    bcrypt = Bcrypt(app)
    app.config["JWT_SECRET_KEY"] = "myspecialKey"
    jwt = JWTManager(app)

    conn = psycopg2.connect(
        dbname="taskmanager",
        user="akshayesharma",
        host="localhost",
        port="5432"
    )

    cursor = conn.cursor()

    register_routes(app, cursor, conn, bcrypt)

    return app
