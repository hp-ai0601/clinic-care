from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


consultation_diagnoses = Table(
    "consultation_diagnoses",
    Base.metadata,
    Column("consultation_id", Integer, ForeignKey("consultations.id", ondelete="CASCADE"), primary_key=True),
    Column("diagnosis_id", Integer, ForeignKey("diagnoses.id"), primary_key=True),
)


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    consultations = relationship("Consultation", back_populates="doctor")


class Diagnosis(Base):
    __tablename__ = "diagnoses"
    __table_args__ = (UniqueConstraint("code", name="uq_diagnosis_code"),)

    id = Column(Integer, primary_key=True)
    code = Column(String(16), nullable=False, index=True)
    description = Column(String(255), nullable=False)

    consultations = relationship(
        "Consultation",
        secondary=consultation_diagnoses,
        back_populates="diagnoses",
    )


class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True)
    patient_name = Column(String(120), nullable=False, index=True)
    notes = Column(Text, nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    doctor = relationship("Doctor", back_populates="consultations")
    diagnoses = relationship(
        "Diagnosis",
        secondary=consultation_diagnoses,
        back_populates="consultations",
    )
