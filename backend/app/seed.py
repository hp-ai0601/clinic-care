from pathlib import Path

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import Consultation, Diagnosis, Doctor
from app.security import hash_password

SQL_FILE = Path(__file__).resolve().parent.parent / "sql" / "seed_icd10.sql"

DEMO_EMAIL = "lan@clinic.local"
DEMO_PASSWORD = "clinic123"


def seed_diagnoses(db: Session):
    if db.query(Diagnosis).count() > 0:
        return
    db.execute(text(SQL_FILE.read_text(encoding="utf-8")))
    db.commit()


def seed_demo_doctor(db: Session) -> Doctor:
    doctor = db.query(Doctor).filter(Doctor.email == DEMO_EMAIL).first()
    if doctor:
        return doctor
    doctor = Doctor(
        name="Dr. Lan Pham",
        email=DEMO_EMAIL,
        password_hash=hash_password(DEMO_PASSWORD),
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


def seed_sample_notes(db: Session, doctor: Doctor):
    if db.query(Consultation).count() > 0:
        return

    def dx(*codes):
        return db.query(Diagnosis).filter(Diagnosis.code.in_(codes)).all()

    samples = [
        Consultation(
            patient_name="Nguyen Van Minh",
            notes="BP 148/92. Continue amlodipine 5mg daily, lifestyle advice, review in 4 weeks.",
            doctor_id=doctor.id,
            diagnoses=dx("I10", "E78.5"),
        ),
        Consultation(
            patient_name="Tran Thi Hoa",
            notes="Type 2 DM, HbA1c 7.8%. Increase metformin to 1000mg BID. Recheck labs in 3 months.",
            doctor_id=doctor.id,
            diagnoses=dx("E11.9"),
        ),
        Consultation(
            patient_name="Le Duc Anh",
            notes="Mechanical LBP after lifting. NSAID + stretching. No red flags. Follow up if not improving.",
            doctor_id=doctor.id,
            diagnoses=dx("M54.5"),
        ),
    ]
    db.add_all(samples)
    db.commit()


def seed_all(db: Session):
    seed_diagnoses(db)
    doctor = seed_demo_doctor(db)
    seed_sample_notes(db, doctor)
