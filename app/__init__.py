from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
import psycopg2
from app.routes import register_routes
from .config import Config

def create_app(test_config=None, test_conn=None, test_cursor=None):
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static'
                )
    app.config.from_object(Config or test_config)

    bcrypt = Bcrypt(app)
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    jwt = JWTManager(app)
    print("Config.DB_NAME", Config.DB_NAME)
    print("Config.DB_USER", Config.DB_USER)
    print("Config.DB_PASSWORD", Config.DB_PASSWORD)
    print("Config.DB_HOST", Config.DB_HOST)
    print("Config.DB_PORT", Config.DB_PORT)
    conn = test_conn or psycopg2.connect(
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT
    )

    cursor = test_cursor or conn.cursor()

    register_routes(app, cursor, conn, bcrypt)

    return app