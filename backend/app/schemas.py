from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class DiagnosisOut(BaseModel):
    id: int
    code: str
    description: str

    class Config:
        from_attributes = True


class ConsultationCreate(BaseModel):
    patient_name: str = Field(..., min_length=2, max_length=120)
    notes: str = Field(..., min_length=3, max_length=8000)
    diagnosis_codes: List[str] = Field(..., min_length=1, max_length=20)

    @field_validator("patient_name", "notes")
    @classmethod
    def strip_text(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("cannot be empty")
        return v

    @field_validator("diagnosis_codes")
    @classmethod
    def normalize_codes(cls, codes: List[str]) -> List[str]:
        cleaned = []
        seen = set()
        for raw in codes:
            code = raw.strip().upper()
            if not code or code in seen:
                continue
            seen.add(code)
            cleaned.append(code)
        if not cleaned:
            raise ValueError("at least one diagnosis code is required")
        return cleaned


class ConsultationOut(BaseModel):
    id: int
    patient_name: str
    notes: str
    created_at: datetime
    doctor_name: Optional[str] = None
    diagnoses: List[DiagnosisOut]

    class Config:
        from_attributes = True
