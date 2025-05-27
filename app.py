from flask import Flask, request, jsonify
import psycopg2

"""
app.py - Basic web app for managing tasks.

Commands:
    add, delete, edit, clear and list
"""

app = Flask(__name__)

conn = psycopg2.connect(
    dbname="manager",
    user="akshayesharma",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

@app.route("/tasks/clear", methods=["GET"])
def clear_list():
    """
    Clear list of tasks.
    """

    cursor.execute("SELECT * FROM tasks")
    if not cursor.fetchall():
        return jsonify({"error":"No tasks found."})

    cursor.execute("TRUNCATE TABLE tasks RESTART IDENTITY")
    conn.commit()
    return jsonify({"Clear list":"List tasks cleared."})

@app.route("/tasks", methods=["GET"])
def list_tasks():
    """
    List all tasks.

    :return: JSON with task ID and description of tasks.
    """
    
    cursor.execute("SELECT id, description FROM tasks")
    rows = cursor.fetchall()
    if not rows:
        return jsonify({"error":"No tasks found."})
    else:
        task_list = [f"{row[0]}. {row[1]}" for row in rows]
        return jsonify(task_list)

@app.route("/tasks", methods=["POST"])
def add_task():
    """
    Add a new task.

    :return: JSON with task ID and description or an error message.
    """

    data = request.get_json()
    description = data.get("description")

    if not description:
        return jsonify({"error": "Task description is required"}), 400

    cursor.execute("INSERT INTO tasks (description) VALUES (%s)", (description,))
    conn.commit()
    return jsonify({"Added task ": description}), 201

@app.route("/tasks", methods=["PATCH"])
def edit_task():
    """
    Edit a task.

    :return: JSON with the task ID and description of the update task or
    an error message.
    """

    data = request.get_json()
    id = data.get("id")
    description = data.get("description")

    if not id:
        return jsonify({"error": "Task number is requried."}), 400

    if not description:
        return jsonify({"error": "Task description is requried."}), 400

    cursor.execute("SELECT * FROM tasks WHERE id = %s", (id,))
    task = cursor.fetchone()

    if not task:
        return jsonify({"error": "No such task found."}), 400
    
    cursor.execute("UPDATE tasks SET description = %s WHERE id = %s", (description, id))
    conn.commit()
    return jsonify({"Task edited": {"id": id, "description": description}})


@app.route("/tasks", methods=["DELETE"])
def delete_task():
    """
    Delete a task.
    
    :return: JSON with the deleted task.
    """

    data = request.get_json()
    id = data.get("id")

    if not id:
        return jsonify({"error": "Task number is requried."}), 400
    
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (id,))
    task = cursor.fetchone()

    if not task:
        return jsonify({"error": "No such task found."}), 400
    
    cursor.execute("DELETE FROM tasks WHERE id = %s", (id,))
    conn.commit()
    return jsonify({"Deleted task" : task}), 200


if __name__ == "__main__":
    app.run(debug=True)