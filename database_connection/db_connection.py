#!usr/bin/env python

from datetime import datetime
import peewee

database = peewee.SqliteDatabase('todoCLI.db')


class BaseModel(peewee.Model):
    class Meta:
        database = database


class List(BaseModel):
    list_name = peewee.CharField(max_length=50, unique=True, null=True)
    creation_date = peewee.DateField(default=datetime.now())

    def __str__(self):
        return self.list_name

    class Meta:
        db_table = 'list'


class Task(BaseModel):
    list_id = peewee.ForeignKeyField(List, backref='task', on_delete='CASCADE')
    desc = peewee.CharField(max_length=200, null=False)
    state = peewee.BooleanField(default=False)

    def __str__(self):
        return '{} task for {} list'.format(self.desc, self.list_id)

    class Meta:
        db_table = 'task'
