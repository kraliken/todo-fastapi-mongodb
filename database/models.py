from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class Status(str, Enum):
    backlog = "backlog"
    progress = "progress"
    done = "done"


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Todo(BaseModel):
    title: str = Field(..., min_length=3)
    description: Optional[str] = Field(default=None, min_length=3)
    status: Status = Field(default=Status.backlog)
    priority: Priority = Field(default=Priority.low)
    deadline: Optional[datetime] = None
    archived: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
