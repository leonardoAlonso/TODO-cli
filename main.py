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
    for _list in List.select():
        click.echo(tabulate([[click.style(str(_list.id), fg='green'),
                              click.style(_list.list_name, fg='green'),
                              click.style(_list.creation_date.strftime('%m/%d/%Y'), fg='green')]],
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
    if not _list:
        click.echo(click.style("This list does not exist \U0001F625"), fg='red')
    _list.delete().execute()
    click.echo(click.style("The list has been deleted \U0001F5D1", fg='green'))


@main.command()
@click.option('-l', '--list', help='The name of the list where you can add a task')
@click.argumen('task_name')
def add_task(list, task_name):
    pass


if __name__ == '__main__':
    main()
