#!usr/bin/env python

from tabulate import tabulate
from datetime import datetime
from db_connection import database, List, Task
from colors import bcolors
import click
import peewee

MODELS = [ List, Task ]

@click.group()
def main():
    pass

@main.command()
def init():
    """Creates the tables and the database connection"""
    with database:
        database.create_tables(MODELS)
    print(bcolors.HEADER + 'TODO-cli ready to be useed')
    print("Use --help to get all possible commands")

@main.command()
@click.argument('list_name')
def create_list(list_name):
    """Create a new list"""
    print(bcolors.WARNING + 'You are about to create: ' +
          bcolors.OKBLUE + list_name)
    confirm = input(bcolors.WARNING + 'Continue? \U0001F914 (Y/N): ')
    if confirm != "N":
        try:
            List.create(list_name=list_name)
            print(bcolors.OKGREEN + "Success \U0001f44d")
        except peewee.IntegrityError:
            print(bcolors.FAIL + 'You already has a list with this name \U0001F616')

@main.command()
def get_all_list():
    """Get all list names"""
    for l in List.select():
        print(tabulate([[bcolors.OKGREEN + str(l.id),
                         bcolors.OKGREEN + l.list_name,
                         bcolors.OKGREEN + l.creation_date.strftime('%m/%d/%Y')]],
                         headers=[bcolors.HEADER + 'ID', bcolors.HEADER + 'Name', bcolors.HEADER + 'Creation date']))

if __name__ == '__main__':
    main()
