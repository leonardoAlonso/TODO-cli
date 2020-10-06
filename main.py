#!usr/bin/env python

from tabulate import tabulate
from database_connection.db_connection import database, List, Task
import click
import peewee

MODELS = [List, Task]


@click.group()
def main():
    pass


@main.command()
def init():
    """Creates the tables and the database connection"""
    with database:
        database.create_tables(MODELS)
    click.echo(click.style('Success! \nTODO-cli ready to be useed', fg='green'))
    click.echo("Use --help to get all possible commands")


@main.command()
@click.argument('list_name')
def create_list(list_name):
    """Create a new list"""
    click.echo(click.style('You are about to create: ' + list_name, fg='blue'))
    if click.confirm(click.style("Continue? \U0001F914", fg='yellow'), abort=True):
        try:
            List.create(list_name=list_name)
            click.echo(click.style("Success!", fg='green'))
        except peewee.IntegrityError:
            click.echo(click.style('You already has a list with this name \U0001F616', fg='red'))


@main.command()
def get_all_list():
    """Get all list names"""
    table = []
    for _list in List.select():
        table.append([
            click.style(str(_list.id), fg='green'),
            click.style(_list.list_name, fg='green'),
            click.style(_list.creation_date.strftime('%m/%d/%Y'), fg='green')
        ])
    click.echo(tabulate(table,
                        headers=[click.style('ID', fg='red'),
                                 click.style('Name', fg='red'),
                                 click.style('Creation date', fg='red')]))


@main.command()
@click.argument('list_name')
def delete_list(list_name):
    """Allows to delete a List based on list name.
    This will delete all task related
        - argument list_name
    """
    _list = List.get_or_none(List.list_name == list_name)
    try:
        _list.delete().execute()
        click.echo(click.style("The list has been deleted \U0001F5D1", fg='green'))
    except AttributeError:
        click.echo(click.style("This list does not exist \U0001F625", fg='red'))


@main.command()
@click.option('-l', '--listname', help='The name of the list where you can add a task')
@click.argument('task')
def add_task(listname, task):
    _list = List.get_or_none(List.list_name == listname)
    try:
        task = Task.create(list_id=_list, desc=task)
        click.echo(click.style("Success! \U0001F44D", fg='green'))
    except AttributeError:
        click.echo(click.style('This list does not exist \U0001F625', fg='red'))
    except peewee.IntegrityError as e:
        click.echo(click.style('Error: ' + e, fg='red'))


@main.command()
@click.option('-l', '--listname', help='The name of the list where you can add a task')
def see_task_list(listname):
    _list = List.get_or_none(List.list_name == listname)
    try:
        table = []
        for task in _list.task:
            table.append([
                click.style(str(task.id), fg='blue'),
                click.style(task.desc, fg='green'),
                click.style(
                    '\U00002705' if task.state else '\U0000274C', fg='green')
            ])
        click.echo(tabulate(table, headers=[click.style('ID', fg='red'),
                                            click.style('Name', fg='red'),
                                            click.style('State', fg='red')]))
    except AttributeError:
        click.echo(click.style('This list does not exist \U0001F625', fg='red'))
    except peewee.IntegrityError as e:
        click.echo(click.style('Error: ' + e, fg='red'))


@main.command()
@click.option('-l', '--listname', help='The name of the list where you can add a task')
@click.argument('task_id')
def set_task_done(listname, task_id):
    """Set some task as done, use de id of task and task list name"""
    _list = List.get_or_none(List.list_name == listname)
    try:
        task = Task.select().where(Task.list_id == _list.id, Task.id == task_id).first()
        if task is None:
            click.echo(click.style('This task does not exist \U0001F625', fg='red'))
        task.state = True
        task.save()
        click.echo(click.style('Task done \U0001F44D', fg='green'))
    except AttributeError:
        click.echo(click.style('This list does not exist \U0001F625', fg='red'))


if __name__ == '__main__':
    main()
