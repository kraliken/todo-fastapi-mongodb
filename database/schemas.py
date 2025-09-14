from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

from database.models import Category, Priority, Status


class CreateTodoSchema(BaseModel):
    title: str = Field(..., min_length=3)
    description: Optional[str] = Field(default=None, min_length=3)
    category: Optional[Category] = None
    deadline: datetime
    priority: Optional[Priority] = None


class UpdateTodoSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=3)
    description: Optional[str] = Field(None, min_length=3)
    status: Optional[Status] = None
    category: Optional[Category] = None
    deadline: Optional[datetime] = None
    time_spent: Optional[timedelta] = None
    priority: Optional[Priority] = None


class ReadTodoSchema(BaseModel):
    id: str = Field(validation_alias="_id")
    title: str
    description: Optional[str] = None
    status: Status
    category: Category
    deadline: Optional[datetime] = None
    time_spent: Optional[timedelta] = None
    priority: Priority
    archived: bool
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(populate_by_name=True)


def doc_to_todo_out(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])

    if "time_spent" in doc and isinstance(doc["time_spent"], int):
        doc["time_spent"] = timedelta(seconds=doc["time_spent"])

    return doc
