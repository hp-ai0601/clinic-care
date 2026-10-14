from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Doctor
from app.security import create_token, get_current_doctor, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginIn(BaseModel):
    email: str = Field(..., min_length=3, max_length=120)
    password: str = Field(..., min_length=6, max_length=128)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class DoctorOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.email == payload.email.strip().lower()).first()
    if not doctor or not verify_password(payload.password, doctor.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return TokenOut(access_token=create_token(doctor.email))


@router.get("/me", response_model=DoctorOut)
def me(doctor: Doctor = Depends(get_current_doctor)):
    return doctor
