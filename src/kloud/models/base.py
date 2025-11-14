# src/kloud/models/base.py

from sqlalchemy.orm import declarative_base

# This Base is the central registry for all your tables.
# All your model classes will inherit from this.
Base = declarative_base()