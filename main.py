import click

# Simple in memory task list
tasks = []

@click.group()
def cli():
    """Task manager CLI"""
    pass


@cli.command()
@click.argument('description')
def add(description):
    """ Adding a new task. """
    tasks.append(description)
    click.echo(f"Task added: {description}")

@cli.command()
@click.argument('task_id', type=int)
def delete(task_id):
    """ Deleting a task. """
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
    """ Edit an existing task. """
    if 1 <= task_id <= len(tasks):
        tasks[task_id - 1] = new_description
        click.echo(f"Task {task_id} updated.")
    else:
        click.echo("Invalid task ID.")

@cli.command()
def list():
    """ List all current tasks. """
    if not tasks:
        click.echo("No tasks found.")
        return
    
    for i, task in enumerate(tasks, 1):
        click.echo("f{i}. {task}")

if __name__ == "__main__":
    cli()