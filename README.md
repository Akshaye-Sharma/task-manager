# TaskManager API

A secure, RESTful Flask API for managing user-specific task lists with JWT-based authentication and PostgreSQL.

## Features

* User Registration & Login (with hashed passwords and `Bycrpt`)
* JWT Authentication to protect task endpoints.
* Web API with endpoints to add, list, edit, delete and clear tasks.
* Task data is stored in a PostgreSQL database (`manager`).
* Task numbering per user.

## Tech Stack
* Backend: Python (Flask)
* Database: PostgreSQL
* Authentication: JWT (via `flask-jwt-extended`)
* Password Security: `Bcrypt`
* Environment Management: `python-dotenv`

## Project Structure

```bash
TaskManager/
├── app/                         
│   ├── __init__.py              
│   ├── config.py                
│   ├── managers/                
│   │   ├── user_manager.py
│   │   └── task_manager.py
│   └── routes/                  
│       ├── __init__.py          # Sets up all routes
│       ├── auth_routes.py       # Auth and page-rendering routes
│       └── task_routes.py       # Task-related routes
├── templates/
│   ├── auth_page.html
│   └── tasks_page.html
├── static/
│   ├── auth.js
│   ├── tasks.js
│   └── style.css
├── .gitignore
├── run.py                       # Entry point for running the app
├── requirements.txt
└── README.md

```
## Prerequisites

Python 3.x
PostgreSQL installed and running locally.


## Setup Instructions

1. Clone the repository & install dependencies

```bash
git clone https://github.come/Akshaye-Sharma/TaskManager.git
cd TaskManager
pip install -r requirements.txt
```

2. Set up PostgreSQL in `psql`.

```sql

CREATE DATABASE taskmanager;
\c taskmanager

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id),
    user_task_number INTEGER NOT NULL
);
```

3. Configure environment

Create an environment file in the root:

```env
JWT_SECRET_KEY=your_secret_key
DB_NAME=taskmanager
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

4. Run the app

```bash
python run.py
```
