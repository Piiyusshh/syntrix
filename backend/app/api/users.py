from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import (
    create_user,
    get_all_users,
    get_user_by_id,
    delete_user,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse, status_code=201)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_user(db, user)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/", response_model=list[UserResponse])
def read_users(
    db: Session = Depends(get_db)
):
    return get_all_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.delete("/{user_id}")
def remove_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = delete_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully"
    }