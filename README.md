# TaskManager API

A simple RESTful web API to manage tasks using **Python**, **Flask**, and **PostgreSQL**.

## Current Status

* Web API with endpoints to add, list, edit, delete and clear tasks.
* Task data is stored in a PostgreSQL database (`manager`).
* API built using Flask `app.py`

## Prerequisites

* Python 3.x
* PostgreSQL installed and running locally.
* Required python packages: `Flask`, `psycopg2`.

## Setup Instructions

1. Ensure PostgreSQL is installed and running:

On MacOS (using Homebrew):
```bash
brew update
brew install postgresql
brew services start postgresql
```

2. Installing Python dependencies:

```bash
pip install flask psycopg2
```
>If you have issues with `psycopg2`, try:
>```bash
>pip install psycopg2-binary
>```
3. Create a PostgreSQL database and table:
```sql
CREATE DATABASE manager;
\c manager
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL
);
```
4. Run the app:
```bash
python app.py
```