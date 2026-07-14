from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.db.database import get_db
from app.schemas.user import Token, UserLogin
from app.services.user_service import get_user_by_email

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login", response_model=Token)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    db_user = get_user_by_email(db, user.email)

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": db_user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }