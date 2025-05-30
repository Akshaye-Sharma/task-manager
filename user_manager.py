from flask import request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
import psycopg2

class UserManager:
    def __init__(self, cursor, conn, bcrypt):
        self.cursor = cursor
        self.conn = conn
        self.bcrypt = bcrypt
    
    def register_user(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        hashed_pw = self.bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
            self.conn.commit()
        except psycopg2.IntegrityError:
            self.conn.rollback()
            return jsonify({"error": "Username already exists"}), 400

        return jsonify({"message" : "User registered"}), 201
    
    def login_user(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400
        
        self.cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
        user = self.cursor.fetchone()

        if user and self.bcrypt.check_password_hash(user[1], password):
            token = create_access_token(identity=str(user[0]))
            return jsonify(message = "Login successful", access_token=token)
        
        return jsonify({"Failed": "Invalid credentials"}), 401
