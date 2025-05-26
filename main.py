import click
"""
main.py - A CLI tool for managing tasks in memory.

Commands:
    add, list, edit, delete
"""

# Simple in memory task list
tasks = []

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
    tasks.append(description)
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
    if not tasks:
        click.echo("No tasks found.")
        return
    if 1<= task_id <= len(tasks):
        removed = tasks.pop()
        click.echo(f"Deleted task: {removed}")
    else:
        click.echo("Invalid task ID.")

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
    if 1 <= task_id <= len(tasks):
        tasks[task_id - 1] = new_description
        click.echo(f"Task {task_id} updated.")
    else:
        click.echo("Invalid task ID.")

@cli.command()
def list():
    """
    List all tasks.
    
    :return: none
    """
    if not tasks:
        click.echo("No tasks found.")
    else:
        for i, task in enumerate(tasks, 1):
            click.echo(f"{i}. {task}")

if __name__ == "__main__":
    cli()