from flask import request, render_template
from flask_jwt_extended import jwt_required
from app.managers.task_manager import TaskManager

def register_task_routes(app, cursor, conn):
    task_manager = TaskManager(cursor, conn)

    @app.route("/tasks")
    def tasks_page():
        return render_template("tasks_page.html")

    @app.route("/tasks", methods=["POST"])
    @jwt_required()
    def add_task():
        return task_manager.add_task()

    @app.route("/api/tasks", methods=["GET"])
    @jwt_required()
    def list_tasks():
        return task_manager.list_tasks()
    
    @app.route("/tasks/<int:task_id>", methods=["PATCH"])
    @jwt_required()
    def edit_task(task_id):
        return task_manager.edit_task(task_id)

    @app.route("/tasks/<int:task_id>", methods=["DELETE"])
    @jwt_required()
    def delete_task(task_id):
        return task_manager.delete_task(task_id)

    @app.route("/tasks/clear", methods=["GET"])
    @jwt_required()
    def clear_list():
        return task_manager.clear_list()
