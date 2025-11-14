from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    __tablename__ = 'users'

    # TODO: check the fields
    # TODO: add support for login with Google

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String, nullable=False) # For security

    # --- Relationships ---

    # 1. Tasks this user OWNS (One-to-Many)
    created_tasks = relationship(
        "Task",
        back_populates="owner"
    )


    # 2. Tasks this user is a MEMBER OF (Many-to-Many)
    assigned_tasks = relationship(
        "Task",
        secondary="task_members", # This is the name of our association table
        back_populates="assigned_users"
    )

    # TODO: add lists and folders

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"