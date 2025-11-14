from sqlalchemy import Table, Column, Integer, ForeignKey
from .base import Base

# This is NOT a class model, it's a direct Table definition.
# This table connects Users and Tasks.
task_members_table = Table(
    'task_members',  # The name of the table in the database
    Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)