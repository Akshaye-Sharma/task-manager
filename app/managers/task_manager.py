from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

class TaskManager:
    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

    def add_task(self):
        data = request.get_json()
        user_id = get_jwt_identity()
        description = data.get("description")
        if not description:
            return jsonify({"error": "Task description is required"}), 400

        self.cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = %s", (user_id,))
        user_task_number = self.cursor.fetchone()[0] + 1

        self.cursor.execute(
            "INSERT INTO tasks (description, user_id, user_task_number) VALUES (%s, %s, %s)", (description, user_id, user_task_number))
        
        self.conn.commit()
        return jsonify({"Added task ": description}), 201
    
    def list_tasks(self):
        user_id = get_jwt_identity()
        self.cursor.execute(
            "SELECT user_task_number, description FROM tasks WHERE user_id = %s ORDER BY user_task_number", (user_id))
        rows = self.cursor.fetchall()
        if not rows:
            return jsonify({"error":"No tasks found."}), 404
        else:
            task_list = [f"{row[0]}. {row[1]}" for row in rows]
            return jsonify(task_list)

    def edit_task(self, user_task_number):
        data = request.get_json()
        user_id = get_jwt_identity()
        description = data.get("description")
        if not user_task_number:
            return jsonify({"error": "Task number is requried."}), 400

        if not description:
            return jsonify({"error": "Task description is requried."}), 400

        self.cursor.execute("SELECT * FROM tasks WHERE user_task_number = %s AND user_id = %s", (user_task_number, user_id,))
        task = self.cursor.fetchone()

        if not task:
            return jsonify({"error": "No such task found."}), 400
        
        self.cursor.execute("UPDATE tasks SET description = %s WHERE user_task_number = %s AND user_id = %s", (description, user_task_number, user_id))
        self.conn.commit()
        return jsonify({"Task edited": {"id": user_task_number, "description": description}})
    
    def delete_task(self, user_task_number):
        user_id = get_jwt_identity()    
        if not user_task_number:
            return jsonify({"error": "Task number is requried."}), 400
        
        self.cursor.execute("SELECT * FROM tasks WHERE user_task_number = %s AND user_id = %s", (user_task_number, user_id,))
        task = self.cursor.fetchone()

        if not task:
            return jsonify({"error": "No such task found."}), 400
        
        self.cursor.execute("DELETE FROM tasks WHERE user_task_number = %s AND user_id = %s", (user_task_number, user_id,))

        self.cursor.execute("SELECT id FROM tasks WHERE user_id = %s", (user_id,))
        result = self.cursor.fetchall()

        for i in range(len(result)):
            self.cursor.execute("UPDATE tasks SET user_task_number = %s WHERE id = %s", (i+1, result[i][0],))
        self.conn.commit()

        
        return jsonify({"Deleted task" : task}), 200
    
    def clear_list(self):
        user_id = get_jwt_identity()
        self.cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
        if not self.cursor.fetchall():
            return jsonify({"message":"No tasks found."})

        self.cursor.execute("DELETE FROM tasks WHERE user_id = %s", (user_id,))
        self.conn.commit()
        
        return jsonify({"Clear list":"List tasks cleared."})