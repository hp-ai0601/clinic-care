# ClinicCare Mini EMR

Doctors can look up ICD-10 codes, write a consultation note, and search past notes by patient or diagnosis.

## Run locally

API (port 8000):

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

UI (port 3000):

```bash
cd frontend
npm install
npm run dev
```

Then open http://localhost:3000

Demo login: `lan@clinic.local` / `clinic123`

## API

| Method | Path | Notes |
|---|---|---|
| POST | `/auth/login` | `{ email, password }` → JWT |
| GET | `/auth/me` | current doctor |
| GET | `/diagnosis?search=` | code or description, local table |
| POST | `/consultation` | body: `patient_name`, `notes`, `diagnosis_codes` |
| GET | `/consultation` | optional `patient`, `diagnosis` query params |

Swagger: http://127.0.0.1:8000/docs

## Data

- SQLite file is created on first API start (`backend/clinic.db`)
- 100 ICD-10-CM codes are loaded from `backend/sql/seed_icd10.sql` (from [ICD10Data](https://www.icd10data.com/ICD10CM/Codes))
- A few sample notes are inserted so the list is not empty

JWT on the clinical endpoints is included as the optional auth piece from the assignment.
