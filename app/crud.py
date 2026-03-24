# ============================================================
# crud.py - All database operations (Create, Read, Update, Delete)
# ============================================================

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from fastapi import HTTPException, status

from app import models, schemas
from app.auth import hash_password


# ─────────────────────────────────────────
# USER CRUD
# ─────────────────────────────────────────

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """Fetch a user by their username."""
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Fetch a user by their email address."""
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Register a new user.
    - Checks for duplicate username/email before creating.
    - Hashes the password before saving.
    """
    # Check if username already taken
    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    # Check if email already taken
    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create the user with hashed password
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Load DB-generated fields (id, created_at)
    return db_user


# ─────────────────────────────────────────
# TASK CRUD
# ─────────────────────────────────────────

def get_tasks(
    db: Session,
    user_id: int,
    completed: Optional[bool] = None,
    page: int = 1,
    page_size: int = 10
) -> dict:
    """
    Get all tasks for a user with optional filtering and pagination.
    - completed: filter by True (done) or False (pending), or None (all)
    - page/page_size: pagination controls
    """
    query = db.query(models.Task).filter(models.Task.user_id == user_id)

    # Apply filter if provided
    if completed is not None:
        query = query.filter(models.Task.completed == completed)

    # Count total before pagination (for response metadata)
    total = query.count()

    # Apply pagination
    offset = (page - 1) * page_size
    tasks = query.order_by(models.Task.created_at.desc()).offset(offset).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "tasks": tasks
    }


def get_task_by_id(db: Session, task_id: int, user_id: int) -> models.Task:
    """
    Get a single task by ID — only if it belongs to the requesting user.
    Raises 404 if task not found or belongs to another user.
    """
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == user_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task


def create_task(db: Session, task: schemas.TaskCreate, user_id: int) -> models.Task:
    """Create a new task for the given user."""
    db_task = models.Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=user_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task_data: schemas.TaskUpdate, user_id: int) -> models.Task:
    """
    Update an existing task — only fields provided will be updated (PATCH-style).
    Raises 404 if the task doesn't exist or doesn't belong to the user.
    """
    db_task = get_task_by_id(db, task_id, user_id)

    # Only update fields that were actually sent in the request
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int, user_id: int) -> dict:
    """
    Delete a task by ID — only if it belongs to the requesting user.
    Raises 404 if not found.
    """
    db_task = get_task_by_id(db, task_id, user_id)
    db.delete(db_task)
    db.commit()
    return {"message": f"Task {task_id} deleted successfully"}