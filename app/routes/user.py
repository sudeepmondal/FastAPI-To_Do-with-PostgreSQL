# ============================================================
# routes/user.py - User registration and login endpoints
# ============================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app import schemas, crud, models
from app.database import get_db
from app.auth import (
    verify_password,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(tags=["Authentication"])


# ─────────────────────────────────────────
# POST /register
# ─────────────────────────────────────────

@router.post("/register", response_model=schemas.UserResponse, status_code=201)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    - Validates unique username and email
    - Hashes password before storing
    - Returns created user (without password)
    """
    return crud.create_user(db=db, user=user)


# ─────────────────────────────────────────
# POST /login
# ─────────────────────────────────────────

@router.post("/login", response_model=schemas.Token)
def login(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    """
    Login with username and password.
    - Verifies credentials
    - Returns a JWT access token on success
    """
    # Find user by username
    user = crud.get_user_by_username(db, login_data.username)

    # Check user exists and password is correct
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token with username as the subject
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token, "token_type": "bearer"}


# ─────────────────────────────────────────
# GET /me (optional: see current user info)
# ─────────────────────────────────────────

@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    """
    Get the currently authenticated user's profile.
    Requires a valid JWT token.
    """
    return current_user