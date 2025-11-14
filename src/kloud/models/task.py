# src/kloud/models/task.py

import enum
from datetime import datetime, timedelta
from sqlalchemy import (
    Column, Integer, String, DateTime, Enum as DBEnum, Text,
    Interval, ForeignKey, Boolean
)
from sqlalchemy.orm import relationship

from .base import Base
from .user import User
from .association import task_members_table

class TaskPriority(enum.Enum):
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    NONE = 1

class TaskStatus(enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    WONT_DO = "wont_do"

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)

    owner_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    owner = relationship(
        "User",
        back_populates="created_tasks"
    )

    assigned_users = relationship(
        "User",
        secondary=task_members_table,  # Tell SQLAlchemy to use our bridge table
        back_populates="assigned_tasks"
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    title = Column(String(255), nullable=False)

    description_blocks = relationship(
        "ContentBlock",
        back_populates="task",
        order_by="ContentBlock.order",
        cascade="all, delete-orphan"  # If you delete a Task, delete all its blocks too
    )

    priority = Column(DBEnum(TaskPriority), default=TaskPriority.NONE, nullable=False)

    date = Column(DateTime, nullable=True)  # "When I want to start"
    duration = Column(Interval, nullable=True)    # "How long it will take (e.g., 1.5 hours)"
    deadline = Column(DateTime, nullable=True)    # "The final deadline"

    status = Column(DBEnum(TaskStatus), default=TaskStatus.TODO, nullable=False)

    # --- Your Sub-task feature (the recursive relationship) ---

    # This stores the ID of the task *above* this one.
    parent_id = Column(Integer, ForeignKey('tasks.id'), nullable=True)

    # This 'parent' attribute lets you access the parent task.
    parent = relationship("Task", remote_side=[id], back_populates="subtasks")

    # This 'subtasks' attribute gives you a list of all child tasks.
    subtasks = relationship("Task", back_populates="parent")

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status.value}')>"