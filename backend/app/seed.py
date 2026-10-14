from pathlib import Path

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import Diagnosis

SQL_FILE = Path(__file__).resolve().parent.parent / "sql" / "seed_icd10.sql"


def seed_diagnoses(db: Session):
    if db.query(Diagnosis).count() > 0:
        return

    db.execute(text(SQL_FILE.read_text(encoding="utf-8")))
    db.commit()
