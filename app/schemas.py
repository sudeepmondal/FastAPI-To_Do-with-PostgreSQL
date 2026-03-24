# ============================================================
# schemas.py - Pydantic models for request/response validation
# ============================================================

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ─────────────────────────────────────────
# USER SCHEMAS
# ─────────────────────────────────────────

class UserCreate(BaseModel):
    """Schema for registering a new user (request body)."""
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for returning user data (response body — no password)."""
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True  # Allows ORM model → Pydantic conversion


# ─────────────────────────────────────────
# AUTH SCHEMAS
# ─────────────────────────────────────────

class LoginRequest(BaseModel):
    """Schema for login request."""
    username: str
    password: str


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for decoded JWT payload."""
    username: Optional[str] = None


# ─────────────────────────────────────────
# TASK SCHEMAS
# ─────────────────────────────────────────

class TaskCreate(BaseModel):
    """Schema for creating a new task (request body)."""
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskUpdate(BaseModel):
    """Schema for updating a task (all fields optional)."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(BaseModel):
    """Schema for returning task data (response body)."""
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: Optional[datetime]
    user_id: int

    class Config:
        from_attributes = True


class PaginatedTaskResponse(BaseModel):
    """Schema for paginated task list response."""
    total: int
    page: int
    page_size: int
    tasks: list[TaskResponse]