from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Diagnosis, Doctor
from app.schemas import DiagnosisOut
from app.security import get_current_doctor

router = APIRouter(tags=["diagnosis"])


@router.get("/diagnosis", response_model=list[DiagnosisOut])
def search_diagnosis(
    search: str = Query("", max_length=80),
    db: Session = Depends(get_db),
    _: Doctor = Depends(get_current_doctor),
):
    q = db.query(Diagnosis).order_by(Diagnosis.code)
    term = search.strip()
    if term:
        like = f"%{term}%"
        q = q.filter(
            or_(
                Diagnosis.code.ilike(like),
                Diagnosis.description.ilike(like),
            )
        )
    return q.limit(25).all()
