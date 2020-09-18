#!usr/bin/env python
import click
from db_connection import database, List, Task
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

@main.command()
@click.argument('list_name')
def create_list(list_name):
    """Create a new list"""
    print("Estas a punto de crear la lista: ", list_name)
    confirm = input("Deseas continuar (Y/N): ")
    if confirm == "Y":
        try:
            lista = List.create(list_name=list_name)
            print("Lista creada :)")
        except peewee.IntegrityError as e:
            print("Upps ya existe una lista con ese nombre :(")

if __name__ == '__main__':
    main()