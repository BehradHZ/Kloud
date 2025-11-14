# src/kloud/models/content_block.py

import enum
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum as DBEnum
from sqlalchemy.orm import relationship

from .base import Base

class BlockType(enum.Enum):
    TEXT = "text"
    BULLET_POINT = "bullet_point"
    LINK = "link"
    FILE = "file"
    HEADING = "heading"


class ContentBlock(Base):
    __tablename__ = 'content_blocks'

    id = Column(Integer, primary_key=True)

    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)

    type = Column(DBEnum(BlockType), nullable=False, default=BlockType.TEXT)

    # The content (the text itself, a URL, or a file path)
    # We use Text for flexibility.
    content = Column(Text, nullable=True)

    # The order of this block in the description
    order = Column(Integer, nullable=False, default=0)

    # Relationship to get the parent task
    task = relationship("Task", back_populates="description_blocks")

    def __repr__(self):
        return f"<ContentBlock(id={self.id}, type='{self.type.name}', order={self.order})>"