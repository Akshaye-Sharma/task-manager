from .auth_routes import register_user_routes
from .task_routes import register_task_routes

def register_routes(app, cursor, conn, bcrypt):
    register_user_routes(app, cursor, conn, bcrypt)
    register_task_routes(app, cursor, conn)