from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.managers.user_manager import UserManager
from app.managers.task_manager import TaskManager

def register_routes(app, cursor, conn, bcrypt):

    user_manager = UserManager(cursor, conn, bcrypt)
    task_manager = TaskManager(cursor, conn)


    @app.route("/tasks/register", methods=["POST"])
    def register():
        return user_manager.register_user()

    @app.route("/tasks/login", methods=["POST"])
    def login():
        return user_manager.login_user()

    @app.route("/tasks", methods=["POST"])
    @jwt_required()
    def add_task():
        return task_manager.add_task()

    @app.route("/tasks/clear", methods=["GET"])
    @jwt_required()
    def clear_list():
        return task_manager.clear_tasks()

    @app.route("/tasks", methods=["GET"])
    @jwt_required()
    def list_tasks():
        return task_manager.list_tasks()

    @app.route("/tasks", methods=["PATCH"])
    @jwt_required()
    def edit_task():
        return task_manager.edit_task()

    @app.route("/tasks", methods=["DELETE"])
    @jwt_required()
    def delete_task():
        return task_manager.delete_task()
    
    return app
