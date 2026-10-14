from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Consultation, Diagnosis, Doctor
from app.schemas import ConsultationCreate, ConsultationOut
from app.security import get_current_doctor

router = APIRouter(tags=["consultation"])


def _to_out(row: Consultation) -> ConsultationOut:
    return ConsultationOut(
        id=row.id,
        patient_name=row.patient_name,
        notes=row.notes,
        created_at=row.created_at,
        doctor_name=row.doctor.name if row.doctor else None,
        diagnoses=row.diagnoses,
    )


@router.post("/consultation", response_model=ConsultationOut, status_code=status.HTTP_201_CREATED)
def create_consultation(
    payload: ConsultationCreate,
    db: Session = Depends(get_db),
    doctor: Doctor = Depends(get_current_doctor),
):
    diagnoses = (
        db.query(Diagnosis)
        .filter(Diagnosis.code.in_(payload.diagnosis_codes))
        .all()
    )
    found = {d.code.upper() for d in diagnoses}
    missing = [c for c in payload.diagnosis_codes if c not in found]
    if missing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown diagnosis code(s): {', '.join(missing)}",
        )

    row = Consultation(
        patient_name=payload.patient_name,
        notes=payload.notes,
        doctor_id=doctor.id,
        diagnoses=diagnoses,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return _to_out(row)


@router.get("/consultation", response_model=list[ConsultationOut])
def list_consultations(
    patient: str = Query("", max_length=120),
    diagnosis: str = Query("", max_length=80),
    db: Session = Depends(get_db),
    _: Doctor = Depends(get_current_doctor),
):
    q = (
        db.query(Consultation)
        .options(joinedload(Consultation.diagnoses), joinedload(Consultation.doctor))
        .order_by(Consultation.created_at.desc())
    )

    patient_term = patient.strip()
    if patient_term:
        q = q.filter(Consultation.patient_name.ilike(f"%{patient_term}%"))

    dx_term = diagnosis.strip()
    if dx_term:
        like = f"%{dx_term}%"
        q = q.filter(
            Consultation.diagnoses.any(
                (Diagnosis.code.ilike(like)) | (Diagnosis.description.ilike(like))
            )
        )

    return [_to_out(row) for row in q.limit(200).all()]
