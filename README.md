# TaskManager

A simple command-line interface (CLI) tool to manage tasks using Python, PostgreSQL and Click.

> 🚧 **This project is in early development.** Currently, it runs only on my local machine and uses a local PostgreSQL database. More features and cross-platform compatibility will be added soon.

## Current Status

* Basic CLI tool with commands to add, list, edit and delete tasks.
* Task data is stored in a PostgreSQL database (`manager`).
* Single script: `main.py`.

## Prerequisites

* Python 3.x
* PostgreSQL installed and running locally.
* Required python packages: `click`, `psycopg2`.

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
pip install click psycopg2
```
>If you have issues with `psycopg2`, try `psycopg2-binary` instead:
>```bash
>pip install psycopg2-binary
>```
3. Create a database named `manager`:
```sql
CREATE DATABASE manager;
```
4. Create a `tasks` table:
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL
);
```