from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

# -------------------
# Password helpers
# -------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# -------------------
# TEMP auth dependency
# -------------------
def get_current_user(
    request,
    db: Session = Depends(get_db),
):
    """
    Temporary auth handler.
    Later replace with JWT.
    """
    user = db.query(models.User).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No users found. Please create admin user."
        )

    return user
