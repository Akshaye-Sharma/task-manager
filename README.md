# TaskManager API

A secure, full-stack task manager app featuring a RESTful Flask API backend and a responsive frontend web interface
for user registration, login, and task management.

## Backend API

* User registration & login with secure hashed passwords using `Bcrypt`.
* JWT Authentication to protect task-related API endpoints.
* RESTful API endpoints to add, list, edit, delete, and clear user-specific tasks.
* Data persistence using PostgreSQL database (`taskmanager`).
* Task numbering scoped per user.

## Frontend Web App

* Responsive login and registration pages.
* Task management UI with add/edit/delete/clear operations.
* Username persistence across pages using Local Storage.
* Clean, simple UI styled with CSS for usability.
* Dynamic display of logged-in user information.

## Tech Stack
* Backend: Python (Flask)
* Database: PostgreSQL
* Authentication: JWT (via `flask-jwt-extended`)
* Password Security: `Bcrypt`
* Environment Management: `python-dotenv`
* Frontend: HTML, CSS, JavaScript

## Project Structure

```bash
task-manager/
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
├── tests/
│   └── test_api.py
├── .gitignore
├── .env
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
git clone https://github.come/Akshaye-Sharma/task-manager.git
cd task-manager
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
python3 run.py
```

## Running Tests

Make sure PostgreSQL is running and environment variables are set.

```bash
python3 -m unittest discover tests
```