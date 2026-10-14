from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import JWT_ALG, SECRET_KEY, TOKEN_EXPIRE_MINUTES
from app.database import get_db
from app.models import Doctor

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def create_token(email: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": email, "exp": exp}, SECRET_KEY, algorithm=JWT_ALG)


def get_current_doctor(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Doctor:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALG])
        email = payload.get("sub")
    except jwt.PyJWTError:
        email = None

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    doctor = db.query(Doctor).filter(Doctor.email == email).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return doctor
