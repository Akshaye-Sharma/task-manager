from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
import psycopg2
from app.routes import register_routes
from .config import Config

def create_app():
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static'
                )

    bcrypt = Bcrypt(app)
    app.config["JWT_SECRET_KEY"] = "myspecialKey"
    jwt = JWTManager(app)

    conn = psycopg2.connect(
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        host=Config.DB_HOST,
        port=Config.DB_PORT
    )

    cursor = conn.cursor()

    register_routes(app, cursor, conn, bcrypt)

    return app