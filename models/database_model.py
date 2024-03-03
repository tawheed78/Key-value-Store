"""This module defines the database model."""
from pydantic import BaseModel


class KeyValueDb(BaseModel):
    """Model representing key-value pairs for the database."""
    key: str
    value: dict
