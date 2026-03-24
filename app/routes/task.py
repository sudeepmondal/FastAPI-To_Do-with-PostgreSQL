# ============================================================
# routes/task.py - Task CRUD endpoints (protected by JWT auth)
# ============================================================

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app import schemas, crud, models
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# ─────────────────────────────────────────
# GET /tasks — List all tasks (with filter + pagination)
# ─────────────────────────────────────────

@router.get("/", response_model=schemas.PaginatedTaskResponse)
def get_tasks(
    completed: Optional[bool] = Query(None, description="Filter by completion status: true or false"),
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of tasks per page (max 100)"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Get all tasks for the logged-in user.
    - Optional filter: ?completed=true or ?completed=false
    - Pagination: ?page=1&page_size=10
    """
    return crud.get_tasks(
        db=db,
        user_id=current_user.id,
        completed=completed,
        page=page,
        page_size=page_size
    )


# ─────────────────────────────────────────
# POST /tasks — Create a new task
# ─────────────────────────────────────────

@router.post("/", response_model=schemas.TaskResponse, status_code=201)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Create a new task for the logged-in user.
    - title is required
    - description and completed are optional
    """
    return crud.create_task(db=db, task=task, user_id=current_user.id)


# ─────────────────────────────────────────
# PUT /tasks/{id} — Update an existing task
# ─────────────────────────────────────────

@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    task_data: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Update a task by ID.
    - Only the logged-in user's tasks can be updated
    - Only provided fields are updated (partial update)
    - Returns 404 if task not found
    """
    return crud.update_task(db=db, task_id=task_id, task_data=task_data, user_id=current_user.id)


# ─────────────────────────────────────────
# DELETE /tasks/{id} — Delete a task
# ─────────────────────────────────────────

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Delete a task by ID.
    - Only the logged-in user's tasks can be deleted
    - Returns 404 if task not found
    """
    return crud.delete_task(db=db, task_id=task_id, user_id=current_user.id)