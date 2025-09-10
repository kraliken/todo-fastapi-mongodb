from typing import List
from fastapi import APIRouter, HTTPException, Response, status
from database.models import Category, Priority, Status
from database.db_config import collection
from database.schemas import (
    CreateTodoSchema,
    ReadTodoSchema,
    UpdateTodoSchema,
    doc_to_todo_out,
)

from bson.objectid import ObjectId
from datetime import datetime, timezone
from pymongo import ReturnDocument


router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/", response_model=List[ReadTodoSchema], status_code=status.HTTP_200_OK)
async def get_all_todos():
    docs = collection.find({"archived": False})
    return [ReadTodoSchema(**doc_to_todo_out(d)) for d in docs]


@router.post("/", response_model=ReadTodoSchema, status_code=status.HTTP_201_CREATED)
async def create_todo(new_todo: CreateTodoSchema):
    try:
        now = datetime.now(timezone.utc)
        doc = {
            "title": new_todo.title,
            "description": new_todo.description,
            "status": Status.backlog,  # default
            "category": Category.work,  # default
            "priority": Priority.low,  # default
            "deadline": None,
            "archived": False,
            "created_at": now,  # default
            "updated_at": now,  # default
            "completed_at": None,
        }
        result = collection.insert_one(doc)
        doc = collection.find_one({"_id": result.inserted_id})

        print(doc)

        return ReadTodoSchema(**doc_to_todo_out(doc))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("/{todo_id}", response_model=ReadTodoSchema)
async def update_todo(todo_id: str, payload: UpdateTodoSchema):
    try:
        id = ObjectId(todo_id)
        existing_doc = collection.find_one({"_id": id})
        if not existing_doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo does not exits"
            )

        update_doc = payload.model_dump(exclude_unset=True)
        update_doc["updated_at"] = datetime.now(timezone.utc)

        updated = collection.find_one_and_update(
            {"_id": id},
            {"$set": update_doc},
            return_document=ReturnDocument.AFTER,
        )

        return ReadTodoSchema(**doc_to_todo_out(updated))

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occured {e}")


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_todo(todo_id: str):
    try:
        id = ObjectId(todo_id)
        existing_doc = collection.find_one({"_id": id})
        if not existing_doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo does not exits"
            )

        now = datetime.now(timezone.utc)
        collection.update_one(
            {"_id": id}, {"$set": {"archived": True, "updated_at": now}}
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occured {e}")
