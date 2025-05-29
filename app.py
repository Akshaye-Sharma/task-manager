from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
import psycopg2

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

@app.route("/tasks/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
        conn.commit()
    except psycopg2.IntegrityError:
        conn.rollback()
        return jsonify({"error": "Username already exists"}), 400

    return jsonify({"message" : "User registered"}), 201

@app.route("/tasks/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and bcrypt.check_password_hash(user[1], password):
        token = create_access_token(identity=str(user[0]))
        return jsonify(message = "Login successful", access_token=token)
    
    return jsonify({"Failed": "Invalid credentials"}), 401

@app.route("/tasks", methods=["POST"])
@jwt_required()
def add_task():
    user_id = get_jwt_identity()
    data = request.get_json()
    description = data.get("description")

    if not description:
        return jsonify({"error": "Task description is required"}), 400

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = %s", (user_id,))
    user_task_number = cursor.fetchone()[0] + 1

    cursor.execute(
        "INSERT INTO tasks (description, user_id, user_task_number) VALUES (%s, %s, %s)", (description, user_id, user_task_number))
    
    conn.commit()
    return jsonify({"Added task ": description}), 201

@app.route("/tasks/clear", methods=["GET"])
@jwt_required()
def clear_list():
    user_id = get_jwt_identity()

    cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
    if not cursor.fetchall():
        return jsonify({"message":"No tasks found."})

    cursor.execute("DELETE FROM tasks WHERE user_id = %s", (user_id,))
    conn.commit()
    return jsonify({"Clear list":"List tasks cleared."})


@app.route("/tasks", methods=["GET"])
@jwt_required()
def list_tasks():
    user_id = get_jwt_identity()

    cursor.execute(
        "SELECT user_task_number, description FROM tasks WHERE user_id = %s ORDER BY user_task_number", (user_id))
    rows = cursor.fetchall()
    if not rows:
        return jsonify({"error":"No tasks found."})
    else:
        task_list = [f"{row[0]}. {row[1]}" for row in rows]
        return jsonify(task_list)

@app.route("/tasks", methods=["PATCH"])
@jwt_required()
def edit_task():
    data = request.get_json()

    user_id = get_jwt_identity()
    user_task_number = data.get("id")
    description = data.get("description")

    if not user_task_number:
        return jsonify({"error": "Task number is requried."}), 400

    if not description:
        return jsonify({"error": "Task description is requried."}), 400

    cursor.execute("SELECT * FROM tasks WHERE user_task_number = %s AND user_id = %s", (user_task_number, user_id,))
    task = cursor.fetchone()

    if not task:
        return jsonify({"error": "No such task found."}), 400
    
    cursor.execute("UPDATE tasks SET description = %s WHERE user_task_number = %s AND user_id = %s", (description, user_task_number, user_id))
    conn.commit()
    return jsonify({"Task edited": {"id": user_task_number, "description": description}})


@app.route("/tasks", methods=["DELETE"])
@jwt_required()
def delete_task():
    data = request.get_json()

    user_id = get_jwt_identity()
    user_task_number = data.get("id")

    if not user_task_number:
        return jsonify({"error": "Task number is requried."}), 400
    
    cursor.execute("SELECT * FROM tasks WHERE user_task_number = %s AND user_id = %s", (user_task_number, user_id,))
    task = cursor.fetchone()

    if not task:
        return jsonify({"error": "No such task found."}), 400
    
    cursor.execute("DELETE FROM tasks WHERE user_task_number = %s AND user_id = %s", (user_task_number, user_id,))

    cursor.execute("SELECT id FROM tasks WHERE user_id = %s", (user_id,))
    result = cursor.fetchall()

    for i in range(len(result)):
        cursor.execute(
            """UPDATE tasks
            SET user_task_number = %s
            WHERE id = %s
            """, 
            (i+1, result[i],)
        )

    conn.commit()
    return jsonify({"Deleted task" : task}), 200


if __name__ == "__main__":
    app.run(debug=True)