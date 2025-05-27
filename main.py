import click
import psycopg2

"""
main.py - A CLI tool for managing tasks in memory.

Commands:
    add, delete, edit, clear, list
"""

# Connecting database to postgreSQL database

conn = psycopg2.connect(
    dbname="manager",
    user="akshayesharma",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

@click.group()
def cli():
    """Task manager CLI"""
    pass


@cli.command()
@click.argument('description')
def add(description):
    """
    Add a new task to the list.

    :param description: The task to be added.
    :type description: str
    :return: none
    """
    cursor.execute("INSERT INTO tasks (description) VALUES (%s)", (description,))
    conn.commit()
    click.echo(f"Task added: {description}")

@cli.command()
@click.argument('task_id', type=int)
def delete(task_id):
    """ 
    Deleting a task from the list. 
    
    :param task_id: The task to be deleted.
    :type task_id: int
    :return: none
    """

    cursor.execute("SELECT description FROM tasks WHERE id = %s", (task_id,))
    result = cursor.fetchone()
    if result is None:
        click.echo("No such task found.")
        return
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    click.echo(f"Deleted task: {result[0]}")

@cli.command()
@click.argument('task_id', type=int)
@click.argument('new_description')
def edit(task_id, new_description):
    """
    Edit an existing task. 
    
    :param task_id: The task being edited.
    :type task_id: int
    :param new_description: The updated task.
    :type new_description: int
    :return: none
    """
    cursor.execute("SELECT description FROM tasks WHERE id = %s", (task_id,))
    result = cursor.fetchone()
    if result is None:
        click.echo("No such task found.")
        return
    
    cursor.execute("UPDATE tasks SET description = %s WHERE id = %s", (new_description, task_id))
    conn.commit()
    click.echo(f"Task {task_id} updated.")

@cli.command()
def clear():
    """
    Clear the list of tasks.

    :return: none
    """
    cursor.execute("SELECT * FROM tasks")
    result = cursor.fetchone()
    if not result:
        click.echo("No tasks found.")

    cursor.execute("TRUNCATE TABLE tasks RESTART IDENTITY")
    conn.commit()
    click.echo("List tasks cleared.")

@cli.command()
def list():
    """
    List all tasks.
    
    :return: none
    """
    cursor.execute("SELECT id, description FROM tasks ORDER BY id")
    rows = cursor.fetchall()
    if not rows:
        click.echo("No tasks found.")
    else:
        for row in rows:
            click.echo(f"{row[0]}. {row[1]}")

if __name__ == "__main__":
    cli()